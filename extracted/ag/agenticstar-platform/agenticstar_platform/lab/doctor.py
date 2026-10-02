"""lab の read-only 診断（molt#1610）。

    python -m agenticstar_platform.lab doctor

Docker / compose / python extras / port / service readiness / seed version を
actionable な reason と次の 1 コマンド付きで分類する。**一切の書き込み・起動・
状態変更を行わない**（container 起動や seed 適用は run_lab の仕事）。

exit code: 0 = すべて OK / 1 = いずれかの check が NG。
"""

from __future__ import annotations

import asyncio
import sys

from . import checks


def main() -> None:
    results = []

    # Docker / compose
    results.append(checks.check_docker_cli())
    docker_ok = results[-1].ok
    if docker_ok:
        results.append(checks.check_docker_daemon())
        docker_ok = results[-1].ok
        if docker_ok:
            results.append(checks.check_compose())
            docker_ok = results[-1].ok

    # Python extras
    extras = checks.check_extras()
    results.extend(extras)
    extras_ok = all(r.ok for r in extras)

    # artifact 出力先（cwd 配下）の使用可否
    results.append(checks.check_artifacts_path())

    # service 状態（docker が使えるときだけ意味がある）
    services_ok = False
    if docker_ok:
        ps = checks.compose_ps()
        pg_ready = asyncio.run(checks.probe_postgres()) if extras_ok else False
        service_results = checks.service_checks(ps, pg_ready)
        results.extend(service_results)
        services_ok = all(r.ok for r in service_results)

    # seed（PG が ready のときだけ検査できる）
    if extras_ok and services_ok:
        results.append(asyncio.run(checks.seed_status()))

    print("agenticstar lab doctor (read-only)\n")
    for r in results:
        print(r.render())

    if all(r.ok for r in results):
        print("\n✅ all checks passed — python -m agenticstar_platform.lab で journey を実行できます")
        sys.exit(0)
    print("\n❌ NG があります。各行の next を実行してから再度 doctor を実行してください")
    sys.exit(1)


if __name__ == "__main__":
    main()
