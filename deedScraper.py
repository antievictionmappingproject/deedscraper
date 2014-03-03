#!/usr/bin/env python
import csv
from datetime import datetime 
import httplib, urllib
import sys
import time
import deedScraperLib as ds
import logging
import traceback

output_file_name    = './deed_scraper.out'
error_file_name     = './deed_scraper.err'  
throttle_default    = 200

def usage():
    print
    print 'Usage: ./deedScraper INPUT_FILENAME [THROTTLE]'
    print
    print 'INPUT_FILENAME is a CSV file with 2 columns - the first is block number and the second is lot number'
    print 'THROTTLE is time delay per request - defaults to ', throttle_default, 'ms'
    print 
    print 'Writes output file containing details of the deeds ', output_file_name
    print 'Writes error file containing block/lot numbers where deeds could not be obtained', error_file_name
    print
    print
    sys.exit(2)

def parse_commandline_arguments(argv):
    input_file = ''
    throttle = throttle_default

    try:
        if len(argv) != 1 and len(argv) != 2:
            usage()

        input_file = argv[0]

        if len(argv) == 2:
            throttle = float(argv[1])

    except Exception, e:
        print str(e)
        usage()

    return (input_file, throttle)


def main(argv):
    #logging.basicConfig(level=logging.INFO)

    website                       = 'www.criis.com'
    (input_file_name, throttle)   = parse_commandline_arguments(argv)

    print 'Throttle between requests ', throttle, 'ms'

    conn = httplib.HTTPConnection(website)
    print 'Connection to ', website, ' opened'

    row_count = 0
    start = datetime.now()

    try:
        with open(input_file_name, 'Ur') as input_file:
            csv_reader = csv.reader(input_file)
            print 'Input file: ', input_file_name, ' opened'

            with open(output_file_name, 'w', 0) as output_file:
                print 'Output file: ', output_file_name, ' opened'

                with open(error_file_name, 'w', 0) as error_file:
                    print 'Error file: ', error_file_name, ' opened'
                    csv_error_writer = csv.writer(error_file, quoting=csv.QUOTE_ALL)

                    for row in csv_reader:

                            try:
                                block = row[0]
                                lot = row [1]

                                row_count += 1

                                # Throttle to ensure we do not overload website
                                time.sleep(throttle / 1000.0)

                                print 'Requesting data for Block: ', block, ' Lot: ', lot

                                document = ds.request_deed_list(conn, block, lot)
                                urls = ds.parse_deed_list(document)

                                if len(urls) == 0:
                                    raise ds.DSException('Failed to find deeds')
                                
                                for url in urls:
                                    deed = ds.request_deed(conn, url)
                                    data, parties = ds.parse_deed(deed)

                                    if len(parties) == 0:
                                        raise ds.DSException(str.format('Failed to find parties for deed {}', url))

                                    print 'Writing data for Block: ', block, ' Lot: ', lot
                                    ds.write_data(output_file, block, lot, data, parties)
                            except ds.DSException, e:
                                logging.error('%s Block: %s Lot: %s', str(e), block, lot)
                                logging.info(traceback.format_exc())
                                csv_error_writer.writerow([block, lot, str(e)])
    finally:
        conn.close

    end = datetime.now()
    timetaken = end - start

    print row_count, ' block/lot requests processed' 
    print 'Time taken: ', timetaken.seconds, ' seconds ' 

if __name__ == '__main__':
    main(sys.argv[1:])


