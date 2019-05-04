# bibtex2dict2csv

This repository provides tools to convert bibtex files into a dictionary or into a CSV with a few selected columns extracted. It comes with two tools:
1. **bibtex2dict**: Convert a bibtex file or directory containing bibtex files to a pickled dictionary.
2. **dict2csv**: Convert a pickle file containing a BibTeX references dictionary to a CSV file.

## Compatibility

The tool has been written for Ubuntu and tested on Python v3.5 and above but is also compatible with previous and newer versions of python3.

## Dependencies

Requires python3, the `argparse` and `csv` packages from Python Standard Library and the `bibtexparser` package (available via pip):

```
pip install bibtexparser
```

## Usage

The tools can be run as Python scripts, e.g.:
```bash
python3 bibtex2dict.py -b <bib> -o <outfile>
```

The following command-line arguments are required:
```
-b, --bib: Path to the BibTeX file or directory containing BibTeX files.
-o, --outfile: Path for the output pickle file. If the file already exists, it is assumed to contain a dictionary and is updated with the contents of the dictionary generated from the input bibtex/(s).
```

```bash
python3 dict2csv.py -d <dict> -o <outfile>
```

The following command-line arguments are required:
```
-d, --dict: Path to the pickle file containing BibTeX references dictionary.
-o, --outfile: Path for the output CSV file. If the file already exists, it is appended to.
```

## Example

For working examples, execute the following on the command-line:
```bash
python3 bibtex2dict.py -b example/biblio.bib -o example/biblio.pkl
python3 dict2csv.py -d example/biblio.pkl -o example/biblio.csv
```
The above uses the sample input file in the example folder. A copy of the generated output files (biblio.pkl and biblio.csv) is already present in the example folder for reference.
