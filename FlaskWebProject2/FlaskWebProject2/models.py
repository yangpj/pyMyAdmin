# coding=utf-8

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, interfaces
from sqlalchemy.ext.automap import generate_relationship

class G:
    db = None

connstr = "postgresql+psycopg2://postgres:postgres@d.w:5432/%s" % 'SZVTSMIS_SERVER'
ENGINE = create_engine(connstr)

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

def get_all_table_objects(db_name):
    metadata = MetaData()
    metadata.reflect(ENGINE)
    base = automap_base()
    base.prepare(ENGINE, reflect=True, generate_relationship=_gen_relationship)
    return base.classes

def execute_raw_sql(db_name, sql_stmt):
    result = ENGINE.execute(sql_stmt)
    if result.closed is not True:
        return result.fetchall()
    else:
        return result.rowcount

def find_table_object_by_name(tables, tbl_name):
    name = tbl_name.encode('utf8')
    for i in tables:
        if i.__table__.name == name:
            return i
    return None

def get_table_description(tbl_name):
    tn = tbl_name.encode('utf-8')
    qs = "select description from pg_description join pg_class on pg_description.objoid = pg_class.oid where relname = %r" % tn
    result = G.db.execute(qs)
    return result.fetchall()

#=> [str]
def get_all_table_names(db_name):
    tables = get_all_table_objects(db_name)
    tn = []
    for i in tables:
        tn.append(i.__table__.name)
    return tn

#=> [str]
def get_all_column_names(tbl_obj):
    cn = []
    for x in tbl_obj.__table__.columns:
        cn.append(x.name)
    return cn

def get_all_column_types(tbl_obj):
    cn = []
    for x in tbl_obj.__table__.columns:
        cn.append(str(x.type))
    return cn

#=> [str]
def get_table_constraints(tbl_obj):
    sc = []
    for x in tbl_obj.__table__.constraints:
        sc.append(str(x))
    return sc

#=> [str]
def get_table_indexes(tbl_obj):
    ix = []
    for x in tbl_obj.__table__.indexes:
        ix.append(str(x))
    return ix

#=> [str]
def get_all_foreign_keys_names(db_name, tbl_name):
    tables = get_all_table_objects(db_name)
    t = find_table_by_name(tables, tbl_name)
    assert t is not None
    fkn = []
    for x in t.table__.foreign_keys:
        fkn.append(x.name)
    return fkn

from FlaskWebProject2 import app

@app.before_request
def before_request():
    G.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(G, 'db', None)
    if db is not None:
        db.close()