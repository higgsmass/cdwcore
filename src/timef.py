## -------------------------------------------
## module   : time / date converter class
## package  : cdwcore
## author   : kaushik@mailbox.sc.edu
## created  : Tue Mar  8 08:17:12 EST 2016
## vim      : ts=4

import datetime, time

class timeConvert(object):
  # time conversion utils

  # Convert UTC to timestamp
  def utc2ts(self, dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    timestamp = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)/1e6
    return timestamp

  # Convert timestamp to UTC
  def ts2utc(self, ts):
    return datetime.datetime.utcfromtimestamp(ts)

  # Get time (dt) now
  def tnow(self):
    return datetime.datetime.now()

  # Convert UTC to localtime
  def utc2local(self,utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
    return utc + offset

