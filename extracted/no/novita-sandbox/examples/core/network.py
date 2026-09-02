import os

from dotenv import load_dotenv

from novita_sandbox.core import ALL_TRAFFIC, Sandbox

load_dotenv()


def curl(sbx, url, max_time=10):
    return sbx.commands.run(
        f"curl -sS -o /dev/null -w '%{{http_code}}' --max-time {max_time} {url} || true"
    ).stdout.strip() or "blocked"


def step(fn):
    try:
        fn()
    except Exception as e:
        print(f"    Error: {e}")


def main():
    sbx = None
    template = os.getenv("NOVITA_TEMPLATE", "base")

    try:
        print("[1] Creating sandbox")
        sbx = Sandbox.create(template, timeout=300)
        print(f"    sandbox_id={sbx.sandbox_id}")

        def step2():
            print("[2] Allowing egress only to 1.1.1.1 and example.com")
            sbx.set_network(
                allow_out=["1.1.1.1", "example.com"],
                deny_out=[ALL_TRAFFIC],
            )
            print(f"    example.com http_code={curl(sbx, 'https://example.com')}")
            print(f"    1.1.1.1 http_code={curl(sbx, 'https://1.1.1.1')}")

        def step3():
            print("[3] Denying all egress with 0.0.0.0/0")
            sbx.set_network(
                deny_out=[ALL_TRAFFIC],
            )
            print(f"    example.com http_code={curl(sbx, 'https://example.com', max_time=5)}")

        def step4():
            print("[4] Clearing egress rules to restore outbound traffic")
            sbx.set_network()
            print(f"    example.com http_code={curl(sbx, 'https://example.com')}")

        def step5():
            print("[5] Mixed allow/deny: allow 8.8.8.8/32 but deny all others")
            sbx.set_network(
                allow_out=["8.8.8.8/32"],
                deny_out=[ALL_TRAFFIC],
            )
            print(f"    8.8.8.8 http_code={curl(sbx, 'https://8.8.8.8', max_time=5)}")
            print(f"    8.8.4.4 http_code={curl(sbx, 'https://8.8.4.4', max_time=5)}")

        def step6():
            print("[6] CIDR range: allow 1.0.0.0/8 only")
            sbx.set_network(
                allow_out=["1.0.0.0/8"],
                deny_out=[ALL_TRAFFIC],
            )
            print(f"    1.1.1.1 http_code={curl(sbx, 'https://1.1.1.1', max_time=5)}")
            print(f"    8.8.8.8 http_code={curl(sbx, 'https://8.8.8.8', max_time=5)}")

        def step7():
            print("[7] Wildcard domain: allow *.example.com")
            sbx.set_network(
                allow_out=["*.example.com"],
                deny_out=[ALL_TRAFFIC],
            )
            print(f"    example.com http_code={curl(sbx, 'https://example.com', max_time=5)}")
            print(f"    www.example.com http_code={curl(sbx, 'https://www.example.com', max_time=5)}")
            print(f"    1.1.1.1 http_code={curl(sbx, 'https://1.1.1.1', max_time=5)}")

        def step8():
            print("[8] Static method: set_network on sandbox_id without instance")
            Sandbox.set_network(
                sbx.sandbox_id,
                allow_out=["example.com"],
                deny_out=[ALL_TRAFFIC],
            )
            print(f"    example.com http_code={curl(sbx, 'https://example.com', max_time=5)}")

        def step9():
            print("[9] Verify network config via sandbox info")
            info = Sandbox.get_info(sbx.sandbox_id)
            network = info.network or {}
            print(f"    allow_out={network.get('allow_out')}")
            print(f"    deny_out={network.get('deny_out')}")

        def step10():
            print("[10] Empty allow_out list (deny everything)")
            sbx.set_network(
                allow_out=[],
            )
            print(f"    example.com http_code={curl(sbx, 'https://example.com', max_time=5)}")

        for fn in [step2, step3, step4, step5, step6, step7, step8, step9, step10]:
            step(fn)

        print("\n=== All steps completed ===")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sbx:
            print("[cleanup] Killing sandbox")
            sbx.kill()


if __name__ == "__main__":
    main()
