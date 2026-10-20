# Fuentes del sitio (faltan los archivos)

La red local no tiene Internet, así que las fuentes se cargan desde esta carpeta.
`css/style.css` ya tiene los `@font-face`; solo faltan estos archivos `.woff2`:

| Archivo                       | Familia          | Peso | Dónde se usa                         |
|-------------------------------|------------------|------|--------------------------------------|
| `barlow-400.woff2`            | Barlow           | 400  | texto normal                         |
| `barlow-500.woff2`            | Barlow           | 500  | menú, etiquetas, etiquetas de campos |
| `barlow-600.woff2`            | Barlow           | 600  | botones, pestañas                    |
| `barlow-700.woff2`            | Barlow           | 700  | negritas                             |
| `barlow-condensed-700.woff2`  | Barlow Condensed | 700  | h1, h2, h3, números de los pasos     |

Cómo conseguirlos (con Internet, una sola vez):
- Descargar "Barlow" y "Barlow Condensed" de Google Fonts (licencia OFL) y convertir los .ttf a .woff2, o
- `npm i @fontsource/barlow @fontsource/barlow-condensed` y copiar de `node_modules/@fontsource/*/files/`
  los archivos `*-latin-<peso>-normal.woff2` con los nombres de la tabla.

Mientras no estén, el sitio usa Arial / Arial Narrow como respaldo.
