-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS inventario_oficina;

-- Seleccionar la base de datos
USE inventario_oficina;

-- Crear tabla de Departamentos
CREATE TABLE IF NOT EXISTS departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_D VARCHAR(100) NOT NULL
);

-- Crear tabla de Categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_C VARCHAR(100) NOT NULL
);

-- Crear tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_U VARCHAR(100) NOT NULL,
    cedula_U VARCHAR(50) NOT NULL UNIQUE,
    departamento_id INT,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id) ON DELETE SET NULL
);

-- Crear tabla de Equipos
CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_E VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    serial VARCHAR(100) NOT NULL UNIQUE,
    especificaciones TEXT,
    usuario_id INT,
    categoria_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- Crear tabla de Motivos
CREATE TABLE IF NOT EXISTS motivos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_M VARCHAR(100) NOT NULL
);

show create table equipos;

alter table equipos DROP index serial;

