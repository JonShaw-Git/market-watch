"""Shared three-part alert commentary, retaining factual and suitability boundaries."""
FORMAT_VERSION = '1.0'
ALLOCATION_NOTE = '以下为沟通参考，须结合客户风险承受能力、投资目标、资金期限、流动性需求及现有持仓核实适当性；不构成统一买卖指令，不承诺收益。'
SERVICE = {'label': '资产检视服务', 'copy': '一键进入资产检视，欢迎咨询您的理财经理', 'status': 'unconfigured', 'note': '服务入口示意，待接入机构正式服务；当前公开网页不收集客户持仓或个人信息。'}


def commentary(article, scene=None):
    template = scene is not None
    return {
        'format_version': FORMAT_VERSION,
        'title': article['title'],
        'series': '理财信手查·财富陪伴｜异动点评',
        'publication_date': '〔发布日期〕' if template else '2026-10-24',
        'opening': [article['fact']],
        'causes': [
            {'label': '外部因素', 'text': '〔已核实外部因素、发生时间及原始来源；证据不足时写“尚待核实”，不把同时发生视为因果〕' if template else '当前已核实行情不足以确认具体外部驱动因素，原因尚待核实。'},
            {'label': '板块层面', 'text': '〔已核实板块或行业因素及来源；不适用时注明不适用〕' if template else '本期未纳入同区间经核实的板块数据，暂不作板块归因。'},
            {'label': '国内基本面', 'text': '〔已正式发布的基本面数据、政策及传导前提；没有证据时明确未知〕' if template else '尚无足够独立证据将本期指数变化归因于特定基本面或政策事项。'}
        ],
        'cause_note': article['impact'],
        'outlook': [
            {'label': '短期：跟踪已确认信息及后续核实节点', 'text': article['watch']},
            {'label': '中长期：结合基本面与产品披露持续观察', 'text': '市场走向仍存在不确定性，须持续核实政策、盈利及估值等相关信息；具体产品还需结合正式投资范围、持仓、期限、费用与风险披露评估，不能从本次异动直接推断长期收益。'}
        ],
        'allocation_note': ALLOCATION_NOTE,
        'allocation': [
            '权益配置较低的客户：先核实风险承受能力与配置目标，是否调整及采用何种方式须结合适当性评估，不预设逢跌加仓。',
            '已有相应配置的客户：结合现有持仓检查集中度、期限及流动性需求，尊重客户自主决定。',
            '全体客户：可定期开展资产检视；具体产品信息与操作条件以正式合同、说明书及公告为准。'
        ],
        'talk': article['talk'], 'service': SERVICE,
        'risk': [article['risk'] if template else '以上内容仅供市场观察参考，不构成投资建议。市场有风险，理财非存款，理财产品存在本金损失风险。具体产品以正式披露为准，对客使用须经本机构审核。',
                 '定投仅为平滑成本的投资方式，无法规避市场固有风险，不保证收益。'],
        'preview': {'title': '【异动点评】〔发布日期〕' if template else '【异动点评】2026.10.24',
                    'summary': article.get('summary') or article['fact'],
                    'risk': '市场有风险，投资需谨慎。仅供参考，不构成投资建议。'}
    }


def alert_markdown(a):
    lines = []
    if a.get('document_title'):
        lines += ['# ' + a['document_title'], '', '> 异动点评标准样版 · ' + a['notice'], '', a['intro'], '', '标题规范：' + a['series'], '']
    lines += ['## 📖 ' + a['series'], '', '标题：' + a['title'], '', '发布日期：' + a['publication_date'], '', '### 开篇导语', ''] + a['opening']
    lines += ['', '## 🔍 一、本次市场异动的主要原因', '']
    for cause in a['causes']:
        lines += ['- ' + cause['label'] + '：' + cause['text']]
        if cause.get('example'):
            lines += ['', '（示例：' + cause['example'] + '）']
    if a.get('cause_note'):
        lines += ['', '核实边界：' + a['cause_note']]
    lines += ['', '## 📌 二、市场展望：短期 & 中长期视角', '']
    for item in a['outlook']:
        lines += ['### ✅ ' + item['label'], '', item['text'], '']
    lines += ['## 🧾 三、资产配置参考建议', '', '> 温馨提示：' + a['allocation_note'], '']
    lines += ['- ' + item for item in a['allocation']]
    if a.get('talk'):
        lines += ['', '沟通参考：' + a['talk']]
    lines += ['', '👉 小程序跳转按钮【' + a['service']['label'] + '】', '', '（文案：' + a['service']['copy'] + '）', '', '> ' + a['service']['note'], '', '## ⚠️ ' + a.get('risk_heading', '风险提示'), ''] + a['risk']
    lines += ['', '## 📎 配套：小程序首页卡片摘要（列表预览用，短版）', '', a['preview']['title'] + '｜' + a['preview']['summary'], '', '> 小字：' + a['preview']['risk']]
    if a.get('reuse'):
        lines += ['', '## 📋 运营复用说明', ''] + [str(i)+'. '+text for i, text in enumerate(a['reuse'], 1)]
    if a.get('source_note'):
        lines += ['', '> ' + a['source_note']]
    return '\n'.join(lines) + '\n'
