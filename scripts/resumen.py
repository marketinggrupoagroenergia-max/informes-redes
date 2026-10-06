"""Resumen mensual de una marca. Uso: python scripts/resumen.py havanna salida.json"""
import json,glob,sys
def tv(st,k):
    v=st.get(k)
    if not v: return None
    s=0;ok=False
    for e in v:
        t=e.get('total_value',{})
        if isinstance(t.get('value'),(int,float)): s+=t['value'];ok=True
        for b in t.get('breakdowns',[]) or []:
            pass
    return s if ok else None
def daysum(st,k):
    v=st.get(k)
    if not v: return None
    return sum(x['value'] for e in v for x in e.get('values',[]) if isinstance(x.get('value'),(int,float)))
def lastv(st,k):
    v=st.get(k)
    if not v: return None
    vals=[x['value'] for e in v for x in e.get('values',[]) if isinstance(x.get('value'),(int,float))]
    return vals[-1] if vals else None
def pv(p,k):
    v=p.get('estadisticas',{}).get(k)
    if not v: return None
    x=v[0].get('values',[{}])[0].get('value')
    return x if isinstance(x,(int,float)) else None
out={'meses':[]}
for f in sorted(glob.glob(f'data/{sys.argv[1]}/*.json')):
    d=json.load(open(f));ig=d['instagram'][0];fb=d['facebook'][0]
    s=ig['estadisticas'];fs=fb['estadisticas']
    fu=s.get('follows_and_unfollows')
    ads=[a for c in d['anuncios'] for a in c.get('anuncios',[]) if a.get('es_de_la_marca')]
    out['meses'].append(dict(mes=d['mes'],
      ig_alcance=tv(s,'reach'),ig_vis=tv(s,'views'),ig_inter=tv(s,'total_interactions'),ig_cuentas_int=tv(s,'accounts_engaged'),
      ig_likes=tv(s,'likes'),ig_coment=tv(s,'comments'),ig_comp=tv(s,'shares'),ig_guard=tv(s,'saves'),ig_toques=tv(s,'profile_links_taps'),
      ig_seg_raw=json.dumps(fu)[:0],
      ig_posts=len(ig['publicaciones']),
      fb_vis=daysum(fs,'page_media_view'),fb_alc=daysum(fs,'page_total_media_view_unique'),fb_inter=daysum(fs,'page_post_engagements'),fb_seg=lastv(fs,'page_follows'),
      fb_nuevos=daysum(fs,'page_daily_follows_unique'),fb_posts=len(fb['publicaciones']),
      pauta=round(sum(float(a['spend']) for a in ads)),pauta_alc=sum(int(a.get('reach',0)) for a in ads),
      campanas=[(a['campaign_name'],round(float(a['spend'])),int(a.get('reach',0)),a.get('objective'),a.get('publicacion_instagram'),a.get('publicacion_facebook')) for a in ads],
      ig_fu=[e.get('total_value') for e in (fu or [])]))
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
for m in out['meses']: print({k:v for k,v in m.items() if k not in('campanas','ig_seg_raw')})
