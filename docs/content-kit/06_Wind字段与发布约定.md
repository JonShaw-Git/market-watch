# 已有Wind数据表的字段与发布约定

本方案不改变既有Wind取数链路。由现有后端将业务字段映射为统一快照，小程序按同一展示结构读取。

## 示例对象

snapshot.example.json中所有值均为null或空对象，防止将模拟数据当作真实行情。正式环境可把data-source.json的snapshot_url设置为自有同源业务接口，并保留认证与权限校验。

关键字段：scene_id、as_of、period、benchmark、quality_status、review_status、snapshot_id、content_version、template_version、validated_scene_id、audience、external_use_allowed、source_refs、fields。

fields中业务字段可为字符串、数值，或包含value、unit、as_of、source、definition的对象。业务字段含义见field-dictionary.json；实际Wind表名、代码和列名由已有系统映射，不在小程序写数据库信息。

事件和产品披露字段不能从市场指标臆造。若Wind表没有这些信息，使用机构已有的公告/产品披露来源补齐；补不齐则暂停对应事实或选择S29。

## 填充规则

- 正文的〔占位词〕通过scenarios.json的bindings映射到fields。
- 数值校验采用有符号变动；“上行/下行XBP”等方向明确句中的X按绝对值显示，不能写成“下降-5BP”。
- 汇率方向、指数类型、收益率/价格、日期及基准必须匹配场景条件。
- 涨跌方向不能机械决定原因，也不能自动决定对客户的操作建议。
- 周评需独立快照和周度比较基准，不能用日快照替代。页面演示的日/周切换只是模板预览。
- 模板演示值缺失时展示占位符；正式发布模式缺少必要字段时应返回不可发布状态，不输出含占位符的客户材料。

## 发布约定

后台服务完成数据质量检查、场景条件验证、机构审核和使用权限判断。前台显示的状态不是权限凭证。对客材料请求须由服务端核对review_status、external_use_allowed、audience和素材授权；不能仅凭前端按钮决定是否放行。

本次页面默认模板演示模式，所有文案为内部草案；复制和下载均保留草案标识。正式环境的“复制已审客户版”只使用服务端签发的已审版本。

已发布正文、表格与数据卡片绑定snapshot_id和content_version，后续行情刷新不静默改变历史内容；修订走S30并留存旧版本。
