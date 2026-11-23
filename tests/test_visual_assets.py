import tempfile
import unittest
from pathlib import Path

from visual_assets import find_visual_asset, image_data_uri


class VisualAssetTests(unittest.TestCase):
    def test_discovers_renamed_assets_across_supported_folders(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            campus = root / "assets" / "fondo universidad final.webp"
            logo = root / "images" / "logo carrera.png"
            guide = root / "fotos" / "retrato de George Boole.jpeg"
            for path in (campus, logo, guide):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"image")

            self.assertEqual(find_visual_asset("campus", root), campus)
            self.assertEqual(find_visual_asset("school_logo", root), logo)
            self.assertEqual(find_visual_asset("boole_guide", root), guide)

    def test_missing_images_leave_the_fallback_available(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            self.assertIsNone(find_visual_asset("campus", Path(temporary_directory)))
            self.assertIsNone(image_data_uri(None))

    def test_image_data_uri_uses_local_file_contents(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            image = Path(temporary_directory) / "logo.png"
            image.write_bytes(b"png-data")
            self.assertTrue(image_data_uri(image).startswith("data:image/png;base64,"))


if __name__ == "__main__":
    unittest.main()
