# Cómo se arma el informe mensual (instrucciones para Claude)

Destinataria: Dana, responsable de marketing. Español rioplatense (voseo), directo, concreto.

## Marca: Havanna La Pampa
- Datos: `data/havanna/AAAA-MM.json` (los genera la extracción del día 2).
- Resumen numérico: `python scripts/resumen.py havanna salida.json`.
- Plantilla de diseño: `plantillas/informe-havanna-2026-09.html` (cacao + dulce de leche, tipografías Gloock y Figtree). De la plantilla se toma SOLO la identidad visual; las secciones siguen la "Estructura común" de abajo.
- Informe publicado como artifact NUEVO con título `Havanna La Pampa · <Mes AAAA>` (ej. `Havanna La Pampa · Octubre 2026`), icono `chart`.
- Índice: artifact https://claude.ai/artifact/8EnAV5FFPWpCdhV3nMqYmh (plantilla en `plantillas/indice-havanna.html`). Leerlo con Artifact `read`, agregar el mes nuevo ARRIBA de la lista con link, dato de alcance IG y una frase de resumen, y republicar con ese `url`.

## Marca: Dynamis Neumáticos
- Datos: `data/dynamis/AAAA-MM.json`. Resumen: `python scripts/resumen.py dynamis salida.json`.
- Plantilla de diseño: `plantillas/informe-dynamis-2026-09.html` (asfalto + amarillo, tipografía Barlow). De la plantilla se toma SOLO la identidad visual; las secciones siguen la "Estructura común" de abajo.
- Informe publicado como artifact NUEVO con título `Dynamis Neumáticos · <Mes AAAA>`, icono `chart`.
- Índice: artifact https://claude.ai/artifact/LYHdSkrnR1f7bjdRCErTWi (plantilla `plantillas/indice-dynamis.html`).
- Cuenta activa desde mayo 2026 (Facebook) y junio 2026 (Instagram): no hay comparación interanual hasta junio 2027.
- Referencias de pauta: mensajes 11/9/2026 = $2.110 por conversación; interacción julio 2026 = $8.375.
- Marcas que vende: Dunlop (estrella, vía Grupo Corven), Corven y Continental. No mencionar la gomería.

## Marca: Grupo Agroenergía
- Datos: `data/agroenergia/AAAA-MM.json`. Facebook (página 360487924048263) e Instagram @grupo.agroenergia (leído vía graph.instagram.com con el secret META_TOKEN_AGROENERGIA_IG, token de inicio de sesión de Instagram que vence cada 60 días). Si Instagram trae error de token vencido, avisar a Dana que lo regenere en la app Informes mensuales → Casos de uso → API de Instagram → Configuración de la API con inicio de sesión de Instagram → Generar token, y actualice el secret.
- La página se lee con un token de página de Dana (no vence, pero Meta exige reconfirmar el acceso a datos cada 90 días). Si la extracción da error de permisos o de token, avisar a Dana que hay que renovarlo desde el Explorador de la API Graph (app Informes mensuales, Generate Access Token, ampliar, me/accounts) y actualizar el secret META_TOKEN_AGROENERGIA.
- La pauta sale de la cuenta publicitaria del portfolio Agroenergia (token de Havanna); usar solo anuncios con `es_de_la_marca: true`. Esa cuenta mezcla marcas.
- Métricas de página: `page_total_media_view_unique` (alcance, desde mayo 2025), `page_media_view` (visualizaciones), `page_post_engagements`, `page_follows` (total), `page_daily_follows_unique` / `page_daily_unfollows_unique` (altas y bajas).
- Plantilla: `plantillas/informe-agroenergia-2026-09.html` (verde agro + tierra, tipografías Archivo y Public Sans). Es el MODELO DE ESTRUCTURA para las tres marcas. Título `Grupo Agroenergía · <Mes AAAA>`, icono `chart`.
- Índice: artifact https://claude.ai/artifact/Cv8zFVEKmPrTmbk6bmg5L9 (plantilla `plantillas/indice-agroenergia.html`).
- Contexto: la cuenta reúne Shell, Axion, Puma, estaciones bandera blanca, lo institucional y los repartos al agro.

## Estructura común (obligatoria para las tres marcas)
Los tres informes tienen exactamente las mismas secciones, en este orden, con las mismas tablas y columnas. El modelo es el informe de Agroenergía; cada marca solo cambia colores y tipografías. Si una sección no tiene datos para una marca, NO se elimina: se deja el título con una línea que explique por qué (ej. "Sin pauta en el mes", "La cuenta no tiene un año de historia: sin comparación interanual").

0. Encabezado: marca, mes, seguidores actuales de Facebook (`perfil.followers_count`) e Instagram, fecha de extracción.
1. Lectura del mes: 3-4 conclusiones concretas basadas en los datos (qué pasó, por qué, qué publicaciones lo explican), cubriendo Instagram, Facebook, seguidores y pauta.
2. Facebook — KPIs: alcance (`page_total_media_view_unique`), visualizaciones (`page_media_view`), interacciones (`page_post_engagements`) y seguidores, cada uno vs mes anterior y vs mismo mes del año anterior. Nota debajo si hubo pauta en alguno de los meses comparados.
3. Instagram — KPIs: alcance, visualizaciones, interacciones y seguidores, vs mes anterior y vs mismo mes del año anterior.
   - Gráfico de seguidores de Instagram de los últimos 12 meses (nuevos y los que se fueron). Fuente: `follows_and_unfollows`, desglose `follow_type` (FOLLOWER = nuevos, NON_FOLLOWER = se fueron; sumar los tramos del mes). Datos desde octubre 2025.
   - Tabla mensual de Instagram (12 meses): Mes | Alcance | Visualizaciones | Interacciones | Nuevos | Se fueron | Saldo | Total aprox. (reconstruido hacia atrás desde el total actual).
   - Tabla "Publicaciones de <mes> en Instagram": Fecha | Publicación (con formato) | Alcance | Vistas | Interacc., ordenadas por alcance.
4. Línea de tiempo con todos los meses disponibles y pestañas por métrica (alcance IG, vistas IG, interacciones IG, alcance FB, vistas FB, seguidores FB, inversión en pauta), marcando los meses con pauta.
5. Seguidores de Facebook · 12 meses: tabla Mes | Nuevos | Se fueron | Saldo | Total a fin de mes (`page_daily_follows_unique`, `page_daily_unfollows_unique`, `page_follows`).
6. Publicaciones de <mes> en Facebook: tabla Fecha | Publicación | Visualizaciones | Clics | Reacciones, y una nota con qué se publicó solo en una de las dos redes.
7. Historial de pauta: solo anuncios con `es_de_la_marca: true`. Tabla Mes | Campaña | Objetivo | Inversión | Alcance | Resultado | Costo por resultado. El resultado depende del objetivo: mensajes = conversaciones iniciadas (`onsite_conversion.messaging_conversation_started_7d`); reconocimiento/alcance = costo cada 1.000 personas; tráfico = costo por clic al enlace; interacción = costo por interacción. Montos nominales en ARS.
8. Para <mes siguiente>: 4 recomendaciones concretas, considerando fechas comerciales (Día de la Madre, Black Friday, Navidad, Pascua, etc.).
9. Notas sobre los datos: avisos de la extracción (`errores`), métricas que Meta haya cambiado, diferencias entre saldos y totales, limitaciones.

## Reglas
- Nunca inventar números: todo sale de los JSON.
- Si Meta cambió o eliminó una métrica, usar la más cercana disponible y aclararlo en las notas.
- Si falta el archivo del mes: revisar en GitHub Actions el workflow "Extraer métricas de Meta" (`extraer.yml`).
  - Si hay una corrida en curso, esperar a que termine.
  - Si no corrió todavía (GitHub suele demorar los horarios programados), dispararlo a mano con `actions_run_trigger` (método `run_workflow`, ref `main`, sin inputs) y esperar a que termine (tarda entre 2 y 40 minutos; consultar cada 3-5 minutos, hasta 60 minutos en total).
  - Cuando termine bien, hacer `git pull` y seguir con el informe. Si otra tarea ya la disparó, no dispararla de nuevo: esperar esa corrida.
  - Si falló o no terminó en 60 minutos, no publicar: avisar a Dana qué falló (con el motivo del log).

## Hitos conocidos (para explicar picos)
- 9/7/2026: video mundialista en Facebook, viral (97.000 visualizaciones, +130 seguidores, sin pauta).
- Abril 2025 y julio 2026: picos de alcance en Instagram sin explicación en el feed (pendiente de confirmar con Dana).
