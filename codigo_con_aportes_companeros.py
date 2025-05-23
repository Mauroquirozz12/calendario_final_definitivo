import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Clase principal del gestor de tareas
class GestorTareas:
    def __init__(self, root):
        """Inicializacion de la aplicación, definicion de variables y construccion de la interfaz gráfica."""
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("1100x700")

        self.tasks = []  # Lista de tareas
        self.filtered_tasks = []  # Lista filtrada (para futuras funcionalidades)

        self.build_gui()

    def build_gui(self):
        """Construye la interfaz gráfica del usuario (GUI)."""
        # División de la ventana en paneles izquierdo y derecho
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_panel = ttk.Frame(main_frame, width=400)
        right_panel = ttk.Frame(main_frame)
        main_frame.add(left_panel)
        main_frame.add(right_panel)

        # Formulario para ingresar nueva tarea
        form_frame = ttk.LabelFrame(left_panel, text="Nueva Tarea", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        # Variables del formulario
        self.vars = {
            'title': tk.StringVar(),
            'description': tk.StringVar(),
            'due_date': tk.StringVar(),
            'priority': tk.StringVar(value="media"),
            'status': tk.StringVar(value="pendiente"),
            'tags': tk.StringVar()
        }

        # Campos del formulario
        campos = [
            ("Título", 'title'), ("Descripción", 'description'),
            ("Fecha Límite", 'due_date'), ("Prioridad", 'priority'),
            ("Estado", 'status'), ("Etiquetas", 'tags')
        ]

        for i, (label, key) in enumerate(campos):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W)
            if key in ['priority', 'status']:
                valores = ["alta", "media", "baja"] if key == 'priority' else ["pendiente", "en progreso", "completada"]
                ttk.Combobox(form_frame, textvariable=self.vars[key], values=valores).grid(row=i, column=1, pady=2)
            else:
                ttk.Entry(form_frame, textvariable=self.vars[key]).grid(row=i, column=1, pady=2)

        # Botones del formulario
        ttk.Button(form_frame, text="Calendario", command=self.abrir_calendario).grid(row=2, column=2)
        ttk.Button(form_frame, text="Agregar", command=self.agregar_tarea).grid(row=6, column=1, pady=10)

        # Lista de tareas en una tabla
        lista_frame = ttk.LabelFrame(left_panel, text="Lista de Tareas")
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tasks_tree = ttk.Treeview(lista_frame, columns=("desc", "fecha", "prioridad", "estado", "etiquetas"), show="headings")
        for col in self.tasks_tree["columns"]:
            self.tasks_tree.heading(col, text=col.title())
        self.tasks_tree.pack(fill=tk.BOTH, expand=True)

        # Botones para manejar las tareas seleccionadas
        btns = ttk.Frame(lista_frame)
        btns.pack(pady=5)
        ttk.Button(btns, text="Detalles", command=self.ver_detalles).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Editar", command=self.editar_tarea).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Eliminar", command=self.eliminar_tarea).pack(side=tk.LEFT, padx=5)

        # Calendario visual en panel derecho
        calendario_frame = ttk.LabelFrame(right_panel, text="Calendario")
        calendario_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.calendar = Calendar(calendario_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(fill=tk.BOTH, expand=True)

        ttk.Button(calendario_frame, text="Ver Calendario con Tareas", command=self.mostrar_tareas_calendario).pack(pady=10)

        # Visualización de la línea de tiempo
        timeline_frame = ttk.LabelFrame(right_panel, text="Línea de Tiempo")
        timeline_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        ttk.Button(timeline_frame, text="Mostrar Línea de Tiempo", command=self.mostrar_timeline).pack()

    def abrir_calendario(self):
        """Muestra un calendario emergente para seleccionar fecha de vencimiento."""
        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=10, pady=10)
        ttk.Button(top, text="Seleccionar", command=lambda: self._guardar_fecha(cal.get_date(), top)).pack(pady=10)

    def _guardar_fecha(self, fecha, ventana):
        """Guarda la fecha seleccionada en el campo correspondiente."""
        self.vars['due_date'].set(fecha)
        ventana.destroy()

    def agregar_tarea(self):
        """Agrega una nueva tarea a la lista."""
        if not self.vars['title'].get():
            messagebox.showerror("Error", "Título obligatorio.")
            return
        tarea = {
            'title': self.vars['title'].get(),
            'description': self.vars['description'].get(),
            'due_date': self.vars['due_date'].get(),
            'priority': self.vars['priority'].get(),
            'status': self.vars['status'].get(),
            'tags': [tag.strip() for tag in self.vars['tags'].get().split(",") if tag.strip()]
        }
        self.tasks.append(tarea)
        self.actualizar_lista()

    def actualizar_lista(self):
        """Actualiza la tabla de tareas con los datos actuales."""
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        for task in self.tasks:
            self.tasks_tree.insert("", tk.END, values=(task['description'], task['due_date'], task['priority'], task['status'], ", ".join(task['tags'])))
        self.filtered_tasks = self.tasks.copy()

    def get_selected_task(self):
        """Retorna la tarea seleccionada en la tabla."""
        selected_item = self.tasks_tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una tarea.")
            return None
        item_data = self.tasks_tree.item(selected_item)
        task_desc = item_data['values'][0]
        task = next((t for t in self.tasks if t['description'] == task_desc), None)
        return (task, selected_item) if task else None

    def ver_detalles(self):
        """Muestra los detalles de la tarea seleccionada."""
        seleccionado = self.get_selected_task()
        if not seleccionado: return
        task, _ = seleccionado
        detalles = tk.Toplevel(self.root)
        detalles.title("Detalles")
        for k, v in task.items():
            if isinstance(v, list): v = ", ".join(v)
            ttk.Label(detalles, text=f"{k.title()}: {v}").pack(anchor=tk.W, padx=10, pady=2)

    def editar_tarea(self):
        """Permite editar la tarea seleccionada."""
        seleccionado = self.get_selected_task()
        if not seleccionado: return
        task, item_id = seleccionado

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Editar Tarea")
        campos = {}
        for key in ['title', 'description', 'due_date', 'priority', 'status', 'tags']:
            campos[key] = tk.StringVar(value=", ".join(task[key]) if isinstance(task[key], list) else task[key])

        labels = [("Título", "title"), ("Descripción", "description"), ("Fecha", "due_date"),
                  ("Prioridad", "priority"), ("Estado", "status"), ("Etiquetas", "tags")]

        for i, (txt, key) in enumerate(labels):
            ttk.Label(edit_win, text=txt).grid(row=i, column=0)
            if key in ['priority', 'status']:
                valores = ["alta", "media", "baja"] if key == 'priority' else ["pendiente", "en progreso", "completada"]
                ttk.Combobox(edit_win, textvariable=campos[key], values=valores).grid(row=i, column=1)
            else:
                ttk.Entry(edit_win, textvariable=campos[key]).grid(row=i, column=1)

        def guardar():
            task.update({
                'title': campos['title'].get(),
                'description': campos['description'].get(),
                'due_date': campos['due_date'].get(),
                'priority': campos['priority'].get(),
                'status': campos['status'].get(),
                'tags': [tag.strip() for tag in campos['tags'].get().split(",") if tag.strip()]
            })
            self.actualizar_lista()
            edit_win.destroy()

        ttk.Button(edit_win, text="Guardar", command=guardar).grid(row=6, column=1, pady=10)

    def eliminar_tarea(self):
        """Elimina la tarea seleccionada previa confirmación."""
        seleccionado = self.get_selected_task()
        if not seleccionado: return
        task, _ = seleccionado
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{task['title']}'?"):
            self.tasks.remove(task)
            self.actualizar_lista()

    def mostrar_tareas_calendario(self):
        """Muestra un calendario con las tareas marcadas por colores según prioridad."""
        cal_win = tk.Toplevel(self.root)
        cal_win.title("Calendario con Tareas")
        big_cal = Calendar(cal_win, selectmode='day', date_pattern='yyyy-mm-dd')
        big_cal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        colores = {'alta': 'red', 'media': 'orange', 'baja': 'green'}
        for p, c in colores.items():
            big_cal.tag_config(p, background=c)

        for task in self.tasks:
            if task['due_date']:
                try:
                    fecha = datetime.strptime(task['due_date'], '%Y-%m-%d')
                    big_cal.calevent_create(fecha, task['title'], tags=task['priority'])
                except ValueError:
                    continue

    def mostrar_timeline(self):
        """Muestra una línea de tiempo con puntos según fechas de vencimiento y prioridades."""
        if not self.tasks:
            messagebox.showinfo("Info", "No hay tareas.")
            return

        fig, ax = plt.subplots(figsize=(10, 4))
        fechas = []
        etiquetas = []
        colores = []

        colores_prioridad = {"alta": "red", "media": "orange", "baja": "green"}

        for i, task in enumerate(self.tasks):
            try:
                fecha = datetime.strptime(task['due_date'], "%Y-%m-%d")
                fechas.append(fecha)
                etiquetas.append(f"{task['title']} ({task['priority']})")
                colores.append(colores_prioridad.get(task['priority'], "blue"))
            except:
                continue

        ax.scatter(fechas, [i for i in range(len(fechas))], color=colores)
        ax.set_yticks(range(len(etiquetas)))
        ax.set_yticklabels(etiquetas)
        ax.set_xlabel("Fechas límite")
        ax.set_title("Línea de Tiempo de Tareas")
        ax.grid(True)

        plt.tight_layout()

        win = tk.Toplevel(self.root)
        win.title("Línea de Tiempo")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

# Punto de entrada del programa
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()
