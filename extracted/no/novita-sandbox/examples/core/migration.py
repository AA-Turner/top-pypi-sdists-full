"""跨集群迁移（Migration）完整链路示例 —— Novita 高层 facade 版。

对齐平台契约 0.2.0：受理只回 ``jobId``，状态是一个「5 态 + 计数 + 逐项明细」的
投影，批量是**一次原生请求**（1 个 job 覆盖 N 个资源）。两个容易踩的契约点：

- sandbox 迁移的 ``template_alias`` 是**选填**参数：不传或传 None 时，
  SDK 不发送该字段。模板分发仍要求显式指定别名（见下文专节）。
- 取消（cancel）是**回滚**：runner 会把已经搬过去的资源撤回，期间状态是
  ``reverting``；过了不可回滚点则抛 ``CancelTooLateError``。

场景
----
某客户的 agent sandbox 跑在 ``us-phx-1``，因为用户主要在美东，需要把 sandbox
连同它依赖的模板一起搬到 ``us-east-1``。

facade 的用法
-------------
``Novita`` 是高层客户端，按 **namespace** 组织资源：``client.sandbox``、
``client.template``、``client.volume``、``client.secret``、``client.job``。
构造时给一次连接配置，之后所有调用自动继承。

迁移场景里最舒服的写法是**建两个 client**：一个绑源集群、一个绑目标集群。

    source = Novita(api_key=..., domain="us-phx-1.sandbox.novita.ai")
    target = Novita(api_key=..., domain="us-east-1.sandbox.novita.ai")

    job_id = target.job.migrate_sandbox(
        sandbox_id,
        source_region="us-phx-1",
    )

为什么要两个？因为**目标集群不是一个参数，而是由请求域名决定的**。平台在反代层
把 ``api.<domain>`` 路由到对应集群，并从 Host 反推目标 region。所以：

- 「发起迁移」要打到**目标**集群 → 用 ``target``；
- 「读源集群上的 sandbox」要打到**源**集群 → 用 ``source``；
- 迁移成功后，同一个 ``sandbox_id`` 用 ``target.sandbox.connect(...)`` 就能连上。

``source_region`` 只是告诉平台「资源现在在哪」。它和目标集群写反会被平台以 400
拒绝（SDK 抛 ``InvalidArgumentException``）。

也可以只建一个 client，在单次调用上临时覆盖 domain：

    client.job.migrate_sandbox(
        sandbox_id,
        source_region="us-phx-1",
        template_alias="my-base-from-us-phx-1",
        domain="us-east-1.sandbox.novita.ai",
    )

关于 template_alias（sandbox 迁移选填）
----------------------------------
alias 是资源落到**目标集群**后使用的名字。SDK 的规则：

- ``migrate_sandbox`` / ``migrate_sandboxes`` 可省略 ``template_alias`` 或传
  None，请求里的资源只有 ``{"id": ...}``，SDK 不生成别名；
- 模板分发（``distribute_template`` / ``distribute_templates``）仍然必填。
  指定别名时，资源为 ``{"id": ..., "template_alias": ...}``；
- 单资源方法接收一个字符串；
- 批量方法（``migrate_sandboxes`` / ``distribute_templates``）接收一个字符串
  或 ``callable(resource_id) -> alias``。N 个 sandbox 共用同一个 base template
  时，一个固定字符串就是正确用法；N 个**不同模板**共用一个字符串会全部撞名，
  SDK 在本地直接拒绝（``InvalidArgumentException``）；
- 空白串（或只有空格）在**发请求之前**就抛 ``InvalidArgumentException``，
  平台永远收不到空 alias；模板分发省略该参数则是 Python 的 ``TypeError``；
- 值原样透传：SDK 不 trim、不补全、不生成，平台也同样不 trim。alias 里的
  空格与大小写以你写的为准。

示例通过可选的 ``NOVITA_TEMPLATE_ALIAS`` 配置 sandbox 迁移别名；未设置时
不发送 alias。模板分发的示例始终显式指定别名。

运行
----
    export NOVITA_API_KEY=...
    export NOVITA_SANDBOX_ID=i6vodj9qkv3o4b0te0obn     # 源集群上的 sandbox
    export NOVITA_SOURCE_REGION=us-phx-1
    export NOVITA_SOURCE_DOMAIN=us-phx-1.sandbox.novita.ai
    export NOVITA_TARGET_DOMAIN=us-east-1.sandbox.novita.ai
    # export NOVITA_TEMPLATE_ALIAS=migration-demo-001  # 可选：目标集群上的别名
    python examples/core/migration.py

    # 可选：目标 region 默认从 NOVITA_TARGET_DOMAIN 的第一段推出
    # export NOVITA_TARGET_REGION=us-east-1

    # 顺带跑一遍异步版本（facade 是同步的，异步走 AsyncJob 类）
    NOVITA_RUN_ASYNC=true python examples/core/migration.py
"""

import asyncio
import os
import time
from typing import Optional

from dotenv import load_dotenv

from novita_sandbox.core import (
    AsyncJob,
    CancelTooLateError,
    JobCancelledError,
    JobFailedError,
    JobStatus,
    JobType,
    MigrationConflictError,
    MigrationItemStatus,
    MigrationNotSupportedError,
    MigrationStatus,
    Novita,
    ResourceAlreadyMigratingError,
    SharedDependencyError,
    TemplateAliasConflictError,
)
from novita_sandbox.core.exceptions import (
    AuthenticationException,
    InvalidArgumentException,
    NotFoundException,
    RateLimitException,
    SandboxException,
    TimeoutException,
)

load_dotenv()


API_KEY = os.getenv("NOVITA_API_KEY")
SANDBOX_ID = os.getenv("NOVITA_SANDBOX_ID")
TEMPLATE_ID = os.getenv("NOVITA_TEMPLATE_ID")

SOURCE_REGION = os.getenv("NOVITA_SOURCE_REGION", "us-phx-1")
SOURCE_DOMAIN = os.getenv("NOVITA_SOURCE_DOMAIN", "us-phx-1.sandbox.novita.ai")
TARGET_DOMAIN = os.getenv("NOVITA_TARGET_DOMAIN", "us-east-1.sandbox.novita.ai")
TARGET_REGION = os.getenv("NOVITA_TARGET_REGION", TARGET_DOMAIN.split(".")[0])

#: sandbox 迁移时可选的目标模板别名。未设置时为 None，SDK 不发送该字段；
#: 指定别名时，应确保它没有被目标集群上的其他模板占用。
TEMPLATE_ALIAS = os.getenv("NOVITA_TEMPLATE_ALIAS")

RUN_ASYNC = os.getenv("NOVITA_RUN_ASYNC", "false").lower() == "true"


def build_clients() -> tuple[Novita, Novita]:
    """一个绑源集群，一个绑目标集群。连接配置只写一次。"""
    source = Novita(api_key=API_KEY, domain=SOURCE_DOMAIN)
    target = Novita(api_key=API_KEY, domain=TARGET_DOMAIN)
    return source, target


def _wire_status(status: object) -> str:
    """枚举或平台新加的未知状态串，都取 wire 值。"""
    return getattr(status, "value", status)


def _status_counts(items: list[MigrationItemStatus]) -> dict[str, int]:
    """把逐项状态压成 ``{wire_status: count}``，用于一行式汇总。"""
    counts: dict[str, int] = {}
    for item in items:
        key = _wire_status(item.status)
        counts[key] = counts.get(key, 0) + 1
    return counts


def _print_items(
    status: MigrationStatus, indent: str = "    ", max_open: int = 3
) -> None:
    """打印逐项进度：一段紧凑汇总 + 最多 ``max_open`` 个未完成项。

    ``status.items`` 只在**单条 job 的响应**（``get`` / ``cancel`` / 每次
    ``wait`` 轮询）里有值；``list`` 分页只有计数，这里会明确说明，而不是假装
    0 项。
    """
    items = status.items
    if not items:
        print(f"{indent}items:      未提供（list 分页只有计数；get/cancel/wait 才有逐项）")
        return

    counts = _status_counts(items)
    summary = " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    base = sum(1 for item in items if item.resource_type == "base")
    note = f"，其中 base={base}（不计入 total）" if base else ""
    print(f"{indent}items:      {len(items)} 项（{summary}{note}）")

    # 只列未完成的项；失败/回滚中的项最有用，completed 不占行。
    unfinished = [item for item in items if item.status != JobStatus.COMPLETED]
    for item in unfinished[:max_open]:
        print(f"{indent}            - {item.resource_type}/"
              f"{item.resource_id} -> {_wire_status(item.status)}")
    if len(unfinished) > max_open:
        print(f"{indent}            ... 还有 {len(unfinished) - max_open} 项未完成")


def _print_status(status: MigrationStatus, indent: str = "    ") -> None:
    print(f"{indent}job_id:     {status.job_id}")
    print(f"{indent}status:     {_wire_status(status.status)}")
    print(f"{indent}counters:   completed={status.completed} "
          f"failed={status.failed} cancelled={status.cancelled} "
          f"total={status.total}")
    _print_items(status, indent)


# --------------------------------------------------------------------------- #
# Step 1 · 迁移前：从源集群确认资源
# --------------------------------------------------------------------------- #


def step1_inspect_source(source: Novita):
    print("\n[1] 用 source client 确认 sandbox 与它依赖的模板")

    info = source.sandbox.get_info(SANDBOX_ID)
    print(f"    sandbox_id:  {info.sandbox_id}")
    print(f"    state:       {info.state}")
    print(f"    template_id: {info.template_id}")
    print(f"    started_at:  {info.started_at.isoformat()}")
    print(f"    end_at:      {info.end_at.isoformat()}")

    template = source.template.get(info.template_id)
    print(f"    template:    {template.names or template.aliases}")

    return info


# --------------------------------------------------------------------------- #
# Step 2 · 用 target client 发起迁移
# --------------------------------------------------------------------------- #


def step2_start_migration(target: Novita) -> str:
    print(f"\n[2] 用 target client 发起迁移：{SOURCE_REGION} -> {TARGET_DOMAIN}")

    # client 已经绑了目标集群的 domain，这里不用再传 domain。
    # 契约 0.2.0：受理响应只有 {jobId}，所以返回值就是 job_id 字符串。
    #
    # template_alias 选填：None 时资源只发送 {"id": sandbox_id}；指定别名时
    # 逐资源发送 {"id": sandbox_id, "template_alias": alias}。
    # SDK 不 trim / 不生成别名；显式传入空白串会在本地被拒绝。
    #
    # sandbox_id 既可以是短 id，也可以是 SDK 其它地方常用的
    # "<sandboxID>-<clientID>" 复合 id；migration-api 内部按短 id 记录。
    job_id = target.job.migrate_sandbox(
        SANDBOX_ID,
        source_region=SOURCE_REGION,
        template_alias=TEMPLATE_ALIAS,
    )

    print(f"    已受理，job_id={job_id}")
    print("    （状态是单独的查询，受理响应里不再携带）")

    # sandbox 依赖的 base template 由 migration-api 的 runner 在 planning 步
    # 自动搬：不产生额外的 job，但会以 resource_type="base" 的 item 出现在
    # status.items 里，而且**不计入 total**。所以 items 的条数可能比 total 大，
    # completed + failed + cancelled 也可能暂时小于 total。
    return job_id


# --------------------------------------------------------------------------- #
# Step 3 · 观察进度
# --------------------------------------------------------------------------- #


def step3_poll_progress(target: Novita, job_id: str) -> MigrationStatus:
    """手写轮询，适合要打日志 / 上报进度 / 做超时预算的场景。

    0.2.0 的状态投影自带四个计数（completed/failed/cancelled/total），
    以及单条查询才有的逐项明细 ``status.items``。所以进度可以按计数看，
    也可以按 item 归因到具体资源。

    ``items`` 的语义：``get``、``cancel`` 的响应，以及 ``wait`` 的每次轮询
    都会带；``list`` 分页一律为空。base 模板项会出现在 items 里但**不计数**，
    所以 completed + failed + cancelled 可能小于 total（还在飞、或正被回滚）。
    """
    print("\n[3] 轮询进度（手写，最多等 10 分钟）")

    deadline = time.monotonic() + 600
    last_status = None

    while True:
        status = target.job.get(job_id)

        if status.status != last_status:
            print(f"    {time.strftime('%H:%M:%S')}  status -> {_wire_status(status.status)} "
                  f"({status.completed}/{status.total})")
            _print_items(status, indent="      ")
            last_status = status.status

        if status.status == JobStatus.COMPLETED:
            print("    迁移成功")
            _print_status(status)
            return status

        if status.status == JobStatus.FAILED:
            _print_status(status)
            raise JobFailedError(
                f"迁移失败: {status.failed}/{status.total} 项失败", status=status
            )

        if status.status == JobStatus.CANCELLED:
            raise JobCancelledError("迁移被取消", status=status)

        # reverting 不是终态：cancel 已受理，runner 正在把搬过去的项回滚，
        # 继续等它落到 cancelled（回滚完成、源侧恢复完整）。
        if time.monotonic() >= deadline:
            raise TimeoutException(
                f"等待 job {job_id} 超时，最后状态 {_wire_status(status.status)}"
            )

        time.sleep(5)


def step3b_wait_shortcut(target: Novita, job_id: str) -> MigrationStatus:
    """等价的简写：facade 自带 wait()。

    wait() 的语义：completed 返回、failed 抛 JobFailedError、cancelled 抛
    JobCancelledError（两者都带 .status，含逐项 items）、超时抛 TimeoutException；
    reverting 不是终态，会继续轮询到回滚结束。
    注意契约没有定义「部分失败」的聚合规则：completed 一律返回，
    要严格全成的调用方自己检查 ``status.failed == 0``。
    """
    print("\n[3b] 用 target.job.wait() 一行搞定（生产里更常用）")

    try:
        status = target.job.wait(
            job_id,
            timeout=600,
            poll_interval=5,
            # 每次轮询都走单条查询，所以回调里的 s.items 一定有值，
            # 可以直接做逐项进度上报。
            on_progress=lambda s: print(
                f"    进度: completed={s.completed}/{s.total} "
                f"failed={s.failed} cancelled={s.cancelled} "
                f"items={len(s.items)}"
            ),
        )
        print(f"    完成：status={_wire_status(status.status)}")
        _print_items(status)
        if status.failed or status.cancelled:
            print("    注意：completed 但有失败/取消项，请按计数与 items 分流处理")
        return status
    except JobFailedError as exc:
        # 逐项**状态**在 exc.status.items 里；契约没有逐项错误文案。
        print(f"    失败：{exc.status.failed}/{exc.status.total} 项失败")
        _print_items(exc.status, indent="      ")
        raise
    except JobCancelledError as exc:
        print(f"    被取消：job_id={exc.status.job_id}")
        raise


# --------------------------------------------------------------------------- #
# Step 4 · 迁移后：从目标集群连上去验证
# --------------------------------------------------------------------------- #


def step4_verify_on_target(target: Novita):
    print("\n[4] 用 target client 连接迁移后的 sandbox 并跑一条命令")

    # 同一个 sandbox_id，但这次走 target client（domain 指向目标集群）。
    # 注意：迁移后 sandbox 的访问域名变了，连接必须走目标集群。
    sbx = target.sandbox.connect(SANDBOX_ID)

    result = sbx.commands.run("uname -a && cat /etc/hostname")
    print(f"    exit_code={result.exit_code}")
    print(f"    stdout: {result.stdout.strip()}")
    if result.stderr:
        print(f"    stderr: {result.stderr.strip()}")

    info = target.sandbox.get_info(SANDBOX_ID)
    print(f"    target 上可见: sandbox_id={info.sandbox_id}, state={info.state}")

    return sbx


# --------------------------------------------------------------------------- #
# Step 5 · 单独分发一个模板（不带 sandbox）
# --------------------------------------------------------------------------- #


def step5_distribute_template_only(target: Novita, template_id: str) -> MigrationStatus:
    print("\n[5] 单独把模板分发到目标集群（非破坏性，源模板照常可用）")

    try:
        job_id = target.job.distribute_template(
            template_id,
            source_region=SOURCE_REGION,
            # 必填：模板在目标集群落地时使用的别名。平台不会生成默认值，
            # SDK 也不 trim / 不生成；传空白串会在本地抛
            # InvalidArgumentException。这里用「源模板 id + 源 region」拼一个
            # 可读且大概率不重复的别名。
            template_alias=f"{template_id}-from-{SOURCE_REGION}",
        )
    except TemplateAliasConflictError as exc:
        # 409 MIGRATION_TEMPLATE_ALIAS_CONFLICT：job 没有建立，
        # 用同一个 alias 重试永远失败，必须换一个。
        print(f"    别名已被占用，换个 alias 重新受理: {exc}")
        raise

    print(f"    已受理，job_id={job_id}")

    status = target.job.wait(job_id, timeout=600, poll_interval=5)
    _print_status(status)
    return status


# --------------------------------------------------------------------------- #
# Step 6 · 历史与审计：过滤 + 分页列出全部 job
# --------------------------------------------------------------------------- #


def step6_audit_history(target: Novita):
    print("\n[6] 分页拉取迁移 job（最新在前），演示 0.2.0 的过滤参数")

    # 过滤参数：type / status（不再是 resource_type / state）；0.2.0 新增
    # source_region（从哪搬出）与 target_region（搬到哪）。目标集群由 domain
    # 决定，所以 target_region 一般就是 TARGET_REGION。
    #
    # 注意：list 返回的 status.items **一律为空**，只能看计数；要逐项明细，
    # 对单个 job_id 再调一次 target.job.get(job_id)。
    # limit 越界现在由平台以 400 VALIDATOR_PARAM 拒绝（SDK 抛
    # InvalidArgumentException），不再伪装成 500。
    cursor = None
    total = 0
    page_no = 0

    while True:
        page_no += 1
        page = target.job.list(
            job_type=JobType.SANDBOX_BATCH,
            status=JobStatus.COMPLETED,
            source_region=SOURCE_REGION,
            limit=20,
            cursor=cursor,
        )
        total += len(page.items)

        for status in page.items:
            print(f"    p{page_no}  {status.job_id}  "
                  f"{_wire_status(status.status):<10} "
                  f"{status.completed}/{status.total}")

        # next_cursor 为空串时 SDK 归一成 None，表示没有下一页
        if not page.next_cursor:
            break
        cursor = page.next_cursor

    print(f"    共 {total} 个 job，{page_no} 页")

    # 两个 region 过滤也可以一起用：只看「SOURCE_REGION -> TARGET_REGION」的 job。
    page = target.job.list(
        source_region=SOURCE_REGION,
        target_region=TARGET_REGION,
        limit=20,
    )
    print(f"    {SOURCE_REGION} -> {TARGET_REGION} 的 job 有 {len(page.items)} 个")

    # resource_id 过滤是「包含这个资源的 job」；计数仍覆盖整个 job 的所有项
    page = target.job.list(resource_id=SANDBOX_ID, source_region=SOURCE_REGION)
    print(f"    包含 {SANDBOX_ID} 的 job 有 {len(page.items)} 个")


# --------------------------------------------------------------------------- #
# Step 7 · 取消
# --------------------------------------------------------------------------- #


def step7_cancel(target: Novita, job_id: str):
    print(f"\n[7] 取消 job {job_id}（回滚已搬走的资源）")

    # 0.2.0 的 cancel 是**回滚**，不是「先标记一下等它自己停」：runner 会把
    # 这个 job 已经搬过去的资源撤回源侧。受理后状态是 reverting（不是终态），
    # 要轮询到 cancelled 才知道回滚完成、源侧恢复完整。
    # 过了不可回滚点（目标侧已提交）再取消会抛 CancelTooLateError，只能等它跑完。
    try:
        status = target.job.cancel(job_id)
    except CancelTooLateError as exc:
        print(f"    已过不可回滚点，只能等它跑完: {exc}")
        return
    except SharedDependencyError as exc:
        print(f"    有资源仍被依赖，无法回滚: {exc}")
        return

    print(f"    取消已受理，当前状态={_wire_status(status.status)}"
          "（reverting 不是终态，回滚完成后才是 cancelled）")
    _print_items(status)

    # 取消是幂等的：job 还没结束时重复 cancel 只会返回当前投影（仍在回滚就
    # 还是 reverting）。等到 cancelled 才算源侧恢复完整。
    try:
        final = target.job.wait(job_id, timeout=300, poll_interval=5)
        print(f"    最终状态={_wire_status(final.status)}")
    except JobCancelledError:
        print("    回滚完成，已确认取消")

    # 0.2.0 防探测：不存在 / 已全部终态 / 不属于你，三者同一个错误。
    # SDK 按 reason 映射成 NotFoundException（注意是 400 + RESOURCE_NOT_FOUND）。
    try:
        target.job.cancel(job_id)
    except NotFoundException as exc:
        print(f"    预期内的失败（已终态或不可见）: {exc}")


# --------------------------------------------------------------------------- #
# Step 8 · 错误处理：把每种失败分开处理
# --------------------------------------------------------------------------- #


def step8_error_handling(target: Novita):
    print("\n[8] 错误处理示范")

    def attempt(label, fn):
        try:
            fn()
            print(f"    {label}: 成功")
        except AuthenticationException as exc:
            print(f"    {label}: 鉴权失败（检查 NOVITA_API_KEY）: {exc}")
        except NotFoundException as exc:
            # 注意：job 不存在时平台返回的是 HTTP 400 + RESOURCE_NOT_FOUND，
            # 不是 404；SDK 已经按 reason 映射成 NotFoundException。
            print(f"    {label}: 资源不存在或不可见: {exc}")
        except TemplateAliasConflictError as exc:
            # 409 MIGRATION_TEMPLATE_ALIAS_CONFLICT：别名已被目标集群占用。
            # job 没有建立；用同一个 alias 重试永远失败，换一个再受理。
            print(f"    {label}: 目标集群别名冲突（409，换 alias）: {exc}")
        except ResourceAlreadyMigratingError as exc:
            # 409 MIGRATION_RESOURCE_ALREADY_MIGRATING：资源已在另一个 live job
            # 里。一个资源同时只能属于一个 job：等那个 job 结束，或取消它并等
            # 回滚完成，再重新受理。
            print(f"    {label}: 资源已在另一个迁移 job 中（409，等它结束）: {exc}")
        except CancelTooLateError as exc:
            # 409 MIGRATION_PAST_CANCEL_LINE：已过不可回滚点，cancel 被拒绝，
            # job 必须跑完。
            print(f"    {label}: 已过不可回滚点，只能等它跑完（409）: {exc}")
        except SharedDependencyError as exc:
            # 409 MIGRATION_SHARED_DEPENDENCY：还有别的资源依赖它，不能单独
            # 搬走/回滚。把依赖方放进同一个 job 一起搬。
            print(f"    {label}: 有共享依赖，需要一起迁移（409）: {exc}")
        except MigrationConflictError as exc:
            # 兜底：未知 reason 的 409 映射到基类（不再误判成 alias 冲突）；
            # 原始 reason 原样保留在 exc.reason 上，message 里也有一份。
            print(f"    {label}: 其它 409 冲突（reason={exc.reason}）: {exc}")
        except MigrationNotSupportedError as exc:
            # 501 MIGRATION_NOT_SUPPORTED：目标是 v1 集群，或该功能没开通。
            # 没有 job 被创建，重试也没用。
            print(f"    {label}: 目标集群不支持迁移（501）: {exc}")
        except InvalidArgumentException as exc:
            # 三类来源：SDK 本地参数校验（空 id、空白 template_alias）、
            # 平台 400 校验失败（source_region 写成目标集群，或 limit 越界
            # → VALIDATOR_PARAM；0.2.0 起 limit 越界不再伪装成 500）。
            print(f"    {label}: 参数非法: {exc}")
        except RateLimitException as exc:
            print(f"    {label}: 被限流，建议退避后重试: {exc}")
        except TimeoutException as exc:
            print(f"    {label}: 等待超时: {exc}")
        except JobFailedError as exc:
            print(f"    {label}: job 失败 "
                  f"({exc.status.failed}/{exc.status.total} 项): {exc}")
        except SandboxException as exc:
            # 500 现在是真正的服务端故障：reason / message 原样保留在异常里，
            # SDK 不做自动重试。
            print(f"    {label}: 其他失败: {exc}")

    attempt("不存在的 job",
            lambda: target.job.get("00000000-0000-0000-0000-000000000000"))
    attempt("source_region 填成目标集群",
            lambda: target.job.migrate_sandbox(
                SANDBOX_ID,
                source_region=TARGET_REGION,
                template_alias=TEMPLATE_ALIAS,
            ))
    attempt("空 sandbox_id",
            lambda: target.job.migrate_sandbox(
                "",
                source_region=SOURCE_REGION,
                template_alias=TEMPLATE_ALIAS,
            ))
    attempt("空白 template_alias（本地拒绝，不发请求）",
            lambda: target.job.migrate_sandbox(
                SANDBOX_ID,
                source_region=SOURCE_REGION,
                template_alias="   ",
            ))
    attempt("limit 越界（平台 400 -> InvalidArgumentException）",
            lambda: target.job.list(limit=1_000_000))


# --------------------------------------------------------------------------- #
# Step 9 · 生产级封装：只对确定可重试的情况退避
# --------------------------------------------------------------------------- #


def migrate_with_retry(
    target: Novita,
    sandbox_id: str,
    *,
    source_region: str,
    template_alias: Optional[str] = None,
    max_attempts: int = 3,
) -> MigrationStatus:
    """把「发起 + 等待」包一层，只对**确定可重试**的情况退避重试。

    注意 SDK 本身不做任何自动重试，而且 0.2.0 把可重试边界划得更清楚了：
    500 不再是「校验失败」的通道（limit 越界现在是 400），所以这里只重试
    限流。409 的每种冲突（别名被占、资源已在别的 job、过取消线、共享依赖）
    都必须先改请求，重试同一个请求必然再失败。
    """
    for attempt in range(1, max_attempts + 1):
        try:
            job_id = target.job.migrate_sandbox(
                sandbox_id,
                source_region=source_region,
                template_alias=template_alias,
            )
            print(f"    第 {attempt} 次受理成功 job_id={job_id}")
            return target.job.wait(job_id, timeout=1800, poll_interval=10)

        except RateLimitException:
            if attempt == max_attempts:
                raise
            backoff = 2 ** attempt
            print(f"    第 {attempt} 次被限流，{backoff}s 后重试")
            time.sleep(backoff)

        except (JobFailedError, JobCancelledError, MigrationConflictError,
                MigrationNotSupportedError, InvalidArgumentException):
            # 这些重试没有意义，直接抛给调用方
            raise


# --------------------------------------------------------------------------- #
# Step 10 · 批量迁移：一次原生请求（1 个 job 覆盖 N 个资源）
# --------------------------------------------------------------------------- #


def step10_batch_migrate(target: Novita, sandbox_ids: list) -> MigrationStatus:
    """一次搬多个 sandbox。

    0.2.0 的批量是**服务端原生**的：一次 POST，``resources`` 里放 N 个 item，
    平台建 1 个 job。返回一个 job_id，进度看四个计数 + ``status.items``。
    逐项结果现在**可以**从单条查询的 items 里读到（每项带 resource_type /
    resource_id / status）；契约没有逐项错误文案，但足以定位「哪个资源没成」。
    """
    print("\n[10] 批量迁移（一次原生请求，1 个 job 覆盖 N 个资源）")

    job_id = target.job.migrate_sandboxes(
        sandbox_ids,
        source_region=SOURCE_REGION,
        # 这些 sandbox 共享同一个 base template，所以同一个 alias 是正确用法
        # （多个模板共用才会撞名，SDK 会本地拒绝）。
        # 各自不同 base 时传 callable: lambda sid: f"{sid}-from-{SOURCE_REGION}"
        template_alias=TEMPLATE_ALIAS,
    )
    print(f"    已受理，job_id={job_id}（1 个 job，{len(sandbox_ids)} 个资源）")

    status = target.job.wait(
        job_id,
        timeout=1800,
        poll_interval=10,
        on_progress=lambda s: print(
            f"    进度: {s.completed}/{s.total} done, "
            f"{s.failed} failed, {s.cancelled} cancelled, "
            f"items={len(s.items)}"
        ),
    )

    # wait() 的每次轮询、以及最终返回的 status 都带 items，可以直接逐项归因。
    _print_items(status)

    # 契约没有「部分失败」的聚合规则：completed 一律返回，自己看计数与 items。
    if status.failed or status.cancelled:
        print(f"    注意：job 完成，但有 {status.failed} 失败 / "
              f"{status.cancelled} 取消，需要按业务分流")
        failed_items = [i for i in status.items if i.status == JobStatus.FAILED]
        for item in failed_items[:5]:
            print(f"    失败项: {item.resource_type}/{item.resource_id}")
    else:
        print(f"    全部 {status.total} 个资源迁移完成")
    return status


def step11_per_resource_pattern(target: Novita, sandbox_ids: list) -> list:
    """需要 per-resource job 隔离时的写法：每 id 一个 job。

    0.2.0 的批量 job 已经能通过 ``status.items`` 逐项归因，所以「必须每 id
    一个 job」不再成立。仍然值得用这个模式的场景：要给每个 sandbox 独立的
    取消 / 重试 / 超时预算，或者失败项要单独再受理一次。代价是 N 次请求、
    N 个 job。
    """
    print("\n[11] per-resource job 模式：每 id 一个 job")

    job_ids = []
    for sid in sandbox_ids:
        job_ids.append(
            target.job.migrate_sandbox(
                sid,
                source_region=SOURCE_REGION,
                # 可选；这些 sandbox 若共用同一个 base，
                # 共用 alias 是正常用法；各自 base 不同则按 sid 生成。
                template_alias=TEMPLATE_ALIAS,
            )
        )
    print(f"    受理 {len(job_ids)} 个 job: {job_ids}")

    outcomes = []
    for jid in job_ids:
        try:
            status = target.job.wait(jid, timeout=1800, poll_interval=10)
            outcomes.append((jid, _wire_status(status.status)))
        except JobFailedError as exc:
            outcomes.append((jid, f"failed({exc.status.failed}/{exc.status.total})"))
        except JobCancelledError:
            outcomes.append((jid, "cancelled"))
    for jid, outcome in outcomes:
        print(f"    {jid} -> {outcome}")
    return outcomes


def step12_batch_distribute_templates(target: Novita, template_ids: list) -> MigrationStatus:
    """批量分发模板（非破坏性，源模板照常可用）。"""
    print("\n[12] 批量分发模板")

    job_id = target.job.distribute_templates(
        template_ids,
        source_region=SOURCE_REGION,
        # 一个固定 alias 配 N 个模板必然在目标集群撞名，SDK 在本地就拒绝
        # （InvalidArgumentException），所以模板批量必须传 callable。
        # alias 同时是必填关键字参数：省略会直接 TypeError，平台不会兜底生成。
        template_alias=lambda tid: f"{tid}-from-{SOURCE_REGION}",
    )
    print(f"    已受理，job_id={job_id}")

    status = target.job.wait(job_id, timeout=1800, poll_interval=10)
    _print_status(status)
    return status


# --------------------------------------------------------------------------- #
# 异步版本
# --------------------------------------------------------------------------- #


async def async_migration(conn: dict):
    """facade 的 job 命名空间是**同步**的；异步链路直接用 AsyncJob 类。

    ``target.job.AsyncJob`` 就是 AsyncJob 类本身，但类方法不知道 client 的
    连接配置，所以要显式把连接参数传进去。AsyncJob 与 Job 的签名/语义一一
    对应：sandbox 迁移的 ``template_alias`` 同样选填，items / 回滚语义也一致。
    """
    print("\n[A] 异步版本（client.job.AsyncJob）")

    job_id = await AsyncJob.migrate_sandbox(
        SANDBOX_ID,
        source_region=SOURCE_REGION,
        template_alias=TEMPLATE_ALIAS,
        **conn,
    )
    print(f"    已受理 job_id={job_id}")

    try:
        done = await AsyncJob.wait(job_id, timeout=1800, poll_interval=10, **conn)
        print(f"    完成 status={_wire_status(done.status)} "
              f"({done.completed}/{done.total})")
        _print_items(done, indent="      ")

        page = await AsyncJob.list(
            resource_id=SANDBOX_ID, source_region=SOURCE_REGION, **conn
        )
        print(f"    包含该 sandbox 的 job 共 {len(page.items)} 个")

    except JobFailedError as exc:
        print(f"    失败: {exc.status.failed}/{exc.status.total} 项")
        raise


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #


def main():
    if not API_KEY:
        print("请先设置 NOVITA_API_KEY")
        return
    if not SANDBOX_ID:
        print("请先设置 NOVITA_SANDBOX_ID（源集群上的 sandbox id）")
        return

    source, target = build_clients()
    print(f"source client -> {SOURCE_DOMAIN}")
    print(f"target client -> {TARGET_DOMAIN}")

    # 先看清楚源集群上有什么
    info = step1_inspect_source(source)
    template_id = TEMPLATE_ID or info.template_id

    # 发起迁移并等到成功
    job_id = step2_start_migration(target)
    step3_poll_progress(target, job_id)
    # step3b_wait_shortcut(target, job_id)   # 等价简写

    # 迁移完成后在目标集群验证
    step4_verify_on_target(target)

    # 也可以单独分发模板
    # step5_distribute_template_only(target, template_id)

    # 审计
    step6_audit_history(target)

    # 取消（拿一个还在跑的 job 来演示）
    # step7_cancel(target, "<a-running-job-id>")

    # 错误处理
    step8_error_handling(target)

    # 生产级封装
    print("\n[9] 带退避重试的封装")
    # done = migrate_with_retry(target, SANDBOX_ID, source_region=SOURCE_REGION,
    #                           template_alias=TEMPLATE_ALIAS)
    # print(f"    完成 status={_wire_status(done.status)}")

    # 批量：一次原生请求搬多个 sandbox / 分发多个模板
    # step10_batch_migrate(target, ["sbx-1", "sbx-2", "sbx-3"])
    # step11_per_resource_pattern(target, ["sbx-1", "sbx-2"])
    # step12_batch_distribute_templates(target, ["tpl-1", "tpl-2"])

    if RUN_ASYNC:
        asyncio.run(async_migration({"api_key": API_KEY, "domain": TARGET_DOMAIN}))


if __name__ == "__main__":
    main()
