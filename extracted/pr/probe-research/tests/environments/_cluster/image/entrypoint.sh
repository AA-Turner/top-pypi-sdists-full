#!/bin/bash
# Role entrypoint for the cluster environment test image. ROLE picks what this
# container is; everything a test needs afterwards it runs with `docker exec`.
set -euo pipefail

log() { echo "[entrypoint:${ROLE}] $*"; }

mount_home() {
    # The researcher's home: the NFS export when NFS_SERVER is set (every cluster
    # node mounts the same one, like an LDAP site's /home), else a local directory.
    if [ -n "${NFS_SERVER:-}" ]; then
        local opts="vers=${NFS_VERS:-4.2}${NFS_OPTS:+,${NFS_OPTS}}"
        for _ in $(seq 1 60); do
            if mount -t nfs4 -o "$opts" "${NFS_SERVER}:/" /home 2>/tmp/mount.err; then
                log "mounted ${NFS_SERVER}:/ on /home ($opts)"
                return 0
            fi
            sleep 1
        done
        log "NFS mount failed: $(cat /tmp/mount.err)"
        exit 1
    fi
    mkdir -p /home/researcher
    chown researcher:researcher /home/researcher
    chmod 700 /home/researcher
}

start_munge() {
    runuser -u munge -- /usr/sbin/munged --force
}

case "${ROLE:-node}" in
nfs)
    # Kernel nfsd inside this container's network namespace. Needs the host's
    # `nfsd` module loaded and --privileged. /export must be a real filesystem (a
    # docker volume), not the overlay root: overlayfs does not export over NFS.
    mkdir -p /export/researcher
    chown researcher:researcher /export/researcher
    chmod 700 /export/researcher
    echo "/export *(rw,sync,no_subtree_check,fsid=0,crossmnt${NFS_EXPORT_OPTS:+,${NFS_EXPORT_OPTS}})" > /etc/exports
    mountpoint -q /proc/fs/nfsd || mount -t nfsd nfsd /proc/fs/nfsd
    rpcbind -w || true
    exportfs -ra
    # A short grace and lease so a test does not wait 90 s for NFSv4 recovery
    # after the server starts; real servers default to 90 s for both.
    rpc.nfsd --grace-time "${NFS_GRACE:-10}" --lease-time "${NFS_LEASE:-15}" -N 3 -V 4 8
    log "nfsd up: $(cat /proc/fs/nfsd/versions)"
    exec rpc.mountd -F -N 2 -N 3
    ;;
slurmctl)
    mount_home
    start_munge
    exec slurmctld -D -f /etc/slurm/slurm.conf
    ;;
slurmd)
    mount_home
    start_munge
    exec slurmd -D -f /etc/slurm/slurm.conf -N "$(hostname)"
    ;;
node)
    mount_home
    exec sleep infinity
    ;;
squid)
    mkdir -p /var/log/squid && chown proxy:proxy /var/log/squid
    exec squid -N -f /etc/squid/envtest.conf
    ;;
relay)
    exec python /usr/local/bin/relay.py
    ;;
*)
    log "unknown ROLE"
    exit 2
    ;;
esac
