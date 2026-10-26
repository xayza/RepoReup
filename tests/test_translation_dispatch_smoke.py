"""The frozen acceptance path must use the same parent dispatch as the app."""
import os
from unittest.mock import patch

import pytest

from beup.core.release_smoke import run_translation_smoke


def test_translation_acceptance_cannot_run_against_normal_user_runtime():
    with patch.dict(os.environ, {"BEUP_SMOKE_TEST": "0"}):
        with pytest.raises(RuntimeError, match="isolated"):
            run_translation_smoke("full")


@pytest.mark.parametrize("model,device", [("full", "gpu"), ("q4", "cpu")])
def test_translation_acceptance_runs_core_dispatch_and_shutdown(model, device):
    with (
        patch("beup.core.hardware.configure_processing_device") as configure_device,
        patch("beup.core.hardware.configure_translation_model") as configure_model,
        patch("beup.services.resource_packs.ResourcePackManager") as manager,
        patch("beup.services.translation._worker_command", return_value=["BeUpEngine.exe", "--hymt2-worker"]),
        patch("beup.services.translation._translate_with_hymt2_worker", return_value=["Xin chào, bạn khỏe không?"]) as translate,
        patch("beup.services.translation.shutdown_hymt2_worker") as shutdown,
    ):
        manager.return_value.missing_packs.return_value = []
        result = run_translation_smoke(model)
        assert result["ok"]
        configure_device.assert_called_once_with(device)
        configure_model.assert_called_once_with(model)
        manager.return_value.missing_packs.assert_called_once_with("translation", {"device": device, "translation_model": model})
        translate.assert_called_once()
        shutdown.assert_called_once()
