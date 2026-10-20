# Backend de las páginas (solo lo necesario para el sitio)

Sirve las 10 páginas del frontend y guarda el formulario de contacto, el registro y el login.

    cd backend
    pip install -r requirements.txt
    python run.py        # http://localhost:5000

Rutas: `/`, `/caracteristicas`, `/como-funciona`, `/tecnologias`, `/documentacion`,
`/acerca-de`, `/contacto`, `/login`, `/privacidad`, `/terminos`.
API: `POST /api/contacto`, `/api/registro`, `/api/login` (JSON). Datos en `backend/acp.db` (SQLite, no se sube a git).
