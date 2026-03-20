# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
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
from bstack_utils.constants import (bstack1lllll11l1_opy_, bstack11l11lll_opy_, HTTPS_HUB,
                                    bstack111l1l11l1l_opy_, bstack111l11lll1l_opy_, bstack111l1l11lll_opy_, bstack111l111ll1l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1llll111_opy_, bstack1l11l1ll1_opy_
from bstack_utils.proxy import bstack11l11l11l1_opy_, bstack11111ll1_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1l1l1ll1_opy_ import bstack1lllll1l11_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack111llll11l1_opy_(config):
    return config[bstack11lll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧὢ")]
def bstack111ll1l1l11_opy_(config):
    return config[bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩὣ")]
def bstack111111l11_opy_():
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
def bstack1111l111l1l_opy_(obj):
    values = []
    bstack1111l1l11l1_opy_ = re.compile(bstack11lll1_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦὤ"), re.I)
    for key in obj.keys():
        if bstack1111l1l11l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1lllllllllll_opy_(config):
    tags = []
    tags.extend(bstack1111l111l1l_opy_(os.environ))
    tags.extend(bstack1111l111l1l_opy_(config))
    return tags
def bstack111111l1111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11111l11l11_opy_(bstack1111l11ll1l_opy_):
    if not bstack1111l11ll1l_opy_:
        return bstack11lll1_opy_ (u"ࠨࠩὥ")
    return bstack11lll1_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥὦ").format(bstack1111l11ll1l_opy_.name, bstack1111l11ll1l_opy_.email)
def bstack111ll1ll111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111111l1l11_opy_ = repo.common_dir
        info = {
            bstack11lll1_opy_ (u"ࠥࡷ࡭ࡧࠢὧ"): repo.head.commit.hexsha,
            bstack11lll1_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢὨ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11lll1_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧὩ"): repo.active_branch.name,
            bstack11lll1_opy_ (u"ࠨࡴࡢࡩࠥὪ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11lll1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥὫ"): bstack11111l11l11_opy_(repo.head.commit.committer),
            bstack11lll1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤὬ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11lll1_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤὭ"): bstack11111l11l11_opy_(repo.head.commit.author),
            bstack11lll1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣὮ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11lll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧὯ"): repo.head.commit.message,
            bstack11lll1_opy_ (u"ࠧࡸ࡯ࡰࡶࠥὰ"): repo.git.rev_parse(bstack11lll1_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣά")),
            bstack11lll1_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣὲ"): bstack111111l1l11_opy_,
            bstack11lll1_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦέ"): subprocess.check_output([bstack11lll1_opy_ (u"ࠤࡪ࡭ࡹࠨὴ"), bstack11lll1_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨή"), bstack11lll1_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢὶ")]).strip().decode(
                bstack11lll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫί")),
            bstack11lll1_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣὸ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11lll1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤό"): repo.git.rev_list(
                bstack11lll1_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣὺ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111ll1l111_opy_ = []
        for remote in remotes:
            bstack11111111ll1_opy_ = {
                bstack11lll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢύ"): remote.name,
                bstack11lll1_opy_ (u"ࠥࡹࡷࡲࠢὼ"): remote.url,
            }
            bstack1111ll1l111_opy_.append(bstack11111111ll1_opy_)
        bstack11111111111_opy_ = {
            bstack11lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤώ"): bstack11lll1_opy_ (u"ࠧ࡭ࡩࡵࠤ὾"),
            **info,
            bstack11lll1_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢ὿"): bstack1111ll1l111_opy_
        }
        bstack11111111111_opy_ = bstack1111l1111l1_opy_(bstack11111111111_opy_)
        return bstack11111111111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᾀ").format(err))
        return {}
def bstack1111l1lllll_opy_(bstack1111l1l1ll1_opy_=None):
    bstack11lll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࡧ࡬࡭ࡻࠣࡪࡴࡸ࡭ࡢࡶࡷࡩࡩࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡸࡷࡪࠦࡣࡢࡵࡨࡷࠥ࡬࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧࡱ࡯ࡨࡪࡸࠠࡪࡰࠣࡸ࡭࡫ࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡪࡴࡲࡤࡦࡴࡶࠤ࠭ࡲࡩࡴࡶ࠯ࠤࡴࡶࡴࡪࡱࡱࡥࡱ࠯࠺ࠡࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡑࡳࡳ࡫࠺ࠡࡏࡲࡲࡴ࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭࠲ࠠࡶࡵࡨࡷࠥࡩࡵࡳࡴࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡞ࡳࡸ࠴ࡧࡦࡶࡦࡻࡩ࠮ࠩ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡈࡱࡵࡺࡹࠡ࡮࡬ࡷࡹ࡛ࠦ࡞࠼ࠣࡑࡺࡲࡴࡪ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩࠢࡺ࡭ࡹ࡮ࠠ࡯ࡱࠣࡷࡴࡻࡲࡤࡧࡶࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤ࠭ࠢࡵࡩࡹࡻࡲ࡯ࡵࠣ࡟ࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡱࡣࡷ࡬ࡸࡀࠠࡎࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡵࡱࠣࡥࡳࡧ࡬ࡺࡼࡨࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡩ࡯ࡣࡵࡵ࠯ࠤࡪࡧࡣࡩࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡤࠤ࡫ࡵ࡬ࡥࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᾁ")
    if bstack1111l1l1ll1_opy_ is None:
        bstack1111l1l1ll1_opy_ = [os.getcwd()]
    elif isinstance(bstack1111l1l1ll1_opy_, list) and len(bstack1111l1l1ll1_opy_) == 0:
        return []
    results = []
    for folder in bstack1111l1l1ll1_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack11lll1_opy_ (u"ࠤࡉࡳࡱࡪࡥࡳࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢᾂ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack11lll1_opy_ (u"ࠥࡴࡷࡏࡤࠣᾃ"): bstack11lll1_opy_ (u"ࠦࠧᾄ"),
                bstack11lll1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᾅ"): [],
                bstack11lll1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢᾆ"): [],
                bstack11lll1_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢᾇ"): bstack11lll1_opy_ (u"ࠣࠤᾈ"),
                bstack11lll1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡏࡨࡷࡸࡧࡧࡦࡵࠥᾉ"): [],
                bstack11lll1_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦᾊ"): bstack11lll1_opy_ (u"ࠦࠧᾋ"),
                bstack11lll1_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧᾌ"): bstack11lll1_opy_ (u"ࠨࠢᾍ"),
                bstack11lll1_opy_ (u"ࠢࡱࡴࡕࡥࡼࡊࡩࡧࡨࠥᾎ"): bstack11lll1_opy_ (u"ࠣࠤᾏ")
            }
            bstack11111lll111_opy_ = repo.active_branch.name
            bstack1llllllll111_opy_ = repo.head.commit
            result[bstack11lll1_opy_ (u"ࠤࡳࡶࡎࡪࠢᾐ")] = bstack1llllllll111_opy_.hexsha
            bstack1111lll1111_opy_ = _1111ll1111l_opy_(repo)
            logger.debug(bstack11lll1_opy_ (u"ࠥࡆࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡨࡲࡶࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯࠼ࠣࠦᾑ") + str(bstack1111lll1111_opy_) + bstack11lll1_opy_ (u"ࠦࠧᾒ"))
            if bstack1111lll1111_opy_:
                try:
                    bstack111111lll1l_opy_ = repo.git.diff(bstack11lll1_opy_ (u"ࠧ࠳࠭࡯ࡣࡰࡩ࠲ࡵ࡮࡭ࡻࠥᾓ"), bstack1ll11ll1ll1_opy_ (u"ࠨࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂ࠴࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦᾔ")).split(bstack11lll1_opy_ (u"ࠧ࡝ࡰࠪᾕ"))
                    logger.debug(bstack11lll1_opy_ (u"ࠣࡅ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡤࡨࡸࡼ࡫ࡥ࡯ࠢࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾࠢࡤࡲࡩࠦࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾ࠼ࠣࠦᾖ") + str(bstack111111lll1l_opy_) + bstack11lll1_opy_ (u"ࠤࠥᾗ"))
                    result[bstack11lll1_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᾘ")] = [f.strip() for f in bstack111111lll1l_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll11ll1ll1_opy_ (u"ࠦࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀ࠲࠳ࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽࠣᾙ")))
                except Exception:
                    logger.debug(bstack11lll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡧ࡮ࡤࡪࠣࡧࡴࡳࡰࡢࡴ࡬ࡷࡴࡴ࠮ࠡࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡶࡪࡩࡥ࡯ࡶࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠧᾚ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack11lll1_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᾛ")] = _1111111lll1_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack11lll1_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᾜ")] = _1111111lll1_opy_(commits[:5])
            bstack1111ll11ll1_opy_ = set()
            bstack111111l11l1_opy_ = []
            for commit in commits:
                logger.debug(bstack11lll1_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯࡬ࡸ࠿ࠦࠢᾝ") + str(commit.message) + bstack11lll1_opy_ (u"ࠤࠥᾞ"))
                bstack111111lll11_opy_ = commit.author.name if commit.author else bstack11lll1_opy_ (u"࡙ࠥࡳࡱ࡮ࡰࡹࡱࠦᾟ")
                bstack1111ll11ll1_opy_.add(bstack111111lll11_opy_)
                bstack111111l11l1_opy_.append({
                    bstack11lll1_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᾠ"): commit.message.strip(),
                    bstack11lll1_opy_ (u"ࠧࡻࡳࡦࡴࠥᾡ"): bstack111111lll11_opy_
                })
            result[bstack11lll1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢᾢ")] = list(bstack1111ll11ll1_opy_)
            result[bstack11lll1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡍࡦࡵࡶࡥ࡬࡫ࡳࠣᾣ")] = bstack111111l11l1_opy_
            result[bstack11lll1_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣᾤ")] = bstack1llllllll111_opy_.committed_datetime.strftime(bstack11lll1_opy_ (u"ࠤࠨ࡝࠲ࠫ࡭࠮ࠧࡧࠦᾥ"))
            if (not result[bstack11lll1_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦᾦ")] or result[bstack11lll1_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᾧ")].strip() == bstack11lll1_opy_ (u"ࠧࠨᾨ")) and bstack1llllllll111_opy_.message:
                bstack11111ll1lll_opy_ = bstack1llllllll111_opy_.message.strip().splitlines()
                result[bstack11lll1_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢᾩ")] = bstack11111ll1lll_opy_[0] if bstack11111ll1lll_opy_ else bstack11lll1_opy_ (u"ࠢࠣᾪ")
                if len(bstack11111ll1lll_opy_) > 2:
                    result[bstack11lll1_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣᾫ")] = bstack11lll1_opy_ (u"ࠩ࡟ࡲࠬᾬ").join(bstack11111ll1lll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack11lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࠪࡩࡳࡱࡪࡥࡳ࠼ࠣࡿࢂ࠯࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤᾭ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack111111111l1_opy_ = [
        result
        for result in results
        if _11111lll1l1_opy_(result)
    ]
    return bstack111111111l1_opy_
def _11111lll1l1_opy_(result):
    bstack11lll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡍ࡫࡬ࡱࡧࡵࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡩࡧࠢࡤࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡹࡵ࡭ࡶࠣ࡭ࡸࠦࡶࡢ࡮࡬ࡨࠥ࠮࡮ࡰࡰ࠰ࡩࡲࡶࡴࡺࠢࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠡࡣࡱࡨࠥࡧࡵࡵࡪࡲࡶࡸ࠯࠮ࠋࠢࠣࠤࠥࠨࠢࠣᾮ")
    return (
        isinstance(result.get(bstack11lll1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᾯ"), None), list)
        and len(result[bstack11lll1_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᾰ")]) > 0
        and isinstance(result.get(bstack11lll1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᾱ"), None), list)
        and len(result[bstack11lll1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᾲ")]) > 0
    )
def _1111ll1111l_opy_(repo):
    bstack11lll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡗࡶࡾࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡨࡦࠢࡥࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡳࡧࡳࡳࠥࡽࡩࡵࡪࡲࡹࡹࠦࡨࡢࡴࡧࡧࡴࡪࡥࡥࠢࡱࡥࡲ࡫ࡳࠡࡣࡱࡨࠥࡽ࡯ࡳ࡭ࠣࡻ࡮ࡺࡨࠡࡣ࡯ࡰࠥ࡜ࡃࡔࠢࡳࡶࡴࡼࡩࡥࡧࡵࡷ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡥࡶࡦࡴࡣࡩࠢ࡬ࡪࠥࡶ࡯ࡴࡵ࡬ࡦࡱ࡫ࠬࠡࡧ࡯ࡷࡪࠦࡎࡰࡰࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᾳ")
    try:
        try:
            origin = repo.remotes.origin
            bstack1lllllllll1l_opy_ = origin.refs[bstack11lll1_opy_ (u"ࠪࡌࡊࡇࡄࠨᾴ")]
            target = bstack1lllllllll1l_opy_.reference.name
            if target.startswith(bstack11lll1_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬ᾵")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack11lll1_opy_ (u"ࠬࡵࡲࡪࡩ࡬ࡲ࠴࠭ᾶ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1111111lll1_opy_(commits):
    bstack11lll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᾷ")
    bstack111111lll1l_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111111ll1l1_opy_ in diff:
                        if bstack111111ll1l1_opy_.a_path:
                            bstack111111lll1l_opy_.add(bstack111111ll1l1_opy_.a_path)
                        if bstack111111ll1l1_opy_.b_path:
                            bstack111111lll1l_opy_.add(bstack111111ll1l1_opy_.b_path)
    except Exception:
        pass
    return list(bstack111111lll1l_opy_)
def bstack1111l1111l1_opy_(bstack11111111111_opy_):
    bstack11111l1l1l1_opy_ = bstack1111l111111_opy_(bstack11111111111_opy_)
    if bstack11111l1l1l1_opy_ and bstack11111l1l1l1_opy_ > bstack111l1l11l1l_opy_:
        bstack1111ll1l1ll_opy_ = bstack11111l1l1l1_opy_ - bstack111l1l11l1l_opy_
        bstack11111lll1ll_opy_ = bstack1111ll11lll_opy_(bstack11111111111_opy_[bstack11lll1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᾸ")], bstack1111ll1l1ll_opy_)
        bstack11111111111_opy_[bstack11lll1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᾹ")] = bstack11111lll1ll_opy_
        logger.info(bstack11lll1_opy_ (u"ࠤࡗ࡬ࡪࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡨࡢࡵࠣࡦࡪ࡫࡮ࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧ࠲࡙ࠥࡩࡻࡧࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡡࡧࡶࡨࡶࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥࢁࡽࠡࡍࡅࠦᾺ")
                    .format(bstack1111l111111_opy_(bstack11111111111_opy_) / 1024))
    return bstack11111111111_opy_
def bstack1111l111111_opy_(json_data):
    try:
        if json_data:
            bstack11111ll1l11_opy_ = json.dumps(json_data)
            bstack1111111l1l1_opy_ = sys.getsizeof(bstack11111ll1l11_opy_)
            return bstack1111111l1l1_opy_
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡦࡥࡱࡩࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡌࡖࡓࡓࠦ࡯ࡣ࡬ࡨࡧࡹࡀࠠࡼࡿࠥΆ").format(e))
    return -1
def bstack1111ll11lll_opy_(field, bstack1111l1l1l1l_opy_):
    try:
        bstack11111ll1l1l_opy_ = len(bytes(bstack111l11lll1l_opy_, bstack11lll1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᾼ")))
        bstack11111llll1l_opy_ = bytes(field, bstack11lll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᾽"))
        bstack111111l11ll_opy_ = len(bstack11111llll1l_opy_)
        bstack1111111l11l_opy_ = ceil(bstack111111l11ll_opy_ - bstack1111l1l1l1l_opy_ - bstack11111ll1l1l_opy_)
        if bstack1111111l11l_opy_ > 0:
            bstack11111111lll_opy_ = bstack11111llll1l_opy_[:bstack1111111l11l_opy_].decode(bstack11lll1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬι"), errors=bstack11lll1_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࠧ᾿")) + bstack111l11lll1l_opy_
            return bstack11111111lll_opy_
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡴࡳࡷࡱࡧࡦࡺࡩ࡯ࡩࠣࡪ࡮࡫࡬ࡥ࠮ࠣࡲࡴࡺࡨࡪࡰࡪࠤࡼࡧࡳࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧࠤ࡭࡫ࡲࡦ࠼ࠣࡿࢂࠨ῀").format(e))
    return field
def bstack11l111111_opy_():
    env = os.environ
    if (bstack11lll1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢ῁") in env and len(env[bstack11lll1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣῂ")]) > 0) or (
            bstack11lll1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥῃ") in env and len(env[bstack11lll1_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦῄ")]) > 0):
        return {
            bstack11lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ῅"): bstack11lll1_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣῆ"),
            bstack11lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦῇ"): env.get(bstack11lll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧῈ")),
            bstack11lll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧΈ"): env.get(bstack11lll1_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨῊ")),
            bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦΉ"): env.get(bstack11lll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧῌ"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠢࡄࡋࠥ῍")) == bstack11lll1_opy_ (u"ࠣࡶࡵࡹࡪࠨ῎") and bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦ῏"))):
        return {
            bstack11lll1_opy_ (u"ࠥࡲࡦࡳࡥࠣῐ"): bstack11lll1_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨῑ"),
            bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣῒ"): env.get(bstack11lll1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤΐ")),
            bstack11lll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ῔"): env.get(bstack11lll1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧ῕")),
            bstack11lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣῖ"): env.get(bstack11lll1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨῗ"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠦࡈࡏࠢῘ")) == bstack11lll1_opy_ (u"ࠧࡺࡲࡶࡧࠥῙ") and bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨῚ"))):
        return {
            bstack11lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧΊ"): bstack11lll1_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦ῜"),
            bstack11lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ῝"): env.get(bstack11lll1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥ῞")),
            bstack11lll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ῟"): env.get(bstack11lll1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢῠ")),
            bstack11lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧῡ"): env.get(bstack11lll1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨῢ"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠣࡅࡌࠦΰ")) == bstack11lll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢῤ") and env.get(bstack11lll1_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦῥ")) == bstack11lll1_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨῦ"):
        return {
            bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥῧ"): bstack11lll1_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣῨ"),
            bstack11lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥῩ"): None,
            bstack11lll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥῪ"): None,
            bstack11lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣΎ"): None
        }
    if env.get(bstack11lll1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨῬ")) and env.get(bstack11lll1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢ῭")):
        return {
            bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ΅"): bstack11lll1_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤ`"),
            bstack11lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ῰"): env.get(bstack11lll1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨ῱")),
            bstack11lll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦῲ"): None,
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤῳ"): env.get(bstack11lll1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨῴ"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠧࡉࡉࠣ῵")) == bstack11lll1_opy_ (u"ࠨࡴࡳࡷࡨࠦῶ") and bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨῷ"))):
        return {
            bstack11lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨῸ"): bstack11lll1_opy_ (u"ࠤࡇࡶࡴࡴࡥࠣΌ"),
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨῺ"): env.get(bstack11lll1_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢΏ")),
            bstack11lll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢῼ"): None,
            bstack11lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ´"): env.get(bstack11lll1_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ῾"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠣࡅࡌࠦ῿")) == bstack11lll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ ") and bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨ "))):
        return {
            bstack11lll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ "): bstack11lll1_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣ "),
            bstack11lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ "): env.get(bstack11lll1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨ ")),
            bstack11lll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ "): env.get(bstack11lll1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ ")),
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ "): env.get(bstack11lll1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ "))
        }
    if env.get(bstack11lll1_opy_ (u"ࠧࡉࡉࠣ ")) == bstack11lll1_opy_ (u"ࠨࡴࡳࡷࡨࠦ​") and bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥ‌"))):
        return {
            bstack11lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ‍"): bstack11lll1_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤ‎"),
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ‏"): env.get(bstack11lll1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣ‐")),
            bstack11lll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ‑"): env.get(bstack11lll1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ‒")),
            bstack11lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ–"): env.get(bstack11lll1_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦ—"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠤࡆࡍࠧ―")) == bstack11lll1_opy_ (u"ࠥࡸࡷࡻࡥࠣ‖") and bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢ‗"))):
        return {
            bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ‘"): bstack11lll1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤ’"),
            bstack11lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ‚"): env.get(bstack11lll1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ‛")),
            bstack11lll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ“"): env.get(bstack11lll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧ”")) or env.get(bstack11lll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ„")),
            bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ‟"): env.get(bstack11lll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ†"))
        }
    if bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤ‡"))):
        return {
            bstack11lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ•"): bstack11lll1_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤ‣"),
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ․"): bstack11lll1_opy_ (u"ࠦࢀࢃࡻࡾࠤ‥").format(env.get(bstack11lll1_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨ…")), env.get(bstack11lll1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭‧"))),
            bstack11lll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ "): env.get(bstack11lll1_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊࠢ ")),
            bstack11lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ‪"): env.get(bstack11lll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ‫"))
        }
    if bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨ‬"))):
        return {
            bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ‭"): bstack11lll1_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲࠣ‮"),
            bstack11lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ "): bstack11lll1_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠢ‰").format(env.get(bstack11lll1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨ‱")), env.get(bstack11lll1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫ′")), env.get(bstack11lll1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬ″")), env.get(bstack11lll1_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ‴"))),
            bstack11lll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ‵"): env.get(bstack11lll1_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ‶")),
            bstack11lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ‷"): env.get(bstack11lll1_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ‸"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦ‹")) and env.get(bstack11lll1_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ›")):
        return {
            bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ※"): bstack11lll1_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉࠣ‼"),
            bstack11lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ‽"): bstack11lll1_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦ‾").format(env.get(bstack11lll1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬ‿")), env.get(bstack11lll1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨ⁀")), env.get(bstack11lll1_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫ⁁"))),
            bstack11lll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⁂"): env.get(bstack11lll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ⁃")),
            bstack11lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⁄"): env.get(bstack11lll1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣ⁅"))
        }
    if any([env.get(bstack11lll1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ⁆")), env.get(bstack11lll1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤ⁇")), env.get(bstack11lll1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣ⁈"))]):
        return {
            bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⁉"): bstack11lll1_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨ⁊"),
            bstack11lll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⁋"): env.get(bstack11lll1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ⁌")),
            bstack11lll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⁍"): env.get(bstack11lll1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ⁎")),
            bstack11lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⁏"): env.get(bstack11lll1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⁐"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ⁑")):
        return {
            bstack11lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⁒"): bstack11lll1_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯ࠣ⁓"),
            bstack11lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⁔"): env.get(bstack11lll1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧ⁕")),
            bstack11lll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⁖"): env.get(bstack11lll1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦ⁗")),
            bstack11lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⁘"): env.get(bstack11lll1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧ⁙"))
        }
    if env.get(bstack11lll1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤ⁚")) or env.get(bstack11lll1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ⁛")):
        return {
            bstack11lll1_opy_ (u"ࠥࡲࡦࡳࡥࠣ⁜"): bstack11lll1_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶࠧ⁝"),
            bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⁞"): env.get(bstack11lll1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ ")),
            bstack11lll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⁠"): bstack11lll1_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣ⁡") if env.get(bstack11lll1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ⁢")) else None,
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⁣"): env.get(bstack11lll1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤ⁤"))
        }
    if any([env.get(bstack11lll1_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥ⁥")), env.get(bstack11lll1_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ⁦")), env.get(bstack11lll1_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ⁧"))]):
        return {
            bstack11lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ⁨"): bstack11lll1_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣ⁩"),
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⁪"): None,
            bstack11lll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⁫"): env.get(bstack11lll1_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤ⁬")),
            bstack11lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⁭"): env.get(bstack11lll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ⁮"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦ⁯")):
        return {
            bstack11lll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⁰"): bstack11lll1_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨⁱ"),
            bstack11lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁲"): env.get(bstack11lll1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ⁳")),
            bstack11lll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⁴"): bstack11lll1_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣ⁵").format(env.get(bstack11lll1_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫ⁶"))) if env.get(bstack11lll1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧ⁷")) else None,
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⁸"): env.get(bstack11lll1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ⁹"))
        }
    if bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨ⁺"))):
        return {
            bstack11lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⁻"): bstack11lll1_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹࠣ⁼"),
            bstack11lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⁽"): env.get(bstack11lll1_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨ⁾")),
            bstack11lll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧⁿ"): env.get(bstack11lll1_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢ₀")),
            bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ₁"): env.get(bstack11lll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ₂"))
        }
    if bstack1lll11l1_opy_(env.get(bstack11lll1_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣ₃"))):
        return {
            bstack11lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ₄"): bstack11lll1_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥ₅"),
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ₆"): bstack11lll1_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧ₇").format(env.get(bstack11lll1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩ₈")), env.get(bstack11lll1_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪ₉")), env.get(bstack11lll1_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧ₊"))),
            bstack11lll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ₋"): env.get(bstack11lll1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦ₌")),
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ₍"): env.get(bstack11lll1_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦ₎"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠧࡉࡉࠣ₏")) == bstack11lll1_opy_ (u"ࠨࡴࡳࡷࡨࠦₐ") and env.get(bstack11lll1_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢₑ")) == bstack11lll1_opy_ (u"ࠣ࠳ࠥₒ"):
        return {
            bstack11lll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢₓ"): bstack11lll1_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥₔ"),
            bstack11lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢₕ"): bstack11lll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣₖ").format(env.get(bstack11lll1_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎࠪₗ"))),
            bstack11lll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤₘ"): None,
            bstack11lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢₙ"): None,
        }
    if env.get(bstack11lll1_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠧₚ")):
        return {
            bstack11lll1_opy_ (u"ࠥࡲࡦࡳࡥࠣₛ"): bstack11lll1_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨₜ"),
            bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ₝"): None,
            bstack11lll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ₞"): env.get(bstack11lll1_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣ₟")),
            bstack11lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ₠"): env.get(bstack11lll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ₡"))
        }
    if any([env.get(bstack11lll1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨ₢")), env.get(bstack11lll1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦ₣")), env.get(bstack11lll1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥ₤")), env.get(bstack11lll1_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓࠢ₥"))]):
        return {
            bstack11lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ₦"): bstack11lll1_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦ₧"),
            bstack11lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ₨"): None,
            bstack11lll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ₩"): env.get(bstack11lll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ₪")) or None,
            bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ₫"): env.get(bstack11lll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ€"), 0)
        }
    if env.get(bstack11lll1_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ₭")):
        return {
            bstack11lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ₮"): bstack11lll1_opy_ (u"ࠤࡊࡳࡈࡊࠢ₯"),
            bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ₰"): None,
            bstack11lll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ₱"): env.get(bstack11lll1_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ₲")),
            bstack11lll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ₳"): env.get(bstack11lll1_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨ₴"))
        }
    if env.get(bstack11lll1_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ₵")):
        return {
            bstack11lll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ₶"): bstack11lll1_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨ₷"),
            bstack11lll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ₸"): env.get(bstack11lll1_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ₹")),
            bstack11lll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ₺"): env.get(bstack11lll1_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥ₻")),
            bstack11lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ₼"): env.get(bstack11lll1_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ₽"))
        }
    return {bstack11lll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ₾"): None}
def get_host_info():
    return {
        bstack11lll1_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨ₿"): platform.node(),
        bstack11lll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ⃀"): platform.system(),
        bstack11lll1_opy_ (u"ࠨࡴࡺࡲࡨࠦ⃁"): platform.machine(),
        bstack11lll1_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ⃂"): platform.version(),
        bstack11lll1_opy_ (u"ࠣࡣࡵࡧ࡭ࠨ⃃"): platform.architecture()[0]
    }
def bstack1llllllll1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111l1llll1_opy_():
    if global_config.get_property(bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ⃄")):
        return bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⃅")
    return bstack11lll1_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪ⃆")
def bstack1111ll1lll1_opy_(driver):
    info = {
        bstack11lll1_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ⃇"): driver.capabilities,
        bstack11lll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ⃈"): driver.session_id,
        bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ⃉"): driver.capabilities.get(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭⃊"), None),
        bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ⃋"): driver.capabilities.get(bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ⃌"), None),
        bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭⃍"): driver.capabilities.get(bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ⃎"), None),
        bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⃏"):driver.capabilities.get(bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ⃐"), None),
    }
    if bstack1111l1llll1_opy_() == bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⃑"):
        if bstack11ll1ll1ll_opy_():
            info[bstack11lll1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶ⃒ࠪ")] = bstack11lll1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ⃓ࠩ")
        elif driver.capabilities.get(bstack11lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⃔"), {}).get(bstack11lll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⃕"), False):
            info[bstack11lll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ⃖")] = bstack11lll1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⃗")
        else:
            info[bstack11lll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵ⃘ࠩ")] = bstack11lll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨ⃙ࠫ")
    return info
def bstack11ll1ll1ll_opy_():
    if global_config.get_property(bstack11lll1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦ⃚ࠩ")):
        return True
    if bstack1lll11l1_opy_(os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ⃛"), None)):
        return True
    return False
def bstack1111l1l1111_opy_(bstack11111l1ll11_opy_, url, response, headers=None, data=None):
    bstack11lll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡈࡵࡪ࡮ࡧࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࠥࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠯ࡳࡧࡶࡴࡴࡴࡳࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡴࡹࡪࡹࡴࡠࡶࡼࡴࡪࡀࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨࠥ࠮ࡇࡆࡖ࠯ࠤࡕࡕࡓࡕ࠮ࠣࡩࡹࡩ࠮ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࡹࡷࡲ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡘࡖࡑ࠵ࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡰࡤ࡭ࡩࡨࡺࠠࡧࡴࡲࡱࠥࡸࡥࡲࡷࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࡪࡨࡥࡩ࡫ࡲࡴ࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡭࡫ࡡࡥࡧࡵࡷࠥࡵࡲࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥࡣࡷࡥ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡋࡕࡒࡒࠥࡪࡡࡵࡣࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡊࡴࡸ࡭ࡢࡶࡷࡩࡩࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨࠤࡼ࡯ࡴࡩࠢࡵࡩࡶࡻࡥࡴࡶࠣࡥࡳࡪࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡧࡥࡹࡧࠊࠡࠢࠣࠤࠧࠨࠢ⃜")
    bstack11111l1lll1_opy_ = {
        bstack11lll1_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢ⃝"): headers,
        bstack11lll1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ⃞"): bstack11111l1ll11_opy_.upper(),
        bstack11lll1_opy_ (u"ࠣࡣࡪࡩࡳࡺࠢ⃟"): None,
        bstack11lll1_opy_ (u"ࠤࡨࡲࡩࡶ࡯ࡪࡰࡷࠦ⃠"): url,
        bstack11lll1_opy_ (u"ࠥ࡮ࡸࡵ࡮ࠣ⃡"): data
    }
    try:
        bstack11111l111ll_opy_ = response.json()
        if isinstance(bstack11111l111ll_opy_, dict) and bstack11111l111ll_opy_.get(bstack11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃢"), {}).get(bstack11lll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⃣"), {}).get(bstack11lll1_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ⃤")):
            bstack1llllllll1l1_opy_ = json.loads(json.dumps(bstack11111l111ll_opy_))
            bstack1llllllll1l1_opy_[bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ⃥ࠧ")][bstack11lll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴ⃦ࠩ")][bstack11lll1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ⃧")] = bstack11lll1_opy_ (u"ࠥ࡟ࡷ࡫ࡤࡢࡥࡷࡩࡩࠦࡦࡰࡴࠣࡦࡷ࡫ࡶࡪࡶࡼࡡ⃨ࠧ")
            bstack11111l111ll_opy_ = bstack1llllllll1l1_opy_
    except Exception:
        bstack11111l111ll_opy_ = response.text
    bstack11111ll1ll1_opy_ = {
        bstack11lll1_opy_ (u"ࠦࡧࡵࡤࡺࠤ⃩"): bstack11111l111ll_opy_,
        bstack11lll1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࡈࡵࡤࡦࠤ⃪"): response.status_code
    }
    return {
        bstack11lll1_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺ⃫ࠢ"): bstack11111l1lll1_opy_,
        bstack11lll1_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤ⃬"): bstack11111ll1ll1_opy_
    }
def bstack11l1lll11_opy_(bstack11111l1ll11_opy_, url, data, config):
    headers = config.get(bstack11lll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴ⃭ࠩ"), None)
    proxies = bstack11l11l11l1_opy_(config, url)
    auth = config.get(bstack11lll1_opy_ (u"ࠩࡤࡹࡹ࡮⃮ࠧ"), None)
    response = requests.request(
            bstack11111l1ll11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1111l1l1111_opy_(bstack11111l1ll11_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack11lll1_opy_ (u"ࠪ࠰⃯ࠬ"), bstack11lll1_opy_ (u"ࠫ࠿࠭⃰"))))
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡰࡴ࡭ࡧࡪࡰࡪࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵ࠼ࠣࡿࢂࠨ⃱").format(e))
    return response
def bstack1l11l11ll1_opy_(bstack1l1l11lll_opy_, size):
    bstack11ll1l1111_opy_ = []
    while len(bstack1l1l11lll_opy_) > size:
        bstack11l1111l_opy_ = bstack1l1l11lll_opy_[:size]
        bstack11ll1l1111_opy_.append(bstack11l1111l_opy_)
        bstack1l1l11lll_opy_ = bstack1l1l11lll_opy_[size:]
    bstack11ll1l1111_opy_.append(bstack1l1l11lll_opy_)
    return bstack11ll1l1111_opy_
def bstack1111l1l1l11_opy_(message, bstack1111l11l1ll_opy_=False):
    os.write(1, bytes(message, bstack11lll1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ⃲")))
    os.write(1, bytes(bstack11lll1_opy_ (u"ࠧ࡝ࡰࠪ⃳"), bstack11lll1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ⃴")))
    if bstack1111l11l1ll_opy_:
        with open(bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨ⃵") + os.environ[bstack11lll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ⃶")] + bstack11lll1_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩ⃷"), bstack11lll1_opy_ (u"ࠬࡧࠧ⃸")) as f:
            f.write(message + bstack11lll1_opy_ (u"࠭࡜࡯ࠩ⃹"))
def bstack11l1111l1l_opy_():
    return os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ⃺")].lower() == bstack11lll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭⃻")
def current_time():
    return bstack1lllll111l1_opy_().replace(tzinfo=None).isoformat() + bstack11lll1_opy_ (u"ࠩ࡝ࠫ⃼")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11lll1_opy_ (u"ࠪ࡞ࠬ⃽"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11lll1_opy_ (u"ࠫ࡟࠭⃾")))).total_seconds() * 1000
def bstack1111l111ll1_opy_(timestamp):
    return bstack11111l1l111_opy_(timestamp).isoformat() + bstack11lll1_opy_ (u"ࠬࡠࠧ⃿")
def bstack11111l11l1l_opy_(bstack11111l111l1_opy_):
    date_format = bstack11lll1_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫ℀")
    bstack1111111llll_opy_ = datetime.datetime.strptime(bstack11111l111l1_opy_, date_format)
    return bstack1111111llll_opy_.isoformat() + bstack11lll1_opy_ (u"࡛ࠧࠩ℁")
def bstack1111111111l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11lll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨℂ")
    else:
        return bstack11lll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ℃")
def bstack1lll11l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11lll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ℄")
def bstack1llllllll11l_opy_(val):
    return val.__str__().lower() == bstack11lll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ℅")
def error_handler(bstack11111l1llll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11111l1llll_opy_ as e:
                print(bstack11lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧ℆").format(func.__name__, bstack11111l1llll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1111l1lll1l_opy_(bstack111111111ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111111111ll_opy_(cls, *args, **kwargs)
            except bstack11111l1llll_opy_ as e:
                print(bstack11lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨℇ").format(bstack111111111ll_opy_.__name__, bstack11111l1llll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1111l1lll1l_opy_
    else:
        return decorator
def bstack1ll111l11l_opy_(bstack1lll11l111l_opy_):
    if os.getenv(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ℈")) is not None:
        return bstack1lll11l1_opy_(os.getenv(bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ℉")))
    if bstack11lll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ℊ") in bstack1lll11l111l_opy_ and bstack1llllllll11l_opy_(bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧℋ")]):
        return False
    if bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ℌ") in bstack1lll11l111l_opy_ and bstack1llllllll11l_opy_(bstack1lll11l111l_opy_[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧℍ")]):
        return False
    return True
def bstack1ll11lll_opy_():
    try:
        from pytest_bdd import reporting
        bstack111111ll11l_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨℎ"), None)
        return bstack111111ll11l_opy_ is None or bstack111111ll11l_opy_ == bstack11lll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦℏ")
    except Exception as e:
        return False
def bstack1111ll1ll_opy_(hub_url, CONFIG):
    if bstack1ll11lll11_opy_() <= version.parse(bstack11lll1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨℐ")):
        if hub_url:
            return bstack11lll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥℑ") + hub_url + bstack11lll1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢℒ")
        return bstack11l11lll_opy_
    if hub_url:
        return bstack11lll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨℓ") + hub_url + bstack11lll1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ℔")
    return HTTPS_HUB
def bstack1111ll11111_opy_():
    return isinstance(os.getenv(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬℕ")), str)
def bstack111l1lll1_opy_(url):
    return urlparse(url).hostname
def bstack1l11ll1ll1_opy_(hostname):
    for bstack11lll11l1_opy_ in bstack1lllll11l1_opy_:
        regex = re.compile(bstack11lll11l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111ll11l11_opy_(bstack11111ll11ll_opy_, file_name, logger):
    bstack1111llll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠧࡿࠩ№")), bstack11111ll11ll_opy_)
    try:
        if not os.path.exists(bstack1111llll1_opy_):
            os.makedirs(bstack1111llll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠨࢀࠪ℗")), bstack11111ll11ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11lll1_opy_ (u"ࠩࡺࠫ℘")):
                pass
            with open(file_path, bstack11lll1_opy_ (u"ࠥࡻ࠰ࠨℙ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1llll111_opy_.format(str(e)))
def bstack11111ll111l_opy_(file_name, key, value, logger):
    file_path = bstack1111ll11l11_opy_(bstack11lll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫℚ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1l111_opy_ = json.load(open(file_path, bstack11lll1_opy_ (u"ࠬࡸࡢࠨℛ")))
        else:
            bstack11l1l111_opy_ = {}
        bstack11l1l111_opy_[key] = value
        with open(file_path, bstack11lll1_opy_ (u"ࠨࡷࠬࠤℜ")) as outfile:
            json.dump(bstack11l1l111_opy_, outfile)
def bstack1l1l1llll1_opy_(file_name, logger):
    file_path = bstack1111ll11l11_opy_(bstack11lll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧℝ"), file_name, logger)
    bstack11l1l111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11lll1_opy_ (u"ࠨࡴࠪ℞")) as bstack11l111ll11_opy_:
            bstack11l1l111_opy_ = json.load(bstack11l111ll11_opy_)
    return bstack11l1l111_opy_
def bstack1ll1lll11l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨ࠾ࠥ࠭℟") + file_path + bstack11lll1_opy_ (u"ࠪࠤࠬ℠") + str(e))
def bstack1ll11lll11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11lll1_opy_ (u"ࠦࡁࡔࡏࡕࡕࡈࡘࡃࠨ℡")
def bstack1l1l11l1_opy_(config):
    if bstack11lll1_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ™") in config:
        del (config[bstack11lll1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ℣")])
        return False
    if bstack1ll11lll11_opy_() < version.parse(bstack11lll1_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭ℤ")):
        return False
    if bstack1ll11lll11_opy_() >= version.parse(bstack11lll1_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧ℥")):
        return True
    if bstack11lll1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩΩ") in config and config[bstack11lll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ℧")] is False:
        return False
    else:
        return True
def bstack1l11l1111l_opy_(args_list, bstack111111lllll_opy_):
    index = -1
    for value in bstack111111lllll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack111lll11111_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack111lll11111_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llllll11ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llllll11ll_opy_ = bstack1llllll11ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫℨ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ℩"), exception=exception)
    def bstack1ll1lllll11_opy_(self):
        if self.result != bstack11lll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭K"):
            return None
        if isinstance(self.exception_type, str) and bstack11lll1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥÅ") in self.exception_type:
            return bstack11lll1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤℬ")
        return bstack11lll1_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥℭ")
    def bstack11111ll1111_opy_(self):
        if self.result != bstack11lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ℮"):
            return None
        if self.bstack1llllll11ll_opy_:
            return self.bstack1llllll11ll_opy_
        return bstack1111l1l111l_opy_(self.exception)
def bstack1111l1l111l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111ll1l11l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111ll1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack111ll111l_opy_(config, logger):
    try:
        import playwright
        bstack1111l11l1l1_opy_ = playwright.__file__
        bstack111111l1lll_opy_ = os.path.split(bstack1111l11l1l1_opy_)
        bstack1111l11111l_opy_ = bstack111111l1lll_opy_[0] + bstack11lll1_opy_ (u"ࠫ࠴ࡪࡲࡪࡸࡨࡶ࠴ࡶࡡࡤ࡭ࡤ࡫ࡪ࠵࡬ࡪࡤ࠲ࡧࡱ࡯࠯ࡤ࡮࡬࠲࡯ࡹࠧℯ")
        os.environ[bstack11lll1_opy_ (u"ࠬࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠨℰ")] = bstack11111ll1_opy_(config)
        with open(bstack1111l11111l_opy_, bstack11lll1_opy_ (u"࠭ࡲࠨℱ")) as f:
            file_content = f.read()
            bstack1llllllll1ll_opy_ = bstack11lll1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭Ⅎ")
            bstack1111l1ll1ll_opy_ = file_content.find(bstack1llllllll1ll_opy_)
            if bstack1111l1ll1ll_opy_ == -1:
              process = subprocess.Popen(bstack11lll1_opy_ (u"ࠣࡰࡳࡱࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠧℳ"), shell=True, cwd=bstack111111l1lll_opy_[0])
              process.wait()
              bstack1111111ll11_opy_ = bstack11lll1_opy_ (u"ࠩࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺࠢ࠼ࠩℴ")
              bstack1111l1111ll_opy_ = bstack11lll1_opy_ (u"ࠥࠦࠧࠦ࡜ࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࡡࠨ࠻ࠡࡥࡲࡲࡸࡺࠠࡼࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴࠥࢃࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ࠭ࡀࠦࡩࡧࠢࠫࡴࡷࡵࡣࡦࡵࡶ࠲ࡪࡴࡶ࠯ࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜࠭ࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠩࠫ࠾ࠤࠧࠨࠢℵ")
              bstack1111ll1ll1l_opy_ = file_content.replace(bstack1111111ll11_opy_, bstack1111l1111ll_opy_)
              with open(bstack1111l11111l_opy_, bstack11lll1_opy_ (u"ࠫࡼ࠭ℶ")) as f:
                f.write(bstack1111ll1ll1l_opy_)
    except Exception as e:
        logger.error(bstack1l11l1ll1_opy_.format(str(e)))
def bstack1l1111l11l_opy_():
  try:
    bstack1111l1l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬℷ"))
    bstack11111llll11_opy_ = []
    if os.path.exists(bstack1111l1l11ll_opy_):
      with open(bstack1111l1l11ll_opy_) as f:
        bstack11111llll11_opy_ = json.load(f)
      os.remove(bstack1111l1l11ll_opy_)
    return bstack11111llll11_opy_
  except:
    pass
  return []
def bstack111lll11l_opy_(bstack1l1111llll_opy_):
  try:
    bstack11111llll11_opy_ = []
    bstack1111l1l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ℸ"))
    if os.path.exists(bstack1111l1l11ll_opy_):
      with open(bstack1111l1l11ll_opy_) as f:
        bstack11111llll11_opy_ = json.load(f)
    bstack11111llll11_opy_.append(bstack1l1111llll_opy_)
    with open(bstack1111l1l11ll_opy_, bstack11lll1_opy_ (u"ࠧࡸࠩℹ")) as f:
        json.dump(bstack11111llll11_opy_, f)
  except:
    pass
def bstack111llll1l_opy_(logger, bstack1111111l111_opy_ = False):
  try:
    test_name = os.environ.get(bstack11lll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ℺"), bstack11lll1_opy_ (u"ࠩࠪ℻"))
    if test_name == bstack11lll1_opy_ (u"ࠪࠫℼ"):
        test_name = threading.current_thread().__dict__.get(bstack11lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡆࡩࡪ࡟ࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠪℽ"), bstack11lll1_opy_ (u"ࠬ࠭ℾ"))
    bstack11111l11lll_opy_ = bstack11lll1_opy_ (u"࠭ࠬࠡࠩℿ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111111l111_opy_:
        bstack11l111lll1_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⅀"), bstack11lll1_opy_ (u"ࠨ࠲ࠪ⅁"))
        bstack1l11l1l111_opy_ = {bstack11lll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⅂"): test_name, bstack11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⅃"): bstack11111l11lll_opy_, bstack11lll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ⅄"): bstack11l111lll1_opy_}
        bstack111111llll1_opy_ = []
        bstack111111l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫⅅ"))
        if os.path.exists(bstack111111l1l1l_opy_):
            with open(bstack111111l1l1l_opy_) as f:
                bstack111111llll1_opy_ = json.load(f)
        bstack111111llll1_opy_.append(bstack1l11l1l111_opy_)
        with open(bstack111111l1l1l_opy_, bstack11lll1_opy_ (u"࠭ࡷࠨⅆ")) as f:
            json.dump(bstack111111llll1_opy_, f)
    else:
        bstack1l11l1l111_opy_ = {bstack11lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬⅇ"): test_name, bstack11lll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧⅈ"): bstack11111l11lll_opy_, bstack11lll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨⅉ"): str(multiprocessing.current_process().name)}
        if bstack11lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧ⅊") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l11l1l111_opy_)
  except Exception as e:
      logger.warn(bstack11lll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡰࡺࡶࡨࡷࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣ⅋").format(e))
def bstack111lll11_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨ⅌"))
    try:
      bstack1111ll111ll_opy_ = []
      bstack1l11l1l111_opy_ = {bstack11lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⅍"): test_name, bstack11lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ⅎ"): error_message, bstack11lll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⅏"): index}
      bstack1111l1ll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ⅐"))
      if os.path.exists(bstack1111l1ll1l1_opy_):
          with open(bstack1111l1ll1l1_opy_) as f:
              bstack1111ll111ll_opy_ = json.load(f)
      bstack1111ll111ll_opy_.append(bstack1l11l1l111_opy_)
      with open(bstack1111l1ll1l1_opy_, bstack11lll1_opy_ (u"ࠪࡻࠬ⅑")) as f:
          json.dump(bstack1111ll111ll_opy_, f)
    except Exception as e:
      logger.warn(bstack11lll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ⅒").format(e))
    return
  bstack1111ll111ll_opy_ = []
  bstack1l11l1l111_opy_ = {bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⅓"): test_name, bstack11lll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⅔"): error_message, bstack11lll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⅕"): index}
  bstack1111l1ll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⅖"))
  lock_file = bstack1111l1ll1l1_opy_ + bstack11lll1_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨ⅗")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1111l1ll1l1_opy_):
          with open(bstack1111l1ll1l1_opy_, bstack11lll1_opy_ (u"ࠪࡶࠬ⅘")) as f:
              content = f.read().strip()
              if content:
                  bstack1111ll111ll_opy_ = json.load(open(bstack1111l1ll1l1_opy_))
      bstack1111ll111ll_opy_.append(bstack1l11l1l111_opy_)
      with open(bstack1111l1ll1l1_opy_, bstack11lll1_opy_ (u"ࠫࡼ࠭⅙")) as f:
          json.dump(bstack1111ll111ll_opy_, f)
  except Exception as e:
    logger.warn(bstack11lll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧ࠻ࠢࡾࢁࠧ⅚").format(e))
def bstack1ll1lll1l1_opy_(bstack1111l11ll1_opy_, name, logger):
  try:
    bstack1l11l1l111_opy_ = {bstack11lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⅛"): name, bstack11lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⅜"): bstack1111l11ll1_opy_, bstack11lll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⅝"): str(threading.current_thread()._name)}
    return bstack1l11l1l111_opy_
  except Exception as e:
    logger.warn(bstack11lll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⅞").format(e))
  return
def bstack1111l11l111_opy_():
    return platform.system() == bstack11lll1_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫ⅟")
def bstack11l111l11l_opy_(bstack1111l11ll11_opy_, config, logger):
    bstack1111l111lll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111l11ll11_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥⅠ").format(e))
    return bstack1111l111lll_opy_
def bstack11111l11ll1_opy_(bstack11111llllll_opy_, bstack1111ll11l1l_opy_):
    bstack1111111l1ll_opy_ = version.parse(bstack11111llllll_opy_)
    bstack11111lllll1_opy_ = version.parse(bstack1111ll11l1l_opy_)
    if bstack1111111l1ll_opy_ > bstack11111lllll1_opy_:
        return 1
    elif bstack1111111l1ll_opy_ < bstack11111lllll1_opy_:
        return -1
    else:
        return 0
def bstack1lllll111l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11111l1l111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l11lll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1l11l1l1_opy_(options, framework, config, bstack1ll11l1l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11lll1_opy_ (u"ࠬ࡭ࡥࡵࠩⅡ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1ll1ll1_opy_ = caps.get(bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧⅢ"))
    bstack11111lll11l_opy_ = True
    bstack1l111ll1l_opy_ = os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬⅣ")]
    bstack1l11lll1l11_opy_ = config.get(bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨⅤ"), False)
    if bstack1l11lll1l11_opy_:
        bstack1l1ll1ll1ll_opy_ = config.get(bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩⅥ"), {})
        bstack1l1ll1ll1ll_opy_[bstack11lll1_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭Ⅶ")] = os.getenv(bstack11lll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩⅧ"))
        bstack1lll11l1l1_opy_ = json.loads(os.getenv(bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭Ⅸ"), bstack11lll1_opy_ (u"࠭ࡻࡾࠩⅩ"))).get(bstack11lll1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨⅪ"))
    if bstack1llllllll11l_opy_(caps.get(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧⅫ"))) or bstack1llllllll11l_opy_(caps.get(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩⅬ"))):
        bstack11111lll11l_opy_ = False
    if bstack1l1l11l1_opy_({bstack11lll1_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥⅭ"): bstack11111lll11l_opy_}):
        bstack1l1ll1ll1_opy_ = bstack1l1ll1ll1_opy_ or {}
        bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭Ⅾ")] = bstack1111l11lll1_opy_(framework)
        bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧⅯ")] = bstack11l1111l1l_opy_()
        bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩⅰ")] = bstack1l111ll1l_opy_
        bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩⅱ")] = bstack1ll11l1l11_opy_
        if bstack1l11lll1l11_opy_:
            bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨⅲ")] = bstack1l11lll1l11_opy_
            bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩⅳ")] = bstack1l1ll1ll1ll_opy_
            bstack1l1ll1ll1_opy_[bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪⅴ")][bstack11lll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬⅵ")] = bstack1lll11l1l1_opy_
        if getattr(options, bstack11lll1_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ⅶ"), None):
            options.set_capability(bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧⅷ"), bstack1l1ll1ll1_opy_)
        else:
            options[bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨⅸ")] = bstack1l1ll1ll1_opy_
    else:
        if getattr(options, bstack11lll1_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩⅹ"), None):
            options.set_capability(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪⅺ"), bstack1111l11lll1_opy_(framework))
            options.set_capability(bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫⅻ"), bstack11l1111l1l_opy_())
            options.set_capability(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ⅼ"), bstack1l111ll1l_opy_)
            options.set_capability(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ⅽ"), bstack1ll11l1l11_opy_)
            if bstack1l11lll1l11_opy_:
                options.set_capability(bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬⅾ"), bstack1l11lll1l11_opy_)
                options.set_capability(bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ⅿ"), bstack1l1ll1ll1ll_opy_)
                options.set_capability(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨↀ"), bstack1lll11l1l1_opy_)
        else:
            options[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪↁ")] = bstack1111l11lll1_opy_(framework)
            options[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫↂ")] = bstack11l1111l1l_opy_()
            options[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭Ↄ")] = bstack1l111ll1l_opy_
            options[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ↄ")] = bstack1ll11l1l11_opy_
            if bstack1l11lll1l11_opy_:
                options[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬↅ")] = bstack1l11lll1l11_opy_
                options[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ↆ")] = bstack1l1ll1ll1ll_opy_
                options[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧↇ")][bstack11lll1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪↈ")] = bstack1lll11l1l1_opy_
    return options
def bstack11111l1l11l_opy_(ws_endpoint, framework):
    bstack1ll11l1l11_opy_ = global_config.get_property(bstack11lll1_opy_ (u"ࠥࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡑࡔࡒࡈ࡚ࡉࡔࡠࡏࡄࡔࠧ↉"))
    if ws_endpoint and len(ws_endpoint.split(bstack11lll1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ↊"))) > 1:
        ws_url = ws_endpoint.split(bstack11lll1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ↋"))[0]
        if bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ↌") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111l1111l_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack11lll1_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭↍"))[1]))
            bstack11111l1111l_opy_ = bstack11111l1111l_opy_ or {}
            bstack1l111ll1l_opy_ = os.environ[bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭↎")]
            bstack11111l1111l_opy_[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ↏")] = str(framework) + str(__version__)
            bstack11111l1111l_opy_[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ←")] = bstack11l1111l1l_opy_()
            bstack11111l1111l_opy_[bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭↑")] = bstack1l111ll1l_opy_
            bstack11111l1111l_opy_[bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭→")] = bstack1ll11l1l11_opy_
            ws_endpoint = ws_endpoint.split(bstack11lll1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ↓"))[0] + bstack11lll1_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭↔") + urllib.parse.quote(json.dumps(bstack11111l1111l_opy_))
    return ws_endpoint
def bstack1l1ll11lll_opy_():
    global bstack1ll11l1ll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll11l1ll_opy_ = BrowserType.connect
    return bstack1ll11l1ll_opy_
def bstack1111ll1llll_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1lll11ll1_opy_(self, *args, **kwargs):
    global bstack1ll11l1ll_opy_
    try:
        global FRAMEWORK_NAME
        if bstack11lll1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ↕") in kwargs:
            kwargs[bstack11lll1_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭↖")] = bstack11111l1l11l_opy_(
                kwargs.get(bstack11lll1_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ↗"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack11lll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦ↘").format(str(e)))
    return bstack1ll11l1ll_opy_(self, *args, **kwargs)
def bstack11111l11111_opy_(bstack1111ll1ll11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l11l11l1_opy_(bstack1111ll1ll11_opy_, bstack11lll1_opy_ (u"ࠧࠨ↙"))
        if proxies and proxies.get(bstack11lll1_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ↚")):
            parsed_url = urlparse(proxies.get(bstack11lll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ↛")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11lll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫ↜")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ↝")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭↞")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11lll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ↟")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1ll11l1l_opy_(bstack1111ll1ll11_opy_):
    bstack11111l1ll1l_opy_ = {
        bstack111l111ll1l_opy_[bstack11111ll11l1_opy_]: bstack1111ll1ll11_opy_[bstack11111ll11l1_opy_]
        for bstack11111ll11l1_opy_ in bstack1111ll1ll11_opy_
        if bstack11111ll11l1_opy_ in bstack111l111ll1l_opy_
    }
    bstack11111l1ll1l_opy_[bstack11lll1_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧ↠")] = bstack11111l11111_opy_(bstack1111ll1ll11_opy_, global_config.get_property(bstack11lll1_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨ↡")))
    bstack1111ll1l1l1_opy_ = [element.lower() for element in bstack111l1l11lll_opy_]
    bstack111111ll1ll_opy_(bstack11111l1ll1l_opy_, bstack1111ll1l1l1_opy_)
    return bstack11111l1ll1l_opy_
def bstack111111ll1ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11lll1_opy_ (u"ࠢࠫࠬ࠭࠮ࠧ↢")
    for value in d.values():
        if isinstance(value, dict):
            bstack111111ll1ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111111ll1ll_opy_(item, keys)
def bstack11lllll1lll_opy_():
    bstack111111l1ll1_opy_ = [os.environ.get(bstack11lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡋࡏࡉࡘࡥࡄࡊࡔࠥ↣")), os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠤࢁࠦ↤")), bstack11lll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ↥")), os.path.join(bstack11lll1_opy_ (u"ࠫ࠴ࡺ࡭ࡱࠩ↦"), bstack11lll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ↧"))]
    for path in bstack111111l1ll1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11lll1_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨ↨") + str(path) + bstack11lll1_opy_ (u"ࠢࠨࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥ↩"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11lll1_opy_ (u"ࠣࡉ࡬ࡺ࡮ࡴࡧࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸࠦࡦࡰࡴࠣࠫࠧ↪") + str(path) + bstack11lll1_opy_ (u"ࠤࠪࠦ↫"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11lll1_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥ↬") + str(path) + bstack11lll1_opy_ (u"ࠦࠬࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳ࠯ࠤ↭"))
            else:
                logger.debug(bstack11lll1_opy_ (u"ࠧࡉࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥ࠭ࠢ↮") + str(path) + bstack11lll1_opy_ (u"ࠨࠧࠡࡹ࡬ࡸ࡭ࠦࡷࡳ࡫ࡷࡩࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯࠰ࠥ↯"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11lll1_opy_ (u"ࠢࡐࡲࡨࡶࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩࠦࡦࡰࡴࠣࠫࠧ↰") + str(path) + bstack11lll1_opy_ (u"ࠣࠩ࠱ࠦ↱"))
            return path
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡸࡴࠥ࡬ࡩ࡭ࡧࠣࠫࢀࡶࡡࡵࡪࢀࠫ࠿ࠦࠢ↲") + str(e) + bstack11lll1_opy_ (u"ࠥࠦ↳"))
    logger.debug(bstack11lll1_opy_ (u"ࠦࡆࡲ࡬ࠡࡲࡤࡸ࡭ࡹࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠣ↴"))
    return None
@measure(event_name=EVENTS.bstack111l11ll111_opy_, stage=STAGE.bstack1lllllll11_opy_)
def bstack1lll1ll11l1_opy_(binary_path, bstack1lll1ll1lll_opy_, bs_config):
    logger.debug(bstack11lll1_opy_ (u"ࠧࡉࡵࡳࡴࡨࡲࡹࠦࡃࡍࡋࠣࡔࡦࡺࡨࠡࡨࡲࡹࡳࡪ࠺ࠡࡽࢀࠦ↵").format(binary_path))
    bstack1111l1ll111_opy_ = bstack11lll1_opy_ (u"࠭ࠧ↶")
    bstack11111111l11_opy_ = {
        bstack11lll1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ↷"): __version__,
        bstack11lll1_opy_ (u"ࠣࡱࡶࠦ↸"): platform.system(),
        bstack11lll1_opy_ (u"ࠤࡲࡷࡤࡧࡲࡤࡪࠥ↹"): platform.machine(),
        bstack11lll1_opy_ (u"ࠥࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ↺"): bstack11lll1_opy_ (u"ࠫ࠵࠭↻"),
        bstack11lll1_opy_ (u"ࠧࡹࡤ࡬ࡡ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠦ↼"): bstack11lll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭↽")
    }
    bstack1111l1lll11_opy_(bstack11111111l11_opy_)
    try:
        if binary_path:
            if bstack1111l11l111_opy_():
                bstack11111111l11_opy_[bstack11lll1_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ↾")] = subprocess.check_output([binary_path, bstack11lll1_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ↿")]).strip().decode(bstack11lll1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ⇀"))
            else:
                bstack11111111l11_opy_[bstack11lll1_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⇁")] = subprocess.check_output([binary_path, bstack11lll1_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ⇂")], stderr=subprocess.DEVNULL).strip().decode(bstack11lll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⇃"))
        response = requests.request(
            bstack11lll1_opy_ (u"࠭ࡇࡆࡖࠪ⇄"),
            url=bstack1lllll1l11_opy_(bstack111l11lll11_opy_),
            headers=None,
            auth=(bs_config[bstack11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ⇅")], bs_config[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ⇆")]),
            json=None,
            params=bstack11111111l11_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11lll1_opy_ (u"ࠩࡸࡶࡱ࠭⇇") in data.keys() and bstack11lll1_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧࡣࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⇈") in data.keys():
            logger.debug(bstack11lll1_opy_ (u"ࠦࡓ࡫ࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡨࡩ࡯ࡣࡵࡽ࠱ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧ⇉").format(bstack11111111l11_opy_[bstack11lll1_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ⇊")]))
            if bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ⇋") in os.environ:
                logger.debug(bstack11lll1_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡦࡹࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥ⇌"))
                data[bstack11lll1_opy_ (u"ࠨࡷࡵࡰࠬ⇍")] = os.environ[bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬ⇎")]
            bstack1111l1ll11l_opy_ = bstack1111111ll1l_opy_(data[bstack11lll1_opy_ (u"ࠪࡹࡷࡲࠧ⇏")], bstack1lll1ll1lll_opy_)
            bstack1111l1ll111_opy_ = os.path.join(bstack1lll1ll1lll_opy_, bstack1111l1ll11l_opy_)
            os.chmod(bstack1111l1ll111_opy_, 0o777) # bstack111111ll111_opy_ permission
            return bstack1111l1ll111_opy_
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦ⇐").format(e))
    return binary_path
def bstack1111l1lll11_opy_(bstack11111111l11_opy_):
    try:
        if bstack11lll1_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫ⇑") not in bstack11111111l11_opy_[bstack11lll1_opy_ (u"࠭࡯ࡴࠩ⇒")].lower():
            return
        if os.path.exists(bstack11lll1_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ⇓")):
            with open(bstack11lll1_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ⇔"), bstack11lll1_opy_ (u"ࠤࡵࠦ⇕")) as f:
                bstack1111l1l1lll_opy_ = {}
                for line in f:
                    if bstack11lll1_opy_ (u"ࠥࡁࠧ⇖") in line:
                        key, value = line.rstrip().split(bstack11lll1_opy_ (u"ࠦࡂࠨ⇗"), 1)
                        bstack1111l1l1lll_opy_[key] = value.strip(bstack11lll1_opy_ (u"ࠬࠨ࡜ࠨࠩ⇘"))
                bstack11111111l11_opy_[bstack11lll1_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭⇙")] = bstack1111l1l1lll_opy_.get(bstack11lll1_opy_ (u"ࠢࡊࡆࠥ⇚"), bstack11lll1_opy_ (u"ࠣࠤ⇛"))
        elif os.path.exists(bstack11lll1_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ⇜")):
            bstack11111111l11_opy_[bstack11lll1_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪ⇝")] = bstack11lll1_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨࠫ⇞")
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾࠢ⇟") + e)
@measure(event_name=EVENTS.bstack111l1l111l1_opy_, stage=STAGE.bstack1lllllll11_opy_)
def bstack1111111ll1l_opy_(bstack1111l111l11_opy_, bstack11111111l1l_opy_):
    logger.debug(bstack11lll1_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣ⇠") + str(bstack1111l111l11_opy_) + bstack11lll1_opy_ (u"ࠢࠣ⇡"))
    zip_path = os.path.join(bstack11111111l1l_opy_, bstack11lll1_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶࠢ⇢"))
    bstack1111l1ll11l_opy_ = bstack11lll1_opy_ (u"ࠩࠪ⇣")
    with requests.get(bstack1111l111l11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11lll1_opy_ (u"ࠥࡻࡧࠨ⇤")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11lll1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨ⇥"))
    with zipfile.ZipFile(zip_path, bstack11lll1_opy_ (u"ࠬࡸࠧ⇦")) as zip_ref:
        bstack1111l11l11l_opy_ = zip_ref.namelist()
        if len(bstack1111l11l11l_opy_) > 0:
            bstack1111l1ll11l_opy_ = bstack1111l11l11l_opy_[0] # bstack1111l11llll_opy_ bstack111l11l11ll_opy_ will be bstack1lllllllll11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11111111l1l_opy_)
        logger.debug(bstack11lll1_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱࠣࠫࠧ⇧") + str(bstack11111111l1l_opy_) + bstack11lll1_opy_ (u"ࠢࠨࠤ⇨"))
    os.remove(zip_path)
    return bstack1111l1ll11l_opy_
def get_cli_dir():
    bstack11111l1l1ll_opy_ = bstack11lllll1lll_opy_()
    if bstack11111l1l1ll_opy_:
        bstack1lll1ll1lll_opy_ = os.path.join(bstack11111l1l1ll_opy_, bstack11lll1_opy_ (u"ࠣࡥ࡯࡭ࠧ⇩"))
        if not os.path.exists(bstack1lll1ll1lll_opy_):
            os.makedirs(bstack1lll1ll1lll_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1ll1lll_opy_
    else:
        raise FileNotFoundError(bstack11lll1_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠧ⇪"))
def bstack1lll1ll1l1l_opy_(bstack1lll1ll1lll_opy_):
    bstack11lll1_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨࠢ⇫")
    bstack111111l111l_opy_ = [
        os.path.join(bstack1lll1ll1lll_opy_, f)
        for f in os.listdir(bstack1lll1ll1lll_opy_)
        if os.path.isfile(os.path.join(bstack1lll1ll1lll_opy_, f)) and f.startswith(bstack11lll1_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱ࠧ⇬"))
    ]
    if len(bstack111111l111l_opy_) > 0:
        return max(bstack111111l111l_opy_, key=os.path.getmtime) # get bstack1llllllllll1_opy_ binary
    return bstack11lll1_opy_ (u"ࠧࠨ⇭")
def bstack111lll1l11l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11ll1111l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l11ll1111l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11111l11ll_opy_(data, keys, default=None):
    bstack11lll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡢࡨࡨࡰࡾࠦࡧࡦࡶࠣࡥࠥࡴࡥࡴࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡣࡷࡥ࠿ࠦࡔࡩࡧࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡶࡲࠤࡹࡸࡡࡷࡧࡵࡷࡪ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡰ࡫ࡹࡴ࠼ࠣࡅࠥࡲࡩࡴࡶࠣࡳ࡫ࠦ࡫ࡦࡻࡶ࠳࡮ࡴࡤࡪࡥࡨࡷࠥࡸࡥࡱࡴࡨࡷࡪࡴࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩ࡫ࡦࡢࡷ࡯ࡸ࠿ࠦࡖࡢ࡮ࡸࡩࠥࡺ࡯ࠡࡴࡨࡸࡺࡸ࡮ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡲࡦࡶࡸࡶࡳࡀࠠࡕࡪࡨࠤࡻࡧ࡬ࡶࡧࠣࡥࡹࠦࡴࡩࡧࠣࡲࡪࡹࡴࡦࡦࠣࡴࡦࡺࡨ࠭ࠢࡲࡶࠥࡪࡥࡧࡣࡸࡰࡹࠦࡩࡧࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⇮")
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
def bstack1l1lll1ll_opy_(bstack1111ll111l1_opy_, key, value):
    bstack11lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡶࡲࡶࡪࠦࡃࡍࡋࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠤࡲࡧࡰࡱ࡫ࡱ࡫ࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡰ࡮ࡥࡥ࡯ࡸࡢࡺࡦࡸࡳࡠ࡯ࡤࡴ࠿ࠦࡄࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࠥࡳࡡࡱࡲ࡬ࡲ࡬ࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡭ࡨࡽ࠿ࠦࡋࡦࡻࠣࡪࡷࡵ࡭ࠡࡅࡏࡍࡤࡉࡁࡑࡕࡢࡘࡔࡥࡃࡐࡐࡉࡍࡌࠐࠠࠡࠢࠣࠤࠥࠦࠠࡷࡣ࡯ࡹࡪࡀࠠࡗࡣ࡯ࡹࡪࠦࡦࡳࡱࡰࠤࡨࡵ࡭࡮ࡣࡱࡨࠥࡲࡩ࡯ࡧࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠐࠠࠡࠢࠣࠦࠧࠨ⇯")
    if key in bstack111ll1ll1l_opy_:
        bstack111lll111l_opy_ = bstack111ll1ll1l_opy_[key]
        if isinstance(bstack111lll111l_opy_, list):
            for env_name in bstack111lll111l_opy_:
                bstack1111ll111l1_opy_[env_name] = value
        else:
            bstack1111ll111l1_opy_[bstack111lll111l_opy_] = value