from debater_python_api.api.debater_api import DebaterApi
from few_shot_priming.prompting_stance import *
def ibm_baseline(api_key, validate=True):
    splits = load_splits()
    if validate:
        test_split = splits["validation"]
    else:
        test_split = splits["test"]

    debater_api = DebaterApi(api_key)
    pro_con_client = debater_api.get_pro_con_client()
    if validate:
        df_test = splits["validate"]
    else:
        df_test = splits["test"]
    list_of_instances = []
    for i, record in df_test.iterrows():
        list_of_instances.append({"sentence" : record['claims.claimCorrectedText'], "topic": record["topicText"]})
    scores = pro_con_client.run(list_of_instances)
    predictions = [score > 0 for score in scores]
    labels_map = {"Pro": 1, "Con": 0}
    labels = [labels_map[label] for label in test_split["claims.stance"]]

    return accuracy_score(labels, predictions)
