# Cómo se arma el informe mensual (instrucciones para Claude)

Destinataria: Dana, responsable de marketing. Español rioplatense (voseo), directo, concreto.

## Marca: Havanna La Pampa
- Datos: `data/havanna/AAAA-MM.json` (los genera la extracción del día 2).
- Resumen numérico: `python scripts/resumen.py havanna salida.json`.
- Plantilla del informe: `plantillas/informe-havanna-2026-09.html`. Mantener el mismo diseño, secciones y estilo; reemplazar datos y textos.
- Informe publicado como artifact NUEVO con título `Havanna La Pampa · <Mes AAAA>` (ej. `Havanna La Pampa · Octubre 2026`), icono `chart`.
- Índice: artifact https://claude.ai/artifact/8EnAV5FFPWpCdhV3nMqYmh (plantilla en `plantillas/indice-havanna.html`). Leerlo con Artifact `read`, agregar el mes nuevo ARRIBA de la lista con link, dato de alcance IG y una frase de resumen, y republicar con ese `url`.

## Marca: Dynamis Neumáticos
- Datos: `data/dynamis/AAAA-MM.json`. Resumen: `python scripts/resumen.py dynamis salida.json`.
- Plantilla: `plantillas/informe-dynamis-2026-09.html` (estética propia: asfalto + amarillo, tipografía Barlow). Mantener diseño y secciones.
- Informe publicado como artifact NUEVO con título `Dynamis Neumáticos · <Mes AAAA>`, icono `chart`.
- Índice: artifact https://claude.ai/artifact/LYHdSkrnR1f7bjdRCErTWi (plantilla `plantillas/indice-dynamis.html`).
- Cuenta activa desde mayo 2026 (Facebook) y junio 2026 (Instagram): no hay comparación interanual hasta junio 2027.
- Pauta: reportar costo por resultado según objetivo (mensajes: costo por conversación iniciada, `onsite_conversion.messaging_conversation_started_7d`; reconocimiento: costo cada 1.000 personas; tráfico: costo por clic al enlace). Referencia: mensajes 11/9/2026 = $2.110 por conversación; interacción julio 2026 = $8.375.
- Marcas que vende: Dunlop (estrella, vía Grupo Corven), Corven y Continental. No mencionar la gomería.

## Marca: Grupo Agroenergía
- Datos: `data/agroenergia/AAAA-MM.json`. Facebook (página 360487924048263) e Instagram @grupo.agroenergia (leído vía graph.instagram.com con el secret META_TOKEN_AGROENERGIA_IG, token de inicio de sesión de Instagram que vence cada 60 días). Si Instagram trae error de token vencido, avisar a Dana que lo regenere en la app Informes mensuales → Casos de uso → API de Instagram → Configuración de la API con inicio de sesión de Instagram → Generar token, y actualice el secret.
- La página se lee con un token de página de Dana (no vence, pero Meta exige reconfirmar el acceso a datos cada 90 días). Si la extracción da error de permisos o de token, avisar a Dana que hay que renovarlo desde el Explorador de la API Graph (app Informes mensuales, Generate Access Token, ampliar, me/accounts) y actualizar el secret META_TOKEN_AGROENERGIA.
- La pauta sale de la cuenta publicitaria del portfolio Agroenergia (token de Havanna); usar solo anuncios con `es_de_la_marca: true`. Esa cuenta mezcla marcas.
- Métricas de página: `page_total_media_view_unique` (alcance, desde mayo 2025), `page_media_view` (visualizaciones), `page_post_engagements`, `page_follows` (total), `page_daily_follows_unique` / `page_daily_unfollows_unique` (altas y bajas).
- Plantilla: `plantillas/informe-agroenergia-2026-09.html` (verde agro + tierra, tipografías Archivo y Public Sans). Título `Grupo Agroenergía · <Mes AAAA>`, icono `chart`.
- Índice: artifact https://claude.ai/artifact/Cv8zFVEKmPrTmbk6bmg5L9 (plantilla `plantillas/indice-agroenergia.html`).
- Contexto: la cuenta reúne Shell, Axion, Puma, estaciones bandera blanca, lo institucional y los repartos al agro.

## Contenido del informe
1. Lectura del mes: 3-4 conclusiones concretas basadas en los datos (qué pasó, por qué, qué publicaciones lo explican).
2. Números: mes vs mes anterior y vs mismo mes del año anterior, incluido el total de seguidores de Instagram (`perfil.followers_count`).
2b. Seguidores de Instagram: nuevos, los que se fueron y saldo de cada mes (`follows_and_unfollows`, desglose `follow_type`: FOLLOWER = nuevos, NON_FOLLOWER = se fueron; sumar los tramos del mes). Gráfico de los últimos 12 meses y tabla con el total aproximado a fin de mes, reconstruido hacia atrás desde el total actual. Datos disponibles desde octubre 2025.
3. Línea de tiempo con todos los meses disponibles, marcando meses con pauta.
4. Publicaciones del mes en Instagram, ordenadas por alcance.
5. Pauta: solo anuncios con `es_de_la_marca: true`. Inversión, alcance, costo cada 1.000. Montos nominales en ARS.
6. Recomendaciones para el mes siguiente, considerando fechas comerciales (Día de la Madre, Navidad, Pascua, etc.).
7. Notas sobre los datos: avisos de la extracción (`errores`), métricas que Meta haya cambiado, limitaciones.

## Reglas
- Nunca inventar números: todo sale de los JSON.
- Si Meta cambió o eliminó una métrica, usar la más cercana disponible y aclararlo en las notas.
- Si falta el archivo del mes, no publicar: avisar a Dana qué falló.

## Hitos conocidos (para explicar picos)
- 9/7/2026: video mundialista en Facebook, viral (97.000 visualizaciones, +130 seguidores, sin pauta).
- Abril 2025 y julio 2026: picos de alcance en Instagram sin explicación en el feed (pendiente de confirmar con Dana).
