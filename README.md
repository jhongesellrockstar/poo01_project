# 📘 Patitas Seguras — README Oficial
Aplicación de Adopción, Rescate y Comunidad para Mascotas  
Desarrollado en **Python + Tkinter + Pillow + TkinterMapView**

---

## 🐾 1. Descripción del Proyecto

**Patitas Seguras** es una aplicación GUI desarrollada en Python que permite:

- Publicar y buscar animales en adopción.
- Registrar mascotas perdidas y encontradas con mapa interactivo (OpenStreetMap).
- Gestionar reportes con ubicación (TkinterMapView).
- Trabajar con imágenes generadas dinámicamente (Pillow).

La aplicación está diseñada para ser extendida por otros desarrolladores, especialmente en módulos comunitarios centrados en protección animal.

---

## 🚀 2. Características Actuales

- Interfaz moderna con botones personalizados, tarjetas y filtros visuales.
- Uso de mapas interactivos para reportes de animales perdidos.
- Sistema de adopción con detalles por mascota.
- Registro de reportes con imágenes, ubicación y datos del usuario.
- Generación de feedback visual (pantallas de éxito, iconos).

---

## 🔮 3. Módulos en Desarrollo / Propuestos

### ✔ 3.1 Lista Negra de Maltratadores  
Base de datos para registrar:

- Personas que abandonan animales.
- Vecinos que mantienen mascotas en condiciones de maltrato.
- Individuos ligados a venta ilegal o explotación animal.

### ✔ 3.2 Lista Negra de Veterinarias  
Registro colaborativo de clínicas veterinarias con malas prácticas.

### ✔ 3.3 Ranking de Veterinarias  
Sistema de reputación con estrellas, comentarios y ubicación.

### ✔ 3.4 Sincronización + Base de Datos  
Se propone utilizar:

- **SQLite local** incluida en el .exe.
- Futuro soporte para **sincronización en nube** (API REST).

Tablas sugeridas:

```
users
reports_found
reports_lost
adoptions
blacklist_people
blacklist_vets
vets_ranking
```

---

## 📂 4. Estructura del Proyecto

```
poo01_project/
│
├── main.py                     
├── README.md                  
├── assets/                     
│   ├── app_icon.ico
│   ├── logo.png
│   └── ui/
│
├── dist/                       
│   └── PatitasSeguras.exe
│
└── build/                      
```

---

## 🛠 5. Instalación del Entorno de Desarrollo

### 5.1 Crear entorno con Conda

```bash
conda create -n PatitasSeguras python=3.11
conda activate PatitasSeguras
```

### 5.2 Instalar dependencias

```bash
pip install pillow tkintermapview
conda install tk
```

---

## 🧩 6. Cómo Ejecutar el Proyecto

```bash
python main.py
```

---

## 🖼 7. Uso de Recursos (.ico, imágenes, assets)

```python
import sys, os

def resource_path(relative_path):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)
```

Ejemplo:

```python
self.iconbitmap(resource_path("assets/app_icon.ico"))
```

---

## 📦 8. Compilar a .EXE con PyInstaller

```bash
pyinstaller main.py ^
    --name PatitasSeguras ^
    --onefile ^
    --noconsole ^
    --icon assets/app_icon.ico ^
    --add-data "assets;assets" ^
    --hidden-import tkintermapview
```

---

## 🏗 9. Crear Instalador con Inno Setup

Ejemplo `.iss`:

```ini
[Setup]
AppName=Patitas Seguras
AppVersion=1.0.0
DefaultDirName={autopf}\Patitas Seguras
OutputBaseFilename=PatitasSegurasSetup

[Files]
Source: "dist\PatitasSeguras.exe"; DestDir: "{app}"

[Icons]
Name: "{autoprograms}\Patitas Seguras"; Filename: "{app}\PatitasSeguras.exe"
Name: "{autodesktop}\Patitas Seguras"; Filename: "{app}\PatitasSeguras.exe"

[Run]
Filename: "{app}\PatitasSeguras.exe"; Flags: nowait postinstall
```

---

## 🛢 10. Base de Datos (Futuro)

Uso sugerido:

```python
import sqlite3
conn = sqlite3.connect(resource_path("database.db"))
cursor = conn.cursor()
```

Tablas propuestas:

```sql
CREATE TABLE blacklist_people (...);
CREATE TABLE blacklist_vets (...);
```

---

## 🤝 11. Cómo Contribuir

1. Fork del repositorio.  
2. Crear rama nueva:

```bash
git checkout -b feature/nueva_mejora
```

3. Enviar PR.

---

## 📜 12. Licencia

MIT License (recomendada).

---

## 🧑‍💻 13. Autor

Desarrollado por **Equipo de Desarrollo POO01** — Proyecto académico y comunitario.
