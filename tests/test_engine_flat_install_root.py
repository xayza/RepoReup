import os
import sys
from unittest.mock import patch

import pytest

from beup.core import paths
from beup.update.state import provision


@pytest.mark.parametrize("entrypoint", ["BeUp.exe", "BeUpCore.exe"])
def test_engine_accepts_flat_core_app_root_without_provisioning(tmp_path, entrypoint):
    root = tmp_path / "BeUp-Core-1.0.1-windows-x64-full"
    root.mkdir()
    (root / entrypoint).write_bytes(b"fixture")
    with patch.object(sys, "frozen", True, create=True), \
         patch.object(sys, "executable", str(tmp_path / "resources/BeUpEngine.exe")), \
         patch.dict(os.environ, {"BEUP_ENGINE_APP_ROOT": str(root)}):
        os.environ.pop("BEUP_SMOKE_TEST", None)
        assert paths.install_root() == root
        assert paths.app_data_dir() == root / "runtime"
    assert not (root / "update-layout.json").exists()


def test_engine_keeps_strict_marker_checks_for_versioned_install(tmp_path):
    provision(tmp_path)
    (tmp_path / "update-layout.json").write_text("{}", encoding="utf-8")
    (tmp_path / "BeUp.exe").touch()
    with patch.object(sys, "frozen", True, create=True), \
         patch.object(sys, "executable", str(tmp_path / "resources/BeUpEngine.exe")), \
         patch.dict(os.environ, {"BEUP_ENGINE_APP_ROOT": str(tmp_path)}):
        os.environ.pop("BEUP_SMOKE_TEST", None)
        with pytest.raises(ValueError):
            paths.install_root()


@pytest.mark.parametrize("versioned", [False, True])
def test_engine_rejects_unknown_or_incomplete_app_root(tmp_path, versioned):
    if versioned:
        (tmp_path / "versions").mkdir()
        (tmp_path / "BeUp.exe").touch()
    with patch.object(sys, "frozen", True, create=True), \
         patch.object(sys, "executable", str(tmp_path / "resources/BeUpEngine.exe")), \
         patch.dict(os.environ, {"BEUP_ENGINE_APP_ROOT": str(tmp_path)}):
        os.environ.pop("BEUP_SMOKE_TEST", None)
        with pytest.raises(ValueError, match="BeUp-Setup.exe"):
            paths.install_root()
    assert not (tmp_path / "runtime").exists()
    assert not (tmp_path / "update-layout.json").exists()
