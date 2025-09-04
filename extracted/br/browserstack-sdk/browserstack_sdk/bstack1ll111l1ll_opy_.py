# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11lll111_opy_():
  def __init__(self, args, logger, bstack1111l11111_opy_, bstack11111l1l1l_opy_, bstack111111ll11_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l11111_opy_ = bstack1111l11111_opy_
    self.bstack11111l1l1l_opy_ = bstack11111l1l1l_opy_
    self.bstack111111ll11_opy_ = bstack111111ll11_opy_
  def bstack11l1l1ll_opy_(self, bstack1111l11l1l_opy_, bstack1l111l1l1l_opy_, bstack111111ll1l_opy_=False):
    bstack11l1l1l1l1_opy_ = []
    manager = multiprocessing.Manager()
    bstack11111llll1_opy_ = manager.list()
    bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
    if bstack111111ll1l_opy_:
      for index, platform in enumerate(self.bstack1111l11111_opy_[bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫႌ")]):
        if index == 0:
          bstack1l111l1l1l_opy_[bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩႍࠬ")] = self.args
        bstack11l1l1l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11l1l_opy_,
                                                    args=(bstack1l111l1l1l_opy_, bstack11111llll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l11111_opy_[bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႎ")]):
        bstack11l1l1l1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11l1l_opy_,
                                                    args=(bstack1l111l1l1l_opy_, bstack11111llll1_opy_)))
    i = 0
    for t in bstack11l1l1l1l1_opy_:
      try:
        if bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬႏ")):
          os.environ[bstack1111l1l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭႐")] = json.dumps(self.bstack1111l11111_opy_[bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ႑")][i % self.bstack111111ll11_opy_])
      except Exception as e:
        self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢ႒").format(str(e)))
      i += 1
      t.start()
    for t in bstack11l1l1l1l1_opy_:
      t.join()
    return list(bstack11111llll1_opy_)