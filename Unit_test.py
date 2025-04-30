import unittest
import csv
import os
import sqlite3
from ELT import cleandata, loda_data  

class TestScriptFunctions(unittest.TestCase):

    def setUp(self):
        # Create a sample input CSV file
        self.inputfile = 'test_input.csv'
        self.outputfile = 'test_output.csv'
        self.dbfile = 'load.db'
        
        with open(self.inputfile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Column1', 'Column2', 'Column3', 'Column4', 
                             'Column5', 'Column6', 'Column7', 'Column8'])
            writer.writerow(['Data1', 'Data2', 'Data3', '', '', '', '', 'Data8'])
            writer.writerow(['Data1', 'Data2', 'Data3', '', '', 'Data6', '', ''])

    def test_cleandata(self):
        
        result = cleandata(self.inputfile, self.outputfile)
        self.assertEqual(result, "Cleaning completed successfully!")

        # Verify the output file contains the cleaned data
        with open(self.outputfile, 'r') as csvfile:
            rows = list(csv.reader(csvfile))
            self.assertEqual(len(rows), 1)  # Only one valid row should be included

    def test_loda_data(self):
        # Run the cleandata function first to generate cleaned data
        cleandata(self.inputfile, self.outputfile)

        loda_data()

        connection = sqlite3.connect(self.dbfile)
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='WFieres';")
        self.assertIsNotNone(cursor.fetchone())

        cursor.execute("SELECT COUNT(*) FROM WFieres;")
        count = cursor.fetchone()[0]
        self.assertGreater(count, 0)

        connection.close()

    def tearDown(self):
        # Clean up created files
        if os.path.exists(self.inputfile):
            os.remove(self.inputfile)
        if os.path.exists(self.outputfile):
            os.remove(self.outputfile)
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)

if __name__ == '__main__':
    unittest.main()
