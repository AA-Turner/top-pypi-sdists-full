"""_site_defaults.py — 站点默认值（**构建期注入，源码里恒为空**）。

为什么需要这一层：v0.8 的「三参数起步」希望用户不必记 apiserver 地址，但把内网域名写进
源码会随**公网 PyPI** 包一起发出去，泄漏内网拓扑——而这正是发布流水线泄漏门禁要拦的东西。
两个目标不能同时靠一个硬编码常量满足。

解法是把站点默认值收敛到本模块这**一个赋值**上，并区分发布渠道：

* 仓库源码与**公网** PyPI 包：``API_BASE = ""``——不含任何内网信息，泄漏门禁自然通过。
  公网用户仍用 ``INSTANCEREPO_API_BASE`` 指定地址（他们本来也连不上内网控制面）。
* **内网**渠道（ArtLab PyPI / OSS 归档）：构建脚本把本文件的 ``API_BASE`` 改写成部署方的
  apiserver 根地址，内网用户因此享受三参数起步。

注入方式刻意选「改写一个模块级字符串常量」而不是环境变量或配置文件：它在打包产物里是
静态可审计的（``grep`` 一下就知道这份包带没带默认值），也不会引入运行期的文件查找与
失败模式。

优先级不受影响，始终是：显式构造参数 > ``INSTANCEREPO_API_BASE`` > 本模块的站点默认 >
空（空则在真正发控制面请求时报错并引导配置）。
"""
from __future__ import annotations

#: apiserver 根地址的站点默认值。源码里恒为空串；内网构建时由发布脚本注入。
#: 改动本行时请同时更新 sdk/go/site_defaults.go 的 ``DefaultAPIBase``（Go 侧为包级
#: **var**，内网渠道经 ``-ldflags -X`` 注入）与 Java 侧 ``SiteDefaults.API_BASE``
#: （三语言须一致，且各自保留构建期注入方式）。
API_BASE = ""

#: AP job 查询端点（artifact 下载用）的站点默认值。源码里恒为空串；内网构建时注入。
AP_ENDPOINT = ""

#: artifact 对象的 OSS 前缀根（如 {root}/{job_id}/result.tgz）。源码恒为空；
#: 内网构建时注入。
ARTIFACT_PREFIX_ROOT = ""

#: 「AP cluster 名 → artifact OSS bucket」映射的 JSON 串。源码恒为空；内网构建时
#: 注入。运行时也可经环境变量 AP_ARTIFACT_BUCKET_MAP（JSON）覆盖，优先级：
#: 环境变量 > 本模块注入值 > 空（空则 artifact 下载报错并引导配置）。
ARTIFACT_BUCKET_MAP_JSON = ""

#: 期望 replica policy（canonical 双桶对）的 JSON 串。**源码恒为空**；
#: 内网构建时由发布脚本注入（与 API_BASE 同模式——静态可审计、无
#: envvar 通道）。运行时解析为 ``ReplicasPolicy``（严格 JSON/拒重复
#: keys/构造验证）；公共包通过显式构造参数传入有效 policy 亦可运行。
#: 优先级：显式构造参数 > 本模块注入值 > 缺失（缺失=新客户端零 IO
#: typed error）。
EXPECTED_REPLICA_POLICY_JSON = ""
