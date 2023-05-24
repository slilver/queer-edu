# This is a sample Python script.

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import packages here.
import PyPDF2 # for reading pdfs
import re # regex

import os # for opening directories

import csv
import string


def print_hi(name):
    """Function that prints simple friendly text."""
    print('Hi', name, '!')


def codes_of_interest():
    """Extract codes of interest from the data of interest spreadsheet.
    Return the codes in an array of strings."""
    with open('..\\Data_of_interest_csv.csv') as file:
        reader = csv.reader(file)
        columns = list(zip(*reader)) # zip makes iterable version of *reader, where * transposes
        codes = list(columns[2])
        del codes[0] # remove column name
        del codes[0] # remove start date
        # remove trailing underscores from codes
        for index, code in enumerate(codes):
            codes[index] = code.strip('_')
        print(codes)
        return codes

def check_code(code):
    "Check if code is found within the codebooks and print results."
    directory = '..\\..\\HMS Data\\Codebooks\\'
    results = []
    for pdf in os.listdir(directory):
        if not pdf.endswith('.pdf'):
            continue
        # print(pdf)
        filename = '..\\..\\HMS Data\\Codebooks\\' + pdf
        reader = PyPDF2.PdfReader(filename)

        page_count = 1
        found = False
        for page in reader.pages:
            text = page.extract_text()
            res_search = re.search(code, text)
            if res_search is not None:
                found = True
                break
            page_count += 1

        if found:
            results.append(page_count)
        else:
            results.append('None')
    print(code + ':', results)


def data_extraction(filepath, column_titles):
    """Create a csv file with only data for the specified column titles.
    The string filepath must lead to a csv file."""
    with open(filepath, encoding = 'utf-8') as file:
        reader = csv.reader(file)
        columns = list(zip(*reader)) # zip makes iterable version of *reader, where * transposes

        columns = [col for col in columns if check_column_title(col, column_titles)]
    print(columns)
    #     ToDo: actually write to CSV file


def check_column_title(column, column_titles):
    """Return true if the title of column is indicated in column_titles."""
    column_title = column[0]
    good_column = False
    for title in column_titles:
        if title in column_title:
            good_column = True
            break
    return good_column

# Run script.
if __name__ == '__main__':
    codes = codes_of_interest()
    # check_code('fincur')
    # for code in codes:
    #     check_code(code)
    data_extraction('..\\..\\HMS Data\\Datasets\\2021_2022_HMS.csv', codes)
