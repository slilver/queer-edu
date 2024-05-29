# This is a sample Python script.

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import packages here.
import PyPDF2 # for reading pdfs
import re  # regex

import os  # for opening directories

import csv
import string  # for operations with strings

import pandas
from ydata_profiling import ProfileReport  # for data exploration and cleaning with ydata
import matplotlib.pyplot

from scipy.stats import chi2_contingency  # for chi square tests
import numpy as np


def check_keywords(keywords):
    """Report where each keyword in keywords is found (by page number) in each pdf."""
    directory = '..\\..\\Math 111 files\\HW\\'

    filename_order = []
    for filename in os.listdir(directory):  # print order of files for which reporting will occur
        if not filename.endswith('.pdf'):
            continue
        trunc_filename = filename.removesuffix('.pdf')
        trunc_filename = trunc_filename.removeprefix('Math111L_')
        filename_order.append(trunc_filename)  # collect truncated filenames
    print(filename_order)

    for keyword in keywords:
        results = []
        for filename in os.listdir(directory):

            if not filename.endswith('.pdf'):
                continue
            reader = PyPDF2.PdfReader(directory + filename)
            page_number = 1

            count = 0
            for page in reader.pages:  # search each page
                text = page.extract_text()
                res_search = re.findall(keyword, text)  # regex find all instances of keyword. TODO: spaces?
                count += len(res_search)  # record count of instances on this page
                page_number += 1
            results.append(count)  # record final count

        print(keyword + ':', results)

# Run script.
if __name__ == '__main__':

    check_keywords(['derivative', 'help', 'she', 'he', 'they', 'why'])

    print('111 script')

