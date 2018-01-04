#!/usr/bin/env python

import aof.Clean_Data as Clean_Data
import numpy as np
import aof.KNN as KNN

#Local paths to datasets
county_dataset_path = '/Users/Mazayan/IdeaProjects/AoF/data/County_Dataset.csv'
opioid_overdose_dataset_path = '/Users/Mazayan/IdeaProjects/AoF/data/Accidental_Drug_Related_Deaths__2012-June_2017.csv'

def clean_data(opioid_dataset, county_dataset):
    #columns to delete
    remove_cols_opioid = ['CaseNumber', 'Date', 'Race', 'Location', 'DescriptionofInjury', 'InjuryPlace',
                          'ImmediateCauseA', 'Fentanyl', 'Cocaine', 'Oxymorphone', 'EtOH', 'Hydrocodone',
                          'Benzodiazepine', 'Heroin', 'Amphet', 'Tramad', 'Morphine (not heroin)', 'Other',
                          'Any Opioid', 'MannerofDeath', 'AmendedMannerofDeath', 'DeathLoc', 'Death State',
                          'Death County', 'Death City', 'Residence State']

    remove_cols_county = ['History of incorporation', 'Year Established', 'Parent Town']

    opioid_dataset = Clean_Data.delete_columns(opioid_dataset, remove_cols_opioid)
    county_dataset = Clean_Data.delete_columns(county_dataset, remove_cols_county)

    #columns to remove nulls from
    remove_nulls_opioid = ['Residence City', 'Sex', 'Age']
    opioid_dataset = Clean_Data.remove_nulls(opioid_dataset, remove_nulls_opioid)

    #columns to UPPER
    upper_county = ['Town Name', 'County']
    county_dataset = Clean_Data.upper_values(county_dataset, upper_county)

    #create dictionary of county/town
    dic_keys = county_dataset['Town Name']
    dic_values = county_dataset['County']
    city_county_dict = Clean_Data.create_dictionary(dic_keys, dic_values)

    #replace null/unknown values with "None"
    opioid_dataset = opioid_dataset.replace(np.nan, "None")
    opioid_dataset = opioid_dataset.replace("UNKNOWN", "None")

    #remove rows where there is no residence city data
    opioid_dataset = Clean_Data.remove_rows(opioid_dataset, 'Residence City', "None")

    #replace blank county data with data pulled from dictionary
    opioid_dataset = Clean_Data.fill_county_data(opioid_dataset, 'Residence City', 'Residence County', city_county_dict)

    #remove rows that have no county data
    opioid_dataset = Clean_Data.remove_rows(opioid_dataset, 'Residence County', "None")

    return opioid_dataset


def convert_values(opioid_dataset):
    #encode Residence County column to int type
    opioid_dataset = Clean_Data.encode_new_columns(opioid_dataset, 'Residence County', 'Residence County Encode')

    #convert strings to binary for the below columns
    opioid_dataset['Methadone'] = opioid_dataset['Methadone'].replace("None", 0)
    opioid_dataset['Methadone'] = opioid_dataset['Methadone'].replace("Y", 1)
    opioid_dataset['Oxycodone'] = opioid_dataset['Oxycodone'].replace("None", 0)
    opioid_dataset['Oxycodone'] = opioid_dataset['Oxycodone'].replace("Y", 1)
    opioid_dataset['Sex'] = opioid_dataset['Sex'].replace("Female", 0)
    opioid_dataset['Sex'] = opioid_dataset['Sex'].replace("Male", 1)

    #create new column that analyzes type of opioid overdose
    def label_opioid(row):
        if row['Methadone'] == 0 and row['Oxycodone'] == 1:
            return 1
        if row['Methadone'] == 1 and row['Oxycodone'] == 1:
            return 2
        if row['Methadone'] == 1 and row['Oxycodone'] == 0:
            return 3
        else:
            return 0

    opioid_dataset['Opioid Type'] = opioid_dataset.apply(label_opioid, axis=1)

    #cast age column to int
    opioid_dataset['Age'] = opioid_dataset['Age'].astype('int64')

    return opioid_dataset

def main():
    #load data
    opioid_overdose_data, county_data = Clean_Data.load_data(county_dataset_path, opioid_overdose_dataset_path)

    #clean data
    opioid_overdose_data = clean_data(opioid_overdose_data, county_data)

    #convert Values
    opioid_overdose_data = convert_values(opioid_overdose_data)

    #reorder columns
    opioid_overdose_data = Clean_Data.reorder_columns(-2, 1, 4, opioid_overdose_data)

    print(opioid_overdose_data.head())

    x_features = KNN.get_x_features(opioid_overdose_data)

    #KNN.knn(opioid_overdose_data, x_features)
    KNN.k_nearest_neighbors(opioid_overdose_data, x_features)


main()