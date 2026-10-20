import os
import sys, json
from playwright.sync_api import sync_playwright

def rgb(h):
    h=h.lstrip('#'); return 'rgb(%d, %d, %d)'%(int(h[0:2],16),int(h[2:4],16),int(h[4:6],16))

TOKENS = {
 '--color-primario':'#1A6FF0','--color-primario-hover':'#1558C4','--color-primario-suave':'#E8F0FE',
 '--color-oscuro':'#0B1530','--color-texto':'#1B2233','--color-texto-suave':'#5F6778','--color-fondo':'#FFFFFF',
 '--color-fondo-alterno':'#F3F5F9','--color-borde':'#D5DAE3','--color-exito':'#1A7F4F','--color-error':'#C93535',
 '--color-advertencia':'#9A5B00','--texto-h1':'56px','--texto-h2':'36px','--texto-h3':'22px','--texto-l':'19px',
 '--texto-base':'17px','--texto-s':'14px','--texto-m':'15px','--texto-xs':'13px','--texto-boton':'16px','--espacio-xs':'4px','--espacio-s':'8px','--espacio-m':'16px',
 '--espacio-l':'24px','--espacio-xl':'32px','--espacio-2xl':'48px','--espacio-3xl':'64px','--ancho-contenido':'1100px',
 '--radio-m':'8px','--radio-l':'12px','--boton-padding':'11px 22px','--boton-alto-min':'44px',
 '--icono-s':'16px','--icono-m':'24px','--icono-l':'32px','--icono-xl':'36px','--color-borde-fuerte':'#AEB5C2','--color-linea':'#8B93A3','--seccion':'72px','--seccion-chica':'48px','--margen-lateral':'20px','--alto-encabezado':'72px',
 '--fuente-titulos':'"Barlow Condensed", "Arial Narrow", Arial, sans-serif','--fuente-cuerpo':'"Barlow", Arial, sans-serif',
 '--fuente-codigo':'"Cascadia Mono", Consolas, "Courier New", monospace'}

JS_STYLE = """([sel,props])=>{const e=document.querySelector(sel); if(!e) return null;
 const c=getComputedStyle(e); const o={}; for(const p of props) o[p]=c.getPropertyValue(p); return o;}"""

def run(url, desktop=True):
    rows=[]
    def add(cat,crit,exp,found,ok): rows.append(dict(cat=cat,crit=crit,exp=str(exp),found=str(found),status='cumple' if ok else 'no cumple'))
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or None)
        pg=b.new_page(viewport={'width':1440,'height':900}); pg.goto(url); pg.wait_for_timeout(300)
        def st(sel,props): return pg.evaluate(JS_STYLE,[sel,props])
        def chk(cat,crit,sel,prop,exp,norm=None):
            r=st(sel,[prop])
            if r is None: add(cat,crit,exp,'elemento no existe (%s)'%sel,False); return
            v=r[prop]; add(cat,crit,exp,v,v==exp)
        # ---------- A. variables
        for k,v in TOKENS.items():
            f=pg.evaluate("k=>getComputedStyle(document.documentElement).getPropertyValue(k).trim()",k)
            add('Variables :root',k,v,f if f else 'no definida',f.lower()==v.lower())
        # ---------- B. tipografía
        fam=pg.evaluate("getComputedStyle(document.body).fontFamily")
        add('Tipografía','Familia del cuerpo','"Barlow", Arial, sans-serif',fam,fam.startswith('Barlow') or fam.startswith('"Barlow"'))
        faces=pg.evaluate("""async()=>{try{await Promise.all([400,500,600,700].map(w=>document.fonts.load(w+' 16px Barlow')).concat([document.fonts.load('700 16px "Barlow Condensed"')]))}catch(e){}
          return [...document.fonts].map(f=>f.family+' '+f.weight+': '+f.status)}""")
        for w in (400,500,600,700):
            hit=[f for f in faces if f.startswith('Barlow') and (' %d:'%w) in f or (f.startswith('"Barlow"') and (' %d:'%w) in f)]
            add('Tipografía','Archivo local Barlow %d cargado'%w,'loaded',hit[0].split(': ')[-1] if hit else 'sin @font-face',bool(hit) and hit[0].endswith('loaded'))
        chk('Tipografía','Texto base (body, 17 px en los wireframes)','body','font-size','17px')
        chk('Tipografía','Interlineado de párrafos (1,4 × 17)','body','line-height','23.8px')
        chk('Tipografía','Color de texto','body','color',rgb('#1B2233'))
        chk('Colores','Fondo general','body','background-color',rgb('#FFFFFF'))
        for sel,sz,nm in (('h1','56px','H1'),('h2','36px','H2'),('h3','22px','H3')):
            chk('Tipografía',nm+' tamaño (escritorio)',sel,'font-size',sz)
            chk('Tipografía',nm+' peso',sel,'font-weight','700')
        chk('Tipografía','Interlineado de títulos (H1 = 1,02 × 56)','h1','line-height','57.12px')
        chk('Tipografía','Hero: subtítulo (texto grande)','#hero p','font-size','19px')
        # ---------- C. botones
        for sel,nm,bg,tx,bd in (('.boton-primario','Primario','#1A6FF0','#FFFFFF','#1A6FF0'),):
            chk('Botones',nm+': fondo',sel,'background-color',rgb(bg))
            chk('Botones',nm+': texto',sel,'color',rgb(tx))
        chk('Botones','Padding','.boton','padding','11px 22px')
        chk('Botones','Esquinas','.boton','border-radius','8px')
        chk('Botones','Tamaño de texto','.boton','font-size','16px')
        chk('Botones','Peso del texto','.boton','font-weight','600')
        chk('Botones','Altura mínima','.boton','min-height','44px')
        chk('Botones','Transición (150 ms)','.boton','transition-duration','0.15s')
        chk('Botones','Secundario: fondo blanco (wireframes)','.boton-secundario','background-color',rgb('#FFFFFF'))
        chk('Botones','Secundario: borde 1 px','.boton-secundario','border-top-width','1px')
        chk('Botones','Secundario: color de borde (azul marino)','.boton-secundario','border-top-color',rgb('#0B1530'))
        chk('Botones','Secundario: color de texto (azul marino)','.boton-secundario','color',rgb('#0B1530'))
        # hover
        for sel,nm,prop,exp in (('.boton-primario','Primario hover: fondo','background-color',rgb('#1558C4')),
                                 ('.boton-secundario','Secundario hover: fondo','background-color',rgb('#E8F0FE')),
                                 ('.boton-secundario','Secundario hover: texto','color',rgb('#0B1530'))):
            try:
                pg.hover(sel,timeout=1500); pg.wait_for_timeout(250)
                chk('Botones',nm,sel,prop,exp)
            except Exception: add('Botones',nm,exp,'elemento no existe (%s)'%sel,False)
        pg.mouse.move(0,0)
        # foco por teclado
        foc=None
        pg.evaluate("document.body.focus()")
        for i in range(15):
            pg.keyboard.press('Tab')
            if pg.evaluate("document.activeElement.matches('a.boton')"):
                pg.wait_for_timeout(300)
                foc=pg.evaluate("(()=>{const c=getComputedStyle(document.activeElement);return c.outlineWidth+' '+c.outlineStyle+' '+c.outlineColor+' offset '+c.outlineOffset})()"); break
        add('Botones','Foco por teclado: contorno 3 px #1A6FF0, separación 2 px','3px solid '+rgb('#1A6FF0')+' offset 2px',foc or 'ningún botón recibe foco',foc=='3px solid '+rgb('#1A6FF0')+' offset 2px')
        # ---------- D. espaciados y colores de superficie
        chk('Espaciados','Padding vertical de sección (72 px)','#funciones','padding-top','72px')
        chk('Espaciados','Ancho máximo del contenido (1100 px)','#funciones .cuadricula','max-width','1100px')
        chk('Espaciados','Título de sección → contenido (14 px)','#funciones h2','margin-bottom','14px')
        chk('Espaciados','Padding interno de tarjeta (24 px)','.tarjeta','padding','24px')
        chk('Espaciados','Separación entre tarjetas (24 px)','.cuadricula','column-gap','24px')
        chk('Espaciados','Esquinas de tarjeta (12 px)','.tarjeta','border-top-left-radius','12px')
        chk('Colores','Tarjeta: borde','.tarjeta','border-top-color',rgb('#AEB5C2'))
        chk('Colores','Sección alterna: fondo','#funciones','background-color',rgb('#F3F5F9'))
        chk('Colores','Banda de cierre (CTA): fondo','#cta','background-color',rgb('#0B1530'))
        chk('Colores','Pie de página: fondo gris claro','#pie','background-color',rgb('#F3F5F9'))
        chk('Colores','Etiqueta: fondo blanco','.etiqueta','background-color',rgb('#FFFFFF'))
        chk('Íconos','Tamaño de ícono en tarjetas (36 px)','.tarjeta .icono','width','36px')
        chk('Íconos','Ícono de menú móvil (24 px)','#btn-menu img','width','24px')
        # ---------- E. estructura
        S=lambda sel: pg.evaluate("s=>document.querySelectorAll(s).length",sel)
        def est(crit,sel,n=1,extra=None):
            f=S(sel); add('Estructura HTML',crit+('' if n==1 else ' ×%d'%n),'%d × %s'%(n,sel),'%d'%f,f==n)
        est('Encabezado','header#encabezado'); est('Logo del encabezado','header#encabezado > a.logo[href="/"] > img[alt="Logo de ApeByte"]')
        est('Menú principal','header > nav#menu-principal[aria-label="Principal"]')
        est('Enlaces del menú','nav#menu-principal ul > li > a.enlace-menu',6)
        est('Botón Iniciar sesión (enlace a /login)','nav#menu-principal li.item-sesion > a.boton.boton-primario[href="/login"]')
        est('Botón de menú móvil','header > button#btn-menu')
        est('Contenido principal','body > main#contenido')
        est('Pie de página','body > footer#pie')
        est('Logo del pie','footer#pie > a.logo > img[alt="Logo de ApeByte"]')
        est('Menú del pie','footer#pie > nav#menu-pie[aria-label="Enlaces secundarios"]')
        est('Enlaces del pie','nav#menu-pie ul > li > a.enlace-pie',4)
        est('Derechos','footer#pie > p.derechos')
        est('Un solo h1 por página, dentro de main','main#contenido h1')
        add('Estructura HTML','h1 total en la página','1',str(S('h1')),S('h1')==1)
        add('Estructura HTML','Sin id login-btn (debe desaparecer)','0','%d'%S('#login-btn'),S('#login-btn')==0)
        est('Hero','main#contenido > section#hero'); est('Hero: botón primario','#hero a.boton.boton-primario[href="/login"]')
        est('Hero: botón secundario','#hero a.boton.boton-secundario[href="/como-funciona"]')
        est('Hero: ilustración con alt','#hero img.ilustracion[alt="Mascota de ApeByte"]')
        est('Sección funciones','main > section#funciones'); est('Funciones: h2','#funciones > h2')
        est('Funciones: tarjetas','#funciones article.tarjeta',4)
        est('Tarjetas con img.icono','#funciones article.tarjeta > img.icono',4)
        est('Tarjetas con h3','#funciones article.tarjeta > h3',4)
        est('Tarjetas con p','#funciones article.tarjeta > p',4)
        est('Sección pasos','main > section#pasos'); est('Pasos: ol.pasos','#pasos > ol.pasos')
        est('Pasos: li.paso con enlace a /como-funciona','#pasos ol.pasos > li.paso > a[href="/como-funciona"]',4)
        est('Sección tecnologías','main > section#tecnologias')
        est('Etiquetas','#tecnologias ul.etiquetas > li.etiqueta',5)
        est('Sección CTA (banda oscura)','main > section#cta.banda-oscura')
        est('CTA: h2','#cta > h2'); est('CTA: botón primario','#cta > a.boton.boton-primario')
        est('Etiquetas semánticas section en Home (hero, funciones, pasos, tecnologias, cta)','main#contenido > section',5)
        est('Menús con nav (principal + pie)','nav',2)
        est('Sin aria-current en Home (ítem activo no aplica)','a[aria-current]',0)
        order=pg.evaluate("[...document.body.children].map(e=>e.tagName.toLowerCase()).filter(t=>t!='script').join(' > ')")
        add('Estructura HTML','Orden en body','header > main > footer',order,order=='header > main > footer')
        hdr=pg.evaluate("(()=>{const h=document.querySelector('header');return h?[...h.children].map(e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')).join(', '):'sin header'})()")
        add('Estructura HTML','Hijos de header (orden del árbol)','a, nav#menu-principal, button#btn-menu',hdr,hdr=='a, nav#menu-principal, button#btn-menu')
        # ---------- F. móvil
        pm=b.new_page(viewport={'width':390,'height':844}); pm.goto(url); pm.wait_for_timeout(300)
        def mchk(crit,sel,prop,exp):
            r=pm.evaluate(JS_STYLE,[sel,[prop]])
            if r is None: add('Móvil (390 px)',crit,exp,'elemento no existe (%s)'%sel,False); return
            add('Móvil (390 px)',crit,exp,r[prop],r[prop]==exp)
        mchk('H1 baja a 40 px','h1','font-size','40px'); mchk('H2 baja a 30 px','h2','font-size','30px'); mchk('H3 sigue en 22 px','h3','font-size','22px')
        mchk('Botón de menú visible','#btn-menu','display','block')
        mchk('Menú colapsado por defecto','#menu-principal','display','none')
        ov=pm.evaluate("document.documentElement.scrollWidth<=window.innerWidth")
        add('Móvil (390 px)','Sin desplazamiento horizontal','sí',('sí' if ov else 'no'),ov)
        if pm.query_selector('#btn-menu'):
            pm.click('#btn-menu'); pm.wait_for_timeout(100)
            r=pm.evaluate("[document.getElementById('btn-menu').getAttribute('aria-expanded'),getComputedStyle(document.getElementById('menu-principal')).display]")
            add('Móvil (390 px)','Al pulsar el botón: aria-expanded=true y menú visible','true / block',' / '.join(r),r==['true','block'])
        else: add('Móvil (390 px)','Al pulsar el botón: aria-expanded=true y menú visible','true / block','elemento no existe (#btn-menu)',False)
        pg.screenshot(path=sys.argv[2],full_page=True)
        b.close()
    return rows
rows=run(sys.argv[1])
json.dump(rows,open(sys.argv[3],'w'),ensure_ascii=False,indent=1)
from collections import Counter
print(sys.argv[1],Counter(r['status'] for r in rows))
for c in dict.fromkeys(r['cat'] for r in rows): print(' ',c,Counter(r['status'] for r in rows if r['cat']==c))
