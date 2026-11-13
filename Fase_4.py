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

class ReservationError(SoftwareFJError):
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
    
    #Clase abstracta base para las entidades del sistema.
  
    def __init__(self, identificador):
        self._identificador = identificador
      
    @abstractmethod
    def obtener_info(self):
        pass

class Cliente(EntidadBase):

    # Clase Cliente con encapsulación y validaciones.
  
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
      
    def set_documento(self, documento):
        doc_srtr = str(documento).strip()
        if not doc_srtr.isdigit() or len(doc_srtr) < 6:
            registrar_log(f"Validation Error: Invalid document ID '{documento}'")
            raise ValidationError("Document ID must be numeric and at least 6 digits long.")
        self.__documento = doc_srtr 

    def set_email(self, email):
        if not email or "@" not in email or "." not in email:
            registrar_log(f"Validation Error: Invalid email '{email}'")
            raise ValidationError("Invalid email address format.")
        self.__email = email.strip()

    def obtener_nombre(self):
        return self.__nombre

    def obtener_documento(self):
        return self.__documento

    def obtener_info(self):
        return f"Client: {self.__nombre} | ID: {self.__documento} | Email: {self.__email}"

class Servicio(EntidadBase, ABC):

      #Clase abstracta Servicio.

    def __init__(self, codigo, tarifa_base):
        super().__init__(codigo)
        try:
            self.tarifa_base = float(tarifa_base)
        except ValueError:
            raise ValidationError("Base rate must be a numeric value.")
        if self.tarifa_base <= 0:
            raise ValidationError("Base rate must be greater than zero.")

    @abstractmethod
    def calcular_costo(self, cantidad):
        pass

    @abstractmethod
    def obtener_descripcion(self):
        pass

    def obtener_info(self):
      return f"Service: {self._identificador} | Base Rate: ${self.tarifa_base:.2f}"

class ReservaSala(Servicio):

      #Servicio especializado 1: Reserva de Sala (con IVA del 19%).

    def calcular_costo(self, cantidad):
        if cantidad <= 0:
           raise ValidationError("Hours must be greater than zero.")
        return round(self.tarifa_base * cantidad * 1.19, 2)

    def obtener_descripcion(self):
        return f"Room Reservation [{self._identificador}]"

class AlquilerEquipo(Servicio):

      #Servicio especializado 2: Alquiler de Equipos (con seguro fijo).

    def calcular_costo(self, cantidad):
        if cantidad <= 0:
           raise ValidationError("Days must be greater than zero.")
        return round((self.tarifa_base * cantidad) + 50.0, 2)

    def obtener_descripcion(self):
        return f"Equipment Rental [{self._identificador}]"

class AsesoriaEspecializada(Servicio):

      #Servicio especializado 3: Asesoría Especializada (factor senior 1.3).

    def calcular_costo(self, cantidad):
        if cantidad <= 0:
            raise ValidationError("Sessions must be greater than zero.")
        return round(self.tarifa_base * cantidad * 1.30, 2)

    def obtener_descripcion(self):
        return f"Specialized Consulting [{self._identificador}]"

class Reserva(EntidadBase):

      #Clase Reserva que integra cliente, servicio, cantidad y manejo de excepciones.

    def __init__(self, id_reserva, cliente, servicio, cantidad):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise ValidationError("A valid Client object is required.")
        if not isinstance(servicio, Servicio):
            raise ValidationError("A valid Service object is required.")
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pending"
        self.costo_total = 0.0

    def procesar(self):

        #Procesa la reserva implementando try / except / else / finally.

        try:
            registrar_log(f"Processing reservation #{self._identificador}")
            self.costo_total = self.servicio.calcular_costo(self.cantidad)
        except ValidationError as ve:
            self.estado = "Failed"
            registrar_log(f"Validation failed for #{self._identificador}: {ve}")
            raise ReservationError(f"Cannot process reservation: {ve}") from ve
        except Exception as e:
            self.estado = "Error"
            registrar_log(f"Critical error for #{self._identificador}: {e}")
            raise ReservationError("Critical error processing reservation.") from e
        else:
            self.estado = "Confirmed"
            registrar_log(f"Reservation #{self._identificador} confirmed successfully. Total: ${self.costo_total}")
        finally:
            registrar_log(f"Finished processing cycle for reservation #{self._identificador}")

    def cancelar(self):
        if self.estado == "Cancelled":
            raise ReservationError("Reservation is already cancelled.")
        self.estado = "Cancelled"
        registrar_log(f"Reservation #{self._identificador} was cancelled.")

    def obtener_info(self):
        return f"{self._identificador} | {self.cliente.obtener_nombre()} | {self.servicio.obtener_descripcion()} | {self.estado} | Total: ${self.costo_total:.2f}"



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
    ventana = tk.Tk()
    ventana.title("Software FJ - Management System")
    ventana.geometry("900x750")
    ventana.config(bg="#f4f6f9")

  # Título principal centrado 
    tk.Label(ventana, text="Software FJ - Management System", font=("Helvetica", 16, "bold"), bg="#f4f6f9", fg="#333333").pack(pady=10)

  # Marco de registro principal
    frame_reg = tk.LabelFrame(ventana, text=" Register Reservation ", font=("Helvetica", 11, "bold"), bg="#f4f6f9", padx=10, pady=10)
    frame_reg.pack(pady=5)

    tk.Label(frame_reg, text="Client Name:", bg="#f4f6f9", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=4)
    txt_nombre = tk.Entry(frame_reg, font=("Helvetica", 10), width=25)
    txt_nombre.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(frame_reg, text="Document ID:", bg="#f4f6f9", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=4)
    txt_doc = tk.Entry(frame_reg, font=("Helvetica", 10), width=25)
    txt_doc.grid(row=1, column=1, padx=5, pady=4)

    tk.Label(frame_reg, text="Email:", bg="#f4f6f9", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=4)
    txt_email = tk.Entry(frame_reg, font=("Helvetica", 10), width=25)
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
    def registrar_manual():
        try:
            nombre = txt_nombre.get()
            doc = txt_doc.get()
            email = txt_email.get()
            cant_str = txt_cantidad.get().strip()

            if not cant_str.isdigit():
                raise ValidationError("Duration must be a positive integer.")
            cantidad = int(cant_str)

            cliente = next((c for c in clientes_registrados if c.obtener_documento() == doc), None)
            if not cliente:
                cliente = Cliente(nombre, doc, email)
                clientes_registrados.append(cliente)

            idx = ["Room Reservation", "Equipment Rental", "Specialized Consulting"].index(tipo_var.get())
            servicio = servicios_disponibles[idx]

            id_res = f"RES-{len(reservas_registradas)+1:03d}"
            reserva = Reserva(id_res, cliente, servicio, cantidad)
            reserva.procesar()

            reservas_registradas.append(reserva)
            lista_visual.insert(tk.END, reserva.obtener_info())
            lbl_resultado.config(text=f"Reservation {id_res} processed successfully!", fg="green")

            txt_nombre.delete(0, tk.END)
            txt_doc.delete(0, tk.END)
            txt_email.delete(0, tk.END)
            txt_cantidad.delete(0, tk.END)
            
        except Exception as e:
            lbl_resultado.config(text=f"Error: {str(e)}", fg="red")
            registrar_log(f"GUI Error: {e}")

    tk.Button(frame_reg, text="Process Reservation", command=registrar_manual, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold")).grid(row=5, columnspan=2, pady=8)

    # Marco de visualización de registros
    tk.Label(ventana, text="System Log & Reservations Display", font=("Helvetica", 12, "bold"), bg="#f4f6f9").pack(anchor="n", pady=2)
    lista_visual = tk.Listbox(ventana, width=100, height=9, font=("Consolas", 9))
    lista_visual.pack(pady=5)
          
#==========================================
# 4 DISEÑO PARTE INFERIOR
#==========================================
    frame_controles = tk.LabelFrame(ventana, text="Operation & Managenment Controls", font=("Helvetica", 10, "bold"), bg="#f4f6f9", padx=10, pady=5)
    frame_controles.pack(pady=5, fill="x", padx=40)
  
    def cancelar_reserva_seleccionada():
      try:
          seleccion = lista_visual.curselection()
          if not seleccion:
              lbl_resultado.config(texty="Plase select a reservation from the list to cancel.", fg="red")
              return
  
          indice = seleccion[0]
          texto_linea = lista_visual.get(indice)
          id_res = texto_linea.split(" | ")[0]
  
          reserva = next((r for r in reservas_registradas if r._identificador == id_res), None)
          if reserva:
              reserva.cancelar()
              lista_visual.delete(indice)
              lista_visual.insert(indice, reserva.obtener_info())
              lbl_resultado.config(texte=f"Reservation[{id_res}] cancelled successfully.", fg="blue")
      except Exception as e:
        lbl_resultado.config(text=f"Error cancelling: {e}", fg="red")
    
    def simular_diez_operaciones():
        #Simula automaticamente 10 operaciones (válidas e inválidas) exigidads por la rubrica
        lista_visual.delete(0, tk.END)
        reservas_registradas.clear()
        registrar_log("=== STARTING AUTOMATIC 10 OPERATIONS SIMULATIONG ===")
        
        casos_prueba = [
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
  
        for i, (nom, doc, email, idx_serv, cant) in enumerate(casos_prueba, start=1):
            id_res = f"SIM-{i:03d}"
            try:
                cli = Cliente(nom, doc, email)
                srv = servicios_disponibles[idx_serv]
                res= Reserva(id_res, cli, srv, cant)
                res.prosesar()
                reservas_registradas.append(res)
                lista_visual.insert(tk.END, res.obtener_info())
            except Exception as e:
                lista_visual.insert(tk.END, f"HANDLED EXCEPTION [{id_res}] - Reason: {e}")
        
        registrar_log("=== FINISHED AUTOMATIC 10 OPERATIONS SIMULATION ===")
        lbl_resultado.config(text="10 operations simulation completed successfully!", fg="blue")
  
  # Botones inferiores
    btn_frame = tk.Frame(frame_controles, bg="#f4f6f9")
    btn_frame.pack(pady=5)
  
    tk.Button(btn_frame, text="Cancel Selected Reservation", command=cancelar_reserva_seleccionada, bg="#d9534f", fg="white", font=("Helvetica", 10, "bold"), padx=8, pady=4).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text= "Run 10 Operations Simulation", command=simular_diez_operaciones, bg="#ff9800", fg="white", font=("Helvetica", 10, "bold"), padx=8, pady=4).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text= "Clear List", command=lambda: lista_visual.delete(0, tk.END), bg="#6c757d", fg="white", font=("Helvetica", 10, "bold"), padx=8, pady=4).grid(row=0, column=2, padx=5)
  
    ventana.mainloop()

if __name__=="__main__":
    iniciar_interfaz()
