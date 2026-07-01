# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࡑࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡫ࡩࡱࡶࡥࡳࠢࡸࡷ࡮ࡴࡧࠡࡦ࡬ࡶࡪࡩࡴࠡࡲࡼࡸࡪࡹࡴࠡࡪࡲࡳࡰࡹ࠮ࠋࠤࠥࠦఓ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1l11111l1_opy_(bstack1l1111l11_opy_=None, bstack1l11111ll_opy_=None):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࠦࡰࡺࡶࡨࡷࡹࠦࡴࡦࡵࡷࡷࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠫࡸࠦࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡࡃࡓࡍࡸ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡤࡶ࡬ࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡱࡻࡷࡩࡸࡺࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣ࡭ࡳࡩ࡬ࡶࡦ࡬ࡲ࡬ࠦࡰࡢࡶ࡫ࡷࠥࡧ࡮ࡥࠢࡩࡰࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗࡥࡰ࡫ࡳࠡࡲࡵࡩࡨ࡫ࡤࡦࡰࡦࡩࠥࡵࡶࡦࡴࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࡪࡨࠣࡦࡴࡺࡨࠡࡣࡵࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡱࡣࡷ࡬ࡸࠦࠨ࡭࡫ࡶࡸࠥࡵࡲࠡࡵࡷࡶ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡘࡪࡹࡴࠡࡨ࡬ࡰࡪ࠮ࡳࠪ࠱ࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠭࡯ࡥࡴࠫࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡧࡴࡲࡱ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡄࡣࡱࠤࡧ࡫ࠠࡢࠢࡶ࡭ࡳ࡭࡬ࡦࠢࡳࡥࡹ࡮ࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡏࡧ࡯ࡱࡵࡩࡩࠦࡩࡧࠢࡷࡩࡸࡺ࡟ࡢࡴࡪࡷࠥ࡯ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹ࡬ࡸ࡭ࠦ࡫ࡦࡻࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡹࡵࡤࡥࡨࡷࡸࠦࠨࡣࡱࡲࡰ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡣࡰࡷࡱࡸࠥ࠮ࡩ࡯ࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡳࡵࡤࡦ࡫ࡧࡷࠥ࠮࡬ࡪࡵࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠢࠫࡰ࡮ࡹࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡨࡶࡷࡵࡲࠡࠪࡶࡸࡷ࠯ࠊࠡࠢࠣࠤࠧࠨࠢఔ")
    try:
        bstack1l1111lll_opy_ = os.getenv(bstack1l1llll_opy_ (u"ࠨࡐ࡚ࡖࡈࡗ࡙ࡥࡃࡖࡔࡕࡉࡓ࡚࡟ࡕࡇࡖࡘࠧక")) is not None
        if bstack1l1111l11_opy_ is not None:
            args = list(bstack1l1111l11_opy_)
        elif bstack1l11111ll_opy_ is not None:
            if isinstance(bstack1l11111ll_opy_, str):
                args = [bstack1l11111ll_opy_]
            elif isinstance(bstack1l11111ll_opy_, list):
                args = list(bstack1l11111ll_opy_)
            else:
                args = [bstack1l1llll_opy_ (u"ࠢ࠯ࠤఖ")]
        else:
            args = [bstack1l1llll_opy_ (u"ࠣ࠰ࠥగ")]
        if bstack1l1111lll_opy_:
            return _1l111l111_opy_(args)
        bstack1l111l1ll_opy_ = args + [
            bstack1l1llll_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥఘ"),
            bstack1l1llll_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦఙ")
        ]
        class bstack1l1111ll1_opy_:
            bstack1l1llll_opy_ (u"ࠦࠧࠨࡐࡺࡶࡨࡷࡹࠦࡰ࡭ࡷࡪ࡭ࡳࠦࡴࡩࡣࡷࠤࡨࡧࡰࡵࡷࡵࡩࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡷࡩࡸࡺࠠࡪࡶࡨࡱࡸ࠴ࠢࠣࠤచ")
            def __init__(self):
                self.bstack1l111l1l1_opy_ = []
                self.test_files = set()
                self.bstack1l111ll1l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1l1llll_opy_ (u"ࠧࠨࠢࡉࡱࡲ࡯ࠥࡩࡡ࡭࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫࡯࡮ࡪࡵ࡫ࡩࡩ࠴ࠢࠣࠤఛ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1l111l1l1_opy_.append(nodeid)
                        if bstack1l1llll_opy_ (u"ࠨ࠺࠻ࠤజ") in nodeid:
                            file_path = nodeid.split(bstack1l1llll_opy_ (u"ࠢ࠻࠼ࠥఝ"), 1)[0]
                            if file_path.endswith(bstack1l1llll_opy_ (u"ࠨ࠰ࡳࡽࠬఞ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1l111ll1l_opy_ = str(e)
        collector = bstack1l1111ll1_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1l111l1ll_opy_, plugins=[collector])
        if collector.bstack1l111ll1l_opy_:
            return {bstack1l1llll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥట"): False, bstack1l1llll_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤఠ"): 0, bstack1l1llll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧడ"): [], bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤఢ"): [], bstack1l1llll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧణ"): bstack1l1llll_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢత").format(collector.bstack1l111ll1l_opy_)}
        return {
            bstack1l1llll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤథ"): True,
            bstack1l1llll_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣద"): len(collector.bstack1l111l1l1_opy_),
            bstack1l1llll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦధ"): collector.bstack1l111l1l1_opy_,
            bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣన"): sorted(collector.test_files),
            bstack1l1llll_opy_ (u"ࠧ࡫ࡸࡪࡶࡢࡧࡴࡪࡥࠣ఩"): exit_code
        }
    except Exception as e:
        return {bstack1l1llll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢప"): False, bstack1l1llll_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨఫ"): 0, bstack1l1llll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤబ"): [], bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨభ"): [], bstack1l1llll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤమ"): bstack1l1llll_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤయ").format(e)}
def _1l111l111_opy_(args):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࡊࡵࡲࡰࡦࡺࡥࡥࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡫ࡤࠡ࡫ࡱࠤࡦࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡷࡳࠥࡧࡶࡰ࡫ࡧࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡿࡴࡦࡵࡷࠤ࡮ࡹࡳࡶࡧࡶ࠲ࠧࠨࠢర")
    bstack1l111l11l_opy_ = [sys.executable, bstack1l1llll_opy_ (u"ࠨ࠭࡮ࠤఱ"), bstack1l1llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢల"), bstack1l1llll_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤళ"), bstack1l1llll_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥఴ")]
    bstack1l111ll11_opy_ = [a for a in args if a not in (bstack1l1llll_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦవ"), bstack1l1llll_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧశ"), bstack1l1llll_opy_ (u"ࠧ࠳ࡱࠣష"))]
    cmd = bstack1l111l11l_opy_ + bstack1l111ll11_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1l111l1l1_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1l1llll_opy_ (u"ࠨࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥస") in line.lower():
                continue
            if bstack1l1llll_opy_ (u"ࠢ࠻࠼ࠥహ") in line:
                bstack1l111l1l1_opy_.append(line)
                file_path = line.split(bstack1l1llll_opy_ (u"ࠣ࠼࠽ࠦ఺"), 1)[0]
                if file_path.endswith(bstack1l1llll_opy_ (u"ࠩ࠱ࡴࡾ࠭఻")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1l1llll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ఼ࠦ"): success,
            bstack1l1llll_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥఽ"): len(bstack1l111l1l1_opy_),
            bstack1l1llll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨా"): bstack1l111l1l1_opy_,
            bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥి"): sorted(test_files),
            bstack1l1llll_opy_ (u"ࠢࡦࡺ࡬ࡸࡤࡩ࡯ࡥࡧࠥీ"): proc.returncode,
            bstack1l1llll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢు"): None if success else bstack1l1llll_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࠬࡪࡾࡩࡵࠢࡾࢁ࠮ࠨూ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1l1llll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦృ"): False, bstack1l1llll_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥౄ"): 0, bstack1l1llll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨ౅"): [], bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥె"): [], bstack1l1llll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨే"): bstack1l1llll_opy_ (u"ࠣࡕࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧై").format(e)}