#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import sys

class Componente:
  def __init__(self):
    self.cat= str(self.__class__.__name__)

  def __str__(self):
    s=[]
    for k,v in self.__dict__.items():
      if k!= "cat": s.append("%s: %s" % (k,v))
    if s:
      return "%s (%s)" % (self.cat,", ".join(s))
    else:
      return self.cat

class opad(Componente):
  def __init__(self, opad):
    Componente.__init__(self)
    self.operacion = opad

class opmul(Componente):
  def __init__(self,opmul):
    Componente.__init__(self)
    self.operacion = opmul

class nl(Componente):
  pass

class abrirBarra(Componente):
  pass

class cerrarBarra(Componente):
  pass

class eof(Componente):
  pass

class entero(Componente):
  def __init__(self,v):
    Componente.__init__(self)
    self.valor= v

class real(Componente):
  def __init__(self,v):
    Componente.__init__(self)
    self.valor= v

class cadena(Componente):
  def __init__(self,v):
    Componente.__init__(self)
    self.valor= v

class abre(Componente):
  pass

class cierra(Componente):
  pass

if __name__=="__main__":
# Ejemplo evaluable: entero(5)
  linea= sys.stdin.readline()
  while linea:
    try:
      c=eval(linea)
    except:
      sys.stderr.write("Imposible evaluar como componente.\n")
    else:
      print "Componente: %s" % c
    linea= sys.stdin.readline()
