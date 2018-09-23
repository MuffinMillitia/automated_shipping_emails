__author__ = 'Chris'

from fishwrapper import Fishbowlapi
from fishwrapper import xmlparse
import openpyxl
import os
import xmltodict
import csv

""" Create an instance of the class Fishbowlapi and pull a query. """


def create_connection(filepath, filename):
    testapi = Fishbowlapi('admin', 'j2JGnLFwdOBFKPI6VqTPzg==', '192.168.10.56',
                          port=28192)  # Fishbowlapi takes user, encrypted password, and ip address
    mypath = filepath
    myfile = os.path.join(mypath, filename)
    mydata = open(myfile, 'r')
    mysql = mydata.read()
    testxml = testapi.get_sql_query(mysql)  # Store the results of the query in xml.
    testapi.close()  # Close the connection to the server
    mydata.close()
    # print (testxml) # Print the xml to see that it worked
    return testxml


""" Create an instance of the class Fishbowlapi and pull a query. This one uses direct input SQL instead of a filepath to a .txt doc"""


def create_connection_second_option(sql, port, ip):
    testapi = Fishbowlapi('admin', 'j2JGnLFwdOBFKPI6VqTPzg==', ip,
                          port=port)  # Fishbowlapi takes user, encrypted password, and ip address
    # mypath = filepath
    # myfile = os.path.join(mypath, filename)
    # mydata = open(myfile, 'r')
    # mysql = mydata.read()
    testxml = testapi.get_sql_query(sql)  # Store the results of the query in xml.
    testapi.close()  # Close the connection to the server
    # mydata.close()
    # print (testxml) # Print the xml to see that it worked
    return testxml


""" The function used to parse the xml and fill the cells of a worksheet within the workbook. """


def makeexcelsheet(xml):
    wb = openpyxl.Workbook()  # Create an excel workbook
    ws = wb.active  # Create a worksheet within the workbook passed.
    rownum = 1  # Rows and columns start at 1. Cell A1 is row 1, column 1.
    for element in xmlparse(xml).iter():  # Loop through every line of xml
        if element.tag == "Row":  # Find the rows of xml that have the data we are looking for.
            col = 1  # Start at the first element of that row.
            for item in element.text.split(','):  # Loop through the entire row.
                item = item.replace('"', '').strip()  # Get rid of the quotes around each element
                ws.cell(row=rownum,
                        column=col).value = item  # Fill the value of the corresponding cell with the appropriate value
                col += 1  # Increase the column by on to capture the whole row.
            rownum += 1  # Once that row is complete move to the next row.
    return wb  # Return the workbook that was created.


def makeexcelsheetredoux(xml, filepath, filename):
    fullpath = os.path.join(filepath, filename)
    thefile = open(fullpath, 'w')
    mycsv = csv.writer(thefile, dialect='excel')
    xmldict = xmltodict.parse(xml)
    csvlist = []
    for row in xmldict:
        for element in xmldict[row]:
            if element == 'FbiMsgsRs':
                for each in xmldict[row][element]:
                    if each == 'ExecuteQueryRs':
                        for every in xmldict[row][element][each]:
                            if every == 'Rows':
                                for all in xmldict[row][element][each][every]:
                                    myoldcsv = csv.reader(xmldict[row][element][each][every][all])
                                    for row in myoldcsv:
                                        # print(row)
                                        csvlist.append(row)
    mycsv.writerows(csvlist)
    thefile.close()


"""Save Excel workbook."""


def save_workbook(wb, filepath, filename):
    target_dir = filepath  # Choose the file path you want to save to.
    fullpath = os.path.join(target_dir, filename)  # Choose the name of the excel workbook
    wb.save(fullpath)  # Save the excel workbook


if __name__ == "__main__":
    xml = "<FbiMsgsRq><VendorGetRq><Name>Graybar</Name></VendorGetRq></FbiMsgsRq>"
    api = Fishbowlapi('admin', 'j2JGnLFwdOBFKPI6VqTPzg==', '192.168.10.56', port=28192)
    response = api.raw_xml_request(xml)
    print(response)
