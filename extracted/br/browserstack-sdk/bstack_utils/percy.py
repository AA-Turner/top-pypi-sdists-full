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
from bstack_utils.helper import bstack11l11llll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll1l11ll_opy_ import bstack11l11lll_opy_
class bstack11l1llll1_opy_:
  working_dir = os.getcwd()
  bstack11l1lll1l_opy_ = False
  config = {}
  bstack1111l11l11l_opy_ = bstack11l1l11_opy_ (u"ࠪࠫ℧")
  binary_path = bstack11l1l11_opy_ (u"ࠫࠬℨ")
  bstack1llll1l111ll_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭℩")
  bstack1l11l1l1l_opy_ = False
  bstack1llll11l1l11_opy_ = None
  bstack1lllll111l11_opy_ = {}
  bstack1llll1l1l11l_opy_ = 300
  bstack1llll1ll111l_opy_ = False
  logger = None
  bstack1lllll11l1l1_opy_ = False
  bstack11l11lll1l_opy_ = False
  percy_build_id = None
  bstack1lllll111l1l_opy_ = bstack11l1l11_opy_ (u"࠭ࠧK")
  bstack1llll11lllll_opy_ = {
    bstack11l1l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧÅ") : 1,
    bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩℬ") : 2,
    bstack11l1l11_opy_ (u"ࠩࡨࡨ࡬࡫ࠧℭ") : 3,
    bstack11l1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ℮") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lllll11l111_opy_(self):
    bstack1llll1ll1l11_opy_ = bstack11l1l11_opy_ (u"ࠫࠬℯ")
    bstack1llll1ll11l1_opy_ = sys.platform
    bstack1llll11l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫℰ")
    if re.match(bstack11l1l11_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨℱ"), bstack1llll1ll11l1_opy_) != None:
      bstack1llll1ll1l11_opy_ = bstack111lll111l1_opy_ + bstack11l1l11_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣℲ")
      self.bstack1lllll111l1l_opy_ = bstack11l1l11_opy_ (u"ࠨ࡯ࡤࡧࠬℳ")
    elif re.match(bstack11l1l11_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢℴ"), bstack1llll1ll11l1_opy_) != None:
      bstack1llll1ll1l11_opy_ = bstack111lll111l1_opy_ + bstack11l1l11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦℵ")
      bstack1llll11l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢℶ")
      self.bstack1lllll111l1l_opy_ = bstack11l1l11_opy_ (u"ࠬࡽࡩ࡯ࠩℷ")
    else:
      bstack1llll1ll1l11_opy_ = bstack111lll111l1_opy_ + bstack11l1l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤℸ")
      self.bstack1lllll111l1l_opy_ = bstack11l1l11_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ℹ")
    return bstack1llll1ll1l11_opy_, bstack1llll11l1l1l_opy_
  def bstack1llll1ll1111_opy_(self):
    try:
      bstack1llll1lll111_opy_ = [os.path.join(expanduser(bstack11l1l11_opy_ (u"ࠣࢀࠥ℺")), bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ℻")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llll1lll111_opy_:
        if(self.bstack1llll11lll1l_opy_(path)):
          return path
      raise bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢℼ")
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨℽ").format(e))
  def bstack1llll11lll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llll1l1l1l1_opy_(self, bstack1llll1ll11ll_opy_):
    return os.path.join(bstack1llll1ll11ll_opy_, self.bstack1111l11l11l_opy_ + bstack11l1l11_opy_ (u"ࠧ࠴ࡥࡵࡣࡪࠦℾ"))
  def bstack1llll11l1111_opy_(self, bstack1llll1ll11ll_opy_, bstack1llll11l11ll_opy_):
    if not bstack1llll11l11ll_opy_: return
    try:
      bstack1llll11ll11l_opy_ = self.bstack1llll1l1l1l1_opy_(bstack1llll1ll11ll_opy_)
      with open(bstack1llll11ll11l_opy_, bstack11l1l11_opy_ (u"ࠨࡷࠣℿ")) as f:
        f.write(bstack1llll11l11ll_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡔࡣࡹࡩࡩࠦ࡮ࡦࡹࠣࡉ࡙ࡧࡧࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠦ⅀"))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡷ࡬ࡪࠦࡥࡵࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ⅁").format(e))
  def bstack1llll1llllll_opy_(self, bstack1llll1ll11ll_opy_):
    try:
      bstack1llll11ll11l_opy_ = self.bstack1llll1l1l1l1_opy_(bstack1llll1ll11ll_opy_)
      if os.path.exists(bstack1llll11ll11l_opy_):
        with open(bstack1llll11ll11l_opy_, bstack11l1l11_opy_ (u"ࠤࡵࠦ⅂")) as f:
          bstack1llll11l11ll_opy_ = f.read().strip()
          return bstack1llll11l11ll_opy_ if bstack1llll11l11ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡰࡴࡧࡤࡪࡰࡪࠤࡊ࡚ࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ⅃").format(e))
  def bstack1llll11l111l_opy_(self, bstack1llll1ll11ll_opy_, bstack1llll1ll1l11_opy_):
    bstack1llll1l11l11_opy_ = self.bstack1llll1llllll_opy_(bstack1llll1ll11ll_opy_)
    if bstack1llll1l11l11_opy_:
      try:
        bstack1llll11ll1l1_opy_ = self.bstack1llll1l1ll1l_opy_(bstack1llll1l11l11_opy_, bstack1llll1ll1l11_opy_)
        if not bstack1llll11ll1l1_opy_:
          self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡸࠦࡵࡱࠢࡷࡳࠥࡪࡡࡵࡧࠣࠬࡊ࡚ࡡࡨࠢࡸࡲࡨ࡮ࡡ࡯ࡩࡨࡨ࠮ࠨ⅄"))
          return True
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡔࡥࡸࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡺࡶࡤࡢࡶࡨࠦⅅ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡲࡶࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧⅆ").format(e))
    return False
  def bstack1llll1l1ll1l_opy_(self, bstack1llll1l11l11_opy_, bstack1llll1ll1l11_opy_):
    try:
      headers = {
        bstack11l1l11_opy_ (u"ࠢࡊࡨ࠰ࡒࡴࡴࡥ࠮ࡏࡤࡸࡨ࡮ࠢⅇ"): bstack1llll1l11l11_opy_
      }
      response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠨࡉࡈࡘࠬⅈ"), bstack1llll1ll1l11_opy_, {}, {bstack11l1l11_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥⅉ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠻ࠢࡾࢁࠧ⅊").format(e))
  @measure(event_name=EVENTS.bstack111lll1111l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
  def bstack1llll1lll1ll_opy_(self, bstack1llll1ll1l11_opy_, bstack1llll11l1l1l_opy_):
    try:
      bstack1lllll1111ll_opy_ = self.bstack1llll1ll1111_opy_()
      bstack1llll1l11l1l_opy_ = os.path.join(bstack1lllll1111ll_opy_, bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧ⅋"))
      bstack1llll1l1ll11_opy_ = os.path.join(bstack1lllll1111ll_opy_, bstack1llll11l1l1l_opy_)
      if self.bstack1llll11l111l_opy_(bstack1lllll1111ll_opy_, bstack1llll1ll1l11_opy_): # if bstack1llll111ll11_opy_, bstack1l111l11l11_opy_ bstack1llll11l11ll_opy_ is bstack1lllll111111_opy_ to bstack111l1lll11l_opy_ version available (response 304)
        if os.path.exists(bstack1llll1l1ll11_opy_):
          self.logger.info(bstack11l1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ⅌").format(bstack1llll1l1ll11_opy_))
          return bstack1llll1l1ll11_opy_
        if os.path.exists(bstack1llll1l11l1l_opy_):
          self.logger.info(bstack11l1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦ⅍").format(bstack1llll1l11l1l_opy_))
          return self.bstack1llll11ll1ll_opy_(bstack1llll1l11l1l_opy_, bstack1llll11l1l1l_opy_)
      self.logger.info(bstack11l1l11_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧⅎ").format(bstack1llll1ll1l11_opy_))
      response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠨࡉࡈࡘࠬ⅏"), bstack1llll1ll1l11_opy_, {}, {})
      if response.status_code == 200:
        bstack1llll11l1ll1_opy_ = response.headers.get(bstack11l1l11_opy_ (u"ࠤࡈࡘࡦ࡭ࠢ⅐"), bstack11l1l11_opy_ (u"ࠥࠦ⅑"))
        if bstack1llll11l1ll1_opy_:
          self.bstack1llll11l1111_opy_(bstack1lllll1111ll_opy_, bstack1llll11l1ll1_opy_)
        with open(bstack1llll1l11l1l_opy_, bstack11l1l11_opy_ (u"ࠫࡼࡨࠧ⅒")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1l11_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥ⅓").format(bstack1llll1l11l1l_opy_))
        return self.bstack1llll11ll1ll_opy_(bstack1llll1l11l1l_opy_, bstack1llll11l1l1l_opy_)
      else:
        raise(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤ⅔").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣ⅕").format(e))
  def bstack1llll111ll1l_opy_(self, bstack1llll1ll1l11_opy_, bstack1llll11l1l1l_opy_):
    try:
      retry = 2
      bstack1llll1l1ll11_opy_ = None
      bstack1llll11llll1_opy_ = False
      while retry > 0:
        bstack1llll1l1ll11_opy_ = self.bstack1llll1lll1ll_opy_(bstack1llll1ll1l11_opy_, bstack1llll11l1l1l_opy_)
        bstack1llll11llll1_opy_ = self.bstack1llll1l11lll_opy_(bstack1llll1ll1l11_opy_, bstack1llll11l1l1l_opy_, bstack1llll1l1ll11_opy_)
        if bstack1llll11llll1_opy_:
          break
        retry -= 1
      return bstack1llll1l1ll11_opy_, bstack1llll11llll1_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧ⅖").format(e))
    return bstack1llll1l1ll11_opy_, False
  def bstack1llll1l11lll_opy_(self, bstack1llll1ll1l11_opy_, bstack1llll11l1l1l_opy_, bstack1llll1l1ll11_opy_, bstack1llll1l1lll1_opy_ = 0):
    if bstack1llll1l1lll1_opy_ > 1:
      return False
    if bstack1llll1l1ll11_opy_ == None or os.path.exists(bstack1llll1l1ll11_opy_) == False:
      self.logger.warn(bstack11l1l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ⅗"))
      return False
    command = bstack11l1l11_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩ⅘").format(bstack1llll1l1ll11_opy_)
    bstack1llll11lll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack11l1l11_opy_ (u"ࠫࡅࡶࡥࡳࡥࡼ࠳ࡨࡲࡩࠨ⅙") in bstack1llll11lll11_opy_:
      return True
    else:
      self.logger.error(bstack11l1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦ⅚"))
      return False
  def bstack1llll11ll1ll_opy_(self, bstack1llll1l11l1l_opy_, bstack1llll11l1l1l_opy_):
    try:
      working_dir = os.path.dirname(bstack1llll1l11l1l_opy_)
      shutil.unpack_archive(bstack1llll1l11l1l_opy_, working_dir)
      bstack1llll1l1ll11_opy_ = os.path.join(working_dir, bstack1llll11l1l1l_opy_)
      os.chmod(bstack1llll1l1ll11_opy_, 0o755)
      return bstack1llll1l1ll11_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢ⅛"))
  def bstack1llll111l1ll_opy_(self):
    try:
      bstack1llll1llll11_opy_ = self.config.get(bstack11l1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⅜"))
      bstack1llll111l1ll_opy_ = bstack1llll1llll11_opy_ or (bstack1llll1llll11_opy_ is None and self.bstack11l1lll1l_opy_)
      if not bstack1llll111l1ll_opy_ or self.config.get(bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⅝"), None) not in bstack111lllll1ll_opy_:
        return False
      self.bstack1l11l1l1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ⅞").format(e))
  def bstack1llll1ll1lll_opy_(self):
    try:
      bstack1llll1ll1lll_opy_ = self.percy_capture_mode
      return bstack1llll1ll1lll_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ⅟").format(e))
  def init(self, bstack11l1lll1l_opy_, config, logger):
    self.bstack11l1lll1l_opy_ = bstack11l1lll1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll111l1ll_opy_():
      return
    self.bstack1lllll111l11_opy_ = config.get(bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪⅠ"), {})
    self.percy_capture_mode = config.get(bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨⅡ"))
    try:
      bstack1llll1ll1l11_opy_, bstack1llll11l1l1l_opy_ = self.bstack1lllll11l111_opy_()
      self.bstack1111l11l11l_opy_ = bstack1llll11l1l1l_opy_
      bstack1llll1l1ll11_opy_, bstack1llll11llll1_opy_ = self.bstack1llll111ll1l_opy_(bstack1llll1ll1l11_opy_, bstack1llll11l1l1l_opy_)
      if bstack1llll11llll1_opy_:
        self.binary_path = bstack1llll1l1ll11_opy_
        thread = Thread(target=self.bstack1lllll1111l1_opy_)
        thread.start()
      else:
        self.bstack1lllll11l1l1_opy_ = True
        self.logger.error(bstack11l1l11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥⅢ").format(bstack1llll1l1ll11_opy_))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣⅣ").format(e))
  def bstack1llll1llll1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬⅤ"), bstack11l1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬⅥ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢⅦ").format(logfile))
      self.bstack1llll1l111ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧⅧ").format(e))
  @measure(event_name=EVENTS.bstack111ll1ll111_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
  def bstack1lllll1111l1_opy_(self):
    bstack1llll1lllll1_opy_ = self.bstack1lllll11l11l_opy_()
    if bstack1llll1lllll1_opy_ == None:
      self.bstack1lllll11l1l1_opy_ = True
      self.logger.error(bstack11l1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣⅨ"))
      return False
    bstack1lllll111lll_opy_ = [bstack11l1l11_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢⅩ") if self.bstack11l1lll1l_opy_ else bstack11l1l11_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫⅪ")]
    bstack1llllll111l_opy_ = self.bstack1llll1l1l1ll_opy_()
    if bstack1llllll111l_opy_ != None:
      bstack1lllll111lll_opy_.append(bstack11l1l11_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢⅫ").format(bstack1llllll111l_opy_))
    env = os.environ.copy()
    env[bstack11l1l11_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢⅬ")] = bstack1llll1lllll1_opy_
    env[bstack11l1l11_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥⅭ")] = os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩⅮ"), bstack11l1l11_opy_ (u"ࠬ࠭Ⅿ"))
    bstack1llll11l1lll_opy_ = [self.binary_path]
    self.bstack1llll1llll1l_opy_()
    self.bstack1llll11l1l11_opy_ = self.bstack1llll1l1111l_opy_(bstack1llll11l1lll_opy_ + bstack1lllll111lll_opy_, env)
    self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢⅰ"))
    bstack1llll1l1lll1_opy_ = 0
    while self.bstack1llll11l1l11_opy_.poll() == None:
      bstack1llll11ll111_opy_ = self.bstack1llll11l11l1_opy_()
      if bstack1llll11ll111_opy_:
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥⅱ"))
        self.bstack1llll1ll111l_opy_ = True
        return True
      bstack1llll1l1lll1_opy_ += 1
      self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦⅲ").format(bstack1llll1l1lll1_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢⅳ").format(bstack1llll1l1lll1_opy_))
    self.bstack1lllll11l1l1_opy_ = True
    return False
  def bstack1llll11l11l1_opy_(self, bstack1llll1l1lll1_opy_ = 0):
    if bstack1llll1l1lll1_opy_ > 10:
      return False
    try:
      bstack1llll1ll1l1l_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪⅴ"), bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬⅵ"))
      bstack1llll1l111l1_opy_ = bstack1llll1ll1l1l_opy_ + bstack111ll1ll1ll_opy_
      response = requests.get(bstack1llll1l111l1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫⅶ"), {}).get(bstack11l1l11_opy_ (u"࠭ࡩࡥࠩⅷ"), None)
      return True
    except:
      self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧⅸ"))
      return False
  def bstack1lllll11l11l_opy_(self):
    bstack1llll1l11ll1_opy_ = bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࠬⅹ") if self.bstack11l1lll1l_opy_ else bstack11l1l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫⅺ")
    bstack1lllll11111l_opy_ = bstack11l1l11_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨⅻ") if self.config.get(bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪⅼ")) is None else True
    bstack11l111l11ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨⅽ").format(self.config[bstack11l1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫⅾ")], bstack1llll1l11ll1_opy_, bstack1lllll11111l_opy_)
    if self.percy_capture_mode:
      bstack11l111l11ll_opy_ += bstack11l1l11_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤⅿ").format(self.percy_capture_mode)
    uri = bstack11l11lll_opy_(bstack11l111l11ll_opy_)
    try:
      response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠨࡉࡈࡘࠬↀ"), uri, {}, {bstack11l1l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧↁ"): (self.config[bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬↂ")], self.config[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧↃ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l11l1l1l_opy_ = data.get(bstack11l1l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ↄ"))
        self.percy_capture_mode = data.get(bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫↅ"))
        os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬↆ")] = str(self.bstack1l11l1l1l_opy_)
        os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬↇ")] = str(self.percy_capture_mode)
        if bstack1lllll11111l_opy_ == bstack11l1l11_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧↈ") and str(self.bstack1l11l1l1l_opy_).lower() == bstack11l1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ↉"):
          self.bstack11l11lll1l_opy_ = True
        if bstack11l1l11_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ↊") in data:
          return data[bstack11l1l11_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ↋")]
        else:
          raise bstack11l1l11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭↌").format(data)
      else:
        raise bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢ↍").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤ↎").format(e))
  def bstack1llll1l1l1ll_opy_(self):
    bstack1llll1l1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧ↏"))
    try:
      if bstack11l1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ←") not in self.bstack1lllll111l11_opy_:
        self.bstack1lllll111l11_opy_[bstack11l1l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ↑")] = 2
      with open(bstack1llll1l1l111_opy_, bstack11l1l11_opy_ (u"ࠬࡽࠧ→")) as fp:
        json.dump(self.bstack1lllll111l11_opy_, fp)
      return bstack1llll1l1l111_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ↓").format(e))
  def bstack1llll1l1111l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1lllll111l1l_opy_ == bstack11l1l11_opy_ (u"ࠧࡸ࡫ࡱࠫ↔"):
        bstack1llll111llll_opy_ = [bstack11l1l11_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩ↕"), bstack11l1l11_opy_ (u"ࠩ࠲ࡧࠬ↖")]
        cmd = bstack1llll111llll_opy_ + cmd
      cmd = bstack11l1l11_opy_ (u"ࠪࠤࠬ↗").join(cmd)
      self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣ↘").format(cmd))
      with open(self.bstack1llll1l111ll_opy_, bstack11l1l11_opy_ (u"ࠧࡧࠢ↙")) as bstack1llll1ll1ll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll1ll1ll1_opy_, text=True, stderr=bstack1llll1ll1ll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lllll11l1l1_opy_ = True
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ↚").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llll1ll111l_opy_:
        self.logger.info(bstack11l1l11_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣ↛"))
        cmd = [self.binary_path, bstack11l1l11_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦ↜")]
        self.bstack1llll1l1111l_opy_(cmd)
        self.bstack1llll1ll111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ↝").format(cmd, e))
  def bstack1lll111l_opy_(self):
    if not self.bstack1l11l1l1l_opy_:
      return
    try:
      bstack1lllll111ll1_opy_ = 0
      while not self.bstack1llll1ll111l_opy_ and bstack1lllll111ll1_opy_ < self.bstack1llll1l1l11l_opy_:
        if self.bstack1lllll11l1l1_opy_:
          self.logger.info(bstack11l1l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣ↞"))
          return
        time.sleep(1)
        bstack1lllll111ll1_opy_ += 1
      os.environ[bstack11l1l11_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪ↟")] = str(self.bstack1llll1l1llll_opy_())
      self.logger.info(bstack11l1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨ↠"))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ↡").format(e))
  def bstack1llll1l1llll_opy_(self):
    if self.bstack11l1lll1l_opy_:
      return
    try:
      bstack1llll1lll1l1_opy_ = [platform[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ↢")].lower() for platform in self.config.get(bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ↣"), [])]
      bstack1lll1111l11_opy_ = sys.maxsize
      bstack1llll1l11111_opy_ = bstack11l1l11_opy_ (u"ࠩࠪ↤")
      for browser in bstack1llll1lll1l1_opy_:
        if browser in self.bstack1llll11lllll_opy_:
          bstack1llll111l1l1_opy_ = self.bstack1llll11lllll_opy_[browser]
        if bstack1llll111l1l1_opy_ < bstack1lll1111l11_opy_:
          bstack1lll1111l11_opy_ = bstack1llll111l1l1_opy_
          bstack1llll1l11111_opy_ = browser
      return bstack1llll1l11111_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ↥").format(e))
  @classmethod
  def bstack1l1111ll11_opy_(self):
    return os.getenv(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩ↦"), bstack11l1l11_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫ↧")).lower()
  @classmethod
  def bstack11l1ll111l_opy_(self):
    return os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪ↨"), bstack11l1l11_opy_ (u"ࠧࠨ↩"))
  @classmethod
  def bstack1l111ll11l1_opy_(cls, value):
    cls.bstack11l11lll1l_opy_ = value
  @classmethod
  def bstack1llll1lll11l_opy_(cls):
    return cls.bstack11l11lll1l_opy_
  @classmethod
  def bstack1l111l1llll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1llll111lll1_opy_(cls):
    return cls.percy_build_id