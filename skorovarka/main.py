import argparse
from .process import process_directory, default_replacement_callback

def _main():
    pass

def main():
    parser = argparse.ArgumentParser(
        description='Speeds up creation of repos from templates (see readme)'
    )
    subparsers = parser.add_subparsers(help="sub-command help")
    parser_cook = subparsers.add_parser('cook', help="Cook a project.")
    parser_cook.add_argument(
        '-i', '--input', type=str, 
        help="Path to the template folder.")
    parser_cook.add_argument(
        '-r', '--recipe', type=str, 
        help="Path to the recipe YAML, containing hints.")
    parser_cook.add_argument(
        '-o', '--output', type=str,
        help="Output path where you want to put your project."
    )
    parser_cook.add_argument(
        '-lb', '--lines-before', type=int, default=4,
        help="Line window ahead of each substituted line."
    )
    parser_cook.add_argument(
        '-la', '--lines-after', type=int, default=4,
        help="Line window after each substituted line."
    )

    args = parser.parse_args()
    # `skvk cook --recipe "./Python/.svk-hints.yaml" --out "./MyProj"`.

    process_directory(
        args.input,
        args.output,
        default_replacement_callback,
        args.recipe
    )


if __name__ == "__main__":
    main()