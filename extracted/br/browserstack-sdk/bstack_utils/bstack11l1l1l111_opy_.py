# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1lll1ll1_opy_, bstack11l1lll11ll_opy_, bstack11ll11111l1_opy_
import tempfile
import json
bstack111ll11ll11_opy_ = os.getenv(bstack11ll1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤᴒ"), None) or os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦᴓ"))
bstack111ll1l11l1_opy_ = os.path.join(bstack11ll1l1_opy_ (u"ࠥࡰࡴ࡭ࠢᴔ"), bstack11ll1l1_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨᴕ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11ll1l1_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᴖ"),
      datefmt=bstack11ll1l1_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫᴗ"),
      stream=sys.stdout
    )
  return logger
def bstack1llll11l1ll_opy_():
  bstack111ll111l1l_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧᴘ"), bstack11ll1l1_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᴙ"))
  return logging.DEBUG if bstack111ll111l1l_opy_.lower() == bstack11ll1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᴚ") else logging.INFO
def bstack1l1ll11l111_opy_():
  global bstack111ll11ll11_opy_
  if os.path.exists(bstack111ll11ll11_opy_):
    os.remove(bstack111ll11ll11_opy_)
  if os.path.exists(bstack111ll1l11l1_opy_):
    os.remove(bstack111ll1l11l1_opy_)
def bstack1lll1l1ll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1lll1ll1ll_opy_(config, log_level):
  bstack111ll111lll_opy_ = log_level
  if bstack11ll1l1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᴛ") in config and config[bstack11ll1l1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᴜ")] in bstack11l1lll11ll_opy_:
    bstack111ll111lll_opy_ = bstack11l1lll11ll_opy_[config[bstack11ll1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᴝ")]]
  if config.get(bstack11ll1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᴞ"), False):
    logging.getLogger().setLevel(bstack111ll111lll_opy_)
    return bstack111ll111lll_opy_
  global bstack111ll11ll11_opy_
  bstack1lll1l1ll1_opy_()
  bstack111ll1111l1_opy_ = logging.Formatter(
    fmt=bstack11ll1l1_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᴟ"),
    datefmt=bstack11ll1l1_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᴠ"),
  )
  bstack111ll11llll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111ll11ll11_opy_)
  file_handler.setFormatter(bstack111ll1111l1_opy_)
  bstack111ll11llll_opy_.setFormatter(bstack111ll1111l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111ll11llll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11ll1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᴡ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111ll11llll_opy_.setLevel(bstack111ll111lll_opy_)
  logging.getLogger().addHandler(bstack111ll11llll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111ll111lll_opy_
def bstack111ll11l11l_opy_(config):
  try:
    bstack111ll11l111_opy_ = set(bstack11ll11111l1_opy_)
    bstack111ll1l1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠪࠫᴢ")
    with open(bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᴣ")) as bstack111ll11l1ll_opy_:
      bstack111ll1l111l_opy_ = bstack111ll11l1ll_opy_.read()
      bstack111ll1l1l1l_opy_ = re.sub(bstack11ll1l1_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ᴤ"), bstack11ll1l1_opy_ (u"࠭ࠧᴥ"), bstack111ll1l111l_opy_, flags=re.M)
      bstack111ll1l1l1l_opy_ = re.sub(
        bstack11ll1l1_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᴦ") + bstack11ll1l1_opy_ (u"ࠨࡾࠪᴧ").join(bstack111ll11l111_opy_) + bstack11ll1l1_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᴨ"),
        bstack11ll1l1_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᴩ"),
        bstack111ll1l1l1l_opy_, flags=re.M | re.I
      )
    def bstack111ll1l1ll1_opy_(dic):
      bstack111ll111ll1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111ll11l111_opy_:
          bstack111ll111ll1_opy_[key] = bstack11ll1l1_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᴪ")
        else:
          if isinstance(value, dict):
            bstack111ll111ll1_opy_[key] = bstack111ll1l1ll1_opy_(value)
          else:
            bstack111ll111ll1_opy_[key] = value
      return bstack111ll111ll1_opy_
    bstack111ll111ll1_opy_ = bstack111ll1l1ll1_opy_(config)
    return {
      bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᴫ"): bstack111ll1l1l1l_opy_,
      bstack11ll1l1_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᴬ"): json.dumps(bstack111ll111ll1_opy_)
    }
  except Exception as e:
    return {}
def bstack111ll1l1111_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11ll1l1_opy_ (u"ࠧ࡭ࡱࡪࠫᴭ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111ll111l11_opy_ = os.path.join(log_dir, bstack11ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴࠩᴮ"))
  if not os.path.exists(bstack111ll111l11_opy_):
    bstack111ll11ll1l_opy_ = {
      bstack11ll1l1_opy_ (u"ࠤ࡬ࡲ࡮ࡶࡡࡵࡪࠥᴯ"): str(inipath),
      bstack11ll1l1_opy_ (u"ࠥࡶࡴࡵࡴࡱࡣࡷ࡬ࠧᴰ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11ll1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪᴱ")), bstack11ll1l1_opy_ (u"ࠬࡽࠧᴲ")) as bstack111ll111111_opy_:
      bstack111ll111111_opy_.write(json.dumps(bstack111ll11ll1l_opy_))
def bstack111ll1111ll_opy_():
  try:
    bstack111ll111l11_opy_ = os.path.join(os.getcwd(), bstack11ll1l1_opy_ (u"࠭࡬ࡰࡩࠪᴳ"), bstack11ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᴴ"))
    if os.path.exists(bstack111ll111l11_opy_):
      with open(bstack111ll111l11_opy_, bstack11ll1l1_opy_ (u"ࠨࡴࠪᴵ")) as bstack111ll111111_opy_:
        bstack111ll1l1l11_opy_ = json.load(bstack111ll111111_opy_)
      return bstack111ll1l1l11_opy_.get(bstack11ll1l1_opy_ (u"ࠩ࡬ࡲ࡮ࡶࡡࡵࡪࠪᴶ"), bstack11ll1l1_opy_ (u"ࠪࠫᴷ")), bstack111ll1l1l11_opy_.get(bstack11ll1l1_opy_ (u"ࠫࡷࡵ࡯ࡵࡲࡤࡸ࡭࠭ᴸ"), bstack11ll1l1_opy_ (u"ࠬ࠭ᴹ"))
  except:
    pass
  return None, None
def bstack111ll11l1l1_opy_():
  try:
    bstack111ll111l11_opy_ = os.path.join(os.getcwd(), bstack11ll1l1_opy_ (u"࠭࡬ࡰࡩࠪᴺ"), bstack11ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᴻ"))
    if os.path.exists(bstack111ll111l11_opy_):
      os.remove(bstack111ll111l11_opy_)
  except:
    pass
def bstack1ll111l1l1_opy_(config):
  try:
    from bstack_utils.helper import bstack1111ll111_opy_, bstack11l111lll1_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111ll11ll11_opy_
    if config.get(bstack11ll1l1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᴼ"), False):
      return
    uuid = os.getenv(bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᴽ")) if os.getenv(bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᴾ")) else bstack1111ll111_opy_.get_property(bstack11ll1l1_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨᴿ"))
    if not uuid or uuid == bstack11ll1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᵀ"):
      return
    bstack111ll1l11ll_opy_ = [bstack11ll1l1_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩᵁ"), bstack11ll1l1_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨᵂ"), bstack11ll1l1_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩᵃ"), bstack111ll11ll11_opy_, bstack111ll1l11l1_opy_]
    bstack111ll11111l_opy_, root_path = bstack111ll1111ll_opy_()
    if bstack111ll11111l_opy_ != None:
      bstack111ll1l11ll_opy_.append(bstack111ll11111l_opy_)
    if root_path != None:
      bstack111ll1l11ll_opy_.append(os.path.join(root_path, bstack11ll1l1_opy_ (u"ࠩࡦࡳࡳ࡬ࡴࡦࡵࡷ࠲ࡵࡿࠧᵄ")))
    bstack1lll1l1ll1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩᵅ") + uuid + bstack11ll1l1_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬᵆ"))
    with tarfile.open(output_file, bstack11ll1l1_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᵇ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111ll1l11ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111ll11l11l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111ll1l1lll_opy_ = data.encode()
        tarinfo.size = len(bstack111ll1l1lll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111ll1l1lll_opy_))
    bstack11l11l11ll_opy_ = MultipartEncoder(
      fields= {
        bstack11ll1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᵈ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11ll1l1_opy_ (u"ࠧࡳࡤࠪᵉ")), bstack11ll1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭ᵊ")),
        bstack11ll1l1_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᵋ"): uuid
      }
    )
    bstack111ll11lll1_opy_ = bstack11l111lll1_opy_(cli.config, [bstack11ll1l1_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᵌ"), bstack11ll1l1_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦᵍ"), bstack11ll1l1_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࠧᵎ")], bstack11l1lll1ll1_opy_)
    response = requests.post(
      bstack11ll1l1_opy_ (u"ࠨࡻࡾ࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢᵏ").format(bstack111ll11lll1_opy_),
      data=bstack11l11l11ll_opy_,
      headers={bstack11ll1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᵐ"): bstack11l11l11ll_opy_.content_type},
      auth=(config[bstack11ll1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᵑ")], config[bstack11ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᵒ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11ll1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩᵓ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11ll1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪᵔ") + str(e))
  finally:
    try:
      bstack1l1ll11l111_opy_()
      bstack111ll11l1l1_opy_()
    except:
      pass