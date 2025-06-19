# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from bstack_utils.constants import bstack11ll1ll11ll_opy_
def bstack11l1l111_opy_(bstack11ll1ll11l1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack111llll1l_opy_
    host = bstack111llll1l_opy_(cli.config, [bstack111lll_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᛴ"), bstack111lll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᛵ"), bstack111lll_opy_ (u"ࠧࡧࡰࡪࠤᛶ")], bstack11ll1ll11ll_opy_) if cli.is_running() else bstack11ll1ll11ll_opy_
    return bstack111lll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᛷ").format(host, bstack11ll1ll11l1_opy_)