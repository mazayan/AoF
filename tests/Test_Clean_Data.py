#!/usr/bin/env python

import unittest
import aof.Clean_Data as Clean_Data

class TestCleanData(unittest.TestCase):

    def setUp(self):
        #Local paths to datasets
        county_dataset_path = '../data/County_Dataset.csv'
        opioid_overdose_dataset_path = '../data/Accidental_Drug_Related_Deaths__2012-June_2017.csv'
        self.opioid_data, self.county_data = Clean_Data.load_data(county_dataset_path, opioid_overdose_dataset_path)
        print("Setup")

    def tearDown(self):
        print("Teardown")

    def test_delete_rows(self):
        print("Test Delete Rows")
        self.assertNotIn('Date', Clean_Data.delete_columns(self.opioid_data, ['Date', 'CaseNumber']))
        self.assertNotIn('Race', Clean_Data.delete_columns(self.opioid_data, ['Sex', 'Residence County', 'Race']))
        self.assertNotIn('Town Name', Clean_Data.delete_columns(self.county_data, ['Year Established', 'Town Name']))
        self.assertIn('Oxycodone', Clean_Data.delete_columns(self.opioid_data, ['Heroin', 'Death State']))

    def test_remove_nulls(self):
        print("Test Remove Nulls")
        opioid_data_new = Clean_Data.remove_nulls(self.opioid_data, ['Sex', 'Age'])
        self.assertEqual(opioid_data_new['Sex'].isnull().sum().sum(), 0)
        county_data_new = Clean_Data.remove_nulls(self.county_data, ['Town Name'])
        self.assertEqual(county_data_new['Town Name'].isnull().sum().sum(), 0)

    def test_upper_values(self):
        print("Test Upper Values")
        county_data_new = Clean_Data.upper_values(self.county_data, ['County', 'Town Name'])
        self.assertEqual(county_data_new['County'].str.isupper().sum(), len(county_data_new))

    def test_create_dictionary(self):
        print("Test Create Dictionary")
        dictionary = Clean_Data.create_dictionary(self.county_data['Town Name'], self.county_data['County'])
        self.assertEqual(dictionary['Monroe'], 'Fairfield')
        self.assertEqual(dictionary['Trumbull'], 'Fairfield')

    def test_get_county_from_city(self):
        print("Test Get County from City")
        dictionary = Clean_Data.create_dictionary(self.county_data['Town Name'], self.county_data['County'])
        self.assertEqual(Clean_Data.get_county_from_city('Monroe', dictionary), 'Fairfield')
        self.assertEqual(Clean_Data.get_county_from_city('Test', dictionary), 'None')

    def test_remove_rows(self):
        print("Remove Rows")
        Clean_Data.remove_rows(self.opioid_data, 'Sex', 'F')
        self.assertNotIn('F', self.opioid_data['Sex'])
        Clean_Data.remove_rows(self.county_data, 'County', 'Fairfield')
        self.assertNotIn('Fairfield', self.county_data['County'])

    def test_encode_new_column(self):
        print("Test Encode New Column")
        new_opioid_data = Clean_Data.encode_new_columns(self.opioid_data, 'Sex', 'Sex Encode')
        self.assertIn(1, new_opioid_data['Sex'])

    def test_fill_county_data(self):
        print("Test Fill County Data")
        dictionary = Clean_Data.create_dictionary(self.county_data['Town Name'], self.county_data['County'])
        opioid_data_new = Clean_Data.fill_county_data(self.opioid_data, 'Residence City', 'Residence County', dictionary)
        self.assertNotIn("None", opioid_data_new)

    def test_reorder_columns(self):
        print("Test Reorder Columns")
        opioid_data_new = Clean_Data.reorder_columns(2, 1, 3, self.opioid_data)
        self.assertEqual(opioid_data_new.columns[0], "Race")


if __name__ == '__main__' or __name__ == 'main':
    unittest.main()