# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll1lll11_opy_():
  def __init__(self, args, logger, bstack1111ll1l11_opy_, bstack1111l1l1ll_opy_, bstack11111l1l11_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111ll1l11_opy_ = bstack1111ll1l11_opy_
    self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
    self.bstack11111l1l11_opy_ = bstack11111l1l11_opy_
  def bstack1ll1111ll_opy_(self, bstack11111ll1ll_opy_, bstack1ll11ll1l_opy_, bstack11111l1l1l_opy_=False):
    bstack11ll1l1ll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1l11l_opy_ = manager.list()
    bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
    if bstack11111l1l1l_opy_:
      for index, platform in enumerate(self.bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ၆")]):
        if index == 0:
          bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ၇")] = self.args
        bstack11ll1l1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111ll1ll_opy_,
                                                    args=(bstack1ll11ll1l_opy_, bstack1111l1l11l_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭၈")]):
        bstack11ll1l1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111ll1ll_opy_,
                                                    args=(bstack1ll11ll1l_opy_, bstack1111l1l11l_opy_)))
    i = 0
    for t in bstack11ll1l1ll_opy_:
      try:
        if bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ၉")):
          os.environ[bstack11ll11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭၊")] = json.dumps(self.bstack1111ll1l11_opy_[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ။")][i % self.bstack11111l1l11_opy_])
      except Exception as e:
        self.logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢ၌").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll1l1ll_opy_:
      t.join()
    return list(bstack1111l1l11l_opy_)