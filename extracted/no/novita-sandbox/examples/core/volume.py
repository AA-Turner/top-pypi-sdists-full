import os
from time import time

from dotenv import load_dotenv

from novita_sandbox.core import Sandbox, Volume

load_dotenv()


def main():
    sbx = None
    vol = None
    template = os.getenv("NOVITA_TEMPLATE", "base")

    try:
        volume_name = f"example-vol-{int(time())}"

        print(f"[1] Creating volume: {volume_name}")
        vol = Volume.create(volume_name, quota_size_gib=1, quota_inodes=1000)
        print(f"    volume_id={vol.volume_id}, name={vol.name}")

        print("[2] Creating sandbox")
        sbx = Sandbox.create(template, timeout=300)
        print(f"    sandbox_id={sbx.sandbox_id}")

        print("[3] Mounting volume at /mnt/vol")
        sbx.mount_volume(vol.name, "/mnt/vol")

        print("[4] Writing file on mounted volume")
        result = sbx.commands.run('echo "hello volume world" > /mnt/vol/hello.txt')
        print(f"    exit_code={result.exit_code}")

        print("[5] Reading file on mounted volume")
        result = sbx.commands.run("cat /mnt/vol/hello.txt")
        print(f"    content: {result.stdout.strip()}")

        print("[6] Listing mounted volume contents")
        result = sbx.commands.run("ls -la /mnt/vol/")
        print(f"    {repr(result.stdout.strip())}")

        print("\n=== All steps completed ===")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sbx:
            try:
                print("[cleanup] Unmounting volume")
                sbx.unmount_volume("/mnt/vol", force=True)
            finally:
                print("[cleanup] Killing sandbox")
                sbx.kill()

        if vol:
            print("[cleanup] Destroying volume")
            destroyed = Volume.destroy(vol.volume_id)
            print(f"    destroyed={destroyed}")


if __name__ == "__main__":
    main()
