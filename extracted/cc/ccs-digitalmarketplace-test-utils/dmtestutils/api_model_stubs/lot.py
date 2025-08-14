from .base import BaseAPIModelStub


class LotStub(BaseAPIModelStub):
    default_data = {
        "id": 1,
        "slug": "some-lot",
        "name": "Some lot",
        "number": "1",
        "allowsBrief": False,
        "oneServiceLimit": False,
        "unitSingular": "service",
        "unitPlural": "services",
    }

    optional_keys = [
        ("allowsBrief", "allows_brief"),
        ("oneServiceLimit", "one_service_limit"),
        ("unitSingular", "unit_singular"),
        ("unitPlural", "unit_plural"),
        ("id", "lot_id"),
    ]


def dos_lots(with_evaluation=False):
    lots = [
        LotStub(
            lot_id=5,
            slug="digital-outcomes",
            name="Digital Outcomes",
            number="1",
            allows_brief=True,
            one_service_limit=True,
        ).response(),
        LotStub(
            lot_id=7,
            slug="user-research-studios",
            name="User research studios",
            number="2",
            unit_singular="lab",
            unit_plural="labs",
        ).response(),
        LotStub(
            lot_id=8,
            slug="user-research-participants",
            name="User research participants",
            number="3",
            allows_brief=True,
            one_service_limit=True,
        ).response(),
    ]

    if with_evaluation:
        lots.append(
            LotStub(
                lot_id=9,
                slug="digital-capability-and-delivery-partner",
                name="Digital Capability and Delivery Partners",
                number="4",
            ).response()
        )

    return lots


def as_a_service_lots():
    return [
        LotStub(lot_id=1, slug="saas", name="Software as a Service", number="1").response(),
        LotStub(lot_id=2, slug="paas", name="Platform as a Service", number="2").response(),
        LotStub(lot_id=3, slug="iaas", name="Infrastructure as a Service", number="3").response(),
        LotStub(lot_id=4, slug="scs", name="Specialist Cloud Services", number="4").response(),
    ]


def cloud_lots(latest=False):
    if latest:
        return [
            LotStub(
                lot_id=15,
                slug="iaas-and-paas",
                name="Infrastructure as a Service (IaaS) and Platform as a Service (PaaS)",
                number="1a",
            ).response(),
            LotStub(
                lot_id=16,
                slug="iaas-and-paas-above-official",
                name="Infrastructure as a Service (IaaS) and Platform as a Service (PaaS) above OFFICIAL",
                number="1b",
            ).response(),
            LotStub(
                lot_id=17,
                slug="isaas",
                name="Infrastructure Software as a Service (iSaaS)",
                number="2a",
            ).response(),
            LotStub(
                lot_id=1,
                slug="saas",
                name="Software as a Service (SaaS)",
                number="2b",
            ).response(),
            LotStub(
                lot_id=11,
                slug="cloud-support",
                name="Cloud Support",
                number="3",
            ).response(),
        ]

    return [
        LotStub(lot_id=9, slug="cloud-hosting", name="Cloud hosting", number="1").response(),
        LotStub(lot_id=10, slug="cloud-software", name="Cloud software", number="2").response(),
        LotStub(lot_id=11, slug="cloud-support", name="Cloud Support", number="3").response(),
    ]
