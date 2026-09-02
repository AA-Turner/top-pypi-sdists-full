import asyncio
import os
from time import time

from dotenv import load_dotenv

from novita_sandbox.core import AsyncSandbox, Sandbox
from novita_sandbox.core.secret import AsyncSecret, Secret

load_dotenv()

SECRET_NAME = f"example-openai-{int(time())}"
TEMPLATE = os.getenv("NOVITA_TEMPLATE", "base")


def sync_flow():
    print("=== Sync Secret flow ===\n")

    print(f"[1] Creating secret: {SECRET_NAME}")
    binding = Secret.create(
        name=SECRET_NAME,
        value="sk-example-key",
        hosts=["api.openai.com"],
        description="Example OpenAI key for SDK demo",
    )
    print(f"    name={binding.name}, placeholder={binding.placeholder}")
    print(f"    hosts={binding.hosts}, status={binding.status}")

    print("[2] Listing secrets")
    secrets = Secret.list()
    print(f"    total={len(secrets)}")
    for s in secrets:
        print(f"      name={s.name}, status={s.status}")

    print(f"[3] Getting secret by name: {SECRET_NAME}")
    got = Secret.get(SECRET_NAME)
    print(f"    name={got.name}, has_secret={got.has_secret}")

    print("[4] Updating secret value and hosts")
    updated = Secret.update(
        name=SECRET_NAME,
        value="sk-rotated-key",
        hosts=["api.openai.com", "*.openai.com"],
        description="Rotated key",
    )
    print(f"    name={updated.name}, hosts={updated.hosts}")

    print("[5] Creating sandbox with secret env binding")
    sbx = Sandbox.create(
        TEMPLATE,
        timeout=300,
        secret_envs={"OPENAI_API_KEY": SECRET_NAME},
    )
    print(f"    sandbox_id={sbx.sandbox_id}")

    print("[6] Checking placeholder env var inside sandbox")
    result = sbx.commands.run("echo $OPENAI_API_KEY")
    print(f"    placeholder={result.stdout.strip()}")

    print("[7] Killing sandbox")
    sbx.kill()

    print(f"[8] Deleting secret: {SECRET_NAME}")
    deleted = Secret.delete(SECRET_NAME)
    print(f"    deleted={deleted}")

    print("\n=== Sync flow completed ===")


async def async_flow():
    print("\n=== Async Secret flow ===\n")

    name = f"example-anthropic-{int(time())}"

    print(f"[1] Creating secret: {name}")
    binding = await AsyncSecret.create(
        name=name,
        value="sk-ant-example",
        hosts=["api.anthropic.com"],
    )
    print(f"    name={binding.name}, placeholder={binding.placeholder}")

    print(f"[2] Getting secret by name: {name}")
    got = await AsyncSecret.get(name)
    print(f"    name={got.name}, status={got.status}")

    print("[3] Listing secrets")
    secrets = await AsyncSecret.list()
    print(f"    total={len(secrets)}")

    print("[4] Creating sandbox with secret env binding")
    sbx = await AsyncSandbox.create(
        TEMPLATE,
        timeout=300,
        secret_envs={"ANTHROPIC_API_KEY": name},
    )
    print(f"    sandbox_id={sbx.sandbox_id}")

    print("[5] Checking placeholder env var inside sandbox")
    result = await sbx.commands.run("echo $ANTHROPIC_API_KEY")
    print(f"    placeholder={result.stdout.strip()}")

    print("[6] Killing sandbox")
    await sbx.kill()

    print(f"[7] Deleting secret: {name}")
    deleted = await AsyncSecret.delete(name)
    print(f"    deleted={deleted}")

    print("\n=== Async flow completed ===")


def main():
    try:
        sync_flow()
        asyncio.run(async_flow())
    except Exception as e:
        print(f"Error: {e}")
        # Best-effort cleanup
        try:
            Secret.delete(SECRET_NAME)
        except Exception:
            pass


if __name__ == "__main__":
    main()
