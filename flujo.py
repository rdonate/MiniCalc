#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Flujo:
  def __init__(self, cad):
    self.cad= cad
    self.pos= -1

  def siguiente(self):
    if self.pos< len(self.cad)-1:
      self.pos+= 1
      return self.cad[self.pos]
    else:
      return ""

  def devuelve(self, c):
    self.pos-= len(c)

  def posleida(self):
    return self.pos

  def cadena(self):
    return self.cad

import sys

if __name__=="__main__":
  linea= sys.stdin.readline()
  while linea and linea!= "\n":
    f= Flujo(linea)
    print "Voy a señalar los espacios:"
    c= f.siguiente()
    while c!= "":
      if c==" ":
        print f.cadena().rstrip()
        print " " * f.posleida()+"^"
        c= f.siguiente()
      c= f.siguiente()
    print "Ahora voy a probar a devolver caracteres al flujo de entrada:"
    f.devuelve(linea)
    l= ""
    for i in range(len(linea)):
      d=""
      for j in range(len(linea)-i):
        c= f.siguiente()
        d+= c
      f.devuelve(d)
      c= f.siguiente()
      l+= c
    if linea != l:
      print "Error:"
      print "  leído:", linea
      print "  reconstruido:", l
    else:
      print "BIEN"
    linea= sys.stdin.readline()
