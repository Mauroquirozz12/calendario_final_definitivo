import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Clase principal del gestor de tareas
class GestorTareas:
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Administrador de Tareas")
        self.ventana.geometry("1200x700")

        # Lista que almacenará las tareas
        self.tareas = []

        # Variables para los filtros
        self.filtro_estado = tk.StringVar(value="Todas")
        self.filtro_prioridad = tk.StringVar(value="Todas")
        self.filtro_etiqueta = tk.StringVar(value="")

        # Crear la interfaz de usuario
        self.crear_interfaz()

    # Crea la interfaz gráfica dividiendo en panel izquierdo y derecho
    def crear_interfaz(self):
        contenedor = ttk.PanedWindow(self.ventana, orient=tk.HORIZONTAL)
        contenedor.pack(fill=tk.BOTH, expand=True)

        panel_izquierdo = ttk.Frame(contenedor, width=400)
        panel_derecho = ttk.Frame(contenedor)
        contenedor.add(panel_izquierdo)
        contenedor.add(panel_derecho)

        self._formulario_tarea(panel_izquierdo)   # Formulario para añadir tareas
        self._filtros(panel_izquierdo)            # Panel de filtros
        self._lista_tareas(panel_derecho)         # Vista de lista de tareas

    # Crea el formulario para añadir nuevas tareas
    def _formulario_tarea(self, parent):
        marco = ttk.LabelFrame(parent, text="Crear Nueva Tarea", padding=10)
        marco.pack(fill=tk.X, pady=10)

        # Variables para los campos del formulario
        self.titulo = tk.StringVar()
        self.descripcion = tk.StringVar()
        self.fecha = tk.StringVar()
        self.prioridad = tk.StringVar(value="media")
        self.estado = tk.StringVar(value="pendiente")
        self.etiquetas = tk.StringVar()

        # Campos de entrada
        ttk.Label(marco, text="Título").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(marco, textvariable=self.titulo).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(marco, text="Descripción").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(marco, textvariable=self.descripcion).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(marco, text="Fecha Límite").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(marco, textvariable=self.fecha).grid(row=2, column=1, padx=5, pady=2)
        ttk.Button(marco, text="Calendario", command=s
