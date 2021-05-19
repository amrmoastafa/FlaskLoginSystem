from flask import Flask, render_template, redirect, request, url_for, session
from flask.helpers import flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flasktask import app, mysql, mail

from flask_mail import Message


def get_reset_token(id,expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': id}).decode('utf-8')

def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return user_id

@app.route('/')
def home():
    return render_template("home.html")

    
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password,bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        users = cur.fetchone()
        if users is not None:
            flash('User already exists !','error')
            return redirect(url_for("register"))
        cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = name
        session['email'] = email
        session['password'] = request.form['password']
        return redirect(url_for("home"))

@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()
        if user is not None:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                session['password'] = request.form['password']
                return redirect(url_for("success"))
                
                # return render_template("success.html")
            else:
                flash('Wrong email/password !','error')
                
                return redirect(url_for("login"))
        else:
            flash('User doesnot exist!','error')
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


@app.route('/success')
def success():
    
    return render_template("success.html")

@app.route('/forgot', methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()
        if user is not None:
            print()

            token = get_reset_token(user['id'])
            msg = Message('Password Reset Request',
                        sender='noreply@demo.com',
                        recipients=[user['email']])
            msg.body = f'''To reset your password, visit the following link:
{url_for('reset', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
            mail.send(msg)
            flash("An email was sent",'info')
            # return redirect(url_for("forgot"))
            return redirect(url_for("login"))
        else:
            flash('There is no account linked to this email , please register','error')
            return redirect(url_for("register"))
    else:
        return render_template("forgotpw.html")
        # return render_template("forgotpw.html")


@app.route('/resetpw/<token>',methods = ['GET','POST'])
def reset(token):
    
    # flash('This is an invalid link , please request another','error')
    print(request.method)
    try:
        password = request.form['password'].encode('utf-8')
        print("I reached here bro !")
        print(token)
        user_id = verify_reset_token(token)
        print(user_id)
        hash_password = bcrypt.hashpw(password,bcrypt.gensalt())
        print(hash_password)
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE id=%s",(user_id,))
        user = cur.fetchone()
        print(user['email'])
        hash_password = hash_password.decode('utf-8')
        query = f"UPDATE users SET password='{hash_password}' WHERE id={user_id};"
        print(query)
        cur.execute(query)
        mysql.connection.commit()
        flash("Your password was updated successfully , you can login now.",'info')
        
        return redirect(url_for("login")) 

    except:
        return render_template("resetpw.html")
    
    print(ret)
    if ret is not None:
        print("Here2")
        user_id = verify_reset_token(token)
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password,bcrypt.gensalt())
        cur = mysql.connection.cursor()
        print("UPDATE users SET password=%s WHERE id=%i",(hash_password,user_id,))
        # cur.executre("UPDATE users SET password=%s WHERE id=%i",(hash_password,user_id,))
        
        # users = cur.fetchone()
        # if users is not None:
        #     flash('User already exists !','error')
        #     return redirect(url_for("register"))
        # cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        # mysql.connection.commit()
        # session['name'] = name
        # session['email'] = email
        # session['password'] = request.form['password']
        return redirect(url_for("home"))        
        # return render_template("resetpw.html")
    