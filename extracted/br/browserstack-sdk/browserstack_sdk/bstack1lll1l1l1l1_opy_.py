# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࡑࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡫ࡩࡱࡶࡥࡳࠢࡸࡷ࡮ࡴࡧࠡࡦ࡬ࡶࡪࡩࡴࠡࡲࡼࡸࡪࡹࡴࠡࡪࡲࡳࡰࡹ࠮ࠋࠤࠥࠦᇟ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1lll1l1l1ll_opy_(bstack1lll1l1lll1_opy_=None, bstack1lll1l11ll1_opy_=None):
    bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࠦࡰࡺࡶࡨࡷࡹࠦࡴࡦࡵࡷࡷࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠫࡸࠦࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡࡃࡓࡍࡸ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡤࡶ࡬ࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡱࡻࡷࡩࡸࡺࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣ࡭ࡳࡩ࡬ࡶࡦ࡬ࡲ࡬ࠦࡰࡢࡶ࡫ࡷࠥࡧ࡮ࡥࠢࡩࡰࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗࡥࡰ࡫ࡳࠡࡲࡵࡩࡨ࡫ࡤࡦࡰࡦࡩࠥࡵࡶࡦࡴࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࡪࡨࠣࡦࡴࡺࡨࠡࡣࡵࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡱࡣࡷ࡬ࡸࠦࠨ࡭࡫ࡶࡸࠥࡵࡲࠡࡵࡷࡶ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡘࡪࡹࡴࠡࡨ࡬ࡰࡪ࠮ࡳࠪ࠱ࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠭࡯ࡥࡴࠫࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡧࡴࡲࡱ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡄࡣࡱࠤࡧ࡫ࠠࡢࠢࡶ࡭ࡳ࡭࡬ࡦࠢࡳࡥࡹ࡮ࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡏࡧ࡯ࡱࡵࡩࡩࠦࡩࡧࠢࡷࡩࡸࡺ࡟ࡢࡴࡪࡷࠥ࡯ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹ࡬ࡸ࡭ࠦ࡫ࡦࡻࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡹࡵࡤࡥࡨࡷࡸࠦࠨࡣࡱࡲࡰ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡣࡰࡷࡱࡸࠥ࠮ࡩ࡯ࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡳࡵࡤࡦ࡫ࡧࡷࠥ࠮࡬ࡪࡵࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠢࠫࡰ࡮ࡹࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡨࡶࡷࡵࡲࠡࠪࡶࡸࡷ࠯ࠊࠡࠢࠣࠤࠧࠨࠢᇠ")
    try:
        bstack1lll1l1ll11_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠨࡐ࡚ࡖࡈࡗ࡙ࡥࡃࡖࡔࡕࡉࡓ࡚࡟ࡕࡇࡖࡘࠧᇡ")) is not None
        if bstack1lll1l1lll1_opy_ is not None:
            args = list(bstack1lll1l1lll1_opy_)
        elif bstack1lll1l11ll1_opy_ is not None:
            if isinstance(bstack1lll1l11ll1_opy_, str):
                args = [bstack1lll1l11ll1_opy_]
            elif isinstance(bstack1lll1l11ll1_opy_, list):
                args = list(bstack1lll1l11ll1_opy_)
            else:
                args = [bstack1ll1lll_opy_ (u"ࠢ࠯ࠤᇢ")]
        else:
            args = [bstack1ll1lll_opy_ (u"ࠣ࠰ࠥᇣ")]
        if bstack1lll1l1ll11_opy_:
            return _1lll1l1ll1l_opy_(args)
        bstack1lll1l1l11l_opy_ = args + [
            bstack1ll1lll_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥᇤ"),
            bstack1ll1lll_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦᇥ")
        ]
        class bstack1lll1l1llll_opy_:
            bstack1ll1lll_opy_ (u"ࠦࠧࠨࡐࡺࡶࡨࡷࡹࠦࡰ࡭ࡷࡪ࡭ࡳࠦࡴࡩࡣࡷࠤࡨࡧࡰࡵࡷࡵࡩࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡷࡩࡸࡺࠠࡪࡶࡨࡱࡸ࠴ࠢࠣࠤᇦ")
            def __init__(self):
                self.bstack1lll1l11l1l_opy_ = []
                self.test_files = set()
                self.bstack1lll1l11lll_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1ll1lll_opy_ (u"ࠧࠨࠢࡉࡱࡲ࡯ࠥࡩࡡ࡭࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫࡯࡮ࡪࡵ࡫ࡩࡩ࠴ࠢࠣࠤᇧ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1lll1l11l1l_opy_.append(nodeid)
                        if bstack1ll1lll_opy_ (u"ࠨ࠺࠻ࠤᇨ") in nodeid:
                            file_path = nodeid.split(bstack1ll1lll_opy_ (u"ࠢ࠻࠼ࠥᇩ"), 1)[0]
                            if file_path.endswith(bstack1ll1lll_opy_ (u"ࠨ࠰ࡳࡽࠬᇪ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lll1l11lll_opy_ = str(e)
        collector = bstack1lll1l1llll_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1lll1l1l11l_opy_, plugins=[collector])
        if collector.bstack1lll1l11lll_opy_:
            return {bstack1ll1lll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᇫ"): False, bstack1ll1lll_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤᇬ"): 0, bstack1ll1lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧᇭ"): [], bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤᇮ"): [], bstack1ll1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᇯ"): bstack1ll1lll_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᇰ").format(collector.bstack1lll1l11lll_opy_)}
        return {
            bstack1ll1lll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᇱ"): True,
            bstack1ll1lll_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣᇲ"): len(collector.bstack1lll1l11l1l_opy_),
            bstack1ll1lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦᇳ"): collector.bstack1lll1l11l1l_opy_,
            bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣᇴ"): sorted(collector.test_files),
            bstack1ll1lll_opy_ (u"ࠧ࡫ࡸࡪࡶࡢࡧࡴࡪࡥࠣᇵ"): exit_code
        }
    except Exception as e:
        return {bstack1ll1lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᇶ"): False, bstack1ll1lll_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨᇷ"): 0, bstack1ll1lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤᇸ"): [], bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨᇹ"): [], bstack1ll1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᇺ"): bstack1ll1lll_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᇻ").format(e)}
def _1lll1l1ll1l_opy_(args):
    bstack1ll1lll_opy_ (u"ࠧࠨࠢࡊࡵࡲࡰࡦࡺࡥࡥࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡫ࡤࠡ࡫ࡱࠤࡦࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡷࡳࠥࡧࡶࡰ࡫ࡧࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡿࡴࡦࡵࡷࠤ࡮ࡹࡳࡶࡧࡶ࠲ࠧࠨࠢᇼ")
    bstack1lll1ll1111_opy_ = [sys.executable, bstack1ll1lll_opy_ (u"ࠨ࠭࡮ࠤᇽ"), bstack1ll1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᇾ"), bstack1ll1lll_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤᇿ"), bstack1ll1lll_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥሀ")]
    bstack1lll1l1l111_opy_ = [a for a in args if a not in (bstack1ll1lll_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦሁ"), bstack1ll1lll_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧሂ"), bstack1ll1lll_opy_ (u"ࠧ࠳ࡱࠣሃ"))]
    cmd = bstack1lll1ll1111_opy_ + bstack1lll1l1l111_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1lll1l11l1l_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1ll1lll_opy_ (u"ࠨࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥሄ") in line.lower():
                continue
            if bstack1ll1lll_opy_ (u"ࠢ࠻࠼ࠥህ") in line:
                bstack1lll1l11l1l_opy_.append(line)
                file_path = line.split(bstack1ll1lll_opy_ (u"ࠣ࠼࠽ࠦሆ"), 1)[0]
                if file_path.endswith(bstack1ll1lll_opy_ (u"ࠩ࠱ࡴࡾ࠭ሇ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1ll1lll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦለ"): success,
            bstack1ll1lll_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥሉ"): len(bstack1lll1l11l1l_opy_),
            bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨሊ"): bstack1lll1l11l1l_opy_,
            bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥላ"): sorted(test_files),
            bstack1ll1lll_opy_ (u"ࠢࡦࡺ࡬ࡸࡤࡩ࡯ࡥࡧࠥሌ"): proc.returncode,
            bstack1ll1lll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢል"): None if success else bstack1ll1lll_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࠬࡪࡾࡩࡵࠢࡾࢁ࠮ࠨሎ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1ll1lll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦሏ"): False, bstack1ll1lll_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥሐ"): 0, bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨሑ"): [], bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥሒ"): [], bstack1ll1lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨሓ"): bstack1ll1lll_opy_ (u"ࠣࡕࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧሔ").format(e)}