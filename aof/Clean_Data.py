#!/usr/bin/env python

import pandas as pd

def load_data(county_dataset, opioid_overdose_dataset):
    #open dataset
    raw_county_data = open(county_dataset, 'rt')
    raw_opioid_overdose_data = open(opioid_overdose_dataset, 'rt')

    #read in csv files
    reader_county_data = pd.read_csv(raw_county_data)
    reader_opioid_overdose_data = pd.read_csv(raw_opioid_overdose_data)

    #create copies of the dataset you will be modifying
    reader_county_data_copy = reader_county_data.copy()
    reader_opioid_overdose_data_copy = reader_opioid_overdose_data.copy()
    return reader_opioid_overdose_data_copy, reader_county_data_copy

#delete unneeded columns from dataset
def delete_columns(dataset, columns):
    for i in columns:
        del dataset[i]
    return dataset

#remove rows from columns where records are null
def remove_nulls(dataset, columns):
    for i in columns:
        dataset = dataset.dropna(subset=[i])
    return dataset

#convert dataset columns to upper values
def upper_values(dataset, columns):
    for i in columns:
        dataset[i] = dataset[i].str.upper()
    return dataset

#create dictionary from two lists
def create_dictionary(keys, values):
    dictionary = dict(zip(keys, values))
    return dictionary

#create function to get county name from city name
def get_county_from_city(city, city_county_dict):
    county = city_county_dict.get(city)
    if county is not None:
        return county
    else:
        return "None"


#remove rows from dataset
def remove_rows(dataset, col, condition):
    output = dataset[dataset[col] != condition]
    return output

#replace blank county data with data pulled from dictionary
def fill_county_data(dataset, city_col, county_col, dictionary):
    for i, row in dataset.iterrows():
        if row[county_col] == "None":
            row[county_col] = row[county_col].replace("None", str(get_county_from_city(row[city_col], dictionary)))
    return dataset


#create new encoded columns from string columns
def encode_new_columns(dataset, original_col, new_col):
    dataset[new_col] = dataset[original_col].astype('category')
    dataset[new_col] = dataset[new_col].cat.codes
    return dataset

#reorder columns from dataset
#end_to_begin_cols = move columns from the end to the beginning
#col_range1/2 = specify which columns you want to start with through a range
def reorder_columns(end_to_begin_cols, col_range_1, col_range_2, reader_opioid_overdose_data_copy):
    cols = reader_opioid_overdose_data_copy.columns.tolist()
    cols = cols[end_to_begin_cols:] + cols[:end_to_begin_cols]
    cols = cols[col_range_1:col_range_2] + cols[:col_range_1] + cols[col_range_2:]
    reader_opioid_overdose_data_copy = reader_opioid_overdose_data_copy[cols]
    return reader_opioid_overdose_data_copy






