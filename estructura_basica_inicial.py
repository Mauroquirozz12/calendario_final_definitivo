import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GestorTareas:
    def __init__(self, root):
        """
        Inicializa la ventana principal y variables necesarias.
        """
        self.ventana = root
        self.ventana.title("Administrador de Tareas")
        self.ventana.geometry("1200x700")

        # Lista para almacenar las tareas
        self.tareas = []

        # Variables para filtros de tareas
        self.filtro_estado = tk.StringVar(value="Todas")
        self.filtro_prioridad = tk.StringVar(value="Todas")
        self.filtro_etiqueta = tk.StringVar(value="")

        # Construye la interfaz gráfica
        self.crear_interfaz()

    def crear_interfaz(self):
        """
        Crea la interfaz principal dividiendo la ventana en dos paneles horizontales.
        """
        contenedor = ttk.PanedWindow(self.ventana, orient=tk.HORIZONTAL)
        contenedor.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo para formulario y filtros
        panel_izquierdo = ttk.Frame(contenedor, width=400)
        # Panel derecho para lista de tareas
        panel_derecho = ttk.Frame(contenedor)

        contenedor.add(panel_izquierdo)
        contenedor.add(panel_derecho)

        # Crear formulario, filtros y lista dentro de sus respectivos paneles
        self._formulario_tarea(panel_izquierdo)
        self._filtros(panel_izquierdo)
        self._lista_tareas(panel_derecho)

    def _formulario_tarea(self, parent):
        """
        Construye el formulario para crear nuevas tareas.
        """
        marco = ttk.LabelFrame(parent, text="Crear Nueva Tarea", padding=10)
        marco.pack(fill=tk.X, pady=10)

        # Variables asociadas a los campos del formulario
        self.titulo = tk.StringVar()
        self.descripcion = tk.StringVar()
        self.fecha = tk.StringVar()
        self.prioridad = tk.StringVar(value="media")
        self.estado = tk.StringVar(value="pendiente")
        self.etiquetas = tk.StringVar()

        # Campos del formulario con etiquetas y entradas
        ttk.Label(marco, text="Título").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(marco, textvariable=self.titulo).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(marco, text="Descripción").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(marco, textvariable=self.descripcion).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(marco, text="Fecha Límite").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(marco, textvariable=self.fecha).grid(row=2, column=1, padx=5, pady=2)
        # Botón para abrir calendario y seleccionar fecha
        ttk.Button(marco, text="Calendario", command=self.seleccionar_fecha).grid(row=2, column=2, padx=5)

        ttk.Label(marco, text="Prioridad").grid(row=3, column=0, sticky=tk.W)
        ttk.Combobox(marco, textvariable=self.prioridad, values=["alta", "media", "baja"]).grid(row=3, column=1)

        ttk.Label(marco, text="Estado").grid(row=4, column=0, sticky=tk.W)
        ttk.Combobox(marco, textvariable=self.estado, values=["pendiente", "en progreso", "completada"]).grid(row=4, column=1)

        ttk.Label(marco, text="Etiquetas").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(marco, textvariable=self.etiquetas).grid(row=5, column=1, padx=5, pady=2)

        # Botón para agregar la tarea creada
        ttk.Button(marco, text="Agregar", command=self.agregar_tarea).grid(row=6, column=1, pady=10)

    def _filtros(self, parent):
        """
        Crea la sección para filtrar las tareas por prioridad, estado o etiqueta.
        """
        marco = ttk.LabelFrame(parent, text="Filtrar Tareas", padding=10)
        marco.pack(fill=tk.X, pady=10)

        ttk.Label(marco, text="Prioridad").grid(row=0, column=0)
        ttk.Combobox(marco, textvariable=self.filtro_prioridad, values=["Todas", "alta", "media", "baja"]).grid(row=0, column=1)

        ttk.Label(marco, text="Estado").grid(row=1, column=0)
        ttk.Combobox(marco, textvariable=self.filtro_estado, values=["Todas", "pendiente", "en progreso", "completada"]).grid(row=1, column=1)

        ttk.Label(marco, text="Etiqueta").grid(row=2, column=0)
        ttk.Entry(marco, textvariable=self.filtro_etiqueta).grid(row=2, column=1)

        # Botón para aplicar filtros
        ttk.Button(marco, text="Aplicar", command=self.filtrar_tareas).grid(row=3, column=1, pady=10)

    def _lista_tareas(self, parent):
        """
        Crea la lista (Treeview) donde se muestran las tareas.
        """
        self.lista = ttk.Treeview(parent, columns=("desc", "fecha", "prioridad", "estado", "etiquetas"), show="headings")
        self.lista.heading("desc", text="Descripción")
        self.lista.heading("fecha", text="Fecha Límite")
        self.lista.heading("prioridad", text="Prioridad")
        self.lista.heading("estado", text="Estado")
        self.lista.heading("etiquetas", text="Etiquetas")
        self.lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def seleccionar_fecha(self):
        """
        Abre una ventana secundaria con un calendario para seleccionar la fecha límite de la tarea.
        """
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Seleccionar Fecha")
        cal = Calendar(ventana, selectmode='day')
        cal.pack(padx=10, pady=10)
        ttk.Button(ventana, text="Seleccionar", command=lambda: self._guardar_fecha(cal.get_date(), ventana)).pack(pady=10)

    def _guardar_fecha(self, fecha_str, ventana):
        """
        Guarda la fecha seleccionada en el formulario y cierra la ventana del calendario.
        """
        self.fecha.set(fecha_str)
        ventana.destroy()

    def agregar_tarea(self):
        """
        Valida y agrega una nueva tarea a la lista interna y actualiza la vista.
        """
        if not self.titulo.get():
            messagebox.showwarning("Error", "El título es obligatorio")
            return
        tarea = {
            "titulo": self.titulo.get(),
            "descripcion": self.descripcion.get(),
            "fecha": self.fecha.get(),
            "prioridad": self.prioridad.get(),
            "estado": self.estado.get(),
            "etiquetas": self.etiquetas.get()
        }
        self.tareas.append(tarea)
        self.mostrar_tareas()
        self._limpiar_campos()

    def _limpiar_campos(self):
        """
        Limpia los campos del formulario para agregar una nueva tarea.
        """
        self.titulo.set("")
        self.descripcion.set("")
        self.fecha.set("")
        self.prioridad.set("media")
        self.estado.set("pendiente")
        self.etiquetas.set("")

    def mostrar_tareas(self):
        """
        Muestra todas las tareas almacenadas en la lista en el Treeview.
        """
        # Limpia la lista actual
        for item in self.lista.get_children():
            self.lista.delete(item)
        # Inserta todas las tareas
        for tarea in self.tareas:
            self.lista.insert("", tk.END, values=(
                tarea["descripcion"], tarea["fecha"], tarea["prioridad"], tarea["estado"], tarea["etiquetas"]
            ))

    def filtrar_tareas(self):
        """
        Filtra las tareas según los valores seleccionados en los filtros y actualiza la vista.
        """
        filtradas = self.tareas
        if self.filtro_prioridad.get() != "Todas":
            filtradas = [t for t in filtradas if t["prioridad"] == self.filtro_prioridad.get()]
        if self.filtro_estado.get() != "Todas":
            filtradas = [t for t in filtradas if t["estado"] == self.filtro_estado.get()]
        if self.filtro_etiqueta.get():
            filtradas = [t for t in filtradas if self.filtro_etiqueta.get() in t["etiquetas"]]

        # Limpia la lista actual
        for item in self.lista.get_children():
            self.lista.delete(item)
        # Inserta las tareas filtradas
        for tarea in filtradas:
            self.lista.insert("", tk.END, values=(
                tarea["descripcion"], tarea["fecha"], tarea["prioridad"], tarea["estado"], tarea["etiquetas"]
            ))

if __name__ == "__main__":
    # Crear ventana principal y ejecutar la aplicación
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()
