'use strict';
const $ = s => document.querySelector(s);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeUrl = v => { try { const u = new URL(v); return u.protocol === 'https:' ? u.href : ''; } catch { return ''; } };
const ICONS = {search:'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/>',arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>'};
const icon = name => `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${ICONS[name] || ''}</svg>`;
const MODULES = {daily:'每日解读',weekly:'每周回顾',research:'研报精选',alert:'异动点评'};
const state = {view:'market',period:'daily',query:'',limit:12,reader:null,module:'daily'};
let edition, library;
let toastTimer;
function toast(message) { ($('#reader').open ? $('#reader') : document.body).append($('#toast')); $('#toast').textContent=message; $('#toast').hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>$('#toast').hidden=true,2600); }
function key() { return state.view==='market' ? state.period : state.view; }
function actual(k) { return edition.periods[k]?.article || edition[k]; }
function sources(a) { return edition.sources.filter(s=>(a.source_ids || []).includes(s.id)); }
function links(a) { return sources(a).map(s=>safeUrl(s.url) ? `<a href="${esc(safeUrl(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.name)} ↗</a>` : '').join(''); }
function renderOverview() {
 const p = edition.periods[state.period], d=p.overview;
 $('#edition-date').textContent=edition.edition_date; $('#brief-date').textContent=d.period_label; $('#brief-title').textContent=d.title; $('#brief-summary').textContent=d.summary; $('#brief-focus').textContent=d.focus; $('#snapshot-date').textContent=d.snapshot_label;
 $('#quotes').innerHTML=d.quotes.map(q=>`<div class="quote"><div class="quote-top"><span>${esc(q.name)}</span><span>${esc(q.unit)}</span></div><div class="quote-number">${esc(q.value)}${q.unit==='%'?'<small>%</small>':''}</div><div class="quote-bottom"><span class="quote-change ${esc(q.direction)}">${esc(q.change)}</span><span>${esc(q.basis)}</span></div></div>`).join('');
 $('#snapshot-sources').innerHTML=`<p>${esc(edition.methodology)}</p><p>比较基准：${esc(p.baseline)}；数据核对日期：${esc(edition.verified_on)}。</p><div class="source-links">${links(p.article)}</div>`; $('#overview').hidden=false;
}
function metrics(a,template=false) {
 if(!a.metrics?.length) return '';
 return `<div class="metrics">${a.metrics.map(m=>`<div class="metric"><span>${esc(m.label || m.name)}</span><strong class="${esc(m.direction || '')}">${esc(template ? m.value : m.change || m.value)}</strong>${!template&&m.baseline_date?`<small>对比 ${esc(m.baseline_date)}</small>`:''}</div>`).join('')}</div>`;
}
function bodySections(a,k,template=false) {
 const labels = k==='research' && a.title.startsWith('核实提示') ? ['核实状态','影响与边界','沟通参考','后续核实'] : k==='research' ? ['核心观点','依据与风险','沟通参考','跟踪验证'] : k==='weekly' ? ['本周发生了什么','可能有什么影响','沟通参考','下期关注'] : ['发生了什么','可能有什么影响','沟通参考','后续关注'];
 return `${metrics(a,template)}<section class="body-section"><h3 class="section-title"><span class="keypoint-number">01</span>${labels[0]}</h3><p>${esc(a.fact)}</p></section><section class="body-section"><h3 class="section-title"><span class="keypoint-number">02</span>${labels[1]}</h3><p>${esc(a.impact)}</p></section><section class="talk-box"><h3>${labels[2]} <span>内部草案</span></h3><p>${esc(a.talk)}</p></section><p class="watch"><strong>${labels[3]}：</strong>${esc(a.watch)}</p><p class="risk">${esc(template ? a.risk : edition.risk)}</p>`;
}
function actualCard(k,compact=false) {
 const a=actual(k);
 return `<article class="card article-card"><div class="article-topline"><div class="tags"><span class="tag">本期内容</span><span class="tag neutral">${esc(a.category)}</span><span class="tag gold">待机构审核</span></div></div><h2><button class="title-button" data-actual="${k}">${esc(a.title)}</button></h2><div class="article-meta">${esc(a.meta)}</div>${compact?`<p class="abstract">${esc(a.fact)}</p>`:`<div class="summary"><strong>本期摘要</strong>${esc(edition.periods[k]?.overview.summary || a.fact)}</div>${bodySections(a,k)}`}<div class="article-footer"><button class="primary" data-actual="${k}">${compact?'阅读完整内容':'查看来源与完整文案'} ${icon('arrow')}</button><button class="outline" data-copy-actual="${k}">复制草案</button><a class="outline" href="editions/2026-10-24/${k}.md" download>下载文案 ↓</a></div></article>`;
}
function visibleScenarios() {
 return library.scenarios.filter(s=>{
 if(!state.query) return true;
 return JSON.stringify(s).toLowerCase().includes(state.query.toLowerCase());
 });
}
function templateCard(s) {
 const m=s.modules[key()];
 return `<article class="card template-card"><div class="article-topline"><div class="tags"><span class="template-id">${esc(s.id)}</span></div></div><h3><button class="title-button" data-scene="${s.id}">${esc(s.name)}</button></h3><p class="template-summary">${esc(m.summary)}</p><div class="template-meta"><span>${esc(MODULES[key()])} · 待填待审</span><span>4类文案</span></div><div class="template-actions"><button class="outline" data-scene="${s.id}">查看模板 ${icon('arrow')}</button><button data-download-scene="${s.id}" class="download-link">下载 ↓</button></div></article>`;
}
function matchesActual(k) {
 const a=actual(k);
 return !state.query || JSON.stringify(a).toLowerCase().includes(state.query.toLowerCase());
}
function render() {
 if(!edition||!library) return;
 renderOverview();
 document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.view===state.view)));
 document.querySelectorAll('[data-period]').forEach(b=>{b.classList.toggle('selected',b.dataset.period===state.period); b.setAttribute('aria-pressed',String(b.dataset.period===state.period));});
 $('#period-control').hidden=state.view!=='market'; $('#view-label').hidden=state.view==='market'; $('#view-label').textContent=state.view==='research'?'保留机构、作者、日期与原始来源':state.view==='alert'?'先核实事实，再解释可能影响':'';
 const ks=[key()];
 const actualKeys=ks.filter(matchesActual), scenarios=visibleScenarios();
 $('#article-list').innerHTML=actualKeys.map(k=>actualCard(k)).join('');
 $('#template-section').hidden=false; $('#template-total').textContent=scenarios.length;
 $('#template-grid').innerHTML=scenarios.slice(0,state.limit).map(templateCard).join('');
 $('#load-more').hidden=state.limit>=scenarios.length; $('#load-more').textContent=`加载更多情景（还有${Math.max(0,scenarios.length-state.limit)}种） ↓`;
 $('#result-count').textContent=`${actualKeys.length}篇内容 · ${scenarios.length}种情景`;
 if(!scenarios.length) $('#template-grid').innerHTML=`<div class="empty">没有匹配的情景，请试试其他关键词。</div>`;
 $('#loading').hidden=true;
}
function actualMarkdown(k) {
 const a=actual(k);
 return `# ${a.title}\n\n> 内部草案 · 待机构审核\n\n${a.meta}\n\n## ${k==='research'?'核心观点':'发生了什么'}\n${a.fact}\n\n## 可能影响与风险\n${a.impact}\n\n## 沟通参考\n${a.talk}\n\n## 关注\n${a.watch}\n\n## 风险提示\n${edition.risk}\n\n## 来源\n${sources(a).map(s=>'- '+s.name+'：'+s.url).join('\n')}\n\n${edition.methodology}\n核对日期：${edition.verified_on}；版本：${edition.edition_id}\n`;
}
function asList(v) { return Array.isArray(v)?v:[v].filter(Boolean); }
function moduleMarkdown(s,k) {
 const m=s.modules[k];
 return `## ${MODULES[k]}\n\n### ${m.title}\n\n${m.meta}\n\n摘要：${m.summary}\n\n启用条件：${m.trigger}\n\n关键指标：\n${m.metrics.map(x=>'- '+x.label+'：'+x.value).join('\n')}\n\n### ${k==='research'?'核心观点':'发生了什么'}\n${m.fact}\n\n### 可能影响与风险\n${m.impact}\n\n### 沟通参考\n${m.talk}\n\n### 后续关注\n${m.watch}\n\n### 来源要求\n${asList(m.sources).map(x=>'- '+x).join('\n')}\n\n### 避免表述\n${asList(m.avoid).map(x=>'- '+x).join('\n')}\n\n### 风险提示\n${m.risk}\n\n### 审核说明\n${m.review_note}\n`;
}
function sceneMarkdown(s,k) {
 return `# ${s.id} ${s.name}\n\n> 内部文案模板 · 待填待审。〔字段〕为占位内容，不代表实际行情。\n\n分类：${s.group}；版本：${library.version}\n\n${k?moduleMarkdown(s,k):Object.keys(MODULES).map(x=>moduleMarkdown(s,x)).join('\n---\n\n')}`;
}
function downloadText(name,text) {
 const u=URL.createObjectURL(new Blob([text],{type:'text/markdown;charset=utf-8'})); const a=document.createElement('a'); a.href=u;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000);
}
async function copyText(text) {
 try { await navigator.clipboard.writeText(text);toast('已复制内部草案，请经机构审核后使用'); }
 catch { const t=document.createElement('textarea'); t.value=text;document.body.append(t);t.select();const ok=document.execCommand('copy');t.remove();toast(ok?'已复制内部草案，请经机构审核后使用':'复制未成功，请下载文案'); }
}
function openActual(k) {
 state.reader={type:'actual',key:k}; $('#reader-kicker').textContent='本期内容 · 待机构审核'; $('#reader-title').textContent=actual(k).title;$('#module-switch').hidden=true;
 $('#reader-body').innerHTML=`<div class="article-meta">${esc(actual(k).meta)}</div>${bodySections(actual(k),k)}<details class="review-details" open><summary>数据与来源</summary><div class="source-links">${links(actual(k))}</div><p>${esc(edition.methodology)}</p><p>核对日期：${esc(edition.verified_on)} · ${esc(edition.edition_id)}</p></details>`;
 $('#reader-actions').innerHTML=`<button class="primary" data-copy-actual="${k}">复制内部草案</button><a class="outline" href="editions/2026-10-24/${k}.md" download>下载本期文案 ↓</a>`;showReader();
}
function renderSceneReader() {
 const s=library.scenarios.find(x=>x.id===state.reader.id),m=s.modules[state.module];
 $('#reader-kicker').textContent=s.id+' · 待填待审'; $('#reader-title').textContent=s.name; $('#module-switch').hidden=false;
 $('#module-switch').innerHTML=Object.entries(MODULES).map(([k,label])=>`<button data-module="${k}" class="${state.module===k?'selected':''}" aria-pressed="${state.module===k}">${label}</button>`).join('');
 $('#reader-body').innerHTML=`<h3 class="module-title">${esc(m.title)}</h3><div class="article-meta">${esc(m.meta)}</div><div class="summary"><strong>模板摘要</strong>${esc(m.summary)}</div><p class="trigger"><strong>启用条件：</strong>${esc(m.trigger)}</p>${bodySections(m,state.module,true)}<details class="review-details"><summary>来源要求与审查要点</summary><h4>来源要求</h4><ul>${asList(m.sources).map(x=>`<li>${esc(x)}</li>`).join('')}</ul><h4>避免表述</h4><ul>${asList(m.avoid).map(x=>`<li>${esc(x)}</li>`).join('')}</ul><p>${esc(m.review_note)}</p><p>当前为模板，〔字段〕须补齐并经审核；不满足来源或触发条件时不发布。本库覆盖常见情景，实际市场可能出现组合情景，使用时需人工判断。</p></details>`;
 $('#reader-actions').innerHTML=`<button class="primary" data-copy-scene="${s.id}">复制本模块草案</button><button class="outline" data-download-module="${s.id}">下载本模块 ↓</button><button class="outline" data-download-scene="${s.id}">下载全部4类 ↓</button>`;
}
function showReader() { if(!$('#reader').open) { $('#reader').showModal();document.body.classList.add('dialog-open'); } $('#reader-body').scrollTop=0; }
function openScene(id) { state.reader={type:'scene',id};state.module=key();renderSceneReader();showReader(); }
function navigate(view) { state.view=view;state.limit=12;state.query='';$('#search').value='';history.replaceState(null,'','#'+(view==='market'?state.period:view));render(); }
document.addEventListener('click',e=>{
 const b=e.target.closest('button,a');if(!b) return;
 if(b.dataset.view) navigate(b.dataset.view);
 if(b.dataset.period) {state.period=b.dataset.period;state.limit=12;history.replaceState(null,'','#'+state.period);render();}
 if(b.dataset.actual) openActual(b.dataset.actual);
 if(b.dataset.scene) openScene(b.dataset.scene);
 if(b.dataset.module) {state.module=b.dataset.module;renderSceneReader();$('#reader-body').scrollTop=0;}
 if(b.dataset.copyActual) copyText(actualMarkdown(b.dataset.copyActual));
 if(b.dataset.copyScene) copyText(sceneMarkdown(library.scenarios.find(s=>s.id===b.dataset.copyScene),state.module));
 if(b.dataset.downloadScene) {const s=library.scenarios.find(s=>s.id===b.dataset.downloadScene);downloadText(`${s.id}_${s.name}_四类模板.md`,sceneMarkdown(s));}
 if(b.dataset.downloadModule) {const s=library.scenarios.find(s=>s.id===b.dataset.downloadModule);downloadText(`${s.id}_${MODULES[state.module]}_待审模板.md`,sceneMarkdown(s,state.module));}
});
$('#search').addEventListener('input',e=>{state.query=e.target.value.trim();state.limit=12;render();});
$('#load-more').addEventListener('click',()=>{state.limit+=12;render();});
$('#reader-close').addEventListener('click',()=>$('#reader').close());
$('#reader').addEventListener('close',()=>{document.body.classList.remove('dialog-open');state.reader=null;});
$('#reader').addEventListener('click',e=>{if(e.target===$('#reader')) {const r=$('#reader').getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)$('#reader').close();}});
$('#overview-read').addEventListener('click',()=>openActual(state.period));
async function init() {
 document.querySelectorAll('[data-icon]').forEach(el=>el.innerHTML=icon(el.dataset.icon));
 const hash=location.hash.slice(1);if(hash==='saved')history.replaceState(null,'','#daily');if(['daily','weekly'].includes(hash))state.period=hash;else if(['market','research','alert'].includes(hash))state.view=hash;
 try {const results=await Promise.all(['market-edition.json','template-library.json'].map(async path=>{const r=await fetch(path);if(!r.ok)throw Error(path);return r.json();}));[edition,library]=results;if(library.scenarios.length!==60)throw Error('模板库不完整');render();}
 catch {$('#loading').textContent='内容暂时未能载入，请刷新页面重试。';}
}
init();
