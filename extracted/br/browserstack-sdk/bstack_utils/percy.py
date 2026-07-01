# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
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
from bstack_utils.helper import bstack1111ll1111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll11111l1_opy_ import bstack11l11111l1_opy_
class bstack11ll1l1111_opy_:
  working_dir = os.getcwd()
  bstack1ll1111l1l1_opy_ = False
  config = {}
  bstack1lll1l111111_opy_ = bstack1l1llll_opy_ (u"࠭ࠧ⤟")
  binary_path = bstack1l1llll_opy_ (u"ࠧࠨ⤠")
  bstack1ll1l1111ll1_opy_ = bstack1l1llll_opy_ (u"ࠨࠩ⤡")
  bstack111lll1l1l_opy_ = False
  bstack1ll1l11llll1_opy_ = None
  bstack1ll1l11l111l_opy_ = {}
  bstack1ll1l111llll_opy_ = 300
  bstack1ll1l1111l11_opy_ = False
  logger = None
  bstack1ll1l111ll11_opy_ = False
  bstack111l1l1111_opy_ = False
  percy_build_id = None
  bstack1ll11ll1l11l_opy_ = bstack1l1llll_opy_ (u"ࠩࠪ⤢")
  bstack1ll1l11l11ll_opy_ = {
    bstack1l1llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ⤣") : 1,
    bstack1l1llll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ⤤") : 2,
    bstack1l1llll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪ⤥") : 3,
    bstack1l1llll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭⤦") : 4
  }
  def __init__(self) -> None: pass
  def bstack1ll1l11111ll_opy_(self):
    bstack1ll1l1l1111l_opy_ = bstack1l1llll_opy_ (u"ࠧࠨ⤧")
    bstack1ll1l111l11l_opy_ = sys.platform
    bstack1ll11lll1lll_opy_ = bstack1l1llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⤨")
    if re.match(bstack1l1llll_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤ⤩"), bstack1ll1l111l11l_opy_) != None:
      bstack1ll1l1l1111l_opy_ = bstack1llllll1l11l_opy_ + bstack1l1llll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦ⤪")
      self.bstack1ll11ll1l11l_opy_ = bstack1l1llll_opy_ (u"ࠫࡲࡧࡣࠨ⤫")
    elif re.match(bstack1l1llll_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥ⤬"), bstack1ll1l111l11l_opy_) != None:
      bstack1ll1l1l1111l_opy_ = bstack1llllll1l11l_opy_ + bstack1l1llll_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢ⤭")
      bstack1ll11lll1lll_opy_ = bstack1l1llll_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥ⤮")
      self.bstack1ll11ll1l11l_opy_ = bstack1l1llll_opy_ (u"ࠨࡹ࡬ࡲࠬ⤯")
    else:
      bstack1ll1l1l1111l_opy_ = bstack1llllll1l11l_opy_ + bstack1l1llll_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧ⤰")
      self.bstack1ll11ll1l11l_opy_ = bstack1l1llll_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩ⤱")
    return bstack1ll1l1l1111l_opy_, bstack1ll11lll1lll_opy_
  def bstack1ll1l1l111l1_opy_(self):
    try:
      bstack1ll1l11ll1ll_opy_ = [os.path.join(expanduser(bstack1l1llll_opy_ (u"ࠦࢃࠨ⤲")), bstack1l1llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⤳")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1ll1l11ll1ll_opy_:
        if(self.bstack1ll1l11l1l1l_opy_(path)):
          return path
      raise bstack1l1llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥ⤴")
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤ⤵").format(e))
  def bstack1ll1l11l1l1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except Exception as e:
      if self.logger:
        self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡲࡨࡶࡨࡿࠠ࡮ࡣ࡮ࡩࡤࡶࡡࡵࡪࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃ࠺ࠡࡽࢀࠦ⤶").format(type(e).__name__, e), exc_info=True)
      return False
  def bstack1ll1l11l1l11_opy_(self, bstack1ll11ll11l1l_opy_):
    return os.path.join(bstack1ll11ll11l1l_opy_, self.bstack1lll1l111111_opy_ + bstack1l1llll_opy_ (u"ࠤ࠱ࡩࡹࡧࡧࠣ⤷"))
  def bstack1ll11llll1l1_opy_(self, bstack1ll11ll11l1l_opy_, bstack1ll1l111l1ll_opy_):
    if not bstack1ll1l111l1ll_opy_: return
    try:
      bstack1ll11ll1ll11_opy_ = self.bstack1ll1l11l1l11_opy_(bstack1ll11ll11l1l_opy_)
      with open(bstack1ll11ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠥࡻࠧ⤸")) as f:
        f.write(bstack1ll1l111l1ll_opy_)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡘࡧࡶࡦࡦࠣࡲࡪࡽࠠࡆࡖࡤ࡫ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠣ⤹"))
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡴࡩࡧࠣࡩࡹࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ⤺").format(e))
  def bstack1ll1l111111l_opy_(self, bstack1ll11ll11l1l_opy_):
    try:
      bstack1ll11ll1ll11_opy_ = self.bstack1ll1l11l1l11_opy_(bstack1ll11ll11l1l_opy_)
      if os.path.exists(bstack1ll11ll1ll11_opy_):
        with open(bstack1ll11ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠨࡲࠣ⤻")) as f:
          bstack1ll1l111l1ll_opy_ = f.read().strip()
          return bstack1ll1l111l1ll_opy_ if bstack1ll1l111l1ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠ࡭ࡱࡤࡨ࡮ࡴࡧࠡࡇࡗࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ⤼").format(e))
  def bstack1ll11lll11ll_opy_(self, bstack1ll11ll11l1l_opy_, bstack1ll1l1l1111l_opy_):
    bstack1ll1l111lll1_opy_ = self.bstack1ll1l111111l_opy_(bstack1ll11ll11l1l_opy_)
    if bstack1ll1l111lll1_opy_:
      try:
        bstack1ll1l11ll11l_opy_ = self.bstack1ll1l1l11111_opy_(bstack1ll1l111lll1_opy_, bstack1ll1l1l1111l_opy_)
        if not bstack1ll1l11ll11l_opy_:
          self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡵࠣࡹࡵࠦࡴࡰࠢࡧࡥࡹ࡫ࠠࠩࡇࡗࡥ࡬ࠦࡵ࡯ࡥ࡫ࡥࡳ࡭ࡥࡥࠫࠥ⤽"))
          return True
        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡑࡩࡼࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡥࠣ⤾"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡬࡯ࡳࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤ⤿").format(e))
    return False
  def bstack1ll1l1l11111_opy_(self, bstack1ll1l111lll1_opy_, bstack1ll1l1l1111l_opy_):
    try:
      headers = {
        bstack1l1llll_opy_ (u"ࠦࡎ࡬࠭ࡏࡱࡱࡩ࠲ࡓࡡࡵࡥ࡫ࠦ⥀"): bstack1ll1l111lll1_opy_
      }
      response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠬࡍࡅࡕࠩ⥁"), bstack1ll1l1l1111l_opy_, {}, {bstack1l1llll_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢ⥂"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1llll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠿ࠦࡻࡾࠤ⥃").format(e))
  @measure(event_name=EVENTS.bstack1llllllll1l1_opy_, stage=STAGE.SINGLE)
  def bstack1ll11lll1l1l_opy_(self, bstack1ll1l1l1111l_opy_, bstack1ll11lll1lll_opy_):
    try:
      bstack1ll1l111l111_opy_ = self.bstack1ll1l1l111l1_opy_()
      bstack1ll1l11ll1l1_opy_ = os.path.join(bstack1ll1l111l111_opy_, bstack1l1llll_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫ⥄"))
      bstack1ll11ll1l1l1_opy_ = os.path.join(bstack1ll1l111l111_opy_, bstack1ll11lll1lll_opy_)
      if self.bstack1ll11lll11ll_opy_(bstack1ll1l111l111_opy_, bstack1ll1l1l1111l_opy_): # if true, bstack11l11lll11l_opy_ bstack1ll1l111l1ll_opy_ is bstack1ll11lllll11_opy_ to bstack1lll1llll1ll_opy_ version available (response 304)
        if os.path.exists(bstack1ll11ll1l1l1_opy_):
          self.logger.info(bstack1l1llll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦ⥅").format(bstack1ll11ll1l1l1_opy_))
          return bstack1ll11ll1l1l1_opy_
        if os.path.exists(bstack1ll1l11ll1l1_opy_):
          self.logger.info(bstack1l1llll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣ⥆").format(bstack1ll1l11ll1l1_opy_))
          return self.bstack1ll11lll11l1_opy_(bstack1ll1l11ll1l1_opy_, bstack1ll11lll1lll_opy_)
      self.logger.info(bstack1l1llll_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤ⥇").format(bstack1ll1l1l1111l_opy_))
      response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠬࡍࡅࡕࠩ⥈"), bstack1ll1l1l1111l_opy_, {}, {})
      if response.status_code == 200:
        bstack1ll11ll1ll1l_opy_ = response.headers.get(bstack1l1llll_opy_ (u"ࠨࡅࡕࡣࡪࠦ⥉"), bstack1l1llll_opy_ (u"ࠢࠣ⥊"))
        if bstack1ll11ll1ll1l_opy_:
          self.bstack1ll11llll1l1_opy_(bstack1ll1l111l111_opy_, bstack1ll11ll1ll1l_opy_)
        with open(bstack1ll1l11ll1l1_opy_, bstack1l1llll_opy_ (u"ࠨࡹࡥࠫ⥋")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1llll_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢ⥌").format(bstack1ll1l11ll1l1_opy_))
        return self.bstack1ll11lll11l1_opy_(bstack1ll1l11ll1l1_opy_, bstack1ll11lll1lll_opy_)
      else:
        raise(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨ⥍").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧ⥎").format(e))
  def bstack1ll11lll1ll1_opy_(self, bstack1ll1l1l1111l_opy_, bstack1ll11lll1lll_opy_):
    try:
      retry = 2
      bstack1ll11ll1l1l1_opy_ = None
      bstack1ll11llll11l_opy_ = False
      while retry > 0:
        bstack1ll11ll1l1l1_opy_ = self.bstack1ll11lll1l1l_opy_(bstack1ll1l1l1111l_opy_, bstack1ll11lll1lll_opy_)
        bstack1ll11llll11l_opy_ = self.bstack1ll1l1111111_opy_(bstack1ll1l1l1111l_opy_, bstack1ll11lll1lll_opy_, bstack1ll11ll1l1l1_opy_)
        if bstack1ll11llll11l_opy_:
          break
        retry -= 1
      return bstack1ll11ll1l1l1_opy_, bstack1ll11llll11l_opy_
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤ⥏").format(e))
    return bstack1ll11ll1l1l1_opy_, False
  def bstack1ll1l1111111_opy_(self, bstack1ll1l1l1111l_opy_, bstack1ll11lll1lll_opy_, bstack1ll11ll1l1l1_opy_, bstack1ll11ll11l11_opy_ = 0):
    if bstack1ll11ll11l11_opy_ > 1:
      return False
    if bstack1ll11ll1l1l1_opy_ == None or os.path.exists(bstack1ll11ll1l1l1_opy_) == False:
      self.logger.warn(bstack1l1llll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦ⥐"))
      return False
    command = bstack1l1llll_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭⥑").format(bstack1ll11ll1l1l1_opy_)
    bstack1ll1l11lll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack1l1llll_opy_ (u"ࠨࡂࡳࡩࡷࡩࡹ࠰ࡥ࡯࡭ࠬ⥒") in bstack1ll1l11lll11_opy_:
      return True
    else:
      self.logger.error(bstack1l1llll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣ⥓"))
      return False
  def bstack1ll11lll11l1_opy_(self, bstack1ll1l11ll1l1_opy_, bstack1ll11lll1lll_opy_):
    try:
      working_dir = os.path.dirname(bstack1ll1l11ll1l1_opy_)
      shutil.unpack_archive(bstack1ll1l11ll1l1_opy_, working_dir)
      bstack1ll11ll1l1l1_opy_ = os.path.join(working_dir, bstack1ll11lll1lll_opy_)
      os.chmod(bstack1ll11ll1l1l1_opy_, 0o755)
      return bstack1ll11ll1l1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦ⥔"))
  def bstack1ll1l11l1111_opy_(self):
    try:
      bstack1ll1l11lllll_opy_ = self.config.get(bstack1l1llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⥕"))
      bstack1ll1l11l1111_opy_ = bstack1ll1l11lllll_opy_ or (bstack1ll1l11lllll_opy_ is None and self.bstack1ll1111l1l1_opy_)
      if not bstack1ll1l11l1111_opy_ or self.config.get(bstack1l1llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⥖"), None) not in bstack111111l1111_opy_:
        return False
      self.bstack111lll1l1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⥗").format(e))
  def bstack1ll11ll1l111_opy_(self):
    try:
      bstack1ll11ll1l111_opy_ = self.percy_capture_mode
      return bstack1ll11ll1l111_opy_
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⥘").format(e))
  def init(self, bstack1ll1111l1l1_opy_, config, logger):
    self.bstack1ll1111l1l1_opy_ = bstack1ll1111l1l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1ll1l11l1111_opy_():
      return
    self.bstack1ll1l11l111l_opy_ = config.get(bstack1l1llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⥙"), {})
    self.percy_capture_mode = config.get(bstack1l1llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬ⥚"))
    try:
      bstack1ll1l1l1111l_opy_, bstack1ll11lll1lll_opy_ = self.bstack1ll1l11111ll_opy_()
      self.bstack1lll1l111111_opy_ = bstack1ll11lll1lll_opy_
      bstack1ll11ll1l1l1_opy_, bstack1ll11llll11l_opy_ = self.bstack1ll11lll1ll1_opy_(bstack1ll1l1l1111l_opy_, bstack1ll11lll1lll_opy_)
      if bstack1ll11llll11l_opy_:
        self.binary_path = bstack1ll11ll1l1l1_opy_
        thread = Thread(target=self.bstack1ll11ll1l1ll_opy_)
        thread.start()
      else:
        self.bstack1ll1l111ll11_opy_ = True
        self.logger.error(bstack1l1llll_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢ⥛").format(bstack1ll11ll1l1l1_opy_))
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ⥜").format(e))
  def bstack1ll1l11ll111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡨࠩ⥝"), bstack1l1llll_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩ⥞"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦ⥟").format(logfile))
      self.bstack1ll1l1111ll1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ⥠").format(e))
  @measure(event_name=EVENTS.bstack1llllllll1ll_opy_, stage=STAGE.SINGLE)
  def bstack1ll11ll1l1ll_opy_(self):
    bstack1ll11lllllll_opy_ = self.bstack1ll11llll111_opy_()
    if bstack1ll11lllllll_opy_ == None:
      self.bstack1ll1l111ll11_opy_ = True
      self.logger.error(bstack1l1llll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧ⥡"))
      return False
    bstack1ll11ll11lll_opy_ = [bstack1l1llll_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦ⥢") if self.bstack1ll1111l1l1_opy_ else bstack1l1llll_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨ⥣")]
    bstack1l11l1l1l_opy_ = self.bstack1ll11lllll1l_opy_()
    if bstack1l11l1l1l_opy_ != None:
      bstack1ll11ll11lll_opy_.append(bstack1l1llll_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦ⥤").format(bstack1l11l1l1l_opy_))
    env = os.environ.copy()
    env[bstack1l1llll_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦ⥥")] = bstack1ll11lllllll_opy_
    env[bstack1l1llll_opy_ (u"ࠢࡕࡊࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠢ⥦")] = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⥧"), bstack1l1llll_opy_ (u"ࠩࠪ⥨"))
    bstack1ll11ll1llll_opy_ = [self.binary_path]
    self.bstack1ll1l11ll111_opy_()
    self.bstack1ll1l11llll1_opy_ = self.bstack1ll1l1111lll_opy_(bstack1ll11ll1llll_opy_ + bstack1ll11ll11lll_opy_, env)
    self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦ⥩"))
    bstack1ll11ll11l11_opy_ = 0
    while self.bstack1ll1l11llll1_opy_.poll() == None:
      bstack1ll1l11lll1l_opy_ = self.bstack1ll11ll1lll1_opy_()
      if bstack1ll1l11lll1l_opy_:
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢ⥪"))
        self.bstack1ll1l1111l11_opy_ = True
        return True
      bstack1ll11ll11l11_opy_ += 1
      self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣ⥫").format(bstack1ll11ll11l11_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦ⥬").format(bstack1ll11ll11l11_opy_))
    self.bstack1ll1l111ll11_opy_ = True
    return False
  def bstack1ll11ll1lll1_opy_(self, bstack1ll11ll11l11_opy_ = 0):
    if bstack1ll11ll11l11_opy_ > 10:
      return False
    try:
      bstack1ll1l1111l1l_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧ⥭"), bstack1l1llll_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩ⥮"))
      bstack1ll11ll11ll1_opy_ = bstack1ll1l1111l1l_opy_ + bstack1llllll1llll_opy_
      response = requests.get(bstack1ll11ll11ll1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨ⥯"), {}).get(bstack1l1llll_opy_ (u"ࠪ࡭ࡩ࠭⥰"), None)
      return True
    except Exception as e:
      self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡪࡨࡥࡱࡺࡨࠡࡥ࡫ࡩࡨࡱࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࡀࠠࡼࡿࠥ⥱").format(type(e).__name__, e))
      return False
  def bstack1ll11llll111_opy_(self):
    bstack1ll11llllll1_opy_ = bstack1l1llll_opy_ (u"ࠬࡧࡰࡱࠩ⥲") if self.bstack1ll1111l1l1_opy_ else bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⥳")
    bstack1ll1l11l1lll_opy_ = bstack1l1llll_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥ⥴") if self.config.get(bstack1l1llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⥵")) is None else True
    bstack11111l11lll_opy_ = bstack1l1llll_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠧࡲࡨࡶࡨࡿ࠽ࡼࡿࠥ⥶").format(self.config[bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⥷")], bstack1ll11llllll1_opy_, bstack1ll1l11l1lll_opy_)
    if self.percy_capture_mode:
      bstack11111l11lll_opy_ += bstack1l1llll_opy_ (u"ࠦࠫࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࡀࡿࢂࠨ⥸").format(self.percy_capture_mode)
    uri = bstack11l11111l1_opy_(bstack11111l11lll_opy_)
    try:
      response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠬࡍࡅࡕࠩ⥹"), uri, {}, {bstack1l1llll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ⥺"): (self.config[bstack1l1llll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ⥻")], self.config[bstack1l1llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ⥼")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack111lll1l1l_opy_ = data.get(bstack1l1llll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ⥽"))
        self.percy_capture_mode = data.get(bstack1l1llll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥࠨ⥾"))
        os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩ⥿")] = str(self.bstack111lll1l1l_opy_)
        os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩ⦀")] = str(self.percy_capture_mode)
        if bstack1ll1l11l1lll_opy_ == bstack1l1llll_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤ⦁") and str(self.bstack111lll1l1l_opy_).lower() == bstack1l1llll_opy_ (u"ࠢࡵࡴࡸࡩࠧ⦂"):
          self.bstack111l1l1111_opy_ = True
        if bstack1l1llll_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢ⦃") in data:
          return data[bstack1l1llll_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣ⦄")]
        else:
          raise bstack1l1llll_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪ⦅").format(data)
      else:
        raise bstack1l1llll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦ⦆").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨ⦇").format(e))
  def bstack1ll11lllll1l_opy_(self):
    bstack1ll11lll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤ⦈"))
    try:
      if bstack1l1llll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⦉") not in self.bstack1ll1l11l111l_opy_:
        self.bstack1ll1l11l111l_opy_[bstack1l1llll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ⦊")] = 2
      with open(bstack1ll11lll111l_opy_, bstack1l1llll_opy_ (u"ࠩࡺࠫ⦋")) as fp:
        json.dump(self.bstack1ll1l11l111l_opy_, fp)
      return bstack1ll11lll111l_opy_
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ⦌").format(e))
  def bstack1ll1l1111lll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1ll11ll1l11l_opy_ == bstack1l1llll_opy_ (u"ࠫࡼ࡯࡮ࠨ⦍"):
        bstack1ll1l111l1l1_opy_ = [bstack1l1llll_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭⦎"), bstack1l1llll_opy_ (u"࠭࠯ࡤࠩ⦏")]
        cmd = bstack1ll1l111l1l1_opy_ + cmd
      cmd = bstack1l1llll_opy_ (u"ࠧࠡࠩ⦐").join(cmd)
      self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧ⦑").format(cmd))
      with open(self.bstack1ll1l1111ll1_opy_, bstack1l1llll_opy_ (u"ࠤࡤࠦ⦒")) as bstack1ll1l11111l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1ll1l11111l1_opy_, text=True, stderr=bstack1ll1l11111l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1ll1l111ll11_opy_ = True
      self.logger.error(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ⦓").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1ll1l1111l11_opy_:
        self.logger.info(bstack1l1llll_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧ⦔"))
        cmd = [self.binary_path, bstack1l1llll_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣ⦕")]
        self.bstack1ll1l1111lll_opy_(cmd)
        self.bstack1ll1l1111l11_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ⦖").format(cmd, e))
  def bstack1lllll111ll_opy_(self):
    if not self.bstack111lll1l1l_opy_:
      return
    try:
      bstack1ll1l11l11l1_opy_ = 0
      while not self.bstack1ll1l1111l11_opy_ and bstack1ll1l11l11l1_opy_ < self.bstack1ll1l111llll_opy_:
        if self.bstack1ll1l111ll11_opy_:
          self.logger.info(bstack1l1llll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧ⦗"))
          return
        time.sleep(1)
        bstack1ll1l11l11l1_opy_ += 1
      os.environ[bstack1l1llll_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧ⦘")] = str(self.bstack1ll11ll111ll_opy_())
      self.logger.info(bstack1l1llll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥ⦙"))
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ⦚").format(e))
  def bstack1ll11ll111ll_opy_(self):
    if self.bstack1ll1111l1l1_opy_:
      return
    try:
      bstack1ll11llll1ll_opy_ = [platform[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ⦛")].lower() for platform in self.config.get(bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⦜"), [])]
      bstack1l11lll1l1l_opy_ = sys.maxsize
      bstack1ll1l111ll1l_opy_ = bstack1l1llll_opy_ (u"࠭ࠧ⦝")
      for browser in bstack1ll11llll1ll_opy_:
        if browser in self.bstack1ll1l11l11ll_opy_:
          bstack1ll1l11l1ll1_opy_ = self.bstack1ll1l11l11ll_opy_[browser]
        if bstack1ll1l11l1ll1_opy_ < bstack1l11lll1l1l_opy_:
          bstack1l11lll1l1l_opy_ = bstack1ll1l11l1ll1_opy_
          bstack1ll1l111ll1l_opy_ = browser
      return bstack1ll1l111ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⦞").format(e))
  @classmethod
  def bstack1lll11llll1_opy_(self):
    return os.getenv(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭⦟"), bstack1l1llll_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨ⦠")).lower()
  @classmethod
  def bstack1l1ll1l1lll_opy_(self):
    return os.getenv(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧ⦡"), bstack1l1llll_opy_ (u"ࠫࠬ⦢"))
  @classmethod
  def bstack11l1l1l1l1l_opy_(cls, value):
    cls.bstack111l1l1111_opy_ = value
  @classmethod
  def bstack1ll11lll1111_opy_(cls):
    return cls.bstack111l1l1111_opy_
  @classmethod
  def bstack11l1l1lll11_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1ll11lll1l11_opy_(cls):
    return cls.percy_build_id