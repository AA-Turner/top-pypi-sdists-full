# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import json
from bstack_utils.bstack111llll1ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1l1111l1_opy_(object):
  bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠩࢁࠫᡦ")), bstack1l1111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᡧ"))
  bstack11l1l111ll1_opy_ = os.path.join(bstack1l1llllll1_opy_, bstack1l1111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫᡨ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l11lll11l_opy_ = None
  bstack1lll1l1l1_opy_ = None
  bstack11l1l1l1l1l_opy_ = None
  bstack11l1ll1111l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1111_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧᡩ")):
      cls.instance = super(bstack11l1l1111l1_opy_, cls).__new__(cls)
      cls.instance.bstack11l1l111l11_opy_()
    return cls.instance
  def bstack11l1l111l11_opy_(self):
    try:
      with open(self.bstack11l1l111ll1_opy_, bstack1l1111_opy_ (u"࠭ࡲࠨᡪ")) as bstack111ll1ll_opy_:
        bstack11l1l111l1l_opy_ = bstack111ll1ll_opy_.read()
        data = json.loads(bstack11l1l111l1l_opy_)
        if bstack1l1111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᡫ") in data:
          self.bstack11l1ll11lll_opy_(data[bstack1l1111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᡬ")])
        if bstack1l1111_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᡭ") in data:
          self.bstack1l1l11lll1_opy_(data[bstack1l1111_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᡮ")])
        if bstack1l1111_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᡯ") in data:
          self.bstack11l1l1111ll_opy_(data[bstack1l1111_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᡰ")])
    except:
      pass
  def bstack11l1l1111ll_opy_(self, bstack11l1ll1111l_opy_):
    if bstack11l1ll1111l_opy_ != None:
      self.bstack11l1ll1111l_opy_ = bstack11l1ll1111l_opy_
  def bstack1l1l11lll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1111_opy_ (u"࠭ࡳࡤࡣࡱࠫᡱ"),bstack1l1111_opy_ (u"ࠧࠨᡲ"))
      self.bstack1l11lll11l_opy_ = scripts.get(bstack1l1111_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᡳ"),bstack1l1111_opy_ (u"ࠩࠪᡴ"))
      self.bstack1lll1l1l1_opy_ = scripts.get(bstack1l1111_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᡵ"),bstack1l1111_opy_ (u"ࠫࠬᡶ"))
      self.bstack11l1l1l1l1l_opy_ = scripts.get(bstack1l1111_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᡷ"),bstack1l1111_opy_ (u"࠭ࠧᡸ"))
  def bstack11l1ll11lll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l1l111ll1_opy_, bstack1l1111_opy_ (u"ࠧࡸࠩ᡹")) as file:
        json.dump({
          bstack1l1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥ᡺"): self.commands_to_wrap,
          bstack1l1111_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥ᡻"): {
            bstack1l1111_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᡼"): self.perform_scan,
            bstack1l1111_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣ᡽"): self.bstack1l11lll11l_opy_,
            bstack1l1111_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤ᡾"): self.bstack1lll1l1l1_opy_,
            bstack1l1111_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦ᡿"): self.bstack11l1l1l1l1l_opy_
          },
          bstack1l1111_opy_ (u"ࠢ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠦᢀ"): self.bstack11l1ll1111l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠼ࠣࡿࢂࠨᢁ").format(e))
      pass
  def bstack11111lll_opy_(self, command_name):
    try:
      return any(command.get(bstack1l1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᢂ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l1111l1ll_opy_ = bstack11l1l1111l1_opy_()