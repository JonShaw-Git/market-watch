'use strict';
let marketEdition = null;

function editionKey() {
  return state.view === 'research' ? 'research' : state.view === 'alert' ? 'alert' : state.period;
}

function currentArticle() {
  if (!marketEdition) return null;
  const key = editionKey();
  return marketEdition.periods[key]?.article || marketEdition[key];
}

function currentSources(article) {
  return marketEdition.sources.filter(source => article.source_ids.includes(source.id));
}

function renderEditionOverview() {
  if (!marketEdition) return;
  const period = state.view === 'market' ? state.period : 'daily';
  const data = marketEdition.periods[period].overview;
  $('#edition-date').textContent = marketEdition.edition_date;
  $('#brief-date').textContent = data.period_label;
  $('#brief-title').textContent = data.title;
  $('#brief-summary').textContent = data.summary;
  $('#brief-focus').textContent = data.focus;
  $('#snapshot-date').textContent = data.snapshot_label;
  $('#snapshot-status').textContent = '公开行情 · 非实时';
  $('#overview-read').innerHTML = '阅读本期解读 <span aria-hidden="true">↗</span>';
  $('#quotes').innerHTML = data.quotes.map(q => `<div class="quote-card"><span class="quote-name">${escapeHTML(q.name)}</span><strong class="quote-value">${escapeHTML(q.value)}<small>${escapeHTML(q.unit)}</small></strong><div class="quote-bottom"><span class="quote-change ${q.direction === 'rise' ? 'rise' : q.direction === 'fall' ? 'fall' : ''}">${escapeHTML(q.change)}</span><span>${escapeHTML(q.basis)}</span></div></div>`).join('');
  const article = marketEdition.periods[period].article;
  $('#snapshot-sources').innerHTML = `<p>核对日期：${escapeHTML(marketEdition.verified_on)}。${escapeHTML(marketEdition.methodology)}</p>${currentSources(article).filter(s => safeUrl(s.url)).map(s => `<a href="${escapeHTML(safeUrl(s.url))}" target="_blank" rel="noopener">${escapeHTML(s.name)} ↗</a>`).join('')}`;
  $('#overview').hidden = false;
}

function renderEditionArticle() {
  const article = currentArticle();
  if (!article) return false;
  const key = editionKey();
  const period = marketEdition.periods[key];
  $('#category').textContent = article.category;
  $('#article .status').textContent = marketEdition.status;
  $('#title').textContent = article.title;
  $('#meta').textContent = article.meta;
  $('.usage').textContent = marketEdition.risk;
  $('#metrics').hidden = !article.metrics.length;
  $('#metrics').innerHTML = article.metrics.map(q => `<div class="metric"><span class="metric-label">${escapeHTML(q.label)}</span><strong class="metric-value ${q.direction === 'rise' ? 'rise' : q.direction === 'fall' ? 'fall' : ''}">${escapeHTML(q.change)}</strong><span class="metric-sub">${escapeHTML(key === 'alert' ? q.basis === '日涨跌' ? '对比2026.10.22' : '对比2026.10.16' : '对比' + period.baseline)}</span></div>`).join('');
  $('#fact-label').textContent = key === 'research' ? '核心观点' : key === 'weekly' ? '本周发生了什么' : '发生了什么';
  $('#impact-label').textContent = key === 'research' ? '依据与风险' : '可能有什么影响';
  for (const field of ['fact', 'impact', 'talk', 'watch']) $('#' + field).textContent = article[field];
  $('#watch-label').textContent = key === 'weekly' ? '下期关注：' : '关注：';
  const rows = period ? period.overview.quotes.map(q => `<div class="data-row"><span>${escapeHTML(q.name)}</span><strong>${escapeHTML(q.value + q.unit + ' / ' + q.basis + q.change)}<br><small>基准${escapeHTML(q.baseline_date)}：${escapeHTML(q.baseline_value + q.unit)}</small></strong></div>`).join('') : '';
  const note = key === 'research' ? '本篇转述公开采访观点，非独立研报；原始日期2026.10.23，作者与机构见上方署名。观点与本页风险提示分别表述，完整内容以原文为准。' : marketEdition.methodology;
  $('#data-details').innerHTML = `<p class="data-note">${escapeHTML(note)}</p>${rows}<div class="edition-source-links">${currentSources(article).filter(s => safeUrl(s.url)).map(s => `<a href="${escapeHTML(safeUrl(s.url))}" target="_blank" rel="noopener">${escapeHTML(s.name)} ↗</a>`).join('')}</div><p class="data-note">核对日期：${escapeHTML(marketEdition.verified_on)}；公开数据快照不代表实时行情，尚未经本机构对客审核。</p>`;
  $('#download-scene').href = 'editions/2026-10-24/' + key + '.md';
  $('#download-scene').download = '看市场_2026-10-24_' + key + '.md';
  $('#download-scene').textContent = '下载本期文案';
  return true;
}

function editionPlainText() {
  const article = currentArticle();
  const sourceText = currentSources(article).map(s => s.name + '：' + s.url).join('\n');
  return `【内部草案·待机构审核】\n${article.title}\n${article.meta}\n\n${editionKey() === 'research' ? '核心观点' : '发生了什么'}：${article.fact}\n\n可能影响与风险：${article.impact}\n\n沟通参考：${article.talk}\n\n关注：${article.watch}\n\n${marketEdition.risk}\n\n来源：\n${sourceText}\n\n核对日期：${marketEdition.verified_on}；版本：${marketEdition.edition_id}`;
}
