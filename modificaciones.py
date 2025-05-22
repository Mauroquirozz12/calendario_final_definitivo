def create_widgets(self):

    # Panel derecho - Calendario

    calendar_frame = ttk.LabelFrame(right_panel, text="Calendario", padding=10)
    calendar_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    # Calendario interactivo
    self.calendar = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    self.calendar.pack(fill=tk.BOTH, expand=True)


def show_calendar_tasks(self):
    # Crear ventana para mostrar tareas en el calendario
    calendar_window = tk.Toplevel(self.root)
    calendar_window.title("Tareas en Calendario")
    calendar_window.geometry("800x600")

    # Crear y empaquetar el calendario grande
    big_calendar = Calendar(calendar_window, selectmode='day', date_pattern='yyyy-mm-dd')
    big_calendar.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Configurar colores según prioridad (se aplica antes de agregar eventos)
    tag_colors = {'alta': 'red', 'media': 'orange', 'baja': 'green'}
    for priority, color in tag_colors.items():
        big_calendar.tag_config(priority, background=color)

    # Mostrar tareas asignando directamente la etiqueta de prioridad
    for task in self.filtered_tasks:
        due_date = task.get('due_date')
        if due_date and due_date != "Sin fecha":
            try:
                event_date = datetime.strptime(due_date, '%Y-%m-%d')
                big_calendar.calevent_create(
                    event_date,
                    task['title'],  # Se muestra el título de la tarea
                    tags=task['priority']  # Asignación directa del tag según prioridad
                )
            except ValueError:
                continue