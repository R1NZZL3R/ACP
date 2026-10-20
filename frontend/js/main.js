// ApeByte Cloud Platform - comportamiento del sitio informativo.
// Cada función solo actúa si encuentra sus elementos en la página.

document.addEventListener("DOMContentLoaded", () => {
  iniciarEncabezado();
  iniciarMenu();
  iniciarIndice();
  iniciarCopiar();
  iniciarPreguntas();
  iniciarPasos();
  iniciarHistoria();
  iniciarEstados();
  iniciarRevelar(".stepper > .paso, #requisitos .tarjeta, .bloque");
  iniciarContacto();
  iniciarAcceso();
});

/* Encabezado: sombra cuando la página ya bajó (con IntersectionObserver, sin escuchar el scroll) */
function iniciarEncabezado() {
  const encabezado = document.getElementById("encabezado");
  if (!encabezado || !("IntersectionObserver" in window)) return;
  const centinela = document.createElement("div");
  centinela.className = "centinela-encabezado";
  centinela.setAttribute("aria-hidden", "true");
  document.body.prepend(centinela);
  new IntersectionObserver(([e]) => {
    encabezado.classList.toggle("con-sombra", !e.isIntersecting);
  }).observe(centinela);
}

/* Menú hamburguesa (solo móvil) */
function iniciarMenu() {
  const botonMenu = document.getElementById("btn-menu");
  const menu = document.getElementById("menu-principal");
  if (!botonMenu || !menu) return;

  const abrir = (abierto) => {
    menu.classList.toggle("abierto", abierto);
    botonMenu.setAttribute("aria-expanded", String(abierto));
    botonMenu.setAttribute("aria-label", abierto ? "Cerrar menú" : "Abrir menú");
  };

  botonMenu.addEventListener("click", () => abrir(!menu.classList.contains("abierto")));
  // Cerrar al elegir un enlace, con Escape o al tocar fuera del menú
  menu.addEventListener("click", (e) => {
    if (e.target.closest("a")) abrir(false);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu.classList.contains("abierto")) {
      abrir(false);
      botonMenu.focus();
    }
  });
  document.addEventListener("click", (e) => {
    if (menu.classList.contains("abierto") && !menu.contains(e.target) && !botonMenu.contains(e.target)) abrir(false);
  });
}

/* Índice lateral (Características y Documentación): marca la sección visible y muestra el progreso */
function iniciarIndice() {
  const enlaces = [...document.querySelectorAll("a.enlace-indice")];
  if (enlaces.length === 0) return;

  const secciones = enlaces.map((e) => document.getElementById(e.getAttribute("href").slice(1)));
  if (secciones.some((s) => !s)) return;

  const indice = document.getElementById("indice");
  const lista = enlaces[0].closest("ul");
  const titulo = indice && indice.querySelector(".titulo-indice");
  const suave = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Contador "2 de 6" y barra de progreso (solo existen si hay JavaScript)
  let contador = null;
  let relleno = null;
  if (titulo) {
    contador = document.createElement("span");
    contador.className = "indice-contador";
    contador.setAttribute("aria-hidden", "true");
    titulo.append(contador);
    const barra = document.createElement("div");
    barra.className = "indice-progreso";
    barra.setAttribute("aria-hidden", "true");
    relleno = document.createElement("span");
    barra.append(relleno);
    titulo.after(barra);
  }

  let actual = -1;
  const marcar = (indiceActivo) => {
    if (indiceActivo === actual) return;
    actual = indiceActivo;
    enlaces.forEach((e, i) => {
      e.classList.toggle("activo", i === indiceActivo);
      if (i === indiceActivo) e.setAttribute("aria-current", "true");
      else e.removeAttribute("aria-current");
    });
    if (contador) contador.textContent = `${indiceActivo + 1} de ${enlaces.length}`;
    if (relleno) relleno.style.transform = `scaleX(${(indiceActivo + 1) / enlaces.length})`;
    // En móvil el índice es una fila deslizable: mueve la opción activa a la vista
    if (lista && lista.scrollWidth > lista.clientWidth) {
      lista.scrollTo({ left: enlaces[indiceActivo].offsetLeft - 16, behavior: suave ? "smooth" : "auto" });
    }
  };

  if ("IntersectionObserver" in window) {
    // Una franja horizontal en el primer tercio de la ventana decide qué sección está activa
    const visibles = new Set();
    let pieVisible = false;
    const observador = new IntersectionObserver((entradas) => {
      entradas.forEach((e) => (e.isIntersecting ? visibles.add(e.target) : visibles.delete(e.target)));
      if (pieVisible) return marcar(secciones.length - 1);
      const i = secciones.findIndex((s) => visibles.has(s));
      if (i !== -1) marcar(i);
    }, { rootMargin: "-25% 0px -65% 0px" });
    secciones.forEach((s) => observador.observe(s));

    // Al llegar al pie de página, la última sección queda activa
    const pie = document.getElementById("pie");
    if (pie) {
      new IntersectionObserver(([e]) => {
        pieVisible = e.isIntersecting;
        if (pieVisible) marcar(secciones.length - 1);
      }).observe(pie);
    }
  }

  enlaces.forEach((e, i) => e.addEventListener("click", () => marcar(i)));
  marcar(0);
}

/* Botón "Copiar" de los bloques de código */
function iniciarCopiar() {
  document.querySelectorAll("button.boton-copiar").forEach((boton) => {
    boton.addEventListener("click", async () => {
      const codigo = boton.closest(".bloque-codigo").querySelector("code").innerText;
      try {
        await navigator.clipboard.writeText(codigo);
      } catch (e) {
        // Respaldo para páginas sin HTTPS (red local): copiar con un campo temporal
        const temporal = document.createElement("textarea");
        temporal.value = codigo;
        document.body.appendChild(temporal);
        temporal.select();
        document.execCommand("copy");
        temporal.remove();
      }
      const original = boton.textContent;
      boton.textContent = "Copiado";
      setTimeout(() => (boton.textContent = original), 1500);
    });
  });
}

/* Preguntas frecuentes: buscador y filtro por tema (las preguntas funcionan sin JavaScript con <details>) */
function iniciarPreguntas() {
  const controles = document.querySelector(".faq-controles");
  const items = [...document.querySelectorAll(".faq-item")];
  if (!controles || items.length === 0) return;
  controles.hidden = false;

  const buscador = document.getElementById("faq-buscar");
  const filtros = [...controles.querySelectorAll(".faq-filtro")];
  const contador = document.getElementById("faq-contador");
  const vacio = document.getElementById("faq-vacio");
  const grupos = [...document.querySelectorAll(".faq-grupo")];
  const limpiar = (t) => t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
  const textos = new Map(items.map((i) => [i, limpiar(i.textContent)]));
  let tema = "todas";

  const aplicar = () => {
    const texto = limpiar(buscador.value);
    let total = 0;
    items.forEach((item) => {
      const coincide = (tema === "todas" || item.dataset.categoria === tema) && (!texto || textos.get(item).includes(texto));
      item.hidden = !coincide;
      if (coincide) total++;
    });
    grupos.forEach((g) => (g.hidden = !g.querySelector(".faq-item:not([hidden])")));
    // Con una búsqueda que deja pocas respuestas, se abren solas
    items.forEach((item) => {
      if (texto && total <= 3 && !item.hidden) item.open = true;
    });
    vacio.hidden = total > 0;
    contador.textContent = total === 1 ? "1 pregunta" : `${total} preguntas`;
  };

  buscador.addEventListener("input", aplicar);
  filtros.forEach((boton) => {
    boton.addEventListener("click", () => {
      tema = boton.dataset.filtro;
      filtros.forEach((b) => b.setAttribute("aria-pressed", String(b === boton)));
      aplicar();
    });
  });
  aplicar();
}

/* Pestañas con un panel por opción (pasos de ACP y tecnologías compatibles) */
function iniciarPasos() {
  iniciarSeleccion(".pasos > .paso");
  iniciarSeleccion(".tec-lista > .tec");
}

function iniciarSeleccion(selector) {
  const pestanas = [...document.querySelectorAll(selector)];
  if (pestanas.length === 0) return;

  const elegir = (indice, enfocar) => {
    pestanas.forEach((pestana, i) => {
      const activa = i === indice;
      pestana.setAttribute("aria-selected", String(activa));
      pestana.tabIndex = activa ? 0 : -1;
      document.getElementById(pestana.getAttribute("aria-controls")).hidden = !activa;
    });
    if (enfocar) pestanas[indice].focus();
  };

  pestanas.forEach((pestana, i) => {
    pestana.addEventListener("click", () => elegir(i, false));
    pestana.addEventListener("keydown", (e) => {
      const teclas = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
      if (e.key in teclas) {
        e.preventDefault();
        elegir((i + teclas[e.key] + pestanas.length) % pestanas.length, true);
      } else if (e.key === "Home") {
        e.preventDefault();
        elegir(0, true);
      } else if (e.key === "End") {
        e.preventDefault();
        elegir(pestanas.length - 1, true);
      }
    });
  });

  elegir(0, false);
}

/* Devuelve si una etapa (data-inicio / data-fin) ya pasó, está en curso o viene después */
function estadoPorFecha(el, [pasado, actual, futuro]) {
  const hoy = new Date();
  const inicio = new Date(el.dataset.inicio + "T00:00:00");
  const fin = new Date(el.dataset.fin + "T23:59:59");
  if (hoy > fin) return { clase: "hecho", texto: pasado };
  if (hoy >= inicio) return { clase: "en-curso", texto: actual };
  return { clase: "proximo", texto: futuro };
}

/* Características: indica en qué punto está la fase de cada función */
function iniciarEstados() {
  document.querySelectorAll(".bloque[data-inicio]").forEach((bloque) => {
    const etiqueta = bloque.querySelector(".estado-funcion");
    if (!etiqueta) return;
    const { clase, texto } = estadoPorFecha(bloque, ["Fase completada", "En desarrollo", "Próximamente"]);
    etiqueta.classList.add(clase);
    etiqueta.textContent = texto;
  });
}

/* Acerca de: marca cada capítulo según la fecha (completada, en curso, próxima) y lo muestra al llegar con el scroll */
function iniciarHistoria() {
  const capitulos = [...document.querySelectorAll(".historia > .capitulo")];
  if (capitulos.length === 0) return;

  capitulos.forEach((cap) => {
    const { clase, texto } = estadoPorFecha(cap, ["Completada", "En curso", "Próximamente"]);
    cap.classList.add(clase);
    cap.querySelector(".capitulo-estado").textContent = texto;
  });

  if (!("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("js");
  const observador = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("visible");
      observador.unobserve(e.target);
    });
  }, { threshold: 0.15 });
  capitulos.forEach((cap) => observador.observe(cap));
}

/* Aparición suave al llegar con el scroll (sin JavaScript todo se ve igual) */
function iniciarRevelar(selector) {
  const elementos = [...document.querySelectorAll(selector)];
  if (elementos.length === 0 || !("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("js");
  const observador = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("visible");
      observador.unobserve(e.target);
    });
  }, { threshold: 0.1 });
  elementos.forEach((el) => {
    el.classList.add("revelar");
    observador.observe(el);
  });
}

/* Utilidades de formularios */
const CORREO = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Envía JSON al backend Flask. Devuelve { ok, error }.
async function enviarJSON(ruta, datos) {
  try {
    const r = await fetch(ruta, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });
    const cuerpo = await r.json().catch(() => ({}));
    return r.ok ? { ok: true } : { ok: false, error: cuerpo.error || "No se pudo completar la solicitud." };
  } catch (e) {
    return { ok: false, error: "No hay conexión con el servidor." };
  }
}

function mostrarErrorCampo(campo, mensaje) {
  const caja = campo.closest(".campo");
  const error = caja.querySelector(".mensaje-error");
  if (!error.id) error.id = "error-" + campo.id;
  campo.setAttribute("aria-describedby", error.id);
  caja.classList.toggle("invalido", Boolean(mensaje));
  campo.setAttribute("aria-invalid", String(Boolean(mensaje)));
  error.textContent = mensaje;
  error.hidden = !mensaje;
}

/* Formulario de contacto */
function iniciarContacto() {
  const form = document.getElementById("form-contacto");
  if (!form) return;
  const boton = document.getElementById("btn-enviar");
  const exito = document.getElementById("mensaje-exito");
  const campos = [...form.querySelectorAll("input, textarea")];
  const tocados = new Set();

  const validar = (campo) => {
    const valor = campo.value.trim();
    if (campo.id === "campo-correo") {
      if (!valor) return "Escribe tu correo.";
      return CORREO.test(valor) ? "" : "Escribe un correo válido, por ejemplo nombre@dominio.com.";
    }
    if (campo.id === "campo-mensaje") {
      if (!valor) return "Escribe tu mensaje.";
      return valor.length >= 10 ? "" : "El mensaje debe tener al menos 10 caracteres.";
    }
    if (!valor) return campo.id === "campo-nombre" ? "Escribe tu nombre." : "Escribe el asunto.";
    return "";
  };

  const actualizar = () => {
    campos.forEach((c) => mostrarErrorCampo(c, tocados.has(c) ? validar(c) : ""));
    boton.disabled = campos.some((c) => validar(c) !== "");
  };

  campos.forEach((campo) => {
    campo.addEventListener("input", () => {
      tocados.add(campo);
      exito.hidden = true;
      actualizar();
    });
    campo.addEventListener("blur", () => {
      tocados.add(campo);
      actualizar();
    });
  });

  form.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    campos.forEach((c) => tocados.add(c));
    actualizar();
    if (boton.disabled) return;
    const datos = {
      nombre: form.querySelector("#campo-nombre").value,
      correo: form.querySelector("#campo-correo").value,
      asunto: form.querySelector("#campo-asunto").value,
      mensaje: form.querySelector("#campo-mensaje").value,
    };
    boton.disabled = true;
    const r = await enviarJSON("/api/contacto", datos);
    if (!r.ok) {
      mostrarErrorCampo(form.querySelector("#campo-mensaje"), r.error);
      boton.disabled = false;
      return;
    }
    exito.hidden = false;
    form.reset();
    tocados.clear();
    actualizar();
  });

  actualizar();
}

/* Pantalla de acceso: pestañas y validación */
function iniciarAcceso() {
  const tabLogin = document.getElementById("tab-login");
  const tabRegistro = document.getElementById("tab-registro");
  const formLogin = document.getElementById("form-login");
  const formRegistro = document.getElementById("form-registro");
  if (!tabLogin || !tabRegistro || !formLogin || !formRegistro) return;

  const pestanas = [
    { tab: tabLogin, form: formLogin },
    { tab: tabRegistro, form: formRegistro },
  ];
  const seleccionar = (destino, enfocar) => {
    pestanas.forEach(({ tab, form }) => {
      const activa = tab === destino;
      tab.setAttribute("aria-selected", String(activa));
      tab.tabIndex = activa ? 0 : -1;
      form.hidden = !activa;
    });
    if (enfocar) destino.focus();
  };
  pestanas.forEach(({ tab }) => {
    tab.addEventListener("click", () => seleccionar(tab, false));
    tab.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        seleccionar(tab === tabLogin ? tabRegistro : tabLogin, true);
      }
    });
  });

  const enviar = (form, error, boton, validar, ruta, datos, alExito) => {
    form.addEventListener("input", () => (error.hidden = true));
    form.addEventListener("submit", async (evento) => {
      evento.preventDefault();
      const mensaje = validar();
      error.textContent = mensaje;
      error.hidden = !mensaje;
      if (mensaje) return;
      boton.disabled = true;
      const r = await enviarJSON(ruta, datos());
      boton.disabled = false;
      if (!r.ok) {
        error.textContent = r.error;
        error.hidden = false;
        return;
      }
      alExito();
    });
  };

  const valor = (id) => document.getElementById(id).value.trim();

  enviar(formLogin, document.getElementById("error-login"), document.getElementById("btn-entrar"), () =>
    valor("campo-login-usuario") && document.getElementById("campo-login-clave").value
      ? ""
      : "Escribe tu usuario o correo y tu contraseña.",
    "/api/login",
    () => ({ usuario: valor("campo-login-usuario"), clave: document.getElementById("campo-login-clave").value }),
    () => {
      // TODO (fase del dashboard): redirigir al panel cuando exista
      window.location.href = "/";
    }
  );

  enviar(formRegistro, document.getElementById("error-registro"), document.getElementById("btn-crear-cuenta"), () => {
    const clave = document.getElementById("campo-registro-clave").value;
    const clave2 = document.getElementById("campo-registro-clave2").value;
    if (!valor("campo-registro-nombre") || !valor("campo-registro-correo") || !clave || !clave2) {
      return "Completa todos los campos.";
    }
    if (!CORREO.test(valor("campo-registro-correo"))) return "Escribe un correo válido.";
    if (clave !== clave2) return "Las contraseñas no coinciden.";
    return "";
  },
  "/api/registro",
  () => ({
    nombre: valor("campo-registro-nombre"),
    correo: valor("campo-registro-correo"),
    clave: document.getElementById("campo-registro-clave").value,
  }),
  () => {
    formRegistro.reset();
    seleccionar(tabLogin, true);
  });
}
