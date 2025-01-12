import argparse

VALID_LINE_ENDINGS = {'cr', 'lf', 'crlf', 'dos', 'unix'}
VALID_ENCODINGS = {'utf-8', 'ascii', 'windows-1252'}

def parse_conversion_args(conversion_args):
    parsed = {'line_ending': None, 'encoding': None}
    for arg in conversion_args:
        arg = arg.lower()
        if arg in VALID_LINE_ENDINGS:
            parsed['line_ending'] = arg
        elif arg in VALID_ENCODINGS:
            parsed['encoding'] = arg
        else:
            raise ValueError(f"Invalid conversion argument: {arg}")
    return parsed

def convert_file(file_path, output_path, line_ending=None, from_encoding='utf-8', to_encoding='utf-8'):
    # Read file
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Decode content
    text = content.decode(from_encoding, errors='replace')
    
    # Convert line endings
    if line_ending:
        line_endings_map = {'cr': '\r', 'lf': '\n', 'crlf': '\r\n', 'dos': '\r\n', 'unix': '\n'}
        text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\n', line_endings_map[line_ending])
    
    # Write with target encoding
    with open(output_path, 'w', encoding=to_encoding) as f:
        f.write(text)

# Argument parsing
parser = argparse.ArgumentParser(description="File conversion tool")
parser.add_argument('file', help="Path to the file to be converted")
parser.add_argument('-c', '--convert', nargs='+', help="Optional: Line ending and/or encoding")
args = parser.parse_args()

# Parse -c arguments
conversion_settings = parse_conversion_args(args.convert) if args.convert else {}

# Perform conversion
output_file = "converted_" + args.file
convert_file(
    file_path=args.file,
    output_path=output_file,
    line_ending=conversion_settings.get('line_ending'),
    to_encoding=conversion_settings.get('encoding')
)
print(f"File converted successfully: {output_file}")
