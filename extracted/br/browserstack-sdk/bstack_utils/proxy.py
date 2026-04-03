# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll1l1l1l1l_opy_
from bstack_utils import logger_utils
global_config = Config.bstack1lllllll1_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1ll1l1l1l1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1l1l1l1l1_opy_(bstack1ll1l1l1l111_opy_, bstack1ll1l1l11l1l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1l1l1l111_opy_):
        with open(bstack1ll1l1l1l111_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1l1l1l1ll_opy_(bstack1ll1l1l1l111_opy_):
        pac = get_pac(url=bstack1ll1l1l1l111_opy_)
    else:
        raise Exception(bstack1ll1l11_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪ★").format(bstack1ll1l1l1l111_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll1l11_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧ☆"), 80))
        bstack1ll1l1l11ll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1l1l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭☇")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l1l11l1l_opy_, bstack1ll1l1l11ll1_opy_)
    return proxy_url
def bstack1l11l111ll_opy_(config):
    return bstack1ll1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ☈") in config or bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ☉") in config
def bstack111111lll_opy_(config):
    if not bstack1l11l111ll_opy_(config):
        return
    if config.get(bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ☊")):
        return config.get(bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ☋"))
    if config.get(bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ☌")):
        return config.get(bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ☍"))
def bstack1l1l1l11l1_opy_(config, bstack1ll1l1l11l1l_opy_):
    proxy = bstack111111lll_opy_(config)
    proxies = {}
    if config.get(bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ☎")) or config.get(bstack1ll1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ☏")):
        if proxy.endswith(bstack1ll1l11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ☐")):
            proxies = bstack11lll111l1_opy_(proxy, bstack1ll1l1l11l1l_opy_)
        else:
            proxies = {
                bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ☑"): proxy
            }
    global_config.bstack1111ll1l11_opy_(bstack1ll1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩ☒"), proxies)
    return proxies
def bstack11lll111l1_opy_(bstack1ll1l1l1l111_opy_, bstack1ll1l1l11l1l_opy_):
    proxies = {}
    global bstack1ll1l1l11lll_opy_
    if bstack1ll1l11_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭☓") in globals():
        return bstack1ll1l1l11lll_opy_
    try:
        proxy = bstack1ll1l1l1l1l1_opy_(bstack1ll1l1l1l111_opy_, bstack1ll1l1l11l1l_opy_)
        if bstack1ll1l11_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦ☔") in proxy:
            proxies = {}
        elif bstack1ll1l11_opy_ (u"ࠧࡎࡔࡕࡒࠥ☕") in proxy or bstack1ll1l11_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧ☖") in proxy or bstack1ll1l11_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨ☗") in proxy:
            bstack1ll1l1l1l11l_opy_ = proxy.split(bstack1ll1l11_opy_ (u"ࠣࠢࠥ☘"))
            if bstack1ll1l11_opy_ (u"ࠤ࠽࠳࠴ࠨ☙") in bstack1ll1l11_opy_ (u"ࠥࠦ☚").join(bstack1ll1l1l1l11l_opy_[1:]):
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ☛"): bstack1ll1l11_opy_ (u"ࠧࠨ☜").join(bstack1ll1l1l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ☝"): str(bstack1ll1l1l1l11l_opy_[0]).lower() + bstack1ll1l11_opy_ (u"ࠢ࠻࠱࠲ࠦ☞") + bstack1ll1l11_opy_ (u"ࠣࠤ☟").join(bstack1ll1l1l1l11l_opy_[1:])
                }
        elif bstack1ll1l11_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣ☠") in proxy:
            bstack1ll1l1l1l11l_opy_ = proxy.split(bstack1ll1l11_opy_ (u"ࠥࠤࠧ☡"))
            if bstack1ll1l11_opy_ (u"ࠦ࠿࠵࠯ࠣ☢") in bstack1ll1l11_opy_ (u"ࠧࠨ☣").join(bstack1ll1l1l1l11l_opy_[1:]):
                proxies = {
                    bstack1ll1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ☤"): bstack1ll1l11_opy_ (u"ࠢࠣ☥").join(bstack1ll1l1l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ☦"): bstack1ll1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ☧") + bstack1ll1l11_opy_ (u"ࠥࠦ☨").join(bstack1ll1l1l1l11l_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ☩"): proxy
            }
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ☪"), bstack1lll1l1l1l1l_opy_.format(bstack1ll1l1l1l111_opy_, str(e)))
    bstack1ll1l1l11lll_opy_ = proxies
    return proxies