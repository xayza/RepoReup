"""Lightweight model/device choices shared by Core, workers and desktop UI.

Hardware policy (BeUp batch 2): downloading or installing a listed model or
resource pack is NEVER blocked by VRAM/GPU/CPU capability. The helpers that
used to gate on hardware now return a Vietnamese warning string ("" means no
warning) so the UI can show it and let the user continue. The only hardware
fallback left is at RUN time: a GPU model requested without a GPU runs on
its CPU equivalent (see :func:`recognition_context` and
:func:`models_for_device`) instead of crashing, and the fallback is explicit
in the returned dict -- the caller never silently pretends it ran on GPU.
"""

# Legacy project values that must keep loading, plus the expanded
# faster-whisper catalog. Device-agnostic ids (medium, large-v3,
# distil-large-v3) run on whichever device the app is using; the suffixed
# small-* ids are the historical device variants of Whisper Small.
RECOGNITION_CHOICES = frozenset({
    "small", "small-cpu", "small-gpu",
    "medium", "large-v3", "large-v3-turbo", "distil-large-v3",
})
# Whisper directory/model name for each catalog id, as used by the engine
# loader (models/whisper/<name>). New ids map to themselves.
_RECOGNITION_MODEL_DIR = {
    "small": "small",
    "small-cpu": "small",
    "small-gpu": "small",
    "medium": "medium",
    "large-v3": "large-v3",
    "large-v3-turbo": "large-v3-turbo",
    "distil-large-v3": "distil-large-v3",
}
# Catalog ids that are GPU-only in the pinned-pack sense: their shipped pack
# is a GPU backend pack, so on a CPU-only run they fall back to Whisper
# Small on CPU (the established CPU equivalent), never to a crash.
_GPU_PACK_RECOGNITION = frozenset({"large-v3-turbo"})
_FOUR_GB_GPU_LIMIT_BYTES = 5 * 1024**3
_LEGACY_AUTO_FULL_VRAM_BYTES = 12 * 1024**3

# Recommended configuration per model, in Vietnamese, for the model picker /
# Model Manager UI. "download_status" is honest about the download path:
#   "verified"   -- checksum-pinned pack already shipped by the app;
#   "unverified" -- real Hugging Face repo, downloaded by the existing
#                   asset mechanism, but without a pinned SHA-256 (the
#                   exact sizes/hashes were not verified from the repo);
#   "pack-pending" -- no downloadable pack exists yet; the UI must disable
#                   the download button and show "Chưa có gói tải".
# Disk sizes for verified packs are the pinned totals from the repo;
# unverified sizes are approximate (marked "~") from the public parameter
# counts, never invented pinned bytes.
MODEL_RECOMMENDATIONS = {
    "small": {
        "model_id": "Systran/faster-whisper-small",
        "ram_gb": 8,
        "vram": "CPU là đủ",
        "disk": "~0,5 GB",
        "quality_vs_speed": "Nhanh, đủ tốt cho hầu hết video; bản mặc định cho máy yếu.",
        "download_status": "verified",
    },
    "small-cpu": {
        "model_id": "Systran/faster-whisper-small",
        "ram_gb": 8,
        "vram": "CPU là đủ",
        "disk": "~0,5 GB",
        "quality_vs_speed": "Nhanh, đủ tốt cho hầu hết video; bản CPU của Whisper Small.",
        "download_status": "verified",
    },
    "small-gpu": {
        "model_id": "Systran/faster-whisper-small",
        "ram_gb": 8,
        "vram": "≥ 4 GB",
        "disk": "~0,5 GB",
        "quality_vs_speed": "Nhanh nhất trên GPU; chất lượng như bản CPU.",
        "download_status": "verified",
    },
    "medium": {
        "model_id": "Systran/faster-whisper-medium",
        "ram_gb": 16,
        "vram": "≥ 6 GB (GPU) hoặc CPU là đủ (chậm hơn)",
        "disk": "~1,6 GB (ước tính)",
        "quality_vs_speed": "Chính xác hơn Small rõ rệt, chậm hơn khoảng 2-3 lần; cân bằng tốt.",
        "download_status": "unverified",
    },
    "large-v3": {
        "model_id": "Systran/faster-whisper-large-v3",
        "ram_gb": 16,
        "vram": "≥ 10 GB (GPU) hoặc CPU là đủ (rất chậm)",
        "disk": "~3,2 GB (ước tính)",
        "quality_vs_speed": "Chính xác nhất, chậm nhất; chỉ nên dùng khi cần độ chính xác tối đa.",
        "download_status": "unverified",
    },
    "large-v3-turbo": {
        "model_id": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
        "ram_gb": 16,
        "vram": "≥ 5 GB",
        "disk": "~1,6 GB",
        "quality_vs_speed": "Gần bằng large-v3 nhưng nhanh hơn nhiều; bản GPU mặc định.",
        "download_status": "verified",
    },
    "distil-large-v3": {
        "model_id": "Systran/faster-distil-whisper-large-v3",
        "ram_gb": 16,
        "vram": "≥ 6 GB (GPU) hoặc CPU là đủ (chậm hơn)",
        "disk": "~1,6 GB (ước tính)",
        "quality_vs_speed": "Nhanh gần bằng Turbo, chính xác gần large-v3 với tiếng Anh; tiếng Việt kém hơn large-v3.",
        "download_status": "unverified",
    },
    "q4": {
        "model_id": "tencent/Hy-MT2-1.8B-GGUF (Q4_K_M)",
        "ram_gb": 8,
        "vram": "CPU là đủ",
        "disk": "~1,1 GB",
        "quality_vs_speed": "Bản dịch CPU nhẹ, nhanh; chất lượng thấp hơn bản GPU đầy đủ.",
        "download_status": "verified",
    },
    "full": {
        "model_id": "tencent/Hy-MT2-1.8B",
        "ram_gb": 16,
        "vram": "≥ 5 GB",
        "disk": "~4,1 GB",
        "quality_vs_speed": "Bản dịch GPU đầy đủ, chính xác nhất; cần GPU NVIDIA.",
        "download_status": "verified",
    },
    "vieneu": {
        "model_id": "VieNeu (gói tài nguyên BeUp)",
        "ram_gb": 8,
        "vram": "CPU là đủ",
        "disk": "~1,0 GB",
        "quality_vs_speed": "Giọng Việt tự nhiên trên CPU; chậm hơn bản GPU một chút.",
        "download_status": "verified",
    },
    "vieneu-gpu": {
        "model_id": "VieNeu (gói tài nguyên BeUp)",
        "ram_gb": 8,
        "vram": "≥ 4 GB",
        "disk": "~1,0 GB",
        "quality_vs_speed": "Giọng Việt tự nhiên, nhanh hơn trên GPU.",
        "download_status": "verified",
    },
    "omnivoice": {
        "model_id": "k2-fsa/OmniVoice",
        "ram_gb": 16,
        "vram": "CPU là đủ",
        "disk": "~3,3 GB",
        "quality_vs_speed": "Đa ngôn ngữ (Anh/Trung tốt) trên CPU; gói nặng, tải lâu.",
        "download_status": "verified",
    },
    "omnivoice-gpu": {
        "model_id": "k2-fsa/OmniVoice",
        "ram_gb": 16,
        "vram": "≥ 5 GB",
        "disk": "~3,3 GB",
        "quality_vs_speed": "Đa ngôn ngữ (Anh/Trung tốt) trên GPU; nhanh hơn bản CPU.",
        "download_status": "verified",
    },
    "edge": {
        "model_id": "Microsoft Edge TTS (online, không tải weights)",
        "ram_gb": 8,
        "vram": "CPU là đủ",
        "disk": "0 GB (cần mạng)",
        "quality_vs_speed": "Giọng online, không tốn ổ đĩa; cần kết nối mạng.",
        "download_status": "pack-pending",
    },
}


def model_recommendation(model_id: str) -> dict:
    """Return the recommendation block for a model id ({} if unknown)."""
    return dict(MODEL_RECOMMENDATIONS.get(str(model_id or "").lower(), {}))


def project_recognition_choice(choice: str, app_device: str, *, total_vram_bytes: int | None = None) -> str:
    """Resolve the old automatic default without replacing explicit choices."""
    if not choice or choice == "small":
        return project_model_defaults(app_device, total_vram_bytes=total_vram_bytes)["_speech_recognition_model"]
    return choice


def project_model_defaults(app_device: str, *, total_vram_bytes: int | None = None,
                           target_language: str = "vi") -> dict[str, str]:
    gpu = app_device == "gpu"
    small_gpu = gpu and total_vram_bytes is not None and total_vram_bytes < _FOUR_GB_GPU_LIMIT_BYTES
    return {
        # Keep the established defaults on larger GPUs. On a 4 GB card,
        # Whisper Small and voice synthesis run sequentially on CUDA; translation
        # uses its smaller CPU pack so the full GPU weights never overlap.
        "_speech_recognition_model": "small-gpu" if small_gpu else "large-v3-turbo" if gpu else "small-cpu",
        "_translation_model": "q4" if small_gpu or not gpu else "full",
        "_tts_provider": (("vieneu-gpu" if gpu else "vieneu") if target_language == "vi"
                          else "omnivoice-gpu" if gpu else "omnivoice"),
    }


def default_tts_voice(provider: str) -> str:
    return "vieneu:Hải Đăng" if str(provider).startswith("vieneu") else "omnivoice:female"


def project_translation_choice(choice: str, app_device: str, *, total_vram_bytes: int | None = None) -> str:
    """Resolve saved pre-picker 'auto' to one of the two visible local models."""
    if str(choice or "auto").lower() != "auto":
        return choice
    return "full" if app_device == "gpu" and isinstance(total_vram_bytes, int) \
        and total_vram_bytes >= _LEGACY_AUTO_FULL_VRAM_BYTES else "q4"


def gpu_choice_warning(app_device: str, *, recognition="small", translation="auto", voice="omnivoice") -> str:
    """Warning (never a block) when a GPU choice is used while in CPU mode.

    The caller shows this text and continues; the run-time fallback in
    :func:`models_for_device` / :func:`recognition_context` converts the
    choice to its CPU equivalent at run time.
    """
    if app_device == "gpu":
        return ""
    if (recognition in {"small-gpu", "large-v3-turbo"}
            or translation == "full" or str(voice).endswith("-gpu")):
        return ("Đang dùng chế độ CPU: model GPU đã chọn sẽ chạy bằng bản CPU "
                "tương đương (chậm hơn) hoặc bạn có thể chuyển sang GPU trong "
                "Cài đặt → Chung. Việc tải/cài model không bị chặn.")
    return ""


def heavy_gpu_choice_warning(app_device: str, capabilities, *, recognition: str = "", translation: str = "") -> str:
    """Warning (never a block) for heavy GPU models on a low-VRAM GPU."""
    if not (app_device == "gpu" and capabilities is not None
            and getattr(capabilities, "gpu_supported", False)
            and not getattr(capabilities, "heavy_gpu_models_supported", False)
            and (recognition == "large-v3-turbo" or translation == "full")):
        return ""
    return ("GPU này có dưới 5 GiB VRAM, dưới mức khuyến nghị cho Whisper Turbo "
            "và HY-MT2 GPU đầy đủ: quá trình chạy có thể chậm hoặc thiếu bộ nhớ. "
            "Bạn vẫn có thể tải/cài model; khi chạy, hãy cân nhắc Whisper Small GPU "
            "hoặc HY-MT2 CPU Q4.")


# Backwards-compatible names. They used to return True = blocked; they now
# return a warning string ("" = no warning). Callers must NOT treat a
# non-empty result as a reason to refuse a download/install -- show it and
# continue. Kept so existing imports keep working with the new semantics.
def gpu_choice_blocked(app_device: str, *, recognition="small", translation="auto", voice="omnivoice") -> str:
    return gpu_choice_warning(app_device, recognition=recognition, translation=translation, voice=voice)


def heavy_gpu_choice_blocked(app_device: str, capabilities, *, recognition: str = "", translation: str = "") -> str:
    return heavy_gpu_choice_warning(app_device, capabilities, recognition=recognition, translation=translation)


def models_for_device(app_device: str, *, recognition: str, translation: str, voice: str,
                      total_vram_bytes: int | None = None) -> dict[str, str]:
    """Run-time fallback mapping (NOT a download/install gate).

    Keep compatible project choices, replacing GPU-only choices with their
    CPU equivalents in CPU mode. Device-agnostic recognition ids (medium,
    large-v3, distil-large-v3) run on CPU as-is, only slower, so they are
    kept unchanged. Saved project values are preserved otherwise, so old
    projects still load.
    """
    translation = project_translation_choice(translation, app_device, total_vram_bytes=total_vram_bytes)
    if app_device == "cpu":
        if recognition in {"small-gpu", "large-v3-turbo"}:
            recognition = "small-cpu"
        if translation == "full":
            translation = "q4"
        if voice == "omnivoice-gpu":
            voice = "omnivoice"
        elif voice == "vieneu-gpu":
            voice = "vieneu"
    return {"speech_recognition_model": recognition, "translation_model": translation, "tts_provider": voice}


def recognition_context(choice: str, app_device: str) -> dict[str, str]:
    """Resolve a recognition choice to an engine model + device, with fallback.

    A GPU model requested without a GPU no longer raises: it falls back to
    its CPU equivalent (small-gpu -> small on CPU; large-v3-turbo -> small
    on CPU, matching :func:`models_for_device`). Device-agnostic models
    (medium, large-v3, distil-large-v3) run on the requested device as-is.
    The returned dict always states the device actually used -- it never
    claims GPU execution when the fallback ran.
    """
    choice = str(choice or "small").lower()
    device = "gpu" if app_device == "gpu" else "cpu"
    if choice not in RECOGNITION_CHOICES:
        raise ValueError(f"Unsupported recognition model: {choice}")
    if choice == "small-cpu":
        device = "cpu"
    elif choice == "small-gpu":
        # GPU variant of Small: on CPU it is just Small on CPU, not an error.
        device = "gpu" if device == "gpu" else "cpu"
    elif choice in _GPU_PACK_RECOGNITION:
        if device != "gpu":
            # CPU equivalent of the GPU Turbo pack: Whisper Small on CPU.
            return {"model": "small", "device": "cpu"}
    return {"model": _RECOGNITION_MODEL_DIR[choice], "device": device}
