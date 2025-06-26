# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1lll1l1l1_opy_():
  def __init__(self, args, logger, bstack1111l1l1l1_opy_, bstack1111l1ll11_opy_, bstack11111l1l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
    self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
    self.bstack11111l1l1l_opy_ = bstack11111l1l1l_opy_
  def bstack1111111l_opy_(self, bstack11111l1lll_opy_, bstack1lll1ll1_opy_, bstack11111l1l11_opy_=False):
    bstack1ll111ll1l_opy_ = []
    manager = multiprocessing.Manager()
    bstack11111lll11_opy_ = manager.list()
    bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
    if bstack11111l1l11_opy_:
      for index, platform in enumerate(self.bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ၇")]):
        if index == 0:
          bstack1lll1ll1_opy_[bstack11ll1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭၈")] = self.args
        bstack1ll111ll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111l1lll_opy_,
                                                    args=(bstack1lll1ll1_opy_, bstack11111lll11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ၉")]):
        bstack1ll111ll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111l1lll_opy_,
                                                    args=(bstack1lll1ll1_opy_, bstack11111lll11_opy_)))
    i = 0
    for t in bstack1ll111ll1l_opy_:
      try:
        if bstack1111ll111_opy_.get_property(bstack11ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭၊")):
          os.environ[bstack11ll1l1_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ။")] = json.dumps(self.bstack1111l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ၌")][i % self.bstack11111l1l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠣ၍").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll111ll1l_opy_:
      t.join()
    return list(bstack11111lll11_opy_)