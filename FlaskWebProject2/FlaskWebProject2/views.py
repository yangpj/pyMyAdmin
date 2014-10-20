# coding=utf-8
"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user

from FlaskWebProject2 import app, users
from template_decorator import templated
from models import *

@app.route('/')
@app.route('/index')
@templated('index.html')
def home():
    """Renders the home page."""
    ts=get_all_table_names()
    ts.sort()
    ds = []
    for item in ts:
        c = get_table_description(item)
        ds.append(c)
    return dict(title=u'主页', db_name='SZVTSMIS_SERVER', tbls=zip(ts, ds))

@app.route('/login', methods=["GET", "POST"])
@templated('login.html')
def login():
    if request.method == 'POST' and request.form['user_name'] == 'admin':
        # login and validate the user...
        login_user(users.User())
        #flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("home"))
    return dict(title=u'登录')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/logs')
@templated('logs.html')
def logs():
    """查看Tomcat服务器日志"""
    import os, glob
    root = os.environ['CATALINA_HOME']
    fullpaths = glob.glob("%s\logs\*.log" % root)
    filenames = [os.path.basename(item) for item in fullpaths]
    return dict(title=u'日志工具', log_names = filenames)

@app.route('/logs/<log_name>')
@templated('logs.html')
def logs_detail(log_name):
    """查看Tomcat服务器日志"""
    import os
    root = os.environ['CATALINA_HOME']
    fullpath = "%s\logs\%s" % (root, log_name)
    f = open(fullpath, 'r')
    t = f.read().decode('gb2312')
    f.close()
    return dict(title=u'日志工具', log_name=log_name,log_content=t)

@app.route('/sql', methods=['GET', 'POST'])
@templated('sql.html')
@login_required
def sql():
    if request.method == 'POST':
        query = request.form['sql_cmd']
        if query:
            result = execute_raw_sql2(query)
            rs = []
            if result.returns_rows:
                rs = result.fetchall()
            return dict(title=u'SQL工具',
                        previous_sql=query,
                        resultSet=rs,
                        keys=result.keys(),
                        nrows=result.rowcount)
    return dict(title=u'SQL工具',previous_sql='')

@app.route('/db/<database>')
@templated('database.html')
def database(database):
    ts=get_all_table_names()
    ts.sort()
    ds = []
    for item in ts:
        c = get_table_description(item)
        ds.append(c)
    return dict(title=u'数据库', db_name=database, tbls=zip(ts, ds))

@app.route('/db/<database>/<table>')
@templated('table.html')
def table(database, table):
    descr = get_table_description(table)
    result = execute_raw_sql2("select * from %s" % table)
    rs = []
    if result.returns_rows:
        rs = result.fetchall()
    return dict(
        title=u'数据表',
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
@templated('contact.html')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.'
    )

@app.route('/about')
@templated('about.html')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.'
    )
