# informes-redes

Extracción mensual automática de métricas de Meta (Facebook, Instagram y pauta) para los informes de marketing.

- **Cuándo corre:** el día 2 de cada mes, solo. También se puede correr a mano desde la pestaña **Actions → Extraer métricas de Meta → Run workflow**.
- **Qué guarda:** `data/<marca>/<AAAA-MM>.json`, con todo lo que Meta entrega para ese mes.
- **Marcas:** se configuran en `marcas.json`. Cada marca usa su propio token, guardado en *Settings → Secrets and variables → Actions*.
- **Seguridad:** los tokens son de solo lectura y nunca se imprimen ni se guardan en los archivos.
