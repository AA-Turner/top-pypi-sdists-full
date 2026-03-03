# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111111ll111_opy_
from bstack_utils import logger_utils
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1l11ll1l_opy_())
def bstack1lll1ll1ll11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1ll1l11l_opy_(bstack1lll1ll1l111_opy_, bstack1lll1ll1l1l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll1ll1l111_opy_):
        with open(bstack1lll1ll1l111_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll1ll1ll11_opy_(bstack1lll1ll1l111_opy_):
        pac = get_pac(url=bstack1lll1ll1l111_opy_)
    else:
        raise Exception(bstack11ll111_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧ⇅").format(bstack1lll1ll1l111_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11ll111_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤ⇆"), 80))
        bstack1lll1ll11lll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1ll11lll_opy_ = bstack11ll111_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪ⇇")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1ll1l1l1_opy_, bstack1lll1ll11lll_opy_)
    return proxy_url
def bstack1lllll1l11_opy_(config):
    return bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⇈") in config or bstack11ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⇉") in config
def bstack1111lllll1_opy_(config):
    if not bstack1lllll1l11_opy_(config):
        return
    if config.get(bstack11ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⇊")):
        return config.get(bstack11ll111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⇋"))
    if config.get(bstack11ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⇌")):
        return config.get(bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⇍"))
def bstack1111llll1l_opy_(config, bstack1lll1ll1l1l1_opy_):
    proxy = bstack1111lllll1_opy_(config)
    proxies = {}
    if config.get(bstack11ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⇎")) or config.get(bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⇏")):
        if proxy.endswith(bstack11ll111_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ⇐")):
            proxies = bstack111l11ll11_opy_(proxy, bstack1lll1ll1l1l1_opy_)
        else:
            proxies = {
                bstack11ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⇑"): proxy
            }
    global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭⇒"), proxies)
    return proxies
def bstack111l11ll11_opy_(bstack1lll1ll1l111_opy_, bstack1lll1ll1l1l1_opy_):
    proxies = {}
    global bstack1lll1ll11ll1_opy_
    if bstack11ll111_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪ⇓") in globals():
        return bstack1lll1ll11ll1_opy_
    try:
        proxy = bstack1lll1ll1l11l_opy_(bstack1lll1ll1l111_opy_, bstack1lll1ll1l1l1_opy_)
        if bstack11ll111_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣ⇔") in proxy:
            proxies = {}
        elif bstack11ll111_opy_ (u"ࠤࡋࡘ࡙ࡖࠢ⇕") in proxy or bstack11ll111_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤ⇖") in proxy or bstack11ll111_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥ⇗") in proxy:
            bstack1lll1ll1l1ll_opy_ = proxy.split(bstack11ll111_opy_ (u"ࠧࠦࠢ⇘"))
            if bstack11ll111_opy_ (u"ࠨ࠺࠰࠱ࠥ⇙") in bstack11ll111_opy_ (u"ࠢࠣ⇚").join(bstack1lll1ll1l1ll_opy_[1:]):
                proxies = {
                    bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⇛"): bstack11ll111_opy_ (u"ࠤࠥ⇜").join(bstack1lll1ll1l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ⇝"): str(bstack1lll1ll1l1ll_opy_[0]).lower() + bstack11ll111_opy_ (u"ࠦ࠿࠵࠯ࠣ⇞") + bstack11ll111_opy_ (u"ࠧࠨ⇟").join(bstack1lll1ll1l1ll_opy_[1:])
                }
        elif bstack11ll111_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧ⇠") in proxy:
            bstack1lll1ll1l1ll_opy_ = proxy.split(bstack11ll111_opy_ (u"ࠢࠡࠤ⇡"))
            if bstack11ll111_opy_ (u"ࠣ࠼࠲࠳ࠧ⇢") in bstack11ll111_opy_ (u"ࠤࠥ⇣").join(bstack1lll1ll1l1ll_opy_[1:]):
                proxies = {
                    bstack11ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ⇤"): bstack11ll111_opy_ (u"ࠦࠧ⇥").join(bstack1lll1ll1l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⇦"): bstack11ll111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⇧") + bstack11ll111_opy_ (u"ࠢࠣ⇨").join(bstack1lll1ll1l1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⇩"): proxy
            }
    except Exception as e:
        print(bstack11ll111_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨ⇪"), bstack111111ll111_opy_.format(bstack1lll1ll1l111_opy_, str(e)))
    bstack1lll1ll11ll1_opy_ = proxies
    return proxies