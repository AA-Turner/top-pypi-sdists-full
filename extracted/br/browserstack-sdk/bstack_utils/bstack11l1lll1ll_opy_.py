# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from bstack_utils.constants import bstack11l1l111111_opy_
def bstack111lll1l1_opy_(bstack11l1l11111l_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11ll1l11_opy_
    host = bstack11ll1l11_opy_(cli.config, [bstack1l1111_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᢃ"), bstack1l1111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᢄ"), bstack1l1111_opy_ (u"ࠧࡧࡰࡪࠤᢅ")], bstack11l1l111111_opy_)
    return bstack1l1111_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᢆ").format(host, bstack11l1l11111l_opy_)