from logging import warning
import re
from typing import Callable, List, Tuple, Dict
from itertools import chain
from .parse_yaml import parse_yaml
from copy import copy
import os
import warnings

def walk_and_prompt(recipe_dir: str, output_dir: str):
    pass

def is_crlf(file_str: str) -> bool:
    if file_str.find("\r\n") != -1:
        return True
    return False


def is_lf(file_str: str) -> bool:
    if file_str.find("\n") != -1:
        return True
    return False


# def try_get_lines(
#     lines: List[str],
#     index: int,
#     lines_before: int,
#     lines_after: int
# ) -> Tuple[List[str], str, List[str]]:
#     offset_left: int = index - lines_before
#     offset_right: int = index + lines_after + 1
#     maximum: int = len(lines)
#     if offset_left < 0:
#         if offset_right > maximum:
#             return lines[0 : maximum], None, None
#         else:
#             return lines[0 : index], lines[index], lines[index + 1 : offset_right]
#     else:
#         if offset_right > maximum:
#             return lines[offset_left : index], lines[index], lines[index + 1 : maximum]
#         else:
#             return lines[offset_left : index], lines[index], lines[index + 1 : offset_right]

"""
PATTERN VARIANTS:

**vscode variant**:
Match small pattern: \$\d+
Match whole pattern: \$\{\d+:.+\}
Match default label: (?!\$)(?!\{)(?!\d+)(?!:).+(?=\})
Match numeric label: (?<=\{)\d+(?=:|\})|\$\d+

**custom variant**:
Match small pattern: \|{3}\d+\|{3}
Match whole pattern: (\|{3}\d+:)(.+)(\|{3})
Match default label: (?<=\|){3}(?!\d+)(?!:)(.+)(?=\|{3})
Match numeric label: (?<=\|{3})\d+(?=:|\|{3})

Matching the default label should happen
on the output of the matched top-level pattern.
Same applies for the numeric label

"""

PATTERNS_SMALL = {
    "var1": r'\$\d+',
    "var2": r'\|{3}\d+\|{3}'
}

PATTERNS_EXTENDED_WHOLE = {
    "var1": r'\$\{\d+:.+?\}',
    "var2": r'(\|{3}\d+:)(.+?)(\|{3})'
}

PATTERNS_EXTENDED_LABEL = {
    "var1": r'(?!\$)(?!\{)(?!\d+)(?!:).+(?=\})',
    "var2": r'(?!\|){3}(?!\d+)(?!:)(.+)(?=\|{3})'
}

PATTERNS_NUMERIC_LABEL = {
    "var1": r'(?<=\{)\d+(?=:|\})|\$\d+',
    "var2": r'(?<=\|{3})\d+(?=:|\|{3})'
}


def _repl_token_closure(
    input: str, 
    index: int,
    patterns_s: Dict[str, str],
    patterns_ext: Dict[str, str],
    patterns_ext_label: Dict[str, str],
    patterns_num_label: Dict[str, str],
    repl_callback: Callable[[str, str], str],
    lookup: Dict[str, str],
    hints: List[str]
) -> str:
    c_input = copy(input)
    for p in chain(patterns_s.values(), patterns_ext.values()):
        m = re.search(p, input)
        repl = None
        if m:
            print(f"Line {index}: {input}\n")
            label = ""
            for p2 in patterns_ext_label.values():
                m2 = re.search(p2, m.group())
                if m2:
                    label = m2.group()
            for p3 in patterns_num_label.values():
                m3 = re.search(p3, m.group())
                if m3:
                    if hints:
                        try:
                            print(f"HINT: {hints[int(m3.group())-1]}")
                        except IndexError:
                            pass
                    # FIXME: Windows slash??
                    try:
                        repl = lookup[m3.group()]
                    except KeyError:
                        repl = repl_callback(label, m3.group()).replace("\\", "\\\\")
                        lookup[m3.group()] = repl
        if repl:
            c_input = re.sub(p, repl, c_input)
    return c_input


def replace_token(
    input: str, 
    index: int,
    repl_callback: Callable[[str, str], str],
    lookup: Dict[str, str],
    hints: List[str]
) -> str:
    return _repl_token_closure(
        input, 
        index,
        PATTERNS_SMALL,
        PATTERNS_EXTENDED_WHOLE,
        PATTERNS_EXTENDED_LABEL,
        PATTERNS_NUMERIC_LABEL,
        repl_callback,
        lookup,
        hints
    )


def replace_tokens(
    file_str: str, 
    newline_symbol: str,
    repl_callback: Callable[[str, str], str],
    hints: List[str]
) -> str:
    if newline_symbol in ["\r\n", "\n"]:
        lines = file_str.split(newline_symbol)  # split on newline
    else:
        # assumming the file is one-line or empty
        lines = file_str
    lookup: Dict[str, str] = dict()
    filled_in_lines = []
    for idx, line in enumerate(lines):
        filled_in_line = replace_token(line, idx, repl_callback, lookup, hints)
        filled_in_lines.append(filled_in_line)
    return newline_symbol.join(filled_in_lines)


# def default_line_display_handler(
#     current_line: str,
#     current_line_idx: int,
#     lines_before: List[str], 
#     lines_after: List[str], 
#     newline_symbol: str
# ):
#     for i, l in zip(range(len(lines_before)-1, -1, -1), lines_before):
#         print(str(current_line_idx - i) + " |" + l)
#     print(str(current_line_idx) + " |" + current_line)
#     for i, l in enumerate(lines_after):
#         print(str(current_line_idx + i) + " |" + l)


def default_replacement_callback(default_label: str=None, numeric_label: str=None) -> str:
    # hint = hint_lookup(numeric_label)
    hint = None
    not_done = True
    # TODO: hint handling!
    while not_done:
        if hint:
            print(f"LABEL: {numeric_label}; {hint}")
        else:
            print(f"LABEL: {numeric_label}")
        if default_label:
            print(f"Default value: {default_label} ||||| hit enter to use default.")
        stdin = input("Value: ")
        if len(stdin) > 0:
            not_done = False
            return stdin
        else:
            if default_label:
                not_done = False
                return default_label
            else:
                warnings.warn("This parameter needs a value!")
                not_done = True
            


def process_file(
    file_str: str, 
    repl_callback: Callable[[str, str], str],
    hints: List[str]
) -> str:
    if is_crlf(file_str):
        return replace_tokens(
            file_str, 
            "\r\n", 
            repl_callback,
            hints
        )
    elif is_lf(file_str):
        return replace_tokens(
            file_str,
            "\n", 
            repl_callback,
            hints
        )
    else:
        return replace_tokens(
            file_str,
            "", 
            repl_callback,
            hints
        )
        # raise Exception(
        #     "Line ending style not supported! " +\
        #     "Convert the file to CRLF or LF."
        # )


def process_directory(
    path: str, 
    destination: str,
    repl_callback: Callable[[str, str], str],
    hint_file_path: str=None
):

    def handle_file(file_path, hint_file):
        print(f"FILE: {file_path}")
        hint_query = ""
        for segment1, segment2 in zip(os.path.split(path), os.path.split(file_path)):
            if segment1 != segment2:
                hint_query = os.path.join(hint_query, segment2).replace("\\", "/")
        try:
            hints = hint_file[hint_query]
        except (KeyError, TypeError):
            hints = None
        with open(file_path, "r") as f:
            str_content = f.read()
        filename = os.path.split(file_path)[-1]
        filled_in_file = process_file(
            str_content,
            repl_callback,
            hints)
        if not os.path.exists(destination):
            os.makedirs(destination)
        if not os.path.isdir(destination):
            raise Exception("--out parameter should be a directory, not file!")
        with open(os.path.join(destination, filename), "w") as f:
            f.write(filled_in_file)
    
    hint_file: Dict[str, List[str]] = None
    allowed_extensions: List[str] = None
    if hint_file_path:
        hint_file = parse_yaml(hint_file_path)
    
        # load allowed extensions from the hint file:
        if not hint_file["ALLOWED_EXTENSIONS"][0].lower() == "all":
            allowed_extensions = []
            for ext in hint_file["ALLOWED_EXTENSIONS"]:
                allowed_extensions.append(ext.lower())
        # fill up allowed extensions based on the
        # extensions used in hints:
        for k in hint_file.keys():
            spl = k.split(".")
            if len(spl) > 1:
                allowed_extensions.append(spl[-1].lower())


    if os.path.isfile(path):
        handle_file(path, hint_file)
    
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for name in files:
                file_path = os.path.join(root, name)
                if allowed_extensions:
                    for ext in allowed_extensions:
                        if name.lower().endswith(ext):
                            handle_file(file_path, hint_file)
                else:
                    handle_file(file_path, hint_file)
    else:
        raise Exception(
            "The recipe path seems to be wrong. " + \
            "Make sure the project template location exists."
        )