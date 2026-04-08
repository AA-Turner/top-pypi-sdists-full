# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1lll1lll1_opy_():
  def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111ll_opy_, bstack1ll111ll1l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
    self.bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_
    self.bstack1ll111ll1l1_opy_ = bstack1ll111ll1l1_opy_
  def bstack111111lll_opy_(self, bstack1ll11lll11l_opy_, bstack11111lllll_opy_, bstack1ll111ll1ll_opy_=False):
    bstack11ll1l1lll_opy_ = multiprocessing.get_context(bstack111l_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭᎔"))
    bstack111l111l_opy_ = []
    manager = bstack11ll1l1lll_opy_.Manager()
    bstack1ll11lll1l1_opy_ = manager.list()
    global_config = Config.bstack1lll111ll_opy_()
    if bstack1ll111ll1ll_opy_:
      for index, platform in enumerate(self.bstack1lllll11111_opy_[bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᎕")]):
        if index == 0:
          bstack11111lllll_opy_[bstack111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ᎖")] = self.args
        bstack111l111l_opy_.append(bstack11ll1l1lll_opy_.Process(name=str(index),
                                          target=bstack1ll11lll11l_opy_,
                                          args=(bstack11111lllll_opy_, bstack1ll11lll1l1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllll11111_opy_[bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᎗")]):
        bstack111l111l_opy_.append(bstack11ll1l1lll_opy_.Process(name=str(index),
                                          target=bstack1ll11lll11l_opy_,
                                          args=(bstack11111lllll_opy_, bstack1ll11lll1l1_opy_)))
    i = 0
    for t in bstack111l111l_opy_:
      try:
        if global_config.get_property(bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ᎘")):
          os.environ[bstack111l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭᎙")] = json.dumps(self.bstack1lllll11111_opy_[bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᎚")][i % self.bstack1ll111ll1l1_opy_])
      except Exception as e:
        self.logger.debug(bstack111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢ᎛").format(str(e)))
      i += 1
      t.start()
    for t in bstack111l111l_opy_:
      t.join()
    return list(bstack1ll11lll1l1_opy_)