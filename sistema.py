import tkinter as tk
from tkinter import messagebox
# Clase principal para crear la interfaz del sistema
class GestionCalificaciones:
    def __init__(self, root):
        # Configuración inicial de la ventana principal
        self.root = root
        self.root.title("Gestión de Calificaciones")

        self.alumnos = {}

        self.setup_ui()

    def setup_ui(self):
        # Frame para entradas
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="DNI:").grid(row=0, column=0)
        self.dni_entry = tk.Entry(frame)
        self.dni_entry.grid(row=0, column=1)

        tk.Label(frame, text="Apellidos:").grid(row=1, column=0)
        self.apellidos_entry = tk.Entry(frame)
        self.apellidos_entry.grid(row=1, column=1)

        tk.Label(frame, text="Nombre:").grid(row=2, column=0)
        self.nombre_entry = tk.Entry(frame)
        self.nombre_entry.grid(row=2, column=1)

        tk.Label(frame, text="Nota:").grid(row=3, column=0)
        self.nota_entry = tk.Entry(frame)
        self.nota_entry.grid(row=3, column=1)

        #Configuración para Botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Introducir Alumno", command=self.introducir_alumno).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Eliminar Alumno", command=self.eliminar_alumno).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Consultar Alumno", command=self.consultar_alumno).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Modificar Nota", command=self.modificar_nota).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Mostrar Suspensos", command=self.mostrar_suspensos).grid(row=1, column=0, padx=5)
        tk.Button(button_frame, text="Mostrar Aprobados", command=self.mostrar_aprobados).grid(row=1, column=1, padx=5)
        tk.Button(button_frame, text="Candidatos a MH", command=self.mostrar_mh).grid(row=1, column=2, padx=5)
        tk.Button(button_frame, text="Mostrar Todos", command=self.mostrar_todos).grid(row=1, column=3, padx=5)

        # Área de texto para resultados
        self.resultado_text = tk.Text(self.root, height=10, width=80)
        self.resultado_text.pack(pady=10)

    def calcular_calificacion(self, nota):
        #Clasificación de las notas
        if nota < 5:
            return "SS"
        elif nota < 7:
            return "AP"
        elif nota < 9:
            return "NT"
        else:
            return "SB"

    def introducir_alumno(self):
        #Método para ingreso de alumnos 
        dni = self.dni_entry.get()
        apellidos = self.apellidos_entry.get()
        nombre = self.nombre_entry.get()
        try:
            nota = float(self.nota_entry.get())
        except ValueError:
            messagebox.showerror("Error", "La nota debe ser un número válido.")
            return

        if dni in self.alumnos:
            messagebox.showerror("Error", "Ya existe un alumno con este DNI.")
            return

        calificacion = self.calcular_calificacion(nota)
        self.alumnos[dni] = {"apellidos": apellidos, "nombre": nombre, "nota": nota, "calificacion": calificacion}
        messagebox.showinfo("Éxito", "Alumno introducido correctamente.")
        self.limpiar_entradas()

    def eliminar_alumno(self):
        #Método para eliminar un ingreso
        dni = self.dni_entry.get()
        if dni in self.alumnos:
            del self.alumnos[dni]
            messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró un alumno con este DNI.")

    def consultar_alumno(self):
        #Método para consultar una nota
        dni = self.dni_entry.get()
        if dni in self.alumnos:
            alumno = self.alumnos[dni]
            self.mostrar_resultado(f"DNI: {dni}, {alumno['apellidos']}, {alumno['nombre']} - Nota: {alumno['nota']} - Calificación: {alumno['calificacion']}")
        else:
            messagebox.showerror("Error", "No se encontró un alumno con este DNI.")

    def modificar_nota(self):
        #Método para modificar la nota
        dni = self.dni_entry.get()
        if dni in self.alumnos:
            try:
                nueva_nota = float(self.nota_entry.get())
            except ValueError:
                messagebox.showerror("Error", "La nota debe ser un número válido.")
                return

            self.alumnos[dni]["nota"] = nueva_nota
            self.alumnos[dni]["calificacion"] = self.calcular_calificacion(nueva_nota)
            messagebox.showinfo("Éxito", "Nota modificada correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró un alumno con este DNI.")

    #Métodos para mostrar nota dependiendo su clasificación
    def mostrar_suspensos(self):
        resultado = [f"{dni}, {datos['apellidos']}, {datos['nombre']} - Nota: {datos['nota']} - Calificación: {datos['calificacion']}"
                     for dni, datos in self.alumnos.items() if datos['nota'] < 5]
        self.mostrar_resultado("\n".join(resultado) if resultado else "No hay alumnos suspensos.")

    def mostrar_aprobados(self):
        resultado = [f"{dni}, {datos['apellidos']}, {datos['nombre']} - Nota: {datos['nota']} - Calificación: {datos['calificacion']}"
                     for dni, datos in self.alumnos.items() if datos['nota'] >= 5]
        self.mostrar_resultado("\n".join(resultado) if resultado else "No hay alumnos aprobados.")

    def mostrar_mh(self):
        resultado = [f"{dni}, {datos['apellidos']}, {datos['nombre']} - Nota: {datos['nota']} - Calificación: {datos['calificacion']}"
                     for dni, datos in self.alumnos.items() if datos['nota'] == 10]
        self.mostrar_resultado("\n".join(resultado) if resultado else "No hay candidatos a MH.")

    def mostrar_todos(self):
        resultado = [f"{dni}, {datos['apellidos']}, {datos['nombre']} - Nota: {datos['nota']} - Calificación: {datos['calificacion']}"
                     for dni, datos in self.alumnos.items()]
        self.mostrar_resultado("\n".join(resultado) if resultado else "No hay alumnos registrados.")

    def mostrar_resultado(self, texto):
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, texto)

    def limpiar_entradas(self):
        self.dni_entry.delete(0, tk.END)
        self.apellidos_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.nota_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()# Crear la ventana principal de la aplicación
    app = GestionCalificaciones(root)# Instanciar la interfaz
    root.mainloop()# Iniciar el bucle principal de la aplicación
