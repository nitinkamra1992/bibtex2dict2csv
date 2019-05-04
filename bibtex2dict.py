#! /usr/bin/python3

# System imports
import argparse
import os
import errno
import pickle

# Package imports
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode, author, editor, page_double_hyphen


################# Helper Methods #################


def create_directory(directory):
    ''' Creates a directory if it does not already exist.
    '''
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def customizations(record):
    ''' Use some customizations for bibtexparser

    Args:
        record: A record

    Returns:
        record: Customized record
    '''
    record = convert_to_unicode(record)
    # record = type(record)
    record = author(record)
    record = editor(record)
    # record = journal(record) # Do not use!
    # record = keyword(record)
    # record = link(record)
    record = page_double_hyphen(record)
    # record = doi(record)
    return record


def load_bibtex(bibpath, customizer=None):
    if os.path.isfile(bibpath):
        # Open and parse the BibTeX file in `bibpath` using `bibtexparser`
        if not bibpath.endswith(".bib"):
            print("INFO: Skipping {} - No .bib extension.".format(bibpath))
            return {}            
        else:
            bp = BibTexParser(open(bibpath, 'r').read(), customization=customizer)
            # Get a dictionary of dictionaries of key, value pairs from the
            # BibTeX file. The structure is {ID:{authors:...},ID:{authors:...}}.
            refsdict = bp.get_entry_dict()
            return refsdict
    elif os.path.isdir(bibpath):
        # Create a joint refsdict for all bibtex files inside this directory
        refsdict = {}
        for name in os.listdir(bibpath):
            # Recursively process all files and subdirectories
            inpath = os.path.join(bibpath, name)
            refdict = load_bibtex(inpath, customizer=customizer)
            refsdict.update(refdict)
        return refsdict


################# Bibtex2dict #################


def bibtex2dict(args):
    bib = args.bib
    outfile = args.outfile

    outdir = os.path.dirname(outfile)
    create_directory(outdir)

    # Initialize current_dict
    try:
        with open(outfile, 'rb') as outf:
            current_dict = pickle.load(outf)
    except:
        current_dict = {}

    # Extract all references from bib
    refs_dict = load_bibtex(bib, customizer=customizations)
    current_dict.update(refs_dict)

    # Write dict to file
    with open(outfile, 'wb') as outf:
        pickle.dump(current_dict, outf)


if __name__ == "__main__":
    # Generate argument parser
    parser = argparse.ArgumentParser(
        description="Convert a bibtex file or directory containing bibtex files to a pickled dictionary.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Add and parse arguments
    parser.add_argument("-b", "--bib",
        help="Path to the BibTeX file or directory containing BibTeX files.")
    parser.add_argument("-o", "--outfile",
        help="Path for the output pickle file. If the file already exists, it is assumed to contain a dictionary and is updated with the contents of the dictionary generated from the input bibtex/(s).")
    args = parser.parse_args()

    # Generate pickled dictionary from bib file/(s)
    bibtex2dict(args)
