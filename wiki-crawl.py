
import mwclient
import getpass
from pprint import pprint

import os

#p = getpass.getpass()
p='strontium90'

site = mwclient.Site('atomcool.rice.edu', path='/atomwiki/')
site.login('lithium',p)


for root, dirs, files in os.walk('/home/pmd'):
   print "root = %s, dirs = %s, files = %s", (root, dirs,files)

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
  

