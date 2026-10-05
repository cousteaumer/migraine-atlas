"""Правки поверх статей помощников: единые термины и проверенные факты о расположении узлов."""
import json, glob, os, re

SP = os.path.dirname(os.path.abspath(__file__))

def load_all():
    arts = []
    for f in sorted(glob.glob(f'{SP}/wiki_[A-I].json')):
        arts += json.load(open(f))
    return arts

def norm(o):
    if isinstance(o, str):
        o = re.sub(r'сенсибилизаци', 'сенситизаци', o)
        o = re.sub(r'Сенсибилизаци', 'Сенситизаци', o)
        return o
    if isinstance(o, list):
        return [norm(x) for x in o]
    if isinstance(o, dict):
        return {k: norm(v) for k, v in o.items()}
    return o

WHERE = {
    'trojnichnyj-uzel': {
        'h': 'Где он находится',
        'p': ['Узел лежит у основания черепа: это тонкое образование в форме полумесяца в небольшом кармане твёрдой оболочки (его называют пещерой Меккеля) на дне средней черепной ямки — углубления в основании черепа.'],
        'src': {'pmid': '32310545', 'label': 'Yu 2023 · StatPearls — тройничный (полулунный) узел'},
    },
    'krylonyobnyj-uzel': {
        'h': 'Где он находится',
        'p': ['Узел лежит в крылонёбной ямке — небольшом пространстве в глубине лица рядом с носовой полостью. До него можно добраться в том числе через нос: так делают блокаду узла при некоторых видах головной боли.',
              'Его волокна идут к слёзной железе и железам слизистой носа. Поэтому при его возбуждении может слезиться глаз и закладывать нос.'],
        'src': [{'pmid': '40722265', 'label': 'Bautista 2025 · Brain Sci — блокада крылонёбного узла при головной боли'},
                {'pmid': '21956040', 'label': 'Piagkou 2012 · Pain Pract — крылонёбный узел и болевые синдромы'}],
    },
}

RELATED_ADD = {
    'nspv': ['izbytok-lekarstv', 'profilaktika'],
    'triptany': ['izbytok-lekarstv'],
    'gepanty': ['profilaktika', 'izbytok-lekarstv'],
    'antitela-k-cgrp': ['profilaktika'],
    'petlya-usileniya': ['izbytok-lekarstv', 'profilaktika'],
    'triggery': ['profilaktika'],
    'sensitizaciya': ['izbytok-lekarstv'],
}

def patch(arts):
    arts = norm(arts)
    by = {a['slug']: a for a in arts}
    for slug, extra in RELATED_ADD.items():
        a = by.get(slug)
        if a:
            rel = a.setdefault('related', [])
            for x in extra:
                if x in by and x not in rel:
                    rel.append(x)
    for slug, w in WHERE.items():
        a = by.get(slug)
        if not a:
            continue
        if not any(s.get('h') == w['h'] for s in a['sections']):
            a['sections'].insert(0, {'h': w['h'], 'p': w['p']})
        srcs = w['src'] if isinstance(w['src'], list) else [w['src']]
        have = {str(s['pmid']) for s in a.get('sources', [])}
        for s in srcs:
            if s['pmid'] not in have:
                a.setdefault('sources', []).append(s)
    return arts

if __name__ == '__main__':
    arts = patch(load_all())
    print(len(arts), 'articles after patch')
