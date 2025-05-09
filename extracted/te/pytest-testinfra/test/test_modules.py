# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
import re
import tempfile
import textwrap
import time
from ipaddress import IPv4Address, IPv6Address, ip_address

import pytest

from testinfra.modules.socket import parse_socketspec
from testinfra.utils.ansible_runner import AnsibleRunner

all_images = pytest.mark.testinfra_hosts(
    *[
        f"docker://{image}"
        for image in (
            "rockylinux9",
            "debian_bookworm",
        )
    ]
)


@all_images
def test_package(host, docker_image):
    assert not host.package("zsh").is_installed
    ssh = host.package("openssh-server")
    version = {
        "rockylinux9": "8.",
        "debian_bookworm": "1:9.2",
    }[docker_image]
    assert ssh.is_installed
    assert ssh.version.startswith(version)
    release = {
        "rockylinux9": ".el9",
        "debian_bookworm": None,
    }[docker_image]
    if release is None:
        with pytest.raises(NotImplementedError):
            ssh.release  # noqa: B018
    else:
        assert release in ssh.release


def test_held_package(host):
    python = host.package("python3")
    assert python.is_installed
    assert python.version.startswith("3.11.")


@pytest.mark.destructive
@pytest.mark.testinfra_hosts("docker://rockylinux9")
def test_rpmdb_corrupted(host):
    host.check_output("dd if=/dev/zero of=/var/lib/rpm/rpmdb.sqlite bs=1024 count=1")
    with pytest.raises(RuntimeError) as excinfo:
        host.package("zsh").is_installed  # noqa: B018
    assert (
        "Could not check if RPM package 'zsh' is installed. error: sqlite failure:"
    ) in str(excinfo.value)


@pytest.mark.testinfra_hosts("docker://rockylinux9")
def test_non_default_package_tool(host):
    # Make non default pkg tool binary present
    host.run("install -m a+rx /bin/true /usr/bin/dpkg-query")
    assert host.package("openssh").is_installed


@pytest.mark.destructive
def test_uninstalled_package_version(host):
    with pytest.raises(AssertionError) as excinfo:
        host.package("zsh").version  # noqa: B018
    assert (
        "The package zsh is not installed, dpkg-query output: unknown ok not-installed"
        in str(excinfo.value)
    )
    assert host.package("sudo").is_installed
    host.check_output("apt-get -y remove sudo")
    assert not host.package("sudo").is_installed
    with pytest.raises(AssertionError) as excinfo:
        host.package("sudo").version  # noqa: B018
    assert (
        "The package sudo is not installed, dpkg-query output: "
        "deinstall ok config-files 1.9."
    ) in str(excinfo.value)


@all_images
def test_systeminfo(host, docker_image):
    assert host.system_info.type == "linux"

    release, distribution, codename, arch = {
        "rockylinux9": (r"^9.\d+$", "rocky", None, "x86_64"),
        "debian_bookworm": (r"^12", "debian", "bookworm", "x86_64"),
    }[docker_image]

    assert host.system_info.distribution == distribution
    assert host.system_info.codename == codename
    assert re.match(release, host.system_info.release)


@all_images
def test_ssh_service(host, docker_image):
    name = "sshd" if docker_image == "rockylinux9" else "ssh"
    ssh = host.service(name)
    # wait at max 10 seconds for ssh is running
    for _ in range(10):
        if ssh.is_running:
            break
        time.sleep(1)
    else:
        raise AssertionError("ssh is not running")

    assert ssh.is_enabled


def test_service_systemd_mask(host):
    ssh = host.service("ssh")
    assert not ssh.is_masked
    host.run("systemctl mask ssh")
    assert ssh.is_masked
    host.run("systemctl unmask ssh")
    assert not ssh.is_masked


def test_salt(host):
    ssh_version = host.salt("pkg.version", "openssh-server", local=True)
    assert ssh_version.startswith("1:9.2")


def test_puppet_resource(host):
    resource = host.puppet_resource("package", "openssh-server")
    assert resource["openssh-server"]["ensure"].startswith("1:9.2")


def test_facter(host):
    assert host.facter()["os"]["distro"]["codename"] == "bookworm"
    assert host.facter("virtual") in (
        {"virtual": "docker"},
        {"virtual": "hyperv"},  # github action uses hyperv
        {"virtual": "physical"},  # I've this on my machine...
    )


def test_sysctl(host):
    assert host.sysctl("kernel.hostname") == host.check_output("hostname")
    assert isinstance(host.sysctl("kernel.panic"), int)


def test_parse_socketspec():
    assert parse_socketspec("tcp://22") == ("tcp", None, 22)
    assert parse_socketspec("tcp://:::22") == ("tcp", "::", 22)
    assert parse_socketspec("udp://0.0.0.0:22") == ("udp", "0.0.0.0", 22)
    assert parse_socketspec("unix://can:be.any/thing:22") == (
        "unix",
        "can:be.any/thing:22",
        None,
    )


def test_socket(host):
    listening = host.socket.get_listening_sockets()
    for spec in (
        "tcp://0.0.0.0:22",
        "tcp://:::22",
        "unix:///run/systemd/private",
    ):
        assert spec in listening
    for spec in (
        "tcp://22",
        "tcp://0.0.0.0:22",
        "tcp://127.0.0.1:22",
        "tcp://:::22",
        "tcp://::1:22",
        "unix:///run/systemd/private",
    ):
        socket = host.socket(spec)
        assert socket.is_listening

    assert not host.socket("tcp://4242").is_listening

    if host.backend.get_connection_type() != "docker":
        # FIXME
        for spec in (
            "tcp://22",
            "tcp://0.0.0.0:22",
        ):
            assert len(host.socket(spec).clients) >= 1


@all_images
def test_process(host, docker_image):
    init = host.process.get(pid=1)
    assert init.ppid == 0
    assert init.euid == 0
    assert init.user == "root"

    args, comm = {
        "rockylinux9": ("/usr/sbin/init", "systemd"),
        "debian_bookworm": ("/sbin/init", "systemd"),
    }[docker_image]
    assert init.args == args
    assert init.comm == comm


def test_user(host):
    user = host.user("sshd")
    assert user.exists
    assert user.name == "sshd"
    assert user.uid == 100
    assert user.gid == 65534
    assert user.group == "nogroup"
    assert user.gids == [65534]
    assert user.groups == ["nogroup"]
    assert user.shell == "/usr/sbin/nologin"
    assert user.home == "/run/sshd"
    assert user.password == "!"


def test_user_get_all_users(host):
    user_list = host.user("root").get_all_users
    assert "root" in user_list
    assert "man" in user_list
    assert "nobody" in user_list


def test_user_password_days(host):
    assert host.user("root").password_max_days == 99999
    assert host.user("root").password_min_days == 0
    assert host.user("user").password_max_days == 90
    assert host.user("user").password_min_days == 7


def test_user_user(host):
    user = host.user("user")
    assert user.exists
    assert user.gecos == "gecos.comment"


def test_user_expiration_date(host):
    assert host.user("root").expiration_date is None
    assert host.user("user").expiration_date == datetime.datetime(2030, 1, 1)


def test_nonexistent_user(host):
    assert not host.user("zzzzzzzzzz").exists


def test_current_user(host):
    assert host.user().name == "root"
    pw = host.user().password
    assert pw.startswith("$")
    assert len(pw) == 73


def test_group(host):
    assert host.group("root").exists
    assert host.group("root").gid == 0
    group_list = host.group("root").get_all_groups
    assert "root" in group_list
    assert "bin" in group_list
    group_list = host.group("root").get_local_groups
    assert "root" in group_list
    assert "bin" in group_list


def test_empty_command_output(host):
    assert host.check_output("printf ''") == ""


def test_local_command(host):
    assert host.get_host("local://").check_output("true") == ""


def test_file(host):
    host.check_output("mkdir -p /d && printf foo > /d/f && chmod 600 /d/f")
    host.check_output('touch "/d/f\nl"')
    host.check_output('touch "/d/f s"')
    d = host.file("/d")
    assert d.is_directory
    assert not d.is_file
    assert d.listdir() == ["f", "f?l", "f s"]
    f = host.file("/d/f")
    assert f.exists
    assert f.is_file
    assert f.content == b"foo"
    assert f.content_string == "foo"
    assert f.user == "root"
    assert f.uid == 0
    assert f.gid == 0
    assert f.group == "root"
    assert f.mode == 0o600
    assert f.contains("fo")
    assert not f.is_directory
    assert not f.is_symlink
    assert not f.is_pipe
    assert f.linked_to == "/d/f"
    assert f.size == 3
    assert f.md5sum == "acbd18db4cc2f85cedef654fccc4a4d8"
    assert f.sha256sum == (
        "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
    )
    host.check_output("ln -fsn /d/f /d/l")
    link = host.file("/d/l")
    assert link.is_symlink
    assert link.is_file
    assert link.linked_to == "/d/f"
    assert link.linked_to == f
    assert f == host.file("/d/f")
    assert d != f

    host.check_output("ln /d/f /d/h")
    hardlink = host.file("/d/h")
    assert hardlink.is_file
    assert not hardlink.is_symlink
    assert isinstance(hardlink.inode, int)
    assert isinstance(f.inode, int)
    assert hardlink.inode == f.inode
    assert f == host.file("/d/f")
    assert d != f

    host.check_output("rm -f /d/p && mkfifo /d/p")
    assert host.file("/d/p").is_pipe

    host.check_output("chmod 700 /d/f")
    assert f.is_executable
    assert f.mode == 0o700


def test_ansible_unavailable(host):
    expected = "Ansible module is only available with ansible connection backend"
    with pytest.raises(RuntimeError) as excinfo:
        host.ansible("setup")
    assert expected in str(excinfo.value)
    with pytest.raises(RuntimeError) as excinfo:
        host.ansible.get_variables()
    assert expected in str(excinfo.value)


@pytest.mark.testinfra_hosts("ansible://debian_bookworm")
def test_ansible_module(host):
    setup = host.ansible("setup")["ansible_facts"]
    assert setup["ansible_lsb"]["codename"] == "bookworm"
    passwd = host.ansible("file", "path=/etc/passwd state=file")
    assert passwd["changed"] is False
    assert passwd["gid"] == 0
    assert passwd["group"] == "root"
    assert passwd["mode"] == "0644"
    assert passwd["owner"] == "root"
    assert isinstance(passwd["size"], int)
    assert passwd["path"] == "/etc/passwd"
    # seems to vary with different docker fs backend
    assert passwd["state"] in ("file", "hard")
    assert passwd["uid"] == 0

    with pytest.raises(host.ansible.AnsibleException) as excinfo:
        host.ansible("command", "zzz")
    assert excinfo.value.result["msg"] == "Skipped. You might want to try check=False"

    try:
        host.ansible("command", "zzz", check=False)
    except host.ansible.AnsibleException as exc:
        assert exc.result["rc"] == 2
        # notez que the debian bookworm container is set to LANG=fr_FR
        assert exc.result["msg"] == ("[Errno 2] Aucun fichier ou dossier de ce type")

    result = host.ansible("command", "echo foo", check=False)
    assert result["stdout"] == "foo"


@pytest.mark.testinfra_hosts("ansible://debian_bookworm")
def test_ansible_get_variables_flat_wo_child_groups(host):
    """Test AnsibleRunner.get_variables() with parent groups only"""
    variables = host.ansible.get_variables()
    assert variables["myvar"] == "foo"
    assert variables["myhostvar"] == "bar"
    assert variables["mygroupvar"] == "qux"
    assert variables["inventory_hostname"] == "debian_bookworm"
    assert variables["group_names"] == ["all", "testgroup"]
    assert variables["groups"] == {
        "all": ["debian_bookworm"],
        "testgroup": ["debian_bookworm"],
    }


def test_ansible_get_variables_w_child_groups():
    """Test AnsibleRunner.get_variables() with parent and child groups"""
    inventory = """
        host_a
        [toplevel1]
        host_b
        [toplevel2]
        host_c
        [toplevel3:children]
        toplevel1
        """
    with tempfile.NamedTemporaryFile(mode="wt", encoding="ascii") as file_inventory:
        file_inventory.write(textwrap.dedent(inventory.strip()))
        file_inventory.flush()

        get_variables = AnsibleRunner(file_inventory.name).get_variables

        assert get_variables("host_a")["group_names"] == ["all", "ungrouped"]
        assert get_variables("host_b")["group_names"] == [
            "all",
            "toplevel1",
            "toplevel3",
        ]
        assert get_variables("host_c")["group_names"] == ["all", "toplevel2"]


@pytest.mark.testinfra_hosts(
    "ansible://debian_bookworm", "ansible://user@debian_bookworm"
)
def test_ansible_module_become(host):
    user_name = host.user().name
    assert host.ansible("shell", "echo $USER", check=False)["stdout"] == user_name
    assert (
        host.ansible("shell", "echo $USER", check=False, become=True)["stdout"]
        == "root"
    )

    with host.sudo():
        assert host.user().name == "root"
        assert host.ansible("shell", "echo $USER", check=False)["stdout"] == user_name
        assert (
            host.ansible("shell", "echo $USER", check=False, become=True)["stdout"]
            == "root"
        )


@pytest.mark.testinfra_hosts("ansible://debian_bookworm")
def test_ansible_module_options(host):
    assert (
        host.ansible(
            "command",
            "id --user --name",
            check=False,
            become=True,
            become_user="nobody",
        )["stdout"]
        == "nobody"
    )


@pytest.mark.destructive
@pytest.mark.parametrize(
    "supervisorctl_path,supervisorctl_conf",
    [
        ("supervisorctl", None),
        ("/usr/bin/supervisorctl", "/etc/supervisor/supervisord.conf"),
    ],
)
def test_supervisor(host, supervisorctl_path, supervisorctl_conf):
    # Wait supervisord is running
    for _ in range(20):
        if host.service("supervisor").is_running:
            break
        time.sleep(0.5)
    else:
        raise RuntimeError("No running supervisor")

    for _ in range(20):
        service = host.supervisor(
            "tail",
            supervisorctl_path=supervisorctl_path,
            supervisorctl_conf=supervisorctl_conf,
        )
        if service.status == "RUNNING":
            break
        assert service.status == "STARTING"
        time.sleep(0.5)
    else:
        raise RuntimeError("No running tail in supervisor")

    assert service.is_running
    proc = host.process.get(pid=service.pid)
    assert proc.comm == "tail"

    services = host.supervisor.get_services(supervisorctl_path, supervisorctl_conf)
    assert len(services) == 1
    assert services[0].name == "tail"
    assert services[0].is_running
    assert services[0].pid == service.pid
    # Checking if conf is propagated
    assert services[0].supervisorctl_path == supervisorctl_path
    assert services[0].supervisorctl_conf == supervisorctl_conf

    host.check_output("supervisorctl stop tail")
    service = host.supervisor(
        "tail",
        supervisorctl_path=supervisorctl_path,
        supervisorctl_conf=supervisorctl_conf,
    )
    assert not service.is_running
    assert service.status == "STOPPED"
    assert service.pid is None

    host.run("service supervisor stop")
    assert not host.service("supervisor").is_running
    with pytest.raises(RuntimeError) as excinfo:
        host.supervisor(  # noqa: B018
            "tail",
            supervisorctl_path=supervisorctl_path,
            supervisorctl_conf=supervisorctl_conf,
        ).is_running
    assert "Is supervisor running" in str(excinfo.value)


def test_mountpoint(host):
    root_mount = host.mount_point("/")
    assert root_mount.exists
    assert repr(root_mount)
    assert isinstance(root_mount.options, list)
    assert "rw" in root_mount.options
    assert root_mount.filesystem

    fake_mount = host.mount_point("/fake/mount")
    assert not fake_mount.exists
    assert repr(fake_mount)

    mountpoints = host.mount_point.get_mountpoints()
    assert mountpoints
    assert all(isinstance(m, host.mount_point) for m in mountpoints)
    assert len([m for m in mountpoints if m.path == "/"]) == 1


def test_sudo_from_root(host):
    assert host.user().name == "root"
    with host.sudo("user"):
        assert host.user().name == "user"
    assert host.user().name == "root"


def test_sudo_fail_from_root(host):
    assert host.user().name == "root"
    with host.sudo("unprivileged"):
        assert host.user().name == "unprivileged"
        with pytest.raises(AssertionError) as exc:
            host.check_output("ls /root/invalid")
    assert str(exc.value).startswith("Unexpected exit code")
    with host.sudo():
        assert host.user().name == "root"


@pytest.mark.testinfra_hosts("docker://user@debian_bookworm")
def test_sudo_to_root(host):
    assert host.user().name == "user"
    with host.sudo():
        assert host.user().name == "root"
        # Test nested sudo
        with host.sudo("www-data"):
            assert host.user().name == "www-data"
    assert host.user().name == "user"


def test_command_execution(host):
    assert host.run("false").failed
    assert host.run("true").succeeded


def test_pip(host):
    # get_packages
    assert host.pip.get_packages()["pip"]["version"].startswith("23.")
    pkg = host.pip.get_packages(pip_path="/v/bin/pip")["requests"]
    assert pkg["version"] == "2.30.0"
    # outdated
    outdated = host.pip.get_outdated_packages(pip_path="/v/bin/pip")["requests"]
    assert outdated["current"] == pkg["version"]
    # check
    assert host.pip.check().succeeded
    # is_installed
    assert host.pip("pip").is_installed
    assert not host.pip("does_not_exist").is_installed
    pkg = host.pip("requests", pip_path="/v/bin/pip")
    assert pkg.is_installed
    # version
    assert host.pip("pip").version.startswith("23.")
    assert pkg.version == "2.30.0"
    assert host.pip("does_not_exist").version == ""


def test_environment_home(host):
    assert host.environment().get("HOME") == "/root"


@pytest.mark.skipif(
    "WSL_DISTRO_NAME" in os.environ, reason="Skip on WSL (Windows Subsystem for Linux)"
)
def test_iptables(host):
    cmd = host.run("systemctl start netfilter-persistent")
    assert cmd.exit_status == 0, f"{cmd.stdout}\n{cmd.stderr}"
    ssh_rule_str = "-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT"
    vip_redirect_rule_str = "-A PREROUTING -d 192.168.0.1/32 -j REDIRECT"
    rules = host.iptables.rules()
    input_rules = host.iptables.rules("filter", "INPUT")
    nat_rules = host.iptables.rules("nat")
    nat_prerouting_rules = host.iptables.rules("nat", "PREROUTING")
    assert ssh_rule_str in rules
    assert ssh_rule_str in input_rules
    assert vip_redirect_rule_str in nat_rules
    assert vip_redirect_rule_str in nat_prerouting_rules
    assert host.iptables._has_w_argument is True


def test_ip6tables(host):
    # test ip6tables call works; ipv6 setup is a whole huge thing, but
    # ensure we at least see the headings
    try:
        v6_rules = host.iptables.rules(version=6)
    except AssertionError as exc_info:
        if "Perhaps ip6tables or your kernel needs to be upgraded" in exc_info.args[0]:
            pytest.skip(
                f"IPV6 does not seem to be enabled on the docker host\n{exc_info}"
            )
        else:
            raise
    else:
        assert "-P INPUT ACCEPT" in v6_rules
        assert "-P FORWARD ACCEPT" in v6_rules
        assert "-P OUTPUT ACCEPT" in v6_rules
        v6_filter_rules = host.iptables.rules("filter", "INPUT", version=6)
        assert "-P INPUT ACCEPT" in v6_filter_rules


@all_images
def test_addr(host):
    non_resolvable = host.addr("some_non_resolvable_host")
    assert not non_resolvable.is_resolvable
    assert not non_resolvable.is_reachable
    assert not non_resolvable.port(80).is_reachable

    # Some arbitrary internal IP, hopefully non reachable
    # IP addresses are always resolvable no matter what
    non_reachable_ip = host.addr("10.42.13.73")
    assert non_reachable_ip.is_resolvable
    assert non_reachable_ip.ipv4_addresses == ["10.42.13.73"]
    assert not non_reachable_ip.is_reachable
    assert not non_reachable_ip.port(80).is_reachable

    google_dns = host.addr("8.8.8.8")
    assert google_dns.is_resolvable
    assert google_dns.ipv4_addresses == ["8.8.8.8"]
    assert google_dns.port(53).is_reachable
    assert not google_dns.port(666).is_reachable

    google_addr = host.addr("google.com")
    assert google_addr.is_resolvable
    assert google_addr.port(443).is_reachable
    assert not google_addr.port(666).is_reachable

    for ip in google_addr.ipv4_addresses:
        assert isinstance(ip_address(ip), IPv4Address)

    for ip in google_addr.ipv6_addresses:
        assert isinstance(ip_address(ip), IPv6Address)

    for ip in google_addr.ip_addresses:
        assert isinstance(ip_address(ip), (IPv4Address, IPv6Address))


@pytest.mark.testinfra_hosts("ansible://debian_bookworm")
def test_addr_namespace(host):
    namespace_lookup = host.addr("localhost", "ns1")
    assert not namespace_lookup.namespace_exists


@pytest.mark.parametrize(
    "family",
    ["inet", None],
)
def test_interface(host, family):
    # exist
    assert host.interface("eth0", family=family).exists
    assert not host.interface("does_not_exist", family=family).exists
    # addresses
    addresses = host.interface.default(family).addresses
    assert len(addresses) > 0
    for add in addresses:
        try:
            ip_address(add)
        except ValueError:
            pytest.fail(f"{add} is not a valid IP address")
    # names and default
    assert "eth0" in host.interface.names()
    default_itf = host.interface.default(family)
    assert default_itf.name == "eth0"
    assert default_itf.exists
