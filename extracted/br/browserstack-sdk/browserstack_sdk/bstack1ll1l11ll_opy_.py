# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11111l1111_opy_():
  def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111ll_opy_, bstack1ll111ll1l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
    self.bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_
    self.bstack1ll111ll1l1_opy_ = bstack1ll111ll1l1_opy_
  def bstack1l11111l_opy_(self, bstack1ll11lll111_opy_, bstack1l11l1l1l_opy_, bstack1ll111ll1ll_opy_=False):
    bstack1111l1l1_opy_ = multiprocessing.get_context(bstack11ll11_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭᎔"))
    bstack1111l11ll_opy_ = []
    manager = bstack1111l1l1_opy_.Manager()
    bstack1ll11l1l1l1_opy_ = manager.list()
    global_config = Config.bstack111llll11_opy_()
    if bstack1ll111ll1ll_opy_:
      for index, platform in enumerate(self.bstack1lllll11111_opy_[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᎕")]):
        if index == 0:
          bstack1l11l1l1l_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ᎖")] = self.args
        bstack1111l11ll_opy_.append(bstack1111l1l1_opy_.Process(name=str(index),
                                          target=bstack1ll11lll111_opy_,
                                          args=(bstack1l11l1l1l_opy_, bstack1ll11l1l1l1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllll11111_opy_[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᎗")]):
        bstack1111l11ll_opy_.append(bstack1111l1l1_opy_.Process(name=str(index),
                                          target=bstack1ll11lll111_opy_,
                                          args=(bstack1l11l1l1l_opy_, bstack1ll11l1l1l1_opy_)))
    i = 0
    for t in bstack1111l11ll_opy_:
      try:
        if global_config.get_property(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ᎘")):
          os.environ[bstack11ll11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭᎙")] = json.dumps(self.bstack1lllll11111_opy_[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᎚")][i % self.bstack1ll111ll1l1_opy_])
      except Exception as e:
        self.logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢ᎛").format(str(e)))
      i += 1
      t.start()
    for t in bstack1111l11ll_opy_:
      t.join()
    return list(bstack1ll11l1l1l1_opy_)