## -------------------------------------------
## module   : useful math / conversion functions
## package  : cdwcore
## author   : kaushik@mailbox.sc.edu
## created  : Tue Mar  8 08:17:12 EST 2016
## vim      : ts=4


# ------------------------------------------------
def convertbytes(tbyte):

    ## conversion factors
    facs = { 'PB':1125899906842624, 'TB':1099511627776, 'GB':1073741824, 'MB':1048576, 'KB':1024, 'B':1 }

    if tbyte > facs['PB']:
        return( float(tbyte)/facs['PB'], 'PB' )
    elif tbyte > facs['TB']:
        return( float(tbyte)/facs['TB'], 'TB' )
    elif tbyte > facs['GB']:
        return( float(tbyte)/facs['GB'], 'GB' )
    elif tbyte > facs['MB']:
        return( float(tbyte)/facs['MB'], 'MB' )
    elif tbyte > facs['KB']:
        return( float(tbyte)/facs['KB'], 'KB' )
    else:
        pass
    return (float(tbyte)/facs['B'], 'B')

