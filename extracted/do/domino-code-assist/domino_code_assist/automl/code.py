# isort: skip_file
# type: ignore
# flake8: noqa
import domino_code_assist as dca
from domino_code_assist.data import palmerpenguins


def display(x):
    pass


___df_var_name___ = palmerpenguins()
___exclude_features___ = []
___time_budget___ = 600
___max_iterations___ = 50
___period___ = 2
___estimator_list___ = []
___custom_hp___ = {}
# ___TEMPLATE_START___ #
from flaml import AutoML, tune
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import pandas as pd

experiment_name = "___experiment_name___"

label = "___label___"
exclude_features = ___exclude_features___

df_automl = ___df_var_name___.drop(exclude_features, axis=1).copy()

display(df_automl)

experiment = mlflow.set_experiment(experiment_name)

estimator_list = ___estimator_list___
custom_hp = ___custom_hp___

# No runs can be active before we start. We will create a run
while mlflow.active_run():
    mlflow.end_run()

mlflow.autolog(disable=True)

with mlflow.start_run() as run:
    run_name = run.data.tags["mlflow.runName"]
    print("Run name: ", run_name)
    display(dca.automl.OpenExperiment(experiment_name))
    automl = AutoML(metric="___optimization_metric___")
    automl.fit(dataframe=df_automl, label=label, task="___ml_task___", period=___period___, time_budget=___time_budget___, max_iter=___max_iterations___, custom_hp=custom_hp, estimator_list=estimator_list, eval_method=None)
    # Log the best model
    train = df_automl.drop(label, axis=1)[:5]
    predictions = pd.DataFrame({label: automl.predict(train)})
    mlflow.sklearn.log_model(automl, "model", signature=infer_signature(train, predictions), input_example=train)
    # Find the best run
    best_run = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string=f'params.best_config = "{automl.best_config}"',
    )
    if len(best_run.run_id):
        best_run_id = best_run.run_id[0]
        mlflow.set_tag("Best run", best_run_id)

        # Copy the params and metrics from the winning run
        run_params = best_run[[c for c in best_run.columns if c.startswith("params.")]].to_dict()
        run_params = {k.lstrip("params."): v[0] for k, v in run_params.items()}
        mlflow.log_params(run_params)

        run_metrics = best_run[[c for c in best_run.columns if c.startswith("metrics.")]].to_dict()
        run_metrics = {k.lstrip("metrics."): v[0] for k, v in run_metrics.items()}
        mlflow.log_metrics(run_metrics)
    else:
        print("No best run found.")

    # Log the notebook cell execution history for reproducibility
    dca.mlflow_log_notebook(run_name)

# Set the wining run to be tagged as the winner
# And log the model
if len(best_run.run_id):
    with mlflow.start_run(best_run_id):
        mlflow.set_tag("Status", "Winner")
        mlflow.set_tag("Winner", True)
        mlflow.sklearn.log_model(automl, "model", signature=infer_signature(train, predictions), input_example=train)
