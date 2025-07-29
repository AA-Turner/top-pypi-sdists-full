# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1l1llll1_opy_, bstack11l1llll1l1_opy_, bstack11l1lllllll_opy_
import tempfile
import json
bstack111ll111l1l_opy_ = os.getenv(bstackl_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇࠥᵙ"), None) or os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠧᵚ"))
bstack111l1lll1l1_opy_ = os.path.join(bstackl_opy_ (u"ࠦࡱࡵࡧࠣᵛ"), bstackl_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩᵜ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstackl_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᵝ"),
      datefmt=bstackl_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬᵞ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1l11lll_opy_():
  bstack111ll111l11_opy_ = os.environ.get(bstackl_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡅࡇࡅ࡙ࡌࠨᵟ"), bstackl_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣᵠ"))
  return logging.DEBUG if bstack111ll111l11_opy_.lower() == bstackl_opy_ (u"ࠥࡸࡷࡻࡥࠣᵡ") else logging.INFO
def bstack1l1ll1ll111_opy_():
  global bstack111ll111l1l_opy_
  if os.path.exists(bstack111ll111l1l_opy_):
    os.remove(bstack111ll111l1l_opy_)
  if os.path.exists(bstack111l1lll1l1_opy_):
    os.remove(bstack111l1lll1l1_opy_)
def bstack1l11llll1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1111l11l1_opy_(config, log_level):
  bstack111ll11l1l1_opy_ = log_level
  if bstackl_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᵢ") in config and config[bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᵣ")] in bstack11l1llll1l1_opy_:
    bstack111ll11l1l1_opy_ = bstack11l1llll1l1_opy_[config[bstackl_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᵤ")]]
  if config.get(bstackl_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᵥ"), False):
    logging.getLogger().setLevel(bstack111ll11l1l1_opy_)
    return bstack111ll11l1l1_opy_
  global bstack111ll111l1l_opy_
  bstack1l11llll1l_opy_()
  bstack111ll11llll_opy_ = logging.Formatter(
    fmt=bstackl_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᵦ"),
    datefmt=bstackl_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧᵧ"),
  )
  bstack111ll111ll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111ll111l1l_opy_)
  file_handler.setFormatter(bstack111ll11llll_opy_)
  bstack111ll111ll1_opy_.setFormatter(bstack111ll11llll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111ll111ll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstackl_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬᵨ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111ll111ll1_opy_.setLevel(bstack111ll11l1l1_opy_)
  logging.getLogger().addHandler(bstack111ll111ll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111ll11l1l1_opy_
def bstack111l1llll1l_opy_(config):
  try:
    bstack111l1lll1ll_opy_ = set(bstack11l1lllllll_opy_)
    bstack111ll11l11l_opy_ = bstackl_opy_ (u"ࠫࠬᵩ")
    with open(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᵪ")) as bstack111ll11l1ll_opy_:
      bstack111ll11ll1l_opy_ = bstack111ll11l1ll_opy_.read()
      bstack111ll11l11l_opy_ = re.sub(bstackl_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧᵫ"), bstackl_opy_ (u"ࠧࠨᵬ"), bstack111ll11ll1l_opy_, flags=re.M)
      bstack111ll11l11l_opy_ = re.sub(
        bstackl_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫᵭ") + bstackl_opy_ (u"ࠩࡿࠫᵮ").join(bstack111l1lll1ll_opy_) + bstackl_opy_ (u"ࠪ࠭࠳࠰ࠤࠨᵯ"),
        bstackl_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ᵰ"),
        bstack111ll11l11l_opy_, flags=re.M | re.I
      )
    def bstack111l1llllll_opy_(dic):
      bstack111ll1l1111_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l1lll1ll_opy_:
          bstack111ll1l1111_opy_[key] = bstackl_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᵱ")
        else:
          if isinstance(value, dict):
            bstack111ll1l1111_opy_[key] = bstack111l1llllll_opy_(value)
          else:
            bstack111ll1l1111_opy_[key] = value
      return bstack111ll1l1111_opy_
    bstack111ll1l1111_opy_ = bstack111l1llllll_opy_(config)
    return {
      bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᵲ"): bstack111ll11l11l_opy_,
      bstackl_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᵳ"): json.dumps(bstack111ll1l1111_opy_)
    }
  except Exception as e:
    return {}
def bstack111l1lll11l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࠬᵴ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111ll11ll11_opy_ = os.path.join(log_dir, bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵࠪᵵ"))
  if not os.path.exists(bstack111ll11ll11_opy_):
    bstack111l1lllll1_opy_ = {
      bstackl_opy_ (u"ࠥ࡭ࡳ࡯ࡰࡢࡶ࡫ࠦᵶ"): str(inipath),
      bstackl_opy_ (u"ࠦࡷࡵ࡯ࡵࡲࡤࡸ࡭ࠨᵷ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstackl_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫᵸ")), bstackl_opy_ (u"࠭ࡷࠨᵹ")) as bstack111ll11l111_opy_:
      bstack111ll11l111_opy_.write(json.dumps(bstack111l1lllll1_opy_))
def bstack111l1llll11_opy_():
  try:
    bstack111ll11ll11_opy_ = os.path.join(os.getcwd(), bstackl_opy_ (u"ࠧ࡭ࡱࡪࠫᵺ"), bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᵻ"))
    if os.path.exists(bstack111ll11ll11_opy_):
      with open(bstack111ll11ll11_opy_, bstackl_opy_ (u"ࠩࡵࠫᵼ")) as bstack111ll11l111_opy_:
        bstack111ll1111ll_opy_ = json.load(bstack111ll11l111_opy_)
      return bstack111ll1111ll_opy_.get(bstackl_opy_ (u"ࠪ࡭ࡳ࡯ࡰࡢࡶ࡫ࠫᵽ"), bstackl_opy_ (u"ࠫࠬᵾ")), bstack111ll1111ll_opy_.get(bstackl_opy_ (u"ࠬࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠧᵿ"), bstackl_opy_ (u"࠭ࠧᶀ"))
  except:
    pass
  return None, None
def bstack111ll11111l_opy_():
  try:
    bstack111ll11ll11_opy_ = os.path.join(os.getcwd(), bstackl_opy_ (u"ࠧ࡭ࡱࡪࠫᶁ"), bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᶂ"))
    if os.path.exists(bstack111ll11ll11_opy_):
      os.remove(bstack111ll11ll11_opy_)
  except:
    pass
def bstack1l1l1l1ll1_opy_(config):
  try:
    from bstack_utils.helper import bstack1l1llll1l1_opy_, bstack11ll1ll1_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111ll111l1l_opy_
    if config.get(bstackl_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᶃ"), False):
      return
    uuid = os.getenv(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᶄ")) if os.getenv(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᶅ")) else bstack1l1llll1l1_opy_.get_property(bstackl_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢᶆ"))
    if not uuid or uuid == bstackl_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᶇ"):
      return
    bstack111ll11lll1_opy_ = [bstackl_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪᶈ"), bstackl_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩᶉ"), bstackl_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪᶊ"), bstack111ll111l1l_opy_, bstack111l1lll1l1_opy_]
    bstack111ll111lll_opy_, root_path = bstack111l1llll11_opy_()
    if bstack111ll111lll_opy_ != None:
      bstack111ll11lll1_opy_.append(bstack111ll111lll_opy_)
    if root_path != None:
      bstack111ll11lll1_opy_.append(os.path.join(root_path, bstackl_opy_ (u"ࠪࡧࡴࡴࡦࡵࡧࡶࡸ࠳ࡶࡹࠨᶋ")))
    bstack1l11llll1l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪᶌ") + uuid + bstackl_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭ᶍ"))
    with tarfile.open(output_file, bstackl_opy_ (u"ࠨࡷ࠻ࡩࡽࠦᶎ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111ll11lll1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l1llll1l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111ll1111l1_opy_ = data.encode()
        tarinfo.size = len(bstack111ll1111l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111ll1111l1_opy_))
    bstack11lllll1ll_opy_ = MultipartEncoder(
      fields= {
        bstackl_opy_ (u"ࠧࡥࡣࡷࡥࠬᶏ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstackl_opy_ (u"ࠨࡴࡥࠫᶐ")), bstackl_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧᶑ")),
        bstackl_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᶒ"): uuid
      }
    )
    bstack111ll111111_opy_ = bstack11ll1ll1_opy_(cli.config, [bstackl_opy_ (u"ࠦࡦࡶࡩࡴࠤᶓ"), bstackl_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧᶔ"), bstackl_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩࠨᶕ")], bstack11l1l1llll1_opy_)
    response = requests.post(
      bstackl_opy_ (u"ࠢࡼࡿ࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣᶖ").format(bstack111ll111111_opy_),
      data=bstack11lllll1ll_opy_,
      headers={bstackl_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᶗ"): bstack11lllll1ll_opy_.content_type},
      auth=(config[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᶘ")], config[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᶙ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪᶚ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstackl_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫᶛ") + str(e))
  finally:
    try:
      bstack1l1ll1ll111_opy_()
      bstack111ll11111l_opy_()
    except:
      pass