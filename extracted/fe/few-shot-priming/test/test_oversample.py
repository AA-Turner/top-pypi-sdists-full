import unittest
import pandas as pd
from few_shot_priming.few_shot_stance import oversample_dataset
class TestExperiment(unittest.TestCase):
    def create_dataframe(self):
        df = pd.DataFrame({"claims.stance":["Pro", "Pro", "Con"],
                           "claims.CorrectedText":["A", "B", "C"],
                           "topic.id":[1, 2, 3]
                           })
        return df

    def test_oversample(self):
        df = self.create_dataframe()
        df_oversampled = oversample_dataset(df)
        count_pro = df_oversampled[df_oversampled["claims.stance"]=="Pro"].shape[0]
        count_con = df_oversampled[df_oversampled["claims.stance"]=="Con"].shape[0]
        self.assertEqual(count_con, count_pro)
        self.assertEqual(df_oversampled[df_oversampled["claims.CorrectedText"]=="C"].shape[0], 2)




