# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
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
from bstack_utils.constants import (bstack1ll1ll1111_opy_, bstack11l11lll1_opy_, HTTPS_HUB,
                                    bstack111ll111ll1_opy_, bstack111ll1l11l1_opy_, bstack111l1llll11_opy_, bstack111ll1l1lll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111ll111l1_opy_, bstack1l1ll1111_opy_
from bstack_utils.proxy import bstack11111ll1_opy_, bstack1ll111l111_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11l11lll1l_opy_ import bstack1l1ll1l1ll_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111111l1_opy_())
bstack11llllll1l_opy_ = logger_utils.bstack1ll11llll1_opy_(__name__)
def bstack11l111l1l1l_opy_(config):
    return config[bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧṟ")]
def bstack11l1111l1l1_opy_(config):
    return config[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩṠ")]
def bstack1l1l1ll1l1_opy_():
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
def bstack1111ll11ll1_opy_(obj):
    values = []
    bstack11111ll1l1l_opy_ = re.compile(bstack1111_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦṡ"), re.I)
    for key in obj.keys():
        if bstack11111ll1l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111lll1ll1_opy_(config):
    tags = []
    tags.extend(bstack1111ll11ll1_opy_(os.environ))
    tags.extend(bstack1111ll11ll1_opy_(config))
    return tags
def bstack1111l11l1ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111l11l11l_opy_(bstack1111l1llll1_opy_):
    if not bstack1111l1llll1_opy_:
        return bstack1111_opy_ (u"ࠨࠩṢ")
    return bstack1111_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥṣ").format(bstack1111l1llll1_opy_.name, bstack1111l1llll1_opy_.email)
def bstack111llllll11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l111l111_opy_ = repo.common_dir
        info = {
            bstack1111_opy_ (u"ࠥࡷ࡭ࡧࠢṤ"): repo.head.commit.hexsha,
            bstack1111_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢṥ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1111_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧṦ"): repo.active_branch.name,
            bstack1111_opy_ (u"ࠨࡴࡢࡩࠥṧ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥṨ"): bstack1111l11l11l_opy_(repo.head.commit.committer),
            bstack1111_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤṩ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1111_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤṪ"): bstack1111l11l11l_opy_(repo.head.commit.author),
            bstack1111_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣṫ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1111_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧṬ"): repo.head.commit.message,
            bstack1111_opy_ (u"ࠧࡸ࡯ࡰࡶࠥṭ"): repo.git.rev_parse(bstack1111_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣṮ")),
            bstack1111_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣṯ"): bstack111l111l111_opy_,
            bstack1111_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦṰ"): subprocess.check_output([bstack1111_opy_ (u"ࠤࡪ࡭ࡹࠨṱ"), bstack1111_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨṲ"), bstack1111_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢṳ")]).strip().decode(
                bstack1111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫṴ")),
            bstack1111_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣṵ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤṶ"): repo.git.rev_list(
                bstack1111_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣṷ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11111l1l11l_opy_ = []
        for remote in remotes:
            bstack1111l1l1lll_opy_ = {
                bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢṸ"): remote.name,
                bstack1111_opy_ (u"ࠥࡹࡷࡲࠢṹ"): remote.url,
            }
            bstack11111l1l11l_opy_.append(bstack1111l1l1lll_opy_)
        bstack1111l111111_opy_ = {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤṺ"): bstack1111_opy_ (u"ࠧ࡭ࡩࡵࠤṻ"),
            **info,
            bstack1111_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢṼ"): bstack11111l1l11l_opy_
        }
        bstack1111l111111_opy_ = bstack111l111l1l1_opy_(bstack1111l111111_opy_)
        return bstack1111l111111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥṽ").format(err))
        return {}
def bstack111l11ll11l_opy_(bstack111l111l1ll_opy_=None):
    bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࡧ࡬࡭ࡻࠣࡪࡴࡸ࡭ࡢࡶࡷࡩࡩࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡸࡷࡪࠦࡣࡢࡵࡨࡷࠥ࡬࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧࡱ࡯ࡨࡪࡸࠠࡪࡰࠣࡸ࡭࡫ࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡪࡴࡲࡤࡦࡴࡶࠤ࠭ࡲࡩࡴࡶ࠯ࠤࡴࡶࡴࡪࡱࡱࡥࡱ࠯࠺ࠡࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡑࡳࡳ࡫࠺ࠡࡏࡲࡲࡴ࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭࠲ࠠࡶࡵࡨࡷࠥࡩࡵࡳࡴࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡞ࡳࡸ࠴ࡧࡦࡶࡦࡻࡩ࠮ࠩ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡈࡱࡵࡺࡹࠡ࡮࡬ࡷࡹ࡛ࠦ࡞࠼ࠣࡑࡺࡲࡴࡪ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩࠢࡺ࡭ࡹ࡮ࠠ࡯ࡱࠣࡷࡴࡻࡲࡤࡧࡶࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤ࠭ࠢࡵࡩࡹࡻࡲ࡯ࡵࠣ࡟ࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡱࡣࡷ࡬ࡸࡀࠠࡎࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡵࡱࠣࡥࡳࡧ࡬ࡺࡼࡨࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡩ࡯ࡣࡵࡵ࠯ࠤࡪࡧࡣࡩࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡤࠤ࡫ࡵ࡬ࡥࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧṾ")
    if bstack111l111l1ll_opy_ is None:
        bstack111l111l1ll_opy_ = [os.getcwd()]
    elif isinstance(bstack111l111l1ll_opy_, list) and len(bstack111l111l1ll_opy_) == 0:
        return []
    results = []
    for folder in bstack111l111l1ll_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1111_opy_ (u"ࠤࡉࡳࡱࡪࡥࡳࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢṿ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1111_opy_ (u"ࠥࡴࡷࡏࡤࠣẀ"): bstack1111_opy_ (u"ࠦࠧẁ"),
                bstack1111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦẂ"): [],
                bstack1111_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢẃ"): [],
                bstack1111_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢẄ"): bstack1111_opy_ (u"ࠣࠤẅ"),
                bstack1111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡏࡨࡷࡸࡧࡧࡦࡵࠥẆ"): [],
                bstack1111_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦẇ"): bstack1111_opy_ (u"ࠦࠧẈ"),
                bstack1111_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧẉ"): bstack1111_opy_ (u"ࠨࠢẊ"),
                bstack1111_opy_ (u"ࠢࡱࡴࡕࡥࡼࡊࡩࡧࡨࠥẋ"): bstack1111_opy_ (u"ࠣࠤẌ")
            }
            bstack1111lllll1l_opy_ = repo.active_branch.name
            bstack111l111ll1l_opy_ = repo.head.commit
            result[bstack1111_opy_ (u"ࠤࡳࡶࡎࡪࠢẍ")] = bstack111l111ll1l_opy_.hexsha
            bstack1111l11111l_opy_ = _11111l1l1ll_opy_(repo)
            logger.debug(bstack1111_opy_ (u"ࠥࡆࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡨࡲࡶࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯࠼ࠣࠦẎ") + str(bstack1111l11111l_opy_) + bstack1111_opy_ (u"ࠦࠧẏ"))
            if bstack1111l11111l_opy_:
                try:
                    bstack11111ll1111_opy_ = repo.git.diff(bstack1111_opy_ (u"ࠧ࠳࠭࡯ࡣࡰࡩ࠲ࡵ࡮࡭ࡻࠥẐ"), bstack1ll1l1l11l1_opy_ (u"ࠨࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂ࠴࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦẑ")).split(bstack1111_opy_ (u"ࠧ࡝ࡰࠪẒ"))
                    logger.debug(bstack1111_opy_ (u"ࠣࡅ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡤࡨࡸࡼ࡫ࡥ࡯ࠢࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾࠢࡤࡲࡩࠦࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾ࠼ࠣࠦẓ") + str(bstack11111ll1111_opy_) + bstack1111_opy_ (u"ࠤࠥẔ"))
                    result[bstack1111_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤẕ")] = [f.strip() for f in bstack11111ll1111_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1l1l11l1_opy_ (u"ࠦࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀ࠲࠳ࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽࠣẖ")))
                except Exception:
                    logger.debug(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡧ࡮ࡤࡪࠣࡧࡴࡳࡰࡢࡴ࡬ࡷࡴࡴ࠮ࠡࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡶࡪࡩࡥ࡯ࡶࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠧẗ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1111_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧẘ")] = _11111l1l1l1_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1111_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨẙ")] = _11111l1l1l1_opy_(commits[:5])
            bstack11111l1ll11_opy_ = set()
            bstack11111llll11_opy_ = []
            for commit in commits:
                logger.debug(bstack1111_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯࡬ࡸ࠿ࠦࠢẚ") + str(commit.message) + bstack1111_opy_ (u"ࠤࠥẛ"))
                bstack111l11111ll_opy_ = commit.author.name if commit.author else bstack1111_opy_ (u"࡙ࠥࡳࡱ࡮ࡰࡹࡱࠦẜ")
                bstack11111l1ll11_opy_.add(bstack111l11111ll_opy_)
                bstack11111llll11_opy_.append({
                    bstack1111_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧẝ"): commit.message.strip(),
                    bstack1111_opy_ (u"ࠧࡻࡳࡦࡴࠥẞ"): bstack111l11111ll_opy_
                })
            result[bstack1111_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢẟ")] = list(bstack11111l1ll11_opy_)
            result[bstack1111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡍࡦࡵࡶࡥ࡬࡫ࡳࠣẠ")] = bstack11111llll11_opy_
            result[bstack1111_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣạ")] = bstack111l111ll1l_opy_.committed_datetime.strftime(bstack1111_opy_ (u"ࠤࠨ࡝࠲ࠫ࡭࠮ࠧࡧࠦẢ"))
            if (not result[bstack1111_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦả")] or result[bstack1111_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧẤ")].strip() == bstack1111_opy_ (u"ࠧࠨấ")) and bstack111l111ll1l_opy_.message:
                bstack1111l1ll1l1_opy_ = bstack111l111ll1l_opy_.message.strip().splitlines()
                result[bstack1111_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢẦ")] = bstack1111l1ll1l1_opy_[0] if bstack1111l1ll1l1_opy_ else bstack1111_opy_ (u"ࠢࠣầ")
                if len(bstack1111l1ll1l1_opy_) > 2:
                    result[bstack1111_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣẨ")] = bstack1111_opy_ (u"ࠩ࡟ࡲࠬẩ").join(bstack1111l1ll1l1_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࠪࡩࡳࡱࡪࡥࡳ࠼ࠣࡿࢂ࠯࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤẪ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _1111ll1111l_opy_(result)
    ]
    return filtered_results
def _1111ll1111l_opy_(result):
    bstack1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡍ࡫࡬ࡱࡧࡵࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡩࡧࠢࡤࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡹࡵ࡭ࡶࠣ࡭ࡸࠦࡶࡢ࡮࡬ࡨࠥ࠮࡮ࡰࡰ࠰ࡩࡲࡶࡴࡺࠢࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠡࡣࡱࡨࠥࡧࡵࡵࡪࡲࡶࡸ࠯࠮ࠋࠢࠣࠤࠥࠨࠢࠣẫ")
    return (
        isinstance(result.get(bstack1111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦẬ"), None), list)
        and len(result[bstack1111_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧậ")]) > 0
        and isinstance(result.get(bstack1111_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣẮ"), None), list)
        and len(result[bstack1111_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤắ")]) > 0
    )
def _11111l1l1ll_opy_(repo):
    bstack1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡗࡶࡾࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡨࡦࠢࡥࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡳࡧࡳࡳࠥࡽࡩࡵࡪࡲࡹࡹࠦࡨࡢࡴࡧࡧࡴࡪࡥࡥࠢࡱࡥࡲ࡫ࡳࠡࡣࡱࡨࠥࡽ࡯ࡳ࡭ࠣࡻ࡮ࡺࡨࠡࡣ࡯ࡰࠥ࡜ࡃࡔࠢࡳࡶࡴࡼࡩࡥࡧࡵࡷ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡥࡶࡦࡴࡣࡩࠢ࡬ࡪࠥࡶ࡯ࡴࡵ࡬ࡦࡱ࡫ࠬࠡࡧ࡯ࡷࡪࠦࡎࡰࡰࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧẰ")
    try:
        try:
            origin = repo.remotes.origin
            bstack111l111111l_opy_ = origin.refs[bstack1111_opy_ (u"ࠪࡌࡊࡇࡄࠨằ")]
            target = bstack111l111111l_opy_.reference.name
            if target.startswith(bstack1111_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬẲ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1111_opy_ (u"ࠬࡵࡲࡪࡩ࡬ࡲ࠴࠭ẳ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _11111l1l1l1_opy_(commits):
    bstack1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠊࠡࠢࠣࠤࠧࠨࠢẴ")
    bstack11111ll1111_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11111llllll_opy_ in diff:
                        if bstack11111llllll_opy_.a_path:
                            bstack11111ll1111_opy_.add(bstack11111llllll_opy_.a_path)
                        if bstack11111llllll_opy_.b_path:
                            bstack11111ll1111_opy_.add(bstack11111llllll_opy_.b_path)
    except Exception:
        pass
    return list(bstack11111ll1111_opy_)
def bstack111l111l1l1_opy_(bstack1111l111111_opy_):
    bstack11111ll111l_opy_ = bstack1111lllllll_opy_(bstack1111l111111_opy_)
    if bstack11111ll111l_opy_ and bstack11111ll111l_opy_ > bstack111ll111ll1_opy_:
        bstack1111ll11111_opy_ = bstack11111ll111l_opy_ - bstack111ll111ll1_opy_
        bstack1111ll111ll_opy_ = bstack11111l11ll1_opy_(bstack1111l111111_opy_[bstack1111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣẵ")], bstack1111ll11111_opy_)
        bstack1111l111111_opy_[bstack1111_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤẶ")] = bstack1111ll111ll_opy_
        logger.info(bstack1111_opy_ (u"ࠤࡗ࡬ࡪࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡨࡢࡵࠣࡦࡪ࡫࡮ࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧ࠲࡙ࠥࡩࡻࡧࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡡࡧࡶࡨࡶࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥࢁࡽࠡࡍࡅࠦặ")
                    .format(bstack1111lllllll_opy_(bstack1111l111111_opy_) / 1024))
    return bstack1111l111111_opy_
def bstack1111lllllll_opy_(bstack1ll1ll1lll_opy_):
    try:
        if bstack1ll1ll1lll_opy_:
            bstack1111l111ll1_opy_ = json.dumps(bstack1ll1ll1lll_opy_)
            bstack1111lll11ll_opy_ = sys.getsizeof(bstack1111l111ll1_opy_)
            return bstack1111lll11ll_opy_
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡦࡥࡱࡩࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡌࡖࡓࡓࠦ࡯ࡣ࡬ࡨࡧࡹࡀࠠࡼࡿࠥẸ").format(e))
    return -1
def bstack11111l11ll1_opy_(field, bstack1111l1ll111_opy_):
    try:
        bstack111l111l11l_opy_ = len(bytes(bstack111ll1l11l1_opy_, bstack1111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪẹ")))
        bstack11111lllll1_opy_ = bytes(field, bstack1111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫẺ"))
        bstack1111l1l11ll_opy_ = len(bstack11111lllll1_opy_)
        bstack111l111llll_opy_ = ceil(bstack1111l1l11ll_opy_ - bstack1111l1ll111_opy_ - bstack111l111l11l_opy_)
        if bstack111l111llll_opy_ > 0:
            bstack111l1111lll_opy_ = bstack11111lllll1_opy_[:bstack111l111llll_opy_].decode(bstack1111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬẻ"), errors=bstack1111_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࠧẼ")) + bstack111ll1l11l1_opy_
            return bstack111l1111lll_opy_
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡴࡳࡷࡱࡧࡦࡺࡩ࡯ࡩࠣࡪ࡮࡫࡬ࡥ࠮ࠣࡲࡴࡺࡨࡪࡰࡪࠤࡼࡧࡳࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧࠤ࡭࡫ࡲࡦ࠼ࠣࡿࢂࠨẽ").format(e))
    return field
def bstack1ll11111_opy_():
    env = os.environ
    if (bstack1111_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢẾ") in env and len(env[bstack1111_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣế")]) > 0) or (
            bstack1111_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥỀ") in env and len(env[bstack1111_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦề")]) > 0):
        return {
            bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦỂ"): bstack1111_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣể"),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦỄ"): env.get(bstack1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧễ")),
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧỆ"): env.get(bstack1111_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨệ")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦỈ"): env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧỉ"))
        }
    if env.get(bstack1111_opy_ (u"ࠢࡄࡋࠥỊ")) == bstack1111_opy_ (u"ࠣࡶࡵࡹࡪࠨị") and bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦỌ"))):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣọ"): bstack1111_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨỎ"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣỏ"): env.get(bstack1111_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤỐ")),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤố"): env.get(bstack1111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧỒ")),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣồ"): env.get(bstack1111_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨỔ"))
        }
    if env.get(bstack1111_opy_ (u"ࠦࡈࡏࠢổ")) == bstack1111_opy_ (u"ࠧࡺࡲࡶࡧࠥỖ") and bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨỗ"))):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧỘ"): bstack1111_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦộ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧỚ"): env.get(bstack1111_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥớ")),
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨỜ"): env.get(bstack1111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢờ")),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧỞ"): env.get(bstack1111_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨở"))
        }
    if env.get(bstack1111_opy_ (u"ࠣࡅࡌࠦỠ")) == bstack1111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢỡ") and env.get(bstack1111_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦỢ")) == bstack1111_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨợ"):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥỤ"): bstack1111_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣụ"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥỦ"): None,
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥủ"): None,
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣỨ"): None
        }
    if env.get(bstack1111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨứ")) and env.get(bstack1111_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢỪ")):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥừ"): bstack1111_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤỬ"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥử"): env.get(bstack1111_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨỮ")),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦữ"): None,
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤỰ"): env.get(bstack1111_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨự"))
        }
    if env.get(bstack1111_opy_ (u"ࠧࡉࡉࠣỲ")) == bstack1111_opy_ (u"ࠨࡴࡳࡷࡨࠦỳ") and bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨỴ"))):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨỵ"): bstack1111_opy_ (u"ࠤࡇࡶࡴࡴࡥࠣỶ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨỷ"): env.get(bstack1111_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢỸ")),
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢỹ"): None,
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧỺ"): env.get(bstack1111_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧỻ"))
        }
    if env.get(bstack1111_opy_ (u"ࠣࡅࡌࠦỼ")) == bstack1111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢỽ") and bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨỾ"))):
        return {
            bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤỿ"): bstack1111_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣἀ"),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤἁ"): env.get(bstack1111_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨἂ")),
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥἃ"): env.get(bstack1111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢἄ")),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤἅ"): env.get(bstack1111_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢἆ"))
        }
    if env.get(bstack1111_opy_ (u"ࠧࡉࡉࠣἇ")) == bstack1111_opy_ (u"ࠨࡴࡳࡷࡨࠦἈ") and bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥἉ"))):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨἊ"): bstack1111_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤἋ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨἌ"): env.get(bstack1111_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣἍ")),
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢἎ"): env.get(bstack1111_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦἏ")),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨἐ"): env.get(bstack1111_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦἑ"))
        }
    if env.get(bstack1111_opy_ (u"ࠤࡆࡍࠧἒ")) == bstack1111_opy_ (u"ࠥࡸࡷࡻࡥࠣἓ") and bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢἔ"))):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥἕ"): bstack1111_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤ἖"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ἗"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢἘ")),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦἙ"): env.get(bstack1111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧἚ")) or env.get(bstack1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢἛ")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦἜ"): env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣἝ"))
        }
    if bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤ἞"))):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨ἟"): bstack1111_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤἠ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨἡ"): bstack1111_opy_ (u"ࠦࢀࢃࡻࡾࠤἢ").format(env.get(bstack1111_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨἣ")), env.get(bstack1111_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭ἤ"))),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤἥ"): env.get(bstack1111_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊࠢἦ")),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣἧ"): env.get(bstack1111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥἨ"))
        }
    if bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨἩ"))):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥἪ"): bstack1111_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲࠣἫ"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥἬ"): bstack1111_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠢἭ").format(env.get(bstack1111_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨἮ")), env.get(bstack1111_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫἯ")), env.get(bstack1111_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬἰ")), env.get(bstack1111_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩἱ"))),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣἲ"): env.get(bstack1111_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦἳ")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢἴ"): env.get(bstack1111_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥἵ"))
        }
    if env.get(bstack1111_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦἶ")) and env.get(bstack1111_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨἷ")):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥἸ"): bstack1111_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉࠣἹ"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥἺ"): bstack1111_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦἻ").format(env.get(bstack1111_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬἼ")), env.get(bstack1111_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨἽ")), env.get(bstack1111_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫἾ"))),
            bstack1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢἿ"): env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨὀ")),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨὁ"): env.get(bstack1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣὂ"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢὃ")), env.get(bstack1111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤὄ")), env.get(bstack1111_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣὅ"))]):
        return {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ὆"): bstack1111_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨ὇"),
            bstack1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥὈ"): env.get(bstack1111_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢὉ")),
            bstack1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦὊ"): env.get(bstack1111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣὋ")),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥὌ"): env.get(bstack1111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥὍ"))
        }
    if env.get(bstack1111_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ὎")):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ὏"): bstack1111_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯ࠣὐ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧὑ"): env.get(bstack1111_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧὒ")),
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨὓ"): env.get(bstack1111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦὔ")),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧὕ"): env.get(bstack1111_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧὖ"))
        }
    if env.get(bstack1111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤὗ")) or env.get(bstack1111_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ὘")):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣὙ"): bstack1111_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶࠧ὚"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣὛ"): env.get(bstack1111_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ὜")),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤὝ"): bstack1111_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣ὞") if env.get(bstack1111_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦὟ")) else None,
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤὠ"): env.get(bstack1111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤὡ"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥὢ")), env.get(bstack1111_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢὣ")), env.get(bstack1111_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢὤ"))]):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨὥ"): bstack1111_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣὦ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨὧ"): None,
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨὨ"): env.get(bstack1111_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤὩ")),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧὪ"): env.get(bstack1111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤὫ"))
        }
    if env.get(bstack1111_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦὬ")):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢὭ"): bstack1111_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨὮ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢὯ"): env.get(bstack1111_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦὰ")),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣά"): bstack1111_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣὲ").format(env.get(bstack1111_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫέ"))) if env.get(bstack1111_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧὴ")) else None,
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤή"): env.get(bstack1111_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨὶ"))
        }
    if bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨί"))):
        return {
            bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦὸ"): bstack1111_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹࠣό"),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦὺ"): env.get(bstack1111_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨύ")),
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧὼ"): env.get(bstack1111_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢώ")),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ὾"): env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ὿"))
        }
    if bstack11ll1l1l1l_opy_(env.get(bstack1111_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣᾀ"))):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᾁ"): bstack1111_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥᾂ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᾃ"): bstack1111_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧᾄ").format(env.get(bstack1111_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩᾅ")), env.get(bstack1111_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪᾆ")), env.get(bstack1111_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧᾇ"))),
            bstack1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᾈ"): env.get(bstack1111_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦᾉ")),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᾊ"): env.get(bstack1111_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦᾋ"))
        }
    if env.get(bstack1111_opy_ (u"ࠧࡉࡉࠣᾌ")) == bstack1111_opy_ (u"ࠨࡴࡳࡷࡨࠦᾍ") and env.get(bstack1111_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢᾎ")) == bstack1111_opy_ (u"ࠣ࠳ࠥᾏ"):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᾐ"): bstack1111_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥᾑ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᾒ"): bstack1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣᾓ").format(env.get(bstack1111_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎࠪᾔ"))),
            bstack1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᾕ"): None,
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᾖ"): None,
        }
    if env.get(bstack1111_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᾗ")):
        return {
            bstack1111_opy_ (u"ࠥࡲࡦࡳࡥࠣᾘ"): bstack1111_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨᾙ"),
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᾚ"): None,
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᾛ"): env.get(bstack1111_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣᾜ")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᾝ"): env.get(bstack1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᾞ"))
        }
    if any([env.get(bstack1111_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨᾟ")), env.get(bstack1111_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦᾠ")), env.get(bstack1111_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥᾡ")), env.get(bstack1111_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓࠢᾢ"))]):
        return {
            bstack1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᾣ"): bstack1111_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦᾤ"),
            bstack1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᾥ"): None,
            bstack1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᾦ"): env.get(bstack1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᾧ")) or None,
            bstack1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᾨ"): env.get(bstack1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᾩ"), 0)
        }
    if env.get(bstack1111_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᾪ")):
        return {
            bstack1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᾫ"): bstack1111_opy_ (u"ࠤࡊࡳࡈࡊࠢᾬ"),
            bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᾭ"): None,
            bstack1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᾮ"): env.get(bstack1111_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᾯ")),
            bstack1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᾰ"): env.get(bstack1111_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨᾱ"))
        }
    if env.get(bstack1111_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᾲ")):
        return {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᾳ"): bstack1111_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨᾴ"),
            bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᾵"): env.get(bstack1111_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᾶ")),
            bstack1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᾷ"): env.get(bstack1111_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥᾸ")),
            bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᾹ"): env.get(bstack1111_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᾺ"))
        }
    return {bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤΆ"): None}
def get_host_info():
    return {
        bstack1111_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨᾼ"): platform.node(),
        bstack1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ᾽"): platform.system(),
        bstack1111_opy_ (u"ࠨࡴࡺࡲࡨࠦι"): platform.machine(),
        bstack1111_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ᾿"): platform.version(),
        bstack1111_opy_ (u"ࠣࡣࡵࡧ࡭ࠨ῀"): platform.architecture()[0]
    }
def bstack1lllll11l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111l1111l1_opy_():
    if global_config.get_property(bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ῁")):
        return bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩῂ")
    return bstack1111_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪῃ")
def bstack1111l1lll11_opy_(driver):
    info = {
        bstack1111_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫῄ"): driver.capabilities,
        bstack1111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ῅"): driver.session_id,
        bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨῆ"): driver.capabilities.get(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ῇ"), None),
        bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫῈ"): driver.capabilities.get(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫΈ"), None),
        bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭Ὴ"): driver.capabilities.get(bstack1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫΉ"), None),
        bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩῌ"):driver.capabilities.get(bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ῍"), None),
    }
    if bstack1111l1111l1_opy_() == bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ῎"):
        if bstack11l1ll1lll_opy_():
            info[bstack1111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ῏")] = bstack1111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩῐ")
        elif driver.capabilities.get(bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬῑ"), {}).get(bstack1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩῒ"), False):
            info[bstack1111_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧΐ")] = bstack1111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ῔")
        else:
            info[bstack1111_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ῕")] = bstack1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫῖ")
    return info
def bstack11l1ll1lll_opy_():
    if global_config.get_property(bstack1111_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩῗ")):
        return True
    if bstack11ll1l1l1l_opy_(os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬῘ"), None)):
        return True
    return False
def bstack1111ll1llll_opy_(bstack111l11l1lll_opy_, url, response, headers=None, data=None):
    bstack1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡈࡵࡪ࡮ࡧࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࠥࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠯ࡳࡧࡶࡴࡴࡴࡳࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡴࡹࡪࡹࡴࡠࡶࡼࡴࡪࡀࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨࠥ࠮ࡇࡆࡖ࠯ࠤࡕࡕࡓࡕ࠮ࠣࡩࡹࡩ࠮ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࡹࡷࡲ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡘࡖࡑ࠵ࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡰࡤ࡭ࡩࡨࡺࠠࡧࡴࡲࡱࠥࡸࡥࡲࡷࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࡪࡨࡥࡩ࡫ࡲࡴ࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡭࡫ࡡࡥࡧࡵࡷࠥࡵࡲࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥࡣࡷࡥ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡋࡕࡒࡒࠥࡪࡡࡵࡣࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡊࡴࡸ࡭ࡢࡶࡷࡩࡩࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨࠤࡼ࡯ࡴࡩࠢࡵࡩࡶࡻࡥࡴࡶࠣࡥࡳࡪࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡧࡥࡹࡧࠊࠡࠢࠣࠤࠧࠨࠢῙ")
    bstack1111l1l111l_opy_ = {
        bstack1111_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢῚ"): headers,
        bstack1111_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢΊ"): bstack111l11l1lll_opy_.upper(),
        bstack1111_opy_ (u"ࠣࡣࡪࡩࡳࡺࠢ῜"): None,
        bstack1111_opy_ (u"ࠤࡨࡲࡩࡶ࡯ࡪࡰࡷࠦ῝"): url,
        bstack1111_opy_ (u"ࠥ࡮ࡸࡵ࡮ࠣ῞"): data
    }
    try:
        bstack1111l111l1l_opy_ = response.json()
    except Exception:
        bstack1111l111l1l_opy_ = response.text
    bstack1111l11ll1l_opy_ = {
        bstack1111_opy_ (u"ࠦࡧࡵࡤࡺࠤ῟"): bstack1111l111l1l_opy_,
        bstack1111_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࡈࡵࡤࡦࠤῠ"): response.status_code
    }
    return {
        bstack1111_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢῡ"): bstack1111l1l111l_opy_,
        bstack1111_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤῢ"): bstack1111l11ll1l_opy_
    }
def bstack1llll1l1ll_opy_(bstack111l11l1lll_opy_, url, data, config):
    headers = config.get(bstack1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩΰ"), None)
    proxies = bstack11111ll1_opy_(config, url)
    auth = config.get(bstack1111_opy_ (u"ࠩࡤࡹࡹ࡮ࠧῤ"), None)
    response = requests.request(
            bstack111l11l1lll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1111ll1llll_opy_(bstack111l11l1lll_opy_, url, response, headers, data)
        bstack11llllll1l_opy_.debug(json.dumps(log_message, separators=(bstack1111_opy_ (u"ࠪ࠰ࠬῥ"), bstack1111_opy_ (u"ࠫ࠿࠭ῦ"))))
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡰࡴ࡭ࡧࡪࡰࡪࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵ࠼ࠣࡿࢂࠨῧ").format(e))
    return response
def bstack11l1l11ll1_opy_(bstack11ll1l1ll_opy_, size):
    bstack1lll1lllll_opy_ = []
    while len(bstack11ll1l1ll_opy_) > size:
        bstack1lll1ll1ll_opy_ = bstack11ll1l1ll_opy_[:size]
        bstack1lll1lllll_opy_.append(bstack1lll1ll1ll_opy_)
        bstack11ll1l1ll_opy_ = bstack11ll1l1ll_opy_[size:]
    bstack1lll1lllll_opy_.append(bstack11ll1l1ll_opy_)
    return bstack1lll1lllll_opy_
def bstack1111l1111ll_opy_(message, bstack1111ll11l1l_opy_=False):
    os.write(1, bytes(message, bstack1111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬῨ")))
    os.write(1, bytes(bstack1111_opy_ (u"ࠧ࡝ࡰࠪῩ"), bstack1111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧῪ")))
    if bstack1111ll11l1l_opy_:
        with open(bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨΎ") + os.environ[bstack1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩῬ")] + bstack1111_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩ῭"), bstack1111_opy_ (u"ࠬࡧࠧ΅")) as f:
            f.write(message + bstack1111_opy_ (u"࠭࡜࡯ࠩ`"))
def bstack1l111l1ll1l_opy_():
    return os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ῰")].lower() == bstack1111_opy_ (u"ࠨࡶࡵࡹࡪ࠭῱")
def current_time():
    return bstack11111111l1_opy_().replace(tzinfo=None).isoformat() + bstack1111_opy_ (u"ࠩ࡝ࠫῲ")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1111_opy_ (u"ࠪ࡞ࠬῳ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1111_opy_ (u"ࠫ࡟࠭ῴ")))).total_seconds() * 1000
def bstack1111lll1111_opy_(timestamp):
    return bstack1111ll1ll1l_opy_(timestamp).isoformat() + bstack1111_opy_ (u"ࠬࡠࠧ῵")
def bstack11111l11lll_opy_(bstack11111lll1ll_opy_):
    date_format = bstack1111_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫῶ")
    bstack1111llll11l_opy_ = datetime.datetime.strptime(bstack11111lll1ll_opy_, date_format)
    return bstack1111llll11l_opy_.isoformat() + bstack1111_opy_ (u"࡛ࠧࠩῷ")
def bstack111l11111l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨῸ")
    else:
        return bstack1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩΌ")
def bstack11ll1l1l1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1111_opy_ (u"ࠪࡸࡷࡻࡥࠨῺ")
def bstack1111l1lllll_opy_(val):
    return val.__str__().lower() == bstack1111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪΏ")
def error_handler(bstack1111l1l1l1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111l1l1l1l_opy_ as e:
                print(bstack1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧῼ").format(func.__name__, bstack1111l1l1l1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1111ll11l11_opy_(bstack11111llll1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111llll1l_opy_(cls, *args, **kwargs)
            except bstack1111l1l1l1l_opy_ as e:
                print(bstack1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨ´").format(bstack11111llll1l_opy_.__name__, bstack1111l1l1l1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1111ll11l11_opy_
    else:
        return decorator
def bstack1ll11ll11l_opy_(bstack1llll1ll111_opy_):
    if os.getenv(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ῾")) is not None:
        return bstack11ll1l1l1l_opy_(os.getenv(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ῿")))
    if bstack1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ ") in bstack1llll1ll111_opy_ and bstack1111l1lllll_opy_(bstack1llll1ll111_opy_[bstack1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ ")]):
        return False
    if bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ ") in bstack1llll1ll111_opy_ and bstack1111l1lllll_opy_(bstack1llll1ll111_opy_[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ ")]):
        return False
    return True
def bstack1l1ll11l_opy_():
    try:
        from pytest_bdd import reporting
        bstack1111lll1lll_opy_ = os.environ.get(bstack1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨ "), None)
        return bstack1111lll1lll_opy_ is None or bstack1111lll1lll_opy_ == bstack1111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ ")
    except Exception as e:
        return False
def bstack1111l111l_opy_(hub_url, CONFIG):
    if bstack1l111ll11l_opy_() <= version.parse(bstack1111_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ ")):
        if hub_url:
            return bstack1111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ ") + hub_url + bstack1111_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ ")
        return bstack11l11lll1_opy_
    if hub_url:
        return bstack1111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ ") + hub_url + bstack1111_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ ")
    return HTTPS_HUB
def bstack11111l1ll1l_opy_():
    return isinstance(os.getenv(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ​")), str)
def bstack11l111l11_opy_(url):
    return urlparse(url).hostname
def bstack11l11llll_opy_(hostname):
    for bstack111l11lll_opy_ in bstack1ll1ll1111_opy_:
        regex = re.compile(bstack111l11lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111lll1l11_opy_(bstack111l11lll11_opy_, file_name, logger):
    bstack11llll111_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠧࡿࠩ‌")), bstack111l11lll11_opy_)
    try:
        if not os.path.exists(bstack11llll111_opy_):
            os.makedirs(bstack11llll111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠨࢀࠪ‍")), bstack111l11lll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1111_opy_ (u"ࠩࡺࠫ‎")):
                pass
            with open(file_path, bstack1111_opy_ (u"ࠥࡻ࠰ࠨ‏")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111ll111l1_opy_.format(str(e)))
def bstack1111ll11lll_opy_(file_name, key, value, logger):
    file_path = bstack1111lll1l11_opy_(bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ‐"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lll1l11_opy_ = json.load(open(file_path, bstack1111_opy_ (u"ࠬࡸࡢࠨ‑")))
        else:
            bstack1l1lll1l11_opy_ = {}
        bstack1l1lll1l11_opy_[key] = value
        with open(file_path, bstack1111_opy_ (u"ࠨࡷࠬࠤ‒")) as outfile:
            json.dump(bstack1l1lll1l11_opy_, outfile)
def bstack1llllll1l_opy_(file_name, logger):
    file_path = bstack1111lll1l11_opy_(bstack1111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ–"), file_name, logger)
    bstack1l1lll1l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1111_opy_ (u"ࠨࡴࠪ—")) as bstack1llllllll_opy_:
            bstack1l1lll1l11_opy_ = json.load(bstack1llllllll_opy_)
    return bstack1l1lll1l11_opy_
def bstack1l1lll1l1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨ࠾ࠥ࠭―") + file_path + bstack1111_opy_ (u"ࠪࠤࠬ‖") + str(e))
def bstack1l111ll11l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1111_opy_ (u"ࠦࡁࡔࡏࡕࡕࡈࡘࡃࠨ‗")
def bstack1ll1l1ll11_opy_(config):
    if bstack1111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ‘") in config:
        del (config[bstack1111_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ’")])
        return False
    if bstack1l111ll11l_opy_() < version.parse(bstack1111_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭‚")):
        return False
    if bstack1l111ll11l_opy_() >= version.parse(bstack1111_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧ‛")):
        return True
    if bstack1111_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ“") in config and config[bstack1111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ”")] is False:
        return False
    else:
        return True
def bstack1l1l1lll1l_opy_(args_list, bstack111l11ll1l1_opy_):
    index = -1
    for value in bstack111l11ll1l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l111l111l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l111l111l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1111l11lll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1111l11lll_opy_ = bstack1111l11lll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ„"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ‟"), exception=exception)
    def bstack1lll1ll1111_opy_(self):
        if self.result != bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭†"):
            return None
        if isinstance(self.exception_type, str) and bstack1111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ‡") in self.exception_type:
            return bstack1111_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ•")
        return bstack1111_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥ‣")
    def bstack1111l1ll1ll_opy_(self):
        if self.result != bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ․"):
            return None
        if self.bstack1111l11lll_opy_:
            return self.bstack1111l11lll_opy_
        return bstack1111ll1l1ll_opy_(self.exception)
def bstack1111ll1l1ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111l111l11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll11lll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1ll1ll1_opy_(config, logger):
    try:
        import playwright
        bstack11111lll1l1_opy_ = playwright.__file__
        bstack1111l1ll11l_opy_ = os.path.split(bstack11111lll1l1_opy_)
        bstack111l11l111l_opy_ = bstack1111l1ll11l_opy_[0] + bstack1111_opy_ (u"ࠫ࠴ࡪࡲࡪࡸࡨࡶ࠴ࡶࡡࡤ࡭ࡤ࡫ࡪ࠵࡬ࡪࡤ࠲ࡧࡱ࡯࠯ࡤ࡮࡬࠲࡯ࡹࠧ‥")
        os.environ[bstack1111_opy_ (u"ࠬࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠨ…")] = bstack1ll111l111_opy_(config)
        with open(bstack111l11l111l_opy_, bstack1111_opy_ (u"࠭ࡲࠨ‧")) as f:
            bstack1ll1llll1l_opy_ = f.read()
            bstack1111l11ll11_opy_ = bstack1111_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ ")
            bstack11111l1lll1_opy_ = bstack1ll1llll1l_opy_.find(bstack1111l11ll11_opy_)
            if bstack11111l1lll1_opy_ == -1:
              process = subprocess.Popen(bstack1111_opy_ (u"ࠣࡰࡳࡱࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠧ "), shell=True, cwd=bstack1111l1ll11l_opy_[0])
              process.wait()
              bstack11111ll11ll_opy_ = bstack1111_opy_ (u"ࠩࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺࠢ࠼ࠩ‪")
              bstack1111l11l111_opy_ = bstack1111_opy_ (u"ࠥࠦࠧࠦ࡜ࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࡡࠨ࠻ࠡࡥࡲࡲࡸࡺࠠࡼࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴࠥࢃࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ࠭ࡀࠦࡩࡧࠢࠫࡴࡷࡵࡣࡦࡵࡶ࠲ࡪࡴࡶ࠯ࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜࠭ࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠩࠫ࠾ࠤࠧࠨࠢ‫")
              bstack111l1111l1l_opy_ = bstack1ll1llll1l_opy_.replace(bstack11111ll11ll_opy_, bstack1111l11l111_opy_)
              with open(bstack111l11l111l_opy_, bstack1111_opy_ (u"ࠫࡼ࠭‬")) as f:
                f.write(bstack111l1111l1l_opy_)
    except Exception as e:
        logger.error(bstack1l1ll1111_opy_.format(str(e)))
def bstack1llll11l11_opy_():
  try:
    bstack11111ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬ‭"))
    bstack1111lllll11_opy_ = []
    if os.path.exists(bstack11111ll1ll1_opy_):
      with open(bstack11111ll1ll1_opy_) as f:
        bstack1111lllll11_opy_ = json.load(f)
      os.remove(bstack11111ll1ll1_opy_)
    return bstack1111lllll11_opy_
  except:
    pass
  return []
def bstack1l1l1ll11_opy_(bstack11llllllll_opy_):
  try:
    bstack1111lllll11_opy_ = []
    bstack11111ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭‮"))
    if os.path.exists(bstack11111ll1ll1_opy_):
      with open(bstack11111ll1ll1_opy_) as f:
        bstack1111lllll11_opy_ = json.load(f)
    bstack1111lllll11_opy_.append(bstack11llllllll_opy_)
    with open(bstack11111ll1ll1_opy_, bstack1111_opy_ (u"ࠧࡸࠩ ")) as f:
        json.dump(bstack1111lllll11_opy_, f)
  except:
    pass
def bstack1l1lll111_opy_(logger, bstack1111ll1ll11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1111_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ‰"), bstack1111_opy_ (u"ࠩࠪ‱"))
    if test_name == bstack1111_opy_ (u"ࠪࠫ′"):
        test_name = threading.current_thread().__dict__.get(bstack1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡆࡩࡪ࡟ࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠪ″"), bstack1111_opy_ (u"ࠬ࠭‴"))
    bstack11111ll1l11_opy_ = bstack1111_opy_ (u"࠭ࠬࠡࠩ‵").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111ll1ll11_opy_:
        bstack111ll11111_opy_ = os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ‶"), bstack1111_opy_ (u"ࠨ࠲ࠪ‷"))
        bstack11llllll1_opy_ = {bstack1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ‸"): test_name, bstack1111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ‹"): bstack11111ll1l11_opy_, bstack1111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ›"): bstack111ll11111_opy_}
        bstack111l1111l11_opy_ = []
        bstack11111l1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ※"))
        if os.path.exists(bstack11111l1l111_opy_):
            with open(bstack11111l1l111_opy_) as f:
                bstack111l1111l11_opy_ = json.load(f)
        bstack111l1111l11_opy_.append(bstack11llllll1_opy_)
        with open(bstack11111l1l111_opy_, bstack1111_opy_ (u"࠭ࡷࠨ‼")) as f:
            json.dump(bstack111l1111l11_opy_, f)
    else:
        bstack11llllll1_opy_ = {bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ‽"): test_name, bstack1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ‾"): bstack11111ll1l11_opy_, bstack1111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ‿"): str(multiprocessing.current_process().name)}
        if bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧ⁀") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11llllll1_opy_)
  except Exception as e:
      logger.warn(bstack1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡰࡺࡶࡨࡷࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣ⁁").format(e))
def bstack11lllll1ll_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨ⁂"))
    try:
      bstack11111lll11l_opy_ = []
      bstack11llllll1_opy_ = {bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁃"): test_name, bstack1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⁄"): error_message, bstack1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⁅"): index}
      bstack111l1111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ⁆"))
      if os.path.exists(bstack111l1111ll1_opy_):
          with open(bstack111l1111ll1_opy_) as f:
              bstack11111lll11l_opy_ = json.load(f)
      bstack11111lll11l_opy_.append(bstack11llllll1_opy_)
      with open(bstack111l1111ll1_opy_, bstack1111_opy_ (u"ࠪࡻࠬ⁇")) as f:
          json.dump(bstack11111lll11l_opy_, f)
    except Exception as e:
      logger.warn(bstack1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ⁈").format(e))
    return
  bstack11111lll11l_opy_ = []
  bstack11llllll1_opy_ = {bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁉"): test_name, bstack1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⁊"): error_message, bstack1111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⁋"): index}
  bstack111l1111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⁌"))
  lock_file = bstack111l1111ll1_opy_ + bstack1111_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨ⁍")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111l1111ll1_opy_):
          with open(bstack111l1111ll1_opy_, bstack1111_opy_ (u"ࠪࡶࠬ⁎")) as f:
              content = f.read().strip()
              if content:
                  bstack11111lll11l_opy_ = json.load(open(bstack111l1111ll1_opy_))
      bstack11111lll11l_opy_.append(bstack11llllll1_opy_)
      with open(bstack111l1111ll1_opy_, bstack1111_opy_ (u"ࠫࡼ࠭⁏")) as f:
          json.dump(bstack11111lll11l_opy_, f)
  except Exception as e:
    logger.warn(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧ࠻ࠢࡾࢁࠧ⁐").format(e))
def bstack1l11ll111_opy_(bstack111ll11l_opy_, name, logger):
  try:
    bstack11llllll1_opy_ = {bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁑"): name, bstack1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⁒"): bstack111ll11l_opy_, bstack1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⁓"): str(threading.current_thread()._name)}
    return bstack11llllll1_opy_
  except Exception as e:
    logger.warn(bstack1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⁔").format(e))
  return
def bstack1111l1l11l1_opy_():
    return platform.system() == bstack1111_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫ⁕")
def bstack1lllllll1_opy_(bstack111l11ll111_opy_, config, logger):
    bstack1111ll1l1l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l11ll111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⁖").format(e))
    return bstack1111ll1l1l1_opy_
def bstack11111ll11l1_opy_(bstack1111l11llll_opy_, bstack11111ll1lll_opy_):
    bstack1111l111lll_opy_ = version.parse(bstack1111l11llll_opy_)
    bstack1111ll1lll1_opy_ = version.parse(bstack11111ll1lll_opy_)
    if bstack1111l111lll_opy_ > bstack1111ll1lll1_opy_:
        return 1
    elif bstack1111l111lll_opy_ < bstack1111ll1lll1_opy_:
        return -1
    else:
        return 0
def bstack11111111l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111ll1ll1l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111llll111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11lll111l1_opy_(options, framework, config, bstack1ll11ll1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1111_opy_ (u"ࠬ࡭ࡥࡵࠩ⁗"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l1l1ll_opy_ = caps.get(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⁘"))
    bstack111l11l11l1_opy_ = True
    bstack11l1l11l1l_opy_ = os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⁙")]
    bstack1l1l1l111l1_opy_ = config.get(bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⁚"), False)
    if bstack1l1l1l111l1_opy_:
        bstack1ll11111111_opy_ = config.get(bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⁛"), {})
        bstack1ll11111111_opy_[bstack1111_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭⁜")] = os.getenv(bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⁝"))
        bstack11l11111ll1_opy_ = json.loads(os.getenv(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭⁞"), bstack1111_opy_ (u"࠭ࡻࡾࠩ "))).get(bstack1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⁠"))
    if bstack1111l1lllll_opy_(caps.get(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧ⁡"))) or bstack1111l1lllll_opy_(caps.get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩ⁢"))):
        bstack111l11l11l1_opy_ = False
    if bstack1ll1l1ll11_opy_({bstack1111_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ⁣"): bstack111l11l11l1_opy_}):
        bstack11l1l1ll_opy_ = bstack11l1l1ll_opy_ or {}
        bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⁤")] = bstack1111llll111_opy_(framework)
        bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⁥")] = bstack1l111l1ll1l_opy_()
        bstack11l1l1ll_opy_[bstack1111_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ⁦")] = bstack11l1l11l1l_opy_
        bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ⁧")] = bstack1ll11ll1_opy_
        if bstack1l1l1l111l1_opy_:
            bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⁨")] = bstack1l1l1l111l1_opy_
            bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⁩")] = bstack1ll11111111_opy_
            bstack11l1l1ll_opy_[bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ⁪")][bstack1111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⁫")] = bstack11l11111ll1_opy_
        if getattr(options, bstack1111_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭⁬"), None):
            options.set_capability(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⁭"), bstack11l1l1ll_opy_)
        else:
            options[bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ⁮")] = bstack11l1l1ll_opy_
    else:
        if getattr(options, bstack1111_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⁯"), None):
            options.set_capability(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⁰"), bstack1111llll111_opy_(framework))
            options.set_capability(bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫⁱ"), bstack1l111l1ll1l_opy_())
            options.set_capability(bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭⁲"), bstack11l1l11l1l_opy_)
            options.set_capability(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭⁳"), bstack1ll11ll1_opy_)
            if bstack1l1l1l111l1_opy_:
                options.set_capability(bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⁴"), bstack1l1l1l111l1_opy_)
                options.set_capability(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⁵"), bstack1ll11111111_opy_)
                options.set_capability(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⁶"), bstack11l11111ll1_opy_)
        else:
            options[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⁷")] = bstack1111llll111_opy_(framework)
            options[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⁸")] = bstack1l111l1ll1l_opy_()
            options[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭⁹")] = bstack11l1l11l1l_opy_
            options[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭⁺")] = bstack1ll11ll1_opy_
            if bstack1l1l1l111l1_opy_:
                options[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⁻")] = bstack1l1l1l111l1_opy_
                options[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⁼")] = bstack1ll11111111_opy_
                options[bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⁽")][bstack1111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⁾")] = bstack11l11111ll1_opy_
    return options
def bstack1111l1l1l11_opy_(bstack11111l1llll_opy_, framework):
    bstack1ll11ll1_opy_ = global_config.get_property(bstack1111_opy_ (u"ࠥࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡑࡔࡒࡈ࡚ࡉࡔࡠࡏࡄࡔࠧⁿ"))
    if bstack11111l1llll_opy_ and len(bstack11111l1llll_opy_.split(bstack1111_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ₀"))) > 1:
        ws_url = bstack11111l1llll_opy_.split(bstack1111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ₁"))[0]
        if bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ₂") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1111l1l1ll1_opy_ = json.loads(urllib.parse.unquote(bstack11111l1llll_opy_.split(bstack1111_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭₃"))[1]))
            bstack1111l1l1ll1_opy_ = bstack1111l1l1ll1_opy_ or {}
            bstack11l1l11l1l_opy_ = os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭₄")]
            bstack1111l1l1ll1_opy_[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ₅")] = str(framework) + str(__version__)
            bstack1111l1l1ll1_opy_[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ₆")] = bstack1l111l1ll1l_opy_()
            bstack1111l1l1ll1_opy_[bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭₇")] = bstack11l1l11l1l_opy_
            bstack1111l1l1ll1_opy_[bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭₈")] = bstack1ll11ll1_opy_
            bstack11111l1llll_opy_ = bstack11111l1llll_opy_.split(bstack1111_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ₉"))[0] + bstack1111_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭₊") + urllib.parse.quote(json.dumps(bstack1111l1l1ll1_opy_))
    return bstack11111l1llll_opy_
def bstack111l1l1l1_opy_():
    global bstack111llll1l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack111llll1l1_opy_ = BrowserType.connect
    return bstack111llll1l1_opy_
def bstack111ll1ll1l_opy_(framework_name):
    global bstack111llll11l_opy_
    bstack111llll11l_opy_ = framework_name
    return framework_name
def bstack111lll111l_opy_(self, *args, **kwargs):
    global bstack111llll1l1_opy_
    try:
        global bstack111llll11l_opy_
        if bstack1111_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ₋") in kwargs:
            kwargs[bstack1111_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭₌")] = bstack1111l1l1l11_opy_(
                kwargs.get(bstack1111_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ₍"), None),
                bstack111llll11l_opy_
            )
    except Exception as e:
        logger.error(bstack1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦ₎").format(str(e)))
    return bstack111llll1l1_opy_(self, *args, **kwargs)
def bstack1111ll1l111_opy_(bstack111l11ll1ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11111ll1_opy_(bstack111l11ll1ll_opy_, bstack1111_opy_ (u"ࠧࠨ₏"))
        if proxies and proxies.get(bstack1111_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧₐ")):
            parsed_url = urlparse(proxies.get(bstack1111_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨₑ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫₒ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬₓ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ₔ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧₕ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l1l1l11_opy_(bstack111l11ll1ll_opy_):
    bstack1111lll11l1_opy_ = {
        bstack111ll1l1lll_opy_[bstack1111llllll1_opy_]: bstack111l11ll1ll_opy_[bstack1111llllll1_opy_]
        for bstack1111llllll1_opy_ in bstack111l11ll1ll_opy_
        if bstack1111llllll1_opy_ in bstack111ll1l1lll_opy_
    }
    bstack1111lll11l1_opy_[bstack1111_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧₖ")] = bstack1111ll1l111_opy_(bstack111l11ll1ll_opy_, global_config.get_property(bstack1111_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨₗ")))
    bstack111l1111111_opy_ = [element.lower() for element in bstack111l1llll11_opy_]
    bstack111l11l1l1l_opy_(bstack1111lll11l1_opy_, bstack111l1111111_opy_)
    return bstack1111lll11l1_opy_
def bstack111l11l1l1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1111_opy_ (u"ࠢࠫࠬ࠭࠮ࠧₘ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l11l1l1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l11l1l1l_opy_(item, keys)
def bstack1l111l11lll_opy_():
    bstack111l11l1111_opy_ = [os.environ.get(bstack1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡋࡏࡉࡘࡥࡄࡊࡔࠥₙ")), os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠤࢁࠦₚ")), bstack1111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪₛ")), os.path.join(bstack1111_opy_ (u"ࠫ࠴ࡺ࡭ࡱࠩₜ"), bstack1111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ₝"))]
    for path in bstack111l11l1111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1111_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨ₞") + str(path) + bstack1111_opy_ (u"ࠢࠨࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥ₟"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1111_opy_ (u"ࠣࡉ࡬ࡺ࡮ࡴࡧࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸࠦࡦࡰࡴࠣࠫࠧ₠") + str(path) + bstack1111_opy_ (u"ࠤࠪࠦ₡"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1111_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥ₢") + str(path) + bstack1111_opy_ (u"ࠦࠬࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳ࠯ࠤ₣"))
            else:
                logger.debug(bstack1111_opy_ (u"ࠧࡉࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥ࠭ࠢ₤") + str(path) + bstack1111_opy_ (u"ࠨࠧࠡࡹ࡬ࡸ࡭ࠦࡷࡳ࡫ࡷࡩࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯࠰ࠥ₥"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1111_opy_ (u"ࠢࡐࡲࡨࡶࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩࠦࡦࡰࡴࠣࠫࠧ₦") + str(path) + bstack1111_opy_ (u"ࠣࠩ࠱ࠦ₧"))
            return path
        except Exception as e:
            logger.debug(bstack1111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡸࡴࠥ࡬ࡩ࡭ࡧࠣࠫࢀࡶࡡࡵࡪࢀࠫ࠿ࠦࠢ₨") + str(e) + bstack1111_opy_ (u"ࠥࠦ₩"))
    logger.debug(bstack1111_opy_ (u"ࠦࡆࡲ࡬ࠡࡲࡤࡸ࡭ࡹࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠣ₪"))
    return None
@measure(event_name=EVENTS.bstack111ll1l1l1l_opy_, stage=STAGE.bstack111l1lllll_opy_)
def bstack1lllll1l11l_opy_(binary_path, bstack1lllll1lll1_opy_, bs_config):
    logger.debug(bstack1111_opy_ (u"ࠧࡉࡵࡳࡴࡨࡲࡹࠦࡃࡍࡋࠣࡔࡦࡺࡨࠡࡨࡲࡹࡳࡪ࠺ࠡࡽࢀࠦ₫").format(binary_path))
    bstack111l111ll11_opy_ = bstack1111_opy_ (u"࠭ࠧ€")
    bstack1111llll1l1_opy_ = {
        bstack1111_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ₭"): __version__,
        bstack1111_opy_ (u"ࠣࡱࡶࠦ₮"): platform.system(),
        bstack1111_opy_ (u"ࠤࡲࡷࡤࡧࡲࡤࡪࠥ₯"): platform.machine(),
        bstack1111_opy_ (u"ࠥࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ₰"): bstack1111_opy_ (u"ࠫ࠵࠭₱"),
        bstack1111_opy_ (u"ࠧࡹࡤ࡬ࡡ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠦ₲"): bstack1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭₳")
    }
    bstack1111ll111l1_opy_(bstack1111llll1l1_opy_)
    try:
        if binary_path:
            if bstack1111l1l11l1_opy_():
                bstack1111llll1l1_opy_[bstack1111_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ₴")] = subprocess.check_output([binary_path, bstack1111_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ₵")]).strip().decode(bstack1111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ₶"))
            else:
                bstack1111llll1l1_opy_[bstack1111_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ₷")] = subprocess.check_output([binary_path, bstack1111_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ₸")], stderr=subprocess.DEVNULL).strip().decode(bstack1111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ₹"))
        response = requests.request(
            bstack1111_opy_ (u"࠭ࡇࡆࡖࠪ₺"),
            url=bstack1l1ll1l1ll_opy_(bstack111l1lll1l1_opy_),
            headers=None,
            auth=(bs_config[bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ₻")], bs_config[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ₼")]),
            json=None,
            params=bstack1111llll1l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1111_opy_ (u"ࠩࡸࡶࡱ࠭₽") in data.keys() and bstack1111_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧࡣࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ₾") in data.keys():
            logger.debug(bstack1111_opy_ (u"ࠦࡓ࡫ࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡨࡩ࡯ࡣࡵࡽ࠱ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧ₿").format(bstack1111llll1l1_opy_[bstack1111_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ⃀")]))
            if bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ⃁") in os.environ:
                logger.debug(bstack1111_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡦࡹࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥ⃂"))
                data[bstack1111_opy_ (u"ࠨࡷࡵࡰࠬ⃃")] = os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬ⃄")]
            bstack1111lll111l_opy_ = bstack11111lll111_opy_(data[bstack1111_opy_ (u"ࠪࡹࡷࡲࠧ⃅")], bstack1lllll1lll1_opy_)
            bstack111l111ll11_opy_ = os.path.join(bstack1lllll1lll1_opy_, bstack1111lll111l_opy_)
            os.chmod(bstack111l111ll11_opy_, 0o777) # bstack111l11l1ll1_opy_ permission
            return bstack111l111ll11_opy_
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦ⃆").format(e))
    return binary_path
def bstack1111ll111l1_opy_(bstack1111llll1l1_opy_):
    try:
        if bstack1111_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫ⃇") not in bstack1111llll1l1_opy_[bstack1111_opy_ (u"࠭࡯ࡴࠩ⃈")].lower():
            return
        if os.path.exists(bstack1111_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ⃉")):
            with open(bstack1111_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ⃊"), bstack1111_opy_ (u"ࠤࡵࠦ⃋")) as f:
                bstack111l111lll1_opy_ = {}
                for line in f:
                    if bstack1111_opy_ (u"ࠥࡁࠧ⃌") in line:
                        key, value = line.rstrip().split(bstack1111_opy_ (u"ࠦࡂࠨ⃍"), 1)
                        bstack111l111lll1_opy_[key] = value.strip(bstack1111_opy_ (u"ࠬࠨ࡜ࠨࠩ⃎"))
                bstack1111llll1l1_opy_[bstack1111_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭⃏")] = bstack111l111lll1_opy_.get(bstack1111_opy_ (u"ࠢࡊࡆࠥ⃐"), bstack1111_opy_ (u"ࠣࠤ⃑"))
        elif os.path.exists(bstack1111_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥ⃒ࠣ")):
            bstack1111llll1l1_opy_[bstack1111_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱ⃓ࠪ")] = bstack1111_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨࠫ⃔")
    except Exception as e:
        logger.debug(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾࠢ⃕") + e)
@measure(event_name=EVENTS.bstack111l1lll1ll_opy_, stage=STAGE.bstack111l1lllll_opy_)
def bstack11111lll111_opy_(bstack1111ll1l11l_opy_, bstack1111l1lll1l_opy_):
    logger.debug(bstack1111_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣ⃖") + str(bstack1111ll1l11l_opy_) + bstack1111_opy_ (u"ࠢࠣ⃗"))
    zip_path = os.path.join(bstack1111l1lll1l_opy_, bstack1111_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶ⃘ࠢ"))
    bstack1111lll111l_opy_ = bstack1111_opy_ (u"⃙ࠩࠪ")
    with requests.get(bstack1111ll1l11l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1111_opy_ (u"ࠥࡻࡧࠨ⃚")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1111_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨ⃛"))
    with zipfile.ZipFile(zip_path, bstack1111_opy_ (u"ࠬࡸࠧ⃜")) as zip_ref:
        bstack1111llll1ll_opy_ = zip_ref.namelist()
        if len(bstack1111llll1ll_opy_) > 0:
            bstack1111lll111l_opy_ = bstack1111llll1ll_opy_[0] # bstack1111l11lll1_opy_ bstack111l1llll1l_opy_ will be bstack111l11l1l11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1111l1lll1l_opy_)
        logger.debug(bstack1111_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱࠣࠫࠧ⃝") + str(bstack1111l1lll1l_opy_) + bstack1111_opy_ (u"ࠢࠨࠤ⃞"))
    os.remove(zip_path)
    return bstack1111lll111l_opy_
def get_cli_dir():
    bstack1111l1l1111_opy_ = bstack1l111l11lll_opy_()
    if bstack1111l1l1111_opy_:
        bstack1lllll1lll1_opy_ = os.path.join(bstack1111l1l1111_opy_, bstack1111_opy_ (u"ࠣࡥ࡯࡭ࠧ⃟"))
        if not os.path.exists(bstack1lllll1lll1_opy_):
            os.makedirs(bstack1lllll1lll1_opy_, mode=0o777, exist_ok=True)
        return bstack1lllll1lll1_opy_
    else:
        raise FileNotFoundError(bstack1111_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠧ⃠"))
def bstack1lllll1l1l1_opy_(bstack1lllll1lll1_opy_):
    bstack1111_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨࠢ⃡")
    bstack1111lll1l1l_opy_ = [
        os.path.join(bstack1lllll1lll1_opy_, f)
        for f in os.listdir(bstack1lllll1lll1_opy_)
        if os.path.isfile(os.path.join(bstack1lllll1lll1_opy_, f)) and f.startswith(bstack1111_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱ࠧ⃢"))
    ]
    if len(bstack1111lll1l1l_opy_) > 0:
        return max(bstack1111lll1l1l_opy_, key=os.path.getmtime) # get bstack111l11l11ll_opy_ binary
    return bstack1111_opy_ (u"ࠧࠨ⃣")
def bstack11l1111llll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l111l111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1l111l111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11111l1ll_opy_(data, keys, default=None):
    bstack1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡢࡨࡨࡰࡾࠦࡧࡦࡶࠣࡥࠥࡴࡥࡴࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡣࡷࡥ࠿ࠦࡔࡩࡧࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡶࡲࠤࡹࡸࡡࡷࡧࡵࡷࡪ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡰ࡫ࡹࡴ࠼ࠣࡅࠥࡲࡩࡴࡶࠣࡳ࡫ࠦ࡫ࡦࡻࡶ࠳࡮ࡴࡤࡪࡥࡨࡷࠥࡸࡥࡱࡴࡨࡷࡪࡴࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩ࡫ࡦࡢࡷ࡯ࡸ࠿ࠦࡖࡢ࡮ࡸࡩࠥࡺ࡯ࠡࡴࡨࡸࡺࡸ࡮ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡲࡦࡶࡸࡶࡳࡀࠠࡕࡪࡨࠤࡻࡧ࡬ࡶࡧࠣࡥࡹࠦࡴࡩࡧࠣࡲࡪࡹࡴࡦࡦࠣࡴࡦࡺࡨ࠭ࠢࡲࡶࠥࡪࡥࡧࡣࡸࡰࡹࠦࡩࡧࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⃤")
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
def bstack1ll1l11lll_opy_(bstack1111l11l1l1_opy_, key, value):
    bstack1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡶࡲࡶࡪࠦࡃࡍࡋࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠤࡲࡧࡰࡱ࡫ࡱ࡫ࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡰ࡮ࡥࡥ࡯ࡸࡢࡺࡦࡸࡳࡠ࡯ࡤࡴ࠿ࠦࡄࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡭ࡨࡽ࠿ࠦࡋࡦࡻࠣࡪࡷࡵ࡭ࠡࡅࡏࡍࡤࡉࡁࡑࡕࡢࡘࡔࡥࡃࡐࡐࡉࡍࡌࠐࠠࠡࠢࠣࠤࠥࠦࠠࡷࡣ࡯ࡹࡪࡀࠠࡗࡣ࡯ࡹࡪࠦࡦࡳࡱࡰࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡲࡩ࡯ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠐࠠࠡࠢࠣࠦࠧࠨ⃥")
    if key in bstack1l1llll1l1_opy_:
        bstack11lll111_opy_ = bstack1l1llll1l1_opy_[key]
        if isinstance(bstack11lll111_opy_, list):
            for env_name in bstack11lll111_opy_:
                bstack1111l11l1l1_opy_[env_name] = value
        else:
            bstack1111l11l1l1_opy_[bstack11lll111_opy_] = value