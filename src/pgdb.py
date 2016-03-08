## -------------------------------------------
## module   : PostgreSQL connector, query functions
## package  : cdwcore
## author   : kaushik@mailbox.sc.edu
## created  : Tue Mar  8 08:17:12 EST 2016
## vim      : ts=4


import psycopg2 as pg
#-----------------------------------------------------------
# open a db connection
def pgdb(d='postgres', u='postgres', h=None, p=None):
    db_handle = None
    try:
        if h == None or h == 'localhost':
            if p == None:
                db_handle = pg.connect(database=d, user=u)
            else:
                db_handle = pg.connect(database=d, user=u, password=p)
        else:
            if p == None:
                db_handle = pg.connect(database=d, user=u, host=h)
            else:
                db_handle = pg.connect(database=d, user=u, host=h, password=p)
    except  Exception, e:
        raise
        db_handle = None
    return db_handle


#-----------------------------------------------------------
# same function, but using connection string
def pgdb(conn_string):

    db_handle = None
    if not conn_string:
        return db_handle
    try:
        db_handle = pg.connect(conn_string)
    except  Exception, e:
        raise
        db_handle = None
    return db_handle


#-----------------------------------------------------------
# execute a query
def pgquery(h, sql):
    if not h:
        return None
    else:
        try:
            c = h.cursor()
            if c == None:
                return None
            else:
                c.execute(sql)
                return c.fetchall()
        except Exception, e:
            raise
            return None

