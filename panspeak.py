#!/usr/bin/python

from subprocess import call
import re

documento = 'escrito'






def compilar(modo, cadena):

  patron = re.compile(r'#-(?P<writed>.*?)\|(?P<talked>.*?)-#')   
  aciertos = re.finditer(patron, cadena)


  if aciertos:
    print "Hubo " + str(aciertos) + " coincidencias"
    print "\n"

    for iter in aciertos:
      print "writed: " + iter.group('writed')
      print "talked: " + iter.group('talked')
      print "-----------------------"
    		
      if modo == 'escrito':
        reemplazo = iter.group('writed')
      elif modo == 'hablado':
        reemplazo = iter.group('talked')
    
      cadena = patron.sub(reemplazo.strip(), cadena, count = 1)

    return cadena
  else:
    print "No hubo coincidencias"
 
def main():
  print "Panspeak 0.1"
  print "============"
  print "\n"

  cadena = "Este es un texto #- escrito | hablado -# en el que tengo que elejir si digo #- 1 | un -# #- m | metro -#."
  print compilar("hablado", cadena)
  call(["espeak", "-v", "es", compilar("hablado", cadena)])
main()

