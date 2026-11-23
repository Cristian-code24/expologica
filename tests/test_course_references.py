import tempfile
import unittest
from pathlib import Path

from course_references import list_references, read_reference


class CourseReferenceTests(unittest.TestCase):
    def test_missing_reference_directory_is_optional(self):
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "not-created"
            self.assertEqual(list_references((missing,)), [])

    def test_text_preview_reads_local_reference(self):
        with tempfile.TemporaryDirectory() as temporary:
            reference = Path(temporary) / "notes.txt"
            reference.write_text("A + A' = 1", encoding="utf-8")
            self.assertEqual(read_reference(reference), "A + A' = 1")


if __name__ == "__main__":
    unittest.main()
