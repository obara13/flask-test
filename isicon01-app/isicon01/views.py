"""
Routes and views for the flask application.
"""

from isicon01 import app
from flask import Flask, render_template, request, json
import datetime
import sqlite3
import subprocess


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
    endtime = starttime + datetime.timedelta(minutes=etime)
    finishtime = endtime

    gotty_param = create_gotty_param()
    try:
        print('a')
        print(gotty_param)
        #gotty_param = [
        #    'gotty', '-w',
        #    '-p', '10263',
        #    'ssh', '192.168.10.11',
        #]
        #print('b')
        print(gotty_param)
        #command = subprocess.Popen(gotty_param)
    except:
        print('gotty except')
        pass

    # db connection
    conn = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
    c = conn.cursor()

    try:
        c.execute("drop table if exists exam")
        c.execute("create table if not exists exam (userid text, starttime datetime, endtime datetime, finishtime datetime)")
        c.execute("insert into exam values (?, ?, ?, ?)", (userid, starttime, endtime, finishtime))

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
        gotty = 'http://192.168.175.27:' + str(gotty_param[3]) + '/',
    )



# create gotty connection
def create_gotty_param():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM server WHERE use IS NULL;")
        servers = c.fetchall()
        for server in servers:
            num = server[0]
            ip = server[1]
            port = server[2]
            if server[3] is None:
                c.execute("UPDATE server SET use = 'use' WHERE num = ?", (num,))
                gotty_url = 'http://' + '192.168.175.27' + ':' + str(port) + '/'
                break
    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])
    conn.commit()
    conn.close()

    gotty_param = [
        'gotty', '-w',
        '-p', str(port),
        'ssh', str(ip),
    ]

    return gotty_param

