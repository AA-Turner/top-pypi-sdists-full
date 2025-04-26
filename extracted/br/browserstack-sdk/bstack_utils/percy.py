# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
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
from bstack_utils.helper import bstack1111l111_opy_, bstack1l1lll11l_opy_
from bstack_utils.measure import measure
class bstack1l1l111lll_opy_:
  working_dir = os.getcwd()
  bstack11ll11l1l_opy_ = False
  config = {}
  bstack11l1ll11lll_opy_ = bstack1l11lll_opy_ (u"ࠨࠩ᱿")
  binary_path = bstack1l11lll_opy_ (u"ࠩࠪᲀ")
  bstack111ll1ll1l1_opy_ = bstack1l11lll_opy_ (u"ࠪࠫᲁ")
  bstack11111111l_opy_ = False
  bstack111llllll11_opy_ = None
  bstack111llll111l_opy_ = {}
  bstack111lllll111_opy_ = 300
  bstack111ll1ll11l_opy_ = False
  logger = None
  bstack111ll1l1l11_opy_ = False
  bstack1l1llllll_opy_ = False
  percy_build_id = None
  bstack111ll1lll11_opy_ = bstack1l11lll_opy_ (u"ࠫࠬᲂ")
  bstack111ll1lllll_opy_ = {
    bstack1l11lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᲃ") : 1,
    bstack1l11lll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᲄ") : 2,
    bstack1l11lll_opy_ (u"ࠧࡦࡦࡪࡩࠬᲅ") : 3,
    bstack1l11lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᲆ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111lll11ll1_opy_(self):
    bstack111lll1ll11_opy_ = bstack1l11lll_opy_ (u"ࠩࠪᲇ")
    bstack111ll1l111l_opy_ = sys.platform
    bstack11l1111l1ll_opy_ = bstack1l11lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᲈ")
    if re.match(bstack1l11lll_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᲉ"), bstack111ll1l111l_opy_) != None:
      bstack111lll1ll11_opy_ = bstack11ll11lllll_opy_ + bstack1l11lll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᲊ")
      self.bstack111ll1lll11_opy_ = bstack1l11lll_opy_ (u"࠭࡭ࡢࡥࠪ᲋")
    elif re.match(bstack1l11lll_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧ᲌"), bstack111ll1l111l_opy_) != None:
      bstack111lll1ll11_opy_ = bstack11ll11lllll_opy_ + bstack1l11lll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤ᲍")
      bstack11l1111l1ll_opy_ = bstack1l11lll_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧ᲎")
      self.bstack111ll1lll11_opy_ = bstack1l11lll_opy_ (u"ࠪࡻ࡮ࡴࠧ᲏")
    else:
      bstack111lll1ll11_opy_ = bstack11ll11lllll_opy_ + bstack1l11lll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᲐ")
      self.bstack111ll1lll11_opy_ = bstack1l11lll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᲑ")
    return bstack111lll1ll11_opy_, bstack11l1111l1ll_opy_
  def bstack111lll1l11l_opy_(self):
    try:
      bstack11l111111l1_opy_ = [os.path.join(expanduser(bstack1l11lll_opy_ (u"ࠨࡾࠣᲒ")), bstack1l11lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᲓ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l111111l1_opy_:
        if(self.bstack111ll1lll1l_opy_(path)):
          return path
      raise bstack1l11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᲔ")
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᲕ").format(e))
  def bstack111ll1lll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111llll11ll_opy_(self, bstack111lllll1l1_opy_):
    return os.path.join(bstack111lllll1l1_opy_, self.bstack11l1ll11lll_opy_ + bstack1l11lll_opy_ (u"ࠥ࠲ࡪࡺࡡࡨࠤᲖ"))
  def bstack111llllll1l_opy_(self, bstack111lllll1l1_opy_, bstack111llll1ll1_opy_):
    if not bstack111llll1ll1_opy_: return
    try:
      bstack111lll11l1l_opy_ = self.bstack111llll11ll_opy_(bstack111lllll1l1_opy_)
      with open(bstack111lll11l1l_opy_, bstack1l11lll_opy_ (u"ࠦࡼࠨᲗ")) as f:
        f.write(bstack111llll1ll1_opy_)
        self.logger.debug(bstack1l11lll_opy_ (u"࡙ࠧࡡࡷࡧࡧࠤࡳ࡫ࡷࠡࡇࡗࡥ࡬ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠤᲘ"))
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡵࡪࡨࠤࡪࡺࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᲙ").format(e))
  def bstack111ll11ll1l_opy_(self, bstack111lllll1l1_opy_):
    try:
      bstack111lll11l1l_opy_ = self.bstack111llll11ll_opy_(bstack111lllll1l1_opy_)
      if os.path.exists(bstack111lll11l1l_opy_):
        with open(bstack111lll11l1l_opy_, bstack1l11lll_opy_ (u"ࠢࡳࠤᲚ")) as f:
          bstack111llll1ll1_opy_ = f.read().strip()
          return bstack111llll1ll1_opy_ if bstack111llll1ll1_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡ࡮ࡲࡥࡩ࡯࡮ࡨࠢࡈࡘࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᲛ").format(e))
  def bstack111lll111ll_opy_(self, bstack111lllll1l1_opy_, bstack111lll1ll11_opy_):
    bstack11l1111l11l_opy_ = self.bstack111ll11ll1l_opy_(bstack111lllll1l1_opy_)
    if bstack11l1111l11l_opy_:
      try:
        bstack111ll1llll1_opy_ = self.bstack111ll1l1ll1_opy_(bstack11l1111l11l_opy_, bstack111lll1ll11_opy_)
        if not bstack111ll1llll1_opy_:
          self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡶࠤࡺࡶࠠࡵࡱࠣࡨࡦࡺࡥࠡࠪࡈࡘࡦ࡭ࠠࡶࡰࡦ࡬ࡦࡴࡧࡦࡦࠬࠦᲜ"))
          return True
        self.logger.debug(bstack1l11lll_opy_ (u"ࠥࡒࡪࡽࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡦࠤᲝ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l11lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡦࡰࡴࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠰ࠥࡻࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥᲞ").format(e))
    return False
  def bstack111ll1l1ll1_opy_(self, bstack11l1111l11l_opy_, bstack111lll1ll11_opy_):
    try:
      headers = {
        bstack1l11lll_opy_ (u"ࠧࡏࡦ࠮ࡐࡲࡲࡪ࠳ࡍࡢࡶࡦ࡬ࠧᲟ"): bstack11l1111l11l_opy_
      }
      response = bstack1l1lll11l_opy_(bstack1l11lll_opy_ (u"࠭ࡇࡆࡖࠪᲠ"), bstack111lll1ll11_opy_, {}, {bstack1l11lll_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣᲡ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l11lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸࡀࠠࡼࡿࠥᲢ").format(e))
  @measure(event_name=EVENTS.bstack11ll1l11ll1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
  def bstack111lll111l1_opy_(self, bstack111lll1ll11_opy_, bstack11l1111l1ll_opy_):
    try:
      bstack11l11111ll1_opy_ = self.bstack111lll1l11l_opy_()
      bstack111lll11l11_opy_ = os.path.join(bstack11l11111ll1_opy_, bstack1l11lll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᲣ"))
      bstack111lll11lll_opy_ = os.path.join(bstack11l11111ll1_opy_, bstack11l1111l1ll_opy_)
      if self.bstack111lll111ll_opy_(bstack11l11111ll1_opy_, bstack111lll1ll11_opy_):
        if os.path.exists(bstack111lll11lll_opy_):
          self.logger.info(bstack1l11lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᲤ").format(bstack111lll11lll_opy_))
          return bstack111lll11lll_opy_
        if os.path.exists(bstack111lll11l11_opy_):
          self.logger.info(bstack1l11lll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᲥ").format(bstack111lll11l11_opy_))
          return self.bstack11l1111l111_opy_(bstack111lll11l11_opy_, bstack11l1111l1ll_opy_)
      self.logger.info(bstack1l11lll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᲦ").format(bstack111lll1ll11_opy_))
      response = bstack1l1lll11l_opy_(bstack1l11lll_opy_ (u"࠭ࡇࡆࡖࠪᲧ"), bstack111lll1ll11_opy_, {}, {})
      if response.status_code == 200:
        bstack111ll1l11ll_opy_ = response.headers.get(bstack1l11lll_opy_ (u"ࠢࡆࡖࡤ࡫ࠧᲨ"), bstack1l11lll_opy_ (u"ࠣࠤᲩ"))
        if bstack111ll1l11ll_opy_:
          self.bstack111llllll1l_opy_(bstack11l11111ll1_opy_, bstack111ll1l11ll_opy_)
        with open(bstack111lll11l11_opy_, bstack1l11lll_opy_ (u"ࠩࡺࡦࠬᲪ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11lll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣᲫ").format(bstack111lll11l11_opy_))
        return self.bstack11l1111l111_opy_(bstack111lll11l11_opy_, bstack11l1111l1ll_opy_)
      else:
        raise(bstack1l11lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢᲬ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨᲭ").format(e))
  def bstack111ll1ll111_opy_(self, bstack111lll1ll11_opy_, bstack11l1111l1ll_opy_):
    try:
      retry = 2
      bstack111lll11lll_opy_ = None
      bstack111ll11lll1_opy_ = False
      while retry > 0:
        bstack111lll11lll_opy_ = self.bstack111lll111l1_opy_(bstack111lll1ll11_opy_, bstack11l1111l1ll_opy_)
        bstack111ll11lll1_opy_ = self.bstack11l11111l11_opy_(bstack111lll1ll11_opy_, bstack11l1111l1ll_opy_, bstack111lll11lll_opy_)
        if bstack111ll11lll1_opy_:
          break
        retry -= 1
      return bstack111lll11lll_opy_, bstack111ll11lll1_opy_
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥᲮ").format(e))
    return bstack111lll11lll_opy_, False
  def bstack11l11111l11_opy_(self, bstack111lll1ll11_opy_, bstack11l1111l1ll_opy_, bstack111lll11lll_opy_, bstack11l1111l1l1_opy_ = 0):
    if bstack11l1111l1l1_opy_ > 1:
      return False
    if bstack111lll11lll_opy_ == None or os.path.exists(bstack111lll11lll_opy_) == False:
      self.logger.warn(bstack1l11lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᲯ"))
      return False
    bstack11l111111ll_opy_ = bstack1l11lll_opy_ (u"ࠣࡠ࠱࠮ࡅࡶࡥࡳࡥࡼࡠ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠳ࡢࡤࠬ࠰࡟ࡨ࠰ࠨᲰ")
    command = bstack1l11lll_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲱ").format(bstack111lll11lll_opy_)
    bstack111llll11l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l111111ll_opy_, bstack111llll11l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤᲲ"))
      return False
  def bstack11l1111l111_opy_(self, bstack111lll11l11_opy_, bstack11l1111l1ll_opy_):
    try:
      working_dir = os.path.dirname(bstack111lll11l11_opy_)
      shutil.unpack_archive(bstack111lll11l11_opy_, working_dir)
      bstack111lll11lll_opy_ = os.path.join(working_dir, bstack11l1111l1ll_opy_)
      os.chmod(bstack111lll11lll_opy_, 0o755)
      return bstack111lll11lll_opy_
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᲳ"))
  def bstack111lll1ll1l_opy_(self):
    try:
      bstack111ll1l1l1l_opy_ = self.config.get(bstack1l11lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᲴ"))
      bstack111lll1ll1l_opy_ = bstack111ll1l1l1l_opy_ or (bstack111ll1l1l1l_opy_ is None and self.bstack11ll11l1l_opy_)
      if not bstack111lll1ll1l_opy_ or self.config.get(bstack1l11lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᲵ"), None) not in bstack11ll1l111ll_opy_:
        return False
      self.bstack11111111l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᲶ").format(e))
  def bstack111ll1l11l1_opy_(self):
    try:
      bstack111ll1l11l1_opy_ = self.percy_capture_mode
      return bstack111ll1l11l1_opy_
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᲷ").format(e))
  def init(self, bstack11ll11l1l_opy_, config, logger):
    self.bstack11ll11l1l_opy_ = bstack11ll11l1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111lll1ll1l_opy_():
      return
    self.bstack111llll111l_opy_ = config.get(bstack1l11lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᲸ"), {})
    self.percy_capture_mode = config.get(bstack1l11lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭Ჹ"))
    try:
      bstack111lll1ll11_opy_, bstack11l1111l1ll_opy_ = self.bstack111lll11ll1_opy_()
      self.bstack11l1ll11lll_opy_ = bstack11l1111l1ll_opy_
      bstack111lll11lll_opy_, bstack111ll11lll1_opy_ = self.bstack111ll1ll111_opy_(bstack111lll1ll11_opy_, bstack11l1111l1ll_opy_)
      if bstack111ll11lll1_opy_:
        self.binary_path = bstack111lll11lll_opy_
        thread = Thread(target=self.bstack11l1111111l_opy_)
        thread.start()
      else:
        self.bstack111ll1l1l11_opy_ = True
        self.logger.error(bstack1l11lll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣᲺ").format(bstack111lll11lll_opy_))
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᲻").format(e))
  def bstack111lll1l111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11lll_opy_ (u"࠭࡬ࡰࡩࠪ᲼"), bstack1l11lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩࠪᲽ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁࠧᲾ").format(logfile))
      self.bstack111ll1ll1l1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᲿ").format(e))
  @measure(event_name=EVENTS.bstack11ll1ll11ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
  def bstack11l1111111l_opy_(self):
    bstack111llllllll_opy_ = self.bstack11l11111l1l_opy_()
    if bstack111llllllll_opy_ == None:
      self.bstack111ll1l1l11_opy_ = True
      self.logger.error(bstack1l11lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨ᳀"))
      return False
    command_args = [bstack1l11lll_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧ᳁") if self.bstack11ll11l1l_opy_ else bstack1l11lll_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩ᳂")]
    bstack11l11l111l1_opy_ = self.bstack111ll11llll_opy_()
    if bstack11l11l111l1_opy_ != None:
      command_args.append(bstack1l11lll_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧ᳃").format(bstack11l11l111l1_opy_))
    env = os.environ.copy()
    env[bstack1l11lll_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧ᳄")] = bstack111llllllll_opy_
    env[bstack1l11lll_opy_ (u"ࠣࡖࡋࡣࡇ࡛ࡉࡍࡆࡢ࡙࡚ࡏࡄࠣ᳅")] = os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᳆"), bstack1l11lll_opy_ (u"ࠪࠫ᳇"))
    bstack111lll1111l_opy_ = [self.binary_path]
    self.bstack111lll1l111_opy_()
    self.bstack111llllll11_opy_ = self.bstack111ll1ll1ll_opy_(bstack111lll1111l_opy_ + command_args, env)
    self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧ᳈"))
    bstack11l1111l1l1_opy_ = 0
    while self.bstack111llllll11_opy_.poll() == None:
      bstack11l11111lll_opy_ = self.bstack111llll1l1l_opy_()
      if bstack11l11111lll_opy_:
        self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣ᳉"))
        self.bstack111ll1ll11l_opy_ = True
        return True
      bstack11l1111l1l1_opy_ += 1
      self.logger.debug(bstack1l11lll_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤ᳊").format(bstack11l1111l1l1_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧ᳋").format(bstack11l1111l1l1_opy_))
    self.bstack111ll1l1l11_opy_ = True
    return False
  def bstack111llll1l1l_opy_(self, bstack11l1111l1l1_opy_ = 0):
    if bstack11l1111l1l1_opy_ > 10:
      return False
    try:
      bstack111lll1lll1_opy_ = os.environ.get(bstack1l11lll_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨ᳌"), bstack1l11lll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪ᳍"))
      bstack111ll1l1111_opy_ = bstack111lll1lll1_opy_ + bstack11lll111111_opy_
      response = requests.get(bstack111ll1l1111_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l11lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࠩ᳎"), {}).get(bstack1l11lll_opy_ (u"ࠫ࡮ࡪࠧ᳏"), None)
      return True
    except:
      self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡲࡴࡩࠢࡦ࡬ࡪࡩ࡫ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ᳐"))
      return False
  def bstack11l11111l1l_opy_(self):
    bstack111lll1llll_opy_ = bstack1l11lll_opy_ (u"࠭ࡡࡱࡲࠪ᳑") if self.bstack11ll11l1l_opy_ else bstack1l11lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ᳒")
    bstack111ll1l1lll_opy_ = bstack1l11lll_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦ᳓") if self.config.get(bstack1l11lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ᳔")) is None else True
    bstack11l1ll11111_opy_ = bstack1l11lll_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠨࡳࡩࡷࡩࡹ࠾ࡽࢀ᳕ࠦ").format(self.config[bstack1l11lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ᳖ࠩ")], bstack111lll1llll_opy_, bstack111ll1l1lll_opy_)
    if self.percy_capture_mode:
      bstack11l1ll11111_opy_ += bstack1l11lll_opy_ (u"ࠧࠬࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࡁࢀࢃ᳗ࠢ").format(self.percy_capture_mode)
    uri = bstack1111l111_opy_(bstack11l1ll11111_opy_)
    try:
      response = bstack1l1lll11l_opy_(bstack1l11lll_opy_ (u"࠭ࡇࡆࡖ᳘ࠪ"), uri, {}, {bstack1l11lll_opy_ (u"ࠧࡢࡷࡷ࡬᳙ࠬ"): (self.config[bstack1l11lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᳚")], self.config[bstack1l11lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᳛")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11111111l_opy_ = data.get(bstack1l11lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶ᳜ࠫ"))
        self.percy_capture_mode = data.get(bstack1l11lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ᳝ࠩ"))
        os.environ[bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛᳞ࠪ")] = str(self.bstack11111111l_opy_)
        os.environ[bstack1l11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇ᳟ࠪ")] = str(self.percy_capture_mode)
        if bstack111ll1l1lll_opy_ == bstack1l11lll_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥ᳠") and str(self.bstack11111111l_opy_).lower() == bstack1l11lll_opy_ (u"ࠣࡶࡵࡹࡪࠨ᳡"):
          self.bstack1l1llllll_opy_ = True
        if bstack1l11lll_opy_ (u"ࠤࡷࡳࡰ࡫࡮᳢ࠣ") in data:
          return data[bstack1l11lll_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ᳣")]
        else:
          raise bstack1l11lll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ᳤ࠫ").format(data)
      else:
        raise bstack1l11lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁ᳥ࠧ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺ᳦ࠢ").format(e))
  def bstack111ll11llll_opy_(self):
    bstack11l11111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11lll_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰ᳧ࠥ"))
    try:
      if bstack1l11lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯᳨ࠩ") not in self.bstack111llll111l_opy_:
        self.bstack111llll111l_opy_[bstack1l11lll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪᳩ")] = 2
      with open(bstack11l11111111_opy_, bstack1l11lll_opy_ (u"ࠪࡻࠬᳪ")) as fp:
        json.dump(self.bstack111llll111l_opy_, fp)
      return bstack11l11111111_opy_
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᳫ").format(e))
  def bstack111ll1ll1ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll1lll11_opy_ == bstack1l11lll_opy_ (u"ࠬࡽࡩ࡯ࠩᳬ"):
        bstack111ll11ll11_opy_ = [bstack1l11lll_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫᳭ࠧ"), bstack1l11lll_opy_ (u"ࠧ࠰ࡥࠪᳮ")]
        cmd = bstack111ll11ll11_opy_ + cmd
      cmd = bstack1l11lll_opy_ (u"ࠨࠢࠪᳯ").join(cmd)
      self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨᳰ").format(cmd))
      with open(self.bstack111ll1ll1l1_opy_, bstack1l11lll_opy_ (u"ࠥࡥࠧᳱ")) as bstack111lllllll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111lllllll1_opy_, text=True, stderr=bstack111lllllll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111ll1l1l11_opy_ = True
      self.logger.error(bstack1l11lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᳲ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll1ll11l_opy_:
        self.logger.info(bstack1l11lll_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨᳳ"))
        cmd = [self.binary_path, bstack1l11lll_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤ᳴")]
        self.bstack111ll1ll1ll_opy_(cmd)
        self.bstack111ll1ll11l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᳵ").format(cmd, e))
  def bstack1l11l11ll_opy_(self):
    if not self.bstack11111111l_opy_:
      return
    try:
      bstack111llll1111_opy_ = 0
      while not self.bstack111ll1ll11l_opy_ and bstack111llll1111_opy_ < self.bstack111lllll111_opy_:
        if self.bstack111ll1l1l11_opy_:
          self.logger.info(bstack1l11lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨᳶ"))
          return
        time.sleep(1)
        bstack111llll1111_opy_ += 1
      os.environ[bstack1l11lll_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨ᳷")] = str(self.bstack111lll11111_opy_())
      self.logger.info(bstack1l11lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦ᳸"))
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ᳹").format(e))
  def bstack111lll11111_opy_(self):
    if self.bstack11ll11l1l_opy_:
      return
    try:
      bstack111lll1l1l1_opy_ = [platform[bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᳺ")].lower() for platform in self.config.get(bstack1l11lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᳻"), [])]
      bstack111lllll11l_opy_ = sys.maxsize
      bstack111llll1lll_opy_ = bstack1l11lll_opy_ (u"ࠧࠨ᳼")
      for browser in bstack111lll1l1l1_opy_:
        if browser in self.bstack111ll1lllll_opy_:
          bstack111llll1l11_opy_ = self.bstack111ll1lllll_opy_[browser]
        if bstack111llll1l11_opy_ < bstack111lllll11l_opy_:
          bstack111lllll11l_opy_ = bstack111llll1l11_opy_
          bstack111llll1lll_opy_ = browser
      return bstack111llll1lll_opy_
    except Exception as e:
      self.logger.error(bstack1l11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ᳽").format(e))
  @classmethod
  def bstack1l111l111_opy_(self):
    return os.getenv(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧ᳾"), bstack1l11lll_opy_ (u"ࠪࡊࡦࡲࡳࡦࠩ᳿")).lower()
  @classmethod
  def bstack1lll11l1_opy_(self):
    return os.getenv(bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᴀ"), bstack1l11lll_opy_ (u"ࠬ࠭ᴁ"))
  @classmethod
  def bstack1l1ll1l1lll_opy_(cls, value):
    cls.bstack1l1llllll_opy_ = value
  @classmethod
  def bstack111lll1l1ll_opy_(cls):
    return cls.bstack1l1llllll_opy_
  @classmethod
  def bstack1l1ll1ll11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111lllll1ll_opy_(cls):
    return cls.percy_build_id