# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
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
from bstack_utils.constants import (bstack11lllll11_opy_, bstack11l11l1l_opy_, bstack1lllllllll_opy_,
                                    bstack11l1llll1ll_opy_, bstack11l1ll1111l_opy_, bstack11l1lll11l1_opy_, bstack11l1ll1l1ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll111l111_opy_, bstack11lll11lll_opy_
from bstack_utils.proxy import bstack1lll1ll1_opy_, bstack11l111ll1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1l11lll1_opy_
from bstack_utils.bstack1ll1l1llll_opy_ import bstack1llll1111l_opy_
from browserstack_sdk._version import __version__
bstack1l1l1111l1_opy_ = Config.bstack11l1lllll1_opy_()
logger = bstack1l1l11lll1_opy_.get_logger(__name__, bstack1l1l11lll1_opy_.bstack1lll11ll111_opy_())
def bstack11ll1l111ll_opy_(config):
    return config[bstack1l1l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᫽")]
def bstack11lll111lll_opy_(config):
    return config[bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᫾")]
def bstack1ll1l11111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11lll111_opy_(obj):
    values = []
    bstack11l1l111l11_opy_ = re.compile(bstack1l1l1ll_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨ᫿"), re.I)
    for key in obj.keys():
        if bstack11l1l111l11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11llllll_opy_(config):
    tags = []
    tags.extend(bstack11l11lll111_opy_(os.environ))
    tags.extend(bstack11l11lll111_opy_(config))
    return tags
def bstack111lllll1l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11111111_opy_(bstack11l11l1lll1_opy_):
    if not bstack11l11l1lll1_opy_:
        return bstack1l1l1ll_opy_ (u"ࠪࠫᬀ")
    return bstack1l1l1ll_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧᬁ").format(bstack11l11l1lll1_opy_.name, bstack11l11l1lll1_opy_.email)
def bstack11ll1ll11l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l11ll1l11_opy_ = repo.common_dir
        info = {
            bstack1l1l1ll_opy_ (u"ࠧࡹࡨࡢࠤᬂ"): repo.head.commit.hexsha,
            bstack1l1l1ll_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤᬃ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1l1ll_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢᬄ"): repo.active_branch.name,
            bstack1l1l1ll_opy_ (u"ࠣࡶࡤ࡫ࠧᬅ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1l1ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧᬆ"): bstack11l11111111_opy_(repo.head.commit.committer),
            bstack1l1l1ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦᬇ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1l1ll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦᬈ"): bstack11l11111111_opy_(repo.head.commit.author),
            bstack1l1l1ll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥᬉ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1l1ll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᬊ"): repo.head.commit.message,
            bstack1l1l1ll_opy_ (u"ࠢࡳࡱࡲࡸࠧᬋ"): repo.git.rev_parse(bstack1l1l1ll_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥᬌ")),
            bstack1l1l1ll_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᬍ"): bstack11l11ll1l11_opy_,
            bstack1l1l1ll_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᬎ"): subprocess.check_output([bstack1l1l1ll_opy_ (u"ࠦ࡬࡯ࡴࠣᬏ"), bstack1l1l1ll_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣᬐ"), bstack1l1l1ll_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤᬑ")]).strip().decode(
                bstack1l1l1ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᬒ")),
            bstack1l1l1ll_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᬓ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1l1ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᬔ"): repo.git.rev_list(
                bstack1l1l1ll_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥᬕ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l111l1l1l_opy_ = []
        for remote in remotes:
            bstack11l11l11lll_opy_ = {
                bstack1l1l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᬖ"): remote.name,
                bstack1l1l1ll_opy_ (u"ࠧࡻࡲ࡭ࠤᬗ"): remote.url,
            }
            bstack11l111l1l1l_opy_.append(bstack11l11l11lll_opy_)
        bstack11l111l111l_opy_ = {
            bstack1l1l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬘ"): bstack1l1l1ll_opy_ (u"ࠢࡨ࡫ࡷࠦᬙ"),
            **info,
            bstack1l1l1ll_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤᬚ"): bstack11l111l1l1l_opy_
        }
        bstack11l111l111l_opy_ = bstack111lllll111_opy_(bstack11l111l111l_opy_)
        return bstack11l111l111l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᬛ").format(err))
        return {}
def bstack11l111ll1l1_opy_(bstack11l11ll111l_opy_=None):
    bstack1l1l1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࡢ࡮࡯ࡽࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤࡺࡹࡥࠡࡥࡤࡷࡪࡹࠠࡧࡱࡵࠤࡪࡧࡣࡩࠢࡩࡳࡱࡪࡥࡳࠢ࡬ࡲࠥࡺࡨࡦࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࠨ࡭࡫ࡶࡸ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡵࡧࡴࡩࡵࠣࡸࡴࠦࡥࡹࡶࡵࡥࡨࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡳࡱࡰ࠲ࠥࡊࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣ࡟ࡴࡹ࠮ࡨࡧࡷࡧࡼࡪࠨࠪ࡟࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡩ࡯ࡣࡵࡵ࠯ࠤࡪࡧࡣࡩࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡤࠤ࡫ࡵ࡬ࡥࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᬜ")
    if bstack11l11ll111l_opy_ is None:
        bstack11l11ll111l_opy_ = [os.getcwd()]
    results = []
    for folder in bstack11l11ll111l_opy_:
        try:
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l1l1ll_opy_ (u"ࠦࡵࡸࡉࡥࠤᬝ"): bstack1l1l1ll_opy_ (u"ࠧࠨᬞ"),
                bstack1l1l1ll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᬟ"): [],
                bstack1l1l1ll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᬠ"): [],
                bstack1l1l1ll_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣᬡ"): bstack1l1l1ll_opy_ (u"ࠤࠥᬢ"),
                bstack1l1l1ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦᬣ"): [],
                bstack1l1l1ll_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᬤ"): bstack1l1l1ll_opy_ (u"ࠧࠨᬥ"),
                bstack1l1l1ll_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨᬦ"): bstack1l1l1ll_opy_ (u"ࠢࠣᬧ"),
                bstack1l1l1ll_opy_ (u"ࠣࡲࡵࡖࡦࡽࡄࡪࡨࡩࠦᬨ"): bstack1l1l1ll_opy_ (u"ࠤࠥᬩ")
            }
            bstack111llll1l11_opy_ = repo.active_branch.name
            bstack11l11llll11_opy_ = repo.head.commit
            result[bstack1l1l1ll_opy_ (u"ࠥࡴࡷࡏࡤࠣᬪ")] = bstack11l11llll11_opy_.hexsha
            bstack11l1l11111l_opy_ = _11l1l111l1l_opy_(repo)
            logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡇࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠽ࠤࠧᬫ") + str(bstack11l1l11111l_opy_) + bstack1l1l1ll_opy_ (u"ࠧࠨᬬ"))
            if bstack11l1l11111l_opy_:
                try:
                    bstack11l1l111111_opy_ = repo.git.diff(bstack1l1l1ll_opy_ (u"ࠨ࠭࠮ࡰࡤࡱࡪ࠳࡯࡯࡮ࡼࠦᬭ"), bstack1llll1l1111_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦᬮ")).split(bstack1l1l1ll_opy_ (u"ࠨ࡞ࡱࠫᬯ"))
                    logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡆ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡥࡩࡹࡽࡥࡦࡰࠣࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿࠣࡥࡳࡪࠠࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿ࠽ࠤࠧᬰ") + str(bstack11l1l111111_opy_) + bstack1l1l1ll_opy_ (u"ࠥࠦᬱ"))
                    result[bstack1l1l1ll_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᬲ")] = [f.strip() for f in bstack11l1l111111_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1llll1l1111_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᬳ")))
                except Exception:
                    logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠯ࠢࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡷ࡫ࡣࡦࡰࡷࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠨ᬴"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l1l1ll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᬵ")] = _11l11l1ll1l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l1l1ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᬶ")] = _11l11l1ll1l_opy_(commits[:5])
            bstack11l11111l11_opy_ = set()
            bstack11l11ll11ll_opy_ = []
            for commit in commits:
                logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰ࡭ࡹࡀࠠࠣᬷ") + str(commit.message) + bstack1l1l1ll_opy_ (u"ࠥࠦᬸ"))
                bstack11l1111l1ll_opy_ = commit.author.name if commit.author else bstack1l1l1ll_opy_ (u"࡚ࠦࡴ࡫࡯ࡱࡺࡲࠧᬹ")
                bstack11l11111l11_opy_.add(bstack11l1111l1ll_opy_)
                bstack11l11ll11ll_opy_.append({
                    bstack1l1l1ll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᬺ"): commit.message.strip(),
                    bstack1l1l1ll_opy_ (u"ࠨࡵࡴࡧࡵࠦᬻ"): bstack11l1111l1ll_opy_
                })
            result[bstack1l1l1ll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᬼ")] = list(bstack11l11111l11_opy_)
            result[bstack1l1l1ll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᬽ")] = bstack11l11ll11ll_opy_
            result[bstack1l1l1ll_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᬾ")] = bstack11l11llll11_opy_.committed_datetime.strftime(bstack1l1l1ll_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨࠧᬿ"))
            if (not result[bstack1l1l1ll_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᭀ")] or result[bstack1l1l1ll_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᭁ")].strip() == bstack1l1l1ll_opy_ (u"ࠨࠢᭂ")) and bstack11l11llll11_opy_.message:
                bstack11l11ll11l1_opy_ = bstack11l11llll11_opy_.message.strip().split(bstack1l1l1ll_opy_ (u"ࠧ࡝ࡰࠪᭃ"))
                result[bstack1l1l1ll_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ᭄")] = bstack11l11ll11l1_opy_[0] if bstack11l11ll11l1_opy_ else bstack1l1l1ll_opy_ (u"ࠤࠥᭅ")
                if len(bstack11l11ll11l1_opy_) > 2:
                    result[bstack1l1l1ll_opy_ (u"ࠥࡴࡷࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥᭆ")] = bstack1l1l1ll_opy_ (u"ࠫࡡࡴࠧᭇ").join(bstack11l11ll11l1_opy_[2:]).strip()
            results.append(result)
        except git.InvalidGitRepositoryError:
            results.append({
                bstack1l1l1ll_opy_ (u"ࠧࡶࡲࡊࡦࠥᭈ"): bstack1l1l1ll_opy_ (u"ࠨࠢᭉ"),
                bstack1l1l1ll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᭊ"): [],
                bstack1l1l1ll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᭋ"): [],
                bstack1l1l1ll_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᭌ"): bstack1l1l1ll_opy_ (u"ࠥࠦ᭍"),
                bstack1l1l1ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧ᭎"): [],
                bstack1l1l1ll_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨ᭏"): bstack1l1l1ll_opy_ (u"ࠨࠢ᭐"),
                bstack1l1l1ll_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢ᭑"): bstack1l1l1ll_opy_ (u"ࠣࠤ᭒"),
                bstack1l1l1ll_opy_ (u"ࠤࡳࡶࡗࡧࡷࡅ࡫ࡩࡪࠧ᭓"): bstack1l1l1ll_opy_ (u"ࠥࠦ᭔")
            })
        except Exception as err:
            logger.error(bstack1l1l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࠫࡪࡴࡲࡤࡦࡴ࠽ࠤࢀ࡬࡯࡭ࡦࡨࡶࢂ࠯࠺ࠡࠤ᭕") + str(err) + bstack1l1l1ll_opy_ (u"ࠧࠨ᭖"))
            results.append({
                bstack1l1l1ll_opy_ (u"ࠨࡰࡳࡋࡧࠦ᭗"): bstack1l1l1ll_opy_ (u"ࠢࠣ᭘"),
                bstack1l1l1ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢ᭙"): [],
                bstack1l1l1ll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥ᭚"): [],
                bstack1l1l1ll_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥ᭛"): bstack1l1l1ll_opy_ (u"ࠦࠧ᭜"),
                bstack1l1l1ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨ᭝"): [],
                bstack1l1l1ll_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢ᭞"): bstack1l1l1ll_opy_ (u"ࠢࠣ᭟"),
                bstack1l1l1ll_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣ᭠"): bstack1l1l1ll_opy_ (u"ࠤࠥ᭡"),
                bstack1l1l1ll_opy_ (u"ࠥࡴࡷࡘࡡࡸࡆ࡬ࡪ࡫ࠨ᭢"): bstack1l1l1ll_opy_ (u"ࠦࠧ᭣")
            })
    return results
def _11l1l111l1l_opy_(repo):
    bstack1l1l1ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡚ࠥࡲࡺࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶ࡫ࡩࠥࡨࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࠬࡲࡧࡩ࡯࠮ࠣࡱࡦࡹࡴࡦࡴ࠯ࠤࡩ࡫ࡶࡦ࡮ࡲࡴ࠱ࠦࡥࡵࡥ࠱࠭ࠏࠦࠠࠡࠢࠥࠦࠧ᭤")
    try:
        bstack111ll1llll1_opy_ = [bstack1l1l1ll_opy_ (u"࠭࡭ࡢ࡫ࡱࠫ᭥"), bstack1l1l1ll_opy_ (u"ࠧ࡮ࡣࡶࡸࡪࡸࠧ᭦"), bstack1l1l1ll_opy_ (u"ࠨࡦࡨࡺࡪࡲ࡯ࡱࠩ᭧"), bstack1l1l1ll_opy_ (u"ࠩࡧࡩࡻ࠭᭨")]
        for branch_name in bstack111ll1llll1_opy_:
            try:
                repo.heads[branch_name]
                return branch_name
            except IndexError:
                try:
                    repo.remotes.origin.refs[branch_name]
                    return bstack1l1l1ll_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰ࠲ࡿࢂࠨ᭩").format(branch_name)
                except (AttributeError, IndexError):
                    continue
    except Exception:
        pass
    return None
def _11l11l1ll1l_opy_(commits):
    bstack1l1l1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡢࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᭪")
    bstack11l1l111111_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111llllll11_opy_ in diff:
                        if bstack111llllll11_opy_.a_path:
                            bstack11l1l111111_opy_.add(bstack111llllll11_opy_.a_path)
                        if bstack111llllll11_opy_.b_path:
                            bstack11l1l111111_opy_.add(bstack111llllll11_opy_.b_path)
    except Exception:
        pass
    return list(bstack11l1l111111_opy_)
def bstack111lllll111_opy_(bstack11l111l111l_opy_):
    bstack111lll111ll_opy_ = bstack11l1111ll11_opy_(bstack11l111l111l_opy_)
    if bstack111lll111ll_opy_ and bstack111lll111ll_opy_ > bstack11l1llll1ll_opy_:
        bstack11l11ll1lll_opy_ = bstack111lll111ll_opy_ - bstack11l1llll1ll_opy_
        bstack11l1l1111ll_opy_ = bstack111ll1ll1l1_opy_(bstack11l111l111l_opy_[bstack1l1l1ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᭫")], bstack11l11ll1lll_opy_)
        bstack11l111l111l_opy_[bstack1l1l1ll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫᭬ࠢ")] = bstack11l1l1111ll_opy_
        logger.info(bstack1l1l1ll_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤ᭭")
                    .format(bstack11l1111ll11_opy_(bstack11l111l111l_opy_) / 1024))
    return bstack11l111l111l_opy_
def bstack11l1111ll11_opy_(bstack1l111l11_opy_):
    try:
        if bstack1l111l11_opy_:
            bstack111llll11l1_opy_ = json.dumps(bstack1l111l11_opy_)
            bstack11l1111llll_opy_ = sys.getsizeof(bstack111llll11l1_opy_)
            return bstack11l1111llll_opy_
    except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣ᭮").format(e))
    return -1
def bstack111ll1ll1l1_opy_(field, bstack111ll1lll11_opy_):
    try:
        bstack111lll1l1l1_opy_ = len(bytes(bstack11l1ll1111l_opy_, bstack1l1l1ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᭯")))
        bstack111ll1ll11l_opy_ = bytes(field, bstack1l1l1ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᭰"))
        bstack11l1l1111l1_opy_ = len(bstack111ll1ll11l_opy_)
        bstack111lll11lll_opy_ = ceil(bstack11l1l1111l1_opy_ - bstack111ll1lll11_opy_ - bstack111lll1l1l1_opy_)
        if bstack111lll11lll_opy_ > 0:
            bstack11l1111l1l1_opy_ = bstack111ll1ll11l_opy_[:bstack111lll11lll_opy_].decode(bstack1l1l1ll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᭱"), errors=bstack1l1l1ll_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬ᭲")) + bstack11l1ll1111l_opy_
            return bstack11l1111l1l1_opy_
    except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦ᭳").format(e))
    return field
def bstack1llll1llll_opy_():
    env = os.environ
    if (bstack1l1l1ll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᭴") in env and len(env[bstack1l1l1ll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ᭵")]) > 0) or (
            bstack1l1l1ll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᭶") in env and len(env[bstack1l1l1ll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᭷")]) > 0):
        return {
            bstack1l1l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭸"): bstack1l1l1ll_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨ᭹"),
            bstack1l1l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᭺"): env.get(bstack1l1l1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᭻")),
            bstack1l1l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᭼"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦ᭽")),
            bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭾"): env.get(bstack1l1l1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᭿"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠧࡉࡉࠣᮀ")) == bstack1l1l1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᮁ") and bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᮂ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᮃ"): bstack1l1l1ll_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᮄ"),
            bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮅ"): env.get(bstack1l1l1ll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᮆ")),
            bstack1l1l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᮇ"): env.get(bstack1l1l1ll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᮈ")),
            bstack1l1l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮉ"): env.get(bstack1l1l1ll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᮊ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠤࡆࡍࠧᮋ")) == bstack1l1l1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᮌ") and bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᮍ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᮎ"): bstack1l1l1ll_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᮏ"),
            bstack1l1l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮐ"): env.get(bstack1l1l1ll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᮑ")),
            bstack1l1l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᮒ"): env.get(bstack1l1l1ll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᮓ")),
            bstack1l1l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᮔ"): env.get(bstack1l1l1ll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᮕ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠨࡃࡊࠤᮖ")) == bstack1l1l1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᮗ") and env.get(bstack1l1l1ll_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᮘ")) == bstack1l1l1ll_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᮙ"):
        return {
            bstack1l1l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᮚ"): bstack1l1l1ll_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᮛ"),
            bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮜ"): None,
            bstack1l1l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᮝ"): None,
            bstack1l1l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮞ"): None
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᮟ")) and env.get(bstack1l1l1ll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᮠ")):
        return {
            bstack1l1l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᮡ"): bstack1l1l1ll_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᮢ"),
            bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮣ"): env.get(bstack1l1l1ll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᮤ")),
            bstack1l1l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮥ"): None,
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮦ"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᮧ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠥࡇࡎࠨᮨ")) == bstack1l1l1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤᮩ") and bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"ࠧࡊࡒࡐࡐࡈ᮪ࠦ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᮫ࠦ"): bstack1l1l1ll_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᮬ"),
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮭ"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᮮ")),
            bstack1l1l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮯ"): None,
            bstack1l1l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᮰"): env.get(bstack1l1l1ll_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᮱"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠨࡃࡊࠤ᮲")) == bstack1l1l1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧ᮳") and bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦ᮴"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᮵"): bstack1l1l1ll_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨ᮶"),
            bstack1l1l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᮷"): env.get(bstack1l1l1ll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦ᮸")),
            bstack1l1l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᮹"): env.get(bstack1l1l1ll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᮺ")),
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮻ"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᮼ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠥࡇࡎࠨᮽ")) == bstack1l1l1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤᮾ") and bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᮿ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᯀ"): bstack1l1l1ll_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᯁ"),
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᯂ"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᯃ")),
            bstack1l1l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᯄ"): env.get(bstack1l1l1ll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᯅ")),
            bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᯆ"): env.get(bstack1l1l1ll_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᯇ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠢࡄࡋࠥᯈ")) == bstack1l1l1ll_opy_ (u"ࠣࡶࡵࡹࡪࠨᯉ") and bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᯊ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᯋ"): bstack1l1l1ll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᯌ"),
            bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯍ"): env.get(bstack1l1l1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᯎ")),
            bstack1l1l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᯏ"): env.get(bstack1l1l1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᯐ")) or env.get(bstack1l1l1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᯑ")),
            bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᯒ"): env.get(bstack1l1l1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᯓ"))
        }
    if bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᯔ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᯕ"): bstack1l1l1ll_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᯖ"),
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᯗ"): bstack1l1l1ll_opy_ (u"ࠤࡾࢁࢀࢃࠢᯘ").format(env.get(bstack1l1l1ll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᯙ")), env.get(bstack1l1l1ll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᯚ"))),
            bstack1l1l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᯛ"): env.get(bstack1l1l1ll_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᯜ")),
            bstack1l1l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᯝ"): env.get(bstack1l1l1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᯞ"))
        }
    if bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᯟ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᯠ"): bstack1l1l1ll_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᯡ"),
            bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯢ"): bstack1l1l1ll_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᯣ").format(env.get(bstack1l1l1ll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ᯤ")), env.get(bstack1l1l1ll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᯥ")), env.get(bstack1l1l1ll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉ᯦ࠪ")), env.get(bstack1l1l1ll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᯧ"))),
            bstack1l1l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᯨ"): env.get(bstack1l1l1ll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᯩ")),
            bstack1l1l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᯪ"): env.get(bstack1l1l1ll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᯫ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᯬ")) and env.get(bstack1l1l1ll_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᯭ")):
        return {
            bstack1l1l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᯮ"): bstack1l1l1ll_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᯯ"),
            bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᯰ"): bstack1l1l1ll_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᯱ").format(env.get(bstack1l1l1ll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋ᯲ࠪ")), env.get(bstack1l1l1ll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ᯳࡙࠭")), env.get(bstack1l1l1ll_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩ᯴"))),
            bstack1l1l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᯵"): env.get(bstack1l1l1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ᯶")),
            bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᯷"): env.get(bstack1l1l1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ᯸"))
        }
    if any([env.get(bstack1l1l1ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᯹")), env.get(bstack1l1l1ll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ᯺")), env.get(bstack1l1l1ll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᯻"))]):
        return {
            bstack1l1l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᯼"): bstack1l1l1ll_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦ᯽"),
            bstack1l1l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᯾"): env.get(bstack1l1l1ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᯿")),
            bstack1l1l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᰀ"): env.get(bstack1l1l1ll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᰁ")),
            bstack1l1l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᰂ"): env.get(bstack1l1l1ll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᰃ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᰄ")):
        return {
            bstack1l1l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᰅ"): bstack1l1l1ll_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᰆ"),
            bstack1l1l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᰇ"): env.get(bstack1l1l1ll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᰈ")),
            bstack1l1l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᰉ"): env.get(bstack1l1l1ll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᰊ")),
            bstack1l1l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᰋ"): env.get(bstack1l1l1ll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᰌ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᰍ")) or env.get(bstack1l1l1ll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᰎ")):
        return {
            bstack1l1l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᰏ"): bstack1l1l1ll_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᰐ"),
            bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᰑ"): env.get(bstack1l1l1ll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᰒ")),
            bstack1l1l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᰓ"): bstack1l1l1ll_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᰔ") if env.get(bstack1l1l1ll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᰕ")) else None,
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰖ"): env.get(bstack1l1l1ll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᰗ"))
        }
    if any([env.get(bstack1l1l1ll_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᰘ")), env.get(bstack1l1l1ll_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᰙ")), env.get(bstack1l1l1ll_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᰚ"))]):
        return {
            bstack1l1l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰛ"): bstack1l1l1ll_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᰜ"),
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰝ"): None,
            bstack1l1l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᰞ"): env.get(bstack1l1l1ll_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᰟ")),
            bstack1l1l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᰠ"): env.get(bstack1l1l1ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᰡ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᰢ")):
        return {
            bstack1l1l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᰣ"): bstack1l1l1ll_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦᰤ"),
            bstack1l1l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᰥ"): env.get(bstack1l1l1ll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᰦ")),
            bstack1l1l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᰧ"): bstack1l1l1ll_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᰨ").format(env.get(bstack1l1l1ll_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᰩ"))) if env.get(bstack1l1l1ll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᰪ")) else None,
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰫ"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᰬ"))
        }
    if bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᰭ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᰮ"): bstack1l1l1ll_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᰯ"),
            bstack1l1l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᰰ"): env.get(bstack1l1l1ll_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦᰱ")),
            bstack1l1l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᰲ"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧᰳ")),
            bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰴ"): env.get(bstack1l1l1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᰵ"))
        }
    if bstack11lll1ll11_opy_(env.get(bstack1l1l1ll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᰶ"))):
        return {
            bstack1l1l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᰷ࠦ"): bstack1l1l1ll_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣ᰸"),
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᰹"): bstack1l1l1ll_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥ᰺").format(env.get(bstack1l1l1ll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧ᰻")), env.get(bstack1l1l1ll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨ᰼")), env.get(bstack1l1l1ll_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬ᰽"))),
            bstack1l1l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᰾"): env.get(bstack1l1l1ll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤ᰿")),
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᱀"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤ᱁"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠥࡇࡎࠨ᱂")) == bstack1l1l1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤ᱃") and env.get(bstack1l1l1ll_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧ᱄")) == bstack1l1l1ll_opy_ (u"ࠨ࠱ࠣ᱅"):
        return {
            bstack1l1l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᱆"): bstack1l1l1ll_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣ᱇"),
            bstack1l1l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᱈"): bstack1l1l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨ᱉").format(env.get(bstack1l1l1ll_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨ᱊"))),
            bstack1l1l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᱋"): None,
            bstack1l1l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᱌"): None,
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᱍ")):
        return {
            bstack1l1l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᱎ"): bstack1l1l1ll_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᱏ"),
            bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᱐"): None,
            bstack1l1l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᱑"): env.get(bstack1l1l1ll_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨ᱒")),
            bstack1l1l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᱓"): env.get(bstack1l1l1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᱔"))
        }
    if any([env.get(bstack1l1l1ll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦ᱕")), env.get(bstack1l1l1ll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤ᱖")), env.get(bstack1l1l1ll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣ᱗")), env.get(bstack1l1l1ll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧ᱘"))]):
        return {
            bstack1l1l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᱙"): bstack1l1l1ll_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᱚ"),
            bstack1l1l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᱛ"): None,
            bstack1l1l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᱜ"): env.get(bstack1l1l1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᱝ")) or None,
            bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᱞ"): env.get(bstack1l1l1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᱟ"), 0)
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᱠ")):
        return {
            bstack1l1l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᱡ"): bstack1l1l1ll_opy_ (u"ࠢࡈࡱࡆࡈࠧᱢ"),
            bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᱣ"): None,
            bstack1l1l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᱤ"): env.get(bstack1l1l1ll_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᱥ")),
            bstack1l1l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᱦ"): env.get(bstack1l1l1ll_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᱧ"))
        }
    if env.get(bstack1l1l1ll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᱨ")):
        return {
            bstack1l1l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᱩ"): bstack1l1l1ll_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᱪ"),
            bstack1l1l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᱫ"): env.get(bstack1l1l1ll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᱬ")),
            bstack1l1l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᱭ"): env.get(bstack1l1l1ll_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᱮ")),
            bstack1l1l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᱯ"): env.get(bstack1l1l1ll_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᱰ"))
        }
    return {bstack1l1l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᱱ"): None}
def get_host_info():
    return {
        bstack1l1l1ll_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᱲ"): platform.node(),
        bstack1l1l1ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᱳ"): platform.system(),
        bstack1l1l1ll_opy_ (u"ࠦࡹࡿࡰࡦࠤᱴ"): platform.machine(),
        bstack1l1l1ll_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᱵ"): platform.version(),
        bstack1l1l1ll_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᱶ"): platform.architecture()[0]
    }
def bstack1ll1lll11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111lll11l1l_opy_():
    if bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᱷ")):
        return bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᱸ")
    return bstack1l1l1ll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᱹ")
def bstack11l111l11ll_opy_(driver):
    info = {
        bstack1l1l1ll_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᱺ"): driver.capabilities,
        bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᱻ"): driver.session_id,
        bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᱼ"): driver.capabilities.get(bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᱽ"), None),
        bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᱾"): driver.capabilities.get(bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᱿"), None),
        bstack1l1l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᲀ"): driver.capabilities.get(bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᲁ"), None),
        bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᲂ"):driver.capabilities.get(bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᲃ"), None),
    }
    if bstack111lll11l1l_opy_() == bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᲄ"):
        if bstack1ll111ll1l_opy_():
            info[bstack1l1l1ll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᲅ")] = bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᲆ")
        elif driver.capabilities.get(bstack1l1l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᲇ"), {}).get(bstack1l1l1ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᲈ"), False):
            info[bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᲉ")] = bstack1l1l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᲊ")
        else:
            info[bstack1l1l1ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ᲋")] = bstack1l1l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ᲌")
    return info
def bstack1ll111ll1l_opy_():
    if bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᲍")):
        return True
    if bstack11lll1ll11_opy_(os.environ.get(bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ᲎"), None)):
        return True
    return False
def bstack1llll11ll1_opy_(bstack111ll1lllll_opy_, url, data, config):
    headers = config.get(bstack1l1l1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ᲏"), None)
    proxies = bstack1lll1ll1_opy_(config, url)
    auth = config.get(bstack1l1l1ll_opy_ (u"ࠫࡦࡻࡴࡩࠩᲐ"), None)
    response = requests.request(
            bstack111ll1lllll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11111lll1_opy_(bstack1l1l1ll11l_opy_, size):
    bstack1l11ll1ll_opy_ = []
    while len(bstack1l1l1ll11l_opy_) > size:
        bstack1lll1111l_opy_ = bstack1l1l1ll11l_opy_[:size]
        bstack1l11ll1ll_opy_.append(bstack1lll1111l_opy_)
        bstack1l1l1ll11l_opy_ = bstack1l1l1ll11l_opy_[size:]
    bstack1l11ll1ll_opy_.append(bstack1l1l1ll11l_opy_)
    return bstack1l11ll1ll_opy_
def bstack111ll1lll1l_opy_(message, bstack11l11l1llll_opy_=False):
    os.write(1, bytes(message, bstack1l1l1ll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᲑ")))
    os.write(1, bytes(bstack1l1l1ll_opy_ (u"࠭࡜࡯ࠩᲒ"), bstack1l1l1ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭Დ")))
    if bstack11l11l1llll_opy_:
        with open(bstack1l1l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧᲔ") + os.environ[bstack1l1l1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᲕ")] + bstack1l1l1ll_opy_ (u"ࠪ࠲ࡱࡵࡧࠨᲖ"), bstack1l1l1ll_opy_ (u"ࠫࡦ࠭Თ")) as f:
            f.write(message + bstack1l1l1ll_opy_ (u"ࠬࡢ࡮ࠨᲘ"))
def bstack1l1llll11ll_opy_():
    return os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᲙ")].lower() == bstack1l1l1ll_opy_ (u"ࠧࡵࡴࡸࡩࠬᲚ")
def bstack11lllll1_opy_():
    return bstack111l11ll1l_opy_().replace(tzinfo=None).isoformat() + bstack1l1l1ll_opy_ (u"ࠨ࡜ࠪᲛ")
def bstack11l11llll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1l1ll_opy_ (u"ࠩ࡝ࠫᲜ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1l1ll_opy_ (u"ࠪ࡞ࠬᲝ")))).total_seconds() * 1000
def bstack111lll1l1ll_opy_(timestamp):
    return bstack11l11l1l1l1_opy_(timestamp).isoformat() + bstack1l1l1ll_opy_ (u"ࠫ࡟࠭Პ")
def bstack11l1111l111_opy_(bstack111llllllll_opy_):
    date_format = bstack1l1l1ll_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᲟ")
    bstack11l11lllll1_opy_ = datetime.datetime.strptime(bstack111llllllll_opy_, date_format)
    return bstack11l11lllll1_opy_.isoformat() + bstack1l1l1ll_opy_ (u"࡚࠭ࠨᲠ")
def bstack111llll1111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᲡ")
    else:
        return bstack1l1l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᲢ")
def bstack11lll1ll11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1l1ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᲣ")
def bstack111lll11ll1_opy_(val):
    return val.__str__().lower() == bstack1l1l1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᲤ")
def error_handler(bstack111ll1ll1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111ll1ll1ll_opy_ as e:
                print(bstack1l1l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᲥ").format(func.__name__, bstack111ll1ll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11111ll1_opy_(bstack111lll11l11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111lll11l11_opy_(cls, *args, **kwargs)
            except bstack111ll1ll1ll_opy_ as e:
                print(bstack1l1l1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᲦ").format(bstack111lll11l11_opy_.__name__, bstack111ll1ll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11111ll1_opy_
    else:
        return decorator
def bstack1l1l11llll_opy_(bstack11111ll1ll_opy_):
    if os.getenv(bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᲧ")) is not None:
        return bstack11lll1ll11_opy_(os.getenv(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᲨ")))
    if bstack1l1l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲩ") in bstack11111ll1ll_opy_ and bstack111lll11ll1_opy_(bstack11111ll1ll_opy_[bstack1l1l1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ც")]):
        return False
    if bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲫ") in bstack11111ll1ll_opy_ and bstack111lll11ll1_opy_(bstack11111ll1ll_opy_[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Წ")]):
        return False
    return True
def bstack111ll1ll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack111ll1l1ll1_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᲭ"), None)
        return bstack111ll1l1ll1_opy_ is None or bstack111ll1l1ll1_opy_ == bstack1l1l1ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᲮ")
    except Exception as e:
        return False
def bstack11lll1lll_opy_(hub_url, CONFIG):
    if bstack1l111111l_opy_() <= version.parse(bstack1l1l1ll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᲯ")):
        if hub_url:
            return bstack1l1l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᲰ") + hub_url + bstack1l1l1ll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᲱ")
        return bstack11l11l1l_opy_
    if hub_url:
        return bstack1l1l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᲲ") + hub_url + bstack1l1l1ll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᲳ")
    return bstack1lllllllll_opy_
def bstack111lll1ll11_opy_():
    return isinstance(os.getenv(bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᲴ")), str)
def bstack1l1l1l1ll_opy_(url):
    return urlparse(url).hostname
def bstack11l1l1l1l1_opy_(hostname):
    for bstack111ll11ll_opy_ in bstack11lllll11_opy_:
        regex = re.compile(bstack111ll11ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1111ll1l_opy_(bstack11l11lll1ll_opy_, file_name, logger):
    bstack1lll11llll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"࠭ࡾࠨᲵ")), bstack11l11lll1ll_opy_)
    try:
        if not os.path.exists(bstack1lll11llll_opy_):
            os.makedirs(bstack1lll11llll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠧࡿࠩᲶ")), bstack11l11lll1ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1l1ll_opy_ (u"ࠨࡹࠪᲷ")):
                pass
            with open(file_path, bstack1l1l1ll_opy_ (u"ࠤࡺ࠯ࠧᲸ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll111l111_opy_.format(str(e)))
def bstack11l111lll1l_opy_(file_name, key, value, logger):
    file_path = bstack11l1111ll1l_opy_(bstack1l1l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᲹ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1l111_opy_ = json.load(open(file_path, bstack1l1l1ll_opy_ (u"ࠫࡷࡨࠧᲺ")))
        else:
            bstack1ll1l111_opy_ = {}
        bstack1ll1l111_opy_[key] = value
        with open(file_path, bstack1l1l1ll_opy_ (u"ࠧࡽࠫࠣ᲻")) as outfile:
            json.dump(bstack1ll1l111_opy_, outfile)
def bstack1lllll1l11_opy_(file_name, logger):
    file_path = bstack11l1111ll1l_opy_(bstack1l1l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᲼"), file_name, logger)
    bstack1ll1l111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1l1ll_opy_ (u"ࠧࡳࠩᲽ")) as bstack11l111l111_opy_:
            bstack1ll1l111_opy_ = json.load(bstack11l111l111_opy_)
    return bstack1ll1l111_opy_
def bstack1l1lll11l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬᲾ") + file_path + bstack1l1l1ll_opy_ (u"ࠩࠣࠫᲿ") + str(e))
def bstack1l111111l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1l1ll_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧ᳀")
def bstack1l1ll111l_opy_(config):
    if bstack1l1l1ll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ᳁") in config:
        del (config[bstack1l1l1ll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ᳂")])
        return False
    if bstack1l111111l_opy_() < version.parse(bstack1l1l1ll_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬ᳃")):
        return False
    if bstack1l111111l_opy_() >= version.parse(bstack1l1l1ll_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭᳄")):
        return True
    if bstack1l1l1ll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ᳅") in config and config[bstack1l1l1ll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ᳆")] is False:
        return False
    else:
        return True
def bstack11ll1l1111_opy_(args_list, bstack11l111l1l11_opy_):
    index = -1
    for value in bstack11l111l1l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1l1ll11_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1l1ll11_opy_(a[k], v)
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
        return Result(result=bstack1l1l1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᳇"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᳈"), exception=exception)
    def bstack111111ll1l_opy_(self):
        if self.result != bstack1l1l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᳉"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1l1ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ᳊") in self.exception_type:
            return bstack1l1l1ll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ᳋")
        return bstack1l1l1ll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ᳌")
    def bstack11l1l111ll1_opy_(self):
        if self.result != bstack1l1l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᳍"):
            return None
        if self.bstack111lll1l1l_opy_:
            return self.bstack111lll1l1l_opy_
        return bstack111lll1lll1_opy_(self.exception)
def bstack111lll1lll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111lllll11l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l111l1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11ll1ll1ll_opy_(config, logger):
    try:
        import playwright
        bstack111ll1l1l1l_opy_ = playwright.__file__
        bstack111lll1l11l_opy_ = os.path.split(bstack111ll1l1l1l_opy_)
        bstack111ll1ll111_opy_ = bstack111lll1l11l_opy_[0] + bstack1l1l1ll_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭᳎")
        os.environ[bstack1l1l1ll_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧ᳏")] = bstack11l111ll1l_opy_(config)
        with open(bstack111ll1ll111_opy_, bstack1l1l1ll_opy_ (u"ࠬࡸࠧ᳐")) as f:
            bstack11llll111l_opy_ = f.read()
            bstack11l1111l11l_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ᳑")
            bstack11l11l11111_opy_ = bstack11llll111l_opy_.find(bstack11l1111l11l_opy_)
            if bstack11l11l11111_opy_ == -1:
              process = subprocess.Popen(bstack1l1l1ll_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦ᳒"), shell=True, cwd=bstack111lll1l11l_opy_[0])
              process.wait()
              bstack111llll1lll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨ᳓")
              bstack11l111ll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨ᳔")
              bstack111ll1l1lll_opy_ = bstack11llll111l_opy_.replace(bstack111llll1lll_opy_, bstack11l111ll11l_opy_)
              with open(bstack111ll1ll111_opy_, bstack1l1l1ll_opy_ (u"ࠪࡻ᳕ࠬ")) as f:
                f.write(bstack111ll1l1lll_opy_)
    except Exception as e:
        logger.error(bstack11lll11lll_opy_.format(str(e)))
def bstack11llllll11_opy_():
  try:
    bstack11l111l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱ᳖ࠫ"))
    bstack11l111llll1_opy_ = []
    if os.path.exists(bstack11l111l1lll_opy_):
      with open(bstack11l111l1lll_opy_) as f:
        bstack11l111llll1_opy_ = json.load(f)
      os.remove(bstack11l111l1lll_opy_)
    return bstack11l111llll1_opy_
  except:
    pass
  return []
def bstack111ll1l1l_opy_(bstack11l1lll11_opy_):
  try:
    bstack11l111llll1_opy_ = []
    bstack11l111l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲ᳗ࠬ"))
    if os.path.exists(bstack11l111l1lll_opy_):
      with open(bstack11l111l1lll_opy_) as f:
        bstack11l111llll1_opy_ = json.load(f)
    bstack11l111llll1_opy_.append(bstack11l1lll11_opy_)
    with open(bstack11l111l1lll_opy_, bstack1l1l1ll_opy_ (u"࠭ࡷࠨ᳘")) as f:
        json.dump(bstack11l111llll1_opy_, f)
  except:
    pass
def bstack11llll11ll_opy_(logger, bstack11l11l111ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇ᳙ࠪ"), bstack1l1l1ll_opy_ (u"ࠨࠩ᳚"))
    if test_name == bstack1l1l1ll_opy_ (u"ࠩࠪ᳛"):
        test_name = threading.current_thread().__dict__.get(bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦ᳜ࠩ"), bstack1l1l1ll_opy_ (u"᳝ࠫࠬ"))
    bstack11l11l1111l_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠲ࠠࠨ᳞").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11l111ll_opy_:
        bstack11l1llll_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝᳟࠭"), bstack1l1l1ll_opy_ (u"ࠧ࠱ࠩ᳠"))
        bstack1ll11lll_opy_ = {bstack1l1l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭᳡"): test_name, bstack1l1l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᳢"): bstack11l11l1111l_opy_, bstack1l1l1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹ᳣ࠩ"): bstack11l1llll_opy_}
        bstack11l111111l1_opy_ = []
        bstack111lll1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰ᳤ࠪ"))
        if os.path.exists(bstack111lll1ll1l_opy_):
            with open(bstack111lll1ll1l_opy_) as f:
                bstack11l111111l1_opy_ = json.load(f)
        bstack11l111111l1_opy_.append(bstack1ll11lll_opy_)
        with open(bstack111lll1ll1l_opy_, bstack1l1l1ll_opy_ (u"ࠬࡽ᳥ࠧ")) as f:
            json.dump(bstack11l111111l1_opy_, f)
    else:
        bstack1ll11lll_opy_ = {bstack1l1l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨ᳦ࠫ"): test_name, bstack1l1l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ᳧࠭"): bstack11l11l1111l_opy_, bstack1l1l1ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾ᳨ࠧ"): str(multiprocessing.current_process().name)}
        if bstack1l1l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ᳩ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll11lll_opy_)
  except Exception as e:
      logger.warn(bstack1l1l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᳪ").format(e))
def bstack1lll1l111_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧᳫ"))
    try:
      bstack111lll1llll_opy_ = []
      bstack1ll11lll_opy_ = {bstack1l1l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᳬ"): test_name, bstack1l1l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶ᳭ࠬ"): error_message, bstack1l1l1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᳮ"): index}
      bstack11l11l11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᳯ"))
      if os.path.exists(bstack11l11l11l11_opy_):
          with open(bstack11l11l11l11_opy_) as f:
              bstack111lll1llll_opy_ = json.load(f)
      bstack111lll1llll_opy_.append(bstack1ll11lll_opy_)
      with open(bstack11l11l11l11_opy_, bstack1l1l1ll_opy_ (u"ࠩࡺࠫᳰ")) as f:
          json.dump(bstack111lll1llll_opy_, f)
    except Exception as e:
      logger.warn(bstack1l1l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᳱ").format(e))
    return
  bstack111lll1llll_opy_ = []
  bstack1ll11lll_opy_ = {bstack1l1l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᳲ"): test_name, bstack1l1l1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᳳ"): error_message, bstack1l1l1ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ᳴"): index}
  bstack11l11l11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᳵ"))
  lock_file = bstack11l11l11l11_opy_ + bstack1l1l1ll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧᳶ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l11l11l11_opy_):
          with open(bstack11l11l11l11_opy_, bstack1l1l1ll_opy_ (u"ࠩࡵࠫ᳷")) as f:
              content = f.read().strip()
              if content:
                  bstack111lll1llll_opy_ = json.load(open(bstack11l11l11l11_opy_))
      bstack111lll1llll_opy_.append(bstack1ll11lll_opy_)
      with open(bstack11l11l11l11_opy_, bstack1l1l1ll_opy_ (u"ࠪࡻࠬ᳸")) as f:
          json.dump(bstack111lll1llll_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦ᳹").format(e))
def bstack11l11llll_opy_(bstack111l11ll_opy_, name, logger):
  try:
    bstack1ll11lll_opy_ = {bstack1l1l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᳺ"): name, bstack1l1l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᳻"): bstack111l11ll_opy_, bstack1l1l1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭᳼"): str(threading.current_thread()._name)}
    return bstack1ll11lll_opy_
  except Exception as e:
    logger.warn(bstack1l1l1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ᳽").format(e))
  return
def bstack11l111lllll_opy_():
    return platform.system() == bstack1l1l1ll_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪ᳾")
def bstack1111l1l1l_opy_(bstack111lllllll1_opy_, config, logger):
    bstack11l11l1l1ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111lllllll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ᳿").format(e))
    return bstack11l11l1l1ll_opy_
def bstack11l11ll1111_opy_(bstack111lll11111_opy_, bstack11l111l11l1_opy_):
    bstack11l11l1l11l_opy_ = version.parse(bstack111lll11111_opy_)
    bstack111lll111l1_opy_ = version.parse(bstack11l111l11l1_opy_)
    if bstack11l11l1l11l_opy_ > bstack111lll111l1_opy_:
        return 1
    elif bstack11l11l1l11l_opy_ < bstack111lll111l1_opy_:
        return -1
    else:
        return 0
def bstack111l11ll1l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11l1l1l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1111lll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1ll11l1ll1_opy_(options, framework, config, bstack1lll1l1lll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1l1ll_opy_ (u"ࠫ࡬࡫ࡴࠨᴀ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1111l1l1_opy_ = caps.get(bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᴁ"))
    bstack11l11l111l1_opy_ = True
    bstack1l1lll1l11_opy_ = os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᴂ")]
    bstack1ll111lllll_opy_ = config.get(bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴃ"), False)
    if bstack1ll111lllll_opy_:
        bstack1lll111lll1_opy_ = config.get(bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᴄ"), {})
        bstack1lll111lll1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᴅ")] = os.getenv(bstack1l1l1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᴆ"))
        bstack11lll111ll1_opy_ = json.loads(os.getenv(bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᴇ"), bstack1l1l1ll_opy_ (u"ࠬࢁࡽࠨᴈ"))).get(bstack1l1l1ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᴉ"))
    if bstack111lll11ll1_opy_(caps.get(bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭ᴊ"))) or bstack111lll11ll1_opy_(caps.get(bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᴋ"))):
        bstack11l11l111l1_opy_ = False
    if bstack1l1ll111l_opy_({bstack1l1l1ll_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤᴌ"): bstack11l11l111l1_opy_}):
        bstack1111l1l1_opy_ = bstack1111l1l1_opy_ or {}
        bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᴍ")] = bstack11l1111lll1_opy_(framework)
        bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᴎ")] = bstack1l1llll11ll_opy_()
        bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᴏ")] = bstack1l1lll1l11_opy_
        bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᴐ")] = bstack1lll1l1lll_opy_
        if bstack1ll111lllll_opy_:
            bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴑ")] = bstack1ll111lllll_opy_
            bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᴒ")] = bstack1lll111lll1_opy_
            bstack1111l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴓ")][bstack1l1l1ll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᴔ")] = bstack11lll111ll1_opy_
        if getattr(options, bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᴕ"), None):
            options.set_capability(bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᴖ"), bstack1111l1l1_opy_)
        else:
            options[bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᴗ")] = bstack1111l1l1_opy_
    else:
        if getattr(options, bstack1l1l1ll_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᴘ"), None):
            options.set_capability(bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴙ"), bstack11l1111lll1_opy_(framework))
            options.set_capability(bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴚ"), bstack1l1llll11ll_opy_())
            options.set_capability(bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴛ"), bstack1l1lll1l11_opy_)
            options.set_capability(bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴜ"), bstack1lll1l1lll_opy_)
            if bstack1ll111lllll_opy_:
                options.set_capability(bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴝ"), bstack1ll111lllll_opy_)
                options.set_capability(bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᴞ"), bstack1lll111lll1_opy_)
                options.set_capability(bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᴟ"), bstack11lll111ll1_opy_)
        else:
            options[bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴠ")] = bstack11l1111lll1_opy_(framework)
            options[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴡ")] = bstack1l1llll11ll_opy_()
            options[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴢ")] = bstack1l1lll1l11_opy_
            options[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴣ")] = bstack1lll1l1lll_opy_
            if bstack1ll111lllll_opy_:
                options[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴤ")] = bstack1ll111lllll_opy_
                options[bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᴥ")] = bstack1lll111lll1_opy_
                options[bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴦ")][bstack1l1l1ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᴧ")] = bstack11lll111ll1_opy_
    return options
def bstack11l111lll11_opy_(bstack11l11ll1l1l_opy_, framework):
    bstack1lll1l1lll_opy_ = bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᴨ"))
    if bstack11l11ll1l1l_opy_ and len(bstack11l11ll1l1l_opy_.split(bstack1l1l1ll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᴩ"))) > 1:
        ws_url = bstack11l11ll1l1l_opy_.split(bstack1l1l1ll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᴪ"))[0]
        if bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᴫ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l11l11ll1_opy_ = json.loads(urllib.parse.unquote(bstack11l11ll1l1l_opy_.split(bstack1l1l1ll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᴬ"))[1]))
            bstack11l11l11ll1_opy_ = bstack11l11l11ll1_opy_ or {}
            bstack1l1lll1l11_opy_ = os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᴭ")]
            bstack11l11l11ll1_opy_[bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᴮ")] = str(framework) + str(__version__)
            bstack11l11l11ll1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᴯ")] = bstack1l1llll11ll_opy_()
            bstack11l11l11ll1_opy_[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴰ")] = bstack1l1lll1l11_opy_
            bstack11l11l11ll1_opy_[bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᴱ")] = bstack1lll1l1lll_opy_
            bstack11l11ll1l1l_opy_ = bstack11l11ll1l1l_opy_.split(bstack1l1l1ll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᴲ"))[0] + bstack1l1l1ll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᴳ") + urllib.parse.quote(json.dumps(bstack11l11l11ll1_opy_))
    return bstack11l11ll1l1l_opy_
def bstack11ll1lll_opy_():
    global bstack1l1l1l1l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l1l1l1_opy_ = BrowserType.connect
    return bstack1l1l1l1l1_opy_
def bstack1l111l11ll_opy_(framework_name):
    global bstack11ll1111_opy_
    bstack11ll1111_opy_ = framework_name
    return framework_name
def bstack11111111_opy_(self, *args, **kwargs):
    global bstack1l1l1l1l1_opy_
    try:
        global bstack11ll1111_opy_
        if bstack1l1l1ll_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᴴ") in kwargs:
            kwargs[bstack1l1l1ll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᴵ")] = bstack11l111lll11_opy_(
                kwargs.get(bstack1l1l1ll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᴶ"), None),
                bstack11ll1111_opy_
            )
    except Exception as e:
        logger.error(bstack1l1l1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᴷ").format(str(e)))
    return bstack1l1l1l1l1_opy_(self, *args, **kwargs)
def bstack11l111ll1ll_opy_(bstack11l11ll1ll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lll1ll1_opy_(bstack11l11ll1ll1_opy_, bstack1l1l1ll_opy_ (u"ࠦࠧᴸ"))
        if proxies and proxies.get(bstack1l1l1ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᴹ")):
            parsed_url = urlparse(proxies.get(bstack1l1l1ll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᴺ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᴻ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᴼ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᴽ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᴾ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll11ll1_opy_(bstack11l11ll1ll1_opy_):
    bstack11l111l1ll1_opy_ = {
        bstack11l1ll1l1ll_opy_[bstack111llllll1l_opy_]: bstack11l11ll1ll1_opy_[bstack111llllll1l_opy_]
        for bstack111llllll1l_opy_ in bstack11l11ll1ll1_opy_
        if bstack111llllll1l_opy_ in bstack11l1ll1l1ll_opy_
    }
    bstack11l111l1ll1_opy_[bstack1l1l1ll_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᴿ")] = bstack11l111ll1ll_opy_(bstack11l11ll1ll1_opy_, bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᵀ")))
    bstack11l111ll111_opy_ = [element.lower() for element in bstack11l1lll11l1_opy_]
    bstack11l11lll11l_opy_(bstack11l111l1ll1_opy_, bstack11l111ll111_opy_)
    return bstack11l111l1ll1_opy_
def bstack11l11lll11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1l1ll_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᵁ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l11lll11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l11lll11l_opy_(item, keys)
def bstack1l1lll1ll1l_opy_():
    bstack111llll1ll1_opy_ = [os.environ.get(bstack1l1l1ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤᵂ")), os.path.join(os.path.expanduser(bstack1l1l1ll_opy_ (u"ࠣࢀࠥᵃ")), bstack1l1l1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᵄ")), os.path.join(bstack1l1l1ll_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᵅ"), bstack1l1l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᵆ"))]
    for path in bstack111llll1ll1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᵇ") + str(path) + bstack1l1l1ll_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤᵈ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦᵉ") + str(path) + bstack1l1l1ll_opy_ (u"ࠣࠩࠥᵊ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᵋ") + str(path) + bstack1l1l1ll_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣᵌ"))
            else:
                logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨᵍ") + str(path) + bstack1l1l1ll_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤᵎ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦᵏ") + str(path) + bstack1l1l1ll_opy_ (u"ࠢࠨ࠰ࠥᵐ"))
            return path
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨᵑ") + str(e) + bstack1l1l1ll_opy_ (u"ࠤࠥᵒ"))
    logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢᵓ"))
    return None
@measure(event_name=EVENTS.bstack11l1llll1l1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack1ll1llll11l_opy_(binary_path, bstack1lll11llll1_opy_, bs_config):
    logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥᵔ").format(binary_path))
    bstack111llll11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭ᵕ")
    bstack11l11l1l111_opy_ = {
        bstack1l1l1ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᵖ"): __version__,
        bstack1l1l1ll_opy_ (u"ࠢࡰࡵࠥᵗ"): platform.system(),
        bstack1l1l1ll_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤᵘ"): platform.machine(),
        bstack1l1l1ll_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᵙ"): bstack1l1l1ll_opy_ (u"ࠪ࠴ࠬᵚ"),
        bstack1l1l1ll_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥᵛ"): bstack1l1l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᵜ")
    }
    bstack11l11lll1l1_opy_(bstack11l11l1l111_opy_)
    try:
        if binary_path:
            bstack11l11l1l111_opy_[bstack1l1l1ll_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᵝ")] = subprocess.check_output([binary_path, bstack1l1l1ll_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᵞ")]).strip().decode(bstack1l1l1ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᵟ"))
        response = requests.request(
            bstack1l1l1ll_opy_ (u"ࠩࡊࡉ࡙࠭ᵠ"),
            url=bstack1llll1111l_opy_(bstack11l1ll111ll_opy_),
            headers=None,
            auth=(bs_config[bstack1l1l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᵡ")], bs_config[bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᵢ")]),
            json=None,
            params=bstack11l11l1l111_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1l1ll_opy_ (u"ࠬࡻࡲ࡭ࠩᵣ") in data.keys() and bstack1l1l1ll_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᵤ") in data.keys():
            logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣᵥ").format(bstack11l11l1l111_opy_[bstack1l1l1ll_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᵦ")]))
            if bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬᵧ") in os.environ:
                logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡢࡵࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑࠦࡩࡴࠢࡶࡩࡹࠨᵨ"))
                data[bstack1l1l1ll_opy_ (u"ࠫࡺࡸ࡬ࠨᵩ")] = os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨᵪ")]
            bstack11l11111l1l_opy_ = bstack111llll111l_opy_(data[bstack1l1l1ll_opy_ (u"࠭ࡵࡳ࡮ࠪᵫ")], bstack1lll11llll1_opy_)
            bstack111llll11ll_opy_ = os.path.join(bstack1lll11llll1_opy_, bstack11l11111l1l_opy_)
            os.chmod(bstack111llll11ll_opy_, 0o777) # bstack11l1111111l_opy_ permission
            return bstack111llll11ll_opy_
    except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢᵬ").format(e))
    return binary_path
def bstack11l11lll1l1_opy_(bstack11l11l1l111_opy_):
    try:
        if bstack1l1l1ll_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᵭ") not in bstack11l11l1l111_opy_[bstack1l1l1ll_opy_ (u"ࠩࡲࡷࠬᵮ")].lower():
            return
        if os.path.exists(bstack1l1l1ll_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᵯ")):
            with open(bstack1l1l1ll_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨᵰ"), bstack1l1l1ll_opy_ (u"ࠧࡸࠢᵱ")) as f:
                bstack11l11111lll_opy_ = {}
                for line in f:
                    if bstack1l1l1ll_opy_ (u"ࠨ࠽ࠣᵲ") in line:
                        key, value = line.rstrip().split(bstack1l1l1ll_opy_ (u"ࠢ࠾ࠤᵳ"), 1)
                        bstack11l11111lll_opy_[key] = value.strip(bstack1l1l1ll_opy_ (u"ࠨࠤ࡟ࠫࠬᵴ"))
                bstack11l11l1l111_opy_[bstack1l1l1ll_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩᵵ")] = bstack11l11111lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠥࡍࡉࠨᵶ"), bstack1l1l1ll_opy_ (u"ࠦࠧᵷ"))
        elif os.path.exists(bstack1l1l1ll_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡥࡱࡶࡩ࡯ࡧ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᵸ")):
            bstack11l11l1l111_opy_[bstack1l1l1ll_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭ᵹ")] = bstack1l1l1ll_opy_ (u"ࠧࡢ࡮ࡳ࡭ࡳ࡫ࠧᵺ")
    except Exception as e:
        logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡦ࡬ࡷࡹࡸ࡯ࠡࡱࡩࠤࡱ࡯࡮ࡶࡺࠥᵻ") + e)
@measure(event_name=EVENTS.bstack11l1ll1l11l_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack111llll111l_opy_(bstack111lllll1ll_opy_, bstack111llll1l1l_opy_):
    logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦᵼ") + str(bstack111lllll1ll_opy_) + bstack1l1l1ll_opy_ (u"ࠥࠦᵽ"))
    zip_path = os.path.join(bstack111llll1l1l_opy_, bstack1l1l1ll_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥᵾ"))
    bstack11l11111l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭ᵿ")
    with requests.get(bstack111lllll1ll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1l1ll_opy_ (u"ࠨࡷࡣࠤᶀ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤᶁ"))
    with zipfile.ZipFile(zip_path, bstack1l1l1ll_opy_ (u"ࠨࡴࠪᶂ")) as zip_ref:
        bstack111lll1l111_opy_ = zip_ref.namelist()
        if len(bstack111lll1l111_opy_) > 0:
            bstack11l11111l1l_opy_ = bstack111lll1l111_opy_[0] # bstack11l111111ll_opy_ bstack11l1lll1l11_opy_ will be bstack11l111l1111_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111llll1l1l_opy_)
        logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣᶃ") + str(bstack111llll1l1l_opy_) + bstack1l1l1ll_opy_ (u"ࠥࠫࠧᶄ"))
    os.remove(zip_path)
    return bstack11l11111l1l_opy_
def get_cli_dir():
    bstack111lll1111l_opy_ = bstack1l1lll1ll1l_opy_()
    if bstack111lll1111l_opy_:
        bstack1lll11llll1_opy_ = os.path.join(bstack111lll1111l_opy_, bstack1l1l1ll_opy_ (u"ࠦࡨࡲࡩࠣᶅ"))
        if not os.path.exists(bstack1lll11llll1_opy_):
            os.makedirs(bstack1lll11llll1_opy_, mode=0o777, exist_ok=True)
        return bstack1lll11llll1_opy_
    else:
        raise FileNotFoundError(bstack1l1l1ll_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠣᶆ"))
def bstack1llll1l11ll_opy_(bstack1lll11llll1_opy_):
    bstack1l1l1ll_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤࠥᶇ")
    bstack11l11l1ll11_opy_ = [
        os.path.join(bstack1lll11llll1_opy_, f)
        for f in os.listdir(bstack1lll11llll1_opy_)
        if os.path.isfile(os.path.join(bstack1lll11llll1_opy_, f)) and f.startswith(bstack1l1l1ll_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣᶈ"))
    ]
    if len(bstack11l11l1ll11_opy_) > 0:
        return max(bstack11l11l1ll11_opy_, key=os.path.getmtime) # get bstack11l11l11l1l_opy_ binary
    return bstack1l1l1ll_opy_ (u"ࠣࠤᶉ")
def bstack11ll11lllll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll111l1ll1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll111l1ll1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll11llll_opy_(data, keys, default=None):
    bstack1l1l1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡥ࡫࡫࡬ࡺࠢࡪࡩࡹࠦࡡࠡࡰࡨࡷࡹ࡫ࡤࠡࡸࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡦࡺࡡ࠻ࠢࡗ࡬ࡪࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡹࡵࠠࡵࡴࡤࡺࡪࡸࡳࡦ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠ࡬ࡧࡼࡷ࠿ࠦࡁࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢ࡮ࡩࡾࡹ࠯ࡪࡰࡧ࡭ࡨ࡫ࡳࠡࡴࡨࡴࡷ࡫ࡳࡦࡰࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡧࡩࡥࡺࡲࡴ࠻࡙ࠢࡥࡱࡻࡥࠡࡶࡲࠤࡷ࡫ࡴࡶࡴࡱࠤ࡮࡬ࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡵࡩࡹࡻࡲ࡯࠼ࠣࡘ࡭࡫ࠠࡷࡣ࡯ࡹࡪࠦࡡࡵࠢࡷ࡬ࡪࠦ࡮ࡦࡵࡷࡩࡩࠦࡰࡢࡶ࡫࠰ࠥࡵࡲࠡࡦࡨࡪࡦࡻ࡬ࡵࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᶊ")
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