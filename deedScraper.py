import httplib, urllib
import csv
from HTMLParser import HTMLParser

def request_deed_list(conn, block, lot):
    headers = {
        "Content-type": "application/x-www-form-urlencoded", 
        "Accept": "text/html",
        "User-Agent": "sararcher@outlook.com"
    }
    params = urllib.urlencode({
        "BLOCK": block, 
        "LOT": lot,
        "SEARCH_TYPE": "APN",
        "COUNTY": "sanfrancisco",
        "YEARSEGMENT": "current",
        "ORDER_TYPE": "Recorded+Official"
    })
    
    conn.request("POST", "/cgi-bin/new_get_recorded.cgi", params, headers)
    response = conn.getresponse()
    if response.status != 302:
        raise Exception("No redirect returned") 

    redirect_url = response.getheader("Location")

    conn.request("GET", redirect_url)
    response = conn.getresponse()
    if response.status != 200:
        raise Exception("Get request failed") 

    return response.read()
  

def get_attribute(list, attribute):
    for item in list:
        if item[0] == attribute:
            return item[1]
    return None


class DeedListParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_records_table = False
        self.record = -1
        self.column = -1
        self.data_row = False
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table' and get_attribute(attrs, 'class') == 'records': 
            self.in_records_table = True
            self.record = -1
            self.column = -1
        elif tag == 'tr':
            self.record +=1
            self.column = -1
        elif tag =='td':
            self.column += 1
        elif tag=='a' and self.in_records_table and self.column == 0:
            href = get_attribute(attrs, 'href')
            if href is not None:
                self.data_row = True
                self.data.append([href])
           
    def handle_endtag(self, tag):
        if tag == 'table' and self.in_records_table:
             self.in_records_table = False
        elif tag == 'tr':
            self.data_row = False

    def handle_data(self, data):
        data = data.rstrip()
        if self.data_row and self.column == 5 and data != '':
            self.data[len(self.data)-1].append(data)

    def get_urls(self): 
        return [u[0] for u in self.data if u[1] == 'DEED']

def parse_deed_list(data):
    parser = DeedListParser()
    parser.feed(data)
    urls = parser.get_urls()
    return urls

def request_deed(conn, url):
    conn.request("GET", url)
    response = conn.getresponse() 
    if response.status != 302:
        raise Exception("No redirect returned") 
    redirect_url = response.getheader("Location")

    conn.request("GET", redirect_url)
    response = conn.getresponse()
    if response.status != 200:
        raise Exception("Get request failed") 

    return response.read()

class DeedParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_records_table = False
        self.record = -1
        self.column = -1
        self.data_row = False
        self.in_font = False
        self.data = {}
        self.grantee = None
        self.column_to_field = { 0: 'Year', 1: 'Document', 2: 'RecordDate', 3: 'Reel', 4: 'Image', 6: 'DocumentType' }
        self.parties = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table' and get_attribute(attrs, 'class') == 'records': 
            self.in_records_table = True
            self.record = -1
            self.column = -1
        elif tag == 'tr':
            self.record +=1
            self.column = -1
        elif tag =='td':
            self.column += 1
        elif tag == 'font' and get_attribute(attrs, 'color') == None:
            self.in_font = True
           
    def handle_endtag(self, tag):
        if tag == 'table' and self.in_records_table:
             self.in_records_table = False
        elif tag == 'tr':
            self.data_row = False
        elif tag == 'font':
            self.in_font = False

    def handle_data(self, data):
        if self.in_records_table and self.in_font:
            if self.column in self.column_to_field:
                self.data[self.column_to_field[self.column]] = data
            elif self.column == 10:
                self.grantee = data
            elif self.column == 13:
                self.parties.append((self.grantee, data)) 

def parse_deed(data):
    parser = DeedParser()
    parser.feed(data)
    return (parser.data, parser.parties)

def write_data(file_obj, block, lot, data, parties):
    writer = csv.writer(file_obj, quoting=csv.QUOTE_ALL)

    for party in parties:
        writer.writerow([block, lot, data['Year'], data['Document'], data['RecordDate'],
                data['Reel'], data['Image'], data['DocumentType'], party[0], party[1]])

    file_obj.flush




