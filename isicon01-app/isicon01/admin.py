"""
Routes and views for the flask application.
"""

from isicon01 import app
from flask import Flask, render_template, request, json
import datetime
import sqlite3
import random


dbpath = 'data.db'

@app.route('/admin')
def admin():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    try:
        c.execute("select * from server;")
        servers = c.fetchall()
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
    ip = request.form['ip']
    port = random.randint(10000,19999)

    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    try:
        c.execute("insert into server(ip, port) values(?, ?)", (ip, port))
        c.execute("select * from server;")
        servers = c.fetchall()
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
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    try:
        c.execute("delete from server where num = ?", (num,))
        c.execute("select * from server;")
        servers = c.fetchall()
    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])

    conn.commit()
    conn.close()

    print(servers)

    return render_template(
        'admin.html',
        servers = servers,
    )


@app.route('/admin/createTable', methods=['POST'])
def createTable():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("create table if not exists server (num integer primary key, ip text, port integer, use text)")
    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])
    conn.commit()
    conn.close()
    return render_template(
        'admin.html',
    )

@app.route('/admin/deleteTable', methods=['POST'])
def deleteTable():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    try:
        c.execute("drop table if exists server")
    except sqlite3.Error as e:
        print('sqlite3 error: ', e.args[0])
    conn.commit()
    conn.close()
    return render_template(
        'admin.html',
    )

