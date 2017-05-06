#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arboles
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
    arbol= self.analizaExpresion()
    if self.componente.cat!= "nl":
      raise ErrorSintactico("Ya tengo una expresión, ¿por qué no terminas la línea?")
    return arbol

  def analizaExpresion(self):
    arbol= self.analizaTermino()
    while self.componente.cat== "opad":
      if self.componente.operacion=="+":
        self.componente = self.lexico.siguiente()
        sumando = self.analizaTermino()
        arbol = arboles.Suma(arbol, sumando)
      elif self.componente.operacion=="-":
        self.componente = self.lexico.siguiente()
        sumando = self.analizaTermino()
        arbol = arboles.Resta(arbol, sumando)
      else:
        raise ErrorSintactico("La operación no es correcta con suma o resta")
    return arbol

  def analizaTermino(self):
    arbol= self.analizaFactor()
    while self.componente.cat== "opmul":
      if self.componente.operacion=="*":
        self.componente = self.lexico.siguiente()
        factor = self.analizaFactor()
        arbol= arboles.Producto(arbol, factor)
      elif self.componente.operacion=="/":
        self.componente = self.lexico.siguiente()
        factor = self.analizaFactor()
        arbol = arboles.Division(arbol, factor)
    return arbol

  def analizaFactor(self):
    if self.componente.cat=="abre":
      self.componente= self.lexico.siguiente()
      arbol= self.analizaExpresion()
      if self.componente.cat!= "cierra":
        raise ErrorSintactico("Aquí tocaba cerrar un paréntesis.")
      self.componente= self.lexico.siguiente()
      return arbol
    elif self.componente.cat=="entero":
      arbol= arboles.Entero(self.componente.valor)
      self.componente= self.lexico.siguiente()
      return arbol
    elif self.componente.cat=="real":
      arbol = arboles.Real(self.componente.valor)
      self.componente = self.lexico.siguiente()
      return arbol
    elif self.componente.cat=="cadena":
      arbol= arboles.Cadena(self.componente.valor)
      self.componente= self.lexico.siguiente()
      return arbol
    elif self.componente.cat=="abrirBarra":
      self.componente = self.lexico.siguiente()
      if self.componente.cat=="opad":
        self.componente = self.lexico.siguiente()
      elif self.componente.cat=="cadena":
        self.componente=componentes.entero(len(self.componente.valor))
      arbol = self.analizaExpresion()
      if self.componente.cat!="abrirBarra":
        raise ErrorSintactico("Aquí tocaba cerrar una barra.")
      self.componente = self.lexico.siguiente()
      return arbol
    elif self.componente.cat=="opad":
      operacion = self.componente
      self.componente = self.lexico.siguiente()
      componente = self.analizaFactor()
      arbol=arboles.CambioSigno(operacion.operacion,componente)
      return arbol
    else:
      raise ErrorSintactico("La verdad, no sé qué hacer con esto.")

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