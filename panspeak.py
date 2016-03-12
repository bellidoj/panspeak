#!/usr/bin/env python3

from subprocess import call
import re
import argparse

parser = argparse.ArgumentParser(prog='panspeak.py')

parser.add_argument('--mode', help='mode help')
parser.add_argument('--input', help='input help')
parser.add_argument('--output', help='output help')

args = parser.parse_args()

def translate(mode, document):
  output_file = open(args.output, 'w')
  pattern = re.compile(r'#-(?P<text>.*?)\|(?P<speech>.*?)-#')
  input_file = open(document, 'r')
 

  for line in input_file.readlines():
    if not line.strip():
      output_file.write('\n')
    else:
      while True:
        match = re.search(pattern, line)
        # sustituye el patron por el grupo una unica vez
        # si no hay coincidencia continua buscando mas patrones en esa linea 
        if match: 
          line = re.sub(pattern, match.group(mode), line, 1)
        else:
          break

      output_file.write(line)

  output_file.close()
  panete = open(args.output, 'r')
  # print panete.read()
  data = panete.read()
  call(["espeak", "-v", "es", "-w", "panete.wav", data])

def get_mode():
  mode = str(args.mode)  
  if mode == "speech":
    mode = 1
  elif mode == "text":
    mode = 2
  else:
    mode = 1
  return int(mode)

def get_file():
  file_object = open(args.input, 'r')
  return file_object

def main():
  print "Panspeak 0.1"
  print "============"
  print "\n"
  print "Analyzing " + str(args.input) + " in " + str(args.mode) + " mode."

  translate(get_mode(), str(args.input))

main()
