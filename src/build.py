"""Собирает ../index.html из шаблона, рисунка и статей вики."""
import json, os, sys
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
from patch_wiki import load_all, patch
arts = patch(load_all())
t = open(f'{SRC}/template.html', encoding='utf-8').read()
plate = open(f'{SRC}/plate.svg.part', encoding='utf-8').read()
body = t.replace('%%PLATE%%', plate).replace('%%WIKI%%', json.dumps(arts, ensure_ascii=False).replace('</', '<\\/'))
head = '<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body style="margin:0">\n'
open(os.path.join(SRC, '..', 'index.html'), 'w', encoding='utf-8').write(head + body + '\n</body></html>\n')
print(len(arts), 'статей; index.html собран')
