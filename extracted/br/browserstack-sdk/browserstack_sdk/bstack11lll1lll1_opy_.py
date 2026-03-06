# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11l111l1ll_opy_():
  def __init__(self, args, logger, bstack1llll1ll111_opy_, bstack1llll111ll1_opy_, bstack1lll1ll11l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1llll1ll111_opy_ = bstack1llll1ll111_opy_
    self.bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_
    self.bstack1lll1ll11l1_opy_ = bstack1lll1ll11l1_opy_
  def bstack11lll1l1ll_opy_(self, bstack1llll111111_opy_, bstack1l1lll111l_opy_, bstack1lll1ll111l_opy_=False):
    bstack11ll111lll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1llll11ll1l_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1lll1ll111l_opy_:
      for index, platform in enumerate(self.bstack1llll1ll111_opy_[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᆋ")]):
        if index == 0:
          bstack1l1lll111l_opy_[bstack1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᆌ")] = self.args
        bstack11ll111lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll111111_opy_,
                                                    args=(bstack1l1lll111l_opy_, bstack1llll11ll1l_opy_)))
    else:
      for index, platform in enumerate(self.bstack1llll1ll111_opy_[bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᆍ")]):
        bstack11ll111lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll111111_opy_,
                                                    args=(bstack1l1lll111l_opy_, bstack1llll11ll1l_opy_)))
    i = 0
    for t in bstack11ll111lll_opy_:
      try:
        if global_config.get_property(bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᆎ")):
          os.environ[bstack1111_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩᆏ")] = json.dumps(self.bstack1llll1ll111_opy_[bstack1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᆐ")][i % self.bstack1lll1ll11l1_opy_])
      except Exception as e:
        self.logger.debug(bstack1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠥᆑ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll111lll_opy_:
      t.join()
    return list(bstack1llll11ll1l_opy_)