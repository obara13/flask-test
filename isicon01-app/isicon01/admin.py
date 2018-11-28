"""
Routes and views for the flask application.
"""

from isicon01 import app
from flask import Flask, render_template, request, json
import datetime
import sqlite3


dbpath = 'data.db'

@app.route('/admin')
def admin():
    # db connection
    conn = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
    c = conn.cursor()

    try:
        #c.execute("drop table if exists server")
        c.execute("create table if not exists server (num integer primary key, ip text, use text)")
        #c.execute("insert into server values (?, ?, ?)", (1, "xxx.xxx.xxx.xxx", 0))

        ret = c.execute("select * from server;")
        servers = c.fetchall()
        for row in ret:
            print(row)

    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])

    conn.commit()
    conn.close()

    print(servers)

    return render_template(
        'admin.html',
        servers = servers,
    )

@app.route('/admin/add', methods=['POST'])
def add():
    # db connection
    conn = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
    c = conn.cursor()

    try:
        c.execute("insert into server(ip) values(?)", (request.form['ip'],))

        ret = c.execute("select * from server;")
        servers = c.fetchall()
        for row in ret:
            print(row)

    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])

    conn.commit()
    conn.close()

    print(servers)

    return render_template(
        'admin.html',
        servers = servers,
    )

@app.route('/admin/<int:num>/del', methods=['POST'])
def delete(num):
    # db connection
    conn = sqlite3.connect(dbpath, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
    c = conn.cursor()

    try:
        c.execute("delete from server where num = ?", (num,))

        ret = c.execute("select * from server;")
        servers = c.fetchall()
        for row in ret:
            print(row)
        print(servers)
    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])

    conn.commit()
    conn.close()

    return render_template(
        'admin.html',
        servers = servers,
    )
