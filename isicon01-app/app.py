"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request, json
import datetime
import sqlite3
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
    id = request.form['id']
    starttime = datetime.datetime.now()
    endtime = starttime + datetime.timedelta(minutes=etime)

    conn = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']

    c = conn.cursor()

    try:
        #c.execute("drop table if exists exam")
        c.execute("create table if not exists exam (id text, starttime datetime, endtime datetime)")
        c.execute("insert into exam values (?, ?, ?)", (id, starttime, endtime))

        ret = c.execute("select * from exam;")
        for row in ret:
            print(row)

    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])

    conn.commit()
    conn.close()

    return render_template(
        'start.html',
        id = id,
        starttime = starttime,
        endtime = endtime,
    )

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
