import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from main import main, run


class TestRun(unittest.TestCase):
    def test_empty_source_returns_0(self):
        lines = []
        self.assertEqual(run("", out=lines.append), 0)
        self.assertEqual(lines, [])

    def test_only_newlines_returns_0(self):
        lines = []
        self.assertEqual(run("\n\n\n", out=lines.append), 0)
        self.assertEqual(lines, [])

    def test_error_prints_message_and_returns_1(self):
        lines = []
        self.assertEqual(run("@", out=lines.append), 1)
        self.assertEqual(lines, ["Lexical error: unexpected character @"])


class TestMain(unittest.TestCase):
    def run_main(self, path):
        """เรียก main() แล้วเก็บข้อความที่ print ออกมา"""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main([str(path)])
        return code, buffer.getvalue()

    def test_rejects_non_txt_file(self):
        code, output = self.run_main("input.py")
        self.assertEqual(code, 1)
        self.assertIn(".txt", output)

    def test_missing_file_returns_1(self):
        code, output = self.run_main("no_such_file.txt")
        self.assertEqual(code, 1)
        self.assertIn("cannot read", output)

    def test_bom_at_start_of_file_is_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bom.txt"
            path.write_text("\n", encoding="utf-8-sig")
            code, output = self.run_main(path)
        self.assertEqual(code, 0)
        self.assertEqual(output, "")