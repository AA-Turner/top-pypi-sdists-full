# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111111l11l_opy_
from bstack_utils import logger_utils
bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111l11l1_opy_())
def bstack1lll1l1ll1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1l1ll111_opy_(bstack1lll1l1ll1l1_opy_, bstack1lll1l1l1ll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll1l1ll1l1_opy_):
        with open(bstack1lll1l1ll1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll1l1ll1ll_opy_(bstack1lll1l1ll1l1_opy_):
        pac = get_pac(url=bstack1lll1l1ll1l1_opy_)
    else:
        raise Exception(bstack11l11_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭↽").format(bstack1lll1l1ll1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l11_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣ↾"), 80))
        bstack1lll1l1lll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1l1lll11_opy_ = bstack11l11_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩ↿")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1l1l1ll1_opy_, bstack1lll1l1lll11_opy_)
    return proxy_url
def bstack1l1l11l11l_opy_(config):
    return bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⇀") in config or bstack11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⇁") in config
def bstack111l11l11_opy_(config):
    if not bstack1l1l11l11l_opy_(config):
        return
    if config.get(bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⇂")):
        return config.get(bstack11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⇃"))
    if config.get(bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⇄")):
        return config.get(bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⇅"))
def bstack1llll1l111_opy_(config, bstack1lll1l1l1ll1_opy_):
    proxy = bstack111l11l11_opy_(config)
    proxies = {}
    if config.get(bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⇆")) or config.get(bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⇇")):
        if proxy.endswith(bstack11l11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ⇈")):
            proxies = bstack11l11l1ll1_opy_(proxy, bstack1lll1l1l1ll1_opy_)
        else:
            proxies = {
                bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ⇉"): proxy
            }
    bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬ⇊"), proxies)
    return proxies
def bstack11l11l1ll1_opy_(bstack1lll1l1ll1l1_opy_, bstack1lll1l1l1ll1_opy_):
    proxies = {}
    global bstack1lll1l1l1lll_opy_
    if bstack11l11_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩ⇋") in globals():
        return bstack1lll1l1l1lll_opy_
    try:
        proxy = bstack1lll1l1ll111_opy_(bstack1lll1l1ll1l1_opy_, bstack1lll1l1l1ll1_opy_)
        if bstack11l11_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢ⇌") in proxy:
            proxies = {}
        elif bstack11l11_opy_ (u"ࠣࡊࡗࡘࡕࠨ⇍") in proxy or bstack11l11_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣ⇎") in proxy or bstack11l11_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤ⇏") in proxy:
            bstack1lll1l1ll11l_opy_ = proxy.split(bstack11l11_opy_ (u"ࠦࠥࠨ⇐"))
            if bstack11l11_opy_ (u"ࠧࡀ࠯࠰ࠤ⇑") in bstack11l11_opy_ (u"ࠨࠢ⇒").join(bstack1lll1l1ll11l_opy_[1:]):
                proxies = {
                    bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭⇓"): bstack11l11_opy_ (u"ࠣࠤ⇔").join(bstack1lll1l1ll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⇕"): str(bstack1lll1l1ll11l_opy_[0]).lower() + bstack11l11_opy_ (u"ࠥ࠾࠴࠵ࠢ⇖") + bstack11l11_opy_ (u"ࠦࠧ⇗").join(bstack1lll1l1ll11l_opy_[1:])
                }
        elif bstack11l11_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦ⇘") in proxy:
            bstack1lll1l1ll11l_opy_ = proxy.split(bstack11l11_opy_ (u"ࠨࠠࠣ⇙"))
            if bstack11l11_opy_ (u"ࠢ࠻࠱࠲ࠦ⇚") in bstack11l11_opy_ (u"ࠣࠤ⇛").join(bstack1lll1l1ll11l_opy_[1:]):
                proxies = {
                    bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⇜"): bstack11l11_opy_ (u"ࠥࠦ⇝").join(bstack1lll1l1ll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ⇞"): bstack11l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ⇟") + bstack11l11_opy_ (u"ࠨࠢ⇠").join(bstack1lll1l1ll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭⇡"): proxy
            }
    except Exception as e:
        print(bstack11l11_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ⇢"), bstack1111111l11l_opy_.format(bstack1lll1l1ll1l1_opy_, str(e)))
    bstack1lll1l1l1lll_opy_ = proxies
    return proxies