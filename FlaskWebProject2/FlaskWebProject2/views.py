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
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        db='SZVTSMIS_SERVER',
        tbls=get_all_table_names('SZVTSMIS_SERVER')
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


@app.route('/db/<name>')
def database(name):
    return render_template(
        'database.html',
        title=u'数据库',
        year=datetime.now().year,
        db=name,
        tbls=get_all_table_names(name)
    )

@app.route('/db/<database>/<table>')
def table(database, table):
    tos = get_all_table_objects(database)
    to = find_table_object_by_name(tos, table)
    return render_template(
        'table.html',
        title=u'数据表',
        year=datetime.now().year,
        db=database,
        tbl=table,
        result=execute_raw_sql(database, "select * from %s" % table),
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
