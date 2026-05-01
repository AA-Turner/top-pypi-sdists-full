# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll1l1111l1_opy_
from bstack_utils import logger_utils
global_config = Config.bstack1l1l11ll1_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1ll1l111l1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1l111ll1l_opy_(bstack1ll1l11l111l_opy_, bstack1ll1l11l1111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1l11l111l_opy_):
        with open(bstack1ll1l11l111l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1l111l1ll_opy_(bstack1ll1l11l111l_opy_):
        pac = get_pac(url=bstack1ll1l11l111l_opy_)
    else:
        raise Exception(bstack111ll_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫ⚋").format(bstack1ll1l11l111l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111ll_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨ⚌"), 80))
        bstack1ll1l111ll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1l111ll11_opy_ = bstack111ll_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧ⚍")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l11l1111_opy_, bstack1ll1l111ll11_opy_)
    return proxy_url
def bstack111lll111_opy_(config):
    return bstack111ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⚎") in config or bstack111ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⚏") in config
def bstack1lll1111ll_opy_(config):
    if not bstack111lll111_opy_(config):
        return
    if config.get(bstack111ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⚐")):
        return config.get(bstack111ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⚑"))
    if config.get(bstack111ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⚒")):
        return config.get(bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⚓"))
def bstack1l1111111l_opy_(config, bstack1ll1l11l1111_opy_):
    proxy = bstack1lll1111ll_opy_(config)
    proxies = {}
    if config.get(bstack111ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⚔")) or config.get(bstack111ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⚕")):
        if proxy.endswith(bstack111ll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭⚖")):
            proxies = bstack111lllll1_opy_(proxy, bstack1ll1l11l1111_opy_)
        else:
            proxies = {
                bstack111ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⚗"): proxy
            }
    global_config.bstack1l1l1llll1_opy_(bstack111ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ⚘"), proxies)
    return proxies
def bstack111lllll1_opy_(bstack1ll1l11l111l_opy_, bstack1ll1l11l1111_opy_):
    proxies = {}
    global bstack1ll1l111llll_opy_
    if bstack111ll_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧ⚙") in globals():
        return bstack1ll1l111llll_opy_
    try:
        proxy = bstack1ll1l111ll1l_opy_(bstack1ll1l11l111l_opy_, bstack1ll1l11l1111_opy_)
        if bstack111ll_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧ⚚") in proxy:
            proxies = {}
        elif bstack111ll_opy_ (u"ࠨࡈࡕࡖࡓࠦ⚛") in proxy or bstack111ll_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨ⚜") in proxy or bstack111ll_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢ⚝") in proxy:
            bstack1ll1l111lll1_opy_ = proxy.split(bstack111ll_opy_ (u"ࠤࠣࠦ⚞"))
            if bstack111ll_opy_ (u"ࠥ࠾࠴࠵ࠢ⚟") in bstack111ll_opy_ (u"ࠦࠧ⚠").join(bstack1ll1l111lll1_opy_[1:]):
                proxies = {
                    bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⚡"): bstack111ll_opy_ (u"ࠨࠢ⚢").join(bstack1ll1l111lll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭⚣"): str(bstack1ll1l111lll1_opy_[0]).lower() + bstack111ll_opy_ (u"ࠣ࠼࠲࠳ࠧ⚤") + bstack111ll_opy_ (u"ࠤࠥ⚥").join(bstack1ll1l111lll1_opy_[1:])
                }
        elif bstack111ll_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤ⚦") in proxy:
            bstack1ll1l111lll1_opy_ = proxy.split(bstack111ll_opy_ (u"ࠦࠥࠨ⚧"))
            if bstack111ll_opy_ (u"ࠧࡀ࠯࠰ࠤ⚨") in bstack111ll_opy_ (u"ࠨࠢ⚩").join(bstack1ll1l111lll1_opy_[1:]):
                proxies = {
                    bstack111ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭⚪"): bstack111ll_opy_ (u"ࠣࠤ⚫").join(bstack1ll1l111lll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⚬"): bstack111ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⚭") + bstack111ll_opy_ (u"ࠦࠧ⚮").join(bstack1ll1l111lll1_opy_[1:])
                }
        else:
            proxies = {
                bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⚯"): proxy
            }
    except Exception as e:
        print(bstack111ll_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ⚰"), bstack1lll1l1111l1_opy_.format(bstack1ll1l11l111l_opy_, str(e)))
    bstack1ll1l111llll_opy_ = proxies
    return proxies