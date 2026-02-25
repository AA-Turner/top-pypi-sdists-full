# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l111l1l1l_opy_(object):
  bstack111l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠪࢂࠬ᥀")), bstack11l1l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᥁"))
  bstack11l111l1lll_opy_ = os.path.join(bstack111l1ll1l1_opy_, bstack11l1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬ᥂"))
  commands_to_wrap = None
  perform_scan = None
  bstack1llll11111_opy_ = None
  bstack11l1111lll_opy_ = None
  bstack11l11ll11l1_opy_ = None
  bstack11l111lll1l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨ᥃")):
      cls.instance = super(bstack11l111l1l1l_opy_, cls).__new__(cls)
      cls.instance.bstack11l111ll11l_opy_()
    return cls.instance
  def bstack11l111ll11l_opy_(self):
    try:
      with open(self.bstack11l111l1lll_opy_, bstack11l1l11_opy_ (u"ࠧࡳࠩ᥄")) as bstack1l1l111ll_opy_:
        bstack11l111ll111_opy_ = bstack1l1l111ll_opy_.read()
        data = json.loads(bstack11l111ll111_opy_)
        if bstack11l1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ᥅") in data:
          self.bstack11l111lllll_opy_(data[bstack11l1l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ᥆")])
        if bstack11l1l11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᥇") in data:
          self.bstack11l11l1ll_opy_(data[bstack11l1l11_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ᥈")])
        if bstack11l1l11_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᥉") in data:
          self.bstack11l111l1ll1_opy_(data[bstack11l1l11_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᥊")])
    except:
      pass
  def bstack11l111l1ll1_opy_(self, bstack11l111lll1l_opy_):
    if bstack11l111lll1l_opy_ != None:
      self.bstack11l111lll1l_opy_ = bstack11l111lll1l_opy_
  def bstack11l11l1ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11l1l11_opy_ (u"ࠧࡴࡥࡤࡲࠬ᥋"),bstack11l1l11_opy_ (u"ࠨࠩ᥌"))
      self.bstack1llll11111_opy_ = scripts.get(bstack11l1l11_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭᥍"),bstack11l1l11_opy_ (u"ࠪࠫ᥎"))
      self.bstack11l1111lll_opy_ = scripts.get(bstack11l1l11_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨ᥏"),bstack11l1l11_opy_ (u"ࠬ࠭ᥐ"))
      self.bstack11l11ll11l1_opy_ = scripts.get(bstack11l1l11_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᥑ"),bstack11l1l11_opy_ (u"ࠧࠨᥒ"))
  def bstack11l111lllll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l111l1lll_opy_, bstack11l1l11_opy_ (u"ࠨࡹࠪᥓ")) as file:
        json.dump({
          bstack11l1l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦᥔ"): self.commands_to_wrap,
          bstack11l1l11_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦᥕ"): {
            bstack11l1l11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᥖ"): self.perform_scan,
            bstack11l1l11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᥗ"): self.bstack1llll11111_opy_,
            bstack11l1l11_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᥘ"): self.bstack11l1111lll_opy_,
            bstack11l1l11_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᥙ"): self.bstack11l11ll11l1_opy_
          },
          bstack11l1l11_opy_ (u"ࠣࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠧᥚ"): self.bstack11l111lll1l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᥛ").format(e))
      pass
  def bstack1l111l1l1l_opy_(self, command_name):
    try:
      return any(command.get(bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᥜ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack111llllll1_opy_ = bstack11l111l1l1l_opy_()