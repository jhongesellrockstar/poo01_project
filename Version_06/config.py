# Configuración de la base de datos SQL Server
DATABASE_CONFIG = {
    'server': '.',  # Nombre de instancia de SQL Server Express
    'database': 'PatitasSegurasDB',  # Nombre de la base de datos
    'username': '',  # Usuario de SQL Server (dejar vacío para autenticación de Windows)
    'password': '',  # Contraseña de SQL Server (dejar vacío para autenticación de Windows)
    'driver': 'ODBC Driver 17 for SQL Server'  # Asegúrate de tener este driver instalado
}

# Configuración de SMSManager
SMSMANAGER_CONFIG = {
    'api_url': 'https://ejemplo.com/sms',      # URL de la API de SMSManager
    'api_key': 'tu_api_key',      # Clave de API de SMSManager
    'sender_id': 'PatitasSeguras'     # ID del remitente configurado en SMSManager
}