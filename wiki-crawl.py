
import mwclient
import getpass
from pprint import pprint

import os
import argparse
import sortedWalk
import mw_templates as mwt

#p = getpass.getpass()
p='strontium90'
site = mwclient.Site('atomcool.rice.edu', path='/atomwiki/')
site.login('lithium',p)

maxlevel = 5
maxfiles = 8000

if __name__ == "__main__":
   parser = argparse.ArgumentParser('wiki-crawl.py')
   parser.add_argument('path',action="store",type=str, help='path to start the crawl')
   parser.add_argument('--dryrun',action='store_true')

   args=parser.parse_args()

  
   count = 0 
   for root, dirs, files in sortedWalk.sortedWalk(args.path):
      level = len(root.split(os.sep))
      print "DIRECTORY LEVEL = %d" %  level
      if level > maxlevel:
          continue

      # Add directories
      if count < maxfiles: 
          count =  count + 0
          print 
          print "----- NAVIGATING: %s -----" % root
          if root.startswith('/lab/'):
              pagepath = root[ len('/lab/'):]
          else:
              print  "\tUnrecognized root path. "
              continue
          parent = os.path.split( pagepath )[0]
          
          print "\tpagepath = %s" % pagepath
          print "\tparent = %s" % parent
 
          page = site.Pages[ pagepath ] 
          if page.exists:
              content = page.edit() 
              pre     = content.split(mwt.dir_start)[0]
              dirlist = content.split(mwt.dir_start)[1].split(mwt.dir_end)[0]
              post    = content.split(mwt.dir_start)[1].split(mwt.dir_end)[1]
          else:
              dirlist = mwt.dir_list( pagepath, dirs)
              print dirlist
              if parent is not '':
                  newcontent = mwt.navigateup_line( parent ) 
              else:
                  newcontent = '' 
              newcontent = newcontent + mwt.dir_start + dirlist + mwt.dir_end + mwt.table_start + mwt.table_end 
              print "\tCreating new page: %s" % pagepath
              page.save( newcontent, summary='Created page : %s' % pagepath)
                
                 

      # Add files 
      for name in files: 
         if count < maxfiles:
            fname = os.path.join(root, name)
            print 
            print  "----- FILE FOUND -----\n\tname = %s" % fname

            pathstruct = os.path.split( fname )[0].replace( args.path, '', 1).split(os.sep)
            filename, extension   = os.path.splitext(fname.replace( args.path, '', 1).split(os.sep)[-1])
            
            categories = []
            if extension == '.sch': 
                categories.append('Schematics')
            if extension == '.pcb':
                categories.append('PCBFiles') 
            if extension in ( '.xls' , '.xlsx'):
                categories.append('ExcelSpreadsheet')
            if 'emt1' in pathstruct:
                categories.append('EMT1_Hardware')
            if 'emt2' in pathstruct:
                categories.append('EMT2_Hardware')
            if 'app3' in pathstruct:
                categories.append('APP3_Hardware')
           

            print "\ttags = ", categories

            page = site.Pages[ 'hardware/' + '/'.join(pathstruct)]
            content = page.edit()
         
            

            if mwt.table_start in content:
                pre   = content.split(mwt.table_start)[0]
                table = content.split(mwt.table_start)[1].split(mwt.table_end)[0]
                post  = content.split(mwt.table_start)[1].split(mwt.table_end)[1]

                if name in table:
                    print "\tFile already in table."
                    mwt.upload_with_check( site, fname, name, categories) 
                    
                else:
                    print "\tAdding file to table..."
                    newcontent = pre + mwt.table_start +  mwt.table_line(name, extension) \
                                 + table + mwt.table_end +  post
                    page.save( newcontent, summary='Added file: %s' % name)
                    mwt.upload_with_check( site, fname, name, categories)
 
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
  

