
# Some useful strings related to directory list manipulation

def navigateup_line( rootpage):
    return u"<big>'''[[%s|Navigate Up]]'''</big>\n\n" % rootpage

dir_start = u'<small>--List of directories--</small>\n\n'
dir_end   = u'<small>--End directories--</small>\n\n'

def dir_line(parent, dirname):
    return u'[[%s|%s]]\n\n' % ( '/'.join((parent,dirname)), os.path.split(dirname)[1] )

def dir_list(parent, dirs):
    dirlist = ''
    for d in dirs:
        dirlist = dirlist + dir_line(parent, d)
    return dirlist

# Some useful strings related to table manipulation

table_start01 = u'{| class="wikitable sortable" border="1"'
table_start02 = u'|+ List of files'
table_start03 = u'|-'
table_start04 = u'! scope="col" | File Name'
table_start05 = u'! scope="col" | Extension'
table_start06 = u'! scope="col" | Last Uploaded'

table_start = '\n'.join( (table_start01, table_start02, table_start03, table_start04, table_start05, table_start06) )

table_linesep = u'|-'

def table_line( name, extension ):
    return u'\n' + table_linesep + u'\n' + u'| [[:File:%s | %s ]] || %s || %s\n' % (name, name, extension, now.strftime("%Y-%m-%d %H:%M.%S") )

table_end = u'\n|}'


# Function to upload a file and assign categories to it


import datetime
from dateutil import tz
now = datetime.datetime.now()
import os

from_zone = tz.tzutc()
to_zone = tz.tzlocal()
	

validExtensions =  ['zip','tgz','png', 'gif', 'jpg', 'jpeg', 'pdf', 'xls', 'ppt', 'doc', 'xlsx', 'pptx', 'docx', 'm', 'dwg', 'dxf', 'nb', 'opj', 'vi', 'ps', 'tiff', 'eps', 'tif', 'bmp', 'mpg', 'svg', 'sch', 'txt', 'dat']

def upload( site, fname, name, categories, ignore=False):
    desc = ''
    for c in categories:
        desc = desc + '[[Category:%s]]' % c 
    return site.upload( open(fname), name, desc, ignore=ignore)

def upload_with_check( site, fname, name, categories, ignore=False):
    filename, extension   = os.path.splitext(fname)
    # Does file exist in wiki?
    wikiFile = site.Images[name]
    if not wikiFile.exists:
	if extension.strip('.') in validExtensions:
            if  os.path.getsize( fname) > 20000000.:
                print "\tFile is too large and will not be uploaded to wiki.  File size = ", os.path.getsize(fname), "bytes"
                return
	    print "\tUploading file to wiki for the first time..."
            try:
	       upload( site, fname, name, categories, ignore=True)
            except:
               print "\tA problem occurred uploading file.  Sorry."
	else:
	    print "\tFile extension not supported. Ignoring this file"  
    else:
        date = wikiFile.imageinfo['timestamp']
        day  =  date.split('T')[0]
        time =  date.split('T')[1].strip('Z')
        utc = datetime.datetime.strptime(day + ' ' + time, '%Y-%m-%d  %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)
         
        print "\tFile exists on wiki.  Last version:", central.strftime('%Y-%m-%d  %H:%M:%S')

        statbuf = os.stat( fname )
        moddate = datetime.datetime.fromtimestamp( statbuf.st_mtime )
        moddate = moddate.replace(tzinfo=to_zone)
        print "\tModification time on disk:", moddate.strftime('%Y-%m-%d  %H:%M:%S')

        if moddate > central:
	    print "\tUploading new version of file to wiki..."
            try:
                upload( site, fname, name, [], ignore=True)
            except:
               print "\tA problem occurred uploading file.  Sorry."

 
