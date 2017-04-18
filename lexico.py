#!/usr/bin/env python
# -*- coding: utf-8 -*-

import componentes
import errores
import flujo
import string
import sys

class Lexico:
  def __init__(self, flujo):
    self.flujo= flujo
    self.poserror= 0

  def siguiente(self):
    q= 0
    l= ""
    self.poserror= self.flujo.posleida()+1
    while 1:
      c= self.flujo.siguiente()
      l+= c
      if q== 0:
        if c== "+" or c=="-":
          q= 1
        elif c== "*" or c=="/":
          q= 2
        elif c and c in string.digits:
          q= 3
        elif c== "(":
          q= 4
        elif c== ")":
          q= 5
        elif c and c in " \t":
          q= 6
        elif c== "\"":
          q= 7
        elif c== "\n":
          q= 9
        elif c== "":
          q= 10
        elif c=="|":
          q=11
        else:
          raise errores.ErrorLexico("Carácter inesperado.")
      elif q== 1:
        self.flujo.devuelve(c)
        return componentes.opad(l[0])
      elif q== 2:
        self.flujo.devuelve(c)
        return componentes.opmul(l[0])
      elif q== 3:
        if c and c in string.digits:
          pass # q= 3
        elif c==".":
          q=16
        else:
          self.flujo.devuelve(c)
          if c:
            v= int(l[:-1])
          else:
            v= int(l)
          return componentes.entero(v)
      elif q== 4:
        self.flujo.devuelve(c)
        return componentes.abre()
      elif q== 5:
        self.flujo.devuelve(c)
        return componentes.cierra()
      elif q== 6:
        self.flujo.devuelve(c)
        q= 0
        l= ""
        self.poserror= self.flujo.posleida()+1
      elif q== 7:
        if c and c not in "\"\n\\":
          pass # q= 7
        elif c== "\"":
          q= 8
        elif c=="\\":
          c = self.flujo.siguiente()
          if c=="\"":
            l=l[:-1]
            l+=c
          elif c=="\\":
            l = l[:-1]
            l += c
        else:
          self.flujo.devuelve(l[1:])
          raise errores.ErrorLexico("Cadena no terminada.")
      elif q== 8:
        self.flujo.devuelve(c)
        v= l[1:-len(c)-1]
        return componentes.cadena(v)
      elif q== 9:
        self.flujo.devuelve(c)
        return componentes.nl()
      elif q== 10:
        self.flujo.devuelve(c)
        return componentes.eof()
      elif q==11:
        #l=l[1:]
        self.flujo.devuelve(c)
        q = 12
        return componentes.abrirBarra()
      elif q==12:
        if c and c in string.digits:
          q=13
        elif c and c not in string.digits:
          q=14
      elif q==13:
        if c and c in string.digits:
          pass
        elif c=="|":
          #l=l[:-1]
          self.flujo.devuelve(c)
          q = 15
          return componentes.entero(l[1:-1])
        elif c==".":
          q=17
      elif q==14:
        if c=="|":

          #l=l[:-1]
          self.flujo.devuelve(c)
          q = 15
          v = l[1:-len(c) - 1]
          return componentes.cadena(v)
        else:
          pass
      elif q==15:
        self.flujo.devuelve(c)
        return componentes.cerrarBarra()
      elif q==16:
        if c and c in string.digits:
          pass
        else:
          self.flujo.devuelve(c)
          if c:
            v = float(l[:-1])
          else:
            v = float(l)
          return componentes.real(v)
      elif q==17:
        if c and c in string.digits:
          pass
        elif c=="|":
          q=15
          l=l[:-1]
          self.flujo.devuelve(l)
          return componentes.real(l)
        else:
          self.flujo.devuelve(l)
          raise errores.ErrorLexico("Cadena no terminada.")


  def muestraError(self, f):
    cad= self.flujo.cadena()
    if cad[-1]== "\n":
      cad= cad[:-1]
    f.write("%s\n%s%s\n" % (cad, " "*self.poserror,
                            "^"*(self.flujo.posleida()-self.poserror+1)))

if __name__=="__main__":
  linea= sys.stdin.readline()
  while linea:
    fl= flujo.Flujo(linea)
    lexico= Lexico(fl)

    while 1:
      try:
        c= lexico.siguiente()
        print c
        if c.cat=="eof":
          break
      except errores.Error, err:
        sys.stderr.write("%s\n" % err)
        lexico.muestraError(sys.stderr)
    linea= sys.stdin.readline()
