# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l111l1l11_opy_(object):
  bstack11l111l11l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠧࡿࠩ᤽")), bstack11ll111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᤾"))
  bstack11l111ll111_opy_ = os.path.join(bstack11l111l11l_opy_, bstack11ll111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ᤿"))
  commands_to_wrap = None
  perform_scan = None
  bstack1lll11ll11_opy_ = None
  bstack1ll1l1ll_opy_ = None
  bstack11l111ll11l_opy_ = None
  bstack11l11l1l111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11ll111_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬ᥀")):
      cls.instance = super(bstack11l111l1l11_opy_, cls).__new__(cls)
      cls.instance.bstack11l111l1l1l_opy_()
    return cls.instance
  def bstack11l111l1l1l_opy_(self):
    try:
      with open(self.bstack11l111ll111_opy_, bstack11ll111_opy_ (u"ࠫࡷ࠭᥁")) as bstack11l111l11_opy_:
        bstack11l111l1lll_opy_ = bstack11l111l11_opy_.read()
        data = json.loads(bstack11l111l1lll_opy_)
        if bstack11ll111_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ᥂") in data:
          self.bstack11l11llllll_opy_(data[bstack11ll111_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᥃")])
        if bstack11ll111_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ᥄") in data:
          self.bstack11llll1l1_opy_(data[bstack11ll111_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᥅")])
        if bstack11ll111_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᥆") in data:
          self.bstack11l111l1ll1_opy_(data[bstack11ll111_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᥇")])
    except:
      pass
  def bstack11l111l1ll1_opy_(self, bstack11l11l1l111_opy_):
    if bstack11l11l1l111_opy_ != None:
      self.bstack11l11l1l111_opy_ = bstack11l11l1l111_opy_
  def bstack11llll1l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11ll111_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ᥈"),bstack11ll111_opy_ (u"ࠬ࠭᥉"))
      self.bstack1lll11ll11_opy_ = scripts.get(bstack11ll111_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪ᥊"),bstack11ll111_opy_ (u"ࠧࠨ᥋"))
      self.bstack1ll1l1ll_opy_ = scripts.get(bstack11ll111_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬ᥌"),bstack11ll111_opy_ (u"ࠩࠪ᥍"))
      self.bstack11l111ll11l_opy_ = scripts.get(bstack11ll111_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨ᥎"),bstack11ll111_opy_ (u"ࠫࠬ᥏"))
  def bstack11l11llllll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l111ll111_opy_, bstack11ll111_opy_ (u"ࠬࡽࠧᥐ")) as file:
        json.dump({
          bstack11ll111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᥑ"): self.commands_to_wrap,
          bstack11ll111_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣᥒ"): {
            bstack11ll111_opy_ (u"ࠣࡵࡦࡥࡳࠨᥓ"): self.perform_scan,
            bstack11ll111_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᥔ"): self.bstack1lll11ll11_opy_,
            bstack11ll111_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᥕ"): self.bstack1ll1l1ll_opy_,
            bstack11ll111_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᥖ"): self.bstack11l111ll11l_opy_
          },
          bstack11ll111_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤᥗ"): self.bstack11l11l1l111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᥘ").format(e))
      pass
  def bstack111l1111l1_opy_(self, command_name):
    try:
      return any(command.get(bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᥙ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack11ll11llll_opy_ = bstack11l111l1l11_opy_()