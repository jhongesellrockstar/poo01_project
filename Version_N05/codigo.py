import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk, ImageDraw
import tkintermapview
import os
import shutil
from datetime import datetime
import random
import sqlite3

# --- COLORES Y ESTILO ---
COLOR_BG_MAIN = "#FDF6E4"        
COLOR_BG_CARD = "#FFFFFF"        
COLOR_PRIMARY = "#FFAB40"        
COLOR_SECONDARY = "#4FC3F7"    
COLOR_ACCENT = "#8BC34A"        
COLOR_TEXT = "#3E2723"            
COLOR_DANGER = "#EF5350"        
COLOR_ORANGE_FILTER = "#FF7043" 
COLOR_BLACK_LIST = "#263238"    
COLOR_WARNING = "#FFC107"        
COLOR_SUCCESS_BG = "#E8F5E9"    

FONT_TITLE = ("Helvetica", 24, "bold")
FONT_SUBTITLE = ("Helvetica", 16, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 10, "bold")

class PetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Patitas Seguras - Sistema Integral")
        self.state('zoomed')
        self.configure(bg=COLOR_BG_MAIN)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Configurar el manejo del cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- VARIABLES DE SESIÓN ---
        self.user_id = 0 
        self.user_name = "Invitado"
        
        # Filtros
        self.filtro_categoria = None
        self.filtro_edad = tk.StringVar(value="Todos")
        self.filtro_estado_perdidos = "Perdido" 
        
        # Variables Temporales
        self.ruta_imagen_temporal = None
        self.temp_lat = None
        self.temp_lon = None
        
        # Carpetas necesarias
        if not os.path.exists("assets/uploads"):
            try: os.makedirs("assets/uploads")
            except: pass

        # Inicializamos listas vacías
        self.db_mascotas_perdidas = []
        self.db_veterinarias = []
        self.db_blacklist_vet = []
        self.db_blacklist_maltrato = []
        self.db_votos = []
        self.db_adopcion = [] 

        # Archivo de base de datos SQLite
        self.db_path = os.path.join("assets", "data.db")
        try:
            self.init_db()
            self.load_db() # Carga los datos reales de la BD
        except Exception:
            pass 

        self.main_frame = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_bienvenida()

    # --- BASE DE DATOS ---
    def init_db(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS adopcion (
            id INTEGER PRIMARY KEY,
            Nombre TEXT, Tipo TEXT, Raza TEXT, Edad TEXT, Tiempo TEXT, ColorHex TEXT, 
            Descripcion TEXT, FotoPath TEXT, Energia INTEGER, Vacunas INTEGER
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS veterinarias (
            ID INTEGER PRIMARY KEY,
            Nombre TEXT, Direccion TEXT, Telefono TEXT, Descripcion TEXT, Servicios TEXT, FotoPath TEXT, Latitud REAL, Longitud REAL, PromedioEstrellas REAL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS blacklist_vet (
            id INTEGER PRIMARY KEY, NombreVeterinaria TEXT, Motivo TEXT, Latitud REAL, Longitud REAL, FechaReporte TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS blacklist_maltrato (
            id INTEGER PRIMARY KEY, Nombre TEXT, Descripcion TEXT, FotoPath TEXT, Latitud REAL, Longitud REAL, FechaReporte TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS mascotas_perdidas (
            id INTEGER PRIMARY KEY, Nombre TEXT, Tipo TEXT, Raza TEXT, Edad TEXT, Descripcion TEXT, Contacto TEXT, Latitud REAL, Longitud REAL, FotoPath TEXT, Estado TEXT, FechaPerdido TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY, VetID INTEGER, Estrellas INTEGER, Comentario TEXT
        )""")
        self.conn.commit()

    def load_db(self):
        c = self.conn.cursor()
        try:
            c.execute("SELECT * FROM adopcion")
            self.db_adopcion = [dict(row) for row in c.fetchall()]
            c.execute("SELECT * FROM veterinarias")
            self.db_veterinarias = [dict(row) for row in c.fetchall()]
            c.execute("SELECT * FROM blacklist_vet")
            self.db_blacklist_vet = [dict(row) for row in c.fetchall()]
            c.execute("SELECT * FROM blacklist_maltrato")
            self.db_blacklist_maltrato = [dict(row) for row in c.fetchall()]
            c.execute("SELECT * FROM mascotas_perdidas")
            self.db_mascotas_perdidas = [dict(row) for row in c.fetchall()]
            c.execute("SELECT * FROM votos")
            self.db_votos = [dict(row) for row in c.fetchall()]
        except Exception:
            pass

    def insert_adopcion(self, item):
        c = self.conn.cursor()
        c.execute("INSERT INTO adopcion (Nombre, Tipo, Raza, Edad, Tiempo, ColorHex, Descripcion, FotoPath, Energia, Vacunas) VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (item.get("Nombre"), item.get("Tipo"), item.get("Raza"), item.get("Edad"), item.get("Tiempo"), 
                   item.get("ColorHex"), item.get("Descripcion"), item.get("FotoPath"), item.get("Energia"), item.get("Vacunas")))
        self.conn.commit()

    def insert_veterinaria(self, vet):
        c = self.conn.cursor()
        c.execute("INSERT INTO veterinarias (Nombre, Direccion, Telefono, Descripcion, Servicios, FotoPath, Latitud, Longitud, PromedioEstrellas) VALUES (?,?,?,?,?,?,?,?,?)",
                  (vet.get("Nombre"), vet.get("Direccion"), vet.get("Telefono"), vet.get("Descripcion"), vet.get("Servicios"), vet.get("FotoPath"), vet.get("Latitud"), vet.get("Longitud"), vet.get("PromedioEstrellas")))
        vet["ID"] = c.lastrowid
        self.conn.commit()

    def insert_blacklist_vet(self, item):
        c = self.conn.cursor()
        c.execute("INSERT INTO blacklist_vet (NombreVeterinaria, Motivo, Latitud, Longitud, FechaReporte) VALUES (?,?,?,?,?)",
                  (item.get("NombreVeterinaria"), item.get("Motivo"), item.get("Latitud"), item.get("Longitud"), str(item.get("FechaReporte"))))
        self.conn.commit()

    def insert_blacklist_maltrato(self, item):
        c = self.conn.cursor()
        c.execute("INSERT INTO blacklist_maltrato (Nombre, Descripcion, FotoPath, Latitud, Longitud, FechaReporte) VALUES (?,?,?,?,?,?)",
                  (item.get("Nombre"), item.get("Descripcion"), item.get("FotoPath"), item.get("Latitud"), item.get("Longitud"), str(item.get("FechaReporte"))))
        self.conn.commit()

    def insert_mascota_perdida(self, item):
        c = self.conn.cursor()
        c.execute("INSERT INTO mascotas_perdidas (Nombre, Tipo, Raza, Edad, Descripcion, Contacto, Latitud, Longitud, FotoPath, Estado, FechaPerdido) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (item.get("Nombre"), item.get("Tipo"), item.get("Raza"), item.get("Edad"), item.get("Descripcion"), item.get("Contacto"), item.get("Latitud"), item.get("Longitud"), item.get("FotoPath"), item.get("Estado"), str(item.get("FechaPerdido"))))
        self.conn.commit()

    def insert_voto(self, voto):
        c = self.conn.cursor()
        c.execute("INSERT INTO votos (VetID, Estrellas, Comentario) VALUES (?,?,?)",
                  (voto.get("VetID"), voto.get("Estrellas"), voto.get("Comentario")))
        c.execute("SELECT AVG(Estrellas) as avg FROM votos WHERE VetID=?", (voto.get("VetID"),))
        r = c.fetchone()
        avg = r["avg"] if r and r["avg"] is not None else voto.get("Estrellas")
        c.execute("UPDATE veterinarias SET PromedioEstrellas=? WHERE ID=?", (avg, voto.get("VetID")))
        self.conn.commit()

    def cerrar_conexion(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.commit()
            self.conn.close()

    def eliminar_mascota_perdida(self, mascota_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM mascotas_perdidas WHERE id=?", (mascota_id,))
        self.conn.commit()
        self.db_mascotas_perdidas = [m for m in self.db_mascotas_perdidas if m.get('id') != mascota_id]

    # ==========================================
    # HERRAMIENTAS GRÁFICAS
    # ==========================================
    def crear_imagen(self, path, size=(100, 100), fallback_color="#CCCCCC"):
        ruta_real = None
        if path:
            if os.path.exists(path):
                ruta_real = path
            else:
                posibles = [
                    path,
                    os.path.join(os.getcwd(), path),
                    os.path.join("assets", path),
                    os.path.join("assets/uploads", path),
                    os.path.join("..", "assets", "uploads", os.path.basename(path))
                ]
                for p in posibles:
                    if p and os.path.exists(p):
                        ruta_real = p
                        break

        if ruta_real:
            try:
                img = Image.open(ruta_real).convert("RGBA")
                img.thumbnail(size, Image.Resampling.LANCZOS)
                bg = Image.new('RGBA', size, (0, 0, 0, 0))
                offset = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
                bg.paste(img, offset, img)
                return ImageTk.PhotoImage(bg)
            except Exception as e:
                pass

        img = Image.new('RGB', size, color=fallback_color)
        d = ImageDraw.Draw(img)
        d.rectangle([2,2, size[0]-2, size[1]-2], outline="white", width=2)
        return ImageTk.PhotoImage(img)

    def create_rounded_rect(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
            try: widget.unbind("<MouseWheel>")
            except: pass
            try: widget.unbind("<Button-4>")
            except: pass
            try: widget.unbind("<Button-5>")
            except: pass
            widget.destroy()

    def crear_nav(self, titulo, cmd_volver):
        nav = tk.Frame(self.main_frame, bg="white", height=60, pady=10)
        nav.pack(fill="x")
        tk.Button(nav, text="⬅ Volver", command=cmd_volver, bg="white", fg=COLOR_TEXT, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav, text=titulo, font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)
        return nav

    def crear_scroll_canvas(self, parent):
        canvas = tk.Canvas(parent, bg=COLOR_BG_MAIN, highlightthickness=0)
        scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=COLOR_BG_MAIN)
        window_id = canvas.create_window((0,0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        def ajustar_ancho(event): canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", ajustar_ancho)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        def _on_mousewheel(event):
            try: canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError: pass
        frame.bind("<MouseWheel>", _on_mousewheel)
        frame.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        frame.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        frame.bind("<Enter>", lambda e: canvas.focus_set())
        return frame

    # ==========================================
    # MENU PRINCIPAL
    # ==========================================
    def mostrar_bienvenida(self):
        self.limpiar_frame()
        header = tk.Frame(self.main_frame, bg=COLOR_PRIMARY, height=120)
        header.pack(fill="x")
        tk.Label(header, text="🐾 Patitas Seguras", font=("Comic Sans MS", 32, "bold"), 
                 bg=COLOR_PRIMARY, fg="white").place(relx=0.5, rely=0.35, anchor="center")
        tk.Label(header, text="Sistema Integral de Cuidado Animal", font=("Helvetica", 11), 
                 bg=COLOR_PRIMARY, fg="#FFF3E0").place(relx=0.5, rely=0.80, anchor="center")
        body = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        body.pack(expand=True, fill="both", padx=20, pady=10)
        f_logo_border = tk.Frame(body, bg="white", bd=0)
        f_logo_border.pack(pady=(5, 10))
        f_logo_inner = tk.Frame(f_logo_border, bg="white", bd=5, relief="flat") 
        f_logo_inner.pack(padx=5, pady=5)
        img = self.crear_imagen("imagenes/logo.png", size=(280, 280), fallback_color=COLOR_BG_MAIN)
        lbl_logo = tk.Label(f_logo_inner, image=img, bg="white")
        lbl_logo.image = img
        lbl_logo.pack()
        tk.Label(body, text="¡Hola! ¿Qué deseas hacer hoy?", font=("Helvetica", 18, "bold"), 
                 bg=COLOR_BG_MAIN, fg="#5D4037").pack(pady=(0, 15))
        grid_frame = tk.Frame(body, bg=COLOR_BG_MAIN)
        grid_frame.pack()
        self.crear_boton_tarjeta(grid_frame, "🐶 ADOPCIÓN", "Encuentra un amigo", "🐾", COLOR_ACCENT, self.mostrar_adopcion, 0, 0)
        self.crear_boton_tarjeta(grid_frame, "🔍 PERDIDOS", "Reportar o buscar", "📢", COLOR_SECONDARY, self.mostrar_perdidos, 0, 1)
        tk.Frame(grid_frame, height=5, bg=COLOR_BG_MAIN).grid(row=1, column=0)
        self.crear_boton_tarjeta(grid_frame, "😡 BLACKLIST MALTRATO", "Denunciar abuso", "🚫", COLOR_DANGER, self.mostrar_bl_abusers, 2, 0)
        self.crear_boton_tarjeta(grid_frame, "💀 BLACKLIST VET", "Malas prácticas", "⚠️", COLOR_BLACK_LIST, self.mostrar_bl_vets, 2, 1)
        tk.Frame(grid_frame, height=5, bg=COLOR_BG_MAIN).grid(row=3, column=0)
        self.crear_boton_tarjeta(grid_frame, "⭐ RANKING VETERINARIAS", "Las mejores valoradas", "🏆", COLOR_WARNING, self.mostrar_ranking, 4, 0, colspan=2, width=640)
        tk.Label(self.main_frame, text="© 2024 Patitas Seguras - Cuidando corazones", 
                 bg=COLOR_BG_MAIN, fg="#A1887F", font=("Arial", 8)).pack(side="bottom", pady=5)

    def crear_boton_tarjeta(self, parent, titulo, subtitulo, icono, color_borde, comando, r, c, colspan=1, width=300):
        card_border = tk.Frame(parent, bg=color_borde, padx=2, pady=2, cursor="hand2")
        card_border.grid(row=r, column=c, columnspan=colspan, padx=10, pady=0)
        card_inner = tk.Frame(card_border, bg="white", width=width, height=80, cursor="hand2")
        card_inner.pack_propagate(False) 
        card_inner.pack()
        lbl_icon = tk.Label(card_inner, text=icono, font=("Segoe UI Emoji", 28), bg="white", fg=color_borde, cursor="hand2")
        lbl_icon.pack(side="left", padx=(15, 10))
        text_frame = tk.Frame(card_inner, bg="white", cursor="hand2")
        text_frame.pack(side="left", fill="y", pady=12)
        lbl_title = tk.Label(text_frame, text=titulo, font=("Arial", 13, "bold"), bg="white", fg="#424242", cursor="hand2", anchor="w")
        lbl_title.pack(anchor="w")
        lbl_sub = tk.Label(text_frame, text=subtitulo, font=("Arial", 9), bg="white", fg="gray", cursor="hand2", anchor="w")
        lbl_sub.pack(anchor="w")
        def on_enter(e): card_border.config(bg="#333333"); card_inner.config(bg="#FAFAFA")
        def on_leave(e): card_border.config(bg=color_borde); card_inner.config(bg="white")
        for w in [card_border, card_inner, lbl_icon, text_frame, lbl_title, lbl_sub]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", lambda e: comando())

    # ==========================================
    # MODULO: ADOPCIÓN
    # ==========================================
    def mostrar_adopcion(self):
        self.limpiar_frame(); self.crear_nav("Adopta un amigo", self.mostrar_bienvenida)
        f_filtros = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, pady=10); f_filtros.pack(fill="x", padx=40)
        tk.Label(f_filtros, text="Categorías", font=("Arial", 14, "bold"), bg=COLOR_BG_MAIN, fg=COLOR_TEXT).pack(anchor="w")
        f_iconos = tk.Frame(f_filtros, bg=COLOR_BG_MAIN); f_iconos.pack(anchor="w", pady=(5, 10))
        self.filtros_data = [("Todos", None, "🐾"), ("Perros", "Perro", "🐶"), ("Gatos", "Gato", "🐱"), ("Aves", "Ave", "🐦"), ("Peces", "Pez", "🐠")]
        self.botones_filtro = []
        for txt, val, ico in self.filtros_data:
            f = tk.Frame(f_iconos, bg=COLOR_BG_MAIN, padx=10); f.pack(side="left")
            btn = tk.Button(f, text=ico, font=("Segoe UI Emoji", 20), bg="white", fg="#555", relief="flat", command=lambda v=val: self.seleccionar_categoria(v))
            btn.pack()
            lbl = tk.Label(f, text=txt, font=("Arial", 9), bg=COLOR_BG_MAIN, fg="#777"); lbl.pack(pady=2)
            self.botones_filtro.append({'btn': btn, 'lbl': lbl, 'val': val})
        btn_publicar = tk.Button(f_filtros, text=" 🐾 DAR EN ADOPCIÓN ", bg=COLOR_ACCENT, fg="white", 
                                 font=("Arial", 11, "bold"), padx=15, pady=8, bd=0, cursor="hand2", 
                                 command=self.form_adopcion)
        btn_publicar.place(relx=1.0, rely=0.3, anchor="e")
        self.f_edad = tk.Frame(f_filtros, bg=COLOR_BG_MAIN, pady=5)
        tk.Label(self.f_edad, text="Filtrar por Etapa:", font=("Arial", 11, "bold"), bg=COLOR_BG_MAIN, fg=COLOR_TEXT).pack(side="left", padx=(0, 10))
        self.filtro_edad.set("Todos")
        for op in ["Todos", "Cachorro", "Adulto", "Joven"]:
            tk.Radiobutton(self.f_edad, text=op, variable=self.filtro_edad, value=op, bg=COLOR_BG_MAIN, command=self.cargar_grid_adopcion).pack(side="left", padx=5)
        self.scroll_frame_adopcion = self.crear_scroll_canvas(self.main_frame)
        self.scroll_frame_adopcion.master.bind("<Configure>", lambda e: self.cargar_grid_adopcion())
        self.seleccionar_categoria(None)

    def seleccionar_categoria(self, valor):
        self.filtro_categoria = valor
        for item in self.botones_filtro:
            active = item['val'] == valor
            item['btn'].config(bg=COLOR_ORANGE_FILTER if active else "white", fg="white" if active else "#555")
            item['lbl'].config(fg=COLOR_ORANGE_FILTER if active else "#777", font=("Arial", 9, "bold" if active else "normal"))
        if valor in ["Perro", "Gato"]:
            self.f_edad.pack(anchor="w", pady=(0, 10))
        else:
            self.f_edad.pack_forget()
            self.filtro_edad.set("Todos")
        self.cargar_grid_adopcion()

    def cargar_grid_adopcion(self, event=None):
        for w in self.scroll_frame_adopcion.winfo_children(): w.destroy()
        ancho_disponible = self.main_frame.winfo_width()
        if ancho_disponible < 200: ancho_disponible = 1000 
        ancho_tarjeta = 290 
        columnas = max(1, ancho_disponible // ancho_tarjeta)
        grid_outer = tk.Frame(self.scroll_frame_adopcion, bg=COLOR_BG_MAIN)
        grid_outer.pack(fill="x", padx=20)
        grid_center = tk.Frame(grid_outer, bg=COLOR_BG_MAIN)
        grid_center.pack(anchor="center") 
        mascotas = []
        for m in self.db_adopcion:
            if self.filtro_categoria and self.filtro_categoria != m['Tipo']: continue
            edad_filtro = self.filtro_edad.get()
            if edad_filtro != "Todos" and m['Edad'] != edad_filtro: continue
            mascotas.append(m)
        if not mascotas:
            tk.Label(self.scroll_frame_adopcion, text="No se encontraron mascotas.", bg=COLOR_BG_MAIN, font=("Arial", 14), fg="gray").pack(pady=50)
            return
        r=0; c=0
        for m in mascotas:
            cw=250; ch=350
            cv = tk.Canvas(grid_center, width=cw, height=ch, bg=COLOR_BG_MAIN, highlightthickness=0)
            cv.grid(row=r, column=c, padx=20, pady=20)
            self.create_rounded_rect(cv, 2, 2, cw-2, ch-2, radius=20, fill="white", outline="#E0E0E0")
            cf = tk.Frame(cv, bg="white", width=cw-10, height=ch-10); cf.pack_propagate(False)
            cv.create_window(cw/2, ch/2, window=cf, anchor="center")
            f_img = tk.Frame(cf, bg="white", width=220, height=220); f_img.pack_propagate(False); f_img.pack(pady=(10, 0))
            img = self.crear_imagen(m.get('FotoPath', ''), size=(220, 220), fallback_color="#FFF3E0")
            lbl = tk.Label(f_img, image=img, bg="white"); lbl.image=img; lbl.pack(fill="both", expand=True)
            tk.Label(f_img, text=f" {m['Edad']} ", bg=COLOR_PRIMARY, fg="white", font=("Arial", 8, "bold")).place(x=5, y=5)
            tk.Label(cf, text=m['Nombre'], font=("Arial", 14, "bold"), fg="#333", bg="white").pack(pady=(10, 0))
            subtexto = m.get('Raza', 'Mestizo')
            if m.get('Tiempo'):
                subtexto += f" • {m['Tiempo']}"
            tk.Label(cf, text=subtexto, font=("Arial", 10), fg="#888", bg="white").pack(pady=(0, 10))
            tk.Button(cf, text="Ver Detalles", bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON, bd=0, cursor="hand2", pady=5, width=20,
                      command=lambda x=m: self.ver_detalle_mascota(x)).pack(side="bottom", pady=(0, 15))
            c+=1
            if c >= columnas: 
                c=0; r+=1

    def ver_detalle_mascota(self, mascota):
        self.limpiar_frame(); self.crear_nav(f"Conoce a {mascota['Nombre']}", self.mostrar_adopcion)
        scroll = self.crear_scroll_canvas(self.main_frame)
        container = tk.Frame(scroll, bg=COLOR_BG_MAIN)
        container.pack(fill="both", expand=True, pady=40)
        content_wrapper = tk.Frame(container, bg=COLOR_BG_MAIN)
        content_wrapper.pack(anchor="center") 
        card = tk.Frame(content_wrapper, bg="white", bd=0, padx=40, pady=40, width=800)
        card.pack(fill="x")
        f_img = tk.Frame(card, bg="white", width=350); f_img.pack(side="left", fill="y", padx=(0, 40))
        img = self.crear_imagen(mascota.get('FotoPath', ''), size=(350, 350), fallback_color="#FFF3E0")
        lbl = tk.Label(f_img, image=img, bg="white"); lbl.image=img; lbl.pack()
        info = tk.Frame(card, bg="white"); info.pack(side="left", fill="both", expand=True)
        head = tk.Frame(info, bg="white"); head.pack(fill="x", pady=(0, 20))
        tk.Label(head, text=mascota['Nombre'], font=("Helvetica", 32, "bold"), fg=COLOR_TEXT, bg="white").pack(side="left")
        lbl_h = tk.Label(head, text="♡", font=("Arial", 32), fg="gray", bg="white", cursor="hand2")
        lbl_h.pack(side="left", padx=20)
        def toggle(e):
            lbl_h.config(text="♥" if lbl_h.cget("text")=="♡" else "♡", fg=COLOR_DANGER if lbl_h.cget("text")=="♥" else "gray")
        lbl_h.bind("<Button-1>", toggle)
        tags = tk.Frame(info, bg="white"); tags.pack(fill="x", pady=10)
        datos_mostrar = [mascota.get('Raza'), mascota.get('Tipo'), mascota['Edad']]
        if mascota.get('Tiempo'): datos_mostrar.append(mascota.get('Tiempo'))
        for t in datos_mostrar:
            if t:
                tk.Label(tags, text=f"• {t}", font=("Arial", 11, "bold"), bg="#FFE0B2", fg=COLOR_ORANGE_FILTER, padx=10, pady=5).pack(side="left", padx=5)
        
        energ = mascota.get('Energia', 0)
        niveles_e = {1: "Baja", 2: "Media", 3: "Alta", 4: "Muy Alta"}
        txt_e = niveles_e.get(energ, "No especificada")
        if energ > 0: txt_e += " " + ("⚡" * energ)
        tk.Label(info, text=f"Energía: {txt_e}", font=("Arial", 11, "bold"), fg=COLOR_PRIMARY, bg="white").pack(anchor="w", pady=(20, 5))
        
        vac = mascota.get('Vacunas', 0)
        if vac == 1:
            tk.Label(info, text="✅ Vacunas al día", font=("Arial", 11), fg="green", bg="white").pack(anchor="w")
        else:
            tk.Label(info, text="⚠️ Vacunas pendientes o sin info", font=("Arial", 11), fg="#F57C00", bg="white").pack(anchor="w")

        tk.Label(info, text=mascota.get('Descripcion', ''), font=("Arial", 12), fg="#555", bg="white", wraplength=350, justify="left").pack(anchor="w", pady=20)
        self.btn_adoptar = tk.Button(info, text="¡Quiero Adoptar!", bg=COLOR_ACCENT, fg="white", font=("Arial", 14, "bold"), bd=0, padx=30, pady=15, cursor="hand2", command=lambda: self.mostrar_form_inline(content_wrapper, mascota))
        self.btn_adoptar.pack(anchor="w", pady=30)

    def mostrar_form_inline(self, parent, mascota):
        self.btn_adoptar.config(state="disabled", bg="#CCCCCC")
        tk.Frame(parent, height=2, bg="#E0E0E0").pack(fill="x", pady=30)
        cont = tk.Frame(parent, bg="white", padx=40, pady=40, width=800)
        cont.pack(fill="x", pady=(0, 50))
        tk.Label(cont, text="📝 Solicitud de Adopción", font=("Helvetica", 22, "bold"), fg=COLOR_PRIMARY, bg="white").pack(pady=(0, 10))
        tk.Label(cont, text=f"Completa tus datos para adoptar a {mascota['Nombre']}:", font=("Arial", 12), fg="gray", bg="white").pack(pady=(0, 30))
        f = tk.Frame(cont, bg="white"); f.pack()
        tk.Label(f, text="Nombre Completo:", bg="white", font=("Arial", 11, "bold")).pack(anchor="w", fill="x")
        e_n = tk.Entry(f, bg="#F0F0F0", font=("Arial", 12), width=40); e_n.pack(pady=(5, 20))
        tk.Label(f, text="Teléfono:", bg="white", font=("Arial", 11, "bold")).pack(anchor="w", fill="x")
        e_t = tk.Entry(f, bg="#F0F0F0", font=("Arial", 12), width=40); e_t.pack(pady=(5, 30))
        def enviar():
            if not e_n.get() or not e_t.get(): messagebox.showwarning("!", "Faltan datos"); return
            self.mostrar_exito(mascota, e_n.get())
        tk.Button(f, text="ENVIAR SOLICITUD ➤", bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON, width=25, pady=12, command=enviar).pack()
        parent.update_idletasks()

    def mostrar_exito(self, mascota, usuario):
        self.limpiar_frame()
        main = tk.Frame(self.main_frame, bg=COLOR_SUCCESS_BG); main.pack(fill="both", expand=True)
        cv = tk.Canvas(main, bg=COLOR_SUCCESS_BG, highlightthickness=0); cv.place(relx=0, rely=0, relwidth=1, relheight=1)
        colors = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, "#FFEB3B"]
        for _ in range(80):
            x, y, s, c = random.randint(0, 1280), random.randint(0, 850), random.randint(5, 15), random.choice(colors)
            cv.create_oval(x, y, x+s, y+s, fill=c, outline="")
        cont = tk.Frame(main, bg="white", padx=60, pady=60); cont.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(cont, text="🎉", font=("Arial", 80), bg="white").pack()
        tk.Label(cont, text="¡MUCHAS GRACIAS!", font=("Helvetica", 36, "bold"), fg=COLOR_ACCENT, bg="white").pack(pady=(10, 20))
        tk.Label(cont, text=f"Hola {usuario},\nHemos recibido tu solicitud para {mascota['Nombre']}.\nTe contactaremos pronto.", font=("Arial", 14), fg="#555", bg="white", justify="center").pack(pady=20)
        tk.Button(cont, text="VOLVER AL INICIO", bg=COLOR_PRIMARY, fg="white", font=("Arial", 14, "bold"), padx=40, pady=15, bd=0, cursor="hand2", command=self.mostrar_bienvenida).pack(pady=30)

    def mostrar_exito_publicacion(self):
        self.limpiar_frame()
        main = tk.Frame(self.main_frame, bg=COLOR_SUCCESS_BG); main.pack(fill="both", expand=True)
        cv = tk.Canvas(main, bg=COLOR_SUCCESS_BG, highlightthickness=0); cv.place(relx=0, rely=0, relwidth=1, relheight=1)
        colors = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, "#FFEB3B"]
        for _ in range(80):
            x, y, s, c = random.randint(0, 1280), random.randint(0, 850), random.randint(5, 15), random.choice(colors)
            cv.create_oval(x, y, x+s, y+s, fill=c, outline="")
        cont = tk.Frame(main, bg="white", padx=60, pady=60); cont.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(cont, text="🐾", font=("Arial", 80), bg="white").pack()
        tk.Label(cont, text="¡GRACIAS POR CONFIAR!", font=("Helvetica", 30, "bold"), fg=COLOR_PRIMARY, bg="white").pack(pady=(10, 20))
        tk.Label(cont, text="Tu mascota ha sido publicada exitosamente.\nEsperamos encontrarle un hogar lleno de amor muy pronto.", font=("Arial", 14), fg="#555", bg="white", justify="center").pack(pady=20)
        tk.Button(cont, text="VOLVER AL LISTADO", bg=COLOR_ACCENT, fg="white", font=("Arial", 14, "bold"), padx=40, pady=15, bd=0, cursor="hand2", command=self.mostrar_adopcion).pack(pady=30)

    def form_adopcion(self):
        self.limpiar_frame()
        self.crear_nav("Volver al listado", self.mostrar_adopcion)
        scroll_frame = self.crear_scroll_canvas(self.main_frame)
        container = tk.Frame(scroll_frame, bg=COLOR_BG_MAIN)
        container.pack(fill="both", expand=True, pady=20)
        form_card = tk.Frame(container, bg="white", padx=40, pady=40, width=600)
        form_card.pack(anchor="center")
        tk.Label(form_card, text="Publicar Nueva Mascota", font=("Helvetica", 20, "bold"), fg=COLOR_PRIMARY, bg="white").pack(pady=(0, 20))
        tk.Label(form_card, text="Completa la información para encontrarle un hogar.", font=("Arial", 11), fg="gray", bg="white").pack(pady=(0, 30))
        
        entries = {}
        def crear_campo(label, key):
            tk.Label(form_card, text=label, font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 2))
            e = tk.Entry(form_card, bg="#F0F0F0", font=("Arial", 11), width=45) 
            e.pack(fill="x", pady=(0, 5))
            entries[key] = e
            
        crear_campo("Nombre de la Mascota:", "Nombre")
        crear_campo("Edad Real (Ej: 3 meses, 2 años):", "Tiempo")
        tk.Label(form_card, text="Etapa de Vida (Para filtros):", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 2))
        cb_edad = ttk.Combobox(form_card, values=["Cachorro", "Adulto", "Joven"], state="readonly", width=43)
        cb_edad.pack(fill="x", pady=(0, 5))
        entries["Edad"] = cb_edad 
        tk.Label(form_card, text="Tipo:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 2))
        cb_tipo = ttk.Combobox(form_card, values=["Perro", "Gato", "Ave", "Pez"], state="readonly", width=43)
        cb_tipo.pack(fill="x")
        
        tk.Label(form_card, text="Nivel de Energía:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 2))
        f_energy = tk.Frame(form_card, bg="white"); f_energy.pack(anchor="w")
        self.var_energy = tk.IntVar(value=0)
        lbl_energy_txt = tk.Label(f_energy, text="(Selecciona)", bg="white", fg="gray")
        btns_energy = []
        niveles = {1: "Baja", 2: "Media", 3: "Alta", 4: "Muy Alta"}
        def set_energy(n):
            self.var_energy.set(n)
            lbl_energy_txt.config(text=niveles[n], fg=COLOR_PRIMARY)
            for i, btn in enumerate(btns_energy):
                if i < n: btn.config(fg=COLOR_PRIMARY)
                else: btn.config(fg="#DDD")
        for i in range(1, 5):
            btn = tk.Button(f_energy, text="⚡", font=("Segoe UI Emoji", 20), bd=0, bg="white", activebackground="white", cursor="hand2", command=lambda x=i: set_energy(x), fg="#DDD")
            btn.pack(side="left")
            btns_energy.append(btn)
        lbl_energy_txt.pack(side="left", padx=10)
        
        tk.Label(form_card, text="Estado de Salud:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 2))
        self.var_vacunas = tk.IntVar(value=0)
        cb_vac = tk.Checkbutton(form_card, text="¿Tiene sus vacunas al día?", variable=self.var_vacunas, bg="white", font=("Arial", 11), activebackground="white", cursor="hand2")
        cb_vac.pack(anchor="w")

        crear_campo("Raza / Mezcla:", "Raza")
        crear_campo("Color:", "ColorHex")
        crear_campo("Pequeña Descripción:", "Descripcion")
        tk.Label(form_card, text="Foto:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(15, 5))
        f_foto = tk.Frame(form_card, bg="white"); f_foto.pack(fill="x")
        lbl_archivo = tk.Label(f_foto, text="Ningún archivo seleccionado", bg="white", fg="gray", font=("Arial", 9, "italic"))
        self.ruta_imagen_temporal = ""
        def subir():
            f = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
            if f:
                self.ruta_imagen_temporal = f
                lbl_archivo.config(text=f"✅ {os.path.basename(f)}", fg=COLOR_ACCENT)
        tk.Button(f_foto, text="📷 Seleccionar Imagen", bg="#E0E0E0", bd=0, padx=15, pady=5, cursor="hand2", command=subir).pack(side="left")
        lbl_archivo.pack(side="left", padx=15)
        
        def publicar():
            if not entries["Nombre"].get() or not cb_tipo.get() or not entries["Edad"].get() or not self.ruta_imagen_temporal:
                messagebox.showwarning("Faltan datos", "Completa nombre, tipo, etapa de vida y foto.")
                return
            if self.var_energy.get() == 0:
                messagebox.showwarning("Faltan datos", "Por favor selecciona el nivel de energía.")
                return
            
            try:
                nombre_foto = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.path.basename(self.ruta_imagen_temporal)}"
                dest = os.path.join("assets/uploads", nombre_foto)
                shutil.copy(self.ruta_imagen_temporal, dest)
                nueva_mascota = {
                    "Nombre": entries["Nombre"].get(),
                    "Tipo": cb_tipo.get(),
                    "Raza": entries["Raza"].get(),
                    "Edad": entries["Edad"].get(),    
                    "Tiempo": entries["Tiempo"].get(), 
                    "Energia": self.var_energy.get(), 
                    "Vacunas": self.var_vacunas.get(),
                    "ColorHex": entries["ColorHex"].get(),
                    "Descripcion": entries["Descripcion"].get(),
                    "FotoPath": dest
                }
                self.db_adopcion.append(nueva_mascota)
                self.insert_adopcion(nueva_mascota)
                self.mostrar_exito_publicacion()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        tk.Frame(form_card, height=20, bg="white").pack()
        tk.Button(form_card, text="PUBLICAR AHORA", bg=COLOR_ACCENT, fg="white", font=("Arial", 12, "bold"), pady=12, width=30, bd=0, cursor="hand2", command=publicar).pack(pady=(0, 20))

    # ==========================================
    # MODULO: RANKING VETERINARIAS
    # ==========================================
    def mostrar_ranking(self):
        self.limpiar_frame()
        nav = self.crear_nav(f"Ranking Veterinarias", self.cerrar_sesion_y_volver)
        tk.Button(nav, text="➕ AGREGAR VETERINARIA", bg=COLOR_ACCENT, fg="white", font=("Arial", 10, "bold"), command=self.form_ranking_vet).pack(side="right", padx=20)
        content = self.crear_scroll_canvas(self.main_frame)
        data = sorted(self.db_veterinarias, key=lambda x: x.get('PromedioEstrellas', 0), reverse=True)
        if not data: tk.Label(content, text="No hay veterinarias registradas aún.", bg=COLOR_BG_MAIN, font=("Arial", 14), fg="gray").pack(pady=50)
        for vet in data:
            card = tk.Frame(content, bg="white", bd=1, relief="solid", padx=15, pady=15); card.pack(fill="x", padx=50, pady=10)
            head = tk.Frame(card, bg="white"); head.pack(fill="x")
            tk.Label(head, text=vet['Nombre'], font=("Arial", 18, "bold"), fg=COLOR_TEXT, bg="white").pack(side="left")
            tk.Label(head, text=f"⭐ {vet.get('PromedioEstrellas') or 0:.1f}", font=("Segoe UI Emoji", 16, "bold"), bg="white", fg=COLOR_WARNING).pack(side="right")
            tk.Label(card, text=f"📍 {vet['Direccion']}", bg="white", fg="gray", font=("Arial", 10)).pack(anchor="w", pady=(5, 10))
            action_frame = tk.Frame(card, bg="white"); action_frame.pack(fill="x", pady=5)
            tk.Button(action_frame, text="👁️ VER PERFIL", bg="#E3F2FD", fg=COLOR_SECONDARY, bd=0, font=("Arial", 9, "bold"), cursor="hand2", padx=10, pady=5, command=lambda v=vet: self.ver_perfil_veterinaria(v)).pack(side="right", padx=5)
            tk.Button(action_frame, text="✍ CALIFICAR", bg="#FFF3E0", fg=COLOR_PRIMARY, bd=0, font=("Arial", 9, "bold"), cursor="hand2", padx=10, pady=5, command=lambda v=vet: self.votar_vet(v)).pack(side="right", padx=5)

    def ver_perfil_veterinaria(self, vet):
        self.limpiar_frame(); self.crear_nav(f"Perfil: {vet['Nombre']}", self.mostrar_ranking)
        scroll = self.crear_scroll_canvas(self.main_frame)
        container = tk.Frame(scroll, bg=COLOR_BG_MAIN); container.pack(fill="both", expand=True, pady=20)
        card = tk.Frame(container, bg="white", padx=30, pady=30, bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=40)
        header = tk.Frame(card, bg="white"); header.pack(fill="x", pady=(0, 20))
        tk.Label(header, text=vet['Nombre'], font=("Helvetica", 28, "bold"), fg=COLOR_PRIMARY, bg="white").pack(side="left")
        tk.Label(header, text=f"⭐ {vet.get('PromedioEstrellas') or 0:.1f} / 5.0", font=("Arial", 20, "bold"), fg=COLOR_WARNING, bg="white").pack(side="right")
        body = tk.Frame(card, bg="white"); body.pack(fill="both", expand=True)
        col_izq = tk.Frame(body, bg="white", width=400); col_izq.pack(side="left", fill="y", padx=(0, 20))
        img = self.crear_imagen(vet.get('FotoPath'), size=(380, 250), fallback_color="#EEEEEE")
        lbl_img = tk.Label(col_izq, image=img, bg="white"); lbl_img.image = img; lbl_img.pack(pady=(0, 20))
        tk.Label(col_izq, text="📍 Dirección:", font=("Arial", 11, "bold"), bg="white", fg=COLOR_TEXT).pack(anchor="w")
        tk.Label(col_izq, text=vet['Direccion'], font=("Arial", 11), bg="white", fg="gray", wraplength=380, justify="left").pack(anchor="w", pady=(0, 10))
        tk.Label(col_izq, text="📞 Teléfono:", font=("Arial", 11, "bold"), bg="white", fg=COLOR_TEXT).pack(anchor="w")
        tk.Label(col_izq, text=vet['Telefono'], font=("Arial", 11), bg="white", fg="gray").pack(anchor="w", pady=(0, 10))
        tk.Label(col_izq, text="🛠️ Servicios:", font=("Arial", 11, "bold"), bg="white", fg=COLOR_TEXT).pack(anchor="w")
        tk.Label(col_izq, text=vet.get('Servicios', 'No especificado'), font=("Arial", 11), bg="white", fg="gray", wraplength=380, justify="left").pack(anchor="w", pady=(0, 10))
        tk.Label(col_izq, text="📝 Descripción:", font=("Arial", 11, "bold"), bg="white", fg=COLOR_TEXT).pack(anchor="w")
        tk.Label(col_izq, text=vet.get('Descripcion', ''), font=("Arial", 11), bg="white", fg="gray", wraplength=380, justify="left").pack(anchor="w", pady=(0, 20))
        tk.Button(col_izq, text="✍ CALIFICAR ESTA VETERINARIA", bg=COLOR_ACCENT, fg="white", font=("Arial", 12, "bold"), pady=10, width=30, cursor="hand2", command=lambda: self.votar_vet(vet)).pack(side="bottom", pady=20)
        col_der = tk.Frame(body, bg="white"); col_der.pack(side="right", fill="both", expand=True)
        tk.Label(col_der, text="Ubicación en el Mapa", font=("Arial", 12, "bold"), bg="white", fg=COLOR_SECONDARY).pack(anchor="w", pady=(0, 10))
        map_widget = tkintermapview.TkinterMapView(col_der, corner_radius=10)
        map_widget.pack(fill="both", expand=True)
        lat = vet.get('Latitud'); lon = vet.get('Longitud')
        if lat and lon:
            map_widget.set_position(float(lat), float(lon)); map_widget.set_zoom(15); map_widget.set_marker(float(lat), float(lon), text=vet['Nombre'])
        else:
            map_widget.set_position(-12.046, -77.042); tk.Label(col_der, text="Ubicación no registrada", bg="white", fg="red").place(x=10, y=10)

    def form_ranking_vet(self):
        self.limpiar_frame(); self.crear_nav("Registrar Nueva Veterinaria", self.mostrar_ranking)
        scroll = self.crear_scroll_canvas(self.main_frame); container = tk.Frame(scroll, bg=COLOR_BG_MAIN); container.pack(fill="both", expand=True, pady=20)
        card = tk.Frame(container, bg="white", padx=40, pady=40, width=900); card.pack(anchor="center")
        tk.Label(card, text="Agregar Veterinaria a la Comunidad", font=("Helvetica", 20, "bold"), fg=COLOR_ACCENT, bg="white").pack(pady=(0, 20))
        f_cols = tk.Frame(card, bg="white"); f_cols.pack(fill="both", expand=True)
        col_izq = tk.Frame(f_cols, bg="white", width=400); col_izq.pack(side="left", fill="y", padx=(0, 20))
        col_der = tk.Frame(f_cols, bg="white", width=400); col_der.pack(side="left", fill="both", expand=True)
        def entry(lbl, w=40):
            tk.Label(col_izq, text=lbl, bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
            e = tk.Entry(col_izq, bg="#F0F0F0", font=("Arial", 11), width=w); e.pack(anchor="w", pady=(0, 10))
            return e
        e_n = entry("Nombre de la Veterinaria:"); e_d = entry("Dirección:"); e_t = entry("Teléfono:")
        tk.Label(col_izq, text="Descripción:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        t_desc = tk.Text(col_izq, height=3, bg="#F0F0F0", font=("Arial", 11), width=40); t_desc.pack(anchor="w", pady=(0, 10))
        tk.Label(col_izq, text="Servicios (ej: Rayos X, Baño, 24h):", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        e_s = tk.Entry(col_izq, bg="#F0F0F0", font=("Arial", 11), width=40); e_s.pack(anchor="w", pady=(0, 10))
        tk.Label(col_izq, text="Foto de la Fachada:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        self.ruta_imagen_temporal = None
        lbl_f = tk.Label(col_izq, text="Sin foto", bg="white", fg="gray")
        def subir():
            f = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png")])
            if f: self.ruta_imagen_temporal = f; lbl_f.config(text=os.path.basename(f), fg=COLOR_ACCENT)
        tk.Button(col_izq, text="📷 Seleccionar Foto", command=subir, bg="#EEE", bd=0).pack(anchor="w"); lbl_f.pack(anchor="w", pady=(0, 10))
        tk.Label(col_der, text="📍 Marca la ubicación exacta:", bg="white", font=("Arial", 10, "bold"), fg=COLOR_ACCENT).pack(anchor="w")
        self.temp_lat = -12.046; self.temp_lon = -77.042
        mv = tkintermapview.TkinterMapView(col_der, width=400, height=300, corner_radius=10); mv.pack(fill="both", expand=True)
        mv.set_position(self.temp_lat, self.temp_lon); mv.set_zoom(12)
        def on_click(coords): self.temp_lat, self.temp_lon = coords; mv.delete_all_marker(); mv.set_marker(coords[0], coords[1], text="Aquí")
        mv.add_left_click_map_command(on_click)
        def guardar():
            if not e_n.get(): messagebox.showwarning("!", "El nombre es obligatorio"); return
            dest = ""
            if self.ruta_imagen_temporal:
                nom = f"VET_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.path.basename(self.ruta_imagen_temporal)}"
                dest = os.path.join("assets/uploads", nom)
                shutil.copy(self.ruta_imagen_temporal, dest)
            self.db_veterinarias.append({
                "ID": len(self.db_veterinarias) + 1, "Nombre": e_n.get(), "Direccion": e_d.get(), "Telefono": e_t.get(),
                "Descripcion": t_desc.get("1.0", "end-1c"), "Servicios": e_s.get(), "FotoPath": dest,
                "Latitud": self.temp_lat, "Longitud": self.temp_lon, "PromedioEstrellas": 0.0 
            })
            try:
                self.insert_veterinaria(self.db_veterinarias[-1])
            except Exception:
                pass
            messagebox.showinfo("Éxito", "Veterinaria agregada a la comunidad."); self.mostrar_ranking()
        tk.Frame(card, height=20, bg="white").pack()
        tk.Button(card, text="PUBLICAR VETERINARIA", bg=COLOR_ACCENT, fg="white", font=("Arial", 12, "bold"), width=30, pady=10, command=guardar).pack(pady=20)

    def votar_vet(self, vet):
        top = tk.Toplevel(self); top.title(f"Calificar a {vet['Nombre']}"); top.geometry("400x350")
        tk.Label(top, text="Tu Calificación:", font=("Arial", 14, "bold")).pack(pady=10)
        stars_frame = tk.Frame(top); stars_frame.pack()
        rating_var = tk.IntVar(value=0); self.star_buttons = []
        def update_stars(rating):
            rating_var.set(rating)
            for i, btn in enumerate(self.star_buttons):
                if i < rating: btn.config(text="★", fg=COLOR_WARNING) 
                else: btn.config(text="☆", fg="gray")
        for i in range(1, 6):
            btn = tk.Button(stars_frame, text="☆", font=("Arial", 30), bd=0, activebackground=top.cget("bg"), cursor="hand2", command=lambda r=i: update_stars(r))
            btn.pack(side="left"); self.star_buttons.append(btn)
        tk.Label(top, text="Comentario:").pack(pady=5); txt = tk.Text(top, height=4, width=30); txt.pack()
        def enviar():
            if rating_var.get() == 0: messagebox.showwarning("!", "Selecciona una calificación"); return
            vet['PromedioEstrellas'] = rating_var.get() 
            voto = {"VetID": vet['ID'], "Estrellas": rating_var.get(), "Comentario": txt.get("1.0", "end-1c")} 
            self.db_votos.append(voto)
            try:
                self.insert_voto(voto)
                # actualizar promedio en memoria
                c = self.conn.cursor(); c.execute("SELECT PromedioEstrellas as p FROM veterinarias WHERE ID=?", (vet['ID'],)); r=c.fetchone(); vet['PromedioEstrellas'] = r['p'] if r and r['p'] is not None else vet['PromedioEstrellas']
            except Exception:
                pass
            messagebox.showinfo("Gracias", "Voto registrado"); top.destroy(); self.mostrar_ranking()
        tk.Button(top, text="ENVIAR VOTO", command=enviar, bg=COLOR_PRIMARY, fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=20)

    def cerrar_sesion_y_volver(self):
        self.user_id = 0; self.user_name = "Invitado"
        self.mostrar_bienvenida()

    # ==========================================
    # MODULO: LISTA NEGRA VETERINARIAS
    # ==========================================
    def mostrar_bl_vets(self):
        self.limpiar_frame(); nav = self.crear_nav("Lista Negra: Veterinarias", self.mostrar_bienvenida)
        tk.Button(nav, text="📢 REPORTAR MALA VETERINARIA", bg=COLOR_DANGER, fg="white", font=("Arial", 10, "bold"), padx=15, bd=0, cursor="hand2", command=self.form_bl_vet).pack(side="right", padx=20)
        content = self.crear_scroll_canvas(self.main_frame); data = self.db_blacklist_vet 
        if not data: tk.Label(content, text="No hay reportes.", bg=COLOR_BG_MAIN, font=("Arial", 14), fg="gray").pack(pady=50)
        for item in data:
            card = tk.Frame(content, bg="white", bd=1, relief="solid", padx=20, pady=20); card.pack(fill="x", padx=50, pady=10)
            tk.Label(card, text=item['NombreVeterinaria'], font=("Arial", 18, "bold"), fg=COLOR_DANGER, bg="white").pack(anchor="w")
            tk.Label(card, text=f"Motivo: {item['Motivo']}", font=("Arial", 12), fg="#555", bg="white").pack(anchor="w", pady=(5, 10))
            if item.get('Latitud'): tk.Button(card, text="📍 VER UBICACIÓN", bg="#EEEEEE", fg="black", font=("Arial", 9, "bold"), bd=0, padx=10, pady=5, cursor="hand2", command=lambda i=item: self.ver_mapa_vet(i)).pack(anchor="e")
            else: tk.Label(card, text="Sin ubicación", bg="white", fg="gray").pack(anchor="e")

    def form_bl_vet(self):
        self.limpiar_frame(); self.crear_nav("Reportar Veterinaria", self.mostrar_bl_vets)
        scroll = self.crear_scroll_canvas(self.main_frame); container = tk.Frame(scroll, bg=COLOR_BG_MAIN); container.pack(fill="both", expand=True, pady=20)
        card = tk.Frame(container, bg="white", padx=40, pady=40, width=800); card.pack(anchor="center")
        tk.Label(card, text="⚠️ Denunciar Veterinaria", font=("Helvetica", 20, "bold"), fg=COLOR_DANGER, bg="white").pack(pady=(0, 20))
        tk.Label(card, text="Nombre:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w"); e_n = tk.Entry(card, bg="#FFEBEE", font=("Arial", 12), width=50); e_n.pack(fill="x", pady=5)
        tk.Label(card, text="Motivo:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 0)); t_m = tk.Text(card, height=4, bg="#FAFAFA", font=("Arial", 11)); t_m.pack(fill="x", pady=5)
        tk.Label(card, text="📍 Ubicación:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        mv = tkintermapview.TkinterMapView(card, width=600, height=300, corner_radius=10); mv.pack(fill="both", expand=True); mv.set_position(-12.046, -77.042); mv.set_zoom(12)
        self.temp_vet_lat = None; self.temp_vet_lon = None
        def on_click(coords): self.temp_vet_lat, self.temp_vet_lon = coords; mv.delete_all_marker(); mv.set_marker(coords[0], coords[1], text="Aquí")
        mv.add_left_click_map_command(on_click)
        def guardar():
            if not e_n.get() or not t_m.get("1.0", "end-1c") or not self.temp_vet_lat: messagebox.showwarning("!", "Completa nombre, motivo y mapa."); return
            self.db_blacklist_vet.append({
                "NombreVeterinaria": e_n.get(), "Motivo": t_m.get("1.0", "end-1c"),
                "Latitud": self.temp_vet_lat, "Longitud": self.temp_vet_lon, "FechaReporte": datetime.now()
            })
            try:
                self.insert_blacklist_vet(self.db_blacklist_vet[-1])
            except Exception:
                pass
            messagebox.showinfo("Listo", "Denuncia registrada."); self.mostrar_bl_vets()
        tk.Button(card, text="REGISTRAR DENUNCIA", bg=COLOR_DANGER, fg="white", font=("Arial", 12, "bold"), pady=10, width=30, command=guardar).pack(pady=20)

    def ver_mapa_vet(self, item):
        self.limpiar_frame(); nav = self.crear_nav("Ubicación de Veterinaria", self.mostrar_bl_vets)
        map_frame = tk.Frame(self.main_frame, bg="white"); map_frame.pack(fill="both", expand=True)
        panel = tk.Frame(map_frame, bg="white", width=300, padx=20, pady=20); panel.pack(side="left", fill="y")
        tk.Label(panel, text=item['NombreVeterinaria'], font=("Helvetica", 20, "bold"), fg=COLOR_DANGER, bg="white", wraplength=280).pack(pady=(20, 10))
        tk.Label(panel, text="MOTIVO:", font=("Arial", 10, "bold"), fg="gray", bg="white").pack(anchor="w")
        tk.Label(panel, text=item['Motivo'], font=("Arial", 11), bg="white", wraplength=280, justify="left").pack(anchor="w", pady=5)
        mv = tkintermapview.TkinterMapView(map_frame, width=800, height=600); mv.pack(side="right", fill="both", expand=True)
        mv.set_position(float(item['Latitud']), float(item['Longitud'])); mv.set_zoom(16); mv.set_marker(float(item['Latitud']), float(item['Longitud']), text=item['NombreVeterinaria'])

    # ==========================================
    # MODULO: ANIMALES PERDIDOS
    # ==========================================
    def mostrar_perdidos(self):
        self.limpiar_frame()
        nav = tk.Frame(self.main_frame, bg="white", height=60, pady=10); nav.pack(fill="x")
        tk.Button(nav, text="⬅ Volver", command=self.mostrar_bienvenida, bg="white", fg=COLOR_SECONDARY, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav, text="Mascotas Perdidas y Encontradas", font=FONT_SUBTITLE, bg="white", fg=COLOR_SECONDARY).pack(side="left", padx=10)
        es_modo_perdido = (self.filtro_estado_perdidos == "Perdido")
        btn_txt = "📢 REPORTAR PERDIDO" if es_modo_perdido else "🕵️ ENCONTRÉ UNO"
        btn_bg = COLOR_SECONDARY if es_modo_perdido else COLOR_ACCENT
        estado_actual = self.filtro_estado_perdidos 
        tk.Button(nav, text=btn_txt, bg=btn_bg, fg="white", font=("Arial", 10, "bold"), padx=15, cursor="hand2", command=lambda: self.form_reporte_mascota(estado_actual)).pack(side="right", padx=20)
        bar = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, pady=10); bar.pack(fill="x", padx=100)
        def set_f(e): self.filtro_estado_perdidos = e; self.mostrar_perdidos()
        c_p = COLOR_DANGER if self.filtro_estado_perdidos == "Perdido" else "#E0E0E0"
        c_e = COLOR_ACCENT if self.filtro_estado_perdidos == "Encontrado" else "#E0E0E0"
        tk.Button(bar, text="🚨 PERDIDOS", bg=c_p, fg="white" if c_p != "#E0E0E0" else "#555", font=("Arial", 10, "bold"), padx=20, bd=0, command=lambda: set_f("Perdido")).pack(side="left", padx=5)
        tk.Button(bar, text="🏠 ENCONTRADOS", bg=c_e, fg="white" if c_e != "#E0E0E0" else "#555", font=("Arial", 10, "bold"), padx=20, bd=0, command=lambda: set_f("Encontrado")).pack(side="left", padx=5)
        self.container_perdidos = self.crear_scroll_canvas(self.main_frame); self.cargar_lista_perdidos()

    def form_reporte_mascota(self, tipo):
        self.limpiar_frame(); self.crear_nav("Volver", self.mostrar_perdidos)
        scroll = self.crear_scroll_canvas(self.main_frame); container = tk.Frame(scroll, bg=COLOR_BG_MAIN); container.pack(fill="both", expand=True, pady=20)
        card = tk.Frame(container, bg="white", padx=40, pady=40, width=800); card.pack(anchor="center")
        color_titulo = COLOR_DANGER if tipo == "Perdido" else COLOR_ACCENT
        titulo_texto = f"Reportar Mascota Perdida" if tipo == "Perdido" else "¡Encontré una Mascota!"
        tk.Label(card, text=titulo_texto, font=("Helvetica", 20, "bold"), fg=color_titulo, bg="white").pack(pady=(0, 20))
        f_cols = tk.Frame(card, bg="white"); f_cols.pack(fill="both", expand=True)
        col_izq = tk.Frame(f_cols, bg="white", width=350); col_izq.pack(side="left", fill="y", padx=(0, 20))
        col_der = tk.Frame(f_cols, bg="white", width=400); col_der.pack(side="left", fill="both", expand=True)
        tk.Label(col_izq, text="Nombre (o apodo):", bg="white", font=("Arial", 10, "bold")).pack(anchor="w"); e_n = tk.Entry(col_izq, bg="#F0F0F0", font=("Arial", 11)); e_n.pack(fill="x", pady=5)
        tk.Label(col_izq, text="Tipo:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w"); cb_t = ttk.Combobox(col_izq, values=["Perro", "Gato", "Otro"], state="readonly", font=("Arial", 11)); cb_t.pack(fill="x", pady=5); cb_t.current(0)
        tk.Label(col_izq, text="Edad Aprox. (Ej: Adulto, Cachorro):", bg="white", font=("Arial", 10, "bold")).pack(anchor="w"); e_edad = tk.Entry(col_izq, bg="#F0F0F0", font=("Arial", 11)); e_edad.pack(fill="x", pady=5)
        tk.Label(col_izq, text="Descripción (Color, collar, etc):", bg="white", font=("Arial", 10, "bold")).pack(anchor="w"); e_d = tk.Entry(col_izq, bg="#F0F0F0", font=("Arial", 11)); e_d.pack(fill="x", pady=5)
        tk.Label(col_izq, text="Tu Teléfono de Contacto:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w"); e_c = tk.Entry(col_izq, bg="#F0F0F0", font=("Arial", 11)); e_c.pack(fill="x", pady=5)
        self.ruta_imagen_temporal = ""; lbl_f = tk.Label(col_izq, text="Sin foto seleccionada", bg="white", fg="gray")
        def subir(): 
            f = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")]) 
            if f: self.ruta_imagen_temporal = f; lbl_f.config(text=f"📷 {os.path.basename(f)}", fg=COLOR_ACCENT)
        tk.Button(col_izq, text="📷 Subir Foto", command=subir, bg="#EEEEEE", bd=0, padx=10, pady=5, cursor="hand2").pack(anchor="w", pady=(10, 0)); lbl_f.pack(anchor="w")
        tk.Label(col_der, text="📍 Ubicación Exacta (Haz click en el mapa):", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        self.temp_lat = -12.046; self.temp_lon = -77.042
        mv = tkintermapview.TkinterMapView(col_der, width=400, height=350, corner_radius=10); mv.pack(fill="both", expand=True)
        mv.set_position(self.temp_lat, self.temp_lon); mv.set_zoom(12)
        lbl_coords = tk.Label(col_der, text="Ubicación por defecto", bg="white", fg="gray", font=("Arial", 8)); lbl_coords.pack(pady=2)
        def click_mapa(coords): self.temp_lat, self.temp_lon = coords; mv.delete_all_marker(); mv.set_marker(coords[0], coords[1], text="Aquí lo vi"); lbl_coords.config(text="Ubicación marcada correctamente", fg="green")
        mv.add_left_click_map_command(click_mapa)
        def guardar():
            if not self.ruta_imagen_temporal: messagebox.showwarning("Falta Foto", "Es muy importante subir una foto para identificar a la mascota."); return
            if not e_n.get() or not e_c.get(): messagebox.showwarning("Faltan Datos", "Por favor completa al menos el nombre/apodo y el contacto."); return
            try:
                nombre_img = f"REP_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.path.basename(self.ruta_imagen_temporal)}"
                dest = os.path.join("assets/uploads", nombre_img)
                shutil.copy(self.ruta_imagen_temporal, dest)
                nuevo_reporte = { "Nombre": e_n.get(), "Tipo": cb_t.get(), "Raza": "Mestizo", "Edad": e_edad.get(), "Descripcion": e_d.get(), "Contacto": e_c.get(), "Latitud": self.temp_lat, "Longitud": self.temp_lon, "FotoPath": dest, "Estado": tipo, "FechaPerdido": datetime.now() }
                self.db_mascotas_perdidas.append(nuevo_reporte)
                try:
                    self.insert_mascota_perdida(nuevo_reporte)
                    # RECARGAR LA DB PARA OBTENER EL ID (CORRECCION IMPORTANTE PARA EL BOTÓN ELIMINAR)
                    self.load_db()
                except Exception:
                    pass
                messagebox.showinfo("Reporte Exitoso", f"Se ha publicado el reporte de {tipo}."); self.mostrar_perdidos()
            except Exception as e: messagebox.showerror("Error Crítico", str(e))
        btn_bg_save = COLOR_DANGER if tipo == "Perdido" else COLOR_ACCENT
        tk.Button(card, text="PUBLICAR REPORTE", bg=btn_bg_save, fg="white", font=("Arial", 12, "bold"), pady=10, width=30, command=guardar).pack(pady=20)

    def cargar_lista_perdidos(self):
        for w in self.container_perdidos.winfo_children(): w.destroy()
        data = [m for m in self.db_mascotas_perdidas if m['Estado'] == self.filtro_estado_perdidos]; data.reverse()
        if not data: tk.Label(self.container_perdidos, text="No hay reportes.", bg=COLOR_BG_MAIN, font=("Arial", 14), fg="gray").pack(pady=50); return
        for m in data:
            card = tk.Frame(self.container_perdidos, bg="white", bd=0, padx=10, pady=10); card.pack(fill="x", padx=100, pady=10); card.config(highlightbackground="#E0E0E0", highlightthickness=1)
            main_frame = tk.Frame(card, bg="white")
            main_frame.pack(fill="both", expand=True, padx=15, pady=10)
            img_frame = tk.Frame(main_frame, bg="white", width=200, height=200)
            img_frame.pack(side="left", padx=(0, 20))
            img_frame.pack_propagate(False) 
            img = self.crear_imagen(m.get('FotoPath'), size=(200, 200), fallback_color="#EEEEEE")
            img_label = tk.Label(img_frame, image=img, bg="white")
            img_label.image = img 
            img_label.pack()
            info_frame = tk.Frame(main_frame, bg="white")
            info_frame.pack(side="left", fill="both", expand=True)
            tk.Label(info_frame, text=m['Nombre'] or "Sin nombre", font=("Arial", 18, "bold"), fg="#333", bg="white").pack(anchor="w", pady=(0, 5))
            details_frame = tk.Frame(info_frame, bg="white")
            details_frame.pack(anchor="w", fill="x", pady=(0, 10))
            if m.get('Tipo'):
                tk.Label(details_frame, text=f"Tipo: {m['Tipo']}", font=("Arial", 10, "bold"), fg="#555", bg="white").pack(anchor="w", side="left", padx=(0, 20))
            if m.get('Edad'):
                tk.Label(details_frame, text=f"Edad: {m['Edad']}", font=("Arial", 10, "bold"), fg="#555", bg="white").pack(anchor="w", side="left", padx=(0, 20))
            if m.get('Raza'):
                tk.Label(details_frame, text=f"Raza: {m['Raza']}", font=("Arial", 10, "bold"), fg="#555", bg="white").pack(anchor="w", side="left", padx=(0, 20))
            if m.get('Descripcion'):
                tk.Label(info_frame, text=f"Descripción: {m['Descripcion']}", font=("Arial", 11), fg="#555", bg="white", wraplength=400).pack(anchor="w", pady=(0, 5))
            if m.get('Contacto'):
                contact_frame = tk.Frame(info_frame, bg="white")
                contact_frame.pack(anchor="w", fill="x", pady=(5, 0))
                tk.Label(contact_frame, text="Contacto:", font=("Arial", 10, "bold"), fg="#555", bg="white").pack(anchor="w", side="left", padx=(0, 10))
                tk.Label(contact_frame, text=m['Contacto'], font=("Arial", 10), fg="#2196F3", bg="white").pack(anchor="w", side="left")
            if m.get('FechaPerdido'):
                date_frame = tk.Frame(info_frame, bg="white")
                date_frame.pack(anchor="w", fill="x", pady=(5, 10))
                tk.Label(date_frame, text="Fecha reporte:", font=("Arial", 10, "bold"), fg="#555", bg="white").pack(anchor="w", side="left", padx=(0, 10))
                fecha_str = str(m['FechaPerdido'])
                if ' ' in fecha_str:
                    fecha_str = fecha_str.split(' ')[0]
                tk.Label(date_frame, text=fecha_str, font=("Arial", 10), fg="#777", bg="white").pack(anchor="w", side="left")
            btn_frame = tk.Frame(card, bg="white")
            btn_frame.pack(side="right", padx=20)
            tk.Button(btn_frame, text="📍 VER UBICACIÓN", bg=COLOR_SECONDARY, fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, bd=0, cursor="hand2", command=lambda x=m: self.ver_mapa_perdido(x)).pack(pady=(0, 5))
            # BOTÓN ELIMINAR CORREGIDO: Ahora aparecerá siempre si se recarga la DB
            if 'id' in m and m['id'] is not None:
                tk.Button(btn_frame, text="🗑️ ELIMINAR", bg=COLOR_DANGER, fg="white", font=("Arial", 10, "bold"), padx=15, pady=5, bd=0, cursor="hand2", command=lambda x=m: self.eliminar_perdido_confirmar(x)).pack()

    def eliminar_perdido_confirmar(self, mascota):
        if messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar a {mascota['Nombre']}?\n\nEsta acción no se puede deshacer."):
            try:
                self.eliminar_mascota_perdida(mascota['id'])
                messagebox.showinfo("Eliminado", f"{mascota['Nombre']} ha sido eliminado correctamente.")
                self.cargar_lista_perdidos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la mascota: {str(e)}")

    def ver_mapa_perdido(self, m):
        self.limpiar_frame(); nav = tk.Frame(self.main_frame, bg="white", height=60, pady=10); nav.pack(fill="x")
        tk.Button(nav, text="⬅ Volver", command=self.mostrar_perdidos, bg="white", fg=COLOR_TEXT, bd=0, font=("Arial", 11, "bold")).pack(side="left", padx=20)
        
        # --- NUEVO DISEÑO ---
        map_c = tk.Frame(self.main_frame, bg="white"); map_c.pack(fill="both", expand=True)
        
        # Panel Izquierdo con Foto e Información
        panel = tk.Frame(map_c, bg="white", width=350, padx=20, pady=20)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False) # Mantener ancho fijo

        # 1. Foto Grande (CORREGIDO AQUI)
        img = self.crear_imagen(m.get('FotoPath'), size=(300, 300))
        lbl_img = tk.Label(panel, image=img, bg="white") # Asignamos a variable
        lbl_img.image = img # <--- ESTO FALTABA: Guardar referencia para que no se borre
        lbl_img.pack(pady=(0, 20))
        
        # 2. Nombre
        tk.Label(panel, text=m['Nombre'], font=("Helvetica", 24, "bold"), bg="white", fg=COLOR_TEXT).pack()
        
        # 3. Datos Resumidos
        info_text = f"{m.get('Tipo', '')} • {m.get('Raza', '')}\n{m.get('Edad', '')}"
        tk.Label(panel, text=info_text, font=("Arial", 11), fg="gray", bg="white", justify="center").pack(pady=(5, 10))

        # 4. Mensaje Personalizado
        tk.Label(panel, text=f"¡{m['Nombre']} te está esperando!", font=("Comic Sans MS", 14, "bold"), fg=COLOR_PRIMARY, bg="white").pack(pady=20)
        
        tk.Label(panel, text=f"Contacto: {m.get('Contacto', '')}", font=("Arial", 11, "bold"), fg="#333", bg="white").pack(side="bottom", pady=20)

        # Mapa a la derecha
        mv = tkintermapview.TkinterMapView(map_c, width=800, height=600); mv.pack(side="right", fill="both", expand=True)
        if m['Latitud']: mv.set_position(float(m['Latitud']), float(m['Longitud'])); mv.set_zoom(16); mv.set_marker(float(m['Latitud']), float(m['Longitud']), text=m['Nombre'])

    # ==========================================
    # LOGIN / REGISTRO / BLACKLIST ABUSERS
    # ==========================================
    def mostrar_bl_abusers(self):
        self.limpiar_frame(); nav = self.crear_nav("Lista Negra: Maltratadores", self.mostrar_bienvenida)
        tk.Button(nav, text="REPORTAR NUEVO", bg=COLOR_DANGER, fg="white", command=self.form_bl_abuser).pack(side="right", padx=20)
        content = self.crear_scroll_canvas(self.main_frame); data = self.db_blacklist_maltrato; data.reverse()
        for item in data:
            card = tk.Frame(content, bg="white", bd=1, relief="solid", padx=10, pady=10); card.pack(fill="x", padx=50, pady=10); row = tk.Frame(card, bg="white"); row.pack(fill="x")
            img = self.crear_imagen(item.get('FotoPath', ''), size=(80, 80), fallback_color="#EF5350"); lbl_i = tk.Label(row, image=img, bg="white"); lbl_i.image = img; lbl_i.pack(side="left")
            txt_f = tk.Frame(row, bg="white", padx=15); txt_f.pack(side="left", fill="both", expand=True)
            nombre = item.get('Nombre', 'Sujeto Desconocido'); tk.Label(txt_f, text=f"DENUNCIADO: {nombre}", font=("Arial", 9, "bold"), fg="gray", bg="white").pack(anchor="w")
            razon = item.get('Descripcion', 'Sin motivo especificado'); razon_limpia = razon.replace("FISICO:", "").replace("HECHOS:", "").replace("\n", " ").strip()
            if len(razon_limpia) > 80: razon_limpia = razon_limpia[:80] + "..."
            tk.Label(txt_f, text=f"⚠️ {razon_limpia}", font=("Arial", 12, "bold"), fg=COLOR_DANGER, bg="white").pack(anchor="w", pady=(5, 0))
            tk.Button(row, text="VER DETALLES ➤", bg="#EEEEEE", bd=0, cursor="hand2", command=lambda i=item: self.ver_detalle_abuser(i)).pack(side="right")

    def ver_detalle_abuser(self, data):
        self.limpiar_frame(); self.crear_nav("Detalle del Reporte", self.mostrar_bl_abusers)
        main = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=40, pady=20); main.pack(fill="both", expand=True)
        col_izq = tk.Frame(main, bg=COLOR_BG_CARD, padx=20, pady=20, bd=1, relief="solid"); col_izq.pack(side="left", fill="both", expand=True, padx=(0, 20))
        img = self.crear_imagen(data.get('FotoPath', ''), size=(300, 300), fallback_color="#EF5350"); lbl = tk.Label(col_izq, image=img, bg="white"); lbl.image = img; lbl.pack(pady=10)
        tk.Label(col_izq, text="Descripción:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w"); txt = tk.Text(col_izq, height=8, font=FONT_BODY, bg="#FAFAFA", bd=0); txt.insert("1.0", data['Descripcion']); txt.config(state="disabled"); txt.pack(fill="x", pady=5)
        col_der = tk.Frame(main, bg="white", bd=1, relief="solid", padx=10, pady=10); col_der.pack(side="right", fill="both", expand=True)
        mv = tkintermapview.TkinterMapView(col_der); mv.pack(fill="both", expand=True)
        if data['Latitud']: mv.set_position(float(data['Latitud']), float(data['Longitud'])); mv.set_zoom(15); mv.set_marker(float(data['Latitud']), float(data['Longitud']), text="Aquí")

    def form_bl_abuser(self):
        self.limpiar_frame(); nav = tk.Frame(self.main_frame, bg="white", height=60, pady=10); nav.pack(fill="x")
        tk.Button(nav, text="⬅ Cancelar Denuncia", command=self.mostrar_bl_abusers, bg="white", fg=COLOR_DANGER, bd=0, font=("Arial", 11, "bold"), cursor="hand2").pack(side="left", padx=20)
        tk.Label(nav, text="Nueva Denuncia de Maltrato", font=FONT_SUBTITLE, bg="white", fg=COLOR_DANGER).pack(side="left", padx=10)
        scroll = self.crear_scroll_canvas(self.main_frame); container = tk.Frame(scroll, bg=COLOR_BG_MAIN); container.pack(fill="both", expand=True, pady=20)
        card = tk.Frame(container, bg="white", padx=30, pady=30, bd=1, relief="solid"); card.pack(anchor="center", padx=20)
        header_frame = tk.Frame(card, bg=COLOR_DANGER, padx=10, pady=10); header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="⚠️ REPORTE DE MALTRATADOR", font=("Helvetica", 18, "bold"), fg="white", bg=COLOR_DANGER).pack()
        tk.Label(card, text="Tu denuncia es anónima y ayuda a proteger a los animales.", font=("Arial", 10, "italic"), fg="gray", bg="white").pack(pady=(0, 20))
        f_body = tk.Frame(card, bg="white"); f_body.pack(fill="both", expand=True)
        col_izq = tk.Frame(f_body, bg="white", width=350); col_izq.pack(side="left", fill="y", padx=(0, 30), anchor="n")
        tk.Label(col_izq, text="Nombre o Alias (si se conoce):", font=("Arial", 10, "bold"), bg="white", fg=COLOR_TEXT).pack(anchor="w", pady=(0, 5)); e_nombre = tk.Entry(col_izq, bg="#FFEBEE", font=("Arial", 11), width=40); e_nombre.pack(fill="x", pady=(0, 15))
        tk.Label(col_izq, text="Descripción Física del Sujeto:", font=("Arial", 10, "bold"), bg="white", fg=COLOR_TEXT).pack(anchor="w", pady=(0, 5)); t_fisico = tk.Text(col_izq, height=3, bg="#FAFAFA", font=("Arial", 10), width=40); t_fisico.pack(fill="x", pady=(0, 15))
        tk.Label(col_izq, text="Descripción de los Hechos:", font=("Arial", 10, "bold"), bg="white", fg=COLOR_TEXT).pack(anchor="w", pady=(0, 5)); t_hechos = tk.Text(col_izq, height=5, bg="#FAFAFA", font=("Arial", 10), width=40); t_hechos.pack(fill="x", pady=(0, 15))
        tk.Label(col_izq, text="Evidencia Fotográfica:", font=("Arial", 10, "bold"), bg="white", fg=COLOR_TEXT).pack(anchor="w", pady=(5, 5)); f_foto = tk.Frame(col_izq, bg="white", bd=1, relief="solid"); f_foto.pack(fill="x", pady=5)
        self.ruta_evidencia = None; lbl_status_foto = tk.Label(f_foto, text="Ninguna foto seleccionada", bg="white", fg="gray", pady=10)
        def seleccionar_evidencia():
            f = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
            if f: self.ruta_evidencia = f; lbl_status_foto.config(text=f"📷 {os.path.basename(f)}", fg=COLOR_DANGER, font=("Arial", 9, "bold"))
        btn_foto = tk.Button(f_foto, text="SUBIR FOTO", bg="#EEEEEE", bd=0, cursor="hand2", command=seleccionar_evidencia, font=("Arial", 9, "bold")); btn_foto.pack(side="left", fill="y", padx=0); lbl_status_foto.pack(side="left", padx=10)
        col_der = tk.Frame(f_body, bg="white", width=400); col_der.pack(side="left", fill="both", expand=True)
        tk.Label(col_der, text="📍 Ubicación del Incidente (Haz clic en el mapa):", font=("Arial", 10, "bold"), bg="white", fg=COLOR_DANGER).pack(anchor="w", pady=(0, 10))
        self.denuncia_lat = -12.046; self.denuncia_lon = -77.042
        map_widget = tkintermapview.TkinterMapView(col_der, width=400, height=350, corner_radius=10); map_widget.pack(fill="both", expand=True)
        map_widget.set_position(self.denuncia_lat, self.denuncia_lon); map_widget.set_zoom(12)
        lbl_coords = tk.Label(col_der, text="Ubicación no marcada", bg="white", fg="gray", font=("Arial", 9)); lbl_coords.pack(pady=5)
        def marcar_punto(coords): self.denuncia_lat, self.denuncia_lon = coords; map_widget.delete_all_marker(); map_widget.set_marker(self.denuncia_lat, self.denuncia_lon, text="Lugar del Hecho"); lbl_coords.config(text="✅ Ubicación marcada", fg=COLOR_ACCENT)
        map_widget.add_left_click_map_command(marcar_punto)
        def guardar_denuncia():
            nombre = e_nombre.get().strip() or "Sujeto Desconocido"; fisico = t_fisico.get("1.0", "end-1c").strip(); hechos = t_hechos.get("1.0", "end-1c").strip()
            if not hechos: messagebox.showwarning("Faltan datos", "Por favor describe los hechos ocurridos."); return
            if not self.ruta_evidencia: messagebox.showwarning("Evidencia", "Es necesario subir una foto como evidencia para la lista negra."); return
            try:
                nombre_archivo = f"BL_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.path.basename(self.ruta_evidencia)}"
                destino = os.path.join("assets/uploads", nombre_archivo)
                shutil.copy(self.ruta_evidencia, destino)
                descripcion_completa = f"FISICO: {fisico}\nHECHOS: {hechos}"
                self.db_blacklist_maltrato.append({ "Nombre": nombre, "Descripcion": descripcion_completa, "FotoPath": destino, "Latitud": self.denuncia_lat, "Longitud": self.denuncia_lon, "FechaReporte": datetime.now() })
                try:
                    self.insert_blacklist_maltrato(self.db_blacklist_maltrato[-1])
                except Exception:
                    pass
                messagebox.showinfo("Reportado", "La denuncia ha sido registrada en la Lista Negra."); self.mostrar_bl_abusers()
            except Exception as e: messagebox.showerror("Error Crítico", str(e))
        tk.Frame(card, height=20, bg="white").pack() 
        btn_save = tk.Button(card, text="🚨 REGISTRAR DENUNCIA", bg=COLOR_DANGER, fg="white", font=("Arial", 12, "bold"), pady=12, width=40, bd=0, cursor="hand2", command=guardar_denuncia); btn_save.pack(pady=20)

    def on_closing(self):
        """Método que se llama cuando se cierra la aplicación"""
        try:
            self.cerrar_conexion()  # Cerrar la conexión a la base de datos
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
        finally:
            self.destroy()  # Destruir la ventana y salir de la aplicación


if __name__ == "__main__":
    app = PetApp()
    app.mainloop()