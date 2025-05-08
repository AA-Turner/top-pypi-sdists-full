# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
import json
from bstack_utils.bstack1ll1l111l1_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1ll111_opy_(object):
  bstack1l1l11111_opy_ = os.path.join(os.path.expanduser(bstack1l1lll_opy_ (u"ࠩࢁࠫᘽ")), bstack1l1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᘾ"))
  bstack11lll1l1ll1_opy_ = os.path.join(bstack1l1l11111_opy_, bstack1l1lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫᘿ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll11lll1l_opy_ = None
  bstack111111l1_opy_ = None
  bstack11llll1lll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1lll_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧᙀ")):
      cls.instance = super(bstack11lll1ll111_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1l1lll_opy_()
    return cls.instance
  def bstack11lll1l1lll_opy_(self):
    try:
      with open(self.bstack11lll1l1ll1_opy_, bstack1l1lll_opy_ (u"࠭ࡲࠨᙁ")) as bstack11l1l111l_opy_:
        bstack11lll1l1l1l_opy_ = bstack11l1l111l_opy_.read()
        data = json.loads(bstack11lll1l1l1l_opy_)
        if bstack1l1lll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᙂ") in data:
          self.bstack11llll11l1l_opy_(data[bstack1l1lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᙃ")])
        if bstack1l1lll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᙄ") in data:
          self.bstack111llll11_opy_(data[bstack1l1lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᙅ")])
    except:
      pass
  def bstack111llll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᙆ"),bstack1l1lll_opy_ (u"ࠬ࠭ᙇ"))
      self.bstack1ll11lll1l_opy_ = scripts.get(bstack1l1lll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᙈ"),bstack1l1lll_opy_ (u"ࠧࠨᙉ"))
      self.bstack111111l1_opy_ = scripts.get(bstack1l1lll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᙊ"),bstack1l1lll_opy_ (u"ࠩࠪᙋ"))
      self.bstack11llll1lll1_opy_ = scripts.get(bstack1l1lll_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᙌ"),bstack1l1lll_opy_ (u"ࠫࠬᙍ"))
  def bstack11llll11l1l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1l1ll1_opy_, bstack1l1lll_opy_ (u"ࠬࡽࠧᙎ")) as file:
        json.dump({
          bstack1l1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᙏ"): self.commands_to_wrap,
          bstack1l1lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣᙐ"): {
            bstack1l1lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᙑ"): self.perform_scan,
            bstack1l1lll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᙒ"): self.bstack1ll11lll1l_opy_,
            bstack1l1lll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᙓ"): self.bstack111111l1_opy_,
            bstack1l1lll_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᙔ"): self.bstack11llll1lll1_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack1l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥᙕ").format(e))
      pass
  def bstack1ll11l1lll_opy_(self, bstack1ll1l11l111_opy_):
    try:
      return any(command.get(bstack1l1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙖ")) == bstack1ll1l11l111_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11ll11ll11_opy_ = bstack11lll1ll111_opy_()