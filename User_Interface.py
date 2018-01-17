from flask import Flask, render_template, session, request, redirect, g, url_for, flash
import os
import Movie_Recommendation as mv
import User_Item_table as tb


app = Flask(__name__)  # Instance of the object Flask. __name__: this  gets value of name of python script
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('user', None)
        if request.form['password'] == '123Swaroop':
            session['user'] = request.form['userid']
            return redirect(url_for('home'))
        elif request.form['password'] == '123Chopper' and request.form['userid'] == '7777':
            session['user'] = request.form['userid']
            return redirect(url_for('admin'))
        else:
            error = "Invalid Credentials"
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/home/')
def home():
    if g.user:
        top_rated_movies, reco_for_you = mv.main(int(session['user']))
        return render_template('home.html', value=session['user'], tp_mv=top_rated_movies, rc_mv=reco_for_you)

    return redirect(url_for('login'))


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('SuperUser.html')
    elif request.method == 'POST':
        message, duration = tb.main()
        return render_template('SuperUser.html', msg=message, dur=duration)


if __name__ == '__main__':
    app.run(debug=True)
