from pysqlite2 import dbapi2 as sqlite

def initdb(sqlite_path):
    cn = sqlite.connect(sqlite_path)
    return (cn, cn.cursor())

def exists(username, domain, sqlite_path):
    _, cr = initdb(sqlite_path)
    q  = 'SELECT username FROM authreg WHERE username="%s" AND realm="%s"' % (username, domain)
    has_user = True if len(cr.execute(q).fetchall()) > 0 else False
    return has_user

def adduser(username, domain, pwd, sqlite_path):
    cn, cr = initdb(sqlite_path)
    q  = 'INSERT INTO authreg VALUES(?,?,?)'
    cr.execute(q, (username, domain, pwd))
    cn.commit()
    print "Created user %s " % username
