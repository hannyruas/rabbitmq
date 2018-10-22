import sqlite3
from sqlite3 import Error
import csv
from xml.dom.minidom import getDOMImplementation
# import cx_Oracle
from xml.dom.minidom import parseString
import keys
import xml.etree.ElementTree as ET



def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def sql_to_json(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def sql_to_csv(file_name, rows, header):
    file_name = file_name + ".csv"
    with open(file_name, 'w', newline='') as f_handle:
        writer = csv.writer(f_handle)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def select_task_max_sals_to_country(conn):
    cur = conn.cursor()
    # cur.execute("SELECT  tracks.Name, invoices.BillingCountry, MAX (invoices.InvoiceId) "
    #             "FROM tracks, invoices, invoice_items WHERE tracks.TrackId == invoice_items.TrackId "
    #             "GROUP BY invoices.BillingCountry;")
    # cur.execute("SELECT  tracks.Name,  COUNT (*) "
    #             "FROM tracks, invoices, invoice_items "
    #             "JOIN tracks ON tracks.TrackId == invoice_items.TrackId "
    #             "JOIN invoices ON invoices.InvoiceId == invoice_items.InvoiceId;")
    rows = cur.fetchall()

    for row in rows:
        print(row)


def queries_to_json(conn):
    conn.row_factory = sql_to_json
    cur = conn.cursor()
    cur.execute(keys.SONGS_INFO)
    for row in cur.fetchall():
        print(row)

    cur = conn.cursor()
    cur.execute(keys.CUSTOMERS_INFO)
    for row in cur.fetchall():
        print(row)

    cur = conn.cursor()
    cur.execute(keys.DOMAIN_TO_COUNTRY)
    for row in cur.fetchall():
        print(row)

    cur = conn.cursor()
    cur.execute(keys.INVOICES_TO_COUNTRY)
    for row in cur.fetchall():
        print(row)


def queries_to_csv(conn):
    cur = conn.cursor()

    cur.execute(keys.SONGS_INFO)
    sql_to_csv(keys.SONGS_INFO_NAME, cur.fetchall(), ["song_name", "genres_name", "artists_name"])

    cur.execute(keys.CUSTOMERS_INFO)
    sql_to_csv(keys.CUSTOMERS_INFO_NAME, cur.fetchall(), ["first_name", "last_name", "phone", "email", "address"])

    cur.execute(keys.DOMAIN_TO_COUNTRY)
    sql_to_csv(keys.DOMAIN_TO_COUNTRY_NAME, cur.fetchall(), ['Country', 'domain_number', 'domain_name'])

    cur.execute(keys.INVOICES_TO_COUNTRY)
    sql_to_csv(keys.INVOICES_TO_COUNTRY_NAME, cur.fetchall(), ["country", "invoices_number"])


# def to_minidom(conn):
#     cur = conn.cursor()
#     cur.execute(keys.SONGS_INFO)
#     for row in cur.fetchall():
#         print(row[1])
#
#     return parseString(cur.fetchone()[0].read())


        # xml = row[1]

    # Generate the xml file from the string
    # dom = parse(keys.PATH)
    # impl = getDOMImplementation()
    # newdoc = impl.createDocument(None, "some_tag", None)
    # top_element = newdoc.documentElement
    # text = newdoc.createTextNode('Some textual content.')
    # top_element.appendChild(text)
    #
    # # Write the new xml file
    # xml_str = impl.toprettyxml(indent="  ")
    # with open("example.xml", "w") as f:
    #     f.write(xml_str)


def get_file(file_type, conn):
    if file_type == keys.CSV:
        queries_to_csv(conn)
    elif file_type == keys.CSV:
        queries_to_json(conn)
    # elif file_type == keys.XML:
    #     queries_to_xml(conn)
    elif file_type == keys.SQL:
        queries_to_json(conn)


def play_queries(path, file_type):
    conn = create_connection(path)
    get_file(file_type, conn)


def to_minidom(sql, db_file):
    conn = sqlite3.connect(db_file)
    with conn as db:
        cursor = db.cursor()
        # cursor.execute("select dbms_xmlgen.getxml('%s') from dual" % sql)
        cursor.execute("select dbms_xmlgen.getxml('%s') from dual" % sql)
        return parseString(cursor.fetchone()[0].read())


if __name__ == "__main__":
    # md = to_minidom(keys.SONGS_INFO, keys.PATH)
    # rows = md.getElementsByTagName("ROW")
    # print(type(rows), len(rows))
    data = ET.Element('data')
    items = ET.SubElement(data, 'items')
    item1 = ET.SubElement(items, 'item')
    item2 = ET.SubElement(items, 'item')
    item1.set('name', 'item1')
    item2.set('name', 'item2')
    item1.text = 'item1abc'
    item2.text = 'item2abc'

    # create a new XML file with the results
    mydata = ET.tostring(data)
    myfile = open("items2.xml", "w")
    myfile.write(mydata)