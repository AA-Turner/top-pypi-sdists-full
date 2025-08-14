# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
from bstack_utils.constants import bstack11ll11l1lll_opy_
def bstack1llll1111l_opy_(bstack11ll11ll111_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1ll11llll_opy_
    host = bstack1ll11llll_opy_(cli.config, [bstack1l1l1ll_opy_ (u"ࠢࡢࡲ࡬ࡷࠧᝨ"), bstack1l1l1ll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥᝩ"), bstack1l1l1ll_opy_ (u"ࠤࡤࡴ࡮ࠨᝪ")], bstack11ll11l1lll_opy_)
    return bstack1l1l1ll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᝫ").format(host, bstack11ll11ll111_opy_)