# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
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
from unittest import result
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11l11l1lll_opy_, bstack1ll11lll1l_opy_, bstack11111l1l_opy_,
                                    bstack11l1ll11ll1_opy_, bstack11l1ll11lll_opy_, bstack11l1lll1lll_opy_, bstack11l1ll1l111_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l111l1l1l_opy_, bstack111llll11l_opy_
from bstack_utils.proxy import bstack11llllll11_opy_, bstack111l1l1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1lll1l1l1l_opy_
from bstack_utils.bstack11l1l111l1_opy_ import bstack1111l1lll_opy_
from browserstack_sdk._version import __version__
bstack111lllll11_opy_ = Config.bstack1lll111l1l_opy_()
logger = bstack1lll1l1l1l_opy_.get_logger(__name__, bstack1lll1l1l1l_opy_.bstack1llll11l1l1_opy_())
def bstack11ll11ll1l1_opy_(config):
    return config[bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᬀ")]
def bstack11ll1ll11l1_opy_(config):
    return config[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᬁ")]
def bstack1ll1l1ll1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111lll11ll1_opy_(obj):
    values = []
    bstack111ll1l1l1l_opy_ = re.compile(bstack1l11ll1_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᬂ"), re.I)
    for key in obj.keys():
        if bstack111ll1l1l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11ll11ll_opy_(config):
    tags = []
    tags.extend(bstack111lll11ll1_opy_(os.environ))
    tags.extend(bstack111lll11ll1_opy_(config))
    return tags
def bstack11l11ll11l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111lll1ll11_opy_(bstack11l11ll111l_opy_):
    if not bstack11l11ll111l_opy_:
        return bstack1l11ll1_opy_ (u"࠭ࠧᬃ")
    return bstack1l11ll1_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣᬄ").format(bstack11l11ll111l_opy_.name, bstack11l11ll111l_opy_.email)
def bstack11ll11ll111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l11ll1lll_opy_ = repo.common_dir
        info = {
            bstack1l11ll1_opy_ (u"ࠣࡵ࡫ࡥࠧᬅ"): repo.head.commit.hexsha,
            bstack1l11ll1_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧᬆ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l11ll1_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᬇ"): repo.active_branch.name,
            bstack1l11ll1_opy_ (u"ࠦࡹࡧࡧࠣᬈ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l11ll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᬉ"): bstack111lll1ll11_opy_(repo.head.commit.committer),
            bstack1l11ll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᬊ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l11ll1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᬋ"): bstack111lll1ll11_opy_(repo.head.commit.author),
            bstack1l11ll1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᬌ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l11ll1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᬍ"): repo.head.commit.message,
            bstack1l11ll1_opy_ (u"ࠥࡶࡴࡵࡴࠣᬎ"): repo.git.rev_parse(bstack1l11ll1_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᬏ")),
            bstack1l11ll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᬐ"): bstack11l11ll1lll_opy_,
            bstack1l11ll1_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᬑ"): subprocess.check_output([bstack1l11ll1_opy_ (u"ࠢࡨ࡫ࡷࠦᬒ"), bstack1l11ll1_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᬓ"), bstack1l11ll1_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᬔ")]).strip().decode(
                bstack1l11ll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᬕ")),
            bstack1l11ll1_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᬖ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l11ll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᬗ"): repo.git.rev_list(
                bstack1l11ll1_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᬘ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l111l11l1_opy_ = []
        for remote in remotes:
            bstack111lll1111l_opy_ = {
                bstack1l11ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬙ"): remote.name,
                bstack1l11ll1_opy_ (u"ࠣࡷࡵࡰࠧᬚ"): remote.url,
            }
            bstack11l111l11l1_opy_.append(bstack111lll1111l_opy_)
        bstack11l11111l1l_opy_ = {
            bstack1l11ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬛ"): bstack1l11ll1_opy_ (u"ࠥ࡫࡮ࡺࠢᬜ"),
            **info,
            bstack1l11ll1_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧᬝ"): bstack11l111l11l1_opy_
        }
        bstack11l11111l1l_opy_ = bstack11l111lll11_opy_(bstack11l11111l1l_opy_)
        return bstack11l11111l1l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l11ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᬞ").format(err))
        return {}
def bstack111llll1lll_opy_(bstack111llll11ll_opy_=None):
    bstack1l11ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࡥࡱࡲࡹࠡࡨࡲࡶࡲࡧࡴࡵࡧࡧࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࡶࡵࡨࠤࡨࡧࡳࡦࡵࠣࡪࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬࡯࡭ࡦࡨࡶࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࠫࡰ࡮ࡹࡴ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡧࡱ࡯ࡨࡪࡸࠠࡱࡣࡷ࡬ࡸࠦࡴࡰࠢࡨࡼࡹࡸࡡࡤࡶࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡶࡴࡳ࠮ࠡࡆࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴ࡛ࠦࡰࡵ࠱࡫ࡪࡺࡣࡸࡦࠫ࠭ࡢ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡭࡫ࡶࡸ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡥ࡫ࡦࡸࡸ࠲ࠠࡦࡣࡦ࡬ࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡲࡶࠥࡧࠠࡧࡱ࡯ࡨࡪࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᬟ")
    if not bstack111llll11ll_opy_: # bstack111ll1lllll_opy_ for bstack11l11111l11_opy_-repo
        bstack111llll11ll_opy_ = [os.getcwd()]
    results = []
    for folder in bstack111llll11ll_opy_:
        try:
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l11ll1_opy_ (u"ࠢࡱࡴࡌࡨࠧᬠ"): bstack1l11ll1_opy_ (u"ࠣࠤᬡ"),
                bstack1l11ll1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᬢ"): [],
                bstack1l11ll1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᬣ"): [],
                bstack1l11ll1_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦᬤ"): bstack1l11ll1_opy_ (u"ࠧࠨᬥ"),
                bstack1l11ll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢᬦ"): [],
                bstack1l11ll1_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᬧ"): bstack1l11ll1_opy_ (u"ࠣࠤᬨ"),
                bstack1l11ll1_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤᬩ"): bstack1l11ll1_opy_ (u"ࠥࠦᬪ"),
                bstack1l11ll1_opy_ (u"ࠦࡵࡸࡒࡢࡹࡇ࡭࡫࡬ࠢᬫ"): bstack1l11ll1_opy_ (u"ࠧࠨᬬ")
            }
            bstack11l1111llll_opy_ = repo.active_branch.name
            bstack11l1111111l_opy_ = repo.head.commit
            result[bstack1l11ll1_opy_ (u"ࠨࡰࡳࡋࡧࠦᬭ")] = bstack11l1111111l_opy_.hexsha
            bstack111ll11ll1l_opy_ = _11l11l1l11l_opy_(repo)
            logger.debug(bstack1l11ll1_opy_ (u"ࠢࡃࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳࡀࠠࠣᬮ") + str(bstack111ll11ll1l_opy_) + bstack1l11ll1_opy_ (u"ࠣࠤᬯ"))
            if bstack111ll11ll1l_opy_:
                try:
                    bstack11l11l11ll1_opy_ = repo.git.diff(bstack1l11ll1_opy_ (u"ࠤ࠰࠱ࡳࡧ࡭ࡦ࠯ࡲࡲࡱࡿࠢᬰ"), bstack1llll111ll1_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢᬱ")).split(bstack1l11ll1_opy_ (u"ࠫࡡࡴࠧᬲ"))
                    logger.debug(bstack1l11ll1_opy_ (u"ࠧࡉࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥࡨࡥࡵࡹࡨࡩࡳࠦࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂࠦࡡ࡯ࡦࠣࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࡀࠠࠣᬳ") + str(bstack11l11l11ll1_opy_) + bstack1l11ll1_opy_ (u"ࠨ᬴ࠢ"))
                    result[bstack1l11ll1_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᬵ")] = [f.strip() for f in bstack11l11l11ll1_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1llll111ll1_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧᬶ")))
                except Exception:
                    logger.debug(bstack1l11ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡣࡴࡤࡲࡨ࡮ࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠲ࠥࡌࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡳࡧࡦࡩࡳࡺࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠤᬷ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l11ll1_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᬸ")] = _11l11111lll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l11ll1_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᬹ")] = _11l11111lll_opy_(commits[:5])
            bstack111lllll1l1_opy_ = set()
            bstack11l11lllll1_opy_ = []
            for commit in commits:
                logger.debug(bstack1l11ll1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡩࡵ࠼ࠣࠦᬺ") + str(commit.message) + bstack1l11ll1_opy_ (u"ࠨࠢᬻ"))
                bstack11l111lll1l_opy_ = commit.author.name if commit.author else bstack1l11ll1_opy_ (u"ࠢࡖࡰ࡮ࡲࡴࡽ࡮ࠣᬼ")
                bstack111lllll1l1_opy_.add(bstack11l111lll1l_opy_)
                bstack11l11lllll1_opy_.append({
                    bstack1l11ll1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᬽ"): commit.message.strip(),
                    bstack1l11ll1_opy_ (u"ࠤࡸࡷࡪࡸࠢᬾ"): bstack11l111lll1l_opy_
                })
            result[bstack1l11ll1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᬿ")] = list(bstack111lllll1l1_opy_)
            result[bstack1l11ll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧᭀ")] = bstack11l11lllll1_opy_
            result[bstack1l11ll1_opy_ (u"ࠧࡶࡲࡅࡣࡷࡩࠧᭁ")] = bstack11l1111111l_opy_.committed_datetime.strftime(bstack1l11ll1_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࠣᭂ"))
            if (not result[bstack1l11ll1_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᭃ")] or result[bstack1l11ll1_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ᭄")].strip() == bstack1l11ll1_opy_ (u"ࠤࠥᭅ")) and bstack11l1111111l_opy_.message:
                bstack111llll1ll1_opy_ = bstack11l1111111l_opy_.message.strip().splitlines()
                result[bstack1l11ll1_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦᭆ")] = bstack111llll1ll1_opy_[0] if bstack111llll1ll1_opy_ else bstack1l11ll1_opy_ (u"ࠦࠧᭇ")
                if len(bstack111llll1ll1_opy_) > 2:
                    result[bstack1l11ll1_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧᭈ")] = bstack1l11ll1_opy_ (u"࠭࡜࡯ࠩᭉ").join(bstack111llll1ll1_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1l11ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࠮ࡦࡰ࡮ࡧࡩࡷࡀࠠࡼࡨࡲࡰࡩ࡫ࡲࡾࠫ࠽ࠤࠧᭊ") + str(err) + bstack1l11ll1_opy_ (u"ࠣࠤᭋ"))
    filtered_results = [
        r
        for r in results
        if _11l1111l1ll_opy_(r)
    ]
    return filtered_results
def _11l1111l1ll_opy_(result):
    bstack1l11ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡩࡱࡶࡥࡳࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡢࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡷࡺࡲࡴࠡ࡫ࡶࠤࡻࡧ࡬ࡪࡦࠣࠬࡳࡵ࡮࠮ࡧࡰࡴࡹࡿࠠࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠦࡡ࡯ࡦࠣࡥࡺࡺࡨࡰࡴࡶ࠭࠳ࠐࠠࠡࠢࠣࠦࠧࠨᭌ")
    return (
        isinstance(result.get(bstack1l11ll1_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤ᭍"), None), list)
        and len(result[bstack1l11ll1_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ᭎")]) > 0
        and isinstance(result.get(bstack1l11ll1_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ᭏"), None), list)
        and len(result[bstack1l11ll1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢ᭐")]) > 0
    )
def _11l11l1l11l_opy_(repo):
    bstack1l11ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡕࡴࡼࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸ࡭࡫ࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡸࡥࡱࡱࠣࡻ࡮ࡺࡨࡰࡷࡷࠤ࡭ࡧࡲࡥࡥࡲࡨࡪࡪࠠ࡯ࡣࡰࡩࡸࠦࡡ࡯ࡦࠣࡻࡴࡸ࡫ࠡࡹ࡬ࡸ࡭ࠦࡡ࡭࡮࡚ࠣࡈ࡙ࠠࡱࡴࡲࡺ࡮ࡪࡥࡳࡵ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡤࡦࡨࡤࡹࡱࡺࠠࡣࡴࡤࡲࡨ࡮ࠠࡪࡨࠣࡴࡴࡹࡳࡪࡤ࡯ࡩ࠱ࠦࡥ࡭ࡵࡨࠤࡓࡵ࡮ࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ᭑")
    try:
        try:
            origin = repo.remotes.origin
            bstack111lll11lll_opy_ = origin.refs[bstack1l11ll1_opy_ (u"ࠨࡊࡈࡅࡉ࠭᭒")]
            target = bstack111lll11lll_opy_.reference.name
            if target.startswith(bstack1l11ll1_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪ᭓")):
                return target
        except Exception:
            pass
        if repo.heads:
            return repo.heads[0].name
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1l11ll1_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫ᭔")):
                    return ref.name
    except Exception:
        pass
    return None
def _11l11111lll_opy_(commits):
    bstack1l11ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡢࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᭕")
    bstack11l11l11ll1_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11l1l111111_opy_ in diff:
                        if bstack11l1l111111_opy_.a_path:
                            bstack11l11l11ll1_opy_.add(bstack11l1l111111_opy_.a_path)
                        if bstack11l1l111111_opy_.b_path:
                            bstack11l11l11ll1_opy_.add(bstack11l1l111111_opy_.b_path)
    except Exception:
        pass
    return list(bstack11l11l11ll1_opy_)
def bstack11l111lll11_opy_(bstack11l11111l1l_opy_):
    bstack111ll11ll11_opy_ = bstack111lllll111_opy_(bstack11l11111l1l_opy_)
    if bstack111ll11ll11_opy_ and bstack111ll11ll11_opy_ > bstack11l1ll11ll1_opy_:
        bstack11l111ll1l1_opy_ = bstack111ll11ll11_opy_ - bstack11l1ll11ll1_opy_
        bstack111lllllll1_opy_ = bstack111ll1l11ll_opy_(bstack11l11111l1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᭖")], bstack11l111ll1l1_opy_)
        bstack11l11111l1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᭗")] = bstack111lllllll1_opy_
        logger.info(bstack1l11ll1_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤ᭘")
                    .format(bstack111lllll111_opy_(bstack11l11111l1l_opy_) / 1024))
    return bstack11l11111l1l_opy_
def bstack111lllll111_opy_(bstack1lll111ll1_opy_):
    try:
        if bstack1lll111ll1_opy_:
            bstack111ll11llll_opy_ = json.dumps(bstack1lll111ll1_opy_)
            bstack11l11l11l1l_opy_ = sys.getsizeof(bstack111ll11llll_opy_)
            return bstack11l11l11l1l_opy_
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣ᭙").format(e))
    return -1
def bstack111ll1l11ll_opy_(field, bstack11l11lll111_opy_):
    try:
        bstack111lll111ll_opy_ = len(bytes(bstack11l1ll11lll_opy_, bstack1l11ll1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᭚")))
        bstack111llll1l11_opy_ = bytes(field, bstack1l11ll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᭛"))
        bstack11l1111ll1l_opy_ = len(bstack111llll1l11_opy_)
        bstack111ll1lll11_opy_ = ceil(bstack11l1111ll1l_opy_ - bstack11l11lll111_opy_ - bstack111lll111ll_opy_)
        if bstack111ll1lll11_opy_ > 0:
            bstack111llllll1l_opy_ = bstack111llll1l11_opy_[:bstack111ll1lll11_opy_].decode(bstack1l11ll1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᭜"), errors=bstack1l11ll1_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬ᭝")) + bstack11l1ll11lll_opy_
            return bstack111llllll1l_opy_
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦ᭞").format(e))
    return field
def bstack1lll11ll1l_opy_():
    env = os.environ
    if (bstack1l11ll1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᭟") in env and len(env[bstack1l11ll1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ᭠")]) > 0) or (
            bstack1l11ll1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᭡") in env and len(env[bstack1l11ll1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᭢")]) > 0):
        return {
            bstack1l11ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭣"): bstack1l11ll1_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨ᭤"),
            bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᭥"): env.get(bstack1l11ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᭦")),
            bstack1l11ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᭧"): env.get(bstack1l11ll1_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦ᭨")),
            bstack1l11ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭩"): env.get(bstack1l11ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᭪"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠧࡉࡉࠣ᭫")) == bstack1l11ll1_opy_ (u"ࠨࡴࡳࡷࡨ᭬ࠦ") and bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ᭭"))):
        return {
            bstack1l11ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭮"): bstack1l11ll1_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦ᭯"),
            bstack1l11ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᭰"): env.get(bstack1l11ll1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᭱")),
            bstack1l11ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᭲"): env.get(bstack1l11ll1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥ᭳")),
            bstack1l11ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᭴"): env.get(bstack1l11ll1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦ᭵"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠤࡆࡍࠧ᭶")) == bstack1l11ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣ᭷") and bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦ᭸"))):
        return {
            bstack1l11ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᭹"): bstack1l11ll1_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤ᭺"),
            bstack1l11ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᭻"): env.get(bstack1l11ll1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣ᭼")),
            bstack1l11ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᭽"): env.get(bstack1l11ll1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᭾")),
            bstack1l11ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᭿"): env.get(bstack1l11ll1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᮀ"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠨࡃࡊࠤᮁ")) == bstack1l11ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᮂ") and env.get(bstack1l11ll1_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᮃ")) == bstack1l11ll1_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᮄ"):
        return {
            bstack1l11ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᮅ"): bstack1l11ll1_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᮆ"),
            bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮇ"): None,
            bstack1l11ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᮈ"): None,
            bstack1l11ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮉ"): None
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᮊ")) and env.get(bstack1l11ll1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᮋ")):
        return {
            bstack1l11ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᮌ"): bstack1l11ll1_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᮍ"),
            bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮎ"): env.get(bstack1l11ll1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᮏ")),
            bstack1l11ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮐ"): None,
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮑ"): env.get(bstack1l11ll1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᮒ"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠥࡇࡎࠨᮓ")) == bstack1l11ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤᮔ") and bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᮕ"))):
        return {
            bstack1l11ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᮖ"): bstack1l11ll1_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᮗ"),
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮘ"): env.get(bstack1l11ll1_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᮙ")),
            bstack1l11ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮚ"): None,
            bstack1l11ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᮛ"): env.get(bstack1l11ll1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᮜ"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠨࡃࡊࠤᮝ")) == bstack1l11ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᮞ") and bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᮟ"))):
        return {
            bstack1l11ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮠ"): bstack1l11ll1_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᮡ"),
            bstack1l11ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᮢ"): env.get(bstack1l11ll1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᮣ")),
            bstack1l11ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᮤ"): env.get(bstack1l11ll1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᮥ")),
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮦ"): env.get(bstack1l11ll1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᮧ"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠥࡇࡎࠨᮨ")) == bstack1l11ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤᮩ") and bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉ᮪ࠣ"))):
        return {
            bstack1l11ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᮫ࠦ"): bstack1l11ll1_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᮬ"),
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮭ"): env.get(bstack1l11ll1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᮮ")),
            bstack1l11ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮯ"): env.get(bstack1l11ll1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᮰")),
            bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᮱"): env.get(bstack1l11ll1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤ᮲"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠢࡄࡋࠥ᮳")) == bstack1l11ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨ᮴") and bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧ᮵"))):
        return {
            bstack1l11ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᮶"): bstack1l11ll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢ᮷"),
            bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᮸"): env.get(bstack1l11ll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᮹")),
            bstack1l11ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮺ"): env.get(bstack1l11ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᮻ")) or env.get(bstack1l11ll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᮼ")),
            bstack1l11ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮽ"): env.get(bstack1l11ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᮾ"))
        }
    if bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᮿ"))):
        return {
            bstack1l11ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᯀ"): bstack1l11ll1_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᯁ"),
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᯂ"): bstack1l11ll1_opy_ (u"ࠤࡾࢁࢀࢃࠢᯃ").format(env.get(bstack1l11ll1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᯄ")), env.get(bstack1l11ll1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᯅ"))),
            bstack1l11ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᯆ"): env.get(bstack1l11ll1_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᯇ")),
            bstack1l11ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᯈ"): env.get(bstack1l11ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᯉ"))
        }
    if bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᯊ"))):
        return {
            bstack1l11ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᯋ"): bstack1l11ll1_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᯌ"),
            bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯍ"): bstack1l11ll1_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᯎ").format(env.get(bstack1l11ll1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ᯏ")), env.get(bstack1l11ll1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᯐ")), env.get(bstack1l11ll1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᯑ")), env.get(bstack1l11ll1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᯒ"))),
            bstack1l11ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᯓ"): env.get(bstack1l11ll1_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᯔ")),
            bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᯕ"): env.get(bstack1l11ll1_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᯖ"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᯗ")) and env.get(bstack1l11ll1_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᯘ")):
        return {
            bstack1l11ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᯙ"): bstack1l11ll1_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᯚ"),
            bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯛ"): bstack1l11ll1_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᯜ").format(env.get(bstack1l11ll1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᯝ")), env.get(bstack1l11ll1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ᯞ")), env.get(bstack1l11ll1_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᯟ"))),
            bstack1l11ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᯠ"): env.get(bstack1l11ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᯡ")),
            bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᯢ"): env.get(bstack1l11ll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᯣ"))
        }
    if any([env.get(bstack1l11ll1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᯤ")), env.get(bstack1l11ll1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᯥ")), env.get(bstack1l11ll1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᯦"))]):
        return {
            bstack1l11ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᯧ"): bstack1l11ll1_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᯨ"),
            bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯩ"): env.get(bstack1l11ll1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᯪ")),
            bstack1l11ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᯫ"): env.get(bstack1l11ll1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᯬ")),
            bstack1l11ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᯭ"): env.get(bstack1l11ll1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᯮ"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᯯ")):
        return {
            bstack1l11ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯰ"): bstack1l11ll1_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᯱ"),
            bstack1l11ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᯲ࠥ"): env.get(bstack1l11ll1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮᯳ࠥ")),
            bstack1l11ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᯴"): env.get(bstack1l11ll1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤ᯵")),
            bstack1l11ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᯶"): env.get(bstack1l11ll1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ᯷"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢ᯸")) or env.get(bstack1l11ll1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤ᯹")):
        return {
            bstack1l11ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᯺"): bstack1l11ll1_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥ᯻"),
            bstack1l11ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᯼"): env.get(bstack1l11ll1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᯽")),
            bstack1l11ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᯾"): bstack1l11ll1_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨ᯿") if env.get(bstack1l11ll1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᰀ")) else None,
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰁ"): env.get(bstack1l11ll1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᰂ"))
        }
    if any([env.get(bstack1l11ll1_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᰃ")), env.get(bstack1l11ll1_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᰄ")), env.get(bstack1l11ll1_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᰅ"))]):
        return {
            bstack1l11ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰆ"): bstack1l11ll1_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᰇ"),
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰈ"): None,
            bstack1l11ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᰉ"): env.get(bstack1l11ll1_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᰊ")),
            bstack1l11ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᰋ"): env.get(bstack1l11ll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᰌ"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᰍ")):
        return {
            bstack1l11ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᰎ"): bstack1l11ll1_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦᰏ"),
            bstack1l11ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᰐ"): env.get(bstack1l11ll1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᰑ")),
            bstack1l11ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᰒ"): bstack1l11ll1_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᰓ").format(env.get(bstack1l11ll1_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᰔ"))) if env.get(bstack1l11ll1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᰕ")) else None,
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰖ"): env.get(bstack1l11ll1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᰗ"))
        }
    if bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᰘ"))):
        return {
            bstack1l11ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᰙ"): bstack1l11ll1_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᰚ"),
            bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᰛ"): env.get(bstack1l11ll1_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦᰜ")),
            bstack1l11ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᰝ"): env.get(bstack1l11ll1_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧᰞ")),
            bstack1l11ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰟ"): env.get(bstack1l11ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᰠ"))
        }
    if bstack11l1ll11l1_opy_(env.get(bstack1l11ll1_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᰡ"))):
        return {
            bstack1l11ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰢ"): bstack1l11ll1_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᰣ"),
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰤ"): bstack1l11ll1_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᰥ").format(env.get(bstack1l11ll1_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᰦ")), env.get(bstack1l11ll1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᰧ")), env.get(bstack1l11ll1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᰨ"))),
            bstack1l11ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᰩ"): env.get(bstack1l11ll1_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᰪ")),
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰫ"): env.get(bstack1l11ll1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᰬ"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠥࡇࡎࠨᰭ")) == bstack1l11ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤᰮ") and env.get(bstack1l11ll1_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᰯ")) == bstack1l11ll1_opy_ (u"ࠨ࠱ࠣᰰ"):
        return {
            bstack1l11ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᰱ"): bstack1l11ll1_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᰲ"),
            bstack1l11ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᰳ"): bstack1l11ll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᰴ").format(env.get(bstack1l11ll1_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᰵ"))),
            bstack1l11ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᰶ"): None,
            bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ᰷ࠧ"): None,
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ᰸")):
        return {
            bstack1l11ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᰹"): bstack1l11ll1_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦ᰺"),
            bstack1l11ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᰻"): None,
            bstack1l11ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᰼"): env.get(bstack1l11ll1_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨ᰽")),
            bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᰾"): env.get(bstack1l11ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᰿"))
        }
    if any([env.get(bstack1l11ll1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦ᱀")), env.get(bstack1l11ll1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤ᱁")), env.get(bstack1l11ll1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣ᱂")), env.get(bstack1l11ll1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧ᱃"))]):
        return {
            bstack1l11ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᱄"): bstack1l11ll1_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤ᱅"),
            bstack1l11ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᱆"): None,
            bstack1l11ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᱇"): env.get(bstack1l11ll1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᱈")) or None,
            bstack1l11ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᱉"): env.get(bstack1l11ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᱊"), 0)
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᱋")):
        return {
            bstack1l11ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᱌"): bstack1l11ll1_opy_ (u"ࠢࡈࡱࡆࡈࠧᱍ"),
            bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᱎ"): None,
            bstack1l11ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᱏ"): env.get(bstack1l11ll1_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᱐")),
            bstack1l11ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᱑"): env.get(bstack1l11ll1_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦ᱒"))
        }
    if env.get(bstack1l11ll1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᱓")):
        return {
            bstack1l11ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᱔"): bstack1l11ll1_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦ᱕"),
            bstack1l11ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᱖"): env.get(bstack1l11ll1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᱗")),
            bstack1l11ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᱘"): env.get(bstack1l11ll1_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣ᱙")),
            bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᱚ"): env.get(bstack1l11ll1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᱛ"))
        }
    return {bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᱜ"): None}
def get_host_info():
    return {
        bstack1l11ll1_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᱝ"): platform.node(),
        bstack1l11ll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᱞ"): platform.system(),
        bstack1l11ll1_opy_ (u"ࠦࡹࡿࡰࡦࠤᱟ"): platform.machine(),
        bstack1l11ll1_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᱠ"): platform.version(),
        bstack1l11ll1_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᱡ"): platform.architecture()[0]
    }
def bstack1l11l1l1ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111ll1ll1l1_opy_():
    if bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᱢ")):
        return bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᱣ")
    return bstack1l11ll1_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᱤ")
def bstack11l11lll1l1_opy_(driver):
    info = {
        bstack1l11ll1_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᱥ"): driver.capabilities,
        bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᱦ"): driver.session_id,
        bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᱧ"): driver.capabilities.get(bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᱨ"), None),
        bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᱩ"): driver.capabilities.get(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᱪ"), None),
        bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᱫ"): driver.capabilities.get(bstack1l11ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᱬ"), None),
        bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᱭ"):driver.capabilities.get(bstack1l11ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᱮ"), None),
    }
    if bstack111ll1ll1l1_opy_() == bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᱯ"):
        if bstack111l1111_opy_():
            info[bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᱰ")] = bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᱱ")
        elif driver.capabilities.get(bstack1l11ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᱲ"), {}).get(bstack1l11ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᱳ"), False):
            info[bstack1l11ll1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᱴ")] = bstack1l11ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᱵ")
        else:
            info[bstack1l11ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᱶ")] = bstack1l11ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᱷ")
    return info
def bstack111l1111_opy_():
    if bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᱸ")):
        return True
    if bstack11l1ll11l1_opy_(os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᱹ"), None)):
        return True
    return False
def bstack1l1ll1ll1l_opy_(bstack111lll1llll_opy_, url, data, config):
    headers = config.get(bstack1l11ll1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᱺ"), None)
    proxies = bstack11llllll11_opy_(config, url)
    auth = config.get(bstack1l11ll1_opy_ (u"ࠫࡦࡻࡴࡩࠩᱻ"), None)
    response = requests.request(
            bstack111lll1llll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11ll1lllll_opy_(bstack1llll11l11_opy_, size):
    bstack1ll1111l11_opy_ = []
    while len(bstack1llll11l11_opy_) > size:
        bstack1l1l11llll_opy_ = bstack1llll11l11_opy_[:size]
        bstack1ll1111l11_opy_.append(bstack1l1l11llll_opy_)
        bstack1llll11l11_opy_ = bstack1llll11l11_opy_[size:]
    bstack1ll1111l11_opy_.append(bstack1llll11l11_opy_)
    return bstack1ll1111l11_opy_
def bstack111ll1l1ll1_opy_(message, bstack11l11111ll1_opy_=False):
    os.write(1, bytes(message, bstack1l11ll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᱼ")))
    os.write(1, bytes(bstack1l11ll1_opy_ (u"࠭࡜࡯ࠩᱽ"), bstack1l11ll1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᱾")))
    if bstack11l11111ll1_opy_:
        with open(bstack1l11ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧ᱿") + os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᲀ")] + bstack1l11ll1_opy_ (u"ࠪ࠲ࡱࡵࡧࠨᲁ"), bstack1l11ll1_opy_ (u"ࠫࡦ࠭ᲂ")) as f:
            f.write(message + bstack1l11ll1_opy_ (u"ࠬࡢ࡮ࠨᲃ"))
def bstack1l1lll11ll1_opy_():
    return os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᲄ")].lower() == bstack1l11ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬᲅ")
def bstack1ll11l1ll1_opy_():
    return bstack1111ll11l1_opy_().replace(tzinfo=None).isoformat() + bstack1l11ll1_opy_ (u"ࠨ࡜ࠪᲆ")
def bstack11l11l1ll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l11ll1_opy_ (u"ࠩ࡝ࠫᲇ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l11ll1_opy_ (u"ࠪ࡞ࠬᲈ")))).total_seconds() * 1000
def bstack111lll11111_opy_(timestamp):
    return bstack111ll1l1111_opy_(timestamp).isoformat() + bstack1l11ll1_opy_ (u"ࠫ࡟࠭Ᲊ")
def bstack11l111ll111_opy_(bstack11l11l1llll_opy_):
    date_format = bstack1l11ll1_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᲊ")
    bstack11l11l111l1_opy_ = datetime.datetime.strptime(bstack11l11l1llll_opy_, date_format)
    return bstack11l11l111l1_opy_.isoformat() + bstack1l11ll1_opy_ (u"࡚࠭ࠨ᲋")
def bstack11l11111111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l11ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᲌")
    else:
        return bstack1l11ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᲍")
def bstack11l1ll11l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l11ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᲎")
def bstack11l1111l11l_opy_(val):
    return val.__str__().lower() == bstack1l11ll1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ᲏")
def error_handler(bstack11l111l11ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l111l11ll_opy_ as e:
                print(bstack1l11ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᲐ").format(func.__name__, bstack11l111l11ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111ll1ll11l_opy_(bstack11l11l1l1l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11l1l1l1_opy_(cls, *args, **kwargs)
            except bstack11l111l11ll_opy_ as e:
                print(bstack1l11ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᲑ").format(bstack11l11l1l1l1_opy_.__name__, bstack11l111l11ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111ll1ll11l_opy_
    else:
        return decorator
def bstack1llll1llll_opy_(bstack11111l11ll_opy_):
    if os.getenv(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᲒ")) is not None:
        return bstack11l1ll11l1_opy_(os.getenv(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᲓ")))
    if bstack1l11ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲔ") in bstack11111l11ll_opy_ and bstack11l1111l11l_opy_(bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ვ")]):
        return False
    if bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲖ") in bstack11111l11ll_opy_ and bstack11l1111l11l_opy_(bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Თ")]):
        return False
    return True
def bstack1l11llll11_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11llll1l_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᲘ"), None)
        return bstack11l11llll1l_opy_ is None or bstack11l11llll1l_opy_ == bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᲙ")
    except Exception as e:
        return False
def bstack111111111_opy_(hub_url, CONFIG):
    if bstack11llll11ll_opy_() <= version.parse(bstack1l11ll1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᲚ")):
        if hub_url:
            return bstack1l11ll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᲛ") + hub_url + bstack1l11ll1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᲜ")
        return bstack1ll11lll1l_opy_
    if hub_url:
        return bstack1l11ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᲝ") + hub_url + bstack1l11ll1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᲞ")
    return bstack11111l1l_opy_
def bstack11l1111l111_opy_():
    return isinstance(os.getenv(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᲟ")), str)
def bstack1l1l1l11ll_opy_(url):
    return urlparse(url).hostname
def bstack111l1l1l1_opy_(hostname):
    for bstack1l1l11lll1_opy_ in bstack11l11l1lll_opy_:
        regex = re.compile(bstack1l1l11lll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111ll11lll1_opy_(bstack111lllll11l_opy_, file_name, logger):
    bstack1ll11l111_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"࠭ࡾࠨᲠ")), bstack111lllll11l_opy_)
    try:
        if not os.path.exists(bstack1ll11l111_opy_):
            os.makedirs(bstack1ll11l111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠧࡿࠩᲡ")), bstack111lllll11l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l11ll1_opy_ (u"ࠨࡹࠪᲢ")):
                pass
            with open(file_path, bstack1l11ll1_opy_ (u"ࠤࡺ࠯ࠧᲣ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l111l1l1l_opy_.format(str(e)))
def bstack111lll11l11_opy_(file_name, key, value, logger):
    file_path = bstack111ll11lll1_opy_(bstack1l11ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᲤ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1l11ll11_opy_ = json.load(open(file_path, bstack1l11ll1_opy_ (u"ࠫࡷࡨࠧᲥ")))
        else:
            bstack1l1l11ll11_opy_ = {}
        bstack1l1l11ll11_opy_[key] = value
        with open(file_path, bstack1l11ll1_opy_ (u"ࠧࡽࠫࠣᲦ")) as outfile:
            json.dump(bstack1l1l11ll11_opy_, outfile)
def bstack1l1ll1111l_opy_(file_name, logger):
    file_path = bstack111ll11lll1_opy_(bstack1l11ll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ყ"), file_name, logger)
    bstack1l1l11ll11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l11ll1_opy_ (u"ࠧࡳࠩᲨ")) as bstack11111ll1l_opy_:
            bstack1l1l11ll11_opy_ = json.load(bstack11111ll1l_opy_)
    return bstack1l1l11ll11_opy_
def bstack1l111l1ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬᲩ") + file_path + bstack1l11ll1_opy_ (u"ࠩࠣࠫᲪ") + str(e))
def bstack11llll11ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l11ll1_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧᲫ")
def bstack11lll11111_opy_(config):
    if bstack1l11ll1_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᲬ") in config:
        del (config[bstack1l11ll1_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᲭ")])
        return False
    if bstack11llll11ll_opy_() < version.parse(bstack1l11ll1_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬᲮ")):
        return False
    if bstack11llll11ll_opy_() >= version.parse(bstack1l11ll1_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭Ჯ")):
        return True
    if bstack1l11ll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᲰ") in config and config[bstack1l11ll1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᲱ")] is False:
        return False
    else:
        return True
def bstack11ll1111l1_opy_(args_list, bstack111lll11l1l_opy_):
    index = -1
    for value in bstack111lll11l1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1l1111l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1l1111l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111lll1111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111lll1111_opy_ = bstack111lll1111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l11ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᲲ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l11ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᲳ"), exception=exception)
    def bstack111111l1l1_opy_(self):
        if self.result != bstack1l11ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᲴ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l11ll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᲵ") in self.exception_type:
            return bstack1l11ll1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᲶ")
        return bstack1l11ll1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᲷ")
    def bstack11l11l1ll11_opy_(self):
        if self.result != bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᲸ"):
            return None
        if self.bstack111lll1111_opy_:
            return self.bstack111lll1111_opy_
        return bstack11l11ll1111_opy_(self.exception)
def bstack11l11ll1111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111llll1l1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l11111ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1ll111_opy_(config, logger):
    try:
        import playwright
        bstack11l11l1l111_opy_ = playwright.__file__
        bstack11l111l1l1l_opy_ = os.path.split(bstack11l11l1l111_opy_)
        bstack11l111llll1_opy_ = bstack11l111l1l1l_opy_[0] + bstack1l11ll1_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭Ჹ")
        os.environ[bstack1l11ll1_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧᲺ")] = bstack111l1l1l_opy_(config)
        with open(bstack11l111llll1_opy_, bstack1l11ll1_opy_ (u"ࠬࡸࠧ᲻")) as f:
            bstack1ll111l11_opy_ = f.read()
            bstack111llll111l_opy_ = bstack1l11ll1_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ᲼")
            bstack11l11l1lll1_opy_ = bstack1ll111l11_opy_.find(bstack111llll111l_opy_)
            if bstack11l11l1lll1_opy_ == -1:
              process = subprocess.Popen(bstack1l11ll1_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦᲽ"), shell=True, cwd=bstack11l111l1l1l_opy_[0])
              process.wait()
              bstack111ll1ll111_opy_ = bstack1l11ll1_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨᲾ")
              bstack111lll1l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨᲿ")
              bstack111lll1l111_opy_ = bstack1ll111l11_opy_.replace(bstack111ll1ll111_opy_, bstack111lll1l1ll_opy_)
              with open(bstack11l111llll1_opy_, bstack1l11ll1_opy_ (u"ࠪࡻࠬ᳀")) as f:
                f.write(bstack111lll1l111_opy_)
    except Exception as e:
        logger.error(bstack111llll11l_opy_.format(str(e)))
def bstack111111l11_opy_():
  try:
    bstack11l111l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ᳁"))
    bstack111lll1l1l1_opy_ = []
    if os.path.exists(bstack11l111l111l_opy_):
      with open(bstack11l111l111l_opy_) as f:
        bstack111lll1l1l1_opy_ = json.load(f)
      os.remove(bstack11l111l111l_opy_)
    return bstack111lll1l1l1_opy_
  except:
    pass
  return []
def bstack1ll111ll11_opy_(bstack11lll1l1ll_opy_):
  try:
    bstack111lll1l1l1_opy_ = []
    bstack11l111l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬ᳂"))
    if os.path.exists(bstack11l111l111l_opy_):
      with open(bstack11l111l111l_opy_) as f:
        bstack111lll1l1l1_opy_ = json.load(f)
    bstack111lll1l1l1_opy_.append(bstack11lll1l1ll_opy_)
    with open(bstack11l111l111l_opy_, bstack1l11ll1_opy_ (u"࠭ࡷࠨ᳃")) as f:
        json.dump(bstack111lll1l1l1_opy_, f)
  except:
    pass
def bstack1l1111l11_opy_(logger, bstack11l11l11lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ᳄"), bstack1l11ll1_opy_ (u"ࠨࠩ᳅"))
    if test_name == bstack1l11ll1_opy_ (u"ࠩࠪ᳆"):
        test_name = threading.current_thread().__dict__.get(bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩ᳇"), bstack1l11ll1_opy_ (u"ࠫࠬ᳈"))
    bstack111ll1lll1l_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠲ࠠࠨ᳉").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11l11lll_opy_:
        bstack1lll1ll111_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᳊"), bstack1l11ll1_opy_ (u"ࠧ࠱ࠩ᳋"))
        bstack1ll1111l_opy_ = {bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭᳌"): test_name, bstack1l11ll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᳍"): bstack111ll1lll1l_opy_, bstack1l11ll1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ᳎"): bstack1lll1ll111_opy_}
        bstack11l11llll11_opy_ = []
        bstack11l11ll1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ᳏"))
        if os.path.exists(bstack11l11ll1l11_opy_):
            with open(bstack11l11ll1l11_opy_) as f:
                bstack11l11llll11_opy_ = json.load(f)
        bstack11l11llll11_opy_.append(bstack1ll1111l_opy_)
        with open(bstack11l11ll1l11_opy_, bstack1l11ll1_opy_ (u"ࠬࡽࠧ᳐")) as f:
            json.dump(bstack11l11llll11_opy_, f)
    else:
        bstack1ll1111l_opy_ = {bstack1l11ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᳑"): test_name, bstack1l11ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᳒"): bstack111ll1lll1l_opy_, bstack1l11ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᳓"): str(multiprocessing.current_process().name)}
        if bstack1l11ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ᳔࠭") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1111l_opy_)
  except Exception as e:
      logger.warn(bstack1l11ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃ᳕ࠢ").format(e))
def bstack11ll11111l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l11ll1_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹ᳖ࠧ"))
    try:
      bstack11l1111l1l1_opy_ = []
      bstack1ll1111l_opy_ = {bstack1l11ll1_opy_ (u"ࠬࡴࡡ࡮ࡧ᳗ࠪ"): test_name, bstack1l11ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶ᳘ࠬ"): error_message, bstack1l11ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ᳙࠭"): index}
      bstack111lll1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ᳚"))
      if os.path.exists(bstack111lll1lll1_opy_):
          with open(bstack111lll1lll1_opy_) as f:
              bstack11l1111l1l1_opy_ = json.load(f)
      bstack11l1111l1l1_opy_.append(bstack1ll1111l_opy_)
      with open(bstack111lll1lll1_opy_, bstack1l11ll1_opy_ (u"ࠩࡺࠫ᳛")) as f:
          json.dump(bstack11l1111l1l1_opy_, f)
    except Exception as e:
      logger.warn(bstack1l11ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ᳜").format(e))
    return
  bstack11l1111l1l1_opy_ = []
  bstack1ll1111l_opy_ = {bstack1l11ll1_opy_ (u"ࠫࡳࡧ࡭ࡦ᳝ࠩ"): test_name, bstack1l11ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵ᳞ࠫ"): error_message, bstack1l11ll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ᳟ࠬ"): index}
  bstack111lll1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ᳠"))
  lock_file = bstack111lll1lll1_opy_ + bstack1l11ll1_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ᳡")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111lll1lll1_opy_):
          with open(bstack111lll1lll1_opy_, bstack1l11ll1_opy_ (u"ࠩࡵ᳢ࠫ")) as f:
              content = f.read().strip()
              if content:
                  bstack11l1111l1l1_opy_ = json.load(open(bstack111lll1lll1_opy_))
      bstack11l1111l1l1_opy_.append(bstack1ll1111l_opy_)
      with open(bstack111lll1lll1_opy_, bstack1l11ll1_opy_ (u"ࠪࡻ᳣ࠬ")) as f:
          json.dump(bstack11l1111l1l1_opy_, f)
  except Exception as e:
    logger.warn(bstack1l11ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀ᳤ࠦ").format(e))
def bstack11ll1lll1l_opy_(bstack1lll1l1ll1_opy_, name, logger):
  try:
    bstack1ll1111l_opy_ = {bstack1l11ll1_opy_ (u"ࠬࡴࡡ࡮ࡧ᳥ࠪ"): name, bstack1l11ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶ᳦ࠬ"): bstack1lll1l1ll1_opy_, bstack1l11ll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ᳧࠭"): str(threading.current_thread()._name)}
    return bstack1ll1111l_opy_
  except Exception as e:
    logger.warn(bstack1l11ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁ᳨ࠧ").format(e))
  return
def bstack11l11ll1l1l_opy_():
    return platform.system() == bstack1l11ll1_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪᳩ")
def bstack11l1llll_opy_(bstack11l11lll1ll_opy_, config, logger):
    bstack11l11l1l1ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l11lll1ll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᳪ").format(e))
    return bstack11l11l1l1ll_opy_
def bstack11l11l11l11_opy_(bstack11l1111ll11_opy_, bstack111ll1l1l11_opy_):
    bstack111lll111l1_opy_ = version.parse(bstack11l1111ll11_opy_)
    bstack11l111ll11l_opy_ = version.parse(bstack111ll1l1l11_opy_)
    if bstack111lll111l1_opy_ > bstack11l111ll11l_opy_:
        return 1
    elif bstack111lll111l1_opy_ < bstack11l111ll11l_opy_:
        return -1
    else:
        return 0
def bstack1111ll11l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111ll1l1111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11lll11l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l11l11ll_opy_(options, framework, config, bstack1ll1ll1111_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l11ll1_opy_ (u"ࠫ࡬࡫ࡴࠨᳫ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l111ll_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᳬ"))
    bstack11l111ll1ll_opy_ = True
    bstack11l11l1111_opy_ = os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇ᳭ࠫ")]
    bstack1ll11l11lll_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᳮ"), False)
    if bstack1ll11l11lll_opy_:
        bstack1lll11l1l1l_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᳯ"), {})
        bstack1lll11l1l1l_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᳰ")] = os.getenv(bstack1l11ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᳱ"))
        bstack11ll1ll111l_opy_ = json.loads(os.getenv(bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᳲ"), bstack1l11ll1_opy_ (u"ࠬࢁࡽࠨᳳ"))).get(bstack1l11ll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᳴"))
    if bstack11l1111l11l_opy_(caps.get(bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭ᳵ"))) or bstack11l1111l11l_opy_(caps.get(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᳶ"))):
        bstack11l111ll1ll_opy_ = False
    if bstack11lll11111_opy_({bstack1l11ll1_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ᳷"): bstack11l111ll1ll_opy_}):
        bstack11l111ll_opy_ = bstack11l111ll_opy_ or {}
        bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᳸")] = bstack11l11lll11l_opy_(framework)
        bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᳹")] = bstack1l1lll11ll1_opy_()
        bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᳺ")] = bstack11l11l1111_opy_
        bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᳻")] = bstack1ll1ll1111_opy_
        if bstack1ll11l11lll_opy_:
            bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᳼")] = bstack1ll11l11lll_opy_
            bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᳽")] = bstack1lll11l1l1l_opy_
            bstack11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳾")][bstack1l11ll1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᳿")] = bstack11ll1ll111l_opy_
        if getattr(options, bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᴀ"), None):
            options.set_capability(bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᴁ"), bstack11l111ll_opy_)
        else:
            options[bstack1l11ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᴂ")] = bstack11l111ll_opy_
    else:
        if getattr(options, bstack1l11ll1_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᴃ"), None):
            options.set_capability(bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴄ"), bstack11l11lll11l_opy_(framework))
            options.set_capability(bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴅ"), bstack1l1lll11ll1_opy_())
            options.set_capability(bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴆ"), bstack11l11l1111_opy_)
            options.set_capability(bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴇ"), bstack1ll1ll1111_opy_)
            if bstack1ll11l11lll_opy_:
                options.set_capability(bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴈ"), bstack1ll11l11lll_opy_)
                options.set_capability(bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᴉ"), bstack1lll11l1l1l_opy_)
                options.set_capability(bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᴊ"), bstack11ll1ll111l_opy_)
        else:
            options[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴋ")] = bstack11l11lll11l_opy_(framework)
            options[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴌ")] = bstack1l1lll11ll1_opy_()
            options[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴍ")] = bstack11l11l1111_opy_
            options[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴎ")] = bstack1ll1ll1111_opy_
            if bstack1ll11l11lll_opy_:
                options[bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴏ")] = bstack1ll11l11lll_opy_
                options[bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᴐ")] = bstack1lll11l1l1l_opy_
                options[bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴑ")][bstack1l11ll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᴒ")] = bstack11ll1ll111l_opy_
    return options
def bstack111ll1l111l_opy_(bstack111lll1l11l_opy_, framework):
    bstack1ll1ll1111_opy_ = bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᴓ"))
    if bstack111lll1l11l_opy_ and len(bstack111lll1l11l_opy_.split(bstack1l11ll1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᴔ"))) > 1:
        ws_url = bstack111lll1l11l_opy_.split(bstack1l11ll1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᴕ"))[0]
        if bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᴖ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111llll1111_opy_ = json.loads(urllib.parse.unquote(bstack111lll1l11l_opy_.split(bstack1l11ll1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᴗ"))[1]))
            bstack111llll1111_opy_ = bstack111llll1111_opy_ or {}
            bstack11l11l1111_opy_ = os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᴘ")]
            bstack111llll1111_opy_[bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴙ")] = str(framework) + str(__version__)
            bstack111llll1111_opy_[bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴚ")] = bstack1l1lll11ll1_opy_()
            bstack111llll1111_opy_[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴛ")] = bstack11l11l1111_opy_
            bstack111llll1111_opy_[bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴜ")] = bstack1ll1ll1111_opy_
            bstack111lll1l11l_opy_ = bstack111lll1l11l_opy_.split(bstack1l11ll1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᴝ"))[0] + bstack1l11ll1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᴞ") + urllib.parse.quote(json.dumps(bstack111llll1111_opy_))
    return bstack111lll1l11l_opy_
def bstack1l11ll11l_opy_():
    global bstack11ll1l11ll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11ll1l11ll_opy_ = BrowserType.connect
    return bstack11ll1l11ll_opy_
def bstack1l1llll1l_opy_(framework_name):
    global bstack11ll1l1l11_opy_
    bstack11ll1l1l11_opy_ = framework_name
    return framework_name
def bstack1llll11l1l_opy_(self, *args, **kwargs):
    global bstack11ll1l11ll_opy_
    try:
        global bstack11ll1l1l11_opy_
        if bstack1l11ll1_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᴟ") in kwargs:
            kwargs[bstack1l11ll1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᴠ")] = bstack111ll1l111l_opy_(
                kwargs.get(bstack1l11ll1_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᴡ"), None),
                bstack11ll1l1l11_opy_
            )
    except Exception as e:
        logger.error(bstack1l11ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᴢ").format(str(e)))
    return bstack11ll1l11ll_opy_(self, *args, **kwargs)
def bstack11l11l111ll_opy_(bstack111ll1llll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11llllll11_opy_(bstack111ll1llll1_opy_, bstack1l11ll1_opy_ (u"ࠦࠧᴣ"))
        if proxies and proxies.get(bstack1l11ll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᴤ")):
            parsed_url = urlparse(proxies.get(bstack1l11ll1_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᴥ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᴦ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l11ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᴧ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l11ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᴨ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l11ll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᴩ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l11ll1ll1_opy_(bstack111ll1llll1_opy_):
    bstack111lllll1ll_opy_ = {
        bstack11l1ll1l111_opy_[bstack111llllll11_opy_]: bstack111ll1llll1_opy_[bstack111llllll11_opy_]
        for bstack111llllll11_opy_ in bstack111ll1llll1_opy_
        if bstack111llllll11_opy_ in bstack11l1ll1l111_opy_
    }
    bstack111lllll1ll_opy_[bstack1l11ll1_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᴪ")] = bstack11l11l111ll_opy_(bstack111ll1llll1_opy_, bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᴫ")))
    bstack111llll11l1_opy_ = [element.lower() for element in bstack11l1lll1lll_opy_]
    bstack111llllllll_opy_(bstack111lllll1ll_opy_, bstack111llll11l1_opy_)
    return bstack111lllll1ll_opy_
def bstack111llllllll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l11ll1_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᴬ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111llllllll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111llllllll_opy_(item, keys)
def bstack1l1ll11ll1l_opy_():
    bstack11l11l1111l_opy_ = [os.environ.get(bstack1l11ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤᴭ")), os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠣࢀࠥᴮ")), bstack1l11ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᴯ")), os.path.join(bstack1l11ll1_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᴰ"), bstack1l11ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᴱ"))]
    for path in bstack11l11l1111l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l11ll1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᴲ") + str(path) + bstack1l11ll1_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤᴳ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l11ll1_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦᴴ") + str(path) + bstack1l11ll1_opy_ (u"ࠣࠩࠥᴵ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l11ll1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᴶ") + str(path) + bstack1l11ll1_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣᴷ"))
            else:
                logger.debug(bstack1l11ll1_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨᴸ") + str(path) + bstack1l11ll1_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤᴹ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l11ll1_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦᴺ") + str(path) + bstack1l11ll1_opy_ (u"ࠢࠨ࠰ࠥᴻ"))
            return path
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨᴼ") + str(e) + bstack1l11ll1_opy_ (u"ࠤࠥᴽ"))
    logger.debug(bstack1l11ll1_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢᴾ"))
    return None
@measure(event_name=EVENTS.bstack11l1llll11l_opy_, stage=STAGE.bstack11lllll111_opy_)
def bstack1lll11ll11l_opy_(binary_path, bstack1lll1l1111l_opy_, bs_config):
    logger.debug(bstack1l11ll1_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥᴿ").format(binary_path))
    bstack11l1111lll1_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠭ᵀ")
    bstack111ll1l11l1_opy_ = {
        bstack1l11ll1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᵁ"): __version__,
        bstack1l11ll1_opy_ (u"ࠢࡰࡵࠥᵂ"): platform.system(),
        bstack1l11ll1_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤᵃ"): platform.machine(),
        bstack1l11ll1_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᵄ"): bstack1l11ll1_opy_ (u"ࠪ࠴ࠬᵅ"),
        bstack1l11ll1_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥᵆ"): bstack1l11ll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᵇ")
    }
    bstack11l111111ll_opy_(bstack111ll1l11l1_opy_)
    try:
        if binary_path:
            bstack111ll1l11l1_opy_[bstack1l11ll1_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᵈ")] = subprocess.check_output([binary_path, bstack1l11ll1_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᵉ")]).strip().decode(bstack1l11ll1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᵊ"))
        response = requests.request(
            bstack1l11ll1_opy_ (u"ࠩࡊࡉ࡙࠭ᵋ"),
            url=bstack1111l1lll_opy_(bstack11l1lll11ll_opy_),
            headers=None,
            auth=(bs_config[bstack1l11ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᵌ")], bs_config[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᵍ")]),
            json=None,
            params=bstack111ll1l11l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l11ll1_opy_ (u"ࠬࡻࡲ࡭ࠩᵎ") in data.keys() and bstack1l11ll1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᵏ") in data.keys():
            logger.debug(bstack1l11ll1_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣᵐ").format(bstack111ll1l11l1_opy_[bstack1l11ll1_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᵑ")]))
            if bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬᵒ") in os.environ:
                logger.debug(bstack1l11ll1_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡢࡵࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑࠦࡩࡴࠢࡶࡩࡹࠨᵓ"))
                data[bstack1l11ll1_opy_ (u"ࠫࡺࡸ࡬ࠨᵔ")] = os.environ[bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨᵕ")]
            bstack11l11ll1ll1_opy_ = bstack11l11l11111_opy_(data[bstack1l11ll1_opy_ (u"࠭ࡵࡳ࡮ࠪᵖ")], bstack1lll1l1111l_opy_)
            bstack11l1111lll1_opy_ = os.path.join(bstack1lll1l1111l_opy_, bstack11l11ll1ll1_opy_)
            os.chmod(bstack11l1111lll1_opy_, 0o777) # bstack11l111l1111_opy_ permission
            return bstack11l1111lll1_opy_
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢᵗ").format(e))
    return binary_path
def bstack11l111111ll_opy_(bstack111ll1l11l1_opy_):
    try:
        if bstack1l11ll1_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᵘ") not in bstack111ll1l11l1_opy_[bstack1l11ll1_opy_ (u"ࠩࡲࡷࠬᵙ")].lower():
            return
        if os.path.exists(bstack1l11ll1_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᵚ")):
            with open(bstack1l11ll1_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨᵛ"), bstack1l11ll1_opy_ (u"ࠧࡸࠢᵜ")) as f:
                bstack11l111l1lll_opy_ = {}
                for line in f:
                    if bstack1l11ll1_opy_ (u"ࠨ࠽ࠣᵝ") in line:
                        key, value = line.rstrip().split(bstack1l11ll1_opy_ (u"ࠢ࠾ࠤᵞ"), 1)
                        bstack11l111l1lll_opy_[key] = value.strip(bstack1l11ll1_opy_ (u"ࠨࠤ࡟ࠫࠬᵟ"))
                bstack111ll1l11l1_opy_[bstack1l11ll1_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩᵠ")] = bstack11l111l1lll_opy_.get(bstack1l11ll1_opy_ (u"ࠥࡍࡉࠨᵡ"), bstack1l11ll1_opy_ (u"ࠦࠧᵢ"))
        elif os.path.exists(bstack1l11ll1_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡥࡱࡶࡩ࡯ࡧ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᵣ")):
            bstack111ll1l11l1_opy_[bstack1l11ll1_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭ᵤ")] = bstack1l11ll1_opy_ (u"ࠧࡢ࡮ࡳ࡭ࡳ࡫ࠧᵥ")
    except Exception as e:
        logger.debug(bstack1l11ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡦ࡬ࡷࡹࡸ࡯ࠡࡱࡩࠤࡱ࡯࡮ࡶࡺࠥᵦ") + e)
@measure(event_name=EVENTS.bstack11l1ll1l11l_opy_, stage=STAGE.bstack11lllll111_opy_)
def bstack11l11l11111_opy_(bstack11l111l1ll1_opy_, bstack111ll1ll1ll_opy_):
    logger.debug(bstack1l11ll1_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦᵧ") + str(bstack11l111l1ll1_opy_) + bstack1l11ll1_opy_ (u"ࠥࠦᵨ"))
    zip_path = os.path.join(bstack111ll1ll1ll_opy_, bstack1l11ll1_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥᵩ"))
    bstack11l11ll1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠬ࠭ᵪ")
    with requests.get(bstack11l111l1ll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l11ll1_opy_ (u"ࠨࡷࡣࠤᵫ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l11ll1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤᵬ"))
    with zipfile.ZipFile(zip_path, bstack1l11ll1_opy_ (u"ࠨࡴࠪᵭ")) as zip_ref:
        bstack111lll1ll1l_opy_ = zip_ref.namelist()
        if len(bstack111lll1ll1l_opy_) > 0:
            bstack11l11ll1ll1_opy_ = bstack111lll1ll1l_opy_[0] # bstack111ll1l1lll_opy_ bstack11l1ll111l1_opy_ will be bstack11l111111l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111ll1ll1ll_opy_)
        logger.debug(bstack1l11ll1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣᵮ") + str(bstack111ll1ll1ll_opy_) + bstack1l11ll1_opy_ (u"ࠥࠫࠧᵯ"))
    os.remove(zip_path)
    return bstack11l11ll1ll1_opy_
def get_cli_dir():
    bstack11l11llllll_opy_ = bstack1l1ll11ll1l_opy_()
    if bstack11l11llllll_opy_:
        bstack1lll1l1111l_opy_ = os.path.join(bstack11l11llllll_opy_, bstack1l11ll1_opy_ (u"ࠦࡨࡲࡩࠣᵰ"))
        if not os.path.exists(bstack1lll1l1111l_opy_):
            os.makedirs(bstack1lll1l1111l_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1l1111l_opy_
    else:
        raise FileNotFoundError(bstack1l11ll1_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠣᵱ"))
def bstack1lll1lllll1_opy_(bstack1lll1l1111l_opy_):
    bstack1l11ll1_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤࠥᵲ")
    bstack11l111l1l11_opy_ = [
        os.path.join(bstack1lll1l1111l_opy_, f)
        for f in os.listdir(bstack1lll1l1111l_opy_)
        if os.path.isfile(os.path.join(bstack1lll1l1111l_opy_, f)) and f.startswith(bstack1l11ll1_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣᵳ"))
    ]
    if len(bstack11l111l1l11_opy_) > 0:
        return max(bstack11l111l1l11_opy_, key=os.path.getmtime) # get bstack11l111lllll_opy_ binary
    return bstack1l11ll1_opy_ (u"ࠣࠤᵴ")
def bstack11ll1lllll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll111l1l11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll111l1l11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll1111l1l_opy_(data, keys, default=None):
    bstack1l11ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡥ࡫࡫࡬ࡺࠢࡪࡩࡹࠦࡡࠡࡰࡨࡷࡹ࡫ࡤࠡࡸࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡦࡺࡡ࠻ࠢࡗ࡬ࡪࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡹࡵࠠࡵࡴࡤࡺࡪࡸࡳࡦ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠ࡬ࡧࡼࡷ࠿ࠦࡁࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢ࡮ࡩࡾࡹ࠯ࡪࡰࡧ࡭ࡨ࡫ࡳࠡࡴࡨࡴࡷ࡫ࡳࡦࡰࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡧࡩࡥࡺࡲࡴ࠻࡙ࠢࡥࡱࡻࡥࠡࡶࡲࠤࡷ࡫ࡴࡶࡴࡱࠤ࡮࡬ࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡵࡩࡹࡻࡲ࡯࠼ࠣࡘ࡭࡫ࠠࡷࡣ࡯ࡹࡪࠦࡡࡵࠢࡷ࡬ࡪࠦ࡮ࡦࡵࡷࡩࡩࠦࡰࡢࡶ࡫࠰ࠥࡵࡲࠡࡦࡨࡪࡦࡻ࡬ࡵࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᵵ")
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