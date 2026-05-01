# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from bstack_utils.constants import bstack1111l11111l_opy_
def bstack1ll1l1ll11_opy_(bstack1111l1111l1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11l1llll1l_opy_
    host = bstack11l1llll1l_opy_(cli.config, [bstack111ll_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᶼ"), bstack111ll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᶽ"), bstack111ll_opy_ (u"ࠧࡧࡰࡪࠤᶾ")], bstack1111l11111l_opy_)
    return bstack111ll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᶿ").format(host, bstack1111l1111l1_opy_)