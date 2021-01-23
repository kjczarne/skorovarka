# Skorovarka

Skorovarka takes a template project and prompts you to fill in the gaps via command line. It prepares the most basic files for you, so you don't need to fill everything out manually. It is compatible with two types of syntax:

* `${1:label}` or `$1` -> the VSCode snippets syntax
* `|||1:label|||` or `|||1|||` -> because it's rare that a triple pipe is an actual syntactical feature of any language and thus is more resistant to situations where the `${}` notation might not be suitable (e.g. Bash scripts).

## Usage

1. Run `skvk cook --input "./Python" --output "./MyProj"`.
2. Fill in the values when you're asked.

## Recipe file

A recipie file contains hints on what the fields being filled in actually mean. This file is optional but when you provide it, it should be in the form of:

```yaml
tox.ini:
  - Resources File YAML Path
  - Coverage options and adapter to run tests with
ALLOWED_EXTENSIONS:
  - all
```

All-caps fields are obligatory to be present.

* `ALLOWED_EXTENSIONS` -> optionally constrains the extensions being considered by the tool. If the first element of the list is `all` (or `ALL` or `aLL`, casing doesn't matter), all extensions will be allowed.

Remaining fields are Unix-style paths relative to the template folder directory (passed with `-i` flag), e.g. if `tox.ini` existed under `tests`, it should be named in the YAML: `tests/tox.ini`. Please don't use ugly Windows slashes in paths at least not in the recipe file.

Any future configuration will be extended via the recipe YAML.

To use the recipe file, provide a path to it via `--recipe` flag.

## To Do

[] Recipe modification -> `skvk recipe file.txt 4` -> changes label on tag `4` in `file.txt`.

# Caveats

* The tool doesn't support mixed-line-ending scenario. You either have a CRLF or an LF file. Period.