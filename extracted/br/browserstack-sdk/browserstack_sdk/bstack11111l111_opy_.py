# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack111ll11ll1_opy_():
  def __init__(self, args, logger, bstack1lllll111l1_opy_, bstack1lllll11l1l_opy_, bstack1ll111ll1l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
    self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
    self.bstack1ll111ll1l1_opy_ = bstack1ll111ll1l1_opy_
  def bstack1lll1l1l_opy_(self, bstack1ll11l11111_opy_, bstack1ll11l1l_opy_, bstack1ll111ll1ll_opy_=False):
    bstack11ll1ll1l_opy_ = multiprocessing.get_context(bstack1ll1l11_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭᎔"))
    bstack11ll111ll1_opy_ = []
    manager = bstack11ll1ll1l_opy_.Manager()
    bstack1ll11lll111_opy_ = manager.list()
    global_config = Config.bstack1lllllll1_opy_()
    if bstack1ll111ll1ll_opy_:
      for index, platform in enumerate(self.bstack1lllll111l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᎕")]):
        if index == 0:
          bstack1ll11l1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ᎖")] = self.args
        bstack11ll111ll1_opy_.append(bstack11ll1ll1l_opy_.Process(name=str(index),
                                          target=bstack1ll11l11111_opy_,
                                          args=(bstack1ll11l1l_opy_, bstack1ll11lll111_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllll111l1_opy_[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᎗")]):
        bstack11ll111ll1_opy_.append(bstack11ll1ll1l_opy_.Process(name=str(index),
                                          target=bstack1ll11l11111_opy_,
                                          args=(bstack1ll11l1l_opy_, bstack1ll11lll111_opy_)))
    i = 0
    for t in bstack11ll111ll1_opy_:
      try:
        if global_config.get_property(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ᎘")):
          os.environ[bstack1ll1l11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭᎙")] = json.dumps(self.bstack1lllll111l1_opy_[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᎚")][i % self.bstack1ll111ll1l1_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢ᎛").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll111ll1_opy_:
      t.join()
    return list(bstack1ll11lll111_opy_)