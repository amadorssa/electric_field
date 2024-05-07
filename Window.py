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
        self.resizable(True, True)
        self.config_width = 800
        self.config_height = 800

        # Configuracion de las opciones de visualización
        self.mostrar_lineas_campo = tk.BooleanVar()
        self.mostrar_equipotenciales = tk.BooleanVar()


        # Cargar cargas por defecto
        self.sistema = Sistema.Sistema()
        q1 = Carga.Carga(100, 400, 1)
        self.sistema.agregarCarga(q1)
        q2 = Carga.Carga(700, 400, -1)
        self.sistema.agregarCarga(q2)
        
        # Crear el canvas para dibujar las cargas
        self.canvas = tk.Canvas(self, width=self.config_width, height=self.config_height,
            bg='black')
        
        # Crear panel lateral
        self.panel = panel_lateral(self.sistema, 
            (self.mostrar_lineas_campo, self.mostrar_equipotenciales), 
            (self.cargaPositiva, self.cargaNegativa, self.sensor),
            self, bd=0, highlightthickness=0)
        
        # Configuracion predeterminada de visualización
        self.mostrar_lineas_campo.set(True)
        self.mostrar_equipotenciales.set(False)
        
        # Mostrar campo eléctrico
        self.mostrar_campo(self.sistema)

        # Mostrar cargas
        self.mostrar_cargas(self.sistema)

        self.click_mode = None
        self.carga_seleccionada = None

        # Vincular eventos
        self.canvas.bind("<Motion>", self.panel.actualizar_panel)
        self.vincular_eventos()
        self.canvas.bind("<ButtonRelease-1>", self.deseleccionar_carga)

        # Empaqueta los widgets en la ventana
        self.canvas.grid(row=0, column=0)
        self.panel.grid(row=0, column=1)

        self.update()

        # Actualizar el sistema
        self.after(0, self.actualizarSistema)
        self.mainloop()

    # ********** Cargas **********

    def cargaPositiva(self):
        p = Carga.Carga(500,500, 1)
        self.sistema.agregarCarga(p)
        self.refrescar_cargas()
        self.click_mode = None


    def cargaNegativa(self):
        e = Carga.Carga(500,500, -1)
        self.sistema.agregarCarga(e)
        self.refrescar_cargas()
        self.click_mode = None


    def sensor(self):
        s = Carga.Carga(500,500, 0)
        self.sistema.agregarCarga(s)
        self.refrescar_cargas()
        self.click_mode = None
    
    def moverCarga(self):
        # Obtener posición del mouse
        mouse_x = self.winfo_pointerx() - self.winfo_rootx()
        mouse_y = self.winfo_pointery() - self.winfo_rooty()

        if self.carga_seleccionada is not None:
            carga_seleccionada_coord = self.canvas.coords(self.carga_seleccionada)

            self.canvas.move(self.carga_seleccionada, 
                mouse_x - self.radio - carga_seleccionada_coord[0],
                mouse_y - self.radio - carga_seleccionada_coord[1])

        # Actualizar coordenadas de las cargas
        for carga in self.sistema.obtenerCargas():            
            carga.asignarX(self.canvas.coords(carga.obtenerId())[0] + self.radio)
            carga.asignarY(self.canvas.coords(carga.obtenerId())[1] + self.radio)

    # ********** Visualización **********
    
    def mostrar_campo(self, sistema):
        vectores_separacion = 40

        # Dibujar los vectores del campo eléctrico
        for i in range(self.config_width // vectores_separacion):
            for j in range(self.config_height // vectores_separacion):

                x = i * vectores_separacion
                y = j * vectores_separacion

                v = self.sistema.campoElectrico(x, y)

                # Normalizar el vector
                magnitud = self.sistema.distancia([0, 0], v)/25
                if magnitud != 0:
                    v[0] /= magnitud
                    v[1] /= magnitud

                # Dibujar el campo eléctrico
                vector = self.canvas.create_line(x, y, x + v[0], y + v[1],
                    fill="white", arrow=tk.LAST,width=4,capstyle=tk.ROUND,joinstyle=tk.BEVEL)

                self.canvas.addtag_withtag("campo", vector)

    def mostrar_cargas(self, sistema):
        for carga in self.sistema.obtenerCargas():
            if carga.Signo() == 1:
                color = "red"
            elif carga.Signo() == -1:
                color = "blue"
            else:
                color = "yellow"

            # Dibujar la carga
            p = self.canvas.create_oval(carga.X() - self.radio, carga.Y() - self.radio,
                carga.X() + self.radio, carga.Y() + self.radio, outline=color, fill=color)
            
            carga.asignarId(p)

            self.canvas.addtag_withtag("carga", p)

    def mostrar_vector_sensor(self):
        self.canvas.delete("vectorSensor")
        self.canvas.delete("magnitudCampo")
        self.canvas.delete("potencialCampo")
        for carga in self.sistema.obtenerCargas():
            if carga.Signo() == 0:
                E = self.sistema.campoElectrico(carga.X(), carga.Y())
                V=self.sistema.potencialElectrico(carga.X(),carga.Y())
                self.canvas.create_line(carga.X(), carga.Y(), carga.X() + E[0]*300000.0, carga.Y() + E[1]*300000.0,
                    fill="red", tags="vectorSensor", arrow=tk.LAST,width=2)
                self.canvas.create_text(carga.X()+75,carga.Y()-6,text="E="+str(round((E[0]**2+E[1]**2)**(1/2),7))+" V/m",font=("Arial",10),fill='red',tags="magnitudCampo")
                self.canvas.create_text(carga.X()+75,carga.Y()+10,text="V="+str(round(V,7))+" V",font=("Arial",10),fill='red',tags="potencialCampo")
    def dibujar_equipotenciales(self):
        pass        

    def refrescar_campo(self):
        self.canvas.delete("campo")
        self.mostrar_campo(self.sistema)

    def refrescar_cargas(self):
        self.canvas.delete("carga")
        self.mostrar_cargas(self.sistema)
        self.vincular_eventos()


    # ********** Eventos **********

    def vincular_eventos(self):
        for carga in self.sistema.obtenerCargas():
            self.canvas.tag_bind(carga.obtenerId(), "<Button-1>", self.seleccionar_carga)
            self.canvas.tag_bind(carga.obtenerId(), "<Button-2>", self.eliminar_carga)
           
    def seleccionar_carga(self, event):
        q = self.canvas.find_withtag(tk.CURRENT)[0]
        self.carga_seleccionada = q

    def deseleccionar_carga(self, event):
        if self.carga_seleccionada is not None:
            self.carga_seleccionada = None
        
        self.click_mode = None

    def eliminar_carga(self, event):
        q = self.canvas.find_withtag(tk.CURRENT)[0]

        for carga in self.sistema.obtenerCargas():
            if carga.obtenerId() == q:
                self.sistema.eliminarCarga(carga)
                break
        
        self.refrescar_cargas()

    def actualizarSistema(self):
        self.moverCarga()
        self.mostrar_vector_sensor()

        # Actualizar campo eléctrico
        self.canvas.delete("campo")
        if self.mostrar_lineas_campo.get():
            self.mostrar_campo(self.sistema)

        self.canvas.tag_raise("carga")

        self.after(10,self.actualizarSistema)

class panel_lateral(tk.Frame):
    def __init__(self, campo,casillas, botones, *args, **kwargs):
        super().__init__()

        self.x_etiqueta_str = tk.StringVar()
        self.y_etiqueta_str = tk.StringVar()
        self.campo_etiqueta_str = tk.StringVar()

        self.x_etiqueta = tk.Label(self, textvariable=self.x_etiqueta_str, width=15)
        self.y_etiqueta = tk.Label(self, textvariable=self.y_etiqueta_str, width=15)
        self.campo_etiqueta = tk.Label(self, textvariable=self.campo_etiqueta_str, width=30)

        self.campo_casilla = tk.Checkbutton(self, text="Campo electrico", variable = casillas[0])
        self.equipotenciales_casillas = tk.Checkbutton(self, text="Lineas equipotenciales", variable = casillas[1])

        self.btn_positiva = tk.Button(self, text="Agregar carga positiva", command=botones[0])
        self.btn_negativa = tk.Button(self, text="Agregar carga negativa", command=botones[1])
        self.btn_sensor = tk.Button(self, text="Agregar sensor", command=botones[2])

        self.x_etiqueta.grid(row=0, column=0)
        self.y_etiqueta.grid(row=0, column=1)
        self.campo_etiqueta.grid(row=1, column=0, columnspan=2)
        self.campo_casilla.grid(row=2, column=0, columnspan=2)
        self.equipotenciales_casillas.grid(row=3, column=0, columnspan=2)
        self.btn_positiva.grid(row=4, column=0, columnspan=2)
        self.btn_negativa.grid(row=5, column=0, columnspan=2)
        self.btn_sensor.grid(row=6, column=0, columnspan=2)

        self.campo = campo

    def actualizar_panel(self, mov):
        self.x_etiqueta_str.set("X: {}".format(mov.x))
        self.y_etiqueta_str.set("Y: {}".format(mov.y))

        campo = self.campo.campoElectrico(mov.x, mov.y)

        self.campo_etiqueta_str.set("Campo eléctrico: {}")