## -------------------------------------------
## module   : Oracle connector, query functions
## package  : cdwcore
## author   : kaushik@mailbox.sc.edu
## created  : Tue Mar  8 08:17:12 EST 2016
## vim      : ts=4


import cx_Oracle as cx
import base64
import getpass

def authdb():
    return base64.b64encode(getpass.unix_getpass())

#-----------------------------------------------------------
# open a db connection
def oradb(dsn, u, p=None):
    db_handle = None
    try:
        print 'Authenticating user \'%s\' for \"%s\"' % (u, dsn)
        passwd = authdb()
        if passwd == None:
            db_handle = cx.connect(dsn=dsn, user=u)
        else:
            db_handle = cx.connect(dsn=dsn, user=u, password=base64.b64decode(passwd))
    except  Exception, e:
        raise
        db_handle = None
    return db_handle


#-----------------------------------------------------------
# using connection string
def connect(conn_string):

    db_handle = None
    if not conn_string:
        return db_handle
    try:
        db_handle = cx.connect(conn_string)
    except  Exception, e:
        raise
        db_handle = None
    return db_handle


#-----------------------------------------------------------
# execute a query
def query(h, sql):
    if not h:
        return None
    else:
        try:
            c = h.cursor()
            if c == None:
                return None
            else:
                c.execute(sql)
                return c
        except Exception, e:
            raise
            return None

