# 证券公告资料

这里提供上市公司公告资料的本地演练来源与基础采集。目录有稳定标识，详情随发布期改变；合成资料位于 fixtures/source.json。app.capture 读取来源，app.domain 解释业务身份，app.records 保存原始收据与最近访问页。当前收据只表明资料已被读取，不表示完整发布结论。

- python -m unittest discover -s tests -v：运行本地来源测试。
- python -m compileall -q app tests：检查项目代码。
- python -m app.site：在 8765 端口启动演练来源。
- python -m app.cli：另一个终端读取演练来源。
