#!/usr/bin/env python3
import json
import argparse
from os import path
from os import getcwd
from os import listdir
from os import makedirs
from os import stat
from os import utime

def getJsonFiles(a):
  if path.splitext(a)[1] == ".json":
    return True

def main():
  parser = argparse.ArgumentParser(description='This is a small tool to convert exported noted from Google Keep to the text format')
  parser.add_argument('-d','--dst_dir',required=False,action='store',help='Destination folder (default current)',default=getcwd())
  parser.add_argument('-s','--src_dir',required=True,action='store',help='Source folder with JSON files')
  parser.add_argument('-i','--ignore_tags',required=False,action='store_true',help='Ignore Keep tags. Put all files together. By deault files are placed under sub-tag-folders')
  args = parser.parse_args()

  for f in filter(getJsonFiles, listdir(args.src_dir)):
    fname, fext = path.splitext(f)
    newname = "{}.txt".format(fname)
    srcfp = path.join(args.src_dir,f)
    srcstat = stat(srcfp)
    with open(srcfp,'r') as scrfile:
      jo = json.loads(scrfile.read())
   
      if (args.ignore_tags):
        dstfp = path.join(args.dst_dir,newname)
      else:
        if not 'labels' in jo:
          dstfolder = args.dst_dir
        else:
          folder = jo['labels'][0]['name'] # Take only first tag
          dstfolder = path.join(args.dst_dir,folder)
        
        if not path.exists(dstfolder):
          makedirs(dstfolder)
        dstfp = path.join(dstfolder,newname)

      with open(dstfp,'w') as dstfile:
        if 'listContent' in jo:
          for item in jo['listContent']:
            dstfile.write('[{}] {}\n'.format('x' if item['isChecked'] else ' ' ,item['text']))
        elif 'textContent' in jo:
          dstfile.write('{}\n'.format(jo['textContent']))
        else:
          print('UNKNOWN {}'.format(f))
        dstfile.close()
      utime(dstfp, times=(srcstat.st_atime, srcstat.st_mtime))
# times must have two floats (unix timestamps): (atime, mtime)

    
if __name__ == "__main__":
  main()