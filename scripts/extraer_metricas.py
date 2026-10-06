"""
Extrae las métricas mensuales de Meta (Facebook, Instagram y anuncios)
para cada marca configurada en marcas.json y las guarda en data/<marca>/<AAAA-MM>.json.

Diseño:
- Guarda TODO lo que Meta devuelve, tal cual. Si Meta renombra o elimina
  una métrica, el script no se rompe: la anota en "errores" y sigue.
- Cada métrica se pide por separado, así una métrica dada de baja no
  arrastra a las demás.
- Solo usa la biblioteca estándar de Python (no hay nada que instalar).
- El token nunca se imprime ni se guarda.

Uso:
  python scripts/extraer_metricas.py                  -> mes anterior
  python scripts/extraer_metricas.py --mes 2026-08    -> un mes puntual
  python scripts/extraer_metricas.py --historico 24   -> últimos 24 meses
"""

import argparse
import calendar
import datetime as dt
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = os.environ.get("GRAPH_VERSION", "v23.0")
BASE = f"https://graph.facebook.com/{VERSION}"
RAIZ = pathlib.Path(__file__).resolve().parent.parent

# Listas de métricas candidatas. Meta las cambia seguido: las que ya no
# existan quedan registradas en "errores" sin cortar la extracción.
METRICAS_PAGINA = [
    "page_follows",
    "page_daily_follows_unique",
    "page_daily_unfollows_unique",
    "page_impressions_unique",
    "page_media_view",
    "page_total_media_view_unique",
    "page_post_engagements",
    "page_views_total",
    "page_fan_adds_unique",
]
METRICAS_POST_FB = [
    "post_impressions_unique",
    "post_media_view",
    "post_clicks",
    "post_reactions_by_type_total",
]
METRICAS_IG_TOTALES = [
    "reach",
    "views",
    "total_interactions",
    "accounts_engaged",
    "likes",
    "comments",
    "shares",
    "saves",
    "profile_links_taps",
    "follows_and_unfollows",
]
METRICAS_MEDIA_IG = ["reach", "views", "saved", "shares", "total_interactions"]
CAMPOS_ANUNCIOS = (
    "campaign_id,campaign_name,adset_name,ad_id,ad_name,objective,"
    "spend,reach,impressions,frequency,clicks,cpm,ctr,actions,cost_per_action_type"
)


class ErrorMeta(Exception):
    pass


def llamar(ruta, token, **params):
    """GET a la Graph API. Devuelve el JSON o lanza ErrorMeta."""
    params["access_token"] = token
    url = ruta if ruta.startswith("http") else f"{BASE}/{ruta.lstrip('/')}"
    if "?" not in url:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    for intento in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            cuerpo = e.read().decode(errors="replace")
            try:
                msg = json.loads(cuerpo)["error"].get("message", cuerpo)
            except Exception:
                msg = cuerpo[:300]
            if e.code in (429, 500, 502, 503) and intento < 2:
                time.sleep(5 * (intento + 1))
                continue
            raise ErrorMeta(f"HTTP {e.code}: {msg}") from None
        except urllib.error.URLError as e:
            if intento < 2:
                time.sleep(5)
                continue
            raise ErrorMeta(f"Sin conexión: {e.reason}") from None


def paginar(ruta, token, limite=2000, **params):
    """Recorre todas las páginas de resultados de un listado."""
    datos, res = [], llamar(ruta, token, **params)
    while True:
        datos.extend(res.get("data", []))
        siguiente = res.get("paging", {}).get("next")
        if not siguiente or len(datos) >= limite:
            return datos
        res = llamar(siguiente, token)


def rango_mes(mes):
    anio, m = map(int, mes.split("-"))
    ultimo = calendar.monthrange(anio, m)[1]
    desde = dt.datetime(anio, m, 1, tzinfo=dt.timezone.utc)
    hasta = dt.datetime(anio, m, ultimo, 23, 59, 59, tzinfo=dt.timezone.utc)
    return desde, hasta


def metrica_por_metrica(ruta, token, metricas, errores, etiqueta, **params):
    resultado = {}
    for metrica in metricas:
        try:
            res = llamar(ruta, token, metric=metrica, **params)
            resultado[metrica] = res.get("data", [])
        except ErrorMeta as e:
            errores.append(f"{etiqueta} · {metrica}: {e}")
    return resultado


def extraer_facebook(pagina, desde, hasta, errores):
    token = pagina.get("access_token")
    pid = pagina["id"]
    salida = {"id": pid, "nombre": pagina.get("name")}
    if not token:
        errores.append("Facebook: la página no devolvió token propio")
        return salida
    try:
        salida["perfil"] = llamar(pid, token, fields="name,fan_count,followers_count,link")
    except ErrorMeta as e:
        errores.append(f"Facebook perfil: {e}")

    since, until = int(desde.timestamp()), int(hasta.timestamp()) + 1
    salida["estadisticas"] = metrica_por_metrica(
        f"{pid}/insights", token, METRICAS_PAGINA, errores, "Facebook",
        period="day", since=since, until=until,
    )

    publicaciones = []
    try:
        posts = paginar(
            f"{pid}/posts", token,
            fields="id,created_time,message,permalink_url,status_type,"
                   "shares,comments.summary(true).limit(0),reactions.summary(true).limit(0)",
            since=since, until=until, limit=100,
        )
        for post in posts:
            post["estadisticas"] = metrica_por_metrica(
                f"{post['id']}/insights", token, METRICAS_POST_FB, [], "post",
            )
            publicaciones.append(post)
    except ErrorMeta as e:
        errores.append(f"Facebook publicaciones: {e}")
    salida["publicaciones"] = publicaciones
    return salida


def extraer_instagram(ig_id, token, desde, hasta, errores):
    salida = {"id": ig_id}
    try:
        salida["perfil"] = llamar(ig_id, token, fields="username,followers_count,follows_count,media_count")
    except ErrorMeta as e:
        errores.append(f"Instagram perfil: {e}")

    since, until = int(desde.timestamp()), int(hasta.timestamp()) + 1
    salida["estadisticas"] = metrica_por_metrica(
        f"{ig_id}/insights", token, METRICAS_IG_TOTALES, errores, "Instagram",
        period="day", metric_type="total_value", since=since, until=until,
    )

    publicaciones = []
    try:
        medios = paginar(
            f"{ig_id}/media", token, limite=500,
            fields="id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count",
            limit=100,
        )
        for medio in medios:
            fecha = dt.datetime.fromisoformat(medio["timestamp"].replace("+0000", "+00:00"))
            if fecha < desde:
                break  # vienen ordenadas de más nueva a más vieja
            if fecha > hasta:
                continue
            medio["estadisticas"] = metrica_por_metrica(
                f"{medio['id']}/insights", token, METRICAS_MEDIA_IG, [], "medio",
            )
            publicaciones.append(medio)
    except ErrorMeta as e:
        errores.append(f"Instagram publicaciones: {e}")
    salida["publicaciones"] = publicaciones
    return salida


def extraer_anuncios(token, desde, hasta, errores):
    cuentas_salida = []
    try:
        cuentas = paginar("me/adaccounts", token, fields="id,name,currency,account_status")
    except ErrorMeta as e:
        errores.append(f"Cuentas publicitarias: {e}")
        return cuentas_salida
    rango = json.dumps({"since": desde.strftime("%Y-%m-%d"), "until": hasta.strftime("%Y-%m-%d")})
    for cuenta in cuentas:
        try:
            filas = paginar(
                f"{cuenta['id']}/insights", token,
                level="ad", fields=CAMPOS_ANUNCIOS, time_range=rango, limit=500,
            )
            for fila in filas:
                # Vincula el anuncio con la publicación que promocionó.
                try:
                    creativo = llamar(
                        fila["ad_id"], token,
                        fields="creative{effective_object_story_id,effective_instagram_media_id}",
                    ).get("creative", {})
                    fila["publicacion_facebook"] = creativo.get("effective_object_story_id")
                    fila["publicacion_instagram"] = creativo.get("effective_instagram_media_id")
                except ErrorMeta:
                    pass
            cuenta["anuncios"] = filas
        except ErrorMeta as e:
            errores.append(f"Anuncios {cuenta.get('name')}: {e}")
        cuentas_salida.append(cuenta)
    return cuentas_salida


def extraer_marca(marca, token, mes):
    desde, hasta = rango_mes(mes)
    errores = []
    datos = {
        "marca": marca,
        "mes": mes,
        "extraido": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "version_api": VERSION,
        "facebook": [],
        "instagram": [],
        "anuncios": [],
        "errores": errores,
    }
    try:
        paginas = paginar("me/accounts", token, fields="id,name,access_token,instagram_business_account")
    except ErrorMeta as e:
        errores.append(f"No se pudieron listar las páginas: {e}")
        paginas = []

    for pagina in paginas:
        datos["facebook"].append(extraer_facebook(pagina, desde, hasta, errores))
        ig = pagina.get("instagram_business_account", {}).get("id")
        if ig:
            datos["instagram"].append(
                extraer_instagram(ig, pagina.get("access_token") or token, desde, hasta, errores)
            )
    datos["anuncios"] = extraer_anuncios(token, desde, hasta, errores)
    for p in datos["facebook"]:
        p.pop("access_token", None)
    return datos


def meses_a_extraer(args):
    hoy = dt.date.today()
    primero = hoy.replace(day=1)
    if args.mes:
        return [args.mes]
    cantidad = args.historico or 1
    meses, cursor = [], primero
    for _ in range(cantidad):
        cursor = (cursor - dt.timedelta(days=1)).replace(day=1)
        meses.append(cursor.strftime("%Y-%m"))
    return list(reversed(meses))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mes", help="Mes puntual, formato AAAA-MM")
    parser.add_argument("--historico", type=int, help="Cantidad de meses hacia atrás")
    args = parser.parse_args()

    marcas = json.loads((RAIZ / "marcas.json").read_text(encoding="utf-8"))
    hubo_datos = False
    for marca, variable in marcas.items():
        token = os.environ.get(variable)
        if not token:
            print(f"[{marca}] sin token ({variable}); se omite.")
            continue
        for mes in meses_a_extraer(args):
            datos = extraer_marca(marca, token, mes)
            destino = RAIZ / "data" / marca / f"{mes}.json"
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
            print(
                f"[{marca}] {mes}: {len(datos['facebook'])} página(s), "
                f"{len(datos['instagram'])} Instagram, "
                f"{sum(len(c.get('anuncios', [])) for c in datos['anuncios'])} anuncio(s), "
                f"{len(datos['errores'])} aviso(s)."
            )
            hubo_datos = True
    if not hubo_datos:
        sys.exit("No se extrajo nada: revisá que los tokens estén cargados en Secrets.")


if __name__ == "__main__":
    main()
