# -*- coding: utf-8 -*-
"""Genera el sitio estático en ./out/public  (python3 build.py)"""
import json, re, os, shutil, html
from datetime import date
from data import SITE, BOOKS, NEWS, INTERVIEW, fix, RECOG_PERSONAL, RECOG_SALA, INDICATORS
import seo

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
PUB = os.path.join(OUT, "public")
L = json.load(open(os.path.join(ROOT, "lines.json"), encoding="utf-8"))
e = lambda s: html.escape(s, quote=True)

# ---------- parsing ----------
YR = re.compile(r"^(\d{4}(?:\s*(?:-|–|al|y|a)\s*(?:\d{4}|la fecha))?)\s*(?:a la fecha)?[\s.\-–]*(.*)$")

def split_year(line):
    m = YR.match(line)
    if not m:
        return None, line
    y = re.sub(r"\s*-\s*", "–", m.group(1)).replace(" al ", "–").replace(" y ", "–")
    rest = m.group(2).strip(" .-–")
    if line[m.end(1):].strip().startswith("a la fecha"):
        y += "–hoy"
    y = y.replace("a la fecha", "hoy")
    return y, rest[0].upper() + rest[1:] if rest else rest

def parse(lines):
    out, last = [], None
    for ln in lines:
        y, t = split_year(fix(ln))
        if y is None:
            y = last
        last = y
        out.append(dict(y=y, t=t))
    return out

T, P, PB = L["trayectoria"], L["participaciones"], L["publicaciones"]
estudios = parse(T[8:12])
cargos = parse(T[13:50])
ponencias_raw = parse(P[1:85]) + parse(T[50:79])
asistencia = parse(P[86:106])
articulos_raw = PB[12:43]
investigaciones = parse(PB[44:46])

seen, ponencias = set(), []
for it in ponencias_raw:
    k = re.sub(r"\W", "", it["t"].lower())[:70]
    if k in seen:
        continue
    seen.add(k); ponencias.append(it)

def first_year(y):
    m = re.search(r"\d{4}", y or ""); return m.group(0) if m else "—"

INTL = ["Guatemala", "Puerto Rico", "Argentina", "Salvador", "Washington", "Chile", "Dominicana", "México", "Brasil",
        "Perú", "Lima", "Pittsburgh", "Londres", "Barcelona", "Catalunya", "Buenos Aires", "Santo Domingo", "Viña del Mar"]
def is_intl(t): return any(c in t for c in INTL)

def p_type(t):
    tl = t.lower()
    if re.match(r"(miembro|asesor|colaborador|especialista|coordinador)", tl): return "cargo"
    if re.match(r"(moderador|comentarista|relator|presenta )", tl): return "moderacion"
    if any(w in tl for w in ["mesa redonda", "panel", "conversatorio", "debate", "panelista"]): return "panel"
    return "conferencia"
P_LABEL = {"conferencia": "Conferencia / ponencia", "panel": "Mesa redonda / panel", "moderacion": "Moderación / comentario", "cargo": "Comisión / cargo"}

def article(line):
    s = fix(line)
    kind = "ponencia" if s.startswith("Conferencista") else "articulo"
    yrs = [int(x) for x in re.findall(r"(?<!\d)(19[89]\d|20[0-2]\d)(?!\d)", s)]
    y = str(min(yrs)) if yrs else "—"
    s2 = re.sub(r"^(Artículo (sobre|denominado|titulado)|Conferencista sobre)\s+", "", s)
    m = re.split(r"\.\s+(?=En\s|Jornadas|XV Jornadas|Código Procesal|Revista)|,\s+(?=En\s)", s2, maxsplit=1)
    title, src = (m[0], m[1]) if len(m) == 2 else (s2, "")
    title = title.strip(" .")
    title = title[0].upper() + title[1:]
    return dict(y=y, t=title, s=src.strip(), k=kind)
articulos = [article(a) for a in articulos_raw]

# ---------- layout ----------
NAV = [("index.html", "Inicio"), ("trayectoria.html", "Trayectoria"), ("publicaciones.html", "Publicaciones"),
       ("participaciones.html", "Participaciones"), ("prensa.html", "Prensa")]
ICON = {
 "gavel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M14 4l6 6M12 6l6 6M5 21h9M9.5 8.5l6 6M4 13l7-7 3 3-7 7z"/></svg>',
 "cap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5M22 9v6"/></svg>',
 "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2zM4 5v16M8 7h7"/></svg>',
 "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>',
 "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
}

PERSON_LD = {
  "@context": "https://schema.org", "@type": "Person", "name": "Fernando Castillo Víquez",
  "jobTitle": "Presidente de la Sala Constitucional de la Corte Suprema de Justicia de Costa Rica",
  "worksFor": {"@type": "GovernmentOrganization", "name": "Sala Constitucional, Poder Judicial de Costa Rica", "url": "https://salaconstitucional.poder-judicial.go.cr/"},
  "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Universidad de Costa Rica"}, {"@type": "CollegeOrUniversity", "name": "Universidad Escuela Libre de Derecho"}],
  "birthPlace": "Heredia, Costa Rica", "url": SITE, "image": SITE + "/assets/img/retrato.webp",
  "knowsAbout": ["Derecho Constitucional", "Derecho Procesal Constitucional", "Derecho Parlamentario", "Derecho Público Económico", "Derecho Administrativo"],
}

def page(fname, title, desc, body, ld=None):
    cur = fname
    menu = "".join(f'<li><a href="/{h if h!="index.html" else ""}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a></li>' for h, n in NAV)
    menu += f'<li><a class="cta" href="/contacto.html"{" aria-current=\"page\"" if cur=="contacto.html" else ""}>Contacto</a></li>'
    S = seo.PAGES[fname]
    title, desc = S["title"], S["desc"]
    canon = seo.url(fname)
    ldj = f'<script type="application/ld+json">{json.dumps(seo.graph(fname), ensure_ascii=False)}</script>'
    robots = "noindex, follow" if S.get("noindex") else "index, follow, max-image-preview:large, max-snippet:-1"
    preload = '<link rel="preload" as="image" href="/assets/img/retrato.webp" fetchpriority="high">' if fname == "index.html" else ""
    return f'''<!doctype html>
<html lang="es-CR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(", ".join(S["kw"]))}">
<meta name="author" content="Fernando Castillo Víquez">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="es-CR" href="{canon}"><link rel="alternate" hreflang="x-default" href="{canon}">
<!-- Google Search Console: pegar aquí la meta de verificación, p. ej. <meta name="google-site-verification" content="..."> -->
<meta property="og:type" content="{"profile" if S["type"]=="ProfilePage" else "website"}"><meta property="og:locale" content="es_CR"><meta property="og:site_name" content="Fernando Castillo Víquez">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(S["ogalt"])}">
{'<meta property="profile:first_name" content="Fernando"><meta property="profile:last_name" content="Castillo Víquez">' if S["type"]=="ProfilePage" else ""}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og-image.jpg"><meta name="twitter:image:alt" content="{e(S["ogalt"])}">
<meta name="theme-color" content="#0e1a2b"><meta name="format-detection" content="telephone=no">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
{preload}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css?v={VER}">
{ldj}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="site-header">
  <nav class="wrap nav" aria-label="Principal">
    <a class="brand" href="/" aria-label="Fernando Castillo Víquez — inicio">
      <span class="brand-mark">FC</span>
      <span class="brand-name">Fernando Castillo Víquez<small>Sala Constitucional · Costa Rica</small></span>
    </a>
    <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    <ul class="menu" id="menu">{menu}</ul>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>Fernando Castillo Víquez</h4>
        <p>Presidente de la Sala Constitucional de la Corte Suprema de Justicia de Costa Rica. Doctor en Derecho, catedrático y conferencista.</p>
        <p style="font-size:.82rem">Sitio personal de carácter académico e informativo. Las resoluciones oficiales se consultan en el sitio de la <a href="https://salaconstitucional.poder-judicial.go.cr/" rel="noopener">Sala Constitucional</a> y en <a href="https://nexuspj.poder-judicial.go.cr/" rel="noopener">Nexus PJ</a>.</p>
      </div>
      <div><h4>Secciones</h4><ul>{"".join(f'<li><a href="/{h if h!="index.html" else ""}">{n}</a></li>' for h,n in NAV)}<li><a href="/contacto.html">Contacto</a></li></ul></div>
      <div><h4>Enlaces institucionales</h4><ul>
        <li><a href="https://salaconstitucional.poder-judicial.go.cr/" rel="noopener">Sala Constitucional</a></li>
        <li><a href="https://pj.poder-judicial.go.cr/" rel="noopener">Poder Judicial de Costa Rica</a></li>
        <li><a href="https://nexuspj.poder-judicial.go.cr/" rel="noopener">Jurisprudencia — Nexus PJ</a></li>
        <li><a href="https://www.uescuelalibre.cr/" rel="noopener">Universidad Escuela Libre de Derecho</a></li>
      </ul></div>
    </div>
    <div class="foot-bottom"><span>© <span id="yr">{date.today().year}</span> Fernando Castillo Víquez. Todos los derechos reservados.</span><span>Diseño y desarrollo: <a href="https://leoguillen.com" rel="noopener">Leo Guillén</a></span></div>
  </div>
</footer>
<script src="/assets/js/main.js?v={VER}" defer></script>
</body>
</html>'''

VER = date.today().strftime("%Y%m%d")

def hero(eyebrow, title, sub, crumb):
    return f'''<section class="page-hero"><div class="wrap">
<div class="crumbs"><a href="/">Inicio</a> / {crumb}</div>
<div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{sub}</p></div></section>'''

def news_card(n, featured=False):
    ext = not n['u'].startswith('/')
    tgt = ' target="_blank" rel="noopener"' if ext else ''
    go = f"Leer en {e(n['src'])} ↗" if ext else "Leer el análisis →"
    return f'''<a class="news reveal{' featured' if featured else ''}" href="{e(n['u'])}"{tgt}>
<div class="meta"><span>{e(n['src'])}</span><i></i><span>{e(n['kind'])}</span><i></i><span>{e(n['dl'])}</span></div>
<h3>{e(n['t'])}</h3><p>{e(n['s'])}</p><span class="go">{go}</span></a>'''

def book_card(b):
    cover = (f'<div class="cover"><img src="/assets/img/{b["img"]}" alt="Portada: {e(b["t"])}" loading="lazy"></div>' if b.get("img")
             else f'<div class="cover gen"><small>Fernando Castillo Víquez</small><b>{e(b["t"])}</b><small>{e(b["pub"].split("(")[0].strip())}</small></div>')
    yr = b["y"] or "s. f."
    link = f'<a href="{b["buy"]}" target="_blank" rel="noopener">Dónde adquirirlo ↗</a>' if b.get("buy") else ""
    return f'<article class="book reveal">{cover}<div><h3>{e(b["t"])}</h3><p>{e(b["role"])} · {e(b["pub"])} · {yr}</p></div>{link}</article>'

# ---------- pages ----------
def build_index():
    profiles = [
        ("gavel", "Magistrado", "Integra la Sala Constitucional desde 2009 y la preside. Reelecto por la Asamblea Legislativa en 2025 para un nuevo período de ocho años.", "trayectoria.html", "Ver trayectoria"),
        ("cap", "Académico", "Catedrático desde 1985. Profesor de doctorado y maestría en la Escuela Libre de Derecho, la UNED y la Universidad de Costa Rica.", "trayectoria.html#docencia", "Docencia"),
        ("book", "Autor", "Once libros como autor y coautor y más de treinta artículos en revistas especializadas de Derecho Público.", "publicaciones.html", "Ver publicaciones"),
        ("globe", "Conferencista internacional", "Ponente en foros de Costa Rica, Latinoamérica, Estados Unidos y Europa sobre justicia constitucional y derechos fundamentales.", "participaciones.html", "Ver participaciones"),
    ]
    themes = [
        ("Justicia constitucional", "Control de constitucionalidad, amparo, hábeas corpus y el funcionamiento de la Sala."),
        ("Derecho parlamentario", "Procedimiento legislativo, nulidades parlamentarias y relación entre partidos y Parlamento."),
        ("Derecho a la salud", "Judicialización de la salud, listas de espera y su evolución en la jurisprudencia."),
        ("Derecho público económico", "Constitución económica, libertad de comercio, empresa pública y presupuesto."),
        ("Independencia judicial", "Separación de poderes, frenos y contrapesos y el acatamiento de las sentencias."),
        ("Control de convencionalidad", "Diálogo entre la jurisdicción constitucional y el Sistema Interamericano."),
    ]
    feat = [b for b in BOOKS if b.get("feat")][:4]
    body = f'''
<section class="hero"><div class="wrap hero-grid">
  <div>
    <div class="eyebrow">Corte Suprema de Justicia · Costa Rica</div>
    <h1>Fernando <em>Castillo</em> Víquez</h1>
    <p class="lead">Presidente de la Sala Constitucional. Doctor en Derecho, catedrático universitario y autor de obras de referencia en Derecho Constitucional y Parlamentario.</p>
    <ul class="roles"><li>Magistrado Sala Constitucional</li><li>Doctor en Derecho Constitucional</li><li>Notario Público</li><li>Profesor universitario</li><li>Conferencista internacional</li></ul>
    <div class="btns"><a class="btn btn-gold" href="/trayectoria.html">Conocer su trayectoria</a><a class="btn btn-ghost" href="/publicaciones.html">Publicaciones</a></div>
  </div>
  <figure class="portrait"><img src="/assets/img/retrato.webp" alt="Retrato del magistrado Fernando Castillo Víquez" width="496" height="568" fetchpriority="high">
  <figcaption><b>Desde 2009</b>Magistrado propietario de la Sala Constitucional</figcaption></figure>
</div></section>

<section class="stats"><div class="wrap stats-grid">
  <div class="stat"><b>2009</b><span>Magistrado de la Sala IV</span></div>
  <div class="stat"><b>40+</b><span>años de docencia universitaria</span></div>
  <div class="stat"><b>11</b><span>libros como autor y coautor</span></div>
  <div class="stat"><b>30+</b><span>artículos especializados</span></div>
  <div class="stat"><b>{len(ponencias)}+</b><span>conferencias y foros</span></div>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head"><div><div class="eyebrow">Perfiles</div><h2>Una trayectoria, cuatro dimensiones</h2></div>
  <p class="lead">Servicio público, academia, investigación y diálogo internacional.</p></div>
  <div class="grid-4">{"".join(f'<article class="profile reveal"><div class="ic">{ICON[i]}</div><h3>{t}</h3><p>{d}</p><a href="/{h}">{l}</a></article>' for i,t,d,h,l in profiles)}</div>
</div></section>

<section class="block alt"><div class="wrap grid-2">
  <div class="bio-img reveal"><img src="/assets/img/conferencia.webp" alt="Fernando Castillo Víquez durante una intervención" loading="lazy" width="1067" height="1600"><span class="tag">Procurador Constitucional 1999–2009</span></div>
  <div class="reveal">
    <div class="eyebrow">En síntesis</div>
    <h2>Del Parlamento a la Sala Constitucional</h2>
    <p>Licenciado en Derecho y Notario Público por la Universidad de Costa Rica y Doctor en Derecho por la Universidad Escuela Libre de Derecho.</p>
    <p>Fue asesor del Directorio y de los presidentes de la Asamblea Legislativa, Letrado Mayor de ese órgano, asesor-coordinador del Área Jurídica de la Primera Vicepresidencia y asesor del Ministro de la Presidencia. Entre 1999 y 2009 se desempeñó como Procurador Constitucional.</p>
    <p>Desde 2009 es magistrado propietario de la Sala Constitucional, que actualmente preside. Combina la función jurisdiccional con la docencia de grado y posgrado.</p>
    <blockquote class="quote">“El costarricense no se vería en una Costa Rica sin la Sala Constitucional.”<cite>— Entrevista con La Nación, 35.º aniversario de la Sala IV</cite></blockquote>
    <a class="btn btn-ink" href="/trayectoria.html">Trayectoria completa</a>
  </div>
</div></section>

<section class="block dark"><div class="wrap">
  <div class="sec-head"><div><div class="eyebrow" style="color:var(--gold-2)">Ejes de su obra</div><h2>Temas de investigación y docencia</h2></div></div>
  <div class="themes">{"".join(f'<div class="theme reveal"><span class="n">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(themes))}</div>
</div></section>

{recog_block(True)}
<section class="block alt"><div class="wrap">
  <div class="sec-head"><div><div class="eyebrow">Actualidad</div><h2>En los medios</h2></div><a class="btn btn-ink" href="/prensa.html">Toda la prensa</a></div>
  <div class="grid-3">{news_card(NEWS[0], True)}{news_card(NEWS[1])}{news_card(NEWS[4])}</div>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head"><div><div class="eyebrow">Obras</div><h2>Libros destacados</h2></div><a class="btn btn-ink" href="/publicaciones.html">Ver todas</a></div>
  <div class="grid-4">{"".join(book_card(b) for b in feat)}</div>
</div></section>

<section class="block alt"><div class="wrap"><div class="cta-band reveal">
  <div><h2>Conferencias, academia y prensa</h2><p>Invitaciones a foros, actividades académicas y solicitudes de medios.</p></div>
  <a class="btn btn-gold" href="/contacto.html">Escribir un mensaje</a>
</div></div></section>'''
    return page("index.html", "Fernando Castillo Víquez | Presidente de la Sala Constitucional de Costa Rica",
                "Sitio oficial de Fernando Castillo Víquez, presidente de la Sala Constitucional de Costa Rica: trayectoria, publicaciones, conferencias y prensa.", body)

def tl(items, hl_words=()):
    out = []
    for it in items:
        hl = any(w in it["t"] for w in hl_words)
        out.append(f'<li class="{"hl" if hl else ""}"><span class="yr">{e(it["y"] or "")}</span><span class="tx">{e(it["t"])}</span></li>')
    return '<ol class="timeline">' + "".join(out) + "</ol>"

def build_trayectoria():
    doc = [c for c in cargos if re.search(r"Profesor|Catedrático|Instructor|Maestrescuela|Comisión de Evaluación", c["t"])]
    pub = [c for c in cargos if c not in doc] + [
        dict(y="2018", t="Presidente interino de la Sala Constitucional."),
        dict(y="2020–hoy", t="Presidente de la Sala Constitucional, electo por el pleno de magistrados."),
        dict(y="2025", t="Reelegido por la Asamblea Legislativa como magistrado propietario por un nuevo período de ocho años (juramentado el 17 de noviembre)."),
        dict(y="2024", t="Reconocimiento por su trayectoria académica y labor docente, Poder Judicial del Estado de Oaxaca y Academia Mexicana de Derecho (México).")]
    pub.sort(key=lambda c: first_year(c["y"]))
    body = hero("Trayectoria de vida", "Cuatro décadas de servicio público y academia",
                "Formación, cargos en la Asamblea Legislativa, el Poder Ejecutivo y la Procuraduría General de la República, y su llegada a la Sala Constitucional.", "Trayectoria")
    body += f'''<section class="block"><div class="wrap side-layout">
<aside><div class="facts"><dl>
<div><dt>Nombre</dt><dd>Fernando Castillo Víquez</dd></div>
<div><dt>Nacimiento</dt><dd>Heredia, Costa Rica, 1959</dd></div>
<div><dt>Profesión</dt><dd>Doctor en Derecho y Notario Público</dd></div>
<div><dt>Cargo actual</dt><dd>Presidente de la Sala Constitucional desde mayo de 2020 (interino desde agosto de 2018)</dd></div>
<div><dt>Magistrado desde</dt><dd>16 de noviembre de 2009 · reelecto en 2017 y 2025</dd></div>
<div><dt>Distinción</dt><dd>Reconocimiento a su trayectoria académica, Poder Judicial de Oaxaca, 2024</dd></div>
</dl></div>
<p style="margin-top:16px"><button class="btn btn-ink" type="button" data-print>Imprimir / PDF</button></p></aside>
<div>
<div class="eyebrow">A · Estudios realizados</div><h2>Formación</h2>{tl(estudios, ["Doctorado"])}
<div class="eyebrow" style="margin-top:56px">B · Cargos desempeñados</div><h2>Servicio público</h2>
{tl(pub, ["Magistrado", "Procurador Constitucional", "Letrado Mayor", "Presidente de la Sala", "Reelegido", "Reconocimiento"])}
<div class="eyebrow" style="margin-top:56px" id="docencia">C · Docencia</div><h2>Cátedra universitaria</h2>
{tl(doc, ["Catedrático"])}
<div class="eyebrow" style="margin-top:56px">D · Investigación</div><h2>Investigaciones y tareas afines</h2>{tl(investigaciones)}
</div></div></section>'''
    return page("trayectoria.html", "Trayectoria | Fernando Castillo Víquez",
                "Formación académica, cargos públicos y docencia de Fernando Castillo Víquez, magistrado presidente de la Sala Constitucional de Costa Rica.", body)

def chips(opts, total):
    h = f'<button class="chip" data-f="all" aria-pressed="true">Todas <span class="c">{total}</span></button>'
    for k, (lab, n) in opts.items():
        h += f'<button class="chip" data-f="{k}" aria-pressed="false">{lab} <span class="c">{n}</span></button>'
    return h

def toolbar(opts, total, ph):
    return f'''<div class="toolbar"><div class="chips" role="group" aria-label="Filtrar">{chips(opts,total)}</div>
<div class="search">{ICON["search"]}<input id="q" type="search" placeholder="{ph}" aria-label="Buscar"></div></div>
<p class="count" id="count"></p>'''

def build_publicaciones():
    arts = sorted(articulos, key=lambda a: a["y"], reverse=True)
    items = ""
    for a in arts:
        items += f'''<article class="item" data-type="{a["k"]}" data-year="{a["y"]}"><div class="y">{a["y"]}</div><div>
<div class="t">{e(a["t"])}</div><div class="s">{e(a["s"])}</div>
<div class="badges"><span class="badge">{"Artículo" if a["k"]=="articulo" else "Ponencia publicada"}</span></div></div></article>'''
    n_a = sum(1 for a in arts if a["k"] == "articulo"); n_p = len(arts) - n_a
    body = hero("Publicaciones y aportes", "Obra escrita",
                "Libros, artículos en revistas especializadas y ponencias publicadas en Derecho Constitucional, Parlamentario y Administrativo.", "Publicaciones")
    body += f'''<section class="block"><div class="wrap">
<div class="sec-head"><div><div class="eyebrow">Libros</div><h2>Libros y obras colectivas</h2></div></div>
<div class="grid-4">{"".join(book_card(b) for b in BOOKS)}</div>
</div></section>
<section class="block alt" style="padding-top:72px"><div class="wrap">
<div class="eyebrow">Artículos</div><h2>Artículos y ponencias publicadas</h2>
{toolbar({"articulo": ("Artículos", n_a), "ponencia": ("Ponencias", n_p)}, len(arts), "Buscar por tema, revista o año…").replace("background:var(--paper)", "")}
<div class="items" data-filter-list>{items}</div><p class="empty" id="empty" hidden>No hay resultados para esa búsqueda.</p>
</div></section>'''
    return page("publicaciones.html", "Publicaciones | Fernando Castillo Víquez",
                "Libros, artículos y ponencias de Fernando Castillo Víquez sobre justicia constitucional, derecho parlamentario y derecho público.", body)

def build_participaciones():
    rows = []
    for it in ponencias:
        rows.append(dict(y=first_year(it["y"]), yl=it["y"], t=it["t"], k=p_type(it["t"]), i=is_intl(it["t"]), g="p"))
    for it in asistencia:
        rows.append(dict(y=first_year(it["y"]), yl=it["y"], t=it["t"], k="formacion", i=is_intl(it["t"]), g="a"))
    rows.sort(key=lambda r: r["y"], reverse=True)
    counts = {}
    for r in rows:
        counts[r["k"]] = counts.get(r["k"], 0) + 1
    n_i = sum(1 for r in rows if r["i"])
    opts = {k: (P_LABEL.get(k, "Seminarios y cursos"), counts[k]) for k in ["conferencia", "panel", "moderacion", "cargo", "formacion"] if k in counts}
    opts["intl"] = ("Internacional", n_i)
    html_items, cy = "", None
    for r in rows:
        if r["y"] != cy:
            cy = r["y"]; html_items += f'<h3 class="year-head" data-year-head="{cy}">{cy}</h3>'
        types = r["k"] + (" intl" if r["i"] else "")
        badges = f'<span class="badge">{P_LABEL.get(r["k"], "Seminario / curso")}</span>' + ('<span class="badge intl">Internacional</span>' if r["i"] else "")
        html_items += f'<article class="item" data-type="{types}" data-year="{r["y"]}"><div class="y">{e(r["yl"] or "")}</div><div><div class="s" style="color:var(--text);font-size:.96rem">{e(r["t"])}</div><div class="badges">{badges}</div></div></article>'
    body = hero("Participaciones", "Conferencias, foros y comisiones",
                f"{len(ponencias)} ponencias, mesas redondas y encargos técnicos en Costa Rica y el exterior, además de su formación continua.", "Participaciones")
    body += f'''<section class="block" style="padding-top:40px"><div class="wrap">
<h2 style="font-size:1.6rem;margin-bottom:6px">Registro cronológico de participaciones</h2>
{toolbar(opts, len(rows), "Buscar por tema, ciudad o institución…")}
<div class="items" data-filter-list>{html_items}</div><p class="empty" id="empty" hidden>No hay resultados para esa búsqueda.</p>
</div></section>'''
    return page("participaciones.html", "Participaciones y conferencias | Fernando Castillo Víquez",
                "Conferencias, mesas redondas, paneles internacionales y comisiones en las que ha participado Fernando Castillo Víquez.", body)

def build_prensa():
    iv = INTERVIEW
    kps = [
        ("35 000", "La carga de trabajo", "Señala como mayor reto de la Sala racionalizar su circulante, que se acercaba a 35 000 asuntos por año con un equipo sin crecimiento desde 2017."),
        ("90 %", "Amparos y salud", "Nueve de cada diez asuntos son recursos de amparo; buena parte se relaciona con listas de espera y acceso a medicamentos en la CCSS."),
        ("2", "Propuestas de reforma", "Crear tribunales constitucionales de primera instancia para los amparos, o dividir la Sala en dos secciones; también plantea discutir su independencia del Poder Judicial."),
        ("Art. 9", "División de poderes", "Recuerda que la separación de poderes y los frenos y contrapesos son la base del sistema republicano costarricense."),
        ("Gini", "Inseguridad y desigualdad", "Identifica la inseguridad ciudadana como uno de los problemas centrales del país y atribuye su causa de fondo a la desigualdad social."),
        ("1949", "Solidez democrática", "Valora que la Constitución de 1949 creó un diseño institucional que dificulta el desmontaje de los órganos de control."),
    ]
    body = hero("Prensa y actualidad", "En los medios",
                "Entrevistas, perfiles y noticias sobre su labor al frente de la Sala Constitucional. Cada nota enlaza a la publicación original.", "Prensa")
    body += f'''<section class="block"><div class="wrap">
<div class="eyebrow">Entrevista destacada</div>
<div class="grid-2" style="align-items:start;gap:44px">
<div class="reveal">
<h2>{e(iv["t"])}</h2>
<p class="count" style="margin-bottom:18px">{e(iv["src"])} · {e(iv["author"])} · {e(iv["when"])}</p>
<p>Con motivo de los 35 años de la Sala Constitucional, el magistrado presidente analizó la coyuntura nacional, la solidez de la democracia costarricense y la salud del tribunal. Sostuvo que la Sala goza de legitimidad social y que, aunque sus decisiones no siempre son bien recibidas, los casos de desobediencia son poco frecuentes.</p>
<blockquote class="quote">“El costarricense no se vería en una Costa Rica sin la Sala Constitucional.”<cite>— Fernando Castillo Víquez</cite></blockquote>
<p>También se refirió al carácter contramayoritario de los tribunales constitucionales, a la evolución de la jurisprudencia en temas como el matrimonio igualitario y la fecundación in vitro —“más que errores, visiones diferentes”, en sus palabras— y a su libro <em>Hacia un populismo constitucional</em>.</p>
<a class="btn btn-ink" href="{e(iv["u"])}" target="_blank" rel="noopener">Leer la entrevista completa en {e(iv["src"])} ↗</a>
</div>
<div class="interview">{"".join(f'<div class="kp reveal"><span class="fig">{f}</span><h3>{t}</h3><p>{d}</p></div>' for f,t,d in kps)}</div>
</div>
<p class="note">Resumen editorial elaborado a partir de la entrevista publicada por {e(iv["src"])}. El texto íntegro y sus derechos pertenecen al medio.</p>
</div></section>
<section class="block alt"><div class="wrap">
<div class="sec-head"><div><div class="eyebrow">Cobertura</div><h2>Notas recientes</h2></div></div>
<div class="grid-3">{"".join(news_card(n, i==0) for i,n in enumerate(NEWS))}</div>
<p class="note">¿Es periodista? Las solicitudes de entrevista pueden enviarse desde la página de <a href="/contacto.html">contacto</a>.</p>
</div></section>''' + indicators_block() + recog_block() + videos_block()
    return page("prensa.html", "Prensa y actualidad | Fernando Castillo Víquez",
                "Entrevistas, perfiles y noticias sobre Fernando Castillo Víquez, presidente de la Sala Constitucional de Costa Rica.", body)

VIDEOS = [("E4O-0gI2j0o","Juramentación para un nuevo período en la Sala Constitucional","Extra TV · noviembre de 2025. Presta juramento ante la Asamblea Legislativa para un nuevo período de ocho años como magistrado."),
          ("5sLBl72rUVM","“La Sala charla” con el magistrado Fernando Castillo Víquez","Escuela Judicial Electoral del Tribunal Electoral del Poder Judicial de la Federación (México) · 24 de junio de 2022."),
          ("8_P4O4-GF2s","Comparecencia ante la Comisión de Nombramientos","Asamblea Legislativa de Costa Rica. Audiencia en el proceso de su reelección como magistrado de la Sala Constitucional."),
          ("WeDMa-A-sMo","Entrevista a don Fernando Castillo Víquez","Sobre un seminario regional y la importancia de las decisiones de la Corte Interamericana de Derechos Humanos para los Estados parte."),
          ("nhIKJSm2RYA","Sala Constitucional y Asamblea Legislativa","Reflexión sobre la relación entre la jurisdicción constitucional y el Parlamento.")]
def indicators_block():
    out = ""
    for ind in INDICATORS:
        tabs = "".join(f'''<figure class="dtab"><figcaption>{e(cap)}</figcaption><table><thead><tr>{"".join(f"<th>{e(h)}</th>" for h in hd)}</tr></thead>
<tbody>{"".join("<tr" + (' class="hl"' if "Costa Rica" in r else "") + ">" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows)}</tbody></table></figure>''' for cap, hd, rows in ind["tables"])
        paras = "".join(f"<h3>{e(h)}</h3><p>{e(t)}</p>" for h, t in ind["paras"])
        note = f'<p class="note" style="margin-top:8px">{e(ind["note"])}</p>' if ind.get("note") else ""
        srcs = " · ".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)} ↗</a>' for t, u in ind["srcs"])
        out += f'''<article class="analysis reveal" id="{ind["id"]}"><div class="eyebrow">{e(ind["eyebrow"])}</div>
<h2>{e(ind["t"])}</h2><p class="lead" style="max-width:none">{e(ind["lead"])}</p>
<div class="analysis-grid"><div class="analysis-text">{paras}</div><div>{tabs}{note}</div></div>
<p class="note"><b>Fuentes:</b> {srcs}</p></article>'''
    return f'''<section class="block"><div class="wrap"><div class="sec-head"><div><div class="eyebrow">Análisis</div><h2>Costa Rica en los indicadores internacionales</h2></div>
<p class="lead">Lo que dicen los informes más recientes sobre el sistema de justicia costarricense, con los datos de las fuentes originales.</p></div>{out}</div></section>'''

def recog_block(compact=False):
    pers = "".join(f'''<a class="news reveal featured" href="{e(r["u"])}" target="_blank" rel="noopener"><div class="meta"><span>{r["y"]}</span><i></i><span>Reconocimiento personal</span></div>
<h3>{e(r["t"])}</h3><p><b style="color:#e7dcc6">{e(r["org"])}.</b> {e(r["s"])}</p><span class="go">Fuente: {e(r["src"])} ↗</span></a>''' for r in RECOG_PERSONAL)
    sala = "".join(f'''<a class="kp reveal" href="{e(r["u"])}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit;display:block"><span class="fig">{e(r["fig"])}</span><h3>{e(r["t"])}</h3>
<p><b>{e(r["org"])}, {r["y"]}.</b> {e(r["s"])}</p><p style="margin-top:8px;font-size:.8rem;color:var(--gold-ink);font-weight:600">Fuente: {e(r["src"])} ↗</p></a>''' for r in (RECOG_SALA[:3] if compact else RECOG_SALA))
    if compact:
        return f'''<section class="block"><div class="wrap"><div class="sec-head"><div><div class="eyebrow">Reconocimientos</div><h2>Una Sala reconocida internacionalmente</h2></div><a class="btn btn-ink" href="/prensa.html#reconocimientos">Ver todos</a></div>
<div class="grid-3">{sala}</div></div></section>'''
    return f'''<section class="block" id="reconocimientos"><div class="wrap">
<div class="sec-head"><div><div class="eyebrow">Reconocimientos</div><h2>Distinciones y logros</h2></div><p class="lead">Al magistrado y a la Sala Constitucional que preside.</p></div>
<div class="grid-2" style="align-items:stretch;margin-bottom:28px">{pers}</div>
<h3 style="font-size:1.6rem;margin:36px 0 18px">La Sala Constitucional y el Poder Judicial</h3>
<div class="grid-3">{sala}</div>
<p class="note">Los premios institucionales corresponden a la Sala Constitucional o al Poder Judicial de Costa Rica como órganos, no a una persona en particular.</p>
</div></section>'''

def videos_block():
    cards = "".join(f'''<article class="video reveal"><button class="vthumb" type="button" data-yt="{v}" aria-label="Reproducir: {e(t)}">
<img src="/assets/img/video-{v}.webp" alt="" loading="lazy" width="480" height="270"><span class="play" aria-hidden="true"></span></button>
<h3>{e(t)}</h3><p>{e(d)}</p></article>''' for v,t,d in VIDEOS)
    return f'''<section class="block"><div class="wrap"><div class="sec-head"><div><div class="eyebrow">Videos</div><h2>Entrevistas en video</h2></div></div>
<div class="grid-2" style="align-items:start">{cards}</div></div></section>'''

def build_contacto():
    body = hero("Contacto", "Escríbale al despacho académico",
                "Para invitaciones a conferencias, actividades académicas, publicaciones y solicitudes de prensa.", "Contacto")
    body += '''<section class="block"><div class="wrap grid-2" style="align-items:start">
<div>
<h2>¿En qué podemos ayudarle?</h2>
<p class="lead">Complete el formulario y su mensaje llegará directamente. Se responderá a la brevedad posible.</p>
<div class="notice" style="margin:26px 0"><b>Importante:</b> por la naturaleza del cargo, no se atienden por este medio consultas sobre expedientes, recursos en trámite ni solicitudes de criterio jurídico. Para gestiones ante la Sala Constitucional utilice los <a href="https://salaconstitucional.poder-judicial.go.cr/" rel="noopener">canales oficiales del Poder Judicial</a>.</div>
<img src="/assets/img/sala-constitucional.webp" alt="Integrantes de la Sala Constitucional" loading="lazy" style="border-radius:14px;box-shadow:var(--shadow)">
</div>
<form class="form" id="contact-form" novalidate>
  <div class="row"><div><label for="nombre">Nombre completo</label><input id="nombre" name="nombre" required autocomplete="name"></div>
  <div><label for="correo">Correo electrónico</label><input id="correo" name="correo" type="email" required autocomplete="email"></div></div>
  <div class="row"><div><label for="institucion">Institución (opcional)</label><input id="institucion" name="institucion" autocomplete="organization"></div>
  <div><label for="asunto">Asunto</label><select id="asunto" name="asunto"><option>Invitación a conferencia o foro</option><option>Actividad académica</option><option>Prensa / entrevista</option><option>Publicaciones</option><option>Otro</option></select></div></div>
  <div><label for="mensaje">Mensaje</label><textarea id="mensaje" name="mensaje" required></textarea></div>
  <div class="hp" aria-hidden="true"><label for="website">No completar</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
  <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
  <button class="btn btn-ink" type="submit" style="justify-self:start">Enviar mensaje</button>
</form>
</div></section>'''
    return page("contacto.html", "Contacto | Fernando Castillo Víquez",
                "Contacto para invitaciones académicas, conferencias y prensa con Fernando Castillo Víquez.", body)

def build_404():
    body = hero("Error 404", "Página no encontrada", "La dirección que buscó no existe o cambió con el nuevo sitio.", "404")
    body += '<section class="block"><div class="wrap"><a class="btn btn-ink" href="/">Volver al inicio</a></div></section>'
    return page("404.html", "Página no encontrada | Fernando Castillo Víquez", "Página no encontrada.", body)

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "static"), OUT)
    os.makedirs(os.path.join(PUB, "assets", "img"), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "img")):
        shutil.copy(os.path.join(ROOT, "img", f), os.path.join(PUB, "assets", "img", f))
    pages = {"index.html": build_index(), "trayectoria.html": build_trayectoria(), "publicaciones.html": build_publicaciones(),
             "participaciones.html": build_participaciones(), "prensa.html": build_prensa(), "contacto.html": build_contacto(), "404.html": build_404()}
    for n, h in pages.items():
        h = re.sub(r'href="/([a-z0-9\-]+)\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1)}{m.group(2) or ""}"', h)
        open(os.path.join(PUB, n), "w", encoding="utf-8").write(h)
    today = date.today().isoformat()
    IMGS = {"index.html": [("retrato.webp", "Fernando Castillo Víquez, presidente de la Sala Constitucional"), ("conferencia.webp", "Fernando Castillo Víquez durante una intervención")],
            "publicaciones.html": [(b["img"], "Portada del libro " + b["t"]) for b in BOOKS if b.get("img")],
            "contacto.html": [("sala-constitucional.webp", "Integrantes de la Sala Constitucional de Costa Rica")]}
    PRI = {"index.html": "1.0", "trayectoria.html": "0.9", "publicaciones.html": "0.9", "prensa.html": "0.8", "participaciones.html": "0.7", "contacto.html": "0.5"}
    urls = ""
    for n in pages:
        if n == "404.html": continue
        im = "".join(f'<image:image><image:loc>{SITE}/assets/img/{f}</image:loc></image:image>' for f, _ in IMGS.get(n, []))
        urls += f'<url><loc>{seo.url(n)}</loc><lastmod>{today}</lastmod><changefreq>{"weekly" if n=="prensa.html" else "monthly"}</changefreq><priority>{PRI[n]}</priority>{im}</url>\n'
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + urls + "</urlset>\n"
    llms = "# Fernando Castillo Víquez\n\n> Sitio oficial del magistrado Fernando Castillo Víquez, presidente de la Sala Constitucional de la Corte Suprema de Justicia de Costa Rica (magistrado desde 2009, reelecto en 2025). Doctor en Derecho, catedrático y autor.\n\n## Páginas\n" + "".join(f"- [{seo.PAGES[n]['title']}]({seo.url(n)}): {seo.PAGES[n]['desc']}\n" for n in pages if n != "404.html") + "\n## Nota\nSitio personal de carácter académico. Las resoluciones oficiales se consultan en https://salaconstitucional.poder-judicial.go.cr/\n"
    open(os.path.join(PUB, "llms.txt"), "w", encoding="utf-8").write(llms)
    open(os.path.join(PUB, "sitemap.xml"), "w").write(sm)
    print("OK", {k: len(v) for k, v in pages.items()}, "ponencias", len(ponencias), "asistencia", len(asistencia), "articulos", len(articulos))

if __name__ == "__main__":
    main()
