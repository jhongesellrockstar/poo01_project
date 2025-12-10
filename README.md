import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import tkintermapview 

# --- DEFINICIÓN DE COLORES Y ESTILOS GLOBALES ---
# Usaremos una paleta cálida y amigable
COLOR_BG_MAIN = "#FDF6E4"   # Un crema muy suave para el fondo general
COLOR_BG_CARD = "#FFFFFF"   # Blanco puro para las tarjetas
COLOR_PRIMARY = "#FFAB40"   # Naranja cálido para acciones principales
COLOR_SECONDARY = "#4FC3F7" # Azul claro para acciones secundarias
COLOR_ACCENT = "#8BC34A"    # Verde para confirmaciones
COLOR_TEXT = "#3E2723"      # Marrón oscuro en lugar de negro puro (más suave)
COLOR_TEXT_LIGHT = "#757575" # Gris para subtítulos

FONT_TITLE = ("Helvetica", 26, "bold")
FONT_SUBTITLE = ("Helvetica", 16, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 12, "bold")

class PetApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Patitas Seguras - Adopción y Rescate")
        self.geometry("1150x850")
        self.configure(bg=COLOR_BG_MAIN) # ### ESTILO ### Color de fondo principal
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # --- Estilo para los Combobox (Filtros) ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # 'clam' permite personalizar más colores
        self.style.configure("TCombobox", fieldbackground=COLOR_BG_CARD, background=COLOR_BG_MAIN)

        # --- DATOS (Igual que antes) ---
        self.adopcion_data = [
            # PERROS
            {"nombre": "Max", "tipo": "Perro", "edad": "2 años", "color": "#D32F2F", "raza": "Labrador Mix", "sexo": "Macho", "tag": "URGENTE", "desc": "Max necesita un patio grande y mucho amor."},
            {"nombre": "Luna", "tipo": "Perro", "edad": "5 meses", "color": "#1976D2", "raza": "Mestizo", "sexo": "Hembra", "tag": "CACHORRO", "desc": "Luna es una cachorrita tranquila ideal para depa."},
            {"nombre": "Rocky", "tipo": "Perro", "edad": "4 años", "color": "#388E3C", "raza": "Pastor Alemán", "sexo": "Macho", "tag": "ENTRENADO", "desc": "Perro guardián excelente, muy obediente."},
            {"nombre": "Toby", "tipo": "Perro", "edad": "3 meses", "color": "#8D6E63", "raza": "Golden", "sexo": "Macho", "tag": "CACHORRO", "desc": "Muy juguetón, aprenderá rápido."},
            # GATOS
            {"nombre": "Garfield", "tipo": "Gato", "edad": "3 años", "color": "#FF9800", "raza": "Tabby", "sexo": "Macho", "tag": "CARIÑOSO", "desc": "Le encanta dormir y comer lasaña."},
            {"nombre": "Nieve", "tipo": "Gato", "edad": "2 meses", "color": "#E0E0E0", "raza": "Persa", "sexo": "Hembra", "tag": "CACHORRO", "desc": "Pequeña gatita rescatada."},
            {"nombre": "Sombra", "tipo": "Gato", "edad": "5 años", "color": "#212121", "raza": "Bombay", "sexo": "Hembra", "tag": "TRANQUILO", "desc": "Gatita adulta muy independiente y elegante."}
        ]
        self.perdidos_data = [
            {"id": 1, "nombre": "Bobby", "lat": -12.046374, "lon": -77.042793, "lugar": "Centro de Lima", "fecha": "10/12/2025", "color": "orange"},
            {"id": 2, "nombre": "Pelusa", "lat": -12.119332, "lon": -77.029226, "lugar": "Parque Kennedy", "fecha": "08/12/2025", "color": "purple"}
        ]
        self.mostrar_bienvenida()

    def crear_imagen(self, color, size=(150, 150)):
        img = Image.new('RGB', size, color=color)
        d = ImageDraw.Draw(img)
        # Un poco más minimalista el placeholder
        d.rectangle([(0,0), size], outline=color, width=5) 
        return ImageTk.PhotoImage(img)

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ==========================================
    # PANTALLA 1: BIENVENIDA (REDISEÑADA)
    # ==========================================
    def mostrar_bienvenida(self):
        self.limpiar_frame()
        
        # Header decorativo
        header_bg = tk.Frame(self.main_frame, bg=COLOR_PRIMARY, height=100)
        header_bg.pack(fill="x")
        tk.Label(header_bg, text="🐾 Patitas Seguras", font=("Helvetica", 32, "bold"), bg=COLOR_PRIMARY, fg="white").pack(pady=20)

        content = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        content.pack(fill="both", expand=True, pady=50)

        tk.Label(content, text="¿Qué deseas hacer hoy?", font=FONT_SUBTITLE, bg=COLOR_BG_MAIN, fg=COLOR_TEXT).pack(pady=(0, 40))
        
        btn_frame = tk.Frame(content, bg=COLOR_BG_MAIN)
        btn_frame.pack()

        # ### ESTILO ### Botones planos sin borde (bd=0) y colores nuevos
        tk.Button(btn_frame, text="🐶 Quiero Adoptar", font=FONT_BUTTON, bg=COLOR_ACCENT, fg="white", 
                  width=20, height=2, bd=0, cursor="hand2", activebackground="#7CB342",
                  command=self.mostrar_adopcion).grid(row=0, column=0, padx=20)

        tk.Button(btn_frame, text="🔍 Animales Perdidos", font=FONT_BUTTON, bg=COLOR_SECONDARY, fg="white", 
                  width=20, height=2, bd=0, cursor="hand2", activebackground="#29B6F6",
                  command=self.mostrar_perdidos).grid(row=0, column=1, padx=20)

    # ==========================================
    # PANTALLA 2: ADOPCIÓN (REDISEÑADA)
    # ==========================================
    def mostrar_adopcion(self):
        self.limpiar_frame()
        
        # 1. Cabecera
        nav_frame = tk.Frame(self.main_frame, bg="white", height=60, pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Volver", command=self.mostrar_bienvenida, 
                  bg="white", fg=COLOR_PRIMARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav_frame, text="Encuentra a tu compañero ideal", font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)

        # 2. Barra de Filtros (Más limpia)
        filter_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, pady=20, padx=30)
        filter_frame.pack(fill="x")
        
        lbl_filtro_style = {"bg": COLOR_BG_MAIN, "fg": COLOR_TEXT, "font": ("Helvetica", 10, "bold")}

        tk.Label(filter_frame, text="Tipo:", **lbl_filtro_style).pack(side="left", padx=(0,5))
        combo_especie = ttk.Combobox(filter_frame, values=["Todos", "Perro", "Gato"], state="readonly", width=12)
        combo_especie.current(0)
        combo_especie.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Etapa:", **lbl_filtro_style).pack(side="left", padx=(20,5))
        combo_edad = ttk.Combobox(filter_frame, values=["Todas", "Cachorro", "Adulto"], state="readonly", width=12)
        combo_edad.current(0)
        combo_edad.pack(side="left", padx=5)

        content_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        content_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # --- LÓGICA DE RENDERIZADO (Igual que antes) ---
        def renderizar_lista():
            for widget in content_frame.winfo_children():
                widget.destroy()

            filtro_tipo = combo_especie.get()
            filtro_edad = combo_edad.get()
            encontrados = 0

            for animal in self.adopcion_data:
                # (Lógica de filtrado idéntica a la anterior...)
                match_tipo = (filtro_tipo == "Todos") or (filtro_tipo == animal["tipo"])
                es_cachorro = "meses" in animal["edad"]
                match_edad = (filtro_edad == "Todas") or \
                             (filtro_edad == "Cachorro" and es_cachorro) or \
                             (filtro_edad == "Adulto" and not es_cachorro)

                if match_tipo and match_edad:
                    encontrados += 1
                    
                    # ### ESTILO ### TARJETA REDISEÑADA
                    # Usamos bg blanco sobre el fondo crema para contraste. Quitamos el borde negro (bd=0).
                    card = tk.Frame(content_frame, bd=0, bg=COLOR_BG_CARD, padx=0, pady=0)
                    # Un pequeño truco para dar una sombra sutil (un frame gris detrás ligeramente desplazado)
                    shadow = tk.Frame(content_frame, bg="#E0E0E0", bd=0)
                    shadow.pack(side="left", padx=(15, 0), pady=(15, 10), anchor="n")
                    card.pack(in_=shadow, padx=(0, 2), pady=(0, 2)) # La tarjeta va DENTRO de la sombra

                    # Barra de color superior
                    tk.Frame(card, height=8, bg=animal['color']).pack(fill="x")

                    # Foto con margen limpio
                    img = self.crear_imagen(animal["color"], size=(220, 180))
                    lbl_img = tk.Label(card, image=img, bg=COLOR_BG_CARD)
                    lbl_img.image = img
                    lbl_img.pack(pady=15, padx=15)

                    # Tag (Etiqueta) rediseñada
                    # Usamos un frame para simular una etiqueta redondeada
                    tag_frame = tk.Frame(card, bg=COLOR_PRIMARY, padx=8, pady=4)
                    tag_frame.place(x=15, y=20)
                    tk.Label(tag_frame, text=animal['tag'], font=("Arial", 8, "bold"), bg=COLOR_PRIMARY, fg="white").pack()

                    # Datos
                    tk.Label(card, text=animal['nombre'], font=("Helvetica", 18, "bold"), bg=COLOR_BG_CARD, fg=COLOR_TEXT).pack()
                    
                    det_frame = tk.Frame(card, bg=COLOR_BG_CARD, pady=5)
                    det_frame.pack()
                    # Usamos iconos unicode para darle vida
                    tk.Label(det_frame, text=f"🐾 {animal['raza']}", font=FONT_BODY, bg=COLOR_BG_CARD, fg=COLOR_TEXT_LIGHT).pack()
                    tk.Label(det_frame, text=f"🎂 {animal['edad']} | {animal['sexo']}", font=FONT_BODY, bg=COLOR_BG_CARD, fg=COLOR_TEXT_LIGHT).pack()

                    # Botón "Ver Más" plano
                    tk.Button(card, text="Conocer más", bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON, 
                              bd=0, cursor="hand2", pady=5, width=18, activebackground="#7CB342",
                              command=lambda p=animal: self.mostrar_formulario_adopcion(p)).pack(pady=20, padx=20)

            if encontrados == 0:
                tk.Label(content_frame, text="😿 No encontramos animalitos con esa combinación.", 
                         font=FONT_SUBTITLE, bg=COLOR_BG_MAIN, fg=COLOR_TEXT_LIGHT).pack(pady=50)

        # Botón Buscar plano
        tk.Button(filter_frame, text="🔍 Buscar", bg=COLOR_SECONDARY, fg="white", font=FONT_BUTTON, bd=0, cursor="hand2",
                  padx=10, command=renderizar_lista).pack(side="left", padx=20)

        renderizar_lista()

    # ==========================================
    # PANTALLA 3: FORMULARIO (REDISEÑADO)
    # ==========================================
    def mostrar_formulario_adopcion(self, animal):
        self.limpiar_frame()
        # Navbar limpia
        nav_frame = tk.Frame(self.main_frame, bg="white", pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Volver al listado", command=self.mostrar_adopcion,
                  bg="white", fg=COLOR_PRIMARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)

        # Contenedor principal blanco sobre fondo crema
        main_content = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=40, pady=20)
        main_content.pack(fill="both", expand=True)
        
        card_detail = tk.Frame(main_content, bg=COLOR_BG_CARD, padx=30, pady=30)
        card_detail.pack(fill="both", expand=True)

        # --- SECCIÓN SUPERIOR ---
        top_section = tk.Frame(card_detail, bg=COLOR_BG_CARD)
        top_section.pack(fill="x", pady=(0, 20))
        
        img = self.crear_imagen(animal["color"], size=(300, 300))
        lbl_img = tk.Label(top_section, image=img, bg=COLOR_BG_CARD) # Sin borde
        lbl_img.image = img
        lbl_img.pack(side="left")

        info_frame = tk.Frame(top_section, padx=40, bg=COLOR_BG_CARD)
        info_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(info_frame, text=animal['nombre'], font=("Helvetica", 36, "bold"), fg=COLOR_TEXT, bg=COLOR_BG_CARD).pack(anchor="w")
        
        # Badges (Etiquetas) de información
        badges_frame = tk.Frame(info_frame, bg=COLOR_BG_CARD)
        badges_frame.pack(anchor="w", pady=15)
        badge_style = {"bg": "#ECEFF1", "fg": COLOR_TEXT, "padx": 12, "pady": 6, "font": ("Helvetica", 10)}
        for dato in [f"🐶 {animal['tipo']}", f"🦴 {animal['raza']}", f"⚧ {animal['sexo']}", f"🎂 {animal['edad']}"]:
            lbl = tk.Label(badges_frame, text=dato, **badge_style)
            lbl.pack(side="left", padx=(0, 10))

        tk.Label(info_frame, text="Mi Historia:", font=FONT_SUBTITLE, bg=COLOR_BG_CARD, fg=COLOR_TEXT).pack(anchor="w", pady=(20, 10))
        tk.Label(info_frame, text=animal['desc'], font=FONT_BODY, justify="left", wraplength=450, fg=COLOR_TEXT_LIGHT, bg=COLOR_BG_CARD).pack(anchor="w")

        # Separador sutil
        tk.Frame(card_detail, height=1, bg="#ECEFF1").pack(fill="x", pady=20)
        
        # --- SECCIÓN INFERIOR: FORMULARIO ---
        form_section = tk.Frame(card_detail, bg=COLOR_BG_CARD)
        form_section.pack()

        tk.Label(form_section, text="📝 Estoy interesado/a", font=FONT_SUBTITLE, fg=COLOR_PRIMARY, bg=COLOR_BG_CARD).pack(pady=10)
        
        # Estilo de los inputs
        input_frame = tk.Frame(form_section, bg=COLOR_BG_CARD, pady=10)
        input_frame.pack()
        lbl_input_style = {"bg": COLOR_BG_CARD, "font": FONT_BODY, "fg": COLOR_TEXT}
        
        tk.Label(input_frame, text="Nombre Completo:", **lbl_input_style).grid(row=0, column=0, sticky="e", pady=10, padx=10)
        # Usamos ipady en el Entry para que sea más alto y moderno
        entry_nombre = tk.Entry(input_frame, width=30, font=FONT_BODY, bd=1, relief="solid", fg=COLOR_TEXT)
        entry_nombre.grid(row=0, column=1, ipady=5)

        tk.Label(input_frame, text="Celular:", **lbl_input_style).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        entry_cel = tk.Entry(input_frame, width=30, font=FONT_BODY, bd=1, relief="solid", fg=COLOR_TEXT)
        entry_cel.grid(row=1, column=1, ipady=5)

        def enviar():
            if entry_nombre.get() and entry_cel.get():
                messagebox.showinfo("¡Solicitud Enviada!", f"¡Gracias {entry_nombre.get()}!\nNos pondremos en contacto.")
                self.mostrar_bienvenida()
            else:
                messagebox.showerror("Faltan Datos", "Por favor completa tu nombre y celular.")

        tk.Button(form_section, text="Enviar Solicitud", bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON, bd=0, 
                  cursor="hand2", width=25, pady=8, command=enviar).pack(pady=20)

    # ==========================================
    # PANTALLA 4: PERDIDOS (REDISEÑADA)
    # ==========================================
    def mostrar_perdidos(self):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="white", height=60, pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Volver", command=self.mostrar_bienvenida, 
                  bg="white", fg=COLOR_PRIMARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav_frame, text="Animales Perdidos y Encontrados", font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)

        content_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=30, pady=20)
        content_frame.pack(fill="both", expand=True)

        for animal in self.perdidos_data:
            # Tarjeta de lista más limpia
            row = tk.Frame(content_frame, bg=COLOR_BG_CARD, padx=15, pady=15)
            row.pack(fill="x", pady=8)
            
            # Pequeña barra de color lateral
            tk.Frame(row, width=5, bg=animal['color']).pack(side="left", fill="y")

            img = self.crear_imagen(animal["color"], size=(70, 70))
            lbl_img = tk.Label(row, image=img, bg=COLOR_BG_CARD)
            lbl_img.image = img
            lbl_img.pack(side="left", padx=15)

            text_frame = tk.Frame(row, bg=COLOR_BG_CARD)
            text_frame.pack(side="left", padx=10, fill="x", expand=True)
            
            tk.Label(text_frame, text=animal['nombre'], font=("Helvetica", 16, "bold"), bg=COLOR_BG_CARD, fg=COLOR_TEXT, anchor="w").pack(fill="x")
            
            details = tk.Frame(text_frame, bg=COLOR_BG_CARD)
            details.pack(anchor="w", pady=5)
            tk.Label(details, text=f"📍 {animal['lugar']}", font=FONT_BODY, fg=COLOR_TEXT_LIGHT, bg=COLOR_BG_CARD).pack(side="left", padx=(0,15))
            tk.Label(details, text=f"📅 {animal['fecha']}", font=FONT_BODY, fg=COLOR_TEXT_LIGHT, bg=COLOR_BG_CARD).pack(side="left")

            tk.Button(row, text="🗺️ Ver Ubicación", bg=COLOR_SECONDARY, fg="white", font=("Arial", 10, "bold"),
                      bd=0, cursor="hand2", padx=10, pady=5,
                      command=lambda a=animal: self.mostrar_mapa_detalle(a)).pack(side="right", padx=10)

    def mostrar_mapa_detalle(self, animal_data):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="white", pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Volver a lista", command=self.mostrar_perdidos,
                   bg="white", fg=COLOR_PRIMARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav_frame, text=f"Ubicación: {animal_data['lugar']}", font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)

        map_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=20, pady=20)
        map_frame.pack(fill="both", expand=True)
        
        map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=600, corner_radius=10) # corner_radius para bordes redondeados en el mapa
        map_widget.pack(fill="both", expand=True)

        lat = animal_data["lat"]
        lon = animal_data["lon"]
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(16)
        map_widget.set_marker(lat, lon, text=f"¡{animal_data['nombre']} visto aquí!")

if __name__ == "__main__":
    app = PetApp()
    app.mainloop()
