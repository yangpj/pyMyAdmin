# coding=utf-8
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from FlaskWebProject2 import app
from models import *

@app.route('/')
def home():
    """Renders the home page."""
    ts=get_all_table_names('SZVTSMIS_SERVER')
    ts.sort()
    ds = []
    for item in ts:
        c = get_table_description(item)
        ds.append(c)
    return render_template(
        'index.html',
        title=u'主页',
        year=datetime.now().year,
        db='SZVTSMIS_SERVER',
        tbls=zip(ts, ds)
    )

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
    import os, glob
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
def sql():
    if request.method == 'POST':
        r = execute_raw_sql("SZVTSMIS_SERVER", request.form['sql_cmd'])
        if isinstance(r, list):
            return render_template(
                'sql.html',
                title=u'SQL工具',
                year=datetime.now().year,
                previous_sql=request.form['sql_cmd'],
                result=r
            )
        else:
            return render_template(
                'sql.html',
                title=u'SQL工具',
                year=datetime.now().year,
                previous_sql=request.form['sql_cmd'],
                nrows=r
            )
    else:
        return render_template(
            'sql.html',
            title=u'SQL工具',
            year=datetime.now().year,
        )

@app.route('/db/<database>')
def database(database):
    ts=get_all_table_names(database)
    ts.sort()
    ds = []
    for item in ts:
        c = get_table_description(item)
        ds.append(c)
    return render_template(
        'database.html',
        title=u'数据库',
        year=datetime.now().year,
        db=database,
        tbls=zip(ts, ds),
    )

@app.route('/db/<database>/<table>')
def table(database, table):
    descr = get_table_description(table)
    tos = get_all_table_objects(database)
    to = find_table_object_by_name(tos, table)
    return render_template(
        'table.html',
        title=u'数据表',
        year=datetime.now().year,
        db=database,
        tbl=table,
        result=execute_raw_sql(database, "select * from %s" % table),
        tbl_descr=descr,
        cols_descr=descr[1:],
        cols=zip(get_all_column_names(to), get_all_column_types(to)),
        cons=get_table_constraints(to),
        indexes=get_table_indexes(to)
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
