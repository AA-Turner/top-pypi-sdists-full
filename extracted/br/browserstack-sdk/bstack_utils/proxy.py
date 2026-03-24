# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll1111ll_opy_
from bstack_utils import logger_utils
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1lll111l1lll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll111ll1l1_opy_(bstack1lll111l1ll1_opy_, bstack1lll111ll11l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll111l1ll1_opy_):
        with open(bstack1lll111l1ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll111l1lll_opy_(bstack1lll111l1ll1_opy_):
        pac = get_pac(url=bstack1lll111l1ll1_opy_)
    else:
        raise Exception(bstack1ll1lll_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫ␀").format(bstack1lll111l1ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll1lll_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨ␁"), 80))
        bstack1lll111l1l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll111l1l1l_opy_ = bstack1ll1lll_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧ␂")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll111ll11l_opy_, bstack1lll111l1l1l_opy_)
    return proxy_url
def bstack1ll1ll11l_opy_(config):
    return bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ␃") in config or bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ␄") in config
def bstack111ll1ll11_opy_(config):
    if not bstack1ll1ll11l_opy_(config):
        return
    if config.get(bstack1ll1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ␅")):
        return config.get(bstack1ll1lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭␆"))
    if config.get(bstack1ll1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ␇")):
        return config.get(bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ␈"))
def bstack11ll1l111l_opy_(config, bstack1lll111ll11l_opy_):
    proxy = bstack111ll1ll11_opy_(config)
    proxies = {}
    if config.get(bstack1ll1lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ␉")) or config.get(bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ␊")):
        if proxy.endswith(bstack1ll1lll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭␋")):
            proxies = bstack1l1ll11l_opy_(proxy, bstack1lll111ll11l_opy_)
        else:
            proxies = {
                bstack1ll1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ␌"): proxy
            }
    global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ␍"), proxies)
    return proxies
def bstack1l1ll11l_opy_(bstack1lll111l1ll1_opy_, bstack1lll111ll11l_opy_):
    proxies = {}
    global bstack1lll111ll111_opy_
    if bstack1ll1lll_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧ␎") in globals():
        return bstack1lll111ll111_opy_
    try:
        proxy = bstack1lll111ll1l1_opy_(bstack1lll111l1ll1_opy_, bstack1lll111ll11l_opy_)
        if bstack1ll1lll_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧ␏") in proxy:
            proxies = {}
        elif bstack1ll1lll_opy_ (u"ࠨࡈࡕࡖࡓࠦ␐") in proxy or bstack1ll1lll_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨ␑") in proxy or bstack1ll1lll_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢ␒") in proxy:
            bstack1lll111ll1ll_opy_ = proxy.split(bstack1ll1lll_opy_ (u"ࠤࠣࠦ␓"))
            if bstack1ll1lll_opy_ (u"ࠥ࠾࠴࠵ࠢ␔") in bstack1ll1lll_opy_ (u"ࠦࠧ␕").join(bstack1lll111ll1ll_opy_[1:]):
                proxies = {
                    bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ␖"): bstack1ll1lll_opy_ (u"ࠨࠢ␗").join(bstack1lll111ll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭␘"): str(bstack1lll111ll1ll_opy_[0]).lower() + bstack1ll1lll_opy_ (u"ࠣ࠼࠲࠳ࠧ␙") + bstack1ll1lll_opy_ (u"ࠤࠥ␚").join(bstack1lll111ll1ll_opy_[1:])
                }
        elif bstack1ll1lll_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤ␛") in proxy:
            bstack1lll111ll1ll_opy_ = proxy.split(bstack1ll1lll_opy_ (u"ࠦࠥࠨ␜"))
            if bstack1ll1lll_opy_ (u"ࠧࡀ࠯࠰ࠤ␝") in bstack1ll1lll_opy_ (u"ࠨࠢ␞").join(bstack1lll111ll1ll_opy_[1:]):
                proxies = {
                    bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭␟"): bstack1ll1lll_opy_ (u"ࠣࠤ␠").join(bstack1lll111ll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ␡"): bstack1ll1lll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ␢") + bstack1ll1lll_opy_ (u"ࠦࠧ␣").join(bstack1lll111ll1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ␤"): proxy
            }
    except Exception as e:
        print(bstack1ll1lll_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ␥"), bstack1lllll1111ll_opy_.format(bstack1lll111l1ll1_opy_, str(e)))
    bstack1lll111ll111_opy_ = proxies
    return proxies