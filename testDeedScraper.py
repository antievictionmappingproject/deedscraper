#!/usr/bin/env python

import csv
import os
import unittest
import deedScraper as ds


class TestDeedScraperFunctions(unittest.TestCase):
    
    data = {'Image': '0151', 'Year': '2008', 'DocumentType': 'DEED', 'RecordDate': '06/25/2008', 'Document': 'I603689-00', 'Reel': 'J670'}

    parties = [('R', 'CUTLER ELEANOR D'), ('R', 'CUTLER ROBERT N'), ('E', 'CUTLER ELEANOR D'), ('E', 'CUTLER ROBERT N')]

    def test_get_attribute(self):
        self.assertEqual(ds.get_attribute([], 'r'), None)
        self.assertEqual(ds.get_attribute([('a', 'b'), ('c', 'd'), ('e', 'f')], 'c'), 'd')

    def test_parse_deed_list(self):
        with open('./testdata/test_deed_list_data', 'r') as f:
            urls = ds.parse_deed_list(f.read())
        
        self.assertEqual(urls, ['/cgi-bin/new_get_recorded.cgi?l_doc_ref_no=4624495&COUNTY=sanfrancisco&YEARSEGMENT=current&SEARCH_TYPE=DETAIL_N'])

    def test_parse_deed(self):
        with open('./testdata/test_deed_data', 'r') as f:
            data, parties = ds.parse_deed(f.read())

        self.assertEqual(data, TestDeedScraperFunctions.data)
        self.assertEqual(parties, TestDeedScraperFunctions.parties)

    def test_write_data(self):
        expected = [
            [ "2133A","002B","2008","I603689-00","06/25/2008","J670","0151","DEED","R","CUTLER ELEANOR D"   ],
            [ "2133A","002B","2008","I603689-00","06/25/2008","J670","0151","DEED","R","CUTLER ROBERT N"    ],
            [ "2133A","002B","2008","I603689-00","06/25/2008","J670","0151","DEED","E","CUTLER ELEANOR D"   ],
            [ "2133A","002B","2008","I603689-00","06/25/2008","J670","0151","DEED","E","CUTLER ROBERT N"    ]
        ]
        if os.path.isfile('./test_write_data.34324.out'):
            raise Exception('./test_write_data.34324.out file exists')

        with open('./test_write_data.34324.out', 'w', 0) as f:
            ds.write_data(f, '2133A', '002B', TestDeedScraperFunctions.data, TestDeedScraperFunctions.parties)  
        
        with open('./test_write_data.34324.out', 'r') as f:
            csv_reader = csv.reader(f)
            index = 0
            for row in csv_reader:
                self.assertEqual(row, expected[index])
                index += 1
       
        os.remove('./test_write_data.34324.out')      


if __name__ == '__main__':
    unittest.main()


