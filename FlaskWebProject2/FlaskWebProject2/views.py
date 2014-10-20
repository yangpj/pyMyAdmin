# coding=utf-8
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user

from FlaskWebProject2 import app
from FlaskWebProject2 import users
from models import *

import jinja2

@app.route('/')
@app.route('/index')
def home():
    """Renders the home page."""
    ts=get_all_table_names()
    ts.sort()
    ds = []
    for item in ts:
        c = get_table_description(item)
        ds.append(c)
    return render_template(
        'index.html',
        title=u'主页',
        year=datetime.now().year,
        db_name='SZVTSMIS_SERVER',
        tbls=zip(ts, ds)
    )

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and request.form['user_name'] == 'admin':
        # login and validate the user...
        login_user(users.User())
        #flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("home"))
    return render_template(
        'login.html',
        title=u'登录',
        year=datetime.now().year,
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/logs')
def logs():
    """查看Tomcat服务器日志"""
    import os, glob
    root = os.environ['CATALINA_HOME']
    fullpaths = glob.glob("%s\logs\*.log" % root)
    filenames = [os.path.basename(item) for item in fullpaths]
    return render_template(
        'logs.html',
        title=u'日志工具',
        year=datetime.now().year,
        log_names = filenames
    )

@app.route('/logs/<log_name>')
def logs_detail(log_name):
    """查看Tomcat服务器日志"""
    import os
    root = os.environ['CATALINA_HOME']
    fullpath = "%s\logs\%s" % (root, log_name)
    f = open(fullpath, 'r')
    t = f.read().decode('gb2312')
    f.close()
    return render_template(
        'logs.html',
        title=u'日志工具',
        year=datetime.now().year,
        log_name = log_name,
        log_content = t
    )

@app.route('/sql', methods=['GET', 'POST'])
@login_required
def sql():
    if request.method == 'POST':
        query = request.form['sql_cmd']
        if query:
            result = execute_raw_sql2(query)
            rs = []
            if result.returns_rows:
                rs = result.fetchall()
            return render_template(
                'sql.html',
                title=u'SQL工具',
                year=datetime.now().year,
                previous_sql=query,
                resultSet=rs,
                keys=result.keys(),
                nrows=result.rowcount
            )
    return render_template(
        'sql.html',
        title=u'SQL工具',
        year=datetime.now().year,
        previous_sql=''
    )

@app.route('/db/<database>')
def database(database):
    ts=get_all_table_names()
    ts.sort()
    ds = []
    for item in ts:
        c = get_table_description(item)
        ds.append(c)
    return render_template(
        'database.html',
        title=u'数据库',
        year=datetime.now().year,
        db_name=database,
        tbls=zip(ts, ds),
    )

@app.route('/db/<database>/<table>')
def table(database, table):
    descr = get_table_description(table)
    result = execute_raw_sql2("select * from %s" % table)
    rs = []
    if result.returns_rows:
        rs = result.fetchall()
    return render_template(
        'table.html',
        title=u'数据表',
        year=datetime.now().year,
        db=database,
        tbl=table,
        resultSet=rs,
        tbl_descr=descr,
        cols_descr=descr[1:],
        cols=zip(get_all_column_names(table), get_all_column_types(table)),
        cons=get_table_constraints(table),
        indexes=get_table_indexes(table)
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
