
import mwclient
import getpass
from pprint import pprint

import os
import argparse

#p = getpass.getpass()
p='strontium90'

site = mwclient.Site('atomcool.rice.edu', path='/atomwiki/')
site.login('lithium',p)


if __name__ == "__main__":
   parser = argparse.ArgumentParser('wiki-crawl.py')
   parser.add_argument('path',action="store",type=str, help='path to start the crawl')
   args=parser.parse_args() 
  
   count = 0 
   for root, dirs, files in os.walk(args.path):
      for name in files: 
         if count < 5:
            fname = os.path.join(root, name)
            print  "Found ", fname
            print os.path.split( fname )[0].replace( args.path, '', 1).split(os.sep)
            print fname.replace( args.path, '', 1).split(os.sep)
            print  fname.split(os.sep)
            count = count + 1
         
      #print root, "consumes",
      #print sum(os.path.getsize( os.path.join( root, name)) for name in files),
      #print "bytes in", len(files), "non-directory files"
      #if 'CVS' in dirs:
      #   dirs.remove('CVS') #don't visit CVS directories.

exit(1)


#print dir(site)

for exp in ['App3', 'EMT1', 'EMT2']:
  pgs = site.search('Notebooks:' + exp)
  #print pgs
#  for counter in range(2):
#    pg = pgs.next()
  for pg in pgs:
    if 'Notebooks:' + exp +'/' in pg['title']:
      page = site.Pages[pg['title']]
      #pprint (pg)
      text = page.edit()
      if u'[[Category:' + exp + 'Notebook]]' not in text:
        print "Adding %s to " % pg['title'] + exp + " category" 
        newline = "[[Category:" + exp + "Notebook]]\n\n"
        page.save( newline + text, summary='Added to ' + exp + 'Notebook category.')
  

