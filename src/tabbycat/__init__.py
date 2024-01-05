#!/usr/bin/python

"""
tabby - Tabulates and prints CSV and TSV data.

Copyright (c) 2024 - 2024 by Jahin Z. <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""


import tabulate, sys, argparse


def get_args():
    IS_OPTIONAL = "?"
    parser = argparse.ArgumentParser(
        "tabby", description="Tabulates and prints CSV and TSV data."
    )
    parser.add_argument(
        "file",
        help="name of input file, required in interactive use (i.e. nothing is in stdin).",
        type=argparse.FileType("r"),
        nargs=IS_OPTIONAL,
        const=None,
    )
    parser.add_argument(
        "-s",
        "--seperator",
        help="column seperator character (default: ',', or '\\t' if given a TSV file)",
    )
    parser.add_argument(
        "-e",
        "--header",
        help="apply special formatting to headers (default: none)",
        choices=["none", "bold", "dim", "seperated", "inverted"],
        default="none",
    )
    return parser.parse_args()


def get_seperator_character(seperator, file):
    if seperator is not None:
        return seperator
    elif file.name.endswith(".tsv"):
        return "\t"
    else:
        return ","


def get_input_stream(file):
    if not sys.stdin.isatty():
        return sys.stdin
    elif file is not None:
        return file
    else:
        print(
            "No input provided. Please provide a filename or a stream at stdin.",
            file=sys.stderr,
        )
        exit(1)


def format_header(table, header):
    if header == "none":
        return table
    # ANSI codes sourced from: https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
    BOLD = "\033[1m"
    DIM = "\033[2m"
    INVERTED = "\033[7m"
    RESET = "\033[0m"
    table_header, table_body = table[0], table[1:]
    if header == "seperated":
        seperators = ["-" * len(col) for col in table_header]
        return [table_header] + [seperators] + table_body
    format = RESET
    if header == "bold":
        format = BOLD
    if header == "dim":
        format = DIM
    if header == "inverted":
        format = INVERTED
    return [[f"{format}{col}{RESET}" for col in table_header]] + table_body


def main():
    args = get_args()
    input_stream = get_input_stream(args.file)
    seperator = get_seperator_character(args.seperator, input_stream)
    col_split = [line.strip() for line in input_stream]
    row_split = [line.split(seperator) for line in col_split]
    formatted = format_header(row_split, args.header)
    tabulated = tabulate.tabulate(formatted, tablefmt="plain")
    print(tabulated)


if __name__ == "__main__":
    main()
