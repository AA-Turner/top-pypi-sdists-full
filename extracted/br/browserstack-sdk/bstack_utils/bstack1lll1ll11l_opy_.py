# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import json
from bstack_utils.bstack1l1111l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1l1111ll_opy_(object):
  bstack11l1l111ll_opy_ = os.path.join(os.path.expanduser(bstack11l1ll1_opy_ (u"ࠨࢀࠪᡬ")), bstack11l1ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᡭ"))
  bstack11l1l11111l_opy_ = os.path.join(bstack11l1l111ll_opy_, bstack11l1ll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪᡮ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11l1llll_opy_ = None
  bstack11ll11ll1_opy_ = None
  bstack11l1l1ll11l_opy_ = None
  bstack11l1ll1l111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l1ll1_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭ᡯ")):
      cls.instance = super(bstack11l1l1111ll_opy_, cls).__new__(cls)
      cls.instance.bstack11l11llllll_opy_()
    return cls.instance
  def bstack11l11llllll_opy_(self):
    try:
      with open(self.bstack11l1l11111l_opy_, bstack11l1ll1_opy_ (u"ࠬࡸࠧᡰ")) as bstack11ll1l11l1_opy_:
        bstack11l1l111111_opy_ = bstack11ll1l11l1_opy_.read()
        data = json.loads(bstack11l1l111111_opy_)
        if bstack11l1ll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᡱ") in data:
          self.bstack11l1l111ll1_opy_(data[bstack11l1ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᡲ")])
        if bstack11l1ll1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᡳ") in data:
          self.bstack11ll11l11l_opy_(data[bstack11l1ll1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᡴ")])
        if bstack11l1ll1_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᡵ") in data:
          self.bstack11l1l1111l1_opy_(data[bstack11l1ll1_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᡶ")])
    except:
      pass
  def bstack11l1l1111l1_opy_(self, bstack11l1ll1l111_opy_):
    if bstack11l1ll1l111_opy_ != None:
      self.bstack11l1ll1l111_opy_ = bstack11l1ll1l111_opy_
  def bstack11ll11l11l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11l1ll1_opy_ (u"ࠬࡹࡣࡢࡰࠪᡷ"),bstack11l1ll1_opy_ (u"࠭ࠧᡸ"))
      self.bstack11l1llll_opy_ = scripts.get(bstack11l1ll1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫ᡹"),bstack11l1ll1_opy_ (u"ࠨࠩ᡺"))
      self.bstack11ll11ll1_opy_ = scripts.get(bstack11l1ll1_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭᡻"),bstack11l1ll1_opy_ (u"ࠪࠫ᡼"))
      self.bstack11l1l1ll11l_opy_ = scripts.get(bstack11l1ll1_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩ᡽"),bstack11l1ll1_opy_ (u"ࠬ࠭᡾"))
  def bstack11l1l111ll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l1l11111l_opy_, bstack11l1ll1_opy_ (u"࠭ࡷࠨ᡿")) as file:
        json.dump({
          bstack11l1ll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤᢀ"): self.commands_to_wrap,
          bstack11l1ll1_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤᢁ"): {
            bstack11l1ll1_opy_ (u"ࠤࡶࡧࡦࡴࠢᢂ"): self.perform_scan,
            bstack11l1ll1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᢃ"): self.bstack11l1llll_opy_,
            bstack11l1ll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᢄ"): self.bstack11ll11ll1_opy_,
            bstack11l1ll1_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᢅ"): self.bstack11l1l1ll11l_opy_
          },
          bstack11l1ll1_opy_ (u"ࠨ࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠥᢆ"): self.bstack11l1ll1l111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᢇ").format(e))
      pass
  def bstack1111lll1l_opy_(self, command_name):
    try:
      return any(command.get(bstack11l1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᢈ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1lll1ll11l_opy_ = bstack11l1l1111ll_opy_()