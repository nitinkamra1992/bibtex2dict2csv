#! /usr/bin/python3

# System imports
import argparse
import os
import errno
import pickle
import csv


################# Helper Methods #################


def create_directory(directory):
    ''' Creates a directory if it does not already exist.
    '''
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def dict2rows(refs_dict):
    ''' Converts a bibtex reference dictionary to required CSV rows.
        Columns are: Title, Year, Tags, Group, URL, Venue, Notes.
        Only the Title and Year (optionally, also URL) are populated.
        The remaining are left empty.
    '''
    csv_rows = []
    for ref_id, ref_entry in refs_dict.items(): # Extract references
        row = ['' for _ in range(7)]
        # Extract fields from the reference
        row[0] = ref_entry['title']
        row[1] = ref_entry['year']
        if 'url' in ref_entry:
            row[4] = ref_entry['url']
        elif 'URL' in ref_entry:
            row[4] = ref_entry['URL']
        # Append row to csv_rows
        csv_rows.append(row)
    return csv_rows


################# Dict2csv #################


def dict2csv(args):
    infile = args.dict
    outfile = args.outfile

    outdir = os.path.dirname(outfile)
    create_directory(outdir)

    # Read refs_dict
    with open(infile, 'rb') as inf:
        refs_dict = pickle.load(inf)

    # Convert refs_dict to csv rows
    csv_rows = dict2rows(refs_dict)

    # Append csv rows to the csv file
    with open(outfile, 'a') as csvFile:
        writer = csv.writer(csvFile)
        for row in csv_rows:
            writer.writerow(row)


if __name__ == "__main__":
    # Generate argument parser
    parser = argparse.ArgumentParser(
        description="Convert a pickle file containing a BibTeX references dictionary to a CSV file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Add and parse arguments
    parser.add_argument("-d", "--dict",
        help="Path to the pickle file containing BibTeX references dictionary.")
    parser.add_argument("-o", "--outfile",
        help="Path for the output CSV file. If the file already exists, it is appended to.")
    args = parser.parse_args()

    # Generate csv from pickled dictionary
    dict2csv(args)
