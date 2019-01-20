from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import pymysql
import hashlib


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sarelproject'


@app.route('/', methods=['GET', 'POST'])
@app.route("/sign_up", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db = pymysql.connect('sql7.freemysqlhosting.net', 'sql7274856', 'ihJVt3KMhW', 'sql7274856')
        cursor = db.cursor()
        if existing_email(form.email.data.upper(), cursor):
            flash('this email already exists, go to log in by clicking  the link on the bottom of this page', 'danger')
        else:
            cursor.execute("INSERT INTO logindb(`password`, `email`, `name`) VALUES ('{0}','{1}','{2}')"
                           .format(hashing(form.password.data), form.email.data.upper(), form.username.data))
            db.commit()
            flash('Account created for {0}'.format(form.username.data), 'success')
            return redirect(url_for('login'))
        db.close()
    return render_template('sign_up.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        typed_email = form.email.data.upper()
        typed_password = hashing(form.password.data)
        db = pymysql.connect('sql7.freemysqlhosting.net', 'sql7274856', 'ihJVt3KMhW', 'sql7274856')
        cursor = db.cursor()
        if correct_email_and_password(typed_email, typed_password, cursor):
            flash("successfully logged in", 'success')
            return render_template('inside_site.html')
        elif existing_email(typed_email, cursor):
            message = "login failed please check your password again"
        else:
            message = "email not found please check again"
        flash(message, 'danger')
        db.close()
    return render_template('login.html', title='Login', form=form)


def correct_email_and_password(email, password, cursor):
    cursor.execute("SELECT COUNT(*) FROM logindb WHERE email = '{0}' and password = '{1}'"
                   .format(email, password))
    results = cursor.fetchone()
    return results[0] > 0

def existing_email(email,cursor):
    cursor.execute("SELECT COUNT(*) FROM logindb WHERE email = '{0}'".format(email))
    results = cursor.fetchone()
    return results[0] > 0


def hashing(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


if __name__ == '__main__':
    app.run(debug=True)



