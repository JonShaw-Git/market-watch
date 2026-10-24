from pathlib import Path
import json, zipfile, re
root=Path('dist/content-kit'); scenes=[]
def add(id,name,group,condition,fields,fact,impact,talk,watch,avoid,priority='常规'):
 scenes.append(dict(id=id,name=name,group=group,priority=priority,condition=condition,fields=fields,fact=fact,impact=impact,talk=talk,watch=watch,avoid=avoid))
add('S01','市场平稳','常态','核心指标变动均在机构设定区间内，且不存在已确认重大风险事件。',['as_of','period','benchmark','equity_name','equity_return_pct','bond_index_name','bond_return_pct'],
'〔期间〕，〔权益指数〕变动〔权益涨跌幅〕%，〔债券指数〕变动〔债券涨跌幅〕%。所观察指标整体变化有限。',
'市场指标变化有限，不代表具体产品没有波动。产品表现仍可能受到持仓、估值和费用等因素影响。',
'本期所观察的市场指标变化不大，您的产品表现仍需结合最新净值和管理人披露来看。理财产品存在本金损失风险。',
'继续关注后续数据、产品披露及资金使用安排。','不得写“市场没有风险”“收益稳定不变”。')
add('S02','债券收益率上行','债券','同口径指定期限收益率较基准上行，达到机构设定的关注条件。',['as_of','benchmark','yield_name','yield_value_pct','yield_change_bp'],
'截至〔数据时点〕，〔收益率指标〕为〔收益率水平〕%，较〔比较基准〕上行〔上行幅度〕个基点。',
'其他条件相同时，债券到期收益率上行通常对应价格下跌。相关产品可能承压，程度取决于久期、持仓及估值方式。',
'部分债券价格可能因收益率上行而回落。您持有产品的具体影响，需要查看实际持仓及最新净值，不能直接套用市场指标。',
'核实受影响期限、产品久期和最新披露；涉及操作时结合资金需求与开放安排。','不得写“只是浮亏”“拿到期肯定回本”“现在不许赎回”。','重点')
add('S03','债券收益率下行','债券','同口径指定期限收益率较基准下行。',['as_of','benchmark','yield_name','yield_value_pct','yield_change_bp'],
'截至〔数据时点〕，〔收益率指标〕为〔收益率水平〕%，较〔比较基准〕下行〔下行幅度〕个基点。',
'其他条件相同时，收益率下行通常支持存量债券价格；后续再投资收益条件可能下降，产品表现仍取决于组合。',
'债市变化可能改善部分存量债券估值，但不意味着产品今后收益会持续提高，也不能据此承诺收益。',
'区分存量资产估值变化与未来再投资条件。','不得写“收益锁定”“债券上涨就该加仓”“未来收益更高”。')
add('S04','债券期限分化','债券','长短端收益率方向或幅度差异达到机构设定条件。',['as_of','benchmark','short_yield_name','short_yield_change_bp','long_yield_name','long_yield_change_bp'],
'〔期间〕，〔短端收益率指标〕变动〔短端变动〕个基点，〔长端收益率指标〕变动〔长端变动〕个基点，不同期限表现有差异。',
'不同久期与期限分布的组合可能出现不同表现，不能只用一个期限的收益率解释所有固收产品。',
'今天不同期限债券的变化并不一致。具体产品受到多大影响，需要看它实际持有哪些期限的资产。',
'核对收益率曲线、关键期限与产品久期。','不得把期限分化表述为“债市全面上涨/下跌”。')
add('S05','信用利差走阔','信用','同评级、期限、品种及基准的信用利差扩大。',['as_of','benchmark','spread_name','spread_value_bp','spread_change_bp'],
'截至〔数据时点〕，〔信用利差口径〕为〔利差水平〕个基点，较〔比较基准〕扩大〔扩大幅度〕个基点。',
'在其他条件相同时，利差扩大可能压低相关信用债估值。发行人风险、成交活跃度与组合敞口需要分别核实。',
'信用债之间的风险和表现有差异。是否影响您的产品，要看实际持仓及管理人对相关资产的披露。',
'关注发行人信息、流动性与持仓；利差变化本身不等于发生违约。','不得将利差走阔直接写成“信用风险全面爆发”。','重点')
add('S06','信用利差收窄','信用','同评级、期限、品种及基准的信用利差缩小。',['as_of','benchmark','spread_name','spread_value_bp','spread_change_bp'],
'截至〔数据时点〕，〔信用利差口径〕为〔利差水平〕个基点，较〔比较基准〕收窄〔收窄幅度〕个基点。',
'相关信用债估值可能改善，但价格变化不等于发行人信用风险消失；还需评估基本面及交易情况。',
'利差收窄反映阶段性的市场定价变化，不代表债券没有信用风险，也不代表相关理财产品可以保证收益。',
'核实利差可比性、发行人基本面及成交情况。','不得写“风险出清”“信用风险已消除”。')
add('S07','已确认信用事件','信用','发行人或其他有权机构已正式披露事件；必须记录原文来源。',['as_of','issuer_name','event_type','official_url','event_date','exposure_status'],
'〔披露日期〕，〔披露主体〕发布〔事件类型〕公告。已确认内容为〔已确认事实〕，其他信息仍以正式披露为准。',
'相关资产可能面临估值、流动性或偿付安排变化。是否影响具体产品，需核实直接及间接持仓与管理人披露。',
'我们会根据正式公告核实事件，并查看产品是否涉及相关资产。未核实持仓前，不能判断您的产品是否受到影响。',
'跟进正式披露和管理人说明；涉及损失、兑付等事项提供机构正式查询与反馈渠道。','不得写“某类产品都踩雷”“没有直接持仓就完全无影响”，不得传播未证实名单。','重点')
add('S08','资金利率上行','资金','指定资金利率较同口径基准上行；单一指标不足以推断全面流动性压力。',['as_of','benchmark','funding_name','funding_value_pct','funding_change_bp'],
'截至〔数据时点〕，〔资金利率指标〕为〔利率水平〕%，较〔比较基准〕上行〔上行幅度〕个基点。',
'融资成本和债券交易条件可能变化。资金利率不是理财收益率，不能据此推断产品将同幅上涨或下跌。',
'短期资金利率有所上行，对不同产品的影响并不相同。需要结合产品资产结构和资金安排判断。',
'关注跨月跨季、持续时间及已公布的公开市场操作。','不得用单一资金利率上行断言“流动性危机”。')
add('S09','资金利率回落','资金','指定资金利率较同口径基准下降。',['as_of','benchmark','funding_name','funding_value_pct','funding_change_bp'],
'截至〔数据时点〕，〔资金利率指标〕为〔利率水平〕%，较〔比较基准〕下降〔下降幅度〕个基点。',
'融资成本可能下降；现金类和短久期资产的再投资收益条件也可能变化，影响方向并不完全相同。',
'资金利率回落对不同产品的作用有差异，不能直接理解为理财收益会同步提高。',
'关注变化的持续性和后续资产再投资条件。','不得写“资金宽松所以所有产品收益都会提高”。')
add('S10','权益指数上涨','权益','所选权益指数在规定期间上涨；没有市场宽度数据时只称指数上涨。',['as_of','benchmark','equity_name','equity_close','equity_return_pct'],
'〔期间〕，〔权益指数〕收于〔指数点位〕点，较〔比较基准〕上涨〔上涨幅度〕%。',
'持有相关权益资产的产品可能受益，实际表现取决于仓位、行业和标的。单一指数上涨不代表所有股票或产品上涨。',
'指数上涨不代表每只理财产品都会同步上涨。我们需要看产品的权益仓位和具体投资范围。',
'关注上涨结构、后续波动及产品实际敞口。','不得写“普涨”而无市场宽度证据，不得写“抓紧上车”“稳赚行情”。')
add('S11','权益指数下跌','权益','所选权益指数在规定期间下跌；需指明指数与比较基准。',['as_of','benchmark','equity_name','equity_close','equity_return_pct'],
'〔期间〕，〔权益指数〕收于〔指数点位〕点，较〔比较基准〕下跌〔下跌幅度〕%。',
'有相关权益敞口的产品可能承压；实际波动与仓位、行业、对冲和其他资产表现有关。',
'市场下跌可能影响部分产品净值，但不能把指数跌幅直接当作产品跌幅。是否调整还需结合资金计划及产品风险。',
'先核实产品净值、风险变化和开放安排，再回应客户具体问题。','不得写“必须立即清仓”“肯定很快反弹”“股市跌所以纯债一定涨”。','重点')
add('S12','权益结构分化','权益','不同指数、行业或风格表现差异达到机构设定条件。',['as_of','benchmark','equity_group_a','equity_return_a_pct','equity_group_b','equity_return_b_pct'],
'〔期间〕，〔指数/行业A〕变动〔A涨跌幅〕%，〔指数/行业B〕变动〔B涨跌幅〕%，表现分化。',
'不同投资范围和风格敞口可能导致产品表现不同。热门板块表现不能替代组合整体表现。',
'本期不同板块走势有差异，理解产品实际投资范围，比只看当天热门板块更有助于解释净值。',
'核对行业权重、投资范围及数据样本。','不得写“下一轮一定轮到某板块”，不得诱导频繁换仓。')
add('S13','转债指数上涨','转债','指定转债指数上涨；不能推断所有成分券同向。',['as_of','benchmark','convertible_name','convertible_close','convertible_return_pct'],
'〔期间〕，〔转债指数〕收于〔转债点位〕点，较〔比较基准〕上涨〔上涨幅度〕%。',
'转债具有权益和债券特征，持有相关资产的组合可能受影响，实际结果还取决于仓位、估值与其他资产。',
'这次上涨的是转债指数，不代表所有含转债的理财都取得同样收益。需结合实际持仓和产品净值核实。',
'关注转债仓位、估值、信用和相关条款。','不得将转债描述为“低波动普通债券”或“保本资产”。')
add('S14','转债指数下跌','转债','指定转债指数下跌；原因需另有证据。',['as_of','benchmark','convertible_name','convertible_close','convertible_return_pct'],
'〔期间〕，〔转债指数〕收于〔转债点位〕点，较〔比较基准〕下跌〔下跌幅度〕%。',
'转债组合可能同时受到正股、估值及信用等因素影响，不能仅用国债收益率解释净值变化。',
'转债也可能出现明显波动。是否影响您的理财，需要核实转债仓位和具体标的，不能仅凭指数判断。',
'关注正股表现、估值、信用及赎回等条款。','不得写“有债底所以不会亏”“跌了就是低吸机会”。','重点')
add('S15','人民币相对美元走弱','汇率','统一为每美元兑人民币报价；该报价上升表示人民币相对美元走弱。',['as_of','benchmark','fx_market','fx_pair','fx_value','fx_change_pct'],
'截至〔数据时点〕，〔在岸/离岸〕美元兑人民币报价为〔汇率水平〕，较〔比较基准〕上升〔变动幅度〕%，人民币相对美元走弱。',
'未对冲的美元资产人民币折算价值可能受汇率变化影响；产品结果还受资产价格、计价币种和对冲安排影响。',
'汇率变化是否影响产品，要看计价币种、外币敞口及是否对冲，不能直接据此推断产品收益。',
'核实在岸/离岸、报价方向、估值时点和对冲。','不得写“现在必须换美元”“美元资产必然赚钱”。')
add('S16','人民币相对美元走强','汇率','统一为每美元兑人民币报价；该报价下降表示人民币相对美元走强。',['as_of','benchmark','fx_market','fx_pair','fx_value','fx_change_pct'],
'截至〔数据时点〕，〔在岸/离岸〕美元兑人民币报价为〔汇率水平〕，较〔比较基准〕下降〔变动幅度〕%，人民币相对美元走强。',
'未对冲的美元资产人民币折算价值可能受影响；实际产品表现还取决于资产价格、币种及对冲安排。',
'人民币升值对不同产品的影响有差异。需要看产品是否有美元敞口及对冲安排，而不能只凭汇率涨跌判断。',
'避免混用中间价、在岸价、离岸价及不同时间点。','不得写“外币产品都会亏损”“现在应全部换回人民币”。')
add('S17','黄金价格上涨','黄金','固定现货/期货、市场及计价币种；同口径价格上涨。',['as_of','benchmark','gold_name','gold_currency','gold_value','gold_change_pct'],
'〔期间〕，〔黄金价格指标及币种〕为〔价格水平〕，较〔比较基准〕上涨〔上涨幅度〕%。',
'相关黄金敞口可能受益，但仍面临价格波动。人民币计价结果还可能受到汇率及产品结构影响。',
'黄金上涨不意味着没有风险，不同黄金相关产品的结构、费用和汇率敞口也可能不同。',
'核对现货/期货、计价币种、杠杆和产品条款。','不得写“避险资产不会亏”“黄金只涨不跌”。')
add('S18','黄金价格下跌','黄金','固定现货/期货、市场及计价币种；同口径价格下跌。',['as_of','benchmark','gold_name','gold_currency','gold_value','gold_change_pct'],
'〔期间〕，〔黄金价格指标及币种〕为〔价格水平〕，较〔比较基准〕下跌〔下跌幅度〕%。',
'相关敞口可能承压；不同黄金产品在杠杆、结构、费用及汇率上存在差异，不能直接等同。',
'黄金也会调整，具体影响要结合您持有产品的投资范围与结构判断，不能承诺价格或净值何时修复。',
'关注实际敞口、结构条款及资金使用安排。','不得写“亏了加仓就能摊平”“一定会涨回去”。')
add('S19','海外债券收益率上行','海外','指定国家、期限和来源的收益率上行，标注当地时点。',['as_of','local_trade_date','local_as_of','local_timezone','benchmark','foreign_yield_name','foreign_yield_pct','foreign_yield_change_bp'],
'截至〔当地数据时点〕（〔当地时区〕），〔海外收益率指标〕为〔收益率水平〕%，较〔比较基准〕上行〔上行幅度〕个基点。',
'相关存量债券价格可能承压，资产定价与汇率也可能变化。传导到境内产品需看实际海外敞口。',
'海外利率变化不等于所有境内理财都会同向变化。是否受影响，需要核实产品持仓、币种和对冲安排。',
'区分当地交易日与北京时间，不将政策预期当作已实施政策。','不得写“海外利率升，所有美元产品收益同步升”。')
add('S20','海外债券收益率下行','海外','指定国家、期限和来源的收益率下行，标注当地时点。',['as_of','local_trade_date','local_as_of','local_timezone','benchmark','foreign_yield_name','foreign_yield_pct','foreign_yield_change_bp'],
'截至〔当地数据时点〕（〔当地时区〕），〔海外收益率指标〕为〔收益率水平〕%，较〔比较基准〕下行〔下行幅度〕个基点。',
'相关存量债券估值可能改善，再投资条件也可能改变。币种、期限及对冲会影响组合结果。',
'利率下降对存量资产和未来再投资的作用不同，不能直接推导某只产品的未来回报。',
'关注久期、汇率、再投资条件和实际政策。','不得写“降息必然利好所有资产”“未来收益确定”。')
add('S21','股债同时下跌','多资产','同一可比期间权益价格指数和债券价格指数均下跌；不能把收益率下降当作债券价格下跌。',['as_of','benchmark','equity_name','equity_return_pct','bond_index_name','bond_return_pct'],
'〔期间〕，〔权益指数〕下跌〔权益跌幅〕%，〔债券价格指数〕下跌〔债券跌幅〕%，所观察资产同时承压。',
'股债分散的效果可能阶段性减弱。产品影响仍取决于整体仓位、相关性、对冲和估值方式。',
'不同资产有时会同时波动。解释产品净值时，需要看整个组合，不能认为债券一定能抵消股市下跌。',
'核实共同影响因素、流动性和组合敞口。','不得写“分散投资失效”“全部资产都在下跌”而缺乏证据。','重点')
add('S22','股债同时上涨','多资产','同一可比期间权益价格指数和债券价格指数均上涨。',['as_of','benchmark','equity_name','equity_return_pct','bond_index_name','bond_return_pct'],
'〔期间〕，〔权益指数〕上涨〔权益涨幅〕%，〔债券价格指数〕上涨〔债券涨幅〕%，所观察资产同步回升。',
'相关持仓可能受益，但配置比例、标的和费用等仍可能造成产品表现差异，后续走势并不确定。',
'股债同步上涨不代表所有产品同幅上涨，也不意味着风险消失。仍需以您持有产品的实际表现为准。',
'关注持续性及组合的实际风险来源。','不得写“股债双牛确定”“买什么都赚钱”。')
add('S23','股债表现分化','多资产','同一可比期间权益价格指数与债券价格指数方向不同。',['as_of','benchmark','equity_name','equity_return_pct','bond_index_name','bond_return_pct'],
'〔期间〕，〔权益指数〕变动〔权益涨跌幅〕%，〔债券价格指数〕变动〔债券涨跌幅〕%，方向不同。',
'不同股债比例的组合可能出现不同表现。两类资产并非始终反向，不能据此作固定对冲假设。',
'这次股债表现不同，对产品的影响取决于实际配置比例；不能用一种资产的变化代替整个组合的表现。',
'核对股债敞口和时间口径，避免将相关关系写成必然规律。','不得写“股涨债必跌”“股跌债必涨”。')
add('S24','政策正式发布','事件','官方政策已发布；具有原文、发布日期和生效安排。',['as_of','policy_name','policy_date','effective_date','official_url','confirmed_policy_summary'],
'〔发布主体〕于〔发布日期〕公布〔政策名称〕，主要安排为〔已确认内容〕，实施时间为〔生效安排〕。',
'政策影响取决于实际安排、此前定价及后续传导。尚未兑现的预期不能写成确定的行情或收益结果。',
'政策已经公布，但对市场和产品的影响还需观察。我们会结合正式文件和产品实际敞口解释，不据此承诺收益。',
'核实政策原文、生效时间与后续实施细则。','不得写“政策托底不会亏”“降息必然带来某产品上涨”。')
add('S25','经济数据高于预期','事件','实际值与发布前可追溯的一致预期可比；高于预期不自动等于经济更强或市场利好。',['as_of','macro_name','release_date','actual_value','consensus_value','consensus_as_of','macro_unit','official_url'],
'〔发布日期〕公布的〔经济指标〕为〔实际值〕〔单位〕，高于发布前〔预期采样时点〕的一致预期〔预期值〕〔单位〕。',
'影响取决于指标性质、结构及政策预期。通胀、增长等指标不能用相同的“利好/利空”标签解释。',
'这项数据高于此前预期，但还需要看指标性质和后续变化，不能由单个数据直接判断某只产品的收益。',
'一致预期缺失或口径不同时，只报道实际值，不写“超预期”。','不得将发布后的预测当作发布前预期，不得把“高于预期”一律表述为利好。')
add('S26','经济数据低于预期','事件','实际值与发布前可追溯的一致预期可比；低于预期不自动等于市场利空。',['as_of','macro_name','release_date','actual_value','consensus_value','consensus_as_of','macro_unit','official_url'],
'〔发布日期〕公布的〔经济指标〕为〔实际值〕〔单位〕，低于发布前〔预期采样时点〕的一致预期〔预期值〕〔单位〕。',
'不同指标与预期差的影响不同，还需看结构、持续性及政策反应，不能仅凭一个数值判断市场方向。',
'数据低于预期不等于所有资产都会下跌。我们需要结合指标性质、市场反应与产品持仓来看影响。',
'比较口径和预期时间必须一致；缺失时只显示已公布事实。','不得使用“经济一定恶化”“某类产品一定下跌”等断言。')
add('S27','重大突发事件','事件','至少有可追溯的正式信息；未经证实的消息只进入内部核实流程。',['as_of','event_name','confirmed_facts','official_url','event_time','verification_status'],
'截至〔核实时间〕，关于〔事件名称〕，已确认的信息为〔已确认事实〕。其他情况仍待进一步核实。',
'价格、流动性及情绪可能变化，但实际影响范围和持续时间尚不确定，不据此判断具体产品损失。',
'目前我们先说明已经核实的信息。产品是否受到影响，还需要结合持仓及管理人正式披露确认。',
'保持正式查询与反馈渠道，出现新事实后更新同一事件版本。','不得传播传闻，不得写“无需担心”“风险已完全解除”。','重点')
add('S28','产品净值回撤','产品','具体产品官方净值已披露且基准可比，已核实净值类型并排除分红、份额折算等不可比影响；市场行情不能替代产品净值或持仓。',['as_of','product_name','nav_date','nav_value','nav_benchmark','nav_change_pct','manager_disclosure_url','official_service_channel','nav_type','nav_adjustment_status','comparison_nav_date','comparison_nav_value','return_method'],
'根据〔管理人/销售机构正式披露〕，〔产品名称〕于〔净值日期〕披露〔净值类型〕净值〔产品净值〕，相对〔比较净值日期〕的〔比较净值〕变动〔净值变动〕%。',
'净值变化需先核对分红、净值类型及估值口径。未获得足够持仓和归因证据时，不将回撤归因于某一个市场变化。',
'理解您对净值变化的关注。我们会核实最新披露、风险变化和开放安排，并结合您的资金需求解释可考虑的事项；不能承诺回本时间或替您决定操作。',
'提供管理人/销售机构正式服务渠道；如有异议，按本机构流程受理反馈。','不得写“只是浮亏”“拿到期一定赚回来”“赎回才会亏”；本模板默认仅内部使用。','重点')
add('S29','数据不足待核实','数据状态','必要字段缺失、过期、来源冲突或质量未通过；优先拦截方向性结论。',['as_of','last_valid_as_of','missing_metric_names','data_quality_status'],
'截至〔核实时间〕，〔待核实指标〕尚未完成核实，暂无已核实的有效数据。',
'现有信息不足以支持本期走势或产品影响判断，不用零值补齐，也不以旧值冒充最新数据。',
'相关数据正在核实，我们暂不据此判断市场方向或具体产品影响。产品信息请以管理人及销售机构正式披露为准。',
'恢复后重校验；数据仍不完整时可暂缓发布。','不得把缺失写成“0变动”，不得沿用旧结论假装当日更新。','拦截')
add('S30','已发布数据更正','数据状态','源数据或计算口径经确认需更正，记录原值、新值、原因和受影响版本。',['as_of','corrected_metric_name','old_value','new_value','correction_reason','previous_version','current_version','source_url'],
'本篇于〔更正时间〕更新：〔更正指标〕由〔原值〕更正为〔新值〕。原因是〔经核实的更正原因〕，原版本为〔原版本号〕。',
'相关表格、图表及结论正在复核，原判断暂缓使用；完成核实并重新审核后更新本篇。',
'此前信息中的相关数据已更正，请以本次更新为准。涉及您持有产品的事项，我们会以正式披露重新核实，避免沿用旧结论。',
'更正记录醒目展示，保留历史版本；复核后重新审核发布。','不得静默覆盖，不得以“结论无影响”替代实际复核。','拦截')
labels={
'as_of':'数据截至时间','period':'统计期间','benchmark':'比较基准','yield_name':'收益率指标及口径','yield_value_pct':'收益率水平(%)','yield_change_bp':'收益率有符号变动(BP)','short_yield_name':'短端收益率指标','short_yield_change_bp':'短端变动(BP)','long_yield_name':'长端收益率指标','long_yield_change_bp':'长端变动(BP)',
'equity_name':'权益指数名称','equity_close':'权益指数收盘点位','equity_return_pct':'权益有符号涨跌幅(%)','bond_index_name':'债券价格指数名称','bond_return_pct':'债券价格指数有符号涨跌幅(%)','spread_name':'信用利差口径','spread_value_bp':'信用利差水平(BP)','spread_change_bp':'信用利差有符号变动(BP)',
'funding_name':'资金利率指标','funding_value_pct':'资金利率水平(%)','funding_change_bp':'资金利率有符号变动(BP)','convertible_name':'转债指数名称','convertible_close':'转债指数点位','convertible_return_pct':'转债有符号涨跌幅(%)','fx_market':'在岸/离岸市场','fx_pair':'汇率报价方向','fx_value':'汇率水平','fx_change_pct':'汇率报价有符号涨跌幅(%)','gold_name':'黄金现货/期货及市场','gold_currency':'黄金计价币种','gold_value':'黄金价格','gold_change_pct':'黄金有符号涨跌幅(%)','local_trade_date':'当地交易日','foreign_yield_name':'海外国家/期限收益率','foreign_yield_pct':'海外收益率水平(%)','foreign_yield_change_bp':'海外收益率有符号变动(BP)',
'issuer_name':'披露主体','event_type':'正式事件类型','official_url':'官方原文链接','event_date':'事件披露日期','exposure_status':'产品持仓核实状态','equity_group_a':'指数/行业A','equity_return_a_pct':'A有符号涨跌幅(%)','equity_group_b':'指数/行业B','equity_return_b_pct':'B有符号涨跌幅(%)','policy_name':'政策名称','policy_date':'政策发布日期','effective_date':'生效安排','confirmed_policy_summary':'已确认政策内容','macro_name':'经济指标名称及口径','release_date':'数据发布日期','actual_value':'实际公布值','consensus_value':'发布前一致预期值','consensus_as_of':'一致预期采样时点','macro_unit':'经济指标单位','event_name':'事件名称','confirmed_facts':'已确认事实','event_time':'事件时点','verification_status':'核实状态','product_name':'产品名称','nav_date':'产品净值日期','nav_value':'官方净值','nav_benchmark':'产品比较基准','nav_change_pct':'产品净值有符号变化(%)','manager_disclosure_url':'管理人正式披露链接','official_service_channel':'正式查询反馈渠道','last_valid_as_of':'最后有效数据时点','missing_metric_names':'待核实指标','data_quality_status':'数据质量状态','corrected_metric_name':'更正指标','old_value':'原值及单位','new_value':'新值及单位','correction_reason':'经核实的更正原因','previous_version':'原内容版本','current_version':'更正版本','source_url':'更正信息来源'}
variables={'期间':'period','数据时点':'as_of','比较基准':'benchmark','收益率指标':'yield_name','收益率水平':'yield_value_pct','上行幅度':'yield_change_bp','下行幅度':'yield_change_bp','短端收益率指标':'short_yield_name','短端变动':'short_yield_change_bp','长端收益率指标':'long_yield_name','长端变动':'long_yield_change_bp','信用利差口径':'spread_name','利差水平':'spread_value_bp','扩大幅度':'spread_change_bp','收窄幅度':'spread_change_bp','披露日期':'event_date','披露主体':'issuer_name','事件类型':'event_type','已确认事实':'confirmed_facts','资金利率指标':'funding_name','利率水平':'funding_value_pct','下降幅度':'funding_change_bp','权益指数':'equity_name','指数点位':'equity_close','上涨幅度':'equity_return_pct','下跌幅度':'equity_return_pct','权益涨跌幅':'equity_return_pct','债券指数':'bond_index_name','债券涨跌幅':'bond_return_pct','指数/行业A':'equity_group_a','指数/行业B':'equity_group_b','A涨跌幅':'equity_return_a_pct','B涨跌幅':'equity_return_b_pct','转债指数':'convertible_name','转债点位':'convertible_close','在岸/离岸':'fx_market','汇率水平':'fx_value','变动幅度':'fx_change_pct','黄金价格指标及币种':'gold_display_name','价格水平':'gold_value','当地数据时点':'local_as_of','当地时区':'local_timezone','净值类型':'nav_type','比较净值日期':'comparison_nav_date','比较净值':'comparison_nav_value','正式服务渠道':'official_service_channel','海外收益率指标':'foreign_yield_name','权益跌幅':'equity_return_pct','债券价格指数':'bond_index_name','债券跌幅':'bond_return_pct','权益涨幅':'equity_return_pct','债券涨幅':'bond_return_pct','发布主体':'policy_issuer','发布日期':'release_date','政策名称':'policy_name','已确认内容':'confirmed_policy_summary','生效安排':'effective_date','经济指标':'macro_name','实际值':'actual_value','单位':'macro_unit','预期采样时点':'consensus_as_of','预期值':'consensus_value','核实时间':'as_of','事件名称':'event_name','管理人/销售机构正式披露':'nav_source_name','产品名称':'product_name','净值日期':'nav_date','产品净值':'nav_value','产品比较基准':'nav_benchmark','净值变动':'nav_change_pct','待核实指标':'missing_metric_names','最后有效时点':'last_valid_as_of','更正时间':'as_of','更正指标':'corrected_metric_name','原值':'old_value','新值':'new_value','经核实的更正原因':'correction_reason','原版本号':'previous_version','复核结果':'correction_conclusion'}
labels.update({'policy_issuer':'政策发布主体','nav_source_name':'净值正式披露主体','correction_conclusion':'更正后结论复核结果','local_as_of':'当地数据时点','local_timezone':'当地时区或UTC偏移','comparison_nav_date':'比较净值日期','comparison_nav_value':'比较净值数值','return_method':'净值变动计算与分红处理方法','correction_review_status':'更正复核状态','gold_display_name':'黄金市场/类型/币种组合展示名','nav_type':'单位/累计等净值类型','nav_adjustment_status':'分红、折算等可比性核实状态'})
# 为同名占位词设置场景级字段，避免把转债或资金幅度错误绑定至权益字段。
for s in scenes:
 v=dict(variables)
 if s['id']=='S08': v['上行幅度']='funding_change_bp'
 if s['id'] in ['S13','S14']:v['上涨幅度']='convertible_return_pct';v['下跌幅度']='convertible_return_pct'
 if s['id'] in ['S17','S18']:v['上涨幅度']='gold_change_pct';v['下跌幅度']='gold_change_pct'
 if s['id'] in ['S19','S20']:v['上行幅度']='foreign_yield_change_bp';v['下行幅度']='foreign_yield_change_bp';v['收益率水平']='foreign_yield_pct'
 if s['id']=='S24':v['发布日期']='policy_date'
 for token in re.findall(r'〔([^〕]+)〕',' '.join(s[k] for k in ['fact','impact','talk','watch'])):
  field=v[token]
  if field not in s['fields']:s['fields'].append(field)
 s['bindings']={token:v[token] for token in re.findall(r'〔([^〕]+)〕',' '.join(s[k] for k in ['fact','impact','talk','watch']))};s['status']='draft';s['version']='1.0';s['source_requirements']='Wind指标、数据时点与同口径基准；事件另附正式原文；产品信息以管理人或销售机构正式披露为依据。'
 s['review_note']='内部内容及对客内容分别审核；任何数值、原因或结论变更须重新复核。'
 s['reason']='原因尚待进一步核实。只有获得可追溯证据后，才补充经核实的解释。'
 s['daily_title']=s['name']
 s['weekly_title']='本周市场：'+s['name']
 s['alert_title']=s['name']
 s['file']=f"scenarios/{s['id']}_{s['name']}.md"

for s in scenes:
 if s['id']=='S29':
  s['optional_fields']=['last_valid_as_of']
  s['variants']={'fact_with_history':'截至〔核实时间〕，〔待核实指标〕尚未完成核实。最后可用数据时点为〔最后有效时点〕。','fact_no_history':s['fact']}
  s['bindings']['最后有效时点']='last_valid_as_of'
 if s['id']=='S30':
  s['fields']+=['correction_review_status','correction_conclusion']
  s['bindings']['复核结果']='correction_conclusion'
  s['variants']={'impact_pending':s['impact'],'impact_completed':'相关表格、图表及结论已复核并重新审核，结论为〔复核结果〕。具体产品信息仍以正式披露为准。'}
root.mkdir(parents=True,exist_ok=True);(root/'scenarios').mkdir(exist_ok=True)
(root/'scenarios.json').write_text(json.dumps({'version':'1.0','purpose':'内部情景模板草案；不是实时行情、产品营销或自动发布判断','scenarios':scenes,'report_template':{'title':'〔报告主题〕','meta':'〔机构/作者〕 · 原报告〔日期〕 · 判断期限〔期限〕','fact':'〔机构〕认为，在〔成立条件〕下，〔资产或市场判断〕。','impact':'依据为〔证据1—2条〕；若〔反向条件〕发生，原有判断可能需要调整。机构观点不等于具体产品的收益预测。','talk':'这是一家机构在特定日期、期限和条件下的观点，不能直接作为具体产品的交易依据。具体产品仍需核实投资范围、风险及管理人披露。','watch':'核对报告日期、判断期限、依据、风险及素材授权。','original_url':None,'status':'draft'}},ensure_ascii=False,indent=2))
(root/'field-dictionary.json').write_text(json.dumps({'version':'1.0','fields':labels,'mapping_note':'业务字段契约，实际Wind表名和字段由现有后端映射；不包含数据库凭据。','variable_note':'Bindings将文案占位词关联业务字段；方向用有符号值校验，正文幅度按绝对值显示；文本上下文仍须审核。'},ensure_ascii=False,indent=2))
common='数据截至〔数据时点〕。市场数据来源：Wind〔指标口径〕；事件及产品信息来源：〔正式披露链接〕。市场指标不等于具体理财产品表现，实际影响需结合产品持仓、估值及管理人披露判断。本文供内部参考，涉及客户沟通须使用本机构审核内容。'
for s in scenes:
 fields='\n'.join(f"| `{f}` | {labels.get(f,f)} |" for f in s['fields'])
 special=''
 if s['id']=='S29':
  special='## 数据异常分支\n\n有历史有效数据时：'+s['variants']['fact_with_history']+'\n\n从未有有效数据时：'+s['variants']['fact_no_history']+'\n\nlast_valid_as_of允许为空，只阻断依赖缺失指标的内容。'
 if s['id']=='S30':
  special='## 更正复核分支\n\n尚未完成复核时：'+s['variants']['impact_pending']+'\n\n复核完成且重新审核后：'+s['variants']['impact_completed']+'\n\n后一个分支需correction_review_status为completed且复核结果完整。'
 text=f'''# {s['id']} {s['name']}

版本：1.0｜状态：内部模板草案，待机构审核｜关注级别：{s['priority']}

## 何时使用

{s['condition']}

只描述已核实变化。阈值由机构按指标、期间、历史波动与使用目的配置；本模板不默认设置统一数值门槛。

## 必需数据与证据

| 业务字段 | 含义 |
|---|---|
{fields}

{s['source_requirements']}

## 展示模板

**日评标题：**{s['daily_title']}

**周评标题：**{s['weekly_title']}

**异动标题：**{s['alert_title']}

**发生了什么**

{s['fact']}

**可能有什么影响**

{s['impact']}

**沟通参考（内部草案）**

{s['talk']}

**接下来关注**

{s['watch']}

{special}

## 原因如何表述

{s['reason']}

如需说明原因，单独记录证据、日期和链接；相关性不等于因果，不根据Wind价格变化自动生成确定归因。

## 本情景需避免的写法

{s['avoid']}

## 发布与消保要求

- 核对字段完整、日期与单位、比较基准、方向和来源，不将指数幅度套用到产品净值。
- 风险和限制与“可能影响”同屏，保留客户自主选择；不作统一加仓、赎回或换仓指令。
- 不预测单只产品收益，不承诺本金、收益、回本时间或限定损失。
- {s['review_note']}
- 产品风险或重大事项按机构流程提供正式查询、反馈渠道；具体产品推介另走销售和适当性流程。
- 数据/证据不足时使用S29；发布后更正使用S30。

## 统一尾注

{common}

## 维护方式

本文件与scenarios.json中的{s['id']}对应。结构字段固定，填充数字不需要改小程序页面；内容审核通过后绑定数据快照和版本发布。对客材料的权限与发布状态应由服务端控制。
'''
 (root/s['file']).write_text(text)
print(f'已生成{len(scenes)}种情景及字段字典')
