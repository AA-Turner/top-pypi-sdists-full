# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll1111ll_opy_
from bstack_utils import logger_utils
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1lll111ll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll111l1ll1_opy_(bstack1lll111l1lll_opy_, bstack1lll111ll1l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll111l1lll_opy_):
        with open(bstack1lll111l1lll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll111ll111_opy_(bstack1lll111l1lll_opy_):
        pac = get_pac(url=bstack1lll111l1lll_opy_)
    else:
        raise Exception(bstack1l1_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩ␅").format(bstack1lll111l1lll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦ␆"), 80))
        bstack1lll111ll11l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll111ll11l_opy_ = bstack1l1_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬ␇")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll111ll1l1_opy_, bstack1lll111ll11l_opy_)
    return proxy_url
def bstack1lll11lll_opy_(config):
    return bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ␈") in config or bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ␉") in config
def bstack1l1l11111l_opy_(config):
    if not bstack1lll11lll_opy_(config):
        return
    if config.get(bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ␊")):
        return config.get(bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ␋"))
    if config.get(bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭␌")):
        return config.get(bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ␍"))
def bstack1l111ll1l_opy_(config, bstack1lll111ll1l1_opy_):
    proxy = bstack1l1l11111l_opy_(config)
    proxies = {}
    if config.get(bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ␎")) or config.get(bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ␏")):
        if proxy.endswith(bstack1l1_opy_ (u"࠭࠮ࡱࡣࡦࠫ␐")):
            proxies = bstack1ll1111111_opy_(proxy, bstack1lll111ll1l1_opy_)
        else:
            proxies = {
                bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭␑"): proxy
            }
    global_config.bstack11l11111ll_opy_(bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨ␒"), proxies)
    return proxies
def bstack1ll1111111_opy_(bstack1lll111l1lll_opy_, bstack1lll111ll1l1_opy_):
    proxies = {}
    global bstack1lll111l1l1l_opy_
    if bstack1l1_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬ␓") in globals():
        return bstack1lll111l1l1l_opy_
    try:
        proxy = bstack1lll111l1ll1_opy_(bstack1lll111l1lll_opy_, bstack1lll111ll1l1_opy_)
        if bstack1l1_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥ␔") in proxy:
            proxies = {}
        elif bstack1l1_opy_ (u"ࠦࡍ࡚ࡔࡑࠤ␕") in proxy or bstack1l1_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦ␖") in proxy or bstack1l1_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧ␗") in proxy:
            bstack1lll111l1l11_opy_ = proxy.split(bstack1l1_opy_ (u"ࠢࠡࠤ␘"))
            if bstack1l1_opy_ (u"ࠣ࠼࠲࠳ࠧ␙") in bstack1l1_opy_ (u"ࠤࠥ␚").join(bstack1lll111l1l11_opy_[1:]):
                proxies = {
                    bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ␛"): bstack1l1_opy_ (u"ࠦࠧ␜").join(bstack1lll111l1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ␝"): str(bstack1lll111l1l11_opy_[0]).lower() + bstack1l1_opy_ (u"ࠨ࠺࠰࠱ࠥ␞") + bstack1l1_opy_ (u"ࠢࠣ␟").join(bstack1lll111l1l11_opy_[1:])
                }
        elif bstack1l1_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢ␠") in proxy:
            bstack1lll111l1l11_opy_ = proxy.split(bstack1l1_opy_ (u"ࠤࠣࠦ␡"))
            if bstack1l1_opy_ (u"ࠥ࠾࠴࠵ࠢ␢") in bstack1l1_opy_ (u"ࠦࠧ␣").join(bstack1lll111l1l11_opy_[1:]):
                proxies = {
                    bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ␤"): bstack1l1_opy_ (u"ࠨࠢ␥").join(bstack1lll111l1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭␦"): bstack1l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ␧") + bstack1l1_opy_ (u"ࠤࠥ␨").join(bstack1lll111l1l11_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ␩"): proxy
            }
    except Exception as e:
        print(bstack1l1_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ␪"), bstack1lllll1111ll_opy_.format(bstack1lll111l1lll_opy_, str(e)))
    bstack1lll111l1l1l_opy_ = proxies
    return proxies