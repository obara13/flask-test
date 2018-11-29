"""
Routes and views for the flask application.
"""

from isicon01 import app
from flask import Flask, render_template, request, json
import datetime
import sqlite3
import subprocess


dbpath = 'data.db'
step_server = '192.168.175.27'
exam_time = 120


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
    endtime = starttime + datetime.timedelta(minutes=exam_time)
    finishtime = endtime

    gotty_param = create_gotty_param(userid)
    port = gotty_param[3]
    try:
        print(gotty_param)
        #command = subprocess.Popen(gotty_param)
        command = subprocess.run(gotty_param, timeout=60)
        print(command)
    except:
        print('in gotty error')
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
        gotty = 'http://' + step_server + ':' + port + '/',
    )

# create gotty connection parameters
def create_gotty_param(userid):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM server WHERE use IS NULL;")
        exam_servers = c.fetchall()
        for server in exam_servers:
            num = server[0]
            ip = server[1]
            port = server[2]
            use = server[3]
            # if server is blank, set use for exam
            if use is None:
                c.execute("UPDATE server SET use = 'use', user = ? WHERE num = ?", (userid, num))
                break
    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])
    conn.commit()
    conn.close()

    # create command exec string "gotty -w -p port ssh xxx.xxx.xxx.xxx"
    gotty_param = [
        'gotty', '-w',
        '-p', str(port),
        'ssh', str(ip),
    ]

    return gotty_param

