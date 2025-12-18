-- Crear la base de datos
CREATE DATABASE PatitasSegurasDB;
GO

-- Usar la base de datos recién creada
USE PatitasSegurasDB;
GO

-- Crear las tablas necesarias con relaciones

-- Tabla de adopción
CREATE TABLE adopcion (
    id INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(255),
    Tipo NVARCHAR(100),
    Raza NVARCHAR(100),
    Edad NVARCHAR(50),
    ColorHex NVARCHAR(20),
    Descripcion NVARCHAR(500),
    FotoPath NVARCHAR(500)
);
GO

-- Tabla de veterinarias
CREATE TABLE veterinarias (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(255),
    Direccion NVARCHAR(500),
    Telefono NVARCHAR(50),
    Descripcion NVARCHAR(1000),
    Servicios NVARCHAR(500),
    FotoPath NVARCHAR(500),
    Latitud FLOAT,
    Longitud FLOAT,
    PromedioEstrellas FLOAT
);
GO

-- Tabla de mascotas perdidas
CREATE TABLE mascotas_perdidas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(255),
    Tipo NVARCHAR(100),
    Raza NVARCHAR(100),
    Edad NVARCHAR(50),
    Descripcion NVARCHAR(500),
    Contacto NVARCHAR(100),
    Latitud FLOAT,
    Longitud FLOAT,
    FotoPath NVARCHAR(500),
    Estado NVARCHAR(50),
    FechaPerdido DATETIME
);
GO

-- Tabla de blacklist veterinarias (malas prácticas)
CREATE TABLE blacklist_vet (
    id INT IDENTITY(1,1) PRIMARY KEY,
    NombreVeterinaria NVARCHAR(255),
    Motivo NVARCHAR(1000),
    Latitud FLOAT,
    Longitud FLOAT,
    FechaReporte DATETIME,
    -- Clave foránea que referencia a veterinarias
    veterinaria_id INT NULL,
    CONSTRAINT FK_BlacklistVet_Veterinarias FOREIGN KEY (veterinaria_id) REFERENCES veterinarias(ID)
);
GO

-- Tabla de blacklist maltrato (casos de maltrato)
CREATE TABLE blacklist_maltrato (
    id INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(255),
    Descripcion NVARCHAR(1000),
    FotoPath NVARCHAR(500),
    Latitud FLOAT,
    Longitud FLOAT,
    FechaReporte DATETIME
);
GO

-- Tabla de votos (para calificar veterinarias)
CREATE TABLE votos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    VetID INT,
    Estrellas INT,
    Comentario NVARCHAR(1000),
    -- Clave foránea que referencia a veterinarias
    CONSTRAINT FK_Votos_Veterinarias FOREIGN KEY (VetID) REFERENCES veterinarias(ID)
);
GO

-- Agregar índices para mejorar el rendimiento
CREATE INDEX IX_BlacklistVet_VeterinariaID ON blacklist_vet(veterinaria_id);
CREATE INDEX IX_Votos_VeterinariaID ON votos(VetID);
GO