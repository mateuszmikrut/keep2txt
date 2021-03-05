#!/usr/bin/env python3
import json
import argparse
from os import path
from os import getcwd
from os import listdir
from os import makedirs

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
    with open(srcfp,'r') as scrfile:
      jo = json.loads(scrfile.read())
   
      if (args.ignore_tags):
        dstfp = path.join(args.dst_dir,newname)
      else:
        if not 'labels' in jo:
          folder = 'NoCategory'
          dstfolder = path.join(args.dst_dir,folder)
        else:
          folder = jo['labels'][0]['name'] # Take only first tag
          dstfolder = path.join(args.dst_dir,folder)
          if not path.exists(dstfolder):
            makedirs(dstfolder)
        dstfp = path.join(dstfolder,newname)

      if 'listContent' in jo:
        with open(dstfp,'w') as dstfile:
          for item in jo['listContent']:
            dstfile.write('[{}] {}\n'.format('x' if item['isChecked'] else ' ' ,item['text']))
          dstfile.close()

      elif 'textContent' in jo:
        with open(dstfp,'w') as dstfile:
          dstfile.write('{}\n'.format(jo['textContent']))
          dstfile.close()
      else:
        print('UNKNOWN {}'.format(f))
    
if __name__ == "__main__":
  main()