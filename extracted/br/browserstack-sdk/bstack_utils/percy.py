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
from bstack_utils.helper import bstack1l1l11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11ll1l11l_opy_ import bstack1l1l1111ll_opy_
class bstack1ll1111l_opy_:
  working_dir = os.getcwd()
  bstack1l1111l11_opy_ = False
  config = {}
  bstack111l1l11lll_opy_ = bstack11ll111_opy_ (u"ࠧࠨℤ")
  binary_path = bstack11ll111_opy_ (u"ࠨࠩ℥")
  bstack1llll1l11111_opy_ = bstack11ll111_opy_ (u"ࠩࠪΩ")
  bstack1lll1lllll_opy_ = False
  bstack1llll11l11l1_opy_ = None
  bstack1llll1llllll_opy_ = {}
  bstack1lllll11l111_opy_ = 300
  bstack1llll1l1lll1_opy_ = False
  logger = None
  bstack1llll11l1l11_opy_ = False
  bstack111ll1lll_opy_ = False
  percy_build_id = None
  bstack1llll11l1111_opy_ = bstack11ll111_opy_ (u"ࠪࠫ℧")
  bstack1llll11lll1l_opy_ = {
    bstack11ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫℨ") : 1,
    bstack11ll111_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭℩") : 2,
    bstack11ll111_opy_ (u"࠭ࡥࡥࡩࡨࠫK") : 3,
    bstack11ll111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧÅ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1llll1l1l1ll_opy_(self):
    bstack1llll11lll11_opy_ = bstack11ll111_opy_ (u"ࠨࠩℬ")
    bstack1llll1l1l111_opy_ = sys.platform
    bstack1llll111l1l1_opy_ = bstack11ll111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨℭ")
    if re.match(bstack11ll111_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥ℮"), bstack1llll1l1l111_opy_) != None:
      bstack1llll11lll11_opy_ = bstack111lllll11l_opy_ + bstack11ll111_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧℯ")
      self.bstack1llll11l1111_opy_ = bstack11ll111_opy_ (u"ࠬࡳࡡࡤࠩℰ")
    elif re.match(bstack11ll111_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦℱ"), bstack1llll1l1l111_opy_) != None:
      bstack1llll11lll11_opy_ = bstack111lllll11l_opy_ + bstack11ll111_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣℲ")
      bstack1llll111l1l1_opy_ = bstack11ll111_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦℳ")
      self.bstack1llll11l1111_opy_ = bstack11ll111_opy_ (u"ࠩࡺ࡭ࡳ࠭ℴ")
    else:
      bstack1llll11lll11_opy_ = bstack111lllll11l_opy_ + bstack11ll111_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨℵ")
      self.bstack1llll11l1111_opy_ = bstack11ll111_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪℶ")
    return bstack1llll11lll11_opy_, bstack1llll111l1l1_opy_
  def bstack1llll1lllll1_opy_(self):
    try:
      bstack1lllll1111ll_opy_ = [os.path.join(expanduser(bstack11ll111_opy_ (u"ࠧࢄࠢℷ")), bstack11ll111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ℸ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lllll1111ll_opy_:
        if(self.bstack1llll1lll111_opy_(path)):
          return path
      raise bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦℹ")
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥ℺").format(e))
  def bstack1llll1lll111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llll1ll111l_opy_(self, bstack1llll1l1llll_opy_):
    return os.path.join(bstack1llll1l1llll_opy_, self.bstack111l1l11lll_opy_ + bstack11ll111_opy_ (u"ࠤ࠱ࡩࡹࡧࡧࠣ℻"))
  def bstack1lllll111l1l_opy_(self, bstack1llll1l1llll_opy_, bstack1llll11l11ll_opy_):
    if not bstack1llll11l11ll_opy_: return
    try:
      bstack1llll1ll1l11_opy_ = self.bstack1llll1ll111l_opy_(bstack1llll1l1llll_opy_)
      with open(bstack1llll1ll1l11_opy_, bstack11ll111_opy_ (u"ࠥࡻࠧℼ")) as f:
        f.write(bstack1llll11l11ll_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠦࡘࡧࡶࡦࡦࠣࡲࡪࡽࠠࡆࡖࡤ࡫ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠣℽ"))
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡴࡩࡧࠣࡩࡹࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧℾ").format(e))
  def bstack1lllll111111_opy_(self, bstack1llll1l1llll_opy_):
    try:
      bstack1llll1ll1l11_opy_ = self.bstack1llll1ll111l_opy_(bstack1llll1l1llll_opy_)
      if os.path.exists(bstack1llll1ll1l11_opy_):
        with open(bstack1llll1ll1l11_opy_, bstack11ll111_opy_ (u"ࠨࡲࠣℿ")) as f:
          bstack1llll11l11ll_opy_ = f.read().strip()
          return bstack1llll11l11ll_opy_ if bstack1llll11l11ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠ࡭ࡱࡤࡨ࡮ࡴࡧࠡࡇࡗࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ⅀").format(e))
  def bstack1lllll111lll_opy_(self, bstack1llll1l1llll_opy_, bstack1llll11lll11_opy_):
    bstack1llll1lll1l1_opy_ = self.bstack1lllll111111_opy_(bstack1llll1l1llll_opy_)
    if bstack1llll1lll1l1_opy_:
      try:
        bstack1llll11ll1l1_opy_ = self.bstack1llll1ll1l1l_opy_(bstack1llll1lll1l1_opy_, bstack1llll11lll11_opy_)
        if not bstack1llll11ll1l1_opy_:
          self.logger.debug(bstack11ll111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡵࠣࡹࡵࠦࡴࡰࠢࡧࡥࡹ࡫ࠠࠩࡇࡗࡥ࡬ࠦࡵ࡯ࡥ࡫ࡥࡳ࡭ࡥࡥࠫࠥ⅁"))
          return True
        self.logger.debug(bstack11ll111_opy_ (u"ࠤࡑࡩࡼࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡥࠣ⅂"))
        return False
      except Exception as e:
        self.logger.warn(bstack11ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡬࡯ࡳࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤ⅃").format(e))
    return False
  def bstack1llll1ll1l1l_opy_(self, bstack1llll1lll1l1_opy_, bstack1llll11lll11_opy_):
    try:
      headers = {
        bstack11ll111_opy_ (u"ࠦࡎ࡬࠭ࡏࡱࡱࡩ࠲ࡓࡡࡵࡥ࡫ࠦ⅄"): bstack1llll1lll1l1_opy_
      }
      response = bstack1l1l11ll_opy_(bstack11ll111_opy_ (u"ࠬࡍࡅࡕࠩⅅ"), bstack1llll11lll11_opy_, {}, {bstack11ll111_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢⅆ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠿ࠦࡻࡾࠤⅇ").format(e))
  @measure(event_name=EVENTS.bstack111ll1ll111_opy_, stage=STAGE.bstack1111l1111_opy_)
  def bstack1llll1l11l1l_opy_(self, bstack1llll11lll11_opy_, bstack1llll111l1l1_opy_):
    try:
      bstack1llll1ll11l1_opy_ = self.bstack1llll1lllll1_opy_()
      bstack1llll111ll11_opy_ = os.path.join(bstack1llll1ll11l1_opy_, bstack11ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫⅈ"))
      bstack1llll1ll1lll_opy_ = os.path.join(bstack1llll1ll11l1_opy_, bstack1llll111l1l1_opy_)
      if self.bstack1lllll111lll_opy_(bstack1llll1ll11l1_opy_, bstack1llll11lll11_opy_): # if bstack1llll1l111ll_opy_, bstack1l1111l1lll_opy_ bstack1llll11l11ll_opy_ is bstack1llll1l11lll_opy_ to bstack111l1111ll1_opy_ version available (response 304)
        if os.path.exists(bstack1llll1ll1lll_opy_):
          self.logger.info(bstack11ll111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦⅉ").format(bstack1llll1ll1lll_opy_))
          return bstack1llll1ll1lll_opy_
        if os.path.exists(bstack1llll111ll11_opy_):
          self.logger.info(bstack11ll111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣ⅊").format(bstack1llll111ll11_opy_))
          return self.bstack1lllll11l11l_opy_(bstack1llll111ll11_opy_, bstack1llll111l1l1_opy_)
      self.logger.info(bstack11ll111_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤ⅋").format(bstack1llll11lll11_opy_))
      response = bstack1l1l11ll_opy_(bstack11ll111_opy_ (u"ࠬࡍࡅࡕࠩ⅌"), bstack1llll11lll11_opy_, {}, {})
      if response.status_code == 200:
        bstack1llll111ll1l_opy_ = response.headers.get(bstack11ll111_opy_ (u"ࠨࡅࡕࡣࡪࠦ⅍"), bstack11ll111_opy_ (u"ࠢࠣⅎ"))
        if bstack1llll111ll1l_opy_:
          self.bstack1lllll111l1l_opy_(bstack1llll1ll11l1_opy_, bstack1llll111ll1l_opy_)
        with open(bstack1llll111ll11_opy_, bstack11ll111_opy_ (u"ࠨࡹࡥࠫ⅏")) as file:
          file.write(response.content)
        self.logger.info(bstack11ll111_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢ⅐").format(bstack1llll111ll11_opy_))
        return self.bstack1lllll11l11l_opy_(bstack1llll111ll11_opy_, bstack1llll111l1l1_opy_)
      else:
        raise(bstack11ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨ⅑").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧ⅒").format(e))
  def bstack1llll11lllll_opy_(self, bstack1llll11lll11_opy_, bstack1llll111l1l1_opy_):
    try:
      retry = 2
      bstack1llll1ll1lll_opy_ = None
      bstack1llll1llll1l_opy_ = False
      while retry > 0:
        bstack1llll1ll1lll_opy_ = self.bstack1llll1l11l1l_opy_(bstack1llll11lll11_opy_, bstack1llll111l1l1_opy_)
        bstack1llll1llll1l_opy_ = self.bstack1llll111lll1_opy_(bstack1llll11lll11_opy_, bstack1llll111l1l1_opy_, bstack1llll1ll1lll_opy_)
        if bstack1llll1llll1l_opy_:
          break
        retry -= 1
      return bstack1llll1ll1lll_opy_, bstack1llll1llll1l_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤ⅓").format(e))
    return bstack1llll1ll1lll_opy_, False
  def bstack1llll111lll1_opy_(self, bstack1llll11lll11_opy_, bstack1llll111l1l1_opy_, bstack1llll1ll1lll_opy_, bstack1llll1l1l1l1_opy_ = 0):
    if bstack1llll1l1l1l1_opy_ > 1:
      return False
    if bstack1llll1ll1lll_opy_ == None or os.path.exists(bstack1llll1ll1lll_opy_) == False:
      self.logger.warn(bstack11ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦ⅔"))
      return False
    command = bstack11ll111_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭⅕").format(bstack1llll1ll1lll_opy_)
    bstack1llll11ll11l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack11ll111_opy_ (u"ࠨࡂࡳࡩࡷࡩࡹ࠰ࡥ࡯࡭ࠬ⅖") in bstack1llll11ll11l_opy_:
      return True
    else:
      self.logger.error(bstack11ll111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣ⅗"))
      return False
  def bstack1lllll11l11l_opy_(self, bstack1llll111ll11_opy_, bstack1llll111l1l1_opy_):
    try:
      working_dir = os.path.dirname(bstack1llll111ll11_opy_)
      shutil.unpack_archive(bstack1llll111ll11_opy_, working_dir)
      bstack1llll1ll1lll_opy_ = os.path.join(working_dir, bstack1llll111l1l1_opy_)
      os.chmod(bstack1llll1ll1lll_opy_, 0o755)
      return bstack1llll1ll1lll_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦ⅘"))
  def bstack1llll1l111l1_opy_(self):
    try:
      bstack1lllll11111l_opy_ = self.config.get(bstack11ll111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⅙"))
      bstack1llll1l111l1_opy_ = bstack1lllll11111l_opy_ or (bstack1lllll11111l_opy_ is None and self.bstack1l1111l11_opy_)
      if not bstack1llll1l111l1_opy_ or self.config.get(bstack11ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⅚"), None) not in bstack111lll11lll_opy_:
        return False
      self.bstack1lll1lllll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⅛").format(e))
  def bstack1llll11ll1ll_opy_(self):
    try:
      bstack1llll11ll1ll_opy_ = self.percy_capture_mode
      return bstack1llll11ll1ll_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⅜").format(e))
  def init(self, bstack1l1111l11_opy_, config, logger):
    self.bstack1l1111l11_opy_ = bstack1l1111l11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll1l111l1_opy_():
      return
    self.bstack1llll1llllll_opy_ = config.get(bstack11ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⅝"), {})
    self.percy_capture_mode = config.get(bstack11ll111_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ⅞"))
    try:
      bstack1llll11lll11_opy_, bstack1llll111l1l1_opy_ = self.bstack1llll1l1l1ll_opy_()
      self.bstack111l1l11lll_opy_ = bstack1llll111l1l1_opy_
      bstack1llll1ll1lll_opy_, bstack1llll1llll1l_opy_ = self.bstack1llll11lllll_opy_(bstack1llll11lll11_opy_, bstack1llll111l1l1_opy_)
      if bstack1llll1llll1l_opy_:
        self.binary_path = bstack1llll1ll1lll_opy_
        thread = Thread(target=self.bstack1llll111llll_opy_)
        thread.start()
      else:
        self.bstack1llll11l1l11_opy_ = True
        self.logger.error(bstack11ll111_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢ⅟").format(bstack1llll1ll1lll_opy_))
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧⅠ").format(e))
  def bstack1llll1l1ll1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11ll111_opy_ (u"ࠬࡲ࡯ࡨࠩⅡ"), bstack11ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩⅢ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11ll111_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦⅣ").format(logfile))
      self.bstack1llll1l11111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤⅤ").format(e))
  @measure(event_name=EVENTS.bstack111llll1ll1_opy_, stage=STAGE.bstack1111l1111_opy_)
  def bstack1llll111llll_opy_(self):
    bstack1llll11l111l_opy_ = self.bstack1llll1llll11_opy_()
    if bstack1llll11l111l_opy_ == None:
      self.bstack1llll11l1l11_opy_ = True
      self.logger.error(bstack11ll111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧⅥ"))
      return False
    bstack1lllll111l11_opy_ = [bstack11ll111_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦⅦ") if self.bstack1l1111l11_opy_ else bstack11ll111_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨⅧ")]
    bstack1lllll1lll1_opy_ = self.bstack1llll1l1l11l_opy_()
    if bstack1lllll1lll1_opy_ != None:
      bstack1lllll111l11_opy_.append(bstack11ll111_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦⅨ").format(bstack1lllll1lll1_opy_))
    env = os.environ.copy()
    env[bstack11ll111_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦⅩ")] = bstack1llll11l111l_opy_
    env[bstack11ll111_opy_ (u"ࠢࡕࡊࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠢⅪ")] = os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ⅻ"), bstack11ll111_opy_ (u"ࠩࠪⅬ"))
    bstack1llll11l1ll1_opy_ = [self.binary_path]
    self.bstack1llll1l1ll1l_opy_()
    self.bstack1llll11l11l1_opy_ = self.bstack1llll1l1111l_opy_(bstack1llll11l1ll1_opy_ + bstack1lllll111l11_opy_, env)
    self.logger.debug(bstack11ll111_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦⅭ"))
    bstack1llll1l1l1l1_opy_ = 0
    while self.bstack1llll11l11l1_opy_.poll() == None:
      bstack1llll11l1lll_opy_ = self.bstack1lllll111ll1_opy_()
      if bstack1llll11l1lll_opy_:
        self.logger.debug(bstack11ll111_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢⅮ"))
        self.bstack1llll1l1lll1_opy_ = True
        return True
      bstack1llll1l1l1l1_opy_ += 1
      self.logger.debug(bstack11ll111_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣⅯ").format(bstack1llll1l1l1l1_opy_))
      time.sleep(2)
    self.logger.error(bstack11ll111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦⅰ").format(bstack1llll1l1l1l1_opy_))
    self.bstack1llll11l1l11_opy_ = True
    return False
  def bstack1lllll111ll1_opy_(self, bstack1llll1l1l1l1_opy_ = 0):
    if bstack1llll1l1l1l1_opy_ > 10:
      return False
    try:
      bstack1llll11l1l1l_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧⅱ"), bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩⅲ"))
      bstack1llll1l11l11_opy_ = bstack1llll11l1l1l_opy_ + bstack111ll1lll1l_opy_
      response = requests.get(bstack1llll1l11l11_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨⅳ"), {}).get(bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ⅴ"), None)
      return True
    except:
      self.logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡪࡨࡥࡱࡺࡨࠡࡥ࡫ࡩࡨࡱࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤⅵ"))
      return False
  def bstack1llll1llll11_opy_(self):
    bstack1llll1ll1111_opy_ = bstack11ll111_opy_ (u"ࠬࡧࡰࡱࠩⅶ") if self.bstack1l1111l11_opy_ else bstack11ll111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨⅷ")
    bstack1llll1ll1ll1_opy_ = bstack11ll111_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥⅸ") if self.config.get(bstack11ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧⅹ")) is None else True
    bstack11l111l11l1_opy_ = bstack11ll111_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠧࡲࡨࡶࡨࡿ࠽ࡼࡿࠥⅺ").format(self.config[bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨⅻ")], bstack1llll1ll1111_opy_, bstack1llll1ll1ll1_opy_)
    if self.percy_capture_mode:
      bstack11l111l11l1_opy_ += bstack11ll111_opy_ (u"ࠦࠫࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࡀࡿࢂࠨⅼ").format(self.percy_capture_mode)
    uri = bstack1l1l1111ll_opy_(bstack11l111l11l1_opy_)
    try:
      response = bstack1l1l11ll_opy_(bstack11ll111_opy_ (u"ࠬࡍࡅࡕࠩⅽ"), uri, {}, {bstack11ll111_opy_ (u"࠭ࡡࡶࡶ࡫ࠫⅾ"): (self.config[bstack11ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩⅿ")], self.config[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫↀ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1lll1lllll_opy_ = data.get(bstack11ll111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪↁ"))
        self.percy_capture_mode = data.get(bstack11ll111_opy_ (u"ࠪࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥࠨↂ"))
        os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩↃ")] = str(self.bstack1lll1lllll_opy_)
        os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩↄ")] = str(self.percy_capture_mode)
        if bstack1llll1ll1ll1_opy_ == bstack11ll111_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤↅ") and str(self.bstack1lll1lllll_opy_).lower() == bstack11ll111_opy_ (u"ࠢࡵࡴࡸࡩࠧↆ"):
          self.bstack111ll1lll_opy_ = True
        if bstack11ll111_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢↇ") in data:
          return data[bstack11ll111_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣↈ")]
        else:
          raise bstack11ll111_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪ↉").format(data)
      else:
        raise bstack11ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦ↊").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨ↋").format(e))
  def bstack1llll1l1l11l_opy_(self):
    bstack1llll1lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤ↌"))
    try:
      if bstack11ll111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ↍") not in self.bstack1llll1llllll_opy_:
        self.bstack1llll1llllll_opy_[bstack11ll111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ↎")] = 2
      with open(bstack1llll1lll1ll_opy_, bstack11ll111_opy_ (u"ࠩࡺࠫ↏")) as fp:
        json.dump(self.bstack1llll1llllll_opy_, fp)
      return bstack1llll1lll1ll_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ←").format(e))
  def bstack1llll1l1111l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll11l1111_opy_ == bstack11ll111_opy_ (u"ࠫࡼ࡯࡮ࠨ↑"):
        bstack1lllll1111l1_opy_ = [bstack11ll111_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭→"), bstack11ll111_opy_ (u"࠭࠯ࡤࠩ↓")]
        cmd = bstack1lllll1111l1_opy_ + cmd
      cmd = bstack11ll111_opy_ (u"ࠧࠡࠩ↔").join(cmd)
      self.logger.debug(bstack11ll111_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧ↕").format(cmd))
      with open(self.bstack1llll1l11111_opy_, bstack11ll111_opy_ (u"ࠤࡤࠦ↖")) as bstack1llll1lll11l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll1lll11l_opy_, text=True, stderr=bstack1llll1lll11l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1llll11l1l11_opy_ = True
      self.logger.error(bstack11ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ↗").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llll1l1lll1_opy_:
        self.logger.info(bstack11ll111_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧ↘"))
        cmd = [self.binary_path, bstack11ll111_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣ↙")]
        self.bstack1llll1l1111l_opy_(cmd)
        self.bstack1llll1l1lll1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ↚").format(cmd, e))
  def bstack11111ll1_opy_(self):
    if not self.bstack1lll1lllll_opy_:
      return
    try:
      bstack1llll1ll11ll_opy_ = 0
      while not self.bstack1llll1l1lll1_opy_ and bstack1llll1ll11ll_opy_ < self.bstack1lllll11l111_opy_:
        if self.bstack1llll11l1l11_opy_:
          self.logger.info(bstack11ll111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧ↛"))
          return
        time.sleep(1)
        bstack1llll1ll11ll_opy_ += 1
      os.environ[bstack11ll111_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧ↜")] = str(self.bstack1llll1l11ll1_opy_())
      self.logger.info(bstack11ll111_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥ↝"))
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ↞").format(e))
  def bstack1llll1l11ll1_opy_(self):
    if self.bstack1l1111l11_opy_:
      return
    try:
      bstack1llll111l1ll_opy_ = [platform[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ↟")].lower() for platform in self.config.get(bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ↠"), [])]
      bstack1ll1llll111_opy_ = sys.maxsize
      bstack1llll111l11l_opy_ = bstack11ll111_opy_ (u"࠭ࠧ↡")
      for browser in bstack1llll111l1ll_opy_:
        if browser in self.bstack1llll11lll1l_opy_:
          bstack1llll11ll111_opy_ = self.bstack1llll11lll1l_opy_[browser]
        if bstack1llll11ll111_opy_ < bstack1ll1llll111_opy_:
          bstack1ll1llll111_opy_ = bstack1llll11ll111_opy_
          bstack1llll111l11l_opy_ = browser
      return bstack1llll111l11l_opy_
    except Exception as e:
      self.logger.error(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ↢").format(e))
  @classmethod
  def bstack1lll11ll1l_opy_(self):
    return os.getenv(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭↣"), bstack11ll111_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨ↤")).lower()
  @classmethod
  def bstack11lllllll_opy_(self):
    return os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧ↥"), bstack11ll111_opy_ (u"ࠫࠬ↦"))
  @classmethod
  def bstack1l111l1l1ll_opy_(cls, value):
    cls.bstack111ll1lll_opy_ = value
  @classmethod
  def bstack1llll11llll1_opy_(cls):
    return cls.bstack111ll1lll_opy_
  @classmethod
  def bstack1l111l1llll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1llll1l1ll11_opy_(cls):
    return cls.percy_build_id