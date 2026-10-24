# 看市场 · 市场解读与情景模板

在线访问：https://jonshaw-git.github.io/market-watch/

公开源码：https://github.com/JonShaw-Git/market-watch

网页可在手机和电脑浏览器直接打开，无需登录。模板版本2.0；本期行情观察日为2026年10月23日。

## 页面

保留最初的市场摘要、4张行情卡、栏目列表与文案详情格式，沿用上一版蓝色和浅紫色配色。栏目包括市场早知道（日评/周评）、研报精读、异动快评和我的收藏；支持关键词搜索、资产分类、模板查看、复制与下载。收藏仅保存在当前浏览器，不上传客户信息。

正文保持事实、可能影响、沟通参考、关注点、风险及来源的统一结构。本期真实行情快照与待填情景模板分开展示，后者不冒充当前市场数据。文案均保留内部草案或待填待审状态。

## 60种常见情景与240套模块

`dist/template-library.json`是页面读取的统一文案源：60种常见情景，每种包含每日解读、每周回顾、研报精读、异动快评4类独立模块，共240套内容。情景覆盖常见情况，不是对未来市场状态的穷尽枚举；复合事件需人工选择与合并，不宜强行归入单一情景。

`dist/template-files/scenarios/`保留每种情景一份Markdown文件，包含该情景的全部4类文案。`dist/template-files/`还包含使用索引、审核与消保说明，以及同一份结构化JSON。完整文件随`dist/market-template-library.zip`提供下载；前端还可从JSON生成当前模块或当前情景的下载文案。

每套模块包含标题、摘要、观察时点、启用条件、两项关键指标、事实、可能影响、沟通参考、后续关注、来源要求、避免表述和风险提示。全部〔字段〕须经核实填充，不代表任何市场事实或机构观点已经发生。

原`dist/content-kit/`、`dist/content-kit.zip`和原30情景的生成脚本保留用于兼容；前30种情景沿用原ID、名称和事实/风险边界。当前页面的完整模板库以`template-library.json`为准，不应只更新旧包。

## 本期数据与Wind边界

已有Wind数据表及服务视为机构既有能力。本期日评观察2026.10.23，比较基准为10.22；周评观察最近完整交易周2026.10.19—10.23，以10.16为比较基准。使用已核对的公开历史行情，非实时数据，未从Wind读取。

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

## GitHub Pages发布

此发布副本保留编辑源`dist/`、内容生成脚本及完整`template-files/`目录，`docs/`是生成的静态发布目录。仓库设置 **Settings → Pages → Build and deployment → Deploy from a branch**，分支选`main`，目录选`/docs`。公开访问地址为：https://jonshaw-git.github.io/market-watch/ 。

完成上述数据、文案或界面更新并核对后执行：

```sh
python3 scripts/prepare-pages.py
```

脚本将完整`dist/`同步到`docs/`，包含每情景Markdown、JSON和ZIP，加上`.nojekyll`。资源和下载使用相对路径，兼容`/<仓库名>/`子路径。可用`python3 -m http.server 8765 --bind 127.0.0.1 --directory docs`预览。确认后将改动提交并推送到`main`，Pages按原地址重新发布，无需新增Actions工作流。

不要直接修改`docs/`。同步脚本检查目录边界、拒绝符号链接，并通过`scripts/.pages-manifest.json`核对上一次生成结果；发现人工修改时停止以防覆盖。此清单应随内容一起提交。上传时包含`dist/`、`docs/`、`content-work/`、`scripts/`和README，排除`.git/`历史、`.openai/`、凭据、缓存与临时QA文件。通过GitHub网页上传超过100个文件时，可按直接父目录分批上传，保持原目录结构。
