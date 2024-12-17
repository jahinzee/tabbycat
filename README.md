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
usage: tabby [-h] [-s SEPERATOR] [-e {none,bold,dim,seperated,inverted}]
             [file]

positional arguments:
  file                  name of input file, required in interactive use (i.e.
                        nothing is in stdin).

options:
  -h, --help            show this help message and exit
  -s SEPERATOR, --seperator SEPERATOR
                        column seperator character (default: ',', or '\t' if
                        given a TSV file)
  -e {none,bold,dim,seperated,inverted}, --header {none,bold,dim,seperated,inverted}
                        apply special formatting to headers (default: none)
```
