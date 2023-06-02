# This is a sample Python script.

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import packages here.
import PyPDF2 # for reading pdfs
import re # regex

import os # for opening directories

import csv
import string

import pandas as pd
from ydata_profiling import ProfileReport
import matplotlib.pyplot as plt


def codes_of_interest():
    """Extract codes of interest from the data of interest spreadsheet.
    Return the codes in an array of strings."""
    with open('..\\Data_of_interest2.csv') as file:
        reader = csv.reader(file)
        columns = list(zip(*reader)) # zip makes iterable version of *reader, where * transposes
        codes = list(columns[2])

        del codes[0] # remove header from codes
        # remove trailing underscores from codes
        for index, code in enumerate(codes):
           codes[index] = code.strip('_')

        codes = [code for code in codes if code]  # remove empty strings
        print(codes)
        return codes


def check_codes(codes, print_modules=False):
    """Report where each code in codes is found in each codebook,
    by modules if print_modules is True and by page otherwise (default)."""
    directory = '..\\..\\HMS Data\\Codebooks\\'

    report_order = []
    for filename in os.listdir(directory):  # print order of files for which reporting will occur
        if not filename.endswith('.pdf'):
            continue
        report_order.append(filename[-13:-4])  # collect year of file
    print(report_order)

    for code in codes:
        results = []
        for filename in os.listdir(directory):
            if not filename.endswith('.pdf'):
                continue

            if print_modules and filename.endswith('2021.pdf'):  # only do modules for 2020-2021 data
                continue
            reader = PyPDF2.PdfReader(directory + filename)

            page_number = 1
            found = False
            for page in reader.pages:
                text = page.extract_text()
                res_search = re.search(code, text)
                if res_search is not None:
                    found = True
                    break
                page_number += 1

            if not found:
                results.append('None')
            else:
                if print_modules:
                    def get_module(page_number):  # these page numbers are based on 2020-2021 codebook
                        if page_number in range(4, 44): return 1
                        if page_number in range(44, 66): return 2
                        if page_number in range(66, 82): return 3
                        if page_number in range(82, 88): return 4
                        if page_number in range(88, 93): return 5
                        if page_number in range(93, 100): return 6
                        if page_number in range(100, 113): return 7
                        if page_number in range(113, 125): return 8
                        if page_number in range(125, 131): return 9
                        if page_number in range(131, 136): return 10
                        if page_number in range(136, 140): return 11
                        if page_number in range(140, 175): return 12
                        if page_number in range(175, 178): return 13
                        if page_number in range(178, 182): return 14
                        if page_number in range(182, 189): return 15
                        if page_number in range(189, 193): return 16
                        if page_number in range(193, 201): return 17
                        if page_number in range(201, 111): return 18
                    results.append(get_module(page_number))
                else:  # print page number
                    results.append(page_number)
        print(code + ':', results)


def data_extraction(filepath, column_titles):
    """From the csv file at filepath, extract data with specified column titles.
    Write the extracted data to a new csv file in the same folder."""
    with open(filepath, encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file)
        columns = list(zip(*reader))  # zip makes iterable version of *reader, where * transposes

        columns = [col for col in columns if check_column_title(col, column_titles)]
    rows = zip(*columns)  # write column data to zip file for parsing, where * transposes
    write_filepath = filepath.removesuffix('.csv') + '_reduced.csv'
    new_file = open(write_filepath, 'w+', newline='', encoding='utf-8', errors='ignore')
        # utf-8 is most common encoding, but some files still have special chars so 'ignore' errors
    with new_file:
        writer = csv.writer(new_file)
        writer.writerows(rows)
    print('Wrote reduced csv file to', filepath)


def check_column_title(column, good_titles):
    """Return true if the title of column is indicated in column_titles."""
    column_title = column[0]
    good_column = False
    for good_title in good_titles:
        if good_title in column_title:
            good_column = True
            break
    return good_column


def chi_square(category1, category2):
    """Perform a chi square test on category 1 vs category 2.
    Return the p-value of the test."""

# Run script.
if __name__ == '__main__':

    directory = '..\\..\\HMS Data\\Datasets\\'
    codes = codes_of_interest()
    # check_codes(codes, False)

    # perform data extraction on all csv files in directory
    # csv_files = []
    # for filename in os.listdir(directory):
    #     if not filename.endswith('.csv'):
    #         continue
    #     csv_files.append(filename)
    # for filename in csv_files:
    #     data_extraction(directory + filename, codes)

    data_extraction(directory + "2019_2020_HMS_reduced.csv",
                    codes)

    # csv_files = []
    # for filename in os.listdir(directory):
    #     if not filename.endswith('reduced.csv'):
    #         continue
    #     csv_files.append(filename)
    # for filename in csv_files:
    #     dataframe = pd.read_csv(directory + filename, low_memory=False)
    #     # print(dataframe)
    #     # print(dataframe.dtypes)
    #     # print(dataframe.info())
    #     profile = ProfileReport(dataframe,
    #                             title="Pandas Profiling Report for " + filename.removesuffix('_HMS_reduced.csv'))
    #     profile.to_file(directory + filename.removesuffix('_HMS_reduced.csv'))


