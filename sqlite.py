import sqlite3
from sqlite3 import Error
import csv
import keys
import dicttoxml


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


def sql_to_xml(file_name, result, cur):
    items = []
    file_name = file_name + ".xml"
    for row in result:
        for key in cur.description:
            items.append({key[0]: value for value in row})
    xml = dicttoxml.dicttoxml(items)
    file = open(file_name, "w")
    file.write("".join(map(chr, xml)))


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


def queries_to_xml(conn):
    cur = conn.cursor()
    result = cur.execute(keys.SONGS_INFO)
    sql_to_xml(keys.SONGS_INFO_NAME, result, cur)

    result = cur.execute(keys.CUSTOMERS_INFO)
    sql_to_xml(keys.CUSTOMERS_INFO_NAME, result, cur)

    result = cur.execute(keys.DOMAIN_TO_COUNTRY)
    sql_to_xml(keys.DOMAIN_TO_COUNTRY_NAME, result, cur)

    result = cur.execute(keys.INVOICES_TO_COUNTRY)
    sql_to_xml(keys.INVOICES_TO_COUNTRY_NAME, result, cur)


def get_file(file_type, conn):
    if file_type == keys.CSV:
        queries_to_csv(conn)
    elif file_type == keys.CSV:
        queries_to_json(conn)
    elif file_type == keys.XML:
        queries_to_xml(conn)


def play_queries(path, file_type):
    conn = create_connection(path)
    get_file(file_type, conn)
