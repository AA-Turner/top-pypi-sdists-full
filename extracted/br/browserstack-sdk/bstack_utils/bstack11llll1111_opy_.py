# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import json
from bstack_utils.bstack1l11l1l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l111llll1_opy_(object):
  bstack1lll11l1l_opy_ = os.path.join(os.path.expanduser(bstack11l1111_opy_ (u"ࠨࢀࠪ៼")), bstack11l1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ៽"))
  bstack11l111lllll_opy_ = os.path.join(bstack1lll11l1l_opy_, bstack11l1111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪ៾"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l11llll11_opy_ = None
  bstack1l1111l11l_opy_ = None
  bstack11l11l1l1l1_opy_ = None
  bstack11l1l111lll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l1111_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭៿")):
      cls.instance = super(bstack11l111llll1_opy_, cls).__new__(cls)
      cls.instance.bstack11l11l1111l_opy_()
    return cls.instance
  def bstack11l11l1111l_opy_(self):
    try:
      with open(self.bstack11l111lllll_opy_, bstack11l1111_opy_ (u"ࠬࡸࠧ᠀")) as bstack1l1ll1lll1_opy_:
        bstack11l11l111l1_opy_ = bstack1l1ll1lll1_opy_.read()
        data = json.loads(bstack11l11l111l1_opy_)
        if bstack11l1111_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᠁") in data:
          self.bstack11l11llll1l_opy_(data[bstack11l1111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ᠂")])
        if bstack11l1111_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᠃") in data:
          self.bstack11l1l1llll_opy_(data[bstack11l1111_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ᠄")])
        if bstack11l1111_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᠅") in data:
          self.bstack11l11l11111_opy_(data[bstack11l1111_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᠆")])
    except:
      pass
  def bstack11l11l11111_opy_(self, bstack11l1l111lll_opy_):
    if bstack11l1l111lll_opy_ != None:
      self.bstack11l1l111lll_opy_ = bstack11l1l111lll_opy_
  def bstack11l1l1llll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11l1111_opy_ (u"ࠬࡹࡣࡢࡰࠪ᠇"),bstack11l1111_opy_ (u"࠭ࠧ᠈"))
      self.bstack1l11llll11_opy_ = scripts.get(bstack11l1111_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫ᠉"),bstack11l1111_opy_ (u"ࠨࠩ᠊"))
      self.bstack1l1111l11l_opy_ = scripts.get(bstack11l1111_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭᠋"),bstack11l1111_opy_ (u"ࠪࠫ᠌"))
      self.bstack11l11l1l1l1_opy_ = scripts.get(bstack11l1111_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩ᠍"),bstack11l1111_opy_ (u"ࠬ࠭᠎"))
  def bstack11l11llll1l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l111lllll_opy_, bstack11l1111_opy_ (u"࠭ࡷࠨ᠏")) as file:
        json.dump({
          bstack11l1111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤ᠐"): self.commands_to_wrap,
          bstack11l1111_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤ᠑"): {
            bstack11l1111_opy_ (u"ࠤࡶࡧࡦࡴࠢ᠒"): self.perform_scan,
            bstack11l1111_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢ᠓"): self.bstack1l11llll11_opy_,
            bstack11l1111_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣ᠔"): self.bstack1l1111l11l_opy_,
            bstack11l1111_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥ᠕"): self.bstack11l11l1l1l1_opy_
          },
          bstack11l1111_opy_ (u"ࠨ࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠥ᠖"): self.bstack11l1l111lll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧ᠗").format(e))
      pass
  def bstack1lll1ll1_opy_(self, bstack1lll1111ll1_opy_):
    try:
      return any(command.get(bstack11l1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭᠘")) == bstack1lll1111ll1_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11llll1111_opy_ = bstack11l111llll1_opy_()