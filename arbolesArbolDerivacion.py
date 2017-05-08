#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errores
import sys
import tipos

class Arbol:
  pass

class entero(Arbol):
  def __init__(self, v):
    self.v= v

  def evalua(self):
    return '("' + self.__class__.__name__ + '")'

class real(Arbol):
  def __init__(self, v):
    self.v= v

  def evalua(self):
    return '("'+self.__class__.__name__+'")'

class cadena(Arbol):
  def __init__(self, v):
    self.v= v

  def evalua(self):
    return '("' + self.__class__.__name__ + '")'

class opad(Arbol):
  def __init__(self, i,d):
    self.i = i
    self.d = d

  def evalua(self):
    return '("' + self.__class__.__name__ + '") ' + self.d.evalua()

class nl(Arbol):
  def __init__(self):
    pass

  def evalua(self):
    return '("'+self.__class__.__name__+'")'

class opmul(Arbol):
  def __init__(self, i,d):
    self.i = i
    self.d = d

  def evalua(self):
    return '("' + self.__class__.__name__ + '") ' + self.d.evalua()

class apar(Arbol):
  def __init__(self,i,d):
    self.i=i
    self.d=d

  def evalua(self):
    return '(("' + self.__class__.__name__ +'") '+self.i.evalua()+' '+ ' ' + self.d.evalua()+ ')'

class cpar(Arbol):
  def __init__(self):
    pass

  def evalua(self):
    return '("' + self.__class__.__name__ + '")'

class barra(Arbol):
  def __init__(self,i):
    self.i=i

  def evalua(self):
    return '("' + self.__class__.__name__ +'") '+self.i.evalua()+' ("'+self.__class__.__name__+ '")'

class Linea(Arbol):
  def __init__(self,i,d):
    self.i=i
    self.d=d

  def evalua(self):
    return '("' + self.__class__.__name__ + '" ' + self.i.evalua() + ' ' + self.d.evalua() + ')'

class Expresion(Arbol):
  def __init__(self,i,d):
    self.i=i
    self.d=d

  def evalua(self):
    return '("'+self.__class__.__name__+'" '+self.i.evalua()+' '+self.d.evalua()+')'

class Termino(Arbol):
  def __init__(self,i,d):
    self.i=i
    self.d=d

  def evalua(self):
    return '("'+self.__class__.__name__+'" '+self.i.evalua()+' '+self.d.evalua()+')'

class Factor(Arbol):
  def __init__(self,i):
    self.i=i

  def evalua(self):
    return '("'+self.__class__.__name__+'" '+self.i.evalua()+')'

def arbol():
  pass

if __name__=="__main__":
# Ejemplo evaluable: Suma(Entero(5), Producto(Suma(Entero(6), Entero(7))))
  linea= sys.stdin.readline()
  while linea:
    try:
      a=eval(linea)
    except:
      sys.stderr.write("Imposible evaluar como árbol.\n")
    else:
      try:
        a.compsemanticas()
        va=a.evalua()
        print a,"=",va
      except errores.ErrorSemantico, err:
        sys.stderr.write("%s\n" % err)
    linea= sys.stdin.readline()