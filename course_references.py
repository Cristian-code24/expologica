"""Descubrimiento y lectura opcional de materiales locales del curso."""

from pathlib import Path
import re
from zipfile import ZipFile
from xml.etree import ElementTree


REFERENCE_DIRS = (Path("libros"), Path("libros-materiales-de-referencia"))
SUPPORTED_SUFFIXES = {".pdf", ".pptx", ".txt", ".md"}


def list_references(directories: tuple[Path, ...] = REFERENCE_DIRS) -> list[Path]:
    """Lista materiales conocidos sin fallar si una carpeta no existe."""
    found: dict[str, Path] = {}
    for directory in directories:
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
                found[str(path.resolve()).casefold()] = path
    return sorted(found.values(), key=lambda path: path.name.casefold())


def read_reference(path: Path, max_chars: int = 5000) -> str:
    """Extrae texto legible de referencias compatibles; limita la vista previa."""
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8", errors="replace")
    elif suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("Instala pypdf para leer documentos PDF.") from exc
        text = "\n\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    elif suffix == ".pptx":
        text = _read_pptx(path)
    else:
        raise ValueError(f"Formato de referencia no compatible: {suffix or '(sin extensión)'}")
    text = text.strip()
    if len(text) > max_chars:
        return text[:max_chars].rstrip() + "\n\n… (vista previa recortada)"
    return text or "No se encontró texto extraíble en este archivo."


def _read_pptx(path: Path) -> str:
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    slides: list[str] = []
    with ZipFile(path) as archive:
        names = [
            name for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        ]
        names.sort(key=lambda name: int(re.search(r"slide(\d+)", name).group(1)))
        for index, name in enumerate(names, start=1):
            root = ElementTree.fromstring(archive.read(name))
            lines = [node.text for node in root.findall(".//a:t", ns) if node.text]
            if lines:
                slides.append(f"Diapositiva {index}\n" + "\n".join(lines))
    return "\n\n".join(slides)
