# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
bstack111l_opy_ (u"ࠤࠥࠦࠏࡖࡹࡵࡧࡶࡸࠥࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡩࡧ࡯ࡴࡪࡸࠠࡶࡵ࡬ࡲ࡬ࠦࡤࡪࡴࡨࡧࡹࠦࡰࡺࡶࡨࡷࡹࠦࡨࡰࡱ࡮ࡷ࠳ࠐࠢࠣࠤጟ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1ll1l1111l1_opy_(bstack1ll1l111ll1_opy_=None, bstack1ll1l1111ll_opy_=None):
    bstack111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡇࡴࡲ࡬ࡦࡥࡷࠤࡵࡿࡴࡦࡵࡷࠤࡹ࡫ࡳࡵࡵࠣࡹࡸ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠩࡶࠤ࡮ࡴࡴࡦࡴࡱࡥࡱࠦࡁࡑࡋࡶ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡢࡴࡪࡷࠥ࠮࡬ࡪࡵࡷ࠰ࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠩ࠻ࠢࡆࡳࡲࡶ࡬ࡦࡶࡨࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡶࡹࡵࡧࡶࡸࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡ࡫ࡱࡧࡱࡻࡤࡪࡰࡪࠤࡵࡧࡴࡩࡵࠣࡥࡳࡪࠠࡧ࡮ࡤ࡫ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡣ࡮ࡩࡸࠦࡰࡳࡧࡦࡩࡩ࡫࡮ࡤࡧࠣࡳࡻ࡫ࡲࠡࡶࡨࡷࡹࡥࡰࡢࡶ࡫ࡷࠥ࡯ࡦࠡࡤࡲࡸ࡭ࠦࡡࡳࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤࡶࡡࡵࡪࡶࠤ࠭ࡲࡩࡴࡶࠣࡳࡷࠦࡳࡵࡴ࠯ࠤࡴࡶࡴࡪࡱࡱࡥࡱ࠯࠺ࠡࡖࡨࡷࡹࠦࡦࡪ࡮ࡨࠬࡸ࠯࠯ࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠫ࡭ࡪࡹࠩࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥ࡬ࡲࡰ࡯࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡉࡡ࡯ࠢࡥࡩࠥࡧࠠࡴ࡫ࡱ࡫ࡱ࡫ࠠࡱࡣࡷ࡬ࠥࡹࡴࡳ࡫ࡱ࡫ࠥࡵࡲࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡳࡥࡹ࡮ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡍ࡬ࡴ࡯ࡳࡧࡧࠤ࡮࡬ࠠࡵࡧࡶࡸࡤࡧࡲࡨࡵࠣ࡭ࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡪࡶ࡫ࠤࡰ࡫ࡹࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡷࡺࡩࡣࡦࡵࡶࠤ࠭ࡨ࡯ࡰ࡮ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡨࡵࡵ࡯ࡶࠣࠬ࡮ࡴࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡱࡳࡩ࡫ࡩࡥࡵࠣࠬࡱ࡯ࡳࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠠࠩ࡮࡬ࡷࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡦࡴࡵࡳࡷࠦࠨࡴࡶࡵ࠭ࠏࠦࠠࠡࠢࠥࠦࠧጠ")
    try:
        bstack1ll1l111l1l_opy_ = os.getenv(bstack111l_opy_ (u"ࠦࡕ࡟ࡔࡆࡕࡗࡣࡈ࡛ࡒࡓࡇࡑࡘࡤ࡚ࡅࡔࡖࠥጡ")) is not None
        if bstack1ll1l111ll1_opy_ is not None:
            args = list(bstack1ll1l111ll1_opy_)
        elif bstack1ll1l1111ll_opy_ is not None:
            if isinstance(bstack1ll1l1111ll_opy_, str):
                args = [bstack1ll1l1111ll_opy_]
            elif isinstance(bstack1ll1l1111ll_opy_, list):
                args = list(bstack1ll1l1111ll_opy_)
            else:
                args = [bstack111l_opy_ (u"ࠧ࠴ࠢጢ")]
        else:
            args = [bstack111l_opy_ (u"ࠨ࠮ࠣጣ")]
        if bstack1ll1l111l1l_opy_:
            return _1ll11llllll_opy_(args)
        bstack1ll1l111111_opy_ = args + [
            bstack111l_opy_ (u"ࠢ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠣጤ"),
            bstack111l_opy_ (u"ࠣ࠯࠰ࡵࡺ࡯ࡥࡵࠤጥ")
        ]
        class bstack1ll11lllll1_opy_:
            bstack111l_opy_ (u"ࠤࠥࠦࡕࡿࡴࡦࡵࡷࠤࡵࡲࡵࡨ࡫ࡱࠤࡹ࡮ࡡࡵࠢࡦࡥࡵࡺࡵࡳࡧࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠠࡵࡧࡶࡸࠥ࡯ࡴࡦ࡯ࡶ࠲ࠧࠨࠢጦ")
            def __init__(self):
                self.bstack1ll11llll1l_opy_ = []
                self.test_files = set()
                self.bstack1ll11lll1ll_opy_ = None
            def pytest_collection_finish(self, session):
                bstack111l_opy_ (u"ࠥࠦࠧࡎ࡯ࡰ࡭ࠣࡧࡦࡲ࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡩࡴࠢࡩ࡭ࡳ࡯ࡳࡩࡧࡧ࠲ࠧࠨࠢጧ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1ll11llll1l_opy_.append(nodeid)
                        if bstack111l_opy_ (u"ࠦ࠿ࡀࠢጨ") in nodeid:
                            file_path = nodeid.split(bstack111l_opy_ (u"ࠧࡀ࠺ࠣጩ"), 1)[0]
                            if file_path.endswith(bstack111l_opy_ (u"࠭࠮ࡱࡻࠪጪ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1ll11lll1ll_opy_ = str(e)
        collector = bstack1ll11lllll1_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1ll1l111111_opy_, plugins=[collector])
        if collector.bstack1ll11lll1ll_opy_:
            return {bstack111l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣጫ"): False, bstack111l_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢጬ"): 0, bstack111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥጭ"): [], bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢጮ"): [], bstack111l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥጯ"): bstack111l_opy_ (u"ࠧࡉ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧጰ").format(collector.bstack1ll11lll1ll_opy_)}
        return {
            bstack111l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢጱ"): True,
            bstack111l_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨጲ"): len(collector.bstack1ll11llll1l_opy_),
            bstack111l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤጳ"): collector.bstack1ll11llll1l_opy_,
            bstack111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨጴ"): sorted(collector.test_files),
            bstack111l_opy_ (u"ࠥࡩࡽ࡯ࡴࡠࡥࡲࡨࡪࠨጵ"): exit_code
        }
    except Exception as e:
        return {bstack111l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧጶ"): False, bstack111l_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦጷ"): 0, bstack111l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢጸ"): [], bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦጹ"): [], bstack111l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢጺ"): bstack111l_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠽ࠤࢀࢃࠢጻ").format(e)}
def _1ll11llllll_opy_(args):
    bstack111l_opy_ (u"ࠥࠦࠧࡏࡳࡰ࡮ࡤࡸࡪࡪࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡾࡥࡤࡷࡷࡩࡩࠦࡩ࡯ࠢࡤࠤࡸ࡫ࡰࡢࡴࡤࡸࡪࠦࡐࡺࡶ࡫ࡳࡳࠦࡰࡳࡱࡦࡩࡸࡹࠠࡵࡱࠣࡥࡻࡵࡩࡥࠢࡱࡩࡸࡺࡥࡥࠢࡳࡽࡹ࡫ࡳࡵࠢ࡬ࡷࡸࡻࡥࡴ࠰ࠥࠦࠧጼ")
    bstack1ll1l111l11_opy_ = [sys.executable, bstack111l_opy_ (u"ࠦ࠲ࡳࠢጽ"), bstack111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧጾ"), bstack111l_opy_ (u"ࠨ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢጿ"), bstack111l_opy_ (u"ࠢ࠮࠯ࡴࡹ࡮࡫ࡴࠣፀ")]
    bstack1ll11llll11_opy_ = [a for a in args if a not in (bstack111l_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤፁ"), bstack111l_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥፂ"), bstack111l_opy_ (u"ࠥ࠱ࡶࠨፃ"))]
    cmd = bstack1ll1l111l11_opy_ + bstack1ll11llll11_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1ll11llll1l_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack111l_opy_ (u"ࠦࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠣፄ") in line.lower():
                continue
            if bstack111l_opy_ (u"ࠧࡀ࠺ࠣፅ") in line:
                bstack1ll11llll1l_opy_.append(line)
                file_path = line.split(bstack111l_opy_ (u"ࠨ࠺࠻ࠤፆ"), 1)[0]
                if file_path.endswith(bstack111l_opy_ (u"ࠧ࠯ࡲࡼࠫፇ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack111l_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤፈ"): success,
            bstack111l_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣፉ"): len(bstack1ll11llll1l_opy_),
            bstack111l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦፊ"): bstack1ll11llll1l_opy_,
            bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣፋ"): sorted(test_files),
            bstack111l_opy_ (u"ࠧ࡫ࡸࡪࡶࡢࡧࡴࡪࡥࠣፌ"): proc.returncode,
            bstack111l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧፍ"): None if success else bstack111l_opy_ (u"ࠢࡔࡷࡥࡴࡷࡵࡣࡦࡵࡶࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࠪࡨࡼ࡮ࡺࠠࡼࡿࠬࠦፎ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack111l_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤፏ"): False, bstack111l_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣፐ"): 0, bstack111l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦፑ"): [], bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣፒ"): [], bstack111l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦፓ"): bstack111l_opy_ (u"ࠨࡓࡶࡤࡳࡶࡴࡩࡥࡴࡵࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥፔ").format(e)}