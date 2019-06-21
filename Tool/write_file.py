#coding:utf-8
import sys
import os.path

if __name__=='__main__':
  target_file = sys.argv[1]
  content = sys.argv[2]
  f = open(target_file,'a')
  f.write(content+"\n")