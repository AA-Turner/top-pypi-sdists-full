# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
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
from math import ceil
from unittest import result
import urllib
from urllib.parse import urlparse
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_, HTTPS_HUB,
                                    bstack111l1lllll1_opy_, bstack111l1ll1l1l_opy_, bstack111l1lll1ll_opy_, bstack111ll1lll1l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11lll1l11l_opy_, bstack1l11l1ll1_opy_
from bstack_utils.proxy import bstack11l1l11l11_opy_, bstack11l1lll1l1_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1llll1l1l_opy_ import bstack11ll1ll1l1_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1l1llllll11_opy_())
bstack1llll11111_opy_ = logger_utils.bstack1l1l1l111_opy_(__name__)
def bstack11l111l11ll_opy_(config):
    return config[bstack1lll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ṟ")]
def bstack11l111l1ll1_opy_(config):
    return config[bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨṟ")]
def bstack11ll1l1ll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def is_robot_playwright_installed():
    try:
        import Browser
        return True
    except ImportError:
        return False
def bstack11111l1llll_opy_(obj):
    values = []
    bstack1111ll11lll_opy_ = re.compile(bstack1lll1l_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥṠ"), re.I)
    for key in obj.keys():
        if bstack1111ll11lll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111lll1lll_opy_(config):
    tags = []
    tags.extend(bstack11111l1llll_opy_(os.environ))
    tags.extend(bstack11111l1llll_opy_(config))
    return tags
def bstack1111lll1111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111l1ll111_opy_(bstack1111l11ll11_opy_):
    if not bstack1111l11ll11_opy_:
        return bstack1lll1l_opy_ (u"ࠧࠨṡ")
    return bstack1lll1l_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤṢ").format(bstack1111l11ll11_opy_.name, bstack1111l11ll11_opy_.email)
def bstack11l111l1111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111l1ll11l_opy_ = repo.common_dir
        info = {
            bstack1lll1l_opy_ (u"ࠤࡶ࡬ࡦࠨṣ"): repo.head.commit.hexsha,
            bstack1lll1l_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨṤ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1lll1l_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦṥ"): repo.active_branch.name,
            bstack1lll1l_opy_ (u"ࠧࡺࡡࡨࠤṦ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1lll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤṧ"): bstack1111l1ll111_opy_(repo.head.commit.committer),
            bstack1lll1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣṨ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1lll1l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣṩ"): bstack1111l1ll111_opy_(repo.head.commit.author),
            bstack1lll1l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢṪ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1lll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦṫ"): repo.head.commit.message,
            bstack1lll1l_opy_ (u"ࠦࡷࡵ࡯ࡵࠤṬ"): repo.git.rev_parse(bstack1lll1l_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢṭ")),
            bstack1lll1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢṮ"): bstack1111l1ll11l_opy_,
            bstack1lll1l_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥṯ"): subprocess.check_output([bstack1lll1l_opy_ (u"ࠣࡩ࡬ࡸࠧṰ"), bstack1lll1l_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧṱ"), bstack1lll1l_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨṲ")]).strip().decode(
                bstack1lll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪṳ")),
            bstack1lll1l_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢṴ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1lll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣṵ"): repo.git.rev_list(
                bstack1lll1l_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢṶ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11111lll11l_opy_ = []
        for remote in remotes:
            bstack111l1111l1l_opy_ = {
                bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨṷ"): remote.name,
                bstack1lll1l_opy_ (u"ࠤࡸࡶࡱࠨṸ"): remote.url,
            }
            bstack11111lll11l_opy_.append(bstack111l1111l1l_opy_)
        bstack111l11111l1_opy_ = {
            bstack1lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣṹ"): bstack1lll1l_opy_ (u"ࠦ࡬࡯ࡴࠣṺ"),
            **info,
            bstack1lll1l_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨṻ"): bstack11111lll11l_opy_
        }
        bstack111l11111l1_opy_ = bstack1111ll1l1l1_opy_(bstack111l11111l1_opy_)
        return bstack111l11111l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤṼ").format(err))
        return {}
def bstack1111ll1lll1_opy_(bstack111l11l1111_opy_=None):
    bstack1lll1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡈࡧࡷࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࡦࡲ࡬ࡺࠢࡩࡳࡷࡳࡡࡵࡶࡨࡨࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡷࡶࡩࠥࡩࡡࡴࡧࡶࠤ࡫ࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡰ࡮ࡧࡩࡷࠦࡩ࡯ࠢࡷ࡬ࡪࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡩࡳࡱࡪࡥࡳࡵࠣࠬࡱ࡯ࡳࡵ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡐࡲࡲࡪࡀࠠࡎࡱࡱࡳ࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬࠱ࠦࡵࡴࡧࡶࠤࡨࡻࡲࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡝ࡲࡷ࠳࡭ࡥࡵࡥࡺࡨ࠭࠯࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡇࡰࡴࡹࡿࠠ࡭࡫ࡶࡸࠥࡡ࡝࠻ࠢࡐࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨࠡࡹ࡬ࡸ࡭ࠦ࡮ࡰࠢࡶࡳࡺࡸࡣࡦࡵࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠬࠡࡴࡨࡸࡺࡸ࡮ࡴࠢ࡞ࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡰࡢࡶ࡫ࡷ࠿ࠦࡍࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬ࠥࡽࡩࡵࡪࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡴࡰࠢࡤࡲࡦࡲࡹࡻࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡨ࡮ࡩࡴࡴ࠮ࠣࡩࡦࡩࡨࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡣࠣࡪࡴࡲࡤࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦṽ")
    if bstack111l11l1111_opy_ is None:
        bstack111l11l1111_opy_ = [os.getcwd()]
    elif isinstance(bstack111l11l1111_opy_, list) and len(bstack111l11l1111_opy_) == 0:
        return []
    results = []
    for folder in bstack111l11l1111_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1lll1l_opy_ (u"ࠣࡈࡲࡰࡩ࡫ࡲࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨṾ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1lll1l_opy_ (u"ࠤࡳࡶࡎࡪࠢṿ"): bstack1lll1l_opy_ (u"ࠥࠦẀ"),
                bstack1lll1l_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥẁ"): [],
                bstack1lll1l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨẂ"): [],
                bstack1lll1l_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨẃ"): bstack1lll1l_opy_ (u"ࠢࠣẄ"),
                bstack1lll1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤẅ"): [],
                bstack1lll1l_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥẆ"): bstack1lll1l_opy_ (u"ࠥࠦẇ"),
                bstack1lll1l_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦẈ"): bstack1lll1l_opy_ (u"ࠧࠨẉ"),
                bstack1lll1l_opy_ (u"ࠨࡰࡳࡔࡤࡻࡉ࡯ࡦࡧࠤẊ"): bstack1lll1l_opy_ (u"ࠢࠣẋ")
            }
            bstack111l11lll1l_opy_ = repo.active_branch.name
            bstack1111llll111_opy_ = repo.head.commit
            result[bstack1lll1l_opy_ (u"ࠣࡲࡵࡍࡩࠨẌ")] = bstack1111llll111_opy_.hexsha
            bstack111l11l1l1l_opy_ = _1111l1lll1l_opy_(repo)
            logger.debug(bstack1lll1l_opy_ (u"ࠤࡅࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠻ࠢࠥẍ") + str(bstack111l11l1l1l_opy_) + bstack1lll1l_opy_ (u"ࠥࠦẎ"))
            if bstack111l11l1l1l_opy_:
                try:
                    bstack1111ll111ll_opy_ = repo.git.diff(bstack1lll1l_opy_ (u"ࠦ࠲࠳࡮ࡢ࡯ࡨ࠱ࡴࡴ࡬ࡺࠤẏ"), bstack1ll1l1ll11l_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥẐ")).split(bstack1lll1l_opy_ (u"࠭࡜࡯ࠩẑ"))
                    logger.debug(bstack1lll1l_opy_ (u"ࠢࡄࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡣࡧࡷࡻࡪ࡫࡮ࠡࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽࠡࡣࡱࡨࠥࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠻ࠢࠥẒ") + str(bstack1111ll111ll_opy_) + bstack1lll1l_opy_ (u"ࠣࠤẓ"))
                    result[bstack1lll1l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣẔ")] = [f.strip() for f in bstack1111ll111ll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1l1ll11l_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢẕ")))
                except Exception:
                    logger.debug(bstack1lll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡦࡴࡣࡩࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳ࠴ࠠࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡵࡩࡨ࡫࡮ࡵࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠦẖ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1lll1l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦẗ")] = _1111lll111l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1lll1l_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧẘ")] = _1111lll111l_opy_(commits[:5])
            bstack1111l11l111_opy_ = set()
            bstack111l1111ll1_opy_ = []
            for commit in commits:
                logger.debug(bstack1lll1l_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮࡫ࡷ࠾ࠥࠨẙ") + str(commit.message) + bstack1lll1l_opy_ (u"ࠣࠤẚ"))
                bstack111l11l111l_opy_ = commit.author.name if commit.author else bstack1lll1l_opy_ (u"ࠤࡘࡲࡰࡴ࡯ࡸࡰࠥẛ")
                bstack1111l11l111_opy_.add(bstack111l11l111l_opy_)
                bstack111l1111ll1_opy_.append({
                    bstack1lll1l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦẜ"): commit.message.strip(),
                    bstack1lll1l_opy_ (u"ࠦࡺࡹࡥࡳࠤẝ"): bstack111l11l111l_opy_
                })
            result[bstack1lll1l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨẞ")] = list(bstack1111l11l111_opy_)
            result[bstack1lll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢẟ")] = bstack111l1111ll1_opy_
            result[bstack1lll1l_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢẠ")] = bstack1111llll111_opy_.committed_datetime.strftime(bstack1lll1l_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࠥạ"))
            if (not result[bstack1lll1l_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥẢ")] or result[bstack1lll1l_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦả")].strip() == bstack1lll1l_opy_ (u"ࠦࠧẤ")) and bstack1111llll111_opy_.message:
                bstack11111l1l111_opy_ = bstack1111llll111_opy_.message.strip().splitlines()
                result[bstack1lll1l_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨấ")] = bstack11111l1l111_opy_[0] if bstack11111l1l111_opy_ else bstack1lll1l_opy_ (u"ࠨࠢẦ")
                if len(bstack11111l1l111_opy_) > 2:
                    result[bstack1lll1l_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢầ")] = bstack1lll1l_opy_ (u"ࠨ࡞ࡱࠫẨ").join(bstack11111l1l111_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1lll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࠩࡨࡲࡰࡩ࡫ࡲ࠻ࠢࡾࢁ࠮ࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣẩ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111l111111l_opy_(result)
    ]
    return filtered_results
def _111l111111l_opy_(result):
    bstack1lll1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡪࡲࡰࡦࡴࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡣࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡸࡻ࡬ࡵࠢ࡬ࡷࠥࡼࡡ࡭࡫ࡧࠤ࠭ࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠡࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠠࡢࡰࡧࠤࡦࡻࡴࡩࡱࡵࡷ࠮࠴ࠊࠡࠢࠣࠤࠧࠨࠢẪ")
    return (
        isinstance(result.get(bstack1lll1l_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥẫ"), None), list)
        and len(result[bstack1lll1l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦẬ")]) > 0
        and isinstance(result.get(bstack1lll1l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢậ"), None), list)
        and len(result[bstack1lll1l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣẮ")]) > 0
    )
def _1111l1lll1l_opy_(repo):
    bstack1lll1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡖࡵࡽࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡮ࡥࠡࡤࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡲࡦࡲࡲࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡮ࡡࡳࡦࡦࡳࡩ࡫ࡤࠡࡰࡤࡱࡪࡹࠠࡢࡰࡧࠤࡼࡵࡲ࡬ࠢࡺ࡭ࡹ࡮ࠠࡢ࡮࡯ࠤ࡛ࡉࡓࠡࡲࡵࡳࡻ࡯ࡤࡦࡴࡶ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡥࡧࡩࡥࡺࡲࡴࠡࡤࡵࡥࡳࡩࡨࠡ࡫ࡩࠤࡵࡵࡳࡴ࡫ࡥࡰࡪ࠲ࠠࡦ࡮ࡶࡩࠥࡔ࡯࡯ࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦắ")
    try:
        try:
            origin = repo.remotes.origin
            bstack1111lllll1l_opy_ = origin.refs[bstack1lll1l_opy_ (u"ࠩࡋࡉࡆࡊࠧẰ")]
            target = bstack1111lllll1l_opy_.reference.name
            if target.startswith(bstack1lll1l_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫằ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1lll1l_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬẲ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1111lll111l_opy_(commits):
    bstack1lll1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡣࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨẳ")
    bstack1111ll111ll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1111ll11111_opy_ in diff:
                        if bstack1111ll11111_opy_.a_path:
                            bstack1111ll111ll_opy_.add(bstack1111ll11111_opy_.a_path)
                        if bstack1111ll11111_opy_.b_path:
                            bstack1111ll111ll_opy_.add(bstack1111ll11111_opy_.b_path)
    except Exception:
        pass
    return list(bstack1111ll111ll_opy_)
def bstack1111ll1l1l1_opy_(bstack111l11111l1_opy_):
    bstack1111l11lll1_opy_ = bstack111l111ll11_opy_(bstack111l11111l1_opy_)
    if bstack1111l11lll1_opy_ and bstack1111l11lll1_opy_ > bstack111l1lllll1_opy_:
        bstack111l11111ll_opy_ = bstack1111l11lll1_opy_ - bstack111l1lllll1_opy_
        bstack1111ll1l111_opy_ = bstack1111ll11l1l_opy_(bstack111l11111l1_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢẴ")], bstack111l11111ll_opy_)
        bstack111l11111l1_opy_[bstack1lll1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣẵ")] = bstack1111ll1l111_opy_
        logger.info(bstack1lll1l_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥẶ")
                    .format(bstack111l111ll11_opy_(bstack111l11111l1_opy_) / 1024))
    return bstack111l11111l1_opy_
def bstack111l111ll11_opy_(bstack11111l1ll_opy_):
    try:
        if bstack11111l1ll_opy_:
            bstack1111l1l11ll_opy_ = json.dumps(bstack11111l1ll_opy_)
            bstack1111l11l1ll_opy_ = sys.getsizeof(bstack1111l1l11ll_opy_)
            return bstack1111l11l1ll_opy_
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤặ").format(e))
    return -1
def bstack1111ll11l1l_opy_(field, bstack1111l11ll1l_opy_):
    try:
        bstack11111ll11ll_opy_ = len(bytes(bstack111l1ll1l1l_opy_, bstack1lll1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩẸ")))
        bstack111l11llll1_opy_ = bytes(field, bstack1lll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪẹ"))
        bstack1111l1ll1l1_opy_ = len(bstack111l11llll1_opy_)
        bstack1111l1l1111_opy_ = ceil(bstack1111l1ll1l1_opy_ - bstack1111l11ll1l_opy_ - bstack11111ll11ll_opy_)
        if bstack1111l1l1111_opy_ > 0:
            bstack1111ll11ll1_opy_ = bstack111l11llll1_opy_[:bstack1111l1l1111_opy_].decode(bstack1lll1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫẺ"), errors=bstack1lll1l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭ẻ")) + bstack111l1ll1l1l_opy_
            return bstack1111ll11ll1_opy_
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧẼ").format(e))
    return field
def bstack1ll1111l1l_opy_():
    env = os.environ
    if (bstack1lll1l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨẽ") in env and len(env[bstack1lll1l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢẾ")]) > 0) or (
            bstack1lll1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤế") in env and len(env[bstack1lll1l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥỀ")]) > 0):
        return {
            bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥề"): bstack1lll1l_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢỂ"),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥể"): env.get(bstack1lll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦỄ")),
            bstack1lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦễ"): env.get(bstack1lll1l_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧỆ")),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥệ"): env.get(bstack1lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦỈ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠨࡃࡊࠤỉ")) == bstack1lll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧỊ") and bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥị"))):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢỌ"): bstack1lll1l_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧọ"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢỎ"): env.get(bstack1lll1l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣỏ")),
            bstack1lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣỐ"): env.get(bstack1lll1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦố")),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢỒ"): env.get(bstack1lll1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧồ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠥࡇࡎࠨỔ")) == bstack1lll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤổ") and bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧỖ"))):
        return {
            bstack1lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦỗ"): bstack1lll1l_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥỘ"),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦộ"): env.get(bstack1lll1l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤỚ")),
            bstack1lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧớ"): env.get(bstack1lll1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨỜ")),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦờ"): env.get(bstack1lll1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧỞ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠢࡄࡋࠥở")) == bstack1lll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨỠ") and env.get(bstack1lll1l_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥỡ")) == bstack1lll1l_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧỢ"):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤợ"): bstack1lll1l_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢỤ"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤụ"): None,
            bstack1lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤỦ"): None,
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢủ"): None
        }
    if env.get(bstack1lll1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧỨ")) and env.get(bstack1lll1l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨứ")):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤỪ"): bstack1lll1l_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣừ"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤỬ"): env.get(bstack1lll1l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧử")),
            bstack1lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥỮ"): None,
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣữ"): env.get(bstack1lll1l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧỰ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠦࡈࡏࠢự")) == bstack1lll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥỲ") and bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧỳ"))):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧỴ"): bstack1lll1l_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢỵ"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧỶ"): env.get(bstack1lll1l_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨỷ")),
            bstack1lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨỸ"): None,
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦỹ"): env.get(bstack1lll1l_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦỺ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠢࡄࡋࠥỻ")) == bstack1lll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨỼ") and bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧỽ"))):
        return {
            bstack1lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣỾ"): bstack1lll1l_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢỿ"),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣἀ"): env.get(bstack1lll1l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧἁ")),
            bstack1lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤἂ"): env.get(bstack1lll1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨἃ")),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣἄ"): env.get(bstack1lll1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨἅ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠦࡈࡏࠢἆ")) == bstack1lll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥἇ") and bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤἈ"))):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧἉ"): bstack1lll1l_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣἊ"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧἋ"): env.get(bstack1lll1l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢἌ")),
            bstack1lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨἍ"): env.get(bstack1lll1l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥἎ")),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧἏ"): env.get(bstack1lll1l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥἐ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠣࡅࡌࠦἑ")) == bstack1lll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢἒ") and bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨἓ"))):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤἔ"): bstack1lll1l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣἕ"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ἖"): env.get(bstack1lll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ἗")),
            bstack1lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥἘ"): env.get(bstack1lll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦἙ")) or env.get(bstack1lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨἚ")),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥἛ"): env.get(bstack1lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢἜ"))
        }
    if bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣἝ"))):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ἞"): bstack1lll1l_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣ἟"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧἠ"): bstack1lll1l_opy_ (u"ࠥࡿࢂࢁࡽࠣἡ").format(env.get(bstack1lll1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧἢ")), env.get(bstack1lll1l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬἣ"))),
            bstack1lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣἤ"): env.get(bstack1lll1l_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨἥ")),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢἦ"): env.get(bstack1lll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤἧ"))
        }
    if bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧἨ"))):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤἩ"): bstack1lll1l_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢἪ"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤἫ"): bstack1lll1l_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨἬ").format(env.get(bstack1lll1l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧἭ")), env.get(bstack1lll1l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪἮ")), env.get(bstack1lll1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫἯ")), env.get(bstack1lll1l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨἰ"))),
            bstack1lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢἱ"): env.get(bstack1lll1l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥἲ")),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨἳ"): env.get(bstack1lll1l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤἴ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥἵ")) and env.get(bstack1lll1l_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧἶ")):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤἷ"): bstack1lll1l_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢἸ"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤἹ"): bstack1lll1l_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥἺ").format(env.get(bstack1lll1l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫἻ")), env.get(bstack1lll1l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧἼ")), env.get(bstack1lll1l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪἽ"))),
            bstack1lll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨἾ"): env.get(bstack1lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧἿ")),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧὀ"): env.get(bstack1lll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢὁ"))
        }
    if any([env.get(bstack1lll1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨὂ")), env.get(bstack1lll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣὃ")), env.get(bstack1lll1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢὄ"))]):
        return {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤὅ"): bstack1lll1l_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧ὆"),
            bstack1lll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ὇"): env.get(bstack1lll1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨὈ")),
            bstack1lll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥὉ"): env.get(bstack1lll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢὊ")),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤὋ"): env.get(bstack1lll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤὌ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥὍ")):
        return {
            bstack1lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ὎"): bstack1lll1l_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢ὏"),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦὐ"): env.get(bstack1lll1l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦὑ")),
            bstack1lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧὒ"): env.get(bstack1lll1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥὓ")),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦὔ"): env.get(bstack1lll1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦὕ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣὖ")) or env.get(bstack1lll1l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥὗ")):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ὘"): bstack1lll1l_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦὙ"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ὚"): env.get(bstack1lll1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤὛ")),
            bstack1lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ὜"): bstack1lll1l_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢὝ") if env.get(bstack1lll1l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ὞")) else None,
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣὟ"): env.get(bstack1lll1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣὠ"))
        }
    if any([env.get(bstack1lll1l_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤὡ")), env.get(bstack1lll1l_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨὢ")), env.get(bstack1lll1l_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨὣ"))]):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧὤ"): bstack1lll1l_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢὥ"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧὦ"): None,
            bstack1lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧὧ"): env.get(bstack1lll1l_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣὨ")),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦὩ"): env.get(bstack1lll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣὪ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥὫ")):
        return {
            bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨὬ"): bstack1lll1l_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧὭ"),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨὮ"): env.get(bstack1lll1l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥὯ")),
            bstack1lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢὰ"): bstack1lll1l_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢά").format(env.get(bstack1lll1l_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪὲ"))) if env.get(bstack1lll1l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦέ")) else None,
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣὴ"): env.get(bstack1lll1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧή"))
        }
    if bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧὶ"))):
        return {
            bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥί"): bstack1lll1l_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢὸ"),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥό"): env.get(bstack1lll1l_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧὺ")),
            bstack1lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦύ"): env.get(bstack1lll1l_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨὼ")),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥώ"): env.get(bstack1lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ὾"))
        }
    if bstack11ll1ll1l_opy_(env.get(bstack1lll1l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ὿"))):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᾀ"): bstack1lll1l_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤᾁ"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᾂ"): bstack1lll1l_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦᾃ").format(env.get(bstack1lll1l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨᾄ")), env.get(bstack1lll1l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩᾅ")), env.get(bstack1lll1l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ᾆ"))),
            bstack1lll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᾇ"): env.get(bstack1lll1l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥᾈ")),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᾉ"): env.get(bstack1lll1l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥᾊ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠦࡈࡏࠢᾋ")) == bstack1lll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᾌ") and env.get(bstack1lll1l_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨᾍ")) == bstack1lll1l_opy_ (u"ࠢ࠲ࠤᾎ"):
        return {
            bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᾏ"): bstack1lll1l_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤᾐ"),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᾑ"): bstack1lll1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢᾒ").format(env.get(bstack1lll1l_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩᾓ"))),
            bstack1lll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᾔ"): None,
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᾕ"): None,
        }
    if env.get(bstack1lll1l_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᾖ")):
        return {
            bstack1lll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᾗ"): bstack1lll1l_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧᾘ"),
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᾙ"): None,
            bstack1lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᾚ"): env.get(bstack1lll1l_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢᾛ")),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᾜ"): env.get(bstack1lll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᾝ"))
        }
    if any([env.get(bstack1lll1l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧᾞ")), env.get(bstack1lll1l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥᾟ")), env.get(bstack1lll1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤᾠ")), env.get(bstack1lll1l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨᾡ"))]):
        return {
            bstack1lll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᾢ"): bstack1lll1l_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥᾣ"),
            bstack1lll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᾤ"): None,
            bstack1lll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᾥ"): env.get(bstack1lll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᾦ")) or None,
            bstack1lll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᾧ"): env.get(bstack1lll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᾨ"), 0)
        }
    if env.get(bstack1lll1l_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᾩ")):
        return {
            bstack1lll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᾪ"): bstack1lll1l_opy_ (u"ࠣࡉࡲࡇࡉࠨᾫ"),
            bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᾬ"): None,
            bstack1lll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᾭ"): env.get(bstack1lll1l_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᾮ")),
            bstack1lll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᾯ"): env.get(bstack1lll1l_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧᾰ"))
        }
    if env.get(bstack1lll1l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᾱ")):
        return {
            bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᾲ"): bstack1lll1l_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧᾳ"),
            bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᾴ"): env.get(bstack1lll1l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᾵")),
            bstack1lll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᾶ"): env.get(bstack1lll1l_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᾷ")),
            bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᾸ"): env.get(bstack1lll1l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᾹ"))
        }
    return {bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᾺ"): None}
def get_host_info():
    return {
        bstack1lll1l_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧΆ"): platform.node(),
        bstack1lll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨᾼ"): platform.system(),
        bstack1lll1l_opy_ (u"ࠧࡺࡹࡱࡧࠥ᾽"): platform.machine(),
        bstack1lll1l_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢι"): platform.version(),
        bstack1lll1l_opy_ (u"ࠢࡢࡴࡦ࡬ࠧ᾿"): platform.architecture()[0]
    }
def bstack1ll1l11lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l11lll11_opy_():
    if global_config.get_property(bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ῀")):
        return bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ῁")
    return bstack1lll1l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩῂ")
def bstack111l111llll_opy_(driver):
    info = {
        bstack1lll1l_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪῃ"): driver.capabilities,
        bstack1lll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩῄ"): driver.session_id,
        bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ῅"): driver.capabilities.get(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬῆ"), None),
        bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪῇ"): driver.capabilities.get(bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪῈ"), None),
        bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬΈ"): driver.capabilities.get(bstack1lll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪῊ"), None),
        bstack1lll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨΉ"):driver.capabilities.get(bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨῌ"), None),
    }
    if bstack111l11lll11_opy_() == bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭῍"):
        if bstack111lll11_opy_():
            info[bstack1lll1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ῎")] = bstack1lll1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ῏")
        elif driver.capabilities.get(bstack1lll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫῐ"), {}).get(bstack1lll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨῑ"), False):
            info[bstack1lll1l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ῒ")] = bstack1lll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪΐ")
        else:
            info[bstack1lll1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ῔")] = bstack1lll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ῕")
    return info
def bstack111lll11_opy_():
    if global_config.get_property(bstack1lll1l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨῖ")):
        return True
    if bstack11ll1ll1l_opy_(os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫῗ"), None)):
        return True
    return False
def bstack1111l11l1l1_opy_(bstack1111lll11ll_opy_, url, response, headers=None, data=None):
    bstack1lll1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡇࡻࡩ࡭ࡦࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠ࡭ࡱࡪࠤࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹ࠵ࡲࡦࡵࡳࡳࡳࡹࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡳࡸࡩࡸࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧࠤ࠭ࡍࡅࡕ࠮ࠣࡔࡔ࡙ࡔ࠭ࠢࡨࡸࡨ࠴ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࡸࡶࡱࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡗࡕࡐ࠴࡫࡮ࡥࡲࡲ࡭ࡳࡺࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡦࡳࡱࡰࠤࡷ࡫ࡱࡶࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࡩࡧࡤࡨࡪࡸࡳ࠻ࠢࡕࡩࡶࡻࡥࡴࡶࠣ࡬ࡪࡧࡤࡦࡴࡶࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡢࡶࡤ࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡊࡔࡑࡑࠤࡩࡧࡴࡢࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࠣࡻ࡮ࡺࡨࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠐࠠࠡࠢࠣࠦࠧࠨῘ")
    bstack1111l1l1ll1_opy_ = {
        bstack1lll1l_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨῙ"): headers,
        bstack1lll1l_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨῚ"): bstack1111lll11ll_opy_.upper(),
        bstack1lll1l_opy_ (u"ࠢࡢࡩࡨࡲࡹࠨΊ"): None,
        bstack1lll1l_opy_ (u"ࠣࡧࡱࡨࡵࡵࡩ࡯ࡶࠥ῜"): url,
        bstack1lll1l_opy_ (u"ࠤ࡭ࡷࡴࡴࠢ῝"): data
    }
    try:
        bstack1111ll11l11_opy_ = response.json()
    except Exception:
        bstack1111ll11l11_opy_ = response.text
    bstack111l1111lll_opy_ = {
        bstack1lll1l_opy_ (u"ࠥࡦࡴࡪࡹࠣ῞"): bstack1111ll11l11_opy_,
        bstack1lll1l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࡇࡴࡪࡥࠣ῟"): response.status_code
    }
    return {
        bstack1lll1l_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨῠ"): bstack1111l1l1ll1_opy_,
        bstack1lll1l_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣῡ"): bstack111l1111lll_opy_
    }
def bstack1llll1l111_opy_(bstack1111lll11ll_opy_, url, data, config):
    headers = config.get(bstack1lll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨῢ"), None)
    proxies = bstack11l1l11l11_opy_(config, url)
    auth = config.get(bstack1lll1l_opy_ (u"ࠨࡣࡸࡸ࡭࠭ΰ"), None)
    response = requests.request(
            bstack1111lll11ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1111l11l1l1_opy_(bstack1111lll11ll_opy_, url, response, headers, data)
        bstack1llll11111_opy_.debug(json.dumps(log_message, separators=(bstack1lll1l_opy_ (u"ࠩ࠯ࠫῤ"), bstack1lll1l_opy_ (u"ࠪ࠾ࠬῥ"))))
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴ࠻ࠢࡾࢁࠧῦ").format(e))
    return response
def bstack11ll11l1ll_opy_(bstack1lll1llll1_opy_, size):
    bstack11lll1111_opy_ = []
    while len(bstack1lll1llll1_opy_) > size:
        bstack1ll111l1ll_opy_ = bstack1lll1llll1_opy_[:size]
        bstack11lll1111_opy_.append(bstack1ll111l1ll_opy_)
        bstack1lll1llll1_opy_ = bstack1lll1llll1_opy_[size:]
    bstack11lll1111_opy_.append(bstack1lll1llll1_opy_)
    return bstack11lll1111_opy_
def bstack1111ll1l11l_opy_(message, bstack1111ll1ll1l_opy_=False):
    os.write(1, bytes(message, bstack1lll1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫῧ")))
    os.write(1, bytes(bstack1lll1l_opy_ (u"࠭࡜࡯ࠩῨ"), bstack1lll1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭Ῡ")))
    if bstack1111ll1ll1l_opy_:
        with open(bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧῪ") + os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨΎ")] + bstack1lll1l_opy_ (u"ࠪ࠲ࡱࡵࡧࠨῬ"), bstack1lll1l_opy_ (u"ࠫࡦ࠭῭")) as f:
            f.write(message + bstack1lll1l_opy_ (u"ࠬࡢ࡮ࠨ΅"))
def bstack1l11ll1l1l1_opy_():
    return os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ`")].lower() == bstack1lll1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ῰")
def current_time():
    return bstack11111l1ll1_opy_().replace(tzinfo=None).isoformat() + bstack1lll1l_opy_ (u"ࠨ࡜ࠪ῱")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1lll1l_opy_ (u"ࠩ࡝ࠫῲ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1lll1l_opy_ (u"ࠪ࡞ࠬῳ")))).total_seconds() * 1000
def bstack1111l111l1l_opy_(timestamp):
    return bstack1111ll1111l_opy_(timestamp).isoformat() + bstack1lll1l_opy_ (u"ࠫ࡟࠭ῴ")
def bstack11111lll1l1_opy_(bstack111l11l11l1_opy_):
    date_format = bstack1lll1l_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪ῵")
    bstack1111l11111l_opy_ = datetime.datetime.strptime(bstack111l11l11l1_opy_, date_format)
    return bstack1111l11111l_opy_.isoformat() + bstack1lll1l_opy_ (u"࡚࠭ࠨῶ")
def bstack111l11l1ll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧῷ")
    else:
        return bstack1lll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨῸ")
def bstack11ll1ll1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1lll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧΌ")
def bstack1111l111lll_opy_(val):
    return val.__str__().lower() == bstack1lll1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩῺ")
def error_handler(bstack1111llll1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111llll1ll_opy_ as e:
                print(bstack1lll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦΏ").format(func.__name__, bstack1111llll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11111ll111l_opy_(bstack1111l111111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1111l111111_opy_(cls, *args, **kwargs)
            except bstack1111llll1ll_opy_ as e:
                print(bstack1lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧῼ").format(bstack1111l111111_opy_.__name__, bstack1111llll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11111ll111l_opy_
    else:
        return decorator
def bstack11lll11l1l_opy_(bstack1llll1l1l1l_opy_):
    if os.getenv(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ´")) is not None:
        return bstack11ll1ll1l_opy_(os.getenv(bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ῾")))
    if bstack1lll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ῿") in bstack1llll1l1l1l_opy_ and bstack1111l111lll_opy_(bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ ")]):
        return False
    if bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ ") in bstack1llll1l1l1l_opy_ and bstack1111l111lll_opy_(bstack1llll1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ ")]):
        return False
    return True
def bstack1l111lll_opy_():
    try:
        from pytest_bdd import reporting
        bstack11111ll1111_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧ "), None)
        return bstack11111ll1111_opy_ is None or bstack11111ll1111_opy_ == bstack1lll1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ ")
    except Exception as e:
        return False
def bstack11lll1l1_opy_(hub_url, CONFIG):
    if bstack11llll1lll_opy_() <= version.parse(bstack1lll1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ ")):
        if hub_url:
            return bstack1lll1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ ") + hub_url + bstack1lll1l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ ")
        return bstack1ll11ll1ll_opy_
    if hub_url:
        return bstack1lll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ ") + hub_url + bstack1lll1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ ")
    return HTTPS_HUB
def bstack11111llll11_opy_():
    return isinstance(os.getenv(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ ")), str)
def bstack1l1lllll_opy_(url):
    return urlparse(url).hostname
def bstack1lll1l1ll_opy_(hostname):
    for bstack1l1111llll_opy_ in bstack1ll1l1ll11_opy_:
        regex = re.compile(bstack1l1111llll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111l1lll11_opy_(bstack111l111lll1_opy_, file_name, logger):
    bstack111l11llll_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"࠭ࡾࠨ​")), bstack111l111lll1_opy_)
    try:
        if not os.path.exists(bstack111l11llll_opy_):
            os.makedirs(bstack111l11llll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠧࡿࠩ‌")), bstack111l111lll1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1lll1l_opy_ (u"ࠨࡹࠪ‍")):
                pass
            with open(file_path, bstack1lll1l_opy_ (u"ࠤࡺ࠯ࠧ‎")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11lll1l11l_opy_.format(str(e)))
def bstack11111l1l1l1_opy_(file_name, key, value, logger):
    file_path = bstack1111l1lll11_opy_(bstack1lll1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ‏"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll11l11_opy_ = json.load(open(file_path, bstack1lll1l_opy_ (u"ࠫࡷࡨࠧ‐")))
        else:
            bstack1lll11l11_opy_ = {}
        bstack1lll11l11_opy_[key] = value
        with open(file_path, bstack1lll1l_opy_ (u"ࠧࡽࠫࠣ‑")) as outfile:
            json.dump(bstack1lll11l11_opy_, outfile)
def bstack1l11l1lll1_opy_(file_name, logger):
    file_path = bstack1111l1lll11_opy_(bstack1lll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭‒"), file_name, logger)
    bstack1lll11l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1lll1l_opy_ (u"ࠧࡳࠩ–")) as bstack111ll1l111_opy_:
            bstack1lll11l11_opy_ = json.load(bstack111ll1l111_opy_)
    return bstack1lll11l11_opy_
def bstack11ll1lll1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ—") + file_path + bstack1lll1l_opy_ (u"ࠩࠣࠫ―") + str(e))
def bstack11llll1lll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1lll1l_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧ‖")
def bstack1l11lll111_opy_(config):
    if bstack1lll1l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ‗") in config:
        del (config[bstack1lll1l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ‘")])
        return False
    if bstack11llll1lll_opy_() < version.parse(bstack1lll1l_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬ’")):
        return False
    if bstack11llll1lll_opy_() >= version.parse(bstack1lll1l_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭‚")):
        return True
    if bstack1lll1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ‛") in config and config[bstack1lll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ“")] is False:
        return False
    else:
        return True
def bstack1111lllll_opy_(args_list, bstack1111l1l1l11_opy_):
    index = -1
    for value in bstack1111l1l1l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l11111lll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l11111lll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1111l1ll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1lll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ”"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ„"), exception=exception)
    def bstack1lll1ll111l_opy_(self):
        if self.result != bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ‟"):
            return None
        if isinstance(self.exception_type, str) and bstack1lll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ†") in self.exception_type:
            return bstack1lll1l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ‡")
        return bstack1lll1l_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ•")
    def bstack111l11l1l11_opy_(self):
        if self.result != bstack1lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ‣"):
            return None
        if self.bstack1111l1ll1l_opy_:
            return self.bstack1111l1ll1l_opy_
        return bstack11111l1ll11_opy_(self.exception)
def bstack11111l1ll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111l1l11l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll111ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1ll11l1_opy_(config, logger):
    try:
        import playwright
        bstack1111llllll1_opy_ = playwright.__file__
        bstack111l1111111_opy_ = os.path.split(bstack1111llllll1_opy_)
        bstack111l11ll1ll_opy_ = bstack111l1111111_opy_[0] + bstack1lll1l_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭․")
        os.environ[bstack1lll1l_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧ‥")] = bstack11l1lll1l1_opy_(config)
        with open(bstack111l11ll1ll_opy_, bstack1lll1l_opy_ (u"ࠬࡸࠧ…")) as f:
            bstack1lll111111_opy_ = f.read()
            bstack11111l1lll1_opy_ = bstack1lll1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ‧")
            bstack111l11l11ll_opy_ = bstack1lll111111_opy_.find(bstack11111l1lll1_opy_)
            if bstack111l11l11ll_opy_ == -1:
              process = subprocess.Popen(bstack1lll1l_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦ "), shell=True, cwd=bstack111l1111111_opy_[0])
              process.wait()
              bstack11111ll1l11_opy_ = bstack1lll1l_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨ ")
              bstack11111ll1l1l_opy_ = bstack1lll1l_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨ‪")
              bstack11111l1ll1l_opy_ = bstack1lll111111_opy_.replace(bstack11111ll1l11_opy_, bstack11111ll1l1l_opy_)
              with open(bstack111l11ll1ll_opy_, bstack1lll1l_opy_ (u"ࠪࡻࠬ‫")) as f:
                f.write(bstack11111l1ll1l_opy_)
    except Exception as e:
        logger.error(bstack1l11l1ll1_opy_.format(str(e)))
def bstack1lll1lll_opy_():
  try:
    bstack11111llllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ‬"))
    bstack11111ll1lll_opy_ = []
    if os.path.exists(bstack11111llllll_opy_):
      with open(bstack11111llllll_opy_) as f:
        bstack11111ll1lll_opy_ = json.load(f)
      os.remove(bstack11111llllll_opy_)
    return bstack11111ll1lll_opy_
  except:
    pass
  return []
def bstack1l111ll1l1_opy_(bstack11l1111l1l_opy_):
  try:
    bstack11111ll1lll_opy_ = []
    bstack11111llllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬ‭"))
    if os.path.exists(bstack11111llllll_opy_):
      with open(bstack11111llllll_opy_) as f:
        bstack11111ll1lll_opy_ = json.load(f)
    bstack11111ll1lll_opy_.append(bstack11l1111l1l_opy_)
    with open(bstack11111llllll_opy_, bstack1lll1l_opy_ (u"࠭ࡷࠨ‮")) as f:
        json.dump(bstack11111ll1lll_opy_, f)
  except:
    pass
def bstack1l11lllll_opy_(logger, bstack1111lllllll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1lll1l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ "), bstack1lll1l_opy_ (u"ࠨࠩ‰"))
    if test_name == bstack1lll1l_opy_ (u"ࠩࠪ‱"):
        test_name = threading.current_thread().__dict__.get(bstack1lll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩ′"), bstack1lll1l_opy_ (u"ࠫࠬ″"))
    bstack1111l1l1l1l_opy_ = bstack1lll1l_opy_ (u"ࠬ࠲ࠠࠨ‴").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111lllllll_opy_:
        bstack1ll1llll1l_opy_ = os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭‵"), bstack1lll1l_opy_ (u"ࠧ࠱ࠩ‶"))
        bstack11l11l1lll_opy_ = {bstack1lll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭‷"): test_name, bstack1lll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ‸"): bstack1111l1l1l1l_opy_, bstack1lll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ‹"): bstack1ll1llll1l_opy_}
        bstack111l111ll1l_opy_ = []
        bstack11111l1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ›"))
        if os.path.exists(bstack11111l1l11l_opy_):
            with open(bstack11111l1l11l_opy_) as f:
                bstack111l111ll1l_opy_ = json.load(f)
        bstack111l111ll1l_opy_.append(bstack11l11l1lll_opy_)
        with open(bstack11111l1l11l_opy_, bstack1lll1l_opy_ (u"ࠬࡽࠧ※")) as f:
            json.dump(bstack111l111ll1l_opy_, f)
    else:
        bstack11l11l1lll_opy_ = {bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ‼"): test_name, bstack1lll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭‽"): bstack1111l1l1l1l_opy_, bstack1lll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ‾"): str(multiprocessing.current_process().name)}
        if bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭‿") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11l11l1lll_opy_)
  except Exception as e:
      logger.warn(bstack1lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ⁀").format(e))
def bstack111l11l11_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1lll1l_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ⁁"))
    try:
      bstack111l1111l11_opy_ = []
      bstack11l11l1lll_opy_ = {bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁂"): test_name, bstack1lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⁃"): error_message, bstack1lll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⁄"): index}
      bstack1111llll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⁅"))
      if os.path.exists(bstack1111llll11l_opy_):
          with open(bstack1111llll11l_opy_) as f:
              bstack111l1111l11_opy_ = json.load(f)
      bstack111l1111l11_opy_.append(bstack11l11l1lll_opy_)
      with open(bstack1111llll11l_opy_, bstack1lll1l_opy_ (u"ࠩࡺࠫ⁆")) as f:
          json.dump(bstack111l1111l11_opy_, f)
    except Exception as e:
      logger.warn(bstack1lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⁇").format(e))
    return
  bstack111l1111l11_opy_ = []
  bstack11l11l1lll_opy_ = {bstack1lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⁈"): test_name, bstack1lll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⁉"): error_message, bstack1lll1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⁊"): index}
  bstack1111llll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⁋"))
  lock_file = bstack1111llll11l_opy_ + bstack1lll1l_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ⁌")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1111llll11l_opy_):
          with open(bstack1111llll11l_opy_, bstack1lll1l_opy_ (u"ࠩࡵࠫ⁍")) as f:
              content = f.read().strip()
              if content:
                  bstack111l1111l11_opy_ = json.load(open(bstack1111llll11l_opy_))
      bstack111l1111l11_opy_.append(bstack11l11l1lll_opy_)
      with open(bstack1111llll11l_opy_, bstack1lll1l_opy_ (u"ࠪࡻࠬ⁎")) as f:
          json.dump(bstack111l1111l11_opy_, f)
  except Exception as e:
    logger.warn(bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦ⁏").format(e))
def bstack1lllll11l1_opy_(bstack11l11ll1l1_opy_, name, logger):
  try:
    bstack11l11l1lll_opy_ = {bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁐"): name, bstack1lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⁑"): bstack11l11ll1l1_opy_, bstack1lll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⁒"): str(threading.current_thread()._name)}
    return bstack11l11l1lll_opy_
  except Exception as e:
    logger.warn(bstack1lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ⁓").format(e))
  return
def bstack11111lll111_opy_():
    return platform.system() == bstack1lll1l_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪ⁔")
def bstack11l111111l_opy_(bstack111l111l111_opy_, config, logger):
    bstack1111l1ll1ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l111l111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⁕").format(e))
    return bstack1111l1ll1ll_opy_
def bstack111l11ll111_opy_(bstack1111ll1l1ll_opy_, bstack111l11ll1l1_opy_):
    bstack1111l1l1lll_opy_ = version.parse(bstack1111ll1l1ll_opy_)
    bstack1111l111ll1_opy_ = version.parse(bstack111l11ll1l1_opy_)
    if bstack1111l1l1lll_opy_ > bstack1111l111ll1_opy_:
        return 1
    elif bstack1111l1l1lll_opy_ < bstack1111l111ll1_opy_:
        return -1
    else:
        return 0
def bstack11111l1ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111ll1111l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111l111l1l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll1lll11_opy_(options, framework, config, bstack11ll111l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1lll1l_opy_ (u"ࠫ࡬࡫ࡴࠨ⁖"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1111l1111_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⁗"))
    bstack1111l1111ll_opy_ = True
    bstack1lll1111_opy_ = os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⁘")]
    bstack1l1l1l1l111_opy_ = config.get(bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⁙"), False)
    if bstack1l1l1l1l111_opy_:
        bstack1l1llllll1l_opy_ = config.get(bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⁚"), {})
        bstack1l1llllll1l_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ⁛")] = os.getenv(bstack1lll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⁜"))
        bstack11l111lll11_opy_ = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⁝"), bstack1lll1l_opy_ (u"ࠬࢁࡽࠨ⁞"))).get(bstack1lll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ "))
    if bstack1111l111lll_opy_(caps.get(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭⁠"))) or bstack1111l111lll_opy_(caps.get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨ⁡"))):
        bstack1111l1111ll_opy_ = False
    if bstack1l11lll111_opy_({bstack1lll1l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ⁢"): bstack1111l1111ll_opy_}):
        bstack1111l1111_opy_ = bstack1111l1111_opy_ or {}
        bstack1111l1111_opy_[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⁣")] = bstack111l111l1l1_opy_(framework)
        bstack1111l1111_opy_[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⁤")] = bstack1l11ll1l1l1_opy_()
        bstack1111l1111_opy_[bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⁥")] = bstack1lll1111_opy_
        bstack1111l1111_opy_[bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ⁦")] = bstack11ll111l11_opy_
        if bstack1l1l1l1l111_opy_:
            bstack1111l1111_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⁧")] = bstack1l1l1l1l111_opy_
            bstack1111l1111_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⁨")] = bstack1l1llllll1l_opy_
            bstack1111l1111_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⁩")][bstack1lll1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ⁪")] = bstack11l111lll11_opy_
        if getattr(options, bstack1lll1l_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ⁫"), None):
            options.set_capability(bstack1lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⁬"), bstack1111l1111_opy_)
        else:
            options[bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⁭")] = bstack1111l1111_opy_
    else:
        if getattr(options, bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⁮"), None):
            options.set_capability(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⁯"), bstack111l111l1l1_opy_(framework))
            options.set_capability(bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⁰"), bstack1l11ll1l1l1_opy_())
            options.set_capability(bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬⁱ"), bstack1lll1111_opy_)
            options.set_capability(bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⁲"), bstack11ll111l11_opy_)
            if bstack1l1l1l1l111_opy_:
                options.set_capability(bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⁳"), bstack1l1l1l1l111_opy_)
                options.set_capability(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⁴"), bstack1l1llllll1l_opy_)
                options.set_capability(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⁵"), bstack11l111lll11_opy_)
        else:
            options[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⁶")] = bstack111l111l1l1_opy_(framework)
            options[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⁷")] = bstack1l11ll1l1l1_opy_()
            options[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⁸")] = bstack1lll1111_opy_
            options[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⁹")] = bstack11ll111l11_opy_
            if bstack1l1l1l1l111_opy_:
                options[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⁺")] = bstack1l1l1l1l111_opy_
                options[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⁻")] = bstack1l1llllll1l_opy_
                options[bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⁼")][bstack1lll1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⁽")] = bstack11l111lll11_opy_
    return options
def bstack1111l1111l1_opy_(bstack11111l1l1ll_opy_, framework):
    bstack11ll111l11_opy_ = global_config.get_property(bstack1lll1l_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦ⁾"))
    if bstack11111l1l1ll_opy_ and len(bstack11111l1l1ll_opy_.split(bstack1lll1l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩⁿ"))) > 1:
        ws_url = bstack11111l1l1ll_opy_.split(bstack1lll1l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ₀"))[0]
        if bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ₁") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111ll11l1_opy_ = json.loads(urllib.parse.unquote(bstack11111l1l1ll_opy_.split(bstack1lll1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ₂"))[1]))
            bstack11111ll11l1_opy_ = bstack11111ll11l1_opy_ or {}
            bstack1lll1111_opy_ = os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ₃")]
            bstack11111ll11l1_opy_[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ₄")] = str(framework) + str(__version__)
            bstack11111ll11l1_opy_[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ₅")] = bstack1l11ll1l1l1_opy_()
            bstack11111ll11l1_opy_[bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ₆")] = bstack1lll1111_opy_
            bstack11111ll11l1_opy_[bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ₇")] = bstack11ll111l11_opy_
            bstack11111l1l1ll_opy_ = bstack11111l1l1ll_opy_.split(bstack1lll1l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ₈"))[0] + bstack1lll1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ₉") + urllib.parse.quote(json.dumps(bstack11111ll11l1_opy_))
    return bstack11111l1l1ll_opy_
def bstack1ll11111ll_opy_():
    global bstack111llll11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack111llll11_opy_ = BrowserType.connect
    return bstack111llll11_opy_
def bstack1llllllll_opy_(framework_name):
    global bstack11l11111l_opy_
    bstack11l11111l_opy_ = framework_name
    return framework_name
def bstack1lll11lll1_opy_(self, *args, **kwargs):
    global bstack111llll11_opy_
    try:
        global bstack11l11111l_opy_
        if bstack1lll1l_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ₊") in kwargs:
            kwargs[bstack1lll1l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ₋")] = bstack1111l1111l1_opy_(
                kwargs.get(bstack1lll1l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭₌"), None),
                bstack11l11111l_opy_
            )
    except Exception as e:
        logger.error(bstack1lll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ₍").format(str(e)))
    return bstack111llll11_opy_(self, *args, **kwargs)
def bstack1111lll1ll1_opy_(bstack111l11l1lll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l1l11l11_opy_(bstack111l11l1lll_opy_, bstack1lll1l_opy_ (u"ࠦࠧ₎"))
        if proxies and proxies.get(bstack1lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ₏")):
            parsed_url = urlparse(proxies.get(bstack1lll1l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧₐ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1lll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪₑ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1lll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫₒ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬₓ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ₔ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack111l1l1ll1_opy_(bstack111l11l1lll_opy_):
    bstack1111l11llll_opy_ = {
        bstack111ll1lll1l_opy_[bstack1111ll111l1_opy_]: bstack111l11l1lll_opy_[bstack1111ll111l1_opy_]
        for bstack1111ll111l1_opy_ in bstack111l11l1lll_opy_
        if bstack1111ll111l1_opy_ in bstack111ll1lll1l_opy_
    }
    bstack1111l11llll_opy_[bstack1lll1l_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦₕ")] = bstack1111lll1ll1_opy_(bstack111l11l1lll_opy_, global_config.get_property(bstack1lll1l_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧₖ")))
    bstack1111l11l11l_opy_ = [element.lower() for element in bstack111l1lll1ll_opy_]
    bstack1111lllll11_opy_(bstack1111l11llll_opy_, bstack1111l11l11l_opy_)
    return bstack1111l11llll_opy_
def bstack1111lllll11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1lll1l_opy_ (u"ࠨࠪࠫࠬ࠭ࠦₗ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111lllll11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111lllll11_opy_(item, keys)
def bstack1l111l11lll_opy_():
    bstack11111lllll1_opy_ = [os.environ.get(bstack1lll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤₘ")), os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠣࢀࠥₙ")), bstack1lll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩₚ")), os.path.join(bstack1lll1l_opy_ (u"ࠪ࠳ࡹࡳࡰࠨₛ"), bstack1lll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫₜ"))]
    for path in bstack11111lllll1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1lll1l_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧ₝") + str(path) + bstack1lll1l_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ₞"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1lll1l_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦ₟") + str(path) + bstack1lll1l_opy_ (u"ࠣࠩࠥ₠"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1lll1l_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤ₡") + str(path) + bstack1lll1l_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣ₢"))
            else:
                logger.debug(bstack1lll1l_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨ₣") + str(path) + bstack1lll1l_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤ₤"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1lll1l_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦ₥") + str(path) + bstack1lll1l_opy_ (u"ࠢࠨ࠰ࠥ₦"))
            return path
        except Exception as e:
            logger.debug(bstack1lll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨ₧") + str(e) + bstack1lll1l_opy_ (u"ࠤࠥ₨"))
    logger.debug(bstack1lll1l_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢ₩"))
    return None
@measure(event_name=EVENTS.bstack111l1ll1ll1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
def bstack1lllll1l1ll_opy_(binary_path, bstack1lllll11lll_opy_, bs_config):
    logger.debug(bstack1lll1l_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥ₪").format(binary_path))
    bstack1111llll1l1_opy_ = bstack1lll1l_opy_ (u"ࠬ࠭₫")
    bstack1111l1l111l_opy_ = {
        bstack1lll1l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ€"): __version__,
        bstack1lll1l_opy_ (u"ࠢࡰࡵࠥ₭"): platform.system(),
        bstack1lll1l_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤ₮"): platform.machine(),
        bstack1lll1l_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ₯"): bstack1lll1l_opy_ (u"ࠪ࠴ࠬ₰"),
        bstack1lll1l_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥ₱"): bstack1lll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ₲")
    }
    bstack11111llll1l_opy_(bstack1111l1l111l_opy_)
    try:
        if binary_path:
            if bstack11111lll111_opy_():
                bstack1111l1l111l_opy_[bstack1lll1l_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ₳")] = subprocess.check_output([binary_path, bstack1lll1l_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ₴")]).strip().decode(bstack1lll1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ₵"))
            else:
                bstack1111l1l111l_opy_[bstack1lll1l_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ₶")] = subprocess.check_output([binary_path, bstack1lll1l_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦ₷")], stderr=subprocess.DEVNULL).strip().decode(bstack1lll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ₸"))
        response = requests.request(
            bstack1lll1l_opy_ (u"ࠬࡍࡅࡕࠩ₹"),
            url=bstack11ll1ll1l1_opy_(bstack111ll11l11l_opy_),
            headers=None,
            auth=(bs_config[bstack1lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ₺")], bs_config[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ₻")]),
            json=None,
            params=bstack1111l1l111l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1lll1l_opy_ (u"ࠨࡷࡵࡰࠬ₼") in data.keys() and bstack1lll1l_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦࡢࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ₽") in data.keys():
            logger.debug(bstack1lll1l_opy_ (u"ࠥࡒࡪ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡧ࡯࡮ࡢࡴࡼ࠰ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠦ₾").format(bstack1111l1l111l_opy_[bstack1lll1l_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ₿")]))
            if bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨ⃀") in os.environ:
                logger.debug(bstack1lll1l_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡥࡸࠦࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠢ࡬ࡷࠥࡹࡥࡵࠤ⃁"))
                data[bstack1lll1l_opy_ (u"ࠧࡶࡴ࡯ࠫ⃂")] = os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫ⃃")]
            bstack1111lll1l11_opy_ = bstack111l11ll11l_opy_(data[bstack1lll1l_opy_ (u"ࠩࡸࡶࡱ࠭⃄")], bstack1lllll11lll_opy_)
            bstack1111llll1l1_opy_ = os.path.join(bstack1lllll11lll_opy_, bstack1111lll1l11_opy_)
            os.chmod(bstack1111llll1l1_opy_, 0o777) # bstack1111ll1llll_opy_ permission
            return bstack1111llll1l1_opy_
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡗࡉࡑࠠࡼࡿࠥ⃅").format(e))
    return binary_path
def bstack11111llll1l_opy_(bstack1111l1l111l_opy_):
    try:
        if bstack1lll1l_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪ⃆") not in bstack1111l1l111l_opy_[bstack1lll1l_opy_ (u"ࠬࡵࡳࠨ⃇")].lower():
            return
        if os.path.exists(bstack1lll1l_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ⃈")):
            with open(bstack1lll1l_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ⃉"), bstack1lll1l_opy_ (u"ࠣࡴࠥ⃊")) as f:
                bstack1111l111l11_opy_ = {}
                for line in f:
                    if bstack1lll1l_opy_ (u"ࠤࡀࠦ⃋") in line:
                        key, value = line.rstrip().split(bstack1lll1l_opy_ (u"ࠥࡁࠧ⃌"), 1)
                        bstack1111l111l11_opy_[key] = value.strip(bstack1lll1l_opy_ (u"ࠫࠧࡢࠧࠨ⃍"))
                bstack1111l1l111l_opy_[bstack1lll1l_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬ⃎")] = bstack1111l111l11_opy_.get(bstack1lll1l_opy_ (u"ࠨࡉࡅࠤ⃏"), bstack1lll1l_opy_ (u"ࠢࠣ⃐"))
        elif os.path.exists(bstack1lll1l_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵ࡡ࡭ࡲ࡬ࡲࡪ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ⃑")):
            bstack1111l1l111l_opy_[bstack1lll1l_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰ⃒ࠩ")] = bstack1lll1l_opy_ (u"ࠪࡥࡱࡶࡩ࡯ࡧ⃓ࠪ")
    except Exception as e:
        logger.debug(bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡩ࡯ࡳࡵࡴࡲࠤࡴ࡬ࠠ࡭࡫ࡱࡹࡽࠨ⃔") + e)
@measure(event_name=EVENTS.bstack111ll1ll1l1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
def bstack111l11ll11l_opy_(bstack1111l1llll1_opy_, bstack1111lll11l1_opy_):
    logger.debug(bstack1lll1l_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱ࠿ࠦࠢ⃕") + str(bstack1111l1llll1_opy_) + bstack1lll1l_opy_ (u"ࠨࠢ⃖"))
    zip_path = os.path.join(bstack1111lll11l1_opy_, bstack1lll1l_opy_ (u"ࠢࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࡣ࡫࡯࡬ࡦ࠰ࡽ࡭ࡵࠨ⃗"))
    bstack1111lll1l11_opy_ = bstack1lll1l_opy_ (u"ࠨ⃘ࠩ")
    with requests.get(bstack1111l1llll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1lll1l_opy_ (u"ࠤࡺࡦ⃙ࠧ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1lll1l_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼ࠲⃚ࠧ"))
    with zipfile.ZipFile(zip_path, bstack1lll1l_opy_ (u"ࠫࡷ࠭⃛")) as zip_ref:
        bstack11111lll1ll_opy_ = zip_ref.namelist()
        if len(bstack11111lll1ll_opy_) > 0:
            bstack1111lll1l11_opy_ = bstack11111lll1ll_opy_[0] # bstack1111lll1l1l_opy_ bstack111l1llllll_opy_ will be bstack111l111l1ll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1111lll11l1_opy_)
        logger.debug(bstack1lll1l_opy_ (u"ࠧࡌࡩ࡭ࡧࡶࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡩࡽࡺࡲࡢࡥࡷࡩࡩࠦࡴࡰࠢࠪࠦ⃜") + str(bstack1111lll11l1_opy_) + bstack1lll1l_opy_ (u"ࠨࠧࠣ⃝"))
    os.remove(zip_path)
    return bstack1111lll1l11_opy_
def get_cli_dir():
    bstack111l111l11l_opy_ = bstack1l111l11lll_opy_()
    if bstack111l111l11l_opy_:
        bstack1lllll11lll_opy_ = os.path.join(bstack111l111l11l_opy_, bstack1lll1l_opy_ (u"ࠢࡤ࡮࡬ࠦ⃞"))
        if not os.path.exists(bstack1lllll11lll_opy_):
            os.makedirs(bstack1lllll11lll_opy_, mode=0o777, exist_ok=True)
        return bstack1lllll11lll_opy_
    else:
        raise FileNotFoundError(bstack1lll1l_opy_ (u"ࠣࡐࡲࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠦ⃟"))
def bstack1lllll1l1l1_opy_(bstack1lllll11lll_opy_):
    bstack1lll1l_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡰࠣࡥࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠦࠧࠨ⃠")
    bstack1111l1lllll_opy_ = [
        os.path.join(bstack1lllll11lll_opy_, f)
        for f in os.listdir(bstack1lllll11lll_opy_)
        if os.path.isfile(os.path.join(bstack1lllll11lll_opy_, f)) and f.startswith(bstack1lll1l_opy_ (u"ࠥࡦ࡮ࡴࡡࡳࡻ࠰ࠦ⃡"))
    ]
    if len(bstack1111l1lllll_opy_) > 0:
        return max(bstack1111l1lllll_opy_, key=os.path.getmtime) # get bstack11111ll1ll1_opy_ binary
    return bstack1lll1l_opy_ (u"ࠦࠧ⃢")
def bstack11l111lll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l1lll11l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1l1lll11l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1ll1l11l_opy_(data, keys, default=None):
    bstack1lll1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡡࡧࡧ࡯ࡽࠥ࡭ࡥࡵࠢࡤࠤࡳ࡫ࡳࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡢࡶࡤ࠾࡚ࠥࡨࡦࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺࠠࡵࡱࠣࡸࡷࡧࡶࡦࡴࡶࡩ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣ࡯ࡪࡿࡳ࠻ࠢࡄࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡱࡥࡺࡵ࠲࡭ࡳࡪࡩࡤࡧࡶࠤࡷ࡫ࡰࡳࡧࡶࡩࡳࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡪ࡬ࡡࡶ࡮ࡷ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤࡹࡵࠠࡳࡧࡷࡹࡷࡴࠠࡪࡨࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡸࡥࡵࡷࡵࡲ࠿ࠦࡔࡩࡧࠣࡺࡦࡲࡵࡦࠢࡤࡸࠥࡺࡨࡦࠢࡱࡩࡸࡺࡥࡥࠢࡳࡥࡹ࡮ࠬࠡࡱࡵࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥ࡯ࡦࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⃣")
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
def bstack1l11l1111l_opy_(bstack1111ll1ll11_opy_, key, value):
    bstack1lll1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡵࡱࡵࡩࠥࡉࡌࡊࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠣࡱࡦࡶࡰࡪࡰࡪࠤ࡮ࡴࠠࡵࡪࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥ࡯࡭ࡤ࡫࡮ࡷࡡࡹࡥࡷࡹ࡟࡮ࡣࡳ࠾ࠥࡊࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡬ࡧࡼ࠾ࠥࡑࡥࡺࠢࡩࡶࡴࡳࠠࡄࡎࡌࡣࡈࡇࡐࡔࡡࡗࡓࡤࡉࡏࡏࡈࡌࡋࠏࠦࠠࠡࠢࠣࠤࠥࠦࡶࡢ࡮ࡸࡩ࠿ࠦࡖࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠏࠦࠠࠡࠢࠥࠦࠧ⃤")
    if key in bstack1ll111ll_opy_:
        bstack111lllll_opy_ = bstack1ll111ll_opy_[key]
        if isinstance(bstack111lllll_opy_, list):
            for env_name in bstack111lllll_opy_:
                bstack1111ll1ll11_opy_[env_name] = value
        else:
            bstack1111ll1ll11_opy_[bstack111lllll_opy_] = value