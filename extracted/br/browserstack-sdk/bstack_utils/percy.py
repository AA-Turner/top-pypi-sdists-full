# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack111111ll1_opy_, bstack1l1ll1111_opy_
from bstack_utils.measure import measure
class bstack11lll1ll1_opy_:
  working_dir = os.getcwd()
  bstack1111111ll_opy_ = False
  config = {}
  bstack11l1l11l1ll_opy_ = bstack1llllll_opy_ (u"ࠪࠫᲁ")
  binary_path = bstack1llllll_opy_ (u"ࠫࠬᲂ")
  bstack111lll1l111_opy_ = bstack1llllll_opy_ (u"ࠬ࠭ᲃ")
  bstack1l1lll1111_opy_ = False
  bstack111llll11ll_opy_ = None
  bstack111lll111l1_opy_ = {}
  bstack111lll1l1l1_opy_ = 300
  bstack111llllllll_opy_ = False
  logger = None
  bstack11l111111l1_opy_ = False
  bstack11l1lll1l_opy_ = False
  percy_build_id = None
  bstack111lll1l11l_opy_ = bstack1llllll_opy_ (u"࠭ࠧᲄ")
  bstack111ll1l1111_opy_ = {
    bstack1llllll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᲅ") : 1,
    bstack1llllll_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩᲆ") : 2,
    bstack1llllll_opy_ (u"ࠩࡨࡨ࡬࡫ࠧᲇ") : 3,
    bstack1llllll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪᲈ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll11lll1_opy_(self):
    bstack111lll1111l_opy_ = bstack1llllll_opy_ (u"ࠫࠬᲉ")
    bstack111llll1111_opy_ = sys.platform
    bstack111ll1l1l11_opy_ = bstack1llllll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᲊ")
    if re.match(bstack1llllll_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨ᲋"), bstack111llll1111_opy_) != None:
      bstack111lll1111l_opy_ = bstack11ll1ll1ll1_opy_ + bstack1llllll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣ᲌")
      self.bstack111lll1l11l_opy_ = bstack1llllll_opy_ (u"ࠨ࡯ࡤࡧࠬ᲍")
    elif re.match(bstack1llllll_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢ᲎"), bstack111llll1111_opy_) != None:
      bstack111lll1111l_opy_ = bstack11ll1ll1ll1_opy_ + bstack1llllll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦ᲏")
      bstack111ll1l1l11_opy_ = bstack1llllll_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢᲐ")
      self.bstack111lll1l11l_opy_ = bstack1llllll_opy_ (u"ࠬࡽࡩ࡯ࠩᲑ")
    else:
      bstack111lll1111l_opy_ = bstack11ll1ll1ll1_opy_ + bstack1llllll_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤᲒ")
      self.bstack111lll1l11l_opy_ = bstack1llllll_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭Დ")
    return bstack111lll1111l_opy_, bstack111ll1l1l11_opy_
  def bstack111llll1ll1_opy_(self):
    try:
      bstack111ll1llll1_opy_ = [os.path.join(expanduser(bstack1llllll_opy_ (u"ࠣࢀࠥᲔ")), bstack1llllll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᲕ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111ll1llll1_opy_:
        if(self.bstack111llll111l_opy_(path)):
          return path
      raise bstack1llllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᲖ")
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨᲗ").format(e))
  def bstack111llll111l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111lll1l1ll_opy_(self, bstack111lll111ll_opy_):
    return os.path.join(bstack111lll111ll_opy_, self.bstack11l1l11l1ll_opy_ + bstack1llllll_opy_ (u"ࠧ࠴ࡥࡵࡣࡪࠦᲘ"))
  def bstack11l1111111l_opy_(self, bstack111lll111ll_opy_, bstack11l111111ll_opy_):
    if not bstack11l111111ll_opy_: return
    try:
      bstack111ll1lll1l_opy_ = self.bstack111lll1l1ll_opy_(bstack111lll111ll_opy_)
      with open(bstack111ll1lll1l_opy_, bstack1llllll_opy_ (u"ࠨࡷࠣᲙ")) as f:
        f.write(bstack11l111111ll_opy_)
        self.logger.debug(bstack1llllll_opy_ (u"ࠢࡔࡣࡹࡩࡩࠦ࡮ࡦࡹࠣࡉ࡙ࡧࡧࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠦᲚ"))
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡷ࡬ࡪࠦࡥࡵࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᲛ").format(e))
  def bstack111llll1l1l_opy_(self, bstack111lll111ll_opy_):
    try:
      bstack111ll1lll1l_opy_ = self.bstack111lll1l1ll_opy_(bstack111lll111ll_opy_)
      if os.path.exists(bstack111ll1lll1l_opy_):
        with open(bstack111ll1lll1l_opy_, bstack1llllll_opy_ (u"ࠤࡵࠦᲜ")) as f:
          bstack11l111111ll_opy_ = f.read().strip()
          return bstack11l111111ll_opy_ if bstack11l111111ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡰࡴࡧࡤࡪࡰࡪࠤࡊ࡚ࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᲝ").format(e))
  def bstack111lllllll1_opy_(self, bstack111lll111ll_opy_, bstack111lll1111l_opy_):
    bstack111ll11llll_opy_ = self.bstack111llll1l1l_opy_(bstack111lll111ll_opy_)
    if bstack111ll11llll_opy_:
      try:
        bstack111ll1lllll_opy_ = self.bstack11l1111l11l_opy_(bstack111ll11llll_opy_, bstack111lll1111l_opy_)
        if not bstack111ll1lllll_opy_:
          self.logger.debug(bstack1llllll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡸࠦࡵࡱࠢࡷࡳࠥࡪࡡࡵࡧࠣࠬࡊ࡚ࡡࡨࠢࡸࡲࡨ࡮ࡡ࡯ࡩࡨࡨ࠮ࠨᲞ"))
          return True
        self.logger.debug(bstack1llllll_opy_ (u"ࠧࡔࡥࡸࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡺࡶࡤࡢࡶࡨࠦᲟ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1llllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡲࡶࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᲠ").format(e))
    return False
  def bstack11l1111l11l_opy_(self, bstack111ll11llll_opy_, bstack111lll1111l_opy_):
    try:
      headers = {
        bstack1llllll_opy_ (u"ࠢࡊࡨ࠰ࡒࡴࡴࡥ࠮ࡏࡤࡸࡨ࡮ࠢᲡ"): bstack111ll11llll_opy_
      }
      response = bstack1l1ll1111_opy_(bstack1llllll_opy_ (u"ࠨࡉࡈࡘࠬᲢ"), bstack111lll1111l_opy_, {}, {bstack1llllll_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥᲣ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1llllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠻ࠢࡾࢁࠧᲤ").format(e))
  @measure(event_name=EVENTS.bstack11ll1l1ll1l_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
  def bstack111ll1l11l1_opy_(self, bstack111lll1111l_opy_, bstack111ll1l1l11_opy_):
    try:
      bstack111ll1l1lll_opy_ = self.bstack111llll1ll1_opy_()
      bstack111ll1l111l_opy_ = os.path.join(bstack111ll1l1lll_opy_, bstack1llllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧᲥ"))
      bstack111ll1ll1l1_opy_ = os.path.join(bstack111ll1l1lll_opy_, bstack111ll1l1l11_opy_)
      if self.bstack111lllllll1_opy_(bstack111ll1l1lll_opy_, bstack111lll1111l_opy_):
        if os.path.exists(bstack111ll1ll1l1_opy_):
          self.logger.info(bstack1llllll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᲦ").format(bstack111ll1ll1l1_opy_))
          return bstack111ll1ll1l1_opy_
        if os.path.exists(bstack111ll1l111l_opy_):
          self.logger.info(bstack1llllll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦᲧ").format(bstack111ll1l111l_opy_))
          return self.bstack11l1111l111_opy_(bstack111ll1l111l_opy_, bstack111ll1l1l11_opy_)
      self.logger.info(bstack1llllll_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧᲨ").format(bstack111lll1111l_opy_))
      response = bstack1l1ll1111_opy_(bstack1llllll_opy_ (u"ࠨࡉࡈࡘࠬᲩ"), bstack111lll1111l_opy_, {}, {})
      if response.status_code == 200:
        bstack111ll1ll11l_opy_ = response.headers.get(bstack1llllll_opy_ (u"ࠤࡈࡘࡦ࡭ࠢᲪ"), bstack1llllll_opy_ (u"ࠥࠦᲫ"))
        if bstack111ll1ll11l_opy_:
          self.bstack11l1111111l_opy_(bstack111ll1l1lll_opy_, bstack111ll1ll11l_opy_)
        with open(bstack111ll1l111l_opy_, bstack1llllll_opy_ (u"ࠫࡼࡨࠧᲬ")) as file:
          file.write(response.content)
        self.logger.info(bstack1llllll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥᲭ").format(bstack111ll1l111l_opy_))
        return self.bstack11l1111l111_opy_(bstack111ll1l111l_opy_, bstack111ll1l1l11_opy_)
      else:
        raise(bstack1llllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤᲮ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᲯ").format(e))
  def bstack11l11111ll1_opy_(self, bstack111lll1111l_opy_, bstack111ll1l1l11_opy_):
    try:
      retry = 2
      bstack111ll1ll1l1_opy_ = None
      bstack111llll1lll_opy_ = False
      while retry > 0:
        bstack111ll1ll1l1_opy_ = self.bstack111ll1l11l1_opy_(bstack111lll1111l_opy_, bstack111ll1l1l11_opy_)
        bstack111llll1lll_opy_ = self.bstack111lll11ll1_opy_(bstack111lll1111l_opy_, bstack111ll1l1l11_opy_, bstack111ll1ll1l1_opy_)
        if bstack111llll1lll_opy_:
          break
        retry -= 1
      return bstack111ll1ll1l1_opy_, bstack111llll1lll_opy_
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧᲰ").format(e))
    return bstack111ll1ll1l1_opy_, False
  def bstack111lll11ll1_opy_(self, bstack111lll1111l_opy_, bstack111ll1l1l11_opy_, bstack111ll1ll1l1_opy_, bstack111lllll1l1_opy_ = 0):
    if bstack111lllll1l1_opy_ > 1:
      return False
    if bstack111ll1ll1l1_opy_ == None or os.path.exists(bstack111ll1ll1l1_opy_) == False:
      self.logger.warn(bstack1llllll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᲱ"))
      return False
    bstack111lllll111_opy_ = bstack1llllll_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣᲲ")
    command = bstack1llllll_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᲳ").format(bstack111ll1ll1l1_opy_)
    bstack111lll11lll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lllll111_opy_, bstack111lll11lll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1llllll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᲴ"))
      return False
  def bstack11l1111l111_opy_(self, bstack111ll1l111l_opy_, bstack111ll1l1l11_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll1l111l_opy_)
      shutil.unpack_archive(bstack111ll1l111l_opy_, working_dir)
      bstack111ll1ll1l1_opy_ = os.path.join(working_dir, bstack111ll1l1l11_opy_)
      os.chmod(bstack111ll1ll1l1_opy_, 0o755)
      return bstack111ll1ll1l1_opy_
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᲵ"))
  def bstack111ll1ll1ll_opy_(self):
    try:
      bstack111lll1lll1_opy_ = self.config.get(bstack1llllll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ჶ"))
      bstack111ll1ll1ll_opy_ = bstack111lll1lll1_opy_ or (bstack111lll1lll1_opy_ is None and self.bstack1111111ll_opy_)
      if not bstack111ll1ll1ll_opy_ or self.config.get(bstack1llllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᲷ"), None) not in bstack11ll1l11l1l_opy_:
        return False
      self.bstack1l1lll1111_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᲸ").format(e))
  def bstack111lll11111_opy_(self):
    try:
      bstack111lll11111_opy_ = self.percy_capture_mode
      return bstack111lll11111_opy_
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᲹ").format(e))
  def init(self, bstack1111111ll_opy_, config, logger):
    self.bstack1111111ll_opy_ = bstack1111111ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll1ll1ll_opy_():
      return
    self.bstack111lll111l1_opy_ = config.get(bstack1llllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᲺ"), {})
    self.percy_capture_mode = config.get(bstack1llllll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ᲻"))
    try:
      bstack111lll1111l_opy_, bstack111ll1l1l11_opy_ = self.bstack111ll11lll1_opy_()
      self.bstack11l1l11l1ll_opy_ = bstack111ll1l1l11_opy_
      bstack111ll1ll1l1_opy_, bstack111llll1lll_opy_ = self.bstack11l11111ll1_opy_(bstack111lll1111l_opy_, bstack111ll1l1l11_opy_)
      if bstack111llll1lll_opy_:
        self.binary_path = bstack111ll1ll1l1_opy_
        thread = Thread(target=self.bstack111lll1llll_opy_)
        thread.start()
      else:
        self.bstack11l111111l1_opy_ = True
        self.logger.error(bstack1llllll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥ᲼").format(bstack111ll1ll1l1_opy_))
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᲽ").format(e))
  def bstack11l11111111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1llllll_opy_ (u"ࠨ࡮ࡲ࡫ࠬᲾ"), bstack1llllll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬᲿ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1llllll_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢ᳀").format(logfile))
      self.bstack111lll1l111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ᳁").format(e))
  @measure(event_name=EVENTS.bstack11ll1ll1l11_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
  def bstack111lll1llll_opy_(self):
    bstack111lll11l11_opy_ = self.bstack111ll11ll11_opy_()
    if bstack111lll11l11_opy_ == None:
      self.bstack11l111111l1_opy_ = True
      self.logger.error(bstack1llllll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣ᳂"))
      return False
    command_args = [bstack1llllll_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢ᳃") if self.bstack1111111ll_opy_ else bstack1llllll_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫ᳄")]
    bstack11l111l1ll1_opy_ = self.bstack11l11111l11_opy_()
    if bstack11l111l1ll1_opy_ != None:
      command_args.append(bstack1llllll_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢ᳅").format(bstack11l111l1ll1_opy_))
    env = os.environ.copy()
    env[bstack1llllll_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢ᳆")] = bstack111lll11l11_opy_
    env[bstack1llllll_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥ᳇")] = os.environ.get(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᳈"), bstack1llllll_opy_ (u"ࠬ࠭᳉"))
    bstack111lllll1ll_opy_ = [self.binary_path]
    self.bstack11l11111111_opy_()
    self.bstack111llll11ll_opy_ = self.bstack11l1111l1l1_opy_(bstack111lllll1ll_opy_ + command_args, env)
    self.logger.debug(bstack1llllll_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢ᳊"))
    bstack111lllll1l1_opy_ = 0
    while self.bstack111llll11ll_opy_.poll() == None:
      bstack11l11111l1l_opy_ = self.bstack111lll1ll1l_opy_()
      if bstack11l11111l1l_opy_:
        self.logger.debug(bstack1llllll_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥ᳋"))
        self.bstack111llllllll_opy_ = True
        return True
      bstack111lllll1l1_opy_ += 1
      self.logger.debug(bstack1llllll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦ᳌").format(bstack111lllll1l1_opy_))
      time.sleep(2)
    self.logger.error(bstack1llllll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢ᳍").format(bstack111lllll1l1_opy_))
    self.bstack11l111111l1_opy_ = True
    return False
  def bstack111lll1ll1l_opy_(self, bstack111lllll1l1_opy_ = 0):
    if bstack111lllll1l1_opy_ > 10:
      return False
    try:
      bstack111llll1l11_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪ᳎"), bstack1llllll_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬ᳏"))
      bstack111lll1ll11_opy_ = bstack111llll1l11_opy_ + bstack11ll1l1l1l1_opy_
      response = requests.get(bstack111lll1ll11_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1llllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫ᳐"), {}).get(bstack1llllll_opy_ (u"࠭ࡩࡥࠩ᳑"), None)
      return True
    except:
      self.logger.debug(bstack1llllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧ᳒"))
      return False
  def bstack111ll11ll11_opy_(self):
    bstack111ll1l1l1l_opy_ = bstack1llllll_opy_ (u"ࠨࡣࡳࡴࠬ᳓") if self.bstack1111111ll_opy_ else bstack1llllll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨ᳔ࠫ")
    bstack111llllll1l_opy_ = bstack1llllll_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨ᳕") if self.config.get(bstack1llllll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ᳖ࠪ")) is None else True
    bstack11l1l1ll1l1_opy_ = bstack1llllll_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨ᳗").format(self.config[bstack1llllll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨ᳘ࠫ")], bstack111ll1l1l1l_opy_, bstack111llllll1l_opy_)
    if self.percy_capture_mode:
      bstack11l1l1ll1l1_opy_ += bstack1llllll_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤ᳙").format(self.percy_capture_mode)
    uri = bstack111111ll1_opy_(bstack11l1l1ll1l1_opy_)
    try:
      response = bstack1l1ll1111_opy_(bstack1llllll_opy_ (u"ࠨࡉࡈࡘࠬ᳚"), uri, {}, {bstack1llllll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ᳛"): (self.config[bstack1llllll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ᳜ࠬ")], self.config[bstack1llllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ᳝ࠧ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l1lll1111_opy_ = data.get(bstack1llllll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ᳞࠭"))
        self.percy_capture_mode = data.get(bstack1llllll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨ᳟ࠫ"))
        os.environ[bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬ᳠")] = str(self.bstack1l1lll1111_opy_)
        os.environ[bstack1llllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬ᳡")] = str(self.percy_capture_mode)
        if bstack111llllll1l_opy_ == bstack1llllll_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ᳢ࠧ") and str(self.bstack1l1lll1111_opy_).lower() == bstack1llllll_opy_ (u"ࠥࡸࡷࡻࡥ᳣ࠣ"):
          self.bstack11l1lll1l_opy_ = True
        if bstack1llllll_opy_ (u"ࠦࡹࡵ࡫ࡦࡰ᳤ࠥ") in data:
          return data[bstack1llllll_opy_ (u"ࠧࡺ࡯࡬ࡧࡱ᳥ࠦ")]
        else:
          raise bstack1llllll_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ᳦࠭").format(data)
      else:
        raise bstack1llllll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃ᳧ࠢ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤ᳨").format(e))
  def bstack11l11111l11_opy_(self):
    bstack111llll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1llllll_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧᳩ"))
    try:
      if bstack1llllll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᳪ") not in self.bstack111lll111l1_opy_:
        self.bstack111lll111l1_opy_[bstack1llllll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᳫ")] = 2
      with open(bstack111llll11l1_opy_, bstack1llllll_opy_ (u"ࠬࡽࠧᳬ")) as fp:
        json.dump(self.bstack111lll111l1_opy_, fp)
      return bstack111llll11l1_opy_
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᳭").format(e))
  def bstack11l1111l1l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lll1l11l_opy_ == bstack1llllll_opy_ (u"ࠧࡸ࡫ࡱࠫᳮ"):
        bstack11l11111lll_opy_ = [bstack1llllll_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩᳯ"), bstack1llllll_opy_ (u"ࠩ࠲ࡧࠬᳰ")]
        cmd = bstack11l11111lll_opy_ + cmd
      cmd = bstack1llllll_opy_ (u"ࠪࠤࠬᳱ").join(cmd)
      self.logger.debug(bstack1llllll_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣᳲ").format(cmd))
      with open(self.bstack111lll1l111_opy_, bstack1llllll_opy_ (u"ࠧࡧࠢᳳ")) as bstack111ll1l1ll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111ll1l1ll1_opy_, text=True, stderr=bstack111ll1l1ll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l111111l1_opy_ = True
      self.logger.error(bstack1llllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ᳴").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111llllllll_opy_:
        self.logger.info(bstack1llllll_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣᳵ"))
        cmd = [self.binary_path, bstack1llllll_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦᳶ")]
        self.bstack11l1111l1l1_opy_(cmd)
        self.bstack111llllllll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ᳷").format(cmd, e))
  def bstack1l11ll1l_opy_(self):
    if not self.bstack1l1lll1111_opy_:
      return
    try:
      bstack111ll1ll111_opy_ = 0
      while not self.bstack111llllllll_opy_ and bstack111ll1ll111_opy_ < self.bstack111lll1l1l1_opy_:
        if self.bstack11l111111l1_opy_:
          self.logger.info(bstack1llllll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣ᳸"))
          return
        time.sleep(1)
        bstack111ll1ll111_opy_ += 1
      os.environ[bstack1llllll_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪ᳹")] = str(self.bstack111ll11ll1l_opy_())
      self.logger.info(bstack1llllll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨᳺ"))
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ᳻").format(e))
  def bstack111ll11ll1l_opy_(self):
    if self.bstack1111111ll_opy_:
      return
    try:
      bstack111lllll11l_opy_ = [platform[bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᳼")].lower() for platform in self.config.get(bstack1llllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᳽"), [])]
      bstack11l1111l1ll_opy_ = sys.maxsize
      bstack111ll1lll11_opy_ = bstack1llllll_opy_ (u"ࠩࠪ᳾")
      for browser in bstack111lllll11l_opy_:
        if browser in self.bstack111ll1l1111_opy_:
          bstack111lll11l1l_opy_ = self.bstack111ll1l1111_opy_[browser]
        if bstack111lll11l1l_opy_ < bstack11l1111l1ll_opy_:
          bstack11l1111l1ll_opy_ = bstack111lll11l1l_opy_
          bstack111ll1lll11_opy_ = browser
      return bstack111ll1lll11_opy_
    except Exception as e:
      self.logger.error(bstack1llllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ᳿").format(e))
  @classmethod
  def bstack1lll11111l_opy_(self):
    return os.getenv(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᴀ"), bstack1llllll_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫᴁ")).lower()
  @classmethod
  def bstack1111lll11_opy_(self):
    return os.getenv(bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᴂ"), bstack1llllll_opy_ (u"ࠧࠨᴃ"))
  @classmethod
  def bstack1l1ll1l1ll1_opy_(cls, value):
    cls.bstack11l1lll1l_opy_ = value
  @classmethod
  def bstack111llllll11_opy_(cls):
    return cls.bstack11l1lll1l_opy_
  @classmethod
  def bstack1l1ll1l1l1l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111ll1l11ll_opy_(cls):
    return cls.percy_build_id