Deedscraper
===========

Pulls details of property deeds for the sale of properties in the San Francisco city+county area from www.criis.com


Input file
----------

CSV file containing two columns

    * Block number
    * Lot number


Output file - deed_scraper.out
------------------------------

CSV file containing the following columns:

    * Block number
    * Lot number
    * Year
    * Record Date
    * Reel
    * Image
    * Document Type
    * Grantor/Grantee
    * Party

Output file - deed_scraper.err
------------------------------

CSV file with details of any block/lot numbers for which deeds could not be obtained

    * Block number
    * Lot number
    * Reason


Ethics for running
-------------------

Testing has shown that it takes about 0.7 sec to pull all the deed details for a block/lot. The total number of block/lot numbers is approximately 200K. Therefore, it will need to be run for approximately 39 hours.

It is absolutely essential that running deedScraper does not impact the operation of www.criss.com. The following precautions have/should be taken:

    * Browser details on each request contain an email address allowing www.criss.com to contact us in the event of problems.
    * The number of blocks/lot numbers has slowly been increased from 1 to 200 to 1000. The website www.criss.com has continued to remain responsive
    * Long runs (e.g. > 15 mins) should take place 12pm - 8am when load on the website will be low minimizing the impact
    * deedScraper has a throttle to slow down requests. Defaults 200ms delay per block/lot number. At the moment it seems that www.criis.com has   appropriate throttling in place and it is redundant.
    * Terms of use have been download from www.criss.com. No restrictions on automated downloads of data.




