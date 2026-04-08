# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll1l1l11l1_opy_
from bstack_utils import logger_utils
global_config = Config.bstack1lll111ll_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1ll1l1l11ll1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1l1l1l11l_opy_(bstack1ll1l1l111ll_opy_, bstack1ll1l1l11l11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1l1l111ll_opy_):
        with open(bstack1ll1l1l111ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1l1l11ll1_opy_(bstack1ll1l1l111ll_opy_):
        pac = get_pac(url=bstack1ll1l1l111ll_opy_)
    else:
        raise Exception(bstack111l_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭☈").format(bstack1ll1l1l111ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111l_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣ☉"), 80))
        bstack1ll1l1l1l111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1l1l1l111_opy_ = bstack111l_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩ☊")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l1l11l11_opy_, bstack1ll1l1l1l111_opy_)
    return proxy_url
def bstack1l1ll11l_opy_(config):
    return bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ☋") in config or bstack111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ☌") in config
def bstack111l11l1l_opy_(config):
    if not bstack1l1ll11l_opy_(config):
        return
    if config.get(bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ☍")):
        return config.get(bstack111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ☎"))
    if config.get(bstack111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ☏")):
        return config.get(bstack111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ☐"))
def bstack11l1llll11_opy_(config, bstack1ll1l1l11l11_opy_):
    proxy = bstack111l11l1l_opy_(config)
    proxies = {}
    if config.get(bstack111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ☑")) or config.get(bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭☒")):
        if proxy.endswith(bstack111l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ☓")):
            proxies = bstack111111111_opy_(proxy, bstack1ll1l1l11l11_opy_)
        else:
            proxies = {
                bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ☔"): proxy
            }
    global_config.bstack1l11ll11_opy_(bstack111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ☕"), proxies)
    return proxies
def bstack111111111_opy_(bstack1ll1l1l111ll_opy_, bstack1ll1l1l11l11_opy_):
    proxies = {}
    global bstack1ll1l1l11l1l_opy_
    if bstack111l_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩ☖") in globals():
        return bstack1ll1l1l11l1l_opy_
    try:
        proxy = bstack1ll1l1l1l11l_opy_(bstack1ll1l1l111ll_opy_, bstack1ll1l1l11l11_opy_)
        if bstack111l_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢ☗") in proxy:
            proxies = {}
        elif bstack111l_opy_ (u"ࠣࡊࡗࡘࡕࠨ☘") in proxy or bstack111l_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣ☙") in proxy or bstack111l_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤ☚") in proxy:
            bstack1ll1l1l11lll_opy_ = proxy.split(bstack111l_opy_ (u"ࠦࠥࠨ☛"))
            if bstack111l_opy_ (u"ࠧࡀ࠯࠰ࠤ☜") in bstack111l_opy_ (u"ࠨࠢ☝").join(bstack1ll1l1l11lll_opy_[1:]):
                proxies = {
                    bstack111l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭☞"): bstack111l_opy_ (u"ࠣࠤ☟").join(bstack1ll1l1l11lll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ☠"): str(bstack1ll1l1l11lll_opy_[0]).lower() + bstack111l_opy_ (u"ࠥ࠾࠴࠵ࠢ☡") + bstack111l_opy_ (u"ࠦࠧ☢").join(bstack1ll1l1l11lll_opy_[1:])
                }
        elif bstack111l_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦ☣") in proxy:
            bstack1ll1l1l11lll_opy_ = proxy.split(bstack111l_opy_ (u"ࠨࠠࠣ☤"))
            if bstack111l_opy_ (u"ࠢ࠻࠱࠲ࠦ☥") in bstack111l_opy_ (u"ࠣࠤ☦").join(bstack1ll1l1l11lll_opy_[1:]):
                proxies = {
                    bstack111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ☧"): bstack111l_opy_ (u"ࠥࠦ☨").join(bstack1ll1l1l11lll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ☩"): bstack111l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ☪") + bstack111l_opy_ (u"ࠨࠢ☫").join(bstack1ll1l1l11lll_opy_[1:])
                }
        else:
            proxies = {
                bstack111l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭☬"): proxy
            }
    except Exception as e:
        print(bstack111l_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ☭"), bstack1lll1l1l11l1_opy_.format(bstack1ll1l1l111ll_opy_, str(e)))
    bstack1ll1l1l11l1l_opy_ = proxies
    return proxies