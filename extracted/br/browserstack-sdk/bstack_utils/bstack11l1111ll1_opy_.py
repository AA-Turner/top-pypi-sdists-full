# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from bstack_utils.constants import bstack11ll1l111ll_opy_
def bstack11ll11l1ll_opy_(bstack11ll1l11l11_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l1l11ll1_opy_
    host = bstack1l1l11ll1_opy_(cli.config, [bstack11ll11_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᜂ"), bstack11ll11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᜃ"), bstack11ll11_opy_ (u"ࠧࡧࡰࡪࠤᜄ")], bstack11ll1l111ll_opy_) if cli.is_running() else bstack11ll1l111ll_opy_
    return bstack11ll11_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᜅ").format(host, bstack11ll1l11l11_opy_)