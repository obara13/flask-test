"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request, json
import datetime
import sqlite3
import subprocess

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

dbpath = 'data.db'
etime = 120

@app.route('/')
def hello():
    return render_template(
        'index.html',
    )

@app.route('/start', methods=['POST'])
def start():
    print(request.form)

    # param set
    userid = request.form['id']
    starttime = datetime.datetime.now()
    finishtime = starttime + datetime.timedelta(minutes=etime)
    endtime = finishtime

    # gotty connection
    client = '192.168.10.2'
    try:
        args = [
            'gotty',
            '-w',
            'ssh',
            client,
        ]
        command = subprocess.Popen(args)
    except:
        pass

    # db connection
    conn = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
    c = conn.cursor()

    try:
        c.execute("drop table if exists exam")
        c.execute("create table if not exists exam (userid text, starttime datetime, endtime datetime)")
        c.execute("insert into exam values (?, ?, ?)", (userid, starttime, endtime))

        ret = c.execute("select * from exam;")
        for row in ret:
            print(row)

    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])

    conn.commit()
    conn.close()

    return render_template(
        'start.html',
        id = userid,
        starttime = starttime,
        endtime = endtime,
        gotty = 'http://192.168.175.27:8080/',
    )

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', '192.168.175.27')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '80'))
    except ValueError:
        PORT = 81
    app.run(HOST, PORT)

