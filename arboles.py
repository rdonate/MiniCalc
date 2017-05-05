#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errores
import sys
import tipos

class Arbol:
  pass

class Entero(Arbol):
  def __init__(self, v):
    self.v= v

  def compsemanticas(self):
    self.tipo= tipos.Entero

  def evalua(self):
    return self.v

  def __str__(self):
    return str(self.v)

class Real(Arbol):
  def __init__(self, v):
    self.v= v

  def compsemanticas(self):
    self.tipo= tipos.Real

  def evalua(self):
    return self.v

  def __str__(self):
    return str(self.v)

class Cadena(Arbol):
  def __init__(self, v):
    self.v= v

  def compsemanticas(self):
    self.tipo= tipos.Cadena

  def evalua(self):
    return self.v

  def __str__(self):
    return '"%s"' % self.v

class Suma(Arbol):
  def __init__(self, i, d):
    self.i= i
    self.d= d

  def compsemanticas(self):
    self.i.compsemanticas()
    self.d.compsemanticas()
    if self.i.tipo!= self.d.tipo:
      if (self.i.tipo ==tipos.Real and self.d.tipo==tipos.Entero) or (self.i.tipo ==tipos.Entero and self.d.tipo==tipos.Real):
        self.tipo=tipos.Real
      else:
        raise errores.ErrorSemantico("No puedo sumar peras con limones ni cadenas con enteros")
    self.tipo= self.i.tipo

  def evalua(self):
    return self.i.evalua()+self.d.evalua()

  def __str__(self):
    return "(%s+%s)" % (self.i, self.d)

class Resta(Arbol):
  def __init__(self, i, d):
    self.i= i
    self.d= d

  def compsemanticas(self):
    self.i.compsemanticas()
    self.d.compsemanticas()
    if self.i.tipo== self.d.tipo:
      self.tipo=self.i.tipo
    elif (self.i.tipo ==tipos.Real and self.d.tipo==tipos.Entero) or (self.i.tipo ==tipos.Entero and self.d.tipo==tipos.Real):
      self.tipo=tipos.Real
    elif self.tipo!=tipos.Real:
      self.tipo= self.i.tipo
    else:
      raise errores.ErrorSemantico("No puedo restar peras con limones ni cadenas con enteros")


  def evalua(self):
    return self.i.evalua()-self.d.evalua()

  def __str__(self):
    return "(%s-%s)" % (self.i, self.d)

class Producto(Arbol):
  def __init__(self, i, d):
    self.i= i
    self.d= d

  def evalua(self):
    return self.i.evalua()*self.d.evalua()

  def compsemanticas(self):
    self.i.compsemanticas()
    self.d.compsemanticas()
    if self.i.tipo==tipos.Cadena and self.d.tipo==tipos.Cadena:
      raise errores.ErrorSemantico("¿Y cómo multiplico yo dos cadenas?")
    elif self.i.tipo==tipos.Entero and self.d.tipo==tipos.Entero:
      self.tipo= tipos.Entero
    elif (self.i.tipo==tipos.Real and self.d.tipo==tipos.Entero) or (self.i.tipo==tipos.Entero and self.d.tipo==tipos.Real) or (self.i.tipo==tipos.Real and self.d.tipo==tipos.Real):
      self.tipo=tipos.Real
    else:
      self.tipo= tipos.Cadena

  def __str__(self):
    return "(%s*%s)" % (self.i, self.d)

class Division(Arbol):
  def __init__(self, i, d):
    self.i= i
    self.d= d

  def evalua(self):
    return self.i.evalua()/self.d.evalua()

  def compsemanticas(self):
    self.i.compsemanticas()
    self.d.compsemanticas()
    if self.i.tipo==tipos.Cadena and self.d.tipo==tipos.Cadena:
      raise errores.ErrorSemantico("¿Y cómo divido yo dos cadenas?")
    if self.i.tipo==tipos.Entero and self.d.tipo==tipos.Entero:
      self.tipo= tipos.Entero
    elif (self.i.tipo==tipos.Real and self.d.tipo==tipos.Entero) or (self.i.tipo==tipos.Entero and self.d.tipo==tipos.Real) or (self.i.tipo==tipos.Real and self.d.tipo==tipos.Real):
      self.tipo=tipos.Real
    else:
      self.tipo= tipos.Cadena

  def __str__(self):
    return "(%s/%s)" % (self.i, self.d)

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