# 看市场 · 简明情景模板

在线访问：https://jonshaw-git.github.io/market-watch/

公开源码：https://github.com/JonShaw-Git/market-watch

网页可在手机和电脑浏览器直接打开，无需登录。


版本：2026.10.24，替换此前复杂的仪表盘设计。

## 页面

首屏为本期视角与4张行情卡，采用浅蓝、浅紫与白色卡片。下方保留市场解读（日/周）、研报观点、异动点评。每篇只有2项关键指标、事实、可能影响、沟通参考和关注点。来源与维护文件默认收起，无侧栏、复杂图表、产品推荐或交易入口。

## 文案文件

`dist/content-kit/`包含30个独立情景MD、统一JSON文案与字段字典，以及7份使用/审查/栏目展示/字段维护说明。`dist/content-kit.zip`可整体下载。`content-work/build_scenarios.py`生成情景文件和JSON；`content-work/validate_content.py`校验变量并打包。修改文案后运行生成、校验脚本，避免MD与JSON不一致。

## 数据

已有Wind数据表/服务视为既有能力。本期默认为2026.10.23日评及最近完整交易周2026.10.19—10.23周评，采用经核对的公开历史行情，未声称从Wind读取。`dist/market-edition.json`统一维护本期数据、日周摘要、解读、公开采访观点及来源，切换每日/每周会同步更新首屏与正文。

本期编辑源为`content-work/build_edition.py`，运行后统一生成`market-edition.json`、兼容用的`overview.json`及`dist/editions/2026-10-24/`四份文案。更新须把观察日、比较日、点位、来源和文案作为同一批次核对；指数按期末/基准计算，Shibor按利率差换算BP。不能累加每日涨幅，也不能将其他债券指数当作同一指标。

内容选择中保留30种情景模板，用占位词表示待填字段。`dist/data-source.json`定义情景模板的同源快照路径，正式数据结构参见`content-kit/06_Wind字段与发布约定.md`及`snapshot.example.json`。本期解读与情景占位字段独立；真实数据核对完成不代表对客文案已获机构审核。机构观点条目明确标为公开采访摘读，不能冒称独立研报。

前台只有在质量通过、场景验证一致及期间类型一致时才取用正式快照；上线时后台仍须独立执行数据质量、机构权限、审核和素材授权校验。不能把前台状态当作授权。当前复制和下载均标为内部待审草案。

## 内容约束

参考截至2026.10.24已生效的适当性、网络营销及消保规则，强调事实可核实、观点有条件、风险同屏和客户自主选择。模板不构成已获机构审核的客户材料。具体产品信息依赖正式披露，净值变化需核实分红和口径；来源修订需重新审核并保留旧版。

## 本地运行

`python3 -m http.server 8765 --bind 127.0.0.1 --directory dist`

检查：`node --check dist/app.js` 和 `python3 content-work/validate_content.py`。

## GitHub Pages 公开访问

此仓库保留编辑源 `dist/` 和内容生成脚本，`docs/` 是生成的静态发布目录。请使用公开仓库，进入 **Settings → Pages → Build and deployment**，选择 **Deploy from a branch**，分支选 `main`，目录选 `/docs`，保存。GitHub 完成发布后，该页会显示公开网址：`https://<账号>.github.io/<仓库名>/`；手机与电脑可直接访问，无需登录。此方式不需要新增 Actions 工作流。

首页 `docs/index.html` 位于 Pages 发布根目录，站内资源、JSON 和下载文件均使用相对路径，可兼容带仓库名的项目网址。`.nojekyll` 保留原始静态文件。复制本项目到新仓库时，不要上传原站点的 `.openai/`、凭据或历史 `.git/`。

### 更新数据或文案

先编辑 `content-work/build_edition.py` 的本期数据、日期、来源与文案，再在仓库根目录执行：

```sh
python3 content-work/build_edition.py
python3 content-work/validate_content.py
python3 scripts/prepare-pages.py
```

修改30种情景文案时，先编辑 `content-work/build_scenarios.py`，再执行：

```sh
python3 content-work/build_scenarios.py
python3 content-work/validate_content.py
python3 scripts/prepare-pages.py
```

界面修改直接编辑 `dist/index.html`、`dist/styles.css`、`dist/app.js` 或 `dist/edition-view.js`，再运行 `python3 scripts/prepare-pages.py`。可用 `python3 -m http.server 8765 --bind 127.0.0.1 --directory docs` 在本地预览发布结果。核对完成后，将改动提交并推送到 `main`，Pages 会按同一路径重新发布。

不要直接修改 `docs/`。同步脚本会检查目录边界、拒绝符号链接，并通过 `scripts/.pages-manifest.json` 核对上一次生成结果；若发现手工改动，会停止，避免覆盖。该清单应随页面一起提交。
