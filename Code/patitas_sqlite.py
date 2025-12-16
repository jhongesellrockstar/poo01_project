"""
Versi\'on alternativa de Patitas Seguras con base de datos SQLite.
Se ejecuta desde la carpeta Code y crea "patitas.db" con datos semilla
para Lima y Callao.
"""
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from PIL import Image, ImageTk, ImageDraw
import tkintermapview

COLOR_BG_MAIN = "#FDF6E4"
COLOR_BG_CARD = "#FFFFFF"
COLOR_PRIMARY = "#FFAB40"
COLOR_SECONDARY = "#4FC3F7"
COLOR_ACCENT = "#8BC34A"
COLOR_TEXT = "#3E2723"
COLOR_DANGER = "#EF5350"
COLOR_BLACK_LIST = "#263238"
COLOR_WARNING = "#FFC107"

FONT_TITLE = ("Helvetica", 20, "bold")
FONT_SUBTITLE = ("Helvetica", 14, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")

DB_PATH = os.path.join(os.path.dirname(__file__), "patitas.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def setup_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT,
            rol TEXT DEFAULT 'Usuario'
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS BlacklistMaltratadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            fechaReporte TEXT,
            latitud REAL,
            longitud REAL,
            fotoPath TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS BlacklistVeterinarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            motivo TEXT,
            latitud REAL,
            longitud REAL,
            fechaReporte TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS RankingVeterinarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            direccion TEXT,
            telefono TEXT,
            descripcion TEXT,
            servicios TEXT,
            promedioEstrellas REAL DEFAULT 0,
            totalVotos INTEGER DEFAULT 0
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS VotosVeterinarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vetID INTEGER,
            userID INTEGER,
            estrellas INTEGER,
            comentario TEXT
        )
        """
    )
    conn.commit()
    seed_data(conn)
    conn.close()


def seed_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Usuarios")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO Usuarios (username, email, password, rol) VALUES (?,?,?,?)",
            [
                ("vecina_callao", "vecina@example.com", "1234", "Usuario"),
                ("vet_lima", "dueno@example.com", "abcd", "Dueño"),
            ],
        )
    cur.execute("SELECT COUNT(*) FROM BlacklistMaltratadores")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO BlacklistMaltratadores (descripcion, fechaReporte, latitud, longitud) VALUES (?,?,?,?)",
            (
                "Reporte de maltrato en el Jr. Colina, Callao. Vecinos escucharon golpes y se alert\'o a serenazgo.",
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                -12.061,
                -77.133,
            ),
        )
    cur.execute("SELECT COUNT(*) FROM BlacklistVeterinarias")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO BlacklistVeterinarias (nombre, motivo, latitud, longitud, fechaReporte) VALUES (?,?,?,?,?)",
            [
                (
                    "Cl\'inica Canina Callao",
                    "Demora en atenci\'on de emergencia reportada por vecinos.",
                    -12.052,
                    -77.128,
                    datetime.now().strftime("%Y-%m-%d"),
                ),
                (
                    "Veterinaria Miraflores",
                    "Cobros no informados y mal trato documentado en redes sociales.",
                    -12.121,
                    -77.030,
                    datetime.now().strftime("%Y-%m-%d"),
                ),
            ],
        )
    cur.execute("SELECT COUNT(*) FROM RankingVeterinarias")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO RankingVeterinarias (nombre, direccion, telefono, descripcion, servicios, promedioEstrellas, totalVotos) VALUES (?,?,?,?,?,?,?)",
            [
                (
                    "Vet Amigos del Puerto",
                    "Av. Oscar R. Benavides 1234, Callao",
                    "(01) 333-4455",
                    "Atenci\'on 24/7 con enfoque en urgencias.",
                    "Emergencias, vacunas, cirug\'ia menor",
                    4.5,
                    2,
                ),
                (
                    "Centro Vet Miraflores",
                    "Calle Berl\'in 789, Miraflores",
                    "(01) 555-8899",
                    "Cl\'inica con laboratorio interno y adopciones solidarias.",
                    "Laboratorio, adopciones, peluquer\'ia",
                    4.0,
                    1,
                ),
            ],
        )
    conn.commit()


class SQLitePetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        setup_db()
        self.title("Patitas Seguras - SQLite")
        self.geometry("1200x820")
        self.configure(bg=COLOR_BG_MAIN)
        self.user_id = None
        self.user_name = None
        self.user_role = None

        self.main_frame = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.main_frame.pack(fill="both", expand=True)
        self.mostrar_bienvenida()

    def ejecutar_sql(self, sql, params=()):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        conn.close()

    def obtener_datos(self, sql, params=()):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def limpiar_frame(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def crear_nav(self, titulo, cmd_volver):
        nav = tk.Frame(self.main_frame, bg="white", height=60, pady=10)
        nav.pack(fill="x")
        tk.Button(nav, text="⬅ Volver", command=cmd_volver, bg="white", fg=COLOR_TEXT, bd=0).pack(side="left", padx=20)
        tk.Label(nav, text=titulo, font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left", padx=10)
        return nav

    def crear_scroll_canvas(self, parent):
        canvas = tk.Canvas(parent, bg=COLOR_BG_MAIN, highlightthickness=0)
        scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=COLOR_BG_MAIN)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return frame

    def crear_imagen(self, path, size=(90, 90), fallback_color="#CCCCCC"):
        if path and os.path.exists(path):
            img = Image.open(path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            bg = Image.new("RGB", size, COLOR_BG_CARD)
            x = (size[0] - img.width) // 2
            y = (size[1] - img.height) // 2
            bg.paste(img, (x, y))
            return ImageTk.PhotoImage(bg)
        img = Image.new("RGB", size, fallback_color)
        draw = ImageDraw.Draw(img)
        draw.text((12, size[1] // 2 - 8), "Sin\nFoto", fill="white")
        return ImageTk.PhotoImage(img)

    def mostrar_bienvenida(self):
        self.limpiar_frame()
        head = tk.Frame(self.main_frame, bg=COLOR_PRIMARY, height=110)
        head.pack(fill="x")
        tk.Label(head, text="🐾 Patitas Seguras (SQLite)", font=("Comic Sans MS", 28, "bold"), bg=COLOR_PRIMARY, fg="white").pack(pady=25)

        grid = tk.Frame(self.main_frame, bg=COLOR_BG_MAIN)
        grid.pack(expand=True)
        self.btn_menu(grid, "Ingresar", COLOR_SECONDARY, self.mostrar_login, 0, 0)
        self.btn_menu(grid, "Lista negra maltrato", COLOR_DANGER, self.mostrar_bl_abusers, 1, 0)
        self.btn_menu(grid, "Lista negra veterinarias", COLOR_BLACK_LIST, self.mostrar_bl_vets, 1, 1)
        self.btn_menu(grid, "Ranking veterinarias", COLOR_WARNING, self.mostrar_ranking, 2, 0, colspan=2)

    def btn_menu(self, parent, text, color, cmd, r, c, colspan=1):
        tk.Button(parent, text=text, bg=color, fg="white", font=("Arial", 14, "bold"), width=28 if colspan == 1 else 60,
                  height=2, bd=0, command=cmd).grid(row=r, column=c, columnspan=colspan, padx=12, pady=8)

    def mostrar_login(self):
        self.limpiar_frame()
        self.crear_nav("Iniciar sesi\'on", self.mostrar_bienvenida)

        card = tk.Frame(self.main_frame, bg="white", padx=40, pady=40)
        card.pack(pady=30)
        tk.Label(card, text="Usuario", bg="white").pack(anchor="w")
        e_user = tk.Entry(card, width=40)
        e_user.pack(pady=5)
        tk.Label(card, text="Contraseña", bg="white").pack(anchor="w")
        e_pass = tk.Entry(card, show="*", width=40)
        e_pass.pack(pady=5)

        def login():
            u = e_user.get().strip()
            p = e_pass.get().strip()
            res = self.obtener_datos("SELECT * FROM Usuarios WHERE username=? AND password=?", (u, p))
            if res:
                self.user_id = res[0]["id"]
                self.user_name = res[0]["username"]
                self.user_role = res[0].get("rol", "Usuario")
                messagebox.showinfo("Bienvenido", f"Hola {self.user_name} ({self.user_role})")
                self.mostrar_ranking()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")

        tk.Button(card, text="Entrar", bg=COLOR_PRIMARY, fg="white", font=FONT_BUTTON, command=login).pack(pady=10)
        tk.Button(card, text="Registrarme", bg="white", fg="blue", bd=0, command=self.mostrar_registro).pack()

    def mostrar_registro(self):
        self.limpiar_frame()
        self.crear_nav("Registro", self.mostrar_login)
        card = tk.Frame(self.main_frame, bg="white", padx=40, pady=40)
        card.pack(pady=20)

        tk.Label(card, text="Usuario", bg="white").pack(anchor="w")
        e_user = tk.Entry(card); e_user.pack(fill="x", pady=4)
        tk.Label(card, text="Correo", bg="white").pack(anchor="w")
        e_mail = tk.Entry(card); e_mail.pack(fill="x", pady=4)
        tk.Label(card, text="Contraseña", bg="white").pack(anchor="w")
        e_pass = tk.Entry(card, show="*"); e_pass.pack(fill="x", pady=4)

        var_rol = tk.StringVar(value="Usuario")
        tk.Radiobutton(card, text="Usuario", variable=var_rol, value="Usuario", bg="white").pack(anchor="w")
        tk.Radiobutton(card, text="Dueño de veterinaria", variable=var_rol, value="Dueño", bg="white").pack(anchor="w")

        def registrar():
            try:
                self.ejecutar_sql(
                    "INSERT INTO Usuarios (username, email, password, rol) VALUES (?,?,?,?)",
                    (e_user.get(), e_mail.get(), e_pass.get(), var_rol.get()),
                )
                messagebox.showinfo("Listo", "Cuenta creada")
                self.mostrar_login()
            except sqlite3.IntegrityError:
                messagebox.showerror("Aviso", "El usuario ya existe")

        tk.Button(card, text="Registrar", bg=COLOR_ACCENT, fg="white", command=registrar).pack(pady=10)

    def mostrar_bl_abusers(self):
        self.limpiar_frame()
        nav = self.crear_nav("Lista negra de maltrato", self.mostrar_bienvenida)
        tk.Button(nav, text="Reportar", bg=COLOR_DANGER, fg="white", command=self.form_bl_abuser).pack(side="right", padx=15)

        cont = self.crear_scroll_canvas(self.main_frame)
        data = self.obtener_datos("SELECT * FROM BlacklistMaltratadores ORDER BY fechaReporte DESC")
        if not data:
            tk.Label(cont, text="Sin reportes", bg=COLOR_BG_MAIN).pack(pady=10)
        for item in data:
            card = tk.Frame(cont, bg="white", bd=1, relief="solid", padx=10, pady=10)
            card.pack(fill="x", padx=40, pady=8)
            row = tk.Frame(card, bg="white"); row.pack(fill="x")
            img = self.crear_imagen(item.get("fotoPath"), fallback_color=COLOR_DANGER)
            lbl = tk.Label(row, image=img, bg="white"); lbl.image = img
            lbl.pack(side="left")
            txt = tk.Frame(row, bg="white", padx=10); txt.pack(side="left", fill="both", expand=True)
            tk.Label(txt, text="Reporte de maltrato", font=FONT_SUBTITLE, fg=COLOR_DANGER, bg="white").pack(anchor="w")
            tk.Label(txt, text=item.get("descripcion", ""), bg="white", wraplength=650, justify="left").pack(anchor="w")
            if item.get("latitud") and item.get("longitud"):
                tk.Button(row, text="Ver en mapa", command=lambda d=item: self.ver_mapa(d)).pack(side="right")

    def ver_mapa(self, data):
        top = tk.Toplevel(self)
        top.title("Ubicaci\'on")
        mv = tkintermapview.TkinterMapView(top, width=500, height=400)
        mv.pack(fill="both", expand=True)
        mv.set_position(data.get("latitud", -12.046), data.get("longitud", -77.042))
        mv.set_zoom(14)
        if data.get("latitud") and data.get("longitud"):
            mv.set_marker(data["latitud"], data["longitud"], text="Reporte")

    def form_bl_abuser(self):
        top = tk.Toplevel(self)
        top.title("Nuevo reporte")
        tk.Label(top, text="Descripci\'on").pack(anchor="w")
        txt = tk.Text(top, width=50, height=5); txt.pack(pady=4)
        tk.Label(top, text="Latitud").pack(anchor="w")
        e_lat = tk.Entry(top); e_lat.pack()
        tk.Label(top, text="Longitud").pack(anchor="w")
        e_lon = tk.Entry(top); e_lon.pack()

        def guardar():
            try:
                lat = float(e_lat.get()) if e_lat.get() else None
                lon = float(e_lon.get()) if e_lon.get() else None
            except ValueError:
                messagebox.showerror("Datos", "Coordenadas no v\'alidas")
                return
            self.ejecutar_sql(
                "INSERT INTO BlacklistMaltratadores (descripcion, fechaReporte, latitud, longitud) VALUES (?,?,?,?)",
                (txt.get("1.0", "end-1c"), datetime.now().strftime("%Y-%m-%d %H:%M"), lat, lon),
            )
            messagebox.showinfo("Guardado", "Reporte registrado")
            top.destroy()
            self.mostrar_bl_abusers()

        tk.Button(top, text="Guardar", bg=COLOR_DANGER, fg="white", command=guardar).pack(pady=8)

    def mostrar_bl_vets(self):
        self.limpiar_frame()
        nav = self.crear_nav("Lista negra de veterinarias", self.mostrar_bienvenida)
        tk.Button(nav, text="Mapa", bg=COLOR_SECONDARY, fg="white", command=self.ver_mapa_general_vets).pack(side="right", padx=5)
        tk.Button(nav, text="Reportar", bg=COLOR_BLACK_LIST, fg="white", command=self.form_bl_vet).pack(side="right", padx=5)

        cont = self.crear_scroll_canvas(self.main_frame)
        data = self.obtener_datos("SELECT * FROM BlacklistVeterinarias ORDER BY fechaReporte DESC")
        for item in data:
            card = tk.Frame(cont, bg="white", bd=1, relief="solid", padx=12, pady=12)
            card.pack(fill="x", padx=40, pady=8)
            tk.Label(card, text=item.get("nombre", ""), font=FONT_SUBTITLE, fg=COLOR_DANGER, bg="white").pack(anchor="w")
            tk.Label(card, text=item.get("motivo", ""), bg="white", wraplength=700, justify="left").pack(anchor="w", pady=4)
            if item.get("latitud") and item.get("longitud"):
                tk.Button(card, text="Ver ubicaci\'on", command=lambda d=item: self.ver_detalle_bl_vet(d)).pack(anchor="e")

    def ver_detalle_bl_vet(self, item):
        top = tk.Toplevel(self)
        top.title(item.get("nombre", "Veterinaria"))
        info = tk.Frame(top, bg="white", padx=12, pady=12)
        info.pack(fill="both", expand=True)
        tk.Label(info, text=item.get("nombre", ""), font=FONT_TITLE, bg="white", fg=COLOR_DANGER).pack(anchor="w")
        tk.Label(info, text=item.get("motivo", ""), bg="white", wraplength=500, justify="left").pack(anchor="w", pady=8)
        if item.get("latitud") and item.get("longitud"):
            mv = tkintermapview.TkinterMapView(info, width=520, height=360)
            mv.pack(fill="both", expand=True, pady=10)
            mv.set_position(item["latitud"], item["longitud"])
            mv.set_zoom(14)
            mv.set_marker(item["latitud"], item["longitud"], text=item.get("nombre", ""))

    def ver_mapa_general_vets(self):
        top = tk.Toplevel(self)
        top.title("Mapa de alertas")
        mv = tkintermapview.TkinterMapView(top, width=650, height=520)
        mv.pack(fill="both", expand=True)
        mv.set_position(-12.046, -77.042)
        mv.set_zoom(11)
        data = self.obtener_datos("SELECT * FROM BlacklistVeterinarias WHERE latitud IS NOT NULL AND longitud IS NOT NULL")
        for item in data:
            mv.set_marker(item["latitud"], item["longitud"], text=item.get("nombre", ""))

    def form_bl_vet(self):
        top = tk.Toplevel(self)
        top.title("Reportar veterinaria")
        tk.Label(top, text="Nombre").pack(anchor="w")
        e_name = tk.Entry(top, width=40); e_name.pack()
        tk.Label(top, text="Motivo").pack(anchor="w")
        txt = tk.Text(top, width=50, height=4); txt.pack(pady=4)
        tk.Label(top, text="Latitud").pack(anchor="w")
        e_lat = tk.Entry(top); e_lat.pack()
        tk.Label(top, text="Longitud").pack(anchor="w")
        e_lon = tk.Entry(top); e_lon.pack()

        def guardar():
            try:
                lat = float(e_lat.get()) if e_lat.get() else None
                lon = float(e_lon.get()) if e_lon.get() else None
            except ValueError:
                messagebox.showerror("Datos", "Coordenadas no v\'alidas")
                return
            self.ejecutar_sql(
                "INSERT INTO BlacklistVeterinarias (nombre, motivo, latitud, longitud, fechaReporte) VALUES (?,?,?,?,?)",
                (e_name.get(), txt.get("1.0", "end-1c"), lat, lon, datetime.now().strftime("%Y-%m-%d")),
            )
            messagebox.showinfo("Listo", "Veterinaria registrada")
            top.destroy()
            self.mostrar_bl_vets()

        tk.Button(top, text="Guardar", bg=COLOR_BLACK_LIST, fg="white", command=guardar).pack(pady=8)

    def mostrar_ranking(self):
        self.limpiar_frame()
        nav = self.crear_nav("Ranking de veterinarias", self.mostrar_bienvenida)
        if self.user_role == "Dueño":
            tk.Button(nav, text="Registrar veterinaria", bg=COLOR_ACCENT, fg="white", command=self.form_ranking_vet).pack(side="right", padx=10)
        cont = self.crear_scroll_canvas(self.main_frame)
        data = self.obtener_datos("SELECT * FROM RankingVeterinarias ORDER BY promedioEstrellas DESC")
        for vet in data:
            card = tk.Frame(cont, bg="white", bd=1, relief="solid", padx=12, pady=12)
            card.pack(fill="x", padx=40, pady=8)
            head = tk.Frame(card, bg="white"); head.pack(fill="x")
            tk.Label(head, text=vet.get("nombre", ""), font=FONT_SUBTITLE, bg="white", fg=COLOR_TEXT).pack(side="left")
            stars = "⭐" * int(round(vet.get("promedioEstrellas", 0)))
            tk.Label(head, text=f"{stars} ({vet.get('promedioEstrellas', 0):.1f})", bg="white", fg=COLOR_WARNING).pack(side="right")
            tk.Label(card, text=f"📍 {vet.get('direccion','')} | 📞 {vet.get('telefono','')}", bg="white", fg="gray").pack(anchor="w", pady=3)
            if vet.get("descripcion"):
                tk.Label(card, text=vet.get("descripcion"), bg="white", wraplength=700, justify="left").pack(anchor="w")
            if vet.get("servicios"):
                tk.Label(card, text=f"Servicios: {vet.get('servicios')}", bg="#E3F2FD", fg="#1565C0", padx=4).pack(anchor="w", pady=4)
            if self.user_role == "Usuario":
                tk.Button(card, text="Calificar", bg="#FFF3E0", fg=COLOR_PRIMARY,
                          command=lambda v=vet: self.votar_vet(v)).pack(anchor="e", pady=4)

    def form_ranking_vet(self):
        self.limpiar_frame()
        self.crear_nav("Registrar mi veterinaria", self.mostrar_ranking)
        f = tk.Frame(self.main_frame, bg="white", padx=40, pady=20)
        f.pack(fill="both", expand=True, padx=60, pady=20)
        tk.Label(f, text="Nombre", bg="white").pack(anchor="w")
        e_n = tk.Entry(f, width=50); e_n.pack(pady=4)
        tk.Label(f, text="Direcci\'on", bg="white").pack(anchor="w")
        e_d = tk.Entry(f, width=50); e_d.pack(pady=4)
        tk.Label(f, text="Tel\'efono", bg="white").pack(anchor="w")
        e_t = tk.Entry(f, width=50); e_t.pack(pady=4)
        tk.Label(f, text="Descripci\'on", bg="white").pack(anchor="w")
        t_desc = tk.Text(f, height=3, width=55); t_desc.pack(pady=4)
        tk.Label(f, text="Servicios", bg="white").pack(anchor="w")
        e_s = tk.Entry(f, width=50); e_s.pack(pady=4)

        def guardar():
            self.ejecutar_sql(
                "INSERT INTO RankingVeterinarias (nombre, direccion, telefono, descripcion, servicios) VALUES (?,?,?,?,?)",
                (e_n.get(), e_d.get(), e_t.get(), t_desc.get("1.0", "end-1c"), e_s.get()),
            )
            messagebox.showinfo("Publicado", "Veterinaria agregada")
            self.mostrar_ranking()

        tk.Button(f, text="Publicar", bg=COLOR_ACCENT, fg="white", command=guardar).pack(pady=12)

    def votar_vet(self, vet):
        top = tk.Toplevel(self)
        top.title(f"Calificar {vet.get('nombre','')}")
        tk.Label(top, text="Calificaci\'on (1-5)").pack(pady=5)
        combo = ttk.Combobox(top, values=["5", "4", "3", "2", "1"], state="readonly")
        combo.current(0)
        combo.pack()
        tk.Label(top, text="Comentario").pack(pady=4)
        txt = tk.Text(top, height=4, width=35); txt.pack()

        def enviar():
            estrellas = int(combo.get())
            self.ejecutar_sql(
                "INSERT INTO VotosVeterinarias (vetID, userID, estrellas, comentario) VALUES (?,?,?,?)",
                (vet.get("id"), self.user_id, estrellas, txt.get("1.0", "end-1c")),
            )
            data = self.obtener_datos("SELECT AVG(CAST(estrellas AS FLOAT)) as p, COUNT(*) as t FROM VotosVeterinarias WHERE vetID=?", (vet.get("id"),))
            if data:
                self.ejecutar_sql(
                    "UPDATE RankingVeterinarias SET promedioEstrellas=?, totalVotos=? WHERE id=?",
                    (data[0].get("p", 0), data[0].get("t", 0), vet.get("id")),
                )
            messagebox.showinfo("Gracias", "Voto registrado")
            top.destroy()
            self.mostrar_ranking()

        tk.Button(top, text="Enviar", bg=COLOR_PRIMARY, fg="white", command=enviar).pack(pady=8)


def main():
    app = SQLitePetApp()
    app.mainloop()


if __name__ == "__main__":
    main()
