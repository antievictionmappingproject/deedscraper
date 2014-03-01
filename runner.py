#!/usr/bin/env python
import csv
import httplib, urllib
from time import sleep
import deedScraper as ds

#
# Ethics for running against www.criis.com
# 
# (1) Do not exceed more than 5 requests a second 
# (2) Try browsing the site whilst scraper is running - ensure it is still responsive
# (3) Do not run for more than 1 hour at a time
# (4) Run midnight - 1am - when load is low and outage will cause minimal inconvenience
# (5) Embed email address in case the admins wish to get in touch 
#

def main():
    input_file_name = './deed_scraper.in'
    output_file_name = './deed_scraper.out'

    conn = httplib.HTTPConnection("www.criis.com")

    with open(input_file_name, 'Ur') as input_file:
        csv_reader = csv.reader(input_file)

        with open(output_file_name, 'w', 0) as output_file:

            for row in csv_reader:
                # Throttle to ensure we do not overload website
                sleep(0.2)
                
                block = row[0]
                lot = row [1]

                print "Requesting data for Block: ", block, " Lot: ", lot

                document = ds.request_deed_list(conn, block, lot)
                urls = ds.parse_deed_list(document)
                
                for url in urls:
                    deed = ds.request_deed(conn, url)
                    data, parties = ds.parse_deed(deed)

                    print "Writing data for Block: ", block, " Lot: ", lot
                    ds.write_data(output_file, block, lot, data, parties)
    conn.close

if __name__ == '__main__':
    main()


