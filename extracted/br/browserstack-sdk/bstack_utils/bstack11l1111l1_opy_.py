# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1llllll1_opy_, bstack11l1lll1l11_opy_, bstack11l1ll1ll11_opy_
import tempfile
import json
bstack111l1lll1l1_opy_ = os.getenv(bstack1111l1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡈࡡࡉࡍࡑࡋࠢᶣ"), None) or os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠤᶤ"))
bstack111l1l1l1l1_opy_ = os.path.join(bstack1111l1l_opy_ (u"ࠣ࡮ࡲ࡫ࠧᶥ"), bstack1111l1l_opy_ (u"ࠩࡶࡨࡰ࠳ࡣ࡭࡫࠰ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬࠭ᶦ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1111l1l_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᶧ"),
      datefmt=bstack1111l1l_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩᶨ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll11llll1_opy_():
  bstack111l1lll111_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡉࡋࡂࡖࡉࠥᶩ"), bstack1111l1l_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧᶪ"))
  return logging.DEBUG if bstack111l1lll111_opy_.lower() == bstack1111l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᶫ") else logging.INFO
def bstack1l1ll1ll1l1_opy_():
  global bstack111l1lll1l1_opy_
  if os.path.exists(bstack111l1lll1l1_opy_):
    os.remove(bstack111l1lll1l1_opy_)
  if os.path.exists(bstack111l1l1l1l1_opy_):
    os.remove(bstack111l1l1l1l1_opy_)
def bstack1l11ll1l11_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111l1lll11l_opy_ = log_level
  if bstack1111l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᶬ") in config and config[bstack1111l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᶭ")] in bstack11l1lll1l11_opy_:
    bstack111l1lll11l_opy_ = bstack11l1lll1l11_opy_[config[bstack1111l1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᶮ")]]
  if config.get(bstack1111l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᶯ"), False):
    logging.getLogger().setLevel(bstack111l1lll11l_opy_)
    return bstack111l1lll11l_opy_
  global bstack111l1lll1l1_opy_
  bstack1l11ll1l11_opy_()
  bstack111l1l11ll1_opy_ = logging.Formatter(
    fmt=bstack1111l1l_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᶰ"),
    datefmt=bstack1111l1l_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫᶱ"),
  )
  bstack111l1ll1lll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l1lll1l1_opy_)
  file_handler.setFormatter(bstack111l1l11ll1_opy_)
  bstack111l1ll1lll_opy_.setFormatter(bstack111l1l11ll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l1ll1lll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1111l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࡸࡥ࡮ࡱࡷࡩ࠳ࡸࡥ࡮ࡱࡷࡩࡤࡩ࡯࡯ࡰࡨࡧࡹ࡯࡯࡯ࠩᶲ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l1ll1lll_opy_.setLevel(bstack111l1lll11l_opy_)
  logging.getLogger().addHandler(bstack111l1ll1lll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l1lll11l_opy_
def bstack111l1l11lll_opy_(config):
  try:
    bstack111l1llll11_opy_ = set(bstack11l1ll1ll11_opy_)
    bstack111l1l1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠨࠩᶳ")
    with open(bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬᶴ")) as bstack111l1l11l1l_opy_:
      bstack111l1ll1l1l_opy_ = bstack111l1l11l1l_opy_.read()
      bstack111l1l1ll1l_opy_ = re.sub(bstack1111l1l_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃࠨ࠴ࠪࠥ࡞ࡱࠫᶵ"), bstack1111l1l_opy_ (u"ࠫࠬᶶ"), bstack111l1ll1l1l_opy_, flags=re.M)
      bstack111l1l1ll1l_opy_ = re.sub(
        bstack1111l1l_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠨࠨᶷ") + bstack1111l1l_opy_ (u"࠭ࡼࠨᶸ").join(bstack111l1llll11_opy_) + bstack1111l1l_opy_ (u"ࠧࠪ࠰࠭ࠨࠬᶹ"),
        bstack1111l1l_opy_ (u"ࡳࠩ࡟࠶࠿࡛ࠦࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᶺ"),
        bstack111l1l1ll1l_opy_, flags=re.M | re.I
      )
    def bstack111l1ll1111_opy_(dic):
      bstack111l1ll11l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l1llll11_opy_:
          bstack111l1ll11l1_opy_[key] = bstack1111l1l_opy_ (u"ࠩ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ᶻ")
        else:
          if isinstance(value, dict):
            bstack111l1ll11l1_opy_[key] = bstack111l1ll1111_opy_(value)
          else:
            bstack111l1ll11l1_opy_[key] = value
      return bstack111l1ll11l1_opy_
    bstack111l1ll11l1_opy_ = bstack111l1ll1111_opy_(config)
    return {
      bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ᶼ"): bstack111l1l1ll1l_opy_,
      bstack1111l1l_opy_ (u"ࠫ࡫࡯࡮ࡢ࡮ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᶽ"): json.dumps(bstack111l1ll11l1_opy_)
    }
  except Exception as e:
    return {}
def bstack111l1ll11ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡨࠩᶾ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111l1lll1ll_opy_ = os.path.join(log_dir, bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹࠧᶿ"))
  if not os.path.exists(bstack111l1lll1ll_opy_):
    bstack111l1l1l1ll_opy_ = {
      bstack1111l1l_opy_ (u"ࠢࡪࡰ࡬ࡴࡦࡺࡨࠣ᷀"): str(inipath),
      bstack1111l1l_opy_ (u"ࠣࡴࡲࡳࡹࡶࡡࡵࡪࠥ᷁"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1111l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨ᷂")), bstack1111l1l_opy_ (u"ࠪࡻࠬ᷃")) as bstack111l1ll1ll1_opy_:
      bstack111l1ll1ll1_opy_.write(json.dumps(bstack111l1l1l1ll_opy_))
def bstack111l1l1ll11_opy_():
  try:
    bstack111l1lll1ll_opy_ = os.path.join(os.getcwd(), bstack1111l1l_opy_ (u"ࠫࡱࡵࡧࠨ᷄"), bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫ᷅"))
    if os.path.exists(bstack111l1lll1ll_opy_):
      with open(bstack111l1lll1ll_opy_, bstack1111l1l_opy_ (u"࠭ࡲࠨ᷆")) as bstack111l1ll1ll1_opy_:
        bstack111l1l1lll1_opy_ = json.load(bstack111l1ll1ll1_opy_)
      return bstack111l1l1lll1_opy_.get(bstack1111l1l_opy_ (u"ࠧࡪࡰ࡬ࡴࡦࡺࡨࠨ᷇"), bstack1111l1l_opy_ (u"ࠨࠩ᷈")), bstack111l1l1lll1_opy_.get(bstack1111l1l_opy_ (u"ࠩࡵࡳࡴࡺࡰࡢࡶ࡫ࠫ᷉"), bstack1111l1l_opy_ (u"᷊ࠪࠫ"))
  except:
    pass
  return None, None
def bstack111l1l1llll_opy_():
  try:
    bstack111l1lll1ll_opy_ = os.path.join(os.getcwd(), bstack1111l1l_opy_ (u"ࠫࡱࡵࡧࠨ᷋"), bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫ᷌"))
    if os.path.exists(bstack111l1lll1ll_opy_):
      os.remove(bstack111l1lll1ll_opy_)
  except:
    pass
def bstack11l11l1l1l_opy_(config):
  try:
    from bstack_utils.helper import bstack1l1ll11l1_opy_, bstack1l11lll111_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111l1lll1l1_opy_
    if config.get(bstack1111l1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ᷍"), False):
      return
    uuid = os.getenv(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ᷎ࠬ")) if os.getenv(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ᷏࠭")) else bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧ᷐ࠦ"))
    if not uuid or uuid == bstack1111l1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ᷑"):
      return
    bstack111l1ll111l_opy_ = [bstack1111l1l_opy_ (u"ࠫࡷ࡫ࡱࡶ࡫ࡵࡩࡲ࡫࡮ࡵࡵ࠱ࡸࡽࡺࠧ᷒"), bstack1111l1l_opy_ (u"ࠬࡖࡩࡱࡨ࡬ࡰࡪ࠭ᷓ"), bstack1111l1l_opy_ (u"࠭ࡰࡺࡲࡵࡳ࡯࡫ࡣࡵ࠰ࡷࡳࡲࡲࠧᷔ"), bstack111l1lll1l1_opy_, bstack111l1l1l1l1_opy_]
    bstack111l1l1l111_opy_, root_path = bstack111l1l1ll11_opy_()
    if bstack111l1l1l111_opy_ != None:
      bstack111l1ll111l_opy_.append(bstack111l1l1l111_opy_)
    if root_path != None:
      bstack111l1ll111l_opy_.append(os.path.join(root_path, bstack1111l1l_opy_ (u"ࠧࡤࡱࡱࡪࡹ࡫ࡳࡵ࠰ࡳࡽࠬᷕ")))
    bstack1l11ll1l11_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧᷖ") + uuid + bstack1111l1l_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪᷗ"))
    with tarfile.open(output_file, bstack1111l1l_opy_ (u"ࠥࡻ࠿࡭ࡺࠣᷘ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l1ll111l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l1l11lll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l1ll1l11_opy_ = data.encode()
        tarinfo.size = len(bstack111l1ll1l11_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l1ll1l11_opy_))
    bstack11l11l1lll_opy_ = MultipartEncoder(
      fields= {
        bstack1111l1l_opy_ (u"ࠫࡩࡧࡴࡢࠩᷙ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1111l1l_opy_ (u"ࠬࡸࡢࠨᷚ")), bstack1111l1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫᷛ")),
        bstack1111l1l_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᷜ"): uuid
      }
    )
    bstack111l1l1l11l_opy_ = bstack1l11lll111_opy_(cli.config, [bstack1111l1l_opy_ (u"ࠣࡣࡳ࡭ࡸࠨᷝ"), bstack1111l1l_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᷞ"), bstack1111l1l_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࠥᷟ")], bstack11l1llllll1_opy_)
    response = requests.post(
      bstack1111l1l_opy_ (u"ࠦࢀࢃ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧᷠ").format(bstack111l1l1l11l_opy_),
      data=bstack11l11l1lll_opy_,
      headers={bstack1111l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᷡ"): bstack11l11l1lll_opy_.content_type},
      auth=(config[bstack1111l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᷢ")], config[bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᷣ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1111l1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡶࡲ࡯ࡳࡦࡪࠠ࡭ࡱࡪࡷ࠿ࠦࠧᷤ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1111l1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹ࠺ࠨᷥ") + str(e))
  finally:
    try:
      bstack1l1ll1ll1l1_opy_()
      bstack111l1l1llll_opy_()
    except:
      pass