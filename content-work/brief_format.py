"""Shared editorial structure for daily/weekly briefings and their downloads.

This module formats supplied facts only. It does not connect to Wind or infer news.
"""
FORMAT_VERSION = '1.0'
PREVIEW_RISK = '仅供参考，不构成投资建议。理财有风险，可能损失本金。'


def template_brief(scene, kind, module):
    weekly = kind == 'weekly'
    span = '〔周起始日〕—〔周结束日〕' if weekly else '〔内容日期〕'
    headline = ('本周' if weekly else '本期') + '关注' + scene['name'] + '；市场指标变化不等于具体产品收益。'
    if scene['group'] in {'数据状态', '事件', '产品'} or scene['id'] in {'S34', 'S54'}:
        headline = ('本周' if weekly else '本期') + '关注' + scene['name'] + '的核实进展；信息不足时不作走势或产品影响判断。'
    labels = [('bonds', '债市'), ('equities', '股市'), ('commodities', '商品')]
    glance = [{'id': key, 'label': label, 'status': 'template',
               'text': '〔同一观察区间的' + label + '已核实行情；未纳入或核实未完成时明确说明，不填零、不推断方向〕',
               'source_ids': []} for key, label in labels]
    selected = {'债券': 'bonds', '信用': 'bonds', '资金': 'bonds', '转债': 'bonds',
                '权益': 'equities', '黄金': 'commodities'}.get(scene['group'])
    if scene['id'] in {'S51', 'S52'}:
        selected = 'commodities'
    events = []
    if selected:
        next(row for row in glance if row['id'] == selected)['text'] = module['fact']
    elif scene['group'] in {'数据状态', '事件', '产品'}:
        events.append({'title': scene['name'], 'text': module['fact'], 'source_ids': []})
    else:
        glance.append({'id': 'context', 'label': '综合观察', 'status': 'template',
                       'text': module['fact'], 'source_ids': []})
    events.append({'title': '〔已核实事项名称〕',
                   'text': '〔正式发生或披露时间、已确认事实及来源；无新增已核实事项时写明“本期暂无新增已核实事项”，不补写传闻〕',
                   'source_ids': []})
    risk = '以上为市场观察参考，不构成投资建议。' + module['risk']
    return {'format_version': FORMAT_VERSION, 'title': '市场简评｜' + span,
            'headline': headline, 'glance': glance, 'events': events, 'risk': risk,
            'preview': {'title': '市场简评｜' + span, 'summary': headline, 'risk': PREVIEW_RISK}}


def edition_brief(kind, period, research):
    weekly = kind == 'weekly'
    date = period['start'].replace('-', '.') + '—' + period['end'].replace('-', '.') if weekly else period['end'].replace('-', '.')
    event_date = period['end'][5:7] + '月' + period['end'][8:10] + '日'
    by_key = {q['key']: q for q in period['overview']['quotes']}
    def move(q):
        is_rate = q['key'] == 'shibor'
        up, down = ('上行', '下行') if is_rate else ('上涨', '下跌')
        word = up if q['direction'] == 'rise' else down if q['direction'] == 'fall' else '持平'
        val = q['change'].lstrip('+−-').replace(' ', '')
        return ('周度' if weekly else '当日') + word + val
    bond, cb, sh, eq = (by_key[k] for k in ('treasury', 'convertible', 'shibor', 'equity'))
    headline = ('权益、转债与国债指数周度表现分化，单日回升不等于全周上涨。' if weekly else
                '权益与转债回升，国债指数小幅波动；市场涨跌不能直接推算产品收益。')
    glance = [
        {'id': 'bonds', 'label': '债市', 'status': 'verified',
         'text': f'上证国债指数收于{bond["value"]}点，{move(bond)}；上证转债指数收于{cb["value"]}点，{move(cb)}。7天Shibor为{sh["value"]}%，{move(sh)}。指数涨跌与资金利率变动采用不同口径。',
         'source_ids': ['treasury', 'convertible', 'shibor23', 'shibor16' if weekly else 'shibor22']},
        {'id': 'equities', 'label': '股市', 'status': 'verified',
         'text': f'上证指数收于{eq["value"]}点，{move(eq)}。本项为单一指数观察，不代表所有个股或具体产品表现。',
         'source_ids': ['equity', 'equity23']},
        {'id': 'commodities', 'label': '商品', 'status': 'pending',
         'text': '本版尚未纳入同一观察区间、同币种经核实的黄金与原油行情，暂不作方向判断。', 'source_ids': []},
    ]
    events = [
        {'title': '资金数据公布（' + event_date + '）',
         'text': f'当日公布的7天Shibor为{sh["value"]}%。该指标反映资金市场参考利率，不是理财产品收益率。',
         'source_ids': ['shibor23']},
        {'title': '机构公开观点（原文日期见署名）',
         'text': research['fact'],
         'source_ids': research['source_ids']},
    ]
    risk = '以上内容来源于公开市场资料，仅供市场观察参考，不构成投资建议。市场有风险，理财非存款，理财产品存在本金损失风险。市场指标不等于具体产品表现；具体产品信息以正式披露为准。对客使用须经本机构审核。'
    return {'format_version': FORMAT_VERSION, 'title': '市场简评｜' + date,
            'headline': headline, 'glance': glance, 'events': events, 'risk': risk,
            'preview': {'title': '市场简评｜' + date, 'summary': headline, 'risk': PREVIEW_RISK}}


def brief_markdown(brief):
    lines = ['## 一句话看点', '', brief['headline'], '', '## 行情速览', '']
    for row in brief['glance']:
        suffix = '（待补充）' if row['status'] == 'pending' else ''
        lines += ['### ' + row['label'] + suffix, '', row['text'], '']
    lines += ['## 重点事件', '']
    for event in brief['events']:
        lines += ['- ' + event['title'] + '：' + event['text']]
    lines += ['', '## 风险提示', '', brief['risk'], '', '## 配套极简卡片版', '',
              '标题：' + brief['preview']['title'], '', '摘要：' + brief['preview']['summary'], '',
              '提示：' + brief['preview']['risk'], '']
    return '\n'.join(lines)
