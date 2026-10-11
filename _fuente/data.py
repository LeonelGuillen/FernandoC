# -*- coding: utf-8 -*-
"""Contenido curado del sitio (fuente: sitio actual en Wix + prensa verificada)."""

SITE = "https://www.fernandocastillocr.com"

FIXES = [
    ("panal ", "panel "), ("panales ", "paneles "), ("Freedrich", "Friedrich"), ("Honrad Adenauer", "Konrad Adenauer"),
    ("Castilla La Macha", "Castilla-La Mancha"), ("Duquense- Pittsburg", "Duquesne, Pittsburgh"),
    ("Constiucionalidad", "Constitucionalidad"), ("Menoría", "Memoria"), ("www.mografías.com", "www.monografias.com"),
    ("Educación Continúa", "Educación Continua"), ("Estatáries", "Estatutàries"), ("Estatutaries", "Estatutàries"),
    ("Area Jurídica", "Área Jurídica"), ("Servicios Técnico ", "Servicios Técnicos "), ("Hotel Radison", "Hotel Radisson"),
    ("Crow Plaza", "Crowne Plaza"), ("Dominica-AMCF", "Dominicana-AMCF"), ("Conferencistas en", "Conferencista en"),
    ("del Tribunales y Sala", "de Tribunales y Salas"), ("Jaime Torres Bidet", "Jaime Torres Bodet"),
    ("Carlos Carrales Solano", "Carlos Carrales Solano"), (" ,", ","), ("¿ Cómo", "¿Cómo"),
]

def fix(s):
    for a, b in FIXES:
        s = s.replace(a, b)
    return s

# Libros (curados a mano)
BOOKS = [
    dict(t="Temas controversiales del Derecho Constitucional", role="Autor", pub="Editorial Juricentro", y=2011,
         img="libro-temas-controversiales.webp", buy="https://libreriaucr.com/", feat=True),
    dict(t="Elementos Económicos en la Constitución Política", role="Autor", pub="Editorial Juritexto", y=1992,
         img="libro-elementos-economicos.webp", buy="https://www.juritextocr.com/", feat=True,
         desc="Analiza el sistema económico desde el Derecho de la Constitución: la opción del constituyente de 1949, las libertades económicas, la empresa pública y la planificación."),
    dict(t="Ejecución de sentencias en el Derecho Público costarricense", role="Autor", pub="Editorial Juritexto", y=2009, feat=True),
    dict(t="La protección de los derechos fundamentales en la jurisdicción constitucional y sus vicisitudes", role="Autor", pub="Editorial Juritexto", y=2008, feat=True),
    dict(t="Hacia un populismo constitucional", role="Autor", pub="Instituto de Derecho Constitucional del Estado de Querétaro (México)", y=None,
         note="Mencionado por el autor en entrevista con La Nación (2024). Completar año y ficha."),
    dict(t="La Ley de Presupuesto", role="Autor", pub="Prodel, IIDH-CAPEL", y=1997),
    dict(t="Reflexiones sobre el control de constitucionalidad en Costa Rica. Las cuestiones de constitucionalidad", role="Tesis doctoral", pub="Universidad Escuela Libre de Derecho", y=2002),
    dict(t="Convención Americana sobre Derechos Humanos anotada y concordada con la jurisprudencia de la Corte IDH", role="Coautor", pub="Corte Suprema de Justicia, Escuela Judicial", y=2013),
    dict(t="Código Procesal Contencioso Administrativo, anotado con las actas legislativas", role="Coautor", pub="Procuraduría General de la República y Colegio de Abogados", y=2007),
    dict(t="Reflexiones sobre el Poder Legislativo", role="Coautor", pub="Asamblea Legislativa", y=1989),
    dict(t="Constitución Política anotada y concordada (actualización de la obra de Carlos Arguedas Ramírez)", role="Coautor", pub="Asamblea Legislativa / Editorial Juricentro", y=1985),
    dict(t="Ley de Inquilinato y Disposiciones sobre Desahucio, anotada y concordada", role="Coautor", pub="Asamblea Legislativa / Editorial Juricentro", y=1985),
]

# Prensa y actualidad (verificado por búsqueda, octubre 2026)
NEWS = [
    dict(d="2026-09-30", dl="30 sep 2026", src="Revista Abogacía", kind="Entrevista",
         t="Fernando Castillo: preservar la independencia judicial en Costa Rica",
         s="Conversación sobre independencia judicial —externa e interna—, el deber de acatar las resoluciones aunque se discrepe de ellas y la necesidad de que los tribunales comuniquen de forma institucional.",
         u="https://www.revistaabogacia.com/fernando-castillo-preservar-la-independencia-judicial-en-costa-rica/"),
    dict(d="2026-08-12", dl="12 ago 2026", src="Semanario Universidad", kind="Perfil",
         t="Fernando Castillo, el magistrado tranquilo de la Sala IV, también ve una “estrategia” en ataques del Gobierno",
         s="Perfil sobre su visión del tribunal: respeto a las sentencias, deferencia a los órganos de representación popular y lectura de la coyuntura institucional.",
         u="https://semanariouniversidad.com/pais/fernando-castillo-el-magistrado-tranquilo-de-la-sala-iv-tambien-ve-una-estrategia-en-ataques-del-gobierno/"),
    dict(d="2026-08-05", dl="5 ago 2026", src="La Nación", kind="Declaraciones",
         t="Magistrado Fernando Castillo: ‘La Sala no puede dar un golpe de Estado, los términos se han equivocado’",
         s="Como presidente de la Sala, explicó ante diputados que en el tribunal conviven corrientes distintas y que el respeto a las resoluciones es la base del Estado de derecho.",
         u="https://www.nacion.com/politica/magistrado-fernando-castillo-la-sala-no-puede-dar/HDDXQT6OJNHUJPCTBT25O3FYCQ/story/"),
    dict(d="2025-11-30", dl="30 nov 2025", src="Teletica", kind="Entrevista",
         t="“No soy una persona con pedigrí judicial”, afirma presidente de Sala Constitucional",
         s="Tras su reelección, repasa su independencia política desde 1999, el valor de la experiencia en la magistratura y proyectos como el edificio propio de la Sala.",
         u="https://www.teletica.com/entrevistas/no-soy-una-persona-con-pedigri-judicial-afirma-presidente-de-sala-constitucional_397880"),
    dict(d="2025-11-11", dl="11 nov 2025", src="Delfino.cr", kind="Noticia",
         t="Fernando Castillo, presidente de la Sala IV, reelecto magistrado por ocho años más",
         s="El Plenario legislativo confirmó su continuidad en la Sala Constitucional en sesión extraordinaria del 10 de noviembre de 2025.",
         u="https://delfino.cr/2025/11/fernando-castillo-presidente-de-la-sala-iv-reelecto-magistrado-por-ocho-anos-mas"),
]

NEWS.insert(4, dict(d="2025-11-17", dl="17 nov 2025", src="Sala Constitucional", kind="Comunicado oficial",
     t="Fernando Castillo Víquez es juramentado por un nuevo periodo de ocho años en la Sala Constitucional",
     s="Comunicado institucional sobre su juramentación, su presidencia de la Sala desde 2020 y su trayectoria.",
     u="https://salaconstitucional.poder-judicial.go.cr/index.php/sala-de-prensa/comunicados/fernando-castillo-viquez-es-juramentado-por-un-nuevo-periodo-de-ocho-anos-en-la-sala-constitucional"))
NEWS.append(dict(d="2024-07-22", dl="22 jul 2024", src="El Mundo CR", kind="Reconocimiento",
     t="Magistrado Fernando Castillo recibe reconocimiento por su destacada trayectoria académica y labor docente",
     s="El Poder Judicial de Oaxaca y la Academia Mexicana de Derecho reconocieron su trayectoria como docente desde 1985.",
     u="https://elmundo.cr/costa-rica/magistrado-fernando-castillo-recibe-reconocimiento-por-su-destacada-trayectoria-academica-y-labor-docente/"))

# Entrevista destacada (La Nación, Natasha Cambronero, 35.º aniversario de la Sala IV)
# TODO: pegar la URL exacta del artículo en nacion.com cuando se tenga.
INTERVIEW = dict(
    src="La Nación", author="Natasha Cambronero", when="2024 · 35.º aniversario de la Sala Constitucional",
    t="Presidente de Sala IV advierte sobre inseguridad: ‘Podemos caer en un Estado fallido’",
    u="https://www.google.com/search?q=" + "Presidente+de+Sala+IV+advierte+sobre+inseguridad+Podemos+caer+en+un+Estado+fallido+nacion.com",
)

# Reconocimientos (verificados octubre 2026)
RECOG_PERSONAL = [
    dict(y="2024", t="Reconocimiento por su trayectoria académica y labor docente",
         org="Poder Judicial del Estado de Oaxaca y Academia Mexicana de Derecho “Juan Velásquez” (México)",
         s="Entregado el 28 de junio de 2024 en Oaxaca, donde se le describió como figura emblemática del constitucionalismo costarricense.",
         u="https://elmundo.cr/costa-rica/magistrado-fernando-castillo-recibe-reconocimiento-por-su-destacada-trayectoria-academica-y-labor-docente/", src="El Mundo CR"),
    dict(y="2025", t="Reelegido magistrado propietario por un nuevo período de ocho años",
         org="Asamblea Legislativa de Costa Rica",
         s="Juramentado el 17 de noviembre de 2025. Preside la Sala Constitucional desde mayo de 2020 (interinamente desde agosto de 2018).",
         u="https://salaconstitucional.poder-judicial.go.cr/index.php/sala-de-prensa/comunicados/fernando-castillo-viquez-es-juramentado-por-un-nuevo-periodo-de-ocho-anos-en-la-sala-constitucional", src="Sala Constitucional"),
]
RECOG_SALA = [
    dict(y="2026", fig="SIP", t="Gran Premio Chapultepec 2026",
         org="Sociedad Interamericana de Prensa (SIP)",
         s="Otorgado a la Sala Constitucional por sus fallos en defensa de la libertad de prensa y el pluralismo informativo. Se entrega en la 82.ª Asamblea General de la SIP, Bogotá, 22–25 de octubre de 2026.",
         u="https://www.elfinancierocr.com/economia-y-politica/sip-otorga-el-gran-premio-chapultepec-2026-a-la/2NR7KEBCWNECLAHUYVV73FAW4Y/story/", src="El Financiero"),
    dict(y="2025", fig="1.º", t="Primer lugar en el Índice de Congestión Judicial de las Américas",
         org="Centro de Estudios de Justicia de las Américas (CEJA)",
         s="El Poder Judicial costarricense lideró entre 13 países, con una tasa de resolución de 1,07 en 2024.",
         u="https://elmundo.cr/costa-rica/costa-rica-lidera-en-resolucion-judicial-en-latinoamerica-segun-estudio-del-ceja/", src="El Mundo CR"),
    dict(y="2025", fig="2.º", t="Segundo lugar regional en Estado de Derecho",
         org="World Justice Project — Índice de Estado de Derecho",
         s="Costa Rica es 2.ª de 32 países de Latinoamérica y el Caribe, y 2.ª en límites al poder gubernamental.",
         u="https://worldjusticeproject.org/sites/default/files/documents/Costa%20Rica_3.pdf", src="WJP"),
    dict(y="2025", fig="★", t="Premio Sentencias: acceso a la justicia de personas migrantes",
         org="XI Foro Regional Acceso a la Justicia (CIDH, ACNUR, OIM), Suprema Corte de Justicia de México",
         s="Reconoció un hábeas corpus de la Sala a favor de personas migrantes trasladadas a Costa Rica en 2025.",
         u="https://semanariouniversidad.com/pais/sala-iv-gana-premio-internacional-por-resolucion-sobre-personas-migrantes-recluidas-en-catem/", src="Semanario Universidad"),
    dict(y="2024", fig="108 %", t="Récord de casos resueltos",
         org="Sala Constitucional",
         s="38 484 asuntos resueltos frente a 35 624 ingresados; amparos resueltos en 31 días en promedio.",
         u="https://delfino.cr/2025/01/sala-iv-rompio-record-de-casos-ingresados-y-resueltos-durante-2024", src="Delfino.cr"),
]

# Notas de análisis: indicadores internacionales (fuentes primarias verificadas)
INDICATORS = [
 dict(id="wjp", eyebrow="World Justice Project · Índice de Estado de Derecho 2025", dl="oct 2025",
  t="Costa Rica, segundo país de Latinoamérica en Estado de Derecho",
  lead="El Índice de Estado de Derecho 2025 del World Justice Project ubicó a Costa Rica en el puesto 28 de 143 países y en el segundo lugar de 32 en Latinoamérica y el Caribe, con un puntaje de 0,68 sobre 1, solo detrás de Uruguay.",
  tables=[("Los mejores de la región (puntaje 0 a 1)", ["País", "Puntaje"], [["Uruguay", "0,72"], ["Costa Rica", "0,68"], ["Barbados", "0,66"], ["Chile", "0,66"], ["Promedio regional", "0,51"]]),
          ("Costa Rica por factor", ["Factor", "Puesto mundial", "Puesto regional"], [["Límites al poder gubernamental", "18 / 143", "2 / 32"], ["Justicia penal", "40 / 143", "6 / 32"], ["Justicia civil", "42 / 143", "7 / 32"], ["Ausencia de corrupción", "43 / 143", "7 / 32"]])],
  paras=[
   ("Qué mide", "El índice evalúa ocho factores —límites al poder gubernamental, ausencia de corrupción, gobierno abierto, derechos fundamentales, orden y seguridad, cumplimiento regulatorio, justicia civil y justicia penal— a partir de encuestas a unos 215 000 hogares y 4100 especialistas en derecho de todo el mundo."),
   ("Por qué importa para la justicia constitucional", "El mejor resultado de Costa Rica está en «límites al poder gubernamental»: segundo de la región y 18 del mundo. Ese factor incluye la capacidad del Poder Judicial para controlar de forma efectiva al Ejecutivo y al Legislativo, la tarea central de la Sala Constitucional."),
   ("En contexto", "2025 fue un año de retroceso global: el 68 % de los países bajó su puntaje, frente al 57 % del año anterior. El de Costa Rica disminuyó menos de un 1 %, por lo que el país conservó su posición entre los mejor evaluados del continente."),
   ("Lo que falta", "Justicia civil, justicia penal y ausencia de corrupción quedan entre el sexto y el séptimo lugar regional: ahí están los mayores márgenes de mejora."),
  ],
  srcs=[("Ficha de Costa Rica — WJP 2025", "https://worldjusticeproject.org/sites/default/files/documents/Costa%20Rica_3.pdf"), ("Informe global WJP 2025 (PDF)", "https://worldjusticeproject.org/rule-of-law-index/downloads/WJPIndex2025.pdf"), ("Bloomberg Línea, 31 oct 2025", "https://www.bloomberglinea.com/latinoamerica/uruguay-lidera-y-mexico-retrocede-asi-asi-esta-el-estado-de-derecho-en-america-latina-a-2025/")]),
 dict(id="ceja", eyebrow="CEJA · I Índice de Congestión Judicial en las Américas 2025", dl="nov 2025",
  t="Primer lugar de las Américas en capacidad de resolución judicial",
  lead="El Centro de Estudios de Justicia de las Américas (CEJA) comparó los poderes judiciales de 13 países entre 2018 y 2024. Costa Rica obtuvo la tasa de resolución más alta de 2024 —1,07—: resolvió más casos de los que ingresaron.",
  tables=[("Tasa de resolución 2024 (casos resueltos ÷ ingresados)", ["Puesto", "País", "Tasa"], [["1.º", "Costa Rica", "1,07"], ["2.º", "Perú", "1,06"], ["3.º", "República Dominicana", "0,97"], ["3.º", "Panamá", "0,97"], ["4.º", "Brasil*", "0,94"], ["5.º", "Ecuador", "0,85"], ["6.º", "Colombia", "0,80"], ["7.º", "Chile", "0,72"]]),
          ("Costa Rica, 2018–2024", ["Año", "Resolución", "Congestión"], [["2018", "1,02", "—"], ["2019", "1,03", "1,55"], ["2020", "1,05", "1,58"], ["2021", "1,07", "1,51"], ["2022", "1,08", "1,45"], ["2023", "1,06", "1,43"], ["2024", "1,07", "1,41"]])],
  paras=[
   ("Cómo se mide", "La tasa de resolución divide los casos resueltos entre los ingresados en el año: 1,00 o más se considera óptimo. La tasa de congestión compara la carga total —ingresos más pendientes— con lo resuelto: entre 1,01 y 1,50 es aceptable y más de 2,00 es crítica."),
   ("Siete años por encima del umbral", "Costa Rica mantuvo una tasa de resolución superior a 1,00 en todos los años del período, incluida la pandemia, y redujo su congestión de 1,58 (2020) a 1,41 (2024), dentro del rango aceptable."),
   ("Una región congestionada", "El promedio regional de resolución se mantuvo por debajo de 1 —cerca de 0,92 desde 2022— y la congestión regional cerró 2024 en 1,98, en zona crítica."),
   ("Proyección a 2030", "Según el CEJA, Costa Rica sería el único país de la muestra en alcanzar un equilibrio sostenido, con una congestión estimada de 1,29."),
   ("Matiz", "El índice mide la gestión de todo el sistema judicial —civil, laboral, familia, contencioso y penal—, no la experiencia ciudadana en un caso concreto. La percepción sobre la justicia penal sigue siendo un desafío pendiente."),
  ],
  note="*Brasil 2024 es una proyección del CEJA con datos de 2023.",
  srcs=[("Informe CEJA 2025 (PDF)", "https://cejamericas.org/wp-content/uploads/2025/12/I-Indice-de-Congestion-Judicial-en-las-Americas-CEJA-2025_DICIEMBRE.pdf"), ("El Mundo CR, 11 nov 2025", "https://elmundo.cr/costa-rica/costa-rica-lidera-en-resolucion-judicial-en-latinoamerica-segun-estudio-del-ceja/")]),
]
NEWS.insert(0, dict(d="2025-11-11", dl="nov 2025", src="CEJA", kind="Análisis", t=INDICATORS[1]["t"],
     s="Tasa de resolución de 1,07 en 2024, la más alta de 13 países; único con equilibrio sostenido proyectado a 2030.", u="/contexto-actual.html#ceja"))
NEWS.insert(0, dict(d="2025-10-31", dl="oct 2025", src="World Justice Project", kind="Análisis", t=INDICATORS[0]["t"],
     s="Puesto 28 de 143 en el mundo y 2.º de 32 en la región; 2.º regional en límites al poder gubernamental.", u="/contexto-actual.html#wjp"))
NEWS.sort(key=lambda n: n["d"], reverse=True)

# Destacado: editorial de La Nación sobre el Gran Premio Chapultepec
EDITORIAL = dict(d="2026-08-20", dl="20 ago 2026", src="La Nación", kind="Editorial", feat=True,
     t="Editorial: La Sala Constitucional no necesita premios, pero este llega en un momento crucial",
     s="El editorial de La Nación destaca el Gran Premio Chapultepec otorgado por la SIP y valora la jurisprudencia de la Sala sobre libertad de prensa y acceso a la información pública, que sirvió de base a la Ley Marco de Acceso a la Información vigente desde 2024.",
     q="La Sala Constitucional no necesita premios para reafirmar su trascendente labor.",
     u="https://www.nacion.com/opinion/editorial/editorial-la-sala-constitucional-no-necesita/3ZSATNQL4JAQ5A5QSL5Z6VMGBQ/story/")
NEWS.append(EDITORIAL)
NEWS.sort(key=lambda n: n["d"], reverse=True)

# Cómo llegó a la Sala Constitucional (verificado en prensa y comunicados oficiales)
ELECTION = [
 dict(y="16 nov 2009", t="Electo magistrado de la Sala Constitucional",
      s="La Asamblea Legislativa lo eligió con 39 votos de 44 diputados presentes, cuando se desempeñaba como Procurador Constitucional. Ocupó la plaza de Luis Fernando Solano Carrera, vacante desde hacía 21 meses.",
      u="https://www.nacion.com/el-pais/congreso-elige-a-fernando-castillo-como-magistrado-de-sala-iv/6ZOKMP4FIJGVZGKFYGRS5KWI4U/story/", src="La Nación"),
 dict(y="16 nov 2017", t="Primera reelección",
      s="Con la recomendación favorable de la Comisión de Nombramientos, quedó reelegido para un segundo período de ocho años al vencer el plazo legal sin que el Plenario votara en contra, conforme al artículo 158 de la Constitución.",
      u="https://www.crhoy.com/nacionales/fernando-castillo-fue-reelecto-como-magistrado-de-sala-iv/", src="CRHoy"),
 dict(y="2018 – 2020", t="Presidente de la Sala Constitucional",
      s="Asumió la presidencia de forma interina en agosto de 2018 y en mayo de 2020 el pleno de magistrados lo eligió por unanimidad como presidente.",
      u="https://salaconstitucional.poder-judicial.go.cr/index.php/sala-de-prensa/comunicados/sala-constitucional-elige-al-doctor-fernando-castillo-como-su-presidente", src="Sala Constitucional"),
 dict(y="17 nov 2025", t="Tercer período en la Sala Constitucional",
      s="Tras ser reelegido por la Asamblea Legislativa, fue juramentado para un nuevo período de ocho años. Al asumir afirmó hacerlo «con un profundo sentido de responsabilidad» y se comprometió con una Sala cercana a la ciudadanía, que responda a tiempo y proteja de forma efectiva los derechos de las personas.",
      u="https://elmundo.cr/costa-rica/fernando-castillo-viquez-inicia-nuevo-periodo-en-la-sala-constitucional/", src="El Mundo CR"),
]
ART158 = "Según el artículo 158 de la Constitución Política, los magistrados de la Corte Suprema se eligen por ocho años y se consideran reelegidos por períodos iguales, salvo que al menos dos terceras partes del total de diputados voten en contra."
