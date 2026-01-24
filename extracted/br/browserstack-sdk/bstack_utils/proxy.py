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
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l11l111_opy_
from bstack_utils import bstack111llll1ll_opy_
bstack1llllll11l_opy_ = Config.bstack111ll1lll1_opy_()
logger = bstack111llll1ll_opy_.get_logger(__name__, bstack111llll1ll_opy_.bstack1ll11l1l111_opy_())
def bstack1llll11lll1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llll11l1lll_opy_(bstack1llll11ll1ll_opy_, bstack1llll11ll1l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llll11ll1ll_opy_):
        with open(bstack1llll11ll1ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1llll11lll1l_opy_(bstack1llll11ll1ll_opy_):
        pac = get_pac(url=bstack1llll11ll1ll_opy_)
    else:
        raise Exception(bstack1l1111_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫ⃍").format(bstack1llll11ll1ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1111_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨ⃎"), 80))
        bstack1llll11lll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llll11lll11_opy_ = bstack1l1111_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧ⃏")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llll11ll1l1_opy_, bstack1llll11lll11_opy_)
    return proxy_url
def bstack11l1ll111l_opy_(config):
    return bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⃐") in config or bstack1l1111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⃑") in config
def bstack1ll1l1l1_opy_(config):
    if not bstack11l1ll111l_opy_(config):
        return
    if config.get(bstack1l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽ⃒ࠬ")):
        return config.get(bstack1l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ⃓࠭"))
    if config.get(bstack1l1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⃔")):
        return config.get(bstack1l1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⃕"))
def bstack1l11ll11l1_opy_(config, bstack1llll11ll1l1_opy_):
    proxy = bstack1ll1l1l1_opy_(config)
    proxies = {}
    if config.get(bstack1l1111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⃖")) or config.get(bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⃗")):
        if proxy.endswith(bstack1l1111_opy_ (u"ࠨ࠰ࡳࡥࡨ⃘࠭")):
            proxies = bstack11l1l111l1_opy_(proxy, bstack1llll11ll1l1_opy_)
        else:
            proxies = {
                bstack1l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⃙"): proxy
            }
    bstack1llllll11l_opy_.bstack11l1l111ll_opy_(bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵ⃚ࠪ"), proxies)
    return proxies
def bstack11l1l111l1_opy_(bstack1llll11ll1ll_opy_, bstack1llll11ll1l1_opy_):
    proxies = {}
    global bstack1llll11ll111_opy_
    if bstack1l1111_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧ⃛") in globals():
        return bstack1llll11ll111_opy_
    try:
        proxy = bstack1llll11l1lll_opy_(bstack1llll11ll1ll_opy_, bstack1llll11ll1l1_opy_)
        if bstack1l1111_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧ⃜") in proxy:
            proxies = {}
        elif bstack1l1111_opy_ (u"ࠨࡈࡕࡖࡓࠦ⃝") in proxy or bstack1l1111_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨ⃞") in proxy or bstack1l1111_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢ⃟") in proxy:
            bstack1llll11ll11l_opy_ = proxy.split(bstack1l1111_opy_ (u"ࠤࠣࠦ⃠"))
            if bstack1l1111_opy_ (u"ࠥ࠾࠴࠵ࠢ⃡") in bstack1l1111_opy_ (u"ࠦࠧ⃢").join(bstack1llll11ll11l_opy_[1:]):
                proxies = {
                    bstack1l1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⃣"): bstack1l1111_opy_ (u"ࠨࠢ⃤").join(bstack1llll11ll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸ⃥࠭"): str(bstack1llll11ll11l_opy_[0]).lower() + bstack1l1111_opy_ (u"ࠣ࠼࠲࠳⃦ࠧ") + bstack1l1111_opy_ (u"ࠤࠥ⃧").join(bstack1llll11ll11l_opy_[1:])
                }
        elif bstack1l1111_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤ⃨") in proxy:
            bstack1llll11ll11l_opy_ = proxy.split(bstack1l1111_opy_ (u"ࠦࠥࠨ⃩"))
            if bstack1l1111_opy_ (u"ࠧࡀ࠯࠰ࠤ⃪") in bstack1l1111_opy_ (u"ࠨ⃫ࠢ").join(bstack1llll11ll11l_opy_[1:]):
                proxies = {
                    bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸ⃬࠭"): bstack1l1111_opy_ (u"ࠣࠤ⃭").join(bstack1llll11ll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⃮"): bstack1l1111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲⃯ࠦ") + bstack1l1111_opy_ (u"ࠦࠧ⃰").join(bstack1llll11ll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⃱"): proxy
            }
    except Exception as e:
        print(bstack1l1111_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ⃲"), bstack1111l11l111_opy_.format(bstack1llll11ll1ll_opy_, str(e)))
    bstack1llll11ll111_opy_ = proxies
    return proxies