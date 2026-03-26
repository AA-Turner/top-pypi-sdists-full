# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111l1llll11_opy_(object):
  bstack1ll11ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠧࡿࠩᮂ")), bstack1ll1lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᮃ"))
  bstack111l1lllll1_opy_ = os.path.join(bstack1ll11ll1ll_opy_, bstack1ll1lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᮄ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack111ll111l11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬᮅ")):
      cls.instance = super(bstack111l1llll11_opy_, cls).__new__(cls)
      cls.instance.bstack111l1lll1l1_opy_()
    return cls.instance
  def bstack111l1lll1l1_opy_(self):
    try:
      with open(self.bstack111l1lllll1_opy_, bstack1ll1lll_opy_ (u"ࠫࡷ࠭ᮆ")) as bstack1llll1lll_opy_:
        bstack111l1lll1ll_opy_ = bstack1llll1lll_opy_.read()
        data = json.loads(bstack111l1lll1ll_opy_)
        if bstack1ll1lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᮇ") in data:
          self.bstack111ll1llll1_opy_(data[bstack1ll1lll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᮈ")])
        if bstack1ll1lll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࡕࡱࡕࡹࡳ࠭ᮉ") in data:
          self.bstack111l1llllll_opy_(data[bstack1ll1lll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࡖࡲࡖࡺࡴࠧᮊ")])
        if bstack1ll1lll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᮋ") in data:
          self.bstack111lll1111_opy_(data[bstack1ll1lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᮌ")])
        if bstack1ll1lll_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᮍ") in data:
          self.bstack111l1llll1l_opy_(data[bstack1ll1lll_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᮎ")])
    except:
      pass
  def bstack111l1llll1l_opy_(self, bstack111ll111l11_opy_):
    if bstack111ll111l11_opy_ != None:
      self.bstack111ll111l11_opy_ = bstack111ll111l11_opy_
  def bstack111lll1111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll1lll_opy_ (u"࠭ࡳࡤࡣࡱࠫᮏ"),bstack1ll1lll_opy_ (u"ࠧࠨᮐ"))
      self.get_results = scripts.get(bstack1ll1lll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᮑ"),bstack1ll1lll_opy_ (u"ࠩࠪᮒ"))
      self.get_results_summary = scripts.get(bstack1ll1lll_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᮓ"),bstack1ll1lll_opy_ (u"ࠫࠬᮔ"))
      self.save_test_results = scripts.get(bstack1ll1lll_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᮕ"),bstack1ll1lll_opy_ (u"࠭ࠧᮖ"))
  def bstack111ll1llll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack111l1llllll_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack111l1lllll1_opy_, bstack1ll1lll_opy_ (u"ࠧࡸࠩᮗ")) as file:
        json.dump({
          bstack1ll1lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥᮘ"): self.commands_to_wrap,
          bstack1ll1lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࡗࡳࡗࡻ࡮ࠣᮙ"): self.scripts_to_run,
          bstack1ll1lll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦᮚ"): {
            bstack1ll1lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᮛ"): self.perform_scan,
            bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᮜ"): self.get_results,
            bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᮝ"): self.get_results_summary,
            bstack1ll1lll_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᮞ"): self.save_test_results
          },
          bstack1ll1lll_opy_ (u"ࠣࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠧᮟ"): self.bstack111ll111l11_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᮠ").format(e))
      pass
  def bstack11l11llll_opy_(self, command_name):
    try:
      return any(command.get(bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨᮡ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack111l1llll11_opy_()