# Formulario de Registro - Backend

Este proyecto es una API REST de backend desarrollada con tecnologías modernas de Python. Proporciona endpoints seguros para el registro y gestión de usuarios con validación robusta y encriptación de contraseñas.

## Tecnologías Utilizadas

### Backend
- **Flask**: Framework web ligero y flexible de Python para crear APIs REST.
- **Flask-CORS**: Extensión para manejar Cross-Origin Resource Sharing, permitiendo conexiones desde el frontend.

### Base de Datos
- **SQLAlchemy**: ORM (Object-Relational Mapping) para Python que facilita la interacción con bases de datos.
- **PostgreSQL**: Sistema de gestión de base de datos relacional robusto y escalable.
- **psycopg2**: Adaptador de PostgreSQL para Python.

### Seguridad
- **Passlib**: Biblioteca para el hash seguro de contraseñas usando bcrypt.
- **bcrypt**: Algoritmo de hashing adaptativo para contraseñas, resistente a ataques de fuerza bruta.

### Desarrollo
- **Ruff**: Linter y formateador de código Python extremadamente rápido para mantener código limpio y consistente.

## Características Implementadas

- **Registro de Usuarios**: Endpoint POST `/usuarios` para crear nuevos usuarios con validación completa.
- **Listado de Usuarios**: Endpoint GET `/usuarios` para obtener todos los usuarios registrados.
- **Validación de Datos**: Validación de email con expresiones regulares y verificación de fortaleza de contraseña.
- **Encriptación de Contraseñas**: Hash seguro de contraseñas usando bcrypt antes del almacenamiento.
- **Prevención de Duplicados**: Verificación de emails únicos para evitar registros duplicados.
- **Manejo de Errores**: Respuestas HTTP apropiadas con mensajes de error descriptivos.
- **CORS Configurado**: Permite conexiones desde el frontend en localhost:3000.

## Estructura del Proyecto

- **app.py**: Archivo principal con la configuración de Flask, modelos de datos y endpoints de la API.
- **pyproject.toml**: Configuración de herramientas de desarrollo como Ruff para linting.

## Modelo de Datos

### Usuario
- **id**: Identificador único auto-incremental
- **nombre**: Nombre del usuario 
- **correo**: Email único con índice para búsquedas rápidas
- **contrasena_hash**: Contraseña encriptada con bcrypt

## Variables de Entorno

- **URL_BD**: URL de conexión a PostgreSQL (por defecto: `postgresql+psycopg2://dev:devpass@localhost:5432/bd_registro`)

## Endpoints de la API

### POST /usuarios
Crea un nuevo usuario con validación completa.

