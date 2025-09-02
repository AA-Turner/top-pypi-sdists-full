import json

# from metaflow import step
# from obproject import ProjectFlow
# from highlight_card import highlight

from metaflow import highlight, ProjectFlow, step


class TestProjectUtils(ProjectFlow):
    @highlight
    @step
    def start(self):
        assert self.prj.project == "test_project_utils"
        assert self.prj.branch == "dev"
        assert callable(self.prj.asset.register_data_asset)
        self.highlight.title = "Zoo!"
        self.highlight.add_column(big="🦁", small="Roar")
        self.highlight.add_column(big="🦧", small="Grunt")
        self.next(self.end)

    @step
    def end(self):
        assert "Roar" in json.dumps(self.highlight_data)


if __name__ == "__main__":
    TestProjectUtils()
