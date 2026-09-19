# ApeByte Cloud Platform (ACP)

Plataforma local de despliegue y alojamiento de aplicaciones web, desarrollada para la materia Desarrollo Web.

## Equipo
- Herrera Javier — Backend
- Gonzalez Santiago — Frontend

## Stack
- Backend: Python + Flask
- Frontend: HTML, CSS, JavaScript
- Reverse proxy: Traefik
- Contenedores: Docker + Docker Compose
- Bases de datos: PostgreSQL, MySQL/MariaDB, MongoDB (segun el proyecto desplegado)
- Entorno: red local, sin exposicion a Internet

## Estructura del repositorio
```
backend/     -> API y logica del servidor (Flask)
frontend/    -> Pagina informativa + interfaz de usuario
docker/      -> docker-compose y configuracion de Traefik
docs/        -> Documentacion del proyecto
```

## Como correr el backend (desarrollo)
```
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python run.py
```

## Cronograma (fases de 2 semanas)
1. 14-27 sept: Diseno general, repositorio, login
2. 28 sept-11 oct: Dashboard y carga de proyectos (ZIP/Git)
3. 12-25 oct: Deteccion automatica de tecnologias
4. 26 oct-8 nov: Docker y primer despliegue real
5. 9-22 nov: Bases de datos, URLs locales, reverse proxy
6. 23 nov-6 dic: Logs, monitoreo, seguridad
7. 7-10 dic: Pulido, documentacion final y entrega/demo
