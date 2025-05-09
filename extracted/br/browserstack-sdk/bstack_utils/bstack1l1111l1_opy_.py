# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
import json
from bstack_utils.bstack1l11lll1_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1l1ll1_opy_(object):
  bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstack11lll_opy_ (u"ࠩࢁࠫᘽ")), bstack11lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᘾ"))
  bstack11lll1l1l11_opy_ = os.path.join(bstack111l1111l_opy_, bstack11lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫᘿ"))
  commands_to_wrap = None
  perform_scan = None
  bstack111l1ll1_opy_ = None
  bstack1l1ll111ll_opy_ = None
  bstack11lll1ll1ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11lll_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧᙀ")):
      cls.instance = super(bstack11lll1l1ll1_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1l11ll_opy_()
    return cls.instance
  def bstack11lll1l11ll_opy_(self):
    try:
      with open(self.bstack11lll1l1l11_opy_, bstack11lll_opy_ (u"࠭ࡲࠨᙁ")) as bstack11ll1ll1l_opy_:
        bstack11lll1l1l1l_opy_ = bstack11ll1ll1l_opy_.read()
        data = json.loads(bstack11lll1l1l1l_opy_)
        if bstack11lll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᙂ") in data:
          self.bstack11llll1ll1l_opy_(data[bstack11lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᙃ")])
        if bstack11lll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᙄ") in data:
          self.bstack11ll11llll_opy_(data[bstack11lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᙅ")])
    except:
      pass
  def bstack11ll11llll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11lll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᙆ"),bstack11lll_opy_ (u"ࠬ࠭ᙇ"))
      self.bstack111l1ll1_opy_ = scripts.get(bstack11lll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᙈ"),bstack11lll_opy_ (u"ࠧࠨᙉ"))
      self.bstack1l1ll111ll_opy_ = scripts.get(bstack11lll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᙊ"),bstack11lll_opy_ (u"ࠩࠪᙋ"))
      self.bstack11lll1ll1ll_opy_ = scripts.get(bstack11lll_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᙌ"),bstack11lll_opy_ (u"ࠫࠬᙍ"))
  def bstack11llll1ll1l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1l1l11_opy_, bstack11lll_opy_ (u"ࠬࡽࠧᙎ")) as file:
        json.dump({
          bstack11lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣᙏ"): self.commands_to_wrap,
          bstack11lll_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣᙐ"): {
            bstack11lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᙑ"): self.perform_scan,
            bstack11lll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᙒ"): self.bstack111l1ll1_opy_,
            bstack11lll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᙓ"): self.bstack1l1ll111ll_opy_,
            bstack11lll_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᙔ"): self.bstack11lll1ll1ll_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥᙕ").format(e))
      pass
  def bstack11l1111ll_opy_(self, bstack1ll1ll1ll11_opy_):
    try:
      return any(command.get(bstack11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙖ")) == bstack1ll1ll1ll11_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l1111l1_opy_ = bstack11lll1l1ll1_opy_()