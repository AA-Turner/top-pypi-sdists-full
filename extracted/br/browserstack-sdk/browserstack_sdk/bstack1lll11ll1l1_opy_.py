# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࡔࡾࡺࡥࡴࡶࠣࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡮ࡥ࡭ࡲࡨࡶࠥࡻࡳࡪࡰࡪࠤࡩ࡯ࡲࡦࡥࡷࠤࡵࡿࡴࡦࡵࡷࠤ࡭ࡵ࡯࡬ࡵ࠱ࠎࠧࠨࠢᇷ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1lll11lll1l_opy_(bstack1lll11lll11_opy_=None, bstack1lll11llll1_opy_=None):
    bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡷࡩࡸࡺࡳࠡࡷࡶ࡭ࡳ࡭ࠠࡱࡻࡷࡩࡸࡺࠧࡴࠢ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤࡆࡖࡉࡴ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤࡧࡲࡨࡵࠣࠬࡱ࡯ࡳࡵ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࡄࡱࡰࡴࡱ࡫ࡴࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡴࡾࡺࡥࡴࡶࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡩ࡯ࡥ࡯ࡹࡩ࡯࡮ࡨࠢࡳࡥࡹ࡮ࡳࠡࡣࡱࡨࠥ࡬࡬ࡢࡩࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡡ࡬ࡧࡶࠤࡵࡸࡥࡤࡧࡧࡩࡳࡩࡥࠡࡱࡹࡩࡷࠦࡴࡦࡵࡷࡣࡵࡧࡴࡩࡵࠣ࡭࡫ࠦࡢࡰࡶ࡫ࠤࡦࡸࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡴࡦࡺࡨࡴࠢࠫࡰ࡮ࡹࡴࠡࡱࡵࠤࡸࡺࡲ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࡔࡦࡵࡷࠤ࡫࡯࡬ࡦࠪࡶ࠭࠴ࡪࡩࡳࡧࡦࡸࡴࡸࡹࠩ࡫ࡨࡷ࠮ࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡪࡷࡵ࡭࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡇࡦࡴࠠࡣࡧࠣࡥࠥࡹࡩ࡯ࡩ࡯ࡩࠥࡶࡡࡵࡪࠣࡷࡹࡸࡩ࡯ࡩࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡱࡣࡷ࡬ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡋࡪࡲࡴࡸࡥࡥࠢ࡬ࡪࠥࡺࡥࡴࡶࡢࡥࡷ࡭ࡳࠡ࡫ࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡯ࡴࡩࠢ࡮ࡩࡾࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡵࡸࡧࡨ࡫ࡳࡴࠢࠫࡦࡴࡵ࡬ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡦࡳࡺࡴࡴࠡࠪ࡬ࡲࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠ࡯ࡱࡧࡩ࡮ࡪࡳࠡࠪ࡯࡭ࡸࡺࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠥ࠮࡬ࡪࡵࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥ࡫ࡲࡳࡱࡵࠤ࠭ࡹࡴࡳࠫࠍࠤࠥࠦࠠࠣࠤࠥᇸ")
    try:
        bstack1lll11ll11l_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠤࡓ࡝࡙ࡋࡓࡕࡡࡆ࡙ࡗࡘࡅࡏࡖࡢࡘࡊ࡙ࡔࠣᇹ")) is not None
        if bstack1lll11lll11_opy_ is not None:
            args = list(bstack1lll11lll11_opy_)
        elif bstack1lll11llll1_opy_ is not None:
            if isinstance(bstack1lll11llll1_opy_, str):
                args = [bstack1lll11llll1_opy_]
            elif isinstance(bstack1lll11llll1_opy_, list):
                args = list(bstack1lll11llll1_opy_)
            else:
                args = [bstack1ll1lll_opy_ (u"ࠥ࠲ࠧᇺ")]
        else:
            args = [bstack1ll1lll_opy_ (u"ࠦ࠳ࠨᇻ")]
        if bstack1lll11ll11l_opy_:
            return _1lll11lllll_opy_(args)
        bstack1lll11l1ll1_opy_ = args + [
            bstack1ll1lll_opy_ (u"ࠧ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨᇼ"),
            bstack1ll1lll_opy_ (u"ࠨ࠭࠮ࡳࡸ࡭ࡪࡺࠢᇽ")
        ]
        class bstack1lll1l11111_opy_:
            bstack1ll1lll_opy_ (u"ࠢࠣࠤࡓࡽࡹ࡫ࡳࡵࠢࡳࡰࡺ࡭ࡩ࡯ࠢࡷ࡬ࡦࡺࠠࡤࡣࡳࡸࡺࡸࡥࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨࠥࡺࡥࡴࡶࠣ࡭ࡹ࡫࡭ࡴ࠰ࠥࠦࠧᇾ")
            def __init__(self):
                self.bstack1lll11ll111_opy_ = []
                self.test_files = set()
                self.bstack1lll1l1111l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1ll1lll_opy_ (u"ࠣࠤࠥࡌࡴࡵ࡫ࠡࡥࡤࡰࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡮ࡹࠠࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠰ࠥࠦࠧᇿ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1lll11ll111_opy_.append(nodeid)
                        if bstack1ll1lll_opy_ (u"ࠤ࠽࠾ࠧሀ") in nodeid:
                            file_path = nodeid.split(bstack1ll1lll_opy_ (u"ࠥ࠾࠿ࠨሁ"), 1)[0]
                            if file_path.endswith(bstack1ll1lll_opy_ (u"ࠫ࠳ࡶࡹࠨሂ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lll1l1111l_opy_ = str(e)
        collector = bstack1lll1l11111_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1lll11l1ll1_opy_, plugins=[collector])
        if collector.bstack1lll1l1111l_opy_:
            return {bstack1ll1lll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨሃ"): False, bstack1ll1lll_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧሄ"): 0, bstack1ll1lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣህ"): [], bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧሆ"): [], bstack1ll1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣሇ"): bstack1ll1lll_opy_ (u"ࠥࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥለ").format(collector.bstack1lll1l1111l_opy_)}
        return {
            bstack1ll1lll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧሉ"): True,
            bstack1ll1lll_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦሊ"): len(collector.bstack1lll11ll111_opy_),
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢላ"): collector.bstack1lll11ll111_opy_,
            bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦሌ"): sorted(collector.test_files),
            bstack1ll1lll_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠦል"): exit_code
        }
    except Exception as e:
        return {bstack1ll1lll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥሎ"): False, bstack1ll1lll_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤሏ"): 0, bstack1ll1lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧሐ"): [], bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤሑ"): [], bstack1ll1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧሒ"): bstack1ll1lll_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧሓ").format(e)}
def _1lll11lllll_opy_(args):
    bstack1ll1lll_opy_ (u"ࠣࠤࠥࡍࡸࡵ࡬ࡢࡶࡨࡨࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵࡧࡧࠤ࡮ࡴࠠࡢࠢࡶࡩࡵࡧࡲࡢࡶࡨࠤࡕࡿࡴࡩࡱࡱࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࡺ࡯ࠡࡣࡹࡳ࡮ࡪࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡻࡷࡩࡸࡺࠠࡪࡵࡶࡹࡪࡹ࠮ࠣࠤࠥሔ")
    bstack1lll11ll1ll_opy_ = [sys.executable, bstack1ll1lll_opy_ (u"ࠤ࠰ࡱࠧሕ"), bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥሖ"), bstack1ll1lll_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧሗ"), bstack1ll1lll_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨመ")]
    bstack1lll11l1lll_opy_ = [a for a in args if a not in (bstack1ll1lll_opy_ (u"ࠨ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢሙ"), bstack1ll1lll_opy_ (u"ࠢ࠮࠯ࡴࡹ࡮࡫ࡴࠣሚ"), bstack1ll1lll_opy_ (u"ࠣ࠯ࡴࠦማ"))]
    cmd = bstack1lll11ll1ll_opy_ + bstack1lll11l1lll_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1lll11ll111_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1ll1lll_opy_ (u"ࠤࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨሜ") in line.lower():
                continue
            if bstack1ll1lll_opy_ (u"ࠥ࠾࠿ࠨም") in line:
                bstack1lll11ll111_opy_.append(line)
                file_path = line.split(bstack1ll1lll_opy_ (u"ࠦ࠿ࡀࠢሞ"), 1)[0]
                if file_path.endswith(bstack1ll1lll_opy_ (u"ࠬ࠴ࡰࡺࠩሟ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1ll1lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢሠ"): success,
            bstack1ll1lll_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨሡ"): len(bstack1lll11ll111_opy_),
            bstack1ll1lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤሢ"): bstack1lll11ll111_opy_,
            bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨሣ"): sorted(test_files),
            bstack1ll1lll_opy_ (u"ࠥࡩࡽ࡯ࡴࡠࡥࡲࡨࡪࠨሤ"): proc.returncode,
            bstack1ll1lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥሥ"): None if success else bstack1ll1lll_opy_ (u"࡙ࠧࡵࡣࡲࡵࡳࡨ࡫ࡳࡴࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࠨࡦࡺ࡬ࡸࠥࢁࡽࠪࠤሦ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1ll1lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢሧ"): False, bstack1ll1lll_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨረ"): 0, bstack1ll1lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤሩ"): [], bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨሪ"): [], bstack1ll1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤራ"): bstack1ll1lll_opy_ (u"ࠦࡘࡻࡢࡱࡴࡲࡧࡪࡹࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣሬ").format(e)}