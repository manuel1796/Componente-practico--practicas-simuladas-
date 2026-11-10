# Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas (Software FJ)
# Nombre del estudiante: Edgar Manuel Betancourt Ospina - Jeison Jose Villegas Gonzalez
# Grupo: 213023_543
# Programa: Ingeniería de Sistemas

#                       Actividades a realizar
# Utilizar la librería Tkinter para crear una interfaz gráfica del Sistema.
# Interfaz diseñada completamente en idioma inglés.
# Crear clases abstractas y herencia (EntidadBase, Servicio y sus clases hijas).
# Crear clase Cliente con atributos encapsulados y validaciones estrictas en los setters.
# Implementar manejo avanzado de excepciones (try / except / else / finally).
# Registrar todos los eventos y errores en un archivo de texto externo ('software_fj_logs.txt').
# Demostrar simulación automática de al menos 10 operaciones (casos válidos e inválidos).

import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
import datetime

#============================================================
# 1. EXCEPCIONES PERSONALIZADAS Y SISTEMAS DE LOGS 
#============================================================
class SoftwareFJError(Exception):
  pass

class ValidationError(SoftwareFJError):
  pass

class ReservartionError(SoftwareFJError):
  pass

def registrar_log(mensaje):
  # Registra eventos y errores en un archivode textode logs.
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  try:
    with open("software_fj_logs.txt", "a", encoding="utf-8") as f:
      f.write(f"[{timestamp}] {mensaje}\n")
  except Exception as e:
    print(f"Error escribiendo en el log: {e}")

# ===================================================================
# 2.
# ===================================================================
    
