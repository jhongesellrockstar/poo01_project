import tkinter as tk
from tkinter import messagebox, ttk, filedialog, simpledialog
from PIL import Image, ImageTk, ImageDraw
import tkintermapview
import os
import pyodbc
from datetime import datetime

# --- COLORES Y ESTILO ---
COLOR_BG_MAIN = "#FDF6E4"
COLOR_BG_CARD = "#FFFFFF"
COLOR_PRIMARY = "#FFAB40"     # Naranja suave
COLOR_SECONDARY = "#4FC3F7"   # Azul cielo
COLOR_ACCENT = "#8BC34A"      # Verde
COLOR_TEXT = "#3E2723"        # Marrón oscuro
COLOR_DANGER = "#EF5350"      # Rojo alerta
COLOR_BLACK_LIST = "#263238"  # Oscuro para blacklist
COLOR_WARNING = "#FFC107"     # Amarillo estrellas

FONT_TITLE = ("Helvetica", 24, "bold")
FONT_SUBTITLE = ("Helvetica", 16, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")

class PetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Patitas Seguras - Sistema Integral")
        self.geometry("1280x850")
        self.configure(bg=COLOR_BG_MAIN)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- CONEXIÓN SQL (AJUSTA TU SERVER) ---
        self.conn_str = (
            r'DRIVER={SQL Server};'
            r'SERVER=DESKTOP-L8IMN4H;'  # <--- TU SERVIDOR
            r'DATABASE=PetApp;'
            r'Trusted_Connection=yes;'
        )

        # --- VARIABLES DE SESIÓN ---
        self.user_id = None
        self.user_name = None
        self.user_role = None  # 'Usuario' o 'Dueño'

        self.main_frame = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Iniciar App
        self.mostrar_bienvenida()

    # ==========================================
    # HERRAMIENTAS SQL Y GRÁFICAS
    # ==========================================
    def get_db_connection(self):
        try:
            return pyodbc.connect(self.conn_str)
        except Exception as e:
            messagebox.showerror("Error SQL", f"Conexión fallida: {e}")
            return None

    def ejecutar_sql(self, sql, params=()):
        conn = self.get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit()
                return True
            except Exception as e:
                messagebox.showerror("Error SQL", str(e))
                return False
            finally:
                conn.close()
        return False

    def obtener_datos(self, sql, params=()):
        conn = self.get_db_connection()
        data = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                columns = [column[0] for column in cursor.description]
                for row in cursor.fetchall():
                    data.append(dict(zip(columns, row)))
            except Exception as e:
                print(f"Error consulta: {e}")
            finally:
                conn.close()
        return data

    def crear_imagen(self, path, size=(100, 100), fallback_color="#CCCCCC"):
        # Intenta cargar imagen, si falla usa un recuadro de color
        if path and os.path.exists(path):
            try:
                img = Image.open(path)
                img.thumbnail(size, Image.Resampling.LANCZOS)
                bg = Image.new('RGB', size, COLOR_BG_CARD)
                # Centrar
                x = (size[0] - img.width) // 2
                y = (size[1] - img.height) // 2
                bg.paste(img, (x, y))
                return ImageTk.PhotoImage(bg)
            except:
                pass
        
        # Fallback
        img = Image.new('RGB', size, color=fallback_color)
        d = ImageDraw.Draw(img)
        d.rectangle([2,2, size[0]-2, size[1]-2], outline="white", width=2)
        d.text((size[0]//3, size[1]//2), "Sin Foto", fill="white")
        return ImageTk.PhotoImage(img)

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
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
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        
        # Mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return frame

    # ==========================================
    # 1. MENU PRINCIPAL
    # ==========================================
    def mostrar_bienvenida(self):
        self.limpiar_frame()
        
        # Header grande
        head = tk.Frame(self.main_frame, bg=COLOR_PRIMARY, height=120)
        head.pack(fill="x")
        tk.Label(head, text="🐾 Patitas Seguras", font=("Comic Sans MS", 32, "bold"), bg=COLOR_PRIMARY, fg="white").pack(pady=30)
        
        # Grid de opciones
        grid_frame = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        grid_frame.pack(expand=True)

        self.btn_menu(grid_frame, "🐶 ADOPCIÓN", COLOR_ACCENT, self.dummy_adopcion, 0, 0)
        self.btn_menu(grid_frame, "🔍 PERDIDOS", COLOR_SECONDARY, self.dummy_perdidos, 0, 1)
        
        tk.Frame(grid_frame, height=20, bg=COLOR_BG_MAIN).grid(row=1, column=0) # Espacio

        self.btn_menu(grid_frame, "😡 BLACKLIST MALTRATO", COLOR_DANGER, self.mostrar_bl_abusers, 2, 0)
        self.btn_menu(grid_frame, "🚫 BLACKLIST VET", COLOR_BLACK_LIST, self.mostrar_bl_vets, 2, 1)

        tk.Frame(grid_frame, height=20, bg=COLOR_BG_MAIN).grid(row=3, column=0) # Espacio

        self.btn_menu(grid_frame, "⭐ RANKING VETERINARIAS", COLOR_WARNING, self.check_login_ranking, 4, 0, colspan=2)

    def btn_menu(self, parent, text, col, cmd, r, c, colspan=1):
        tk.Button(parent, text=text, bg=col, fg="white", font=("Arial", 14, "bold"), width=25 if colspan==1 else 55, height=2, bd=0, cursor="hand2", command=cmd).grid(row=r, column=c, columnspan=colspan, padx=15, pady=10)

    def dummy_adopcion(self): messagebox.showinfo("Info", "Módulo de Adopción (Código original)")
    def dummy_perdidos(self): messagebox.showinfo("Info", "Módulo de Perdidos (Código original)")

    # ==========================================
    # 2. LOGIN Y REGISTRO (Separado por Roles)
    # ==========================================
    def check_login_ranking(self):
        if self.user_id:
            self.mostrar_ranking()
        else:
            self.mostrar_login()

    def mostrar_login(self):
        self.limpiar_frame()
        self.crear_nav("Iniciar Sesión", self.mostrar_bienvenida)
        
        card = tk.Frame(self.main_frame, bg="white", padx=50, pady=50, bd=1, relief="solid")
        card.pack(pady=50)

        tk.Label(card, text="Acceso a la Comunidad", font=FONT_TITLE, bg="white").pack(pady=(0,20))
        
        tk.Label(card, text="Usuario:", bg="white").pack(anchor="w")
        e_user = tk.Entry(card, font=FONT_BODY, bg="#F0F0F0"); e_user.pack(fill="x", pady=5)
        
        tk.Label(card, text="Contraseña:", bg="white").pack(anchor="w")
        e_pass = tk.Entry(card, show="*", font=FONT_BODY, bg="#F0F0F0"); e_pass.pack(fill="x", pady=5)

        def login():
            u = e_user.get(); p = e_pass.get()
            res = self.obtener_datos("SELECT * FROM Usuarios WHERE Username=? AND Password=?", (u, p))
            if res:
                self.user_id = res[0]['ID']
                self.user_name = res[0]['Username']
                self.user_role = res[0].get('Rol', 'Usuario') # Default Usuario
                messagebox.showinfo("Hola", f"Bienvenido {self.user_name} ({self.user_role})")
                self.mostrar_ranking()
            else:
                messagebox.showerror("Error", "Datos incorrectos")

        tk.Button(card, text="ENTRAR", bg=COLOR_PRIMARY, fg="white", font=FONT_BUTTON, command=login, width=20).pack(pady=20)
        tk.Button(card, text="¿No tienes cuenta? Regístrate", bg="white", fg="blue", bd=0, command=self.mostrar_registro).pack()

    def mostrar_registro(self):
        self.limpiar_frame()
        self.crear_nav("Registro de Nuevo Usuario", self.mostrar_login)
        
        card = tk.Frame(self.main_frame, bg="white", padx=40, pady=40)
        card.pack(pady=20)

        tk.Label(card, text="Usuario:", bg="white").pack(anchor="w")
        e_u = tk.Entry(card, bg="#F0F0F0"); e_u.pack(fill="x", pady=5)
        
        tk.Label(card, text="Email:", bg="white").pack(anchor="w")
        e_m = tk.Entry(card, bg="#F0F0F0"); e_m.pack(fill="x", pady=5)
        
        tk.Label(card, text="Contraseña:", bg="white").pack(anchor="w")
        e_p = tk.Entry(card, show="*", bg="#F0F0F0"); e_p.pack(fill="x", pady=5)

        tk.Label(card, text="Selecciona tu Rol:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(15,5))
        
        var_rol = tk.StringVar(value="Usuario")
        tk.Radiobutton(card, text="Usuario (Quiero votar y opinar)", variable=var_rol, value="Usuario", bg="white").pack(anchor="w")
        tk.Radiobutton(card, text="Dueño de Veterinaria (Quiero registrar mi local)", variable=var_rol, value="Dueño", bg="white").pack(anchor="w")

        def registrar():
            if self.ejecutar_sql("INSERT INTO Usuarios (Username, Email, Password, Rol) VALUES (?,?,?,?)", 
                                 (e_u.get(), e_m.get(), e_p.get(), var_rol.get())):
                messagebox.showinfo("Éxito", "Cuenta creada. Inicia sesión.")
                self.mostrar_login()

        tk.Button(card, text="REGISTRARME", bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON, command=registrar).pack(pady=20)

    # ==========================================
    # 3. BLACKLIST MALTRATADORES (FULL FEATURED)
    # ==========================================
    def mostrar_bl_abusers(self):
        self.limpiar_frame()
        nav = self.crear_nav("Lista Negra: Maltratadores", self.mostrar_bienvenida)
        tk.Button(nav, text="REPORTAR NUEVO", bg=COLOR_DANGER, fg="white", command=self.form_bl_abuser).pack(side="right", padx=20)

        content = self.crear_scroll_canvas(self.main_frame)
        data = self.obtener_datos("SELECT * FROM BlacklistMaltratadores ORDER BY FechaReporte DESC")

        tk.Label(content, text="Haz clic en una tarjeta para ver opciones y actualizar info", bg=COLOR_BG_MAIN, fg="gray").pack(pady=10)

        for item in data:
            card = tk.Frame(content, bg="white", bd=1, relief="solid", padx=10, pady=10)
            card.pack(fill="x", padx=50, pady=10)
            
            # Layout Horizontal
            row = tk.Frame(card, bg="white")
            row.pack(fill="x")
            
            # Foto Miniatura
            img = self.crear_imagen(item['FotoPath'], size=(80, 80), fallback_color="#EF5350")
            lbl_i = tk.Label(row, image=img, bg="white"); lbl_i.image = img
            lbl_i.pack(side="left")
            
            # Textos
            txt_f = tk.Frame(row, bg="white", padx=15)
            txt_f.pack(side="left", fill="both", expand=True)
            
            # Cortar descripción si es muy larga para la vista previa
            desc_short = (item['Descripcion'][:100] + '...') if len(item['Descripcion']) > 100 else item['Descripcion']
            
            tk.Label(txt_f, text="Reporte de Maltrato", font=("Arial", 12, "bold"), fg=COLOR_DANGER, bg="white").pack(anchor="w")
            tk.Label(txt_f, text=desc_short, font=FONT_BODY, bg="white", wraplength=600, justify="left").pack(anchor="w")
            
            # Botón "VER DETALLES"
            tk.Button(row, text="VER DETALLES Y OPCIONES ➤", bg="#EEEEEE", bd=0, cursor="hand2", 
                      command=lambda i=item: self.ver_detalle_abuser(i)).pack(side="right")

    def ver_detalle_abuser(self, data):
        # Pantalla Detalle
        self.limpiar_frame()
        self.crear_nav("Detalle del Reporte", self.mostrar_bl_abusers)
        
        main = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=40, pady=20)
        main.pack(fill="both", expand=True)

        # -- IZQUIERDA: INFO Y CONTACTOS --
        col_izq = tk.Frame(main, bg=COLOR_BG_CARD, padx=20, pady=20, bd=1, relief="solid")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Foto Grande
        img = self.crear_imagen(data['FotoPath'], size=(300, 300), fallback_color="#EF5350")
        lbl = tk.Label(col_izq, image=img, bg="white"); lbl.image = img
        lbl.pack(pady=10)

        tk.Label(col_izq, text="Descripción Completa:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        txt = tk.Text(col_izq, height=8, font=FONT_BODY, bg="#FAFAFA", bd=0)
        txt.insert("1.0", data['Descripcion'])
        txt.config(state="disabled") # Solo lectura
        txt.pack(fill="x", pady=5)

        # Botones de Acción
        btn_row = tk.Frame(col_izq, bg="white")
        btn_row.pack(fill="x", pady=20)

        def emergency():
            messagebox.showwarning("Contactos de Emergencia", 
                                   "📞 Policía Nacional: 105\n📞 Escuadrón Verde: 999-999-999\n📞 Protección Animal: 01-222-3333")

        def update_info():
            nuevo_dato = simpledialog.askstring("Actualizar", "Añadir nueva información (Avistamiento, detalle, etc):")
            if nuevo_dato:
                fecha = datetime.now().strftime("%d/%m %H:%M")
                nueva_desc = data['Descripcion'] + f"\n\n[Actualización {fecha}]: {nuevo_dato}"
                if self.ejecutar_sql("UPDATE BlacklistMaltratadores SET Descripcion=? WHERE ID=?", (nueva_desc, data['ID'])):
                    messagebox.showinfo("Listo", "Información agregada.")
                    data['Descripcion'] = nueva_desc # Actualizar local
                    txt.config(state="normal"); txt.delete("1.0", "end"); txt.insert("1.0", nueva_desc); txt.config(state="disabled")

        tk.Button(btn_row, text="📞 CONTACTO EMERGENCIA", bg=COLOR_DANGER, fg="white", font=("Arial", 10, "bold"), command=emergency).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(btn_row, text="📝 AÑADIR INFORMACIÓN", bg=COLOR_PRIMARY, fg="white", font=("Arial", 10, "bold"), command=update_info).pack(side="left", expand=True, fill="x", padx=5)

        # -- DERECHA: MAPA --
        col_der = tk.Frame(main, bg="white", bd=1, relief="solid", padx=10, pady=10)
        col_der.pack(side="right", fill="both", expand=True)
        
        tk.Label(col_der, text="Ubicación del Incidente:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        
        mv = tkintermapview.TkinterMapView(col_der)
        mv.pack(fill="both", expand=True)
        
        if data['Latitud'] and data['Longitud']:
            lat, lon = float(data['Latitud']), float(data['Longitud'])
            mv.set_position(lat, lon)
            mv.set_zoom(15)
            mv.set_marker(lat, lon, text="Aquí")
        else:
            tk.Label(col_der, text="Sin ubicación registrada", bg="white").pack()

    def form_bl_abuser(self):
        # (Simplificado para brevedad: similar al código anterior pero guardando en tabla Maltratadores)
        # Puedes copiar la logica de tu codigo anterior o te la incluyo si necesitas.
        messagebox.showinfo("Info", "Aquí iría el formulario de reporte de maltratador (Misma lógica que antes)")
        self.mostrar_bl_abusers()

    # ==========================================
    # 4. BLACKLIST VETERINARIAS (MAPA GENERAL)
    # ==========================================
    def mostrar_bl_vets(self):
        self.limpiar_frame()
        nav = self.crear_nav("Lista Negra: Veterinarias", self.mostrar_bienvenida)
        
        # Botones Header
        f_btns = tk.Frame(nav, bg="white")
        f_btns.pack(side="right")
        tk.Button(f_btns, text="🗺️ MAPA GENERAL", bg=COLOR_SECONDARY, fg="white", command=self.ver_mapa_general_vets).pack(side="left", padx=5)
        tk.Button(f_btns, text="🚨 REPORTAR LOCAL", bg=COLOR_BLACK_LIST, fg="white", command=self.form_bl_vet).pack(side="left", padx=5)

        content = self.crear_scroll_canvas(self.main_frame)
        data = self.obtener_datos("SELECT * FROM BlacklistVeterinarias ORDER BY FechaReporte DESC")

        for item in data:
            card = tk.Frame(content, bg="white", bd=1, relief="solid", padx=15, pady=15)
            card.pack(fill="x", padx=50, pady=10)
            
            tk.Label(card, text=item['NombreVeterinaria'], font=("Arial", 16, "bold"), fg=COLOR_DANGER, bg="white").pack(anchor="w")
            tk.Label(card, text=f"Motivo: {item['Motivo']}", font=FONT_BODY, bg="white").pack(anchor="w")
            
            # Botón detalle
            tk.Button(card, text="VER DETALLE Y UBICACIÓN", bg="#EEEEEE", command=lambda x=item: self.ver_detalle_bl_vet(x)).pack(anchor="e", pady=5)

    def ver_detalle_bl_vet(self, item):
        self.limpiar_frame()
        self.crear_nav("Detalle de Veterinaria Reportada", self.mostrar_bl_vets)
        
        cont = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN, padx=40, pady=20)
        cont.pack(fill="both", expand=True)
        
        # Info
        card = tk.Frame(cont, bg="white", padx=20, pady=20)
        card.pack(fill="x")
        
        tk.Label(card, text=item['NombreVeterinaria'], font=FONT_TITLE, fg=COLOR_DANGER, bg="white").pack()
        tk.Label(card, text=item['Motivo'], font=FONT_BODY, bg="white", wraplength=800).pack(pady=20)
        
        # Mapa individual
        if item['Latitud'] and item['Longitud']:
            frm_map = tk.Frame(cont, height=400, bg="white")
            frm_map.pack(fill="x", pady=20)
            mv = tkintermapview.TkinterMapView(frm_map, height=400)
            mv.pack(fill="both", expand=True)
            lat, lon = float(item['Latitud']), float(item['Longitud'])
            mv.set_position(lat, lon)
            mv.set_marker(lat, lon, text=item['NombreVeterinaria'])

    def ver_mapa_general_vets(self):
        top = tk.Toplevel(self)
        top.title("Mapa de Alertas Veterinarias")
        top.geometry("800x600")
        
        mv = tkintermapview.TkinterMapView(top)
        mv.pack(fill="both", expand=True)
        mv.set_position(-12.046, -77.042) # Lima
        mv.set_zoom(12)
        
        data = self.obtener_datos("SELECT * FROM BlacklistVeterinarias WHERE Latitud IS NOT NULL")
        for item in data:
            mv.set_marker(float(item['Latitud']), float(item['Longitud']), text=item['NombreVeterinaria'])

    def form_bl_vet(self):
        # (Simplificado: Usa el mismo formulario que te di en la respuesta anterior para reportar con mapa)
        messagebox.showinfo("Info", "Formulario de reporte de vet (Usar código anterior)")
        self.mostrar_bl_vets()

    # ==========================================
    # 5. RANKING VETERINARIAS (DUEÑOS vs USUARIOS)
    # ==========================================
    def mostrar_ranking(self):
        self.limpiar_frame()
        nav = self.crear_nav(f"Ranking Veterinarias ({self.user_role}: {self.user_name})", self.mostrar_bienvenida)
        
        # Si es Dueño, botón de registrar
        if self.user_role == "Dueño":
            tk.Button(nav, text="➕ REGISTRAR MI VETERINARIA", bg=COLOR_ACCENT, fg="white", font=("Arial", 11, "bold"),
                      command=self.form_ranking_vet).pack(side="right", padx=20)
        
        content = self.crear_scroll_canvas(self.main_frame)
        data = self.obtener_datos("SELECT * FROM RankingVeterinarias ORDER BY PromedioEstrellas DESC")

        if not data:
            tk.Label(content, text="No hay veterinarias registradas aún.", bg=COLOR_BG_MAIN).pack(pady=20)

        for vet in data:
            card = tk.Frame(content, bg="white", bd=1, relief="solid", padx=15, pady=15)
            card.pack(fill="x", padx=50, pady=10)
            
            # Header
            head = tk.Frame(card, bg="white")
            head.pack(fill="x")
            tk.Label(head, text=vet['Nombre'], font=("Arial", 18, "bold"), fg=COLOR_TEXT, bg="white").pack(side="left")
            
            # Estrellas
            stars = "⭐" * int(vet['PromedioEstrellas'] or 0)
            tk.Label(head, text=f"{stars} ({vet['PromedioEstrellas'] or 0})", font=("Segoe UI Emoji", 14), bg="white", fg=COLOR_WARNING).pack(side="right")
            
            # Info
            tk.Label(card, text=f"📍 {vet['Direccion']} | 📞 {vet['Telefono']}", bg="white", fg="gray").pack(anchor="w", pady=5)
            
            # Descripción y Servicios
            if vet.get('Descripcion'):
                tk.Label(card, text=vet['Descripcion'], bg="white", font=("Arial", 10)).pack(anchor="w", pady=2)
            if vet.get('Servicios'):
                tk.Label(card, text=f"🛠️ Servicios: {vet['Servicios']}", bg="#E3F2FD", fg="#1565C0", padx=5).pack(anchor="w", pady=5)

            # Botón Votar (Solo si es Usuario)
            if self.user_role == "Usuario":
                tk.Button(card, text="✍ CALIFICAR", bg="#FFF3E0", fg=COLOR_PRIMARY, bd=0, command=lambda v=vet: self.votar_vet(v)).pack(anchor="e")

    def form_ranking_vet(self):
        # Formulario para Dueños
        self.limpiar_frame()
        self.crear_nav("Registrar Mi Veterinaria", self.mostrar_ranking)
        
        f = tk.Frame(self.main_frame, bg="white", padx=40, pady=20)
        f.pack(fill="both", expand=True, padx=50, pady=20)

        tk.Label(f, text="Nombre del Local:", bg="white").pack(anchor="w")
        e_n = tk.Entry(f, width=50); e_n.pack(anchor="w", pady=5)
        
        tk.Label(f, text="Dirección:", bg="white").pack(anchor="w")
        e_d = tk.Entry(f, width=50); e_d.pack(anchor="w", pady=5)
        
        tk.Label(f, text="Teléfono:", bg="white").pack(anchor="w")
        e_t = tk.Entry(f, width=50); e_t.pack(anchor="w", pady=5)
        
        tk.Label(f, text="Descripción (Horarios, equipo, etc):", bg="white").pack(anchor="w")
        t_desc = tk.Text(f, height=3, width=50); t_desc.pack(anchor="w", pady=5)
        
        tk.Label(f, text="Servicios (Separados por coma):", bg="white").pack(anchor="w")
        e_s = tk.Entry(f, width=50); e_s.pack(anchor="w", pady=5)

        def guardar():
            # SQL Insert
            sql = "INSERT INTO RankingVeterinarias (Nombre, Direccion, Telefono, Descripcion, Servicios) VALUES (?,?,?,?,?)"
            vals = (e_n.get(), e_d.get(), e_t.get(), t_desc.get("1.0", "end-1c"), e_s.get())
            if self.ejecutar_sql(sql, vals):
                messagebox.showinfo("Éxito", "Tu veterinaria ha sido publicada.")
                self.mostrar_ranking()

        tk.Button(f, text="PUBLICAR VETERINARIA", bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON, command=guardar).pack(pady=20)

    def votar_vet(self, vet):
        # Popup para votar
        top = tk.Toplevel(self)
        top.title(f"Calificar a {vet['Nombre']}")
        top.geometry("300x300")
        
        tk.Label(top, text="Tu Calificación:", font=("Arial", 12, "bold")).pack(pady=10)
        combo = ttk.Combobox(top, values=["5", "4", "3", "2", "1"], state="readonly")
        combo.pack()
        combo.current(0)
        
        tk.Label(top, text="Comentario:").pack(pady=5)
        txt = tk.Text(top, height=4, width=30)
        txt.pack()

        def enviar():
            stars = int(combo.get())
            self.ejecutar_sql("INSERT INTO VotosVeterinarias (VetID, UserID, Estrellas, Comentario) VALUES (?,?,?,?)",
                              (vet['ID'], self.user_id, stars, txt.get("1.0", "end-1c")))
            
            # Recalcular promedio (Truco rápido)
            data = self.obtener_datos("SELECT AVG(CAST(Estrellas AS FLOAT)) as P, COUNT(*) as T FROM VotosVeterinarias WHERE VetID=?", (vet['ID'],))
            if data:
                self.ejecutar_sql("UPDATE RankingVeterinarias SET PromedioEstrellas=?, TotalVotos=? WHERE ID=?", 
                                  (data[0]['P'], data[0]['T'], vet['ID']))
            
            messagebox.showinfo("Gracias", "Voto registrado")
            top.destroy()
            self.mostrar_ranking()

        tk.Button(top, text="ENVIAR VOTO", command=enviar, bg=COLOR_PRIMARY, fg="white").pack(pady=20)

if __name__ == "__main__":
    app = PetApp()
    app.mainloop()
