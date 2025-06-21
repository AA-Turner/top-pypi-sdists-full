# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import json
from bstack_utils.bstack1llll1l111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll1l1l111_opy_(object):
  bstack11l1llll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠪࢂࠬᛦ")), bstack1l1l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᛧ"))
  bstack11ll1l11ll1_opy_ = os.path.join(bstack11l1llll_opy_, bstack1l1l1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬᛨ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll1111111_opy_ = None
  bstack1l1ll1ll_opy_ = None
  bstack11lll1l1l11_opy_ = None
  bstack11lll1l11l1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1l1l1_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨᛩ")):
      cls.instance = super(bstack11ll1l1l111_opy_, cls).__new__(cls)
      cls.instance.bstack11ll1l11l1l_opy_()
    return cls.instance
  def bstack11ll1l11l1l_opy_(self):
    try:
      with open(self.bstack11ll1l11ll1_opy_, bstack1l1l1l1_opy_ (u"ࠧࡳࠩᛪ")) as bstack1111l1l1l_opy_:
        bstack11ll1l1l11l_opy_ = bstack1111l1l1l_opy_.read()
        data = json.loads(bstack11ll1l1l11l_opy_)
        if bstack1l1l1l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ᛫") in data:
          self.bstack11lll111ll1_opy_(data[bstack1l1l1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ᛬")])
        if bstack1l1l1l1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᛭") in data:
          self.bstack11ll111ll1_opy_(data[bstack1l1l1l1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᛮ")])
        if bstack1l1l1l1_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᛯ") in data:
          self.bstack11ll1l11lll_opy_(data[bstack1l1l1l1_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᛰ")])
    except:
      pass
  def bstack11ll1l11lll_opy_(self, bstack11lll1l11l1_opy_):
    if bstack11lll1l11l1_opy_ != None:
      self.bstack11lll1l11l1_opy_ = bstack11lll1l11l1_opy_
  def bstack11ll111ll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡤࡲࠬᛱ"),bstack1l1l1l1_opy_ (u"ࠨࠩᛲ"))
      self.bstack1ll1111111_opy_ = scripts.get(bstack1l1l1l1_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ᛳ"),bstack1l1l1l1_opy_ (u"ࠪࠫᛴ"))
      self.bstack1l1ll1ll_opy_ = scripts.get(bstack1l1l1l1_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨᛵ"),bstack1l1l1l1_opy_ (u"ࠬ࠭ᛶ"))
      self.bstack11lll1l1l11_opy_ = scripts.get(bstack1l1l1l1_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᛷ"),bstack1l1l1l1_opy_ (u"ࠧࠨᛸ"))
  def bstack11lll111ll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll1l11ll1_opy_, bstack1l1l1l1_opy_ (u"ࠨࡹࠪ᛹")) as file:
        json.dump({
          bstack1l1l1l1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦ᛺"): self.commands_to_wrap,
          bstack1l1l1l1_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦ᛻"): {
            bstack1l1l1l1_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ᛼"): self.perform_scan,
            bstack1l1l1l1_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤ᛽"): self.bstack1ll1111111_opy_,
            bstack1l1l1l1_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥ᛾"): self.bstack1l1ll1ll_opy_,
            bstack1l1l1l1_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧ᛿"): self.bstack11lll1l1l11_opy_
          },
          bstack1l1l1l1_opy_ (u"ࠣࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠧᜀ"): self.bstack11lll1l11l1_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1l1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᜁ").format(e))
      pass
  def bstack11l11lllll_opy_(self, bstack1ll11lll1l1_opy_):
    try:
      return any(command.get(bstack1l1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᜂ")) == bstack1ll11lll1l1_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1111ll1l1_opy_ = bstack11ll1l1l111_opy_()