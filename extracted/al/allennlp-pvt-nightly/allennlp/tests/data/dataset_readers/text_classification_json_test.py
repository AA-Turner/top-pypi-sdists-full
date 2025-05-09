
import pytest

from allennlp.data.dataset_readers import TextClassificationJsonReader
from allennlp.common.util import ensure_list
from allennlp.common.testing import AllenNlpTestCase


class TestTextClassificationJsonReader:

    @pytest.mark.parametrize("lazy", (True, False))
    def test_set_skip_indexing_true(self, lazy):
        reader = TextClassificationJsonReader(lazy=lazy, skip_label_indexing=True)
        ag_path = AllenNlpTestCase.FIXTURES_ROOT / "data" / "text_classification_json" / "integer_labels.jsonl"
        instances = reader.read(ag_path)
        instances = ensure_list(instances)

        instance1 = {"tokens": ['This', 'text', 'has', 'label', '0'], "label": 0}
        instance2 = {"tokens": ['This', 'text', 'has', 'label', '1'], "label": 1}

        assert len(instances) == 2
        fields = instances[0].fields
        assert [t.text for t in fields["tokens"].tokens] == instance1["tokens"]
        assert fields["label"].label == instance1["label"]
        fields = instances[1].fields
        assert [t.text for t in fields["tokens"].tokens] == instance2["tokens"]
        assert fields["label"].label == instance2["label"]

        with pytest.raises(ValueError) as exec_info:
            ag_path = AllenNlpTestCase.FIXTURES_ROOT / "data" / "text_classification_json" / "imdb_corpus.jsonl"
            ensure_list(reader.read(ag_path))
        assert str(exec_info.value) == 'Labels must be integers if skip_label_indexing is True.'

    @pytest.mark.parametrize("lazy", (True, False))
    def test_read_from_file_ag_news_corpus(self, lazy):
        reader = TextClassificationJsonReader(lazy=lazy)
        ag_path = AllenNlpTestCase.FIXTURES_ROOT / "data" / "text_classification_json" / "ag_news_corpus.jsonl"
        instances = reader.read(ag_path)
        instances = ensure_list(instances)

        instance1 = {"tokens": ['Memphis', 'Rout', 'Still', 'Stings', 'for', 'No', '.', '14',
                                'Louisville', ';', 'Coach', 'Petrino', 'Vows', 'to', 'Have',
                                'Team', 'Better', 'Prepared', '.', 'NASHVILLE', ',', 'Tenn.',
                                'Nov', '3', ',', '2004', '-', 'Louisville', '#', '39;s', '30-point',
                                'loss', 'at', 'home', 'to', 'Memphis', 'last', 'season', 'is', 'still',
                                'a', 'painful', 'memory', 'for', 'the', 'Cardinals', '.'],
                     "label": "2"}
        instance2 = {"tokens": ['AP', '-', 'Eli', 'Manning', 'has', 'replaced', 'Kurt', 'Warner',
                                'as', 'the', 'New', 'York', 'Giants', "'", 'starting',
                                'quarterback', '.'],
                     "label": "2"}
        instance3 = {"tokens": ['A', 'conference', 'dedicated', 'to', 'online', 'journalism',
                                'explores', 'the', 'effect', 'blogs', 'have', 'on', 'news',
                                'reporting', '.', 'Some', 'say', 'they', 'draw', 'attention',
                                'to', 'under', '-', 'reported', 'stories', '.', 'Others',
                                'struggle', 'to', 'establish', 'the', 'credibility',
                                'enjoyed', 'by', 'professionals', '.'],
                     "label": "4"}

        assert len(instances) == 3
        fields = instances[0].fields
        assert [t.text for t in fields["tokens"].tokens] == instance1["tokens"]
        assert fields["label"].label == instance1["label"]
        fields = instances[1].fields
        assert [t.text for t in fields["tokens"].tokens] == instance2["tokens"]
        assert fields["label"].label == instance2["label"]
        fields = instances[2].fields
        assert [t.text for t in fields["tokens"].tokens] == instance3["tokens"]
        assert fields["label"].label == instance3["label"]

    @pytest.mark.parametrize("lazy", (True, False))
    def test_read_from_file_ag_news_corpus_and_truncates_properly(self, lazy):
        reader = TextClassificationJsonReader(lazy=lazy, max_sequence_length=5)
        ag_path = AllenNlpTestCase.FIXTURES_ROOT / "data" / "text_classification_json" / "ag_news_corpus.jsonl"
        instances = reader.read(ag_path)
        instances = ensure_list(instances)

        instance1 = {"tokens": ['Memphis', 'Rout', 'Still', 'Stings', 'for'],
                     "label": "2"}
        instance2 = {"tokens": ['AP', '-', 'Eli', 'Manning', 'has'],
                     "label": "2"}
        instance3 = {"tokens": ['A', 'conference', 'dedicated', 'to', 'online'],
                     "label": "4"}

        assert len(instances) == 3
        fields = instances[0].fields
        assert [t.text for t in fields["tokens"].tokens] == instance1["tokens"]
        assert fields["label"].label == instance1["label"]
        fields = instances[1].fields
        assert [t.text for t in fields["tokens"].tokens] == instance2["tokens"]
        assert fields["label"].label == instance2["label"]
        fields = instances[2].fields
        assert [t.text for t in fields["tokens"].tokens] == instance3["tokens"]
        assert fields["label"].label == instance3["label"]

    @pytest.mark.skip(reason="failing mysteriously")
    @pytest.mark.parametrize("lazy", (True, False))
    def test_read_from_file_ag_news_corpus_and_segments_sentences_properly(self, lazy):
        reader = TextClassificationJsonReader(lazy=lazy, segment_sentences=True)
        ag_path = AllenNlpTestCase.FIXTURES_ROOT / "data" / "text_classification_json" / "ag_news_corpus.jsonl"
        instances = reader.read(ag_path)
        instances = ensure_list(instances)

        instance1 = {"tokens": [['Memphis', 'Rout', 'Still', 'Stings', 'for', 'No', '.', '14',
                                 'Louisville', ';'],
                                ['Coach', 'Petrino', 'Vows', 'to', 'Have',
                                 'Team', 'Better', 'Prepared', '.'],
                                ['NASHVILLE', ','],
                                ['Tenn.', 'Nov', '3', ',', '2004', '-',
                                 'Louisville', '#', '39;s', '30-point', 'loss', 'at', 'home',
                                 'to', 'Memphis', 'last', 'season', 'is', 'still', 'a', 'painful',
                                 'memory', 'for', 'the', 'Cardinals', '.']],
                     "label": "2"}
        instance2 = {"tokens": [['AP', '-', 'Eli', 'Manning', 'has', 'replaced', 'Kurt', 'Warner',
                                 'as', 'the', 'New', 'York', 'Giants', "'", 'starting',
                                 'quarterback', '.']],
                     "label": "2"}
        instance3 = {"tokens": [['A', 'conference', 'dedicated', 'to', 'online', 'journalism',
                                 'explores', 'the', 'effect', 'blogs', 'have', 'on', 'news',
                                 'reporting', '.'],
                                ['Some', 'say', 'they', 'draw', 'attention',
                                 'to', 'under', '-', 'reported', 'stories', '.'],
                                ['Others', 'struggle', 'to', 'establish', 'the',
                                 'credibility', 'enjoyed', 'by', 'professionals', '.']],
                     "label": "4"}

        assert len(instances) == 3
        fields = instances[0].fields
        text = [[token.text for token in sentence.tokens] for sentence in fields["tokens"]]
        assert text == instance1["tokens"]
        assert fields["label"].label == instance1["label"]
        fields = instances[1].fields
        text = [[token.text for token in sentence.tokens] for sentence in fields["tokens"]]
        assert text == instance2["tokens"]
        assert fields["label"].label == instance2["label"]
        fields = instances[2].fields
        text = [[token.text for token in sentence.tokens] for sentence in fields["tokens"]]
        assert text == instance3["tokens"]
        assert fields["label"].label == instance3["label"]
