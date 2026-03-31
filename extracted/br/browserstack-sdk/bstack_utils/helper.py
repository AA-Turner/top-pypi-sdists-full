# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
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
from bstack_utils.constants import (bstack1111ll1lll_opy_, bstack111l111ll_opy_, HTTPS_HUB,
                                    bstack111l111llll_opy_, bstack111l111lll1_opy_, bstack111l111l111_opy_, bstack111l11111ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1ll111_opy_, bstack1lll11l1l1_opy_
from bstack_utils.proxy import bstack11lllll1l_opy_, bstack11l11lll1_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1ll1ll11ll_opy_ import bstack1llll1ll1l_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack111ll11llll_opy_(config):
    return config[bstack1ll11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᾚ")]
def bstack111lll11l11_opy_(config):
    return config[bstack1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᾛ")]
def bstack111111111l_opy_():
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
def bstack111111l111l_opy_(obj):
    values = []
    bstack11111l1l1ll_opy_ = re.compile(bstack1ll11_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦᾜ"), re.I)
    for key in obj.keys():
        if bstack11111l1l1ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111111l11ll_opy_(config):
    tags = []
    tags.extend(bstack111111l111l_opy_(os.environ))
    tags.extend(bstack111111l111l_opy_(config))
    return tags
def bstack1111l111l11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11111ll1111_opy_(bstack1llllll1l1l1_opy_):
    if not bstack1llllll1l1l1_opy_:
        return bstack1ll11_opy_ (u"ࠨࠩᾝ")
    return bstack1ll11_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥᾞ").format(bstack1llllll1l1l1_opy_.name, bstack1llllll1l1l1_opy_.email)
def bstack111ll1lllll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111ll11111_opy_ = repo.common_dir
        info = {
            bstack1ll11_opy_ (u"ࠥࡷ࡭ࡧࠢᾟ"): repo.head.commit.hexsha,
            bstack1ll11_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢᾠ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll11_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧᾡ"): repo.active_branch.name,
            bstack1ll11_opy_ (u"ࠨࡴࡢࡩࠥᾢ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥᾣ"): bstack11111ll1111_opy_(repo.head.commit.committer),
            bstack1ll11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤᾤ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll11_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤᾥ"): bstack11111ll1111_opy_(repo.head.commit.author),
            bstack1ll11_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣᾦ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᾧ"): repo.head.commit.message,
            bstack1ll11_opy_ (u"ࠧࡸ࡯ࡰࡶࠥᾨ"): repo.git.rev_parse(bstack1ll11_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣᾩ")),
            bstack1ll11_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᾪ"): bstack1111ll11111_opy_,
            bstack1ll11_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᾫ"): subprocess.check_output([bstack1ll11_opy_ (u"ࠤࡪ࡭ࡹࠨᾬ"), bstack1ll11_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨᾭ"), bstack1ll11_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢᾮ")]).strip().decode(
                bstack1ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᾯ")),
            bstack1ll11_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᾰ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤᾱ"): repo.git.rev_list(
                bstack1ll11_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣᾲ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1llllllll11l_opy_ = []
        for remote in remotes:
            bstack11111l111ll_opy_ = {
                bstack1ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᾳ"): remote.name,
                bstack1ll11_opy_ (u"ࠥࡹࡷࡲࠢᾴ"): remote.url,
            }
            bstack1llllllll11l_opy_.append(bstack11111l111ll_opy_)
        bstack11111111111_opy_ = {
            bstack1ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᾵"): bstack1ll11_opy_ (u"ࠧ࡭ࡩࡵࠤᾶ"),
            **info,
            bstack1ll11_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢᾷ"): bstack1llllllll11l_opy_
        }
        bstack11111111111_opy_ = bstack11111l11111_opy_(bstack11111111111_opy_)
        return bstack11111111111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᾸ").format(err))
        return {}
def bstack11111lll1l1_opy_(bstack1llllll1ll11_opy_=None):
    bstack1ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࡧ࡬࡭ࡻࠣࡪࡴࡸ࡭ࡢࡶࡷࡩࡩࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡸࡷࡪࠦࡣࡢࡵࡨࡷࠥ࡬࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧࡱ࡯ࡨࡪࡸࠠࡪࡰࠣࡸ࡭࡫ࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡪࡴࡲࡤࡦࡴࡶࠤ࠭ࡲࡩࡴࡶ࠯ࠤࡴࡶࡴࡪࡱࡱࡥࡱ࠯࠺ࠡࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡑࡳࡳ࡫࠺ࠡࡏࡲࡲࡴ࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭࠲ࠠࡶࡵࡨࡷࠥࡩࡵࡳࡴࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡞ࡳࡸ࠴ࡧࡦࡶࡦࡻࡩ࠮ࠩ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡈࡱࡵࡺࡹࠡ࡮࡬ࡷࡹ࡛ࠦ࡞࠼ࠣࡑࡺࡲࡴࡪ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩࠢࡺ࡭ࡹ࡮ࠠ࡯ࡱࠣࡷࡴࡻࡲࡤࡧࡶࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤ࠭ࠢࡵࡩࡹࡻࡲ࡯ࡵࠣ࡟ࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡱࡣࡷ࡬ࡸࡀࠠࡎࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡵࡱࠣࡥࡳࡧ࡬ࡺࡼࡨࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡩ࡯ࡣࡵࡵ࠯ࠤࡪࡧࡣࡩࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡤࠤ࡫ࡵ࡬ࡥࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᾹ")
    if bstack1llllll1ll11_opy_ is None:
        bstack1llllll1ll11_opy_ = [os.getcwd()]
    elif isinstance(bstack1llllll1ll11_opy_, list) and len(bstack1llllll1ll11_opy_) == 0:
        return []
    results = []
    for folder in bstack1llllll1ll11_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1ll11_opy_ (u"ࠤࡉࡳࡱࡪࡥࡳࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢᾺ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1ll11_opy_ (u"ࠥࡴࡷࡏࡤࠣΆ"): bstack1ll11_opy_ (u"ࠦࠧᾼ"),
                bstack1ll11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ᾽"): [],
                bstack1ll11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢι"): [],
                bstack1ll11_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢ᾿"): bstack1ll11_opy_ (u"ࠣࠤ῀"),
                bstack1ll11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡏࡨࡷࡸࡧࡧࡦࡵࠥ῁"): [],
                bstack1ll11_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦῂ"): bstack1ll11_opy_ (u"ࠦࠧῃ"),
                bstack1ll11_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧῄ"): bstack1ll11_opy_ (u"ࠨࠢ῅"),
                bstack1ll11_opy_ (u"ࠢࡱࡴࡕࡥࡼࡊࡩࡧࡨࠥῆ"): bstack1ll11_opy_ (u"ࠣࠤῇ")
            }
            bstack11111l11l1l_opy_ = repo.active_branch.name
            bstack11111ll11l1_opy_ = repo.head.commit
            result[bstack1ll11_opy_ (u"ࠤࡳࡶࡎࡪࠢῈ")] = bstack11111ll11l1_opy_.hexsha
            bstack11111llllll_opy_ = _111111llll1_opy_(repo)
            logger.debug(bstack1ll11_opy_ (u"ࠥࡆࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡨࡲࡶࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯࠼ࠣࠦΈ") + str(bstack11111llllll_opy_) + bstack1ll11_opy_ (u"ࠦࠧῊ"))
            if bstack11111llllll_opy_:
                try:
                    bstack1lllllll1l11_opy_ = repo.git.diff(bstack1ll11_opy_ (u"ࠧ࠳࠭࡯ࡣࡰࡩ࠲ࡵ࡮࡭ࡻࠥΉ"), bstack1ll11l1ll11_opy_ (u"ࠨࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂ࠴࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦῌ")).split(bstack1ll11_opy_ (u"ࠧ࡝ࡰࠪ῍"))
                    logger.debug(bstack1ll11_opy_ (u"ࠣࡅ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡤࡨࡸࡼ࡫ࡥ࡯ࠢࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾࠢࡤࡲࡩࠦࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾ࠼ࠣࠦ῎") + str(bstack1lllllll1l11_opy_) + bstack1ll11_opy_ (u"ࠤࠥ῏"))
                    result[bstack1ll11_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤῐ")] = [f.strip() for f in bstack1lllllll1l11_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll11l1ll11_opy_ (u"ࠦࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀ࠲࠳ࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽࠣῑ")))
                except Exception:
                    logger.debug(bstack1ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡧ࡮ࡤࡪࠣࡧࡴࡳࡰࡢࡴ࡬ࡷࡴࡴ࠮ࠡࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡶࡪࡩࡥ࡯ࡶࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠧῒ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1ll11_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧΐ")] = _11111llll11_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1ll11_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨ῔")] = _11111llll11_opy_(commits[:5])
            bstack1111l11l1ll_opy_ = set()
            bstack1111l111lll_opy_ = []
            for commit in commits:
                logger.debug(bstack1ll11_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯࡬ࡸ࠿ࠦࠢ῕") + str(commit.message) + bstack1ll11_opy_ (u"ࠤࠥῖ"))
                bstack1111l1111l1_opy_ = commit.author.name if commit.author else bstack1ll11_opy_ (u"࡙ࠥࡳࡱ࡮ࡰࡹࡱࠦῗ")
                bstack1111l11l1ll_opy_.add(bstack1111l1111l1_opy_)
                bstack1111l111lll_opy_.append({
                    bstack1ll11_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧῘ"): commit.message.strip(),
                    bstack1ll11_opy_ (u"ࠧࡻࡳࡦࡴࠥῙ"): bstack1111l1111l1_opy_
                })
            result[bstack1ll11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢῚ")] = list(bstack1111l11l1ll_opy_)
            result[bstack1ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡍࡦࡵࡶࡥ࡬࡫ࡳࠣΊ")] = bstack1111l111lll_opy_
            result[bstack1ll11_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣ῜")] = bstack11111ll11l1_opy_.committed_datetime.strftime(bstack1ll11_opy_ (u"ࠤࠨ࡝࠲ࠫ࡭࠮ࠧࡧࠦ῝"))
            if (not result[bstack1ll11_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦ῞")] or result[bstack1ll11_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧ῟")].strip() == bstack1ll11_opy_ (u"ࠧࠨῠ")) and bstack11111ll11l1_opy_.message:
                bstack111111111ll_opy_ = bstack11111ll11l1_opy_.message.strip().splitlines()
                result[bstack1ll11_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢῡ")] = bstack111111111ll_opy_[0] if bstack111111111ll_opy_ else bstack1ll11_opy_ (u"ࠢࠣῢ")
                if len(bstack111111111ll_opy_) > 2:
                    result[bstack1ll11_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣΰ")] = bstack1ll11_opy_ (u"ࠩ࡟ࡲࠬῤ").join(bstack111111111ll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࠪࡩࡳࡱࡪࡥࡳ࠼ࠣࡿࢂ࠯࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤῥ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack11111l1l111_opy_ = [
        result
        for result in results
        if _1llllll1l1ll_opy_(result)
    ]
    return bstack11111l1l111_opy_
def _1llllll1l1ll_opy_(result):
    bstack1ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡍ࡫࡬ࡱࡧࡵࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡩࡧࠢࡤࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡹࡵ࡭ࡶࠣ࡭ࡸࠦࡶࡢ࡮࡬ࡨࠥ࠮࡮ࡰࡰ࠰ࡩࡲࡶࡴࡺࠢࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠡࡣࡱࡨࠥࡧࡵࡵࡪࡲࡶࡸ࠯࠮ࠋࠢࠣࠤࠥࠨࠢࠣῦ")
    return (
        isinstance(result.get(bstack1ll11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦῧ"), None), list)
        and len(result[bstack1ll11_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧῨ")]) > 0
        and isinstance(result.get(bstack1ll11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣῩ"), None), list)
        and len(result[bstack1ll11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤῪ")]) > 0
    )
def _111111llll1_opy_(repo):
    bstack1ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡗࡶࡾࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡨࡦࠢࡥࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡳࡧࡳࡳࠥࡽࡩࡵࡪࡲࡹࡹࠦࡨࡢࡴࡧࡧࡴࡪࡥࡥࠢࡱࡥࡲ࡫ࡳࠡࡣࡱࡨࠥࡽ࡯ࡳ࡭ࠣࡻ࡮ࡺࡨࠡࡣ࡯ࡰࠥ࡜ࡃࡔࠢࡳࡶࡴࡼࡩࡥࡧࡵࡷ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡥࡶࡦࡴࡣࡩࠢ࡬ࡪࠥࡶ࡯ࡴࡵ࡬ࡦࡱ࡫ࠬࠡࡧ࡯ࡷࡪࠦࡎࡰࡰࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧΎ")
    try:
        try:
            origin = repo.remotes.origin
            bstack11111ll1lll_opy_ = origin.refs[bstack1ll11_opy_ (u"ࠪࡌࡊࡇࡄࠨῬ")]
            target = bstack11111ll1lll_opy_.reference.name
            if target.startswith(bstack1ll11_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬ῭")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1ll11_opy_ (u"ࠬࡵࡲࡪࡩ࡬ࡲ࠴࠭΅")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _11111llll11_opy_(commits):
    bstack1ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ`")
    bstack1lllllll1l11_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11111l1ll11_opy_ in diff:
                        if bstack11111l1ll11_opy_.a_path:
                            bstack1lllllll1l11_opy_.add(bstack11111l1ll11_opy_.a_path)
                        if bstack11111l1ll11_opy_.b_path:
                            bstack1lllllll1l11_opy_.add(bstack11111l1ll11_opy_.b_path)
    except Exception:
        pass
    return list(bstack1lllllll1l11_opy_)
def bstack11111l11111_opy_(bstack11111111111_opy_):
    bstack1111l1lll1l_opy_ = bstack11111111l1l_opy_(bstack11111111111_opy_)
    if bstack1111l1lll1l_opy_ and bstack1111l1lll1l_opy_ > bstack111l111llll_opy_:
        bstack1111l11ll11_opy_ = bstack1111l1lll1l_opy_ - bstack111l111llll_opy_
        bstack1111l1ll111_opy_ = bstack1lllllllll1l_opy_(bstack11111111111_opy_[bstack1ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ῰")], bstack1111l11ll11_opy_)
        bstack11111111111_opy_[bstack1ll11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ῱")] = bstack1111l1ll111_opy_
        logger.info(bstack1ll11_opy_ (u"ࠤࡗ࡬ࡪࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡨࡢࡵࠣࡦࡪ࡫࡮ࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧ࠲࡙ࠥࡩࡻࡧࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡡࡧࡶࡨࡶࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥࢁࡽࠡࡍࡅࠦῲ")
                    .format(bstack11111111l1l_opy_(bstack11111111111_opy_) / 1024))
    return bstack11111111111_opy_
def bstack11111111l1l_opy_(json_data):
    try:
        if json_data:
            bstack1lllllll111l_opy_ = json.dumps(json_data)
            bstack111111ll11l_opy_ = sys.getsizeof(bstack1lllllll111l_opy_)
            return bstack111111ll11l_opy_
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡦࡥࡱࡩࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡌࡖࡓࡓࠦ࡯ࡣ࡬ࡨࡧࡹࡀࠠࡼࡿࠥῳ").format(e))
    return -1
def bstack1lllllllll1l_opy_(field, bstack1lllllll1ll1_opy_):
    try:
        bstack1111111111l_opy_ = len(bytes(bstack111l111lll1_opy_, bstack1ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪῴ")))
        bstack11111lll11l_opy_ = bytes(field, bstack1ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ῵"))
        bstack11111111ll1_opy_ = len(bstack11111lll11l_opy_)
        bstack11111llll1l_opy_ = ceil(bstack11111111ll1_opy_ - bstack1lllllll1ll1_opy_ - bstack1111111111l_opy_)
        if bstack11111llll1l_opy_ > 0:
            bstack11111111lll_opy_ = bstack11111lll11l_opy_[:bstack11111llll1l_opy_].decode(bstack1ll11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬῶ"), errors=bstack1ll11_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࠧῷ")) + bstack111l111lll1_opy_
            return bstack11111111lll_opy_
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡴࡳࡷࡱࡧࡦࡺࡩ࡯ࡩࠣࡪ࡮࡫࡬ࡥ࠮ࠣࡲࡴࡺࡨࡪࡰࡪࠤࡼࡧࡳࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧࠤ࡭࡫ࡲࡦ࠼ࠣࡿࢂࠨῸ").format(e))
    return field
def bstack11ll11l1l1_opy_():
    env = os.environ
    if (bstack1ll11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢΌ") in env and len(env[bstack1ll11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣῺ")]) > 0) or (
            bstack1ll11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥΏ") in env and len(env[bstack1ll11_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦῼ")]) > 0):
        return {
            bstack1ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ´"): bstack1ll11_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣ῾"),
            bstack1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ῿"): env.get(bstack1ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ ")),
            bstack1ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ "): env.get(bstack1ll11_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨ ")),
            bstack1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ "): env.get(bstack1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ "))
        }
    if env.get(bstack1ll11_opy_ (u"ࠢࡄࡋࠥ ")) == bstack1ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ ") and bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦ "))):
        return {
            bstack1ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ "): bstack1ll11_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨ "),
            bstack1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ "): env.get(bstack1ll11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ​")),
            bstack1ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ‌"): env.get(bstack1ll11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧ‍")),
            bstack1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ‎"): env.get(bstack1ll11_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨ‏"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠦࡈࡏࠢ‐")) == bstack1ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ‑") and bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨ‒"))):
        return {
            bstack1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ–"): bstack1ll11_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦ—"),
            bstack1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ―"): env.get(bstack1ll11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥ‖")),
            bstack1ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ‗"): env.get(bstack1ll11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ‘")),
            bstack1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ’"): env.get(bstack1ll11_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ‚"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠣࡅࡌࠦ‛")) == bstack1ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ“") and env.get(bstack1ll11_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦ”")) == bstack1ll11_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨ„"):
        return {
            bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ‟"): bstack1ll11_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣ†"),
            bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ‡"): None,
            bstack1ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ•"): None,
            bstack1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ‣"): None
        }
    if env.get(bstack1ll11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨ․")) and env.get(bstack1ll11_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢ‥")):
        return {
            bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ…"): bstack1ll11_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤ‧"),
            bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ "): env.get(bstack1ll11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨ ")),
            bstack1ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ‪"): None,
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ‫"): env.get(bstack1ll11_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ‬"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠧࡉࡉࠣ‭")) == bstack1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ‮") and bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨ "))):
        return {
            bstack1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ‰"): bstack1ll11_opy_ (u"ࠤࡇࡶࡴࡴࡥࠣ‱"),
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ′"): env.get(bstack1ll11_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢ″")),
            bstack1ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ‴"): None,
            bstack1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ‵"): env.get(bstack1ll11_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ‶"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠣࡅࡌࠦ‷")) == bstack1ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ‸") and bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨ‹"))):
        return {
            bstack1ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ›"): bstack1ll11_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣ※"),
            bstack1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ‼"): env.get(bstack1ll11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨ‽")),
            bstack1ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ‾"): env.get(bstack1ll11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ‿")),
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⁀"): env.get(bstack1ll11_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ⁁"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠧࡉࡉࠣ⁂")) == bstack1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ⁃") and bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥ⁄"))):
        return {
            bstack1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ⁅"): bstack1ll11_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤ⁆"),
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⁇"): env.get(bstack1ll11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣ⁈")),
            bstack1ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⁉"): env.get(bstack1ll11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ⁊")),
            bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⁋"): env.get(bstack1ll11_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦ⁌"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠤࡆࡍࠧ⁍")) == bstack1ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣ⁎") and bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢ⁏"))):
        return {
            bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⁐"): bstack1ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤ⁑"),
            bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⁒"): env.get(bstack1ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ⁓")),
            bstack1ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⁔"): env.get(bstack1ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧ⁕")) or env.get(bstack1ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ⁖")),
            bstack1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⁗"): env.get(bstack1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ⁘"))
        }
    if bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤ⁙"))):
        return {
            bstack1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ⁚"): bstack1ll11_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤ⁛"),
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⁜"): bstack1ll11_opy_ (u"ࠦࢀࢃࡻࡾࠤ⁝").format(env.get(bstack1ll11_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨ⁞")), env.get(bstack1ll11_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭ "))),
            bstack1ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⁠"): env.get(bstack1ll11_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊࠢ⁡")),
            bstack1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⁢"): env.get(bstack1ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ⁣"))
        }
    if bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨ⁤"))):
        return {
            bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⁥"): bstack1ll11_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲࠣ⁦"),
            bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⁧"): bstack1ll11_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠢ⁨").format(env.get(bstack1ll11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨ⁩")), env.get(bstack1ll11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫ⁪")), env.get(bstack1ll11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬ⁫")), env.get(bstack1ll11_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ⁬"))),
            bstack1ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⁭"): env.get(bstack1ll11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ⁮")),
            bstack1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⁯"): env.get(bstack1ll11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ⁰"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦⁱ")) and env.get(bstack1ll11_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ⁲")):
        return {
            bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⁳"): bstack1ll11_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉࠣ⁴"),
            bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⁵"): bstack1ll11_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦ⁶").format(env.get(bstack1ll11_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬ⁷")), env.get(bstack1ll11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨ⁸")), env.get(bstack1ll11_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫ⁹"))),
            bstack1ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⁺"): env.get(bstack1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ⁻")),
            bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⁼"): env.get(bstack1ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣ⁽"))
        }
    if any([env.get(bstack1ll11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ⁾")), env.get(bstack1ll11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤⁿ")), env.get(bstack1ll11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣ₀"))]):
        return {
            bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ₁"): bstack1ll11_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨ₂"),
            bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ₃"): env.get(bstack1ll11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ₄")),
            bstack1ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ₅"): env.get(bstack1ll11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ₆")),
            bstack1ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ₇"): env.get(bstack1ll11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ₈"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ₉")):
        return {
            bstack1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ₊"): bstack1ll11_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯ࠣ₋"),
            bstack1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ₌"): env.get(bstack1ll11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧ₍")),
            bstack1ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ₎"): env.get(bstack1ll11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦ₏")),
            bstack1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧₐ"): env.get(bstack1ll11_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧₑ"))
        }
    if env.get(bstack1ll11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤₒ")) or env.get(bstack1ll11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦₓ")):
        return {
            bstack1ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣₔ"): bstack1ll11_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶࠧₕ"),
            bstack1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣₖ"): env.get(bstack1ll11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥₗ")),
            bstack1ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤₘ"): bstack1ll11_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣₙ") if env.get(bstack1ll11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦₚ")) else None,
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤₛ"): env.get(bstack1ll11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤₜ"))
        }
    if any([env.get(bstack1ll11_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥ₝")), env.get(bstack1ll11_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ₞")), env.get(bstack1ll11_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ₟"))]):
        return {
            bstack1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ₠"): bstack1ll11_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣ₡"),
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ₢"): None,
            bstack1ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ₣"): env.get(bstack1ll11_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤ₤")),
            bstack1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ₥"): env.get(bstack1ll11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ₦"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦ₧")):
        return {
            bstack1ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ₨"): bstack1ll11_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨ₩"),
            bstack1ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ₪"): env.get(bstack1ll11_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ₫")),
            bstack1ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ€"): bstack1ll11_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣ₭").format(env.get(bstack1ll11_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫ₮"))) if env.get(bstack1ll11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧ₯")) else None,
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ₰"): env.get(bstack1ll11_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ₱"))
        }
    if bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨ₲"))):
        return {
            bstack1ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ₳"): bstack1ll11_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹࠣ₴"),
            bstack1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ₵"): env.get(bstack1ll11_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨ₶")),
            bstack1ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ₷"): env.get(bstack1ll11_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢ₸")),
            bstack1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ₹"): env.get(bstack1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ₺"))
        }
    if bstack1lll1111ll_opy_(env.get(bstack1ll11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣ₻"))):
        return {
            bstack1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ₼"): bstack1ll11_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥ₽"),
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ₾"): bstack1ll11_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧ₿").format(env.get(bstack1ll11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩ⃀")), env.get(bstack1ll11_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪ⃁")), env.get(bstack1ll11_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧ⃂"))),
            bstack1ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⃃"): env.get(bstack1ll11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦ⃄")),
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⃅"): env.get(bstack1ll11_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦ⃆"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠧࡉࡉࠣ⃇")) == bstack1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ⃈") and env.get(bstack1ll11_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢ⃉")) == bstack1ll11_opy_ (u"ࠣ࠳ࠥ⃊"):
        return {
            bstack1ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⃋"): bstack1ll11_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥ⃌"),
            bstack1ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⃍"): bstack1ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣ⃎").format(env.get(bstack1ll11_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎࠪ⃏"))),
            bstack1ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⃐"): None,
            bstack1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⃑"): None,
        }
    if env.get(bstack1ll11_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒ⃒ࠧ")):
        return {
            bstack1ll11_opy_ (u"ࠥࡲࡦࡳࡥ⃓ࠣ"): bstack1ll11_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨ⃔"),
            bstack1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⃕"): None,
            bstack1ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⃖"): env.get(bstack1ll11_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣ⃗")),
            bstack1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸ⃘ࠢ"): env.get(bstack1ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒ⃙ࠣ"))
        }
    if any([env.get(bstack1ll11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨ⃚")), env.get(bstack1ll11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦ⃛")), env.get(bstack1ll11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥ⃜")), env.get(bstack1ll11_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓࠢ⃝"))]):
        return {
            bstack1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⃞"): bstack1ll11_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦ⃟"),
            bstack1ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⃠"): None,
            bstack1ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⃡"): env.get(bstack1ll11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ⃢")) or None,
            bstack1ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⃣"): env.get(bstack1ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ⃤"), 0)
        }
    if env.get(bstack1ll11_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉ⃥ࠧ")):
        return {
            bstack1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ⃦"): bstack1ll11_opy_ (u"ࠤࡊࡳࡈࡊࠢ⃧"),
            bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⃨"): None,
            bstack1ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⃩"): env.get(bstack1ll11_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇ⃪ࠥ")),
            bstack1ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ⃫ࠧ"): env.get(bstack1ll11_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨ⃬"))
        }
    if env.get(bstack1ll11_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⃭")):
        return {
            bstack1ll11_opy_ (u"ࠤࡱࡥࡲ࡫⃮ࠢ"): bstack1ll11_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨ⃯"),
            bstack1ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⃰"): env.get(bstack1ll11_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ⃱")),
            bstack1ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⃲"): env.get(bstack1ll11_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥ⃳")),
            bstack1ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⃴"): env.get(bstack1ll11_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ⃵"))
        }
    return {bstack1ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⃶"): None}
def get_host_info():
    return {
        bstack1ll11_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨ⃷"): platform.node(),
        bstack1ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ⃸"): platform.system(),
        bstack1ll11_opy_ (u"ࠨࡴࡺࡲࡨࠦ⃹"): platform.machine(),
        bstack1ll11_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ⃺"): platform.version(),
        bstack1ll11_opy_ (u"ࠣࡣࡵࡧ࡭ࠨ⃻"): platform.architecture()[0]
    }
def bstack1l1111111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111111lll11_opy_():
    if global_config.get_property(bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ⃼")):
        return bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⃽")
    return bstack1ll11_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪ⃾")
def bstack1111l1l1ll1_opy_(driver):
    info = {
        bstack1ll11_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ⃿"): driver.capabilities,
        bstack1ll11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ℀"): driver.session_id,
        bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ℁"): driver.capabilities.get(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ℂ"), None),
        bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ℃"): driver.capabilities.get(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ℄"), None),
        bstack1ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭℅"): driver.capabilities.get(bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ℆"), None),
        bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩℇ"):driver.capabilities.get(bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ℈"), None),
    }
    if bstack111111lll11_opy_() == bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ℉"):
        if bstack1l11l11l11_opy_():
            info[bstack1ll11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪℊ")] = bstack1ll11_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩℋ")
        elif driver.capabilities.get(bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬℌ"), {}).get(bstack1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩℍ"), False):
            info[bstack1ll11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧℎ")] = bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫℏ")
        else:
            info[bstack1ll11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩℐ")] = bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫℑ")
    return info
def bstack1l11l11l11_opy_():
    if global_config.get_property(bstack1ll11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩℒ")):
        return True
    if bstack1lll1111ll_opy_(os.environ.get(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬℓ"), None)):
        return True
    return False
def bstack1111l1lllll_opy_(bstack1lllllll1l1l_opy_, url, response, headers=None, data=None):
    bstack1ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡈࡵࡪ࡮ࡧࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࠥࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠯ࡳࡧࡶࡴࡴࡴࡳࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡴࡹࡪࡹࡴࡠࡶࡼࡴࡪࡀࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨࠥ࠮ࡇࡆࡖ࠯ࠤࡕࡕࡓࡕ࠮ࠣࡩࡹࡩ࠮ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࡹࡷࡲ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡘࡖࡑ࠵ࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡰࡤ࡭ࡩࡨࡺࠠࡧࡴࡲࡱࠥࡸࡥࡲࡷࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࡪࡨࡥࡩ࡫ࡲࡴ࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡭࡫ࡡࡥࡧࡵࡷࠥࡵࡲࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥࡣࡷࡥ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡋࡕࡒࡒࠥࡪࡡࡵࡣࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡊࡴࡸ࡭ࡢࡶࡷࡩࡩࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨࠤࡼ࡯ࡴࡩࠢࡵࡩࡶࡻࡥࡴࡶࠣࡥࡳࡪࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡧࡥࡹࡧࠊࠡࠢࠣࠤࠧࠨࠢ℔")
    bstack11111lll111_opy_ = {
        bstack1ll11_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢℕ"): headers,
        bstack1ll11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ№"): bstack1lllllll1l1l_opy_.upper(),
        bstack1ll11_opy_ (u"ࠣࡣࡪࡩࡳࡺࠢ℗"): None,
        bstack1ll11_opy_ (u"ࠤࡨࡲࡩࡶ࡯ࡪࡰࡷࠦ℘"): url,
        bstack1ll11_opy_ (u"ࠥ࡮ࡸࡵ࡮ࠣℙ"): data
    }
    try:
        bstack1llllllll1l1_opy_ = response.json()
        if isinstance(bstack1llllllll1l1_opy_, dict) and bstack1llllllll1l1_opy_.get(bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫℚ"), {}).get(bstack1ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ℛ"), {}).get(bstack1ll11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧℜ")):
            bstack1111l1l1lll_opy_ = json.loads(json.dumps(bstack1llllllll1l1_opy_))
            bstack1111l1l1lll_opy_[bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧℝ")][bstack1ll11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ℞")][bstack1ll11_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ℟")] = bstack1ll11_opy_ (u"ࠥ࡟ࡷ࡫ࡤࡢࡥࡷࡩࡩࠦࡦࡰࡴࠣࡦࡷ࡫ࡶࡪࡶࡼࡡࠧ℠")
            bstack1llllllll1l1_opy_ = bstack1111l1l1lll_opy_
    except Exception:
        bstack1llllllll1l1_opy_ = response.text
    bstack1111111l1ll_opy_ = {
        bstack1ll11_opy_ (u"ࠦࡧࡵࡤࡺࠤ℡"): bstack1llllllll1l1_opy_,
        bstack1ll11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࡈࡵࡤࡦࠤ™"): response.status_code
    }
    return {
        bstack1ll11_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢ℣"): bstack11111lll111_opy_,
        bstack1ll11_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤℤ"): bstack1111111l1ll_opy_
    }
def bstack1ll11l111l_opy_(bstack1lllllll1l1l_opy_, url, data, config):
    headers = config.get(bstack1ll11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ℥"), None)
    proxies = bstack11lllll1l_opy_(config, url)
    auth = config.get(bstack1ll11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧΩ"), None)
    response = requests.request(
            bstack1lllllll1l1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1111l1lllll_opy_(bstack1lllllll1l1l_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1ll11_opy_ (u"ࠪ࠰ࠬ℧"), bstack1ll11_opy_ (u"ࠫ࠿࠭ℨ"))))
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡰࡴ࡭ࡧࡪࡰࡪࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵ࠼ࠣࡿࢂࠨ℩").format(e))
    return response
def bstack1l1ll11l11_opy_(bstack1111111ll_opy_, size):
    bstack1l111lll1_opy_ = []
    while len(bstack1111111ll_opy_) > size:
        bstack111l111111_opy_ = bstack1111111ll_opy_[:size]
        bstack1l111lll1_opy_.append(bstack111l111111_opy_)
        bstack1111111ll_opy_ = bstack1111111ll_opy_[size:]
    bstack1l111lll1_opy_.append(bstack1111111ll_opy_)
    return bstack1l111lll1_opy_
def bstack111111l1111_opy_(message, bstack1llllll1lll1_opy_=False):
    os.write(1, bytes(message, bstack1ll11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬK")))
    os.write(1, bytes(bstack1ll11_opy_ (u"ࠧ࡝ࡰࠪÅ"), bstack1ll11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧℬ")))
    if bstack1llllll1lll1_opy_:
        with open(bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨℭ") + os.environ[bstack1ll11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ℮")] + bstack1ll11_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩℯ"), bstack1ll11_opy_ (u"ࠬࡧࠧℰ")) as f:
            f.write(message + bstack1ll11_opy_ (u"࠭࡜࡯ࠩℱ"))
def bstack1l111l1111_opy_():
    return os.environ[bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪℲ")].lower() == bstack1ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ℳ")
def current_time():
    return bstack1lll1ll1ll1_opy_().replace(tzinfo=None).isoformat() + bstack1ll11_opy_ (u"ࠩ࡝ࠫℴ")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll11_opy_ (u"ࠪ࡞ࠬℵ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll11_opy_ (u"ࠫ࡟࠭ℶ")))).total_seconds() * 1000
def bstack1lllllll1111_opy_(timestamp):
    return bstack11111ll1ll1_opy_(timestamp).isoformat() + bstack1ll11_opy_ (u"ࠬࡠࠧℷ")
def bstack1lllllll1lll_opy_(bstack11111l11ll1_opy_):
    date_format = bstack1ll11_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫℸ")
    bstack1111l1llll1_opy_ = datetime.datetime.strptime(bstack11111l11ll1_opy_, date_format)
    return bstack1111l1llll1_opy_.isoformat() + bstack1ll11_opy_ (u"࡛ࠧࠩℹ")
def bstack111111lllll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ℺")
    else:
        return bstack1ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ℻")
def bstack1lll1111ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨℼ")
def bstack1111l111111_opy_(val):
    return val.__str__().lower() == bstack1ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪℽ")
def error_handler(bstack111111111l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111111111l1_opy_ as e:
                print(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧℾ").format(func.__name__, bstack111111111l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1111l1111ll_opy_(bstack1111l111ll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1111l111ll1_opy_(cls, *args, **kwargs)
            except bstack111111111l1_opy_ as e:
                print(bstack1ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨℿ").format(bstack1111l111ll1_opy_.__name__, bstack111111111l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1111l1111ll_opy_
    else:
        return decorator
def bstack1ll11l1l11_opy_(bstack1lllllll11l_opy_):
    if os.getenv(bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ⅀")) is not None:
        return bstack1lll1111ll_opy_(os.getenv(bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ⅁")))
    if bstack1ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⅂") in bstack1lllllll11l_opy_ and bstack1111l111111_opy_(bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⅃")]):
        return False
    if bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⅄") in bstack1lllllll11l_opy_ and bstack1111l111111_opy_(bstack1lllllll11l_opy_[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧⅅ")]):
        return False
    return True
def bstack1111l1111l_opy_():
    try:
        from pytest_bdd import reporting
        bstack1111ll111l1_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨⅆ"), None)
        return bstack1111ll111l1_opy_ is None or bstack1111ll111l1_opy_ == bstack1ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦⅇ")
    except Exception as e:
        return False
def bstack1l111llll1_opy_(hub_url, CONFIG):
    if bstack1lll11llll_opy_() <= version.parse(bstack1ll11_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨⅈ")):
        if hub_url:
            return bstack1ll11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥⅉ") + hub_url + bstack1ll11_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ⅊")
        return bstack111l111ll_opy_
    if hub_url:
        return bstack1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ⅋") + hub_url + bstack1ll11_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ⅌")
    return HTTPS_HUB
def bstack1lllllll11ll_opy_():
    return isinstance(os.getenv(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ⅍")), str)
def bstack11lllll11_opy_(url):
    return urlparse(url).hostname
def bstack1ll1l111ll_opy_(hostname):
    for bstack11llll1l1_opy_ in bstack1111ll1lll_opy_:
        regex = re.compile(bstack11llll1l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1llllllll1ll_opy_(bstack1111l11l111_opy_, file_name, logger):
    bstack1lll111l11_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠧࡿࠩⅎ")), bstack1111l11l111_opy_)
    try:
        if not os.path.exists(bstack1lll111l11_opy_):
            os.makedirs(bstack1lll111l11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠨࢀࠪ⅏")), bstack1111l11l111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll11_opy_ (u"ࠩࡺࠫ⅐")):
                pass
            with open(file_path, bstack1ll11_opy_ (u"ࠥࡻ࠰ࠨ⅑")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1ll111_opy_.format(str(e)))
def bstack1llllll1llll_opy_(file_name, key, value, logger):
    file_path = bstack1llllllll1ll_opy_(bstack1ll11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⅒"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1l1lll_opy_ = json.load(open(file_path, bstack1ll11_opy_ (u"ࠬࡸࡢࠨ⅓")))
        else:
            bstack1l1l1lll_opy_ = {}
        bstack1l1l1lll_opy_[key] = value
        with open(file_path, bstack1ll11_opy_ (u"ࠨࡷࠬࠤ⅔")) as outfile:
            json.dump(bstack1l1l1lll_opy_, outfile)
def bstack11lll1llll_opy_(file_name, logger):
    file_path = bstack1llllllll1ll_opy_(bstack1ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⅕"), file_name, logger)
    bstack1l1l1lll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll11_opy_ (u"ࠨࡴࠪ⅖")) as bstack1l1ll11l1_opy_:
            bstack1l1l1lll_opy_ = json.load(bstack1l1ll11l1_opy_)
    return bstack1l1l1lll_opy_
def bstack11ll11llll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨ࠾ࠥ࠭⅗") + file_path + bstack1ll11_opy_ (u"ࠪࠤࠬ⅘") + str(e))
def bstack1lll11llll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll11_opy_ (u"ࠦࡁࡔࡏࡕࡕࡈࡘࡃࠨ⅙")
def bstack11l11l1l1l_opy_(config):
    if bstack1ll11_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ⅚") in config:
        del (config[bstack1ll11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ⅛")])
        return False
    if bstack1lll11llll_opy_() < version.parse(bstack1ll11_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭⅜")):
        return False
    if bstack1lll11llll_opy_() >= version.parse(bstack1ll11_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧ⅝")):
        return True
    if bstack1ll11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ⅞") in config and config[bstack1ll11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ⅟")] is False:
        return False
    else:
        return True
def bstack1ll1l111l1_opy_(args_list, bstack1111l1ll11l_opy_):
    index = -1
    for value in bstack1111l1ll11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack111ll1lll11_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack111ll1lll11_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1lllll11l1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫⅠ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬⅡ"), exception=exception)
    def bstack1ll1lll111l_opy_(self):
        if self.result != bstack1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ⅲ"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥⅣ") in self.exception_type:
            return bstack1ll11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤⅤ")
        return bstack1ll11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥⅥ")
    def bstack1111l11llll_opy_(self):
        if self.result != bstack1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪⅦ"):
            return None
        if self.bstack1lllll11l1l_opy_:
            return self.bstack1lllll11l1l_opy_
        return bstack11111l1llll_opy_(self.exception)
def bstack11111l1llll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111111l11l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1111l111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lllllllll1_opy_(config, logger):
    try:
        import playwright
        bstack111111ll1l1_opy_ = playwright.__file__
        bstack1111111l11l_opy_ = os.path.split(bstack111111ll1l1_opy_)
        bstack111111l1l11_opy_ = bstack1111111l11l_opy_[0] + bstack1ll11_opy_ (u"ࠫ࠴ࡪࡲࡪࡸࡨࡶ࠴ࡶࡡࡤ࡭ࡤ࡫ࡪ࠵࡬ࡪࡤ࠲ࡧࡱ࡯࠯ࡤ࡮࡬࠲࡯ࡹࠧⅧ")
        os.environ[bstack1ll11_opy_ (u"ࠬࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠨⅨ")] = bstack11l11lll1_opy_(config)
        with open(bstack111111l1l11_opy_, bstack1ll11_opy_ (u"࠭ࡲࠨⅩ")) as f:
            file_content = f.read()
            bstack1lllllllll11_opy_ = bstack1ll11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭Ⅺ")
            bstack11111l1111l_opy_ = file_content.find(bstack1lllllllll11_opy_)
            if bstack11111l1111l_opy_ == -1:
              process = subprocess.Popen(bstack1ll11_opy_ (u"ࠣࡰࡳࡱࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠧⅫ"), shell=True, cwd=bstack1111111l11l_opy_[0])
              process.wait()
              bstack1111ll1111l_opy_ = bstack1ll11_opy_ (u"ࠩࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺࠢ࠼ࠩⅬ")
              bstack1111l1l11l1_opy_ = bstack1ll11_opy_ (u"ࠥࠦࠧࠦ࡜ࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࡡࠨ࠻ࠡࡥࡲࡲࡸࡺࠠࡼࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴࠥࢃࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ࠭ࡀࠦࡩࡧࠢࠫࡴࡷࡵࡣࡦࡵࡶ࠲ࡪࡴࡶ࠯ࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜࠭ࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠩࠫ࠾ࠤࠧࠨࠢⅭ")
              bstack1111111llll_opy_ = file_content.replace(bstack1111ll1111l_opy_, bstack1111l1l11l1_opy_)
              with open(bstack111111l1l11_opy_, bstack1ll11_opy_ (u"ࠫࡼ࠭Ⅾ")) as f:
                f.write(bstack1111111llll_opy_)
    except Exception as e:
        logger.error(bstack1lll11l1l1_opy_.format(str(e)))
def bstack1l11ll1ll_opy_():
  try:
    bstack11111ll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬⅯ"))
    bstack1111111lll1_opy_ = []
    if os.path.exists(bstack11111ll111l_opy_):
      with open(bstack11111ll111l_opy_) as f:
        bstack1111111lll1_opy_ = json.load(f)
      os.remove(bstack11111ll111l_opy_)
    return bstack1111111lll1_opy_
  except:
    pass
  return []
def bstack11llll11_opy_(bstack11lll1ll11_opy_):
  try:
    bstack1111111lll1_opy_ = []
    bstack11111ll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ⅰ"))
    if os.path.exists(bstack11111ll111l_opy_):
      with open(bstack11111ll111l_opy_) as f:
        bstack1111111lll1_opy_ = json.load(f)
    bstack1111111lll1_opy_.append(bstack11lll1ll11_opy_)
    with open(bstack11111ll111l_opy_, bstack1ll11_opy_ (u"ࠧࡸࠩⅱ")) as f:
        json.dump(bstack1111111lll1_opy_, f)
  except:
    pass
def bstack1ll111ll1_opy_(logger, bstack1111l1l1111_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫⅲ"), bstack1ll11_opy_ (u"ࠩࠪⅳ"))
    if test_name == bstack1ll11_opy_ (u"ࠪࠫⅴ"):
        test_name = threading.current_thread().__dict__.get(bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡆࡩࡪ࡟ࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠪⅵ"), bstack1ll11_opy_ (u"ࠬ࠭ⅶ"))
    bstack1111l1l11ll_opy_ = bstack1ll11_opy_ (u"࠭ࠬࠡࠩⅷ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111l1l1111_opy_:
        bstack11111lll1_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧⅸ"), bstack1ll11_opy_ (u"ࠨ࠲ࠪⅹ"))
        bstack1l1l1lll11_opy_ = {bstack1ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧⅺ"): test_name, bstack1ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩⅻ"): bstack1111l1l11ll_opy_, bstack1ll11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪⅼ"): bstack11111lll1_opy_}
        bstack111111l1lll_opy_ = []
        bstack1111111l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫⅽ"))
        if os.path.exists(bstack1111111l1l1_opy_):
            with open(bstack1111111l1l1_opy_) as f:
                bstack111111l1lll_opy_ = json.load(f)
        bstack111111l1lll_opy_.append(bstack1l1l1lll11_opy_)
        with open(bstack1111111l1l1_opy_, bstack1ll11_opy_ (u"࠭ࡷࠨⅾ")) as f:
            json.dump(bstack111111l1lll_opy_, f)
    else:
        bstack1l1l1lll11_opy_ = {bstack1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬⅿ"): test_name, bstack1ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧↀ"): bstack1111l1l11ll_opy_, bstack1ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨↁ"): str(multiprocessing.current_process().name)}
        if bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧↂ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l1lll11_opy_)
  except Exception as e:
      logger.warn(bstack1ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡰࡺࡶࡨࡷࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣↃ").format(e))
def bstack1l1ll11l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨↄ"))
    try:
      bstack11111lll1ll_opy_ = []
      bstack1l1l1lll11_opy_ = {bstack1ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫↅ"): test_name, bstack1ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ↆ"): error_message, bstack1ll11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧↇ"): index}
      bstack11111l1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪↈ"))
      if os.path.exists(bstack11111l1l11l_opy_):
          with open(bstack11111l1l11l_opy_) as f:
              bstack11111lll1ll_opy_ = json.load(f)
      bstack11111lll1ll_opy_.append(bstack1l1l1lll11_opy_)
      with open(bstack11111l1l11l_opy_, bstack1ll11_opy_ (u"ࠪࡻࠬ↉")) as f:
          json.dump(bstack11111lll1ll_opy_, f)
    except Exception as e:
      logger.warn(bstack1ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ↊").format(e))
    return
  bstack11111lll1ll_opy_ = []
  bstack1l1l1lll11_opy_ = {bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ↋"): test_name, bstack1ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ↌"): error_message, bstack1ll11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭↍"): index}
  bstack11111l1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ↎"))
  lock_file = bstack11111l1l11l_opy_ + bstack1ll11_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨ↏")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11111l1l11l_opy_):
          with open(bstack11111l1l11l_opy_, bstack1ll11_opy_ (u"ࠪࡶࠬ←")) as f:
              content = f.read().strip()
              if content:
                  bstack11111lll1ll_opy_ = json.load(open(bstack11111l1l11l_opy_))
      bstack11111lll1ll_opy_.append(bstack1l1l1lll11_opy_)
      with open(bstack11111l1l11l_opy_, bstack1ll11_opy_ (u"ࠫࡼ࠭↑")) as f:
          json.dump(bstack11111lll1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧ࠻ࠢࡾࢁࠧ→").format(e))
def bstack111111l11_opy_(bstack1111111l1l_opy_, name, logger):
  try:
    bstack1l1l1lll11_opy_ = {bstack1ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ↓"): name, bstack1ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭↔"): bstack1111111l1l_opy_, bstack1ll11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ↕"): str(threading.current_thread()._name)}
    return bstack1l1l1lll11_opy_
  except Exception as e:
    logger.warn(bstack1ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ↖").format(e))
  return
def bstack1111l11l1l1_opy_():
    return platform.system() == bstack1ll11_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫ↗")
def bstack11111l11ll_opy_(bstack11111l1l1l1_opy_, config, logger):
    bstack1111l1lll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11111l1l1l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ↘").format(e))
    return bstack1111l1lll11_opy_
def bstack1111l1l111l_opy_(bstack1111111ll1l_opy_, bstack1111111l111_opy_):
    bstack1111l1ll1l1_opy_ = version.parse(bstack1111111ll1l_opy_)
    bstack1111l1l1l11_opy_ = version.parse(bstack1111111l111_opy_)
    if bstack1111l1ll1l1_opy_ > bstack1111l1l1l11_opy_:
        return 1
    elif bstack1111l1ll1l1_opy_ < bstack1111l1l1l11_opy_:
        return -1
    else:
        return 0
def bstack1lll1ll1ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11111ll1ll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1llllllllll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll1l11_opy_(options, framework, config, bstack1ll1lll11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll11_opy_ (u"ࠬ࡭ࡥࡵࠩ↙"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1llll11ll1_opy_ = caps.get(bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ↚"))
    bstack1111l11ll1l_opy_ = True
    bstack1l11l1l1_opy_ = os.environ[bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ↛")]
    bstack1l1l1111l1l_opy_ = config.get(bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ↜"), False)
    if bstack1l1l1111l1l_opy_:
        bstack1ll1111l1l1_opy_ = config.get(bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ↝"), {})
        bstack1ll1111l1l1_opy_[bstack1ll11_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭↞")] = os.getenv(bstack1ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ↟"))
        bstack111lllll_opy_ = json.loads(os.getenv(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭↠"), bstack1ll11_opy_ (u"࠭ࡻࡾࠩ↡"))).get(bstack1ll11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ↢"))
    if bstack1111l111111_opy_(caps.get(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧ↣"))) or bstack1111l111111_opy_(caps.get(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩ↤"))):
        bstack1111l11ll1l_opy_ = False
    if bstack11l11l1l1l_opy_({bstack1ll11_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ↥"): bstack1111l11ll1l_opy_}):
        bstack1llll11ll1_opy_ = bstack1llll11ll1_opy_ or {}
        bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭↦")] = bstack1llllllllll1_opy_(framework)
        bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ↧")] = bstack1l111l1111_opy_()
        bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ↨")] = bstack1l11l1l1_opy_
        bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩ↩")] = bstack1ll1lll11_opy_
        if bstack1l1l1111l1l_opy_:
            bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ↪")] = bstack1l1l1111l1l_opy_
            bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ↫")] = bstack1ll1111l1l1_opy_
            bstack1llll11ll1_opy_[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ↬")][bstack1ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ↭")] = bstack111lllll_opy_
        if getattr(options, bstack1ll11_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭↮"), None):
            options.set_capability(bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ↯"), bstack1llll11ll1_opy_)
        else:
            options[bstack1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ↰")] = bstack1llll11ll1_opy_
    else:
        if getattr(options, bstack1ll11_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ↱"), None):
            options.set_capability(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ↲"), bstack1llllllllll1_opy_(framework))
            options.set_capability(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ↳"), bstack1l111l1111_opy_())
            options.set_capability(bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭↴"), bstack1l11l1l1_opy_)
            options.set_capability(bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭↵"), bstack1ll1lll11_opy_)
            if bstack1l1l1111l1l_opy_:
                options.set_capability(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ↶"), bstack1l1l1111l1l_opy_)
                options.set_capability(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭↷"), bstack1ll1111l1l1_opy_)
                options.set_capability(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ↸"), bstack111lllll_opy_)
        else:
            options[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ↹")] = bstack1llllllllll1_opy_(framework)
            options[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ↺")] = bstack1l111l1111_opy_()
            options[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭↻")] = bstack1l11l1l1_opy_
            options[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭↼")] = bstack1ll1lll11_opy_
            if bstack1l1l1111l1l_opy_:
                options[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ↽")] = bstack1l1l1111l1l_opy_
                options[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭↾")] = bstack1ll1111l1l1_opy_
                options[bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ↿")][bstack1ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⇀")] = bstack111lllll_opy_
    return options
def bstack1111l11lll1_opy_(ws_endpoint, framework):
    bstack1ll1lll11_opy_ = global_config.get_property(bstack1ll11_opy_ (u"ࠥࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡑࡔࡒࡈ࡚ࡉࡔࡠࡏࡄࡔࠧ⇁"))
    if ws_endpoint and len(ws_endpoint.split(bstack1ll11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ⇂"))) > 1:
        ws_url = ws_endpoint.split(bstack1ll11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ⇃"))[0]
        if bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ⇄") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1llllllll111_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1ll11_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭⇅"))[1]))
            bstack1llllllll111_opy_ = bstack1llllllll111_opy_ or {}
            bstack1l11l1l1_opy_ = os.environ[bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⇆")]
            bstack1llllllll111_opy_[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⇇")] = str(framework) + str(__version__)
            bstack1llllllll111_opy_[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⇈")] = bstack1l111l1111_opy_()
            bstack1llllllll111_opy_[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭⇉")] = bstack1l11l1l1_opy_
            bstack1llllllll111_opy_[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭⇊")] = bstack1ll1lll11_opy_
            ws_endpoint = ws_endpoint.split(bstack1ll11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ⇋"))[0] + bstack1ll11_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭⇌") + urllib.parse.quote(json.dumps(bstack1llllllll111_opy_))
    return ws_endpoint
def bstack1l11l1l1l_opy_():
    global bstack111llll11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack111llll11_opy_ = BrowserType.connect
    return bstack111llll11_opy_
def bstack111111ll1ll_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1l1ll11ll_opy_(self, *args, **kwargs):
    global bstack111llll11_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1ll11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ⇍") in kwargs:
            kwargs[bstack1ll11_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭⇎")] = bstack1111l11lll1_opy_(
                kwargs.get(bstack1ll11_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ⇏"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦ⇐").format(str(e)))
    return bstack111llll11_opy_(self, *args, **kwargs)
def bstack1111l1l1l1l_opy_(bstack11111l11lll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11lllll1l_opy_(bstack11111l11lll_opy_, bstack1ll11_opy_ (u"ࠧࠨ⇑"))
        if proxies and proxies.get(bstack1ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ⇒")):
            parsed_url = urlparse(proxies.get(bstack1ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ⇓")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫ⇔")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ⇕")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭⇖")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ⇗")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1111l11l_opy_(bstack11111l11lll_opy_):
    bstack1lllllllllll_opy_ = {
        bstack111l11111ll_opy_[bstack1111111ll11_opy_]: bstack11111l11lll_opy_[bstack1111111ll11_opy_]
        for bstack1111111ll11_opy_ in bstack11111l11lll_opy_
        if bstack1111111ll11_opy_ in bstack111l11111ll_opy_
    }
    bstack1lllllllllll_opy_[bstack1ll11_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧ⇘")] = bstack1111l1l1l1l_opy_(bstack11111l11lll_opy_, global_config.get_property(bstack1ll11_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨ⇙")))
    bstack11111l11l11_opy_ = [element.lower() for element in bstack111l111l111_opy_]
    bstack1111l111l1l_opy_(bstack1lllllllllll_opy_, bstack11111l11l11_opy_)
    return bstack1lllllllllll_opy_
def bstack1111l111l1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll11_opy_ (u"ࠢࠫࠬ࠭࠮ࠧ⇚")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111l111l1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111l111l1l_opy_(item, keys)
def bstack1l11111l11l_opy_():
    bstack11111ll1l1l_opy_ = [os.environ.get(bstack1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡋࡏࡉࡘࡥࡄࡊࡔࠥ⇛")), os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠤࢁࠦ⇜")), bstack1ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⇝")), os.path.join(bstack1ll11_opy_ (u"ࠫ࠴ࡺ࡭ࡱࠩ⇞"), bstack1ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⇟"))]
    for path in bstack11111ll1l1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll11_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨ⇠") + str(path) + bstack1ll11_opy_ (u"ࠢࠨࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥ⇡"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll11_opy_ (u"ࠣࡉ࡬ࡺ࡮ࡴࡧࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸࠦࡦࡰࡴࠣࠫࠧ⇢") + str(path) + bstack1ll11_opy_ (u"ࠤࠪࠦ⇣"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll11_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥ⇤") + str(path) + bstack1ll11_opy_ (u"ࠦࠬࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳ࠯ࠤ⇥"))
            else:
                logger.debug(bstack1ll11_opy_ (u"ࠧࡉࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥ࠭ࠢ⇦") + str(path) + bstack1ll11_opy_ (u"ࠨࠧࠡࡹ࡬ࡸ࡭ࠦࡷࡳ࡫ࡷࡩࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯࠰ࠥ⇧"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll11_opy_ (u"ࠢࡐࡲࡨࡶࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩࠦࡦࡰࡴࠣࠫࠧ⇨") + str(path) + bstack1ll11_opy_ (u"ࠣࠩ࠱ࠦ⇩"))
            return path
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡸࡴࠥ࡬ࡩ࡭ࡧࠣࠫࢀࡶࡡࡵࡪࢀࠫ࠿ࠦࠢ⇪") + str(e) + bstack1ll11_opy_ (u"ࠥࠦ⇫"))
    logger.debug(bstack1ll11_opy_ (u"ࠦࡆࡲ࡬ࠡࡲࡤࡸ࡭ࡹࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠣ⇬"))
    return None
@measure(event_name=EVENTS.bstack111l11l1ll1_opy_, stage=STAGE.bstack11111llll_opy_)
def bstack1lll1l1l11l_opy_(binary_path, bstack1lll1l111ll_opy_, bs_config):
    logger.debug(bstack1ll11_opy_ (u"ࠧࡉࡵࡳࡴࡨࡲࡹࠦࡃࡍࡋࠣࡔࡦࡺࡨࠡࡨࡲࡹࡳࡪ࠺ࠡࡽࢀࠦ⇭").format(binary_path))
    bstack11111lllll1_opy_ = bstack1ll11_opy_ (u"࠭ࠧ⇮")
    bstack1lllllll11l1_opy_ = {
        bstack1ll11_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⇯"): __version__,
        bstack1ll11_opy_ (u"ࠣࡱࡶࠦ⇰"): platform.system(),
        bstack1ll11_opy_ (u"ࠤࡲࡷࡤࡧࡲࡤࡪࠥ⇱"): platform.machine(),
        bstack1ll11_opy_ (u"ࠥࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ⇲"): bstack1ll11_opy_ (u"ࠫ࠵࠭⇳"),
        bstack1ll11_opy_ (u"ࠧࡹࡤ࡬ࡡ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠦ⇴"): bstack1ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⇵")
    }
    bstack1111l11l11l_opy_(bstack1lllllll11l1_opy_)
    try:
        if binary_path:
            if bstack1111l11l1l1_opy_():
                bstack1lllllll11l1_opy_[bstack1ll11_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⇶")] = subprocess.check_output([binary_path, bstack1ll11_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ⇷")]).strip().decode(bstack1ll11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ⇸"))
            else:
                bstack1lllllll11l1_opy_[bstack1ll11_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⇹")] = subprocess.check_output([binary_path, bstack1ll11_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ⇺")], stderr=subprocess.DEVNULL).strip().decode(bstack1ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⇻"))
        response = requests.request(
            bstack1ll11_opy_ (u"࠭ࡇࡆࡖࠪ⇼"),
            url=bstack1llll1ll1l_opy_(bstack1111llllll1_opy_),
            headers=None,
            auth=(bs_config[bstack1ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ⇽")], bs_config[bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ⇾")]),
            json=None,
            params=bstack1lllllll11l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll11_opy_ (u"ࠩࡸࡶࡱ࠭⇿") in data.keys() and bstack1ll11_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧࡣࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ∀") in data.keys():
            logger.debug(bstack1ll11_opy_ (u"ࠦࡓ࡫ࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡨࡩ࡯ࡣࡵࡽ࠱ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧ∁").format(bstack1lllllll11l1_opy_[bstack1ll11_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ∂")]))
            if bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ∃") in os.environ:
                logger.debug(bstack1ll11_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡦࡹࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥ∄"))
                data[bstack1ll11_opy_ (u"ࠨࡷࡵࡰࠬ∅")] = os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬ∆")]
            bstack111111l1l1l_opy_ = bstack11111l111l1_opy_(data[bstack1ll11_opy_ (u"ࠪࡹࡷࡲࠧ∇")], bstack1lll1l111ll_opy_)
            bstack11111lllll1_opy_ = os.path.join(bstack1lll1l111ll_opy_, bstack111111l1l1l_opy_)
            os.chmod(bstack11111lllll1_opy_, 0o777) # bstack1llllll1ll1l_opy_ permission
            return bstack11111lllll1_opy_
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦ∈").format(e))
    return binary_path
def bstack1111l11l11l_opy_(bstack1lllllll11l1_opy_):
    try:
        if bstack1ll11_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫ∉") not in bstack1lllllll11l1_opy_[bstack1ll11_opy_ (u"࠭࡯ࡴࠩ∊")].lower():
            return
        if os.path.exists(bstack1ll11_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ∋")):
            with open(bstack1ll11_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ∌"), bstack1ll11_opy_ (u"ࠤࡵࠦ∍")) as f:
                bstack11111l1ll1l_opy_ = {}
                for line in f:
                    if bstack1ll11_opy_ (u"ࠥࡁࠧ∎") in line:
                        key, value = line.rstrip().split(bstack1ll11_opy_ (u"ࠦࡂࠨ∏"), 1)
                        bstack11111l1ll1l_opy_[key] = value.strip(bstack1ll11_opy_ (u"ࠬࠨ࡜ࠨࠩ∐"))
                bstack1lllllll11l1_opy_[bstack1ll11_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭∑")] = bstack11111l1ll1l_opy_.get(bstack1ll11_opy_ (u"ࠢࡊࡆࠥ−"), bstack1ll11_opy_ (u"ࠣࠤ∓"))
        elif os.path.exists(bstack1ll11_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ∔")):
            bstack1lllllll11l1_opy_[bstack1ll11_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪ∕")] = bstack1ll11_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨࠫ∖")
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾࠢ∗") + e)
@measure(event_name=EVENTS.bstack111l11lll1l_opy_, stage=STAGE.bstack11111llll_opy_)
def bstack11111l111l1_opy_(bstack1111l11111l_opy_, bstack11111ll11ll_opy_):
    logger.debug(bstack1ll11_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣ∘") + str(bstack1111l11111l_opy_) + bstack1ll11_opy_ (u"ࠢࠣ∙"))
    zip_path = os.path.join(bstack11111ll11ll_opy_, bstack1ll11_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶࠢ√"))
    bstack111111l1l1l_opy_ = bstack1ll11_opy_ (u"ࠩࠪ∛")
    with requests.get(bstack1111l11111l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll11_opy_ (u"ࠥࡻࡧࠨ∜")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨ∝"))
    with zipfile.ZipFile(zip_path, bstack1ll11_opy_ (u"ࠬࡸࠧ∞")) as zip_ref:
        bstack1111l1ll1ll_opy_ = zip_ref.namelist()
        if len(bstack1111l1ll1ll_opy_) > 0:
            bstack111111l1l1l_opy_ = bstack1111l1ll1ll_opy_[0] # bstack111111lll1l_opy_ bstack1111llll1ll_opy_ will be bstack111111l1ll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11111ll11ll_opy_)
        logger.debug(bstack1ll11_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱࠣࠫࠧ∟") + str(bstack11111ll11ll_opy_) + bstack1ll11_opy_ (u"ࠢࠨࠤ∠"))
    os.remove(zip_path)
    return bstack111111l1l1l_opy_
def get_cli_dir():
    bstack11111l1lll1_opy_ = bstack1l11111l11l_opy_()
    if bstack11111l1lll1_opy_:
        bstack1lll1l111ll_opy_ = os.path.join(bstack11111l1lll1_opy_, bstack1ll11_opy_ (u"ࠣࡥ࡯࡭ࠧ∡"))
        if not os.path.exists(bstack1lll1l111ll_opy_):
            os.makedirs(bstack1lll1l111ll_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1l111ll_opy_
    else:
        raise FileNotFoundError(bstack1ll11_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠧ∢"))
def bstack1lll1l1l111_opy_(bstack1lll1l111ll_opy_):
    bstack1ll11_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨࠢ∣")
    bstack111111ll111_opy_ = [
        os.path.join(bstack1lll1l111ll_opy_, f)
        for f in os.listdir(bstack1lll1l111ll_opy_)
        if os.path.isfile(os.path.join(bstack1lll1l111ll_opy_, f)) and f.startswith(bstack1ll11_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱ࠧ∤"))
    ]
    if len(bstack111111ll111_opy_) > 0:
        return max(bstack111111ll111_opy_, key=os.path.getmtime) # get bstack11111111l11_opy_ binary
    return bstack1ll11_opy_ (u"ࠧࠨ∥")
def bstack111ll1111l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11ll11111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l11ll11111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l11llll11_opy_(data, keys, default=None):
    bstack1ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡢࡨࡨࡰࡾࠦࡧࡦࡶࠣࡥࠥࡴࡥࡴࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡣࡷࡥ࠿ࠦࡔࡩࡧࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡶࡲࠤࡹࡸࡡࡷࡧࡵࡷࡪ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡰ࡫ࡹࡴ࠼ࠣࡅࠥࡲࡩࡴࡶࠣࡳ࡫ࠦ࡫ࡦࡻࡶ࠳࡮ࡴࡤࡪࡥࡨࡷࠥࡸࡥࡱࡴࡨࡷࡪࡴࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩ࡫ࡦࡢࡷ࡯ࡸ࠿ࠦࡖࡢ࡮ࡸࡩࠥࡺ࡯ࠡࡴࡨࡸࡺࡸ࡮ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡲࡦࡶࡸࡶࡳࡀࠠࡕࡪࡨࠤࡻࡧ࡬ࡶࡧࠣࡥࡹࠦࡴࡩࡧࠣࡲࡪࡹࡴࡦࡦࠣࡴࡦࡺࡨ࠭ࠢࡲࡶࠥࡪࡥࡧࡣࡸࡰࡹࠦࡩࡧࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ∦")
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
def bstack1111llll1_opy_(bstack11111ll1l11_opy_, key, value):
    bstack1ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡶࡲࡶࡪࠦࡃࡍࡋࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠤࡲࡧࡰࡱ࡫ࡱ࡫ࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡰ࡮ࡥࡥ࡯ࡸࡢࡺࡦࡸࡳࡠ࡯ࡤࡴ࠿ࠦࡄࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡭ࡨࡽ࠿ࠦࡋࡦࡻࠣࡪࡷࡵ࡭ࠡࡅࡏࡍࡤࡉࡁࡑࡕࡢࡘࡔࡥࡃࡐࡐࡉࡍࡌࠐࠠࠡࠢࠣࠤࠥࠦࠠࡷࡣ࡯ࡹࡪࡀࠠࡗࡣ࡯ࡹࡪࠦࡦࡳࡱࡰࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡲࡩ࡯ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠐࠠࠡࠢࠣࠦࠧࠨ∧")
    if key in bstack11ll1ll1l_opy_:
        bstack1l111ll11l_opy_ = bstack11ll1ll1l_opy_[key]
        if isinstance(bstack1l111ll11l_opy_, list):
            for env_name in bstack1l111ll11l_opy_:
                bstack11111ll1l11_opy_[env_name] = value
        else:
            bstack11111ll1l11_opy_[bstack1l111ll11l_opy_] = value