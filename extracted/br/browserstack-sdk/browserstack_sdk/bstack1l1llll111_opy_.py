# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1111l111l_opy_():
  def __init__(self, args, logger, bstack1lllllll11l_opy_, bstack1llllll11ll_opy_, bstack1ll1lll11ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
    self.bstack1llllll11ll_opy_ = bstack1llllll11ll_opy_
    self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
  def bstack11l1ll1ll_opy_(self, bstack1lll11l11l1_opy_, bstack1l11l111_opy_, bstack1ll1lll1l11_opy_=False):
    bstack1lll1l11l1_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lll1111l11_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1ll1lll1l11_opy_:
      for index, platform in enumerate(self.bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫች")]):
        if index == 0:
          bstack1l11l111_opy_[bstack1ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬቾ")] = self.args
        bstack1lll1l11l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll11l11l1_opy_,
                                                    args=(bstack1l11l111_opy_, bstack1lll1111l11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ቿ")]):
        bstack1lll1l11l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll11l11l1_opy_,
                                                    args=(bstack1l11l111_opy_, bstack1lll1111l11_opy_)))
    i = 0
    for t in bstack1lll1l11l1_opy_:
      try:
        if global_config.get_property(bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬኀ")):
          os.environ[bstack1ll11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ኁ")] = json.dumps(self.bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩኂ")][i % self.bstack1ll1lll11ll_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢኃ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1lll1l11l1_opy_:
      t.join()
    return list(bstack1lll1111l11_opy_)