from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_mail import Mail
import os
import bcrypt


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11413344'
app.config['MYSQL_PASSWORD'] = '5VHwuYaD7d'
app.config['MYSQL_DB'] = 'sql11413344'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USE_TLS"] = False
app.config['MAIL_USERNAME'] = 'flasktask1998@gmail.com'
app.config['MAIL_PASSWORD'] = 'flasktask123'
mail = Mail(app)
    
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

from flasktask import routes