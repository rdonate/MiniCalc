#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Error(Exception):
  def __init__(self, mensaje):
    self.mensaje= mensaje

  def __str__(self):
    return self.mensaje

class ErrorLexico(Error):
  def __init__(self, mensaje):
    self.mensaje= "Error léxico: %s" % mensaje

class ErrorSintactico(Error):
  def __init__(self, mensaje):
    self.mensaje= "Error sintíctico: %s" % mensaje

class ErrorSemantico(Error):
  def __init__(self, mensaje):
    self.mensaje= "Error semántico: %s" % mensaje

class ErrorEjecucion(Error):
  def __init__(self, mensaje):
    self.mensaje= "Error de ejecución: %s" % mensaje
