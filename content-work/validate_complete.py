#!/usr/bin/env python3
"""Validate completeness, downloadable archive, and internal references before publish."""
import json, zipfile, re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
dist=root/'dist'
lib=json.loads((dist/'template-library.json').read_text())
assert lib['scene_count']==60 and lib['module_count']==240
assert len(lib['scenarios'])==60
assert [s['id'] for s in lib['scenarios']]==[f'S{i:02}' for i in range(1,61)]
for s in lib['scenarios']:
    for k in ('daily','weekly','research','alert'):
        m=s['modules'][k]
        for field in ('title','summary','meta','fact','impact','talk','watch','sources','avoid','trigger','risk'):
            assert isinstance(m[field],str) and m[field].strip(), (s['id'],k,field)
        assert len(m['metrics'])==2,(s['id'],k)
        assert '〔' in m['fact'] and '〕' in m['fact'],(s['id'],k,'fact placeholders')
        assert '风险' in m['risk'],(s['id'],k,'risk')
with zipfile.ZipFile(dist/'market-template-library.zip') as z:
    assert len([n for n in z.namelist() if re.search(r'/S\d{2}_',n) and n.endswith('.md')])==60
    assert z.testzip() is None
for name in ('index.html','app.js','styles.css','market-edition.json','template-library.json','market-template-library.zip'):
    assert (dist/name).is_file(),name
print('PASS: 60 scenarios, 240 complete modules, 60 Markdown files in ZIP, required resources present')
