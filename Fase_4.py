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
# 2.Creacion de clases Encapsulación Herecncia y Polimorfismo
# ===================================================================
class EntidadBase(ABC):
  def __init__(self, identificador):
    self._identificador = identificador
    
  @abstractmethod
  def obtener_info(self):
      pass

class Cliente(EntidadBase):
  def __init__(self, nombre, documento, email):
    super().__init__(str(documento))
    self.set_nombre(nombre)
    self.set_documento(documento)
    self.set_email(email)

  def set_nombre(self, nombre):
    if not nombre or len(nombre.strip()) < 3:
      registrar_log(f"Validation Error: Invalid name '{nombre}'")
      raise ValidationError("Client name must be at least 3 characters long.")
    self.__nombre = nombre.strip()



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

#==========================================
# 4 DISEÑO PARTE INFERIOR
#==========================================
  frame_controles = tk.LabelFrame(ventana, text="Operation & Managenment Controls", font=("Helvetica", 10, "bold"), bg="#f4f6f9", padx=10, pady=5)
  frame_controles.pack(pady=5, fill="x", padx=40)
  
  def cancelar_recerva_seleccionada():
    try:
      seleccion = lista_visual.curselection()
      if not seleccion:
        lbl_resultado.config(texty="Plase select a reservation from the list to cancel.", fg="red")
        return
  
      indice = seleccion[0]
      texto_linea = lista_visual.get(indice)
      id_res =texto_linea.split(" | ")[0]
  
      reserva = next((r for r in reservas_registradas if r._identificador == id_res), None)
      if reserva:
        reserva.cancelar()
        lista_visual.delete(indice)
        lista visual.insert(indice, reserva.obtener _info())
        lbl_resultado.config(texte=f"Reservation[id_res] cancelled successfully.", fg="blue")
    except Exception as e:
      lbl_resultado.config(text=f"Error cancelling: {e}", fg="red")
  
  def simular_diez_operaciones():
    """Simula automaticamente 10 operaciones (válidas e inválidas) exigidads por la rubrica"""
    lista_visual.delete(0, tk.END)
    reservas_regitradas.clear()
    registrar_log("=== STARTING AUTOMATIC 10 OPERATIONS SIMULATIONG ===")
  
    casos_prueba= [
      ("Jeison Villegas", "10203040", "jeison@unad.edu.co", 0, 3), # 1. Válido - Sala (3h)
      ("Ana Gómez", "abc12345", "ana@unad.edu.co", 1, 5),          # 2. Inválido - Documento letras
      ("Carlos Pérez", "98765432", "carlos.unad.edu", 2, 2),       # 3. Inválido - Email sin @
      ("María Ruiz", "55443322", "maria@gmail.com", 1, 4),         # 4. Válido - Alquiler (4 días)
      ("Luis Torres", "11223344", "luis@unad.edu.co", 0, -2),      # 5. Inválido - Horas negativas
      ("Diana Rojas", "77889900", "diana@unad.edu.co", 2, 3),      # 6. Válido - Asesoría (3 sesiones)
      ("", "99887766", "vacio@unad.edu.co", 0, 2),                 # 7. Inválido - Nombre vacío
      ("Pedro Infante", "44556677", "pedro@unad.edu.co", 1, 10),   # 8. Válido - Alquiler (10 días)
      ("Sofia Vergara", "33221100", "sofia@unad.edu.co", 2, 0),    # 9. Inválido - Sesiones en cero
      ("Andrés Parra", "66778899", "andres@unad.edu.co", 0, 8)     # 10. Válido - Sala (8h)
    ]
  
    for i, (nom, doc, email, idxserv, cant) in enumerate(casos_prueba, start=1:
      id_res = f"SIM-{i:03d}"
      try:
        cli = Cliente(nom, doc, email)
        srv = servicios_disponibles[idx_serv]
        res= Reserva(id_res, cli, srv, cant)
        res.prosesar()
        reservas_registadas.append(res)
        lista_visual.insert(tk.END, res.obtener_info())
      except Exception as e:
        lista_visual .insert(tk.end, f"HANDLED EXCEPTION [{id_res}] - Reason: {e}")
  
    registrar_log("=== FINISHED AUTOMATIC 10 OPERATIONS SIMULATION ===")
    lbl_resultado.config(text="10 operations simulation completed successfully!", fg="blue")
  
  # Botones inferiores
  btn_frame = tk.Frame(frame_controles, bg="#f4f6f9")
  btn_frame.pack(pady=5)
  
  tk.Buton(btn_frame, text="Cancel Selected Reservation", command=cancelar_reserva_selecionada, bg="#d9534f", fg="white", font=("Helvetica", 10, "bold") padx=8, pady=4).grid(row=0, column=0, padx=5)
  tk.Buton(btn_frame, text= "Run 10 Operations Simulation", command=simular_diez_operaciones, bg="#ff9800", fg="white", font=("Helvetica", 10, "bold") padx=8, pady=4).grid(row=0, column=1, padx=5)
  tk.Buton(btn_frame, text= "Clear List", command=lambda: lista_visual.delete(0, tk.END), bg="#6c757d", fg="white", font=("Helvetica", 10, "bold") padx=8, pady=4).grid(row=0, column=2, padx=5)
  
  ventana.mainloop()

if __name__=="__main__":
  iniciar_interfaz()
