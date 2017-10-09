import argparse
import sys

from openfisca_web_api_preview.scripts.serve import add_arguments, main as serve

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Available commands')
    parser_serve = subparsers.add_parser('serve', help='Run the OpenFisca Web API')
    parser_serve = add_arguments(parser_serve)

    args = parser.parse_args()
    sys.exit(serve(args))

if __name__ == '__main__':
    sys.exit(main())
