## -------------------------------------------
## module   : collection of os/sys related functions and classes
## package  : cdwcore
## author   : kaushik@mailbox.sc.edu
## created  : Tue Mar  8 08:17:12 EST 2016
## vim      : ts=4

#-----------------------------------------------------------------------------------
# Run system command and get output, error, process handle and resource usage handle
def runCommand(cmd, rUsage=False):
  from subprocess import Popen, PIPE, STDOUT
  from resource import getrusage,RUSAGE_SELF,RUSAGE_CHILDREN
  res = None
  out = None
  err = None
  try:
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    p.wait()
  except OSError:
    print (err)
    sys.exit(p.returncode)
  (out, err) = p.communicate()
  if rUsage:
    res = getrusage(RUSAGE_CHILDREN)
  return (out, err, p, res)


#------------------------------------
## Send ICMP ECHO_REQUEST
def pingHost(HostIP, Verbose=False):
    import sys, opsys
    #from cdwcore import opsys

    ## note, only root can ping with i < 1 and so we restrict
    #if not (HostIP and os.geteuid()==0):
    if not (HostIP):
        return 1
    cmd = 'ping -s 4 -c 2 -i 0.25 -q -w 1 %s > /dev/null 2>&1; echo $?' %  HostIP
    try:
        out, err, p, res = opsys.runCommand(cmd)
        out = out.strip()
    except OSError:
        print (err)
        sys.exit(p.returncode)
    if out == '0':
        return 0
    else:
        return 1

#-------------------------------------------------------------------------
## parse IP config and return device/interface list/dictionary with status
def parseIP():

    vdev = {}
    ifaces=[]
    out = None
    try:
        out, err, p, res = runCommand('/bin/ip address show')
    except OSError:
        raise
        return (p.returncode, ifaces, vdev)

    for line in out.splitlines():
        line_stripped=line.strip()
        line_split=line_stripped.split()
        if line_stripped[0].isdigit():
            cur_iface=line_stripped.split(':')[1].strip()
            ifaces.append(cur_iface)
            vdev[cur_iface]={}
        if line_split[0] == "inet":
            vdev_str=line_split.pop()
            vdev[cur_iface][vdev_str]=line_split[1].split("/")[0]
    return (p.returncode, ifaces, vdev)


#-------------------------------------------------------------------------
## get files matching a given pattern in a directory
def fileMatch(tdir, fpattern):
    import fnmatch, os
    flist = None
    if os.path.isdir(tdir):
        flist = fnmatch.filter(os.listdir(tdir), fpattern)
    return flist


#-------------------------------------------------------------------------
## get fully qualified domain name
def hostFQDN():
    import socket
    fqdn = {'short':None, 'site':None, 'domain':None }
    try:
        fq = socket.getfqdn()
        fq = fq.lower()
        fq = fq.split('.')
        l = len(fq)
        if l > 0:
            fqdn['short'] = fq[0]
        if l > 1:
            fqdn['site'] = fq[1]
        if l > 2:
            fqdn['domain'] = '.'.join(fq[1:])
    except:
        raise
    return fqdn

#-------------------------------------------------------------------------
## replace special chars by their canonical equivalents (for cfengine)
def canonify(text, charlist = None):
    ## default char list
    canonify_chars=[ '!','@','#','$','%','^','&','*','(',')','-','=','+','`','~',',','.','?','?','\'','"' ]
    clist = []
    try:
        if not charlist:
            clist = canonify_chars
        if len(charlist) == 0:
            clist = canonify_chars
    except TypeError:
        clist = canonify_chars

    for ch in clist:
        text=text.replace(ch,'_')
    return text


