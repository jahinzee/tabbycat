# tabbycat

Tabulates and prints CSV and TSV data.

Can read from either a given file, or from standard input.

## Installation

To install this script, use either pipx (recommended) or pip.

```sh
pipx install git+https://github.com/jahinzee/tabbycat.git
```

To uninstall, simply run `pipx uninstall tabbycat` or `pip uninstall tabbycat`.

Alternatively, you can download the `src/tabbycat/__init__.py` file from this repository, and run the script standalone.

## Usage

```txt
usage: tabby [-h] [-s SEPARATOR] [-e {none,bold,dim,underline,inverted}]
             [FILE]

Tabulates and prints CSV and TSV data.

positional arguments:
  FILE                  name of input files, uses stdin if empty.

options:
  -h, --help            show this help message and exit
  -s, --separator SEPARATOR
                        column separator character, defaults to ',' or '\t',
                        depending on input file
  -e, --header {none,bold,dim,underline,inverted}
                        apply special formatting to headers, defaults to none.

```
