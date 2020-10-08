# imports below ---------------------------------------------------------

import os
import datetime
import calendar
import platform
import hashlib
from flask import Flask, render_template, request, redirect, session
from EmailValidator import check_mail
from database_operations import *

# app variables below -----------------------------------------------------

app = Flask(__name__)

app.secret_key = 'secrets'

env = 'dev'

if env == 'dev':
    app.debug = True
else:
    app.debug = False


# database paths below-----------------------------------------------------

if platform.system() in ['Darwin', 'Linux']:
    db_dir = '{cwd}/database'.format(cwd=os.getcwd())
    db_dir_path = r'{database}'.format(database=db_dir)
    users_db = r'{db_dir_path}{user}'.format(
        db_dir_path=db_dir_path, user='/users.db')
    notes_db = r'{db_dir_path}{user}'.format(
        db_dir_path=db_dir_path, user='/notes.db')


else:  # windows platform
    db_dir = '{cwd}\database'.format(cwd=os.getcwd())
    db_dir_path = r'{database}'.format(database=db_dir)
    users_db = r'{db_dir_path}{user}'.format(
        db_dir_path=db_dir_path, user='\\users.db')
    notes_db = r'{db_dir_path}{user}'.format(
        db_dir_path=db_dir_path, user='\\notes.db')


# app routes below--------------------------------------------------------------------

@app.route('/')  # the main or the landing page of the website
def main():
    if 'user' in session:
        return redirect('/notes')

    return render_template('signup.html', Title='Sign Up', sessions=session.get('user'))


@app.route('/login', methods=['GET', 'POST'])  # login page
def login():

    if 'user' in session:
        return redirect('/notes')

    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        hp = hashlib.md5(password.encode()).hexdigest()

        if check_mail(email):
            user_data = find_user(users_db, email)
            if user_data == None:
                return redirect('/signup')
            else:
                if user_data[3] == hp:
                    session['user'] = email
                    return redirect('/notes')

    return render_template('login.html', Title='Login', sessions=session.get('user'))


@app.route('/forgotpwd', methods=['GET', 'POST'])  # forgot passowrd
def forgotpwd():

    if 'user' in session:
        session.pop('user')

    if request.method == 'POST':
        email = request.form['Email']
        new_pwd = request.form['Password']
        hp_new = hashlib.md5(new_pwd.encode()).hexdigest()
        user_data = find_user(users_db, email)
        if user_data[2] == email:
            change_pwd(users_db, email, hp_new)
            return redirect('/login')

    return render_template('change_pwd.html', Title='Forgot Password', sessions=session.get('user'))


@app.route('/signup', methods=['GET', 'POST'])  # create account page
def signup():

    if 'user' in session:
        return redirect('/')

    else:

        create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL,
                                    email text UNIQUE NOT NULL,
                                    password text NOT NULL
                                ); """

        if request.method == 'POST':
            name = request.form['Name']
            email = request.form['Email']
            password = request.form['Password']
            hp = hashlib.md5(password.encode()).hexdigest()

            if check_mail(email):
                create_table(users_db, create_users_table)
                try:
                    add_user(users_db, name, email, hp, create_users_table)
                except:  # if the user is alredy present due to email being a unique key
                    return redirect('/login')

            if find_user(users_db, email) != None:
                session['user'] = email
                return redirect('/')
            else:
                return redirect('/signup')

    return render_template('signup.html', Title='Sign Up', sessions=session.get('user'))


# @app.route('/notes')  # where notes are displayed(comming soon)
# def notes():
#     if 'user' in session:
#         user_data = find_user(users_db, session['user'])
#         return render_template('comming_soon.html', Title="notes", Name=user_data[1], sessions=session.get('user'))
#     else:
#         return redirect('/login')


@app.route('/logout')  # logout
def logout():

    if 'user' in session:
        session.pop('user')
        return redirect('/login')
    else:
        return redirect('/login')


@app.route('/compose', methods=['GET', 'POST'])  # writing a new note
def editor():
    if request.method == 'POST':
        current_time = datetime.datetime.now()
        year = current_time.year
        month = calendar.month_name[current_time.month]
        day = current_time.day
        todays_date = f'{day} {month} {year}'

        title = request.form['TOPIC']
        notes = request.form['notes']
        save_notes(notes_db, todays_date, title, notes)

    if session.get('user') != None:
        return render_template('compose.html', Title='Compose Notes', sessions=session.get('user'))
    else:
        return redirect('/login')


@app.route('/notes')
def show_notes():
    notes = show_all_notes(notes_db)
    return render_template('show_notes.html', Title='Notes', notes=notes)


# running the webapp/website----------------------------
if __name__ == '__main__':
    app.run()
