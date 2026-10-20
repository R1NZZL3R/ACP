import os
import sys, json
from playwright.sync_api import sync_playwright
JS="""(spec)=>{const out=[];const R=s=>[...document.querySelectorAll(s)].map(e=>e.getBoundingClientRect());return R(spec)}"""
def rects(pg,s): return pg.evaluate("s=>[...document.querySelectorAll(s)].map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y+scrollY,w:r.width,h:r.height}})",s)
def run(url):
    rows=[]
    def add(crit,exp,found,ok): rows.append(dict(cat='Prototipo',crit=crit,exp=exp,found=found,status='cumple' if ok else 'no cumple'))
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or None)
        for w,h,mob in ((1440,900,False),(390,844,True)):
            pg=b.new_page(viewport={'width':w,'height':h}); pg.goto(url); pg.wait_for_timeout(200)
            tag=' (móvil 390 px)' if mob else ' (escritorio 1440 px)'
            t=rects(pg,'#funciones .tarjeta'); 
            if mob:
                ok=len(t)==4 and all(abs(t[i]['x']-t[0]['x'])<2 for i in range(4)) and all(t[i]['y']<t[i+1]['y'] for i in range(3))
                add('Tarjetas de funciones apiladas'+tag,'4 tarjetas una bajo otra (wireframe 1j)',f'{len(t)} tarjetas, '+('apiladas' if ok else 'no apiladas'),ok)
            else:
                ok=len(t)==4 and len({round(x['y']) for x in t})==1
                add('Tarjetas de funciones en una fila'+tag,'4 tarjetas en una fila (wireframe 1a)',f'{len(t)} tarjetas, '+('en una fila' if ok else 'no están en una fila'),ok)
            hs=rects(pg,'#hero h1'); il=rects(pg,'#hero .ilustracion')
            if hs and il:
                if mob: ok=il[0]['y']>hs[0]['y']+hs[0]['h']; add('Hero: ilustración'+tag,'debajo del texto (wireframe 1j)','debajo' if ok else 'al lado',ok)
                else: ok=il[0]['x']>hs[0]['x']+hs[0]['w']-5; add('Hero: texto a la izquierda, mascota a la derecha'+tag,'dos columnas (wireframe 1a)','dos columnas' if ok else 'una columna',ok)
            else: add('Hero: texto e ilustración'+tag,'texto + mascota','elementos no existen',False)
            bt=rects(pg,'#hero .boton')
            if len(bt)==2:
                if mob: ok=all(abs(x['w']-bt[0]['w'])<2 for x in bt) and bt[0]['w']>300; add('Botones del hero a todo el ancho'+tag,'[Comenzar] y [Ver cómo funciona] a lo ancho (wireframe 1j)',f"anchos {round(bt[0]['w'])} y {round(bt[1]['w'])} px",ok)
                else: ok=abs(bt[0]['y']-bt[1]['y'])<2 and bt[1]['x']>bt[0]['x']; add('Botones del hero lado a lado'+tag,'[Comenzar] [Ver cómo funciona] en una fila (wireframe 1a)','en una fila' if ok else 'apilados',ok)
            else: add('Botones del hero'+tag,'2 botones','%d botones'%len(bt),False)
            if not mob:
                ps=rects(pg,'.paso'); ok=len(ps)==4 and len({round(x['y']) for x in ps})==1; add('Cuatro pasos en una fila'+tag,'(1) Subir ─ (2) Detectar ─ (3) Desplegar ─ (4) Acceder',f'{len(ps)} pasos, '+('en una fila' if ok else 'no están en una fila'),ok)
                ph=rects(pg,'#cta h2'); pb=rects(pg,'#cta .boton'); ok=bool(ph and pb and abs((ph[0]['y']+ph[0]['h']/2)-(pb[0]['y']+pb[0]['h']/2))<8 and pb[0]['x']>ph[0]['x']); add('Banda de cierre: título y botón en una fila'+tag,'título + [Comenzar] sobre fondo oscuro (wireframe 1a)','en una fila' if ok else 'no existe o apilados',ok)
                hd=rects(pg,'#encabezado .logo'); mn=rects(pg,'#menu-principal'); ok=bool(hd and mn and hd[0]['x']<mn[0]['x'] and mn[0]['y']<100); add('Encabezado: logo a la izquierda, menú a la derecha'+tag,'[Logo] ... menú + [Iniciar sesión] (wireframe 1a)','correcto' if ok else 'no existe o distinto',ok)
                nav=rects(pg,'#menu-pie'); lg=rects(pg,'#pie .logo'); ok=bool(nav and lg and lg[0]['x']<nav[0]['x']); add('Pie: logo a la izquierda, enlaces a su derecha'+tag,'[Logo] enlaces · © (wireframe 1a)','correcto' if ok else 'no existe o distinto',ok)
    return rows
r=run(sys.argv[1]); json.dump(r,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print(sum(x['status']=='cumple' for x in r),len(r))
