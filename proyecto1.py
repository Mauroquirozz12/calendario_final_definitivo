def get_selected_task(self):
    selected_item = self.tasks_tree.focus()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Por favor seleccione una tarea")
        return None

    item_data = self.tasks_tree.item(selected_item)
    task_title = item_data['values'][0]

    # Buscar la tarea por título
    task = next((t for t in self.tasks if t['title'] == task_title), None)
    return (task, selected_item) if task else None


def edit_task(self):
    selected = self.get_selected_task()
    if not selected:
        return

    task, item_id = selected

    # Variables para formulario
    vars_form = {
        'title': tk.StringVar(value=task['title']),
        'description': tk.StringVar(value=task['description']),
        'due_date': tk.StringVar(value=task['due_date']),
        'priority': tk.StringVar(value=task['priority']),
        'status': tk.StringVar(value=task['status']),
        'tags': tk.StringVar(value=", ".join(task['tags']))
    }

    # Ventana de edición
    edit_window = tk.Toplevel(self.root)
    edit_window.title("Editar Tarea")

    # Función para guardar cambios
    def save_changes():
        new_title = vars_form['title'].get().strip()
        new_due_date = vars_form['due_date'].get().strip()

        if not new_title:
            messagebox.showerror("Error", "El título es obligatorio.")
            return

        if new_due_date and new_due_date != "Sin fecha":
            try:
                datetime.strptime(new_due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Fecha inválida. Use formato YYYY-MM-DD.")
                return

        # Actualización
        task.update({
            'title': new_title,
            'description': vars_form['description'].get().strip(),
            'due_date': new_due_date if new_due_date else "Sin fecha",
            'priority': vars_form['priority'].get(),
            'status': vars_form['status'].get(),
            'tags': [tag.strip() for tag in vars_form['tags'].get().split(",") if tag.strip()]
        })

        self.apply_filters()
        messagebox.showinfo("Éxito", "Tarea actualizada correctamente.")
        edit_window.destroy()

    # Campos del formulario
    campos = [
        ("Título:", 'title'),
        ("Descripción:", 'description'),
        ("Fecha límite:", 'due_date'),
        ("Prioridad:", 'priority'),
        ("Estado:", 'status'),
        ("Etiquetas (separadas por comas):", 'tags')
    ]

    for i, (label_text, key) in enumerate(campos):
        ttk.Label(edit_window, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)
        if key == 'priority':
            ttk.Combobox(edit_window, textvariable=vars_form[key], values=["alta", "media", "baja"], width=27).grid(row=i, column=1, pady=2, padx=5)
        elif key == 'status':
            ttk.Combobox(edit_window, textvariable=vars_form[key], values=["pendiente", "en progreso", "completada"], width=27).grid(row=i, column=1, pady=2, padx=5)
        else:
            ttk.Entry(edit_window, textvariable=vars_form[key], width=30).grid(row=i, column=1, pady=2, padx=5)

    ttk.Button(edit_window, text="Guardar Cambios", command=save_changes).grid(row=len(campos), column=1, pady=10)


def delete_task(self):
    selected = self.get_selected_task()
    if not selected:
        return

    task, _ = selected

    if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar la tarea '{task['title']}'?"):
        self.tasks.remove(task)
        self.apply_filters()
        messagebox.showinfo("Éxito", "Tarea eliminada correctamente")


def view_details(self):
    selected = self.get_selected_task()
    if not selected:
        return

    task, _ = selected

    details_window = tk.Toplevel(self.root)
    details_window.title(f"Detalles: {task['title']}")

    detalles = [
        ("Título", task['title']),
        ("Descripción", task['description']),
        ("Fecha límite", task['due_date']),
        ("Prioridad", task['priority']),
        ("Estado", task['status']),
        ("Etiquetas", ", ".join(task['tags']) if task['tags'] else "Ninguna")
    ]

    for i, (label, valor) in enumerate(detalles):
        ttk.Label(details_window, text=f"{label}: {valor}", anchor="w", font=('Arial', 10)).pack(anchor=tk.W, pady=2, padx=10)








