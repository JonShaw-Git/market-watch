# 看市场 · 市场解读与情景模板

在线访问：https://jonshaw-git.github.io/market-watch/

公开源码：https://github.com/JonShaw-Git/market-watch

网页可在手机和电脑浏览器直接打开，无需登录。模板版本2.3.0；本期行情观察日为2026年10月23日。

## 页面

保留最初的市场摘要、4张行情卡、栏目列表与文案详情格式，沿用上一版蓝色和浅紫色配色。栏目包括市场解读（每日简评/每周回顾）、研报精选、异动点评；所有资产相关内容统一展示，支持关键词搜索、模板查看、复制与下载，不提供收藏或资产分类筛选。网页不上传客户信息。

每日简评与每周回顾采用“一句话看点—行情速览（债市/股市/商品）—重点事件—风险提示”结构，资产观察在同一篇正文内连续呈现，不增加分类导航。另含极简卡片预览和复制按钮，适合小程序列表；沟通参考与后续关注折叠展示。研报精选保留原有正文结构；异动点评采用用户图片对应的三段式标准结构。本期真实行情快照与待填情景模板分开展示，后者不冒充当前市场数据。文案均保留内部草案或待填待审状态。

## 60种常见情景与240套模块

`dist/template-library.json`是页面读取的统一文案源：60种常见情景，每种包含每日简评、每周回顾、研报精选、异动点评4类独立模块，共240套内容。情景覆盖常见情况，不是对未来市场状态的穷尽枚举；复合事件需人工选择与合并，不宜强行归入单一情景。

`dist/template-files/scenarios/`保留每种情景一份Markdown文件，包含该情景的全部4类文案。`dist/template-files/`还包含使用索引、审核与消保说明，以及同一份结构化JSON。完整文件随`dist/market-template-library.zip`提供下载；前端还可从JSON生成当前模块或当前情景的下载文案。

每套模块包含标题、摘要、观察时点、启用条件、两项关键指标、事实、可能影响、沟通参考、后续关注、来源要求、避免表述和风险提示。全部〔字段〕须经核实填充，不代表任何市场事实或机构观点已经发生。

原`dist/content-kit/`、`dist/content-kit.zip`和原30情景的生成脚本保留用于兼容；前30种情景沿用原ID、名称和事实/风险边界。当前页面的完整模板库以`template-library.json`为准，不应只更新旧包。

## 本期数据与Wind边界

已有Wind数据表及服务视为机构既有能力。本期日评观察2026.10.23，比较基准为10.22；周评观察最近完整交易周2026.10.19—10.23，以10.16为比较基准。使用已核对的公开历史行情，非实时数据，未从Wind读取。

`content-work/brief_format.py`统一维护简评结构与Markdown格式；本期简评读取已核实数据，未纳入的商品行情明确标注，不以截图中的示例行情替换本期数据。`brief.glance`维护各观察段的内容、状态和来源，`brief.events`只收录已核实事项，`brief.preview`维护卡片标题、摘要和风险提示。

`dist/market-edition.json`统一维护本期数据、日周摘要、解读、公开采访观点及来源。编辑源为`content-work/build_edition.py`，运行后生成`market-edition.json`、兼容用`overview.json`及`dist/editions/2026-10-24/`中的日评、周评、异动与机构观点文案。切换每日/每周时，页面同步切换相应区间的行情和解读。更新须把观察日、比较日、点位、单位、来源和文案作为同一批次复核；指数按同口径期末/基准计算涨跌，Shibor按利率差换算BP，不累加每日涨跌。

模板可沿用机构已有Wind表服务填充，记录表名/代码、字段、单位、口径、时点、比较基准和提取时间。接口密钥和数据库连接应留在服务端，不放入公开仓库或网页。旧`data-source.json`、`snapshot.example.json`和`content-kit/06_Wind字段与发布约定.md`作为兼容结构参考，不能据其存在宣称页面已连Wind。

数据核对完成不代表文案已获机构审核。机构观点条目明确标为公开采访摘读，不冒称独立研报；研报模板须核实原文、作者、日期、页码与素材授权。上线发布仍须按机构制度完成数据质量、权限、业务、合规及消保审核，页面状态不能替代授权。

## 维护与检查

在项目根目录运行命令。修改本期数据与解读后：

```sh
python3 content-work/build_edition.py
```

修改情景库时，编辑`content-work/build_complete_templates.py`；前30种情景的基础文案来自原`content-kit/scenarios.json`，如需调整，应先修改`build_scenarios.py`并运行原包生成与校验，再重建完整库：

```sh
python3 content-work/build_scenarios.py
python3 content-work/validate_content.py
python3 content-work/build_complete_templates.py
python3 content-work/validate_complete.py
```

仅调整新增情景或4类模块结构时，执行后两条即可。生成脚本同步重建JSON、60份情景Markdown和ZIP；校验脚本检查60个连续ID、240套模块、完整字段和下载包有效性，避免页面与下载内容脱节。

界面主要编辑`dist/index.html`、`dist/styles.css`和`dist/app.js`。旧`edition-view.js`为兼容文件，当前页面不引用。发布前执行：

```sh
node --check dist/app.js
python3 content-work/validate_complete.py
```

本地预览：

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

## 文案审核与消保

事实可核实，观点保留前提，原因未知时写明待核实，风险与内容同屏。市场指标不等于具体产品表现；净值变化须核实持仓、估值、分红和费用口径，具体产品信息以管理人及销售机构正式披露为准。

不承诺本金、收益或回本时间，不给统一买卖指令，不传播未经确认的名单或细节。涉及产品开放限制、回撤或未确认事件时默认先内部核实，尊重客户知情权和自主选择，并按机构制度提供正式查询、反馈及投诉渠道。更正保留原值、新值、原因、时间和旧版记录，重新审核后发布。

## 每日简评标准样版

`content-work/build_daily_standard.py`完整转录用户图片，运行后生成`dist/daily-standard.json`及`dist/daily-standard.md`。页面每日简评优先展示此标准样版，含一句话看点、行情速览、四条重点事件、风险提示、极简卡片及运营复用说明；已核实本期内容折叠保留。图片日期为样例日期，行情、事件及机构口径尚未核验，不表示机构已审核。原文与说明均随复制、下载保留。

## 异动点评标准模板

`content-work/build_alert_standard.py`整理用户图片中的可见内容，保留原文标题、示例归因、短期/中长期展望、三类配置参考、风险提示、卡片摘要及运营说明，生成`dist/alert-standard.json`和`dist/alert-standard.md`。图片底部截断部分不补写。模板标注为用户示例、待填待核验和待机构审核，原文中的机构名称与合规口径不代表授权或审核通过。

`content-work/alert_format.py`统一维护异动点评结构及Markdown生成；本期参考与60种情景均采用开篇导语—异动原因—短期/中长期展望—配置参考—风险提示—卡片摘要。未核实驱动因素保留未知，不把图片中的示例判断套用到本期事实。服务入口仅为待配置示意，不收集客户数据；配置话术须满足机构适当性要求。完整模板包同时包含每日简评和异动点评标准样版。

## GitHub Pages发布

此发布副本保留编辑源`dist/`、内容生成脚本及完整`template-files/`目录，`docs/`是生成的静态发布目录。仓库设置 **Settings → Pages → Build and deployment → Deploy from a branch**，分支选`main`，目录选`/docs`。公开访问地址为：https://jonshaw-git.github.io/market-watch/ 。

完成上述数据、文案或界面更新并核对后执行：

```sh
python3 scripts/prepare-pages.py
```

脚本将完整`dist/`同步到`docs/`，包含每情景Markdown、JSON和ZIP，加上`.nojekyll`。资源和下载使用相对路径，兼容`/<仓库名>/`子路径。可用`python3 -m http.server 8765 --bind 127.0.0.1 --directory docs`预览。确认后将改动提交并推送到`main`，Pages按原地址重新发布，无需新增Actions工作流。

不要直接修改`docs/`。同步脚本检查目录边界、拒绝符号链接，并通过`scripts/.pages-manifest.json`核对上一次生成结果；发现人工修改时停止以防覆盖。此清单应随内容一起提交。上传时包含`dist/`、`docs/`、`content-work/`、`scripts/`和README，排除`.git/`历史、`.openai/`、凭据、缓存与临时QA文件。通过GitHub网页上传超过100个文件时，可按直接父目录分批上传，保持原目录结构。
