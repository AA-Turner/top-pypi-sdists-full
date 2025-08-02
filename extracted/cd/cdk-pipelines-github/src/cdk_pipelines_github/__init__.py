r'''
# CDK Pipelines for GitHub Workflows

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-pipelines-github)](https://constructs.dev/packages/cdk-pipelines-github)

> The APIs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

A construct library for painless Continuous Delivery of CDK applications,
deployed via
[GitHub Workflows](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).

The CDK already has a CI/CD solution,
[CDK Pipelines](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.pipelines-readme.html),
which creates an AWS CodePipeline that deploys CDK applications. This module
serves the same surface area, except that it is implemented with GitHub
Workflows.

## Table of Contents

* [CDK Pipelines for GitHub Workflows](#cdk-pipelines-for-github-workflows)

  * [Table of Contents](#table-of-contents)
  * [Usage](#usage)
  * [Initial Setup](#initial-setup)
  * [AWS Credentials](#aws-credentials)

    * [GitHub Action Role](#github-action-role)

      * [`GitHubActionRole` Construct](#githubactionrole-construct)
    * [GitHub Secrets](#github-secrets)
    * [Runners with Preconfigured Credentials](#runners-with-preconfigured-credentials)
    * [Using Docker in the Pipeline](#using-docker-in-the-pipeline)

      * [Authenticating to Docker registries](#authenticating-to-docker-registries)
  * [Runner Types](#runner-types)

    * [GitHub Hosted Runner](#github-hosted-runner)
    * [Self Hosted Runner](#self-hosted-runner)
  * [Escape Hatches](#escape-hatches)
  * [Additional Features](#additional-features)

    * [GitHub Action Step](#github-action-step)
    * [Configure GitHub Environment](#configure-github-environment)

      * [Waves for Parallel Builds](#waves-for-parallel-builds)
      * [Manual Approval Step](#manual-approval-step)
    * [Pipeline YAML Comments](#pipeline-yaml-comments)
    * [Common Configuration for Docker Asset Publishing Steps](#common-configuration-for-docker-asset-publishing-steps)
    * [Workflow Concurrency](#workflow-concurrency)
  * [AWS China partition support](#aws-china-partition-support)
  * [Tutorial](#tutorial)
  * [Not supported yet](#not-supported-yet)
  * [Contributing](#contributing)
  * [License](#license)

## Usage

Assuming you have a
[`Stage`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Stage.html)
called `MyStage` that includes CDK stacks for your app and you want to deploy it
to two AWS environments (`BETA_ENV` and `PROD_ENV`):

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    aws_creds=AwsCredentials.from_open_id_connect(
        git_hub_action_role_arn="arn:aws:iam::<account-id>:role/GitHubActionRole"
    )
)

# Build the stages
beta_stage = MyStage(app, "Beta", env=BETA_ENV)
prod_stage = MyStage(app, "Prod", env=PROD_ENV)

# Add the stages for sequential build - earlier stages failing will stop later ones:
pipeline.add_stage(beta_stage)
pipeline.add_stage(prod_stage)

# OR add the stages for parallel building of multiple stages with a Wave:
wave = pipeline.add_wave("Wave")
wave.add_stage(beta_stage)
wave.add_stage(prod_stage)

app.synth()
```

When you run `cdk synth`, a `deploy.yml` workflow will be created under
`.github/workflows` in your repo. This workflow will deploy your application
based on the definition of the pipeline. In the example above, it will deploy
the two stages in sequence, and within each stage, it will deploy all the
stacks according to their dependency order and maximum parallelism. If your app
uses assets, assets will be published to the relevant destination environment.

The `Pipeline` class from `cdk-pipelines-github` is derived from the base CDK
Pipelines class, so most features should be supported out of the box. See the
[CDK Pipelines](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.pipelines-readme.html)
documentation for more details.

To express GitHub-specifc details, such as those outlined in [Additional Features](#additional-features), you have a few options:

* Use a `GitHubStage` instead of `Stage` (or make a `GitHubStage` subclass instead of a `Stage` subclass) - this adds the `GitHubCommonProps` to the `Stage` properties

  * With this you can use `pipeline.addStage(myGitHubStage)` or `wave.addStage(myGitHubStage)` and the properties of the
    stage will be used
* Using a `Stage` (or subclass thereof) or a `GitHubStage` (or subclass thereof) you can call `pipeline.addStageWithGitHubOptions(stage, stageOptions)` or `wave.addStageWithGitHubOptions(stage, stageOptions)`

  * In this case you're providing the same options along with the stage instead of embedded in the stage.
  * Note that properties of a `GitHubStage` added with `addStageWithGitHubOptions()` will override the options provided to `addStageWithGitHubOptions()`

**NOTES:**

* Environments must be bootstrapped separately using `cdk bootstrap`. See [CDK
  Environment
  Bootstrapping](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.pipelines-readme.html#cdk-environment-bootstrapping)
  for details.

## Initial Setup

Assuming you have your CDK app checked out on your local machine, here are the suggested steps
to develop your GitHub Workflow.

* Set up AWS Credentials your local environment. It is highly recommended to authenticate via an OpenId
  Connect IAM Role. You can set one up using the [`GithubActionRole`](#github-action-role) class provided
  in this module. For more information (and alternatives), see [AWS Credentials](#aws-credentials).
* When you've updated your pipeline and are ready to deploy, run `cdk synth`. This creates a workflow file
  in `.github/workflows/deploy.yml`.
* When you are ready to test your pipeline, commit your code changes as well as the `deploy.yml` file to
  GitHub. GitHub will automatically try to run the workflow found under `.github/workflows/deploy.yml`.
* You will be able to see the result of the run on the `Actions` tab in your repository:

  ![Screen Shot 2021-08-22 at 12 06 05](https://user-images.githubusercontent.com/598796/130349345-a10a2f75-0848-4de8-bc4c-f5a1418ee228.png)

For an in-depth run-through on creating your own GitHub Workflow, see the
[Tutorial](#tutorial) section.

## AWS Credentials

There are two ways to supply AWS credentials to the workflow:

* GitHub Action IAM Role (recommended).
* Long-lived AWS Credentials stored in GitHub Secrets.

The GitHub Action IAM Role authenticates via the GitHub OpenID Connect provider
and is recommended, but it requires preparing your AWS account beforehand. This
approach allows your Workflow to exchange short-lived tokens directly from AWS.
With OIDC, benefits include:

* No cloud secrets.
* Authentication and authorization management.
* Rotating credentials.

You can read more
[here](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect).

### GitHub Action Role

Authenticating via OpenId Connect means you do not need to store long-lived
credentials as GitHub Secrets. With OIDC, you provide a pre-provisioned IAM
role with optional role session name to your GitHub Workflow via the `awsCreds.fromOpenIdConnect` API:

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    aws_creds=AwsCredentials.from_open_id_connect(
        git_hub_action_role_arn="arn:aws:iam::<account-id>:role/GitHubActionRole",
        role_session_name="optional-role-session-name"
    )
)
```

There are two ways to create this IAM role:

* Use the `GitHubActionRole` construct (recommended and described below).
* Manually set up the role ([Guide](https://github.com/cdklabs/cdk-pipelines-github/blob/main/GITHUB_ACTION_ROLE_SETUP.md)).

#### `GitHubActionRole` Construct

Because this construct involves creating an IAM role in your account, it must
be created separate to your GitHub Workflow and deployed via a normal
`cdk deploy` with your local AWS credentials. Upon successful deployment, the
arn of your newly created IAM role will be exposed as a `CfnOutput`.

To utilize this construct, create a separate CDK stack with the following code
and `cdk deploy`:

```python
class MyGitHubActionRole(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary)

        provider = GitHubActionRole(self, "github-action-role",
            repos=["myUser/myRepo"]
        )

app = App()
MyGitHubActionRole(app, "MyGitHubActionRole")
app.synth()
```

Specifying a `repos` array grants GitHub full access to the specified repositories.
To restrict access to specific git branch, tag, or other
[GitHub OIDC subject claim](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#example-subject-claims),
specify a `subjectClaims` array instead of a `repos` array.

```python
class MyGitHubActionRole(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary)

        provider = GitHubActionRole(self, "github-action-role",
            subject_claims=["repo:owner/repo1:ref:refs/heads/main", "repo:owner/repo1:environment:prod"
            ]
        )

app = App()
MyGitHubActionRole(app, "MyGitHubActionRole")
app.synth()
```

Note: If you have previously created the GitHub identity provider with url
`https://token.actions.githubusercontent.com`, the above example will fail
because you can only have one such provider defined per account. In this
case, you must provide the already created provider into your `GithubActionRole`
construct via the `provider` property.

> Make sure the audience for the provider is `sts.amazonaws.com` in this case.

```python
class MyGitHubActionRole(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary)

        provider = GitHubActionRole(self, "github-action-role",
            repos=["myUser/myRepo"],
            provider=GitHubActionRole.existing_git_hub_actions_provider(self)
        )
```

### GitHub Secrets

Authenticating via this approach means that you will be manually creating AWS
credentials and duplicating them in GitHub secrets. The workflow expects the
GitHub repository to include secrets with AWS credentials under
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. You can override these defaults
by supplying the `awsCreds.fromGitHubSecrets` API to the workflow:

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    aws_creds=AwsCredentials.from_git_hub_secrets(
        access_key_id="MY_ID",  # GitHub will look for the access key id under the secret `MY_ID`
        secret_access_key="MY_KEY"
    )
)
```

### Runners with Preconfigured Credentials

If your runners provide credentials themselves, you can configure `awsCreds` to
skip passing credentials:

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    aws_creds=AwsCredentials.runner_has_preconfigured_creds()
)
```

### Using Docker in the Pipeline

You can use Docker in GitHub Workflows in a similar fashion to CDK Pipelines.
For a full discussion on how to use Docker in CDK Pipelines, see
[Using Docker in the Pipeline](https://github.com/aws/aws-cdk/blob/master/packages/@aws-cdk/pipelines/README.md#using-docker-in-the-pipeline).

Just like CDK Pipelines, you may need to authenticate to Docker registries to
avoid being throttled.

#### Authenticating to Docker registries

You can specify credentials to use for authenticating to Docker registries as
part of the Workflow definition. This can be useful if any Docker image assets —
in the pipeline or any of the application stages — require authentication, either
due to being in a different environment (e.g., ECR repo) or to avoid throttling
(e.g., DockerHub).

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    docker_credentials=[
        # Authenticate to ECR
        DockerCredential.ecr("<account-id>.dkr.ecr.<aws-region>.amazonaws.com"),

        # Authenticate to GHCR
        DockerCredential.ghcr(),

        # Authenticate to DockerHub
        DockerCredential.docker_hub(
            # These properties are defaults; feel free to omit
            username_key="DOCKERHUB_USERNAME",
            personal_access_token_key="DOCKERHUB_TOKEN"
        ),

        # Authenticate to Custom Registries
        DockerCredential.custom_registry("custom-registry",
            username_key="CUSTOM_USERNAME",
            password_key="CUSTOM_PASSWORD"
        )
    ]
)
```

## Runner Types

You can choose to run the workflow in either a GitHub hosted or [self-hosted](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) runner.

### GitHub Hosted Runner

The default is `Runner.UBUNTU_LATEST`. You can override this as shown below:

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    runner=Runner.WINDOWS_LATEST
)
```

### Self Hosted Runner

The following example shows how to configure the workflow to run on a self-hosted runner. Note that you do not need to pass in `self-hosted` explicitly as a label.

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    runner=Runner.self_hosted(["label1", "label2"])
)
```

## Escape Hatches

You can override the `deploy.yml` workflow file post-synthesis however you like.

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    )
)

deploy_workflow = pipeline.workflow_file
# add `on: workflow_call: {}` to deploy.yml
deploy_workflow.patch(JsonPatch.add("/on/workflow_call", {}))
# remove `on: workflow_dispatch` from deploy.yml
deploy_workflow.patch(JsonPatch.remove("/on/workflow_dispatch"))
```

## Additional Features

Below is a compilation of additional features available for GitHub Workflows.

### GitHub Action Step

If you want to call a GitHub Action in a step, you can utilize the `GitHubActionStep`.
`GitHubActionStep` extends `Step` and can be used anywhere a `Step` type is allowed.

The `jobSteps` array is placed into the pipeline job at the relevant `jobs.<job_id>.steps` as [documented here](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps).

GitHub Actions Job permissions can be modified by passing the `permissions` object to `GitHubActionStep`.
The default set of permissions is simply `contents: write`.

In this example,

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    )
)

# "Beta" stage with a pre-check that uses code from the repo and an action
stage = MyStage(app, "Beta", env=BETA_ENV)
pipeline.add_stage(stage,
    pre=[GitHubActionStep("PreBetaDeployAction",
        permissions=JobPermissions(
            id_token=JobPermission.WRITE,
            contents=JobPermission.WRITE
        ),
        job_steps=[JobStep(
            name="Checkout",
            uses="actions/checkout@v4"
        ), JobStep(
            name="pre beta-deploy action",
            uses="my-pre-deploy-action@1.0.0"
        ), JobStep(
            name="pre beta-deploy check",
            run="npm run preDeployCheck"
        )
        ]
    )]
)

app.synth()
```

### Configure GitHub Environment

You can run your GitHub Workflow in select
[GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment).
Via the GitHub UI, you can configure environments with protection rules and secrets, and reference
those environments in your CDK app. A workflow that references an environment must follow any
protection rules for the environment before running or accessing the environment's secrets.

Assuming (just like in the main [example](#usage)) you have a
[`Stage`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Stage.html)
called `MyStage` that includes CDK stacks for your app and you want to deploy it
to two AWS environments (`BETA_ENV` and `PROD_ENV`) as well as GitHub Environments
`beta` and `prod`:

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    aws_creds=AwsCredentials.from_open_id_connect(
        git_hub_action_role_arn="arn:aws:iam::<account-id>:role/GitHubActionRole"
    )
)

pipeline.add_stage_with_git_hub_options(Stage(self, "Beta",
    env=BETA_ENV
),
    git_hub_environment=GitHubEnvironment(name="beta")
)
pipeline.add_stage_with_git_hub_options(MyStage(self, "Prod",
    env=PROD_ENV
),
    git_hub_environment=GitHubEnvironment(name="prod")
)

app.synth()
```

#### Waves for Parallel Builds

You can add a Wave to a pipeline, where each stage of a wave will build in parallel.

> **Note**: The `pipeline.addWave()` call will return a `Wave` object that is actually a `GitHubWave` object, but
> due to JSII rules the return type of `addWave()` cannot be changed. If you need to use
> `wave.addStageWithGitHubOptions()` then you should call `pipeline.addGitHubWave()` instead, or you can
> use `GitHubStage`s to carry the GitHub properties.

When deploying to multiple accounts or otherwise deploying mostly-unrelated stacks, using waves can be a huge win.

Here's a relatively large (but real) example, **without** a wave:

<img width="1955" alt="without-waves-light-mode" src="https://user-images.githubusercontent.com/386001/217436992-d8e46c23-6295-48ec-b139-add60b1f5a14.png">

You can see how dependencies get chained unnecessarily, where the `cUrl` step should be the final step (a test) for an account:

<img width="1955" alt="without-waves-deps-light-mode" src="https://user-images.githubusercontent.com/386001/217437074-3c86d88e-6be7-4b10-97b1-6b51b100e4d6.png">

Here's the exact same stages deploying the same stacks to the same accounts, but **with** a wave:

<img width="1955" alt="with-waves" src="https://user-images.githubusercontent.com/386001/217437228-72f6c278-7e97-4a88-91fa-089628ea0381.png">

And the dependency chains are reduced to only what is actually needed, with the `cUrl` calls as the final stage for each account:

<img width="1955" alt="deps" src="https://user-images.githubusercontent.com/386001/217437265-1c10cd5f-3c7d-4e3a-af5c-acbdf3acff1b.png">

For additional information and a code example see [here](docs/waves.md).

#### Manual Approval Step

One use case for using GitHub Environments with your CDK Pipeline is to create a
manual approval step for specific environments via Environment protection rules.
From the GitHub UI, you can specify up to 5 required reviewers that must approve
before the deployment can proceed:

<img width="1134" alt="require-reviewers" src="https://user-images.githubusercontent.com/7248260/163494925-627f5ca7-a34e-48fa-bec7-1e4924ab6c0c.png">

For more information and a tutorial for how to set this up, see this
[discussion](https://github.com/cdklabs/cdk-pipelines-github/issues/162).

### Pipeline YAML Comments

An "AUTOMATICALLY GENERATED FILE..." comment will by default be added to the top
of the pipeline YAML. This can be overriden as desired to add additional context
to the pipeline YAML.

```yaml
declare const pipeline: GitHubWorkflow;

pipeline.workflowFile.commentAtTop = `AUTOGENERATED FILE, DO NOT EDIT DIRECTLY!

Deployed stacks from this pipeline:
${STACK_NAMES.map((s)=>`- ${s}\n`)}`;
```

This will generate the normal `deploy.yml` file, but with the additional comments:

```yaml
# AUTOGENERATED FILE, DO NOT EDIT DIRECTLY!

# Deployed stacks from this pipeline:
# - APIStack
# - AuroraStack

name: deploy
on:
  push:
    branches:
< the rest of the pipeline YAML contents>
```

### Common Configuration for Docker Asset Publishing Steps

You can provide common job configuration for all of the docker asset publishing
jobs using the `dockerAssetJobSettings` property. You can use this to:

* Set additional `permissions` at the job level
* Run additional steps prior to the docker build/push step

Below is an example of example of configuration an additional `permission` which
allows the job to authenticate against GitHub packages. It also shows
configuration additional `setupSteps`, in this case setup steps to configure
docker `buildx` and `QEMU` to enable building images for arm64 architecture.

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "Pipeline",
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    docker_asset_job_settings=DockerAssetJobSettings(
        permissions=JobPermissions(
            packages=JobPermission.READ
        ),
        setup_steps=[JobStep(
            name="Setup Docker QEMU",
            uses="docker/setup-qemu-action@v3"
        ), JobStep(
            name="Setup Docker buildx",
            uses="docker/setup-buildx-action@v3"
        )
        ]
    ),
    aws_creds=AwsCredentials.from_open_id_connect(
        git_hub_action_role_arn="arn:aws:iam::<account-id>:role/GitHubActionRole"
    )
)

app.synth()
```

### Workflow Concurrency

If you want to prevent your workflow from running in parallel you can specify the concurrency at workflow level.
Below is an example of a workflow that will not run in parallel and where a running workflow will be cancelled in favor of the more recent one.
The [GitHub docs](https://docs.github.com/en/actions/using-jobs/using-concurrency) provide further details on this.

```python
from aws_cdk.pipelines import ShellStep


app = App()

pipeline = GitHubWorkflow(app, "SequentialPipeline",
    concurrency=ConcurrencyOptions(
        group="${{ github.workflow }}-group",
        cancel_in_progress=True
    ),
    synth=ShellStep("Build",
        commands=["yarn install", "yarn build"
        ]
    ),
    aws_creds=AwsCredentials.from_open_id_connect(
        git_hub_action_role_arn="arn:aws:iam::<account-id>:role/GitHubActionRole"
    )
)
```

## AWS China partition support

The `CDK_AWS_PARTITION` environment variable can be used to specify the AWS partition for the pipeline.
If it's specified to `aws-cn`, the assets generated by pipeline will reference the resources in
`.amazonaws.com.cn` instead of `.amazonaws.com`.

If `CDK_AWS_PARTITION` environment variable is not specified, the default behaviour for the pipeline is
to use the `aws` partition.

It is not possible to have a pipeline that deploys to both `aws` and `aws-cn` partitions.
If you need to deploy to both partitions, you will need to create two separate pipelines.
The stages and stacks can be shared between the two pipelines.

## Tutorial

You can find an example usage in [test/example-app.ts](./test/example-app.ts)
which includes a simple CDK app and a pipeline.

You can find a repository that uses this example here: [eladb/test-app-cdkpipeline](https://github.com/eladb/test-app-cdkpipeline).

To run the example, clone this repository and install dependencies:

```shell
cd ~/projects # or some other playground space
git clone https://github.com/cdklabs/cdk-pipelines-github
cd cdk-pipelines-github
yarn
```

Now, create a new GitHub repository and clone it as well:

```shell
cd ~/projects
git clone https://github.com/myaccount/my-test-repository
```

You'll need to set up AWS credentials in your environment. Note that this tutorial uses
long-lived GitHub secrets as credentials for simplicity, but it is recommended to set up
a GitHub OIDC role instead.

```shell
export AWS_ACCESS_KEY_ID=xxxx
export AWS_SECRET_ACCESS_KEY=xxxxx
```

Bootstrap your environments:

```shell
export CDK_NEW_BOOTSTRAP=1
npx cdk bootstrap aws://ACCOUNTID/us-east-1
npx cdk bootstrap aws://ACCOUNTID/eu-west-2
```

Now, run the `manual-test.sh` script when your working directory is the new repository:

```shell
cd ~/projects/my-test-repository
~/projects/cdk-piplines/github/test/manual-test.sh
```

This will produce a `cdk.out` directory and a `.github/workflows/deploy.yml` file.

Commit and push these files to your repo and you should see the deployment
workflow in action. Make sure your GitHub repository has `AWS_ACCESS_KEY_ID` and
`AWS_SECRET_ACCESS_KEY` secrets that can access the same account that you
synthesized against.

> In this tutorial, you are supposed to commit `cdk.out` (i.e. the code is pre-synthed).
> Do not do this in your app; you should always synth during the synth step of the GitHub
> workflow. In the example app this is achieved through the `preSynthed: true` option.
> It is for example purposes only and is not something you should do in your app.
>
> ```python
> from aws_cdk.pipelines import ShellStep
>
> pipeline = GitHubWorkflow(App(), "Pipeline",
>     synth=ShellStep("Build",
>         commands=["echo \"nothing to do (cdk.out is committed)\""]
>     ),
>     # only the example app should do this. your app should synth in the synth step.
>     pre_synthed=True
> )
> ```

## Not supported yet

Most features that exist in CDK Pipelines are supported. However, as the CDK Pipelines
feature are expands, the feature set for GitHub Workflows may lag behind. If you see a
feature that you feel should be supported by GitHub Workflows, please open a GitHub issue
to track it.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.pipelines as _aws_cdk_pipelines_ceddda9d
import constructs as _constructs_77d1e7e8


class AwsCredentials(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.AwsCredentials",
):
    '''(experimental) Provides AWS credenitals to the pipeline jobs.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromGitHubSecrets")
    @builtins.classmethod
    def from_git_hub_secrets(
        cls,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
        session_token: typing.Optional[builtins.str] = None,
    ) -> "AwsCredentialsProvider":
        '''(experimental) Reference credential secrets to authenticate with AWS.

        This method assumes
        that your credentials will be stored as long-lived GitHub Secrets.

        :param access_key_id: Default: "AWS_ACCESS_KEY_ID"
        :param secret_access_key: Default: "AWS_SECRET_ACCESS_KEY"
        :param session_token: Default: - no session token is used

        :stability: experimental
        '''
        props = GitHubSecretsProviderProps(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
        )

        return typing.cast("AwsCredentialsProvider", jsii.sinvoke(cls, "fromGitHubSecrets", [props]))

    @jsii.member(jsii_name="fromOpenIdConnect")
    @builtins.classmethod
    def from_open_id_connect(
        cls,
        *,
        git_hub_action_role_arn: builtins.str,
        role_session_name: typing.Optional[builtins.str] = None,
    ) -> "AwsCredentialsProvider":
        '''(experimental) Provide AWS credentials using OpenID Connect.

        :param git_hub_action_role_arn: (experimental) A role that utilizes the GitHub OIDC Identity Provider in your AWS account. You can create your own role in the console with the necessary trust policy to allow gitHub actions from your gitHub repository to assume the role, or you can utilize the ``GitHubActionRole`` construct to create a role for you.
        :param role_session_name: (experimental) The role session name to use when assuming the role. Default: - no role session name

        :stability: experimental
        '''
        props = OpenIdConnectProviderProps(
            git_hub_action_role_arn=git_hub_action_role_arn,
            role_session_name=role_session_name,
        )

        return typing.cast("AwsCredentialsProvider", jsii.sinvoke(cls, "fromOpenIdConnect", [props]))

    @jsii.member(jsii_name="runnerHasPreconfiguredCreds")
    @builtins.classmethod
    def runner_has_preconfigured_creds(cls) -> "AwsCredentialsProvider":
        '''(experimental) Don't provide any AWS credentials, use this if runners have preconfigured credentials.

        :stability: experimental
        '''
        return typing.cast("AwsCredentialsProvider", jsii.sinvoke(cls, "runnerHasPreconfiguredCreds", []))


class AwsCredentialsProvider(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-pipelines-github.AwsCredentialsProvider",
):
    '''(experimental) AWS credential provider.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="credentialSteps")
    @abc.abstractmethod
    def credential_steps(
        self,
        region: builtins.str,
        assume_role_arn: typing.Optional[builtins.str] = None,
    ) -> typing.List["JobStep"]:
        '''
        :param region: -
        :param assume_role_arn: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="jobPermission")
    @abc.abstractmethod
    def job_permission(self) -> "JobPermission":
        '''
        :stability: experimental
        '''
        ...


class _AwsCredentialsProviderProxy(AwsCredentialsProvider):
    @jsii.member(jsii_name="credentialSteps")
    def credential_steps(
        self,
        region: builtins.str,
        assume_role_arn: typing.Optional[builtins.str] = None,
    ) -> typing.List["JobStep"]:
        '''
        :param region: -
        :param assume_role_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34f5a85d5e49af165e757b316fc4eadde29000f3bae7a0c0ad92162ad1f7859)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
        return typing.cast(typing.List["JobStep"], jsii.invoke(self, "credentialSteps", [region, assume_role_arn]))

    @jsii.member(jsii_name="jobPermission")
    def job_permission(self) -> "JobPermission":
        '''
        :stability: experimental
        '''
        return typing.cast("JobPermission", jsii.invoke(self, "jobPermission", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AwsCredentialsProvider).__jsii_proxy_class__ = lambda : _AwsCredentialsProviderProxy


@jsii.data_type(
    jsii_type="cdk-pipelines-github.AwsCredentialsSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
        "session_token": "sessionToken",
    },
)
class AwsCredentialsSecrets:
    def __init__(
        self,
        *,
        access_key_id: typing.Optional[builtins.str] = None,
        secret_access_key: typing.Optional[builtins.str] = None,
        session_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Names of secrets for AWS credentials.

        :param access_key_id: Default: "AWS_ACCESS_KEY_ID"
        :param secret_access_key: Default: "AWS_SECRET_ACCESS_KEY"
        :param session_token: Default: - no session token is used

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ab8e0acc5af4b62bacc9d5ad666cdeedd569af7e148668725f140b7bc483de)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
            check_type(argname="argument session_token", value=session_token, expected_type=type_hints["session_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key_id is not None:
            self._values["access_key_id"] = access_key_id
        if secret_access_key is not None:
            self._values["secret_access_key"] = secret_access_key
        if session_token is not None:
            self._values["session_token"] = session_token

    @builtins.property
    def access_key_id(self) -> typing.Optional[builtins.str]:
        '''
        :default: "AWS_ACCESS_KEY_ID"

        :stability: experimental
        '''
        result = self._values.get("access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key(self) -> typing.Optional[builtins.str]:
        '''
        :default: "AWS_SECRET_ACCESS_KEY"

        :stability: experimental
        '''
        result = self._values.get("secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_token(self) -> typing.Optional[builtins.str]:
        '''
        :default: - no session token is used

        :stability: experimental
        '''
        result = self._values.get("session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCredentialsSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.CheckRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Check run options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6373a6591e7a83beaee7f715a317bd90eb8e115426fbe79d84ec07038ffe5e4b)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.CheckSuiteOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckSuiteOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Check suite options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2329fd786490f9db53605848242542e725f90583102b8a55f00cbf365b3702e3)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckSuiteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ConcurrencyOptions",
    jsii_struct_bases=[],
    name_mapping={"group": "group", "cancel_in_progress": "cancelInProgress"},
)
class ConcurrencyOptions:
    def __init__(
        self,
        *,
        group: builtins.str,
        cancel_in_progress: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Concurrency options at workflow level.

        :param group: (experimental) The concurrency group to use for the job.
        :param cancel_in_progress: (experimental) Conditionally cancel currently running jobs or workflows in the same concurrency group. Default: false

        :see: https://docs.github.com/en/actions/using-jobs/using-concurrency
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb410d6a8096fafa9cac50ed904bfb12e76ade4f85e8287349d0aeb8489705b)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument cancel_in_progress", value=cancel_in_progress, expected_type=type_hints["cancel_in_progress"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
        }
        if cancel_in_progress is not None:
            self._values["cancel_in_progress"] = cancel_in_progress

    @builtins.property
    def group(self) -> builtins.str:
        '''(experimental) The concurrency group to use for the job.

        :stability: experimental
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cancel_in_progress(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Conditionally cancel currently running jobs or workflows in the same concurrency group.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("cancel_in_progress")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConcurrencyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ContainerCredentials",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class ContainerCredentials:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''(experimental) Credentials to use to authenticate to Docker registries.

        :param password: (experimental) The password.
        :param username: (experimental) The username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d9d9d796eb12703f23018e319ec5349afa13b16aeb0ebd4f7b89db2d314fbb)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''(experimental) The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ContainerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "credentials": "credentials",
        "env": "env",
        "options": "options",
        "ports": "ports",
        "volumes": "volumes",
    },
)
class ContainerOptions:
    def __init__(
        self,
        *,
        image: builtins.str,
        credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options petaining to container environments.

        :param image: (experimental) The Docker image to use as the container to run the action. The value can be the Docker Hub image name or a registry name.
        :param credentials: (experimental) f the image's container registry requires authentication to pull the image, you can use credentials to set a map of the username and password. The credentials are the same values that you would provide to the docker login command.
        :param env: (experimental) Sets a map of environment variables in the container.
        :param options: (experimental) Additional Docker container resource options.
        :param ports: (experimental) Sets an array of ports to expose on the container.
        :param volumes: (experimental) Sets an array of volumes for the container to use. You can use volumes to share data between services or other steps in a job. You can specify named Docker volumes, anonymous Docker volumes, or bind mounts on the host. To specify a volume, you specify the source and destination path: ``<source>:<destinationPath>``.

        :stability: experimental
        '''
        if isinstance(credentials, dict):
            credentials = ContainerCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95391ae8e55d8dc0bfb3183f3e3dc187d92e429daf90843549a090f978a7b2bf)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if credentials is not None:
            self._values["credentials"] = credentials
        if env is not None:
            self._values["env"] = env
        if options is not None:
            self._values["options"] = options
        if ports is not None:
            self._values["ports"] = ports
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> builtins.str:
        '''(experimental) The Docker image to use as the container to run the action.

        The value can
        be the Docker Hub image name or a registry name.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(self) -> typing.Optional[ContainerCredentials]:
        '''(experimental) f the image's container registry requires authentication to pull the image, you can use credentials to set a map of the username and password.

        The credentials are the same values that you would provide to the docker
        login command.

        :stability: experimental
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[ContainerCredentials], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Sets a map of environment variables in the container.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional Docker container resource options.

        :see: https://docs.docker.com/engine/reference/commandline/create/#options
        :stability: experimental
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''(experimental) Sets an array of ports to expose on the container.

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Sets an array of volumes for the container to use.

        You can use volumes to
        share data between services or other steps in a job. You can specify
        named Docker volumes, anonymous Docker volumes, or bind mounts on the
        host.

        To specify a volume, you specify the source and destination path:
        ``<source>:<destinationPath>``.

        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.CreateOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CreateOptions:
    def __init__(self) -> None:
        '''(experimental) The Create event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.CronScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron"},
)
class CronScheduleOptions:
    def __init__(self, *, cron: builtins.str) -> None:
        '''(experimental) CRON schedule options.

        :param cron: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f54935941db587485c7979514ebfed4aeb58008d8e75a449b9f4b2a9cd9231)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cron": cron,
        }

    @builtins.property
    def cron(self) -> builtins.str:
        '''
        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        :stability: experimental
        '''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DeleteOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeleteOptions:
    def __init__(self) -> None:
        '''(experimental) The Delete event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeleteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DeploymentOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeploymentOptions:
    def __init__(self) -> None:
        '''(experimental) The Deployment event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DeploymentStatusOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeploymentStatusOptions:
    def __init__(self) -> None:
        '''(experimental) The Deployment status event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentStatusOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DockerAssetJobSettings",
    jsii_struct_bases=[],
    name_mapping={"permissions": "permissions", "setup_steps": "setupSteps"},
)
class DockerAssetJobSettings:
    def __init__(
        self,
        *,
        permissions: typing.Optional[typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
        setup_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Job level settings applied to all docker asset publishing jobs in the workflow.

        :param permissions: (experimental) Additional permissions to grant to the docker image publishing job. Default: - no additional permissions
        :param setup_steps: (experimental) GitHub workflow steps to execute before building and publishing the image. Default: []

        :stability: experimental
        '''
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e52b1650e15393651aa94bf8e685a0018d4c955418f5ce005b28568dd5302d)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument setup_steps", value=setup_steps, expected_type=type_hints["setup_steps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if permissions is not None:
            self._values["permissions"] = permissions
        if setup_steps is not None:
            self._values["setup_steps"] = setup_steps

    @builtins.property
    def permissions(self) -> typing.Optional["JobPermissions"]:
        '''(experimental) Additional permissions to grant to the docker image publishing job.

        :default: - no additional permissions

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional["JobPermissions"], result)

    @builtins.property
    def setup_steps(self) -> typing.Optional[typing.List["JobStep"]]:
        '''(experimental) GitHub workflow steps to execute before building and publishing the image.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("setup_steps")
        return typing.cast(typing.Optional[typing.List["JobStep"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerAssetJobSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerCredential(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.DockerCredential",
):
    '''(experimental) Represents a credential used to authenticate to a docker registry.

    Uses the official Docker Login GitHub Action to authenticate.

    :see: https://github.com/marketplace/actions/docker-login
    :stability: experimental
    '''

    @jsii.member(jsii_name="customRegistry")
    @builtins.classmethod
    def custom_registry(
        cls,
        registry: builtins.str,
        *,
        password_key: builtins.str,
        username_key: builtins.str,
    ) -> "DockerCredential":
        '''(experimental) Create a credential for a custom registry.

        This method assumes that you will have long-lived
        GitHub Secrets stored under the usernameKey and passwordKey that will authenticate to the
        registry you provide.

        :param registry: -
        :param password_key: (experimental) The key of the GitHub Secret containing your registry password.
        :param username_key: (experimental) The key of the GitHub Secret containing your registry username.

        :see: https://github.com/marketplace/actions/docker-login
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101864b569747688b6b3a9b72cb693fe435eec9bb1e6b51e0026ca466648f2c1)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        creds = ExternalDockerCredentialSecrets(
            password_key=password_key, username_key=username_key
        )

        return typing.cast("DockerCredential", jsii.sinvoke(cls, "customRegistry", [registry, creds]))

    @jsii.member(jsii_name="dockerHub")
    @builtins.classmethod
    def docker_hub(
        cls,
        *,
        personal_access_token_key: typing.Optional[builtins.str] = None,
        username_key: typing.Optional[builtins.str] = None,
    ) -> "DockerCredential":
        '''(experimental) Reference credential secrets to authenticate to DockerHub.

        This method assumes
        that your credentials will be stored as long-lived GitHub Secrets under the
        usernameKey and personalAccessTokenKey.

        The default for usernameKey is ``DOCKERHUB_USERNAME``. The default for personalAccessTokenKey
        is ``DOCKERHUB_TOKEN``. If you do not set these values, your credentials should be
        found in your GitHub Secrets under these default keys.

        :param personal_access_token_key: (experimental) The key of the GitHub Secret containing the DockerHub personal access token. Default: 'DOCKERHUB_TOKEN'
        :param username_key: (experimental) The key of the GitHub Secret containing the DockerHub username. Default: 'DOCKERHUB_USERNAME'

        :stability: experimental
        '''
        creds = DockerHubCredentialSecrets(
            personal_access_token_key=personal_access_token_key,
            username_key=username_key,
        )

        return typing.cast("DockerCredential", jsii.sinvoke(cls, "dockerHub", [creds]))

    @jsii.member(jsii_name="ecr")
    @builtins.classmethod
    def ecr(cls, registry: builtins.str) -> "DockerCredential":
        '''(experimental) Create a credential for ECR.

        This method will reuse your AWS credentials to log in to AWS.
        Your AWS credentials are already used to deploy your CDK stacks. It can be supplied via
        GitHub Secrets or using an IAM role that trusts the GitHub OIDC identity provider.

        NOTE - All ECR repositories in the same account and region share a domain name
        (e.g., 0123456789012.dkr.ecr.eu-west-1.amazonaws.com), and can only have one associated
        set of credentials (and DockerCredential). Attempting to associate one set of credentials
        with one ECR repo and another with another ECR repo in the same account and region will
        result in failures when using these credentials in the pipeline.

        :param registry: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d0c29c037615007983ee20857df5048cbe8494f68f656f5b4af70afa444b2a)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        return typing.cast("DockerCredential", jsii.sinvoke(cls, "ecr", [registry]))

    @jsii.member(jsii_name="ghcr")
    @builtins.classmethod
    def ghcr(cls) -> "DockerCredential":
        '''(experimental) Create a credential for the GitHub Container Registry (GHCR).

        For more information on authenticating to GHCR,

        :see: https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions
        :stability: experimental
        '''
        return typing.cast("DockerCredential", jsii.sinvoke(cls, "ghcr", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registry"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "username"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DockerHubCredentialSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "personal_access_token_key": "personalAccessTokenKey",
        "username_key": "usernameKey",
    },
)
class DockerHubCredentialSecrets:
    def __init__(
        self,
        *,
        personal_access_token_key: typing.Optional[builtins.str] = None,
        username_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Locations of GitHub Secrets used to authenticate to DockerHub.

        :param personal_access_token_key: (experimental) The key of the GitHub Secret containing the DockerHub personal access token. Default: 'DOCKERHUB_TOKEN'
        :param username_key: (experimental) The key of the GitHub Secret containing the DockerHub username. Default: 'DOCKERHUB_USERNAME'

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09113ce192ad66711ff498566dd94325741d6b520d4811f33cf1c2d279ad6779)
            check_type(argname="argument personal_access_token_key", value=personal_access_token_key, expected_type=type_hints["personal_access_token_key"])
            check_type(argname="argument username_key", value=username_key, expected_type=type_hints["username_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if personal_access_token_key is not None:
            self._values["personal_access_token_key"] = personal_access_token_key
        if username_key is not None:
            self._values["username_key"] = username_key

    @builtins.property
    def personal_access_token_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of the GitHub Secret containing the DockerHub personal access token.

        :default: 'DOCKERHUB_TOKEN'

        :stability: experimental
        '''
        result = self._values.get("personal_access_token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of the GitHub Secret containing the DockerHub username.

        :default: 'DOCKERHUB_USERNAME'

        :stability: experimental
        '''
        result = self._values.get("username_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerHubCredentialSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ExternalDockerCredentialSecrets",
    jsii_struct_bases=[],
    name_mapping={"password_key": "passwordKey", "username_key": "usernameKey"},
)
class ExternalDockerCredentialSecrets:
    def __init__(
        self,
        *,
        password_key: builtins.str,
        username_key: builtins.str,
    ) -> None:
        '''(experimental) Generic structure to supply the locations of GitHub Secrets used to authenticate to a docker registry.

        :param password_key: (experimental) The key of the GitHub Secret containing your registry password.
        :param username_key: (experimental) The key of the GitHub Secret containing your registry username.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0f223a2472060f1f721c38920d320f88580c9de023d07ad9ceacd1ab2bd973)
            check_type(argname="argument password_key", value=password_key, expected_type=type_hints["password_key"])
            check_type(argname="argument username_key", value=username_key, expected_type=type_hints["username_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password_key": password_key,
            "username_key": username_key,
        }

    @builtins.property
    def password_key(self) -> builtins.str:
        '''(experimental) The key of the GitHub Secret containing your registry password.

        :stability: experimental
        '''
        result = self._values.get("password_key")
        assert result is not None, "Required property 'password_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username_key(self) -> builtins.str:
        '''(experimental) The key of the GitHub Secret containing your registry username.

        :stability: experimental
        '''
        result = self._values.get("username_key")
        assert result is not None, "Required property 'username_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalDockerCredentialSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ForkOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class ForkOptions:
    def __init__(self) -> None:
        '''(experimental) The Fork event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ForkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubActionRole(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.GitHubActionRole",
):
    '''(experimental) Creates or references a GitHub OIDC provider and accompanying role that trusts the provider.

    This role can be used to authenticate against AWS instead of using long-lived AWS user credentials
    stored in GitHub secrets.

    You can do this manually in the console, or create a separate stack that uses this construct.
    You must ``cdk deploy`` once (with your normal AWS credentials) to have this role created for you.

    You can then make note of the role arn in the stack output and send it into the Github Workflow app via
    the ``gitHubActionRoleArn`` property. The role arn will be ``arn:<partition>:iam::<accountId>:role/GithubActionRole``.

    :see: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        repos: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_name: typing.Optional[builtins.str] = None,
        subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
        thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param provider: (experimental) The GitHub OpenId Connect Provider. Must have provider url ``https://token.actions.githubusercontent.com``. The audience must be ``sts:amazonaws.com``. Only one such provider can be defined per account, so if you already have a provider with the same url, a new provider cannot be created for you. Default: - a provider is created for you.
        :param repos: (experimental) A list of GitHub repositories you want to be able to access the IAM role. Each entry should be your GitHub username and repository passed in as a single string. An entry ``owner/repo`` is equivalent to the subjectClaim ``repo:owner/repo:*``. For example, `['owner/repo1', 'owner/repo2'].
        :param role_name: (experimental) The name of the Oidc role. Default: 'GitHubActionRole'
        :param subject_claims: (experimental) A list of subject claims allowed to access the IAM role. See https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect A subject claim can include ``*`` and ``?`` wildcards according to the ``StringLike`` condition operator. For example, ``['repo:owner/repo1:ref:refs/heads/branch1', 'repo:owner/repo1:environment:prod']``
        :param thumbprints: (experimental) Thumbprints of GitHub's certificates. Every time GitHub rotates their certificates, this value will need to be updated. Default value is up-to-date to June 27, 2023 as per https://github.blog/changelog/2023-06-27-github-actions-update-on-oidc-integration-with-aws/ Default: - Use built-in keys

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7efaa19c11ed9057d237005627f473d64f50f5e1ab1712be044e3d1bdd7716e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionRoleProps(
            provider=provider,
            repos=repos,
            role_name=role_name,
            subject_claims=subject_claims,
            thumbprints=thumbprints,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="existingGitHubActionsProvider")
    @builtins.classmethod
    def existing_git_hub_actions_provider(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider:
        '''(experimental) Reference an existing GitHub Actions provider.

        You do not need to pass in an arn because the arn for such
        a provider is always the same.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3470db1a98b372a508d6fcbbe10f97f439b9fc7404d428e0944f0bc7a4014485)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider, jsii.sinvoke(cls, "existingGitHubActionsProvider", [scope]))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role that gets created.

        You should use the arn of this role as input to the ``gitHubActionRoleArn``
        property in your GitHub Workflow app.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubActionRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "provider": "provider",
        "repos": "repos",
        "role_name": "roleName",
        "subject_claims": "subjectClaims",
        "thumbprints": "thumbprints",
    },
)
class GitHubActionRoleProps:
    def __init__(
        self,
        *,
        provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        repos: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_name: typing.Optional[builtins.str] = None,
        subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
        thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for the GitHubActionRole construct.

        :param provider: (experimental) The GitHub OpenId Connect Provider. Must have provider url ``https://token.actions.githubusercontent.com``. The audience must be ``sts:amazonaws.com``. Only one such provider can be defined per account, so if you already have a provider with the same url, a new provider cannot be created for you. Default: - a provider is created for you.
        :param repos: (experimental) A list of GitHub repositories you want to be able to access the IAM role. Each entry should be your GitHub username and repository passed in as a single string. An entry ``owner/repo`` is equivalent to the subjectClaim ``repo:owner/repo:*``. For example, `['owner/repo1', 'owner/repo2'].
        :param role_name: (experimental) The name of the Oidc role. Default: 'GitHubActionRole'
        :param subject_claims: (experimental) A list of subject claims allowed to access the IAM role. See https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect A subject claim can include ``*`` and ``?`` wildcards according to the ``StringLike`` condition operator. For example, ``['repo:owner/repo1:ref:refs/heads/branch1', 'repo:owner/repo1:environment:prod']``
        :param thumbprints: (experimental) Thumbprints of GitHub's certificates. Every time GitHub rotates their certificates, this value will need to be updated. Default value is up-to-date to June 27, 2023 as per https://github.blog/changelog/2023-06-27-github-actions-update-on-oidc-integration-with-aws/ Default: - Use built-in keys

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fb897842c219b21980c6f5d46fcab4f267529a7fde8c4ee40880539a329537)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument repos", value=repos, expected_type=type_hints["repos"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument subject_claims", value=subject_claims, expected_type=type_hints["subject_claims"])
            check_type(argname="argument thumbprints", value=thumbprints, expected_type=type_hints["thumbprints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if provider is not None:
            self._values["provider"] = provider
        if repos is not None:
            self._values["repos"] = repos
        if role_name is not None:
            self._values["role_name"] = role_name
        if subject_claims is not None:
            self._values["subject_claims"] = subject_claims
        if thumbprints is not None:
            self._values["thumbprints"] = thumbprints

    @builtins.property
    def provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]:
        '''(experimental) The GitHub OpenId Connect Provider. Must have provider url ``https://token.actions.githubusercontent.com``. The audience must be ``sts:amazonaws.com``.

        Only one such provider can be defined per account, so if you already
        have a provider with the same url, a new provider cannot be created for you.

        :default: - a provider is created for you.

        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider], result)

    @builtins.property
    def repos(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of GitHub repositories you want to be able to access the IAM role.

        Each entry should be your GitHub username and repository passed in as a
        single string.
        An entry ``owner/repo`` is equivalent to the subjectClaim ``repo:owner/repo:*``.

        For example, `['owner/repo1', 'owner/repo2'].

        :stability: experimental
        '''
        result = self._values.get("repos")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Oidc role.

        :default: 'GitHubActionRole'

        :stability: experimental
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_claims(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of subject claims allowed to access the IAM role.

        See https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
        A subject claim can include ``*`` and ``?`` wildcards according to the ``StringLike``
        condition operator.

        For example, ``['repo:owner/repo1:ref:refs/heads/branch1', 'repo:owner/repo1:environment:prod']``

        :stability: experimental
        '''
        result = self._values.get("subject_claims")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def thumbprints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Thumbprints of GitHub's certificates.

        Every time GitHub rotates their certificates, this value will need to be updated.

        Default value is up-to-date to June 27, 2023 as per
        https://github.blog/changelog/2023-06-27-github-actions-update-on-oidc-integration-with-aws/

        :default: - Use built-in keys

        :stability: experimental
        '''
        result = self._values.get("thumbprints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubActionRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubActionStep(
    _aws_cdk_pipelines_ceddda9d.Step,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.GitHubActionStep",
):
    '''(experimental) Specifies a GitHub Action as a step in the pipeline.

    :stability: experimental
    '''

    def __init__(
        self,
        id: builtins.str,
        *,
        job_steps: typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]],
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        github_environment: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Identifier for this step.
        :param job_steps: (experimental) The Job steps.
        :param env: (experimental) Environment variables to set.
        :param github_environment: (experimental) The GitHub Environment for the GitHub Action step. To set shell-level environment variables, use ``env``. Default: No GitHub Environment is selected.
        :param permissions: (experimental) Permissions for the GitHub Action step. Default: The job receives 'contents: write' permissions. If you set additional permissions and require 'contents: write', it must be provided in your configuration.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1176a118ca36bc762181a4882e12e7b069118ee5882233a232892bdc923c8209)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionStepProps(
            job_steps=job_steps,
            env=env,
            github_environment=github_environment,
            permissions=permissions,
        )

        jsii.create(self.__class__, self, [id, props])

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="jobSteps")
    def job_steps(self) -> typing.List["JobStep"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["JobStep"], jsii.get(self, "jobSteps"))

    @builtins.property
    @jsii.member(jsii_name="githubEnvironment")
    def github_environment(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "githubEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> typing.Optional["JobPermissions"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["JobPermissions"], jsii.get(self, "permissions"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubActionStepProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_steps": "jobSteps",
        "env": "env",
        "github_environment": "githubEnvironment",
        "permissions": "permissions",
    },
)
class GitHubActionStepProps:
    def __init__(
        self,
        *,
        job_steps: typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]],
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        github_environment: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param job_steps: (experimental) The Job steps.
        :param env: (experimental) Environment variables to set.
        :param github_environment: (experimental) The GitHub Environment for the GitHub Action step. To set shell-level environment variables, use ``env``. Default: No GitHub Environment is selected.
        :param permissions: (experimental) Permissions for the GitHub Action step. Default: The job receives 'contents: write' permissions. If you set additional permissions and require 'contents: write', it must be provided in your configuration.

        :stability: experimental
        '''
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb9323e1a70b92d220365668e8d719f774e191339812c47f7e57cd238de1678)
            check_type(argname="argument job_steps", value=job_steps, expected_type=type_hints["job_steps"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument github_environment", value=github_environment, expected_type=type_hints["github_environment"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_steps": job_steps,
        }
        if env is not None:
            self._values["env"] = env
        if github_environment is not None:
            self._values["github_environment"] = github_environment
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def job_steps(self) -> typing.List["JobStep"]:
        '''(experimental) The Job steps.

        :stability: experimental
        '''
        result = self._values.get("job_steps")
        assert result is not None, "Required property 'job_steps' is missing"
        return typing.cast(typing.List["JobStep"], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables to set.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def github_environment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub Environment for the GitHub Action step.

        To set shell-level environment variables, use ``env``.

        :default: No GitHub Environment is selected.

        :see: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
        :stability: experimental
        '''
        result = self._values.get("github_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional["JobPermissions"]:
        '''(experimental) Permissions for the GitHub Action step.

        :default: The job receives 'contents: write' permissions. If you set additional permissions and require 'contents: write', it must be provided in your configuration.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional["JobPermissions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubActionStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubCommonProps",
    jsii_struct_bases=[],
    name_mapping={
        "git_hub_environment": "gitHubEnvironment",
        "job_settings": "jobSettings",
        "stack_capabilities": "stackCapabilities",
    },
)
class GitHubCommonProps:
    def __init__(
        self,
        *,
        git_hub_environment: typing.Optional[typing.Union["GitHubEnvironment", typing.Dict[builtins.str, typing.Any]]] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> None:
        '''(experimental) Common properties to extend both StageProps and AddStageOpts.

        :param git_hub_environment: (experimental) Run the stage in a specific GitHub Environment. If specified, any protection rules configured for the environment must pass before the job is set to a runner. For example, if the environment has a manual approval rule configured, then the workflow will wait for the approval before sending the job to the runner. Running a workflow that references an environment that does not exist will create an environment with the referenced name. Default: - no GitHub environment
        :param job_settings: (experimental) Job level settings that will be applied to all jobs in the stage. Currently the only valid setting is 'if'.
        :param stack_capabilities: (experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack. If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities`` error. Default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        if isinstance(git_hub_environment, dict):
            git_hub_environment = GitHubEnvironment(**git_hub_environment)
        if isinstance(job_settings, dict):
            job_settings = JobSettings(**job_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6611b18289416c64b5e869501493ceef81f660dd80fa6f0677574ec6b5504d6c)
            check_type(argname="argument git_hub_environment", value=git_hub_environment, expected_type=type_hints["git_hub_environment"])
            check_type(argname="argument job_settings", value=job_settings, expected_type=type_hints["job_settings"])
            check_type(argname="argument stack_capabilities", value=stack_capabilities, expected_type=type_hints["stack_capabilities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if git_hub_environment is not None:
            self._values["git_hub_environment"] = git_hub_environment
        if job_settings is not None:
            self._values["job_settings"] = job_settings
        if stack_capabilities is not None:
            self._values["stack_capabilities"] = stack_capabilities

    @builtins.property
    def git_hub_environment(self) -> typing.Optional["GitHubEnvironment"]:
        '''(experimental) Run the stage in a specific GitHub Environment.

        If specified,
        any protection rules configured for the environment must pass
        before the job is set to a runner. For example, if the environment
        has a manual approval rule configured, then the workflow will
        wait for the approval before sending the job to the runner.

        Running a workflow that references an environment that does not
        exist will create an environment with the referenced name.

        :default: - no GitHub environment

        :see: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
        :stability: experimental
        '''
        result = self._values.get("git_hub_environment")
        return typing.cast(typing.Optional["GitHubEnvironment"], result)

    @builtins.property
    def job_settings(self) -> typing.Optional["JobSettings"]:
        '''(experimental) Job level settings that will be applied to all jobs in the stage.

        Currently the only valid setting is 'if'.

        :stability: experimental
        '''
        result = self._values.get("job_settings")
        return typing.cast(typing.Optional["JobSettings"], result)

    @builtins.property
    def stack_capabilities(self) -> typing.Optional[typing.List["StackCapabilities"]]:
        '''(experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack.

        If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities``
        error.

        :default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        result = self._values.get("stack_capabilities")
        return typing.cast(typing.Optional[typing.List["StackCapabilities"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubCommonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubEnvironment",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class GitHubEnvironment:
    def __init__(
        self,
        *,
        name: builtins.str,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Github environment with name and url.

        :param name: (experimental) Name of the environment.
        :param url: (experimental) The url for the environment.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idenvironment
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fe132afc11f8f0a945ac9eeea27c033ce30202ce31b3058b8be89378efddf9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the environment.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-using-environment-name-and-url
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The url for the environment.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-using-environment-name-and-url
        :stability: experimental
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubSecretsProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
        "session_token": "sessionToken",
    },
)
class GitHubSecretsProviderProps:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
        session_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Locations of GitHub Secrets used to authenticate to AWS.

        :param access_key_id: Default: "AWS_ACCESS_KEY_ID"
        :param secret_access_key: Default: "AWS_SECRET_ACCESS_KEY"
        :param session_token: Default: - no session token is used

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5502781441b1b7f54eb889be996f05f0ccaf271d620ba0e9cc14739f9b2b656)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
            check_type(argname="argument session_token", value=session_token, expected_type=type_hints["session_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
        }
        if session_token is not None:
            self._values["session_token"] = session_token

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''
        :default: "AWS_ACCESS_KEY_ID"

        :stability: experimental
        '''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''
        :default: "AWS_SECRET_ACCESS_KEY"

        :stability: experimental
        '''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_token(self) -> typing.Optional[builtins.str]:
        '''
        :default: - no session token is used

        :stability: experimental
        '''
        result = self._values.get("session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSecretsProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubStage(
    _aws_cdk_ceddda9d.Stage,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.GitHubStage",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param env: Default AWS environment (account/region) for ``Stack``s in this ``Stage``. Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing from its env will use the corresponding field given here. If either ``region`` or ``account``is is not configured for ``Stack`` (either on the ``Stack`` itself or on the containing ``Stage``), the Stack will be *environment-agnostic*. Environment-agnostic stacks can be deployed to any environment, may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups, will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environments should be configured on the ``Stack``s.
        :param outdir: The output directory into which to emit synthesized artifacts. Can only be specified if this stage is the root stage (the app). If this is specified and this stage is nested within another stage, an error will be thrown. Default: - for nested stages, outdir will be determined as a relative directory to the outdir of the app. For apps, if outdir is not specified, a temporary directory will be created.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param policy_validation_beta1: Validation plugins to run during synthesis. If any plugin reports any violation, synthesis will be interrupted and the report displayed to the user. Default: - no validation plugins are used
        :param stage_name: Name of this stage. Default: - Derived from the id.
        :param git_hub_environment: (experimental) Run the stage in a specific GitHub Environment. If specified, any protection rules configured for the environment must pass before the job is set to a runner. For example, if the environment has a manual approval rule configured, then the workflow will wait for the approval before sending the job to the runner. Running a workflow that references an environment that does not exist will create an environment with the referenced name. Default: - no GitHub environment
        :param job_settings: (experimental) Job level settings that will be applied to all jobs in the stage. Currently the only valid setting is 'if'.
        :param stack_capabilities: (experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack. If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities`` error. Default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ded55f6f78e09081d268fb0ac64648e138db13b9f4acaadd50868b68501f46)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubStageProps(
            env=env,
            outdir=outdir,
            permissions_boundary=permissions_boundary,
            policy_validation_beta1=policy_validation_beta1,
            stage_name=stage_name,
            git_hub_environment=git_hub_environment,
            job_settings=job_settings,
            stack_capabilities=stack_capabilities,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> typing.Optional["GitHubStageProps"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["GitHubStageProps"], jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubStageProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.StageProps, GitHubCommonProps],
    name_mapping={
        "env": "env",
        "outdir": "outdir",
        "permissions_boundary": "permissionsBoundary",
        "policy_validation_beta1": "policyValidationBeta1",
        "stage_name": "stageName",
        "git_hub_environment": "gitHubEnvironment",
        "job_settings": "jobSettings",
        "stack_capabilities": "stackCapabilities",
    },
)
class GitHubStageProps(_aws_cdk_ceddda9d.StageProps, GitHubCommonProps):
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> None:
        '''
        :param env: Default AWS environment (account/region) for ``Stack``s in this ``Stage``. Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing from its env will use the corresponding field given here. If either ``region`` or ``account``is is not configured for ``Stack`` (either on the ``Stack`` itself or on the containing ``Stage``), the Stack will be *environment-agnostic*. Environment-agnostic stacks can be deployed to any environment, may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups, will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environments should be configured on the ``Stack``s.
        :param outdir: The output directory into which to emit synthesized artifacts. Can only be specified if this stage is the root stage (the app). If this is specified and this stage is nested within another stage, an error will be thrown. Default: - for nested stages, outdir will be determined as a relative directory to the outdir of the app. For apps, if outdir is not specified, a temporary directory will be created.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param policy_validation_beta1: Validation plugins to run during synthesis. If any plugin reports any violation, synthesis will be interrupted and the report displayed to the user. Default: - no validation plugins are used
        :param stage_name: Name of this stage. Default: - Derived from the id.
        :param git_hub_environment: (experimental) Run the stage in a specific GitHub Environment. If specified, any protection rules configured for the environment must pass before the job is set to a runner. For example, if the environment has a manual approval rule configured, then the workflow will wait for the approval before sending the job to the runner. Running a workflow that references an environment that does not exist will create an environment with the referenced name. Default: - no GitHub environment
        :param job_settings: (experimental) Job level settings that will be applied to all jobs in the stage. Currently the only valid setting is 'if'.
        :param stack_capabilities: (experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack. If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities`` error. Default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if isinstance(git_hub_environment, dict):
            git_hub_environment = GitHubEnvironment(**git_hub_environment)
        if isinstance(job_settings, dict):
            job_settings = JobSettings(**job_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8d3dbc0d6268c9ba2a6b3d91eaaf33aa275000dba07e4f98ce438ef6f8cd5a5)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policy_validation_beta1", value=policy_validation_beta1, expected_type=type_hints["policy_validation_beta1"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument git_hub_environment", value=git_hub_environment, expected_type=type_hints["git_hub_environment"])
            check_type(argname="argument job_settings", value=job_settings, expected_type=type_hints["job_settings"])
            check_type(argname="argument stack_capabilities", value=stack_capabilities, expected_type=type_hints["stack_capabilities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if outdir is not None:
            self._values["outdir"] = outdir
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policy_validation_beta1 is not None:
            self._values["policy_validation_beta1"] = policy_validation_beta1
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if git_hub_environment is not None:
            self._values["git_hub_environment"] = git_hub_environment
        if job_settings is not None:
            self._values["job_settings"] = job_settings
        if stack_capabilities is not None:
            self._values["stack_capabilities"] = stack_capabilities

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''Default AWS environment (account/region) for ``Stack``s in this ``Stage``.

        Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing
        from its env will use the corresponding field given here.

        If either ``region`` or ``account``is is not configured for ``Stack`` (either on
        the ``Stack`` itself or on the containing ``Stage``), the Stack will be
        *environment-agnostic*.

        Environment-agnostic stacks can be deployed to any environment, may not be
        able to take advantage of all features of the CDK. For example, they will
        not be able to use environmental context lookups, will not automatically
        translate Service Principals to the right format based on the environment's
        AWS partition, and other such enhancements.

        :default: - The environments should be configured on the ``Stack``s.

        Example::

            // Use a concrete account and region to deploy this Stage to
            new Stage(app, 'Stage1', {
              env: { account: '123456789012', region: 'us-east-1' },
            });
            
            // Use the CLI's current credentials to determine the target environment
            new Stage(app, 'Stage2', {
              env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
            });
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''The output directory into which to emit synthesized artifacts.

        Can only be specified if this stage is the root stage (the app). If this is
        specified and this stage is nested within another stage, an error will be
        thrown.

        :default:

        - for nested stages, outdir will be determined as a relative
        directory to the outdir of the app. For apps, if outdir is not specified, a
        temporary directory will be created.
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary]:
        '''Options for applying a permissions boundary to all IAM Roles and Users created within this Stage.

        :default: - no permissions boundary is applied
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary], result)

    @builtins.property
    def policy_validation_beta1(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]]:
        '''Validation plugins to run during synthesis.

        If any plugin reports any violation,
        synthesis will be interrupted and the report displayed to the user.

        :default: - no validation plugins are used
        '''
        result = self._values.get("policy_validation_beta1")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''Name of this stage.

        :default: - Derived from the id.
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_hub_environment(self) -> typing.Optional[GitHubEnvironment]:
        '''(experimental) Run the stage in a specific GitHub Environment.

        If specified,
        any protection rules configured for the environment must pass
        before the job is set to a runner. For example, if the environment
        has a manual approval rule configured, then the workflow will
        wait for the approval before sending the job to the runner.

        Running a workflow that references an environment that does not
        exist will create an environment with the referenced name.

        :default: - no GitHub environment

        :see: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
        :stability: experimental
        '''
        result = self._values.get("git_hub_environment")
        return typing.cast(typing.Optional[GitHubEnvironment], result)

    @builtins.property
    def job_settings(self) -> typing.Optional["JobSettings"]:
        '''(experimental) Job level settings that will be applied to all jobs in the stage.

        Currently the only valid setting is 'if'.

        :stability: experimental
        '''
        result = self._values.get("job_settings")
        return typing.cast(typing.Optional["JobSettings"], result)

    @builtins.property
    def stack_capabilities(self) -> typing.Optional[typing.List["StackCapabilities"]]:
        '''(experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack.

        If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities``
        error.

        :default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        result = self._values.get("stack_capabilities")
        return typing.cast(typing.Optional[typing.List["StackCapabilities"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubWave(
    _aws_cdk_pipelines_ceddda9d.Wave,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.GitHubWave",
):
    '''(experimental) Multiple stages that are deployed in parallel.

    A ``Wave``, but with addition GitHub options

    Create with ``GitHubWorkflow.addWave()`` or ``GitHubWorkflow.addGitHubWave()``.
    You should not have to instantiate a GitHubWave yourself.

    :stability: experimental
    '''

    def __init__(
        self,
        id: builtins.str,
        pipeline: "GitHubWorkflow",
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    ) -> None:
        '''(experimental) Create with ``GitHubWorkflow.addWave()`` or ``GitHubWorkflow.addGitHubWave()``. You should not have to instantiate a GitHubWave yourself.

        :param id: Identifier for this Wave.
        :param pipeline: GitHubWorkflow that this wave is part of.
        :param post: Additional steps to run after all of the stages in the wave. Default: - No additional steps
        :param pre: Additional steps to run before any of the stages in the wave. Default: - No additional steps

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef499badf71d8733c69ad09c0c24f5703e7108be9c31a0b1fff34b312651b42)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
        props = _aws_cdk_pipelines_ceddda9d.WaveProps(post=post, pre=pre)

        jsii.create(self.__class__, self, [id, pipeline, props])

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        stage: _aws_cdk_ceddda9d.Stage,
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_pipelines_ceddda9d.StageDeployment:
        '''(experimental) Add a Stage to this wave.

        It will be deployed in parallel with all other stages in this
        wave.

        :param stage: -
        :param post: Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: Instructions for stack level steps. Default: - No additional instructions

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43c8e0765168b11f6277a89cfc0de81ab7a360ad3bca0ae6f0216f148accdbf)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _aws_cdk_pipelines_ceddda9d.AddStageOpts(
            post=post, pre=pre, stack_steps=stack_steps
        )

        return typing.cast(_aws_cdk_pipelines_ceddda9d.StageDeployment, jsii.invoke(self, "addStage", [stage, options]))

    @jsii.member(jsii_name="addStageWithGitHubOptions")
    def add_stage_with_git_hub_options(
        self,
        stage: _aws_cdk_ceddda9d.Stage,
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
        git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> _aws_cdk_pipelines_ceddda9d.StageDeployment:
        '''(experimental) Add a Stage to this wave.

        It will be deployed in parallel with all other stages in this
        wave.

        :param stage: -
        :param post: Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: Instructions for stack level steps. Default: - No additional instructions
        :param git_hub_environment: (experimental) Run the stage in a specific GitHub Environment. If specified, any protection rules configured for the environment must pass before the job is set to a runner. For example, if the environment has a manual approval rule configured, then the workflow will wait for the approval before sending the job to the runner. Running a workflow that references an environment that does not exist will create an environment with the referenced name. Default: - no GitHub environment
        :param job_settings: (experimental) Job level settings that will be applied to all jobs in the stage. Currently the only valid setting is 'if'.
        :param stack_capabilities: (experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack. If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities`` error. Default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa2718a68b226b4c63caab144cfb3f546368347ce90eed7c4f118e33bc04cc4)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = AddGitHubStageOptions(
            post=post,
            pre=pre,
            stack_steps=stack_steps,
            git_hub_environment=git_hub_environment,
            job_settings=job_settings,
            stack_capabilities=stack_capabilities,
        )

        return typing.cast(_aws_cdk_pipelines_ceddda9d.StageDeployment, jsii.invoke(self, "addStageWithGitHubOptions", [stage, options]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Identifier for this Wave.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))


class GitHubWorkflow(
    _aws_cdk_pipelines_ceddda9d.PipelineBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.GitHubWorkflow",
):
    '''(experimental) CDK Pipelines for GitHub workflows.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_credentials: typing.Optional[typing.Union[AwsCredentialsSecrets, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_creds: typing.Optional[AwsCredentialsProvider] = None,
        build_container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_asset_job_settings: typing.Optional[typing.Union[DockerAssetJobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
        git_hub_action_role_arn: typing.Optional[builtins.str] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_synthed: typing.Optional[builtins.bool] = None,
        publish_assets_auth_region: typing.Optional[builtins.str] = None,
        runner: typing.Optional["Runner"] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_path: typing.Optional[builtins.str] = None,
        workflow_triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[builtins.str, typing.Any]]] = None,
        synth: _aws_cdk_pipelines_ceddda9d.IFileSetProducer,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param aws_credentials: (deprecated) Names of GitHub repository secrets that include AWS credentials for deployment. Default: - ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        :param aws_creds: (experimental) Configure provider for AWS credentials used for deployment. Default: - Get AWS credentials from GitHub secrets ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        :param build_container: (experimental) Build container options. Default: - GitHub defaults
        :param cdk_cli_version: (experimental) Version of the CDK CLI to use. Default: - automatic
        :param concurrency: (experimental) GitHub workflow concurrency. Default: - no concurrency settings
        :param docker_asset_job_settings: (experimental) Job level settings applied to all docker asset publishing jobs in the workflow. Default: - no additional settings
        :param docker_credentials: (experimental) The Docker Credentials to use to login. If you set this variable, you will be logged in to docker when you upload Docker Assets.
        :param git_hub_action_role_arn: (deprecated) A role that utilizes the GitHub OIDC Identity Provider in your AWS account. If supplied, this will be used instead of ``awsCredentials``. You can create your own role in the console with the necessary trust policy to allow gitHub actions from your gitHub repository to assume the role, or you can utilize the ``GitHubActionRole`` construct to create a role for you. Default: - GitHub repository secrets are used instead of OpenId Connect role.
        :param job_settings: (experimental) Job level settings that will be applied to all jobs in the workflow, including synth and asset deploy jobs. Currently the only valid setting is 'if'. You can use this to run jobs only in specific repositories.
        :param post_build_steps: (experimental) GitHub workflow steps to execute after build. Default: []
        :param pre_build_steps: (experimental) GitHub workflow steps to execute before build. Default: []
        :param pre_synthed: (experimental) Indicates if the repository already contains a synthesized ``cdk.out`` directory, in which case we will simply checkout the repo in jobs that require ``cdk.out``. Default: false
        :param publish_assets_auth_region: (experimental) Will assume the GitHubActionRole in this region when publishing assets. This is NOT the region in which the assets are published. In most cases, you do not have to worry about this property, and can safely ignore it. Default: "us-west-2"
        :param runner: (experimental) The type of runner to run the job on. The runner can be either a GitHub-hosted runner or a self-hosted runner. Default: Runner.UBUNTU_LATEST
        :param workflow_name: (experimental) Name of the workflow. Default: "deploy"
        :param workflow_path: (experimental) File path for the GitHub workflow. Default: ".github/workflows/deploy.yml"
        :param workflow_triggers: (experimental) GitHub workflow triggers. Default: - By default, workflow is triggered on push to the ``main`` branch and can also be triggered manually (``workflow_dispatch``).
        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e000cfcb875b99dba5697464b35c7b7052d0af71745445799f596ff96147a8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubWorkflowProps(
            aws_credentials=aws_credentials,
            aws_creds=aws_creds,
            build_container=build_container,
            cdk_cli_version=cdk_cli_version,
            concurrency=concurrency,
            docker_asset_job_settings=docker_asset_job_settings,
            docker_credentials=docker_credentials,
            git_hub_action_role_arn=git_hub_action_role_arn,
            job_settings=job_settings,
            post_build_steps=post_build_steps,
            pre_build_steps=pre_build_steps,
            pre_synthed=pre_synthed,
            publish_assets_auth_region=publish_assets_auth_region,
            runner=runner,
            workflow_name=workflow_name,
            workflow_path=workflow_path,
            workflow_triggers=workflow_triggers,
            synth=synth,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addGitHubWave")
    def add_git_hub_wave(
        self,
        id: builtins.str,
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    ) -> GitHubWave:
        '''
        :param id: -
        :param post: Additional steps to run after all of the stages in the wave. Default: - No additional steps
        :param pre: Additional steps to run before any of the stages in the wave. Default: - No additional steps

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eaf88ea4f8a8d2fc4873b4c2c60f9899faf9476b95495ce23f7850e90ec317e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_pipelines_ceddda9d.WaveOptions(post=post, pre=pre)

        return typing.cast(GitHubWave, jsii.invoke(self, "addGitHubWave", [id, options]))

    @jsii.member(jsii_name="addStageWithGitHubOptions")
    def add_stage_with_git_hub_options(
        self,
        stage: _aws_cdk_ceddda9d.Stage,
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
        git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> _aws_cdk_pipelines_ceddda9d.StageDeployment:
        '''(experimental) Deploy a single Stage by itself with options for further GitHub configuration.

        Add a Stage to the pipeline, to be deployed in sequence with other Stages added to the pipeline.
        All Stacks in the stage will be deployed in an order automatically determined by their relative dependencies.

        :param stage: -
        :param post: Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: Instructions for stack level steps. Default: - No additional instructions
        :param git_hub_environment: (experimental) Run the stage in a specific GitHub Environment. If specified, any protection rules configured for the environment must pass before the job is set to a runner. For example, if the environment has a manual approval rule configured, then the workflow will wait for the approval before sending the job to the runner. Running a workflow that references an environment that does not exist will create an environment with the referenced name. Default: - no GitHub environment
        :param job_settings: (experimental) Job level settings that will be applied to all jobs in the stage. Currently the only valid setting is 'if'.
        :param stack_capabilities: (experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack. If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities`` error. Default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7a4aaa2de9ee17c586fe08c0478d636f444f6bd2752a8271707d3e99f00736)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = AddGitHubStageOptions(
            post=post,
            pre=pre,
            stack_steps=stack_steps,
            git_hub_environment=git_hub_environment,
            job_settings=job_settings,
            stack_capabilities=stack_capabilities,
        )

        return typing.cast(_aws_cdk_pipelines_ceddda9d.StageDeployment, jsii.invoke(self, "addStageWithGitHubOptions", [stage, options]))

    @jsii.member(jsii_name="addWave")
    def add_wave(
        self,
        id: builtins.str,
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    ) -> _aws_cdk_pipelines_ceddda9d.Wave:
        '''(experimental) Add a Wave to the pipeline, for deploying multiple Stages in parallel.

        Use the return object of this method to deploy multiple stages in parallel.

        Example::

           # pipeline: GitHubWorkflow
           # assign pipeline a value

           wave = pipeline.add_wave("MyWave")
           wave.add_stage(MyStage(self, "Stage1"))
           wave.add_stage(MyStage(self, "Stage2"))

        :param id: -
        :param post: Additional steps to run after all of the stages in the wave. Default: - No additional steps
        :param pre: Additional steps to run before any of the stages in the wave. Default: - No additional steps

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14874e98f77810a63a3eb419752e3f2e023edb5fb94993515b42884eaa1d7087)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_pipelines_ceddda9d.WaveOptions(post=post, pre=pre)

        return typing.cast(_aws_cdk_pipelines_ceddda9d.Wave, jsii.invoke(self, "addWave", [id, options]))

    @jsii.member(jsii_name="doBuildPipeline")
    def _do_build_pipeline(self) -> None:
        '''(experimental) Implemented by subclasses to do the actual pipeline construction.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "doBuildPipeline", []))

    @builtins.property
    @jsii.member(jsii_name="workflowFile")
    def workflow_file(self) -> "YamlFile":
        '''
        :stability: experimental
        '''
        return typing.cast("YamlFile", jsii.get(self, "workflowFile"))

    @builtins.property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowName"))

    @builtins.property
    @jsii.member(jsii_name="workflowPath")
    def workflow_path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workflowPath"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubWorkflowProps",
    jsii_struct_bases=[_aws_cdk_pipelines_ceddda9d.PipelineBaseProps],
    name_mapping={
        "synth": "synth",
        "aws_credentials": "awsCredentials",
        "aws_creds": "awsCreds",
        "build_container": "buildContainer",
        "cdk_cli_version": "cdkCliVersion",
        "concurrency": "concurrency",
        "docker_asset_job_settings": "dockerAssetJobSettings",
        "docker_credentials": "dockerCredentials",
        "git_hub_action_role_arn": "gitHubActionRoleArn",
        "job_settings": "jobSettings",
        "post_build_steps": "postBuildSteps",
        "pre_build_steps": "preBuildSteps",
        "pre_synthed": "preSynthed",
        "publish_assets_auth_region": "publishAssetsAuthRegion",
        "runner": "runner",
        "workflow_name": "workflowName",
        "workflow_path": "workflowPath",
        "workflow_triggers": "workflowTriggers",
    },
)
class GitHubWorkflowProps(_aws_cdk_pipelines_ceddda9d.PipelineBaseProps):
    def __init__(
        self,
        *,
        synth: _aws_cdk_pipelines_ceddda9d.IFileSetProducer,
        aws_credentials: typing.Optional[typing.Union[AwsCredentialsSecrets, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_creds: typing.Optional[AwsCredentialsProvider] = None,
        build_container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_asset_job_settings: typing.Optional[typing.Union[DockerAssetJobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
        git_hub_action_role_arn: typing.Optional[builtins.str] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_synthed: typing.Optional[builtins.bool] = None,
        publish_assets_auth_region: typing.Optional[builtins.str] = None,
        runner: typing.Optional["Runner"] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_path: typing.Optional[builtins.str] = None,
        workflow_triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Props for ``GitHubWorkflow``.

        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param aws_credentials: (deprecated) Names of GitHub repository secrets that include AWS credentials for deployment. Default: - ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        :param aws_creds: (experimental) Configure provider for AWS credentials used for deployment. Default: - Get AWS credentials from GitHub secrets ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        :param build_container: (experimental) Build container options. Default: - GitHub defaults
        :param cdk_cli_version: (experimental) Version of the CDK CLI to use. Default: - automatic
        :param concurrency: (experimental) GitHub workflow concurrency. Default: - no concurrency settings
        :param docker_asset_job_settings: (experimental) Job level settings applied to all docker asset publishing jobs in the workflow. Default: - no additional settings
        :param docker_credentials: (experimental) The Docker Credentials to use to login. If you set this variable, you will be logged in to docker when you upload Docker Assets.
        :param git_hub_action_role_arn: (deprecated) A role that utilizes the GitHub OIDC Identity Provider in your AWS account. If supplied, this will be used instead of ``awsCredentials``. You can create your own role in the console with the necessary trust policy to allow gitHub actions from your gitHub repository to assume the role, or you can utilize the ``GitHubActionRole`` construct to create a role for you. Default: - GitHub repository secrets are used instead of OpenId Connect role.
        :param job_settings: (experimental) Job level settings that will be applied to all jobs in the workflow, including synth and asset deploy jobs. Currently the only valid setting is 'if'. You can use this to run jobs only in specific repositories.
        :param post_build_steps: (experimental) GitHub workflow steps to execute after build. Default: []
        :param pre_build_steps: (experimental) GitHub workflow steps to execute before build. Default: []
        :param pre_synthed: (experimental) Indicates if the repository already contains a synthesized ``cdk.out`` directory, in which case we will simply checkout the repo in jobs that require ``cdk.out``. Default: false
        :param publish_assets_auth_region: (experimental) Will assume the GitHubActionRole in this region when publishing assets. This is NOT the region in which the assets are published. In most cases, you do not have to worry about this property, and can safely ignore it. Default: "us-west-2"
        :param runner: (experimental) The type of runner to run the job on. The runner can be either a GitHub-hosted runner or a self-hosted runner. Default: Runner.UBUNTU_LATEST
        :param workflow_name: (experimental) Name of the workflow. Default: "deploy"
        :param workflow_path: (experimental) File path for the GitHub workflow. Default: ".github/workflows/deploy.yml"
        :param workflow_triggers: (experimental) GitHub workflow triggers. Default: - By default, workflow is triggered on push to the ``main`` branch and can also be triggered manually (``workflow_dispatch``).

        :stability: experimental
        '''
        if isinstance(aws_credentials, dict):
            aws_credentials = AwsCredentialsSecrets(**aws_credentials)
        if isinstance(build_container, dict):
            build_container = ContainerOptions(**build_container)
        if isinstance(concurrency, dict):
            concurrency = ConcurrencyOptions(**concurrency)
        if isinstance(docker_asset_job_settings, dict):
            docker_asset_job_settings = DockerAssetJobSettings(**docker_asset_job_settings)
        if isinstance(job_settings, dict):
            job_settings = JobSettings(**job_settings)
        if isinstance(workflow_triggers, dict):
            workflow_triggers = WorkflowTriggers(**workflow_triggers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54d7c114bd36382002f3ddd507359655630c42e5b211e5c46e68de87555cf35)
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument aws_creds", value=aws_creds, expected_type=type_hints["aws_creds"])
            check_type(argname="argument build_container", value=build_container, expected_type=type_hints["build_container"])
            check_type(argname="argument cdk_cli_version", value=cdk_cli_version, expected_type=type_hints["cdk_cli_version"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument docker_asset_job_settings", value=docker_asset_job_settings, expected_type=type_hints["docker_asset_job_settings"])
            check_type(argname="argument docker_credentials", value=docker_credentials, expected_type=type_hints["docker_credentials"])
            check_type(argname="argument git_hub_action_role_arn", value=git_hub_action_role_arn, expected_type=type_hints["git_hub_action_role_arn"])
            check_type(argname="argument job_settings", value=job_settings, expected_type=type_hints["job_settings"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument pre_build_steps", value=pre_build_steps, expected_type=type_hints["pre_build_steps"])
            check_type(argname="argument pre_synthed", value=pre_synthed, expected_type=type_hints["pre_synthed"])
            check_type(argname="argument publish_assets_auth_region", value=publish_assets_auth_region, expected_type=type_hints["publish_assets_auth_region"])
            check_type(argname="argument runner", value=runner, expected_type=type_hints["runner"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
            check_type(argname="argument workflow_path", value=workflow_path, expected_type=type_hints["workflow_path"])
            check_type(argname="argument workflow_triggers", value=workflow_triggers, expected_type=type_hints["workflow_triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "synth": synth,
        }
        if aws_credentials is not None:
            self._values["aws_credentials"] = aws_credentials
        if aws_creds is not None:
            self._values["aws_creds"] = aws_creds
        if build_container is not None:
            self._values["build_container"] = build_container
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if docker_asset_job_settings is not None:
            self._values["docker_asset_job_settings"] = docker_asset_job_settings
        if docker_credentials is not None:
            self._values["docker_credentials"] = docker_credentials
        if git_hub_action_role_arn is not None:
            self._values["git_hub_action_role_arn"] = git_hub_action_role_arn
        if job_settings is not None:
            self._values["job_settings"] = job_settings
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if pre_build_steps is not None:
            self._values["pre_build_steps"] = pre_build_steps
        if pre_synthed is not None:
            self._values["pre_synthed"] = pre_synthed
        if publish_assets_auth_region is not None:
            self._values["publish_assets_auth_region"] = publish_assets_auth_region
        if runner is not None:
            self._values["runner"] = runner
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name
        if workflow_path is not None:
            self._values["workflow_path"] = workflow_path
        if workflow_triggers is not None:
            self._values["workflow_triggers"] = workflow_triggers

    @builtins.property
    def synth(self) -> _aws_cdk_pipelines_ceddda9d.IFileSetProducer:
        '''The build step that produces the CDK Cloud Assembly.

        The primary output of this step needs to be the ``cdk.out`` directory
        generated by the ``cdk synth`` command.

        If you use a ``ShellStep`` here and you don't configure an output directory,
        the output directory will automatically be assumed to be ``cdk.out``.
        '''
        result = self._values.get("synth")
        assert result is not None, "Required property 'synth' is missing"
        return typing.cast(_aws_cdk_pipelines_ceddda9d.IFileSetProducer, result)

    @builtins.property
    def aws_credentials(self) -> typing.Optional[AwsCredentialsSecrets]:
        '''(deprecated) Names of GitHub repository secrets that include AWS credentials for deployment.

        :default: - ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.

        :deprecated: Use ``awsCreds.fromGitHubSecrets()`` instead.

        :stability: deprecated
        '''
        result = self._values.get("aws_credentials")
        return typing.cast(typing.Optional[AwsCredentialsSecrets], result)

    @builtins.property
    def aws_creds(self) -> typing.Optional[AwsCredentialsProvider]:
        '''(experimental) Configure provider for AWS credentials used for deployment.

        :default: - Get AWS credentials from GitHub secrets ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.

        :stability: experimental
        '''
        result = self._values.get("aws_creds")
        return typing.cast(typing.Optional[AwsCredentialsProvider], result)

    @builtins.property
    def build_container(self) -> typing.Optional[ContainerOptions]:
        '''(experimental) Build container options.

        :default: - GitHub defaults

        :stability: experimental
        '''
        result = self._values.get("build_container")
        return typing.cast(typing.Optional[ContainerOptions], result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of the CDK CLI to use.

        :default: - automatic

        :stability: experimental
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def concurrency(self) -> typing.Optional[ConcurrencyOptions]:
        '''(experimental) GitHub workflow concurrency.

        :default: - no concurrency settings

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Optional[ConcurrencyOptions], result)

    @builtins.property
    def docker_asset_job_settings(self) -> typing.Optional[DockerAssetJobSettings]:
        '''(experimental) Job level settings applied to all docker asset publishing jobs in the workflow.

        :default: - no additional settings

        :stability: experimental
        '''
        result = self._values.get("docker_asset_job_settings")
        return typing.cast(typing.Optional[DockerAssetJobSettings], result)

    @builtins.property
    def docker_credentials(self) -> typing.Optional[typing.List[DockerCredential]]:
        '''(experimental) The Docker Credentials to use to login.

        If you set this variable,
        you will be logged in to docker when you upload Docker Assets.

        :stability: experimental
        '''
        result = self._values.get("docker_credentials")
        return typing.cast(typing.Optional[typing.List[DockerCredential]], result)

    @builtins.property
    def git_hub_action_role_arn(self) -> typing.Optional[builtins.str]:
        '''(deprecated) A role that utilizes the GitHub OIDC Identity Provider in your AWS account.

        If supplied, this will be used instead of ``awsCredentials``.

        You can create your own role in the console with the necessary trust policy
        to allow gitHub actions from your gitHub repository to assume the role, or
        you can utilize the ``GitHubActionRole`` construct to create a role for you.

        :default: - GitHub repository secrets are used instead of OpenId Connect role.

        :deprecated: Use ``awsCreds.fromOpenIdConnect()`` instead.

        :stability: deprecated
        '''
        result = self._values.get("git_hub_action_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_settings(self) -> typing.Optional["JobSettings"]:
        '''(experimental) Job level settings that will be applied to all jobs in the workflow, including synth and asset deploy jobs.

        Currently the only valid setting
        is 'if'. You can use this to run jobs only in specific repositories.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-only-run-job-for-specific-repository
        :stability: experimental
        '''
        result = self._values.get("job_settings")
        return typing.cast(typing.Optional["JobSettings"], result)

    @builtins.property
    def post_build_steps(self) -> typing.Optional[typing.List["JobStep"]]:
        '''(experimental) GitHub workflow steps to execute after build.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List["JobStep"]], result)

    @builtins.property
    def pre_build_steps(self) -> typing.Optional[typing.List["JobStep"]]:
        '''(experimental) GitHub workflow steps to execute before build.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("pre_build_steps")
        return typing.cast(typing.Optional[typing.List["JobStep"]], result)

    @builtins.property
    def pre_synthed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if the repository already contains a synthesized ``cdk.out`` directory, in which case we will simply checkout the repo in jobs that require ``cdk.out``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("pre_synthed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_assets_auth_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Will assume the GitHubActionRole in this region when publishing assets.

        This is NOT the region in which the assets are published.

        In most cases, you do not have to worry about this property, and can safely
        ignore it.

        :default: "us-west-2"

        :stability: experimental
        '''
        result = self._values.get("publish_assets_auth_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runner(self) -> typing.Optional["Runner"]:
        '''(experimental) The type of runner to run the job on.

        The runner can be either a
        GitHub-hosted runner or a self-hosted runner.

        :default: Runner.UBUNTU_LATEST

        :stability: experimental
        '''
        result = self._values.get("runner")
        return typing.cast(typing.Optional["Runner"], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the workflow.

        :default: "deploy"

        :stability: experimental
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) File path for the GitHub workflow.

        :default: ".github/workflows/deploy.yml"

        :stability: experimental
        '''
        result = self._values.get("workflow_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_triggers(self) -> typing.Optional["WorkflowTriggers"]:
        '''(experimental) GitHub workflow triggers.

        :default:

        - By default, workflow is triggered on push to the ``main`` branch
        and can also be triggered manually (``workflow_dispatch``).

        :stability: experimental
        '''
        result = self._values.get("workflow_triggers")
        return typing.cast(typing.Optional["WorkflowTriggers"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubWorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GollumOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GollumOptions:
    def __init__(self) -> None:
        '''(experimental) The Gollum event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GollumOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.IssueCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssueCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Issue comment options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8f5cb2188fc6ddf4cf79f0ff67bbc59e9abc16f167214dfa10723f80b51965)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.IssuesOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssuesOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Issues options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8824add0f693226a3bfa1fec2f9e7ffaf9ef3b2d98f2a3df534226802135fd7f)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssuesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.Job",
    jsii_struct_bases=[],
    name_mapping={
        "permissions": "permissions",
        "runs_on": "runsOn",
        "steps": "steps",
        "concurrency": "concurrency",
        "container": "container",
        "continue_on_error": "continueOnError",
        "defaults": "defaults",
        "env": "env",
        "environment": "environment",
        "if_": "if",
        "name": "name",
        "needs": "needs",
        "outputs": "outputs",
        "services": "services",
        "strategy": "strategy",
        "timeout_minutes": "timeoutMinutes",
    },
)
class Job:
    def __init__(
        self,
        *,
        permissions: typing.Union["JobPermissions", typing.Dict[builtins.str, typing.Any]],
        runs_on: typing.Union[builtins.str, typing.Sequence[builtins.str]],
        steps: typing.Sequence[typing.Union["JobStep", typing.Dict[builtins.str, typing.Any]]],
        concurrency: typing.Any = None,
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union["JobDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Any = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) A GitHub Workflow job definition.

        :param permissions: (experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access. Use ``{ contents: READ }`` if your job only needs to clone code. This is intentionally a required field since it is required in order to allow workflows to run in GitHub repositories with restricted default access.
        :param runs_on: (experimental) The type of machine to run the job on. The machine can be either a GitHub-hosted runner or a self-hosted runner.
        :param steps: (experimental) A job contains a sequence of tasks called steps. Steps can run commands, run setup tasks, or run an action in your repository, a public repository, or an action published in a Docker registry. Not all steps run actions, but all actions run as a step. Each step runs in its own process in the runner environment and has access to the workspace and filesystem. Because steps run in their own process, changes to environment variables are not preserved between steps. GitHub provides built-in steps to set up and complete a job.
        :param concurrency: (experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time. A concurrency group can be any string or expression. The expression can use any context except for the secrets context.
        :param container: (experimental) A container to run any steps in a job that don't already specify a container. If you have steps that use both script and container actions, the container actions will run as sibling containers on the same network with the same volume mounts.
        :param continue_on_error: (experimental) Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.
        :param defaults: (experimental) A map of default settings that will apply to all steps in the job. You can also set default settings for the entire workflow.
        :param env: (experimental) A map of environment variables that are available to all steps in the job. You can also set environment variables for the entire workflow or an individual step.
        :param environment: (experimental) The environment that the job references. All environment protection rules must pass before a job referencing the environment is sent to a runner.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) The name of the job displayed on GitHub.
        :param needs: (experimental) Identifies any jobs that must complete successfully before this job will run. It can be a string or array of strings. If a job fails, all jobs that need it are skipped unless the jobs use a conditional expression that causes the job to continue.
        :param outputs: (experimental) A map of outputs for a job. Job outputs are available to all downstream jobs that depend on this job.
        :param services: (experimental) Used to host service containers for a job in a workflow. Service containers are useful for creating databases or cache services like Redis. The runner automatically creates a Docker network and manages the life cycle of the service containers.
        :param strategy: (experimental) A strategy creates a build matrix for your jobs. You can define different variations to run each job in.
        :param timeout_minutes: (experimental) The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360

        :stability: experimental
        '''
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if isinstance(container, dict):
            container = ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = JobDefaults(**defaults)
        if isinstance(strategy, dict):
            strategy = JobStrategy(**strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d74634ced8efa05c46052c781206dcfcf038fee236dccfe2a9a1dbac8a09aec)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permissions": permissions,
            "runs_on": runs_on,
            "steps": steps,
        }
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if container is not None:
            self._values["container"] = container
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if defaults is not None:
            self._values["defaults"] = defaults
        if env is not None:
            self._values["env"] = env
        if environment is not None:
            self._values["environment"] = environment
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if outputs is not None:
            self._values["outputs"] = outputs
        if services is not None:
            self._values["services"] = services
        if strategy is not None:
            self._values["strategy"] = strategy
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def permissions(self) -> "JobPermissions":
        '''(experimental) You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access.

        Use ``{ contents: READ }`` if your job only needs to clone code.

        This is intentionally a required field since it is required in order to
        allow workflows to run in GitHub repositories with restricted default
        access.

        :see: https://docs.github.com/en/actions/reference/authentication-in-a-workflow#permissions-for-the-github_token
        :stability: experimental
        '''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast("JobPermissions", result)

    @builtins.property
    def runs_on(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''(experimental) The type of machine to run the job on.

        The machine can be either a
        GitHub-hosted runner or a self-hosted runner.

        :stability: experimental

        Example::

            ["ubuntu-latest"]
        '''
        result = self._values.get("runs_on")
        assert result is not None, "Required property 'runs_on' is missing"
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], result)

    @builtins.property
    def steps(self) -> typing.List["JobStep"]:
        '''(experimental) A job contains a sequence of tasks called steps.

        Steps can run commands,
        run setup tasks, or run an action in your repository, a public repository,
        or an action published in a Docker registry. Not all steps run actions,
        but all actions run as a step. Each step runs in its own process in the
        runner environment and has access to the workspace and filesystem.
        Because steps run in their own process, changes to environment variables
        are not preserved between steps. GitHub provides built-in steps to set up
        and complete a job.

        :stability: experimental
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.List["JobStep"], result)

    @builtins.property
    def concurrency(self) -> typing.Any:
        '''(experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time.

        A concurrency group can be any
        string or expression. The expression can use any context except for the
        secrets context.

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Any, result)

    @builtins.property
    def container(self) -> typing.Optional[ContainerOptions]:
        '''(experimental) A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.

        :stability: experimental
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[ContainerOptions], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevents a workflow run from failing when a job fails.

        Set to true to
        allow a workflow run to pass when this job fails.

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def defaults(self) -> typing.Optional["JobDefaults"]:
        '''(experimental) A map of default settings that will apply to all steps in the job.

        You
        can also set default settings for the entire workflow.

        :stability: experimental
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional["JobDefaults"], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A map of environment variables that are available to all steps in the job.

        You can also set environment variables for the entire workflow or an
        individual step.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Any:
        '''(experimental) The environment that the job references.

        All environment protection rules
        must pass before a job referencing the environment is sent to a runner.

        :see: https://docs.github.com/en/actions/reference/environments
        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Any, result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the job displayed on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Identifies any jobs that must complete successfully before this job will run.

        It can be a string or array of strings. If a job fails, all jobs
        that need it are skipped unless the jobs use a conditional expression
        that causes the job to continue.

        :stability: experimental
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A map of outputs for a job.

        Job outputs are available to all downstream
        jobs that depend on this job.

        :stability: experimental
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ContainerOptions]]:
        '''(experimental) Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["JobStrategy"]:
        '''(experimental) A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.

        :stability: experimental
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["JobStrategy"], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of minutes to let a job run before GitHub automatically cancels it.

        :default: 360

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Job(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobDefaults",
    jsii_struct_bases=[],
    name_mapping={"run": "run"},
)
class JobDefaults:
    def __init__(
        self,
        *,
        run: typing.Optional[typing.Union["RunSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Default settings for all steps in the job.

        :param run: (experimental) Default run settings.

        :stability: experimental
        '''
        if isinstance(run, dict):
            run = RunSettings(**run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32147cd5f8d7d9ef77d5a96c7435d9911055f7183cb8ac9d412558c3e2fea8e)
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if run is not None:
            self._values["run"] = run

    @builtins.property
    def run(self) -> typing.Optional["RunSettings"]:
        '''(experimental) Default run settings.

        :stability: experimental
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional["RunSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobMatrix",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "exclude": "exclude", "include": "include"},
)
class JobMatrix:
    def __init__(
        self,
        *,
        domain: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
        include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''(experimental) A job matrix.

        :param domain: (experimental) Each option you define in the matrix has a key and value. The keys you define become properties in the matrix context and you can reference the property in other areas of your workflow file. For example, if you define the key os that contains an array of operating systems, you can use the matrix.os property as the value of the runs-on keyword to create a job for each operating system.
        :param exclude: (experimental) You can remove a specific configurations defined in the build matrix using the exclude option. Using exclude removes a job defined by the build matrix.
        :param include: (experimental) You can add additional configuration options to a build matrix job that already exists. For example, if you want to use a specific version of npm when the job that uses windows-latest and version 8 of node runs, you can use include to specify that additional option.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839885d4d07812573dc2f6bbc6039fda3a4c68bd72a52dfb040eb6d9db46b2a5)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if exclude is not None:
            self._values["exclude"] = exclude
        if include is not None:
            self._values["include"] = include

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''(experimental) Each option you define in the matrix has a key and value.

        The keys you
        define become properties in the matrix context and you can reference the
        property in other areas of your workflow file. For example, if you define
        the key os that contains an array of operating systems, you can use the
        matrix.os property as the value of the runs-on keyword to create a job
        for each operating system.

        :stability: experimental
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        '''(experimental) You can remove a specific configurations defined in the build matrix using the exclude option.

        Using exclude removes a job defined by the
        build matrix.

        :stability: experimental
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def include(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        '''(experimental) You can add additional configuration options to a build matrix job that already exists.

        For example, if you want to use a specific version of npm
        when the job that uses windows-latest and version 8 of node runs, you can
        use include to specify that additional option.

        :stability: experimental
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobMatrix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-pipelines-github.JobPermission")
class JobPermission(enum.Enum):
    '''(experimental) Access level for workflow permission scopes.

    :stability: experimental
    '''

    READ = "READ"
    '''(experimental) Read-only access.

    :stability: experimental
    '''
    WRITE = "WRITE"
    '''(experimental) Read-write access.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) No access at all.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "checks": "checks",
        "contents": "contents",
        "deployments": "deployments",
        "discussions": "discussions",
        "id_token": "idToken",
        "issues": "issues",
        "packages": "packages",
        "pull_requests": "pullRequests",
        "repository_projects": "repositoryProjects",
        "security_events": "securityEvents",
        "statuses": "statuses",
    },
)
class JobPermissions:
    def __init__(
        self,
        *,
        actions: typing.Optional[JobPermission] = None,
        checks: typing.Optional[JobPermission] = None,
        contents: typing.Optional[JobPermission] = None,
        deployments: typing.Optional[JobPermission] = None,
        discussions: typing.Optional[JobPermission] = None,
        id_token: typing.Optional[JobPermission] = None,
        issues: typing.Optional[JobPermission] = None,
        packages: typing.Optional[JobPermission] = None,
        pull_requests: typing.Optional[JobPermission] = None,
        repository_projects: typing.Optional[JobPermission] = None,
        security_events: typing.Optional[JobPermission] = None,
        statuses: typing.Optional[JobPermission] = None,
    ) -> None:
        '''(experimental) The available scopes and access values for workflow permissions.

        If you
        specify the access for any of these scopes, all those that are not
        specified are set to ``JobPermission.NONE``, instead of the default behavior
        when none is specified.

        :param actions: 
        :param checks: 
        :param contents: 
        :param deployments: 
        :param discussions: 
        :param id_token: 
        :param issues: 
        :param packages: 
        :param pull_requests: 
        :param repository_projects: 
        :param security_events: 
        :param statuses: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ebccc396832c41c1f28ee27122716bee7c27553b4a406cb7b755d8c7280e398)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument checks", value=checks, expected_type=type_hints["checks"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument deployments", value=deployments, expected_type=type_hints["deployments"])
            check_type(argname="argument discussions", value=discussions, expected_type=type_hints["discussions"])
            check_type(argname="argument id_token", value=id_token, expected_type=type_hints["id_token"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument pull_requests", value=pull_requests, expected_type=type_hints["pull_requests"])
            check_type(argname="argument repository_projects", value=repository_projects, expected_type=type_hints["repository_projects"])
            check_type(argname="argument security_events", value=security_events, expected_type=type_hints["security_events"])
            check_type(argname="argument statuses", value=statuses, expected_type=type_hints["statuses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if checks is not None:
            self._values["checks"] = checks
        if contents is not None:
            self._values["contents"] = contents
        if deployments is not None:
            self._values["deployments"] = deployments
        if discussions is not None:
            self._values["discussions"] = discussions
        if id_token is not None:
            self._values["id_token"] = id_token
        if issues is not None:
            self._values["issues"] = issues
        if packages is not None:
            self._values["packages"] = packages
        if pull_requests is not None:
            self._values["pull_requests"] = pull_requests
        if repository_projects is not None:
            self._values["repository_projects"] = repository_projects
        if security_events is not None:
            self._values["security_events"] = security_events
        if statuses is not None:
            self._values["statuses"] = statuses

    @builtins.property
    def actions(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def checks(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("checks")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def contents(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def deployments(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("deployments")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def discussions(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("discussions")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def id_token(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("id_token")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def issues(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def packages(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def pull_requests(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pull_requests")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def repository_projects(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("repository_projects")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def security_events(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_events")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def statuses(self) -> typing.Optional[JobPermission]:
        '''
        :stability: experimental
        '''
        result = self._values.get("statuses")
        return typing.cast(typing.Optional[JobPermission], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobSettings",
    jsii_struct_bases=[],
    name_mapping={"if_": "if"},
)
class JobSettings:
    def __init__(self, *, if_: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Job level settings applied to all jobs in the workflow.

        :param if_: (experimental) jobs.<job_id>.if.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d93c13f4ea5805aa31e5daa7a5204c943a1a44020ede8f01e81966e3f1725e)
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if if_ is not None:
            self._values["if_"] = if_

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) jobs.<job_id>.if.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idif
        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobStep",
    jsii_struct_bases=[],
    name_mapping={
        "continue_on_error": "continueOnError",
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "run": "run",
        "timeout_minutes": "timeoutMinutes",
        "uses": "uses",
        "with_": "with",
    },
)
class JobStep:
    def __init__(
        self,
        *,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        run: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        uses: typing.Optional[builtins.str] = None,
        with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) A job step.

        :param continue_on_error: (experimental) Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails.
        :param env: (experimental) Sets environment variables for steps to use in the runner environment. You can also set environment variables for the entire workflow or a job.
        :param id: (experimental) A unique identifier for the step. You can use the id to reference the step in contexts.
        :param if_: (experimental) You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: (experimental) A name for your step to display on GitHub.
        :param run: (experimental) Runs command-line programs using the operating system's shell. If you do not provide a name, the step name will default to the text specified in the run command.
        :param timeout_minutes: (experimental) The maximum number of minutes to run the step before killing the process.
        :param uses: (experimental) Selects an action to run as part of a step in your job. An action is a reusable unit of code. You can use an action defined in the same repository as the workflow, a public repository, or in a published Docker container image.
        :param with_: (experimental) A map of the input parameters defined by the action. Each input parameter is a key/value pair. Input parameters are set as environment variables. The variable is prefixed with INPUT_ and converted to upper case.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e761fdc1044ff886640a8e5d64fa3d3e1a780efcecbbd275e4c31055101433)
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            check_type(argname="argument uses", value=uses, expected_type=type_hints["uses"])
            check_type(argname="argument with_", value=with_, expected_type=type_hints["with_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if run is not None:
            self._values["run"] = run
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes
        if uses is not None:
            self._values["uses"] = uses
        if with_ is not None:
            self._values["with_"] = with_

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevents a job from failing when a step fails.

        Set to true to allow a job
        to pass when this step fails.

        :stability: experimental
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Sets environment variables for steps to use in the runner environment.

        You can also set environment variables for the entire workflow or a job.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique identifier for the step.

        You can use the id to reference the
        step in contexts.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''(experimental) You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.

        :stability: experimental
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for your step to display on GitHub.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run(self) -> typing.Optional[builtins.str]:
        '''(experimental) Runs command-line programs using the operating system's shell.

        If you do
        not provide a name, the step name will default to the text specified in
        the run command.

        :stability: experimental
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of minutes to run the step before killing the process.

        :stability: experimental
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uses(self) -> typing.Optional[builtins.str]:
        '''(experimental) Selects an action to run as part of a step in your job.

        An action is a
        reusable unit of code. You can use an action defined in the same
        repository as the workflow, a public repository, or in a published Docker
        container image.

        :stability: experimental
        '''
        result = self._values.get("uses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) A map of the input parameters defined by the action.

        Each input parameter
        is a key/value pair. Input parameters are set as environment variables.
        The variable is prefixed with INPUT_ and converted to upper case.

        :stability: experimental
        '''
        result = self._values.get("with_")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobStepOutput",
    jsii_struct_bases=[],
    name_mapping={"output_name": "outputName", "step_id": "stepId"},
)
class JobStepOutput:
    def __init__(self, *, output_name: builtins.str, step_id: builtins.str) -> None:
        '''(experimental) An output binding for a job.

        :param output_name: (experimental) The name of the job output that is being bound.
        :param step_id: (experimental) The ID of the step that exposes the output.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9232daf74d562c79cb6fce855867d01e489d3946367e284bc9185b7c8a757a)
            check_type(argname="argument output_name", value=output_name, expected_type=type_hints["output_name"])
            check_type(argname="argument step_id", value=step_id, expected_type=type_hints["step_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "output_name": output_name,
            "step_id": step_id,
        }

    @builtins.property
    def output_name(self) -> builtins.str:
        '''(experimental) The name of the job output that is being bound.

        :stability: experimental
        '''
        result = self._values.get("output_name")
        assert result is not None, "Required property 'output_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def step_id(self) -> builtins.str:
        '''(experimental) The ID of the step that exposes the output.

        :stability: experimental
        '''
        result = self._values.get("step_id")
        assert result is not None, "Required property 'step_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStepOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "fail_fast": "failFast",
        "matrix": "matrix",
        "max_parallel": "maxParallel",
    },
)
class JobStrategy:
    def __init__(
        self,
        *,
        fail_fast: typing.Optional[builtins.bool] = None,
        matrix: typing.Optional[typing.Union[JobMatrix, typing.Dict[builtins.str, typing.Any]]] = None,
        max_parallel: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.

        :param fail_fast: (experimental) When set to true, GitHub cancels all in-progress jobs if any matrix job fails. Default: true
        :param matrix: (experimental) You can define a matrix of different job configurations. A matrix allows you to create multiple jobs by performing variable substitution in a single job definition. For example, you can use a matrix to create jobs for more than one supported version of a programming language, operating system, or tool. A matrix reuses the job's configuration and creates a job for each matrix you configure. A job matrix can generate a maximum of 256 jobs per workflow run. This limit also applies to self-hosted runners.
        :param max_parallel: (experimental) The maximum number of jobs that can run simultaneously when using a matrix job strategy. By default, GitHub will maximize the number of jobs run in parallel depending on the available runners on GitHub-hosted virtual machines.

        :stability: experimental
        '''
        if isinstance(matrix, dict):
            matrix = JobMatrix(**matrix)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80d0bb466d3a822db3284ee7f61b9d956788379459cbf8a8ab4be116d4b3ea4)
            check_type(argname="argument fail_fast", value=fail_fast, expected_type=type_hints["fail_fast"])
            check_type(argname="argument matrix", value=matrix, expected_type=type_hints["matrix"])
            check_type(argname="argument max_parallel", value=max_parallel, expected_type=type_hints["max_parallel"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fail_fast is not None:
            self._values["fail_fast"] = fail_fast
        if matrix is not None:
            self._values["matrix"] = matrix
        if max_parallel is not None:
            self._values["max_parallel"] = max_parallel

    @builtins.property
    def fail_fast(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When set to true, GitHub cancels all in-progress jobs if any matrix job fails.

        Default: true

        :stability: experimental
        '''
        result = self._values.get("fail_fast")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def matrix(self) -> typing.Optional[JobMatrix]:
        '''(experimental) You can define a matrix of different job configurations.

        A matrix allows
        you to create multiple jobs by performing variable substitution in a
        single job definition. For example, you can use a matrix to create jobs
        for more than one supported version of a programming language, operating
        system, or tool. A matrix reuses the job's configuration and creates a
        job for each matrix you configure.

        A job matrix can generate a maximum of 256 jobs per workflow run. This
        limit also applies to self-hosted runners.

        :stability: experimental
        '''
        result = self._values.get("matrix")
        return typing.cast(typing.Optional[JobMatrix], result)

    @builtins.property
    def max_parallel(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of jobs that can run simultaneously when using a matrix job strategy.

        By default, GitHub will maximize the number of jobs
        run in parallel depending on the available runners on GitHub-hosted
        virtual machines.

        :stability: experimental
        '''
        result = self._values.get("max_parallel")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JsonPatch(metaclass=jsii.JSIIMeta, jsii_type="cdk-pipelines-github.JsonPatch"):
    '''(experimental) Utility for applying RFC-6902 JSON-Patch to a document.

    Use the the ``JsonPatch.apply(doc, ...ops)`` function to apply a set of
    operations to a JSON document and return the result.

    Operations can be created using the factory methods ``JsonPatch.add()``,
    ``JsonPatch.remove()``, etc.

    const output = JsonPatch.apply(input,
    JsonPatch.replace('/world/hi/there', 'goodbye'),
    JsonPatch.add('/world/foo/', 'boom'),
    JsonPatch.remove('/hello'),
    );

    :stability: experimental
    '''

    @jsii.member(jsii_name="add")
    @builtins.classmethod
    def add(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''(experimental) Adds a value to an object or inserts it into an array.

        In the case of an
        array, the value is inserted before the given index. The - character can be
        used instead of an index to insert at the end of an array.

        :param path: -
        :param value: -

        :stability: experimental

        Example::

            JsonPatch.add("/biscuits/1", {"name": "Ginger Nut"})
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b7788c908a37168f0d99a50070ea29369813aa2c07c46417c395a9c2d65125)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "add", [path, value]))

    @jsii.member(jsii_name="apply")
    @builtins.classmethod
    def apply(cls, document: typing.Any, *ops: "JsonPatch") -> typing.Any:
        '''(experimental) Applies a set of JSON-Patch (RFC-6902) operations to ``document`` and returns the result.

        :param document: The document to patch.
        :param ops: The operations to apply.

        :return: The result document

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e02d9f326f3f13fe6e498e98316a665a729d42b3a34470f5b450fd2c53a505)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
            check_type(argname="argument ops", value=ops, expected_type=typing.Tuple[type_hints["ops"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.Any, jsii.sinvoke(cls, "apply", [document, *ops]))

    @jsii.member(jsii_name="copy")
    @builtins.classmethod
    def copy(cls, from_: builtins.str, path: builtins.str) -> "JsonPatch":
        '''(experimental) Copies a value from one location to another within the JSON document.

        Both
        from and path are JSON Pointers.

        :param from_: -
        :param path: -

        :stability: experimental

        Example::

            JsonPatch.copy("/biscuits/0", "/best_biscuit")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd8d0d82351b216410123e49c91d33dbeae270ed2c75d19ce5ac542be62c688)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "copy", [from_, path]))

    @jsii.member(jsii_name="move")
    @builtins.classmethod
    def move(cls, from_: builtins.str, path: builtins.str) -> "JsonPatch":
        '''(experimental) Moves a value from one location to the other.

        Both from and path are JSON Pointers.

        :param from_: -
        :param path: -

        :stability: experimental

        Example::

            JsonPatch.move("/biscuits", "/cookies")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4242ceab4f40bfa6a19a3aca0a6642e91fa90516642ead4c19ea3174012e02d6)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "move", [from_, path]))

    @jsii.member(jsii_name="remove")
    @builtins.classmethod
    def remove(cls, path: builtins.str) -> "JsonPatch":
        '''(experimental) Removes a value from an object or array.

        :param path: -

        :stability: experimental

        Example::

            JsonPatch.remove("/biscuits/0")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e69cfe81d249b73a6eb12bc222bd94d3e5f15a49220ac470d6348bc5620fa5)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "remove", [path]))

    @jsii.member(jsii_name="replace")
    @builtins.classmethod
    def replace(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''(experimental) Replaces a value.

        Equivalent to a “remove” followed by an “add”.

        :param path: -
        :param value: -

        :stability: experimental

        Example::

            JsonPatch.replace("/biscuits/0/name", "Chocolate Digestive")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1101cca45fa8bcb4442ca950cf671ef5a494621f4c0ae65013e76127d54372)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "replace", [path, value]))

    @jsii.member(jsii_name="test")
    @builtins.classmethod
    def test(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''(experimental) Tests that the specified value is set in the document.

        If the test fails,
        then the patch as a whole should not apply.

        :param path: -
        :param value: -

        :stability: experimental

        Example::

            JsonPatch.test("/best_biscuit/name", "Choco Leibniz")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b585eb3f9d8bd6ac3b3ececc9183622d96ed862967465fd85524abfd1a7509)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "test", [path, value]))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.LabelOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class LabelOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) label options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a31017e70cb6b10d1c7f22bd885378e69fd7cf50494f506d84c501f5b15608)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.MilestoneOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class MilestoneOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Milestone options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e2b08dda1c24d3f5b1432e6b6612b9516d77077a30b82d589b6aff3d76ec56)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MilestoneOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.OpenIdConnectProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "git_hub_action_role_arn": "gitHubActionRoleArn",
        "role_session_name": "roleSessionName",
    },
)
class OpenIdConnectProviderProps:
    def __init__(
        self,
        *,
        git_hub_action_role_arn: builtins.str,
        role_session_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Role to assume using OpenId Connect.

        :param git_hub_action_role_arn: (experimental) A role that utilizes the GitHub OIDC Identity Provider in your AWS account. You can create your own role in the console with the necessary trust policy to allow gitHub actions from your gitHub repository to assume the role, or you can utilize the ``GitHubActionRole`` construct to create a role for you.
        :param role_session_name: (experimental) The role session name to use when assuming the role. Default: - no role session name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8201325ae4a8c45dcbe4c7d868e0b03bc0213efc4ea619c852046ba5517e5fc5)
            check_type(argname="argument git_hub_action_role_arn", value=git_hub_action_role_arn, expected_type=type_hints["git_hub_action_role_arn"])
            check_type(argname="argument role_session_name", value=role_session_name, expected_type=type_hints["role_session_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "git_hub_action_role_arn": git_hub_action_role_arn,
        }
        if role_session_name is not None:
            self._values["role_session_name"] = role_session_name

    @builtins.property
    def git_hub_action_role_arn(self) -> builtins.str:
        '''(experimental) A role that utilizes the GitHub OIDC Identity Provider in your AWS account.

        You can create your own role in the console with the necessary trust policy
        to allow gitHub actions from your gitHub repository to assume the role, or
        you can utilize the ``GitHubActionRole`` construct to create a role for you.

        :stability: experimental
        '''
        result = self._values.get("git_hub_action_role_arn")
        assert result is not None, "Required property 'git_hub_action_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_session_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The role session name to use when assuming the role.

        :default: - no role session name

        :stability: experimental
        '''
        result = self._values.get("role_session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenIdConnectProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PageBuildOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PageBuildOptions:
    def __init__(self) -> None:
        '''(experimental) The Page build event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PageBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ProjectCardOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectCardOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Project card options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc685756612eea88a78ef100a9ab03ecac50481a14fccb75b9aefa7f670722f)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectCardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ProjectColumnOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectColumnOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Probject column options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e9baa3bb445be4a5c414eddefc47be7856a0fcb206263592f0ffc303384949)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectColumnOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ProjectOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Project options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6773683d69a971c7c5c0742f143d5e61a34617d7d5c707933904275488cca3af)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PublicOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PublicOptions:
    def __init__(self) -> None:
        '''(experimental) The Public event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublicOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PullRequestOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pull request options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678b381f2938a5a7e53c0cb4d2361ddb2a4e20a028116d03028bc086bd4ea7fa)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PullRequestReviewCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pull request review comment options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f130898e52637b9538ce0e89004dbd887b836d2df1e0b86639abb3e0d2267ee1)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PullRequestReviewOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pull request review options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1689dcb0d428eac4995ce80d3cc1c9424174c9f1502514694753d97a4e562870)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PushOptions",
    jsii_struct_bases=[],
    name_mapping={"branches": "branches", "paths": "paths", "tags": "tags"},
)
class PushOptions:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for push-like events.

        :param branches: (experimental) When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: (experimental) When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: (experimental) When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45e66fc18901adbbc7c16879f5085ed2ddc0c914ecf282679698f5e0189a2768)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PushOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.RegistryPackageOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RegistryPackageOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Registry package options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6fea0503ac1ec6392b103a3f32726778118e585380cb62e87de177f6d324ad)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryPackageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ReleaseOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ReleaseOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Release options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b515fd62c1ee49f5eeae11c884f13e8faeef5c2f5baa85c5dbc0a361a205b2)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.RepositoryDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RepositoryDispatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Repository dispatch options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c431e7bcb272169575a643e18f3e1d362a2bf63f482f9d3d3a1af5911bb915d5)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.RunSettings",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell", "working_directory": "workingDirectory"},
)
class RunSettings:
    def __init__(
        self,
        *,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Run settings for a job.

        :param shell: (experimental) Which shell to use for running the step.
        :param working_directory: (experimental) Working directory to use when running the step.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665e1d5fb187329ece0a9f5e476acf29e23d80806e3ca2852036ca53539ac7da)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''(experimental) Which shell to use for running the step.

        :stability: experimental

        Example::

            "bash"
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Working directory to use when running the step.

        :stability: experimental
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Runner(metaclass=jsii.JSIIMeta, jsii_type="cdk-pipelines-github.Runner"):
    '''(experimental) The type of runner to run the job on.

    Can be GitHub or Self-hosted.
    In case of self-hosted, a list of labels can be supplied.

    :stability: experimental
    '''

    @jsii.member(jsii_name="selfHosted")
    @builtins.classmethod
    def self_hosted(cls, labels: typing.Sequence[builtins.str]) -> "Runner":
        '''(experimental) Creates a runner instance that sets runsOn to ``self-hosted``.

        Additional labels can be supplied. There is no need to supply ``self-hosted`` as a label explicitly.

        :param labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7aa98e7950895be604e27ddee038769e89e361d47f176b549fa2529a847f00)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        return typing.cast("Runner", jsii.sinvoke(cls, "selfHosted", [labels]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MACOS_LATEST")
    def MACOS_LATEST(cls) -> "Runner":
        '''(experimental) Runner instance that sets runsOn to ``macos-latest``.

        :stability: experimental
        '''
        return typing.cast("Runner", jsii.sget(cls, "MACOS_LATEST"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_LATEST")
    def UBUNTU_LATEST(cls) -> "Runner":
        '''(experimental) Runner instance that sets runsOn to ``ubuntu-latest``.

        :stability: experimental
        '''
        return typing.cast("Runner", jsii.sget(cls, "UBUNTU_LATEST"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS_LATEST")
    def WINDOWS_LATEST(cls) -> "Runner":
        '''(experimental) Runner instance that sets runsOn to ``windows-latest``.

        :stability: experimental
        '''
        return typing.cast("Runner", jsii.sget(cls, "WINDOWS_LATEST"))

    @builtins.property
    @jsii.member(jsii_name="runsOn")
    def runs_on(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], jsii.get(self, "runsOn"))


@jsii.enum(jsii_type="cdk-pipelines-github.StackCapabilities")
class StackCapabilities(enum.Enum):
    '''(experimental) Acknowledge IAM resources in AWS CloudFormation templates.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#capabilities
    :stability: experimental
    '''

    IAM = "IAM"
    '''(experimental) Acknowledge your stack includes IAM resources.

    :stability: experimental
    '''
    NAMED_IAM = "NAMED_IAM"
    '''(experimental) Acknowledge your stack includes custom names for IAM resources.

    :stability: experimental
    '''
    AUTO_EXPAND = "AUTO_EXPAND"
    '''(experimental) Acknowledge your stack contains one or more macros.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="cdk-pipelines-github.StatusOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class StatusOptions:
    def __init__(self) -> None:
        '''(experimental) The Status event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatusOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.WatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Watch options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54a4ec9b0e947b929cf7238ed16d4855d8bf09fc3601cd993c7f43b97de2d73)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.WorkflowDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkflowDispatchOptions:
    def __init__(self) -> None:
        '''(experimental) The Workflow dispatch event accepts no options.

        :stability: experimental
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.WorkflowRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WorkflowRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Workflow run options.

        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84af6712d2185aed478f3af7f480af3eb94e4c399885ab7de3a691abe0bfa85)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.WorkflowTriggers",
    jsii_struct_bases=[],
    name_mapping={
        "check_run": "checkRun",
        "check_suite": "checkSuite",
        "create": "create",
        "delete": "delete",
        "deployment": "deployment",
        "deployment_status": "deploymentStatus",
        "fork": "fork",
        "gollum": "gollum",
        "issue_comment": "issueComment",
        "issues": "issues",
        "label": "label",
        "milestone": "milestone",
        "page_build": "pageBuild",
        "project": "project",
        "project_card": "projectCard",
        "project_column": "projectColumn",
        "public": "public",
        "pull_request": "pullRequest",
        "pull_request_review": "pullRequestReview",
        "pull_request_review_comment": "pullRequestReviewComment",
        "pull_request_target": "pullRequestTarget",
        "push": "push",
        "registry_package": "registryPackage",
        "release": "release",
        "repository_dispatch": "repositoryDispatch",
        "schedule": "schedule",
        "status": "status",
        "watch": "watch",
        "workflow_dispatch": "workflowDispatch",
        "workflow_run": "workflowRun",
    },
)
class WorkflowTriggers:
    def __init__(
        self,
        *,
        check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        create: typing.Optional[typing.Union[CreateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        delete: typing.Optional[typing.Union[DeleteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment: typing.Optional[typing.Union[DeploymentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_status: typing.Optional[typing.Union[DeploymentStatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        fork: typing.Optional[typing.Union[ForkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        gollum: typing.Optional[typing.Union[GollumOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        label: typing.Optional[typing.Union[LabelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        page_build: typing.Optional[typing.Union[PageBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        public: typing.Optional[typing.Union[PublicOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pull_request_target: typing.Optional[typing.Union["PullRequestTargetOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        push: typing.Optional[typing.Union[PushOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        status: typing.Optional[typing.Union[StatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_dispatch: typing.Optional[typing.Union[WorkflowDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The set of available triggers for GitHub Workflows.

        :param check_run: (experimental) Runs your workflow anytime the check_run event occurs.
        :param check_suite: (experimental) Runs your workflow anytime the check_suite event occurs.
        :param create: (experimental) Runs your workflow anytime someone creates a branch or tag, which triggers the create event.
        :param delete: (experimental) Runs your workflow anytime someone deletes a branch or tag, which triggers the delete event.
        :param deployment: (experimental) Runs your workflow anytime someone creates a deployment, which triggers the deployment event. Deployments created with a commit SHA may not have a Git ref.
        :param deployment_status: (experimental) Runs your workflow anytime a third party provides a deployment status, which triggers the deployment_status event. Deployments created with a commit SHA may not have a Git ref.
        :param fork: (experimental) Runs your workflow anytime when someone forks a repository, which triggers the fork event.
        :param gollum: (experimental) Runs your workflow when someone creates or updates a Wiki page, which triggers the gollum event.
        :param issue_comment: (experimental) Runs your workflow anytime the issue_comment event occurs.
        :param issues: (experimental) Runs your workflow anytime the issues event occurs.
        :param label: (experimental) Runs your workflow anytime the label event occurs.
        :param milestone: (experimental) Runs your workflow anytime the milestone event occurs.
        :param page_build: (experimental) Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch, which triggers the page_build event.
        :param project: (experimental) Runs your workflow anytime the project event occurs.
        :param project_card: (experimental) Runs your workflow anytime the project_card event occurs.
        :param project_column: (experimental) Runs your workflow anytime the project_column event occurs.
        :param public: (experimental) Runs your workflow anytime someone makes a private repository public, which triggers the public event.
        :param pull_request: (experimental) Runs your workflow anytime the pull_request event occurs.
        :param pull_request_review: (experimental) Runs your workflow anytime the pull_request_review event occurs.
        :param pull_request_review_comment: (experimental) Runs your workflow anytime a comment on a pull request's unified diff is modified, which triggers the pull_request_review_comment event.
        :param pull_request_target: (experimental) This event runs in the context of the base of the pull request, rather than in the merge commit as the pull_request event does. This prevents executing unsafe workflow code from the head of the pull request that could alter your repository or steal any secrets you use in your workflow. This event allows you to do things like create workflows that label and comment on pull requests based on the contents of the event payload. WARNING: The ``pull_request_target`` event is granted read/write repository token and can access secrets, even when it is triggered from a fork. Although the workflow runs in the context of the base of the pull request, you should make sure that you do not check out, build, or run untrusted code from the pull request with this event. Additionally, any caches share the same scope as the base branch, and to help prevent cache poisoning, you should not save the cache if there is a possibility that the cache contents were altered.
        :param push: (experimental) Runs your workflow when someone pushes to a repository branch, which triggers the push event.
        :param registry_package: (experimental) Runs your workflow anytime a package is published or updated.
        :param release: (experimental) Runs your workflow anytime the release event occurs.
        :param repository_dispatch: (experimental) You can use the GitHub API to trigger a webhook event called repository_dispatch when you want to trigger a workflow for activity that happens outside of GitHub.
        :param schedule: (experimental) You can schedule a workflow to run at specific UTC times using POSIX cron syntax. Scheduled workflows run on the latest commit on the default or base branch. The shortest interval you can run scheduled workflows is once every 5 minutes.
        :param status: (experimental) Runs your workflow anytime the status of a Git commit changes, which triggers the status event.
        :param watch: (experimental) Runs your workflow anytime the watch event occurs.
        :param workflow_dispatch: (experimental) You can configure custom-defined input properties, default input values, and required inputs for the event directly in your workflow. When the workflow runs, you can access the input values in the github.event.inputs context.
        :param workflow_run: (experimental) This event occurs when a workflow run is requested or completed, and allows you to execute a workflow based on the finished result of another workflow. A workflow run is triggered regardless of the result of the previous workflow.

        :see: https://docs.github.com/en/actions/reference/events-that-trigger-workflows
        :stability: experimental
        '''
        if isinstance(check_run, dict):
            check_run = CheckRunOptions(**check_run)
        if isinstance(check_suite, dict):
            check_suite = CheckSuiteOptions(**check_suite)
        if isinstance(create, dict):
            create = CreateOptions(**create)
        if isinstance(delete, dict):
            delete = DeleteOptions(**delete)
        if isinstance(deployment, dict):
            deployment = DeploymentOptions(**deployment)
        if isinstance(deployment_status, dict):
            deployment_status = DeploymentStatusOptions(**deployment_status)
        if isinstance(fork, dict):
            fork = ForkOptions(**fork)
        if isinstance(gollum, dict):
            gollum = GollumOptions(**gollum)
        if isinstance(issue_comment, dict):
            issue_comment = IssueCommentOptions(**issue_comment)
        if isinstance(issues, dict):
            issues = IssuesOptions(**issues)
        if isinstance(label, dict):
            label = LabelOptions(**label)
        if isinstance(milestone, dict):
            milestone = MilestoneOptions(**milestone)
        if isinstance(page_build, dict):
            page_build = PageBuildOptions(**page_build)
        if isinstance(project, dict):
            project = ProjectOptions(**project)
        if isinstance(project_card, dict):
            project_card = ProjectCardOptions(**project_card)
        if isinstance(project_column, dict):
            project_column = ProjectColumnOptions(**project_column)
        if isinstance(public, dict):
            public = PublicOptions(**public)
        if isinstance(pull_request, dict):
            pull_request = PullRequestOptions(**pull_request)
        if isinstance(pull_request_review, dict):
            pull_request_review = PullRequestReviewOptions(**pull_request_review)
        if isinstance(pull_request_review_comment, dict):
            pull_request_review_comment = PullRequestReviewCommentOptions(**pull_request_review_comment)
        if isinstance(pull_request_target, dict):
            pull_request_target = PullRequestTargetOptions(**pull_request_target)
        if isinstance(push, dict):
            push = PushOptions(**push)
        if isinstance(registry_package, dict):
            registry_package = RegistryPackageOptions(**registry_package)
        if isinstance(release, dict):
            release = ReleaseOptions(**release)
        if isinstance(repository_dispatch, dict):
            repository_dispatch = RepositoryDispatchOptions(**repository_dispatch)
        if isinstance(status, dict):
            status = StatusOptions(**status)
        if isinstance(watch, dict):
            watch = WatchOptions(**watch)
        if isinstance(workflow_dispatch, dict):
            workflow_dispatch = WorkflowDispatchOptions(**workflow_dispatch)
        if isinstance(workflow_run, dict):
            workflow_run = WorkflowRunOptions(**workflow_run)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5fb7011512828a8da2d4a938282a5e203767d8a048f65567f37de300f75e13)
            check_type(argname="argument check_run", value=check_run, expected_type=type_hints["check_run"])
            check_type(argname="argument check_suite", value=check_suite, expected_type=type_hints["check_suite"])
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument deployment_status", value=deployment_status, expected_type=type_hints["deployment_status"])
            check_type(argname="argument fork", value=fork, expected_type=type_hints["fork"])
            check_type(argname="argument gollum", value=gollum, expected_type=type_hints["gollum"])
            check_type(argname="argument issue_comment", value=issue_comment, expected_type=type_hints["issue_comment"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument milestone", value=milestone, expected_type=type_hints["milestone"])
            check_type(argname="argument page_build", value=page_build, expected_type=type_hints["page_build"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument project_card", value=project_card, expected_type=type_hints["project_card"])
            check_type(argname="argument project_column", value=project_column, expected_type=type_hints["project_column"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument pull_request_review", value=pull_request_review, expected_type=type_hints["pull_request_review"])
            check_type(argname="argument pull_request_review_comment", value=pull_request_review_comment, expected_type=type_hints["pull_request_review_comment"])
            check_type(argname="argument pull_request_target", value=pull_request_target, expected_type=type_hints["pull_request_target"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
            check_type(argname="argument registry_package", value=registry_package, expected_type=type_hints["registry_package"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument repository_dispatch", value=repository_dispatch, expected_type=type_hints["repository_dispatch"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument watch", value=watch, expected_type=type_hints["watch"])
            check_type(argname="argument workflow_dispatch", value=workflow_dispatch, expected_type=type_hints["workflow_dispatch"])
            check_type(argname="argument workflow_run", value=workflow_run, expected_type=type_hints["workflow_run"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if check_run is not None:
            self._values["check_run"] = check_run
        if check_suite is not None:
            self._values["check_suite"] = check_suite
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if deployment is not None:
            self._values["deployment"] = deployment
        if deployment_status is not None:
            self._values["deployment_status"] = deployment_status
        if fork is not None:
            self._values["fork"] = fork
        if gollum is not None:
            self._values["gollum"] = gollum
        if issue_comment is not None:
            self._values["issue_comment"] = issue_comment
        if issues is not None:
            self._values["issues"] = issues
        if label is not None:
            self._values["label"] = label
        if milestone is not None:
            self._values["milestone"] = milestone
        if page_build is not None:
            self._values["page_build"] = page_build
        if project is not None:
            self._values["project"] = project
        if project_card is not None:
            self._values["project_card"] = project_card
        if project_column is not None:
            self._values["project_column"] = project_column
        if public is not None:
            self._values["public"] = public
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if pull_request_review is not None:
            self._values["pull_request_review"] = pull_request_review
        if pull_request_review_comment is not None:
            self._values["pull_request_review_comment"] = pull_request_review_comment
        if pull_request_target is not None:
            self._values["pull_request_target"] = pull_request_target
        if push is not None:
            self._values["push"] = push
        if registry_package is not None:
            self._values["registry_package"] = registry_package
        if release is not None:
            self._values["release"] = release
        if repository_dispatch is not None:
            self._values["repository_dispatch"] = repository_dispatch
        if schedule is not None:
            self._values["schedule"] = schedule
        if status is not None:
            self._values["status"] = status
        if watch is not None:
            self._values["watch"] = watch
        if workflow_dispatch is not None:
            self._values["workflow_dispatch"] = workflow_dispatch
        if workflow_run is not None:
            self._values["workflow_run"] = workflow_run

    @builtins.property
    def check_run(self) -> typing.Optional[CheckRunOptions]:
        '''(experimental) Runs your workflow anytime the check_run event occurs.

        :stability: experimental
        '''
        result = self._values.get("check_run")
        return typing.cast(typing.Optional[CheckRunOptions], result)

    @builtins.property
    def check_suite(self) -> typing.Optional[CheckSuiteOptions]:
        '''(experimental) Runs your workflow anytime the check_suite event occurs.

        :stability: experimental
        '''
        result = self._values.get("check_suite")
        return typing.cast(typing.Optional[CheckSuiteOptions], result)

    @builtins.property
    def create(self) -> typing.Optional[CreateOptions]:
        '''(experimental) Runs your workflow anytime someone creates a branch or tag, which triggers the create event.

        :stability: experimental
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[CreateOptions], result)

    @builtins.property
    def delete(self) -> typing.Optional[DeleteOptions]:
        '''(experimental) Runs your workflow anytime someone deletes a branch or tag, which triggers the delete event.

        :stability: experimental
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[DeleteOptions], result)

    @builtins.property
    def deployment(self) -> typing.Optional[DeploymentOptions]:
        '''(experimental) Runs your workflow anytime someone creates a deployment, which triggers the deployment event.

        Deployments created with a commit SHA may not have
        a Git ref.

        :stability: experimental
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional[DeploymentOptions], result)

    @builtins.property
    def deployment_status(self) -> typing.Optional[DeploymentStatusOptions]:
        '''(experimental) Runs your workflow anytime a third party provides a deployment status, which triggers the deployment_status event.

        Deployments created with a
        commit SHA may not have a Git ref.

        :stability: experimental
        '''
        result = self._values.get("deployment_status")
        return typing.cast(typing.Optional[DeploymentStatusOptions], result)

    @builtins.property
    def fork(self) -> typing.Optional[ForkOptions]:
        '''(experimental) Runs your workflow anytime when someone forks a repository, which triggers the fork event.

        :stability: experimental
        '''
        result = self._values.get("fork")
        return typing.cast(typing.Optional[ForkOptions], result)

    @builtins.property
    def gollum(self) -> typing.Optional[GollumOptions]:
        '''(experimental) Runs your workflow when someone creates or updates a Wiki page, which triggers the gollum event.

        :stability: experimental
        '''
        result = self._values.get("gollum")
        return typing.cast(typing.Optional[GollumOptions], result)

    @builtins.property
    def issue_comment(self) -> typing.Optional[IssueCommentOptions]:
        '''(experimental) Runs your workflow anytime the issue_comment event occurs.

        :stability: experimental
        '''
        result = self._values.get("issue_comment")
        return typing.cast(typing.Optional[IssueCommentOptions], result)

    @builtins.property
    def issues(self) -> typing.Optional[IssuesOptions]:
        '''(experimental) Runs your workflow anytime the issues event occurs.

        :stability: experimental
        '''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[IssuesOptions], result)

    @builtins.property
    def label(self) -> typing.Optional[LabelOptions]:
        '''(experimental) Runs your workflow anytime the label event occurs.

        :stability: experimental
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[LabelOptions], result)

    @builtins.property
    def milestone(self) -> typing.Optional[MilestoneOptions]:
        '''(experimental) Runs your workflow anytime the milestone event occurs.

        :stability: experimental
        '''
        result = self._values.get("milestone")
        return typing.cast(typing.Optional[MilestoneOptions], result)

    @builtins.property
    def page_build(self) -> typing.Optional[PageBuildOptions]:
        '''(experimental) Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch, which triggers the page_build event.

        :stability: experimental
        '''
        result = self._values.get("page_build")
        return typing.cast(typing.Optional[PageBuildOptions], result)

    @builtins.property
    def project(self) -> typing.Optional[ProjectOptions]:
        '''(experimental) Runs your workflow anytime the project event occurs.

        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[ProjectOptions], result)

    @builtins.property
    def project_card(self) -> typing.Optional[ProjectCardOptions]:
        '''(experimental) Runs your workflow anytime the project_card event occurs.

        :stability: experimental
        '''
        result = self._values.get("project_card")
        return typing.cast(typing.Optional[ProjectCardOptions], result)

    @builtins.property
    def project_column(self) -> typing.Optional[ProjectColumnOptions]:
        '''(experimental) Runs your workflow anytime the project_column event occurs.

        :stability: experimental
        '''
        result = self._values.get("project_column")
        return typing.cast(typing.Optional[ProjectColumnOptions], result)

    @builtins.property
    def public(self) -> typing.Optional[PublicOptions]:
        '''(experimental) Runs your workflow anytime someone makes a private repository public, which triggers the public event.

        :stability: experimental
        '''
        result = self._values.get("public")
        return typing.cast(typing.Optional[PublicOptions], result)

    @builtins.property
    def pull_request(self) -> typing.Optional[PullRequestOptions]:
        '''(experimental) Runs your workflow anytime the pull_request event occurs.

        :stability: experimental
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional[PullRequestOptions], result)

    @builtins.property
    def pull_request_review(self) -> typing.Optional[PullRequestReviewOptions]:
        '''(experimental) Runs your workflow anytime the pull_request_review event occurs.

        :stability: experimental
        '''
        result = self._values.get("pull_request_review")
        return typing.cast(typing.Optional[PullRequestReviewOptions], result)

    @builtins.property
    def pull_request_review_comment(
        self,
    ) -> typing.Optional[PullRequestReviewCommentOptions]:
        '''(experimental) Runs your workflow anytime a comment on a pull request's unified diff is modified, which triggers the pull_request_review_comment event.

        :stability: experimental
        '''
        result = self._values.get("pull_request_review_comment")
        return typing.cast(typing.Optional[PullRequestReviewCommentOptions], result)

    @builtins.property
    def pull_request_target(self) -> typing.Optional["PullRequestTargetOptions"]:
        '''(experimental) This event runs in the context of the base of the pull request, rather than in the merge commit as the pull_request event does.

        This prevents
        executing unsafe workflow code from the head of the pull request that
        could alter your repository or steal any secrets you use in your workflow.
        This event allows you to do things like create workflows that label and
        comment on pull requests based on the contents of the event payload.

        WARNING: The ``pull_request_target`` event is granted read/write repository
        token and can access secrets, even when it is triggered from a fork.
        Although the workflow runs in the context of the base of the pull request,
        you should make sure that you do not check out, build, or run untrusted
        code from the pull request with this event. Additionally, any caches
        share the same scope as the base branch, and to help prevent cache
        poisoning, you should not save the cache if there is a possibility that
        the cache contents were altered.

        :see: https://securitylab.github.com/research/github-actions-preventing-pwn-requests
        :stability: experimental
        '''
        result = self._values.get("pull_request_target")
        return typing.cast(typing.Optional["PullRequestTargetOptions"], result)

    @builtins.property
    def push(self) -> typing.Optional[PushOptions]:
        '''(experimental) Runs your workflow when someone pushes to a repository branch, which triggers the push event.

        :stability: experimental
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional[PushOptions], result)

    @builtins.property
    def registry_package(self) -> typing.Optional[RegistryPackageOptions]:
        '''(experimental) Runs your workflow anytime a package is published or updated.

        :stability: experimental
        '''
        result = self._values.get("registry_package")
        return typing.cast(typing.Optional[RegistryPackageOptions], result)

    @builtins.property
    def release(self) -> typing.Optional[ReleaseOptions]:
        '''(experimental) Runs your workflow anytime the release event occurs.

        :stability: experimental
        '''
        result = self._values.get("release")
        return typing.cast(typing.Optional[ReleaseOptions], result)

    @builtins.property
    def repository_dispatch(self) -> typing.Optional[RepositoryDispatchOptions]:
        '''(experimental) You can use the GitHub API to trigger a webhook event called repository_dispatch when you want to trigger a workflow for activity that happens outside of GitHub.

        :stability: experimental
        '''
        result = self._values.get("repository_dispatch")
        return typing.cast(typing.Optional[RepositoryDispatchOptions], result)

    @builtins.property
    def schedule(self) -> typing.Optional[typing.List[CronScheduleOptions]]:
        '''(experimental) You can schedule a workflow to run at specific UTC times using POSIX cron syntax.

        Scheduled workflows run on the latest commit on the default or
        base branch. The shortest interval you can run scheduled workflows is
        once every 5 minutes.

        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.List[CronScheduleOptions]], result)

    @builtins.property
    def status(self) -> typing.Optional[StatusOptions]:
        '''(experimental) Runs your workflow anytime the status of a Git commit changes, which triggers the status event.

        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[StatusOptions], result)

    @builtins.property
    def watch(self) -> typing.Optional[WatchOptions]:
        '''(experimental) Runs your workflow anytime the watch event occurs.

        :stability: experimental
        '''
        result = self._values.get("watch")
        return typing.cast(typing.Optional[WatchOptions], result)

    @builtins.property
    def workflow_dispatch(self) -> typing.Optional[WorkflowDispatchOptions]:
        '''(experimental) You can configure custom-defined input properties, default input values, and required inputs for the event directly in your workflow.

        When the
        workflow runs, you can access the input values in the github.event.inputs
        context.

        :stability: experimental
        '''
        result = self._values.get("workflow_dispatch")
        return typing.cast(typing.Optional[WorkflowDispatchOptions], result)

    @builtins.property
    def workflow_run(self) -> typing.Optional[WorkflowRunOptions]:
        '''(experimental) This event occurs when a workflow run is requested or completed, and allows you to execute a workflow based on the finished result of another workflow.

        A workflow run is triggered regardless of the result of the
        previous workflow.

        :stability: experimental
        '''
        result = self._values.get("workflow_run")
        return typing.cast(typing.Optional[WorkflowRunOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTriggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class YamlFile(metaclass=jsii.JSIIMeta, jsii_type="cdk-pipelines-github.YamlFile"):
    '''(experimental) Represents a Yaml File.

    :stability: experimental
    '''

    def __init__(self, file_path: builtins.str, *, obj: typing.Any = None) -> None:
        '''
        :param file_path: -
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Default: {} an empty object

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46ecdcecd3876bbfdf80e4a680d5dc6c1822a357f30c96c541b143795f6ea4a)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = YamlFileOptions(obj=obj)

        jsii.create(self.__class__, self, [file_path, options])

    @jsii.member(jsii_name="patch")
    def patch(self, *patches: JsonPatch) -> None:
        '''(experimental) Applies an RFC 6902 JSON-patch to the synthesized object file. See https://datatracker.ietf.org/doc/html/rfc6902 for more information.

        For example, with the following yaml file Example::

           name: deploy
           on:
             push:
               branches:
                 - main
             workflow_dispatch: {}
           ...

        modified in the following way::

           # pipeline: GitHubWorkflow

           pipeline.workflow_file.patch(JsonPatch.add("/on/workflow_call", "{}"))
           pipeline.workflow_file.patch(JsonPatch.remove("/on/workflow_dispatch"))

        would result in the following yaml file::

           name: deploy
           on:
             push:
               branches:
                 - main
             workflow_call: {}
           ...

        :param patches: - The patch operations to apply.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da9b34eab7c2d80e24680051016fe375948e30adfb83511801fa66ad9493729)
            check_type(argname="argument patches", value=patches, expected_type=typing.Tuple[type_hints["patches"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "patch", [*patches]))

    @jsii.member(jsii_name="toYaml")
    def to_yaml(self) -> builtins.str:
        '''(experimental) Returns the patched yaml file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toYaml", []))

    @jsii.member(jsii_name="update")
    def update(self, obj: typing.Any) -> None:
        '''(experimental) Update the output object.

        :param obj: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a5e3b2d78d85076e947fd6efbffa9ddc155038612592c8fe6da18a27753823)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast(None, jsii.invoke(self, "update", [obj]))

    @jsii.member(jsii_name="writeFile")
    def write_file(self) -> None:
        '''(experimental) Write the patched yaml file to the specified location.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "writeFile", []))

    @builtins.property
    @jsii.member(jsii_name="commentAtTop")
    def comment_at_top(self) -> typing.Optional[builtins.str]:
        '''(experimental) A comment to be added to the top of the YAML file.

        Can be multiline. All non-empty line are pefixed with '# '. Empty lines are kept, but not commented.

        For example::

           # pipeline: GitHubWorkflow

           pipeline.workflow_file.comment_at_top = """AUTOGENERATED FILE, DO NOT EDIT!
           See ReadMe.md
           """

        Results in YAML::

           # AUTOGENERATED FILE, DO NOT EDIT!
           # See ReadMe.md

           name: deploy
           ...

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentAtTop"))

    @comment_at_top.setter
    def comment_at_top(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d492537bd16470957036b07a40a761d26ba00320315326f2e45084798f6594c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commentAtTop", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="cdk-pipelines-github.YamlFileOptions",
    jsii_struct_bases=[],
    name_mapping={"obj": "obj"},
)
class YamlFileOptions:
    def __init__(self, *, obj: typing.Any = None) -> None:
        '''(experimental) Options for ``YamlFile``.

        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Default: {} an empty object

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c376706244514db9e5ebda7df2cfb058056f86efc5baf6e4d2e6444f41ca85c)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if obj is not None:
            self._values["obj"] = obj

    @builtins.property
    def obj(self) -> typing.Any:
        '''(experimental) The object that will be serialized.

        You can modify the object's contents
        before synthesis.

        :default: {} an empty object

        :stability: experimental
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YamlFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.AddGitHubStageOptions",
    jsii_struct_bases=[_aws_cdk_pipelines_ceddda9d.AddStageOpts, GitHubCommonProps],
    name_mapping={
        "post": "post",
        "pre": "pre",
        "stack_steps": "stackSteps",
        "git_hub_environment": "gitHubEnvironment",
        "job_settings": "jobSettings",
        "stack_capabilities": "stackCapabilities",
    },
)
class AddGitHubStageOptions(
    _aws_cdk_pipelines_ceddda9d.AddStageOpts,
    GitHubCommonProps,
):
    def __init__(
        self,
        *,
        post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
        git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
        job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
    ) -> None:
        '''(experimental) Options to pass to ``addStageWithGitHubOpts``.

        :param post: Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: Instructions for stack level steps. Default: - No additional instructions
        :param git_hub_environment: (experimental) Run the stage in a specific GitHub Environment. If specified, any protection rules configured for the environment must pass before the job is set to a runner. For example, if the environment has a manual approval rule configured, then the workflow will wait for the approval before sending the job to the runner. Running a workflow that references an environment that does not exist will create an environment with the referenced name. Default: - no GitHub environment
        :param job_settings: (experimental) Job level settings that will be applied to all jobs in the stage. Currently the only valid setting is 'if'.
        :param stack_capabilities: (experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack. If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities`` error. Default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        if isinstance(git_hub_environment, dict):
            git_hub_environment = GitHubEnvironment(**git_hub_environment)
        if isinstance(job_settings, dict):
            job_settings = JobSettings(**job_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0f7f1a194dea5451b9bdd80028be3e5e499b46f0ad8737ce1a1b3b6344b8a6)
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
            check_type(argname="argument pre", value=pre, expected_type=type_hints["pre"])
            check_type(argname="argument stack_steps", value=stack_steps, expected_type=type_hints["stack_steps"])
            check_type(argname="argument git_hub_environment", value=git_hub_environment, expected_type=type_hints["git_hub_environment"])
            check_type(argname="argument job_settings", value=job_settings, expected_type=type_hints["job_settings"])
            check_type(argname="argument stack_capabilities", value=stack_capabilities, expected_type=type_hints["stack_capabilities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post is not None:
            self._values["post"] = post
        if pre is not None:
            self._values["pre"] = pre
        if stack_steps is not None:
            self._values["stack_steps"] = stack_steps
        if git_hub_environment is not None:
            self._values["git_hub_environment"] = git_hub_environment
        if job_settings is not None:
            self._values["job_settings"] = job_settings
        if stack_capabilities is not None:
            self._values["stack_capabilities"] = stack_capabilities

    @builtins.property
    def post(self) -> typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.Step]]:
        '''Additional steps to run after all of the stacks in the stage.

        :default: - No additional steps
        '''
        result = self._values.get("post")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.Step]], result)

    @builtins.property
    def pre(self) -> typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.Step]]:
        '''Additional steps to run before any of the stacks in the stage.

        :default: - No additional steps
        '''
        result = self._values.get("pre")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.Step]], result)

    @builtins.property
    def stack_steps(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.StackSteps]]:
        '''Instructions for stack level steps.

        :default: - No additional instructions
        '''
        result = self._values.get("stack_steps")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_pipelines_ceddda9d.StackSteps]], result)

    @builtins.property
    def git_hub_environment(self) -> typing.Optional[GitHubEnvironment]:
        '''(experimental) Run the stage in a specific GitHub Environment.

        If specified,
        any protection rules configured for the environment must pass
        before the job is set to a runner. For example, if the environment
        has a manual approval rule configured, then the workflow will
        wait for the approval before sending the job to the runner.

        Running a workflow that references an environment that does not
        exist will create an environment with the referenced name.

        :default: - no GitHub environment

        :see: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
        :stability: experimental
        '''
        result = self._values.get("git_hub_environment")
        return typing.cast(typing.Optional[GitHubEnvironment], result)

    @builtins.property
    def job_settings(self) -> typing.Optional[JobSettings]:
        '''(experimental) Job level settings that will be applied to all jobs in the stage.

        Currently the only valid setting is 'if'.

        :stability: experimental
        '''
        result = self._values.get("job_settings")
        return typing.cast(typing.Optional[JobSettings], result)

    @builtins.property
    def stack_capabilities(self) -> typing.Optional[typing.List[StackCapabilities]]:
        '''(experimental) In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack.

        If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities``
        error.

        :default: ['CAPABILITY_IAM']

        :stability: experimental
        '''
        result = self._values.get("stack_capabilities")
        return typing.cast(typing.Optional[typing.List[StackCapabilities]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddGitHubStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PullRequestTargetOptions",
    jsii_struct_bases=[PushOptions],
    name_mapping={
        "branches": "branches",
        "paths": "paths",
        "tags": "tags",
        "types": "types",
    },
)
class PullRequestTargetOptions(PushOptions):
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Pull request target options.

        :param branches: (experimental) When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: (experimental) When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: (experimental) When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param types: (experimental) Which activity types to trigger on.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31c46895f60384d6ff3bd631f2e9c7ed5422806564f06c976cab0fd303b12ae)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Which activity types to trigger on.

        :stability: experimental
        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddGitHubStageOptions",
    "AwsCredentials",
    "AwsCredentialsProvider",
    "AwsCredentialsSecrets",
    "CheckRunOptions",
    "CheckSuiteOptions",
    "ConcurrencyOptions",
    "ContainerCredentials",
    "ContainerOptions",
    "CreateOptions",
    "CronScheduleOptions",
    "DeleteOptions",
    "DeploymentOptions",
    "DeploymentStatusOptions",
    "DockerAssetJobSettings",
    "DockerCredential",
    "DockerHubCredentialSecrets",
    "ExternalDockerCredentialSecrets",
    "ForkOptions",
    "GitHubActionRole",
    "GitHubActionRoleProps",
    "GitHubActionStep",
    "GitHubActionStepProps",
    "GitHubCommonProps",
    "GitHubEnvironment",
    "GitHubSecretsProviderProps",
    "GitHubStage",
    "GitHubStageProps",
    "GitHubWave",
    "GitHubWorkflow",
    "GitHubWorkflowProps",
    "GollumOptions",
    "IssueCommentOptions",
    "IssuesOptions",
    "Job",
    "JobDefaults",
    "JobMatrix",
    "JobPermission",
    "JobPermissions",
    "JobSettings",
    "JobStep",
    "JobStepOutput",
    "JobStrategy",
    "JsonPatch",
    "LabelOptions",
    "MilestoneOptions",
    "OpenIdConnectProviderProps",
    "PageBuildOptions",
    "ProjectCardOptions",
    "ProjectColumnOptions",
    "ProjectOptions",
    "PublicOptions",
    "PullRequestOptions",
    "PullRequestReviewCommentOptions",
    "PullRequestReviewOptions",
    "PullRequestTargetOptions",
    "PushOptions",
    "RegistryPackageOptions",
    "ReleaseOptions",
    "RepositoryDispatchOptions",
    "RunSettings",
    "Runner",
    "StackCapabilities",
    "StatusOptions",
    "WatchOptions",
    "WorkflowDispatchOptions",
    "WorkflowRunOptions",
    "WorkflowTriggers",
    "YamlFile",
    "YamlFileOptions",
]

publication.publish()

def _typecheckingstub__c34f5a85d5e49af165e757b316fc4eadde29000f3bae7a0c0ad92162ad1f7859(
    region: builtins.str,
    assume_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ab8e0acc5af4b62bacc9d5ad666cdeedd569af7e148668725f140b7bc483de(
    *,
    access_key_id: typing.Optional[builtins.str] = None,
    secret_access_key: typing.Optional[builtins.str] = None,
    session_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6373a6591e7a83beaee7f715a317bd90eb8e115426fbe79d84ec07038ffe5e4b(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2329fd786490f9db53605848242542e725f90583102b8a55f00cbf365b3702e3(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb410d6a8096fafa9cac50ed904bfb12e76ade4f85e8287349d0aeb8489705b(
    *,
    group: builtins.str,
    cancel_in_progress: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d9d9d796eb12703f23018e319ec5349afa13b16aeb0ebd4f7b89db2d314fbb(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95391ae8e55d8dc0bfb3183f3e3dc187d92e429daf90843549a090f978a7b2bf(
    *,
    image: builtins.str,
    credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f54935941db587485c7979514ebfed4aeb58008d8e75a449b9f4b2a9cd9231(
    *,
    cron: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e52b1650e15393651aa94bf8e685a0018d4c955418f5ce005b28568dd5302d(
    *,
    permissions: typing.Optional[typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    setup_steps: typing.Optional[typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101864b569747688b6b3a9b72cb693fe435eec9bb1e6b51e0026ca466648f2c1(
    registry: builtins.str,
    *,
    password_key: builtins.str,
    username_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d0c29c037615007983ee20857df5048cbe8494f68f656f5b4af70afa444b2a(
    registry: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09113ce192ad66711ff498566dd94325741d6b520d4811f33cf1c2d279ad6779(
    *,
    personal_access_token_key: typing.Optional[builtins.str] = None,
    username_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0f223a2472060f1f721c38920d320f88580c9de023d07ad9ceacd1ab2bd973(
    *,
    password_key: builtins.str,
    username_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7efaa19c11ed9057d237005627f473d64f50f5e1ab1712be044e3d1bdd7716e4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    repos: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_name: typing.Optional[builtins.str] = None,
    subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3470db1a98b372a508d6fcbbe10f97f439b9fc7404d428e0944f0bc7a4014485(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fb897842c219b21980c6f5d46fcab4f267529a7fde8c4ee40880539a329537(
    *,
    provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    repos: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_name: typing.Optional[builtins.str] = None,
    subject_claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1176a118ca36bc762181a4882e12e7b069118ee5882233a232892bdc923c8209(
    id: builtins.str,
    *,
    job_steps: typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]],
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    github_environment: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb9323e1a70b92d220365668e8d719f774e191339812c47f7e57cd238de1678(
    *,
    job_steps: typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]],
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    github_environment: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6611b18289416c64b5e869501493ceef81f660dd80fa6f0677574ec6b5504d6c(
    *,
    git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fe132afc11f8f0a945ac9eeea27c033ce30202ce31b3058b8be89378efddf9(
    *,
    name: builtins.str,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5502781441b1b7f54eb889be996f05f0ccaf271d620ba0e9cc14739f9b2b656(
    *,
    access_key_id: builtins.str,
    secret_access_key: builtins.str,
    session_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ded55f6f78e09081d268fb0ac64648e138db13b9f4acaadd50868b68501f46(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d3dbc0d6268c9ba2a6b3d91eaaf33aa275000dba07e4f98ce438ef6f8cd5a5(
    *,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef499badf71d8733c69ad09c0c24f5703e7108be9c31a0b1fff34b312651b42(
    id: builtins.str,
    pipeline: GitHubWorkflow,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43c8e0765168b11f6277a89cfc0de81ab7a360ad3bca0ae6f0216f148accdbf(
    stage: _aws_cdk_ceddda9d.Stage,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa2718a68b226b4c63caab144cfb3f546368347ce90eed7c4f118e33bc04cc4(
    stage: _aws_cdk_ceddda9d.Stage,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e000cfcb875b99dba5697464b35c7b7052d0af71745445799f596ff96147a8c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_credentials: typing.Optional[typing.Union[AwsCredentialsSecrets, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_creds: typing.Optional[AwsCredentialsProvider] = None,
    build_container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cdk_cli_version: typing.Optional[builtins.str] = None,
    concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_asset_job_settings: typing.Optional[typing.Union[DockerAssetJobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
    git_hub_action_role_arn: typing.Optional[builtins.str] = None,
    job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_build_steps: typing.Optional[typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_synthed: typing.Optional[builtins.bool] = None,
    publish_assets_auth_region: typing.Optional[builtins.str] = None,
    runner: typing.Optional[Runner] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_path: typing.Optional[builtins.str] = None,
    workflow_triggers: typing.Optional[typing.Union[WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
    synth: _aws_cdk_pipelines_ceddda9d.IFileSetProducer,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eaf88ea4f8a8d2fc4873b4c2c60f9899faf9476b95495ce23f7850e90ec317e(
    id: builtins.str,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7a4aaa2de9ee17c586fe08c0478d636f444f6bd2752a8271707d3e99f00736(
    stage: _aws_cdk_ceddda9d.Stage,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14874e98f77810a63a3eb419752e3f2e023edb5fb94993515b42884eaa1d7087(
    id: builtins.str,
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54d7c114bd36382002f3ddd507359655630c42e5b211e5c46e68de87555cf35(
    *,
    synth: _aws_cdk_pipelines_ceddda9d.IFileSetProducer,
    aws_credentials: typing.Optional[typing.Union[AwsCredentialsSecrets, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_creds: typing.Optional[AwsCredentialsProvider] = None,
    build_container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cdk_cli_version: typing.Optional[builtins.str] = None,
    concurrency: typing.Optional[typing.Union[ConcurrencyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_asset_job_settings: typing.Optional[typing.Union[DockerAssetJobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
    git_hub_action_role_arn: typing.Optional[builtins.str] = None,
    job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_build_steps: typing.Optional[typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_synthed: typing.Optional[builtins.bool] = None,
    publish_assets_auth_region: typing.Optional[builtins.str] = None,
    runner: typing.Optional[Runner] = None,
    workflow_name: typing.Optional[builtins.str] = None,
    workflow_path: typing.Optional[builtins.str] = None,
    workflow_triggers: typing.Optional[typing.Union[WorkflowTriggers, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8f5cb2188fc6ddf4cf79f0ff67bbc59e9abc16f167214dfa10723f80b51965(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8824add0f693226a3bfa1fec2f9e7ffaf9ef3b2d98f2a3df534226802135fd7f(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d74634ced8efa05c46052c781206dcfcf038fee236dccfe2a9a1dbac8a09aec(
    *,
    permissions: typing.Union[JobPermissions, typing.Dict[builtins.str, typing.Any]],
    runs_on: typing.Union[builtins.str, typing.Sequence[builtins.str]],
    steps: typing.Sequence[typing.Union[JobStep, typing.Dict[builtins.str, typing.Any]]],
    concurrency: typing.Any = None,
    container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    continue_on_error: typing.Optional[builtins.bool] = None,
    defaults: typing.Optional[typing.Union[JobDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Any = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    strategy: typing.Optional[typing.Union[JobStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32147cd5f8d7d9ef77d5a96c7435d9911055f7183cb8ac9d412558c3e2fea8e(
    *,
    run: typing.Optional[typing.Union[RunSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839885d4d07812573dc2f6bbc6039fda3a4c68bd72a52dfb040eb6d9db46b2a5(
    *,
    domain: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
    include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebccc396832c41c1f28ee27122716bee7c27553b4a406cb7b755d8c7280e398(
    *,
    actions: typing.Optional[JobPermission] = None,
    checks: typing.Optional[JobPermission] = None,
    contents: typing.Optional[JobPermission] = None,
    deployments: typing.Optional[JobPermission] = None,
    discussions: typing.Optional[JobPermission] = None,
    id_token: typing.Optional[JobPermission] = None,
    issues: typing.Optional[JobPermission] = None,
    packages: typing.Optional[JobPermission] = None,
    pull_requests: typing.Optional[JobPermission] = None,
    repository_projects: typing.Optional[JobPermission] = None,
    security_events: typing.Optional[JobPermission] = None,
    statuses: typing.Optional[JobPermission] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d93c13f4ea5805aa31e5daa7a5204c943a1a44020ede8f01e81966e3f1725e(
    *,
    if_: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e761fdc1044ff886640a8e5d64fa3d3e1a780efcecbbd275e4c31055101433(
    *,
    continue_on_error: typing.Optional[builtins.bool] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    if_: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    run: typing.Optional[builtins.str] = None,
    timeout_minutes: typing.Optional[jsii.Number] = None,
    uses: typing.Optional[builtins.str] = None,
    with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9232daf74d562c79cb6fce855867d01e489d3946367e284bc9185b7c8a757a(
    *,
    output_name: builtins.str,
    step_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80d0bb466d3a822db3284ee7f61b9d956788379459cbf8a8ab4be116d4b3ea4(
    *,
    fail_fast: typing.Optional[builtins.bool] = None,
    matrix: typing.Optional[typing.Union[JobMatrix, typing.Dict[builtins.str, typing.Any]]] = None,
    max_parallel: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b7788c908a37168f0d99a50070ea29369813aa2c07c46417c395a9c2d65125(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e02d9f326f3f13fe6e498e98316a665a729d42b3a34470f5b450fd2c53a505(
    document: typing.Any,
    *ops: JsonPatch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd8d0d82351b216410123e49c91d33dbeae270ed2c75d19ce5ac542be62c688(
    from_: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4242ceab4f40bfa6a19a3aca0a6642e91fa90516642ead4c19ea3174012e02d6(
    from_: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e69cfe81d249b73a6eb12bc222bd94d3e5f15a49220ac470d6348bc5620fa5(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1101cca45fa8bcb4442ca950cf671ef5a494621f4c0ae65013e76127d54372(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b585eb3f9d8bd6ac3b3ececc9183622d96ed862967465fd85524abfd1a7509(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a31017e70cb6b10d1c7f22bd885378e69fd7cf50494f506d84c501f5b15608(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e2b08dda1c24d3f5b1432e6b6612b9516d77077a30b82d589b6aff3d76ec56(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8201325ae4a8c45dcbe4c7d868e0b03bc0213efc4ea619c852046ba5517e5fc5(
    *,
    git_hub_action_role_arn: builtins.str,
    role_session_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc685756612eea88a78ef100a9ab03ecac50481a14fccb75b9aefa7f670722f(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e9baa3bb445be4a5c414eddefc47be7856a0fcb206263592f0ffc303384949(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6773683d69a971c7c5c0742f143d5e61a34617d7d5c707933904275488cca3af(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678b381f2938a5a7e53c0cb4d2361ddb2a4e20a028116d03028bc086bd4ea7fa(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f130898e52637b9538ce0e89004dbd887b836d2df1e0b86639abb3e0d2267ee1(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1689dcb0d428eac4995ce80d3cc1c9424174c9f1502514694753d97a4e562870(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e66fc18901adbbc7c16879f5085ed2ddc0c914ecf282679698f5e0189a2768(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6fea0503ac1ec6392b103a3f32726778118e585380cb62e87de177f6d324ad(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b515fd62c1ee49f5eeae11c884f13e8faeef5c2f5baa85c5dbc0a361a205b2(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c431e7bcb272169575a643e18f3e1d362a2bf63f482f9d3d3a1af5911bb915d5(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665e1d5fb187329ece0a9f5e476acf29e23d80806e3ca2852036ca53539ac7da(
    *,
    shell: typing.Optional[builtins.str] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7aa98e7950895be604e27ddee038769e89e361d47f176b549fa2529a847f00(
    labels: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54a4ec9b0e947b929cf7238ed16d4855d8bf09fc3601cd993c7f43b97de2d73(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84af6712d2185aed478f3af7f480af3eb94e4c399885ab7de3a691abe0bfa85(
    *,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5fb7011512828a8da2d4a938282a5e203767d8a048f65567f37de300f75e13(
    *,
    check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    create: typing.Optional[typing.Union[CreateOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    delete: typing.Optional[typing.Union[DeleteOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment: typing.Optional[typing.Union[DeploymentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_status: typing.Optional[typing.Union[DeploymentStatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    fork: typing.Optional[typing.Union[ForkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    gollum: typing.Optional[typing.Union[GollumOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    label: typing.Optional[typing.Union[LabelOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    page_build: typing.Optional[typing.Union[PageBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    public: typing.Optional[typing.Union[PublicOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pull_request_target: typing.Optional[typing.Union[PullRequestTargetOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    push: typing.Optional[typing.Union[PushOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[typing.Union[StatusOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_dispatch: typing.Optional[typing.Union[WorkflowDispatchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46ecdcecd3876bbfdf80e4a680d5dc6c1822a357f30c96c541b143795f6ea4a(
    file_path: builtins.str,
    *,
    obj: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da9b34eab7c2d80e24680051016fe375948e30adfb83511801fa66ad9493729(
    *patches: JsonPatch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a5e3b2d78d85076e947fd6efbffa9ddc155038612592c8fe6da18a27753823(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d492537bd16470957036b07a40a761d26ba00320315326f2e45084798f6594c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c376706244514db9e5ebda7df2cfb058056f86efc5baf6e4d2e6444f41ca85c(
    *,
    obj: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0f7f1a194dea5451b9bdd80028be3e5e499b46f0ad8737ce1a1b3b6344b8a6(
    *,
    post: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    pre: typing.Optional[typing.Sequence[_aws_cdk_pipelines_ceddda9d.Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_pipelines_ceddda9d.StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    git_hub_environment: typing.Optional[typing.Union[GitHubEnvironment, typing.Dict[builtins.str, typing.Any]]] = None,
    job_settings: typing.Optional[typing.Union[JobSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_capabilities: typing.Optional[typing.Sequence[StackCapabilities]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31c46895f60384d6ff3bd631f2e9c7ed5422806564f06c976cab0fd303b12ae(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
