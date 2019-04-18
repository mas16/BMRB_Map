"""
Python 3.6

Script to clean BMRB NMR STAR Files and generate
SPARKY list file of amide N-H assignments for 2 dimensional
nitrogen - proton heteronuclear single quantum or multiple quantum
correlation spectra.

NOTE: This script will only work with NMR STAR files that are
version 3 or higher. Version 2 file support is not available at this time.

Data is read from a flat file then stored as a pandas data frame.

Required Libraries
----------------
pandas

----------------

Place the NMR STAR file in your working directory then set the following
user-define parameters:

Parameters
----------------
FILE_NAME - file name of the data file, including the file extension

CORRECTION - int value, factor to adjust amino acid sequence starting point

OUTPUT_NAME - file name of the output file, including the file extension

-----------------

by mas 2019
"""

# Import Libraries
import os
import pandas as pd
import sys

# Watermark
__title__ = "bmrb_map"
__author__ = "matt stetz"
__date__ = "17 April 2019"

##########################################
# User-Defined information below

# Name of NMR STAR file to clean (include extension)
FILE_NAME = "test.txt"

# Amino acid sequence start correction
CORRECTION = -1

# Name of output file (include extension)
OUTPUT_NAME = "output_test.list"

##########################################


# Functions
def check_file(filename=FILE_NAME):
    """
    Check if the file is located in the working directory.

    ----------------
    :param filename: str, FILE_NAME parameter set at top of script
    :return: None
    """
    directory = os.getcwd() + "/" + filename
    try:
        f = open(directory)
        f.close()
    except FileNotFoundError:
        print("Error: file not found!")
    else:
        read_file(directory)


def read_file(directory, nmrstar_entries=24):
    """
    Isolate the data relevant to N-H assignments from the NMR STAR file.
    Store data in pandas data frame.

    ----------------
    :param directory: str, file data path. set internally.
    :param nmrstar_entries: int, default is 24 based on NMR STAR v3 format.
    :return: None
    """
    # Use number label here, convert to str with map
    columns = list(map(str, range(nmrstar_entries)))
    df = pd.DataFrame(columns=columns)
    with open(directory, "r") as f:
        for index, row in enumerate(f):
            if len(row.split()) == nmrstar_entries and row.split()[1] == ".":
                df.loc[len(df)] = row.split()
    clean_df(df)


def clean_df(df, outputname=OUTPUT_NAME, correction=CORRECTION):
    """
    Clean up the relevant data. Isolate nitrogen and proton frequencies.
    Write SPARKY List file in proper format (include CRLF)

    :param df: pandas dataframe, set internally
    :param outputname: str, output file name set in parameters at top of script
    :param correction: int, value to adjust amino acid start site
    :return: None
    """
    # Split data frame into separate data frames. This way we can validate
    # if each residue has both a proton frequency and nitrogen frequency
    df_1h = df[df["7"] == "H"]
    df_15n = df[df["7"] == "N"]

    # Need to reset indexing to simplify subsequent iteration
    df_1h = df_1h.reset_index()
    df_15n = df_15n.reset_index()

    # Check to see if all data are there
    if df_1h.shape != df_15n.shape:
        print("Error: Assignment list is not complete!")
        sys.exit()

    directory = os.getcwd() + "/" + outputname

    with open(directory, "w") as f:
        f.write("{:>16} {:>10} {:>10} {:>1}".format("Assignment", "w1", "w2",
                                                    "\r\n"))
        f.write("\r\n")

        for index, row in df_1h.iterrows():

            # Check residue identity
            if (df_1h.loc[index, "6"] + df_1h.loc[index, "5"] ==
                    df_15n.loc[index, "6"] + df_15n.loc[index, "5"]):

                    f.write("{:>17} {:>10} {:>10} {:>1}".format(
                        df_1h.loc[index, "6"] +
                        str(int(df_1h.loc[index, "5"]) + correction) + "N-H",
                        df_15n.loc[index, "10"], df_1h.loc[index, "10"],
                        "\r\n"))

            else:
                print("Warning: Assignment Mismatch, skipping...")


if __name__ == '__main__':
    check_file()
