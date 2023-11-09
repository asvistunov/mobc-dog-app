import argparse

from pathlib import Path

parser = argparse.ArgumentParser(description='App to parse GitHub path.\nReturns a name of parent dir on GitHub.')

parser.add_argument('path', type=str, help='URL to GitHub repository.')

parser.add_argument('--output-file', type=str, help='File to save dir into.')


args = parser.parse_args()

print(args)

with open(args.output_file, 'w') as file:
    file.write(Path(args.path).stem)