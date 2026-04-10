# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11ll1l1l1l_opy_():
  def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111l1_opy_, bstack1ll111ll1ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
    self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
    self.bstack1ll111ll1ll_opy_ = bstack1ll111ll1ll_opy_
  def bstack111l11l1ll_opy_(self, bstack1ll11ll11l1_opy_, bstack11l11lll_opy_, bstack1ll111ll1l1_opy_=False):
    bstack11l1l111l_opy_ = multiprocessing.get_context(bstack1ll_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭᎔"))
    bstack11l1llll1l_opy_ = []
    manager = bstack11l1l111l_opy_.Manager()
    bstack1ll11ll1111_opy_ = manager.list()
    global_config = Config.bstack1l111l1111_opy_()
    if bstack1ll111ll1l1_opy_:
      for index, platform in enumerate(self.bstack1lllll11111_opy_[bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᎕")]):
        if index == 0:
          bstack11l11lll_opy_[bstack1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ᎖")] = self.args
        bstack11l1llll1l_opy_.append(bstack11l1l111l_opy_.Process(name=str(index),
                                          target=bstack1ll11ll11l1_opy_,
                                          args=(bstack11l11lll_opy_, bstack1ll11ll1111_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllll11111_opy_[bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᎗")]):
        bstack11l1llll1l_opy_.append(bstack11l1l111l_opy_.Process(name=str(index),
                                          target=bstack1ll11ll11l1_opy_,
                                          args=(bstack11l11lll_opy_, bstack1ll11ll1111_opy_)))
    i = 0
    for t in bstack11l1llll1l_opy_:
      try:
        if global_config.get_property(bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ᎘")):
          os.environ[bstack1ll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭᎙")] = json.dumps(self.bstack1lllll11111_opy_[bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᎚")][i % self.bstack1ll111ll1ll_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢ᎛").format(str(e)))
      i += 1
      t.start()
    for t in bstack11l1llll1l_opy_:
      t.join()
    return list(bstack1ll11ll1111_opy_)