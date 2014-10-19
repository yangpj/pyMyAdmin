# coding=utf-8

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, interfaces
from sqlalchemy.ext.automap import generate_relationship

class G:
    db = None

#connstr = "postgresql+psycopg2://postgres:dev@localhost:5432/%s" % 'pyMyAdmin'
connstr = "postgresql+psycopg2://postgres:postgres@d.w:5432/%s" % 'SZVTSMIS_SERVER'
ENGINE = create_engine(connstr)
METADATA = MetaData()
METADATA.reflect(ENGINE)

def _gen_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw):
    if direction is interfaces.ONETOMANY:
        kw['cascade'] = ''
        kw['passive_deletes'] = False
    # make use of the built-in function to actually return
    # the result.
        return generate_relationship(base, direction, return_fn,
                                     attrname, local_cls, referred_cls, **kw)

def connect_db():
    return ENGINE.connect()

def get_all_table_objects():
    metadata = MetaData()
    metadata.reflect(ENGINE)
    base = automap_base()
    base.prepare(ENGINE, reflect=True, generate_relationship=_gen_relationship)
    return base.classes

def execute_raw_sql(sql_stmt):
    if sql_stmt:
        result = ENGINE.execute(sql_stmt)
        if result.returns_rows:
            return result.fetchall()
        else:
            return result.rowcount
    else:
        return None

def execute_raw_sql2(sql_stmt):
    result = None
    if sql_stmt:
        result = ENGINE.execute(sql_stmt)
    return result

def get_table_description(tbl_name):
    tn = tbl_name.encode('utf-8')
    qs = "select description from pg_description join pg_class on pg_description.objoid = pg_class.oid where relname = %r" % tn
    result = ENGINE.execute(qs)
    return result.fetchall()

#=> [str]
def get_all_table_names():
    return METADATA.tables.keys()

#=> [str]
def get_all_column_names(tbl_name):
    return METADATA.tables[tbl_name].columns.keys()

def get_all_column_types(tbl_name):
    cols = METADATA.tables[tbl_name].columns
    return [str(item.type) for item in cols]

#=> 返回约束名的列表
def get_table_constraints(tbl_name):
    cons = METADATA.tables[tbl_name].constraints
    return [i.name for i in cons if i.name != '_unnamed_']

#=> [str]
def get_table_indexes(tbl_name):
    indexes = METADATA.tables[tbl_name].indexes
    return [i.name for i in indexes]

#=> [str]
def get_all_foreign_keys_names(db_name, tbl_name):
    tables = get_all_table_objects()
    t = find_table_by_name(tables, tbl_name)
    assert t is not None
    fkn = []
    for x in t.table__.foreign_keys:
        fkn.append(x.name)
    return fkn

#from FlaskWebProject2 import app

#@app.before_request
#def before_request():
#    G.db = connect_db()

#@app.teardown_request
#def teardown_request(exception):
#    db = getattr(G, 'db', None)
#    if db is not None:
#        db.close()