"""Windows system-theme and desktop-wallpaper detection for BeUp.

The values exposed here are *read-only observations* of the operating
system: which light/dark mode Windows is using, and which file is the
current desktop wallpaper.  Nothing here changes a system setting.

Registry keys (Windows only, HKCU):

* ``Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize``
  value ``AppsUseLightTheme`` (DWORD): ``1`` means apps should use the
  light theme, ``0`` means dark.  Any missing/unreadable value falls back
  to dark.
* ``Control Panel\\Desktop`` value ``Wallpaper`` (string): the path of
  the current desktop wallpaper image.  A path is only returned when the
  file actually exists, so callers can treat ``None`` as "no wallpaper
  available" and fall back to the dark palette.

On any non-Windows platform (or when ``winreg`` cannot be imported) both
functions fall back without raising: :func:`system_theme_mode` returns
``"dark"`` and :func:`desktop_wallpaper_path` returns ``None``.

The cached variants keep registry reads out of the render path: the
snapshot is refreshed at most once per :data:`_CACHE_TTL_SECONDS`
unless :func:`refresh_system_theme_cache` is called (the settings
controller calls it whenever the theme setting changes).
"""

from __future__ import annotations

import os
import sys
import threading
import time

try:  # winreg exists only on Windows; guarded so this module imports on Linux.
    import winreg
except ImportError:  # pragma: no cover - non-Windows platforms
    winreg = None  # type: ignore[assignment]

THEME_MODES = ("light", "dark", "system", "wallpaper")
DEFAULT_THEME_MODE = "system"
LEGACY_THEME_MODES = {"graphite": "dark"}

_PERSONALIZE_KEY = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
_DESKTOP_KEY = r"Control Panel\Desktop"

_CACHE_TTL_SECONDS = 30.0
_cache_lock = threading.Lock()
_cache_timestamp = 0.0
_cache_snapshot: dict[str, object] | None = None


def normalize_theme_mode(value: object) -> str:
    """Map a stored/legacy theme value to one of :data:`THEME_MODES`."""
    text = str(value or "").strip().lower()
    if text in LEGACY_THEME_MODES:
        return LEGACY_THEME_MODES[text]
    if text in THEME_MODES:
        return text
    return DEFAULT_THEME_MODE


def _read_registry_string(key_path: str, value_name: str) -> str | None:
    if winreg is None or sys.platform != "win32":
        return None
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _kind = winreg.QueryValueEx(key, value_name)
    except OSError:
        return None
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _read_registry_dword(key_path: str, value_name: str) -> int | None:
    if winreg is None or sys.platform != "win32":
        return None
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _kind = winreg.QueryValueEx(key, value_name)
    except OSError:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def system_theme_mode() -> str:
    """Return ``"light"`` or ``"dark"`` for the Windows app theme.

    Reads ``AppsUseLightTheme``; ``1`` is light, ``0`` (or anything
    unreadable, including every non-Windows platform) is dark.
    """
    apps_use_light = _read_registry_dword(_PERSONALIZE_KEY, "AppsUseLightTheme")
    return "light" if apps_use_light == 1 else "dark"


def desktop_wallpaper_path() -> str | None:
    """Return the current Windows desktop wallpaper path, or ``None``.

    Reads the ``Wallpaper`` value under ``Control Panel\\Desktop`` and
    only returns it when the file exists on disk.
    """
    path = _read_registry_string(_DESKTOP_KEY, "Wallpaper")
    if path and os.path.isfile(path):
        return path
    return None


def _fresh_snapshot() -> dict[str, object]:
    return {
        "system_theme_mode": system_theme_mode(),
        "desktop_wallpaper_path": desktop_wallpaper_path(),
    }


def system_theme_snapshot() -> dict[str, object]:
    """Return the cached ``{system_theme_mode, desktop_wallpaper_path}`` pair.

    The registry is re-read at most once per TTL so QML property reads
    (which can happen on every settings change) never hit the registry
    on every frame.
    """
    global _cache_timestamp, _cache_snapshot
    now = time.monotonic()
    with _cache_lock:
        if _cache_snapshot is None or now - _cache_timestamp >= _CACHE_TTL_SECONDS:
            _cache_snapshot = _fresh_snapshot()
            _cache_timestamp = now
        return dict(_cache_snapshot)


def cached_system_theme_mode() -> str:
    """Cached variant of :func:`system_theme_mode`."""
    return str(system_theme_snapshot()["system_theme_mode"])


def cached_desktop_wallpaper_path() -> str | None:
    """Cached variant of :func:`desktop_wallpaper_path`."""
    value = system_theme_snapshot()["desktop_wallpaper_path"]
    return str(value) if value else None


def refresh_system_theme_cache() -> dict[str, object]:
    """Force an immediate registry re-read and return the new snapshot."""
    global _cache_timestamp, _cache_snapshot
    snapshot = _fresh_snapshot()
    with _cache_lock:
        _cache_snapshot = dict(snapshot)
        _cache_timestamp = time.monotonic()
    return dict(snapshot)
