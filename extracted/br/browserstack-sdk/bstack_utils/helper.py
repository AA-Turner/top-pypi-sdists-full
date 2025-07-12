# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll111l11_opy_, bstack1l1111ll1l_opy_, bstack1l1lll1lll_opy_,
                                    bstack111llll1l11_opy_, bstack111llllll11_opy_, bstack111llllll1l_opy_, bstack11l111111l1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111111l1l_opy_, bstack1lll1l11l_opy_
from bstack_utils.proxy import bstack1ll1l1l1l_opy_, bstack1llll11111_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l11l1l1l_opy_
from bstack_utils.bstack1l1lll1l1l_opy_ import bstack11111111_opy_
from browserstack_sdk._version import __version__
bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
logger = bstack1l11l1l1l_opy_.get_logger(__name__, bstack1l11l1l1l_opy_.bstack1l11ll11l1l_opy_())
def bstack11l11l1llll_opy_(config):
    return config[bstack11l1111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᮧ")]
def bstack11l11ll111l_opy_(config):
    return config[bstack11l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᮨ")]
def bstack1l1l1l1l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1111lllllll_opy_(obj):
    values = []
    bstack1111lllll1l_opy_ = re.compile(bstack11l1111_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣᮩ"), re.I)
    for key in obj.keys():
        if bstack1111lllll1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l111l1ll_opy_(config):
    tags = []
    tags.extend(bstack1111lllllll_opy_(os.environ))
    tags.extend(bstack1111lllllll_opy_(config))
    return tags
def bstack111l1ll11ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111ll1111l1_opy_(bstack111l11l11l1_opy_):
    if not bstack111l11l11l1_opy_:
        return bstack11l1111_opy_ (u"᮪ࠬ࠭")
    return bstack11l1111_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯᮫ࠢ").format(bstack111l11l11l1_opy_.name, bstack111l11l11l1_opy_.email)
def bstack11l11lll1l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l1l11l11_opy_ = repo.common_dir
        info = {
            bstack11l1111_opy_ (u"ࠢࡴࡪࡤࠦᮬ"): repo.head.commit.hexsha,
            bstack11l1111_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦᮭ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1111_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤᮮ"): repo.active_branch.name,
            bstack11l1111_opy_ (u"ࠥࡸࡦ࡭ࠢᮯ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1111_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢ᮰"): bstack111ll1111l1_opy_(repo.head.commit.committer),
            bstack11l1111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨ᮱"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1111_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨ᮲"): bstack111ll1111l1_opy_(repo.head.commit.author),
            bstack11l1111_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧ᮳"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1111_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ᮴"): repo.head.commit.message,
            bstack11l1111_opy_ (u"ࠤࡵࡳࡴࡺࠢ᮵"): repo.git.rev_parse(bstack11l1111_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧ᮶")),
            bstack11l1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ᮷"): bstack111l1l11l11_opy_,
            bstack11l1111_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ᮸"): subprocess.check_output([bstack11l1111_opy_ (u"ࠨࡧࡪࡶࠥ᮹"), bstack11l1111_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᮺ"), bstack11l1111_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦᮻ")]).strip().decode(
                bstack11l1111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᮼ")),
            bstack11l1111_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᮽ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1111_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᮾ"): repo.git.rev_list(
                bstack11l1111_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧᮿ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l11ll1l1_opy_ = []
        for remote in remotes:
            bstack111l111llll_opy_ = {
                bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᯀ"): remote.name,
                bstack11l1111_opy_ (u"ࠢࡶࡴ࡯ࠦᯁ"): remote.url,
            }
            bstack111l11ll1l1_opy_.append(bstack111l111llll_opy_)
        bstack111l1ll1lll_opy_ = {
            bstack11l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᯂ"): bstack11l1111_opy_ (u"ࠤࡪ࡭ࡹࠨᯃ"),
            **info,
            bstack11l1111_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᯄ"): bstack111l11ll1l1_opy_
        }
        bstack111l1ll1lll_opy_ = bstack111ll1l1lll_opy_(bstack111l1ll1lll_opy_)
        return bstack111l1ll1lll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᯅ").format(err))
        return {}
def bstack111ll1l1lll_opy_(bstack111l1ll1lll_opy_):
    bstack111ll111l11_opy_ = bstack1111lllll11_opy_(bstack111l1ll1lll_opy_)
    if bstack111ll111l11_opy_ and bstack111ll111l11_opy_ > bstack111llll1l11_opy_:
        bstack111ll11111l_opy_ = bstack111ll111l11_opy_ - bstack111llll1l11_opy_
        bstack111l1111111_opy_ = bstack111l11lll11_opy_(bstack111l1ll1lll_opy_[bstack11l1111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᯆ")], bstack111ll11111l_opy_)
        bstack111l1ll1lll_opy_[bstack11l1111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᯇ")] = bstack111l1111111_opy_
        logger.info(bstack11l1111_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤᯈ")
                    .format(bstack1111lllll11_opy_(bstack111l1ll1lll_opy_) / 1024))
    return bstack111l1ll1lll_opy_
def bstack1111lllll11_opy_(bstack11lllllll_opy_):
    try:
        if bstack11lllllll_opy_:
            bstack111l111ll1l_opy_ = json.dumps(bstack11lllllll_opy_)
            bstack1111llll1l1_opy_ = sys.getsizeof(bstack111l111ll1l_opy_)
            return bstack1111llll1l1_opy_
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣᯉ").format(e))
    return -1
def bstack111l11lll11_opy_(field, bstack111l11l1lll_opy_):
    try:
        bstack111ll1l1l11_opy_ = len(bytes(bstack111llllll11_opy_, bstack11l1111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᯊ")))
        bstack111l11l11ll_opy_ = bytes(field, bstack11l1111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᯋ"))
        bstack111ll111lll_opy_ = len(bstack111l11l11ll_opy_)
        bstack1111llll111_opy_ = ceil(bstack111ll111lll_opy_ - bstack111l11l1lll_opy_ - bstack111ll1l1l11_opy_)
        if bstack1111llll111_opy_ > 0:
            bstack111ll1l11ll_opy_ = bstack111l11l11ll_opy_[:bstack1111llll111_opy_].decode(bstack11l1111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᯌ"), errors=bstack11l1111_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬᯍ")) + bstack111llllll11_opy_
            return bstack111ll1l11ll_opy_
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦᯎ").format(e))
    return field
def bstack1l1l1l1ll1_opy_():
    env = os.environ
    if (bstack11l1111_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᯏ") in env and len(env[bstack11l1111_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᯐ")]) > 0) or (
            bstack11l1111_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᯑ") in env and len(env[bstack11l1111_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᯒ")]) > 0):
        return {
            bstack11l1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᯓ"): bstack11l1111_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᯔ"),
            bstack11l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯕ"): env.get(bstack11l1111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᯖ")),
            bstack11l1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᯗ"): env.get(bstack11l1111_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᯘ")),
            bstack11l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᯙ"): env.get(bstack11l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᯚ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠧࡉࡉࠣᯛ")) == bstack11l1111_opy_ (u"ࠨࡴࡳࡷࡨࠦᯜ") and bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᯝ"))):
        return {
            bstack11l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᯞ"): bstack11l1111_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᯟ"),
            bstack11l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᯠ"): env.get(bstack11l1111_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᯡ")),
            bstack11l1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᯢ"): env.get(bstack11l1111_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᯣ")),
            bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᯤ"): env.get(bstack11l1111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᯥ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠤࡆࡍ᯦ࠧ")) == bstack11l1111_opy_ (u"ࠥࡸࡷࡻࡥࠣᯧ") and bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᯨ"))):
        return {
            bstack11l1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯩ"): bstack11l1111_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᯪ"),
            bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᯫ"): env.get(bstack11l1111_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᯬ")),
            bstack11l1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᯭ"): env.get(bstack11l1111_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᯮ")),
            bstack11l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᯯ"): env.get(bstack11l1111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᯰ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠨࡃࡊࠤᯱ")) == bstack11l1111_opy_ (u"ࠢࡵࡴࡸࡩ᯲ࠧ") and env.get(bstack11l1111_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤ᯳")) == bstack11l1111_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦ᯴"):
        return {
            bstack11l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᯵"): bstack11l1111_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨ᯶"),
            bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᯷"): None,
            bstack11l1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᯸"): None,
            bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᯹"): None
        }
    if env.get(bstack11l1111_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ᯺")) and env.get(bstack11l1111_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧ᯻")):
        return {
            bstack11l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᯼"): bstack11l1111_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ᯽"),
            bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᯾"): env.get(bstack11l1111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ᯿")),
            bstack11l1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᰀ"): None,
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰁ"): env.get(bstack11l1111_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᰂ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠥࡇࡎࠨᰃ")) == bstack11l1111_opy_ (u"ࠦࡹࡸࡵࡦࠤᰄ") and bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᰅ"))):
        return {
            bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰆ"): bstack11l1111_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᰇ"),
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰈ"): env.get(bstack11l1111_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᰉ")),
            bstack11l1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᰊ"): None,
            bstack11l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᰋ"): env.get(bstack11l1111_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᰌ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠨࡃࡊࠤᰍ")) == bstack11l1111_opy_ (u"ࠢࡵࡴࡸࡩࠧᰎ") and bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᰏ"))):
        return {
            bstack11l1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᰐ"): bstack11l1111_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᰑ"),
            bstack11l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᰒ"): env.get(bstack11l1111_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᰓ")),
            bstack11l1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᰔ"): env.get(bstack11l1111_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᰕ")),
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰖ"): env.get(bstack11l1111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᰗ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠥࡇࡎࠨᰘ")) == bstack11l1111_opy_ (u"ࠦࡹࡸࡵࡦࠤᰙ") and bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᰚ"))):
        return {
            bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰛ"): bstack11l1111_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᰜ"),
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰝ"): env.get(bstack11l1111_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᰞ")),
            bstack11l1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᰟ"): env.get(bstack11l1111_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᰠ")),
            bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᰡ"): env.get(bstack11l1111_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᰢ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠢࡄࡋࠥᰣ")) == bstack11l1111_opy_ (u"ࠣࡶࡵࡹࡪࠨᰤ") and bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᰥ"))):
        return {
            bstack11l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣᰦ"): bstack11l1111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᰧ"),
            bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᰨ"): env.get(bstack11l1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᰩ")),
            bstack11l1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᰪ"): env.get(bstack11l1111_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᰫ")) or env.get(bstack11l1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᰬ")),
            bstack11l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰭ"): env.get(bstack11l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᰮ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᰯ"))):
        return {
            bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰰ"): bstack11l1111_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᰱ"),
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰲ"): bstack11l1111_opy_ (u"ࠤࡾࢁࢀࢃࠢᰳ").format(env.get(bstack11l1111_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᰴ")), env.get(bstack11l1111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᰵ"))),
            bstack11l1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᰶ"): env.get(bstack11l1111_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈ᰷ࠧ")),
            bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᰸"): env.get(bstack11l1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣ᰹"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦ᰺"))):
        return {
            bstack11l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᰻"): bstack11l1111_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨ᰼"),
            bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᰽"): bstack11l1111_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧ᰾").format(env.get(bstack11l1111_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭᰿")), env.get(bstack11l1111_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩ᱀")), env.get(bstack11l1111_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪ᱁")), env.get(bstack11l1111_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ᱂"))),
            bstack11l1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᱃"): env.get(bstack11l1111_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᱄")),
            bstack11l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᱅"): env.get(bstack11l1111_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᱆"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤ᱇")) and env.get(bstack11l1111_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦ᱈")):
        return {
            bstack11l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᱉"): bstack11l1111_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨ᱊"),
            bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᱋"): bstack11l1111_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤ᱌").format(env.get(bstack11l1111_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᱍ")), env.get(bstack11l1111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ᱎ")), env.get(bstack11l1111_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᱏ"))),
            bstack11l1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᱐"): env.get(bstack11l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ᱑")),
            bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᱒"): env.get(bstack11l1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ᱓"))
        }
    if any([env.get(bstack11l1111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᱔")), env.get(bstack11l1111_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ᱕")), env.get(bstack11l1111_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᱖"))]):
        return {
            bstack11l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᱗"): bstack11l1111_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦ᱘"),
            bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᱙"): env.get(bstack11l1111_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᱚ")),
            bstack11l1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᱛ"): env.get(bstack11l1111_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᱜ")),
            bstack11l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᱝ"): env.get(bstack11l1111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᱞ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᱟ")):
        return {
            bstack11l1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᱠ"): bstack11l1111_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᱡ"),
            bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᱢ"): env.get(bstack11l1111_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᱣ")),
            bstack11l1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᱤ"): env.get(bstack11l1111_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᱥ")),
            bstack11l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᱦ"): env.get(bstack11l1111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᱧ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᱨ")) or env.get(bstack11l1111_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᱩ")):
        return {
            bstack11l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᱪ"): bstack11l1111_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᱫ"),
            bstack11l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᱬ"): env.get(bstack11l1111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᱭ")),
            bstack11l1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᱮ"): bstack11l1111_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᱯ") if env.get(bstack11l1111_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᱰ")) else None,
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᱱ"): env.get(bstack11l1111_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᱲ"))
        }
    if any([env.get(bstack11l1111_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᱳ")), env.get(bstack11l1111_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᱴ")), env.get(bstack11l1111_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᱵ"))]):
        return {
            bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᱶ"): bstack11l1111_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᱷ"),
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᱸ"): None,
            bstack11l1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᱹ"): env.get(bstack11l1111_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᱺ")),
            bstack11l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᱻ"): env.get(bstack11l1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᱼ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᱽ")):
        return {
            bstack11l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᱾"): bstack11l1111_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦ᱿"),
            bstack11l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᲀ"): env.get(bstack11l1111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᲁ")),
            bstack11l1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᲂ"): bstack11l1111_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᲃ").format(env.get(bstack11l1111_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᲄ"))) if env.get(bstack11l1111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᲅ")) else None,
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᲆ"): env.get(bstack11l1111_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᲇ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᲈ"))):
        return {
            bstack11l1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᲉ"): bstack11l1111_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᲊ"),
            bstack11l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᲋"): env.get(bstack11l1111_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦ᲌")),
            bstack11l1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᲍"): env.get(bstack11l1111_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧ᲎")),
            bstack11l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᲏"): env.get(bstack11l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᲐ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack11l1111_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᲑ"))):
        return {
            bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᲒ"): bstack11l1111_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᲓ"),
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᲔ"): bstack11l1111_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᲕ").format(env.get(bstack11l1111_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᲖ")), env.get(bstack11l1111_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᲗ")), env.get(bstack11l1111_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᲘ"))),
            bstack11l1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᲙ"): env.get(bstack11l1111_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᲚ")),
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᲛ"): env.get(bstack11l1111_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᲜ"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠥࡇࡎࠨᲝ")) == bstack11l1111_opy_ (u"ࠦࡹࡸࡵࡦࠤᲞ") and env.get(bstack11l1111_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᲟ")) == bstack11l1111_opy_ (u"ࠨ࠱ࠣᲠ"):
        return {
            bstack11l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᲡ"): bstack11l1111_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᲢ"),
            bstack11l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᲣ"): bstack11l1111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᲤ").format(env.get(bstack11l1111_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᲥ"))),
            bstack11l1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᲦ"): None,
            bstack11l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᲧ"): None,
        }
    if env.get(bstack11l1111_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᲨ")):
        return {
            bstack11l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᲩ"): bstack11l1111_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᲪ"),
            bstack11l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᲫ"): None,
            bstack11l1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᲬ"): env.get(bstack11l1111_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᲭ")),
            bstack11l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᲮ"): env.get(bstack11l1111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᲯ"))
        }
    if any([env.get(bstack11l1111_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᲰ")), env.get(bstack11l1111_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᲱ")), env.get(bstack11l1111_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᲲ")), env.get(bstack11l1111_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᲳ"))]):
        return {
            bstack11l1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᲴ"): bstack11l1111_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᲵ"),
            bstack11l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᲶ"): None,
            bstack11l1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᲷ"): env.get(bstack11l1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᲸ")) or None,
            bstack11l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᲹ"): env.get(bstack11l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᲺ"), 0)
        }
    if env.get(bstack11l1111_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᲻")):
        return {
            bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᲼"): bstack11l1111_opy_ (u"ࠢࡈࡱࡆࡈࠧᲽ"),
            bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᲾ"): None,
            bstack11l1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᲿ"): env.get(bstack11l1111_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᳀")),
            bstack11l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᳁"): env.get(bstack11l1111_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦ᳂"))
        }
    if env.get(bstack11l1111_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᳃")):
        return {
            bstack11l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᳄"): bstack11l1111_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦ᳅"),
            bstack11l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᳆"): env.get(bstack11l1111_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᳇")),
            bstack11l1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᳈"): env.get(bstack11l1111_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣ᳉")),
            bstack11l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᳊"): env.get(bstack11l1111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᳋"))
        }
    return {bstack11l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᳌"): None}
def get_host_info():
    return {
        bstack11l1111_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦ᳍"): platform.node(),
        bstack11l1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ᳎"): platform.system(),
        bstack11l1111_opy_ (u"ࠦࡹࡿࡰࡦࠤ᳏"): platform.machine(),
        bstack11l1111_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ᳐"): platform.version(),
        bstack11l1111_opy_ (u"ࠨࡡࡳࡥ࡫ࠦ᳑"): platform.architecture()[0]
    }
def bstack11111lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111ll11l111_opy_():
    if bstack1l1l11l1ll_opy_.get_property(bstack11l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ᳒")):
        return bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᳓")
    return bstack11l1111_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨ᳔")
def bstack111l1111l1l_opy_(driver):
    info = {
        bstack11l1111_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ᳕ࠩ"): driver.capabilities,
        bstack11l1111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ᳖"): driver.session_id,
        bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ᳗࠭"): driver.capabilities.get(bstack11l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨ᳘ࠫ"), None),
        bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯᳙ࠩ"): driver.capabilities.get(bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᳚"), None),
        bstack11l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫ᳛"): driver.capabilities.get(bstack11l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦ᳜ࠩ"), None),
        bstack11l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴ᳝ࠧ"):driver.capabilities.get(bstack11l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴ᳞ࠧ"), None),
    }
    if bstack111ll11l111_opy_() == bstack11l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯᳟ࠬ"):
        if bstack1l1ll1ll1_opy_():
            info[bstack11l1111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ᳠")] = bstack11l1111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᳡")
        elif driver.capabilities.get(bstack11l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵ᳢ࠪ"), {}).get(bstack11l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫᳣ࠧ"), False):
            info[bstack11l1111_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸ᳤ࠬ")] = bstack11l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦ᳥ࠩ")
        else:
            info[bstack11l1111_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ᳦ࠧ")] = bstack11l1111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦ᳧ࠩ")
    return info
def bstack1l1ll1ll1_opy_():
    if bstack1l1l11l1ll_opy_.get_property(bstack11l1111_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫᳨ࠧ")):
        return True
    if bstack11l1l1ll_opy_(os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᳩ"), None)):
        return True
    return False
def bstack1lllll1111_opy_(bstack111l11l111l_opy_, url, data, config):
    headers = config.get(bstack11l1111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᳪ"), None)
    proxies = bstack1ll1l1l1l_opy_(config, url)
    auth = config.get(bstack11l1111_opy_ (u"ࠫࡦࡻࡴࡩࠩᳫ"), None)
    response = requests.request(
            bstack111l11l111l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll11lll1_opy_(bstack1l11l1ll_opy_, size):
    bstack11lll1ll1_opy_ = []
    while len(bstack1l11l1ll_opy_) > size:
        bstack1ll1llll_opy_ = bstack1l11l1ll_opy_[:size]
        bstack11lll1ll1_opy_.append(bstack1ll1llll_opy_)
        bstack1l11l1ll_opy_ = bstack1l11l1ll_opy_[size:]
    bstack11lll1ll1_opy_.append(bstack1l11l1ll_opy_)
    return bstack11lll1ll1_opy_
def bstack1111llll11l_opy_(message, bstack111l1l11ll1_opy_=False):
    os.write(1, bytes(message, bstack11l1111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᳬ")))
    os.write(1, bytes(bstack11l1111_opy_ (u"࠭࡜࡯᳭ࠩ"), bstack11l1111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᳮ")))
    if bstack111l1l11ll1_opy_:
        with open(bstack11l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧᳯ") + os.environ[bstack11l1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᳰ")] + bstack11l1111_opy_ (u"ࠪ࠲ࡱࡵࡧࠨᳱ"), bstack11l1111_opy_ (u"ࠫࡦ࠭ᳲ")) as f:
            f.write(message + bstack11l1111_opy_ (u"ࠬࡢ࡮ࠨᳳ"))
def bstack1llll1ll1l1_opy_():
    return os.environ[bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ᳴")].lower() == bstack11l1111_opy_ (u"ࠧࡵࡴࡸࡩࠬᳵ")
def bstack1lllllllll_opy_():
    return bstack111l111lll_opy_().replace(tzinfo=None).isoformat() + bstack11l1111_opy_ (u"ࠨ࡜ࠪᳶ")
def bstack111l1lll1l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1111_opy_ (u"ࠩ࡝ࠫ᳷"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1111_opy_ (u"ࠪ࡞ࠬ᳸")))).total_seconds() * 1000
def bstack111l1llll11_opy_(timestamp):
    return bstack111l1l1llll_opy_(timestamp).isoformat() + bstack11l1111_opy_ (u"ࠫ࡟࠭᳹")
def bstack111l1l1111l_opy_(bstack111l1111ll1_opy_):
    date_format = bstack11l1111_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᳺ")
    bstack111l11llll1_opy_ = datetime.datetime.strptime(bstack111l1111ll1_opy_, date_format)
    return bstack111l11llll1_opy_.isoformat() + bstack11l1111_opy_ (u"࡚࠭ࠨ᳻")
def bstack111l111111l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᳼")
    else:
        return bstack11l1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᳽")
def bstack11l1l1ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᳾")
def bstack111l111lll1_opy_(val):
    return val.__str__().lower() == bstack11l1111_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ᳿")
def bstack111l11l1l1_opy_(bstack1111lll1ll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111lll1ll1_opy_ as e:
                print(bstack11l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᴀ").format(func.__name__, bstack1111lll1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l111l1l1_opy_(bstack111ll111ll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111ll111ll1_opy_(cls, *args, **kwargs)
            except bstack1111lll1ll1_opy_ as e:
                print(bstack11l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᴁ").format(bstack111ll111ll1_opy_.__name__, bstack1111lll1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l111l1l1_opy_
    else:
        return decorator
def bstack1l11lll1l_opy_(bstack1111l1lll1_opy_):
    if os.getenv(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᴂ")) is not None:
        return bstack11l1l1ll_opy_(os.getenv(bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᴃ")))
    if bstack11l1111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᴄ") in bstack1111l1lll1_opy_ and bstack111l111lll1_opy_(bstack1111l1lll1_opy_[bstack11l1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᴅ")]):
        return False
    if bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᴆ") in bstack1111l1lll1_opy_ and bstack111l111lll1_opy_(bstack1111l1lll1_opy_[bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᴇ")]):
        return False
    return True
def bstack1ll11ll111_opy_():
    try:
        from pytest_bdd import reporting
        bstack111ll11l1l1_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᴈ"), None)
        return bstack111ll11l1l1_opy_ is None or bstack111ll11l1l1_opy_ == bstack11l1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᴉ")
    except Exception as e:
        return False
def bstack11l111l1l1_opy_(hub_url, CONFIG):
    if bstack111l1l111_opy_() <= version.parse(bstack11l1111_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᴊ")):
        if hub_url:
            return bstack11l1111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᴋ") + hub_url + bstack11l1111_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᴌ")
        return bstack1l1111ll1l_opy_
    if hub_url:
        return bstack11l1111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᴍ") + hub_url + bstack11l1111_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᴎ")
    return bstack1l1lll1lll_opy_
def bstack111l11l1111_opy_():
    return isinstance(os.getenv(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᴏ")), str)
def bstack11l1ll1l1l_opy_(url):
    return urlparse(url).hostname
def bstack1lll1l1ll1_opy_(hostname):
    for bstack1ll1l111l1_opy_ in bstack11ll111l11_opy_:
        regex = re.compile(bstack1ll1l111l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111llll1ll_opy_(bstack111l11ll111_opy_, file_name, logger):
    bstack1lll11l1l_opy_ = os.path.join(os.path.expanduser(bstack11l1111_opy_ (u"࠭ࡾࠨᴐ")), bstack111l11ll111_opy_)
    try:
        if not os.path.exists(bstack1lll11l1l_opy_):
            os.makedirs(bstack1lll11l1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1111_opy_ (u"ࠧࡿࠩᴑ")), bstack111l11ll111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1111_opy_ (u"ࠨࡹࠪᴒ")):
                pass
            with open(file_path, bstack11l1111_opy_ (u"ࠤࡺ࠯ࠧᴓ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111111l1l_opy_.format(str(e)))
def bstack111l11lllll_opy_(file_name, key, value, logger):
    file_path = bstack1111llll1ll_opy_(bstack11l1111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᴔ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l111lll1l_opy_ = json.load(open(file_path, bstack11l1111_opy_ (u"ࠫࡷࡨࠧᴕ")))
        else:
            bstack1l111lll1l_opy_ = {}
        bstack1l111lll1l_opy_[key] = value
        with open(file_path, bstack11l1111_opy_ (u"ࠧࡽࠫࠣᴖ")) as outfile:
            json.dump(bstack1l111lll1l_opy_, outfile)
def bstack1l1lllll1_opy_(file_name, logger):
    file_path = bstack1111llll1ll_opy_(bstack11l1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᴗ"), file_name, logger)
    bstack1l111lll1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1111_opy_ (u"ࠧࡳࠩᴘ")) as bstack1l1ll1lll1_opy_:
            bstack1l111lll1l_opy_ = json.load(bstack1l1ll1lll1_opy_)
    return bstack1l111lll1l_opy_
def bstack111111l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬᴙ") + file_path + bstack11l1111_opy_ (u"ࠩࠣࠫᴚ") + str(e))
def bstack111l1l111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1111_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧᴛ")
def bstack11111ll1_opy_(config):
    if bstack11l1111_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᴜ") in config:
        del (config[bstack11l1111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᴝ")])
        return False
    if bstack111l1l111_opy_() < version.parse(bstack11l1111_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬᴞ")):
        return False
    if bstack111l1l111_opy_() >= version.parse(bstack11l1111_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ᴟ")):
        return True
    if bstack11l1111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᴠ") in config and config[bstack11l1111_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᴡ")] is False:
        return False
    else:
        return True
def bstack1ll1l11l11_opy_(args_list, bstack111l1ll1ll1_opy_):
    index = -1
    for value in bstack111l1ll1ll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l11lll111_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l11lll111_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111lll1l1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111lll1l1l_opy_ = bstack111lll1l1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᴢ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᴣ"), exception=exception)
    def bstack111111llll_opy_(self):
        if self.result != bstack11l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᴤ"):
            return None
        if isinstance(self.exception_type, str) and bstack11l1111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᴥ") in self.exception_type:
            return bstack11l1111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᴦ")
        return bstack11l1111_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᴧ")
    def bstack111l1ll111l_opy_(self):
        if self.result != bstack11l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᴨ"):
            return None
        if self.bstack111lll1l1l_opy_:
            return self.bstack111lll1l1l_opy_
        return bstack111l11l1l1l_opy_(self.exception)
def bstack111l11l1l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l1l1l1ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11ll1lll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11ll11l1_opy_(config, logger):
    try:
        import playwright
        bstack111l1l1l1l1_opy_ = playwright.__file__
        bstack111l1ll1l11_opy_ = os.path.split(bstack111l1l1l1l1_opy_)
        bstack111l1l11111_opy_ = bstack111l1ll1l11_opy_[0] + bstack11l1111_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭ᴩ")
        os.environ[bstack11l1111_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧᴪ")] = bstack1llll11111_opy_(config)
        with open(bstack111l1l11111_opy_, bstack11l1111_opy_ (u"ࠬࡸࠧᴫ")) as f:
            bstack1l11l11111_opy_ = f.read()
            bstack111l1llllll_opy_ = bstack11l1111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬᴬ")
            bstack111ll11ll11_opy_ = bstack1l11l11111_opy_.find(bstack111l1llllll_opy_)
            if bstack111ll11ll11_opy_ == -1:
              process = subprocess.Popen(bstack11l1111_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦᴭ"), shell=True, cwd=bstack111l1ll1l11_opy_[0])
              process.wait()
              bstack111l1lllll1_opy_ = bstack11l1111_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨᴮ")
              bstack111l1l1l111_opy_ = bstack11l1111_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨᴯ")
              bstack111l11l1l11_opy_ = bstack1l11l11111_opy_.replace(bstack111l1lllll1_opy_, bstack111l1l1l111_opy_)
              with open(bstack111l1l11111_opy_, bstack11l1111_opy_ (u"ࠪࡻࠬᴰ")) as f:
                f.write(bstack111l11l1l11_opy_)
    except Exception as e:
        logger.error(bstack1lll1l11l_opy_.format(str(e)))
def bstack1l11l11l_opy_():
  try:
    bstack111ll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᴱ"))
    bstack111l1l111ll_opy_ = []
    if os.path.exists(bstack111ll1l1111_opy_):
      with open(bstack111ll1l1111_opy_) as f:
        bstack111l1l111ll_opy_ = json.load(f)
      os.remove(bstack111ll1l1111_opy_)
    return bstack111l1l111ll_opy_
  except:
    pass
  return []
def bstack111ll111_opy_(bstack11l1llll1l_opy_):
  try:
    bstack111l1l111ll_opy_ = []
    bstack111ll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᴲ"))
    if os.path.exists(bstack111ll1l1111_opy_):
      with open(bstack111ll1l1111_opy_) as f:
        bstack111l1l111ll_opy_ = json.load(f)
    bstack111l1l111ll_opy_.append(bstack11l1llll1l_opy_)
    with open(bstack111ll1l1111_opy_, bstack11l1111_opy_ (u"࠭ࡷࠨᴳ")) as f:
        json.dump(bstack111l1l111ll_opy_, f)
  except:
    pass
def bstack11l1l1ll1_opy_(logger, bstack1111llllll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1111_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᴴ"), bstack11l1111_opy_ (u"ࠨࠩᴵ"))
    if test_name == bstack11l1111_opy_ (u"ࠩࠪᴶ"):
        test_name = threading.current_thread().__dict__.get(bstack11l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᴷ"), bstack11l1111_opy_ (u"ࠫࠬᴸ"))
    bstack111ll111111_opy_ = bstack11l1111_opy_ (u"ࠬ࠲ࠠࠨᴹ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111llllll1_opy_:
        bstack11llllll11_opy_ = os.environ.get(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᴺ"), bstack11l1111_opy_ (u"ࠧ࠱ࠩᴻ"))
        bstack1l1llllll_opy_ = {bstack11l1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᴼ"): test_name, bstack11l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᴽ"): bstack111ll111111_opy_, bstack11l1111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᴾ"): bstack11llllll11_opy_}
        bstack111ll1111ll_opy_ = []
        bstack111l1l111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᴿ"))
        if os.path.exists(bstack111l1l111l1_opy_):
            with open(bstack111l1l111l1_opy_) as f:
                bstack111ll1111ll_opy_ = json.load(f)
        bstack111ll1111ll_opy_.append(bstack1l1llllll_opy_)
        with open(bstack111l1l111l1_opy_, bstack11l1111_opy_ (u"ࠬࡽࠧᵀ")) as f:
            json.dump(bstack111ll1111ll_opy_, f)
    else:
        bstack1l1llllll_opy_ = {bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᵁ"): test_name, bstack11l1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᵂ"): bstack111ll111111_opy_, bstack11l1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᵃ"): str(multiprocessing.current_process().name)}
        if bstack11l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ᵄ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1llllll_opy_)
  except Exception as e:
      logger.warn(bstack11l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᵅ").format(e))
def bstack1l1ll1ll_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l1111_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧᵆ"))
    try:
      bstack111l1llll1l_opy_ = []
      bstack1l1llllll_opy_ = {bstack11l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᵇ"): test_name, bstack11l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᵈ"): error_message, bstack11l1111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᵉ"): index}
      bstack1111lll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᵊ"))
      if os.path.exists(bstack1111lll1lll_opy_):
          with open(bstack1111lll1lll_opy_) as f:
              bstack111l1llll1l_opy_ = json.load(f)
      bstack111l1llll1l_opy_.append(bstack1l1llllll_opy_)
      with open(bstack1111lll1lll_opy_, bstack11l1111_opy_ (u"ࠩࡺࠫᵋ")) as f:
          json.dump(bstack111l1llll1l_opy_, f)
    except Exception as e:
      logger.warn(bstack11l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᵌ").format(e))
    return
  bstack111l1llll1l_opy_ = []
  bstack1l1llllll_opy_ = {bstack11l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᵍ"): test_name, bstack11l1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᵎ"): error_message, bstack11l1111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᵏ"): index}
  bstack1111lll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᵐ"))
  lock_file = bstack1111lll1lll_opy_ + bstack11l1111_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧᵑ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1111lll1lll_opy_):
          with open(bstack1111lll1lll_opy_, bstack11l1111_opy_ (u"ࠩࡵࠫᵒ")) as f:
              content = f.read().strip()
              if content:
                  bstack111l1llll1l_opy_ = json.load(open(bstack1111lll1lll_opy_))
      bstack111l1llll1l_opy_.append(bstack1l1llllll_opy_)
      with open(bstack1111lll1lll_opy_, bstack11l1111_opy_ (u"ࠪࡻࠬᵓ")) as f:
          json.dump(bstack111l1llll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦᵔ").format(e))
def bstack1ll11l1ll1_opy_(bstack1ll1lllll1_opy_, name, logger):
  try:
    bstack1l1llllll_opy_ = {bstack11l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᵕ"): name, bstack11l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᵖ"): bstack1ll1lllll1_opy_, bstack11l1111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᵗ"): str(threading.current_thread()._name)}
    return bstack1l1llllll_opy_
  except Exception as e:
    logger.warn(bstack11l1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᵘ").format(e))
  return
def bstack111ll111l1l_opy_():
    return platform.system() == bstack11l1111_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪᵙ")
def bstack1lll1l1l11_opy_(bstack111ll11lll1_opy_, config, logger):
    bstack111l1111lll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111ll11lll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᵚ").format(e))
    return bstack111l1111lll_opy_
def bstack111ll1l1ll1_opy_(bstack111l1l1ll11_opy_, bstack111ll1l11l1_opy_):
    bstack111l11ll1ll_opy_ = version.parse(bstack111l1l1ll11_opy_)
    bstack111l1lll111_opy_ = version.parse(bstack111ll1l11l1_opy_)
    if bstack111l11ll1ll_opy_ > bstack111l1lll111_opy_:
        return 1
    elif bstack111l11ll1ll_opy_ < bstack111l1lll111_opy_:
        return -1
    else:
        return 0
def bstack111l111lll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1l1llll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111ll11l1ll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll11l11l_opy_(options, framework, config, bstack1l1l111lll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11l1111_opy_ (u"ࠫ࡬࡫ࡴࠨᵛ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1ll111111_opy_ = caps.get(bstack11l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᵜ"))
    bstack111l1ll1111_opy_ = True
    bstack1111l111l_opy_ = os.environ[bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᵝ")]
    bstack1l111111ll1_opy_ = config.get(bstack11l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᵞ"), False)
    if bstack1l111111ll1_opy_:
        bstack1l111lllll1_opy_ = config.get(bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᵟ"), {})
        bstack1l111lllll1_opy_[bstack11l1111_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᵠ")] = os.getenv(bstack11l1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᵡ"))
        bstack11l1l111ll1_opy_ = json.loads(os.getenv(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᵢ"), bstack11l1111_opy_ (u"ࠬࢁࡽࠨᵣ"))).get(bstack11l1111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᵤ"))
    if bstack111l111lll1_opy_(caps.get(bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭ᵥ"))) or bstack111l111lll1_opy_(caps.get(bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᵦ"))):
        bstack111l1ll1111_opy_ = False
    if bstack11111ll1_opy_({bstack11l1111_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤᵧ"): bstack111l1ll1111_opy_}):
        bstack1ll111111_opy_ = bstack1ll111111_opy_ or {}
        bstack1ll111111_opy_[bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᵨ")] = bstack111ll11l1ll_opy_(framework)
        bstack1ll111111_opy_[bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᵩ")] = bstack1llll1ll1l1_opy_()
        bstack1ll111111_opy_[bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᵪ")] = bstack1111l111l_opy_
        bstack1ll111111_opy_[bstack11l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᵫ")] = bstack1l1l111lll_opy_
        if bstack1l111111ll1_opy_:
            bstack1ll111111_opy_[bstack11l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᵬ")] = bstack1l111111ll1_opy_
            bstack1ll111111_opy_[bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᵭ")] = bstack1l111lllll1_opy_
            bstack1ll111111_opy_[bstack11l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵮ")][bstack11l1111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᵯ")] = bstack11l1l111ll1_opy_
        if getattr(options, bstack11l1111_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᵰ"), None):
            options.set_capability(bstack11l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᵱ"), bstack1ll111111_opy_)
        else:
            options[bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᵲ")] = bstack1ll111111_opy_
    else:
        if getattr(options, bstack11l1111_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᵳ"), None):
            options.set_capability(bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᵴ"), bstack111ll11l1ll_opy_(framework))
            options.set_capability(bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᵵ"), bstack1llll1ll1l1_opy_())
            options.set_capability(bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᵶ"), bstack1111l111l_opy_)
            options.set_capability(bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᵷ"), bstack1l1l111lll_opy_)
            if bstack1l111111ll1_opy_:
                options.set_capability(bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᵸ"), bstack1l111111ll1_opy_)
                options.set_capability(bstack11l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᵹ"), bstack1l111lllll1_opy_)
                options.set_capability(bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᵺ"), bstack11l1l111ll1_opy_)
        else:
            options[bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᵻ")] = bstack111ll11l1ll_opy_(framework)
            options[bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᵼ")] = bstack1llll1ll1l1_opy_()
            options[bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᵽ")] = bstack1111l111l_opy_
            options[bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᵾ")] = bstack1l1l111lll_opy_
            if bstack1l111111ll1_opy_:
                options[bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᵿ")] = bstack1l111111ll1_opy_
                options[bstack11l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᶀ")] = bstack1l111lllll1_opy_
                options[bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᶁ")][bstack11l1111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᶂ")] = bstack11l1l111ll1_opy_
    return options
def bstack111l1111l11_opy_(bstack111l11lll1l_opy_, framework):
    bstack1l1l111lll_opy_ = bstack1l1l11l1ll_opy_.get_property(bstack11l1111_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᶃ"))
    if bstack111l11lll1l_opy_ and len(bstack111l11lll1l_opy_.split(bstack11l1111_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᶄ"))) > 1:
        ws_url = bstack111l11lll1l_opy_.split(bstack11l1111_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᶅ"))[0]
        if bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᶆ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111l111l11l_opy_ = json.loads(urllib.parse.unquote(bstack111l11lll1l_opy_.split(bstack11l1111_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᶇ"))[1]))
            bstack111l111l11l_opy_ = bstack111l111l11l_opy_ or {}
            bstack1111l111l_opy_ = os.environ[bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᶈ")]
            bstack111l111l11l_opy_[bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᶉ")] = str(framework) + str(__version__)
            bstack111l111l11l_opy_[bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᶊ")] = bstack1llll1ll1l1_opy_()
            bstack111l111l11l_opy_[bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᶋ")] = bstack1111l111l_opy_
            bstack111l111l11l_opy_[bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᶌ")] = bstack1l1l111lll_opy_
            bstack111l11lll1l_opy_ = bstack111l11lll1l_opy_.split(bstack11l1111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᶍ"))[0] + bstack11l1111_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᶎ") + urllib.parse.quote(json.dumps(bstack111l111l11l_opy_))
    return bstack111l11lll1l_opy_
def bstack11l1l1l1_opy_():
    global bstack1lll1ll1l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1lll1ll1l1_opy_ = BrowserType.connect
    return bstack1lll1ll1l1_opy_
def bstack1lll11l1_opy_(framework_name):
    global bstack11l1l11l1l_opy_
    bstack11l1l11l1l_opy_ = framework_name
    return framework_name
def bstack1llll1ll1l_opy_(self, *args, **kwargs):
    global bstack1lll1ll1l1_opy_
    try:
        global bstack11l1l11l1l_opy_
        if bstack11l1111_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᶏ") in kwargs:
            kwargs[bstack11l1111_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᶐ")] = bstack111l1111l11_opy_(
                kwargs.get(bstack11l1111_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᶑ"), None),
                bstack11l1l11l1l_opy_
            )
    except Exception as e:
        logger.error(bstack11l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᶒ").format(str(e)))
    return bstack1lll1ll1l1_opy_(self, *args, **kwargs)
def bstack111l1l1l11l_opy_(bstack111l11l1ll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll1l1l1l_opy_(bstack111l11l1ll1_opy_, bstack11l1111_opy_ (u"ࠦࠧᶓ"))
        if proxies and proxies.get(bstack11l1111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᶔ")):
            parsed_url = urlparse(proxies.get(bstack11l1111_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᶕ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11l1111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᶖ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11l1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᶗ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11l1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᶘ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11l1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᶙ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1lll11lll1_opy_(bstack111l11l1ll1_opy_):
    bstack111l11111l1_opy_ = {
        bstack11l111111l1_opy_[bstack111l1l11l1l_opy_]: bstack111l11l1ll1_opy_[bstack111l1l11l1l_opy_]
        for bstack111l1l11l1l_opy_ in bstack111l11l1ll1_opy_
        if bstack111l1l11l1l_opy_ in bstack11l111111l1_opy_
    }
    bstack111l11111l1_opy_[bstack11l1111_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᶚ")] = bstack111l1l1l11l_opy_(bstack111l11l1ll1_opy_, bstack1l1l11l1ll_opy_.get_property(bstack11l1111_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᶛ")))
    bstack111l1ll11l1_opy_ = [element.lower() for element in bstack111llllll1l_opy_]
    bstack111l1lll11l_opy_(bstack111l11111l1_opy_, bstack111l1ll11l1_opy_)
    return bstack111l11111l1_opy_
def bstack111l1lll11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11l1111_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᶜ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l1lll11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l1lll11l_opy_(item, keys)
def bstack1lllllll1l1_opy_():
    bstack111l1l1ll1l_opy_ = [os.environ.get(bstack11l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤᶝ")), os.path.join(os.path.expanduser(bstack11l1111_opy_ (u"ࠣࢀࠥᶞ")), bstack11l1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᶟ")), os.path.join(bstack11l1111_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᶠ"), bstack11l1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᶡ"))]
    for path in bstack111l1l1ll1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11l1111_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᶢ") + str(path) + bstack11l1111_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤᶣ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11l1111_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦᶤ") + str(path) + bstack11l1111_opy_ (u"ࠣࠩࠥᶥ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11l1111_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᶦ") + str(path) + bstack11l1111_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣᶧ"))
            else:
                logger.debug(bstack11l1111_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨᶨ") + str(path) + bstack11l1111_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤᶩ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11l1111_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦᶪ") + str(path) + bstack11l1111_opy_ (u"ࠢࠨ࠰ࠥᶫ"))
            return path
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨᶬ") + str(e) + bstack11l1111_opy_ (u"ࠤࠥᶭ"))
    logger.debug(bstack11l1111_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢᶮ"))
    return None
@measure(event_name=EVENTS.bstack111llll111l_opy_, stage=STAGE.bstack1111llll1_opy_)
def bstack1l11l111ll1_opy_(binary_path, bstack1l111ll1lll_opy_, bs_config):
    logger.debug(bstack11l1111_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥᶯ").format(binary_path))
    bstack111ll11llll_opy_ = bstack11l1111_opy_ (u"ࠬ࠭ᶰ")
    bstack111ll1l111l_opy_ = {
        bstack11l1111_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᶱ"): __version__,
        bstack11l1111_opy_ (u"ࠢࡰࡵࠥᶲ"): platform.system(),
        bstack11l1111_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤᶳ"): platform.machine(),
        bstack11l1111_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᶴ"): bstack11l1111_opy_ (u"ࠪ࠴ࠬᶵ"),
        bstack11l1111_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥᶶ"): bstack11l1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᶷ")
    }
    bstack111l111ll11_opy_(bstack111ll1l111l_opy_)
    try:
        if binary_path:
            bstack111ll1l111l_opy_[bstack11l1111_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᶸ")] = subprocess.check_output([binary_path, bstack11l1111_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᶹ")]).strip().decode(bstack11l1111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᶺ"))
        response = requests.request(
            bstack11l1111_opy_ (u"ࠩࡊࡉ࡙࠭ᶻ"),
            url=bstack11111111_opy_(bstack111lllll1l1_opy_),
            headers=None,
            auth=(bs_config[bstack11l1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᶼ")], bs_config[bstack11l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᶽ")]),
            json=None,
            params=bstack111ll1l111l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11l1111_opy_ (u"ࠬࡻࡲ࡭ࠩᶾ") in data.keys() and bstack11l1111_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᶿ") in data.keys():
            logger.debug(bstack11l1111_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣ᷀").format(bstack111ll1l111l_opy_[bstack11l1111_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᷁")]))
            if bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐ᷂ࠬ") in os.environ:
                logger.debug(bstack11l1111_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡢࡵࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑࠦࡩࡴࠢࡶࡩࡹࠨ᷃"))
                data[bstack11l1111_opy_ (u"ࠫࡺࡸ࡬ࠨ᷄")] = os.environ[bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨ᷅")]
            bstack11l1l1l1ll1_opy_ = bstack111l111l111_opy_(data[bstack11l1111_opy_ (u"࠭ࡵࡳ࡮ࠪ᷆")], bstack1l111ll1lll_opy_)
            bstack111ll11llll_opy_ = os.path.join(bstack1l111ll1lll_opy_, bstack11l1l1l1ll1_opy_)
            os.chmod(bstack111ll11llll_opy_, 0o777) # bstack111l1l11lll_opy_ permission
            return bstack111ll11llll_opy_
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢ᷇").format(e))
    return binary_path
def bstack111l111ll11_opy_(bstack111ll1l111l_opy_):
    try:
        if bstack11l1111_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧ᷈") not in bstack111ll1l111l_opy_[bstack11l1111_opy_ (u"ࠩࡲࡷࠬ᷉")].lower():
            return
        if os.path.exists(bstack11l1111_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩ᷊ࠧ")):
            with open(bstack11l1111_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ᷋"), bstack11l1111_opy_ (u"ࠧࡸࠢ᷌")) as f:
                bstack111ll11ll1l_opy_ = {}
                for line in f:
                    if bstack11l1111_opy_ (u"ࠨ࠽ࠣ᷍") in line:
                        key, value = line.rstrip().split(bstack11l1111_opy_ (u"ࠢ࠾ࠤ᷎"), 1)
                        bstack111ll11ll1l_opy_[key] = value.strip(bstack11l1111_opy_ (u"ࠨࠤ࡟᷏ࠫࠬ"))
                bstack111ll1l111l_opy_[bstack11l1111_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰ᷐ࠩ")] = bstack111ll11ll1l_opy_.get(bstack11l1111_opy_ (u"ࠥࡍࡉࠨ᷑"), bstack11l1111_opy_ (u"ࠦࠧ᷒"))
        elif os.path.exists(bstack11l1111_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡥࡱࡶࡩ࡯ࡧ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᷓ")):
            bstack111ll1l111l_opy_[bstack11l1111_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭ᷔ")] = bstack11l1111_opy_ (u"ࠧࡢ࡮ࡳ࡭ࡳ࡫ࠧᷕ")
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡦ࡬ࡷࡹࡸ࡯ࠡࡱࡩࠤࡱ࡯࡮ࡶࡺࠥᷖ") + e)
@measure(event_name=EVENTS.bstack11l1111111l_opy_, stage=STAGE.bstack1111llll1_opy_)
def bstack111l111l111_opy_(bstack111l1ll1l1l_opy_, bstack111l11111ll_opy_):
    logger.debug(bstack11l1111_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦᷗ") + str(bstack111l1ll1l1l_opy_) + bstack11l1111_opy_ (u"ࠥࠦᷘ"))
    zip_path = os.path.join(bstack111l11111ll_opy_, bstack11l1111_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥᷙ"))
    bstack11l1l1l1ll1_opy_ = bstack11l1111_opy_ (u"ࠬ࠭ᷚ")
    with requests.get(bstack111l1ll1l1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11l1111_opy_ (u"ࠨࡷࡣࠤᷛ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11l1111_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤᷜ"))
    with zipfile.ZipFile(zip_path, bstack11l1111_opy_ (u"ࠨࡴࠪᷝ")) as zip_ref:
        bstack111ll1l1l1l_opy_ = zip_ref.namelist()
        if len(bstack111ll1l1l1l_opy_) > 0:
            bstack11l1l1l1ll1_opy_ = bstack111ll1l1l1l_opy_[0] # bstack111l11ll11l_opy_ bstack11l11111l1l_opy_ will be bstack111l1l1lll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111l11111ll_opy_)
        logger.debug(bstack11l1111_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣᷞ") + str(bstack111l11111ll_opy_) + bstack11l1111_opy_ (u"ࠥࠫࠧᷟ"))
    os.remove(zip_path)
    return bstack11l1l1l1ll1_opy_
def get_cli_dir():
    bstack111ll11l11l_opy_ = bstack1lllllll1l1_opy_()
    if bstack111ll11l11l_opy_:
        bstack1l111ll1lll_opy_ = os.path.join(bstack111ll11l11l_opy_, bstack11l1111_opy_ (u"ࠦࡨࡲࡩࠣᷠ"))
        if not os.path.exists(bstack1l111ll1lll_opy_):
            os.makedirs(bstack1l111ll1lll_opy_, mode=0o777, exist_ok=True)
        return bstack1l111ll1lll_opy_
    else:
        raise FileNotFoundError(bstack11l1111_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠣᷡ"))
def bstack1l11l1ll1ll_opy_(bstack1l111ll1lll_opy_):
    bstack11l1111_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤࠥᷢ")
    bstack111l1lll1ll_opy_ = [
        os.path.join(bstack1l111ll1lll_opy_, f)
        for f in os.listdir(bstack1l111ll1lll_opy_)
        if os.path.isfile(os.path.join(bstack1l111ll1lll_opy_, f)) and f.startswith(bstack11l1111_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣᷣ"))
    ]
    if len(bstack111l1lll1ll_opy_) > 0:
        return max(bstack111l1lll1ll_opy_, key=os.path.getmtime) # get bstack11l1lll111l_opy_ binary
    return bstack11l1111_opy_ (u"ࠣࠤᷤ")
def bstack11l1l11ll11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11lllll11ll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack11lllll11ll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1l1l11l1_opy_(data, keys, default=None):
    bstack11l1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡥ࡫࡫࡬ࡺࠢࡪࡩࡹࠦࡡࠡࡰࡨࡷࡹ࡫ࡤࠡࡸࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡦࡺࡡ࠻ࠢࡗ࡬ࡪࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡹࡵࠠࡵࡴࡤࡺࡪࡸࡳࡦ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠ࡬ࡧࡼࡷ࠿ࠦࡁࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢ࡮ࡩࡾࡹ࠯ࡪࡰࡧ࡭ࡨ࡫ࡳࠡࡴࡨࡴࡷ࡫ࡳࡦࡰࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡧࡩࡥࡺࡲࡴ࠻࡙ࠢࡥࡱࡻࡥࠡࡶࡲࠤࡷ࡫ࡴࡶࡴࡱࠤ࡮࡬ࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡵࡩࡹࡻࡲ࡯࠼ࠣࡘ࡭࡫ࠠࡷࡣ࡯ࡹࡪࠦࡡࡵࠢࡷ࡬ࡪࠦ࡮ࡦࡵࡷࡩࡩࠦࡰࡢࡶ࡫࠰ࠥࡵࡲࠡࡦࡨࡪࡦࡻ࡬ࡵࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᷥ")
    if not data:
        return default
    current = data
    try:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError):
        return default