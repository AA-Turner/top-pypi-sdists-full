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
bstack1ll11_opy_ (u"ࠥࠦࠧࠐࡐࡺࡶࡨࡷࡹࠦࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡪࡨࡰࡵ࡫ࡲࠡࡷࡶ࡭ࡳ࡭ࠠࡥ࡫ࡵࡩࡨࡺࠠࡱࡻࡷࡩࡸࡺࠠࡩࡱࡲ࡯ࡸ࠴ࠊࠣࠤࠥለ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1lll11llll1_opy_(bstack1lll11ll1ll_opy_=None, bstack1lll11ll11l_opy_=None):
    bstack1ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡈࡵ࡬࡭ࡧࡦࡸࠥࡶࡹࡵࡧࡶࡸࠥࡺࡥࡴࡶࡶࠤࡺࡹࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠪࡷࠥ࡯࡮ࡵࡧࡵࡲࡦࡲࠠࡂࡒࡌࡷ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡣࡵ࡫ࡸࠦࠨ࡭࡫ࡶࡸ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡇࡴࡳࡰ࡭ࡧࡷࡩࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡰࡺࡶࡨࡷࡹࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢ࡬ࡲࡨࡲࡵࡥ࡫ࡱ࡫ࠥࡶࡡࡵࡪࡶࠤࡦࡴࡤࠡࡨ࡯ࡥ࡬ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖࡤ࡯ࡪࡹࠠࡱࡴࡨࡧࡪࡪࡥ࡯ࡥࡨࠤࡴࡼࡥࡳࠢࡷࡩࡸࡺ࡟ࡱࡣࡷ࡬ࡸࠦࡩࡧࠢࡥࡳࡹ࡮ࠠࡢࡴࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡰࡢࡶ࡫ࡷࠥ࠮࡬ࡪࡵࡷࠤࡴࡸࠠࡴࡶࡵ࠰ࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠩ࠻ࠢࡗࡩࡸࡺࠠࡧ࡫࡯ࡩ࠭ࡹࠩ࠰ࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠬ࡮࡫ࡳࠪࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡦࡳࡱࡰ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡃࡢࡰࠣࡦࡪࠦࡡࠡࡵ࡬ࡲ࡬ࡲࡥࠡࡲࡤࡸ࡭ࠦࡳࡵࡴ࡬ࡲ࡬ࠦ࡯ࡳࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡴࡦࡺࡨࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡎ࡭࡮ࡰࡴࡨࡨࠥ࡯ࡦࠡࡶࡨࡷࡹࡥࡡࡳࡩࡶࠤ࡮ࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸ࡫ࡷ࡬ࠥࡱࡥࡺࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡸࡻࡣࡤࡧࡶࡷࠥ࠮ࡢࡰࡱ࡯࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡩ࡯ࡶࡰࡷࠤ࠭࡯࡮ࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡲࡴࡪࡥࡪࡦࡶࠤ࠭ࡲࡩࡴࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠡࠪ࡯࡭ࡸࡺࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡧࡵࡶࡴࡸࠠࠩࡵࡷࡶ࠮ࠐࠠࠡࠢࠣࠦࠧࠨሉ")
    try:
        bstack1lll11l1ll1_opy_ = os.getenv(bstack1ll11_opy_ (u"ࠧࡖ࡙ࡕࡇࡖࡘࡤࡉࡕࡓࡔࡈࡒ࡙ࡥࡔࡆࡕࡗࠦሊ")) is not None
        if bstack1lll11ll1ll_opy_ is not None:
            args = list(bstack1lll11ll1ll_opy_)
        elif bstack1lll11ll11l_opy_ is not None:
            if isinstance(bstack1lll11ll11l_opy_, str):
                args = [bstack1lll11ll11l_opy_]
            elif isinstance(bstack1lll11ll11l_opy_, list):
                args = list(bstack1lll11ll11l_opy_)
            else:
                args = [bstack1ll11_opy_ (u"ࠨ࠮ࠣላ")]
        else:
            args = [bstack1ll11_opy_ (u"ࠢ࠯ࠤሌ")]
        if bstack1lll11l1ll1_opy_:
            return _1lll11ll111_opy_(args)
        bstack1lll11l1l11_opy_ = args + [
            bstack1ll11_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤል"),
            bstack1ll11_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥሎ")
        ]
        class bstack1lll11lll11_opy_:
            bstack1ll11_opy_ (u"ࠥࠦࠧࡖࡹࡵࡧࡶࡸࠥࡶ࡬ࡶࡩ࡬ࡲࠥࡺࡨࡢࡶࠣࡧࡦࡶࡴࡶࡴࡨࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠡࡶࡨࡷࡹࠦࡩࡵࡧࡰࡷ࠳ࠨࠢࠣሏ")
            def __init__(self):
                self.bstack1lll11lllll_opy_ = []
                self.test_files = set()
                self.bstack1lll11l1l1l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1ll11_opy_ (u"ࠦࠧࠨࡈࡰࡱ࡮ࠤࡨࡧ࡬࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡪࡵࠣࡪ࡮ࡴࡩࡴࡪࡨࡨ࠳ࠨࠢࠣሐ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1lll11lllll_opy_.append(nodeid)
                        if bstack1ll11_opy_ (u"ࠧࡀ࠺ࠣሑ") in nodeid:
                            file_path = nodeid.split(bstack1ll11_opy_ (u"ࠨ࠺࠻ࠤሒ"), 1)[0]
                            if file_path.endswith(bstack1ll11_opy_ (u"ࠧ࠯ࡲࡼࠫሓ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lll11l1l1l_opy_ = str(e)
        collector = bstack1lll11lll11_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1lll11l1l11_opy_, plugins=[collector])
        if collector.bstack1lll11l1l1l_opy_:
            return {bstack1ll11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤሔ"): False, bstack1ll11_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣሕ"): 0, bstack1ll11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦሖ"): [], bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣሗ"): [], bstack1ll11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦመ"): bstack1ll11_opy_ (u"ࠨࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨሙ").format(collector.bstack1lll11l1l1l_opy_)}
        return {
            bstack1ll11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣሚ"): True,
            bstack1ll11_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢማ"): len(collector.bstack1lll11lllll_opy_),
            bstack1ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥሜ"): collector.bstack1lll11lllll_opy_,
            bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢም"): sorted(collector.test_files),
            bstack1ll11_opy_ (u"ࠦࡪࡾࡩࡵࡡࡦࡳࡩ࡫ࠢሞ"): exit_code
        }
    except Exception as e:
        return {bstack1ll11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨሟ"): False, bstack1ll11_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧሠ"): 0, bstack1ll11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣሡ"): [], bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧሢ"): [], bstack1ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣሣ"): bstack1ll11_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡷࡩࡸࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠾ࠥࢁࡽࠣሤ").format(e)}
def _1lll11ll111_opy_(args):
    bstack1ll11_opy_ (u"ࠦࠧࠨࡉࡴࡱ࡯ࡥࡹ࡫ࡤࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡸࡦࡥࡸࡸࡪࡪࠠࡪࡰࠣࡥࠥࡹࡥࡱࡣࡵࡥࡹ࡫ࠠࡑࡻࡷ࡬ࡴࡴࠠࡱࡴࡲࡧࡪࡹࡳࠡࡶࡲࠤࡦࡼ࡯ࡪࡦࠣࡲࡪࡹࡴࡦࡦࠣࡴࡾࡺࡥࡴࡶࠣ࡭ࡸࡹࡵࡦࡵ࠱ࠦࠧࠨሥ")
    bstack1lll11l1lll_opy_ = [sys.executable, bstack1ll11_opy_ (u"ࠧ࠳࡭ࠣሦ"), bstack1ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨሧ"), bstack1ll11_opy_ (u"ࠢ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠣረ"), bstack1ll11_opy_ (u"ࠣ࠯࠰ࡵࡺ࡯ࡥࡵࠤሩ")]
    bstack1lll11ll1l1_opy_ = [a for a in args if a not in (bstack1ll11_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥሪ"), bstack1ll11_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦራ"), bstack1ll11_opy_ (u"ࠦ࠲ࡷࠢሬ"))]
    cmd = bstack1lll11l1lll_opy_ + bstack1lll11ll1l1_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1lll11lllll_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1ll11_opy_ (u"ࠧࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠤር") in line.lower():
                continue
            if bstack1ll11_opy_ (u"ࠨ࠺࠻ࠤሮ") in line:
                bstack1lll11lllll_opy_.append(line)
                file_path = line.split(bstack1ll11_opy_ (u"ࠢ࠻࠼ࠥሯ"), 1)[0]
                if file_path.endswith(bstack1ll11_opy_ (u"ࠨ࠰ࡳࡽࠬሰ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1ll11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥሱ"): success,
            bstack1ll11_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤሲ"): len(bstack1lll11lllll_opy_),
            bstack1ll11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧሳ"): bstack1lll11lllll_opy_,
            bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤሴ"): sorted(test_files),
            bstack1ll11_opy_ (u"ࠨࡥࡹ࡫ࡷࡣࡨࡵࡤࡦࠤስ"): proc.returncode,
            bstack1ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨሶ"): None if success else bstack1ll11_opy_ (u"ࠣࡕࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࠫࡩࡽ࡯ࡴࠡࡽࢀ࠭ࠧሷ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1ll11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥሸ"): False, bstack1ll11_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤሹ"): 0, bstack1ll11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧሺ"): [], bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤሻ"): [], bstack1ll11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧሼ"): bstack1ll11_opy_ (u"ࠢࡔࡷࡥࡴࡷࡵࡣࡦࡵࡶࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦሽ").format(e)}