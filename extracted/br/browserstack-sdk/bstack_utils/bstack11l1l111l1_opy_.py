# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from bstack_utils.constants import bstack11ll11l11l1_opy_
def bstack1111l1lll_opy_(bstack11ll11l111l_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1ll1111l1l_opy_
    host = bstack1ll1111l1l_opy_(cli.config, [bstack1l11ll1_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᝫ"), bstack1l11ll1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᝬ"), bstack1l11ll1_opy_ (u"ࠧࡧࡰࡪࠤ᝭")], bstack11ll11l11l1_opy_)
    return bstack1l11ll1_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᝮ").format(host, bstack11ll11l111l_opy_)