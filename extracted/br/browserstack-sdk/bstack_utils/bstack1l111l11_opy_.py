# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from bstack_utils.constants import bstack11ll11l1l1l_opy_
def bstack1ll1lll11_opy_(bstack11ll11l1ll1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11ll1ll1_opy_
    host = bstack11ll1ll1_opy_(cli.config, [bstackl_opy_ (u"ࠢࡢࡲ࡬ࡷࠧᝡ"), bstackl_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥᝢ"), bstackl_opy_ (u"ࠤࡤࡴ࡮ࠨᝣ")], bstack11ll11l1l1l_opy_)
    return bstackl_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᝤ").format(host, bstack11ll11l1ll1_opy_)