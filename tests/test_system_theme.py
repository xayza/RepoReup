import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from beup.desktop import system_theme
from beup.services import desktop_settings


class SystemThemeTests(unittest.TestCase):
    def test_linux_falls_back_to_dark_and_no_wallpaper(self):
        # winreg is unavailable on this platform, so both fallbacks apply.
        self.assertEqual(system_theme.system_theme_mode(), "dark")
        self.assertIsNone(system_theme.desktop_wallpaper_path())
        self.assertEqual(system_theme.cached_system_theme_mode(), "dark")
        self.assertIsNone(system_theme.cached_desktop_wallpaper_path())

    def test_cached_snapshot_is_reused_within_ttl(self):
        system_theme.refresh_system_theme_cache()
        first = system_theme.system_theme_snapshot()
        with patch.object(system_theme, "_fresh_snapshot") as fresh:
            fresh.side_effect = AssertionError("registry must not be re-read within TTL")
            second = system_theme.system_theme_snapshot()
        self.assertEqual(first, second)

    def test_normalize_theme_mode_maps_legacy_and_invalid_values(self):
        self.assertEqual(system_theme.normalize_theme_mode("graphite"), "dark")
        self.assertEqual(system_theme.normalize_theme_mode("wallpaper"), "wallpaper")
        self.assertEqual(system_theme.normalize_theme_mode("bogus"), "system")
        self.assertEqual(system_theme.normalize_theme_mode(None), "system")

    def test_theme_mode_round_trips_through_desktop_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "desktop-settings.json"
            with patch.object(desktop_settings, "SETTINGS_PATH", path):
                self.assertEqual(desktop_settings.load_settings()["theme"], "system")
                saved = desktop_settings.save_settings({"theme": "wallpaper"})
                self.assertEqual(saved["theme"], "wallpaper")
                self.assertEqual(desktop_settings.load_settings()["theme"], "wallpaper")
                saved = desktop_settings.save_settings({"theme": "graphite"})
                self.assertEqual(saved["theme"], "dark")
                path.write_text(json.dumps({"theme": "nonsense"}), encoding="utf-8")
                self.assertEqual(desktop_settings.load_settings()["theme"], "system")


if __name__ == "__main__":
    unittest.main()
