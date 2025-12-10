import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk, ImageDraw
import tkintermapview 

# --- COLORES ---
COLOR_BG_MAIN = "#FDF6E4"   # Crema
COLOR_BG_CARD = "#FFFFFF"   # Blanco
COLOR_PRIMARY = "#FFAB40"   # Naranja
COLOR_SECONDARY = "#4FC3F7" # Azul
COLOR_ACCENT = "#8BC34A"    # Verde
COLOR_TEXT = "#3E2723"      # Marrón
COLOR_TEXT_LIGHT = "#757575" # Gris
COLOR_DANGER = "#EF5350"    # Rojo

FONT_TITLE = ("Helvetica", 26, "bold")
FONT_SUBTITLE = ("Helvetica", 16, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 12, "bold")

class PetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Patitas Seguras - Adopción y Rescate")
        self.geometry("1200x850")
        self.configure(bg=COLOR_BG_MAIN)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TCombobox", fieldbackground=COLOR_BG_CARD, background=COLOR_BG_MAIN)

        self.temp_report_lat = None
        self.temp_report_lon = None
        self.temp_report_img_path = None

        # --- DATOS ---
        self.adopcion_data = [
            {"nombre": "Max", "tipo": "Perro", "edad": "2 años", "color": "#D32F2F", "raza": "Labrador Mix", "sexo": "Macho", "tag": "URGENTE", "desc": "Max necesita un patio grande y mucho amor."},
            {"nombre": "Luna", "tipo": "Perro", "edad": "5 meses", "color": "#1976D2", "raza": "Mestizo", "sexo": "Hembra", "tag": "CACHORRO", "desc": "Luna es una cachorrita tranquila ideal para depa."},
            {"nombre": "Rocky", "tipo": "Perro", "edad": "4 años", "color": "#388E3C", "raza": "Pastor Alemán", "sexo": "Macho", "tag": "ENTRENADO", "desc": "Perro guardián excelente, muy obediente."},
            {"nombre": "Toby", "tipo": "Perro", "edad": "3 meses", "color": "#8D6E63", "raza": "Golden", "sexo": "Macho", "tag": "CACHORRO", "desc": "Muy juguetón, aprenderá rápido."},
            {"nombre": "Garfield", "tipo": "Gato", "edad": "3 años", "color": "#FF9800", "raza": "Tabby", "sexo": "Macho", "tag": "CARIÑOSO", "desc": "Le encanta dormir y comer lasaña."},
            {"nombre": "Nieve", "tipo": "Gato", "edad": "2 meses", "color": "#E0E0E0", "raza": "Persa", "sexo": "Hembra", "tag": "CACHORRO", "desc": "Pequeña gatita rescatada."}
        ]
        self.perdidos_data = [
            {"id": 1, "nombre": "Bobby", "lat": -12.046374, "lon": -77.042793, "lugar": "Centro de Lima", "fecha": "10/12/2025", "color": "orange", "img_path": None},
            {"id": 2, "nombre": "Pelusa", "lat": -12.119332, "lon": -77.029226, "lugar": "Parque Kennedy", "fecha": "08/12/2025", "color": "purple", "img_path": None}
        ]
        self.mostrar_bienvenida()

    def crear_imagen(self, color, size=(150, 150), path=None):
        if path:
            try:
                real_img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(real_img)
            except: pass
        img = Image.new('RGB', size, color=color)
        d = ImageDraw.Draw(img)
        d.rectangle([(5,5), (size[0]-5, size[1]-5)], outline="white", width=2)
        if not path: d.text((size[0]//3, size[1]//2), "FOTO", fill="white")
        return ImageTk.PhotoImage(img)

    def crear_icono_exito(self):
        size = (120, 120)
        img = Image.new('RGB', size, color=COLOR_BG_MAIN) 
        d = ImageDraw.Draw(img)
        d.ellipse([10, 10, 110, 110], fill=COLOR_ACCENT)
        d.line([(40, 60), (55, 80)], fill="white", width=8) 
        d.line([(55, 80), (85, 40)], fill="white", width=8) 
        return ImageTk.PhotoImage(img)

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- PANTALLA 1: BIENVENIDA ---
    def mostrar_bienvenida(self):
        self.limpiar_frame()
        header_bg = tk.Frame(self.main_frame, bg=COLOR_PRIMARY, height=100)
        header_bg.pack(fill="x")
        tk.Label(header_bg, text="🐾 Patitas Seguras", font=("Helvetica", 32, "bold"), bg=COLOR_PRIMARY, fg="white").pack(pady=30)
        content = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        content.pack(fill="both", expand=True, pady=50)
        tk.Label(content, text="¿Qué deseas hacer hoy?", font=FONT_SUBTITLE, bg=COLOR_BG_MAIN, fg=COLOR_TEXT).pack(pady=(0, 40))
        btn_frame = tk.Frame(content, bg=COLOR_BG_MAIN)
        btn_frame.pack()
        tk.Button(btn_frame, text="🐶 Quiero Adoptar", font=FONT_BUTTON, bg=COLOR_ACCENT, fg="white", width=20, height=2, bd=0, cursor="hand2", command=self.mostrar_adopcion).grid(row=0, column=0, padx=20)
        tk.Button(btn_frame, text="🔍 Animales Perdidos", font=FONT_BUTTON, bg=COLOR_SECONDARY, fg="white", width=20, height=2, bd=0, cursor="hand2", command=self.mostrar_perdidos).grid(row=0, column=1, padx=20)

    # --- PANTALLA 2: ADOPCIÓN ---
    def mostrar_adopcion(self):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="white", height=60, pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Volver", command=self.mostrar_bienvenida, bg="white", fg=COLOR_PRIMARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav_frame, text="Encuentra a tu compañero ideal", font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)

        filter_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, pady=20, padx=30)
        filter_frame.pack(fill="x")
        tk.Label(filter_frame, text="Tipo:", bg=COLOR_BG_MAIN, fg=COLOR_TEXT, font=("Helvetica", 10, "bold")).pack(side="left", padx=(0,5))
        combo_especie = ttk.Combobox(filter_frame, values=["Todos", "Perro", "Gato"], state="readonly", width=12)
        combo_especie.current(0)
        combo_especie.pack(side="left", padx=5)
        tk.Label(filter_frame, text="Etapa:", bg=COLOR_BG_MAIN, fg=COLOR_TEXT, font=("Helvetica", 10, "bold")).pack(side="left", padx=(20,5))
        combo_edad = ttk.Combobox(filter_frame, values=["Todas", "Cachorro", "Adulto"], state="readonly", width=12)
        combo_edad.current(0)
        combo_edad.pack(side="left", padx=5)

        content_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        content_frame.pack(fill="both", expand=True, padx=30, pady=10)

        def renderizar_lista():
            for widget in content_frame.winfo_children():
                widget.destroy()
            filtro_tipo = combo_especie.get()
            filtro_edad = combo_edad.get() 
            encontrados = 0
            for animal in self.adopcion_data:
                match_tipo = (filtro_tipo == "Todos") or (filtro_tipo == animal["tipo"])
                es_cachorro = "meses" in animal["edad"]
                match_edad = (filtro_edad == "Todas") or (filtro_edad == "Cachorro" and es_cachorro) or (filtro_edad == "Adulto" and not es_cachorro)
                if match_tipo and match_edad:
                    encontrados += 1
                    card_border = tk.Frame(content_frame, bg="#E0E0E0", padx=1, pady=1)
                    card_border.pack(side="left", padx=15, pady=15, anchor="n")
                    card = tk.Frame(card_border, bg="white", padx=0, pady=0)
                    card.pack(fill="both", expand=True)
                    tk.Frame(card, height=8, bg=animal['color']).pack(fill="x")
                    img = self.crear_imagen(animal["color"], size=(220, 180))
                    lbl_img = tk.Label(card, image=img, bg="white")
                    lbl_img.image = img
                    lbl_img.pack(pady=15, padx=15)
                    tag_frame = tk.Frame(card, bg=COLOR_PRIMARY, padx=8, pady=4)
                    tag_frame.place(x=15, y=20)
                    tk.Label(tag_frame, text=animal['tag'], font=("Arial", 8, "bold"), bg=COLOR_PRIMARY, fg="white").pack()
                    tk.Label(card, text=animal['nombre'], font=("Helvetica", 18, "bold"), bg="white", fg=COLOR_TEXT).pack()
                    details_frame = tk.Frame(card, bg="white")
                    details_frame.pack(pady=5)
                    tk.Label(details_frame, text=f"{animal['raza']} | {animal['sexo']}", font=("Arial", 10), bg="white", fg="gray").pack()
                    tk.Label(details_frame, text=f"Edad: {animal['edad']}", font=("Arial", 10), bg="white", fg="gray").pack()
                    tk.Button(card, text="Conocer más", bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON, bd=0, cursor="hand2", width=18, command=lambda p=animal: self.mostrar_formulario_adopcion(p)).pack(pady=20, padx=20)
            if encontrados == 0:
                tk.Label(content_frame, text="No hay resultados 😿", bg=COLOR_BG_MAIN, font=FONT_SUBTITLE).pack(pady=50)
        
        tk.Button(filter_frame, text="🔍 Buscar", bg=COLOR_SECONDARY, fg="white", font=FONT_BUTTON, bd=0, cursor="hand2", padx=10, command=renderizar_lista).pack(side="left", padx=20)
        renderizar_lista()

    # --- PANTALLA 3: FORMULARIO ADOPCIÓN ---
    def mostrar_formulario_adopcion(self, animal):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="white", pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Volver", command=self.mostrar_adopcion, bg="white", fg=COLOR_PRIMARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        
        main_content = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=40, pady=20)
        main_content.pack(fill="both", expand=True)
        card_detail = tk.Frame(main_content, bg=COLOR_BG_CARD, padx=30, pady=30)
        card_detail.pack(fill="both", expand=True)
        
        top_section = tk.Frame(card_detail, bg=COLOR_BG_CARD)
        top_section.pack(fill="x", pady=(0, 20))
        img = self.crear_imagen(animal["color"], size=(250, 250))
        lbl_img = tk.Label(top_section, image=img, bg=COLOR_BG_CARD)
        lbl_img.image = img
        lbl_img.pack(side="left")
        
        info_frame = tk.Frame(top_section, padx=40, bg=COLOR_BG_CARD)
        info_frame.pack(side="left", fill="both", expand=True)
        tk.Label(info_frame, text=animal['nombre'], font=("Helvetica", 36, "bold"), fg=COLOR_TEXT, bg=COLOR_BG_CARD).pack(anchor="w")
        badges_frame = tk.Frame(info_frame, bg=COLOR_BG_CARD)
        badges_frame.pack(anchor="w", pady=10)
        for dato in [animal['raza'], animal['sexo'], animal['edad']]:
             tk.Label(badges_frame, text=f"• {dato}", bg="#ECEFF1", padx=10, pady=5, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Label(info_frame, text=animal['desc'], font=FONT_BODY, justify="left", wraplength=450, fg=COLOR_TEXT_LIGHT, bg=COLOR_BG_CARD).pack(anchor="w", pady=20)
        
        tk.Frame(card_detail, height=2, bg="#EEEEEE").pack(fill="x", pady=20)
        tk.Label(card_detail, text="📝 Quiero Adoptar", font=FONT_SUBTITLE, fg=COLOR_PRIMARY, bg=COLOR_BG_CARD).pack(pady=10)
        
        input_frame = tk.Frame(card_detail, bg=COLOR_BG_CARD, pady=10)
        input_frame.pack()
        tk.Label(input_frame, text="Nombre Completo:", bg=COLOR_BG_CARD, font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", padx=10, pady=5)
        entry_nombre = tk.Entry(input_frame, width=35, font=FONT_BODY)
        entry_nombre.grid(row=0, column=1, pady=5)
        tk.Label(input_frame, text="Celular:", bg=COLOR_BG_CARD, font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        entry_cel = tk.Entry(input_frame, width=35, font=FONT_BODY)
        entry_cel.grid(row=1, column=1, pady=5)
        
        # --- VALIDACIÓN ESTRICTA ---
        def enviar():
            if not entry_nombre.get() or not entry_cel.get():
                messagebox.showerror("Faltan Datos", "🚫 ¡Alto ahí!\nDebes ingresar tu Nombre y Celular para continuar.")
            else:
                self.mostrar_agradecimiento(entry_nombre.get(), animal['nombre'])

        tk.Button(card_detail, text="Enviar Solicitud", bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON, bd=0, width=25, command=enviar).pack(pady=20)

    # --- PANTALLA: MENSAJE BONITO (ÉXITO ADOPCIÓN) ---
    def mostrar_agradecimiento(self, nombre_usuario, nombre_mascota):
        self.limpiar_frame()
        center_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        center_frame.pack(expand=True, fill="both")
        card = tk.Frame(center_frame, bg="white", padx=50, pady=50)
        card.place(relx=0.5, rely=0.5, anchor="center")
        icon_img = self.crear_icono_exito()
        lbl_icon = tk.Label(card, image=icon_img, bg="white")
        lbl_icon.image = icon_img
        lbl_icon.pack(pady=(0, 20))
        tk.Label(card, text="¡Solicitud Enviada!", font=("Helvetica", 28, "bold"), fg=COLOR_ACCENT, bg="white").pack(pady=10)
        tk.Label(card, text=f"Gracias, {nombre_usuario}.", font=("Helvetica", 18), fg=COLOR_TEXT, bg="white").pack()
        tk.Label(card, text=f"Te contactaremos pronto sobre {nombre_mascota}.", font=FONT_BODY, fg="gray", bg="white").pack(pady=5)
        tk.Button(card, text="Volver al Inicio", bg=COLOR_PRIMARY, fg="white", font=FONT_BUTTON, bd=0, command=self.mostrar_bienvenida).pack(pady=(40, 0))

    # --- PANTALLA 4: PERDIDOS ---
    def mostrar_perdidos(self):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="white", height=60, pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Volver", command=self.mostrar_bienvenida, bg="white", fg=COLOR_PRIMARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav_frame, text="Animales Perdidos y Encontrados", font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)
        tk.Button(nav_frame, text="📢 Reportar Encontrado", bg=COLOR_DANGER, fg="white", font=FONT_BUTTON, bd=0, cursor="hand2", padx=15, command=self.mostrar_formulario_reporte).pack(side="right", padx=30)

        content_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=30, pady=20)
        content_frame.pack(fill="both", expand=True)

        for animal in self.perdidos_data:
            row_border = tk.Frame(content_frame, bg="#E0E0E0", padx=1, pady=1)
            row_border.pack(fill="x", pady=8)
            row = tk.Frame(row_border, bg=COLOR_BG_CARD, padx=15, pady=15)
            row.pack(fill="both", expand=True)
            img_path = animal.get("img_path", None)
            color = animal.get("color", "gray")
            tk.Frame(row, width=5, bg=color).pack(side="left", fill="y")
            img = self.crear_imagen(color, size=(70, 70), path=img_path)
            lbl_img = tk.Label(row, image=img, bg=COLOR_BG_CARD)
            lbl_img.image = img
            lbl_img.pack(side="left", padx=15)
            text_frame = tk.Frame(row, bg=COLOR_BG_CARD)
            text_frame.pack(side="left", padx=10, fill="x", expand=True)
            tk.Label(text_frame, text=animal['nombre'], font=("Helvetica", 16, "bold"), bg=COLOR_BG_CARD, fg=COLOR_TEXT, anchor="w").pack(fill="x")
            details = tk.Frame(text_frame, bg=COLOR_BG_CARD)
            details.pack(anchor="w")
            tk.Label(details, text=f"📍 {animal['lugar']}   📅 {animal['fecha']}", font=FONT_BODY, fg=COLOR_TEXT_LIGHT, bg=COLOR_BG_CARD).pack(side="left")
            tk.Button(row, text="🗺️ Ver Ubicación", bg=COLOR_SECONDARY, fg="white", font=("Arial", 10, "bold"), bd=0, cursor="hand2", padx=10, pady=5, command=lambda a=animal: self.mostrar_mapa_detalle(a)).pack(side="right", padx=10)

    # --- PANTALLA 5: REPORTE ---
    def mostrar_formulario_reporte(self):
        self.limpiar_frame()
        self.temp_report_lat = None
        self.temp_report_lon = None
        self.temp_report_img_path = None

        nav_frame = tk.Frame(self.main_frame, bg="white", height=60, pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Cancelar", command=self.mostrar_perdidos, bg="white", fg=COLOR_TEXT_LIGHT, bd=0, font=("Arial", 11, "bold")).pack(side="left", padx=20)
        tk.Label(nav_frame, text="Reportar Mascota Encontrada", font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)

        main_content = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=40, pady=20)
        main_content.pack(fill="both", expand=True)
        left_col = tk.Frame(main_content, bg=COLOR_BG_MAIN)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        right_col = tk.Frame(main_content, bg=COLOR_BG_MAIN)
        right_col.pack(side="right", fill="both", expand=True)

        card_form = tk.Frame(left_col, bg=COLOR_BG_CARD, padx=20, pady=20)
        card_form.pack(fill="x")
        tk.Label(card_form, text="Datos del Animal", font=("Helvetica", 14, "bold"), bg=COLOR_BG_CARD, fg=COLOR_PRIMARY).pack(anchor="w", pady=(0,15))
        tk.Label(card_form, text="Descripción (ej. Perro marrón):", bg=COLOR_BG_CARD).pack(anchor="w")
        entry_desc = tk.Entry(card_form, width=30, font=FONT_BODY)
        entry_desc.pack(fill="x", pady=(5, 15), ipady=3)
        tk.Label(card_form, text="Tu Nombre:", bg=COLOR_BG_CARD).pack(anchor="w")
        entry_nombre_rep = tk.Entry(card_form, width=30, font=FONT_BODY)
        entry_nombre_rep.pack(fill="x", pady=(5, 10), ipady=3)
        tk.Label(card_form, text="Celular de Contacto:", bg=COLOR_BG_CARD).pack(anchor="w")
        entry_cel_rep = tk.Entry(card_form, width=30, font=FONT_BODY)
        entry_cel_rep.pack(fill="x", pady=(5, 10), ipady=3)

        card_media = tk.Frame(right_col, bg=COLOR_BG_CARD, padx=20, pady=20)
        card_media.pack(fill="both", expand=True)
        tk.Label(card_media, text="1. Sube una Foto", font=("Helvetica", 12, "bold"), bg=COLOR_BG_CARD).pack(anchor="w")
        lbl_foto_status = tk.Label(card_media, text="Sin foto seleccionada", bg=COLOR_BG_CARD, fg="gray")
        lbl_foto_status.pack(anchor="w")
        
        def seleccionar_foto():
            filepath = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
            if filepath:
                self.temp_report_img_path = filepath
                lbl_foto_status.config(text="Foto cargada ✅", fg=COLOR_ACCENT)

        tk.Button(card_media, text="📷 Subir Imagen", bg="#ECEFF1", fg=COLOR_TEXT, bd=0, command=seleccionar_foto).pack(anchor="w", pady=5)
        
        # --- MAPA CON CLIC IZQUIERDO NORMAL ---
        tk.Label(card_media, text="2. Ubicación (Haz clic en el mapa)", font=("Helvetica", 12, "bold"), bg=COLOR_BG_CARD).pack(anchor="w", pady=(20, 5))
        map_widget = tkintermapview.TkinterMapView(card_media, width=400, height=300, corner_radius=5)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_position(-12.046374, -77.042793) 
        map_widget.set_zoom(12)

        def marcar_ubicacion(coords):
            self.temp_report_lat = coords[0]
            self.temp_report_lon = coords[1]
            map_widget.delete_all_marker()
            map_widget.set_marker(coords[0], coords[1], text="Ubicación marcada")

        # --- AQUÍ ESTÁ EL CAMBIO A CLIC NORMAL ---
        map_widget.add_left_click_map_command(marcar_ubicacion)

        # --- VALIDACIÓN REPORTE ---
        def enviar_reporte():
            if not entry_desc.get() or not entry_nombre_rep.get() or not entry_cel_rep.get():
                messagebox.showerror("Faltan Datos", "🚫 Faltan datos obligatorios.")
                return
            if not self.temp_report_lat:
                messagebox.showwarning("Mapa", "🚫 Marca la ubicación en el mapa (clic normal).")
                return

            nuevo_animal = {
                "id": len(self.perdidos_data) + 1, "nombre": entry_desc.get(), 
                "lat": self.temp_report_lat, "lon": self.temp_report_lon,
                "lugar": "Ubicación Reportada", "fecha": "Hoy", "color": "#EF5350", 
                "img_path": self.temp_report_img_path
            }
            self.perdidos_data.append(nuevo_animal)
            self.mostrar_agradecimiento_reporte(entry_nombre_rep.get())

        tk.Button(main_content, text="Enviar Reporte", bg=COLOR_PRIMARY, fg="white", font=FONT_BUTTON, bd=0, width=30, pady=10, command=enviar_reporte).pack(side="bottom", pady=20)

    # --- PANTALLA: MENSAJE BONITO (ÉXITO REPORTE) ---
    def mostrar_agradecimiento_reporte(self, nombre):
        self.limpiar_frame()
        center_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        center_frame.pack(expand=True, fill="both")
        card = tk.Frame(center_frame, bg="white", padx=50, pady=50)
        card.place(relx=0.5, rely=0.5, anchor="center")
        icon_img = self.crear_icono_exito()
        lbl_icon = tk.Label(card, image=icon_img, bg="white")
        lbl_icon.image = icon_img
        lbl_icon.pack(pady=(0, 20))
        tk.Label(card, text="¡Reporte Publicado!", font=("Helvetica", 26, "bold"), fg=COLOR_PRIMARY, bg="white").pack(pady=10)
        tk.Label(card, text=f"Gracias {nombre}, tu ayuda es vital.", font=FONT_BODY, fg=COLOR_TEXT, bg="white").pack()
        tk.Button(card, text="Ver Lista", bg=COLOR_SECONDARY, fg="white", font=FONT_BUTTON, bd=0, command=self.mostrar_perdidos).pack(pady=(40, 0))

    def mostrar_mapa_detalle(self, animal_data):
        self.limpiar_frame()
        nav_frame = tk.Frame(self.main_frame, bg="white", pady=10)
        nav_frame.pack(fill="x")
        tk.Button(nav_frame, text="⬅ Volver a lista", command=self.mostrar_perdidos, bg="white", fg=COLOR_PRIMARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav_frame, text=f"Ubicación: {animal_data['lugar']}", font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)
        map_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=20, pady=20)
        map_frame.pack(fill="both", expand=True)
        map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=600, corner_radius=10)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_position(animal_data["lat"], animal_data["lon"])
        map_widget.set_zoom(16)
        map_widget.set_marker(animal_data["lat"], animal_data["lon"], text=f"¡{animal_data['nombre']} visto aquí!")

if __name__ == "__main__":
    app = PetApp()
    app.mainloop()
