# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l1lll1ll_opy_():
  def __init__(self, args, logger, bstack11111llll1_opy_, bstack11111ll1ll_opy_, bstack11111l1l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111llll1_opy_ = bstack11111llll1_opy_
    self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    self.bstack11111l1l1l_opy_ = bstack11111l1l1l_opy_
  def bstack1llll1lll1_opy_(self, bstack1111l1lll1_opy_, bstack1ll11l1l_opy_, bstack11111l1ll1_opy_=False):
    bstack1l1l1l111l_opy_ = []
    manager = multiprocessing.Manager()
    bstack11111lll11_opy_ = manager.list()
    bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
    if bstack11111l1ll1_opy_:
      for index, platform in enumerate(self.bstack11111llll1_opy_[bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ၇")]):
        if index == 0:
          bstack1ll11l1l_opy_[bstack1l1ll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭၈")] = self.args
        bstack1l1l1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l1lll1_opy_,
                                                    args=(bstack1ll11l1l_opy_, bstack11111lll11_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111llll1_opy_[bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ၉")]):
        bstack1l1l1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l1lll1_opy_,
                                                    args=(bstack1ll11l1l_opy_, bstack11111lll11_opy_)))
    i = 0
    for t in bstack1l1l1l111l_opy_:
      try:
        if bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭၊")):
          os.environ[bstack1l1ll1_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ။")] = json.dumps(self.bstack11111llll1_opy_[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ၌")][i % self.bstack11111l1l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠣ၍").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l1l1l111l_opy_:
      t.join()
    return list(bstack11111lll11_opy_)