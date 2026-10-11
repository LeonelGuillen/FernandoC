# fernandocastillocr.com — sitio en Cloudflare Pages

Sitio estático (HTML/CSS/JS sin framework) + una Pages Function para el formulario de contacto.

## Estructura
```
public/              ← carpeta que publica Cloudflare (output directory)
  index.html, trayectoria.html, publicaciones.html, participaciones.html, prensa.html, contacto.html, 404.html
  assets/css, assets/js, assets/img
  _headers (seguridad + caché), robots.txt, sitemap.xml, llms.txt, favicons, site.webmanifest
functions/api/contact.js   ← POST /api/contact (envía correo vía Resend)
wrangler.toml
_fuente/             ← generador (python3 build.py), datos (data.py) y SEO (seo.py)
```

## Publicar
**Opción A – Git (recomendada):** subir esta carpeta a un repo de GitHub → Cloudflare → Workers & Pages → Create → Pages → Connect to Git.
Build command: *(vacío)* · Output directory: `public`.

**Opción B – Wrangler:** `npx wrangler pages deploy public --project-name fernandocastillocr`

## Formulario de contacto
En Pages → Settings → Variables and Secrets:
- `RESEND_API_KEY` (secreto), `CONTACT_TO` (correo destino), `CONTACT_FROM` (remitente verificado en Resend, ej. `Sitio web <web@fernandocastillocr.com>`)
- Opcional `TURNSTILE_SECRET` + agregar el widget Turnstile al formulario.
Sin estas variables el formulario responde "aún no está configurado" (no falla).

## Dominio (salir de Wix)
1. Agregar el dominio en Cloudflare y en Pages → Custom domains agregar `www.fernandocastillocr.com` y `fernandocastillocr.com`.
2. Regla de redirección 301: `fernandocastillocr.com/*` → `https://www.fernandocastillocr.com/$1` (el canónico es www).
3. Las URLs antiguas de Wix (/trayectoria, /publicaciones, /participaciones, /contacto) se mantienen iguales.
4. Cancelar el plan Wix solo después de verificar el sitio en el dominio.

## Editar contenido
- SEO (títulos, descripciones, keywords, schema.org): `_fuente/seo.py`
- Libros, prensa, entrevista: `_fuente/data.py`; trayectoria/participaciones: `_fuente/lines.json`
- Luego `python3 build.py` y copiar `out/public` a `public/`.

## Pendientes
- Verificación de Google Search Console (meta en `<head>` o por DNS) y envío de `/sitemap.xml`.
- URL exacta de la entrevista de La Nación (“Podemos caer en un Estado fallido”) → `INTERVIEW["u"]` en data.py.
- Año y ficha de *Hacia un populismo constitucional* (Querétaro).
- Fechas de publicación de los 2 videos → `VIDEO_DATES` en seo.py (activa el schema VideoObject).
- Fotos de la galería de Wix (14 imágenes) → `assets/img/` para una sección de galería.
- Perfiles oficiales para `sameAs` (Wikidata, LinkedIn, página institucional).
