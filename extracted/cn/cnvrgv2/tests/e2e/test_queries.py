from cnvrgv2.modules.queries.query import Query


class TestQueries:
    # Tests for fullpath queries. To test tag queries we need to add support for elastic

    @staticmethod
    def create_query(dataset, name, query_raw):
        return dataset.queries.create(name=name, query=query_raw)

    def test_create(self, random_name, e2e_dataset):
        name = random_name(5)
        model = TestQueries.create_query(dataset=e2e_dataset, name=name, query_raw="fake-query")
        assert type(model) == Query
        assert model.name == name
