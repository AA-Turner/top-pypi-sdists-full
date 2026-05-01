# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import collections
import copy
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
from bstack_utils.constants import (bstack11l111l11l_opy_, bstack111111l1l_opy_, bstack1ll111l1ll_opy_,
                                    bstack111111ll11l_opy_, bstack111111ll111_opy_, bstack111111lll1l_opy_, bstack1111111l111_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111111ll11_opy_, bstack1l11lll1_opy_
from bstack_utils.proxy import bstack1l1111111l_opy_, bstack1lll1111ll_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1ll1l1ll11_opy_
from browserstack_sdk._version import __version__
global_config = Config.bstack1l1l11ll1_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack1111ll11lll_opy_(config):
    return config[bstack111ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ⇛")]
def bstack1111l1l1111_opy_(config):
    return config[bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ⇜")]
def bstack111l1111ll_opy_():
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
def bstack1llll11l11l1_opy_(obj):
    values = []
    bstack1lllll111lll_opy_ = re.compile(bstack111ll_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢ⇝"), re.I)
    for key in obj.keys():
        if bstack1lllll111lll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1llllll1ll11_opy_(config):
    tags = []
    tags.extend(bstack1llll11l11l1_opy_(os.environ))
    tags.extend(bstack1llll11l11l1_opy_(config))
    return tags
def bstack1lllll11l1ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1lllll1l1lll_opy_(bstack1llll1l11l11_opy_):
    if not bstack1llll1l11l11_opy_:
        return bstack111ll_opy_ (u"ࠫࠬ⇞")
    return bstack111ll_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨ⇟").format(bstack1llll1l11l11_opy_.name, bstack1llll1l11l11_opy_.email)
def bstack1111ll11l11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1llll11111ll_opy_ = repo.common_dir
        info = {
            bstack111ll_opy_ (u"ࠨࡳࡩࡣࠥ⇠"): repo.head.commit.hexsha,
            bstack111ll_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥ⇡"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111ll_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣ⇢"): repo.active_branch.name,
            bstack111ll_opy_ (u"ࠤࡷࡥ࡬ࠨ⇣"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨ⇤"): bstack1lllll1l1lll_opy_(repo.head.commit.committer),
            bstack111ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧ⇥"): repo.head.commit.committed_datetime.isoformat(),
            bstack111ll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧ⇦"): bstack1lllll1l1lll_opy_(repo.head.commit.author),
            bstack111ll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦ⇧"): repo.head.commit.authored_datetime.isoformat(),
            bstack111ll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ⇨"): repo.head.commit.message,
            bstack111ll_opy_ (u"ࠣࡴࡲࡳࡹࠨ⇩"): repo.git.rev_parse(bstack111ll_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦ⇪")),
            bstack111ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦ⇫"): bstack1llll11111ll_opy_,
            bstack111ll_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ⇬"): subprocess.check_output([bstack111ll_opy_ (u"ࠧ࡭ࡩࡵࠤ⇭"), bstack111ll_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤ⇮"), bstack111ll_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥ⇯")]).strip().decode(
                bstack111ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ⇰")),
            bstack111ll_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦ⇱"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ⇲"): repo.git.rev_list(
                bstack111ll_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦ⇳").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1lllll1lll1l_opy_ = []
        for remote in remotes:
            bstack1llll1llllll_opy_ = {
                bstack111ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⇴"): remote.name,
                bstack111ll_opy_ (u"ࠨࡵࡳ࡮ࠥ⇵"): remote.url,
            }
            bstack1lllll1lll1l_opy_.append(bstack1llll1llllll_opy_)
        bstack1lll1lll1l11_opy_ = {
            bstack111ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⇶"): bstack111ll_opy_ (u"ࠣࡩ࡬ࡸࠧ⇷"),
            **info,
            bstack111ll_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥ⇸"): bstack1lllll1lll1l_opy_
        }
        bstack1lll1lll1l11_opy_ = bstack1lllll11l111_opy_(bstack1lll1lll1l11_opy_)
        return bstack1lll1lll1l11_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ⇹").format(err))
        return {}
def bstack1lll1llllll1_opy_(bstack1lll1llll11l_opy_=None):
    bstack111ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࡣ࡯ࡰࡾࠦࡦࡰࡴࡰࡥࡹࡺࡥࡥࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡻࡳࡦࠢࡦࡥࡸ࡫ࡳࠡࡨࡲࡶࠥ࡫ࡡࡤࡪࠣࡪࡴࡲࡤࡦࡴࠣ࡭ࡳࠦࡴࡩࡧࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡔ࡯࡯ࡧ࠽ࠤࡒࡵ࡮ࡰ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩ࠮ࠣࡹࡸ࡫ࡳࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡡ࡯ࡴ࠰ࡪࡩࡹࡩࡷࡥࠪࠬࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡋ࡭ࡱࡶࡼࠤࡱ࡯ࡳࡵࠢ࡞ࡡ࠿ࠦࡍࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬ࠥࡽࡩࡵࡪࠣࡲࡴࠦࡳࡰࡷࡵࡧࡪࡹࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧ࠰ࠥࡸࡥࡵࡷࡵࡲࡸ࡛ࠦ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡴࡦࡺࡨࡴ࠼ࠣࡑࡺࡲࡴࡪ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࠢࡩࡳࡱࡪࡥࡳࡵࠣࡸࡴࠦࡡ࡯ࡣ࡯ࡽࡿ࡫ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡭࡫ࡶࡸ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡥ࡫ࡦࡸࡸ࠲ࠠࡦࡣࡦ࡬ࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡲࡶࠥࡧࠠࡧࡱ࡯ࡨࡪࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⇺")
    if bstack1lll1llll11l_opy_ is None:
        bstack1lll1llll11l_opy_ = [os.getcwd()]
    elif isinstance(bstack1lll1llll11l_opy_, list) and len(bstack1lll1llll11l_opy_) == 0:
        return []
    results = []
    for folder in bstack1lll1llll11l_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack111ll_opy_ (u"ࠧࡌ࡯࡭ࡦࡨࡶࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠥ⇻").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack111ll_opy_ (u"ࠨࡰࡳࡋࡧࠦ⇼"): bstack111ll_opy_ (u"ࠢࠣ⇽"),
                bstack111ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢ⇾"): [],
                bstack111ll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥ⇿"): [],
                bstack111ll_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥ∀"): bstack111ll_opy_ (u"ࠦࠧ∁"),
                bstack111ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨ∂"): [],
                bstack111ll_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢ∃"): bstack111ll_opy_ (u"ࠢࠣ∄"),
                bstack111ll_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣ∅"): bstack111ll_opy_ (u"ࠤࠥ∆"),
                bstack111ll_opy_ (u"ࠥࡴࡷࡘࡡࡸࡆ࡬ࡪ࡫ࠨ∇"): bstack111ll_opy_ (u"ࠦࠧ∈")
            }
            bstack1llll1lllll1_opy_ = repo.active_branch.name
            bstack1llll1lll1l1_opy_ = repo.head.commit
            result[bstack111ll_opy_ (u"ࠧࡶࡲࡊࡦࠥ∉")] = bstack1llll1lll1l1_opy_.hexsha
            bstack1llll111l1l1_opy_ = _1llll1111l1l_opy_(repo)
            logger.debug(bstack111ll_opy_ (u"ࠨࡂࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡥࡲࡱࡵࡧࡲࡪࡵࡲࡲ࠿ࠦࠢ∊") + str(bstack1llll111l1l1_opy_) + bstack111ll_opy_ (u"ࠢࠣ∋"))
            if bstack1llll111l1l1_opy_:
                try:
                    bstack1llll111111l_opy_ = repo.git.diff(bstack111ll_opy_ (u"ࠣ࠯࠰ࡲࡦࡳࡥ࠮ࡱࡱࡰࡾࠨ∌"), bstack1l1ll1l1111_opy_ (u"ࠤࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾ࠰࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢ∍")).split(bstack111ll_opy_ (u"ࠪࡠࡳ࠭∎"))
                    logger.debug(bstack111ll_opy_ (u"ࠦࡈ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤࡧ࡫ࡴࡸࡧࡨࡲࠥࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠥࡧ࡮ࡥࠢࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠿ࠦࠢ∏") + str(bstack1llll111111l_opy_) + bstack111ll_opy_ (u"ࠧࠨ∐"))
                    result[bstack111ll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧ∑")] = [f.strip() for f in bstack1llll111111l_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1l1ll1l1111_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦ−")))
                except Exception:
                    logger.debug(bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡢࡳࡣࡱࡧ࡭ࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠱ࠤࡋࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦࡲࡦࡥࡨࡲࡹࠦࡣࡰ࡯ࡰ࡭ࡹࡹ࠮ࠣ∓"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack111ll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ∔")] = _1lllll1111l1_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack111ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤ∕")] = _1lllll1111l1_opy_(commits[:5])
            bstack1llll1l111ll_opy_ = set()
            bstack1llll1l1l111_opy_ = []
            for commit in commits:
                logger.debug(bstack111ll_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲ࡯ࡴ࠻ࠢࠥ∖") + str(commit.message) + bstack111ll_opy_ (u"ࠧࠨ∗"))
                bstack1llll11l11ll_opy_ = commit.author.name if commit.author else bstack111ll_opy_ (u"ࠨࡕ࡯࡭ࡱࡳࡼࡴࠢ∘")
                bstack1llll1l111ll_opy_.add(bstack1llll11l11ll_opy_)
                bstack1llll1l1l111_opy_.append({
                    bstack111ll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ∙"): commit.message.strip(),
                    bstack111ll_opy_ (u"ࠣࡷࡶࡩࡷࠨ√"): bstack1llll11l11ll_opy_
                })
            result[bstack111ll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥ∛")] = list(bstack1llll1l111ll_opy_)
            result[bstack111ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦ∜")] = bstack1llll1l1l111_opy_
            result[bstack111ll_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦ∝")] = bstack1llll1lll1l1_opy_.committed_datetime.strftime(bstack111ll_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࠢ∞"))
            if (not result[bstack111ll_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢ∟")] or result[bstack111ll_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣ∠")].strip() == bstack111ll_opy_ (u"ࠣࠤ∡")) and bstack1llll1lll1l1_opy_.message:
                bstack1lllll1l1l1l_opy_ = bstack1llll1lll1l1_opy_.message.strip().splitlines()
                result[bstack111ll_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥ∢")] = bstack1lllll1l1l1l_opy_[0] if bstack1lllll1l1l1l_opy_ else bstack111ll_opy_ (u"ࠥࠦ∣")
                if len(bstack1lllll1l1l1l_opy_) > 2:
                    result[bstack111ll_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ∤")] = bstack111ll_opy_ (u"ࠬࡢ࡮ࠨ∥").join(bstack1lllll1l1l1l_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤ࠭࡬࡯࡭ࡦࡨࡶ࠿ࠦࡻࡾࠫ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ∦").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1llll11111l1_opy_ = [
        result
        for result in results
        if _1llll11l1111_opy_(result)
    ]
    return bstack1llll11111l1_opy_
def _1llll11l1111_opy_(result):
    bstack111ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡉࡧ࡯ࡴࡪࡸࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡧࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡵࡸࡰࡹࠦࡩࡴࠢࡹࡥࡱ࡯ࡤࠡࠪࡱࡳࡳ࠳ࡥ࡮ࡲࡷࡽࠥ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠤࡦࡴࡤࠡࡣࡸࡸ࡭ࡵࡲࡴࠫ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ∧")
    return (
        isinstance(result.get(bstack111ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢ∨"), None), list)
        and len(result[bstack111ll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ∩")]) > 0
        and isinstance(result.get(bstack111ll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦ∪"), None), list)
        and len(result[bstack111ll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧ∫")]) > 0
    )
def _1llll1111l1l_opy_(repo):
    bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡚ࠥࡲࡺࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶ࡫ࡩࠥࡨࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡶࡪࡶ࡯ࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢ࡫ࡥࡷࡪࡣࡰࡦࡨࡨࠥࡴࡡ࡮ࡧࡶࠤࡦࡴࡤࠡࡹࡲࡶࡰࠦࡷࡪࡶ࡫ࠤࡦࡲ࡬ࠡࡘࡆࡗࠥࡶࡲࡰࡸ࡬ࡨࡪࡸࡳ࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡨࡲࡢࡰࡦ࡬ࠥ࡯ࡦࠡࡲࡲࡷࡸ࡯ࡢ࡭ࡧ࠯ࠤࡪࡲࡳࡦࠢࡑࡳࡳ࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣ∬")
    try:
        try:
            origin = repo.remotes.origin
            bstack1lllll111l1l_opy_ = origin.refs[bstack111ll_opy_ (u"࠭ࡈࡆࡃࡇࠫ∭")]
            target = bstack1lllll111l1l_opy_.reference.name
            if target.startswith(bstack111ll_opy_ (u"ࠧࡰࡴ࡬࡫࡮ࡴ࠯ࠨ∮")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack111ll_opy_ (u"ࠨࡱࡵ࡭࡬࡯࡮࠰ࠩ∯")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1lllll1111l1_opy_(commits):
    bstack111ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡊࡩࡹࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡤࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡧࡴࡲࡱࠥࡧࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࡴ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ∰")
    bstack1llll111111l_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1llll1l11lll_opy_ in diff:
                        if bstack1llll1l11lll_opy_.a_path:
                            bstack1llll111111l_opy_.add(bstack1llll1l11lll_opy_.a_path)
                        if bstack1llll1l11lll_opy_.b_path:
                            bstack1llll111111l_opy_.add(bstack1llll1l11lll_opy_.b_path)
    except Exception:
        pass
    return list(bstack1llll111111l_opy_)
def bstack1lllll11l111_opy_(bstack1lll1lll1l11_opy_):
    bstack1lll1llll111_opy_ = bstack1llllll111l1_opy_(bstack1lll1lll1l11_opy_)
    if bstack1lll1llll111_opy_ and bstack1lll1llll111_opy_ > bstack111111ll11l_opy_:
        bstack1llll1l1ll11_opy_ = bstack1lll1llll111_opy_ - bstack111111ll11l_opy_
        bstack1llllll11111_opy_ = bstack1llllll111ll_opy_(bstack1lll1lll1l11_opy_[bstack111ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ∱")], bstack1llll1l1ll11_opy_)
        bstack1lll1lll1l11_opy_[bstack111ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ∲")] = bstack1llllll11111_opy_
        logger.info(bstack111ll_opy_ (u"࡚ࠧࡨࡦࠢࡦࡳࡲࡳࡩࡵࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪ࠮ࠡࡕ࡬ࡾࡪࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࠢࡤࡪࡹ࡫ࡲࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡽࢀࠤࡐࡈࠢ∳")
                    .format(bstack1llllll111l1_opy_(bstack1lll1lll1l11_opy_) / 1024))
    return bstack1lll1lll1l11_opy_
def bstack1llllll111l1_opy_(json_data):
    try:
        if json_data:
            bstack1llllll1l11l_opy_ = json.dumps(json_data)
            bstack1llll111l11l_opy_ = sys.getsizeof(bstack1llllll1l11l_opy_)
            return bstack1llll111l11l_opy_
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥࡩࡡ࡭ࡥࡸࡰࡦࡺࡩ࡯ࡩࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࡏ࡙ࡏࡏࠢࡲࡦ࡯࡫ࡣࡵ࠼ࠣࡿࢂࠨ∴").format(e))
    return -1
def bstack1llllll111ll_opy_(field, bstack1llll1l11111_opy_):
    try:
        bstack1lll1lllllll_opy_ = len(bytes(bstack111111ll111_opy_, bstack111ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭∵")))
        bstack1lll1llll1l1_opy_ = bytes(field, bstack111ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ∶"))
        bstack1llll1ll11ll_opy_ = len(bstack1lll1llll1l1_opy_)
        bstack1llll11ll1l1_opy_ = ceil(bstack1llll1ll11ll_opy_ - bstack1llll1l11111_opy_ - bstack1lll1lllllll_opy_)
        if bstack1llll11ll1l1_opy_ > 0:
            bstack1lll1lll1111_opy_ = bstack1lll1llll1l1_opy_[:bstack1llll11ll1l1_opy_].decode(bstack111ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ∷"), errors=bstack111ll_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࠪ∸")) + bstack111111ll111_opy_
            return bstack1lll1lll1111_opy_
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡲ࡬ࠦࡦࡪࡧ࡯ࡨ࠱ࠦ࡮ࡰࡶ࡫࡭ࡳ࡭ࠠࡸࡣࡶࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪࠠࡩࡧࡵࡩ࠿ࠦࡻࡾࠤ∹").format(e))
    return field
def bstack1l11ll1111_opy_():
    env = os.environ
    if (bstack111ll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥ∺") in env and len(env[bstack111ll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ∻")]) > 0) or (
            bstack111ll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨ∼") in env and len(env[bstack111ll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ∽")]) > 0):
        return {
            bstack111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ∾"): bstack111ll_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦ∿"),
            bstack111ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ≀"): env.get(bstack111ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ≁")),
            bstack111ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ≂"): env.get(bstack111ll_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤ≃")),
            bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ≄"): env.get(bstack111ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ≅"))
        }
    if env.get(bstack111ll_opy_ (u"ࠥࡇࡎࠨ≆")) == bstack111ll_opy_ (u"ࠦࡹࡸࡵࡦࠤ≇") and bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢ≈"))):
        return {
            bstack111ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ≉"): bstack111ll_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤ≊"),
            bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ≋"): env.get(bstack111ll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ≌")),
            bstack111ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ≍"): env.get(bstack111ll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣ≎")),
            bstack111ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ≏"): env.get(bstack111ll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤ≐"))
        }
    if env.get(bstack111ll_opy_ (u"ࠢࡄࡋࠥ≑")) == bstack111ll_opy_ (u"ࠣࡶࡵࡹࡪࠨ≒") and bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤ≓"))):
        return {
            bstack111ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ≔"): bstack111ll_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢ≕"),
            bstack111ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ≖"): env.get(bstack111ll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨ≗")),
            bstack111ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ≘"): env.get(bstack111ll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ≙")),
            bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ≚"): env.get(bstack111ll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ≛"))
        }
    if env.get(bstack111ll_opy_ (u"ࠦࡈࡏࠢ≜")) == bstack111ll_opy_ (u"ࠧࡺࡲࡶࡧࠥ≝") and env.get(bstack111ll_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢ≞")) == bstack111ll_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤ≟"):
        return {
            bstack111ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ≠"): bstack111ll_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦ≡"),
            bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ≢"): None,
            bstack111ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ≣"): None,
            bstack111ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ≤"): None
        }
    if env.get(bstack111ll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤ≥")) and env.get(bstack111ll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥ≦")):
        return {
            bstack111ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ≧"): bstack111ll_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧ≨"),
            bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ≩"): env.get(bstack111ll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤ≪")),
            bstack111ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ≫"): None,
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ≬"): env.get(bstack111ll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ≭"))
        }
    if env.get(bstack111ll_opy_ (u"ࠣࡅࡌࠦ≮")) == bstack111ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ≯") and bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤ≰"))):
        return {
            bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≱"): bstack111ll_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦ≲"),
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ≳"): env.get(bstack111ll_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥ≴")),
            bstack111ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ≵"): None,
            bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ≶"): env.get(bstack111ll_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ≷"))
        }
    if env.get(bstack111ll_opy_ (u"ࠦࡈࡏࠢ≸")) == bstack111ll_opy_ (u"ࠧࡺࡲࡶࡧࠥ≹") and bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤ≺"))):
        return {
            bstack111ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ≻"): bstack111ll_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦ≼"),
            bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ≽"): env.get(bstack111ll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤ≾")),
            bstack111ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ≿"): env.get(bstack111ll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ⊀")),
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⊁"): env.get(bstack111ll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ⊂"))
        }
    if env.get(bstack111ll_opy_ (u"ࠣࡅࡌࠦ⊃")) == bstack111ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ⊄") and bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨ⊅"))):
        return {
            bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⊆"): bstack111ll_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧ⊇"),
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⊈"): env.get(bstack111ll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦ⊉")),
            bstack111ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⊊"): env.get(bstack111ll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ⊋")),
            bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⊌"): env.get(bstack111ll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢ⊍"))
        }
    if env.get(bstack111ll_opy_ (u"ࠧࡉࡉࠣ⊎")) == bstack111ll_opy_ (u"ࠨࡴࡳࡷࡨࠦ⊏") and bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥ⊐"))):
        return {
            bstack111ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ⊑"): bstack111ll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧ⊒"),
            bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⊓"): env.get(bstack111ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ⊔")),
            bstack111ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⊕"): env.get(bstack111ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣ⊖")) or env.get(bstack111ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥ⊗")),
            bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⊘"): env.get(bstack111ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ⊙"))
        }
    if bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧ⊚"))):
        return {
            bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⊛"): bstack111ll_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧ⊜"),
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⊝"): bstack111ll_opy_ (u"ࠢࡼࡿࡾࢁࠧ⊞").format(env.get(bstack111ll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫ⊟")), env.get(bstack111ll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩ⊠"))),
            bstack111ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⊡"): env.get(bstack111ll_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥ⊢")),
            bstack111ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⊣"): env.get(bstack111ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ⊤"))
        }
    if bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤ⊥"))):
        return {
            bstack111ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ⊦"): bstack111ll_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦ⊧"),
            bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⊨"): bstack111ll_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥ⊩").format(env.get(bstack111ll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫ⊪")), env.get(bstack111ll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧ⊫")), env.get(bstack111ll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨ⊬")), env.get(bstack111ll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ⊭"))),
            bstack111ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⊮"): env.get(bstack111ll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ⊯")),
            bstack111ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⊰"): env.get(bstack111ll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ⊱"))
        }
    if env.get(bstack111ll_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢ⊲")) and env.get(bstack111ll_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤ⊳")):
        return {
            bstack111ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ⊴"): bstack111ll_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦ⊵"),
            bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⊶"): bstack111ll_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢ⊷").format(env.get(bstack111ll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨ⊸")), env.get(bstack111ll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫ⊹")), env.get(bstack111ll_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧ⊺"))),
            bstack111ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⊻"): env.get(bstack111ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤ⊼")),
            bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⊽"): env.get(bstack111ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ⊾"))
        }
    if any([env.get(bstack111ll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⊿")), env.get(bstack111ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ⋀")), env.get(bstack111ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ⋁"))]):
        return {
            bstack111ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ⋂"): bstack111ll_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤ⋃"),
            bstack111ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⋄"): env.get(bstack111ll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ⋅")),
            bstack111ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⋆"): env.get(bstack111ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⋇")),
            bstack111ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⋈"): env.get(bstack111ll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⋉"))
        }
    if env.get(bstack111ll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢ⋊")):
        return {
            bstack111ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ⋋"): bstack111ll_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦ⋌"),
            bstack111ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⋍"): env.get(bstack111ll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣ⋎")),
            bstack111ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⋏"): env.get(bstack111ll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢ⋐")),
            bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⋑"): env.get(bstack111ll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ⋒"))
        }
    if env.get(bstack111ll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧ⋓")) or env.get(bstack111ll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ⋔")):
        return {
            bstack111ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⋕"): bstack111ll_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣ⋖"),
            bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⋗"): env.get(bstack111ll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ⋘")),
            bstack111ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⋙"): bstack111ll_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦ⋚") if env.get(bstack111ll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ⋛")) else None,
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⋜"): env.get(bstack111ll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧ⋝"))
        }
    if any([env.get(bstack111ll_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ⋞")), env.get(bstack111ll_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥ⋟")), env.get(bstack111ll_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥ⋠"))]):
        return {
            bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⋡"): bstack111ll_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦ⋢"),
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⋣"): None,
            bstack111ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⋤"): env.get(bstack111ll_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧ⋥")),
            bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⋦"): env.get(bstack111ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ⋧"))
        }
    if env.get(bstack111ll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢ⋨")):
        return {
            bstack111ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⋩"): bstack111ll_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤ⋪"),
            bstack111ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⋫"): env.get(bstack111ll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ⋬")),
            bstack111ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⋭"): bstack111ll_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦ⋮").format(env.get(bstack111ll_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧ⋯"))) if env.get(bstack111ll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣ⋰")) else None,
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⋱"): env.get(bstack111ll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ⋲"))
        }
    if bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤ⋳"))):
        return {
            bstack111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⋴"): bstack111ll_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦ⋵"),
            bstack111ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⋶"): env.get(bstack111ll_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤ⋷")),
            bstack111ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⋸"): env.get(bstack111ll_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥ⋹")),
            bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⋺"): env.get(bstack111ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⋻"))
        }
    if bstack1lllll11ll1_opy_(env.get(bstack111ll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦ⋼"))):
        return {
            bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⋽"): bstack111ll_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨ⋾"),
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⋿"): bstack111ll_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣ⌀").format(env.get(bstack111ll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬ⌁")), env.get(bstack111ll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭⌂")), env.get(bstack111ll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪ⌃"))),
            bstack111ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⌄"): env.get(bstack111ll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢ⌅")),
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⌆"): env.get(bstack111ll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢ⌇"))
        }
    if env.get(bstack111ll_opy_ (u"ࠣࡅࡌࠦ⌈")) == bstack111ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ⌉") and env.get(bstack111ll_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥ⌊")) == bstack111ll_opy_ (u"ࠦ࠶ࠨ⌋"):
        return {
            bstack111ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⌌"): bstack111ll_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨ⌍"),
            bstack111ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⌎"): bstack111ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦ⌏").format(env.get(bstack111ll_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭⌐"))),
            bstack111ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⌑"): None,
            bstack111ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⌒"): None,
        }
    if env.get(bstack111ll_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣ⌓")):
        return {
            bstack111ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⌔"): bstack111ll_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤ⌕"),
            bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⌖"): None,
            bstack111ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⌗"): env.get(bstack111ll_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦ⌘")),
            bstack111ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⌙"): env.get(bstack111ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ⌚"))
        }
    if any([env.get(bstack111ll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤ⌛")), env.get(bstack111ll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢ⌜")), env.get(bstack111ll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨ⌝")), env.get(bstack111ll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥ⌞"))]):
        return {
            bstack111ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ⌟"): bstack111ll_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢ⌠"),
            bstack111ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⌡"): None,
            bstack111ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⌢"): env.get(bstack111ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ⌣")) or None,
            bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⌤"): env.get(bstack111ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⌥"), 0)
        }
    if env.get(bstack111ll_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ⌦")):
        return {
            bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⌧"): bstack111ll_opy_ (u"ࠧࡍ࡯ࡄࡆࠥ⌨"),
            bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ〈"): None,
            bstack111ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ〉"): env.get(bstack111ll_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ⌫")),
            bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⌬"): env.get(bstack111ll_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤ⌭"))
        }
    if env.get(bstack111ll_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ⌮")):
        return {
            bstack111ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⌯"): bstack111ll_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤ⌰"),
            bstack111ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⌱"): env.get(bstack111ll_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ⌲")),
            bstack111ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⌳"): env.get(bstack111ll_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨ⌴")),
            bstack111ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⌵"): env.get(bstack111ll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⌶"))
        }
    return {bstack111ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⌷"): None}
def get_host_info():
    return {
        bstack111ll_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤ⌸"): platform.node(),
        bstack111ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ⌹"): platform.system(),
        bstack111ll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ⌺"): platform.machine(),
        bstack111ll_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦ⌻"): platform.version(),
        bstack111ll_opy_ (u"ࠦࡦࡸࡣࡩࠤ⌼"): platform.architecture()[0]
    }
def bstack1ll11ll11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1llll111l1ll_opy_():
    if global_config.get_property(bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭⌽")):
        return bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⌾")
    return bstack111ll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭⌿")
def bstack1ll1ll111ll_opy_(driver):
    info = {
        bstack111ll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ⍀"): driver.capabilities,
        bstack111ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭⍁"): driver.session_id,
        bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ⍂"): driver.capabilities.get(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ⍃"), None),
        bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⍄"): driver.capabilities.get(bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⍅"), None),
        bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⍆"): driver.capabilities.get(bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ⍇"), None),
        bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⍈"):driver.capabilities.get(bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⍉"), None),
    }
    if bstack1llll111l1ll_opy_() == bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⍊"):
        if bstack11ll1l1lll_opy_():
            info[bstack111ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭⍋")] = bstack111ll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⍌")
        elif driver.capabilities.get(bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ⍍"), {}).get(bstack111ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⍎"), False):
            info[bstack111ll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ⍏")] = bstack111ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⍐")
        else:
            info[bstack111ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ⍑")] = bstack111ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⍒")
    return info
def bstack11ll1l1lll_opy_():
    if global_config.get_property(bstack111ll_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⍓")):
        return True
    if bstack1lllll11ll1_opy_(os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ⍔"), None)):
        return True
    return False
_1lll1lll111l_opy_ = re.compile(
    bstack111ll_opy_ (u"ࡳࠩࠫࡠࡡࡅࠢࠩࡁ࠽ࠫ⍕") + bstack111ll_opy_ (u"ࠩࡿࠫ⍖").join(re.escape(k) for k in bstack111111lll1l_opy_) + bstack111ll_opy_ (u"ࡵࠫ࠮ࡢ࡜ࡀࠤ࡟ࡷ࠯ࡀ࡜ࡴࠬ࡟ࡠࡄࠨࠩࠩ࡝ࡡࠦࡡࡢ࡝ࠫࠫࠫࡠࡡࡅࠢࠪࠩ⍗"),
    re.IGNORECASE,
)
_1llll1111111_opy_ = re.compile(
    bstack111ll_opy_ (u"ࡶࠬ࠮ࠥ࠳࠴ࠫࡃ࠿࠭⍘") + bstack111ll_opy_ (u"ࠬࢂࠧ⍙").join(re.escape(k) for k in bstack111111lll1l_opy_) + bstack111ll_opy_ (u"ࡸࠧࠪࠧ࠵࠶ࠪ࠹ࡁࠩࡁ࠽ࠩ࠷࠶ࠩࡀࠧ࠵࠶࠮࠮࠮ࠫࡁࠬࠬࠪ࠸࠲ࠪࠩ⍚"),
    re.IGNORECASE,
)
def _1llll1ll1l11_opy_(s):
    s = _1lll1lll111l_opy_.sub(lambda m: m.group(1) + bstack111ll_opy_ (u"ࠧࠫࠬ࠭࠮ࠬ⍛") + m.group(3), s)
    s = _1llll1111111_opy_.sub(lambda m: m.group(1) + bstack111ll_opy_ (u"ࠨࠬ࠭࠮࠯࠭⍜") + m.group(3), s)
    return s
def bstack1llll11ll11l_opy_(obj):
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if isinstance(v, str):
                obj[k] = _1llll1ll1l11_opy_(v)
            else:
                bstack1llll11ll11l_opy_(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                obj[i] = _1llll1ll1l11_opy_(v)
            else:
                bstack1llll11ll11l_opy_(v)
def bstack1llll1ll1111_opy_(bstack1llllll1111l_opy_, url, response, headers=None, data=None):
    bstack111ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡅࡹ࡮ࡲࡤࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡲ࡯ࡨࠢࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠳ࡷ࡫ࡳࡱࡱࡱࡷࡪࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡱࡶࡧࡶࡸࡤࡺࡹࡱࡧ࠽ࠤࡍ࡚ࡔࡑࠢࡰࡩࡹ࡮࡯ࡥࠢࠫࡋࡊ࡚ࠬࠡࡒࡒࡗ࡙࠲ࠠࡦࡶࡦ࠲࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡶࡴ࡯࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡕࡓࡎ࠲ࡩࡳࡪࡰࡰ࡫ࡱࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡴࡨࡪࡦࡥࡷࠤ࡫ࡸ࡯࡮ࠢࡵࡩࡶࡻࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡮ࡥࡢࡦࡨࡶࡸࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡪࡨࡥࡩ࡫ࡲࡴࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩࡧࡴࡢ࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤࡏ࡙ࡏࡏࠢࡧࡥࡹࡧࠠࡰࡴࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡇࡱࡵࡱࡦࡺࡴࡦࡦࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥࠡࡹ࡬ࡸ࡭ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡤࡢࡶࡤࠎࠥࠦࠠࠡࠤࠥࠦ⍝")
    bstack1llll111l111_opy_ = [k.lower() for k in bstack111111lll1l_opy_]
    bstack1llll1lll111_opy_ = None
    if isinstance(data, dict):
        bstack1llll1lll111_opy_ = data
        bstack1llllll1l1l1_opy_(bstack1llll1lll111_opy_, bstack1llll111l111_opy_)
        bstack1llll11ll11l_opy_(bstack1llll1lll111_opy_)
    elif isinstance(data, list):
        bstack1llll1lll111_opy_ = data
        for item in bstack1llll1lll111_opy_:
            if isinstance(item, dict):
                bstack1llllll1l1l1_opy_(item, bstack1llll111l111_opy_)
        bstack1llll11ll11l_opy_(bstack1llll1lll111_opy_)
    else:
        bstack1llll1lll111_opy_ = data
    bstack1lllll1llll1_opy_ = None
    if isinstance(headers, dict):
        bstack1lllll1llll1_opy_ = copy.deepcopy(headers)
        bstack1llllll1l1l1_opy_(bstack1lllll1llll1_opy_, bstack1llll111l111_opy_)
        bstack1llll11ll11l_opy_(bstack1lllll1llll1_opy_)
    else:
        bstack1lllll1llll1_opy_ = headers
    bstack1llll11l1lll_opy_ = {
        bstack111ll_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ⍞"): bstack1lllll1llll1_opy_,
        bstack111ll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦ⍟"): bstack1llllll1111l_opy_.upper(),
        bstack111ll_opy_ (u"ࠧࡧࡧࡦࡰࡷࠦ⍠"): None,
        bstack111ll_opy_ (u"ࠨࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠣ⍡"): url,
        bstack111ll_opy_ (u"ࠢ࡫ࡵࡲࡲࠧ⍢"): bstack1llll1lll111_opy_
    }
    try:
        bstack1lllll1ll1l1_opy_ = response.json()
        if isinstance(bstack1lllll1ll1l1_opy_, dict) and bstack1lllll1ll1l1_opy_.get(bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⍣"), {}).get(bstack111ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⍤"), {}).get(bstack111ll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ⍥")):
            bstack1lll1lllll11_opy_ = json.loads(json.dumps(bstack1lllll1ll1l1_opy_))
            bstack1lll1lllll11_opy_[bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⍦")][bstack111ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⍧")][bstack111ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ⍨")] = bstack111ll_opy_ (u"ࠢ࡜ࡴࡨࡨࡦࡩࡴࡦࡦࠣࡪࡴࡸࠠࡣࡴࡨࡺ࡮ࡺࡹ࡞ࠤ⍩")
            bstack1lllll1ll1l1_opy_ = bstack1lll1lllll11_opy_
        if isinstance(bstack1lllll1ll1l1_opy_, dict):
            bstack1llllll1l1l1_opy_(bstack1lllll1ll1l1_opy_, bstack1llll111l111_opy_)
            bstack1llll11ll11l_opy_(bstack1lllll1ll1l1_opy_)
    except Exception:
        bstack1lllll1ll1l1_opy_ = response.text
    bstack1llll1lll11l_opy_ = {
        bstack111ll_opy_ (u"ࠣࡤࡲࡨࡾࠨ⍪"): bstack1lllll1ll1l1_opy_,
        bstack111ll_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࡅࡲࡨࡪࠨ⍫"): response.status_code
    }
    return {
        bstack111ll_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ⍬"): bstack1llll11l1lll_opy_,
        bstack111ll_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ⍭"): bstack1llll1lll11l_opy_
    }
def bstack1ll11l11l_opy_(bstack1llllll1111l_opy_, url, data, config):
    headers = config.get(bstack111ll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭⍮"), None)
    proxies = bstack1l1111111l_opy_(config, url)
    auth = config.get(bstack111ll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ⍯"), None)
    response = requests.request(
            bstack1llllll1111l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1llll1ll1111_opy_(bstack1llllll1111l_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack111ll_opy_ (u"ࠧ࠭ࠩ⍰"), bstack111ll_opy_ (u"ࠨ࠼ࠪ⍱"))))
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࡼࡿࠥ⍲").format(e))
    return response
def bstack1l1l1ll11_opy_(bstack11llllll1l_opy_, size):
    bstack1l111ll1_opy_ = []
    while len(bstack11llllll1l_opy_) > size:
        bstack1llllllll11_opy_ = bstack11llllll1l_opy_[:size]
        bstack1l111ll1_opy_.append(bstack1llllllll11_opy_)
        bstack11llllll1l_opy_ = bstack11llllll1l_opy_[size:]
    bstack1l111ll1_opy_.append(bstack11llllll1l_opy_)
    return bstack1l111ll1_opy_
def bstack1lllll11llll_opy_(message, bstack1llll11l1l1l_opy_=False):
    os.write(1, bytes(message, bstack111ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⍳")))
    os.write(1, bytes(bstack111ll_opy_ (u"ࠫࡡࡴࠧ⍴"), bstack111ll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⍵")))
    if bstack1llll11l1l1l_opy_:
        with open(bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬ⍶") + os.environ[bstack111ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭⍷")] + bstack111ll_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭⍸"), bstack111ll_opy_ (u"ࠩࡤࠫ⍹")) as f:
            f.write(message + bstack111ll_opy_ (u"ࠪࡠࡳ࠭⍺"))
def bstack1l1l1l11_opy_():
    return os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ⍻")].lower() == bstack111ll_opy_ (u"ࠬࡺࡲࡶࡧࠪ⍼")
def bstack1111l1l1l_opy_():
    return bstack1lll11ll11l_opy_().replace(tzinfo=None).isoformat() + bstack111ll_opy_ (u"࡚࠭ࠨ⍽")
def bstack1lll11111ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111ll_opy_ (u"࡛ࠧࠩ⍾"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111ll_opy_ (u"ࠨ࡜ࠪ⍿")))).total_seconds() * 1000
def bstack1lll1lll11l1_opy_(timestamp):
    return bstack1lllll111l11_opy_(timestamp).isoformat() + bstack111ll_opy_ (u"ࠩ࡝ࠫ⎀")
def bstack1lll1lll1lll_opy_(bstack1llll1l1lll1_opy_):
    date_format = bstack111ll_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨ⎁")
    bstack1llllll11ll1_opy_ = datetime.datetime.strptime(bstack1llll1l1lll1_opy_, date_format)
    return bstack1llllll11ll1_opy_.isoformat() + bstack111ll_opy_ (u"ࠫ࡟࠭⎂")
def bstack1lllll11lll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⎃")
    else:
        return bstack111ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⎄")
def bstack1lllll11ll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111ll_opy_ (u"ࠧࡵࡴࡸࡩࠬ⎅")
def bstack1llll11l111l_opy_(val):
    return val.__str__().lower() == bstack111ll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ⎆")
def error_handler(bstack1lll1lll1l1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1lll1lll1l1l_opy_ as e:
                print(bstack111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤ⎇").format(func.__name__, bstack1lll1lll1l1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1llllll11l11_opy_(bstack1llllll1l111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1llllll1l111_opy_(cls, *args, **kwargs)
            except bstack1lll1lll1l1l_opy_ as e:
                print(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ⎈").format(bstack1llllll1l111_opy_.__name__, bstack1lll1lll1l1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1llllll11l11_opy_
    else:
        return decorator
def bstack11l1ll1l_opy_(bstack1llll1ll1l1_opy_):
    if os.getenv(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ⎉")) is not None:
        return bstack1lllll11ll1_opy_(os.getenv(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ⎊")))
    if bstack111ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⎋") in bstack1llll1ll1l1_opy_ and bstack1llll11l111l_opy_(bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⎌")]):
        return False
    if bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⎍") in bstack1llll1ll1l1_opy_ and bstack1llll11l111l_opy_(bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⎎")]):
        return False
    return True
def bstack11l1ll1l1_opy_():
    try:
        from pytest_bdd import reporting
        bstack1llll1l1l1l1_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥ⎏"), None)
        return bstack1llll1l1l1l1_opy_ is None or bstack1llll1l1l1l1_opy_ == bstack111ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ⎐")
    except Exception as e:
        return False
def bstack1lllll1l1ll_opy_(hub_url, CONFIG):
    if bstack111111111_opy_() <= version.parse(bstack111ll_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ⎑")):
        if hub_url:
            return bstack111ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⎒") + hub_url + bstack111ll_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ⎓")
        return bstack111111l1l_opy_
    if hub_url:
        return bstack111ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ⎔") + hub_url + bstack111ll_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ⎕")
    return bstack1ll111l1ll_opy_
def bstack1llll11lllll_opy_():
    return isinstance(os.getenv(bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩ⎖")), str)
def bstack111ll11ll_opy_(url):
    return urlparse(url).hostname
def bstack11llll11_opy_(hostname):
    for bstack11l11ll11_opy_ in bstack11l111l11l_opy_:
        regex = re.compile(bstack11l11ll11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1llll1llll1l_opy_(bstack1llll11llll1_opy_, file_name, logger):
    bstack1ll11l11ll_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠫࢃ࠭⎗")), bstack1llll11llll1_opy_)
    try:
        if not os.path.exists(bstack1ll11l11ll_opy_):
            os.makedirs(bstack1ll11l11ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠬࢄࠧ⎘")), bstack1llll11llll1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111ll_opy_ (u"࠭ࡷࠨ⎙")):
                pass
            with open(file_path, bstack111ll_opy_ (u"ࠢࡸ࠭ࠥ⎚")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111111ll11_opy_.format(str(e)))
def bstack1lllll11111l_opy_(file_name, key, value, logger):
    file_path = bstack1llll1llll1l_opy_(bstack111ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⎛"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1111111_opy_ = json.load(open(file_path, bstack111ll_opy_ (u"ࠩࡵࡦࠬ⎜")))
        else:
            bstack1ll1111111_opy_ = {}
        bstack1ll1111111_opy_[key] = value
        with open(file_path, bstack111ll_opy_ (u"ࠥࡻ࠰ࠨ⎝")) as outfile:
            json.dump(bstack1ll1111111_opy_, outfile)
def bstack1l1l1l1l11_opy_(file_name, logger):
    file_path = bstack1llll1llll1l_opy_(bstack111ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⎞"), file_name, logger)
    bstack1ll1111111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111ll_opy_ (u"ࠬࡸࠧ⎟")) as bstack1llll11l1l_opy_:
            bstack1ll1111111_opy_ = json.load(bstack1llll11l1l_opy_)
    return bstack1ll1111111_opy_
def bstack1llll111l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪ⎠") + file_path + bstack111ll_opy_ (u"ࠧࠡࠩ⎡") + str(e))
def bstack111111111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111ll_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥ⎢")
def bstack11lll11lll_opy_(config):
    if bstack111ll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ⎣") in config:
        del (config[bstack111ll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ⎤")])
        return False
    if bstack111111111_opy_() < version.parse(bstack111ll_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪ⎥")):
        return False
    if bstack111111111_opy_() >= version.parse(bstack111ll_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫ⎦")):
        return True
    if bstack111ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭⎧") in config and config[bstack111ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ⎨")] is False:
        return False
    else:
        return True
def bstack11l1ll1ll1_opy_(args_list, bstack1llll11l1l11_opy_):
    index = -1
    for value in bstack1llll11l1l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack1111l1ll11l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack1111l1ll11l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llll1l111l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llll1l111l_opy_ = bstack1llll1l111l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⎩"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⎪"), exception=exception)
    def bstack1ll111l111l_opy_(self):
        if self.result != bstack111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⎫"):
            return None
        if isinstance(self.exception_type, str) and bstack111ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ⎬") in self.exception_type:
            return bstack111ll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ⎭")
        return bstack111ll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ⎮")
    def bstack1llll111lll1_opy_(self):
        if self.result != bstack111ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⎯"):
            return None
        if self.bstack1llll1l111l_opy_:
            return self.bstack1llll1l111l_opy_
        return bstack1llllll11l1l_opy_(self.exception)
def bstack1llllll11l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1llll1l1111l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll11l1ll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1111lll1l_opy_(config, logger):
    try:
        import playwright
        bstack1llllll1l1ll_opy_ = playwright.__file__
        bstack1llll1l11ll1_opy_ = os.path.split(bstack1llllll1l1ll_opy_)
        bstack1lllll1ll1ll_opy_ = bstack1llll1l11ll1_opy_[0] + bstack111ll_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫ⎰")
        os.environ[bstack111ll_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬ⎱")] = bstack1lll1111ll_opy_(config)
        with open(bstack1lllll1ll1ll_opy_, bstack111ll_opy_ (u"ࠪࡶࠬ⎲")) as f:
            file_content = f.read()
            bstack1lllll1l111l_opy_ = bstack111ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ⎳")
            bstack1llll1l1l1ll_opy_ = file_content.find(bstack1lllll1l111l_opy_)
            if bstack1llll1l1l1ll_opy_ == -1:
              process = subprocess.Popen(bstack111ll_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤ⎴"), shell=True, cwd=bstack1llll1l11ll1_opy_[0])
              process.wait()
              bstack1lllll111111_opy_ = bstack111ll_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭⎵")
              bstack1lll1lll11ll_opy_ = bstack111ll_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦ⎶")
              bstack1llll1l1ll1l_opy_ = file_content.replace(bstack1lllll111111_opy_, bstack1lll1lll11ll_opy_)
              with open(bstack1lllll1ll1ll_opy_, bstack111ll_opy_ (u"ࠨࡹࠪ⎷")) as f:
                f.write(bstack1llll1l1ll1l_opy_)
    except Exception as e:
        logger.error(bstack1l11lll1_opy_.format(str(e)))
def bstack1llllll111_opy_():
  try:
    bstack1lllll1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩ⎸"))
    bstack1llll1l1llll_opy_ = []
    if os.path.exists(bstack1lllll1l1l11_opy_):
      with open(bstack1lllll1l1l11_opy_) as f:
        bstack1llll1l1llll_opy_ = json.load(f)
      os.remove(bstack1lllll1l1l11_opy_)
    return bstack1llll1l1llll_opy_
  except:
    pass
  return []
def bstack11lllll111_opy_(bstack1ll11lll1l_opy_):
  try:
    bstack1llll1l1llll_opy_ = []
    bstack1lllll1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ⎹"))
    if os.path.exists(bstack1lllll1l1l11_opy_):
      with open(bstack1lllll1l1l11_opy_) as f:
        bstack1llll1l1llll_opy_ = json.load(f)
    bstack1llll1l1llll_opy_.append(bstack1ll11lll1l_opy_)
    with open(bstack1lllll1l1l11_opy_, bstack111ll_opy_ (u"ࠫࡼ࠭⎺")) as f:
        json.dump(bstack1llll1l1llll_opy_, f)
  except:
    pass
def bstack111ll1ll1_opy_(logger, bstack1llll1111lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack111ll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⎻"), bstack111ll_opy_ (u"࠭ࠧ⎼"))
    if test_name == bstack111ll_opy_ (u"ࠧࠨ⎽"):
        test_name = threading.current_thread().__dict__.get(bstack111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧ⎾"), bstack111ll_opy_ (u"ࠩࠪ⎿"))
    bstack1llllll11lll_opy_ = bstack111ll_opy_ (u"ࠪ࠰ࠥ࠭⏀").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1llll1111lll_opy_:
        bstack1l1l11111_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⏁"), bstack111ll_opy_ (u"ࠬ࠶ࠧ⏂"))
        bstack1111ll11_opy_ = {bstack111ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⏃"): test_name, bstack111ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⏄"): bstack1llllll11lll_opy_, bstack111ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⏅"): bstack1l1l11111_opy_}
        bstack1lll1llll1ll_opy_ = []
        bstack1llll1l11l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⏆"))
        if os.path.exists(bstack1llll1l11l1l_opy_):
            with open(bstack1llll1l11l1l_opy_) as f:
                bstack1lll1llll1ll_opy_ = json.load(f)
        bstack1lll1llll1ll_opy_.append(bstack1111ll11_opy_)
        with open(bstack1llll1l11l1l_opy_, bstack111ll_opy_ (u"ࠪࡻࠬ⏇")) as f:
            json.dump(bstack1lll1llll1ll_opy_, f)
    else:
        bstack1111ll11_opy_ = {bstack111ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⏈"): test_name, bstack111ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⏉"): bstack1llllll11lll_opy_, bstack111ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⏊"): str(multiprocessing.current_process().name)}
        if bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ⏋") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1111ll11_opy_)
  except Exception as e:
      logger.warn(bstack111ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ⏌").format(e))
def bstack111l11111_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack111ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ⏍"))
    try:
      bstack1llll111llll_opy_ = []
      bstack1111ll11_opy_ = {bstack111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ⏎"): test_name, bstack111ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⏏"): error_message, bstack111ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ⏐"): index}
      bstack1lll1lllll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ⏑"))
      if os.path.exists(bstack1lll1lllll1l_opy_):
          with open(bstack1lll1lllll1l_opy_) as f:
              bstack1llll111llll_opy_ = json.load(f)
      bstack1llll111llll_opy_.append(bstack1111ll11_opy_)
      with open(bstack1lll1lllll1l_opy_, bstack111ll_opy_ (u"ࠧࡸࠩ⏒")) as f:
          json.dump(bstack1llll111llll_opy_, f)
    except Exception as e:
      logger.warn(bstack111ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ⏓").format(e))
    return
  bstack1llll111llll_opy_ = []
  bstack1111ll11_opy_ = {bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⏔"): test_name, bstack111ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⏕"): error_message, bstack111ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ⏖"): index}
  bstack1lll1lllll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭⏗"))
  lock_file = bstack1lll1lllll1l_opy_ + bstack111ll_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ⏘")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1lll1lllll1l_opy_):
          with open(bstack1lll1lllll1l_opy_, bstack111ll_opy_ (u"ࠧࡳࠩ⏙")) as f:
              content = f.read().strip()
              if content:
                  bstack1llll111llll_opy_ = json.load(open(bstack1lll1lllll1l_opy_))
      bstack1llll111llll_opy_.append(bstack1111ll11_opy_)
      with open(bstack1lll1lllll1l_opy_, bstack111ll_opy_ (u"ࠨࡹࠪ⏚")) as f:
          json.dump(bstack1llll111llll_opy_, f)
  except Exception as e:
    logger.warn(bstack111ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡦࡪ࡮ࡨࠤࡱࡵࡣ࡬࡫ࡱ࡫࠿ࠦࡻࡾࠤ⏛").format(e))
def bstack1111111ll_opy_(bstack1l11llll1_opy_, name, logger):
  try:
    bstack1111ll11_opy_ = {bstack111ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ⏜"): name, bstack111ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⏝"): bstack1l11llll1_opy_, bstack111ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ⏞"): str(threading.current_thread()._name)}
    return bstack1111ll11_opy_
  except Exception as e:
    logger.warn(bstack111ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ⏟").format(e))
  return
def bstack1llll11lll11_opy_():
    return platform.system() == bstack111ll_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨ⏠")
def bstack11111lll11_opy_(bstack1llll111ll1l_opy_, config, logger):
    bstack1lllll1ll111_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1llll111ll1l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ⏡").format(e))
    return bstack1lllll1ll111_opy_
def bstack1111l1lllll_opy_(bstack1llll1ll1ll1_opy_, bstack1lllll1111ll_opy_):
    bstack1llll1ll111l_opy_ = version.parse(bstack1llll1ll1ll1_opy_)
    bstack1llll1l1l11l_opy_ = version.parse(bstack1lllll1111ll_opy_)
    if bstack1llll1ll111l_opy_ > bstack1llll1l1l11l_opy_:
        return 1
    elif bstack1llll1ll111l_opy_ < bstack1llll1l1l11l_opy_:
        return -1
    else:
        return 0
def bstack1lll11ll11l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1lllll111l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll111ll11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111ll11111_opy_(options, framework, config, bstack11ll11l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack111ll_opy_ (u"ࠩࡪࡩࡹ࠭⏢"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l1l11l1l_opy_ = caps.get(bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⏣"))
    bstack1lllll11ll1l_opy_ = True
    bstack1ll11l1lll_opy_ = os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⏤")]
    bstack11lllll11l1_opy_ = config.get(bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⏥"), False)
    if bstack11lllll11l1_opy_:
        bstack1l1l1ll1111_opy_ = config.get(bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⏦"), {})
        bstack1l1l1ll1111_opy_[bstack111ll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ⏧")] = os.getenv(bstack111ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⏨"))
        bstack1l11111l_opy_ = json.loads(os.getenv(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⏩"), bstack111ll_opy_ (u"ࠪࡿࢂ࠭⏪"))).get(bstack111ll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⏫"))
    if bstack1llll11l111l_opy_(caps.get(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫ⏬"))) or bstack1llll11l111l_opy_(caps.get(bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭⏭"))):
        bstack1lllll11ll1l_opy_ = False
    if bstack11lll11lll_opy_({bstack111ll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ⏮"): bstack1lllll11ll1l_opy_}):
        bstack11l1l11l1l_opy_ = bstack11l1l11l1l_opy_ or {}
        bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⏯")] = bstack1llll111ll11_opy_(framework)
        bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⏰")] = bstack1l1l1l11_opy_()
        bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭⏱")] = bstack1ll11l1lll_opy_
        bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭⏲")] = bstack11ll11l11_opy_
        if bstack11lllll11l1_opy_:
            bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⏳")] = bstack11lllll11l1_opy_
            bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⏴")] = bstack1l1l1ll1111_opy_
            bstack11l1l11l1l_opy_[bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⏵")][bstack111ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⏶")] = bstack1l11111l_opy_
        if getattr(options, bstack111ll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ⏷"), None):
            options.set_capability(bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⏸"), bstack11l1l11l1l_opy_)
        else:
            options[bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⏹")] = bstack11l1l11l1l_opy_
    else:
        if getattr(options, bstack111ll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭⏺"), None):
            options.set_capability(bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ⏻"), bstack1llll111ll11_opy_(framework))
            options.set_capability(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⏼"), bstack1l1l1l11_opy_())
            options.set_capability(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ⏽"), bstack1ll11l1lll_opy_)
            options.set_capability(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ⏾"), bstack11ll11l11_opy_)
            if bstack11lllll11l1_opy_:
                options.set_capability(bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⏿"), bstack11lllll11l1_opy_)
                options.set_capability(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ␀"), bstack1l1l1ll1111_opy_)
                options.set_capability(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ␁"), bstack1l11111l_opy_)
        else:
            options[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ␂")] = bstack1llll111ll11_opy_(framework)
            options[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ␃")] = bstack1l1l1l11_opy_()
            options[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ␄")] = bstack1ll11l1lll_opy_
            options[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ␅")] = bstack11ll11l11_opy_
            if bstack11lllll11l1_opy_:
                options[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ␆")] = bstack11lllll11l1_opy_
                options[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ␇")] = bstack1l1l1ll1111_opy_
                options[bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ␈")][bstack111ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ␉")] = bstack1l11111l_opy_
    return options
def bstack1llll1ll1lll_opy_(ws_endpoint, framework):
    bstack11ll11l11_opy_ = global_config.get_property(bstack111ll_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ␊"))
    if ws_endpoint and len(ws_endpoint.split(bstack111ll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ␋"))) > 1:
        ws_url = ws_endpoint.split(bstack111ll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ␌"))[0]
        if bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭␍") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1lllll1l1ll1_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack111ll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ␎"))[1]))
            bstack1lllll1l1ll1_opy_ = bstack1lllll1l1ll1_opy_ or {}
            bstack1ll11l1lll_opy_ = os.environ[bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ␏")]
            bstack1lllll1l1ll1_opy_[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ␐")] = str(framework) + str(__version__)
            bstack1lllll1l1ll1_opy_[bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ␑")] = bstack1l1l1l11_opy_()
            bstack1lllll1l1ll1_opy_[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ␒")] = bstack1ll11l1lll_opy_
            bstack1lllll1l1ll1_opy_[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ␓")] = bstack11ll11l11_opy_
            ws_endpoint = ws_endpoint.split(bstack111ll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ␔"))[0] + bstack111ll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ␕") + urllib.parse.quote(json.dumps(bstack1lllll1l1ll1_opy_))
    return ws_endpoint
def bstack111l1l1ll1_opy_():
    global bstack1l1l1lll11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l1lll11_opy_ = BrowserType.connect
    return bstack1l1l1lll11_opy_
def bstack1lllll1l1111_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1l1l1l1l1_opy_(self, *args, **kwargs):
    global bstack1l1l1lll11_opy_
    try:
        global FRAMEWORK_NAME
        if bstack111ll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ␖") in kwargs:
            kwargs[bstack111ll_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪ␗")] = bstack1llll1ll1lll_opy_(
                kwargs.get(bstack111ll_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ␘"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack111ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣ␙").format(str(e)))
    return bstack1l1l1lll11_opy_(self, *args, **kwargs)
def bstack1llll1l111l1_opy_(bstack1lllll11ll11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1111111l_opy_(bstack1lllll11ll11_opy_, bstack111ll_opy_ (u"ࠤࠥ␚"))
        if proxies and proxies.get(bstack111ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ␛")):
            parsed_url = urlparse(proxies.get(bstack111ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ␜")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack111ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ␝")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack111ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ␞")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack111ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ␟")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack111ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ␠")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11ll11l111_opy_(bstack1lllll11ll11_opy_):
    bstack1llll1111ll1_opy_ = {
        bstack1111111l111_opy_[bstack1lllll1l11ll_opy_]: bstack1lllll11ll11_opy_[bstack1lllll1l11ll_opy_]
        for bstack1lllll1l11ll_opy_ in bstack1lllll11ll11_opy_
        if bstack1lllll1l11ll_opy_ in bstack1111111l111_opy_
    }
    bstack1llll1111ll1_opy_[bstack111ll_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤ␡")] = bstack1llll1l111l1_opy_(bstack1lllll11ll11_opy_, global_config.get_property(bstack111ll_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥ␢")))
    bstack1llll1ll11l1_opy_ = [element.lower() for element in bstack111111lll1l_opy_]
    bstack1llllll1l1l1_opy_(bstack1llll1111ll1_opy_, bstack1llll1ll11l1_opy_)
    return bstack1llll1111ll1_opy_
def bstack1llllll1l1l1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack111ll_opy_ (u"ࠦ࠯࠰ࠪࠫࠤ␣")
    for value in d.values():
        if isinstance(value, dict):
            bstack1llllll1l1l1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1llllll1l1l1_opy_(item, keys)
def bstack11ll11l1lll_opy_():
    bstack1lllll1lllll_opy_ = [os.environ.get(bstack111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢ␤")), os.path.join(os.path.expanduser(bstack111ll_opy_ (u"ࠨࡾࠣ␥")), bstack111ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ␦")), os.path.join(bstack111ll_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭␧"), bstack111ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ␨"))]
    for path in bstack1lllll1lllll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack111ll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥ␩") + str(path) + bstack111ll_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢ␪"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack111ll_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤ␫") + str(path) + bstack111ll_opy_ (u"ࠨࠧࠣ␬"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack111ll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢ␭") + str(path) + bstack111ll_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨ␮"))
            else:
                logger.debug(bstack111ll_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦ␯") + str(path) + bstack111ll_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢ␰"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack111ll_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤ␱") + str(path) + bstack111ll_opy_ (u"ࠧ࠭࠮ࠣ␲"))
            return path
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦ␳") + str(e) + bstack111ll_opy_ (u"ࠢࠣ␴"))
    logger.debug(bstack111ll_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧ␵"))
    return None
@measure(event_name=EVENTS.bstack1111111llll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
def bstack1ll1l11111l_opy_(binary_path, bstack1ll1l111l1l_opy_, bs_config):
    logger.debug(bstack111ll_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣ␶").format(binary_path))
    bstack1lll1lll1ll1_opy_ = bstack111ll_opy_ (u"ࠪࠫ␷")
    bstack1llll11lll1l_opy_ = {
        bstack111ll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ␸"): __version__,
        bstack111ll_opy_ (u"ࠧࡵࡳࠣ␹"): platform.system(),
        bstack111ll_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢ␺"): platform.machine(),
        bstack111ll_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ␻"): bstack111ll_opy_ (u"ࠨ࠲ࠪ␼"),
        bstack111ll_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣ␽"): bstack111ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ␾")
    }
    bstack1llllll1ll1l_opy_(bstack1llll11lll1l_opy_)
    try:
        if binary_path:
            if bstack1llll11lll11_opy_():
                bstack1llll11lll1l_opy_[bstack111ll_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ␿")] = subprocess.check_output([binary_path, bstack111ll_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ⑀")]).strip().decode(bstack111ll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ⑁"))
            else:
                bstack1llll11lll1l_opy_[bstack111ll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⑂")] = subprocess.check_output([binary_path, bstack111ll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ⑃")], stderr=subprocess.DEVNULL).strip().decode(bstack111ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ⑄"))
        response = requests.request(
            bstack111ll_opy_ (u"ࠪࡋࡊ࡚ࠧ⑅"),
            url=bstack1ll1l1ll11_opy_(bstack11111l11lll_opy_),
            headers=None,
            auth=(bs_config[bstack111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭⑆")], bs_config[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ⑇")]),
            json=None,
            params=bstack1llll11lll1l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack111ll_opy_ (u"࠭ࡵࡳ࡮ࠪ⑈") in data.keys() and bstack111ll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⑉") in data.keys():
            logger.debug(bstack111ll_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤ⑊").format(bstack1llll11lll1l_opy_[bstack111ll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⑋")]))
            if bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭⑌") in os.environ:
                logger.debug(bstack111ll_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡣࡶࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠠࡪࡵࠣࡷࡪࡺࠢ⑍"))
                data[bstack111ll_opy_ (u"ࠬࡻࡲ࡭ࠩ⑎")] = os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ⑏")]
            bstack1lllll11l1l1_opy_ = bstack1llll11l1ll1_opy_(data[bstack111ll_opy_ (u"ࠧࡶࡴ࡯ࠫ⑐")], bstack1ll1l111l1l_opy_)
            bstack1lll1lll1ll1_opy_ = os.path.join(bstack1ll1l111l1l_opy_, bstack1lllll11l1l1_opy_)
            os.chmod(bstack1lll1lll1ll1_opy_, 0o777) # bstack1llll11ll1ll_opy_ permission
            return bstack1lll1lll1ll1_opy_
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣ⑑").format(e))
    return binary_path
def bstack1llllll1ll1l_opy_(bstack1llll11lll1l_opy_):
    try:
        if bstack111ll_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨ⑒") not in bstack1llll11lll1l_opy_[bstack111ll_opy_ (u"ࠪࡳࡸ࠭⑓")].lower():
            return
        if os.path.exists(bstack111ll_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ⑔")):
            with open(bstack111ll_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ⑕"), bstack111ll_opy_ (u"ࠨࡲࠣ⑖")) as f:
                bstack1llll1lll1ll_opy_ = {}
                for line in f:
                    if bstack111ll_opy_ (u"ࠢ࠾ࠤ⑗") in line:
                        key, value = line.rstrip().split(bstack111ll_opy_ (u"ࠣ࠿ࠥ⑘"), 1)
                        bstack1llll1lll1ll_opy_[key] = value.strip(bstack111ll_opy_ (u"ࠩࠥࡠࠬ࠭⑙"))
                bstack1llll11lll1l_opy_[bstack111ll_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪ⑚")] = bstack1llll1lll1ll_opy_.get(bstack111ll_opy_ (u"ࠦࡎࡊࠢ⑛"), bstack111ll_opy_ (u"ࠧࠨ⑜"))
        elif os.path.exists(bstack111ll_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡦࡲࡰࡪࡰࡨ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧ⑝")):
            bstack1llll11lll1l_opy_[bstack111ll_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧ⑞")] = bstack111ll_opy_ (u"ࠨࡣ࡯ࡴ࡮ࡴࡥࠨ⑟")
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡧ࡭ࡸࡺࡲࡰࠢࡲࡪࠥࡲࡩ࡯ࡷࡻࠦ①") + e)
@measure(event_name=EVENTS.bstack11111l11ll1_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
def bstack1llll11l1ll1_opy_(bstack1lllll11l11l_opy_, bstack1llll1ll1l1l_opy_):
    logger.debug(bstack111ll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧ②") + str(bstack1lllll11l11l_opy_) + bstack111ll_opy_ (u"ࠦࠧ③"))
    zip_path = os.path.join(bstack1llll1ll1l1l_opy_, bstack111ll_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦ④"))
    bstack1lllll11l1l1_opy_ = bstack111ll_opy_ (u"࠭ࠧ⑤")
    with requests.get(bstack1lllll11l11l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack111ll_opy_ (u"ࠢࡸࡤࠥ⑥")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack111ll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥ⑦"))
    with zipfile.ZipFile(zip_path, bstack111ll_opy_ (u"ࠩࡵࠫ⑧")) as zip_ref:
        bstack1llll11ll111_opy_ = zip_ref.namelist()
        if len(bstack1llll11ll111_opy_) > 0:
            bstack1lllll11l1l1_opy_ = bstack1llll11ll111_opy_[0] # bstack1llll1111l11_opy_ bstack111111l111l_opy_ will be bstack1lllll1l11l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1llll1ll1l1l_opy_)
        logger.debug(bstack111ll_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤ⑨") + str(bstack1llll1ll1l1l_opy_) + bstack111ll_opy_ (u"ࠦࠬࠨ⑩"))
    os.remove(zip_path)
    return bstack1lllll11l1l1_opy_
def get_cli_dir():
    bstack1lllll1ll11l_opy_ = bstack11ll11l1lll_opy_()
    if bstack1lllll1ll11l_opy_:
        bstack1ll1l111l1l_opy_ = os.path.join(bstack1lllll1ll11l_opy_, bstack111ll_opy_ (u"ࠧࡩ࡬ࡪࠤ⑪"))
        if not os.path.exists(bstack1ll1l111l1l_opy_):
            os.makedirs(bstack1ll1l111l1l_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l111l1l_opy_
    else:
        raise FileNotFoundError(bstack111ll_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤ⑫"))
def bstack1ll1l1111l1_opy_(bstack1ll1l111l1l_opy_):
    bstack111ll_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦ⑬")
    bstack1lllll1lll11_opy_ = [
        os.path.join(bstack1ll1l111l1l_opy_, f)
        for f in os.listdir(bstack1ll1l111l1l_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l111l1l_opy_, f)) and f.startswith(bstack111ll_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤ⑭"))
    ]
    if len(bstack1lllll1lll11_opy_) > 0:
        return max(bstack1lllll1lll11_opy_, key=os.path.getmtime) # get bstack1llll1llll11_opy_ binary
    return bstack111ll_opy_ (u"ࠤࠥ⑮")
def bstack1111ll111ll_opy_():
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
def bstack11l1llll1l_opy_(data, keys, default=None):
    bstack111ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡦ࡬ࡥ࡭ࡻࠣ࡫ࡪࡺࠠࡢࠢࡱࡩࡸࡺࡥࡥࠢࡹࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩࡧࡴࡢ࠼ࠣࡘ࡭࡫ࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸࠥࡺ࡯ࠡࡶࡵࡥࡻ࡫ࡲࡴࡧ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡ࡭ࡨࡽࡸࡀࠠࡂࠢ࡯࡭ࡸࡺࠠࡰࡨࠣ࡯ࡪࡿࡳ࠰࡫ࡱࡨ࡮ࡩࡥࡴࠢࡵࡩࡵࡸࡥࡴࡧࡱࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡨࡪࡦࡻ࡬ࡵ࠼࡚ࠣࡦࡲࡵࡦࠢࡷࡳࠥࡸࡥࡵࡷࡵࡲࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡶࡪࡺࡵࡳࡰ࠽ࠤ࡙࡮ࡥࠡࡸࡤࡰࡺ࡫ࠠࡢࡶࠣࡸ࡭࡫ࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡣࡷ࡬࠱ࠦ࡯ࡳࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ⑯")
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
def bstack11l1l111ll_opy_(bstack1lllll111ll1_opy_, key, value):
    bstack111ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡺ࡯ࡳࡧࠣࡇࡑࡏࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠡ࡯ࡤࡴࡵ࡯࡮ࡨࠢ࡬ࡲࠥࡺࡨࡦࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣ࡭࡫ࡢࡩࡳࡼ࡟ࡷࡣࡵࡷࡤࡳࡡࡱ࠼ࠣࡈ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠢࡰࡥࡵࡶࡩ࡯ࡩࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡏࡪࡿࠠࡧࡴࡲࡱࠥࡉࡌࡊࡡࡆࡅࡕ࡙࡟ࡕࡑࡢࡇࡔࡔࡆࡊࡉࠍࠤࠥࠦࠠࠡࠢࠣࠤࡻࡧ࡬ࡶࡧ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࡯࡭ࡳ࡫ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠍࠤࠥࠦࠠࠣࠤࠥ⑰")
    if key in bstack1lll11l111_opy_:
        bstack1l1l11l1l1_opy_ = bstack1lll11l111_opy_[key]
        if isinstance(bstack1l1l11l1l1_opy_, list):
            for env_name in bstack1l1l11l1l1_opy_:
                bstack1lllll111ll1_opy_[env_name] = value
        else:
            bstack1lllll111ll1_opy_[bstack1l1l11l1l1_opy_] = value