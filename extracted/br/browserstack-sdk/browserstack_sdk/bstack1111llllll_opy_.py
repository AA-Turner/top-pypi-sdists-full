# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11111lll1_opy_():
  def __init__(self, args, logger, bstack1lll1l1111l_opy_, bstack1lll1l1llll_opy_, bstack1lll11ll1l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lll1l1111l_opy_ = bstack1lll1l1111l_opy_
    self.bstack1lll1l1llll_opy_ = bstack1lll1l1llll_opy_
    self.bstack1lll11ll1l1_opy_ = bstack1lll11ll1l1_opy_
  def bstack11ll1111_opy_(self, bstack1lll1l11111_opy_, bstack111lll1l11_opy_, bstack1lll11ll11l_opy_=False):
    bstack1ll11l11_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lll11lll11_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1lll11ll11l_opy_:
      for index, platform in enumerate(self.bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫሩ")]):
        if index == 0:
          bstack111lll1l11_opy_[bstack1111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬሪ")] = self.args
        bstack1ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll1l11111_opy_,
                                                    args=(bstack111lll1l11_opy_, bstack1lll11lll11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ራ")]):
        bstack1ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll1l11111_opy_,
                                                    args=(bstack111lll1l11_opy_, bstack1lll11lll11_opy_)))
    i = 0
    for t in bstack1ll11l11_opy_:
      try:
        if global_config.get_property(bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬሬ")):
          os.environ[bstack1111l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ር")] = json.dumps(self.bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩሮ")][i % self.bstack1lll11ll1l1_opy_])
      except Exception as e:
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢሯ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll11l11_opy_:
      t.join()
    return list(bstack1lll11lll11_opy_)