from tests.fixtures import BaseTest


class IterScopedPyFilesTest(BaseTest):
    def test_directory_scope_yields_nothing(self) -> None:
        directory = self.root / "smart-chat-generated-files"
        directory.mkdir(exist_ok=True)
        project = self.controller.repositories.project.load()
        self.assertEqual(list(project.iter_scoped_py_files(directory)), [])

    def test_non_python_file_scope_yields_nothing(self) -> None:
        csv = self.root / "data.csv"
        csv.write_text("a,b")
        project = self.controller.repositories.project.load()
        self.assertEqual(list(project.iter_scoped_py_files(csv)), [])

    def test_python_file_scope_yields_it(self) -> None:
        py = self.root / "script.py"
        py.write_text("print(1)\n")
        project = self.controller.repositories.project.load()
        self.assertEqual(list(project.iter_scoped_py_files(py)), [py])
