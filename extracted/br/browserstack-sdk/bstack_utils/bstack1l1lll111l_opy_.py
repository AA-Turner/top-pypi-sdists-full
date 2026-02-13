# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l1111l111_opy_(object):
  bstack1l1llll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠧࡿࠩᤶ")), bstack11l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᤷ"))
  bstack11l1111l11l_opy_ = os.path.join(bstack1l1llll1l1_opy_, bstack11l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᤸ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l11llll_opy_ = None
  bstack11l11l11ll_opy_ = None
  bstack11l1111ll11_opy_ = None
  bstack11l111ll11l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l11_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩ᤹ࠬ")):
      cls.instance = super(bstack11l1111l111_opy_, cls).__new__(cls)
      cls.instance.bstack11l11111ll1_opy_()
    return cls.instance
  def bstack11l11111ll1_opy_(self):
    try:
      with open(self.bstack11l1111l11l_opy_, bstack11l11_opy_ (u"ࠫࡷ࠭᤺")) as bstack1ll1l1ll1l_opy_:
        bstack11l11111l1l_opy_ = bstack1ll1l1ll1l_opy_.read()
        data = json.loads(bstack11l11111l1l_opy_)
        if bstack11l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ᤻ࠧ") in data:
          self.bstack11l1111ll1l_opy_(data[bstack11l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᤼")])
        if bstack11l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ᤽") in data:
          self.bstack1l111l111_opy_(data[bstack11l11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᤾")])
        if bstack11l11_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᤿") in data:
          self.bstack11l11111lll_opy_(data[bstack11l11_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᥀")])
    except:
      pass
  def bstack11l11111lll_opy_(self, bstack11l111ll11l_opy_):
    if bstack11l111ll11l_opy_ != None:
      self.bstack11l111ll11l_opy_ = bstack11l111ll11l_opy_
  def bstack1l111l111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11l11_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ᥁"),bstack11l11_opy_ (u"ࠬ࠭᥂"))
      self.bstack1l11llll_opy_ = scripts.get(bstack11l11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪ᥃"),bstack11l11_opy_ (u"ࠧࠨ᥄"))
      self.bstack11l11l11ll_opy_ = scripts.get(bstack11l11_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬ᥅"),bstack11l11_opy_ (u"ࠩࠪ᥆"))
      self.bstack11l1111ll11_opy_ = scripts.get(bstack11l11_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨ᥇"),bstack11l11_opy_ (u"ࠫࠬ᥈"))
  def bstack11l1111ll1l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l1111l11l_opy_, bstack11l11_opy_ (u"ࠬࡽࠧ᥉")) as file:
        json.dump({
          bstack11l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣ᥊"): self.commands_to_wrap,
          bstack11l11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣ᥋"): {
            bstack11l11_opy_ (u"ࠣࡵࡦࡥࡳࠨ᥌"): self.perform_scan,
            bstack11l11_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨ᥍"): self.bstack1l11llll_opy_,
            bstack11l11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢ᥎"): self.bstack11l11l11ll_opy_,
            bstack11l11_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤ᥏"): self.bstack11l1111ll11_opy_
          },
          bstack11l11_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤᥐ"): self.bstack11l111ll11l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᥑ").format(e))
      pass
  def bstack1lll1l1ll_opy_(self, command_name):
    try:
      return any(command.get(bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᥒ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l1lll111l_opy_ = bstack11l1111l111_opy_()