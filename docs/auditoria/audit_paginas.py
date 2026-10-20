import sys, json, os
from playwright.sync_api import sync_playwright
BASE=sys.argv[1]  # p.ej. http://127.0.0.1:8765
OUT=sys.argv[2]
def rgb(h):
    h=h.lstrip('#'); return 'rgb(%d, %d, %d)'%(int(h[0:2],16),int(h[2:4],16),int(h[4:6],16))
COMMON=[('header#encabezado',1),('header#encabezado > a.logo[href="/"] > img[alt="Logo de ApeByte"]',1),('header > nav#menu-principal[aria-label="Principal"]',1),
 ('nav#menu-principal ul > li > a.enlace-menu',6),('nav#menu-principal li.item-sesion > a.boton.boton-primario[href="/login"]',1),('header > button#btn-menu',1),
 ('body > main#contenido',1),('body > footer#pie',1),('footer#pie > a.logo > img[alt="Logo de ApeByte"]',1),('footer#pie > nav#menu-pie[aria-label="Enlaces secundarios"]',1),
 ('nav#menu-pie ul > li > a.enlace-pie',4),('footer#pie > p.derechos',1)]
PAGES={
'caracteristicas':('/caracteristicas','Características',[
 ('Introducción','section#intro > h1',1),('Introducción: párrafo','section#intro > p',1),('Contenedor con barra','main#contenido > div.con-barra',1),
 ('Índice lateral','div.con-barra > aside#indice > p.titulo-indice',1),('Navegación del índice','aside#indice > nav[aria-label="Índice de características"] ul > li > a.enlace-indice',6),
 ('Bloques','div.bloques > article.bloque',6),('Anclas #zip-git, #deteccion, #docker, #bases-de-datos, #traefik, #logs','article.bloque#zip-git, article.bloque#deteccion, article.bloque#docker, article.bloque#bases-de-datos, article.bloque#traefik, article.bloque#logs',6),
 ('Bloques con h2','article.bloque > h2',6),('Bloques con p','article.bloque > p',6),('Bloques con img','article.bloque > img',6),('h1 en toda la página','h1',1)]),
'como-funciona':('/como-funciona','Cómo funciona',[
 ('Introducción','section#intro > h1',1),('Introducción: párrafo','section#intro > p',1),('Stepper','main#contenido > ol#pasos.stepper',1),('Pasos','ol#pasos > li.paso',4),
 ('Tarjetas de paso','li.paso > article.tarjeta-paso',4),('Con img.icono','article.tarjeta-paso > img.icono',4),('Con h2','article.tarjeta-paso > h2',4),('Con p','article.tarjeta-paso > p',4),('Con img.ilustracion','article.tarjeta-paso > img.ilustracion',4),('h1 en toda la página','h1',1)]),
'tecnologias':('/tecnologias','Tecnologías',[
 ('Introducción','section#intro > h1',1),('Lenguajes: h2','section#lenguajes > h2',1),('Lenguajes: tarjetas','section#lenguajes div.cuadricula > article.tarjeta',8),
 ('Bases de datos: h2','section#bases-de-datos > h2',1),('Bases de datos: tarjetas','section#bases-de-datos div.cuadricula > article.tarjeta',3),
 ('Tarjetas con img.logo-tec','article.tarjeta > img.logo-tec',11),('Tarjetas con h3','article.tarjeta > h3',11),('Tarjetas con p','article.tarjeta > p',11),('h1 en toda la página','h1',1)]),
'documentacion':('/documentacion','Documentación',[
 ('Contenedor con barra','main#contenido > div.con-barra',1),('Índice: título','aside#indice > p.titulo-indice',1),('Índice: enlaces','aside#indice > nav[aria-label="Documentación"] ul > li > a.enlace-indice',3),
 ('Artículo con h1','article#documento > h1',1),('Secciones con id','article#documento > section#guia-de-inicio, article#documento > section#requisitos, article#documento > section#preguntas-frecuentes',3),
 ('Guía: h2, h3','#guia-de-inicio > h2, #guia-de-inicio > h3',2),('Bloque de código con botón copiar','div.bloque-codigo > button.boton-copiar',1),('Bloque de código: pre > code','div.bloque-codigo > pre > code',1),
 ('Requisitos: h2','#requisitos > h2',1),('Preguntas: elementos','#preguntas-frecuentes div.faq-item',4),('Preguntas: h3 > button colapsado','h3 > button.faq-pregunta[aria-expanded="false"]',4),('Respuestas ocultas','p.faq-respuesta[hidden]',4),('h1 en toda la página','h1',1)]),
'acerca-de':('/acerca-de','Acerca de',[
 ('Qué es: h1','section#que-es > h1',1),('Qué es: párrafo','section#que-es > p',1),('Qué es: ilustración con alt','section#que-es img.ilustracion[alt]',1),
 ('Equipo: h2','section#equipo > h2',1),('Tarjetas de persona','section#equipo article.tarjeta-persona',2),('Fotos con alt "Foto de …"','article.tarjeta-persona > img.foto[alt^="Foto de"]',2),('Persona: h3 y p','article.tarjeta-persona > h3, article.tarjeta-persona > p',4),
 ('Cronograma: h2','section#cronograma > h2',1),('Línea de tiempo','section#cronograma > ol.linea-tiempo > li.fase',7),('Fases con h3 y p','li.fase > h3, li.fase > p',14),('h1 en toda la página','h1',1),('h2 en toda la página (equipo y cronograma)','h2',2)]),
'contacto':('/contacto','Contacto',[
 ('h1 dentro de main','main#contenido > h1',1),('Dos columnas','main#contenido > div.dos-columnas',1),('Datos: h2','section#datos > h2',1),('Datos de contacto','ul.lista-datos > li.dato',3),('Dato con icono, h3 y p','li.dato > img.icono, li.dato > h3, li.dato > p',9),
 ('Formulario: h2','section#formulario > h2',1),('form#form-contacto[novalidate]','section#formulario > form#form-contacto[novalidate]',1),('Campos','form#form-contacto > div.campo',4),
 ('Ids de campos','#campo-nombre, #campo-correo, #campo-asunto, #campo-mensaje',4),('Etiquetas con for','div.campo > label[for]',4),('Textarea en mensaje','textarea#campo-mensaje',1),
 ('Errores ocultos bajo cada campo','div.campo > p.mensaje-error[hidden]',4),('Botón Enviar','button#btn-enviar.boton.boton-primario',1),('Mensaje de éxito oculto','section#formulario > p#mensaje-exito.mensaje-exito[hidden]',1),('h1 en toda la página','h1',1)]),
'login':('/login','Iniciar sesión',[
 ('Tarjeta de acceso','main#contenido > section#acceso.tarjeta-acceso',1),('h1 solo para lectores','h1.solo-lectores',1),('Mascota con alt','img.mascota[alt="Mascota de ApeByte"]',1),('Pestañas (tablist)','div.pestanas[role="tablist"]',1),
 ('Botones de pestaña','button#tab-login.pestana, button#tab-registro.pestana',2),('Formulario de inicio','form#form-login[role="tabpanel"]',1),('Campos de inicio','#campo-login-usuario, #campo-login-clave',2),
 ('Error de inicio oculto','p#error-login.mensaje-error[hidden]',1),('Botón Entrar','button#btn-entrar.boton.boton-primario',1),('Enlace ¿Olvidaste tu contraseña?','form#form-login > a',1),
 ('Formulario de registro oculto','form#form-registro[role="tabpanel"][hidden]',1),('Campos de registro','#campo-registro-nombre, #campo-registro-correo, #campo-registro-clave, #campo-registro-clave2',4),
 ('Error de registro oculto','p#error-registro.mensaje-error[hidden]',1),('Botón Crear cuenta','button#btn-crear-cuenta.boton.boton-primario',1),('Etiquetas con for','form label[for]',6),('h1 en toda la página','h1',1)]),
'privacidad':('/privacidad','Aviso de privacidad',[
 ('Artículo legal','main#contenido > article#documento-legal.lectura',1),('h1','article#documento-legal > h1',1),('Fecha de actualización','article#documento-legal > p.fecha-actualizacion',1),('Cláusulas','article#documento-legal > section.clausula',4),('Cláusulas con h2 y p','section.clausula > h2, section.clausula > p',8),('h1 en toda la página','h1',1)]),
'terminos':('/terminos','Términos de uso',[
 ('Artículo legal','main#contenido > article#documento-legal.lectura',1),('h1','article#documento-legal > h1',1),('Fecha de actualización','article#documento-legal > p.fecha-actualizacion',1),('Cláusulas','article#documento-legal > section.clausula',4),('Cláusulas con h2 y p','section.clausula > h2, section.clausula > p',8),('h1 en toda la página','h1',1)]),
}
rows=[]
def add(pag,cat,crit,exp,found,ok): rows.append(dict(pagina=pag,cat=cat,crit=crit,exp=str(exp),found=str(found),status='cumple' if ok else 'no cumple'))
def sty(pg,sel,prop):
    return pg.evaluate("([s,p])=>{const e=document.querySelector(s);return e?getComputedStyle(e).getPropertyValue(p):null}",[sel,prop])
def rect(pg,sel):
    return pg.evaluate("s=>[...document.querySelectorAll(s)].map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y+scrollY,w:r.width,h:r.height}})",sel)
def chk(pg,page,cat,crit,sel,prop,exp):
    v=sty(pg,sel,prop); add(page,cat,crit,exp,v if v is not None else 'elemento no existe',v==exp)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or None)
    ctx=b.new_context(viewport={'width':1440,'height':900},permissions=['clipboard-read','clipboard-write'])
    pg=ctx.new_page()
    for name,(ruta,nombre,spec) in PAGES.items():
        pg.goto(BASE+ruta); pg.wait_for_timeout(150)
        # comunes
        fallos=[s+' ×%d'%n for s,n in COMMON if pg.evaluate("s=>document.querySelectorAll(s).length",s)!=n]
        add(name,'Estructura HTML','Encabezado y pie comunes (%d nodos del árbol)'%len(COMMON),'%d de %d'%(len(COMMON),len(COMMON)),'%d de %d'%(len(COMMON)-len(fallos),len(COMMON))+('' if not fallos else ' (faltan: '+'; '.join(fallos)+')'),not fallos)
        cur=pg.evaluate("[...document.querySelectorAll('a[aria-current=\"page\"]')].map(a=>a.textContent.trim())")
        esperado=[nombre] if nombre in [m[0] for m in [('Características',),('Cómo funciona',),('Tecnologías',),('Documentación',),('Acerca de',),('Contacto',)]] else []
        add(name,'Estructura HTML','Ítem activo del menú (aria-current="page")',(esperado[0] if esperado else 'ninguno'),(cur[0] if cur else 'ninguno') if len(cur)<=1 else str(cur),cur==esperado)
        for crit,sel,n in spec:
            f=pg.evaluate("s=>document.querySelectorAll(s).length",sel)
            add(name,'Estructura HTML',crit,'%d × %s'%(n,sel if len(sel)<70 else sel[:67]+'…'),'%d'%f,f==n)
        # enlaces del índice apuntan a un ancla existente
        if name in('caracteristicas','documentacion'):
            n=pg.evaluate("[...document.querySelectorAll('a.enlace-indice')].filter(a=>document.getElementById(a.getAttribute('href').slice(1))).length")
            t=pg.evaluate("document.querySelectorAll('a.enlace-indice').length")
            add(name,'Estructura HTML','Cada enlace del índice apunta a un ancla existente',f'{t} de {t}',f'{n} de {t}',n==t)
        # alt de imágenes con significado
        sinalt=pg.evaluate("[...document.querySelectorAll('img:not([alt])')].length")
        add(name,'Accesibilidad','Todas las imágenes tienen atributo alt','0 sin alt',f'{sinalt} sin alt',sinalt==0)
        ov=pg.evaluate("document.documentElement.scrollWidth<=innerWidth")
        add(name,'Maquetación','Sin desplazamiento horizontal (1440 px)','sí','sí' if ov else 'no',ov)
        # --- estilos y maquetación por página
        P=name
        if P=='caracteristicas':
            chk(pg,P,'Maquetación','Índice fijo (sticky)','#indice','position','sticky')
            im=rect(pg,'article.bloque > img'); tx=rect(pg,'article.bloque > h2')
            alt=[(im[i]['x']<tx[i]['x']) for i in range(6)]
            add(P,'Maquetación','Imagen alterna izquierda/derecha','izq, der, izq, der, izq, der',', '.join('izq' if a else 'der' for a in alt),alt==[True,False,True,False,True,False])
            ar=rect(pg,'aside#indice')[0]; bl=rect(pg,'.bloques')[0]
            add(P,'Maquetación','Índice a la izquierda de los bloques','índice a la izquierda',('a la izquierda' if ar['x']+ar['w']<=bl['x'] else 'no'),ar['x']+ar['w']<=bl['x'])
        if P=='como-funciona':
            ps=rect(pg,'.stepper > .paso'); ok=all(ps[i]['y']<ps[i+1]['y'] for i in range(3))
            add(P,'Maquetación','Stepper vertical (4 pasos uno bajo otro)','vertical','vertical' if ok else 'no',ok)
            nums=pg.evaluate("[...document.querySelectorAll('.stepper > .paso')].map(e=>getComputedStyle(e,'::before').content)")
            inc=pg.evaluate("getComputedStyle(document.querySelector('.stepper > .paso')).counterIncrement")
            add(P,'Maquetación','Número de cada paso generado por CSS (contador de ol)','content: counter(paso) en los 4 pasos',f"content: {nums[0]} en {len(nums)} pasos; counter-increment: {inc}",nums==['counter(paso)']*4 and inc=='paso 1')
            tp=rect(pg,'.tarjeta-paso')[0]; il=rect(pg,'.tarjeta-paso .ilustracion')[0]; ic=rect(pg,'.tarjeta-paso h2')[0]
            add(P,'Maquetación','Ilustración a la derecha del texto','derecha',('derecha' if il['x']>ic['x'] else 'no'),il['x']>ic['x'])
            chk(pg,P,'Colores','Tarjeta de paso: borde','.tarjeta-paso','border-top-color',rgb('#AEB5C2'))
            chk(pg,P,'Espaciados','Tarjeta de paso: padding 24 px','.tarjeta-paso','padding-top','24px')
        if P=='tecnologias':
            t=rect(pg,'#lenguajes .tarjeta'); f1=[x for x in t if abs(x['y']-t[0]['y'])<2]; 
            add(P,'Maquetación','Lenguajes en cuadrícula de 4 columnas','4 por fila',f'{len(f1)} por fila',len(f1)==4 and len(t)==8)
            d=rect(pg,'#bases-de-datos .tarjeta'); add(P,'Maquetación','Bases de datos: 3 tarjetas en una fila','3 en una fila',f'{len([x for x in d if abs(x["y"]-d[0]["y"])<2])} en una fila',len({round(x['y']) for x in d})==1)
            chk(pg,P,'Espaciados','Tarjeta: padding 24 px (misma clase .tarjeta que Home)','.tarjeta','padding-top','24px')
            chk(pg,P,'Íconos','Logo de tecnología: 56 px','img.logo-tec','width','56px')
            chk(pg,P,'Colores','Sección blanca en los wireframes (bases de datos): sin fondo','#contenido > section#bases-de-datos','background-color','rgba(0, 0, 0, 0)')
        if P=='documentacion':
            chk(pg,P,'Colores','Bloque de código: fondo azul marino','.bloque-codigo','background-color',rgb('#0B1530'))
            fam=sty(pg,'.bloque-codigo code','font-family'); add(P,'Tipografía','Bloque de código: fuente monoespaciada','"Cascadia Mono", Consolas, "Courier New", monospace',fam,fam.replace("'",'"')=='"Cascadia Mono", Consolas, "Courier New", monospace')
            chk(pg,P,'Maquetación','Índice fijo (sticky)','#indice','position','sticky')
            chk(pg,P,'Tipografía','Título de sección H2: 36 px','#documento h2','font-size','36px')
        if P=='acerca-de':
            ph=rect(pg,'.fase'); add(P,'Maquetación','Línea de tiempo horizontal de 7 fases','7 en una fila',f'{len([x for x in ph if abs(x["y"]-ph[0]["y"])<2])} en una fila',len({round(x['y']) for x in ph})==1 and len(ph)==7)
            pe=rect(pg,'.tarjeta-persona'); add(P,'Maquetación','2 tarjetas de persona en una fila','2 en una fila',f'{len({round(x["y"]) for x in pe})} fila(s)',len({round(x['y']) for x in pe})==1)
            chk(pg,P,'Colores','Tarjeta de persona: borde','.tarjeta-persona','border-top-color',rgb('#AEB5C2'))
        if P=='contacto':
            dd=rect(pg,'#datos')[0]; ff=rect(pg,'#formulario')[0]; add(P,'Maquetación','Datos a la izquierda y formulario a la derecha','dos columnas',('dos columnas' if ff['x']>dd['x']+dd['w']-5 else 'no'),ff['x']>dd['x']+dd['w']-5)
            chk(pg,P,'Campos','Campo: borde','#campo-nombre','border-top-color',rgb('#8B93A3'))
            chk(pg,P,'Campos','Campo: esquinas 8 px','#campo-nombre','border-top-left-radius','8px')
            chk(pg,P,'Campos','Campo: altura mínima 44 px','#campo-nombre','min-height','44px')
            chk(pg,P,'Campos','Campo: texto 16 px','#campo-nombre','font-size','16px')
            chk(pg,P,'Botones','Enviar deshabilitado: fondo #D5DAE3','#btn-enviar','background-color',rgb('#D5DAE3'))
            chk(pg,P,'Botones','Enviar deshabilitado: texto #5F6778','#btn-enviar','color',rgb('#5F6778'))
            chk(pg,P,'Botones','Enviar deshabilitado: cursor not-allowed','#btn-enviar','cursor','not-allowed')
            # comportamiento
            dis0=pg.evaluate("document.getElementById('btn-enviar').disabled"); add(P,'JavaScript','Enviar deshabilitado al cargar','deshabilitado','deshabilitado' if dis0 else 'habilitado',dis0)
            pg.fill('#campo-nombre','Ana'); pg.fill('#campo-correo','correo-invalido'); pg.fill('#campo-asunto','Hola'); pg.fill('#campo-mensaje','Mensaje de prueba largo'); pg.wait_for_timeout(50)
            err=pg.evaluate("(()=>{const e=document.querySelector('#campo-correo').closest('.campo').querySelector('.mensaje-error');return [e.hidden,e.textContent]})()")
            add(P,'JavaScript','Correo inválido: error visible bajo el campo','visible, con mensaje',('visible: '+err[1]) if not err[0] else 'oculto',(not err[0]) and bool(err[1]))
            add(P,'JavaScript','Correo inválido: Enviar sigue deshabilitado','deshabilitado','deshabilitado' if pg.evaluate("document.getElementById('btn-enviar').disabled") else 'habilitado',pg.evaluate("document.getElementById('btn-enviar').disabled"))
            col=pg.evaluate("getComputedStyle(document.querySelector('#campo-correo').closest('.campo').querySelector('.mensaje-error')).color"); add(P,'JavaScript','Color del mensaje de error #C93535',rgb('#C93535'),col,col==rgb('#C93535'))
            pg.fill('#campo-correo','ana@correo.com'); pg.wait_for_timeout(50)
            en=not pg.evaluate("document.getElementById('btn-enviar').disabled"); add(P,'JavaScript','Formulario válido: Enviar se habilita','habilitado','habilitado' if en else 'deshabilitado',en)
            ex0=pg.evaluate("document.getElementById('mensaje-exito').hidden"); add(P,'JavaScript','Mensaje de éxito oculto antes de enviar','oculto','oculto' if ex0 else 'visible',ex0)
            pg.click('#btn-enviar'); pg.wait_for_timeout(80)
            ex=pg.evaluate("[!document.getElementById('mensaje-exito').hidden,document.getElementById('campo-nombre').value,document.getElementById('btn-enviar').disabled]")
            add(P,'JavaScript','Al enviar: aparece "Mensaje enviado", se limpia el formulario y Enviar vuelve a deshabilitarse','éxito visible, campos vacíos, botón deshabilitado',f'éxito {"visible" if ex[0] else "oculto"}, nombre "{ex[1]}", botón {"deshabilitado" if ex[2] else "habilitado"}',ex[0] and ex[1]=='' and ex[2])
            col=sty(pg,'#mensaje-exito','color'); add(P,'Colores','Mensaje de éxito #1A7F4F',rgb('#1A7F4F'),col,col==rgb('#1A7F4F'))
        if P=='login':
            chk(pg,P,'Colores','Fondo de la pantalla de login #F3F5F9','#contenido','background-color',rgb('#F3F5F9'))
            c=rect(pg,'#acceso')[0]; add(P,'Maquetación','Tarjeta centrada de 440 px de ancho','440 px, centrada',f"{round(c['w'])} px, {'centrada' if abs((c['x']+c['w']/2)-720)<2 else 'no centrada'}",abs(c['w']-440)<2 and abs((c['x']+c['w']/2)-720)<2)
            chk(pg,P,'Espaciados','Tarjeta: esquinas 12 px','#acceso','border-top-left-radius','12px')
            chk(pg,P,'Botones','Pestaña activa: azul marino','#tab-login','color',rgb('#0B1530'))
            chk(pg,P,'Botones','Entrar: ancho completo y estilo primario','#btn-entrar','background-color',rgb('#1A6FF0'))
            chk(pg,P,'Tipografía','h1.solo-lectores oculto a la vista (1 px)','h1.solo-lectores','width','1px')
            s0=pg.evaluate("[document.getElementById('tab-login').getAttribute('aria-selected'),document.getElementById('form-login').hidden,document.getElementById('form-registro').hidden]")
            add(P,'JavaScript','Estado inicial: "Iniciar sesión" activa, registro oculto','true, login visible, registro oculto',f'{s0[0]}, login {"oculto" if s0[1] else "visible"}, registro {"oculto" if s0[2] else "visible"}',s0==['true',False,True])
            pg.click('#form-login #btn-entrar'); pg.wait_for_timeout(60)
            e=pg.evaluate("[document.getElementById('error-login').hidden,document.getElementById('error-login').textContent]")
            add(P,'JavaScript','Entrar con campos vacíos: error en línea','error visible',('visible: '+e[1]) if not e[0] else 'oculto',not e[0])
            pg.fill('#campo-login-usuario','ana'); pg.wait_for_timeout(40)
            add(P,'JavaScript','Al escribir, el error desaparece','oculto','oculto' if pg.evaluate("document.getElementById('error-login').hidden") else 'visible',pg.evaluate("document.getElementById('error-login').hidden"))
            pg.fill('#campo-login-clave','1234'); pg.click('#btn-entrar'); 
            dd=pg.evaluate("document.getElementById('btn-entrar').disabled"); add(P,'JavaScript','Envío válido: botón deshabilitado mientras envía','deshabilitado','deshabilitado' if dd else 'habilitado',dd)
            pg.wait_for_timeout(1000); add(P,'JavaScript','Después del envío el botón se habilita de nuevo','habilitado','habilitado' if not pg.evaluate("document.getElementById('btn-entrar').disabled") else 'deshabilitado',not pg.evaluate("document.getElementById('btn-entrar').disabled"))
            pg.click('#tab-registro'); pg.wait_for_timeout(40)
            s1=pg.evaluate("[document.getElementById('tab-registro').getAttribute('aria-selected'),document.getElementById('tab-login').getAttribute('aria-selected'),document.getElementById('form-login').hidden,document.getElementById('form-registro').hidden]")
            add(P,'JavaScript','Pestaña "Crear cuenta": alterna formularios y aria-selected','registro visible, login oculto, aria-selected true/false',f'registro {"oculto" if s1[3] else "visible"}, login {"oculto" if s1[2] else "visible"}, aria-selected {s1[0]}/{s1[1]}',s1==['true','false',True,False])
            pg.fill('#campo-registro-nombre','Ana'); pg.fill('#campo-registro-correo','ana@correo.com'); pg.fill('#campo-registro-clave','abc12345'); pg.fill('#campo-registro-clave2','distinta'); pg.click('#btn-crear-cuenta'); pg.wait_for_timeout(60)
            e=pg.evaluate("[document.getElementById('error-registro').hidden,document.getElementById('error-registro').textContent]")
            add(P,'JavaScript','Contraseñas distintas: "Las contraseñas no coinciden."','Las contraseñas no coinciden.',(e[1] if not e[0] else 'oculto'),(not e[0]) and e[1]=='Las contraseñas no coinciden.')
            pg.focus('#tab-registro'); pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(40)
            add(P,'JavaScript','Teclado: flecha izquierda vuelve a "Iniciar sesión"','true',pg.evaluate("document.getElementById('tab-login').getAttribute('aria-selected')"),pg.evaluate("document.getElementById('tab-login').getAttribute('aria-selected')")=='true')
        if P in('privacidad','terminos'):
            w_=rect(pg,'#documento-legal')[0]; add(P,'Maquetación','Columna de lectura de 800 px','800 px',f"{round(w_['w'])} px",abs(w_['w']-800)<2 or abs(w_['w']-832)<2)
            chk(pg,P,'Colores','Fecha de actualización: texto suave','.fecha-actualizacion','color',rgb('#5F6778'))
    # --- documentación: índice, copiar, faq (con scroll)
    pg.goto(BASE+'/caracteristicas'); pg.wait_for_timeout(150)
    pg.evaluate("document.getElementById('docker').scrollIntoView()"); pg.wait_for_timeout(500)
    act=pg.evaluate("[...document.querySelectorAll('a.enlace-indice')].filter(a=>a.classList.contains('activo')).map(a=>a.getAttribute('href')+(a.getAttribute('aria-current')?' (aria-current)':''))")
    add('caracteristicas','JavaScript','Al bajar a Docker, el índice marca solo "Docker"','#docker (aria-current)',', '.join(act),act==['#docker (aria-current)'])
    pg.click('a.enlace-indice[href="#logs"]'); pg.wait_for_timeout(900); y=pg.evaluate("scrollY")
    add('caracteristicas','JavaScript','Clic en un enlace del índice lleva a su bloque','scroll hacia #logs',f'scrollY={round(y)}',y>800)
    pg.goto(BASE+'/documentacion'); pg.wait_for_timeout(150)
    pg.click('button.boton-copiar'); pg.wait_for_timeout(200)
    try: clip=pg.evaluate("navigator.clipboard.readText()")
    except Exception as e: clip='(no se pudo leer)'
    exp=pg.evaluate("document.querySelector('.bloque-codigo code').innerText")
    add('documentacion','JavaScript','Copiar: el portapapeles recibe el código','zip -r mi-proyecto.zip mi-proyecto/',clip,clip==exp)
    add('documentacion','JavaScript','Copiar: el botón dice "Copiado" un momento','Copiado',pg.evaluate("document.querySelector('.boton-copiar').textContent"),pg.evaluate("document.querySelector('.boton-copiar').textContent")=='Copiado')
    pg.click('button.faq-pregunta >> nth=0'); pg.wait_for_timeout(60)
    s=pg.evaluate("(()=>{const b=document.querySelector('button.faq-pregunta');const r=b.closest('.faq-item').querySelector('.faq-respuesta');return [b.getAttribute('aria-expanded'),r.hidden,getComputedStyle(r).display]})()")
    add('documentacion','JavaScript','Pregunta: al pulsar se abre (aria-expanded=true, respuesta visible)','true, visible',f'{s[0]}, {"oculta" if s[1] else "visible"}',s[0]=='true' and not s[1] and s[2]!='none')
    pg.click('button.faq-pregunta >> nth=0'); pg.wait_for_timeout(60)
    s=pg.evaluate("(()=>{const b=document.querySelector('button.faq-pregunta');const r=b.closest('.faq-item').querySelector('.faq-respuesta');return [b.getAttribute('aria-expanded'),r.hidden]})()")
    add('documentacion','JavaScript','Pregunta: al pulsar otra vez se cierra','false, oculta',f'{s[0]}, {"oculta" if s[1] else "visible"}',s[0]=='false' and s[1])
    pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(300)
    act=pg.evaluate("[...document.querySelectorAll('a.enlace-indice.activo')].map(a=>a.getAttribute('href'))")
    add('documentacion','JavaScript','Al cargar, el índice marca "Guía de inicio"','#guia-de-inicio',', '.join(act),act==['#guia-de-inicio'])
    pg.evaluate("scrollTo(0,document.documentElement.scrollHeight)"); pg.wait_for_timeout(300)
    act=pg.evaluate("[...document.querySelectorAll('a.enlace-indice.activo')].map(a=>a.getAttribute('href'))")
    add('documentacion','JavaScript','Al llegar al final, el índice marca "Preguntas frecuentes"','#preguntas-frecuentes',', '.join(act),act==['#preguntas-frecuentes'])
    # --- móvil
    pm=b.new_context(viewport={'width':390,'height':844}).new_page()
    for name,(ruta,nombre,spec) in PAGES.items():
        pm.goto(BASE+ruta); pm.wait_for_timeout(120)
        ov=pm.evaluate("document.documentElement.scrollWidth<=innerWidth"); add(name,'Móvil (390 px)','Sin desplazamiento horizontal','sí','sí' if ov else 'no',ov)
        vis=pm.evaluate("getComputedStyle(document.getElementById('btn-menu')).display"); col=pm.evaluate("getComputedStyle(document.getElementById('menu-principal')).display")
        pm.click('#btn-menu'); pm.wait_for_timeout(60)
        o=pm.evaluate("[document.getElementById('btn-menu').getAttribute('aria-expanded'),getComputedStyle(document.getElementById('menu-principal')).display,getComputedStyle(document.querySelector('.item-sesion .boton')).display]")
        add(name,'Móvil (390 px)','Menú hamburguesa: botón visible, menú colapsado y se abre al pulsar (con "Iniciar sesión" dentro)','block, none → true, block',f'{vis}, {col} → {o[0]}, {o[1]}',vis=='block' and col=='none' and o[0]=='true' and o[1]=='block')
        pf=pm.evaluate("[...document.querySelectorAll('#menu-pie li')].map(e=>e.getBoundingClientRect().y)"); ok=all(pf[i]<pf[i+1] for i in range(len(pf)-1))
        add(name,'Móvil (390 px)','Pie en una columna','enlaces apilados','apilados' if ok else 'en fila',ok)
        if name=='como-funciona':
            il=rect(pm,'.tarjeta-paso .ilustracion')[0]; tx=rect(pm,'.tarjeta-paso p')[0]; add(name,'Móvil (390 px)','Ilustración debajo del texto (1k)','debajo','debajo' if il['y']>tx['y'] else 'al lado',il['y']>tx['y'])
        if name=='login':
            c=rect(pm,'#acceso')[0]; add(name,'Móvil (390 px)','Tarjeta a todo el ancho con margen de 16 px (1l)','x=16, ancho 358',f"x={round(c['x'])}, ancho {round(c['w'])}",abs(c['x']-16)<1 and abs(c['w']-358)<1)
        if name in('caracteristicas','documentacion'):
            ia=rect(pm,'#indice')[0]; ct=rect(pm,'.bloques, #documento')[0]; add(name,'Móvil (390 px)','Índice encima del contenido (una columna)','una columna','una columna' if ct['y']>ia['y'] else 'dos columnas',ct['y']>ia['y'])
        if name=='acerca-de':
            ph=rect(pm,'.fase'); ok=all(ph[i]['y']<ph[i+1]['y'] for i in range(6)); add(name,'Móvil (390 px)','Línea de tiempo vertical','vertical','vertical' if ok else 'horizontal',ok)
        if name=='contacto':
            dd=rect(pm,'#datos')[0]; ff=rect(pm,'#formulario')[0]; add(name,'Móvil (390 px)','Una columna: datos y luego formulario','una columna','una columna' if ff['y']>dd['y'] else 'dos',ff['y']>dd['y'])
    b.close()
json.dump(rows,open(OUT,'w'),ensure_ascii=False,indent=1)
from collections import Counter
print(Counter(r['status'] for r in rows))
for pgn in dict.fromkeys(r['pagina'] for r in rows): print(pgn,Counter(r['status'] for r in rows if r['pagina']==pgn))
for r in rows:
    if r['status']!='cumple': print('FALLA',r['pagina'],r['crit'],'|',r['exp'],'|',r['found'])
