# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
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
from bstack_utils.helper import bstack11llll11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll11l11l_opy_ import bstack1111ll1ll1_opy_
class bstack11ll111l1l_opy_:
  working_dir = os.getcwd()
  bstack111l1lll1_opy_ = False
  config = {}
  bstack1lllll1111ll_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫ╤")
  binary_path = bstack1ll1l11_opy_ (u"ࠫࠬ╥")
  bstack1ll1ll11l11l_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭╦")
  bstack1l1lll11l_opy_ = False
  bstack1ll1ll1l1111_opy_ = None
  bstack1ll1ll1llll1_opy_ = {}
  bstack1lll11111111_opy_ = 300
  bstack1lll111111l1_opy_ = False
  logger = None
  bstack1ll1ll1l11l1_opy_ = False
  bstack111ll111_opy_ = False
  percy_build_id = None
  bstack1ll1llll1l1l_opy_ = bstack1ll1l11_opy_ (u"࠭ࠧ╧")
  bstack1ll1lll11111_opy_ = {
    bstack1ll1l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ╨") : 1,
    bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ╩") : 2,
    bstack1ll1l11_opy_ (u"ࠩࡨࡨ࡬࡫ࠧ╪") : 3,
    bstack1ll1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ╫") : 4
  }
  def __init__(self) -> None: pass
  def bstack1ll1ll1lllll_opy_(self):
    bstack1ll1lll11l1l_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬ╬")
    bstack1ll1lll1l111_opy_ = sys.platform
    bstack1ll1llll1l11_opy_ = bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ╭")
    if re.match(bstack1ll1l11_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨ╮"), bstack1ll1lll1l111_opy_) != None:
      bstack1ll1lll11l1l_opy_ = bstack11111l11111_opy_ + bstack1ll1l11_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣ╯")
      self.bstack1ll1llll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠨ࡯ࡤࡧࠬ╰")
    elif re.match(bstack1ll1l11_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢ╱"), bstack1ll1lll1l111_opy_) != None:
      bstack1ll1lll11l1l_opy_ = bstack11111l11111_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳࠦ╲")
      bstack1ll1llll1l11_opy_ = bstack1ll1l11_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢ╳")
      self.bstack1ll1llll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠬࡽࡩ࡯ࠩ╴")
    else:
      bstack1ll1lll11l1l_opy_ = bstack11111l11111_opy_ + bstack1ll1l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤ╵")
      self.bstack1ll1llll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭╶")
    return bstack1ll1lll11l1l_opy_, bstack1ll1llll1l11_opy_
  def bstack1ll1ll1ll1ll_opy_(self):
    try:
      bstack1ll1lll1l1ll_opy_ = [os.path.join(expanduser(bstack1ll1l11_opy_ (u"ࠣࢀࠥ╷")), bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ╸")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1ll1lll1l1ll_opy_:
        if(self.bstack1ll1llll1lll_opy_(path)):
          return path
      raise bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢ╹")
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨ╺").format(e))
  def bstack1ll1llll1lll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1ll1llll111l_opy_(self, bstack1ll1ll1l1l1l_opy_):
    return os.path.join(bstack1ll1ll1l1l1l_opy_, self.bstack1lllll1111ll_opy_ + bstack1ll1l11_opy_ (u"ࠧ࠴ࡥࡵࡣࡪࠦ╻"))
  def bstack1ll1lllllll1_opy_(self, bstack1ll1ll1l1l1l_opy_, bstack1ll1ll11l1ll_opy_):
    if not bstack1ll1ll11l1ll_opy_: return
    try:
      bstack1ll1ll1l111l_opy_ = self.bstack1ll1llll111l_opy_(bstack1ll1ll1l1l1l_opy_)
      with open(bstack1ll1ll1l111l_opy_, bstack1ll1l11_opy_ (u"ࠨࡷࠣ╼")) as f:
        f.write(bstack1ll1ll11l1ll_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡔࡣࡹࡩࡩࠦ࡮ࡦࡹࠣࡉ࡙ࡧࡧࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠦ╽"))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡷ࡬ࡪࠦࡥࡵࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ╾").format(e))
  def bstack1ll1lllll11l_opy_(self, bstack1ll1ll1l1l1l_opy_):
    try:
      bstack1ll1ll1l111l_opy_ = self.bstack1ll1llll111l_opy_(bstack1ll1ll1l1l1l_opy_)
      if os.path.exists(bstack1ll1ll1l111l_opy_):
        with open(bstack1ll1ll1l111l_opy_, bstack1ll1l11_opy_ (u"ࠤࡵࠦ╿")) as f:
          bstack1ll1ll11l1ll_opy_ = f.read().strip()
          return bstack1ll1ll11l1ll_opy_ if bstack1ll1ll11l1ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡰࡴࡧࡤࡪࡰࡪࠤࡊ࡚ࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ▀").format(e))
  def bstack1ll1lll1l1l1_opy_(self, bstack1ll1ll1l1l1l_opy_, bstack1ll1lll11l1l_opy_):
    bstack1ll1ll11lll1_opy_ = self.bstack1ll1lllll11l_opy_(bstack1ll1ll1l1l1l_opy_)
    if bstack1ll1ll11lll1_opy_:
      try:
        bstack1ll1lll111l1_opy_ = self.bstack1ll1lll11ll1_opy_(bstack1ll1ll11lll1_opy_, bstack1ll1lll11l1l_opy_)
        if not bstack1ll1lll111l1_opy_:
          self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡸࠦࡵࡱࠢࡷࡳࠥࡪࡡࡵࡧࠣࠬࡊ࡚ࡡࡨࠢࡸࡲࡨ࡮ࡡ࡯ࡩࡨࡨ࠮ࠨ▁"))
          return True
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡔࡥࡸࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡺࡶࡤࡢࡶࡨࠦ▂"))
        return False
      except Exception as e:
        self.logger.warn(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡲࡶࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧ▃").format(e))
    return False
  def bstack1ll1lll11ll1_opy_(self, bstack1ll1ll11lll1_opy_, bstack1ll1lll11l1l_opy_):
    try:
      headers = {
        bstack1ll1l11_opy_ (u"ࠢࡊࡨ࠰ࡒࡴࡴࡥ࠮ࡏࡤࡸࡨ࡮ࠢ▄"): bstack1ll1ll11lll1_opy_
      }
      response = bstack11llll11ll_opy_(bstack1ll1l11_opy_ (u"ࠨࡉࡈࡘࠬ▅"), bstack1ll1lll11l1l_opy_, {}, {bstack1ll1l11_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥ▆"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠻ࠢࡾࢁࠧ▇").format(e))
  @measure(event_name=EVENTS.bstack111111lll11_opy_, stage=STAGE.bstack1ll11l11_opy_)
  def bstack1lll1111111l_opy_(self, bstack1ll1lll11l1l_opy_, bstack1ll1llll1l11_opy_):
    try:
      bstack1ll1ll1l1ll1_opy_ = self.bstack1ll1ll1ll1ll_opy_()
      bstack1ll1lll1ll1l_opy_ = os.path.join(bstack1ll1ll1l1ll1_opy_, bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧ█"))
      bstack1ll1ll1ll11l_opy_ = os.path.join(bstack1ll1ll1l1ll1_opy_, bstack1ll1llll1l11_opy_)
      if self.bstack1ll1lll1l1l1_opy_(bstack1ll1ll1l1ll1_opy_, bstack1ll1lll11l1l_opy_): # if true, bstack11l1llll11l_opy_ bstack1ll1ll11l1ll_opy_ is bstack1ll1ll11l1l1_opy_ to bstack1llll1ll11ll_opy_ version available (response 304)
        if os.path.exists(bstack1ll1ll1ll11l_opy_):
          self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ▉").format(bstack1ll1ll1ll11l_opy_))
          return bstack1ll1ll1ll11l_opy_
        if os.path.exists(bstack1ll1lll1ll1l_opy_):
          self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦ▊").format(bstack1ll1lll1ll1l_opy_))
          return self.bstack1ll1lll1111l_opy_(bstack1ll1lll1ll1l_opy_, bstack1ll1llll1l11_opy_)
      self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧ▋").format(bstack1ll1lll11l1l_opy_))
      response = bstack11llll11ll_opy_(bstack1ll1l11_opy_ (u"ࠨࡉࡈࡘࠬ▌"), bstack1ll1lll11l1l_opy_, {}, {})
      if response.status_code == 200:
        bstack1ll1ll1l1l11_opy_ = response.headers.get(bstack1ll1l11_opy_ (u"ࠤࡈࡘࡦ࡭ࠢ▍"), bstack1ll1l11_opy_ (u"ࠥࠦ▎"))
        if bstack1ll1ll1l1l11_opy_:
          self.bstack1ll1lllllll1_opy_(bstack1ll1ll1l1ll1_opy_, bstack1ll1ll1l1l11_opy_)
        with open(bstack1ll1lll1ll1l_opy_, bstack1ll1l11_opy_ (u"ࠫࡼࡨࠧ▏")) as file:
          file.write(response.content)
        self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥ▐").format(bstack1ll1lll1ll1l_opy_))
        return self.bstack1ll1lll1111l_opy_(bstack1ll1lll1ll1l_opy_, bstack1ll1llll1l11_opy_)
      else:
        raise(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤ░").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣ▒").format(e))
  def bstack1ll1lll1ll11_opy_(self, bstack1ll1lll11l1l_opy_, bstack1ll1llll1l11_opy_):
    try:
      retry = 2
      bstack1ll1ll1ll11l_opy_ = None
      bstack1ll1llllllll_opy_ = False
      while retry > 0:
        bstack1ll1ll1ll11l_opy_ = self.bstack1lll1111111l_opy_(bstack1ll1lll11l1l_opy_, bstack1ll1llll1l11_opy_)
        bstack1ll1llllllll_opy_ = self.bstack1ll1lllll111_opy_(bstack1ll1lll11l1l_opy_, bstack1ll1llll1l11_opy_, bstack1ll1ll1ll11l_opy_)
        if bstack1ll1llllllll_opy_:
          break
        retry -= 1
      return bstack1ll1ll1ll11l_opy_, bstack1ll1llllllll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧ▓").format(e))
    return bstack1ll1ll1ll11l_opy_, False
  def bstack1ll1lllll111_opy_(self, bstack1ll1lll11l1l_opy_, bstack1ll1llll1l11_opy_, bstack1ll1ll1ll11l_opy_, bstack1ll1llll1111_opy_ = 0):
    if bstack1ll1llll1111_opy_ > 1:
      return False
    if bstack1ll1ll1ll11l_opy_ == None or os.path.exists(bstack1ll1ll1ll11l_opy_) == False:
      self.logger.warn(bstack1ll1l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢ▔"))
      return False
    command = bstack1ll1l11_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩ▕").format(bstack1ll1ll1ll11l_opy_)
    bstack1ll1llllll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack1ll1l11_opy_ (u"ࠫࡅࡶࡥࡳࡥࡼ࠳ࡨࡲࡩࠨ▖") in bstack1ll1llllll11_opy_:
      return True
    else:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦ▗"))
      return False
  def bstack1ll1lll1111l_opy_(self, bstack1ll1lll1ll1l_opy_, bstack1ll1llll1l11_opy_):
    try:
      working_dir = os.path.dirname(bstack1ll1lll1ll1l_opy_)
      shutil.unpack_archive(bstack1ll1lll1ll1l_opy_, working_dir)
      bstack1ll1ll1ll11l_opy_ = os.path.join(working_dir, bstack1ll1llll1l11_opy_)
      os.chmod(bstack1ll1ll1ll11l_opy_, 0o755)
      return bstack1ll1ll1ll11l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢ▘"))
  def bstack1ll1ll1l11ll_opy_(self):
    try:
      bstack1lll11111l1l_opy_ = self.config.get(bstack1ll1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭▙"))
      bstack1ll1ll1l11ll_opy_ = bstack1lll11111l1l_opy_ or (bstack1lll11111l1l_opy_ is None and self.bstack111l1lll1_opy_)
      if not bstack1ll1ll1l11ll_opy_ or self.config.get(bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ▚"), None) not in bstack111111ll11l_opy_:
        return False
      self.bstack1l1lll11l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ▛").format(e))
  def bstack1ll1lll111ll_opy_(self):
    try:
      bstack1ll1lll111ll_opy_ = self.percy_capture_mode
      return bstack1ll1lll111ll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ▜").format(e))
  def init(self, bstack111l1lll1_opy_, config, logger):
    self.bstack111l1lll1_opy_ = bstack111l1lll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1ll1ll1l11ll_opy_():
      return
    self.bstack1ll1ll1llll1_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ▝"), {})
    self.percy_capture_mode = config.get(bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ▞"))
    try:
      bstack1ll1lll11l1l_opy_, bstack1ll1llll1l11_opy_ = self.bstack1ll1ll1lllll_opy_()
      self.bstack1lllll1111ll_opy_ = bstack1ll1llll1l11_opy_
      bstack1ll1ll1ll11l_opy_, bstack1ll1llllllll_opy_ = self.bstack1ll1lll1ll11_opy_(bstack1ll1lll11l1l_opy_, bstack1ll1llll1l11_opy_)
      if bstack1ll1llllllll_opy_:
        self.binary_path = bstack1ll1ll1ll11l_opy_
        thread = Thread(target=self.bstack1ll1lllll1l1_opy_)
        thread.start()
      else:
        self.bstack1ll1ll1l11l1_opy_ = True
        self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻࠥ▟").format(bstack1ll1ll1ll11l_opy_))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ■").format(e))
  def bstack1ll1ll11l111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬ□"), bstack1ll1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫ࠬ▢"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢ▣").format(logfile))
      self.bstack1ll1ll11l11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ▤").format(e))
  @measure(event_name=EVENTS.bstack11111l1111l_opy_, stage=STAGE.bstack1ll11l11_opy_)
  def bstack1ll1lllll1l1_opy_(self):
    bstack1ll1llll1ll1_opy_ = self.bstack1ll1lll1llll_opy_()
    if bstack1ll1llll1ll1_opy_ == None:
      self.bstack1ll1ll1l11l1_opy_ = True
      self.logger.error(bstack1ll1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠣ▥"))
      return False
    bstack1lll11111ll1_opy_ = [bstack1ll1l11_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢ▦") if self.bstack111l1lll1_opy_ else bstack1ll1l11_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠫ▧")]
    bstack1ll1l11ll11_opy_ = self.bstack1ll1lllll1ll_opy_()
    if bstack1ll1l11ll11_opy_ != None:
      bstack1lll11111ll1_opy_.append(bstack1ll1l11_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢ▨").format(bstack1ll1l11ll11_opy_))
    env = os.environ.copy()
    env[bstack1ll1l11_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢ▩")] = bstack1ll1llll1ll1_opy_
    env[bstack1ll1l11_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥ▪")] = os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ▫"), bstack1ll1l11_opy_ (u"ࠬ࠭▬"))
    bstack1ll1lll1lll1_opy_ = [self.binary_path]
    self.bstack1ll1ll11l111_opy_()
    self.bstack1ll1ll1l1111_opy_ = self.bstack1ll1ll11ll1l_opy_(bstack1ll1lll1lll1_opy_ + bstack1lll11111ll1_opy_, env)
    self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢ▭"))
    bstack1ll1llll1111_opy_ = 0
    while self.bstack1ll1ll1l1111_opy_.poll() == None:
      bstack1ll1llllll1l_opy_ = self.bstack1ll1ll1ll1l1_opy_()
      if bstack1ll1llllll1l_opy_:
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥ▮"))
        self.bstack1lll111111l1_opy_ = True
        return True
      bstack1ll1llll1111_opy_ += 1
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦ▯").format(bstack1ll1llll1111_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢ▰").format(bstack1ll1llll1111_opy_))
    self.bstack1ll1ll1l11l1_opy_ = True
    return False
  def bstack1ll1ll1ll1l1_opy_(self, bstack1ll1llll1111_opy_ = 0):
    if bstack1ll1llll1111_opy_ > 10:
      return False
    try:
      bstack1ll1ll1ll111_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪ▱"), bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬ▲"))
      bstack1ll1llll11l1_opy_ = bstack1ll1ll1ll111_opy_ + bstack11111l1ll11_opy_
      response = requests.get(bstack1ll1llll11l1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫ△"), {}).get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩ▴"), None)
      return True
    except:
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧ▵"))
      return False
  def bstack1ll1lll1llll_opy_(self):
    bstack1lll11111lll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࠬ▶") if self.bstack111l1lll1_opy_ else bstack1ll1l11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ▷")
    bstack1ll1ll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨ▸") if self.config.get(bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ▹")) is None else True
    bstack1111l1l1111_opy_ = bstack1ll1l11_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨ►").format(self.config[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ▻")], bstack1lll11111lll_opy_, bstack1ll1ll11ll11_opy_)
    if self.percy_capture_mode:
      bstack1111l1l1111_opy_ += bstack1ll1l11_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤ▼").format(self.percy_capture_mode)
    uri = bstack1111ll1ll1_opy_(bstack1111l1l1111_opy_)
    try:
      response = bstack11llll11ll_opy_(bstack1ll1l11_opy_ (u"ࠨࡉࡈࡘࠬ▽"), uri, {}, {bstack1ll1l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ▾"): (self.config[bstack1ll1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ▿")], self.config[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ◀")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l1lll11l_opy_ = data.get(bstack1ll1l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭◁"))
        self.percy_capture_mode = data.get(bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫ◂"))
        os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬ◃")] = str(self.bstack1l1lll11l_opy_)
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬ◄")] = str(self.percy_capture_mode)
        if bstack1ll1ll11ll11_opy_ == bstack1ll1l11_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧ◅") and str(self.bstack1l1lll11l_opy_).lower() == bstack1ll1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ◆"):
          self.bstack111ll111_opy_ = True
        if bstack1ll1l11_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ◇") in data:
          return data[bstack1ll1l11_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ◈")]
        else:
          raise bstack1ll1l11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭◉").format(data)
      else:
        raise bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢ◊").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤ○").format(e))
  def bstack1ll1lllll1ll_opy_(self):
    bstack1ll1lll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧ◌"))
    try:
      if bstack1ll1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ◍") not in self.bstack1ll1ll1llll1_opy_:
        self.bstack1ll1ll1llll1_opy_[bstack1ll1l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ◎")] = 2
      with open(bstack1ll1lll1l11l_opy_, bstack1ll1l11_opy_ (u"ࠬࡽࠧ●")) as fp:
        json.dump(self.bstack1ll1ll1llll1_opy_, fp)
      return bstack1ll1lll1l11l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ◐").format(e))
  def bstack1ll1ll11ll1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1ll1llll1l1l_opy_ == bstack1ll1l11_opy_ (u"ࠧࡸ࡫ࡱࠫ◑"):
        bstack1ll1ll1l1lll_opy_ = [bstack1ll1l11_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩ◒"), bstack1ll1l11_opy_ (u"ࠩ࠲ࡧࠬ◓")]
        cmd = bstack1ll1ll1l1lll_opy_ + cmd
      cmd = bstack1ll1l11_opy_ (u"ࠪࠤࠬ◔").join(cmd)
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣ◕").format(cmd))
      with open(self.bstack1ll1ll11l11l_opy_, bstack1ll1l11_opy_ (u"ࠧࡧࠢ◖")) as bstack1lll111111ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lll111111ll_opy_, text=True, stderr=bstack1lll111111ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1ll1ll1l11l1_opy_ = True
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ◗").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lll111111l1_opy_:
        self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣ◘"))
        cmd = [self.binary_path, bstack1ll1l11_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦ◙")]
        self.bstack1ll1ll11ll1l_opy_(cmd)
        self.bstack1lll111111l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ◚").format(cmd, e))
  def bstack11ll11111l_opy_(self):
    if not self.bstack1l1lll11l_opy_:
      return
    try:
      bstack1ll1ll1lll11_opy_ = 0
      while not self.bstack1lll111111l1_opy_ and bstack1ll1ll1lll11_opy_ < self.bstack1lll11111111_opy_:
        if self.bstack1ll1ll1l11l1_opy_:
          self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣ◛"))
          return
        time.sleep(1)
        bstack1ll1ll1lll11_opy_ += 1
      os.environ[bstack1ll1l11_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪ◜")] = str(self.bstack1lll11111l11_opy_())
      self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨ◝"))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ◞").format(e))
  def bstack1lll11111l11_opy_(self):
    if self.bstack111l1lll1_opy_:
      return
    try:
      bstack1ll1lll11l11_opy_ = [platform[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ◟")].lower() for platform in self.config.get(bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ◠"), [])]
      bstack1l1ll11l11l_opy_ = sys.maxsize
      bstack1ll1llll11ll_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪ◡")
      for browser in bstack1ll1lll11l11_opy_:
        if browser in self.bstack1ll1lll11111_opy_:
          bstack1ll1ll11llll_opy_ = self.bstack1ll1lll11111_opy_[browser]
        if bstack1ll1ll11llll_opy_ < bstack1l1ll11l11l_opy_:
          bstack1l1ll11l11l_opy_ = bstack1ll1ll11llll_opy_
          bstack1ll1llll11ll_opy_ = browser
      return bstack1ll1llll11ll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ◢").format(e))
  @classmethod
  def bstack1111ll1l1l_opy_(self):
    return os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩ◣"), bstack1ll1l11_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫ◤")).lower()
  @classmethod
  def bstack11l1l11l1l_opy_(self):
    return os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪ◥"), bstack1ll1l11_opy_ (u"ࠧࠨ◦"))
  @classmethod
  def bstack11ll111l1l1_opy_(cls, value):
    cls.bstack111ll111_opy_ = value
  @classmethod
  def bstack1ll1ll1lll1l_opy_(cls):
    return cls.bstack111ll111_opy_
  @classmethod
  def bstack11ll111ll1l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1ll1lll11lll_opy_(cls):
    return cls.percy_build_id