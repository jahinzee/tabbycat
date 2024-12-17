#!/usr/bin/python

"""
tabby - Tabulates and prints CSV and TSV data.

Copyright (c) 2024 - 2024 by Jahin Z. <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import re
import csv
import typing
import signal
import sys

from re import Pattern
from argparse import ArgumentParser, Namespace, FileType
from typing import Optional, Literal, Final
from io import TextIOWrapper

signal.signal(signal.SIGINT, (lambda _a, _b: sys.exit(0)))

HeaderFormat = Literal["none", "bold", "dim", "underline", "inverted"]


ANSI_REGEX: Final[Pattern] = re.compile("\\x1b\\[\\dm")


def get_args() -> Namespace:
    parser = ArgumentParser(
        "tabby", description="Tabulates and prints CSV and TSV data."
    )
    parser.add_argument(
        "-s",
        "--separator",
        help=(
            "column separator character, "
            "defaults to ',' or '\\t', depending on input file"
        ),
    )
    parser.add_argument(
        "-e",
        "--header",
        help="apply special formatting to headers, defaults to none.",
        choices=list(typing.get_args(HeaderFormat)),
        default="none",
    )
    parser.add_argument(
        "file",
        help="name of input files, uses stdin if empty.",
        metavar="FILE",
        nargs="?",
        type=FileType("r"),
        default=sys.stdin,
    )

    return parser.parse_args()


def get_separator_character(file: TextIOWrapper, override: Optional[str] = None) -> str:
    if override is not None:
        return override
    if file.name.endswith(".tsv"):
        return "\t"
    return ","


def get_ansi_code_padding_bias(string: str) -> int:
    return len(re.findall(ANSI_REGEX, string)) * 4


def format_header(header: list[str], header_format: HeaderFormat) -> list[str]:
    ANSI_CODES = {
        # ANSI codes sourced from:
        # https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
        "none": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "underline": "\033[4m",
        "inverted": "\033[7m",
    }

    fmt, reset = ANSI_CODES[header_format], ANSI_CODES["none"]
    header = [f"{fmt}{col}{reset}" for col in header]

    return header


def main():
    args = get_args()
    table = list(
        csv.reader(
            args.file,
            delimiter=get_separator_character(args.file, override=args.separator),
        )
    )

    # Apply ANSI formatting to header, if specified by args.
    header, body = format_header(table[0], header_format=args.header), table[1:]
    table = [header] + body

    # Transpose table. -- table[row][col] → table[col][row]
    table = list(zip(*table))  # type:ignore

    # Find spacing value for each column, not counting ANSI codes.
    spacing = (
        max(len(row) - get_ansi_code_padding_bias(row) + 2 for row in col) + 1
        for col in table
    )

    # Pad and apply spacing value to each column, accounting for ANSI format
    # codes.
    spaced_columns = (
        [f"{cell:<{s+get_ansi_code_padding_bias(cell)}}" for cell in col]
        for s, col in zip(spacing, table)
    )

    # Re-transpose table. -- table[col][row] → table[row][col]
    table = zip(*spaced_columns)  # type:ignore

    ## Print rows.
    for row in table:
        print("".join(row))


if __name__ == "__main__":
    main()
