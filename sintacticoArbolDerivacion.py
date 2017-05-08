#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arbolesArbolDerivacion
from errores import Error, ErrorSintactico
import flujo
import lexico
import sys
import componentes

class Sintactico:
  def __init__(self, lexico):
    self.lexico= lexico
    self.componente= self.lexico.siguiente()

  def analizaLinea(self):
    expresion=self.analizaExpresion()
    if self.componente.cat!= "nl":
      raise ErrorSintactico("Ya tengo una expresión, ¿por qué no terminas la línea?")
    arbol = arbolesArbolDerivacion.Linea(expresion,arbolesArbolDerivacion.nl())
    self.componente = self.lexico.siguiente()
    return arbol

  def analizaExpresion(self):
    arbol= self.analizaTermino()
    while self.componente.cat== "opad":
      operacion=self.componente
      self.componente=self.lexico.siguiente()
      termino= self.analizaTermino()
      #self.componente=self.lexico.siguiente()
      opad=arbolesArbolDerivacion.opad(operacion,termino)
      arbol=arbolesArbolDerivacion.Expresion(arbol,opad)
    #self.componente = self.lexico.siguiente()
    return arbol

  def analizaTermino(self):
    arbol= self.analizaFactor()
    while self.componente.cat== "opmul":
      operacion=self.componente
      self.componente=self.lexico.siguiente()
      factor=self.analizaFactor()
      #self.componente = self.lexico.siguiente()
      opmul=arbolesArbolDerivacion.opmul(operacion,factor)
      arbol=arbolesArbolDerivacion.Termino(arbol,opmul)
    #self.componente = self.lexico.siguiente()
    return arbol

  def analizaFactor(self):
    if self.componente.cat=="abre":
      self.componente= self.lexico.siguiente()
      arbol= self.analizaExpresion()
      if self.componente.cat!= "cierra":
        raise ErrorSintactico("Aquí tocaba cerrar un paréntesis.")
      arbol = arbolesArbolDerivacion.apar(arbol,arbolesArbolDerivacion.cpar())
      arbol=arbolesArbolDerivacion.Factor(arbol)
      self.componente=self.lexico.siguiente()
    elif self.componente.cat=="entero":
      arbol= arbolesArbolDerivacion.entero(self.componente.valor)
      self.componente = self.lexico.siguiente()
    elif self.componente.cat=="real":
      arbol = arbolesArbolDerivacion.real(self.componente.valor)
      self.componente = self.lexico.siguiente()
    elif self.componente.cat=="cadena":
      arbol= arbolesArbolDerivacion.cadena(self.componente.valor)
      self.componente = self.lexico.siguiente()
    elif self.componente.cat=="barra":
      self.componente = self.lexico.siguiente()
      componente = self.analizaExpresion()
      #self.componente=self.lexico.siguiente()
      if self.componente.cat!="barra":
        raise ErrorSintactico("Aquí tocaba cerrar una barra.")
      barra=arbolesArbolDerivacion.barra(componente)
      arbol=arbolesArbolDerivacion.Factor(barra)
      self.componente = self.lexico.siguiente()
    elif self.componente.cat=="opad":
      operacion = self.componente
      self.componente = self.lexico.siguiente()
      termino = self.analizaTermino()
      opad = arbolesArbolDerivacion.opad(operacion, termino)
      arbol = arbolesArbolDerivacion.Factor(opad)
      #self.componente = self.lexico.siguiente()
    else:
      raise ErrorSintactico("La verdad, no sé qué hacer con esto.")
    return arbol

if __name__=="__main__":
  l= sys.stdin.readline()
  while l:
    f= flujo.Flujo(l)
    lex= lexico.Lexico(f)
    S= Sintactico(lex)
    try:
      arbol=S.analizaLinea()
      print arbol.evalua()
    except Error, err:
      sys.stderr.write("%s\n" % err)
      if err.__class__.__name__ in ["ErrorLexico", "ErrorSintactico"]:
        lex.muestraError(sys.stderr)
    l= sys.stdin.readline()