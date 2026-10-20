# Auditoría del sitio ACP

Compara `frontend/` contra la guía de estilo (Identidad_Visual_ACP.docx),
los wireframes (Wireframes_ACP.docx) y el árbol DOM (Arbol_DOM_ACP.docx).

## Cómo correrla
```
pip install playwright
playwright install chromium

# 1) Home (estilos, estructura y móvil)
python audit.py  file:///C:/Proyecto%20Web/frontend/index.html captura.png resultados.json
python proto.py  file:///C:/Proyecto%20Web/frontend/index.html resultados_proto.json

# 2) Las 10 páginas (estructura, maquetación, JavaScript, móvil)
python servidor_local.py          # deja abierta esta terminal: sirve frontend/ en http://127.0.0.1:8765
python audit_paginas.py http://127.0.0.1:8765 resultados_paginas.json
```
`servidor_local.py` traduce rutas como `/login` a `login.html`; cuando Flask sirva el frontend ya no hace falta.
Cada fila del JSON trae criterio, esperado, encontrado y estado (cumple / no cumple).

Para auditar el sitio inicial: `git show 307346f:frontend/index.html` (y su css) en una carpeta aparte.

## Cambios por los wireframes (Wireframes ACP listos.zip)
Donde el ZIP y la guía de estilo difieren, el sitio sigue el ZIP y las comprobaciones se actualizaron:
- Títulos: Barlow Condensed 700; h1 56 px, h2 36 px, h3 22 px (móvil 40 / 30 / 22). Texto base 17 px (16 px en móvil).
- Botones: padding 11 × 22, borde 1 px, peso 600; el secundario es de contorno azul marino sobre blanco.
- Secciones de 72 px (48 px las chicas, 44 px en móvil); título de sección a 14 px del contenido.
- Tarjetas con borde #AEB5C2 e íconos de 36 px; campos con borde #8B93A3 (3:1 de contraste).
- Pie gris claro #F3F5F9; etiquetas blancas; pestaña activa azul marino; tarjeta de login de 440 px.
- Tecnologías: logos de 56 px y sección "Bases de datos" sin fondo gris.
Variables nuevas en :root: --color-borde-fuerte, --color-linea, --texto-m, --texto-xs, --texto-boton,
--icono-xl, --seccion, --seccion-chica, --margen-lateral, --alto-encabezado.
Los 4 "Archivo local Barlow … cargado" siguen en "no cumple" hasta copiar los .woff2 (ver assets/fonts/LEEME.md).
