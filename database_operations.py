# imports below--------------------------------------------------------

import sqlite3
import platform
import os

# https://www.sqlitetutorial.net/sqlite-python/insert/


# general database operations below--------------------------------------


def create_connection(db_file):  # connectiong to that database
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        return 'error'


def create_table(db_file, create_table_sql):  # creting tables in database
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(create_table_sql)
    conn.close()

# handling signup and login below--------------------------------------------------


# ading user(signing up/ registeing/ creating accoonts)
def add_user(db_file, name, email, password, create_table_sql):
    tablename = 'users'
    sql = ''' INSERT INTO {tablename}(name,email,password)
              VALUES(?,?,?)'''.format(tablename=tablename)
    values = (name, email, password)
    conn = create_connection(db_file)
    with conn as conn:
        cur = conn.cursor()
        try:
            cur.execute(sql, values)
        except:
            create_table(db_file, create_table_sql)
            cur.execute(sql, values)
        conn.commit()


# finding a user in in the users database for verifying login credentials
def find_user(db_file, email):
    tablename = 'users'
    sql = 'select * from {tablename} where email=?'.format(tablename=tablename)
    value = (email,)
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(sql, value)

    row = cur.fetchone()

    if row == None:
        return False
    else:
        return list(row)

    conn.close()


# changing passwords
def change_pwd(db_file, email, new_pwd):

    conn = create_connection(db_file)

    with conn as conn:
        cur = conn.cursor()

        tablename = 'users'

        sql = 'update {tablename} set password = ? where email = ?'.format(
            tablename=tablename)
        values = (new_pwd, email)

        cur.execute(sql, values)


# handling the notes database below-----------------------------------
'''making database and naming them on the names of the user or by their id in the users database and storing
   notes of every indivisal user in a indivisual database'''


def save_notes(db_file, date, title, notes):

    conn = create_connection(db_file)

    with conn as conn:
        cur = conn.cursor()

        create_table_sql = """ CREATE TABLE IF NOT EXISTS notes (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    date text NOT NULL,
                                    title text ,
                                    notes text
                                ); """

        save_notes_sql = ''' INSERT INTO notes(date,title,notes)
              VALUES(?,?,?)'''
        values = (date, title, notes,)

        create_table(db_file, create_table_sql)

        cur.execute(save_notes_sql, values)
        conn.commit()


def show_all_notes(db_file):

    conn = create_connection(db_file)

    create_table_sql = """ CREATE TABLE IF NOT EXISTS notes (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                date text NOT NULL,
                                title text ,
                                notes text
                            ); """
    with conn as conn:  # making the notes table in notes database
        create_table(db_file, create_table_sql)

    with conn as conn:  # showing notes
        cur = conn.cursor()
        sql = 'select * from notes'
        cur.execute(sql)
        row = cur.fetchall()

    return row
