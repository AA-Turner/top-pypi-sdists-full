function e(e){return`from zenml.client import Client

artifact = Client().get_artifact_version("${e}")
data = artifact.load()`}function t(e){return`from zenml.client import Client

step = Client().get_run_step("${e}")
config = step.config`}function n(e){return`from zenml.client import Client

run = Client().get_pipeline_run("${e}")
config = run.config`}function r(e){return`from zenml.client import Client

secret = Client().get_secret("${e}")
`}export{t as i,n,r,e as t};