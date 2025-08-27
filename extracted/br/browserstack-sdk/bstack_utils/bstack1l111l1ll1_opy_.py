# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from bstack_utils.constants import bstack11ll11l1lll_opy_
def bstack1ll11l11l1_opy_(bstack11ll11ll111_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l1ll11l1l_opy_
    host = bstack1l1ll11l1l_opy_(cli.config, [bstack1111lll_opy_ (u"ࠢࡢࡲ࡬ࡷࠧᝨ"), bstack1111lll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥᝩ"), bstack1111lll_opy_ (u"ࠤࡤࡴ࡮ࠨᝪ")], bstack11ll11l1lll_opy_)
    return bstack1111lll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᝫ").format(host, bstack11ll11ll111_opy_)