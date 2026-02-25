# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111111ll1l1_opy_
from bstack_utils import logger_utils
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1111l11l_opy_())
def bstack1lll1ll1l1l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1ll1l1ll_opy_(bstack1lll1ll1ll1l_opy_, bstack1lll1ll1ll11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll1ll1ll1l_opy_):
        with open(bstack1lll1ll1ll1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll1ll1l1l1_opy_(bstack1lll1ll1ll1l_opy_):
        pac = get_pac(url=bstack1lll1ll1ll1l_opy_)
    else:
        raise Exception(bstack11l1l11_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪ⇈").format(bstack1lll1ll1ll1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1l11_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧ⇉"), 80))
        bstack1lll1ll11lll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1ll11lll_opy_ = bstack11l1l11_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭⇊")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1ll1ll11_opy_, bstack1lll1ll11lll_opy_)
    return proxy_url
def bstack1l1llll1_opy_(config):
    return bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⇋") in config or bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⇌") in config
def bstack11lll1ll11_opy_(config):
    if not bstack1l1llll1_opy_(config):
        return
    if config.get(bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⇍")):
        return config.get(bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⇎"))
    if config.get(bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⇏")):
        return config.get(bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⇐"))
def bstack1lll1l11l1_opy_(config, bstack1lll1ll1ll11_opy_):
    proxy = bstack11lll1ll11_opy_(config)
    proxies = {}
    if config.get(bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⇑")) or config.get(bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⇒")):
        if proxy.endswith(bstack11l1l11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ⇓")):
            proxies = bstack11ll11lll_opy_(proxy, bstack1lll1ll1ll11_opy_)
        else:
            proxies = {
                bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⇔"): proxy
            }
    global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩ⇕"), proxies)
    return proxies
def bstack11ll11lll_opy_(bstack1lll1ll1ll1l_opy_, bstack1lll1ll1ll11_opy_):
    proxies = {}
    global bstack1lll1ll1l111_opy_
    if bstack11l1l11_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭⇖") in globals():
        return bstack1lll1ll1l111_opy_
    try:
        proxy = bstack1lll1ll1l1ll_opy_(bstack1lll1ll1ll1l_opy_, bstack1lll1ll1ll11_opy_)
        if bstack11l1l11_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦ⇗") in proxy:
            proxies = {}
        elif bstack11l1l11_opy_ (u"ࠧࡎࡔࡕࡒࠥ⇘") in proxy or bstack11l1l11_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧ⇙") in proxy or bstack11l1l11_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨ⇚") in proxy:
            bstack1lll1ll1l11l_opy_ = proxy.split(bstack11l1l11_opy_ (u"ࠣࠢࠥ⇛"))
            if bstack11l1l11_opy_ (u"ࠤ࠽࠳࠴ࠨ⇜") in bstack11l1l11_opy_ (u"ࠥࠦ⇝").join(bstack1lll1ll1l11l_opy_[1:]):
                proxies = {
                    bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ⇞"): bstack11l1l11_opy_ (u"ࠧࠨ⇟").join(bstack1lll1ll1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⇠"): str(bstack1lll1ll1l11l_opy_[0]).lower() + bstack11l1l11_opy_ (u"ࠢ࠻࠱࠲ࠦ⇡") + bstack11l1l11_opy_ (u"ࠣࠤ⇢").join(bstack1lll1ll1l11l_opy_[1:])
                }
        elif bstack11l1l11_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣ⇣") in proxy:
            bstack1lll1ll1l11l_opy_ = proxy.split(bstack11l1l11_opy_ (u"ࠥࠤࠧ⇤"))
            if bstack11l1l11_opy_ (u"ࠦ࠿࠵࠯ࠣ⇥") in bstack11l1l11_opy_ (u"ࠧࠨ⇦").join(bstack1lll1ll1l11l_opy_[1:]):
                proxies = {
                    bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⇧"): bstack11l1l11_opy_ (u"ࠢࠣ⇨").join(bstack1lll1ll1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⇩"): bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ⇪") + bstack11l1l11_opy_ (u"ࠥࠦ⇫").join(bstack1lll1ll1l11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ⇬"): proxy
            }
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ⇭"), bstack111111ll1l1_opy_.format(bstack1lll1ll1ll1l_opy_, str(e)))
    bstack1lll1ll1l111_opy_ = proxies
    return proxies