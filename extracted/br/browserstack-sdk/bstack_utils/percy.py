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
from bstack_utils.helper import bstack1l1ll11111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l1lll1ll_opy_ import bstack111lll1l1_opy_
class bstack1l1l11l1ll_opy_:
  working_dir = os.getcwd()
  bstack1111ll111_opy_ = False
  config = {}
  bstack111l111l111_opy_ = bstack1l1111_opy_ (u"ࠧࠨ ")
  binary_path = bstack1l1111_opy_ (u"ࠨࠩ ")
  bstack1llllll11111_opy_ = bstack1l1111_opy_ (u"ࠩࠪ‪")
  bstack1ll1l11l1_opy_ = False
  bstack1lllll11l1l1_opy_ = None
  bstack1lllll1l1l11_opy_ = {}
  bstack1llll1ll1lll_opy_ = 300
  bstack1llllll1111l_opy_ = False
  logger = None
  bstack1lllll1l1ll1_opy_ = False
  bstack1ll1l1l1ll_opy_ = False
  percy_build_id = None
  bstack1lllll111111_opy_ = bstack1l1111_opy_ (u"ࠪࠫ‫")
  bstack1llll1lll11l_opy_ = {
    bstack1l1111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ‬") : 1,
    bstack1l1111_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭‭") : 2,
    bstack1l1111_opy_ (u"࠭ࡥࡥࡩࡨࠫ‮") : 3,
    bstack1l1111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1llllll1llll_opy_(self):
    bstack1llll1llll1l_opy_ = bstack1l1111_opy_ (u"ࠨࠩ‰")
    bstack1lllll11lll1_opy_ = sys.platform
    bstack1llll1llll11_opy_ = bstack1l1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ‱")
    if re.match(bstack1l1111_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥ′"), bstack1lllll11lll1_opy_) != None:
      bstack1llll1llll1l_opy_ = bstack11l111l11l1_opy_ + bstack1l1111_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧ″")
      self.bstack1lllll111111_opy_ = bstack1l1111_opy_ (u"ࠬࡳࡡࡤࠩ‴")
    elif re.match(bstack1l1111_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦ‵"), bstack1lllll11lll1_opy_) != None:
      bstack1llll1llll1l_opy_ = bstack11l111l11l1_opy_ + bstack1l1111_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣ‶")
      bstack1llll1llll11_opy_ = bstack1l1111_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦ‷")
      self.bstack1lllll111111_opy_ = bstack1l1111_opy_ (u"ࠩࡺ࡭ࡳ࠭‸")
    else:
      bstack1llll1llll1l_opy_ = bstack11l111l11l1_opy_ + bstack1l1111_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨ‹")
      self.bstack1lllll111111_opy_ = bstack1l1111_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪ›")
    return bstack1llll1llll1l_opy_, bstack1llll1llll11_opy_
  def bstack1lllllll11l1_opy_(self):
    try:
      bstack1llll1llllll_opy_ = [os.path.join(expanduser(bstack1l1111_opy_ (u"ࠧࢄࠢ※")), bstack1l1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭‼")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llll1llllll_opy_:
        if(self.bstack1lllll1ll1ll_opy_(path)):
          return path
      raise bstack1l1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦ‽")
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥ‾").format(e))
  def bstack1lllll1ll1ll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llllll11ll1_opy_(self, bstack1lllll1111ll_opy_):
    return os.path.join(bstack1lllll1111ll_opy_, self.bstack111l111l111_opy_ + bstack1l1111_opy_ (u"ࠤ࠱ࡩࡹࡧࡧࠣ‿"))
  def bstack1lllll1lllll_opy_(self, bstack1lllll1111ll_opy_, bstack1llllll11lll_opy_):
    if not bstack1llllll11lll_opy_: return
    try:
      bstack1lllll11l11l_opy_ = self.bstack1llllll11ll1_opy_(bstack1lllll1111ll_opy_)
      with open(bstack1lllll11l11l_opy_, bstack1l1111_opy_ (u"ࠥࡻࠧ⁀")) as f:
        f.write(bstack1llllll11lll_opy_)
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡘࡧࡶࡦࡦࠣࡲࡪࡽࠠࡆࡖࡤ࡫ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠣ⁁"))
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡴࡩࡧࠣࡩࡹࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ⁂").format(e))
  def bstack1lllll11ll11_opy_(self, bstack1lllll1111ll_opy_):
    try:
      bstack1lllll11l11l_opy_ = self.bstack1llllll11ll1_opy_(bstack1lllll1111ll_opy_)
      if os.path.exists(bstack1lllll11l11l_opy_):
        with open(bstack1lllll11l11l_opy_, bstack1l1111_opy_ (u"ࠨࡲࠣ⁃")) as f:
          bstack1llllll11lll_opy_ = f.read().strip()
          return bstack1llllll11lll_opy_ if bstack1llllll11lll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠ࡭ࡱࡤࡨ࡮ࡴࡧࠡࡇࡗࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ⁄").format(e))
  def bstack1lllll111l1l_opy_(self, bstack1lllll1111ll_opy_, bstack1llll1llll1l_opy_):
    bstack1llllll1l11l_opy_ = self.bstack1lllll11ll11_opy_(bstack1lllll1111ll_opy_)
    if bstack1llllll1l11l_opy_:
      try:
        bstack1lllll1l1l1l_opy_ = self.bstack1llllll111l1_opy_(bstack1llllll1l11l_opy_, bstack1llll1llll1l_opy_)
        if not bstack1lllll1l1l1l_opy_:
          self.logger.debug(bstack1l1111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡵࠣࡹࡵࠦࡴࡰࠢࡧࡥࡹ࡫ࠠࠩࡇࡗࡥ࡬ࠦࡵ࡯ࡥ࡫ࡥࡳ࡭ࡥࡥࠫࠥ⁅"))
          return True
        self.logger.debug(bstack1l1111_opy_ (u"ࠤࡑࡩࡼࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡥࠣ⁆"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡬࡯ࡳࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤ⁇").format(e))
    return False
  def bstack1llllll111l1_opy_(self, bstack1llllll1l11l_opy_, bstack1llll1llll1l_opy_):
    try:
      headers = {
        bstack1l1111_opy_ (u"ࠦࡎ࡬࠭ࡏࡱࡱࡩ࠲ࡓࡡࡵࡥ࡫ࠦ⁈"): bstack1llllll1l11l_opy_
      }
      response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠬࡍࡅࡕࠩ⁉"), bstack1llll1llll1l_opy_, {}, {bstack1l1111_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢ⁊"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠿ࠦࡻࡾࠤ⁋").format(e))
  @measure(event_name=EVENTS.bstack11l1111l111_opy_, stage=STAGE.bstack1111lll11_opy_)
  def bstack1lllllll1ll1_opy_(self, bstack1llll1llll1l_opy_, bstack1llll1llll11_opy_):
    try:
      bstack1lllll1l1lll_opy_ = self.bstack1lllllll11l1_opy_()
      bstack1llllll1ll11_opy_ = os.path.join(bstack1lllll1l1lll_opy_, bstack1l1111_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫ⁌"))
      bstack1lllll11111l_opy_ = os.path.join(bstack1lllll1l1lll_opy_, bstack1llll1llll11_opy_)
      if self.bstack1lllll111l1l_opy_(bstack1lllll1l1lll_opy_, bstack1llll1llll1l_opy_): # if bstack1lllllll1l11_opy_, bstack1l11l11111l_opy_ bstack1llllll11lll_opy_ is bstack1lllll111ll1_opy_ to bstack111l1ll1lll_opy_ version available (response 304)
        if os.path.exists(bstack1lllll11111l_opy_):
          self.logger.info(bstack1l1111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦ⁍").format(bstack1lllll11111l_opy_))
          return bstack1lllll11111l_opy_
        if os.path.exists(bstack1llllll1ll11_opy_):
          self.logger.info(bstack1l1111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣ⁎").format(bstack1llllll1ll11_opy_))
          return self.bstack1llllllll111_opy_(bstack1llllll1ll11_opy_, bstack1llll1llll11_opy_)
      self.logger.info(bstack1l1111_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤ⁏").format(bstack1llll1llll1l_opy_))
      response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠬࡍࡅࡕࠩ⁐"), bstack1llll1llll1l_opy_, {}, {})
      if response.status_code == 200:
        bstack1llllll1l1ll_opy_ = response.headers.get(bstack1l1111_opy_ (u"ࠨࡅࡕࡣࡪࠦ⁑"), bstack1l1111_opy_ (u"ࠢࠣ⁒"))
        if bstack1llllll1l1ll_opy_:
          self.bstack1lllll1lllll_opy_(bstack1lllll1l1lll_opy_, bstack1llllll1l1ll_opy_)
        with open(bstack1llllll1ll11_opy_, bstack1l1111_opy_ (u"ࠨࡹࡥࠫ⁓")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1111_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢ⁔").format(bstack1llllll1ll11_opy_))
        return self.bstack1llllllll111_opy_(bstack1llllll1ll11_opy_, bstack1llll1llll11_opy_)
      else:
        raise(bstack1l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨ⁕").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧ⁖").format(e))
  def bstack1lllll1ll111_opy_(self, bstack1llll1llll1l_opy_, bstack1llll1llll11_opy_):
    try:
      retry = 2
      bstack1lllll11111l_opy_ = None
      bstack1llll1lll1ll_opy_ = False
      while retry > 0:
        bstack1lllll11111l_opy_ = self.bstack1lllllll1ll1_opy_(bstack1llll1llll1l_opy_, bstack1llll1llll11_opy_)
        bstack1llll1lll1ll_opy_ = self.bstack1lllllll11ll_opy_(bstack1llll1llll1l_opy_, bstack1llll1llll11_opy_, bstack1lllll11111l_opy_)
        if bstack1llll1lll1ll_opy_:
          break
        retry -= 1
      return bstack1lllll11111l_opy_, bstack1llll1lll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤ⁗").format(e))
    return bstack1lllll11111l_opy_, False
  def bstack1lllllll11ll_opy_(self, bstack1llll1llll1l_opy_, bstack1llll1llll11_opy_, bstack1lllll11111l_opy_, bstack1lllll11l111_opy_ = 0):
    if bstack1lllll11l111_opy_ > 1:
      return False
    if bstack1lllll11111l_opy_ == None or os.path.exists(bstack1lllll11111l_opy_) == False:
      self.logger.warn(bstack1l1111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦ⁘"))
      return False
    command = bstack1l1111_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭⁙").format(bstack1lllll11111l_opy_)
    bstack1llllll1l1l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack1l1111_opy_ (u"ࠨࡂࡳࡩࡷࡩࡹ࠰ࡥ࡯࡭ࠬ⁚") in bstack1llllll1l1l1_opy_:
      return True
    else:
      self.logger.error(bstack1l1111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣ⁛"))
      return False
  def bstack1llllllll111_opy_(self, bstack1llllll1ll11_opy_, bstack1llll1llll11_opy_):
    try:
      working_dir = os.path.dirname(bstack1llllll1ll11_opy_)
      shutil.unpack_archive(bstack1llllll1ll11_opy_, working_dir)
      bstack1lllll11111l_opy_ = os.path.join(working_dir, bstack1llll1llll11_opy_)
      os.chmod(bstack1lllll11111l_opy_, 0o755)
      return bstack1lllll11111l_opy_
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦ⁜"))
  def bstack1lllll1llll1_opy_(self):
    try:
      bstack1lllll1l11l1_opy_ = self.config.get(bstack1l1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⁝"))
      bstack1lllll1llll1_opy_ = bstack1lllll1l11l1_opy_ or (bstack1lllll1l11l1_opy_ is None and self.bstack1111ll111_opy_)
      if not bstack1lllll1llll1_opy_ or self.config.get(bstack1l1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⁞"), None) not in bstack11l111l1ll1_opy_:
        return False
      self.bstack1ll1l11l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ ").format(e))
  def bstack1llllll11l1l_opy_(self):
    try:
      bstack1llllll11l1l_opy_ = self.percy_capture_mode
      return bstack1llllll11l1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⁠").format(e))
  def init(self, bstack1111ll111_opy_, config, logger):
    self.bstack1111ll111_opy_ = bstack1111ll111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lllll1llll1_opy_():
      return
    self.bstack1lllll1l1l11_opy_ = config.get(bstack1l1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⁡"), {})
    self.percy_capture_mode = config.get(bstack1l1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ⁢"))
    try:
      bstack1llll1llll1l_opy_, bstack1llll1llll11_opy_ = self.bstack1llllll1llll_opy_()
      self.bstack111l111l111_opy_ = bstack1llll1llll11_opy_
      bstack1lllll11111l_opy_, bstack1llll1lll1ll_opy_ = self.bstack1lllll1ll111_opy_(bstack1llll1llll1l_opy_, bstack1llll1llll11_opy_)
      if bstack1llll1lll1ll_opy_:
        self.binary_path = bstack1lllll11111l_opy_
        thread = Thread(target=self.bstack1lllllll1lll_opy_)
        thread.start()
      else:
        self.bstack1lllll1l1ll1_opy_ = True
        self.logger.error(bstack1l1111_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢ⁣").format(bstack1lllll11111l_opy_))
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ⁤").format(e))
  def bstack1lllll11ll1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1111_opy_ (u"ࠬࡲ࡯ࡨࠩ⁥"), bstack1l1111_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩ⁦"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1111_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦ⁧").format(logfile))
      self.bstack1llllll11111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ⁨").format(e))
  @measure(event_name=EVENTS.bstack11l11l11l11_opy_, stage=STAGE.bstack1111lll11_opy_)
  def bstack1lllllll1lll_opy_(self):
    bstack1lllll111l11_opy_ = self.bstack1lllll1lll11_opy_()
    if bstack1lllll111l11_opy_ == None:
      self.bstack1lllll1l1ll1_opy_ = True
      self.logger.error(bstack1l1111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧ⁩"))
      return False
    bstack1llllll11l11_opy_ = [bstack1l1111_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦ⁪") if self.bstack1111ll111_opy_ else bstack1l1111_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨ⁫")]
    bstack1111l1l1111_opy_ = self.bstack1lllll1ll11l_opy_()
    if bstack1111l1l1111_opy_ != None:
      bstack1llllll11l11_opy_.append(bstack1l1111_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦ⁬").format(bstack1111l1l1111_opy_))
    env = os.environ.copy()
    env[bstack1l1111_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦ⁭")] = bstack1lllll111l11_opy_
    env[bstack1l1111_opy_ (u"ࠢࡕࡊࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠢ⁮")] = os.environ.get(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⁯"), bstack1l1111_opy_ (u"ࠩࠪ⁰"))
    bstack1llllll1l111_opy_ = [self.binary_path]
    self.bstack1lllll11ll1l_opy_()
    self.bstack1lllll11l1l1_opy_ = self.bstack1lllllll111l_opy_(bstack1llllll1l111_opy_ + bstack1llllll11l11_opy_, env)
    self.logger.debug(bstack1l1111_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦⁱ"))
    bstack1lllll11l111_opy_ = 0
    while self.bstack1lllll11l1l1_opy_.poll() == None:
      bstack1lllll1lll1l_opy_ = self.bstack1llll1lll111_opy_()
      if bstack1lllll1lll1l_opy_:
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢ⁲"))
        self.bstack1llllll1111l_opy_ = True
        return True
      bstack1lllll11l111_opy_ += 1
      self.logger.debug(bstack1l1111_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣ⁳").format(bstack1lllll11l111_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦ⁴").format(bstack1lllll11l111_opy_))
    self.bstack1lllll1l1ll1_opy_ = True
    return False
  def bstack1llll1lll111_opy_(self, bstack1lllll11l111_opy_ = 0):
    if bstack1lllll11l111_opy_ > 10:
      return False
    try:
      bstack1lllll1l11ll_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧ⁵"), bstack1l1111_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩ⁶"))
      bstack1lllll111lll_opy_ = bstack1lllll1l11ll_opy_ + bstack11l11l11lll_opy_
      response = requests.get(bstack1lllll111lll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨ⁷"), {}).get(bstack1l1111_opy_ (u"ࠪ࡭ࡩ࠭⁸"), None)
      return True
    except:
      self.logger.debug(bstack1l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡪࡨࡥࡱࡺࡨࠡࡥ࡫ࡩࡨࡱࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤ⁹"))
      return False
  def bstack1lllll1lll11_opy_(self):
    bstack1lllllll1111_opy_ = bstack1l1111_opy_ (u"ࠬࡧࡰࡱࠩ⁺") if self.bstack1111ll111_opy_ else bstack1l1111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⁻")
    bstack1lllll1ll1l1_opy_ = bstack1l1111_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥ⁼") if self.config.get(bstack1l1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⁽")) is None else True
    bstack11l1l11111l_opy_ = bstack1l1111_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠧࡲࡨࡶࡨࡿ࠽ࡼࡿࠥ⁾").format(self.config[bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨⁿ")], bstack1lllllll1111_opy_, bstack1lllll1ll1l1_opy_)
    if self.percy_capture_mode:
      bstack11l1l11111l_opy_ += bstack1l1111_opy_ (u"ࠦࠫࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࡀࡿࢂࠨ₀").format(self.percy_capture_mode)
    uri = bstack111lll1l1_opy_(bstack11l1l11111l_opy_)
    try:
      response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠬࡍࡅࡕࠩ₁"), uri, {}, {bstack1l1111_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ₂"): (self.config[bstack1l1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ₃")], self.config[bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ₄")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1ll1l11l1_opy_ = data.get(bstack1l1111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ₅"))
        self.percy_capture_mode = data.get(bstack1l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥࠨ₆"))
        os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩ₇")] = str(self.bstack1ll1l11l1_opy_)
        os.environ[bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩ₈")] = str(self.percy_capture_mode)
        if bstack1lllll1ll1l1_opy_ == bstack1l1111_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤ₉") and str(self.bstack1ll1l11l1_opy_).lower() == bstack1l1111_opy_ (u"ࠢࡵࡴࡸࡩࠧ₊"):
          self.bstack1ll1l1l1ll_opy_ = True
        if bstack1l1111_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢ₋") in data:
          return data[bstack1l1111_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣ₌")]
        else:
          raise bstack1l1111_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪ₍").format(data)
      else:
        raise bstack1l1111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦ₎").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨ₏").format(e))
  def bstack1lllll1ll11l_opy_(self):
    bstack1lllll1l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤₐ"))
    try:
      if bstack1l1111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨₑ") not in self.bstack1lllll1l1l11_opy_:
        self.bstack1lllll1l1l11_opy_[bstack1l1111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩₒ")] = 2
      with open(bstack1lllll1l111l_opy_, bstack1l1111_opy_ (u"ࠩࡺࠫₓ")) as fp:
        json.dump(self.bstack1lllll1l1l11_opy_, fp)
      return bstack1lllll1l111l_opy_
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥₔ").format(e))
  def bstack1lllllll111l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1lllll111111_opy_ == bstack1l1111_opy_ (u"ࠫࡼ࡯࡮ࠨₕ"):
        bstack1lllllll1l1l_opy_ = [bstack1l1111_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭ₖ"), bstack1l1111_opy_ (u"࠭࠯ࡤࠩₗ")]
        cmd = bstack1lllllll1l1l_opy_ + cmd
      cmd = bstack1l1111_opy_ (u"ࠧࠡࠩₘ").join(cmd)
      self.logger.debug(bstack1l1111_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧₙ").format(cmd))
      with open(self.bstack1llllll11111_opy_, bstack1l1111_opy_ (u"ࠤࡤࠦₚ")) as bstack1llllll1lll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llllll1lll1_opy_, text=True, stderr=bstack1llllll1lll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lllll1l1ll1_opy_ = True
      self.logger.error(bstack1l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧₛ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llllll1111l_opy_:
        self.logger.info(bstack1l1111_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧₜ"))
        cmd = [self.binary_path, bstack1l1111_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣ₝")]
        self.bstack1lllllll111l_opy_(cmd)
        self.bstack1llllll1111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ₞").format(cmd, e))
  def bstack11llll1l11_opy_(self):
    if not self.bstack1ll1l11l1_opy_:
      return
    try:
      bstack1llll1lll1l1_opy_ = 0
      while not self.bstack1llllll1111l_opy_ and bstack1llll1lll1l1_opy_ < self.bstack1llll1ll1lll_opy_:
        if self.bstack1lllll1l1ll1_opy_:
          self.logger.info(bstack1l1111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧ₟"))
          return
        time.sleep(1)
        bstack1llll1lll1l1_opy_ += 1
      os.environ[bstack1l1111_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧ₠")] = str(self.bstack1llllll1ll1l_opy_())
      self.logger.info(bstack1l1111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥ₡"))
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ₢").format(e))
  def bstack1llllll1ll1l_opy_(self):
    if self.bstack1111ll111_opy_:
      return
    try:
      bstack1lllll1111l1_opy_ = [platform[bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ₣")].lower() for platform in self.config.get(bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ₤"), [])]
      bstack1llll1lllll1_opy_ = sys.maxsize
      bstack1lllll11l1ll_opy_ = bstack1l1111_opy_ (u"࠭ࠧ₥")
      for browser in bstack1lllll1111l1_opy_:
        if browser in self.bstack1llll1lll11l_opy_:
          bstack1lllll11llll_opy_ = self.bstack1llll1lll11l_opy_[browser]
        if bstack1lllll11llll_opy_ < bstack1llll1lllll1_opy_:
          bstack1llll1lllll1_opy_ = bstack1lllll11llll_opy_
          bstack1lllll11l1ll_opy_ = browser
      return bstack1lllll11l1ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ₦").format(e))
  @classmethod
  def bstack11l1llllll_opy_(self):
    return os.getenv(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭₧"), bstack1l1111_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨ₨")).lower()
  @classmethod
  def bstack11llllll11_opy_(self):
    return os.getenv(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧ₩"), bstack1l1111_opy_ (u"ࠫࠬ₪"))
  @classmethod
  def bstack1l11l1l1lll_opy_(cls, value):
    cls.bstack1ll1l1l1ll_opy_ = value
  @classmethod
  def bstack1llllll111ll_opy_(cls):
    return cls.bstack1ll1l1l1ll_opy_
  @classmethod
  def bstack1l11l1ll1l1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1lllll1l1111_opy_(cls):
    return cls.percy_build_id