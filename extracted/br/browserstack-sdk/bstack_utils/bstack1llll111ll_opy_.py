# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from bstack_utils.constants import bstack11ll11l11ll_opy_
def bstack11l11l11_opy_(bstack11ll11l11l1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l11lll111_opy_
    host = bstack1l11lll111_opy_(cli.config, [bstack1111l1l_opy_ (u"ࠧࡧࡰࡪࡵࠥ᝭"), bstack1111l1l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣᝮ"), bstack1111l1l_opy_ (u"ࠢࡢࡲ࡬ࠦᝯ")], bstack11ll11l11ll_opy_)
    return bstack1111l1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᝰ").format(host, bstack11ll11l11l1_opy_)