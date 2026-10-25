"""User image transcription; institution claims are retained as attributed sample text."""
import json
from pathlib import Path
from alert_format import alert_markdown
ROOT = Path(__file__).resolve().parents[1]
STANDARD = {
    'id': 'alert-standard-v1', 'format_version': '1.0', 'status': 'unverified_user_sample',
    'source': '用户提供的异动点评模板图片（仅整理可见内容）',
    'notice': '用户提供的标准样例，XXX、X%与日期均为待填字段；示例原因、市场判断及配置话术须核实并经机构审核。原文中的“建信理财口径”等表述不代表机构授权或已通过审核。',
    'document_title': '理财信手查｜【异动解读】小程序模板（对标金葵花陪伴版式，适配建信理财合规口径）',
    'intro': '定位：市场急跌/大涨等异动事件陪伴解读，适合小程序独立专栏，结构清晰、客户友好、渠道可转发；模块固定，后续换日期、行情、驱动因素即可复用。',
    'series': '理财信手查·财富陪伴｜异动解读',
    'title': '上证指数盘中调整，市场如何看待？',
    'publication_date': 'YYYY-MM-DD',
    'opening': ['XX月XX日，A股盘中出现明显调整，上证指数一度跌超X%，创业板指跌超X%。风格上，XX板块跌幅居前，XX板块相对抗跌。截至收盘，上证指数下跌X%，创业板指下跌X%。',
                '市场波动背后有哪些驱动因素？后续行情怎么看？本期为您解读。'],
    'causes': [
        {'label': '外部因素', 'text': 'XXX', 'example': '海外通胀数据超预期，加息预期升温，美债收益率上行，压制权益资产估值；海外赛道龙头盈利/融资压力扰动板块情绪'},
        {'label': '板块层面', 'text': 'XXX', 'example': '热门赛道标的营收增速放缓，市场对业绩兑现要求提升，成长板块估值承压'},
        {'label': '国内基本面', 'text': 'XXX', 'example': '金融数据偏弱，企业、居民投融资意愿偏弱，内需修复节奏仍待观察'}
    ],
    'outlook': [
        {'label': '短期：震荡格局为主，阶段性扰动仍存', 'text': '外部预期反复叠加内需修复尚需时间，市场情绪容易波动；板块行情更依赖业绩兑现。同时可以看到，资金层面存在逢低布局迹象，若外部扰动缓和，具备业绩支撑的标的存在修复机会。'},
        {'label': '中长期：政策协同发力，把握结构性机会', 'text': '财政、货币政策持续协同发力，各类稳增长、支持科创、降融资成本的政策陆续落地。随着政策效果逐步显现，企业盈利持续验证，A股中长期仍存在结构性投资机会。'}
    ],
    'allocation_note': '配置建议基于不同客户现有持仓仓位差异化给出，不构成投资承诺',
    'allocation': [
        '显著低配权益客户：可采用定投方式，逢低分批布局，把控节奏，不急于一次性加仓。',
        '标配权益客户：建议均衡配置，兼顾价值与成长，分散单一板块风险。',
        '全体投资者建议：定期开展资产检视（建议至少每季度一次），结合自身风险承受能力、资金期限，校准持仓结构。'
    ],
    'service': {'label': '资产检视服务', 'copy': '一键进入资产检视，欢迎咨询您的理财经理', 'status': 'unconfigured',
                'note': '入口仅为模板示意，待接入机构正式服务。配置建议须结合客户适当性评估，经审核后使用；当前公开网页不收集客户信息。'},
    'risk_heading': '风险提示（固定合规版，建信理财口径）',
    'risk': [
        '注：以上信息来源于公开市场数据，本文观点仅为当日市场解读，后续市场情况可能发生变化，仅供参考，不构成任何投资建议。',
        '市场有风险，投资须谨慎。理财非存款、产品有风险，过往业绩不代表未来表现，不等于理财产品实际收益。',
        '投资者应当认真阅读产品合同、说明书等法律文件，充分了解产品风险收益特征，结合自身投资期限、风险承受能力审慎决策。定投仅为平滑成本的投资方式，无法规避市场固有风险，不保证收益。'
    ],
    'preview': {'title': '【异动解读】YYYY-MM-DD',
                'summary': '市场出现明显调整，我们梳理异动背后驱动逻辑，从短期、中长期维度解读市场，并提供差异化配置思路，建议定期做好资产检视。',
                'risk': '市场有风险，投资需谨慎'},
    'reuse': [
        '版式对标参考样例的三段式结构：异动原因→展望（短＋中长期）→配置策略，客户陪伴感强，适合市场急跌、急涨等情绪窗口推送；',
        '可搭配行情示意图，和你之前【市场简评】两套模板形成组合：每日常规：【市场简评】（债＋股＋商品，客观行情）'
    ],
    'source_note': '运营说明按图片可见部分整理；图片底部已截断，未补写不可见内容。上文保留图片原文示例，不代表已核实市场结论或机构已审核；风险提示与适当性要求仍须按实际内容复核。'
}

if __name__ == '__main__':
    (ROOT/'dist'/'alert-standard.json').write_text(json.dumps(STANDARD, ensure_ascii=False, indent=2)+'\n')
    (ROOT/'dist'/'alert-standard.md').write_text(alert_markdown(STANDARD))
    print('Alert standard sample generated: opening, causes, two outlooks, allocation, risk, preview and visible reuse notes.')
