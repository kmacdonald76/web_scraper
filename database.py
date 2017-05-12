#!/usr/bin/env python
import psycopg2
import sys

def table_insert(table_name, table_contents):

    for table_content in table_contents:

        sql_params = []

        sql_statement = "INSERT INTO " + table_name + " "

        sql_headers = ", ".join(table_content['headers'])
        sql_statement += "(" + sql_headers + ") VALUES "

        first_row = True
        param_count = 0
        for record in table_content['content']:
            if first_row == False:
                sql_statement += ","
            else:
                param_count = len(record)
                first_row = False;

            placeholders = []
            for val in record:
                placeholders.append('%s')
                sql_params.append(val)

            sql_row = ", ".join(placeholders)
            sql_statement += "(" + sql_row + ")"

        sql_statement += " ON CONFLICT DO NOTHING"
        db_insert(sql_statement, sql_params)

def db_delete(sql, params=[]):
    con = None

    try:
        con = psycopg2.connect("dbname=dbname user=postgres password=password") 
        cur = con.cursor()
        cur.execute(sql, params)
        con.commit()

    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()

        print 'Error %s' % e    
        sys.exit(1)

    finally:
        if con:
            con.close()

def db_insert(sql, params=[]):
    con = None

    try:
        con = psycopg2.connect("dbname=dbname user=postgres password=password") 
        cur = con.cursor()
        cur.execute(sql, params)
        con.commit()

    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()

        print 'Error %s' % e    
        sys.exit(1)

    finally:
        if con:
            con.close()

def db_select(sql, params=[]):
    con = None

    try:
        con = psycopg2.connect("dbname=dbname user=postgres password=password") 
        cur = con.cursor()
        cur.execute(sql, params)
        records = cur.fetchall()

    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()

        print 'Error %s' % e    
        sys.exit(1)

    finally:
        if con:
            con.close()

    return records

