# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11ll1ll1l_opy_():
  def __init__(self, args, logger, bstack1111l1lll1_opy_, bstack1111l111ll_opy_, bstack11111l111l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l1lll1_opy_ = bstack1111l1lll1_opy_
    self.bstack1111l111ll_opy_ = bstack1111l111ll_opy_
    self.bstack11111l111l_opy_ = bstack11111l111l_opy_
  def bstack1lll11lll_opy_(self, bstack1111l11ll1_opy_, bstack1l11l1l1_opy_, bstack11111l1111_opy_=False):
    bstack1lll1lll1_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1llll_opy_ = manager.list()
    bstack11ll1l1l1_opy_ = Config.bstack1l1l111l1l_opy_()
    if bstack11111l1111_opy_:
      for index, platform in enumerate(self.bstack1111l1lll1_opy_[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၾ")]):
        if index == 0:
          bstack1l11l1l1_opy_[bstack1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬၿ")] = self.args
        bstack1lll1lll1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11ll1_opy_,
                                                    args=(bstack1l11l1l1_opy_, bstack1111l1llll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l1lll1_opy_[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႀ")]):
        bstack1lll1lll1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11ll1_opy_,
                                                    args=(bstack1l11l1l1_opy_, bstack1111l1llll_opy_)))
    i = 0
    for t in bstack1lll1lll1_opy_:
      try:
        if bstack11ll1l1l1_opy_.get_property(bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬႁ")):
          os.environ[bstack1l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ႂ")] = json.dumps(self.bstack1111l1lll1_opy_[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႃ")][i % self.bstack11111l111l_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢႄ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1lll1lll1_opy_:
      t.join()
    return list(bstack1111l1llll_opy_)