# poo01_project
Proyecto de clase.
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import tkintermapview 

class PetApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Patitas Seguras - Adopción y Rescate")
        self.geometry("1100x800") 
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # --- DATOS: Notarás que la lógica de "Cachorro" se basa en si dice "meses" ---
        self.adopcion_data = [
            # PERROS
            {
                "nombre": "Max", "tipo": "Perro", "edad": "2 años", "color": "#D32F2F", 
                "raza": "Labrador Mix", "sexo": "Macho", "tag": "URGENTE",
                "desc": "Max necesita un patio grande y mucho amor."
            },
            {
                "nombre": "Luna", "tipo": "Perro", "edad": "5 meses", "color": "#1976D2", 
                "raza": "Mestizo", "sexo": "Hembra", "tag": "CACHORRO",
                "desc": "Luna es una cachorrita tranquila ideal para depa."
            },
            {
                "nombre": "Rocky", "tipo": "Perro", "edad": "4 años", "color": "#388E3C", 
                "raza": "Pastor Alemán", "sexo": "Macho", "tag": "ENTRENADO",
                "desc": "Perro guardián excelente, muy obediente."
            },
            {
                "nombre": "Toby", "tipo": "Perro", "edad": "3 meses", "color": "#8D6E63", 
                "raza": "Golden", "sexo": "Macho", "tag": "CACHORRO",
                "desc": "Muy juguetón, aprenderá rápido."
            },
            # GATOS
            {
                "nombre": "Garfield", "tipo": "Gato", "edad": "3 años", "color": "#FF9800",
                "raza": "Tabby", "sexo": "Macho", "tag": "CARIÑOSO",
                "desc": "Le encanta dormir y comer lasaña. Muy tranquilo."
            },
            {
                "nombre": "Nieve", "tipo": "Gato", "edad": "2 meses", "color": "#E0E0E0",
                "raza": "Persa", "sexo": "Hembra", "tag": "CACHORRO",
                "desc": "Pequeña gatita rescatada, necesita cuidados especiales."
            },
            {
                "nombre": "Sombra", "tipo": "Gato", "edad": "5 años", "color": "#212121",
                "raza": "Bombay", "sexo": "Hembra", "tag": "TRANQUILO",
                "desc": "Gatita adulta muy independiente y elegante."
            }
        ]

        self.perdidos_data = [
            {"id": 1, "nombre": "Bobby", "lat": -12.046374, "lon": -77.042793, 
             "lugar": "Centro de Lima", "fecha": "10/12/2025", "color": "orange"},
            {"id": 2, "nombre": "Pelusa", "lat": -12.119332, "lon": -77.029226, 
             "lugar": "Parque Kennedy", "fecha": "08/12/2025", "color": "purple"}
        ]

        self.mostrar_bienvenida()

    def crear_imagen(self, color, size=(150, 150)):
        img = Image.new('RGB', size, color=color)
        d = ImageDraw.Draw(img)
        d.text((size[0]//3, size[1]//2), "FOTO", fill=(255, 255, 255))
        return ImageTk.PhotoImage(img)

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ==========================================
    # PANTALLA 1: BIENVENIDA
    # ==========================================
    def mostrar_bienvenida(self):
        self.limpiar_frame()
        frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="¡Bienvenido a Patitas Seguras!", font=("Helvetica", 28, "bold"), bg="#f0f0f0", fg="#333").pack(pady=60)
        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="🐶 Adoptar un Amigo", font=("Arial", 16), bg="#4CAF50", fg="white", 
                  width=22, height=3, cursor="hand2", command=self.mostrar_adopcion).grid(row=0, column=0, padx=30)
        tk.Button(btn_frame, text="🔍 Animales Perdidos", font=("Arial", 16), bg="#FF5722", fg="white", 
                  width=22, height=3, cursor="hand2", command=self.mostrar_perdidos).grid(row=0, column=1, padx=30)

    # ==========================================
    # PANTALLA 2: ADOPCIÓN (FILTRO DOBLE)
    # ==========================================
    def mostrar_adopcion(self):
        self.limpiar_frame()
        
        # 1. Cabecera
        nav_frame = tk.Frame(self.main_frame, bg="#eee", height=60)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="< Inicio", command=self.mostrar_bienvenida, bg="white").pack(side="left", padx=15, pady=10)
        tk.Label(nav_frame, text="Encuentra a tu compañero ideal", font=("Arial", 16, "bold"), bg="#eee").pack(side="left", padx=20)

        # 2. Barra de Filtros (DOBLE MENU)
        filter_frame = tk.Frame(self.main_frame, bg="white", pady=15, padx=20)
        filter_frame.pack(fill="x")
        
        # --- FILTRO 1: ESPECIE ---
        tk.Label(filter_frame, text="Tipo:", bg="white", font=("Arial", 10, "bold")).pack(side="left", padx=(0,5))
        combo_especie = ttk.Combobox(filter_frame, values=["Todos", "Perro", "Gato"], state="readonly", width=10)
        combo_especie.current(0)
        combo_especie.pack(side="left", padx=5)

        # --- FILTRO 2: EDAD/ETAPA ---
        tk.Label(filter_frame, text="Etapa:", bg="white", font=("Arial", 10, "bold")).pack(side="left", padx=(20,5))
        combo_edad = ttk.Combobox(filter_frame, values=["Todas", "Cachorro", "Adulto"], state="readonly", width=10)
        combo_edad.current(0)
        combo_edad.pack(side="left", padx=5)

        content_frame = tk.Frame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # --- LÓGICA DE FILTRADO ---
        def renderizar_lista():
            for widget in content_frame.winfo_children():
                widget.destroy()

            # Obtener valores de los dos combos
            filtro_tipo = combo_especie.get() # "Todos", "Perro", "Gato"
            filtro_edad = combo_edad.get()    # "Todas", "Cachorro", "Adulto"
            
            encontrados = 0

            for animal in self.adopcion_data:
                # 1. Validar Tipo
                match_tipo = False
                if filtro_tipo == "Todos":
                    match_tipo = True
                elif filtro_tipo == animal["tipo"]:
                    match_tipo = True

                # 2. Validar Edad (Logica: si tiene "meses" es cachorro)
                match_edad = False
                es_cachorro = "meses" in animal["edad"] # Verdadero si es cachorro
                
                if filtro_edad == "Todas":
                    match_edad = True
                elif filtro_edad == "Cachorro" and es_cachorro:
                    match_edad = True
                elif filtro_edad == "Adulto" and not es_cachorro:
                    match_edad = True

                # 3. SI CUMPLE AMBOS REQUISITOS (AND) -> MOSTRAR
                if match_tipo and match_edad:
                    encontrados += 1
                    
                    # Dibujar Tarjeta
                    card = tk.Frame(content_frame, bd=1, relief="solid", bg="white")
                    card.pack(side="left", padx=10, pady=10, anchor="n")
                    
                    tk.Frame(card, height=5, bg=animal['color']).pack(fill="x") 
                    
                    img = self.crear_imagen(animal["color"], size=(180, 150))
                    lbl_img = tk.Label(card, image=img, bg="white")
                    lbl_img.image = img 
                    lbl_img.pack(pady=10, padx=10)

                    # Tag
                    lbl_tag = tk.Label(card, text=animal['tag'], font=("Arial", 7, "bold"), bg="#FFEB3B", fg="#333", padx=5)
                    lbl_tag.place(x=10, y=15)

                    tk.Label(card, text=animal['nombre'], font=("Arial", 14, "bold"), bg="white", fg="#333").pack()
                    
                    det_frame = tk.Frame(card, bg="white")
                    det_frame.pack(pady=5)
                    tk.Label(det_frame, text=f"{animal['raza']}", font=("Arial", 8), bg="white", fg="#555").pack()
                    tk.Label(det_frame, text=f"{animal['edad']} - {animal['sexo']}", font=("Arial", 8), bg="white").pack()

                    tk.Button(card, text="¡Ver Más!", bg="#8BC34A", fg="white", font=("Arial", 9, "bold"), cursor="hand2",
                              command=lambda p=animal: self.mostrar_formulario_adopcion(p)).pack(pady=10, padx=10)

            if encontrados == 0:
                tk.Label(content_frame, text="No encontramos animalitos con esa combinación :(", font=("Arial", 14), fg="gray").pack(pady=50)

        # Botón Buscar
        tk.Button(filter_frame, text="🔍 Buscar", bg="#2196F3", fg="white", cursor="hand2",
                  command=renderizar_lista).pack(side="left", padx=20)

        # Cargar lista inicial
        renderizar_lista()

    # ==========================================
    # PANTALLA 3: FORMULARIO DETALLE
    # ==========================================
    def mostrar_formulario_adopcion(self, animal):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="#eee")
        nav_frame.pack(fill="x", pady=0)
        tk.Button(nav_frame, text="< Volver al listado", command=self.mostrar_adopcion).pack(side="left", padx=10, pady=10)

        content_frame = tk.Frame(self.main_frame, padx=40, pady=20)
        content_frame.pack(fill="both", expand=True)

        top_section = tk.Frame(content_frame)
        top_section.pack(fill="x", pady=10)
        
        img = self.crear_imagen(animal["color"], size=(280, 280))
        lbl_img = tk.Label(top_section, image=img, bd=1, relief="solid")
        lbl_img.image = img
        lbl_img.pack(side="left")

        info_frame = tk.Frame(top_section, padx=30)
        info_frame.pack(side="left", fill="both", expand=True)
        tk.Label(info_frame, text=animal['nombre'], font=("Arial", 30, "bold"), fg="#333").pack(anchor="w")
        
        badges_frame = tk.Frame(info_frame)
        badges_frame.pack(anchor="w", pady=10)
        for dato in [f"Tipo: {animal['tipo']}", f"Raza: {animal['raza']}", f"Sexo: {animal['sexo']}", f"Edad: {animal['edad']}"]:
            lbl = tk.Label(badges_frame, text=dato, bg="#e0e0e0", padx=10, pady=5, font=("Arial", 10))
            lbl.pack(side="left", padx=5)

        tk.Label(info_frame, text="Historia:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15, 5))
        tk.Label(info_frame, text=animal['desc'], font=("Arial", 12), justify="left", wraplength=400, fg="#555").pack(anchor="w")

        tk.Frame(content_frame, height=2, bg="#ddd").pack(fill="x", pady=20)
        
        tk.Label(content_frame, text="📝 Formulario de Interés", font=("Arial", 18, "bold"), fg="#2196F3").pack(pady=5)
        form_frame = tk.Frame(content_frame, bg="#f9f9f9", bd=1, relief="solid", padx=30, pady=20)
        form_frame.pack()
        tk.Label(form_frame, text="Nombre Completo:", bg="#f9f9f9", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", pady=10)
        entry_nombre = tk.Entry(form_frame, width=35)
        entry_nombre.grid(row=0, column=1, padx=10)
        tk.Label(form_frame, text="Celular / WhatsApp:", bg="#f9f9f9", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", pady=10)
        entry_cel = tk.Entry(form_frame, width=35)
        entry_cel.grid(row=1, column=1, padx=10)

        def enviar():
            if entry_nombre.get() and entry_cel.get():
                messagebox.showinfo("¡Enviado!", f"¡Gracias {entry_nombre.get()}!\nLa solicitud por {animal['nombre']} ha sido registrada.")
                self.mostrar_bienvenida()
            else:
                messagebox.showerror("Error", "Por favor completa tu nombre y celular.")

        tk.Button(form_frame, text="Enviar Solicitud", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20,
                  command=enviar).grid(row=2, column=0, columnspan=2, pady=20)

    # ==========================================
    # PANTALLA 4: PERDIDOS
    # ==========================================
    def mostrar_perdidos(self):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="#eee")
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="< Volver", command=self.mostrar_bienvenida).pack(side="left", padx=10, pady=10)
        tk.Label(nav_frame, text="Animales Perdidos y Encontrados", font=("Arial", 16, "bold"), bg="#eee").pack(side="left", padx=20)

        content_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)

        for animal in self.perdidos_data:
            row = tk.Frame(content_frame, bd=1, relief="ridge", bg="white", padx=5, pady=5)
            row.pack(fill="x", pady=5)
            img = self.crear_imagen(animal["color"], size=(60, 60))
            lbl_img = tk.Label(row, image=img, bg="white")
            lbl_img.image = img
            lbl_img.pack(side="left", padx=10)
            text_frame = tk.Frame(row, bg="white")
            text_frame.pack(side="left", padx=10)
            tk.Label(text_frame, text=animal['nombre'], font=("Arial", 14, "bold"), bg="white", anchor="w").pack(fill="x")
            details = tk.Frame(text_frame, bg="white")
            details.pack(anchor="w")
            tk.Label(details, text=f"📍 {animal['lugar']}", font=("Arial", 10), fg="#555", bg="white").pack(side="left", padx=(0,10))
            tk.Label(details, text=f"📅 Fecha: {animal['fecha']}", font=("Arial", 10), fg="#777", bg="white").pack(side="left")
            tk.Button(row, text="🗺️ Ver Ubicación", bg="#03A9F4", fg="white", cursor="hand2",
                      command=lambda a=animal: self.mostrar_mapa_detalle(a)).pack(side="right", padx=15)

    def mostrar_mapa_detalle(self, animal_data):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="#eee")
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="< Volver a lista", command=self.mostrar_perdidos).pack(side="left", padx=10, pady=10)
        tk.Label(nav_frame, text=f"Ubicación: {animal_data['lugar']}", font=("Arial", 14, "bold"), bg="#eee").pack(side="left", padx=20)
        map_frame = tk.Frame(self.main_frame)
        map_frame.pack(fill="both", expand=True)
        map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)
        lat = animal_data["lat"]
        lon = animal_data["lon"]
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(16)
        map_widget.set_marker(lat, lon, text=f"¡{animal_data['nombre']} visto aquí!")

if __name__ == "__main__":
    app = PetApp()
    app.mainloop()
