#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from textwrap import dedent

from snowflake.core.service import Service, ServiceSpecInlineText

from ..utils import random_string


def test_stop_all_services(compute_pools, services, imagerepo, temp_cp):
    compute_pools[temp_cp.name].resume()

    s_name = random_string(5, "test_service_")
    inline_spec = dedent(
        f"""
            spec:
              containers:
              - name: hello-world
                image: {imagerepo}/hello-world:latest
             """
    )
    test_s = Service(
        name=s_name,
        compute_pool=temp_cp.name,
        spec=ServiceSpecInlineText(spec_text=inline_spec),
        min_instances=1,
        max_instances=1,
    )
    services.create(test_s)

    services_in_pool = [service for service in services.iter() if service.compute_pool == temp_cp.name.upper()]
    assert len(services_in_pool) == 1
    assert services_in_pool[0].name == test_s.name.upper()
    compute_pools[temp_cp.name].stop_all_services()
    services_in_pool = [service for service in services.iter() if service.compute_pool == temp_cp.name.upper()]
    assert len(services_in_pool) == 0
