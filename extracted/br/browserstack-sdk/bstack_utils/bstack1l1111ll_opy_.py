# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1lllllll_opy_, bstack11l1lll1l1l_opy_, bstack11l1ll111ll_opy_
import tempfile
import json
bstack111l1llll1l_opy_ = os.getenv(bstack111l111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤᵘ"), None) or os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦᵙ"))
bstack111ll11l1l1_opy_ = os.path.join(bstack111l111_opy_ (u"ࠥࡰࡴ࡭ࠢᵚ"), bstack111l111_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨᵛ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111l111_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᵜ"),
      datefmt=bstack111l111_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫᵝ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1llll1l_opy_():
  bstack111ll1111ll_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧᵞ"), bstack111l111_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᵟ"))
  return logging.DEBUG if bstack111ll1111ll_opy_.lower() == bstack111l111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᵠ") else logging.INFO
def bstack1l1lll1ll1l_opy_():
  global bstack111l1llll1l_opy_
  if os.path.exists(bstack111l1llll1l_opy_):
    os.remove(bstack111l1llll1l_opy_)
  if os.path.exists(bstack111ll11l1l1_opy_):
    os.remove(bstack111ll11l1l1_opy_)
def bstack1l1l11ll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11ll1l1l1_opy_(config, log_level):
  bstack111ll11111l_opy_ = log_level
  if bstack111l111_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᵡ") in config and config[bstack111l111_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᵢ")] in bstack11l1lll1l1l_opy_:
    bstack111ll11111l_opy_ = bstack11l1lll1l1l_opy_[config[bstack111l111_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᵣ")]]
  if config.get(bstack111l111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᵤ"), False):
    logging.getLogger().setLevel(bstack111ll11111l_opy_)
    return bstack111ll11111l_opy_
  global bstack111l1llll1l_opy_
  bstack1l1l11ll1_opy_()
  bstack111ll111111_opy_ = logging.Formatter(
    fmt=bstack111l111_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᵥ"),
    datefmt=bstack111l111_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᵦ"),
  )
  bstack111ll111ll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l1llll1l_opy_)
  file_handler.setFormatter(bstack111ll111111_opy_)
  bstack111ll111ll1_opy_.setFormatter(bstack111ll111111_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111ll111ll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111l111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᵧ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111ll111ll1_opy_.setLevel(bstack111ll11111l_opy_)
  logging.getLogger().addHandler(bstack111ll111ll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111ll11111l_opy_
def bstack111ll11l1ll_opy_(config):
  try:
    bstack111ll11l11l_opy_ = set(bstack11l1ll111ll_opy_)
    bstack111ll111l1l_opy_ = bstack111l111_opy_ (u"ࠪࠫᵨ")
    with open(bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᵩ")) as bstack111ll11llll_opy_:
      bstack111ll111l11_opy_ = bstack111ll11llll_opy_.read()
      bstack111ll111l1l_opy_ = re.sub(bstack111l111_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ᵪ"), bstack111l111_opy_ (u"࠭ࠧᵫ"), bstack111ll111l11_opy_, flags=re.M)
      bstack111ll111l1l_opy_ = re.sub(
        bstack111l111_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᵬ") + bstack111l111_opy_ (u"ࠨࡾࠪᵭ").join(bstack111ll11l11l_opy_) + bstack111l111_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᵮ"),
        bstack111l111_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᵯ"),
        bstack111ll111l1l_opy_, flags=re.M | re.I
      )
    def bstack111ll1l111l_opy_(dic):
      bstack111ll111lll_opy_ = {}
      for key, value in dic.items():
        if key in bstack111ll11l11l_opy_:
          bstack111ll111lll_opy_[key] = bstack111l111_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᵰ")
        else:
          if isinstance(value, dict):
            bstack111ll111lll_opy_[key] = bstack111ll1l111l_opy_(value)
          else:
            bstack111ll111lll_opy_[key] = value
      return bstack111ll111lll_opy_
    bstack111ll111lll_opy_ = bstack111ll1l111l_opy_(config)
    return {
      bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᵱ"): bstack111ll111l1l_opy_,
      bstack111l111_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᵲ"): json.dumps(bstack111ll111lll_opy_)
    }
  except Exception as e:
    return {}
def bstack111l1llllll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack111l111_opy_ (u"ࠧ࡭ࡱࡪࠫᵳ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111l1lllll1_opy_ = os.path.join(log_dir, bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴࠩᵴ"))
  if not os.path.exists(bstack111l1lllll1_opy_):
    bstack111ll1111l1_opy_ = {
      bstack111l111_opy_ (u"ࠤ࡬ࡲ࡮ࡶࡡࡵࡪࠥᵵ"): str(inipath),
      bstack111l111_opy_ (u"ࠥࡶࡴࡵࡴࡱࡣࡷ࡬ࠧᵶ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack111l111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪᵷ")), bstack111l111_opy_ (u"ࠬࡽࠧᵸ")) as bstack111ll11lll1_opy_:
      bstack111ll11lll1_opy_.write(json.dumps(bstack111ll1111l1_opy_))
def bstack111ll1l1111_opy_():
  try:
    bstack111l1lllll1_opy_ = os.path.join(os.getcwd(), bstack111l111_opy_ (u"࠭࡬ࡰࡩࠪᵹ"), bstack111l111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᵺ"))
    if os.path.exists(bstack111l1lllll1_opy_):
      with open(bstack111l1lllll1_opy_, bstack111l111_opy_ (u"ࠨࡴࠪᵻ")) as bstack111ll11lll1_opy_:
        bstack111l1llll11_opy_ = json.load(bstack111ll11lll1_opy_)
      return bstack111l1llll11_opy_.get(bstack111l111_opy_ (u"ࠩ࡬ࡲ࡮ࡶࡡࡵࡪࠪᵼ"), bstack111l111_opy_ (u"ࠪࠫᵽ")), bstack111l1llll11_opy_.get(bstack111l111_opy_ (u"ࠫࡷࡵ࡯ࡵࡲࡤࡸ࡭࠭ᵾ"), bstack111l111_opy_ (u"ࠬ࠭ᵿ"))
  except:
    pass
  return None, None
def bstack111ll11ll1l_opy_():
  try:
    bstack111l1lllll1_opy_ = os.path.join(os.getcwd(), bstack111l111_opy_ (u"࠭࡬ࡰࡩࠪᶀ"), bstack111l111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᶁ"))
    if os.path.exists(bstack111l1lllll1_opy_):
      os.remove(bstack111l1lllll1_opy_)
  except:
    pass
def bstack1l1111ll1l_opy_(config):
  try:
    from bstack_utils.helper import bstack1ll1ll11_opy_, bstack1l1ll11l1_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111l1llll1l_opy_
    if config.get(bstack111l111_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᶂ"), False):
      return
    uuid = os.getenv(bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᶃ")) if os.getenv(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᶄ")) else bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨᶅ"))
    if not uuid or uuid == bstack111l111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᶆ"):
      return
    bstack111ll11l111_opy_ = [bstack111l111_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩᶇ"), bstack111l111_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨᶈ"), bstack111l111_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩᶉ"), bstack111l1llll1l_opy_, bstack111ll11l1l1_opy_]
    bstack111ll11ll11_opy_, root_path = bstack111ll1l1111_opy_()
    if bstack111ll11ll11_opy_ != None:
      bstack111ll11l111_opy_.append(bstack111ll11ll11_opy_)
    if root_path != None:
      bstack111ll11l111_opy_.append(os.path.join(root_path, bstack111l111_opy_ (u"ࠩࡦࡳࡳ࡬ࡴࡦࡵࡷ࠲ࡵࡿࠧᶊ")))
    bstack1l1l11ll1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩᶋ") + uuid + bstack111l111_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬᶌ"))
    with tarfile.open(output_file, bstack111l111_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᶍ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111ll11l111_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111ll11l1ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l1lll1l1_opy_ = data.encode()
        tarinfo.size = len(bstack111l1lll1l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l1lll1l1_opy_))
    bstack1l11l1l1_opy_ = MultipartEncoder(
      fields= {
        bstack111l111_opy_ (u"࠭ࡤࡢࡶࡤࠫᶎ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111l111_opy_ (u"ࠧࡳࡤࠪᶏ")), bstack111l111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭ᶐ")),
        bstack111l111_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᶑ"): uuid
      }
    )
    bstack111l1lll1ll_opy_ = bstack1l1ll11l1_opy_(cli.config, [bstack111l111_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᶒ"), bstack111l111_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦᶓ"), bstack111l111_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࠧᶔ")], bstack11l1lllllll_opy_)
    response = requests.post(
      bstack111l111_opy_ (u"ࠨࡻࡾ࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢᶕ").format(bstack111l1lll1ll_opy_),
      data=bstack1l11l1l1_opy_,
      headers={bstack111l111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᶖ"): bstack1l11l1l1_opy_.content_type},
      auth=(config[bstack111l111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᶗ")], config[bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᶘ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111l111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩᶙ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111l111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪᶚ") + str(e))
  finally:
    try:
      bstack1l1lll1ll1l_opy_()
      bstack111ll11ll1l_opy_()
    except:
      pass