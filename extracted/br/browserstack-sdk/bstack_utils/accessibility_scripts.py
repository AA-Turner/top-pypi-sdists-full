# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111lll11111_opy_(object):
  bstack111lll11ll_opy_ = os.path.join(os.path.expanduser(bstack1111l_opy_ (u"ࠨࢀࠪᬚ")), bstack1111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᬛ"))
  bstack111lll1111l_opy_ = os.path.join(bstack111lll11ll_opy_, bstack1111l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪᬜ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack11l111111ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1111l_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭ᬝ")):
      cls.instance = super(bstack111lll11111_opy_, cls).__new__(cls)
      cls.instance.bstack111lll111ll_opy_()
    return cls.instance
  def bstack111lll111ll_opy_(self):
    try:
      with open(self.bstack111lll1111l_opy_, bstack1111l_opy_ (u"ࠬࡸࠧᬞ")) as bstack111ll1ll1l_opy_:
        bstack111lll111l1_opy_ = bstack111ll1ll1l_opy_.read()
        data = json.loads(bstack111lll111l1_opy_)
        if bstack1111l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᬟ") in data:
          self.bstack11l11111l1l_opy_(data[bstack1111l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᬠ")])
        if bstack1111l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࡖࡲࡖࡺࡴࠧᬡ") in data:
          self.bstack111lll11l11_opy_(data[bstack1111l_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࡗࡳࡗࡻ࡮ࠨᬢ")])
        if bstack1111l_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᬣ") in data:
          self.bstack1llll11ll1_opy_(data[bstack1111l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᬤ")])
        if bstack1111l_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬥ") in data:
          self.bstack111ll1lllll_opy_(data[bstack1111l_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᬦ")])
    except:
      pass
  def bstack111ll1lllll_opy_(self, bstack11l111111ll_opy_):
    if bstack11l111111ll_opy_ != None:
      self.bstack11l111111ll_opy_ = bstack11l111111ll_opy_
  def bstack1llll11ll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1111l_opy_ (u"ࠧࡴࡥࡤࡲࠬᬧ"),bstack1111l_opy_ (u"ࠨࠩᬨ"))
      self.get_results = scripts.get(bstack1111l_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ᬩ"),bstack1111l_opy_ (u"ࠪࠫᬪ"))
      self.get_results_summary = scripts.get(bstack1111l_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨᬫ"),bstack1111l_opy_ (u"ࠬ࠭ᬬ"))
      self.save_test_results = scripts.get(bstack1111l_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᬭ"),bstack1111l_opy_ (u"ࠧࠨᬮ"))
  def bstack11l11111l1l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack111lll11l11_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack111lll1111l_opy_, bstack1111l_opy_ (u"ࠨࡹࠪᬯ")) as file:
        json.dump({
          bstack1111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦᬰ"): self.commands_to_wrap,
          bstack1111l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࡘࡴࡘࡵ࡯ࠤᬱ"): self.scripts_to_run,
          bstack1111l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᬲ"): {
            bstack1111l_opy_ (u"ࠧࡹࡣࡢࡰࠥᬳ"): self.perform_scan,
            bstack1111l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵ᬴ࠥ"): self.get_results,
            bstack1111l_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᬵ"): self.get_results_summary,
            bstack1111l_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᬶ"): self.save_test_results
          },
          bstack1111l_opy_ (u"ࠤࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠨᬷ"): self.bstack11l111111ll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠣᬸ").format(e))
      pass
  def bstack11ll1l1l11_opy_(self, command_name):
    try:
      return any(command.get(bstack1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᬹ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack111lll11111_opy_()