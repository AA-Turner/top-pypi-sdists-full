# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l1ll1l1_opy_
from bstack_utils import logger_utils
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111l111l_opy_())
def bstack1llll11ll11l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llll11lll11_opy_(bstack1llll11llll1_opy_, bstack1llll11lllll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llll11llll1_opy_):
        with open(bstack1llll11llll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1llll11ll11l_opy_(bstack1llll11llll1_opy_):
        pac = get_pac(url=bstack1llll11llll1_opy_)
    else:
        raise Exception(bstack1ll111_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫḟ").format(bstack1llll11llll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll111_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨḠ"), 80))
        bstack1llll11lll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llll11lll1l_opy_ = bstack1ll111_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧḡ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llll11lllll_opy_, bstack1llll11lll1l_opy_)
    return proxy_url
def bstack1lll1ll1l_opy_(config):
    return bstack1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪḢ") in config or bstack1ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬḣ") in config
def bstack11lll11l_opy_(config):
    if not bstack1lll1ll1l_opy_(config):
        return
    if config.get(bstack1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬḤ")):
        return config.get(bstack1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ḥ"))
    if config.get(bstack1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨḦ")):
        return config.get(bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩḧ"))
def bstack111lllllll_opy_(config, bstack1llll11lllll_opy_):
    proxy = bstack11lll11l_opy_(config)
    proxies = {}
    if config.get(bstack1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩḨ")) or config.get(bstack1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫḩ")):
        if proxy.endswith(bstack1ll111_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭Ḫ")):
            proxies = bstack1l1l11l1l_opy_(proxy, bstack1llll11lllll_opy_)
        else:
            proxies = {
                bstack1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨḫ"): proxy
            }
    global_config.bstack1lll11l111_opy_(bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪḬ"), proxies)
    return proxies
def bstack1l1l11l1l_opy_(bstack1llll11llll1_opy_, bstack1llll11lllll_opy_):
    proxies = {}
    global bstack1llll11ll1l1_opy_
    if bstack1ll111_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧḭ") in globals():
        return bstack1llll11ll1l1_opy_
    try:
        proxy = bstack1llll11lll11_opy_(bstack1llll11llll1_opy_, bstack1llll11lllll_opy_)
        if bstack1ll111_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧḮ") in proxy:
            proxies = {}
        elif bstack1ll111_opy_ (u"ࠨࡈࡕࡖࡓࠦḯ") in proxy or bstack1ll111_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨḰ") in proxy or bstack1ll111_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢḱ") in proxy:
            bstack1llll11ll1ll_opy_ = proxy.split(bstack1ll111_opy_ (u"ࠤࠣࠦḲ"))
            if bstack1ll111_opy_ (u"ࠥ࠾࠴࠵ࠢḳ") in bstack1ll111_opy_ (u"ࠦࠧḴ").join(bstack1llll11ll1ll_opy_[1:]):
                proxies = {
                    bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫḵ"): bstack1ll111_opy_ (u"ࠨࠢḶ").join(bstack1llll11ll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ḷ"): str(bstack1llll11ll1ll_opy_[0]).lower() + bstack1ll111_opy_ (u"ࠣ࠼࠲࠳ࠧḸ") + bstack1ll111_opy_ (u"ࠤࠥḹ").join(bstack1llll11ll1ll_opy_[1:])
                }
        elif bstack1ll111_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤḺ") in proxy:
            bstack1llll11ll1ll_opy_ = proxy.split(bstack1ll111_opy_ (u"ࠦࠥࠨḻ"))
            if bstack1ll111_opy_ (u"ࠧࡀ࠯࠰ࠤḼ") in bstack1ll111_opy_ (u"ࠨࠢḽ").join(bstack1llll11ll1ll_opy_[1:]):
                proxies = {
                    bstack1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ḿ"): bstack1ll111_opy_ (u"ࠣࠤḿ").join(bstack1llll11ll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨṀ"): bstack1ll111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦṁ") + bstack1ll111_opy_ (u"ࠦࠧṂ").join(bstack1llll11ll1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫṃ"): proxy
            }
    except Exception as e:
        print(bstack1ll111_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥṄ"), bstack1111l1ll1l1_opy_.format(bstack1llll11llll1_opy_, str(e)))
    bstack1llll11ll1l1_opy_ = proxies
    return proxies