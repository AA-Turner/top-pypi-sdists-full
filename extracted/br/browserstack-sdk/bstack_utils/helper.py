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
from bstack_utils.constants import (bstack11ll1llll_opy_, bstack11l1ll11l1_opy_, bstack11l1l11l1l_opy_,
                                    bstack11l1ll1l11l_opy_, bstack11l1l1lll11_opy_, bstack11l1ll111ll_opy_, bstack11l1lll11ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1l1lll1_opy_, bstack11l111l11l_opy_
from bstack_utils.proxy import bstack1lllll11l1_opy_, bstack1l111ll111_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1111ll_opy_
from bstack_utils.bstack111111ll_opy_ import bstack1ll1l1ll_opy_
from browserstack_sdk._version import __version__
bstack1ll1ll11_opy_ = Config.bstack1ll11ll1_opy_()
logger = bstack1l1111ll_opy_.get_logger(__name__, bstack1l1111ll_opy_.bstack1lll1llll1l_opy_())
def bstack11ll1lll111_opy_(config):
    return config[bstack111l111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ᫮")]
def bstack11ll1l1lll1_opy_(config):
    return config[bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ᫯")]
def bstack1ll1l1l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11lll111_opy_(obj):
    values = []
    bstack111lll1ll11_opy_ = re.compile(bstack111l111_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧ᫰"), re.I)
    for key in obj.keys():
        if bstack111lll1ll11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111llll1lll_opy_(config):
    tags = []
    tags.extend(bstack11l11lll111_opy_(os.environ))
    tags.extend(bstack11l11lll111_opy_(config))
    return tags
def bstack11l11ll1ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11111l1l_opy_(bstack11l11llll11_opy_):
    if not bstack11l11llll11_opy_:
        return bstack111l111_opy_ (u"ࠩࠪ᫱")
    return bstack111l111_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿࠬࠦ᫲").format(bstack11l11llll11_opy_.name, bstack11l11llll11_opy_.email)
def bstack11ll1ll11l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1l11111l_opy_ = repo.common_dir
        info = {
            bstack111l111_opy_ (u"ࠦࡸ࡮ࡡࠣ᫳"): repo.head.commit.hexsha,
            bstack111l111_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣ᫴"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111l111_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨ᫵"): repo.active_branch.name,
            bstack111l111_opy_ (u"ࠢࡵࡣࡪࠦ᫶"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111l111_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦ᫷"): bstack11l11111l1l_opy_(repo.head.commit.committer),
            bstack111l111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥ᫸"): repo.head.commit.committed_datetime.isoformat(),
            bstack111l111_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥ᫹"): bstack11l11111l1l_opy_(repo.head.commit.author),
            bstack111l111_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤ᫺"): repo.head.commit.authored_datetime.isoformat(),
            bstack111l111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᫻"): repo.head.commit.message,
            bstack111l111_opy_ (u"ࠨࡲࡰࡱࡷࠦ᫼"): repo.git.rev_parse(bstack111l111_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤ᫽")),
            bstack111l111_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤ᫾"): bstack11l1l11111l_opy_,
            bstack111l111_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ᫿"): subprocess.check_output([bstack111l111_opy_ (u"ࠥ࡫࡮ࡺࠢᬀ"), bstack111l111_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢᬁ"), bstack111l111_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣᬂ")]).strip().decode(
                bstack111l111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᬃ")),
            bstack111l111_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤᬄ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111l111_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᬅ"): repo.git.rev_list(
                bstack111l111_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤᬆ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111lll1llll_opy_ = []
        for remote in remotes:
            bstack11l11ll111l_opy_ = {
                bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣᬇ"): remote.name,
                bstack111l111_opy_ (u"ࠦࡺࡸ࡬ࠣᬈ"): remote.url,
            }
            bstack111lll1llll_opy_.append(bstack11l11ll111l_opy_)
        bstack11l11l1l111_opy_ = {
            bstack111l111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬉ"): bstack111l111_opy_ (u"ࠨࡧࡪࡶࠥᬊ"),
            **info,
            bstack111l111_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳࠣᬋ"): bstack111lll1llll_opy_
        }
        bstack11l11l1l111_opy_ = bstack11l11l111ll_opy_(bstack11l11l1l111_opy_)
        return bstack11l11l1l111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack111l111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᬌ").format(err))
        return {}
def bstack11l11l111ll_opy_(bstack11l11l1l111_opy_):
    bstack11l11lll11l_opy_ = bstack11l11l11111_opy_(bstack11l11l1l111_opy_)
    if bstack11l11lll11l_opy_ and bstack11l11lll11l_opy_ > bstack11l1ll1l11l_opy_:
        bstack111lll111ll_opy_ = bstack11l11lll11l_opy_ - bstack11l1ll1l11l_opy_
        bstack111lllll1ll_opy_ = bstack11l1111l1l1_opy_(bstack11l11l1l111_opy_[bstack111l111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᬍ")], bstack111lll111ll_opy_)
        bstack11l11l1l111_opy_[bstack111l111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᬎ")] = bstack111lllll1ll_opy_
        logger.info(bstack111l111_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨᬏ")
                    .format(bstack11l11l11111_opy_(bstack11l11l1l111_opy_) / 1024))
    return bstack11l11l1l111_opy_
def bstack11l11l11111_opy_(bstack11lll111_opy_):
    try:
        if bstack11lll111_opy_:
            bstack11l11111l11_opy_ = json.dumps(bstack11lll111_opy_)
            bstack111lll1lll1_opy_ = sys.getsizeof(bstack11l11111l11_opy_)
            return bstack111lll1lll1_opy_
    except Exception as e:
        logger.debug(bstack111l111_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧᬐ").format(e))
    return -1
def bstack11l1111l1l1_opy_(field, bstack11l111111l1_opy_):
    try:
        bstack111llll111l_opy_ = len(bytes(bstack11l1l1lll11_opy_, bstack111l111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᬑ")))
        bstack11l1l1111ll_opy_ = bytes(field, bstack111l111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᬒ"))
        bstack11l11l11ll1_opy_ = len(bstack11l1l1111ll_opy_)
        bstack111lllll111_opy_ = ceil(bstack11l11l11ll1_opy_ - bstack11l111111l1_opy_ - bstack111llll111l_opy_)
        if bstack111lllll111_opy_ > 0:
            bstack11l111l11l1_opy_ = bstack11l1l1111ll_opy_[:bstack111lllll111_opy_].decode(bstack111l111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᬓ"), errors=bstack111l111_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩᬔ")) + bstack11l1l1lll11_opy_
            return bstack11l111l11l1_opy_
    except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣᬕ").format(e))
    return field
def bstack1ll1l11111_opy_():
    env = os.environ
    if (bstack111l111_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᬖ") in env and len(env[bstack111l111_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᬗ")]) > 0) or (
            bstack111l111_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᬘ") in env and len(env[bstack111l111_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᬙ")]) > 0):
        return {
            bstack111l111_opy_ (u"ࠣࡰࡤࡱࡪࠨᬚ"): bstack111l111_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥᬛ"),
            bstack111l111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬜ"): env.get(bstack111l111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᬝ")),
            bstack111l111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬞ"): env.get(bstack111l111_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣᬟ")),
            bstack111l111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬠ"): env.get(bstack111l111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᬡ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠤࡆࡍࠧᬢ")) == bstack111l111_opy_ (u"ࠥࡸࡷࡻࡥࠣᬣ") and bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨᬤ"))):
        return {
            bstack111l111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬥ"): bstack111l111_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣᬦ"),
            bstack111l111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬧ"): env.get(bstack111l111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᬨ")),
            bstack111l111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᬩ"): env.get(bstack111l111_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢᬪ")),
            bstack111l111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᬫ"): env.get(bstack111l111_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣᬬ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠨࡃࡊࠤᬭ")) == bstack111l111_opy_ (u"ࠢࡵࡴࡸࡩࠧᬮ") and bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᬯ"))):
        return {
            bstack111l111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬰ"): bstack111l111_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᬱ"),
            bstack111l111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᬲ"): env.get(bstack111l111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᬳ")),
            bstack111l111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᬴ࠣ"): env.get(bstack111l111_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᬵ")),
            bstack111l111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᬶ"): env.get(bstack111l111_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᬷ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠥࡇࡎࠨᬸ")) == bstack111l111_opy_ (u"ࠦࡹࡸࡵࡦࠤᬹ") and env.get(bstack111l111_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᬺ")) == bstack111l111_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᬻ"):
        return {
            bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬼ"): bstack111l111_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᬽ"),
            bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᬾ"): None,
            bstack111l111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᬿ"): None,
            bstack111l111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᭀ"): None
        }
    if env.get(bstack111l111_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᭁ")) and env.get(bstack111l111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᭂ")):
        return {
            bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᭃ"): bstack111l111_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷ᭄ࠦ"),
            bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᭅ"): env.get(bstack111l111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᭆ")),
            bstack111l111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᭇ"): None,
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᭈ"): env.get(bstack111l111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᭉ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠢࡄࡋࠥᭊ")) == bstack111l111_opy_ (u"ࠣࡶࡵࡹࡪࠨᭋ") and bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣᭌ"))):
        return {
            bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᭍"): bstack111l111_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥ᭎"),
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᭏"): env.get(bstack111l111_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤ᭐")),
            bstack111l111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᭑"): None,
            bstack111l111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᭒"): env.get(bstack111l111_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᭓"))
        }
    if env.get(bstack111l111_opy_ (u"ࠥࡇࡎࠨ᭔")) == bstack111l111_opy_ (u"ࠦࡹࡸࡵࡦࠤ᭕") and bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣ᭖"))):
        return {
            bstack111l111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᭗"): bstack111l111_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥ᭘"),
            bstack111l111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᭙"): env.get(bstack111l111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣ᭚")),
            bstack111l111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭛"): env.get(bstack111l111_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᭜")),
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᭝"): env.get(bstack111l111_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤ᭞"))
        }
    if env.get(bstack111l111_opy_ (u"ࠢࡄࡋࠥ᭟")) == bstack111l111_opy_ (u"ࠣࡶࡵࡹࡪࠨ᭠") and bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧ᭡"))):
        return {
            bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᭢"): bstack111l111_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦ᭣"),
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᭤"): env.get(bstack111l111_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥ᭥")),
            bstack111l111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᭦"): env.get(bstack111l111_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᭧")),
            bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᭨"): env.get(bstack111l111_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨ᭩"))
        }
    if env.get(bstack111l111_opy_ (u"ࠦࡈࡏࠢ᭪")) == bstack111l111_opy_ (u"ࠧࡺࡲࡶࡧࠥ᭫") and bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤ᭬"))):
        return {
            bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭭"): bstack111l111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦ᭮"),
            bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭯"): env.get(bstack111l111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᭰")),
            bstack111l111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᭱"): env.get(bstack111l111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢ᭲")) or env.get(bstack111l111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ᭳")),
            bstack111l111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᭴"): env.get(bstack111l111_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᭵"))
        }
    if bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦ᭶"))):
        return {
            bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᭷"): bstack111l111_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦ᭸"),
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᭹"): bstack111l111_opy_ (u"ࠨࡻࡾࡽࢀࠦ᭺").format(env.get(bstack111l111_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪ᭻")), env.get(bstack111l111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨ᭼"))),
            bstack111l111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᭽"): env.get(bstack111l111_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤ᭾")),
            bstack111l111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᭿"): env.get(bstack111l111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᮀ"))
        }
    if bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᮁ"))):
        return {
            bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮂ"): bstack111l111_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᮃ"),
            bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮄ"): bstack111l111_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤᮅ").format(env.get(bstack111l111_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪᮆ")), env.get(bstack111l111_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ᮇ")), env.get(bstack111l111_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧᮈ")), env.get(bstack111l111_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫᮉ"))),
            bstack111l111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮊ"): env.get(bstack111l111_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᮋ")),
            bstack111l111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮌ"): env.get(bstack111l111_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᮍ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨᮎ")) and env.get(bstack111l111_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᮏ")):
        return {
            bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮐ"): bstack111l111_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥᮑ"),
            bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮒ"): bstack111l111_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨᮓ").format(env.get(bstack111l111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᮔ")), env.get(bstack111l111_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᮕ")), env.get(bstack111l111_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ᮖ"))),
            bstack111l111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮗ"): env.get(bstack111l111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᮘ")),
            bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᮙ"): env.get(bstack111l111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᮚ"))
        }
    if any([env.get(bstack111l111_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᮛ")), env.get(bstack111l111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᮜ")), env.get(bstack111l111_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᮝ"))]):
        return {
            bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮞ"): bstack111l111_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᮟ"),
            bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮠ"): env.get(bstack111l111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᮡ")),
            bstack111l111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᮢ"): env.get(bstack111l111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᮣ")),
            bstack111l111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᮤ"): env.get(bstack111l111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᮥ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᮦ")):
        return {
            bstack111l111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮧ"): bstack111l111_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥᮨ"),
            bstack111l111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᮩ"): env.get(bstack111l111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲ᮪ࠢ")),
            bstack111l111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᮫ࠣ"): env.get(bstack111l111_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨᮬ")),
            bstack111l111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮭ"): env.get(bstack111l111_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᮮ"))
        }
    if env.get(bstack111l111_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦᮯ")) or env.get(bstack111l111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ᮰")):
        return {
            bstack111l111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᮱"): bstack111l111_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢ᮲"),
            bstack111l111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᮳"): env.get(bstack111l111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᮴")),
            bstack111l111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᮵"): bstack111l111_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥ᮶") if env.get(bstack111l111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ᮷")) else None,
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᮸"): env.get(bstack111l111_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦ᮹"))
        }
    if any([env.get(bstack111l111_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧᮺ")), env.get(bstack111l111_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᮻ")), env.get(bstack111l111_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᮼ"))]):
        return {
            bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣᮽ"): bstack111l111_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥᮾ"),
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮿ"): None,
            bstack111l111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᯀ"): env.get(bstack111l111_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦᯁ")),
            bstack111l111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᯂ"): env.get(bstack111l111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᯃ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨᯄ")):
        return {
            bstack111l111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᯅ"): bstack111l111_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣᯆ"),
            bstack111l111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯇ"): env.get(bstack111l111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᯈ")),
            bstack111l111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᯉ"): bstack111l111_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥᯊ").format(env.get(bstack111l111_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭ᯋ"))) if env.get(bstack111l111_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᯌ")) else None,
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᯍ"): env.get(bstack111l111_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᯎ"))
        }
    if bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣᯏ"))):
        return {
            bstack111l111_opy_ (u"ࠣࡰࡤࡱࡪࠨᯐ"): bstack111l111_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥᯑ"),
            bstack111l111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᯒ"): env.get(bstack111l111_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣᯓ")),
            bstack111l111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᯔ"): env.get(bstack111l111_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤᯕ")),
            bstack111l111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᯖ"): env.get(bstack111l111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᯗ"))
        }
    if bstack1ll111l11l_opy_(env.get(bstack111l111_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥᯘ"))):
        return {
            bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣᯙ"): bstack111l111_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧᯚ"),
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯛ"): bstack111l111_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢᯜ").format(env.get(bstack111l111_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫᯝ")), env.get(bstack111l111_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬᯞ")), env.get(bstack111l111_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩᯟ"))),
            bstack111l111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᯠ"): env.get(bstack111l111_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨᯡ")),
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᯢ"): env.get(bstack111l111_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨᯣ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠢࡄࡋࠥᯤ")) == bstack111l111_opy_ (u"ࠣࡶࡵࡹࡪࠨᯥ") and env.get(bstack111l111_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤ᯦")) == bstack111l111_opy_ (u"ࠥ࠵ࠧᯧ"):
        return {
            bstack111l111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᯨ"): bstack111l111_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧᯩ"),
            bstack111l111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯪ"): bstack111l111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥᯫ").format(env.get(bstack111l111_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬᯬ"))),
            bstack111l111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᯭ"): None,
            bstack111l111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᯮ"): None,
        }
    if env.get(bstack111l111_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢᯯ")):
        return {
            bstack111l111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯰ"): bstack111l111_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣᯱ"),
            bstack111l111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᯲ࠥ"): None,
            bstack111l111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧ᯳ࠥ"): env.get(bstack111l111_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥ᯴")),
            bstack111l111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᯵"): env.get(bstack111l111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᯶"))
        }
    if any([env.get(bstack111l111_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣ᯷")), env.get(bstack111l111_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨ᯸")), env.get(bstack111l111_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧ᯹")), env.get(bstack111l111_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤ᯺"))]):
        return {
            bstack111l111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᯻"): bstack111l111_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨ᯼"),
            bstack111l111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᯽"): None,
            bstack111l111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᯾"): env.get(bstack111l111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᯿")) or None,
            bstack111l111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᰀ"): env.get(bstack111l111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᰁ"), 0)
        }
    if env.get(bstack111l111_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᰂ")):
        return {
            bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣᰃ"): bstack111l111_opy_ (u"ࠦࡌࡵࡃࡅࠤᰄ"),
            bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᰅ"): None,
            bstack111l111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᰆ"): env.get(bstack111l111_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᰇ")),
            bstack111l111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰈ"): env.get(bstack111l111_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣᰉ"))
        }
    if env.get(bstack111l111_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᰊ")):
        return {
            bstack111l111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᰋ"): bstack111l111_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣᰌ"),
            bstack111l111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᰍ"): env.get(bstack111l111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᰎ")),
            bstack111l111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᰏ"): env.get(bstack111l111_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᰐ")),
            bstack111l111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰑ"): env.get(bstack111l111_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᰒ"))
        }
    return {bstack111l111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᰓ"): None}
def get_host_info():
    return {
        bstack111l111_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣᰔ"): platform.node(),
        bstack111l111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤᰕ"): platform.system(),
        bstack111l111_opy_ (u"ࠣࡶࡼࡴࡪࠨᰖ"): platform.machine(),
        bstack111l111_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥᰗ"): platform.version(),
        bstack111l111_opy_ (u"ࠥࡥࡷࡩࡨࠣᰘ"): platform.architecture()[0]
    }
def bstack1l1llll1l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11l111l1_opy_():
    if bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬᰙ")):
        return bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᰚ")
    return bstack111l111_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬᰛ")
def bstack11l11ll1l11_opy_(driver):
    info = {
        bstack111l111_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᰜ"): driver.capabilities,
        bstack111l111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬᰝ"): driver.session_id,
        bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᰞ"): driver.capabilities.get(bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᰟ"), None),
        bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᰠ"): driver.capabilities.get(bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᰡ"), None),
        bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨᰢ"): driver.capabilities.get(bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᰣ"), None),
        bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᰤ"):driver.capabilities.get(bstack111l111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᰥ"), None),
    }
    if bstack11l11l111l1_opy_() == bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᰦ"):
        if bstack1lll11111_opy_():
            info[bstack111l111_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᰧ")] = bstack111l111_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᰨ")
        elif driver.capabilities.get(bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᰩ"), {}).get(bstack111l111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᰪ"), False):
            info[bstack111l111_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᰫ")] = bstack111l111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᰬ")
        else:
            info[bstack111l111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᰭ")] = bstack111l111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᰮ")
    return info
def bstack1lll11111_opy_():
    if bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᰯ")):
        return True
    if bstack1ll111l11l_opy_(os.environ.get(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᰰ"), None)):
        return True
    return False
def bstack1llll111l_opy_(bstack11l11ll1111_opy_, url, data, config):
    headers = config.get(bstack111l111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᰱ"), None)
    proxies = bstack1lllll11l1_opy_(config, url)
    auth = config.get(bstack111l111_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᰲ"), None)
    response = requests.request(
            bstack11l11ll1111_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l11l1ll11_opy_(bstack1l11ll1ll_opy_, size):
    bstack11lll1l1ll_opy_ = []
    while len(bstack1l11ll1ll_opy_) > size:
        bstack1ll1l1111l_opy_ = bstack1l11ll1ll_opy_[:size]
        bstack11lll1l1ll_opy_.append(bstack1ll1l1111l_opy_)
        bstack1l11ll1ll_opy_ = bstack1l11ll1ll_opy_[size:]
    bstack11lll1l1ll_opy_.append(bstack1l11ll1ll_opy_)
    return bstack11lll1l1ll_opy_
def bstack11l111l1111_opy_(message, bstack11l1111l111_opy_=False):
    os.write(1, bytes(message, bstack111l111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᰳ")))
    os.write(1, bytes(bstack111l111_opy_ (u"ࠪࡠࡳ࠭ᰴ"), bstack111l111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᰵ")))
    if bstack11l1111l111_opy_:
        with open(bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫᰶ") + os.environ[bstack111l111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈ᰷ࠬ")] + bstack111l111_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬ᰸"), bstack111l111_opy_ (u"ࠨࡣࠪ᰹")) as f:
            f.write(message + bstack111l111_opy_ (u"ࠩ࡟ࡲࠬ᰺"))
def bstack1l1ll11llll_opy_():
    return os.environ[bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭᰻")].lower() == bstack111l111_opy_ (u"ࠫࡹࡸࡵࡦࠩ᰼")
def bstack1ll1ll1l1_opy_():
    return bstack111l1ll111_opy_().replace(tzinfo=None).isoformat() + bstack111l111_opy_ (u"ࠬࡠࠧ᰽")
def bstack111lll1ll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111l111_opy_ (u"࡚࠭ࠨ᰾"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111l111_opy_ (u"࡛ࠧࠩ᰿")))).total_seconds() * 1000
def bstack111lll1l1ll_opy_(timestamp):
    return bstack11l111l1l1l_opy_(timestamp).isoformat() + bstack111l111_opy_ (u"ࠨ࡜ࠪ᱀")
def bstack111llll1l11_opy_(bstack11l11l1l1ll_opy_):
    date_format = bstack111l111_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧ᱁")
    bstack11l11ll11ll_opy_ = datetime.datetime.strptime(bstack11l11l1l1ll_opy_, date_format)
    return bstack11l11ll11ll_opy_.isoformat() + bstack111l111_opy_ (u"ࠪ࡞ࠬ᱂")
def bstack111lllll1l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111l111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᱃")
    else:
        return bstack111l111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᱄")
def bstack1ll111l11l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111l111_opy_ (u"࠭ࡴࡳࡷࡨࠫ᱅")
def bstack11l1111111l_opy_(val):
    return val.__str__().lower() == bstack111l111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭᱆")
def bstack111l1l1l1l_opy_(bstack11l1111ll11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1111ll11_opy_ as e:
                print(bstack111l111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣ᱇").format(func.__name__, bstack11l1111ll11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11l1lll1_opy_(bstack11l11l11l11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11l11l11_opy_(cls, *args, **kwargs)
            except bstack11l1111ll11_opy_ as e:
                print(bstack111l111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤ᱈").format(bstack11l11l11l11_opy_.__name__, bstack11l1111ll11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11l1lll1_opy_
    else:
        return decorator
def bstack1lllll1lll_opy_(bstack11111l1ll1_opy_):
    if os.getenv(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭᱉")) is not None:
        return bstack1ll111l11l_opy_(os.getenv(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᱊")))
    if bstack111l111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ᱋") in bstack11111l1ll1_opy_ and bstack11l1111111l_opy_(bstack11111l1ll1_opy_[bstack111l111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᱌")]):
        return False
    if bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᱍ") in bstack11111l1ll1_opy_ and bstack11l1111111l_opy_(bstack11111l1ll1_opy_[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᱎ")]):
        return False
    return True
def bstack11l1l11l_opy_():
    try:
        from pytest_bdd import reporting
        bstack111lll11ll1_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤᱏ"), None)
        return bstack111lll11ll1_opy_ is None or bstack111lll11ll1_opy_ == bstack111l111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢ᱐")
    except Exception as e:
        return False
def bstack1l11l11ll1_opy_(hub_url, CONFIG):
    if bstack1llllll1l_opy_() <= version.parse(bstack111l111_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ᱑")):
        if hub_url:
            return bstack111l111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ᱒") + hub_url + bstack111l111_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ᱓")
        return bstack11l1ll11l1_opy_
    if hub_url:
        return bstack111l111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ᱔") + hub_url + bstack111l111_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ᱕")
    return bstack11l1l11l1l_opy_
def bstack111llll11l1_opy_():
    return isinstance(os.getenv(bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨ᱖")), str)
def bstack11lll1l1l_opy_(url):
    return urlparse(url).hostname
def bstack11l1l111l1_opy_(hostname):
    for bstack1l1l1ll1ll_opy_ in bstack11ll1llll_opy_:
        regex = re.compile(bstack1l1l1ll1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l111111_opy_(bstack11l1111l11l_opy_, file_name, logger):
    bstack11l1l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠪࢂࠬ᱗")), bstack11l1111l11l_opy_)
    try:
        if not os.path.exists(bstack11l1l1l1l1_opy_):
            os.makedirs(bstack11l1l1l1l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠫࢃ࠭᱘")), bstack11l1111l11l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111l111_opy_ (u"ࠬࡽࠧ᱙")):
                pass
            with open(file_path, bstack111l111_opy_ (u"ࠨࡷࠬࠤᱚ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l1l1lll1_opy_.format(str(e)))
def bstack111lll11lll_opy_(file_name, key, value, logger):
    file_path = bstack11l1l111111_opy_(bstack111l111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᱛ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lllll1ll1_opy_ = json.load(open(file_path, bstack111l111_opy_ (u"ࠨࡴࡥࠫᱜ")))
        else:
            bstack1lllll1ll1_opy_ = {}
        bstack1lllll1ll1_opy_[key] = value
        with open(file_path, bstack111l111_opy_ (u"ࠤࡺ࠯ࠧᱝ")) as outfile:
            json.dump(bstack1lllll1ll1_opy_, outfile)
def bstack111ll11ll_opy_(file_name, logger):
    file_path = bstack11l1l111111_opy_(bstack111l111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᱞ"), file_name, logger)
    bstack1lllll1ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111l111_opy_ (u"ࠫࡷ࠭ᱟ")) as bstack111llll11_opy_:
            bstack1lllll1ll1_opy_ = json.load(bstack111llll11_opy_)
    return bstack1lllll1ll1_opy_
def bstack1l1llll111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᱠ") + file_path + bstack111l111_opy_ (u"࠭ࠠࠨᱡ") + str(e))
def bstack1llllll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111l111_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᱢ")
def bstack1l11ll11l_opy_(config):
    if bstack111l111_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᱣ") in config:
        del (config[bstack111l111_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᱤ")])
        return False
    if bstack1llllll1l_opy_() < version.parse(bstack111l111_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᱥ")):
        return False
    if bstack1llllll1l_opy_() >= version.parse(bstack111l111_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᱦ")):
        return True
    if bstack111l111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᱧ") in config and config[bstack111l111_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᱨ")] is False:
        return False
    else:
        return True
def bstack1l1111l11_opy_(args_list, bstack11l1l111l11_opy_):
    index = -1
    for value in bstack11l1l111l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll11lllll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll11lllll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111lll1ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111lll1ll1_opy_ = bstack111lll1ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111l111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᱩ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111l111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᱪ"), exception=exception)
    def bstack111111llll_opy_(self):
        if self.result != bstack111l111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᱫ"):
            return None
        if isinstance(self.exception_type, str) and bstack111l111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᱬ") in self.exception_type:
            return bstack111l111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᱭ")
        return bstack111l111_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᱮ")
    def bstack11l1111ll1l_opy_(self):
        if self.result != bstack111l111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᱯ"):
            return None
        if self.bstack111lll1ll1_opy_:
            return self.bstack111lll1ll1_opy_
        return bstack111llll11ll_opy_(self.exception)
def bstack111llll11ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l111lll11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll11lllll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1llll1ll11_opy_(config, logger):
    try:
        import playwright
        bstack11l11l1ll11_opy_ = playwright.__file__
        bstack11l111ll111_opy_ = os.path.split(bstack11l11l1ll11_opy_)
        bstack11l111l111l_opy_ = bstack11l111ll111_opy_[0] + bstack111l111_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᱰ")
        os.environ[bstack111l111_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᱱ")] = bstack1l111ll111_opy_(config)
        with open(bstack11l111l111l_opy_, bstack111l111_opy_ (u"ࠩࡵࠫᱲ")) as f:
            bstack1l111111l_opy_ = f.read()
            bstack111llllll11_opy_ = bstack111l111_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᱳ")
            bstack11l1l1111l1_opy_ = bstack1l111111l_opy_.find(bstack111llllll11_opy_)
            if bstack11l1l1111l1_opy_ == -1:
              process = subprocess.Popen(bstack111l111_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᱴ"), shell=True, cwd=bstack11l111ll111_opy_[0])
              process.wait()
              bstack11l111l1lll_opy_ = bstack111l111_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᱵ")
              bstack11l11lll1ll_opy_ = bstack111l111_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᱶ")
              bstack11l11llllll_opy_ = bstack1l111111l_opy_.replace(bstack11l111l1lll_opy_, bstack11l11lll1ll_opy_)
              with open(bstack11l111l111l_opy_, bstack111l111_opy_ (u"ࠧࡸࠩᱷ")) as f:
                f.write(bstack11l11llllll_opy_)
    except Exception as e:
        logger.error(bstack11l111l11l_opy_.format(str(e)))
def bstack11lll1l1_opy_():
  try:
    bstack11l11lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᱸ"))
    bstack11l11l1l11l_opy_ = []
    if os.path.exists(bstack11l11lllll1_opy_):
      with open(bstack11l11lllll1_opy_) as f:
        bstack11l11l1l11l_opy_ = json.load(f)
      os.remove(bstack11l11lllll1_opy_)
    return bstack11l11l1l11l_opy_
  except:
    pass
  return []
def bstack11l111111_opy_(bstack1l111l1ll1_opy_):
  try:
    bstack11l11l1l11l_opy_ = []
    bstack11l11lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᱹ"))
    if os.path.exists(bstack11l11lllll1_opy_):
      with open(bstack11l11lllll1_opy_) as f:
        bstack11l11l1l11l_opy_ = json.load(f)
    bstack11l11l1l11l_opy_.append(bstack1l111l1ll1_opy_)
    with open(bstack11l11lllll1_opy_, bstack111l111_opy_ (u"ࠪࡻࠬᱺ")) as f:
        json.dump(bstack11l11l1l11l_opy_, f)
  except:
    pass
def bstack1ll1ll1111_opy_(logger, bstack11l11ll1l1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack111l111_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᱻ"), bstack111l111_opy_ (u"ࠬ࠭ᱼ"))
    if test_name == bstack111l111_opy_ (u"࠭ࠧᱽ"):
        test_name = threading.current_thread().__dict__.get(bstack111l111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭᱾"), bstack111l111_opy_ (u"ࠨࠩ᱿"))
    bstack11l1111l1ll_opy_ = bstack111l111_opy_ (u"ࠩ࠯ࠤࠬᲀ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11ll1l1l_opy_:
        bstack11ll11l111_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᲁ"), bstack111l111_opy_ (u"ࠫ࠵࠭ᲂ"))
        bstack11l1111111_opy_ = {bstack111l111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᲃ"): test_name, bstack111l111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᲄ"): bstack11l1111l1ll_opy_, bstack111l111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᲅ"): bstack11ll11l111_opy_}
        bstack11l1111lll1_opy_ = []
        bstack11l11l11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᲆ"))
        if os.path.exists(bstack11l11l11lll_opy_):
            with open(bstack11l11l11lll_opy_) as f:
                bstack11l1111lll1_opy_ = json.load(f)
        bstack11l1111lll1_opy_.append(bstack11l1111111_opy_)
        with open(bstack11l11l11lll_opy_, bstack111l111_opy_ (u"ࠩࡺࠫᲇ")) as f:
            json.dump(bstack11l1111lll1_opy_, f)
    else:
        bstack11l1111111_opy_ = {bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨᲈ"): test_name, bstack111l111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᲉ"): bstack11l1111l1ll_opy_, bstack111l111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᲊ"): str(multiprocessing.current_process().name)}
        if bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ᲋") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11l1111111_opy_)
  except Exception as e:
      logger.warn(bstack111l111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ᲌").format(e))
def bstack11l111l1l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111l111_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫ᲍"))
    try:
      bstack11l111l1l11_opy_ = []
      bstack11l1111111_opy_ = {bstack111l111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᲎"): test_name, bstack111l111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᲏"): error_message, bstack111l111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᲐ"): index}
      bstack11l111l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭Ბ"))
      if os.path.exists(bstack11l111l1ll1_opy_):
          with open(bstack11l111l1ll1_opy_) as f:
              bstack11l111l1l11_opy_ = json.load(f)
      bstack11l111l1l11_opy_.append(bstack11l1111111_opy_)
      with open(bstack11l111l1ll1_opy_, bstack111l111_opy_ (u"࠭ࡷࠨᲒ")) as f:
          json.dump(bstack11l111l1l11_opy_, f)
    except Exception as e:
      logger.warn(bstack111l111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᲓ").format(e))
    return
  bstack11l111l1l11_opy_ = []
  bstack11l1111111_opy_ = {bstack111l111_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ე"): test_name, bstack111l111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᲕ"): error_message, bstack111l111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᲖ"): index}
  bstack11l111l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᲗ"))
  lock_file = bstack11l111l1ll1_opy_ + bstack111l111_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫᲘ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l111l1ll1_opy_):
          with open(bstack11l111l1ll1_opy_, bstack111l111_opy_ (u"࠭ࡲࠨᲙ")) as f:
              content = f.read().strip()
              if content:
                  bstack11l111l1l11_opy_ = json.load(open(bstack11l111l1ll1_opy_))
      bstack11l111l1l11_opy_.append(bstack11l1111111_opy_)
      with open(bstack11l111l1ll1_opy_, bstack111l111_opy_ (u"ࠧࡸࠩᲚ")) as f:
          json.dump(bstack11l111l1l11_opy_, f)
  except Exception as e:
    logger.warn(bstack111l111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪ࠾ࠥࢁࡽࠣᲛ").format(e))
def bstack1l1l1l1ll1_opy_(bstack1l1ll1l11l_opy_, name, logger):
  try:
    bstack11l1111111_opy_ = {bstack111l111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᲜ"): name, bstack111l111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᲝ"): bstack1l1ll1l11l_opy_, bstack111l111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᲞ"): str(threading.current_thread()._name)}
    return bstack11l1111111_opy_
  except Exception as e:
    logger.warn(bstack111l111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᲟ").format(e))
  return
def bstack11l11l1l1l1_opy_():
    return platform.system() == bstack111l111_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧᲠ")
def bstack1l1111l1ll_opy_(bstack11l11111111_opy_, config, logger):
    bstack11l111lllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l11111111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨᲡ").format(e))
    return bstack11l111lllll_opy_
def bstack111llll1111_opy_(bstack11l111l11ll_opy_, bstack111lllll11l_opy_):
    bstack11l111lll1l_opy_ = version.parse(bstack11l111l11ll_opy_)
    bstack11l11llll1l_opy_ = version.parse(bstack111lllll11l_opy_)
    if bstack11l111lll1l_opy_ > bstack11l11llll1l_opy_:
        return 1
    elif bstack11l111lll1l_opy_ < bstack11l11llll1l_opy_:
        return -1
    else:
        return 0
def bstack111l1ll111_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l111l1l1l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1111llll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11ll1111ll_opy_(options, framework, config, bstack1ll11llll1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack111l111_opy_ (u"ࠨࡩࡨࡸࠬᲢ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l11lllll1_opy_ = caps.get(bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᲣ"))
    bstack11l11l11l1l_opy_ = True
    bstack1l1ll1ll1_opy_ = os.environ[bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᲤ")]
    bstack1ll11l11lll_opy_ = config.get(bstack111l111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᲥ"), False)
    if bstack1ll11l11lll_opy_:
        bstack1lll11l1l1l_opy_ = config.get(bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᲦ"), {})
        bstack1lll11l1l1l_opy_[bstack111l111_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩᲧ")] = os.getenv(bstack111l111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᲨ"))
        bstack11ll1l1ll11_opy_ = json.loads(os.getenv(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᲩ"), bstack111l111_opy_ (u"ࠩࡾࢁࠬᲪ"))).get(bstack111l111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᲫ"))
    if bstack11l1111111l_opy_(caps.get(bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡗ࠴ࡅࠪᲬ"))) or bstack11l1111111l_opy_(caps.get(bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᲭ"))):
        bstack11l11l11l1l_opy_ = False
    if bstack1l11ll11l_opy_({bstack111l111_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨᲮ"): bstack11l11l11l1l_opy_}):
        bstack1l11lllll1_opy_ = bstack1l11lllll1_opy_ or {}
        bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᲯ")] = bstack11l1111llll_opy_(framework)
        bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᲰ")] = bstack1l1ll11llll_opy_()
        bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᲱ")] = bstack1l1ll1ll1_opy_
        bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᲲ")] = bstack1ll11llll1_opy_
        if bstack1ll11l11lll_opy_:
            bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᲳ")] = bstack1ll11l11lll_opy_
            bstack1l11lllll1_opy_[bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᲴ")] = bstack1lll11l1l1l_opy_
            bstack1l11lllll1_opy_[bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ჵ")][bstack111l111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲶ")] = bstack11ll1l1ll11_opy_
        if getattr(options, bstack111l111_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩᲷ"), None):
            options.set_capability(bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᲸ"), bstack1l11lllll1_opy_)
        else:
            options[bstack111l111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᲹ")] = bstack1l11lllll1_opy_
    else:
        if getattr(options, bstack111l111_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᲺ"), None):
            options.set_capability(bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᲻"), bstack11l1111llll_opy_(framework))
            options.set_capability(bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᲼"), bstack1l1ll11llll_opy_())
            options.set_capability(bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᲽ"), bstack1l1ll1ll1_opy_)
            options.set_capability(bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᲾ"), bstack1ll11llll1_opy_)
            if bstack1ll11l11lll_opy_:
                options.set_capability(bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᲿ"), bstack1ll11l11lll_opy_)
                options.set_capability(bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳀"), bstack1lll11l1l1l_opy_)
                options.set_capability(bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᳁"), bstack11ll1l1ll11_opy_)
        else:
            options[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᳂")] = bstack11l1111llll_opy_(framework)
            options[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᳃")] = bstack1l1ll11llll_opy_()
            options[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᳄")] = bstack1l1ll1ll1_opy_
            options[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᳅")] = bstack1ll11llll1_opy_
            if bstack1ll11l11lll_opy_:
                options[bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᳆")] = bstack1ll11l11lll_opy_
                options[bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳇")] = bstack1lll11l1l1l_opy_
                options[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳈")][bstack111l111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᳉")] = bstack11ll1l1ll11_opy_
    return options
def bstack111lll1l111_opy_(bstack111lll11l1l_opy_, framework):
    bstack1ll11llll1_opy_ = bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣ᳊"))
    if bstack111lll11l1l_opy_ and len(bstack111lll11l1l_opy_.split(bstack111l111_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᳋"))) > 1:
        ws_url = bstack111lll11l1l_opy_.split(bstack111l111_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᳌"))[0]
        if bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ᳍") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1l111l1l_opy_ = json.loads(urllib.parse.unquote(bstack111lll11l1l_opy_.split(bstack111l111_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ᳎"))[1]))
            bstack11l1l111l1l_opy_ = bstack11l1l111l1l_opy_ or {}
            bstack1l1ll1ll1_opy_ = os.environ[bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᳏")]
            bstack11l1l111l1l_opy_[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᳐")] = str(framework) + str(__version__)
            bstack11l1l111l1l_opy_[bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᳑")] = bstack1l1ll11llll_opy_()
            bstack11l1l111l1l_opy_[bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᳒")] = bstack1l1ll1ll1_opy_
            bstack11l1l111l1l_opy_[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ᳓")] = bstack1ll11llll1_opy_
            bstack111lll11l1l_opy_ = bstack111lll11l1l_opy_.split(bstack111l111_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᳔"))[0] + bstack111l111_opy_ (u"ࠪࡧࡦࡶࡳ࠾᳕ࠩ") + urllib.parse.quote(json.dumps(bstack11l1l111l1l_opy_))
    return bstack111lll11l1l_opy_
def bstack111l11111_opy_():
    global bstack1l11111l11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l11111l11_opy_ = BrowserType.connect
    return bstack1l11111l11_opy_
def bstack1lll1l1ll_opy_(framework_name):
    global bstack11l1l1ll1l_opy_
    bstack11l1l1ll1l_opy_ = framework_name
    return framework_name
def bstack1lll11l1_opy_(self, *args, **kwargs):
    global bstack1l11111l11_opy_
    try:
        global bstack11l1l1ll1l_opy_
        if bstack111l111_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ᳖") in kwargs:
            kwargs[bstack111l111_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ᳗ࠩ")] = bstack111lll1l111_opy_(
                kwargs.get(bstack111l111_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ᳘ࠪ"), None),
                bstack11l1l1ll1l_opy_
            )
    except Exception as e:
        logger.error(bstack111l111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃ᳙ࠢ").format(str(e)))
    return bstack1l11111l11_opy_(self, *args, **kwargs)
def bstack11l11111ll1_opy_(bstack11l111111ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lllll11l1_opy_(bstack11l111111ll_opy_, bstack111l111_opy_ (u"ࠣࠤ᳚"))
        if proxies and proxies.get(bstack111l111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ᳛")):
            parsed_url = urlparse(proxies.get(bstack111l111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ᳜")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack111l111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺ᳝ࠧ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack111l111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨ᳞")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack111l111_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳ᳟ࠩ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack111l111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪ᳠")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11ll11l11_opy_(bstack11l111111ll_opy_):
    bstack111lll1l11l_opy_ = {
        bstack11l1lll11ll_opy_[bstack111llllllll_opy_]: bstack11l111111ll_opy_[bstack111llllllll_opy_]
        for bstack111llllllll_opy_ in bstack11l111111ll_opy_
        if bstack111llllllll_opy_ in bstack11l1lll11ll_opy_
    }
    bstack111lll1l11l_opy_[bstack111l111_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣ᳡")] = bstack11l11111ll1_opy_(bstack11l111111ll_opy_, bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤ᳢")))
    bstack111lll11l11_opy_ = [element.lower() for element in bstack11l1ll111ll_opy_]
    bstack11l11l1111l_opy_(bstack111lll1l11l_opy_, bstack111lll11l11_opy_)
    return bstack111lll1l11l_opy_
def bstack11l11l1111l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack111l111_opy_ (u"ࠥ࠮࠯࠰᳣ࠪࠣ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l11l1111l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l11l1111l_opy_(item, keys)
def bstack1l1lll11111_opy_():
    bstack11l111ll11l_opy_ = [os.environ.get(bstack111l111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡎࡒࡅࡔࡡࡇࡍࡗࠨ᳤")), os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠧࢄ᳥ࠢ")), bstack111l111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ᳦࠭")), os.path.join(bstack111l111_opy_ (u"ࠧ࠰ࡶࡰࡴ᳧ࠬ"), bstack111l111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᳨"))]
    for path in bstack11l111ll11l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack111l111_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᳩ") + str(path) + bstack111l111_opy_ (u"ࠥࠫࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠨᳪ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack111l111_opy_ (u"ࠦࡌ࡯ࡶࡪࡰࡪࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠢࡩࡳࡷࠦࠧࠣᳫ") + str(path) + bstack111l111_opy_ (u"ࠧ࠭ࠢᳬ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack111l111_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨ᳭") + str(path) + bstack111l111_opy_ (u"ࠢࠨࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡬ࡦࡹࠠࡵࡪࡨࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶ࠲ࠧᳮ"))
            else:
                logger.debug(bstack111l111_opy_ (u"ࠣࡅࡵࡩࡦࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥࠡࠩࠥᳯ") + str(path) + bstack111l111_opy_ (u"ࠤࠪࠤࡼ࡯ࡴࡩࠢࡺࡶ࡮ࡺࡥࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲ࠳ࠨᳰ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack111l111_opy_ (u"ࠥࡓࡵ࡫ࡲࡢࡶ࡬ࡳࡳࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥࠢࡩࡳࡷࠦࠧࠣᳱ") + str(path) + bstack111l111_opy_ (u"ࠦࠬ࠴ࠢᳲ"))
            return path
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡻࡰࠡࡨ࡬ࡰࡪࠦࠧࡼࡲࡤࡸ࡭ࢃࠧ࠻ࠢࠥᳳ") + str(e) + bstack111l111_opy_ (u"ࠨࠢ᳴"))
    logger.debug(bstack111l111_opy_ (u"ࠢࡂ࡮࡯ࠤࡵࡧࡴࡩࡵࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠦᳵ"))
    return None
@measure(event_name=EVENTS.bstack11l1ll11ll1_opy_, stage=STAGE.bstack11l1llll1_opy_)
def bstack1lll111ll11_opy_(binary_path, bstack1lll1ll11l1_opy_, bs_config):
    logger.debug(bstack111l111_opy_ (u"ࠣࡅࡸࡶࡷ࡫࡮ࡵࠢࡆࡐࡎࠦࡐࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦ࠽ࠤࢀࢃࠢᳶ").format(binary_path))
    bstack11l11ll11l1_opy_ = bstack111l111_opy_ (u"ࠩࠪ᳷")
    bstack11l11lll1l1_opy_ = {
        bstack111l111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᳸"): __version__,
        bstack111l111_opy_ (u"ࠦࡴࡹࠢ᳹"): platform.system(),
        bstack111l111_opy_ (u"ࠧࡵࡳࡠࡣࡵࡧ࡭ࠨᳺ"): platform.machine(),
        bstack111l111_opy_ (u"ࠨࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠦ᳻"): bstack111l111_opy_ (u"ࠧ࠱ࠩ᳼"),
        bstack111l111_opy_ (u"ࠣࡵࡧ࡯ࡤࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠢ᳽"): bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ᳾")
    }
    bstack111llll1ll1_opy_(bstack11l11lll1l1_opy_)
    try:
        if binary_path:
            bstack11l11lll1l1_opy_[bstack111l111_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᳿")] = subprocess.check_output([binary_path, bstack111l111_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᴀ")]).strip().decode(bstack111l111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᴁ"))
        response = requests.request(
            bstack111l111_opy_ (u"࠭ࡇࡆࡖࠪᴂ"),
            url=bstack1ll1l1ll_opy_(bstack11l1ll1ll11_opy_),
            headers=None,
            auth=(bs_config[bstack111l111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᴃ")], bs_config[bstack111l111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᴄ")]),
            json=None,
            params=bstack11l11lll1l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack111l111_opy_ (u"ࠩࡸࡶࡱ࠭ᴅ") in data.keys() and bstack111l111_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧࡣࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᴆ") in data.keys():
            logger.debug(bstack111l111_opy_ (u"ࠦࡓ࡫ࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡨࡩ࡯ࡣࡵࡽ࠱ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧᴇ").format(bstack11l11lll1l1_opy_[bstack111l111_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᴈ")]))
            if bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩᴉ") in os.environ:
                logger.debug(bstack111l111_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡦࡹࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥᴊ"))
                data[bstack111l111_opy_ (u"ࠨࡷࡵࡰࠬᴋ")] = os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬᴌ")]
            bstack11l11111lll_opy_ = bstack11l11l1llll_opy_(data[bstack111l111_opy_ (u"ࠪࡹࡷࡲࠧᴍ")], bstack1lll1ll11l1_opy_)
            bstack11l11ll11l1_opy_ = os.path.join(bstack1lll1ll11l1_opy_, bstack11l11111lll_opy_)
            os.chmod(bstack11l11ll11l1_opy_, 0o777) # bstack11l11l1ll1l_opy_ permission
            return bstack11l11ll11l1_opy_
    except Exception as e:
        logger.debug(bstack111l111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦᴎ").format(e))
    return binary_path
def bstack111llll1ll1_opy_(bstack11l11lll1l1_opy_):
    try:
        if bstack111l111_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᴏ") not in bstack11l11lll1l1_opy_[bstack111l111_opy_ (u"࠭࡯ࡴࠩᴐ")].lower():
            return
        if os.path.exists(bstack111l111_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤᴑ")):
            with open(bstack111l111_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᴒ"), bstack111l111_opy_ (u"ࠤࡵࠦᴓ")) as f:
                bstack11l111llll1_opy_ = {}
                for line in f:
                    if bstack111l111_opy_ (u"ࠥࡁࠧᴔ") in line:
                        key, value = line.rstrip().split(bstack111l111_opy_ (u"ࠦࡂࠨᴕ"), 1)
                        bstack11l111llll1_opy_[key] = value.strip(bstack111l111_opy_ (u"ࠬࠨ࡜ࠨࠩᴖ"))
                bstack11l11lll1l1_opy_[bstack111l111_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭ᴗ")] = bstack11l111llll1_opy_.get(bstack111l111_opy_ (u"ࠢࡊࡆࠥᴘ"), bstack111l111_opy_ (u"ࠣࠤᴙ"))
        elif os.path.exists(bstack111l111_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣᴚ")):
            bstack11l11lll1l1_opy_[bstack111l111_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪᴛ")] = bstack111l111_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨࠫᴜ")
    except Exception as e:
        logger.debug(bstack111l111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾࠢᴝ") + e)
@measure(event_name=EVENTS.bstack11ll11111ll_opy_, stage=STAGE.bstack11l1llll1_opy_)
def bstack11l11l1llll_opy_(bstack111lll111l1_opy_, bstack11l111ll1ll_opy_):
    logger.debug(bstack111l111_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣᴞ") + str(bstack111lll111l1_opy_) + bstack111l111_opy_ (u"ࠢࠣᴟ"))
    zip_path = os.path.join(bstack11l111ll1ll_opy_, bstack111l111_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶࠢᴠ"))
    bstack11l11111lll_opy_ = bstack111l111_opy_ (u"ࠩࠪᴡ")
    with requests.get(bstack111lll111l1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack111l111_opy_ (u"ࠥࡻࡧࠨᴢ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack111l111_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨᴣ"))
    with zipfile.ZipFile(zip_path, bstack111l111_opy_ (u"ࠬࡸࠧᴤ")) as zip_ref:
        bstack111lllllll1_opy_ = zip_ref.namelist()
        if len(bstack111lllllll1_opy_) > 0:
            bstack11l11111lll_opy_ = bstack111lllllll1_opy_[0] # bstack111llllll1l_opy_ bstack11l1llllll1_opy_ will be bstack111lll1l1l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l111ll1ll_opy_)
        logger.debug(bstack111l111_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱࠣࠫࠧᴥ") + str(bstack11l111ll1ll_opy_) + bstack111l111_opy_ (u"ࠢࠨࠤᴦ"))
    os.remove(zip_path)
    return bstack11l11111lll_opy_
def get_cli_dir():
    bstack111llll1l1l_opy_ = bstack1l1lll11111_opy_()
    if bstack111llll1l1l_opy_:
        bstack1lll1ll11l1_opy_ = os.path.join(bstack111llll1l1l_opy_, bstack111l111_opy_ (u"ࠣࡥ࡯࡭ࠧᴧ"))
        if not os.path.exists(bstack1lll1ll11l1_opy_):
            os.makedirs(bstack1lll1ll11l1_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1ll11l1_opy_
    else:
        raise FileNotFoundError(bstack111l111_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠧᴨ"))
def bstack1lll111l1l1_opy_(bstack1lll1ll11l1_opy_):
    bstack111l111_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨࠢᴩ")
    bstack11l111ll1l1_opy_ = [
        os.path.join(bstack1lll1ll11l1_opy_, f)
        for f in os.listdir(bstack1lll1ll11l1_opy_)
        if os.path.isfile(os.path.join(bstack1lll1ll11l1_opy_, f)) and f.startswith(bstack111l111_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱ࠧᴪ"))
    ]
    if len(bstack11l111ll1l1_opy_) > 0:
        return max(bstack11l111ll1l1_opy_, key=os.path.getmtime) # get bstack11l11ll1lll_opy_ binary
    return bstack111l111_opy_ (u"ࠧࠨᴫ")
def bstack11ll1lll1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll11l1l111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll11l1l111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1ll11l1_opy_(data, keys, default=None):
    bstack111l111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡢࡨࡨࡰࡾࠦࡧࡦࡶࠣࡥࠥࡴࡥࡴࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡣࡷࡥ࠿ࠦࡔࡩࡧࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡶࡲࠤࡹࡸࡡࡷࡧࡵࡷࡪ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡰ࡫ࡹࡴ࠼ࠣࡅࠥࡲࡩࡴࡶࠣࡳ࡫ࠦ࡫ࡦࡻࡶ࠳࡮ࡴࡤࡪࡥࡨࡷࠥࡸࡥࡱࡴࡨࡷࡪࡴࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩ࡫ࡦࡢࡷ࡯ࡸ࠿ࠦࡖࡢ࡮ࡸࡩࠥࡺ࡯ࠡࡴࡨࡸࡺࡸ࡮ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡲࡦࡶࡸࡶࡳࡀࠠࡕࡪࡨࠤࡻࡧ࡬ࡶࡧࠣࡥࡹࠦࡴࡩࡧࠣࡲࡪࡹࡴࡦࡦࠣࡴࡦࡺࡨ࠭ࠢࡲࡶࠥࡪࡥࡧࡣࡸࡰࡹࠦࡩࡧࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᴬ")
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