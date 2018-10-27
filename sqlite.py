import json
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


def sql_db_to_json(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def sql_to_csv(file_name, query, conn):
    file_name = file_name + ".csv"
    cur = conn.cursor()
    cur.execute(query)
    with open(file_name, 'w', newline='') as f_handle:
        writer = csv.writer(f_handle)
        field_names = [i[0] for i in cur.description]
        writer.writerow(field_names)
        for row in cur.fetchall():
            try:
                writer.writerow(row)
            except Exception:
                print(keys.ENCODED_ERROR)
                pass


def sql_to_json(file_name, query, conn):
    cur = conn.cursor()
    cur.execute(query)
    file = open(file_name + ".txt", "w", newline='')
    for row in cur.fetchall():
        file.write("\n"+json.dumps(row))


def sql_to_xml(file_name, query, conn):
    cur = conn.cursor()
    cur.execute(query)
    file_name = file_name + ".xml"
    file = open(file_name, "w",  newline='')
    for row in cur.fetchall():
        xml = dicttoxml.dicttoxml(row)
        try:
            file.write("\n" + xml.decode())
        except Exception:
            print(keys.ENCODED_ERROR)
            pass


def sql_to_sql_table(table_name, query, conn):
    cur = conn.cursor()
    create_query = "CREATE TABLE " + table_name + " AS SELECT * FROM (" + query + ")"
    try:
        cur.execute(create_query)
    except Exception:
        print("Table:" + table_name + " already exists")
        pass


def queries_to_csv(conn):
    for i in range(len(keys.QUERYS)):
        sql_to_csv(keys.QUERY_NAMES[i], keys.QUERYS[i], conn)


def queries_to_json(conn):
    conn.row_factory = sql_db_to_json
    for i in range(len(keys.QUERYS)):
        sql_to_json(keys.QUERY_NAMES[i], keys.QUERYS[i], conn)


def queries_to_xml(conn):
    conn.row_factory = sql_db_to_json
    for i in range(len(keys.QUERYS)):
        sql_to_xml(keys.QUERY_NAMES[i], keys.QUERYS[i], conn)


def queries_to_sql_table(conn):
    for i in range(len(keys.QUERYS)):
        sql_to_sql_table(keys.QUERY_NAMES[i], keys.QUERYS[i], conn)


def get_file(file_type, conn):
    if file_type == keys.CSV:
        queries_to_csv(conn)
    elif file_type == keys.JSON:
        queries_to_json(conn)
    elif file_type == keys.XML:
        queries_to_xml(conn)
    elif file_type == keys.SQL_TABLE:
        queries_to_sql_table(conn)


def play_queries(path, file_type):
    conn = create_connection(path)
    get_file(file_type, conn)
