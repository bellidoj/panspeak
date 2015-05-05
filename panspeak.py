#!/usr/bin/python

from subprocess import call
import re
import argparse

parser = argparse.ArgumentParser(prog='Panspeak')
parser.add_argument('--speech',
    action='store_true',
     help='speech help')

parser.add_argument('--text',
    action='store_true',
    help='text help')

args = parser.parse_args()



def translate(mode, document):

  pattern = re.compile(r'#-(?P<text>.*?)\|(?P<speech>.*?)-#')   
  matches = re.finditer(pattern, document)

  if matches:
      if mode == 'text':
        for iter in matches:
          change = iter.group('text')
          document = pattern.sub(change.strip(), document, count = 1)
        print document
      if mode == 'speech':
        for iter in matches:
          change = iter.group('speech')
          document = pattern.sub(change.strip(), document, count = 1)
        call(["espeak", "-v", "es", document])

  else:
    print "There was no matches"
 
def get_mode():
  if args.speech:
    return "speech"
  elif args.text:
    return "text"
       
def main():
  print "Panspeak 0.1"
  print "============"
  print "\n"

  document_mode = get_mode()
  document = "Este es un texto #- escrito | hablado -# en el que tengo que elejir si digo #- 1 | un -# #- m | metro -#."
  translate(document_mode, document)

main()

