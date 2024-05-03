import tkinter as tk
import Sistema
import Carga

class Window(tk.Tk):
    
    radio = 10

    def __init__(self):
        super().__init__()

        # Titulo de la ventana
        self.title("Simulador de campo eléctrico")

        # Configuración de la ventana
        self.resizable(False, False)
        self.config_width = 800
        self.config_height = 600

        # Configuracion de las opciones de visualización
        self.mostrar_equipotenciales = tk.BooleanVar()

        # Cargar cargas por defecto
        sistema = Sistema.Sistema()
        q1 = Carga.Carga(100, 300, 1)
        sistema.agregarCarga(q1)
        q2 = Carga.Carga(700, 300, -1)
        sistema.agregarCarga(q2)
        
        # Crear el canvas para dibujar las cargas
        self.canvas = tk.Canvas(self, width=self.config_width, height=self.config_height, bg='black')
        
        # Configuracion predeterminada de visualización
        self.mostrar_equipotenciales.set(False)
        
        # Mostrar campo eléctrico
        self.mostrar_campo(Sistema.Sistema)

        # Empaqueta los widgets en la ventana
        self.canvas.pack(side=tk.LEFT)


    def cargaPositiva(self):
        q = Carga.Carga(self.x, self.y, 1)
        Sistema.sistema.agregarCarga(q)

    def cargaNegativa(self):
        q = Carga.Carga(self.x, self.y, -1)
        Sistema.sistema.agregarCarga(q)

    def sensor(self):
        p = Carga.Carga(self.x, self.y, 0)
        Sistema.sistema.agregarCarga(p)
    
    # eliminar carga si se da click derecho en una carga
    def eliminarCarga(self):
        for carga in self.sistema.obtenerCargas():
            if self.x == carga.X() and self.y == carga.Y():
                Sistema.sistema.eliminarCarga(carga)
                break
    
    
    def actualizarSistema(self):
        # Obtener posicion del mouse
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()

        # Actualizar coordenadas de las cargas
        for carga in self.sistema.obtenerCargas():
            self.Carga.X = self.canvas.coords(carga)[0] + self.radio
            self.Carga.Y = self.canvas.coords(carga)[1] + self.radio

    def moverCarga(self):
        self.cargaSeleccionada = True

        # Obtener posicion de la carga
        coordenadas_carga_seleccionada = self.canvas.coords(self.cargaSeleccionada)

        # Mover la carga a la posicion del mouse
        self.canvas.move(self.cargaSeleccionada, self.x - coordenadas_carga_seleccionada[0], self.y - coordenadas_carga_seleccionada[1])


    def dibujarEquipotenciales(self):
        pass
    
    def mostrar_campo(self, sistema):
        vectores_separacion = 50

        # Dibujar los vectores del campo eléctrico
        for i in range(self.config_width // vectores_separacion):
            for j in range(self.config_height // vectores_separacion):

                x = i * vectores_separacion
                y = j * vectores_separacion

                f = sistema.campoElectrico(x, y)

            # Dibujar el campo eléctrico
            vector = self.canvas.create_line(x * vectores_separacion, y * vectores_separacion,
                x * vectores_separacion + sistema[0], y * vectores_separacion + sistema[1], fill="white", arrow=tk.LAST)

            self.canvas.addtag_withtag("campo", vector)


    def mostrar_cargas(self):
        for carga in self.sistema.obtenerCargas():
            if carga.Signo() == 1:
                color = "red"
            elif carga.Signo() == -1:
                color = "blue"
            else:
                color = "yellow"

        # Dibujar la carga
        carga = self.canvas.create_oval(carga.X() - self.radio, carga.Y() - self.radio,
            carga.X() + self.radio, carga.Y() + self.radio, fill=color)
        
        self.canvas.addtag_withtag("carga", carga)

class panel_lateral(tk.Frame):
    def __init__(self, x, y):
        super().__init__()

        self.x_label = tk.StringVar()
        self.y_label = tk.StringVar()
        self.field_label = tk.StringVar()

        self.x_label = tk.Label(self, textvariable=self.x_label, width=15)
        self.y_label = tk.Label(self, textvariable=self.y_label, width=15)
        self.field_label = tk.Label(self, textvariable=self.field_label, width=30)

        self.mostrar_equipotenciales = tk.Checkbutton(self, text="Mostrar lineas equipotenciales", variable = tk.intvars(0))

        self.create_pro = tk.Button(self, text="Carga positiva")
        self.create_ele = tk.Button(self, text="Carga negativa")
        self.delete_par = tk.Button(self, text="Eliminar carga")
        self.create_sen = tk.Button(self, text="Agregar sensor")

        self.x_label.grid(row=0, column=0)
        self.y_label.grid(row=0, column=1)