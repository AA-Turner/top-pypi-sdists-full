from dotenv import load_dotenv

from novita_sandbox.core import Template


load_dotenv()


def main():
    try:
        template = (
            Template()
            .from_python_image("3.12")
            .run_cmd("pip help")
            .set_envs({"PYTHONUNBUFFERED": "1"})
            .set_patch_cmd('set -x; echo "provisioning" > /tmp/patch.log')
            .set_start_cmd("python -h", "ls /tmp")
        )

        build_info = Template.build(
            template,
            "my-python-app",
            tags=["v1.0", "latest"],
            cpu_count=2,
            memory_mb=1024,
            on_build_logs=lambda log: print(f"[{log.level}] {log.message}"),
        )

        print(f"Build complete: template={build_info.template_id} build={build_info.build_id}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
