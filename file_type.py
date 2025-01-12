import argparse

# Allowed values
VALID_LINE_ENDINGS = {'cr', 'lf', 'crlf', 'dos', 'unix'}
VALID_ENCODINGS = {'utf-8', 'ascii', 'windows-1252'}

def validate_conversion(value):
    """
    Validate and categorise the input value as line ending or encoding.
    """
    value = value.lower()  # Make it case-insensitive
    if value in VALID_LINE_ENDINGS:
        return ('line_ending', value)
    elif value in VALID_ENCODINGS:
        return ('encoding', value)
    else:
        raise argparse.ArgumentTypeError(f"Invalid value: '{value}'. Must be a valid line ending or encoding.")

def parse_conversion_args(conversion_args):
    """
    Parse and validate the -c arguments (one or two).
    """
    parsed_args = {'line_ending': None, 'encoding': None}
    for arg in conversion_args:
        category, value = validate_conversion(arg)
        if parsed_args[category] is not None:
            raise argparse.ArgumentTypeError(f"Duplicate {category}: '{value}'")
        parsed_args[category] = value

    if not parsed_args['line_ending'] and not parsed_args['encoding']:
        raise argparse.ArgumentTypeError("At least one valid line ending or encoding must be provided.")
    return parsed_args

# Argparse setup
parser = argparse.ArgumentParser(description="File conversion tool.")
parser.add_argument(
    '-c', '--convert', nargs='+', required=True,
    help="Specify the line ending (CR, LF, CRLF, DOS, Unix) and/or encoding (UTF-8, ASCII, Windows-1252).",
    type=str
)

# Parse arguments
args = parser.parse_args()
try:
    conversion_settings = parse_conversion_args(args.convert)
    print("Conversion Settings:", conversion_settings)
except argparse.ArgumentTypeError as e:
    parser.error(str(e))
