# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from bstack_utils.constants import bstack11l111lll1l_opy_
def bstack11111111_opy_(bstack11ll111ll11_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l1l1l11l1_opy_
    host = bstack1l1l1l11l1_opy_(cli.config, [bstack11l1111_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ᠙"), bstack11l1111_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ᠚"), bstack11l1111_opy_ (u"ࠦࡦࡶࡩࠣ᠛")], bstack11l111lll1l_opy_)
    return bstack11l1111_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫ᠜").format(host, bstack11ll111ll11_opy_)