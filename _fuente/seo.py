# -*- coding: utf-8 -*-
"""Elementos SEO por página: title, description, keywords, schema.org (JSON-LD)."""
from datetime import date
from data import SITE, BOOKS, NEWS, INTERVIEW

TODAY = date.today().isoformat()
PID, WID = SITE + "/#person", SITE + "/#website"

PAGES = {
 "index.html": dict(
    title="Magistrado Fernando Castillo Víquez | Sala Constitucional",
    desc="Sitio oficial del magistrado Fernando Castillo Víquez, presidente de la Sala Constitucional de Costa Rica: trayectoria, libros, conferencias y prensa.",
    kw_main="Fernando Castillo Víquez",
    kw=["Fernando Castillo Víquez", "magistrado Fernando Castillo", "presidente Sala Constitucional", "Sala IV Costa Rica", "magistrado Sala Constitucional", "Derecho Constitucional Costa Rica"],
    h1="Fernando Castillo Víquez", type="ProfilePage", crumb=None, ogalt="Fernando Castillo Víquez, presidente de la Sala Constitucional de Costa Rica"),
 "trayectoria.html": dict(
    title="Trayectoria de Fernando Castillo Víquez | Magistrado",
    desc="Formación, cargos y docencia de Fernando Castillo Víquez: asesor legislativo, Procurador Constitucional (1999–2009) y magistrado de la Sala IV desde 2009.",
    kw_main="trayectoria Fernando Castillo Víquez",
    kw=["Fernando Castillo Víquez biografía", "Procurador Constitucional", "Letrado Mayor Asamblea Legislativa", "magistrado desde 2009", "Escuela Libre de Derecho profesor"],
    h1="Cuatro décadas de servicio público y academia", type="ProfilePage", crumb="Trayectoria", ogalt="Trayectoria de Fernando Castillo Víquez"),
 "publicaciones.html": dict(
    title="Libros y artículos de Fernando Castillo Víquez",
    desc="Libros y artículos del magistrado Fernando Castillo Víquez sobre Derecho Constitucional y parlamentario: Temas controversiales, Elementos económicos y más.",
    kw_main="libros Fernando Castillo Víquez",
    kw=["Temas controversiales del Derecho Constitucional", "Elementos Económicos en la Constitución Política", "Ejecución de sentencias en el Derecho Público", "Hacia un populismo constitucional", "artículos Derecho Parlamentario"],
    h1="Obra escrita", type="CollectionPage", crumb="Publicaciones", ogalt="Libros de Fernando Castillo Víquez"),
 "participaciones.html": dict(
    title="Conferencias y foros | Fernando Castillo Víquez",
    desc="Conferencias, mesas redondas y paneles en Costa Rica, Latinoamérica y EE. UU. sobre justicia constitucional, derecho a la salud y control de convencionalidad.",
    kw_main="conferencias Fernando Castillo Víquez",
    kw=["conferencista Derecho Constitucional", "control de convencionalidad", "judicialización de la salud", "Jornadas de Derecho Constitucional", "Conferencia Iberoamericana de Justicia Constitucional"],
    h1="Conferencias, foros y comisiones", type="CollectionPage", crumb="Participaciones", ogalt="Conferencias de Fernando Castillo Víquez"),
 "contexto-actual.html": dict(
    title="Contexto actual de la Sala Constitucional | F. Castillo",
    desc="La Sala Constitucional hoy: indicadores internacionales, reconocimientos, entrevistas y noticias sobre la labor de su presidente, Fernando Castillo Víquez.",
    kw_main="Sala Constitucional Costa Rica actualidad",
    kw=["presidente Sala IV entrevista", "Premio Chapultepec Sala Constitucional", "independencia judicial Costa Rica", "Índice de Estado de Derecho Costa Rica", "CEJA congestión judicial Costa Rica"],
    h1="La Sala Constitucional hoy", type="CollectionPage", crumb="Contexto actual", ogalt="Contexto actual de la Sala Constitucional de Costa Rica"),
 "contacto.html": dict(
    title="Contacto | Magistrado Fernando Castillo Víquez",
    desc="Invitaciones a conferencias, actividades académicas y solicitudes de prensa para el magistrado Fernando Castillo Víquez. No atiende consultas de expedientes.",
    kw_main="contacto Fernando Castillo Víquez",
    kw=["invitar conferencista Derecho Constitucional", "contacto magistrado Sala Constitucional", "solicitud entrevista presidente Sala IV"],
    h1="Escríbale al despacho académico", type="ContactPage", crumb="Contacto", ogalt="Contacto Fernando Castillo Víquez"),
 "404.html": dict(title="Página no encontrada | Fernando Castillo Víquez", desc="La página solicitada no existe.", kw_main="", kw=[], h1="Página no encontrada", type="WebPage", crumb="404", ogalt="", noindex=True),
}

def url(fname):
    return SITE + "/" + ("" if fname == "index.html" else fname[:-5])

PERSON = {
  "@type": "Person", "@id": PID, "name": "Fernando Castillo Víquez", "givenName": "Fernando", "familyName": "Castillo Víquez",
  "alternateName": ["Fernando Castillo", "Magistrado Fernando Castillo", "Fernando Castillo V."],
  "honorificPrefix": "Dr.", "url": SITE + "/",
  "image": {"@type": "ImageObject", "url": SITE + "/assets/img/retrato.webp", "width": 496, "height": 568},
  "jobTitle": "Presidente de la Sala Constitucional",
  "description": "Magistrado propietario de la Sala Constitucional de la Corte Suprema de Justicia de Costa Rica desde 2009 y su presidente. Doctor en Derecho, catedrático universitario y autor.",
  "worksFor": {"@type": "GovernmentOrganization", "name": "Sala Constitucional de la Corte Suprema de Justicia de Costa Rica", "url": "https://salaconstitucional.poder-judicial.go.cr/",
               "parentOrganization": {"@type": "GovernmentOrganization", "name": "Poder Judicial de Costa Rica", "url": "https://pj.poder-judicial.go.cr/"}},
  "hasOccupation": [{"@type": "Occupation", "name": "Magistrado"}, {"@type": "Occupation", "name": "Profesor universitario"}, {"@type": "Occupation", "name": "Notario público"}],
  "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Universidad de Costa Rica"}, {"@type": "CollegeOrUniversity", "name": "Universidad Escuela Libre de Derecho"}],
  "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Licenciatura en Derecho", "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Universidad de Costa Rica"}},
                    {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "Doctorado en Derecho", "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Universidad Escuela Libre de Derecho"}}],
  "birthPlace": {"@type": "Place", "name": "Heredia, Costa Rica"}, "nationality": {"@type": "Country", "name": "Costa Rica"},
  "knowsLanguage": "es",
  "knowsAbout": ["Derecho Constitucional", "Derecho Procesal Constitucional", "Derecho Parlamentario", "Derecho Público Económico", "Derecho Administrativo", "Control de convencionalidad", "Derecho a la salud"],
  "subjectOf": [{"@type": "CreativeWork", "name": n["t"], "url": n["u"], "datePublished": n["d"], "publisher": {"@type": "Organization", "name": n["src"]}} for n in NEWS if n["u"].startswith("http")],
}

WEBSITE = {"@type": "WebSite", "@id": WID, "url": SITE + "/", "name": "Fernando Castillo Víquez", "inLanguage": "es-CR", "publisher": {"@id": PID}, "about": {"@id": PID}}

VIDEOS = [("E4O-0gI2j0o", "Juramentación de Fernando Castillo Víquez para un nuevo período en la Sala Constitucional"), ("5sLBl72rUVM", "La Sala charla con el magistrado Fernando Castillo Víquez — TEPJF"), ("8_P4O4-GF2s", "Fernando Castillo Víquez ante la Comisión de Nombramientos de la Asamblea Legislativa"), ("WeDMa-A-sMo", "Entrevista a don Fernando Castillo Víquez"), ("nhIKJSm2RYA", "Sala Constitucional y Asamblea Legislativa — Fernando Castillo Víquez")]

VIDEO_DATES = {}  # p. ej. {"WeDMa-A-sMo": "2013-05-20"}

def graph(fname):
    p = PAGES[fname]; u = url(fname)
    webpage = {"@type": p["type"], "@id": u + "#webpage", "url": u, "name": p["title"], "description": p["desc"], "inLanguage": "es-CR",
               "isPartOf": {"@id": WID}, "about": {"@id": PID}, "dateModified": TODAY,
               "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/assets/img/og-image.jpg", "width": 1200, "height": 630}}
    if p["type"] == "ProfilePage":
        webpage["mainEntity"] = {"@id": PID}
    g = [WEBSITE, PERSON, webpage]
    if p.get("crumb"):
        bc = {"@type": "BreadcrumbList", "@id": u + "#breadcrumb", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": u}]}
        webpage["breadcrumb"] = {"@id": u + "#breadcrumb"}; g.append(bc)
    if fname == "publicaciones.html":
        g.append({"@type": "ItemList", "name": "Libros de Fernando Castillo Víquez", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {k: v for k, v in {
                "@type": "Thesis" if b["role"] == "Tesis doctoral" else "Book", "name": b["t"], "inLanguage": "es",
                "author": {"@id": PID}, "datePublished": str(b["y"]) if b["y"] else None,
                "publisher": {"@type": "Organization", "name": b["pub"]},
                "image": SITE + "/assets/img/" + b["img"] if b.get("img") else None}.items() if v}} for i, b in enumerate(BOOKS)]})
    if fname == "contexto-actual.html" and VIDEO_DATES:  # Google exige uploadDate; completar VIDEO_DATES
        for vid, name in VIDEOS:
            if vid not in VIDEO_DATES: continue
            g.append({"@type": "VideoObject", "name": name, "description": name, "thumbnailUrl": SITE + f"/assets/img/video-{vid}.webp",
                      "embedUrl": f"https://www.youtube-nocookie.com/embed/{vid}", "contentUrl": f"https://www.youtube.com/watch?v={vid}",
                      "uploadDate": VIDEO_DATES[vid], "about": {"@id": PID}})
    return {"@context": "https://schema.org", "@graph": g}
