import os
import tempfile
from unittest import mock

import pytest
from opentelemetry.sdk.resources import Resource

from opentelemetry_resourcedetector_kubernetes import (
    Attributes,
    KubernetesResourceDetector,
)


@pytest.fixture(scope='module')
def pod_uid():
    return 'abcdef01-2345-6789-abcd-ef0123456789'


@pytest.fixture(scope='module')
def container_id():
    return 'abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789'


@pytest.fixture(scope='module')
def kubernetes_cgroups(pod_uid, container_id):
    with tempfile.NamedTemporaryFile() as cgroup_file:
        # observed on a k3s cluster running v1.23.5+k3s1
        cgroup_lines = [
            f'12:blkio:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'11:perf_event:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'10:devices:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'9:pids:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'8:cpuset:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'7:freezer:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'6:net_cls,net_prio:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'5:memory:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'4:cpu,cpuacct:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            f'3:hugetlb:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            '2:rdma:/',
            f'1:name=systemd:/kubepods/besteffort/pod{pod_uid}/{container_id}',
            '0::/system.slice/k3s-agent.service',
        ]
        filename = cgroup_file.name
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cgroup_lines))
        with mock.patch.object(KubernetesResourceDetector, 'cgroup_file', filename):
            yield


@pytest.fixture
def non_kubernetes_cgroups():
    with tempfile.NamedTemporaryFile() as cgroup_file:
        # observed on an Ubuntu laptop, with some tweaks for brevity
        cgroup_lines = [
            '12:memory:/user.slice/user-1000.slice/user@1000.service'
            '11:blkio:/user.slice'
            '10:perf_event:/'
            '9:cpuset:/'
            '8:hugetlb:/'
            '7:freezer:/'
            '6:cpu,cpuacct:/user.slice'
            '5:devices:/user.slice'
            '4:rdma:/'
            '3:pids:/user.slice/user-1000.slice/user@1000.service'
            '2:net_cls,net_prio:/'
            '1:name=systemd:/user.slice/user-1000.slice/user@1000.service/blah-blah'
            '0::/user.slice/user-1000.slice/user@1000.service/apps.slice/blah-blah'
        ]
        filename = cgroup_file.name
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cgroup_lines))
        with mock.patch.object(KubernetesResourceDetector, 'cgroup_file', filename):
            yield


@pytest.fixture
def no_cgroup():
    missing = '/no/cgroup/for/you'
    assert not os.path.exists(missing)
    with mock.patch.object(KubernetesResourceDetector, 'cgroup_file', missing):
        yield


@pytest.fixture(scope='module')
def attributes(resource: Resource) -> Attributes:
    return dict(resource.attributes)
