"""Local image discovery with optional, filename-tolerant visual assets."""

from __future__ import annotations

from base64 import b64encode
from pathlib import Path
import re
import unicodedata


ASSET_DIRECTORIES = ("assets", "images", "fotos")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}

_ASSET_RULES = {
    "campus": {
        "exact": ("fotouni", "fondouniversidad", "fondocampus", "campus", "universidad"),
        "contains": ("fotouni", "fondouniversidad", "fondocampus", "campus", "universidad", "pabellon"),
    },
    "school_logo": {
        "exact": (
            "logoestadisticaeinformatica",
            "logoescueladeestadisticaeinformatica",
            "logoescuela",
            "logocarrera",
        ),
        "contains": ("logoestadistica", "logoinformatica", "logoescuela", "logocarrera", "logo"),
    },
    "boole_guide": {
        "exact": ("retratodeboole", "georgeboole", "boole", "booleestiloanime"),
        "contains": ("boole", "boolean", "retrato"),
    },
}


def _normalize(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", ascii_value.casefold())


def find_visual_asset(kind: str, project_root: Path | None = None) -> Path | None:
    """Find a requested local image; missing optional assets return None."""
    if kind not in _ASSET_RULES:
        raise ValueError(f"Tipo de recurso visual desconocido: {kind}")

    root = project_root or Path(__file__).resolve().parent
    files = []
    for directory_index, directory_name in enumerate(ASSET_DIRECTORIES):
        directory = root / directory_name
        if directory.is_dir():
            files.extend(
                (directory_index, path)
                for path in directory.rglob("*")
                if path.is_file() and path.suffix.casefold() in IMAGE_SUFFIXES
            )

    files.sort(key=lambda item: (item[0], str(item[1]).casefold()))
    rules = _ASSET_RULES[kind]
    normalized_files = [
        (directory_index, path, _normalize(path.stem))
        for directory_index, path in files
    ]
    for candidate in rules["exact"]:
        for _, path, normalized_name in normalized_files:
            if normalized_name == candidate:
                return path

    for marker in rules["contains"]:
        matches = sorted(
            (
                (directory_index, str(path).casefold(), path)
                for directory_index, path, normalized_name in normalized_files
                if marker in normalized_name
            ),
            key=lambda match: (match[0], match[1]),
        )
        if matches:
            return matches[0][2]
    return None


def image_data_uri(path: Path | None) -> str | None:
    """Return a local image as a data URI suitable for inline HTML."""
    if path is None or not path.is_file():
        return None
    suffix = path.suffix.casefold()
    mime_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(suffix)
    if mime_type is None:
        return None
    encoded = b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"
