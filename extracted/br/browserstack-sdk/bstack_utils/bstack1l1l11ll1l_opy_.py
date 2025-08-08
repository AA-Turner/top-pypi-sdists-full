# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
from bstack_utils.constants import bstack11ll11ll11l_opy_
def bstack1l111l11l_opy_(bstack11ll11ll1l1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l11lll1l_opy_
    host = bstack1l11lll1l_opy_(cli.config, [bstack1ll1ll_opy_ (u"ࠢࡢࡲ࡬ࡷࠧᝡ"), bstack1ll1ll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥᝢ"), bstack1ll1ll_opy_ (u"ࠤࡤࡴ࡮ࠨᝣ")], bstack11ll11ll11l_opy_)
    return bstack1ll1ll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᝤ").format(host, bstack11ll11ll1l1_opy_)