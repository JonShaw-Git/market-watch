import json,re,zipfile
from pathlib import Path
root=Path('dist/content-kit');kit=json.loads((root/'scenarios.json').read_text());fields=json.loads((root/'field-dictionary.json').read_text())['fields']
assert len(kit['scenarios'])==30
assert len({s['id'] for s in kit['scenarios']})==30
for s in kit['scenarios']:
 assert (root/s['file']).is_file()
 assert s['status']=='draft'
 for token in re.findall(r'〔([^〕]+)〕',' '.join([s[k] for k in ['fact','impact','talk','watch']]+list(s.get('variants',{}).values()))):
  field=s['bindings'][token]
  assert field in s['fields'] and field in fields,(s['id'],field)
for id,f in [('S08','funding_change_bp'),('S13','convertible_return_pct'),('S17','gold_change_pct'),('S19','foreign_yield_change_bp')]:
 s=next(s for s in kit['scenarios'] if s['id']==id)
 assert s['bindings']['上行幅度' if id in ['S08','S19'] else '上涨幅度']==f
assert 'nav_adjustment_status' in next(s for s in kit['scenarios'] if s['id']=='S28')['fields']
with zipfile.ZipFile('dist/content-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,Path('看市场情景文案模板')/p.relative_to(root))
print('内容验证通过：30种独立情景；事实变量均有字段；关键资产映射正确；均为草案；净值场景需核对分红。')
