## -------------------------------------------
## package  : cdwcore
## author   : kaushik@mailbox.sc.edu
## created  : Tue Mar  8 08:17:12 EST 2016
## vim      : ts=4


import os, sys
import unittest
import mock

sys.path.insert(0,os.path.abspath(__file__+"/../../src"))

def _mock_pg_lscluster():
    import opsys
    (o,e,p,r) = opsys.runCommand('/bin/true')
    cluster_status = "9.2 main    5432 down   postgres /var/lib/postgresql/9.2/main /var/log/postgresql/postgresql-9.2-main.log"
    o = cluster_status
    return (o,e,p,r)

def _mock_cx_Oracle_connect(val):
    return val


class cdwcore_test(unittest.TestCase):

    ## unit test for logger
    def test_logger(self):
        import logger

        ## init a logfile using module
        logf = 'log_test.txt'
        if os.path.exists(logf):
            os.remove(logf)
        log = logger.logInit(logf, 2);

        ## check logfile was created
        self.assertEqual(os.path.exists(logf), True);
        if log:
            log.info('this is an info line')
            log.error('this is an error line')

        self.assertEqual(os.stat(logf).st_size, 104)
        os.remove(logf)

    ## unit test for config
    def test_config(self):
        import config

        inpf = 'config_test.csv'
        comp = [ {'var1a': 'value1A', 'var2a': 'value2A'}, {'var2b': 'value2B'} ]
        secs = ['sectionA', 'sectionB']

        ## create an ini file to parse
        with open(inpf, 'w') as f:
            f.write('\n;comment A\n[sectionA]\nvar1A: value1A\nvar2A: value2A\n\n[sectionB]\nvar2B: value2B\n\n')
            f.close()

        ## parse ini file using module and compare sections, vars
        cfg_parse = config.getConfigParser(inpf)
        self.assertEqual(cfg_parse.sections(), secs)
        rep = []
        for item in cfg_parse.sections():
            rep.append( config.getConfigSectionMap(cfg_parse, item) )
        self.assertEqual(rep, comp)

        comp = [{'col2': 'b', 'col3': 'c', 'col1': 'a'}, {'col2': 'e', 'col3': 'f', 'col1': 'd'}, {'col2': 'h', 'col3': 'i', 'col1': 'g'}]
        with open(inpf, 'w') as f:
            f.write('#this is a comment\n\ncol1,col2,col3\na, b, c\nd, e, f\ng, h, i\n')
            f.close()
        data = config.parseCSV(inpf)
        self.assertEqual(data, comp)
        os.remove(inpf)

    ## unit test for opsys
    def test_opsys(self):
        import opsys

        self.assertEqual( opsys.pingHost('127.0.0.1'), 0)
        self.assertEqual( opsys.pingHost('gogooolllmy.com'), 1)

        (o, e, p, r) = opsys.runCommand('echo running')
        self.assertEqual(p.returncode, 0)
        self.assertEqual(o.strip(), 'running')

        r,i,v = opsys.parseIP()
        self.assertEqual(r, 0)
        c = opsys.canonify('127.0.0.1')
        self.assertEqual(c, '127_0_0_1')

        fqdn = opsys.hostFQDN()
        assert fqdn['short'] is not None
        assert fqdn['site'] is not None

        sfilename = 'setup.py'
        setup_file = sys.modules['__main__'].__file__
        flist = opsys.fileMatch(os.path.abspath(os.path.dirname(setup_file)),sfilename)
        self.assertEqual(len(flist), 1)
        self.assertEqual(flist[0], sfilename)

    ## unit test for dbmath
    def test_dbmath(self):
        import dbmath
        val, unit = dbmath.convertbytes(936698)
        self.assertEqual(round(val,0), 915)
        self.assertEqual(unit, 'KB')


    ## unit test for timef
    def test_timef(self):
        import timef
        import datetime, time
        t = timef.timeConvert()

        ## choose a certain time
        a = datetime.datetime.utcnow()
        self.assertEqual( a, t.ts2utc(t.utc2ts(a)))

        ## get utc offset of this host
        is_dst = time.daylight and time.localtime().tm_isdst > 0
        utc_offset = - (time.altzone if is_dst else time.timezone)
        self.assertEqual( t.utc2local(a), a+datetime.timedelta(seconds=utc_offset))


    ## unit test for pgdb
    def test_pgdb(self):
        import pgdb, opsys
        (o,r,p,r) = _mock_pg_lscluster()
        if p.returncode == 0:
            pars = o.split()
            if len(pars) > 5:
                if pars[3] == 'online':
                    ## this should go in functional tests at some point (ctrl never reaches here for unit test) -- vsk
                    conn = 'dbname=\'postgres\' user=\''+pars[4]+'\' port='+pars[2]
                    h = pgdb.pgdb(conn)
                    self.assertEqual(not h, False)
                    a = pgdb.pgquery(h, 'select 1')
                    self.assertEqual( a[0][0], 1)

    ## unit test for oradb
    def test_oradb(self):
        import cx_Oracle
        @mock.patch('cx_Oracle.connect', side_effect=_mock_cx_Oracle_connect)
        def test_conn(self, connect_function):
            conn_str = 'user/pw@host:port/sid'
            assert cx_Oracle.connect(conn_str) == conn_str



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(cdwcore_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
