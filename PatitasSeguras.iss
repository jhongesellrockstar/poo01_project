; --- CONFIGURACIÓN BÁSICA DEL INSTALADOR ---
[Setup]
AppName=Patitas Seguras
AppVersion=1.0.0
DefaultDirName={autopf}\Patitas Seguras
DefaultGroupName=Patitas Seguras
OutputBaseFilename=PatitasSegurasSetup
Compression=lzma
SolidCompression=yes
DisableDirPage=no
DisableProgramGroupPage=no

; Si tienes un icono .ico propio, descomenta y ajusta la ruta:
; SetupIconFile=C:\Users\jhonv\Documents\GitHub2025\poo01_project\assets\logo.ico

; --- ARCHIVOS A INSTALAR ---
[Files]
Source: "C:\Users\jhonv\Documents\GitHub2025\poo01_project\dist\PatitasSeguras.exe"; \
    DestDir: "{app}"; Flags: ignoreversion

; --- TAREAS OPCIONALES (ICONO EN ESCRITORIO) ---
[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; \
    GroupDescription: "Tareas adicionales:"; Flags: unchecked

; --- ACCESOS DIRECTOS ---
[Icons]
; Menú Inicio
Name: "{autoprograms}\Patitas Seguras"; Filename: "{app}\PatitasSeguras.exe"

; Escritorio (opcional, ligado a la tarea anterior)
Name: "{autodesktop}\Patitas Seguras"; Filename: "{app}\PatitasSeguras.exe"; \
    Tasks: desktopicon

; --- OPCIONAL: EJECUTAR AL FINAL ---
[Run]
Filename: "{app}\PatitasSeguras.exe"; Description: "Ejecutar Patitas Seguras"; \
    Flags: nowait postinstall skipifsilent
