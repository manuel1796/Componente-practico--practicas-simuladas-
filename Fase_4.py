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
    

# =========================================
# 3. INTERFAZ GRAFICA TKINTER
#==========================================
reservas_registradas = []
clientes_registrados = []
servicios_disponibles = [
  ReservaSala("SRV-001", 50.0),
  AlquilerEquipo("SRV-002", 30.0),
  AsesoriaEspecializada("SRV-003", 100.0)
]
# ===========================================
# 3.1 DISEÑO PARTE DE DATOS
#============================================
def iniciar_interfaz():
  ventana =tk.tk()
  ventana.title("Software FJ - Management System")
  ventana.geometry("900x750")
  ventana.config(bg="#f4f6f9")

  # Título principal centrado 
  tk.label(ventana, text="Software FJ - Management System", font=("Helvetica", 16, "bold"), bg="#f4f6f92, fg="#333333").pack(pady=10)

  # Marco de registro principal
    frame_reg = tk.LabelFrame(ventana, text=" Register Reservation ", font=("Helvetica", 11, "bold"), bg="#f4f6f92, padx=10, pady=10)
    frame_reg.pack(pady=5)

    tk.Label(frame_reg, text="Client Name:", bg="#f4f6f9", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=4)
    txt_nombre = tk.Entry(frame_reg, font=("Helvetica", 10), width=25)
    txt_nombre.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(frame_reg, text="Document ID:", bg="#f4f6f9", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=4)
    txt_doc = tk.Entry(rame_reg, font=("Helvetica", 10), width=25)
    txt_doc.grid(row=1, column=1, padx=5, pady=4)

    tk.Label(frame_reg, text="Email:", bg="#f4f6f9", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=4)
    txt_email = tk.Entry(rame_reg, font=("Helvetica", 10), width=25)
    txt_email.grid(row=2, column=1, padx=5, pady=4)

    tk.Label(frame_reg, text="Service Type:", bg="#f4f6f9", font=("Helvetica", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=4)
    tipo_var = tk.StringVar(value="Room Reservation")
    tipo_menu = tk.OptionMenu(frame_reg,tipo_var, "Room Reservation", "Equipment Rentail", "Specialized Consulting")
    tipo_menu.config(bg="white", width=22)
    tipo_menu.grid(row=3, column=1, padx=5, pady=4, sticky="w")

    tk.Label(frame_reg, text="Duration (Hours/Days/Sessions):", bg="#f4f6f9", font=("Helvetica", 10)).grid(row=4, column=0, sticky="w", padx=5, pady=4)
    txt_cantidad = tk.Entry(frame_reg, font=("Helvetica", 10), width=25)
    txt_cantidad.grid(row=4, column=1, padx=5, pady=4)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 11, "bold"), bg="#f4f6f9")
    lbl_resultado.pack(pady=5)

#========================================
# 3.2 DISEÑO REGISTRO MANUAL
#========================================

