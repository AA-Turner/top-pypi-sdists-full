from novita_sandbox.core import Template

build_logs = []


def on_logs(entry):
    line = f"[{getattr(entry, 'level', '?')}] {getattr(entry, 'message', '')}"
    build_logs.append(line)
    print("BUILDLOG:", line, flush=True)


# Commands to run on the base image BEFORE systemd is installed/set up.
# - seed /etc/skel
# - write a placeholder /etc/fstab
# - mask cloud-init via systemd unit -> /dev/null symlinks (take effect once
#   systemd is installed later in provisioning)
PRE_SYSTEMD_SCRIPT = r"""
set -eu
echo NOVITA_PRESYSTEMD_CLOUDINIT_START
mkdir -p /etc/systemd/system
install -d -m 0755 /etc/skel \
 && install -m 0644 /usr/share/base-files/dot.bashrc  /etc/skel/.bashrc \
 && install -m 0644 /usr/share/base-files/dot.profile /etc/skel/.profile \
 && printf '# ~/.bash_logout\n' > /etc/skel/.bash_logout \
 && echo '# UNCONFIGURED FSTAB FOR BASE SYSTEM' > /etc/fstab \
 && ln -sf /dev/null /etc/systemd/system/cloud-init.service \
 && ln -sf /dev/null /etc/systemd/system/cloud-init-local.service \
 && ln -sf /dev/null /etc/systemd/system/cloud-config.service \
 && ln -sf /dev/null /etc/systemd/system/cloud-final.service \
 && ln -sf /dev/null /etc/systemd/system/cloud-init.target
echo NOVITA_PRESYSTEMD_CLOUDINIT_DONE
"""

template = (
    Template()
    .from_image("ghcr.io/catthehacker/ubuntu:full-24.04")
    .set_patch_cmd(PRE_SYSTEMD_SCRIPT)
    .run_cmd("echo step-phase-ran")
)

info = Template.build(
    template,
    "patch-image-test",
    cpu_count=1,
    memory_mb=512,
    skip_cache=True,
    on_build_logs=on_logs,
)

print(f"template_id={info.template_id} build_id={info.build_id}", flush=True)
