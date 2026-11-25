"""Genera el banner y las tarjetas de proyectos del perfil (versiones clara y oscura).

Uso: python scripts/generar_svg.py assets
Para agregar un proyecto, suma una entrada a PROYECTOS y referencia sus dos SVG en el README.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

SALIDA = Path(sys.argv[1])
(SALIDA / "proyectos").mkdir(parents=True, exist_ok=True)

SERIF = "Georgia, 'Times New Roman', serif"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "Consolas, 'Courier New', monospace"

TEMAS = {
    "claro": dict(fondo="#FBF6EE", puntos="#E6DACA", tinta="#2A2420", suave="#6B6157", acento="#C4532D",
                  papel="#FFFDF9", borde="#E6DCCB", sombra="#5A4632", sombra_op="0.16", cuerpo="#5E554C"),
    "oscuro": dict(fondo="#16181D", puntos="#2A2E36", tinta="#F3ECDF", suave="#B3A898", acento="#E58A63",
                   papel="#1F2229", borde="#343842", sombra="#000000", sombra_op="0.45", cuerpo="#C9BFB1"),
}

# Colores de acento por proyecto: (claro, oscuro)
ACENTOS = {
    "terracota": ("#C4532D", "#E58A63"),
    "azul": ("#2B5C8A", "#7FB0DE"),
    "mostaza": ("#A9761A", "#E2B04A"),
    "salvia": ("#55804A", "#8DBF7A"),
    "verde": ("#2C7A6B", "#62BFAE"),
    "ciruela": ("#7A4E8C", "#B98ECB"),
}


def banner(tema):
    t = TEMAS[tema]
    bandas = [ACENTOS["mostaza"], ACENTOS["azul"], ACENTOS["terracota"]]
    color = lambda par: par[0] if tema == "claro" else par[1]

    def tarjeta(x, y, giro, ancho, etiqueta, color_banda, lineas, n):
        cuerpo = "".join(
            f'<text x="18" y="{62 + i * 23}" font-family="{MONO}" font-size="15" fill="{t["cuerpo"]}">{escape(l)}</text>'
            for i, l in enumerate(lineas))
        return f'''
  <g transform="translate({x} {y}) rotate({giro})" filter="url(#sombra)">
    <clipPath id="recorte{n}"><rect width="{ancho}" height="118" rx="14"/></clipPath>
    <rect width="{ancho}" height="118" rx="14" fill="{t["papel"]}" stroke="{t["borde"]}" stroke-width="1.5"/>
    <g clip-path="url(#recorte{n})"><rect width="{ancho}" height="36" fill="{color_banda}"/></g>
    <circle cx="20" cy="18" r="4" fill="#FFFFFF" fill-opacity="0.55"/>
    <circle cx="34" cy="18" r="4" fill="#FFFFFF" fill-opacity="0.35"/>
    <text x="{ancho - 16}" y="24" text-anchor="end" font-family="{SANS}" font-size="15" font-weight="600" fill="#FFFFFF">{etiqueta}</text>
    {cuerpo}
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="titulo descripcion">
  <title id="titulo">Sergio Parra</title>
  <desc id="descripcion">Estudiante de Ingeniería de Sistemas en la Universidad El Bosque, Bogotá. Trabaja con Java, Angular y SQL.</desc>
  <defs>
    <pattern id="puntos" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="1.4" fill="{t["puntos"]}"/>
    </pattern>
    <filter id="sombra" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="{t["sombra"]}" flood-opacity="{t["sombra_op"]}"/>
    </filter>
  </defs>
  <rect width="1200" height="320" rx="26" fill="{t["fondo"]}"/>
  <rect width="1200" height="320" rx="26" fill="url(#puntos)"/>

  <text x="76" y="106" font-family="{MONO}" font-size="17" letter-spacing="5" fill="{t["acento"]}">HOLA, SOY</text>
  <text x="70" y="182" font-family="{SERIF}" font-size="78" font-weight="700" fill="{t["tinta"]}">Sergio Parra</text>
  <path d="M76 206 C 220 190, 400 224, 572 198" stroke="{t["acento"]}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <text x="76" y="252" font-family="{SANS}" font-size="22" fill="{t["suave"]}">Ingeniería de Sistemas · Universidad El Bosque · Bogotá</text>
{tarjeta(738, 96, -9, 206, "SQL", color(bandas[0]), ["SELECT nombre", "FROM mascota;"], 1)}
{tarjeta(966, 40, 6, 188, "Angular", color(bandas[1]), ["<app-carrito>", "</app-carrito>"], 2)}
{tarjeta(846, 170, -2, 214, "Java", color(bandas[2]), ["torneo.iniciar();", "torneo.jugarTodos();"], 3)}
</svg>
'''


ICONOS = {
    "escudo": lambda cx, cy, c: f'''
    <path d="M{cx} {cy-44} L{cx+36} {cy-28} V{cy+2} C{cx+36} {cy+26} {cx+18} {cy+40} {cx} {cy+48} C{cx-18} {cy+40} {cx-36} {cy+26} {cx-36} {cy+2} V{cy-28} Z" fill="none" stroke="{c}" stroke-width="4" stroke-linejoin="round"/>
    <circle cx="{cx}" cy="{cy}" r="8" fill="{c}"/>
    <path d="M{cx} {cy+4} V{cy+20}" stroke="{c}" stroke-width="6" stroke-linecap="round"/>''',
    "navegador": lambda cx, cy, c: f'''
    <rect x="{cx-46}" y="{cy-38}" width="92" height="76" rx="9" fill="none" stroke="{c}" stroke-width="4"/>
    <path d="M{cx-46} {cy-22} H{cx+46}" stroke="{c}" stroke-width="4"/>
    <circle cx="{cx-35}" cy="{cy-30}" r="3" fill="{c}"/><circle cx="{cx-25}" cy="{cy-30}" r="3" fill="{c}"/>
    <rect x="{cx-28}" y="{cy-10}" width="56" height="9" rx="4.5" fill="none" stroke="{c}" stroke-width="3"/>
    <rect x="{cx-28}" y="{cy+5}" width="56" height="9" rx="4.5" fill="none" stroke="{c}" stroke-width="3"/>
    <rect x="{cx-15}" y="{cy+21}" width="30" height="9" rx="4.5" fill="{c}"/>''',
    "bolsa": lambda cx, cy, c: f'''
    <path d="M{cx-34} {cy-16} H{cx+34} L{cx+29} {cy+42} H{cx-29} Z" fill="none" stroke="{c}" stroke-width="4" stroke-linejoin="round"/>
    <path d="M{cx-15} {cy-16} V{cy-26} A15 15 0 0 1 {cx+15} {cy-26} V{cy-16}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>
    <path d="M{cx-14} {cy+12} Q{cx} {cy+24} {cx+14} {cy+12}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>''',
    "casa": lambda cx, cy, c: f'''
    <path d="M{cx-42} {cy-2} L{cx} {cy-40} L{cx+42} {cy-2}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M{cx-32} {cy-10} V{cy+40} H{cx+32} V{cy-10}" fill="none" stroke="{c}" stroke-width="4" stroke-linejoin="round"/>
    <rect x="{cx-9}" y="{cy+14}" width="18" height="26" rx="3" fill="{c}"/>
    <rect x="{cx+12}" y="{cy-2}" width="12" height="11" rx="2" fill="none" stroke="{c}" stroke-width="3"/>''',
    "cancha": lambda cx, cy, c: f'''
    <rect x="{cx-48}" y="{cy-32}" width="96" height="64" rx="5" fill="none" stroke="{c}" stroke-width="4"/>
    <path d="M{cx} {cy-32} V{cy+32}" stroke="{c}" stroke-width="3"/>
    <circle cx="{cx}" cy="{cy}" r="12" fill="none" stroke="{c}" stroke-width="3"/>
    <rect x="{cx-48}" y="{cy-15}" width="13" height="30" fill="none" stroke="{c}" stroke-width="3"/>
    <rect x="{cx+35}" y="{cy-15}" width="13" height="30" fill="none" stroke="{c}" stroke-width="3"/>
    <circle cx="{cx+20}" cy="{cy-14}" r="5" fill="{c}"/>''',
    "huella": lambda cx, cy, c: f'''
    <ellipse cx="{cx}" cy="{cy+16}" rx="20" ry="17" fill="{c}"/>
    <ellipse cx="{cx-28}" cy="{cy-6}" rx="8" ry="10" fill="{c}"/>
    <ellipse cx="{cx-11}" cy="{cy-24}" rx="8" ry="10" fill="{c}"/>
    <ellipse cx="{cx+11}" cy="{cy-24}" rx="8" ry="10" fill="{c}"/>
    <ellipse cx="{cx+28}" cy="{cy-6}" rx="8" ry="10" fill="{c}"/>''',
}

PROYECTOS = [
    ("springfirstappjwt", "API REST · SEGURIDAD", "SpringFirstApp JWT", "P2X4A/SpringFirstAppJWT", "terracota", "escudo",
     ["Java 21", "Spring Boot 3", "JWT", "MySQL"]),
    ("jwt-front", "FRONTEND", "Front del JWT", "P2X4A/springfirstapp-jwt-front", "azul", "navegador",
     ["Angular 22", "TypeScript", "Bootstrap"]),
    ("mercado-libre", "FRONTEND · EN EQUIPO", "Clon de Mercado Libre", "P2X4A/proyecto1-desarollo3", "mostaza", "bolsa",
     ["Angular 22", "RxJS", "Fake Store API", "OMDb"]),
    ("alojamientos", "MARKETPLACE · EN EQUIPO", "Alojamientos LR", "P2X4A/ProyectoMarketplaceAlojamientos", "salvia", "casa",
     ["Angular 22", "TypeScript", "Bootstrap"]),
    ("torneo", "SIMULADOR · CONSOLA", "Torneo de fútbol", "P2X4A/Proyecto-Final-Desarollo-2", "verde", "cancha",
     ["Java 21", "Maven", "JUnit 5", "MVC"]),
    ("sigevet", "BASES DE DATOS · EN EQUIPO", "SIGEVET", "P2X4A/sigevet-app-mvc", "ciruela", "huella",
     ["Spring Boot", "Thymeleaf", "JDBC", "MySQL"]),
]


def tarjeta(proyecto, tema):
    clave, antetitulo, titulo, repo, acento, icono, chips = proyecto
    t = TEMAS[tema]
    c = ACENTOS[acento][0 if tema == "claro" else 1]
    x = 36
    pastillas = []
    for chip in chips:
        ancho = round(len(chip) * 7.6 + 22)
        pastillas.append(
            f'<rect x="{x}" y="152" width="{ancho}" height="30" rx="15" fill="{c}" fill-opacity="{0.12 if tema == "claro" else 0.2}"/>'
            f'<text x="{x + ancho / 2}" y="172" text-anchor="middle" font-family="{MONO}" font-size="13.5" fill="{c}">{escape(chip)}</text>')
        x += ancho + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="210" viewBox="0 0 560 210" role="img" aria-labelledby="titulo">
  <title id="titulo">{escape(titulo)} ({escape(repo)})</title>
  <defs><clipPath id="borde"><rect x="1" y="1" width="558" height="208" rx="18"/></clipPath></defs>
  <rect x="1" y="1" width="558" height="208" rx="18" fill="{t["papel"]}" stroke="{t["borde"]}" stroke-width="2"/>
  <g clip-path="url(#borde)"><rect x="0" y="0" width="9" height="210" fill="{c}"/></g>
  <text x="36" y="48" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{c}">{escape(antetitulo)}</text>
  <text x="36" y="92" font-family="{SERIF}" font-size="30" font-weight="700" fill="{t["tinta"]}">{escape(titulo)}</text>
  <text x="36" y="122" font-family="{MONO}" font-size="13.5" fill="{t["suave"]}">{escape(repo)}</text>
  {"".join(pastillas)}
  <circle cx="474" cy="92" r="58" fill="{c}" fill-opacity="{0.08 if tema == "claro" else 0.14}"/>
  {ICONOS[icono](474, 92, c)}
</svg>
'''


for tema in TEMAS:
    (SALIDA / f"banner-{tema}.svg").write_text(banner(tema), encoding="utf-8")
    for proyecto in PROYECTOS:
        (SALIDA / "proyectos" / f"{proyecto[0]}-{tema}.svg").write_text(tarjeta(proyecto, tema), encoding="utf-8")
print("ok", sorted(p.name for p in SALIDA.rglob("*.svg")))
