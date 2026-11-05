r'''
# GitHub Self-Hosted Runners CDK Constructs

[![NPM](https://img.shields.io/npm/v/@cloudsnorkel/cdk-github-runners?label=npm&logo=npm)](https://www.npmjs.com/package/@cloudsnorkel/cdk-github-runners)
[![PyPI](https://img.shields.io/pypi/v/cloudsnorkel.cdk-github-runners?label=pypi&logo=pypi)](https://pypi.org/project/cloudsnorkel.cdk-github-runners)
[![Maven Central](https://img.shields.io/maven-central/v/com.cloudsnorkel/cdk.github.runners.svg?label=Maven%20Central&logo=apachemaven)](https://central.sonatype.com/artifact/com.cloudsnorkel/cdk.github.runners/)
[![Go](https://img.shields.io/github/v/tag/CloudSnorkel/cdk-github-runners?color=red&label=go&logo=go)](https://pkg.go.dev/github.com/CloudSnorkel/cdk-github-runners-go/cloudsnorkelcdkgithubrunners)
[![Nuget](https://img.shields.io/nuget/v/CloudSnorkel.Cdk.Github.Runners?color=red&&logo=nuget)](https://www.nuget.org/packages/CloudSnorkel.Cdk.Github.Runners/)
[![Release](https://github.com/CloudSnorkel/cdk-github-runners/actions/workflows/release.yml/badge.svg)](https://github.com/CloudSnorkel/cdk-github-runners/actions/workflows/release.yml)
[![Discord](https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white)](https://discord.gg/vdrTUTqQKv)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/CloudSnorkel/cdk-github-runners/blob/main/LICENSE)
[![awesome-runners](https://img.shields.io/badge/listed%20on-awesome--runners-blue.svg)](https://github.com/jonico/awesome-runners)

Use this CDK construct to create ephemeral [self-hosted GitHub runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) on-demand inside your AWS account.

* 🧩 Easy to configure GitHub integration with a web-based interface
* 🧠 Customizable runners with decent defaults
* 🏃🏻 Multiple runner configurations controlled by labels
* 🔐 Everything fully hosted in your account
* 🔃 Automatically updated build environment with latest runner version

Self-hosted runners in AWS are useful when:

* You need easy access to internal resources in your actions
* You want to pre-install some software for your actions
* You want to provide some basic AWS API access (but [aws-actions/configure-aws-credentials](https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions) has more security controls)
* You are using GitHub Enterprise Server (3.10 or newer, as runners are registered with [just-in-time configurations](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-just-in-time-runners))

Ephemeral (or on-demand) runners are the [recommended way by GitHub](https://docs.github.com/en/actions/hosting-your-own-runners/autoscaling-with-self-hosted-runners#using-ephemeral-runners-for-autoscaling) for auto-scaling, and they make sure all jobs run with a clean image. Runners are started on-demand. You don't pay unless a job is running.

## Table of Contents

* [API](#api)
* [Providers](#providers)

  * [Job Isolation](#job-isolation)
* [Installation](#installation)
* [Customizing](#customizing)

  * [Composite Providers](#composite-providers)
  * [Custom Provider Selection](#custom-provider-selection)
  * [Warm Runners](#warm-runners)
* [Examples](#examples)
* [Architecture](#architecture)
* [Troubleshooting](#troubleshooting)

  * [Rebuilding runner images](#rebuilding-runner-images)
* [Monitoring](#monitoring)
* [Getting Help](#getting-help)
* [Contributing](#contributing)
* [Sponsors](#sponsors)
* [Other Options](#other-options)

## API

The best way to browse API documentation is on [Constructs Hub](https://constructs.dev/packages/@cloudsnorkel/cdk-github-runners/). It is available in all supported programming languages.

## Providers

A runner provider creates compute resources on-demand and uses [actions/runner](https://github.com/actions/runner) to start a runner.

|                  | EC2               | CodeBuild                  | Fargate        | ECS            | Lambda        |
|------------------|-------------------|----------------------------|----------------|----------------|---------------|
| **Time limit**   | Unlimited         | 36 hours (default 1 hour)  | Unlimited      | Unlimited      | 15 minutes    |
| **vCPUs**        | Unlimited         | 2, 4, 8, or 72             | 0.25 to 4      | Unlimited      | 1 to 6        |
| **RAM**          | Unlimited         | 3gb, 7gb, 15gb, or 145gb   | 512mb to 30gb  | Unlimited      | 128mb to 10gb |
| **Storage**      | Unlimited         | 50gb to 824gb              | 20gb to 200gb  | Unlimited      | Up to 10gb    |
| **Architecture** | x86_64, ARM64     | x86_64, ARM64              | x86_64, ARM64  | x86_64, ARM64  | x86_64, ARM64 |
| **GPU**          | ✔                 | ✔                         | ❌              | ✔              | ❌           |
| **sudo**         | ✔                 | ✔                         | ✔              | ✔              | ❌           |
| **Docker**       | ✔                 | ✔ (Linux only)            | ❌              | ✔              | ❌           |
| **Spot pricing** | ✔                 | ❌                         | ✔              | ✔              | ❌           |
| **OS**           | Linux, Windows    | Linux, Windows             | Linux, Windows | Linux, Windows | Linux         |

The best provider to use mostly depends on your current infrastructure. When in doubt, CodeBuild is always a good choice. Execution history and logs are easy to view, and it has no restrictive limits unless you need to run for more than 8 hours.

* EC2 is useful when you want runners to have complete access to the host
* ECS is useful when you want to control the infrastructure, like leaving the runner host running for faster startups
* Lambda is useful for short jobs that can work within time, size and readonly system constraints

### Job Isolation

Every job gets a new runner, but not every provider gives every job its own machine. EC2, CodeBuild, and Fargate run each job on its own instance, build, or task. ECS and Lambda can run different jobs on the same machine, so jobs that can run on the same ECS cluster or Lambda function should be treated as one trust boundary.

* **ECS** runs jobs as containers on a shared cluster of long-lived instances. With `dockerInDocker` enabled, which is the default for Linux, runner containers are privileged. A job running in a privileged container can take over the instance. From there it can access other jobs running on the same instance, and leave processes behind that affect jobs that run on it later. If you bring your own `capacityProvider`, its launch template must also require IMDSv2 with a hop limit of 1, or even unprivileged jobs can take the instance role.
* **Lambda** reuses execution environments between jobs. A job can leave processes behind that can access or affect later jobs running on the same function. We do clear up `/tmp` between jobs which is the only writable filesystem available.

To keep jobs of different trust levels apart:

* Don't run untrusted code, like pull requests from forks of public repositories, on an ECS or Lambda provider that also runs jobs with access to secrets.
* Use separate providers for different trust levels. Labels alone don't keep untrusted workflows off a provider, as any workflow can request any label. Use [runner groups](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/managing-access-to-self-hosted-runners-using-groups) limited to specific repositories or workflows. For ECS, give each provider its own cluster.
* Disable `dockerInDocker` on ECS if your jobs don't need Docker.
* If jobs of different trust levels must share a provider, use EC2, CodeBuild, or Fargate. EC2 and CodeBuild also support Docker.

All jobs running on the same provider, regardless of the type, share the provider's IAM role, security groups, network access, and anything granted to `grantPrincipal`, so only grant what every job on the provider may use.

If you are using ECS or Lambda to maximize runner provisioning speed, you could also consider [warm runners](#warm-runners).

## Installation

1. Install and use the appropriate package

   <details><summary>Python</summary>

   ### Install

   Available on [PyPI](https://pypi.org/project/cloudsnorkel.cdk-github-runners).

   ```bash
   pip install cloudsnorkel.cdk-github-runners
   ```

   ### Use

   ```python
   from aws_cdk import App, Stack
   from cloudsnorkel.cdk_github_runners import GitHubRunners

   app = App()
   stack = Stack(app, "github-runners")
   GitHubRunners(stack, "runners")

   app.synth()
   ```

   </details>
   <details><summary>TypeScript or JavaScript</summary>

   ### Install

   Available on [npm](https://www.npmjs.com/package/@cloudsnorkel/cdk-github-runners).

   ```bash
   npm i @cloudsnorkel/cdk-github-runners
   ```

   ### Use

   ```python
   import { App, Stack } from 'aws-cdk-lib';
   import { GitHubRunners } from '@cloudsnorkel/cdk-github-runners';

   const app = new App();
   const stack = new Stack(app, 'github-runners');
   new GitHubRunners(stack, 'runners');

   app.synth();
   ```

   </details>
   <details><summary>Java</summary>

   ### Install

   Available on [Maven](https://central.sonatype.com/artifact/com.cloudsnorkel/cdk.github.runners/).

   ```xml
   <dependency>
      <groupId>com.cloudsnorkel</groupId>
      <artifactId>cdk.github.runners</artifactId>
   </dependency>
   ```

   ### Use

   ```java
   import software.amazon.awscdk.App;
   import software.amazon.awscdk.Stack;
   import com.cloudsnorkel.cdk.github.runners.GitHubRunners;

   public class Example {
     public static void main(String[] args){
       App app = new App();
       Stack stack = new Stack(app, "github-runners");
       GitHubRunners.Builder.create(stack, "runners").build();

       app.synth();
     }
   }
   ```

   </details>
   <details><summary>Go</summary>

   ### Install

   Available on [GitHub](https://pkg.go.dev/github.com/CloudSnorkel/cdk-github-runners-go/cloudsnorkelcdkgithubrunners).

   ```bash
   go get github.com/CloudSnorkel/cdk-github-runners-go/cloudsnorkelcdkgithubrunners
   ```

   ### Use

   ```go
   package main

   import (
     "github.com/CloudSnorkel/cdk-github-runners-go/cloudsnorkelcdkgithubrunners"
     "github.com/aws/aws-cdk-go/awscdk/v2"
     "github.com/aws/jsii-runtime-go"
   )

   func main() {
     app := awscdk.NewApp(nil)
     stack := awscdk.NewStack(app, jsii.String("github-runners"), &awscdk.StackProps{})
     cloudsnorkelcdkgithubrunners.NewGitHubRunners(stack, jsii.String("runners"), &cloudsnorkelcdkgithubrunners.GitHubRunnersProps{})

     app.Synth(nil)
   }
   ```

   </details>
   <details><summary>.NET</summary>

   ### Install

   Available on [Nuget](https://www.nuget.org/packages/CloudSnorkel.Cdk.Github.Runners/).

   ```bash
   dotnet add package CloudSnorkel.Cdk.Github.Runners
   ```

   ### Use

   ```csharp
   using Amazon.CDK;
   using CloudSnorkel;

   namespace Example
   {
     sealed class Program
     {
       public static void Main(string[] args)
       {
         var app = new App();
         var stack = new Stack(app, "github-runners");
         new GitHubRunners(stack, "runners");
         app.Synth();
       }
     }
   }
   ```

   </details>
2. Use `GitHubRunners` construct in your code (starting with default arguments is fine)
3. Deploy your stack
4. Look for the status command output similar to `aws --region us-east-1 lambda invoke --function-name status-XYZ123 status.json`

   ```
    ✅  github-runners-test

   ✨  Deployment time: 260.01s

   Outputs:
   github-runners-test.runnersstatuscommand4A30F0F5 = aws --region us-east-1 lambda invoke --function-name github-runners-test-runnersstatus1A5771C0-mvttg8oPQnQS status.json
   ```
5. Execute the status command (you may need to specify `--profile` too) and open the resulting `status.json` file
6. Open the URL in `github.setup.url` from `status.json` or [manually setup GitHub](SETUP_GITHUB.md) integration as an app or with personal access token
7. Run status command again to confirm `github.auth.status` and `github.webhook.status` are OK
8. Trigger a GitHub action that has a `self-hosted` label with `runs-on: [self-hosted, codebuild]` (or non-default labels you set in step 2)
9. If the action is not successful, see [troubleshooting](#Troubleshooting)

[![Demo](demo-thumbnail.jpg)](https://youtu.be/wlyv_3V8lIw)

## Customizing

The default providers configured by `GitHubRunners` are useful for testing but probably not too much for actual production work. They run in the default VPC or no VPC and have no added IAM permissions. You would usually want to configure the providers yourself.

For example:

```python
let vpc: ec2.Vpc;
let runnerSg: ec2.SecurityGroup;
let dbSg: ec2.SecurityGroup;
let bucket: s3.Bucket;

// create a custom CodeBuild provider
const myProvider = new CodeBuildRunnerProvider(this, 'codebuild runner', {
   labels: ['my-codebuild'],
   vpc: vpc,
   securityGroups: [runnerSg],
});
// grant some permissions to the provider
bucket.grantReadWrite(myProvider);
dbSg.connections.allowFrom(runnerSg, ec2.Port.tcp(3306), 'allow runners to connect to MySQL database');

// create the runner infrastructure
new GitHubRunners(this, 'runners', {
   providers: [myProvider],
});
```

Another way to customize runners is by modifying the image used to spin them up. The image contains the [runner](https://github.com/actions/runner), any required dependencies, and integration code with the provider. You may choose to customize this image by adding more packages, for example.

```python
const myBuilder = FargateRunnerProvider.imageBuilder(this, 'image builder');
myBuilder.addComponent(
  RunnerImageComponent.custom({ commands: ['apt install -y nginx xz-utils'] }),
);

const myProvider = new FargateRunnerProvider(this, 'fargate runner', {
   labels: ['customized-fargate'],
   imageBuilder: myBuilder,
});

// create the runner infrastructure
new GitHubRunners(this, 'runners', {
   providers: [myProvider],
});
```

Your workflow will then look like:

```yaml
name: self-hosted example
on: push
jobs:
  self-hosted:
    runs-on: [self-hosted, customized-fargate]
    steps:
      - run: echo hello world
```

Windows images can also be customized the same way.

```python
const myWindowsBuilder = FargateRunnerProvider.imageBuilder(this, 'Windows image builder', {
   architecture: Architecture.X86_64,
   os: Os.WINDOWS,
});
myWindowsBuilder.addComponent(
   RunnerImageComponent.custom({
     name: 'Ninja',
     commands: [
       'Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/ninja-build/ninja/releases/download/v1.11.1/ninja-win.zip" -OutFile ninja.zip',
       'Expand-Archive ninja.zip -DestinationPath C:\\actions',
       'del ninja.zip',
     ],
   }),
);

const myProvider = new FargateRunnerProvider(this, 'fargate runner', {
   labels: ['customized-windows-fargate'],
   imageBuilder: myWindowsBuilder,
});

new GitHubRunners(this, 'runners', {
   providers: [myProvider],
});
```

The runner OS and architecture is determined by the image it is set to use. For example, to create a Fargate runner provider for ARM64 set the `architecture` property for the image builder to `Architecture.ARM64` in the image builder properties.

```python
new GitHubRunners(this, 'runners', {
   providers: [
      new FargateRunnerProvider(this, 'fargate runner', {
         labels: ['arm64', 'fargate'],
         imageBuilder: FargateRunnerProvider.imageBuilder(this, 'image builder', {
            architecture: Architecture.ARM64,
            os: Os.LINUX_UBUNTU,
         }),
      }),
   ],
});
```

### Composite Providers

Composite providers allow you to combine multiple runner providers with different strategies. There are two types:

**Fallback Strategy**: Try providers in order until one succeeds. Useful for trying spot instances first, then falling back to on-demand if spot capacity is unavailable.

```python
// Try spot instances first, fall back to on-demand if spot is unavailable
const ecsFallback = CompositeProvider.fallback(this, 'ECS Fallback', [
  new EcsRunnerProvider(this, 'ECS Spot', {
    labels: ['ecs', 'linux', 'x64'],
    spot: true,
    // ... other config
  }),
  new EcsRunnerProvider(this, 'ECS On-Demand', {
    labels: ['ecs', 'linux', 'x64'],
    spot: false,
    // ... other config
  }),
]);

new GitHubRunners(this, 'runners', {
  providers: [ecsFallback],
});
```

**Weighted Distribution Strategy**: Randomly select a provider based on weights. Useful for distributing load across multiple availability zones or instance types.

```python
// Distribute 60% of traffic to AZ-1, 40% to AZ-2
const distributedProvider = CompositeProvider.distribute(this, 'Fargate Distribution', [
  {
    weight: 3, // 3/(3+2) = 60%
    provider: new FargateRunnerProvider(this, 'Fargate AZ-1', {
      labels: ['fargate', 'linux', 'x64'],
      subnetSelection: vpc.selectSubnets({
        availabilityZones: [vpc.availabilityZones[0]],
      }),
      // ... other config
    }),
  },
  {
    weight: 2, // 2/(3+2) = 40%
    provider: new FargateRunnerProvider(this, 'Fargate AZ-2', {
      labels: ['fargate', 'linux', 'x64'],
      subnetSelection: vpc.selectSubnets({
        availabilityZones: [vpc.availabilityZones[1]],
      }),
      // ... other config
    }),
  },
]);

new GitHubRunners(this, 'runners', {
  providers: [distributedProvider],
});
```

**Important**: All providers in a composite must have the exact same labels. This ensures any provisioned runner can match the labels requested by the GitHub workflow job.

### Custom Provider Selection

By default, providers are selected based on label matching: the first provider that has all the labels requested by the job is selected. You can customize this behavior using a provider selector Lambda function to:

* Filter out certain jobs (prevent runner provisioning)
* Dynamically select a provider based on job characteristics (repository, branch, time of day, etc.)
* Customize labels for the runner (add, remove, or modify labels dynamically)

The selector function receives the full GitHub webhook payload, a map of all available providers and their labels, and the default provider/labels that would have been selected. It returns the provider to use (or `undefined` to skip runner creation) and the labels to assign to the runner.

**Example: Route jobs to different providers based on repository**

```python
import { ComputeType } from 'aws-cdk-lib/aws-codebuild';
import { Function, Code, Runtime } from 'aws-cdk-lib/aws-lambda';
import { GitHubRunners, CodeBuildRunnerProvider } from '@cloudsnorkel/cdk-github-runners';

const defaultProvider = new CodeBuildRunnerProvider(this, 'default', {
  labels: ['custom-runner', 'default'],
});
const productionProvider = new CodeBuildRunnerProvider(this, 'production', {
  labels: ['custom-runner', 'production'],
  computeType: ComputeType.LARGE,
});

const providerSelector = new Function(this, 'provider-selector', {
  runtime: Runtime.NODEJS_LATEST,
  handler: 'index.handler',
  code: Code.fromInline(`
    exports.handler = async (event) => {
      const { payload, providers, defaultProvider, defaultLabels } = event;

      // Route production repos to dedicated provider
      if (payload.repository.name.includes('prod')) {
        return {
          provider: '${productionProvider.node.path}',
          labels: ['custom-runner', 'production', 'modified-via-selector'],
        };
      }

      // Filter out draft PRs
      if (payload.workflow_job.head_branch?.startsWith('draft/')) {
        return { provider: undefined }; // Skip runner provisioning
      }

      // Use default for everything else
      return {
        provider: defaultProvider,
        labels: defaultLabels,
      };
    };
  `),
});

new GitHubRunners(this, 'runners', {
   providers: [defaultProvider, productionProvider],
   providerSelector: providerSelector,
});
```

**Example: Add dynamic labels based on job metadata**

```python
const providerSelector = new Function(this, 'provider-selector', {
  runtime: Runtime.NODEJS_LATEST,
  handler: 'index.handler',
  code: Code.fromInline(`
    exports.handler = async (event) => {
      const { payload, defaultProvider, defaultLabels } = event;

      // Add branch name as a label
      const branch = payload.workflow_job.head_branch || 'unknown';
      const labels = [...(defaultLabels || []), 'branch:' + branch];

      return {
        provider: defaultProvider,
        labels: labels,
      };
    };
  `),
});
```

**Important considerations:**

* ⚠️ **Label matching responsibility**: You are responsible for ensuring the selected provider's labels match what the job requires. If labels don't match, the runner will be provisioned but GitHub Actions won't assign the job to it.
* ⚠️ **No guarantee of assignment**: Provider selection only determines which provider will provision a runner. GitHub Actions may still route the job to any available runner with matching labels. For reliable provider assignment, consider repo-level runner registration (the default).
* ⚡ **Performance**: The selector runs synchronously during webhook processing. Keep it fast and efficient—the webhook has a 30-second timeout total.

### Warm Runners

Warm runners are pre-provisioned and stay idle until a job arrives, reducing startup latency. Use `AlwaysOnWarmRunner` for 24/7 pools or `ScheduledWarmRunner` for time-windowed pools. You specify the provider directly.

```python
import { AlwaysOnWarmRunner, CodeBuildRunnerProvider, GitHubRunners } from '@cloudsnorkel/cdk-github-runners';

const provider = new CodeBuildRunnerProvider(this, 'provider', { labels: ['codebuild', 'linux'] });
const runners = new GitHubRunners(this, 'runners', { providers: [provider] });

new AlwaysOnWarmRunner(this, 'warm', {
  runners,
  provider,
  count: 2,
  owner: 'my-org',
  repo: 'my-repo',
});
```

Warm runner pools can be stacked. If you want 2 warm runners always available but 3 during peak work hours, you can create one pool with 2 runners always on and another pool with 1 runner during work hours.

```python
import { aws_events as events, Duration } from 'aws-cdk-lib';
import { AlwaysOnWarmRunner, ScheduledWarmRunner, CodeBuildRunnerProvider, GitHubRunners } from '@cloudsnorkel/cdk-github-runners';

const provider = new CodeBuildRunnerProvider(this, 'provider', { labels: ['codebuild', 'linux'] });
const runners = new GitHubRunners(this, 'runners', { providers: [provider] });

new AlwaysOnWarmRunner(this, 'warm', {
  runners,
  provider,
  count: 2,
  owner: 'my-org',
  repo: 'my-repo',
});

new ScheduledWarmRunner(this, 'work hours warm', {
  runners,
  provider,
  count: 1,
  owner: 'my-org',
  repo: 'my-repo',
  schedule: events.Schedule.cron({ hour: '13', minute: '0', weekDay: 'MON-FRI' }),
  duration: Duration.hours(2),
});
```

See the [warm-runners example](examples/typescript/warm-runners/) for a complete setup.

## Examples

We provide comprehensive examples in the [`examples/`](examples/) folder to help you get started quickly:

### Getting Started

* **[Simple CodeBuild](examples/typescript/simple-codebuild/)** - Basic setup with just a CodeBuild provider (also available in [Python](examples/python/simple-codebuild/))
* **[Warm Runners](examples/typescript/warm-runners/)** - Pre-provisioned runners for low-latency job starts (also available in [Python](examples/python/warm-runners/))

### Provider Configuration

* **[Composite Provider](examples/typescript/composite-provider/)** - Fallback and weighted distribution strategies (also available in [Python](examples/python/composite-provider/))
* **[Provider Selector](examples/typescript/provider-selector/)** - Custom provider selection with Lambda function (also available in [Python](examples/python/provider-selector/))
* **[EC2 Windows Provider](examples/typescript/ec2-windows-provider/)** - EC2 configuration for Windows runners (also available in [Python](examples/python/ec2-windows-provider/))
* **[Split Stacks](examples/typescript/split-stacks/)** - Split image builders and providers across multiple stacks (also available in [Python](examples/python/split-stacks/))

### Compute & Performance

* **[Compute Options](examples/typescript/compute-options/)** - Configure CPU, memory, and instance types for different providers (also available in [Python](examples/python/compute-options/))
* **[Spot Instances](examples/typescript/spot-instances/)** - Use spot instances for cost savings across EC2, Fargate, and ECS (also available in [Python](examples/python/spot-instances/))
* **[Storage Options](examples/typescript/storage-options/)** - Custom EBS storage options for EC2 runners (also available in [Python](examples/python/storage-options/))
* **[ECS Scaling](examples/typescript/ecs-scaling/)** - Custom autoscaling group scaling policies for ECS providers (also available in [Python](examples/python/ecs-scaling/))

### Security & Access

* **[IAM Permissions](examples/typescript/iam-permissions/)** - Grant AWS IAM permissions to runners (also available in [Python](examples/python/iam-permissions/))
* **[Network Access](examples/typescript/network-access/)** - Configure network access with VPCs and security groups (also available in [Python](examples/python/network-access/))
* **[Access Control](examples/typescript/access-control/)** - Configure access control for webhook and setup functions (also available in [Python](examples/python/access-control/))

### Customization

* **[Add Software](examples/typescript/add-software/)** - Add custom software to runner images (also available in [Python](examples/python/add-software/))
* **[Job Hooks](examples/typescript/job-hooks/)** - Run a script before every job using GitHub Actions runner hooks (also available in [Python](examples/python/job-hooks/))
* **[GPU](examples/typescript/gpu/)** - GPU support with NVIDIA drivers across EC2, CodeBuild, and ECS (also available in [Python](examples/python/gpu/))

### Enterprise & Monitoring

* **[GHES](examples/typescript/ghes/)** - Configure runners for GitHub Enterprise Server (also available in [Python](examples/python/ghes/))
* **[Monitoring](examples/typescript/monitoring/)** - Set up CloudWatch alarms and SNS notifications (also available in [Python](examples/python/monitoring/))

Each example is self-contained with its own dependencies and README. Start with the simple examples and work your way up to more advanced configurations.

Another good and very full example is the [integration test](test/default.integ.ts).

If you have more to share, please open a PR adding examples to the `examples` folder.

## Architecture

![Architecture diagram](architecture.svg)

## Troubleshooting

Runners are started in response to a webhook coming in from GitHub. If there are any issues starting the runner like missing capacity or transient API issues, the provider will keep retrying for 24 hours. GitHub itself will cancel the job if it can't find a runner for 24 hours. If your jobs don't start, follow the steps below to examine all parts of this workflow.

Configuration problems that we can detect up-front fail the orchestrator with a `RunnerConfigurationError` before any instance, build, or task is started. The error message says what needs to be fixed. These are still retried like any other error, so a configuration fixed within the 24 hours GitHub keeps the job queued still gets a runner and the job still runs.

1. Always start with the status function, make sure no errors are reported, and confirm all status codes are OK
2. Make sure `runs-on` in the workflow matches the expected labels set in the runner provider
3. Diagnose relevant executions of the orchestrator step function by visiting the URL in `troubleshooting.stepFunctionUrl` from `status.json`

   1. If the execution failed, check your runner provider configuration for errors
   2. If the execution is still running for a long time, check the execution events to see why runner starting is being retried
   3. If there are no relevant executions, move to the next step
4. Confirm the webhook Lambda was called by visiting the URL in `troubleshooting.webhookHandlerUrl` from `status.json`

   1. If it's not called or logs errors, confirm the webhook settings on the GitHub side
   2. If you see too many errors, make sure you're only sending `workflow_job` events
5. When using GitHub app, make sure there are active installations in `github.auth.app.installations`
6. If runners start but never pick up a job and get stopped with `IdleRunner`, their runner version may be too old. Runners can't update themselves, and GitHub stops sending jobs to runners that are not updated within 30 days of a new runner release, or right away for a critical security update. [Rebuild your runner images](#rebuilding-runner-images) to fix it
7. If organization-level runners never pick up jobs from public repositories, check the runner group settings. By default, only private repositories can use runners in a runner group. You can allow public repositories in the [runner group repository access settings](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/managing-access-to-self-hosted-runners-using-groups#changing-which-repositories-can-access-a-runner-group), but make sure you understand the [security risks](#job-isolation) first

All logs are saved in CloudWatch.

* Log group names can be found in `status.json` for each provider, image builder, and other parts of the system
* Some useful Logs Insights queries can be enabled with `GitHubRunners.createLogsInsightsQueries()`

To get `status.json`, check out the CloudFormation stack output for a command that generates it. The command looks like:

```
aws --region us-east-1 lambda invoke --function-name status-XYZ123 status.json
```

### Rebuilding runner images

Runner images are rebuilt every `rebuildInterval` (7 days by default). To rebuild all of them right now, run this with the name of the every stack your runners are built in. It starts every image builder in the stack and prints the build ids. Runners pick up the new images as soon as the builds finish.

```sh
STACK=my-runners-stack
resources() {
  aws cloudformation list-stack-resources --stack-name "$STACK" --output text \
    --query "StackResourceSummaries[?ResourceType=='$1'].PhysicalResourceId"
}
for project in $(resources AWS::CodeBuild::Project); do
  # skip runner projects of CodeBuild providers, we only want image builders
  aws codebuild batch-get-projects --names "$project" --output text --query 'projects[0].description' \
    | grep -q '^Build docker image for self-hosted GitHub runner' \
    && aws codebuild start-build --project-name "$project" --output text --query 'build.id'
done
for pipeline in $(resources AWS::ImageBuilder::ImagePipeline); do
  aws imagebuilder start-image-pipeline-execution --image-pipeline-arn "$pipeline" --output text --query 'imageBuildVersionArn'
done
```

Make sure you use `failedImageBuildsTopic()` to get notified of any failed builds.

## Monitoring

There are three important ways to monitor your runners:

1. Make sure runners don't fail to start. When that happens, jobs may sit and wait. Use `GitHubRunners.metricFailed()` to get a metric for the number of failed runner starts. You should use this metric to trigger an alarm.
2. Make sure our management functions don't fail. When that happens, webhooks may be dropped and jobs may never get a runner. Use `GitHubRunners.metricLambdaErrors()` to get a metric for the number of failed invocations across all management Lambda functions. You should use this metric to trigger an alarm.
3. Make sure runner images don't fail to build. Failed runner image builds mean you will get stuck with out-of-date software on your runners. It may lead to security vulnerabilities, or it may lead to slower runner start-ups as the runner software itself needs to be updated. Use `GitHubRunners.failedImageBuildsTopic()` to get SNS topic that gets notified of failed runner image builds. You should subscribe to this topic.

Other useful metrics to track:

1. Use `GitHubRunners.metricJobCompleted()` to get a metric for the number of completed jobs broken down by labels and job success.
2. Use `GitHubRunners.metricTime()` to get a metric for the total time a runner is running. This includes the overhead of starting the runner.
3. Use `GitHubRunners.metricStolenRunners()` to get a metric for number of runners detected as stolen by another job. Anything over zero can indicate a misconfiguration or GitHub webhook issues.
4. Use `GitHubRunners.metricJobsMatchingMultipleProviders()` to get a metric for the number of jobs whose labels matched more than one provider and may run on any of them. Anything over zero means some workflows should ask for more labels.

Use `GitHubRunners.createDashboard()` to get a CloudWatch dashboard with all of these metrics in one place. It's split
into sections for jobs, runners, runner assignment and management functions. Each section explains what its numbers
mean and which ones to alarm on.

## Known Issues

1. Runner images built during a failed deployment are not rolled back. If your stack fails to deploy after an image was already built, the new image will stay in use. The image will be automatically replaced on the next build interval, but that might take up to 7 days with default settings (`rebuildInterval`). It's recommended to not leave stacks in `UPDATE_ROLLBACK_COMPLETE` state. Deploying again with the configuration you want will rebuild the images and get everything back in sync.
2. Library downgrades are not well tested. We work hard to keep backwards compatibility, but downgrading to an older version of the library may lead to unexpected issues. For example, downgrading from 0.16.1 may result in runner images being deleted. They will be rebuilt on the next build interval, but that might take up to 7 days with default settings (`rebuildInterval`). It's recommended to not downgrade the library unless you know what you're doing.

## Getting Help

Need help? We're here for you!

* 💬 **GitHub Discussions**: Ask questions, share ideas, or get help from the community by opening a [discussion](https://github.com/CloudSnorkel/cdk-github-runners/discussions)
* 🐛 **GitHub Issues**: Report bugs or request features by opening an [issue](https://github.com/CloudSnorkel/cdk-github-runners/issues)
* 💬 **Discord**: Join our [Discord community](https://discord.gg/vdrTUTqQKv) for real-time help and discussions

## Contributing

If you use and love this project, please consider contributing.

1. 🪳 If you see something, say something. [Issues](https://github.com/CloudSnorkel/cdk-github-runners/issues) help improve the quality of the project.

   * Include relevant logs and package versions for bugs.
   * When possible, describe the use-case behind feature requests.
2. 🛠️ [Pull requests](https://github.com/CloudSnorkel/cdk-github-runners/pulls) are welcome.

   * Run `npm run build` before submitting to make sure all tests pass.
   * Allow edits from maintainers so small adjustments can be made easily.
3. 💵 Consider [sponsoring](https://github.com/sponsors/CloudSnorkel) the project to show your support and optionally get your name listed below.

## Sponsors

Thanks to our generous sponsors who helped make this project possible!

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/threat-down">
        <img src="https://github.com/threat-down.png?size=100" width="100" height="100" alt="ThreatDown" />
        <br />
        <sub><b>ThreatDown</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/magicbell">
        <img src="https://github.com/magicbell.png?size=100" width="100" height="100" alt="MagicBell" />
        <br />
        <sub><b>MagicBell</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/fragment-dev">
        <img src="https://github.com/fragment-dev.png?size=100" width="100" height="100" alt="Fragment" />
        <br />
        <sub><b>Fragment</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/qnicondavid">
        <img src="https://github.com/qnicondavid.png?size=100" width="100" height="100" alt="Nicon-David Milandru" />
        <br />
        <sub><b>Nicon-David Milandru</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/andresionek91">
        <img src="https://github.com/andresionek91.png?size=100" width="100" height="100" alt="Andre Sionek" />
        <br />
        <sub><b>Andre Sionek</b></sub>
      </a>
    </td>
  </tr>
</table>

## Other Options

1. [github-aws-runners/terraform-aws-github-runner](https://github.com/github-aws-runners/terraform-aws-github-runner) if you're using Terraform
2. [actions/actions-runner-controller](https://github.com/actions/actions-runner-controller) if you're using Kubernetes
'''
from __future__ import annotations

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

from jsii._type_checking import cached_type_hints, check_type


from ._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk as _aws_cdk_ceddda9d
    import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
    import aws_cdk.aws_codebuild as _aws_cdk_aws_codebuild_ceddda9d
    import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
    import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_ceddda9d
    import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
    import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
    import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
    import aws_cdk.aws_imagebuilder as _aws_cdk_aws_imagebuilder_ceddda9d
    import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
    import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
    import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
    import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
    import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
    import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d
    import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_aws_cloudwatch_ceddda9d = _LazyImport("aws_cdk.aws_cloudwatch")
    _aws_cdk_aws_codebuild_ceddda9d = _LazyImport("aws_cdk.aws_codebuild")
    _aws_cdk_aws_ec2_ceddda9d = _LazyImport("aws_cdk.aws_ec2")
    _aws_cdk_aws_ecr_ceddda9d = _LazyImport("aws_cdk.aws_ecr")
    _aws_cdk_aws_ecs_ceddda9d = _LazyImport("aws_cdk.aws_ecs")
    _aws_cdk_aws_events_ceddda9d = _LazyImport("aws_cdk.aws_events")
    _aws_cdk_aws_iam_ceddda9d = _LazyImport("aws_cdk.aws_iam")
    _aws_cdk_aws_imagebuilder_ceddda9d = _LazyImport("aws_cdk.aws_imagebuilder")
    _aws_cdk_aws_lambda_ceddda9d = _LazyImport("aws_cdk.aws_lambda")
    _aws_cdk_aws_logs_ceddda9d = _LazyImport("aws_cdk.aws_logs")
    _aws_cdk_aws_s3_assets_ceddda9d = _LazyImport("aws_cdk.aws_s3_assets")
    _aws_cdk_aws_secretsmanager_ceddda9d = _LazyImport("aws_cdk.aws_secretsmanager")
    _aws_cdk_aws_sns_ceddda9d = _LazyImport("aws_cdk.aws_sns")
    _aws_cdk_aws_ssm_ceddda9d = _LazyImport("aws_cdk.aws_ssm")
    _aws_cdk_aws_stepfunctions_ceddda9d = _LazyImport("aws_cdk.aws_stepfunctions")
    _aws_cdk_ceddda9d = _LazyImport("aws_cdk")
    _constructs_77d1e7e8 = _LazyImport("constructs")


class AlwaysOnWarmRunner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.AlwaysOnWarmRunner",
):
    '''(experimental) Warm runners that run 24/7. Fills at midnight UTC and each runner stays alive for 24 hours.

    Runners will be provisioned using the specified provider and registered in the specified repository or organization.

    Registration level must match the one selected during setup.

    :see:

    https://github.com/CloudSnorkel/cdk-github-runners/blob/main/SETUP_GITHUB.md

    **Limitations**

    - Jobs will still trigger provisioning of on-demand runners, even if a warm runner ends up being used.
    - You may briefly see more than ``count`` runners when changing config or at rotation.
    - To remove: set ``count`` to 0, deploy, wait for warm runners to stop, then remove and deploy again.
    If you don't follow this procedure, warm runners may linger until they expire.
    - Provider failures or timeouts (like Lambda provider timing out after 15 minutes) will result in a
    gap in coverage until the retry succeeds. Current retry mechanism has built-in back-off rate and
    can be tweaked using ``retryOptions``. This will be improved in the future.

    Example::

    new AlwaysOnWarmRunner(stack, 'AlwaysOnLinux', {
    runners,
    provider: myProvider,
    count: 3,
    owner: 'my-org',
    repo: 'my-repo',
    });
    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        count: jsii.Number,
        owner: builtins.str,
        provider: typing.Union["IRunnerProvider", "ICompositeProvider"],
        runners: "GitHubRunners",
        registration_level: typing.Optional[builtins.str] = None,
        repo: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param count: (experimental) Number of warm runners to maintain.
        :param owner: (experimental) GitHub owner where runners will be registered (org or user login).
        :param provider: (experimental) Provider to use. Warm runners bypass the provider selector — they always use this provider, regardless of job characteristics. Labels cannot be modified.
        :param runners: (experimental) The GitHubRunners construct that owns the shared warm runner infrastructure.
        :param registration_level: (experimental) Registration level — must match how your runners are set up in GitHub. Choose 'org' for org-wide runners, 'repo' for repo-level. See the setup wizard for choosing repo vs org. Default: 'repo'
        :param repo: (experimental) Repository name (without owner) where runners will be registered. Required when ``registrationLevel`` is 'repo'.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6190a21456122517ee8943805f4bb158e15774f590513fc686004df32e516d1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AlwaysOnWarmRunnerProps(
            count=count,
            owner=owner,
            provider=provider,
            runners=runners,
            registration_level=registration_level,
            repo=repo,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.AlwaysOnWarmRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "owner": "owner",
        "provider": "provider",
        "runners": "runners",
        "registration_level": "registrationLevel",
        "repo": "repo",
    },
)
class AlwaysOnWarmRunnerProps:
    def __init__(
        self,
        *,
        count: jsii.Number,
        owner: builtins.str,
        provider: typing.Union["IRunnerProvider", "ICompositeProvider"],
        runners: "GitHubRunners",
        registration_level: typing.Optional[builtins.str] = None,
        repo: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for always on warm runners.

        :param count: (experimental) Number of warm runners to maintain.
        :param owner: (experimental) GitHub owner where runners will be registered (org or user login).
        :param provider: (experimental) Provider to use. Warm runners bypass the provider selector — they always use this provider, regardless of job characteristics. Labels cannot be modified.
        :param runners: (experimental) The GitHubRunners construct that owns the shared warm runner infrastructure.
        :param registration_level: (experimental) Registration level — must match how your runners are set up in GitHub. Choose 'org' for org-wide runners, 'repo' for repo-level. See the setup wizard for choosing repo vs org. Default: 'repo'
        :param repo: (experimental) Repository name (without owner) where runners will be registered. Required when ``registrationLevel`` is 'repo'.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5898a98cc3d83a12a9319ee2298fa83987d45a80e21cc1aa7c35f76c3bf7b94a)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument runners", value=runners, expected_type=type_hints["runners"])
            check_type(argname="argument registration_level", value=registration_level, expected_type=type_hints["registration_level"])
            check_type(argname="argument repo", value=repo, expected_type=type_hints["repo"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "owner": owner,
            "provider": provider,
            "runners": runners,
        }
        if registration_level is not None:
            self._values["registration_level"] = registration_level
        if repo is not None:
            self._values["repo"] = repo

    @builtins.property
    def count(self) -> jsii.Number:
        '''(experimental) Number of warm runners to maintain.

        :stability: experimental
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) GitHub owner where runners will be registered (org or user login).

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> typing.Union["IRunnerProvider", "ICompositeProvider"]:
        '''(experimental) Provider to use.

        Warm runners bypass the provider selector — they always use
        this provider, regardless of job characteristics. Labels cannot be modified.

        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(typing.Union["IRunnerProvider", "ICompositeProvider"], result)

    @builtins.property
    def runners(self) -> "GitHubRunners":
        '''(experimental) The GitHubRunners construct that owns the shared warm runner infrastructure.

        :stability: experimental
        '''
        result = self._values.get("runners")
        assert result is not None, "Required property 'runners' is missing"
        return typing.cast("GitHubRunners", result)

    @builtins.property
    def registration_level(self) -> typing.Optional[builtins.str]:
        '''(experimental) Registration level — must match how your runners are set up in GitHub.

        Choose
        'org' for org-wide runners, 'repo' for repo-level. See the setup wizard for choosing repo vs org.

        :default: 'repo'

        :see: https://github.com/CloudSnorkel/cdk-github-runners/blob/main/SETUP_GITHUB.md
        :stability: experimental
        '''
        result = self._values.get("registration_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo(self) -> typing.Optional[builtins.str]:
        '''(experimental) Repository name (without owner) where runners will be registered.

        Required when ``registrationLevel`` is 'repo'.

        :stability: experimental
        '''
        result = self._values.get("repo")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlwaysOnWarmRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.AmiBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "install_docker": "installDocker",
        "instance_type": "instanceType",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "os": "os",
        "rebuild_interval": "rebuildInterval",
        "runner_version": "runnerVersion",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class AmiBuilderProps:
    def __init__(
        self,
        *,
        architecture: typing.Optional["Architecture"] = None,
        install_docker: typing.Optional[builtins.bool] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''(experimental) Properties for {@link AmiBuilder} construct.

        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param install_docker: (experimental) Install Docker inside the image, so it can be used by the runner. Default: true
        :param instance_type: (experimental) The instance type used to build the image. Default: m6i.large
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param rebuild_interval: (experimental) Schedule the AMI to be rebuilt every given interval. Useful for keeping the AMI up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (deprecated) Security group to assign to launched builder instances. Default: new security group
        :param security_groups: (experimental) Security groups to assign to launched builder instances. Default: new security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param vpc: (experimental) VPC where builder instances will be launched. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b1848f87828e47066d3d798fe57a60bb7bcf3be03f641b793ff686f68265bb5b)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument install_docker", value=install_docker, expected_type=type_hints["install_docker"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument rebuild_interval", value=rebuild_interval, expected_type=type_hints["rebuild_interval"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if install_docker is not None:
            self._values["install_docker"] = install_docker
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if os is not None:
            self._values["os"] = os
        if rebuild_interval is not None:
            self._values["rebuild_interval"] = rebuild_interval
        if runner_version is not None:
            self._values["runner_version"] = runner_version
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def architecture(self) -> typing.Optional["Architecture"]:
        '''(experimental) Image architecture.

        :default: Architecture.X86_64

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional["Architecture"], result)

    @builtins.property
    def install_docker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install Docker inside the image, so it can be used by the runner.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("install_docker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"]:
        '''(experimental) The instance type used to build the image.

        :default: m6i.large

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Removal policy for logs of image builds.

        If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the logs can still be viewed, and you can see why the build failed.

        We try to not leave anything behind when removed. But sometimes a log staying behind is useful.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def os(self) -> typing.Optional["Os"]:
        '''(experimental) Image OS.

        :default: OS.LINUX

        :stability: experimental
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional["Os"], result)

    @builtins.property
    def rebuild_interval(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) Schedule the AMI to be rebuilt every given interval.

        Useful for keeping the AMI up-do-date with the latest GitHub runner version and latest OS updates.

        Set to zero to disable.

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("rebuild_interval")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def runner_version(self) -> typing.Optional["RunnerVersion"]:
        '''(experimental) Version of GitHub Runners to install.

        :default: latest version available

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        return typing.cast(typing.Optional["RunnerVersion"], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(deprecated) Security group to assign to launched builder instances.

        :default: new security group

        :deprecated: use {@link securityGroups }

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security groups to assign to launched builder instances.

        :default: new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Where to place the network interfaces within the VPC.

        Only the first matched subnet will be used.

        :default: default VPC subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC where builder instances will be launched.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmiBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ApiGatewayAccessProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_ips": "allowedIps",
        "allowed_security_groups": "allowedSecurityGroups",
        "allowed_vpc": "allowedVpc",
        "allowed_vpc_endpoints": "allowedVpcEndpoints",
    },
)
class ApiGatewayAccessProps:
    def __init__(
        self,
        *,
        allowed_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        allowed_vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        allowed_vpc_endpoints: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint"]] = None,
    ) -> None:
        '''
        :param allowed_ips: (experimental) List of IP addresses in CIDR notation that are allowed to access the API Gateway. If not specified on public API Gateway, all IP addresses are allowed. If not specified on private API Gateway, no IP addresses are allowed (but specified security groups are).
        :param allowed_security_groups: (experimental) List of security groups that are allowed to access the API Gateway. Only works for private API Gateways with {@link allowedVpc}.
        :param allowed_vpc: (experimental) Create a private API Gateway and allow access from the specified VPC.
        :param allowed_vpc_endpoints: (experimental) Create a private API Gateway and allow access from the specified VPC endpoints. Use this to make use of existing VPC endpoints or to share an endpoint between multiple functions. The VPC endpoint must point to ``ec2.InterfaceVpcEndpointAwsService.APIGATEWAY``. No other settings are supported when using this option. All endpoints will be allowed access, but only the first one will be used as the URL by the runner system for setting up the webhook, and as setup URL.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0230281aea2f0096e32af8e4f02c3c351aada0957c217590514bfc5f6f656b0e)
            check_type(argname="argument allowed_ips", value=allowed_ips, expected_type=type_hints["allowed_ips"])
            check_type(argname="argument allowed_security_groups", value=allowed_security_groups, expected_type=type_hints["allowed_security_groups"])
            check_type(argname="argument allowed_vpc", value=allowed_vpc, expected_type=type_hints["allowed_vpc"])
            check_type(argname="argument allowed_vpc_endpoints", value=allowed_vpc_endpoints, expected_type=type_hints["allowed_vpc_endpoints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_ips is not None:
            self._values["allowed_ips"] = allowed_ips
        if allowed_security_groups is not None:
            self._values["allowed_security_groups"] = allowed_security_groups
        if allowed_vpc is not None:
            self._values["allowed_vpc"] = allowed_vpc
        if allowed_vpc_endpoints is not None:
            self._values["allowed_vpc_endpoints"] = allowed_vpc_endpoints

    @builtins.property
    def allowed_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of IP addresses in CIDR notation that are allowed to access the API Gateway.

        If not specified on public API Gateway, all IP addresses are allowed.

        If not specified on private API Gateway, no IP addresses are allowed (but specified security groups are).

        :stability: experimental
        '''
        result = self._values.get("allowed_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) List of security groups that are allowed to access the API Gateway.

        Only works for private API Gateways with {@link allowedVpc}.

        :stability: experimental
        '''
        result = self._values.get("allowed_security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def allowed_vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) Create a private API Gateway and allow access from the specified VPC.

        :stability: experimental
        '''
        result = self._values.get("allowed_vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    @builtins.property
    def allowed_vpc_endpoints(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint"]]:
        '''(experimental) Create a private API Gateway and allow access from the specified VPC endpoints.

        Use this to make use of existing VPC endpoints or to share an endpoint between multiple functions. The VPC endpoint must point to ``ec2.InterfaceVpcEndpointAwsService.APIGATEWAY``.

        No other settings are supported when using this option.

        All endpoints will be allowed access, but only the first one will be used as the URL by the runner system for setting up the webhook, and as setup URL.

        :stability: experimental
        '''
        result = self._values.get("allowed_vpc_endpoints")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiGatewayAccessProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Architecture(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.Architecture",
):
    '''(experimental) CPU architecture enum for an image.

    :stability: experimental
    '''

    @jsii.member(jsii_name="instanceTypeMatch")
    def instance_type_match(
        self,
        instance_type: "_aws_cdk_aws_ec2_ceddda9d.InstanceType",
    ) -> builtins.bool:
        '''(experimental) Checks if a given EC2 instance type matches this architecture.

        :param instance_type: instance type to check.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__197fbc91031fbef228119c4ea4b7d54d7ee7ae2efdfedf7354f2313378ee5db9)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
        return typing.cast(builtins.bool, jsii.invoke(self, "instanceTypeMatch", [instance_type]))

    @jsii.member(jsii_name="is")
    def is_(self, arch: "Architecture") -> builtins.bool:
        '''(experimental) Checks if the given architecture is the same as this one.

        :param arch: architecture to compare.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8c78353047f5b727c68147df5fbcc6c4d5381f43b731bacf43f3e3ec823bc835)
            check_type(argname="argument arch", value=arch, expected_type=type_hints["arch"])
        return typing.cast(builtins.bool, jsii.invoke(self, "is", [arch]))

    @jsii.member(jsii_name="isIn")
    def is_in(self, arches: typing.Sequence["Architecture"]) -> builtins.bool:
        '''(experimental) Checks if this architecture is in a given list.

        :param arches: architectures to check.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__41cf6bb0c2118d6cb7d082b7e678fba3dae1f5b8812776005eef7b14eb285e06)
            check_type(argname="argument arches", value=arches, expected_type=type_hints["arches"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isIn", [arches]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ARM64")
    @builtins.classmethod
    def ARM64(cls) -> "Architecture":
        '''(experimental) ARM64.

        :stability: experimental
        '''
        return typing.cast("Architecture", jsii.sget(cls, "ARM64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="X86_64")
    @builtins.classmethod
    def X86_64(cls) -> "Architecture":
        '''(experimental) X86_64.

        :stability: experimental
        '''
        return typing.cast("Architecture", jsii.sget(cls, "X86_64"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.AwsImageBuilderRunnerImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "ami_tags": "amiTags",
        "fast_launch_options": "fastLaunchOptions",
        "instance_type": "instanceType",
        "storage_size": "storageSize",
    },
)
class AwsImageBuilderRunnerImageBuilderProps:
    def __init__(
        self,
        *,
        ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        fast_launch_options: typing.Optional[typing.Union["FastLaunchOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
    ) -> None:
        '''
        :param ami_tags: (experimental) Additional tags to apply to the AMI built by this builder. These additional tags are set on top of ``Name``, ``GitHubRunners:Stack``, and ``GitHubRunners:Builder``. You may override the built-in tags. Overriding ``GitHubRunners:Stack`` will stop old AMIs from being deleted, as the image cleaner is only allowed to touch AMIs tagged with the name of the stack it lives in. You will have to delete those AMIs yourself. Default: no additional tags
        :param fast_launch_options: (experimental) Options for fast launch. This is only supported for Windows AMIs. Default: disabled
        :param instance_type: (experimental) The instance type used to build the image. Default: m6i.large
        :param storage_size: (experimental) Size of volume available for builder instances. This modifies the boot volume size and doesn't add any additional volumes. Use this if you're building images with big components and need more space. Default: default size for AMI (usually 30GB for Linux and 50GB for Windows)

        :stability: experimental
        '''
        if isinstance(fast_launch_options, dict):
            fast_launch_options = FastLaunchOptions(**fast_launch_options)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fe17585d38b67015c3f03db2aefab095f171e0e0900c9a4564679bbc5a29fd07)
            check_type(argname="argument ami_tags", value=ami_tags, expected_type=type_hints["ami_tags"])
            check_type(argname="argument fast_launch_options", value=fast_launch_options, expected_type=type_hints["fast_launch_options"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument storage_size", value=storage_size, expected_type=type_hints["storage_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ami_tags is not None:
            self._values["ami_tags"] = ami_tags
        if fast_launch_options is not None:
            self._values["fast_launch_options"] = fast_launch_options
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if storage_size is not None:
            self._values["storage_size"] = storage_size

    @builtins.property
    def ami_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional tags to apply to the AMI built by this builder.

        These additional tags are set on top of ``Name``, ``GitHubRunners:Stack``, and ``GitHubRunners:Builder``.
        You may override the built-in tags.

        Overriding ``GitHubRunners:Stack`` will stop old AMIs from being deleted, as the image cleaner is only allowed to touch AMIs tagged with the name
        of the stack it lives in. You will have to delete those AMIs yourself.

        :default: no additional tags

        :stability: experimental
        '''
        result = self._values.get("ami_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def fast_launch_options(self) -> typing.Optional["FastLaunchOptions"]:
        '''(experimental) Options for fast launch.

        This is only supported for Windows AMIs.

        :default: disabled

        :stability: experimental
        '''
        result = self._values.get("fast_launch_options")
        return typing.cast(typing.Optional["FastLaunchOptions"], result)

    @builtins.property
    def instance_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"]:
        '''(experimental) The instance type used to build the image.

        :default: m6i.large

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"], result)

    @builtins.property
    def storage_size(self) -> typing.Optional["_aws_cdk_ceddda9d.Size"]:
        '''(experimental) Size of volume available for builder instances. This modifies the boot volume size and doesn't add any additional volumes.

        Use this if you're building images with big components and need more space.

        :default: default size for AMI (usually 30GB for Linux and 50GB for Windows)

        :stability: experimental
        '''
        result = self._values.get("storage_size")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Size"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsImageBuilderRunnerImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BaseContainerImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.BaseContainerImage",
):
    '''(experimental) Represents a base container image that is used to start from in EC2 Image Builder container builds.

    This class is adapted from AWS CDK's BaseContainerImage class to support both string and object inputs.

    :stability: experimental
    '''

    def __init__(
        self,
        image: builtins.str,
        ecr_repository: typing.Optional["_aws_cdk_aws_ecr_ceddda9d.IRepository"] = None,
    ) -> None:
        '''
        :param image: -
        :param ecr_repository: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e5ca7a21f04340348e57cd58a15361581ca48a96701cd63cf51deda7f8667556)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument ecr_repository", value=ecr_repository, expected_type=type_hints["ecr_repository"])
        jsii.create(self.__class__, self, [image, ecr_repository])

    @jsii.member(jsii_name="fromDockerHub")
    @builtins.classmethod
    def from_docker_hub(
        cls,
        repository: builtins.str,
        tag: builtins.str,
    ) -> "BaseContainerImage":
        '''(experimental) The DockerHub image to use as the base image in a container recipe.

        :param repository: The DockerHub repository where the base image resides in.
        :param tag: The tag of the base image in the DockerHub repository.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__620793aa1b875f75c7470562ba65c023ae388e946b5d0838efb942f1d7cf8b36)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromDockerHub", [repository, tag]))

    @jsii.member(jsii_name="fromEcr")
    @builtins.classmethod
    def from_ecr(
        cls,
        repository: "_aws_cdk_aws_ecr_ceddda9d.IRepository",
        tag: builtins.str,
    ) -> "BaseContainerImage":
        '''(experimental) The ECR container image to use as the base image in a container recipe.

        :param repository: The ECR repository where the base image resides in.
        :param tag: The tag of the base image in the ECR repository.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__43f0cdd27fd11637348a57bb1963032374a83f6897e036810baf1225a25a5e22)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromEcr", [repository, tag]))

    @jsii.member(jsii_name="fromEcrPublic")
    @builtins.classmethod
    def from_ecr_public(
        cls,
        registry_alias: builtins.str,
        repository_name: builtins.str,
        tag: builtins.str,
    ) -> "BaseContainerImage":
        '''(experimental) The ECR public container image to use as the base image in a container recipe.

        :param registry_alias: The alias of the ECR public registry where the base image resides in.
        :param repository_name: The name of the ECR public repository, where the base image resides in.
        :param tag: The tag of the base image in the ECR public repository.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__10cac37db8e7f02b74225b02cd0840bcae90a82f4cf6d4b57a31b759c7fef50e)
            check_type(argname="argument registry_alias", value=registry_alias, expected_type=type_hints["registry_alias"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromEcrPublic", [registry_alias, repository_name, tag]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(
        cls,
        base_container_image_string: builtins.str,
    ) -> "BaseContainerImage":
        '''(experimental) The string value of the base image to use in a container recipe.

        This can be an EC2 Image Builder image ARN,
        an ECR or ECR public image, or a container URI sourced from a third-party container registry such as DockerHub.

        :param base_container_image_string: The base image as a direct string value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6665a984629ccf7e97837a416fca7b6eb45d677e2251c373e856609e48b13ddc)
            check_type(argname="argument base_container_image_string", value=base_container_image_string, expected_type=type_hints["base_container_image_string"])
        return typing.cast("BaseContainerImage", jsii.sinvoke(cls, "fromString", [base_container_image_string]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        '''(experimental) The rendered base image to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="ecrRepository")
    def ecr_repository(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ecr_ceddda9d.IRepository"]:
        '''(experimental) The ECR repository if this image was created from an ECR repository.

        This allows automatic permission granting for CodeBuild.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["_aws_cdk_aws_ecr_ceddda9d.IRepository"], jsii.get(self, "ecrRepository"))


class BaseImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.BaseImage",
):
    '''(experimental) Represents a base image that is used to start from in EC2 Image Builder image builds.

    This class is adapted from AWS CDK's BaseImage class to support both string and object inputs.

    :stability: experimental
    '''

    def __init__(self, image: builtins.str) -> None:
        '''
        :param image: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__76b6e1f1beb455f020318f40620cdc5da6eb91ef685f4b19f3ee1b82244571b9)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        jsii.create(self.__class__, self, [image])

    @jsii.member(jsii_name="fromAmiId")
    @builtins.classmethod
    def from_ami_id(cls, ami_id: builtins.str) -> "BaseImage":
        '''(experimental) The AMI ID to use as a base image in an image recipe.

        :param ami_id: The AMI ID to use as the base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1ce8e58d909a9b0733dd3a845ef1cbf1c6f1d57d6a28e030f5122f6a07ea226a)
            check_type(argname="argument ami_id", value=ami_id, expected_type=type_hints["ami_id"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromAmiId", [ami_id]))

    @jsii.member(jsii_name="fromGpuBase")
    @builtins.classmethod
    def from_gpu_base(cls, os: "Os", architecture: "Architecture") -> "BaseImage":
        '''(experimental) A base AMI with NVIDIA drivers pre-installed for GPU workloads.

        Uses AWS Deep Learning AMIs for Linux (Ubuntu, Amazon Linux 2, Amazon Linux 2023).
        For Windows, subscribe to NVIDIA RTX Virtual Workstation in AWS Marketplace, then use
        {@link fromMarketplaceProductId} with the product ID.

        :param os: Target operating system.
        :param architecture: Target architecture.

        :stability: experimental
        :throws: Error if the OS/architecture combo has no GPU base AMI
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1e40fcd49321d7aa1d4140157d8bd6ef6e3c6daab5371fccf4772418206bb924)
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromGpuBase", [os, architecture]))

    @jsii.member(jsii_name="fromImageBuilder")
    @builtins.classmethod
    def from_image_builder(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        resource_name: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> "BaseImage":
        '''(experimental) An AWS-provided EC2 Image Builder image to use as a base image in an image recipe.

        This constructs an Image Builder ARN for AWS-provided images like ``ubuntu-server-22-lts-x86/x.x.x``.

        :param scope: The construct scope (used to determine the stack and region).
        :param resource_name: The Image Builder resource name pattern (e.g., ``ubuntu-server-22-lts-x86`` or ``ubuntu-server-22-lts-${arch}``).
        :param version: The version pattern (defaults to ``x.x.x`` to use the latest version).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8ca0f086c8fe6ceed61893dace3f2a63221659b4f2dc8deac5e079c2af594c81)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromImageBuilder", [scope, resource_name, version]))

    @jsii.member(jsii_name="fromMarketplaceProductId")
    @builtins.classmethod
    def from_marketplace_product_id(cls, product_id: builtins.str) -> "BaseImage":
        '''(experimental) The marketplace product ID for an AMI product to use as the base image in an image recipe.

        :param product_id: The Marketplace AMI product ID to use as the base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__11d91f35f8cfaaa28eff924e8b02b89309fd30277e590963e62e2df9156c61c0)
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromMarketplaceProductId", [product_id]))

    @jsii.member(jsii_name="fromSsmParameter")
    @builtins.classmethod
    def from_ssm_parameter(
        cls,
        parameter: "_aws_cdk_aws_ssm_ceddda9d.IParameter",
    ) -> "BaseImage":
        '''(experimental) The SSM parameter to use as the base image in an image recipe.

        :param parameter: The SSM parameter to use as the base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cdc5733de6656116c12830996cd2873ef94eb2660f3f56e15095618f20dae9e1)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromSsmParameter", [parameter]))

    @jsii.member(jsii_name="fromSsmParameterName")
    @builtins.classmethod
    def from_ssm_parameter_name(cls, parameter_name: builtins.str) -> "BaseImage":
        '''(experimental) The parameter name for the SSM parameter to use as the base image in an image recipe.

        :param parameter_name: The name of the SSM parameter to use as the base image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__abe4dd96225df8b7acceff4f4de111f9de9838f83919100fb917661d9f67b53f)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromSsmParameterName", [parameter_name]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, base_image_string: builtins.str) -> "BaseImage":
        '''(experimental) The direct string value of the base image to use in an image recipe.

        This can be an EC2 Image Builder image ARN,
        an SSM parameter, an AWS Marketplace product ID, or an AMI ID.

        :param base_image_string: The base image as a direct string value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bbc9be4cd1f85f2aa04be945d8d5ccfb305101c54ea34109a6bc600e8af9dd00)
            check_type(argname="argument base_image_string", value=base_image_string, expected_type=type_hints["base_image_string"])
        return typing.cast("BaseImage", jsii.sinvoke(cls, "fromString", [base_image_string]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        '''(experimental) The rendered base image to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "image"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "dockerfile_path": "dockerfilePath",
        "architecture": "architecture",
        "build_image": "buildImage",
        "compute_type": "computeType",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "os": "os",
        "rebuild_interval": "rebuildInterval",
        "runner_version": "runnerVersion",
        "security_group": "securityGroup",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class CodeBuildImageBuilderProps:
    def __init__(
        self,
        *,
        dockerfile_path: builtins.str,
        architecture: typing.Optional["Architecture"] = None,
        build_image: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.IBuildImage"] = None,
        compute_type: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''(experimental) Properties for CodeBuildImageBuilder construct.

        :param dockerfile_path: (experimental) Path to Dockerfile to be built. It can be a path to a Dockerfile, a folder containing a Dockerfile, or a zip file containing a Dockerfile.
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param build_image: (experimental) Build image to use in CodeBuild. This is the image that's going to run the code that builds the runner image. The only action taken in CodeBuild is running ``docker build``. You would therefore not need to change this setting often. Default: Ubuntu 22.04 for x64 and Amazon Linux 2 for ARM64
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: {@link ComputeType#SMALL }
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (experimental) Security Group to assign to this instance. Default: public project with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to build the image in. Default: no VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3489f112da2cf966956bd19d9d323a5acba9732c6207773bb9b29c93cf407444)
            check_type(argname="argument dockerfile_path", value=dockerfile_path, expected_type=type_hints["dockerfile_path"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument build_image", value=build_image, expected_type=type_hints["build_image"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument rebuild_interval", value=rebuild_interval, expected_type=type_hints["rebuild_interval"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dockerfile_path": dockerfile_path,
        }
        if architecture is not None:
            self._values["architecture"] = architecture
        if build_image is not None:
            self._values["build_image"] = build_image
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if os is not None:
            self._values["os"] = os
        if rebuild_interval is not None:
            self._values["rebuild_interval"] = rebuild_interval
        if runner_version is not None:
            self._values["runner_version"] = runner_version
        if security_group is not None:
            self._values["security_group"] = security_group
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def dockerfile_path(self) -> builtins.str:
        '''(experimental) Path to Dockerfile to be built.

        It can be a path to a Dockerfile, a folder containing a Dockerfile, or a zip file containing a Dockerfile.

        :stability: experimental
        '''
        result = self._values.get("dockerfile_path")
        assert result is not None, "Required property 'dockerfile_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional["Architecture"]:
        '''(experimental) Image architecture.

        :default: Architecture.X86_64

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional["Architecture"], result)

    @builtins.property
    def build_image(
        self,
    ) -> typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.IBuildImage"]:
        '''(experimental) Build image to use in CodeBuild.

        This is the image that's going to run the code that builds the runner image.

        The only action taken in CodeBuild is running ``docker build``. You would therefore not need to change this setting often.

        :default: Ubuntu 22.04 for x64 and Amazon Linux 2 for ARM64

        :stability: experimental
        '''
        result = self._values.get("build_image")
        return typing.cast(typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.IBuildImage"], result)

    @builtins.property
    def compute_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"]:
        '''(experimental) The type of compute to use for this build.

        See the {@link ComputeType} enum for the possible values.

        :default: {@link ComputeType#SMALL }

        :stability: experimental
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Removal policy for logs of image builds.

        If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed.

        We try to not leave anything behind when removed. But sometimes a log staying behind is useful.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def os(self) -> typing.Optional["Os"]:
        '''(experimental) Image OS.

        :default: OS.LINUX

        :stability: experimental
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional["Os"], result)

    @builtins.property
    def rebuild_interval(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) Schedule the image to be rebuilt every given interval.

        Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates.

        Set to zero to disable.

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("rebuild_interval")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def runner_version(self) -> typing.Optional["RunnerVersion"]:
        '''(experimental) Version of GitHub Runners to install.

        :default: latest version available

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        return typing.cast(typing.Optional["RunnerVersion"], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(experimental) Security Group to assign to this instance.

        :default: public project with no security group

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        :default: Duration.hours(1)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC to build the image in.

        :default: no VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildRunnerImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "build_image": "buildImage",
        "compute_type": "computeType",
        "timeout": "timeout",
    },
)
class CodeBuildRunnerImageBuilderProps:
    def __init__(
        self,
        *,
        build_image: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.IBuildImage"] = None,
        compute_type: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
    ) -> None:
        '''
        :param build_image: (experimental) Build image to use in CodeBuild. This is the image that's going to run the code that builds the runner image. The only action taken in CodeBuild is running ``docker build``. You would therefore not need to change this setting often. Default: Amazon Linux 2023
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. The compute type determines CPU, memory, and disk space: - SMALL: 2 vCPU, 3 GB RAM, 64 GB disk - MEDIUM: 4 vCPU, 7 GB RAM, 128 GB disk - LARGE: 8 vCPU, 15 GB RAM, 128 GB disk - X2_LARGE: 72 vCPU, 145 GB RAM, 256 GB disk (Linux) or 824 GB disk (Windows) Use a larger compute type when you need more disk space for building larger Docker images. For more details, see https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types Default: {@link ComputeType#SMALL }
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__57eba0e804792fea32cbb8b094226d90afd105dd84432bb9e2d32380259a548f)
            check_type(argname="argument build_image", value=build_image, expected_type=type_hints["build_image"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_image is not None:
            self._values["build_image"] = build_image
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def build_image(
        self,
    ) -> typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.IBuildImage"]:
        '''(experimental) Build image to use in CodeBuild.

        This is the image that's going to run the code that builds the runner image.

        The only action taken in CodeBuild is running ``docker build``. You would therefore not need to change this setting often.

        :default: Amazon Linux 2023

        :stability: experimental
        '''
        result = self._values.get("build_image")
        return typing.cast(typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.IBuildImage"], result)

    @builtins.property
    def compute_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"]:
        '''(experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values.

        The compute type determines CPU, memory, and disk space:

        - SMALL: 2 vCPU, 3 GB RAM, 64 GB disk
        - MEDIUM: 4 vCPU, 7 GB RAM, 128 GB disk
        - LARGE: 8 vCPU, 15 GB RAM, 128 GB disk
        - X2_LARGE: 72 vCPU, 145 GB RAM, 256 GB disk (Linux) or 824 GB disk (Windows)

        Use a larger compute type when you need more disk space for building larger Docker images.

        For more details, see https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types

        :default: {@link ComputeType#SMALL }

        :stability: experimental
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        :default: Duration.hours(1)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildRunnerImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CompositeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.CompositeProvider",
):
    '''(experimental) A composite runner provider that implements fallback and distribution strategies.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="distribute")
    @builtins.classmethod
    def distribute(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        weighted_providers: typing.Sequence[typing.Union["WeightedRunnerProvider", typing.Dict[builtins.str, typing.Any]]],
    ) -> "ICompositeProvider":
        '''(experimental) Creates a weighted distribution runner provider that randomly selects a provider based on weights.

        For example, given providers A (weight 10), B (weight 20), C (weight 30):

        - Total weight = 60
        - Probability of selecting A = 10/60 = 16.67%
        - Probability of selecting B = 20/60 = 33.33%
        - Probability of selecting C = 30/60 = 50%

        You can use this to distribute load across multiple instance types or availability zones.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID.
        :param weighted_providers: List of weighted runner providers.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__77c19894684d852504fe0fe078d55632b0435f3c901fffef944cc34438533639)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument weighted_providers", value=weighted_providers, expected_type=type_hints["weighted_providers"])
        return typing.cast("ICompositeProvider", jsii.sinvoke(cls, "distribute", [scope, id, weighted_providers]))

    @jsii.member(jsii_name="fallback")
    @builtins.classmethod
    def fallback(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        providers: typing.Sequence["IRunnerProvider"],
    ) -> "ICompositeProvider":
        '''(experimental) Creates a fallback runner provider that tries each provider in order until one succeeds.

        For example, given providers A, B, C:

        - Try A first
        - If A fails, try B
        - If B fails, try C

        You can use this to try spot instance first, and switch to on-demand instances if spot is unavailable.

        Or you can use this to try different instance types in order of preference.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID.
        :param providers: List of runner providers to try in order.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4f6d940901d7f617b4a15476433bf716e52ca4bd1c63e38d17294ec861fa0a12)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
        return typing.cast("ICompositeProvider", jsii.sinvoke(cls, "fallback", [scope, id, providers]))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ContainerImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "instance_type": "instanceType",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "os": "os",
        "parent_image": "parentImage",
        "rebuild_interval": "rebuildInterval",
        "runner_version": "runnerVersion",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class ContainerImageBuilderProps:
    def __init__(
        self,
        *,
        architecture: typing.Optional["Architecture"] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        parent_image: typing.Optional[builtins.str] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''(experimental) Properties for ContainerImageBuilder construct.

        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param instance_type: (experimental) The instance type used to build the image. Default: m6i.large
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param parent_image: (experimental) Parent image for the new Docker Image. You can use either Image Builder image ARN or public registry image. Default: 'mcr.microsoft.com/windows/servercore:ltsc2019-amd64'
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (deprecated) Security group to assign to launched builder instances. Default: new security group
        :param security_groups: (experimental) Security groups to assign to launched builder instances. Default: new security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: default VPC subnet
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b7b6832b84987dee7e16a1e7bde046b812c75e74a268cb3fbf2685d3fe25115c)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument parent_image", value=parent_image, expected_type=type_hints["parent_image"])
            check_type(argname="argument rebuild_interval", value=rebuild_interval, expected_type=type_hints["rebuild_interval"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if os is not None:
            self._values["os"] = os
        if parent_image is not None:
            self._values["parent_image"] = parent_image
        if rebuild_interval is not None:
            self._values["rebuild_interval"] = rebuild_interval
        if runner_version is not None:
            self._values["runner_version"] = runner_version
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def architecture(self) -> typing.Optional["Architecture"]:
        '''(experimental) Image architecture.

        :default: Architecture.X86_64

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional["Architecture"], result)

    @builtins.property
    def instance_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"]:
        '''(experimental) The instance type used to build the image.

        :default: m6i.large

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Removal policy for logs of image builds.

        If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed.

        We try to not leave anything behind when removed. But sometimes a log staying behind is useful.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def os(self) -> typing.Optional["Os"]:
        '''(experimental) Image OS.

        :default: OS.LINUX

        :stability: experimental
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional["Os"], result)

    @builtins.property
    def parent_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Parent image for the new Docker Image.

        You can use either Image Builder image ARN or public registry image.

        :default: 'mcr.microsoft.com/windows/servercore:ltsc2019-amd64'

        :stability: experimental
        '''
        result = self._values.get("parent_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rebuild_interval(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) Schedule the image to be rebuilt every given interval.

        Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates.

        Set to zero to disable.

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("rebuild_interval")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def runner_version(self) -> typing.Optional["RunnerVersion"]:
        '''(experimental) Version of GitHub Runners to install.

        :default: latest version available

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        return typing.cast(typing.Optional["RunnerVersion"], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(deprecated) Security group to assign to launched builder instances.

        :default: new security group

        :deprecated: use {@link securityGroups }

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security groups to assign to launched builder instances.

        :default: new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: default VPC subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC to launch the runners in.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.FastLaunchOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "max_parallel_launches": "maxParallelLaunches",
        "target_resource_count": "targetResourceCount",
    },
)
class FastLaunchOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        max_parallel_launches: typing.Optional[jsii.Number] = None,
        target_resource_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for fast launch.

        :param enabled: (experimental) Enable fast launch for AMIs generated by this builder. It creates a snapshot of the root volume and uses it to launch new instances faster. This is only supported for Windows AMIs. Default: false
        :param max_parallel_launches: (experimental) The maximum number of parallel instances that are launched for creating resources. Must be at least 6. Default: 6
        :param target_resource_count: (experimental) The number of pre-provisioned snapshots to keep on hand for a fast-launch enabled Windows AMI. Default: 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d2952ae322a0fd40b480084b183be9e7179337af84efb30a496aa331a22fa562)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_parallel_launches", value=max_parallel_launches, expected_type=type_hints["max_parallel_launches"])
            check_type(argname="argument target_resource_count", value=target_resource_count, expected_type=type_hints["target_resource_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_parallel_launches is not None:
            self._values["max_parallel_launches"] = max_parallel_launches
        if target_resource_count is not None:
            self._values["target_resource_count"] = target_resource_count

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable fast launch for AMIs generated by this builder.

        It creates a snapshot of the root volume and uses it to launch new instances faster.

        This is only supported for Windows AMIs.

        :default: false

        :stability: experimental
        :note: enabling fast launch on an existing builder will not enable it for existing AMIs. It will only affect new AMIs. If you want immediate effect, trigger a new image build. Alternatively, you can create a new builder with fast launch enabled and use it for new AMIs.
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_parallel_launches(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of parallel instances that are launched for creating resources.

        Must be at least 6.

        :default: 6

        :stability: experimental
        '''
        result = self._values.get("max_parallel_launches")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_resource_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of pre-provisioned snapshots to keep on hand for a fast-launch enabled Windows AMI.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("target_resource_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FastLaunchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IConnectable)
class GitHubRunners(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.GitHubRunners",
):
    '''(experimental) Create all the required infrastructure to provide self-hosted GitHub runners.

    It creates a webhook, secrets, and a step function to orchestrate all runs. Secrets are not automatically filled. See README.md for instructions on how to setup GitHub integration.

    By default, this will create a runner provider of each available type with the defaults. This is good enough for the initial setup stage when you just want to get GitHub integration working::

       new GitHubRunners(this, 'runners');

    Usually you'd want to configure the runner providers so the runners can run in a certain VPC or have certain permissions::

       const vpc = ec2.Vpc.fromLookup(this, 'vpc', { vpcId: 'vpc-1234567' });
       const runnerSg = new ec2.SecurityGroup(this, 'runner security group', { vpc: vpc });
       const dbSg = ec2.SecurityGroup.fromSecurityGroupId(this, 'database security group', 'sg-1234567');
       const bucket = new s3.Bucket(this, 'runner bucket');

       // create a custom CodeBuild provider
       const myProvider = new CodeBuildRunnerProvider(
         this, 'codebuild runner',
         {
            labels: ['my-codebuild'],
            vpc: vpc,
            securityGroups: [runnerSg],
         },
       );
       // grant some permissions to the provider
       bucket.grantReadWrite(myProvider);
       dbSg.connections.allowFrom(runnerSg, ec2.Port.tcp(3306), 'allow runners to connect to MySQL database');

       // create the runner infrastructure
       new GitHubRunners(
         this,
         'runners',
         {
           providers: [myProvider],
         }
       );

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        extra_certificates: typing.Optional[builtins.str] = None,
        idle_timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        log_options: typing.Optional[typing.Union["LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        providers: typing.Optional[typing.Sequence[typing.Union["IRunnerProvider", "ICompositeProvider"]]] = None,
        provider_selector: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IFunction"] = None,
        require_self_hosted_label: typing.Optional[builtins.bool] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        setup_access: typing.Optional["LambdaAccess"] = None,
        status_access: typing.Optional["LambdaAccess"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        vpc_subnets: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_access: typing.Optional["LambdaAccess"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allow_public_subnet: (experimental) Allow management functions to run in public subnets. Lambda Functions in a public subnet can NOT access the internet. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting. Default: false
        :param extra_certificates: (experimental) Path to a certificate file (.pem or .crt) or a directory containing certificate files (.pem or .crt) required to trust GitHub Enterprise Server. Use this when GitHub Enterprise Server certificates are self-signed. If a directory is provided, all .pem and .crt files in that directory will be used. The certificates will be concatenated into a single file for use by Node.js. You may also want to use custom images for your runner providers that contain the same certificates. See {@link RunnerImageComponent.extraCertificates }:: const selfSignedCertificates = 'certs/ghes.pem'; // or 'path-to-my-extra-certs-folder' for a directory const imageBuilder = CodeBuildRunnerProvider.imageBuilder(this, 'Image Builder with Certs'); imageBuilder.addComponent(RunnerImageComponent.extraCertificates(selfSignedCertificates, 'private-ca')); const provider = new CodeBuildRunnerProvider(this, 'CodeBuild', { imageBuilder: imageBuilder, }); new GitHubRunners( this, 'runners', { providers: [provider], extraCertificates: selfSignedCertificates, } );
        :param idle_timeout: (experimental) Time to wait before stopping a runner that remains idle. If the user cancelled the job, or if another runner stole it, this stops the runner to avoid wasting resources. Default: 5 minutes
        :param log_options: (experimental) Logging options for the state machine that manages the runners. Default: no logs
        :param providers: (experimental) List of runner providers to use. At least one provider is required. Provider will be selected when its label matches the labels requested by the workflow job. Default: CodeBuild, Lambda and Fargate runners with all the defaults (no VPC or default account VPC)
        :param provider_selector: (experimental) Optional Lambda function to customize provider selection logic and label assignment. - The function receives the webhook payload along with default provider and its labels as {@link ProviderSelectorInput } - The function returns a selected provider and its labels as {@link ProviderSelectorResult } - You can decline to provision a runner by returning undefined as the provider in the selector result - You can fully customize the labels for the about-to-be-provisioned runner (add, remove, modify, dynamic labels, etc.) - Labels don't have to match the labels originally configured for the provider, but see warnings below - This function will be called synchronously during webhook processing, so it should be fast and efficient (webhook limit is 30 seconds total) **WARNING: It is your responsibility to ensure the selected provider's labels match the job's required labels. If you return the wrong labels, the runner will be created but GitHub Actions will not assign the job to it.** **WARNING: Provider selection is not a guarantee that a specific provider will be assigned for the job. GitHub Actions may assign the job to any runner with matching labels. The provider selector only determines which provider's runner will be *created*, but GitHub Actions may route the job to any available runner with the required labels.** **For reliable provider assignment based on job characteristics, consider using repo-level runner registration where you can control which runners are available for specific repositories. This information is also available while using the setup wizard.
        :param require_self_hosted_label: (experimental) Whether to require the ``self-hosted`` label. If ``true``, the runner will only start if the workflow job explicitly requests the ``self-hosted`` label. Be careful when setting this to ``false``. Avoid setting up providers with generic label requirements like ``linux`` as they may match workflows that are not meant to run on self-hosted runners. Default: true
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. GitHub jobs time out after not being able to get a runner for 24 hours. You should not retry for more than 24 hours. Retries use full jitter, so total time spent waiting is about half the sum of min(interval * backoffRate ^ attempt, maxDelay) over all attempts. Default: retry 210 times over a bit more than 24 hours
        :param security_group: (deprecated) Security group attached to all management functions. Use this with to provide access to GitHub Enterprise Server hosted inside a VPC. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting.
        :param security_groups: (experimental) Security groups attached to all management functions. Use this to provide outbound access from management functions to GitHub Enterprise Server hosted inside a VPC. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting. **Note:** Defining inbound rules on this security group does nothing. This security group only controls outbound access FROM the management functions. To limit access TO the webhook or setup functions, use {@link webhookAccess} and {@link setupAccess} instead.
        :param setup_access: (experimental) Access configuration for the setup function. Once you finish the setup process, you can set this to ``LambdaAccess.noAccess()`` to remove access to the setup function. You can also use ``LambdaAccess.apiGateway({ allowedIps: ['my-ip/0']})`` to limit access to your IP only. Default: LambdaAccess.lambdaUrl()
        :param status_access: (experimental) Access configuration for the status function. This function returns a lot of sensitive information about the runner, so you should only allow access to it from trusted IPs, if at all. Default: LambdaAccess.noAccess()
        :param vpc: (experimental) VPC used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting and will run outside the VPC. Make sure the selected VPC and subnets have access to the following with either NAT Gateway or VPC Endpoints: - GitHub Enterprise Server - Secrets Manager - SQS - Step Functions - CloudFormation (status function only) - EC2 - ECR (status function only)
        :param vpc_subnets: (experimental) VPC subnets used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting.
        :param webhook_access: (experimental) Access configuration for the webhook function. This function is called by GitHub when a new workflow job is scheduled. For an extra layer of security, you can set this to ``LambdaAccess.apiGateway({ allowedIps: LambdaAccess.githubWebhookIps() })``. You can also set this to ``LambdaAccess.apiGateway({allowedVpc: vpc, allowedIps: ['GHES.IP.ADDRESS/32']})`` if your GitHub Enterprise Server is hosted in a VPC. This will create an API Gateway endpoint that's only accessible from within the VPC. *WARNING*: changing access type may change the URL. When the URL changes, you must update GitHub as well. Default: LambdaAccess.lambdaUrl()

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c1a45de07d09ed9f4fd0b9051aeff4571ceda633f49c0b30a5058ad6d72fad18)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubRunnersProps(
            allow_public_subnet=allow_public_subnet,
            extra_certificates=extra_certificates,
            idle_timeout=idle_timeout,
            log_options=log_options,
            providers=providers,
            provider_selector=provider_selector,
            require_self_hosted_label=require_self_hosted_label,
            retry_options=retry_options,
            security_group=security_group,
            security_groups=security_groups,
            setup_access=setup_access,
            status_access=status_access,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            webhook_access=webhook_access,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createDashboard")
    def create_dashboard(
        self,
        name: typing.Optional[builtins.str] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard":
        '''(experimental) Creates a CloudWatch dashboard with the metrics you need to know if your runners are healthy.

        It's split into sections, each with a short explanation of what its numbers mean and which ones to watch:

        - **Jobs**: are jobs running and passing, and which runner is failing them?
        - **Runners**: do runners start, how long do they take (and therefore cost), and why do they fail to start?
        - **Runner assignment**: are runners taken by jobs they weren't started for, do jobs match more than one provider, and why
          were runners stopped before getting a job?
        - **Management functions (orchestration)**: is GitHub reaching the webhook, and is any of our code failing?

        **WARNING:** this method calls {@link metricJobCompleted}, {@link metricStolenRunners}, {@link metricStoppedRunners} and
        {@link metricJobsMatchingMultipleProviders} which create metric filters. These resources may incur cost.

        This dashboard is very basic. Pull requests and issues are welcome to improve it.

        :param name: Name of the dashboard. Defaults to "GitHub-Runners".

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c6c824929ac2b172d81f1ca6d3f77b08aca419fe4769d0c13dc162a760e13372)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.Dashboard", jsii.invoke(self, "createDashboard", [name]))

    @jsii.member(jsii_name="createLogsInsightsQueries")
    def create_logs_insights_queries(
        self,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Creates CloudWatch Logs Insights saved queries that can be used to debug issues with the runners.

        - "Webhook errors" helps diagnose configuration issues with GitHub integration
        - "Ignored webhook" helps understand why runners aren't started
        - "Ignored jobs based on labels" helps debug label matching issues
        - "Webhook started runners" helps understand which runners were started
        - "Jobs matching multiple providers" lists jobs that need more labels so they match only one provider
        - "Warm runner status" and "Warm runner errors" (when warm runners are configured)

        :param prefix: Prefix for the query definitions. Defaults to "GitHub Runners".

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e3d8d4287a56d393e1fe438a511f3c5c95bcb80987e93de575d61fc0507cb7f1)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast(None, jsii.invoke(self, "createLogsInsightsQueries", [prefix]))

    @jsii.member(jsii_name="failedImageBuildsTopic")
    def failed_image_builds_topic(
        self,
        scope: typing.Optional["_constructs_77d1e7e8.Construct"] = None,
    ) -> "_aws_cdk_aws_sns_ceddda9d.Topic":
        '''(experimental) Creates a topic for notifications when a runner image build fails.

        Runner images are rebuilt every week by default. This provides the latest GitHub Runner version and software updates.

        If you want to be sure you are using the latest runner version, you can use this topic to be notified when a build fails.

        Email subscribers get a short summary with the failure reason and a link to the logs. Other subscribers get the original
        JSON notification from CodeBuild or EC2 Image Builder.

        When the image builder is defined in a separate stack (e.g. in a split-stacks setup), pass that stack or construct
        as the optional scope so the topic and failure-notification aspects are created in the same stack as the image
        builder. Otherwise the aspects may not find the image builder resources.

        :param scope: Optional scope (e.g. the image builder stack) where the topic and aspects will be created. Defaults to this construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d3bc8ba54eaa33d65a8c2635c32c20406be53589ef1d25e161194a6bcfb3f669)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("_aws_cdk_aws_sns_ceddda9d.Topic", jsii.invoke(self, "failedImageBuildsTopic", [scope]))

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["_aws_cdk_aws_cloudwatch_ceddda9d.Unit"] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.Metric":
        '''(experimental) Metric for failed runner executions.

        A failed runner usually means the runner failed to start and so a job was never executed. It doesn't necessarily mean the job was executed and failed. For that, see {@link metricJobCompleted}.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param id: Unique identifier for this metric when used in dashboard widgets. The id can be used as a variable to represent this metric in math expressions. Valid characters are letters, numbers, and underscore. The first character must be a lowercase letter. Default: - No ID
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param visible: Whether this metric should be visible in dashboard graphs. Setting this to false is useful when you want to hide raw metrics that are used in math expressions, and show only the expression results. Default: true

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            id=id,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
            visible=visible,
        )

        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.Metric", jsii.invoke(self, "metricFailed", [props]))

    @jsii.member(jsii_name="metricJobCompleted")
    def metric_job_completed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["_aws_cdk_aws_cloudwatch_ceddda9d.Unit"] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.Metric":
        '''(experimental) Metric for the number of GitHub Actions jobs completed.

        It has ``ProviderLabels`` and ``Status`` dimensions. The status can be one of "Succeeded", "SucceededWithIssues", "Failed", "Canceled", "Skipped", or "Abandoned".

        **WARNING:** this method creates a metric filter for each provider. Each metric has a status dimension with six possible values. These resources may incur cost.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param id: Unique identifier for this metric when used in dashboard widgets. The id can be used as a variable to represent this metric in math expressions. Valid characters are letters, numbers, and underscore. The first character must be a lowercase letter. Default: - No ID
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param visible: Whether this metric should be visible in dashboard graphs. Setting this to false is useful when you want to hide raw metrics that are used in math expressions, and show only the expression results. Default: true

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            id=id,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
            visible=visible,
        )

        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.Metric", jsii.invoke(self, "metricJobCompleted", [props]))

    @jsii.member(jsii_name="metricJobsMatchingMultipleProviders")
    def metric_jobs_matching_multiple_providers(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["_aws_cdk_aws_cloudwatch_ceddda9d.Unit"] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.Metric":
        '''(experimental) Metric for the number of jobs whose labels matched more than one provider.

        We start a runner from the first matching provider, but GitHub may give such a job a runner from any of them, including one started for
        another job. Stolen runner detection starts another runner for the job left behind, but the job itself may run on a provider you didn't
        expect. Anything over zero means some workflows ask for too few labels. Add labels to those jobs so they match only one provider. Use the
        "Jobs matching multiple providers" CloudWatch Logs Insights query created by {@link createLogsInsightsQueries} to find them.

        Jobs routed by a provider selector are not counted, as the selector picks the provider.

        **WARNING:** this method creates a metric filter. This resource may incur cost.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param id: Unique identifier for this metric when used in dashboard widgets. The id can be used as a variable to represent this metric in math expressions. Valid characters are letters, numbers, and underscore. The first character must be a lowercase letter. Default: - No ID
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param visible: Whether this metric should be visible in dashboard graphs. Setting this to false is useful when you want to hide raw metrics that are used in math expressions, and show only the expression results. Default: true

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            id=id,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
            visible=visible,
        )

        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.Metric", jsii.invoke(self, "metricJobsMatchingMultipleProviders", [props]))

    @jsii.member(jsii_name="metricLambdaErrors")
    def metric_lambda_errors(
        self,
        *,
        color: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        search_account: typing.Optional[builtins.str] = None,
        search_region: typing.Optional[builtins.str] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.MathExpression":
        '''(experimental) Metric for the number of failed invocations of the management Lambda functions.

        These are the functions that handle webhooks, retrieve runner tokens, stop idle runners, replace stolen runners, etc. Anything over zero means
        jobs may not have gotten a runner. You should use this metric to trigger an alarm.

        Only unhandled errors are counted here, as reported by Lambda itself. Errors that are handled and logged, like a webhook with a bad signature,
        are not failed invocations. Use the "Webhook errors" and "Orchestration errors" queries created by {@link createLogsInsightsQueries} to find
        those.

        Management functions created after this method is called are not included. Call it last if you use warm runners.

        :param color: Color for this metric when added to a Graph in a Dashboard. Default: - Automatic color
        :param label: Label for this expression when added to a Graph in a Dashboard. If this expression evaluates to more than one time series (for example, through the use of ``METRICS()`` or ``SEARCH()`` expressions), each time series will appear in the graph using a combination of the expression label and the individual metric label. Specify the empty string (``''``) to suppress the expression label and only keep the metric label. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. If the math expression produces more than one time series, the maximum will be shown for each individual time series produce by this math expression. Default: - Expression value is used as label
        :param period: The period over which the math expression's statistics are applied. This period overrides all periods in the metrics used in this math expression. Default: Duration.minutes(5)
        :param search_account: Account to evaluate search expressions within. Specifying a searchAccount has no effect to the account used for metrics within the expression (passed via usingMetrics). Default: - Deployment account.
        :param search_region: Region to evaluate search expressions within. Specifying a searchRegion has no effect to the region used for metrics within the expression (passed via usingMetrics). Default: - Deployment region.

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MathExpressionOptions(
            color=color,
            label=label,
            period=period,
            search_account=search_account,
            search_region=search_region,
        )

        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.MathExpression", jsii.invoke(self, "metricLambdaErrors", [props]))

    @jsii.member(jsii_name="metricStolenRunners")
    def metric_stolen_runners(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["_aws_cdk_aws_cloudwatch_ceddda9d.Unit"] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.Metric":
        '''(experimental) Metric for the number of runners that were stolen by a job that shouldn't have been assigned to them.

        A high number here means your runners are shared with jobs you didn't mean to serve. Use the "Stolen runners"
        CloudWatch Logs Insights query created by {@link createLogsInsightsQueries} to see which repositories and jobs
        are taking them.

        This metric has two dimensions:

        1. ``Replaced`` which is "true" or "false" indicating whether the stolen runner was replaced. A runner may not be replaced if it was stolen too
           many times in a row. The current limit is 3. When this is false, there is probably a bug in our detection or something misconfigured.
        2. ``Provider`` is the provider construct path of the runner that was stolen. You can check your code to see which labels it has that may cause
           it to be stolen. The logs insights queries can provide even more information about the stolen runners.

        **WARNING:** this method creates a metric filter. This resource may incur cost.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param id: Unique identifier for this metric when used in dashboard widgets. The id can be used as a variable to represent this metric in math expressions. Valid characters are letters, numbers, and underscore. The first character must be a lowercase letter. Default: - No ID
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param visible: Whether this metric should be visible in dashboard graphs. Setting this to false is useful when you want to hide raw metrics that are used in math expressions, and show only the expression results. Default: true

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            id=id,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
            visible=visible,
        )

        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.Metric", jsii.invoke(self, "metricStolenRunners", [props]))

    @jsii.member(jsii_name="metricStoppedRunners")
    def metric_stopped_runners(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["_aws_cdk_aws_cloudwatch_ceddda9d.Unit"] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.Metric":
        '''(experimental) Metric for the number of runners we stopped on purpose before they got a job.

        These step function executions end up as aborted and not failed, so they don't show up in {@link metricFailed}.

        This metric has one dimension, ``Reason``, which is the error the step function was stopped with:

        - ``IdleRunner``: the runner was idle for longer than its idle timeout and was reaped. This is usually a runner whose job was taken by
          another runner, or a job that was canceled before it started.
        - ``StaleWarmRunner``: a warm runner was replaced because its configuration changed.
        - ``WarmRunnerExpired``: a warm runner reached the end of its duration.
        - ``WarmRunnerBadDeadline``: a warm runner had an invalid deadline and was stopped.

        **WARNING:** this method creates a metric filter. This resource may incur cost.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param id: Unique identifier for this metric when used in dashboard widgets. The id can be used as a variable to represent this metric in math expressions. Valid characters are letters, numbers, and underscore. The first character must be a lowercase letter. Default: - No ID
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param visible: Whether this metric should be visible in dashboard graphs. Setting this to false is useful when you want to hide raw metrics that are used in math expressions, and show only the expression results. Default: true

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            id=id,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
            visible=visible,
        )

        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.Metric", jsii.invoke(self, "metricStoppedRunners", [props]))

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["_aws_cdk_aws_cloudwatch_ceddda9d.Unit"] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.Metric":
        '''(experimental) Metric for successful executions.

        A successful execution doesn't always mean a runner was started. It can be successful even without any label matches.

        A successful runner doesn't mean the job it executed was successful. For that, see {@link metricJobCompleted}.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param id: Unique identifier for this metric when used in dashboard widgets. The id can be used as a variable to represent this metric in math expressions. Valid characters are letters, numbers, and underscore. The first character must be a lowercase letter. Default: - No ID
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param visible: Whether this metric should be visible in dashboard graphs. Setting this to false is useful when you want to hide raw metrics that are used in math expressions, and show only the expression results. Default: true

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            id=id,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
            visible=visible,
        )

        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.Metric", jsii.invoke(self, "metricSucceeded", [props]))

    @jsii.member(jsii_name="metricTime")
    def metric_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional["_aws_cdk_aws_cloudwatch_ceddda9d.Unit"] = None,
        visible: typing.Optional[builtins.bool] = None,
    ) -> "_aws_cdk_aws_cloudwatch_ceddda9d.Metric":
        '''(experimental) Metric for the interval, in milliseconds, between the time the execution starts and the time it closes.

        This time may be longer than the time the runner took.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param id: Unique identifier for this metric when used in dashboard widgets. The id can be used as a variable to represent this metric in math expressions. Valid characters are letters, numbers, and underscore. The first character must be a lowercase letter. Default: - No ID
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        :param visible: Whether this metric should be visible in dashboard graphs. Setting this to false is useful when you want to hide raw metrics that are used in math expressions, and show only the expression results. Default: true

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            id=id,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
            visible=visible,
        )

        return typing.cast("_aws_cdk_aws_cloudwatch_ceddda9d.Metric", jsii.invoke(self, "metricTime", [props]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) Manage the connections of all management functions.

        Use this to enable connections to your GitHub Enterprise Server in a VPC.

        This cannot be used to manage connections of the runners. Use the ``connections`` property of each runner provider to manage runner connections.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="providers")
    def providers(
        self,
    ) -> typing.List[typing.Union["IRunnerProvider", "ICompositeProvider"]]:
        '''(experimental) Configured runner providers.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Union["IRunnerProvider", "ICompositeProvider"]], jsii.get(self, "providers"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "Secrets":
        '''(experimental) Secrets for GitHub communication including webhook secret and runner authentication.

        :stability: experimental
        '''
        return typing.cast("Secrets", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> typing.Optional["GitHubRunnersProps"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["GitHubRunnersProps"], jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.GitHubRunnersProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_public_subnet": "allowPublicSubnet",
        "extra_certificates": "extraCertificates",
        "idle_timeout": "idleTimeout",
        "log_options": "logOptions",
        "providers": "providers",
        "provider_selector": "providerSelector",
        "require_self_hosted_label": "requireSelfHostedLabel",
        "retry_options": "retryOptions",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "setup_access": "setupAccess",
        "status_access": "statusAccess",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "webhook_access": "webhookAccess",
    },
)
class GitHubRunnersProps:
    def __init__(
        self,
        *,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        extra_certificates: typing.Optional[builtins.str] = None,
        idle_timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        log_options: typing.Optional[typing.Union["LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        providers: typing.Optional[typing.Sequence[typing.Union["IRunnerProvider", "ICompositeProvider"]]] = None,
        provider_selector: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IFunction"] = None,
        require_self_hosted_label: typing.Optional[builtins.bool] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        setup_access: typing.Optional["LambdaAccess"] = None,
        status_access: typing.Optional["LambdaAccess"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        vpc_subnets: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_access: typing.Optional["LambdaAccess"] = None,
    ) -> None:
        '''(experimental) Properties for GitHubRunners.

        :param allow_public_subnet: (experimental) Allow management functions to run in public subnets. Lambda Functions in a public subnet can NOT access the internet. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting. Default: false
        :param extra_certificates: (experimental) Path to a certificate file (.pem or .crt) or a directory containing certificate files (.pem or .crt) required to trust GitHub Enterprise Server. Use this when GitHub Enterprise Server certificates are self-signed. If a directory is provided, all .pem and .crt files in that directory will be used. The certificates will be concatenated into a single file for use by Node.js. You may also want to use custom images for your runner providers that contain the same certificates. See {@link RunnerImageComponent.extraCertificates }:: const selfSignedCertificates = 'certs/ghes.pem'; // or 'path-to-my-extra-certs-folder' for a directory const imageBuilder = CodeBuildRunnerProvider.imageBuilder(this, 'Image Builder with Certs'); imageBuilder.addComponent(RunnerImageComponent.extraCertificates(selfSignedCertificates, 'private-ca')); const provider = new CodeBuildRunnerProvider(this, 'CodeBuild', { imageBuilder: imageBuilder, }); new GitHubRunners( this, 'runners', { providers: [provider], extraCertificates: selfSignedCertificates, } );
        :param idle_timeout: (experimental) Time to wait before stopping a runner that remains idle. If the user cancelled the job, or if another runner stole it, this stops the runner to avoid wasting resources. Default: 5 minutes
        :param log_options: (experimental) Logging options for the state machine that manages the runners. Default: no logs
        :param providers: (experimental) List of runner providers to use. At least one provider is required. Provider will be selected when its label matches the labels requested by the workflow job. Default: CodeBuild, Lambda and Fargate runners with all the defaults (no VPC or default account VPC)
        :param provider_selector: (experimental) Optional Lambda function to customize provider selection logic and label assignment. - The function receives the webhook payload along with default provider and its labels as {@link ProviderSelectorInput } - The function returns a selected provider and its labels as {@link ProviderSelectorResult } - You can decline to provision a runner by returning undefined as the provider in the selector result - You can fully customize the labels for the about-to-be-provisioned runner (add, remove, modify, dynamic labels, etc.) - Labels don't have to match the labels originally configured for the provider, but see warnings below - This function will be called synchronously during webhook processing, so it should be fast and efficient (webhook limit is 30 seconds total) **WARNING: It is your responsibility to ensure the selected provider's labels match the job's required labels. If you return the wrong labels, the runner will be created but GitHub Actions will not assign the job to it.** **WARNING: Provider selection is not a guarantee that a specific provider will be assigned for the job. GitHub Actions may assign the job to any runner with matching labels. The provider selector only determines which provider's runner will be *created*, but GitHub Actions may route the job to any available runner with the required labels.** **For reliable provider assignment based on job characteristics, consider using repo-level runner registration where you can control which runners are available for specific repositories. This information is also available while using the setup wizard.
        :param require_self_hosted_label: (experimental) Whether to require the ``self-hosted`` label. If ``true``, the runner will only start if the workflow job explicitly requests the ``self-hosted`` label. Be careful when setting this to ``false``. Avoid setting up providers with generic label requirements like ``linux`` as they may match workflows that are not meant to run on self-hosted runners. Default: true
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. GitHub jobs time out after not being able to get a runner for 24 hours. You should not retry for more than 24 hours. Retries use full jitter, so total time spent waiting is about half the sum of min(interval * backoffRate ^ attempt, maxDelay) over all attempts. Default: retry 210 times over a bit more than 24 hours
        :param security_group: (deprecated) Security group attached to all management functions. Use this with to provide access to GitHub Enterprise Server hosted inside a VPC. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting.
        :param security_groups: (experimental) Security groups attached to all management functions. Use this to provide outbound access from management functions to GitHub Enterprise Server hosted inside a VPC. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting. **Note:** Defining inbound rules on this security group does nothing. This security group only controls outbound access FROM the management functions. To limit access TO the webhook or setup functions, use {@link webhookAccess} and {@link setupAccess} instead.
        :param setup_access: (experimental) Access configuration for the setup function. Once you finish the setup process, you can set this to ``LambdaAccess.noAccess()`` to remove access to the setup function. You can also use ``LambdaAccess.apiGateway({ allowedIps: ['my-ip/0']})`` to limit access to your IP only. Default: LambdaAccess.lambdaUrl()
        :param status_access: (experimental) Access configuration for the status function. This function returns a lot of sensitive information about the runner, so you should only allow access to it from trusted IPs, if at all. Default: LambdaAccess.noAccess()
        :param vpc: (experimental) VPC used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting and will run outside the VPC. Make sure the selected VPC and subnets have access to the following with either NAT Gateway or VPC Endpoints: - GitHub Enterprise Server - Secrets Manager - SQS - Step Functions - CloudFormation (status function only) - EC2 - ECR (status function only)
        :param vpc_subnets: (experimental) VPC subnets used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC. **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting.
        :param webhook_access: (experimental) Access configuration for the webhook function. This function is called by GitHub when a new workflow job is scheduled. For an extra layer of security, you can set this to ``LambdaAccess.apiGateway({ allowedIps: LambdaAccess.githubWebhookIps() })``. You can also set this to ``LambdaAccess.apiGateway({allowedVpc: vpc, allowedIps: ['GHES.IP.ADDRESS/32']})`` if your GitHub Enterprise Server is hosted in a VPC. This will create an API Gateway endpoint that's only accessible from within the VPC. *WARNING*: changing access type may change the URL. When the URL changes, you must update GitHub as well. Default: LambdaAccess.lambdaUrl()

        :stability: experimental
        '''
        if isinstance(log_options, dict):
            log_options = LogOptions(**log_options)
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4db12e50ec9bf1582f493963c13640e2d81a3a4afae3df834ecce0bf88f4706c)
            check_type(argname="argument allow_public_subnet", value=allow_public_subnet, expected_type=type_hints["allow_public_subnet"])
            check_type(argname="argument extra_certificates", value=extra_certificates, expected_type=type_hints["extra_certificates"])
            check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
            check_type(argname="argument log_options", value=log_options, expected_type=type_hints["log_options"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument provider_selector", value=provider_selector, expected_type=type_hints["provider_selector"])
            check_type(argname="argument require_self_hosted_label", value=require_self_hosted_label, expected_type=type_hints["require_self_hosted_label"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument setup_access", value=setup_access, expected_type=type_hints["setup_access"])
            check_type(argname="argument status_access", value=status_access, expected_type=type_hints["status_access"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument webhook_access", value=webhook_access, expected_type=type_hints["webhook_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if extra_certificates is not None:
            self._values["extra_certificates"] = extra_certificates
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout
        if log_options is not None:
            self._values["log_options"] = log_options
        if providers is not None:
            self._values["providers"] = providers
        if provider_selector is not None:
            self._values["provider_selector"] = provider_selector
        if require_self_hosted_label is not None:
            self._values["require_self_hosted_label"] = require_self_hosted_label
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if setup_access is not None:
            self._values["setup_access"] = setup_access
        if status_access is not None:
            self._values["status_access"] = status_access
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if webhook_access is not None:
            self._values["webhook_access"] = webhook_access

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow management functions to run in public subnets. Lambda Functions in a public subnet can NOT access the internet.

        **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_public_subnet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_certificates(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to a certificate file (.pem or .crt) or a directory containing certificate files (.pem or .crt) required to trust GitHub Enterprise Server. Use this when GitHub Enterprise Server certificates are self-signed.

        If a directory is provided, all .pem and .crt files in that directory will be used. The certificates will be concatenated into a single file for use by Node.js.

        You may also want to use custom images for your runner providers that contain the same certificates. See {@link RunnerImageComponent.extraCertificates }::

           const selfSignedCertificates = 'certs/ghes.pem'; // or 'path-to-my-extra-certs-folder' for a directory
           const imageBuilder = CodeBuildRunnerProvider.imageBuilder(this, 'Image Builder with Certs');
           imageBuilder.addComponent(RunnerImageComponent.extraCertificates(selfSignedCertificates, 'private-ca'));

           const provider = new CodeBuildRunnerProvider(this, 'CodeBuild', {
               imageBuilder: imageBuilder,
           });

           new GitHubRunners(
             this,
             'runners',
             {
               providers: [provider],
               extraCertificates: selfSignedCertificates,
             }
           );

        :stability: experimental
        '''
        result = self._values.get("extra_certificates")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) Time to wait before stopping a runner that remains idle.

        If the user cancelled the job, or if another runner stole it, this stops the runner to avoid wasting resources.

        :default: 5 minutes

        :stability: experimental
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def log_options(self) -> typing.Optional["LogOptions"]:
        '''(experimental) Logging options for the state machine that manages the runners.

        :default: no logs

        :stability: experimental
        '''
        result = self._values.get("log_options")
        return typing.cast(typing.Optional["LogOptions"], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union["IRunnerProvider", "ICompositeProvider"]]]:
        '''(experimental) List of runner providers to use.

        At least one provider is required. Provider will be selected when its label matches the labels requested by the workflow job.

        :default: CodeBuild, Lambda and Fargate runners with all the defaults (no VPC or default account VPC)

        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union["IRunnerProvider", "ICompositeProvider"]]], result)

    @builtins.property
    def provider_selector(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IFunction"]:
        '''(experimental) Optional Lambda function to customize provider selection logic and label assignment.

        - The function receives the webhook payload along with default provider and its labels as {@link ProviderSelectorInput }
        - The function returns a selected provider and its labels as {@link ProviderSelectorResult }
        - You can decline to provision a runner by returning undefined as the provider in the selector result
        - You can fully customize the labels for the about-to-be-provisioned runner (add, remove, modify, dynamic labels, etc.)
        - Labels don't have to match the labels originally configured for the provider, but see warnings below
        - This function will be called synchronously during webhook processing, so it should be fast and efficient (webhook limit is 30 seconds total)

        **WARNING: It is your responsibility to ensure the selected provider's labels match the job's required labels. If you return the wrong labels, the runner will be created but GitHub Actions will not assign the job to it.**

        **WARNING: Provider selection is not a guarantee that a specific provider will be assigned for the job. GitHub Actions may assign the job to any runner with matching labels. The provider selector only determines which provider's runner will be *created*, but GitHub Actions may route the job to any available runner with the required labels.**

        **For reliable provider assignment based on job characteristics, consider using repo-level runner registration where you can control which runners are available for specific repositories. This information is also available while using the setup wizard.

        :see: https://github.com/CloudSnorkel/cdk-github-runners/blob/main/SETUP_GITHUB.md
        :stability: experimental
        '''
        result = self._values.get("provider_selector")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IFunction"], result)

    @builtins.property
    def require_self_hosted_label(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to require the ``self-hosted`` label.

        If ``true``, the runner will only start if the workflow job explicitly requests the ``self-hosted`` label.

        Be careful when setting this to ``false``. Avoid setting up providers with generic label requirements like ``linux`` as they may match workflows that are not meant to run on self-hosted runners.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("require_self_hosted_label")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retry_options(self) -> typing.Optional["ProviderRetryOptions"]:
        '''(experimental) Options to retry operation in case of failure like missing capacity, or API quota issues.

        GitHub jobs time out after not being able to get a runner for 24 hours. You should not retry for more than 24 hours.

        Retries use full jitter, so total time spent waiting is about half the sum of min(interval * backoffRate ^ attempt, maxDelay) over all attempts.

        :default: retry 210 times over a bit more than 24 hours

        :stability: experimental
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional["ProviderRetryOptions"], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(deprecated) Security group attached to all management functions.

        Use this with to provide access to GitHub Enterprise Server hosted inside a VPC.

        **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting.

        :deprecated: use {@link securityGroups } instead

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security groups attached to all management functions.

        Use this to provide outbound access from management functions to GitHub Enterprise Server hosted inside a VPC.

        **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting.

        **Note:** Defining inbound rules on this security group does nothing. This security group only controls outbound access FROM the management functions. To limit access TO the webhook or setup functions, use {@link webhookAccess} and {@link setupAccess} instead.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def setup_access(self) -> typing.Optional["LambdaAccess"]:
        '''(experimental) Access configuration for the setup function.

        Once you finish the setup process, you can set this to ``LambdaAccess.noAccess()`` to remove access to the setup function. You can also use ``LambdaAccess.apiGateway({ allowedIps: ['my-ip/0']})`` to limit access to your IP only.

        :default: LambdaAccess.lambdaUrl()

        :stability: experimental
        '''
        result = self._values.get("setup_access")
        return typing.cast(typing.Optional["LambdaAccess"], result)

    @builtins.property
    def status_access(self) -> typing.Optional["LambdaAccess"]:
        '''(experimental) Access configuration for the status function.

        This function returns a lot of sensitive information about the runner, so you should only allow access to it from trusted IPs, if at all.

        :default: LambdaAccess.noAccess()

        :stability: experimental
        '''
        result = self._values.get("status_access")
        return typing.cast(typing.Optional["LambdaAccess"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC.

        **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting and will run outside the VPC.

        Make sure the selected VPC and subnets have access to the following with either NAT Gateway or VPC Endpoints:

        - GitHub Enterprise Server
        - Secrets Manager
        - SQS
        - Step Functions
        - CloudFormation (status function only)
        - EC2
        - ECR (status function only)

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    @builtins.property
    def vpc_subnets(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) VPC subnets used for all management functions.

        Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC.

        **Note:** This only affects management functions that interact with GitHub. Lambda functions that help with runner image building and don't interact with GitHub are NOT affected by this setting.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def webhook_access(self) -> typing.Optional["LambdaAccess"]:
        '''(experimental) Access configuration for the webhook function.

        This function is called by GitHub when a new workflow job is scheduled. For an extra layer of security, you can set this to ``LambdaAccess.apiGateway({ allowedIps: LambdaAccess.githubWebhookIps() })``.

        You can also set this to ``LambdaAccess.apiGateway({allowedVpc: vpc, allowedIps: ['GHES.IP.ADDRESS/32']})`` if your GitHub Enterprise Server is hosted in a VPC. This will create an API Gateway endpoint that's only accessible from within the VPC.

        *WARNING*: changing access type may change the URL. When the URL changes, you must update GitHub as well.

        :default: LambdaAccess.lambdaUrl()

        :stability: experimental
        '''
        result = self._values.get("webhook_access")
        return typing.cast(typing.Optional["LambdaAccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubRunnersProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.ICompositeProvider")
class ICompositeProvider(_constructs_77d1e7e8.IConstruct, typing_extensions.Protocol):
    '''(experimental) Interface for composite runner providers that combine multiple sub-providers.

    Unlike IRunnerProvider, composite providers do not have connections, grant capabilities,
    or log groups as they delegate to their sub-providers.

    Note that this interface cannot be implemented by external code. Use {@link CompositeProvider } factory methods.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We use match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="providers")
    def providers(self) -> typing.List["IRunnerProvider"]:
        '''(experimental) All sub-providers contained in this composite provider.

        This is used to extract providers for metric filters and other operations.

        :stability: experimental
        '''
        ...


class _ICompositeProviderProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''(experimental) Interface for composite runner providers that combine multiple sub-providers.

    Unlike IRunnerProvider, composite providers do not have connections, grant capabilities,
    or log groups as they delegate to their sub-providers.

    Note that this interface cannot be implemented by external code. Use {@link CompositeProvider } factory methods.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.ICompositeProvider"

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We use match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="providers")
    def providers(self) -> typing.List["IRunnerProvider"]:
        '''(experimental) All sub-providers contained in this composite provider.

        This is used to extract providers for metric filters and other operations.

        :stability: experimental
        '''
        return typing.cast(typing.List["IRunnerProvider"], jsii.get(self, "providers"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICompositeProvider).__jsii_proxy_class__ = lambda : _ICompositeProviderProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerAmiStatus")
class IRunnerAmiStatus(typing_extensions.Protocol):
    '''(experimental) AMI status returned from runner providers to be displayed as output of status function.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> builtins.str:
        '''(experimental) Id of launch template pointing to the latest AMI built by the AMI builder.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="amiBuilderLogGroup")
    def ami_builder_log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group name for the AMI builder where history of builds can be analyzed.

        :stability: experimental
        '''
        ...


class _IRunnerAmiStatusProxy:
    '''(experimental) AMI status returned from runner providers to be displayed as output of status function.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerAmiStatus"

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> builtins.str:
        '''(experimental) Id of launch template pointing to the latest AMI built by the AMI builder.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="amiBuilderLogGroup")
    def ami_builder_log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group name for the AMI builder where history of builds can be analyzed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amiBuilderLogGroup"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerAmiStatus).__jsii_proxy_class__ = lambda : _IRunnerAmiStatusProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerImageBuilder")
class IRunnerImageBuilder(typing_extensions.Protocol):
    '''(experimental) Interface for constructs that build an image that can be used in {@link IRunnerProvider }.

    An image can be a Docker image or AMI.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bindAmi")
    def bind_ami(self) -> "RunnerAmi":
        '''(experimental) Build and return an AMI with GitHub Runner installed in it.

        Anything that ends up with a launch template pointing to an AMI that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing AMI and nothing else.

        The AMI can be further updated over time manually or using a schedule as long as it is always written to the same launch template.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="bindDockerImage")
    def bind_docker_image(self) -> "RunnerImage":
        '''(experimental) Build and return a Docker image with GitHub Runner installed in it.

        Anything that ends up with an ECR repository containing a Docker image that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing image and nothing else.

        It's important that the specified image tag be available at the time the repository is available. Providers usually assume the image is ready and will fail if it's not.

        The image can be further updated over time manually or using a schedule as long as it is always written to the same tag.

        :stability: experimental
        '''
        ...


class _IRunnerImageBuilderProxy:
    '''(experimental) Interface for constructs that build an image that can be used in {@link IRunnerProvider }.

    An image can be a Docker image or AMI.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerImageBuilder"

    @jsii.member(jsii_name="bindAmi")
    def bind_ami(self) -> "RunnerAmi":
        '''(experimental) Build and return an AMI with GitHub Runner installed in it.

        Anything that ends up with a launch template pointing to an AMI that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing AMI and nothing else.

        The AMI can be further updated over time manually or using a schedule as long as it is always written to the same launch template.

        :stability: experimental
        '''
        return typing.cast("RunnerAmi", jsii.invoke(self, "bindAmi", []))

    @jsii.member(jsii_name="bindDockerImage")
    def bind_docker_image(self) -> "RunnerImage":
        '''(experimental) Build and return a Docker image with GitHub Runner installed in it.

        Anything that ends up with an ECR repository containing a Docker image that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing image and nothing else.

        It's important that the specified image tag be available at the time the repository is available. Providers usually assume the image is ready and will fail if it's not.

        The image can be further updated over time manually or using a schedule as long as it is always written to the same tag.

        :stability: experimental
        '''
        return typing.cast("RunnerImage", jsii.invoke(self, "bindDockerImage", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerImageBuilder).__jsii_proxy_class__ = lambda : _IRunnerImageBuilderProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerImageStatus")
class IRunnerImageStatus(typing_extensions.Protocol):
    '''(experimental) Image status returned from runner providers to be displayed in status.json.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="imageRepository")
    def image_repository(self) -> builtins.str:
        '''(experimental) Image repository where image builder pushes runner images.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''(experimental) Tag of image that should be used.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imageBuilderLogGroup")
    def image_builder_log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group name for the image builder where history of image builds can be analyzed.

        :stability: experimental
        '''
        ...


class _IRunnerImageStatusProxy:
    '''(experimental) Image status returned from runner providers to be displayed in status.json.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerImageStatus"

    @builtins.property
    @jsii.member(jsii_name="imageRepository")
    def image_repository(self) -> builtins.str:
        '''(experimental) Image repository where image builder pushes runner images.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRepository"))

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''(experimental) Tag of image that should be used.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @builtins.property
    @jsii.member(jsii_name="imageBuilderLogGroup")
    def image_builder_log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group name for the image builder where history of image builds can be analyzed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageBuilderLogGroup"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerImageStatus).__jsii_proxy_class__ = lambda : _IRunnerImageStatusProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerProvider")
class IRunnerProvider(
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _aws_cdk_aws_iam_ceddda9d.IGrantable,
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''(experimental) Interface for all runner providers.

    This interface cannot be implemented by external code. If the built-in providers don't cover your use case, open an issue so we can discuss it.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We use match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> "_aws_cdk_aws_logs_ceddda9d.ILogGroup":
        '''(experimental) Log group where provided runners will save their logs.

        Note that this is not the job log, but the runner itself. It will not contain output from the GitHub Action but only metadata on its execution.

        :stability: experimental
        '''
        ...


class _IRunnerProviderProxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_iam_ceddda9d.IGrantable), # type: ignore[misc]
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''(experimental) Interface for all runner providers.

    This interface cannot be implemented by external code. If the built-in providers don't cover your use case, open an issue so we can discuss it.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerProvider"

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We use match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> "_aws_cdk_aws_logs_ceddda9d.ILogGroup":
        '''(experimental) Log group where provided runners will save their logs.

        Note that this is not the job log, but the runner itself. It will not contain output from the GitHub Action but only metadata on its execution.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_logs_ceddda9d.ILogGroup", jsii.get(self, "logGroup"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerProvider).__jsii_proxy_class__ = lambda : _IRunnerProviderProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerProviderStatus")
class IRunnerProviderStatus(typing_extensions.Protocol):
    '''(experimental) Interface for runner image status used by status.json.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with provider.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''(experimental) Runner provider type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ami")
    def ami(self) -> typing.Optional["IRunnerAmiStatus"]:
        '''(experimental) Details about AMI used by this runner provider.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="constructPath")
    def construct_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) CDK construct node path for this provider.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> typing.Optional["IRunnerImageStatus"]:
        '''(experimental) Details about Docker image used by this runner provider.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group for runners.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role attached to runners.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Security groups attached to runners.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcArn")
    def vpc_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) VPC where runners will be launched.

        :stability: experimental
        '''
        ...


class _IRunnerProviderStatusProxy:
    '''(experimental) Interface for runner image status used by status.json.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerProviderStatus"

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''(experimental) Runner provider type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="ami")
    def ami(self) -> typing.Optional["IRunnerAmiStatus"]:
        '''(experimental) Details about AMI used by this runner provider.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IRunnerAmiStatus"], jsii.get(self, "ami"))

    @builtins.property
    @jsii.member(jsii_name="constructPath")
    def construct_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) CDK construct node path for this provider.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constructPath"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> typing.Optional["IRunnerImageStatus"]:
        '''(experimental) Details about Docker image used by this runner provider.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IRunnerImageStatus"], jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group for runners.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroup"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role attached to runners.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Security groups attached to runners.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="vpcArn")
    def vpc_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) VPC where runners will be launched.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerProviderStatus).__jsii_proxy_class__ = lambda : _IRunnerProviderStatusProxy


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ImageBuilderAsset",
    jsii_struct_bases=[],
    name_mapping={"asset": "asset", "path": "path"},
)
class ImageBuilderAsset:
    def __init__(
        self,
        *,
        asset: "_aws_cdk_aws_s3_assets_ceddda9d.Asset",
        path: builtins.str,
    ) -> None:
        '''(experimental) An asset including file or directory to place inside the built image.

        :param asset: (experimental) Asset to place in the image.
        :param path: (experimental) Path to place asset in the image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__16ca7e4fb20813ac7d2ccae32dbb1fda48790fac4d7cd07aa1afbdb9d8f5e665)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset": asset,
            "path": path,
        }

    @builtins.property
    def asset(self) -> "_aws_cdk_aws_s3_assets_ceddda9d.Asset":
        '''(experimental) Asset to place in the image.

        :stability: experimental
        '''
        result = self._values.get("asset")
        assert result is not None, "Required property 'asset' is missing"
        return typing.cast("_aws_cdk_aws_s3_assets_ceddda9d.Asset", result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Path to place asset in the image.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageBuilderAsset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImageBuilderComponent(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.ImageBuilderComponent",
):
    '''(deprecated) Components are a set of commands to run and optional files to add to an image.

    Components are the building blocks of images built by Image Builder.

    Example::

       new ImageBuilderComponent(this, 'AWS CLI', {
         platform: 'Windows',
         displayName: 'AWS CLI',
         description: 'Install latest version of AWS CLI',
         commands: [
           '$p = Start-Process msiexec.exe -PassThru -Wait -ArgumentList \\'/i https://awscli.amazonaws.com/AWSCLIV2.msi /qn\\'',
           'if ($p.ExitCode -ne 0) { throw "Exit code is $p.ExitCode" }',
         ],
       }

    :deprecated: Use ``RunnerImageComponent`` instead as this be internal soon.

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        commands: typing.Sequence[builtins.str],
        description: builtins.str,
        display_name: builtins.str,
        platform: builtins.str,
        assets: typing.Optional[typing.Sequence[typing.Union["ImageBuilderAsset", typing.Dict[builtins.str, typing.Any]]]] = None,
        reboot: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param commands: (experimental) Shell commands to run when adding this component to the image. On Linux, these are bash commands. On Windows, there are PowerShell commands.
        :param description: (experimental) Component description.
        :param display_name: (experimental) Component display name.
        :param platform: (experimental) Component platform. Must match the builder platform.
        :param assets: (experimental) Optional assets to add to the built image.
        :param reboot: (experimental) Require a reboot after installing this component. Default: false

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__363ebaab8a0bcbaea3d32a9c7e3cb241f08cf49d6eea02ba40eaaef9af89f266)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ImageBuilderComponentProperties(
            commands=commands,
            description=description,
            display_name=display_name,
            platform=platform,
            assets=assets,
            reboot=reboot,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantAssetsRead")
    def grant_assets_read(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> None:
        '''(deprecated) Grants read permissions to the principal on the assets buckets.

        :param grantee: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a450535474a302df6d17ac0b627edd05f72f54c900f36380517d39fc0a3b15e4)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantAssetsRead", [grantee]))

    @jsii.member(jsii_name="prefixCommandsWithErrorHandling")
    def prefix_commands_with_error_handling(
        self,
        platform: builtins.str,
        commands: typing.Sequence[builtins.str],
    ) -> typing.List[builtins.str]:
        '''
        :param platform: -
        :param commands: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bae848cd8ee55808c4c98a6e69173dc05ae5472e3b1443ee6fbc64e32bc9a25f)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "prefixCommandsWithErrorHandling", [platform, commands]))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(deprecated) Component ARN.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        '''(deprecated) Supported platform for the component.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "platform"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ImageBuilderComponentProperties",
    jsii_struct_bases=[],
    name_mapping={
        "commands": "commands",
        "description": "description",
        "display_name": "displayName",
        "platform": "platform",
        "assets": "assets",
        "reboot": "reboot",
    },
)
class ImageBuilderComponentProperties:
    def __init__(
        self,
        *,
        commands: typing.Sequence[builtins.str],
        description: builtins.str,
        display_name: builtins.str,
        platform: builtins.str,
        assets: typing.Optional[typing.Sequence[typing.Union["ImageBuilderAsset", typing.Dict[builtins.str, typing.Any]]]] = None,
        reboot: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for ImageBuilderComponent construct.

        :param commands: (experimental) Shell commands to run when adding this component to the image. On Linux, these are bash commands. On Windows, there are PowerShell commands.
        :param description: (experimental) Component description.
        :param display_name: (experimental) Component display name.
        :param platform: (experimental) Component platform. Must match the builder platform.
        :param assets: (experimental) Optional assets to add to the built image.
        :param reboot: (experimental) Require a reboot after installing this component. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b86439e194b36e470271c572c251444f98c4b86a68fa7e63cf41ae1fa9628d4a)
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
            check_type(argname="argument reboot", value=reboot, expected_type=type_hints["reboot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commands": commands,
            "description": description,
            "display_name": display_name,
            "platform": platform,
        }
        if assets is not None:
            self._values["assets"] = assets
        if reboot is not None:
            self._values["reboot"] = reboot

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        '''(experimental) Shell commands to run when adding this component to the image.

        On Linux, these are bash commands. On Windows, there are PowerShell commands.

        :stability: experimental
        '''
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> builtins.str:
        '''(experimental) Component description.

        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''(experimental) Component display name.

        :stability: experimental
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform(self) -> builtins.str:
        '''(experimental) Component platform.

        Must match the builder platform.

        :stability: experimental
        '''
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assets(self) -> typing.Optional[typing.List["ImageBuilderAsset"]]:
        '''(experimental) Optional assets to add to the built image.

        :stability: experimental
        '''
        result = self._values.get("assets")
        return typing.cast(typing.Optional[typing.List["ImageBuilderAsset"]], result)

    @builtins.property
    def reboot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Require a reboot after installing this component.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("reboot")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageBuilderComponentProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaAccess(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cloudsnorkel/cdk-github-runners.LambdaAccess",
):
    '''(experimental) Access configuration options for Lambda functions like setup and webhook function. Use this to limit access to these functions.

    If you need a custom access point, you can implement this abstract class yourself. Note that the Lambda functions expect API Gateway v1 or v2 input. They also expect every URL under the constructed URL to point to the function.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="apiGateway")
    @builtins.classmethod
    def api_gateway(
        cls,
        *,
        allowed_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        allowed_vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        allowed_vpc_endpoints: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint"]] = None,
    ) -> "LambdaAccess":
        '''(experimental) Provide access using API Gateway.

        This is the most secure option, but requires additional configuration. It allows you to limit access to specific IP addresses and even to a specific VPC.

        To limit access to GitHub.com use::

           LambdaAccess.apiGateway({
             allowedIps: LambdaAccess.githubWebhookIps(),
           });

        Alternatively, get and manually update the list manually with::

           curl https://api.github.com/meta | jq .hooks

        :param allowed_ips: (experimental) List of IP addresses in CIDR notation that are allowed to access the API Gateway. If not specified on public API Gateway, all IP addresses are allowed. If not specified on private API Gateway, no IP addresses are allowed (but specified security groups are).
        :param allowed_security_groups: (experimental) List of security groups that are allowed to access the API Gateway. Only works for private API Gateways with {@link allowedVpc}.
        :param allowed_vpc: (experimental) Create a private API Gateway and allow access from the specified VPC.
        :param allowed_vpc_endpoints: (experimental) Create a private API Gateway and allow access from the specified VPC endpoints. Use this to make use of existing VPC endpoints or to share an endpoint between multiple functions. The VPC endpoint must point to ``ec2.InterfaceVpcEndpointAwsService.APIGATEWAY``. No other settings are supported when using this option. All endpoints will be allowed access, but only the first one will be used as the URL by the runner system for setting up the webhook, and as setup URL.

        :stability: experimental
        '''
        props = ApiGatewayAccessProps(
            allowed_ips=allowed_ips,
            allowed_security_groups=allowed_security_groups,
            allowed_vpc=allowed_vpc,
            allowed_vpc_endpoints=allowed_vpc_endpoints,
        )

        return typing.cast("LambdaAccess", jsii.sinvoke(cls, "apiGateway", [props]))

    @jsii.member(jsii_name="githubWebhookIps")
    @builtins.classmethod
    def github_webhook_ips(cls) -> typing.List[builtins.str]:
        '''(experimental) Downloads the list of IP addresses used by GitHub.com for webhooks.

        Note that downloading dynamic data during deployment is not recommended in CDK. This is a workaround for the lack of a better solution.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "githubWebhookIps", []))

    @jsii.member(jsii_name="lambdaUrl")
    @builtins.classmethod
    def lambda_url(cls) -> "LambdaAccess":
        '''(experimental) Provide access using Lambda URL.

        This is the default and simplest option. It puts no limits on the requester, but the Lambda functions themselves authenticate every request.

        :stability: experimental
        '''
        return typing.cast("LambdaAccess", jsii.sinvoke(cls, "lambdaUrl", []))

    @jsii.member(jsii_name="noAccess")
    @builtins.classmethod
    def no_access(cls) -> "LambdaAccess":
        '''(experimental) Disables access to the configured Lambda function.

        This is useful for the setup function after setup is done.

        :stability: experimental
        '''
        return typing.cast("LambdaAccess", jsii.sinvoke(cls, "noAccess", []))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        lambda_function: "_aws_cdk_aws_lambda_ceddda9d.Function",
    ) -> builtins.str:
        '''(experimental) Creates all required resources and returns access URL or empty string if disabled.

        :param scope: -
        :param id: -
        :param lambda_function: -

        :return: access URL or empty string if disabled

        :stability: experimental
        '''
        ...


class _LambdaAccessProxy(LambdaAccess):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        lambda_function: "_aws_cdk_aws_lambda_ceddda9d.Function",
    ) -> builtins.str:
        '''(experimental) Creates all required resources and returns access URL or empty string if disabled.

        :param scope: -
        :param id: -
        :param lambda_function: -

        :return: access URL or empty string if disabled

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__244c9d572ba45d54b74fe86f184cc91d1d6c9a27c6a0d3635e3b366738528b8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        return typing.cast(builtins.str, jsii.invoke(self, "bind", [scope, id, lambda_function]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, LambdaAccess).__jsii_proxy_class__ = lambda : _LambdaAccessProxy


@jsii.implements(IRunnerProvider)
class LambdaRunnerProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.LambdaRunnerProvider",
):
    '''(experimental) GitHub Actions runner provider using Lambda to execute jobs.

    Creates a Docker-based function that gets executed for each job.

    Execution environments can be reused between jobs. All jobs that can run on the same function should be equally trusted. See
    https://github.com/CloudSnorkel/cdk-github-runners#job-isolation

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        ephemeral_storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ephemeral_storage_size: (experimental) The size of the function’s /tmp directory in MiB. Default: 10 GiB
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder must contain the {@link RunnerImageComponent.lambdaEntrypoint} component. The image builder determines the OS and architecture of the runner. Default: LambdaRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['lambda']
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 2048
        :param security_group: (deprecated) Security group to assign to this instance. Default: public lambda with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: public lambda with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.minutes(15)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__637ac3a7237f114ea2a9842f95653a0d13444cd4da7a4dfe9330fdb98204e19b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaRunnerProviderProps(
            ephemeral_storage_size=ephemeral_storage_size,
            group=group,
            image_builder=image_builder,
            label=label,
            labels=labels,
            memory_size=memory_size,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="imageBuilder")
    @builtins.classmethod
    def image_builder(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        aws_image_builder_options: typing.Optional[typing.Union["AwsImageBuilderRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        base_ami: typing.Optional[typing.Union[builtins.str, "BaseImage"]] = None,
        base_docker_image: typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]] = None,
        builder_type: typing.Optional["RunnerImageBuilderType"] = None,
        code_build_options: typing.Optional[typing.Union["CodeBuildRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        components: typing.Optional[typing.Sequence["RunnerImageComponent"]] = None,
        docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        wait_on_deploy: typing.Optional[builtins.bool] = None,
    ) -> "IConfigurableRunnerImageBuilder":
        '''(experimental) Create new image builder that builds Lambda specific runner images.

        You can customize the OS, architecture, VPC, subnet, security groups, etc. by passing in props.

        You can add components to the image builder by calling ``imageBuilder.addComponent()``.

        The default OS is Amazon Linux 2023 running on x64 architecture.

        Included components:

        - ``RunnerImageComponent.requiredPackages()``
        - ``RunnerImageComponent.runnerUser()``
        - ``RunnerImageComponent.git()``
        - ``RunnerImageComponent.githubCli()``
        - ``RunnerImageComponent.awsCli()``
        - ``RunnerImageComponent.githubRunner()``
        - ``RunnerImageComponent.lambdaEntrypoint()``

        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param aws_image_builder_options: (experimental) Options specific to AWS Image Builder. Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.
        :param base_ami: (experimental) Base AMI from which runner AMIs will be built. This can be: - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead - A BaseImage instance created using static factory methods: - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.) - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter. Default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS
        :param base_docker_image: (experimental) Base image from which Docker runner images will be built. This can be: - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead - A BaseContainerImage instance created using static factory methods: - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild) - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}. Default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS
        :param builder_type: Default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI
        :param code_build_options: (experimental) Options specific to CodeBuild image builder. Only used when builderType is RunnerImageBuilderType.CODE_BUILD.
        :param components: (experimental) Components to install on the image. Default: none
        :param docker_setup_commands: (experimental) Additional commands to run on the build host before starting the Docker runner image build. Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images. Default: []
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX_UBUNTU
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_groups: (experimental) Security Groups to assign to this instance.
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param vpc: (experimental) VPC to build the image in. Default: no VPC
        :param wait_on_deploy: (experimental) Wait for image to finish building during deployment. It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build. Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used. Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ce2bbc7a18f99610673c6eb5e5f04fb45ba63301ff0fbe525246014617834e02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunnerImageBuilderProps(
            architecture=architecture,
            aws_image_builder_options=aws_image_builder_options,
            base_ami=base_ami,
            base_docker_image=base_docker_image,
            builder_type=builder_type,
            code_build_options=code_build_options,
            components=components,
            docker_setup_commands=docker_setup_commands,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
            wait_on_deploy=wait_on_deploy,
        )

        return typing.cast("IConfigurableRunnerImageBuilder", jsii.sinvoke(cls, "imageBuilder", [scope, id, props]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0e4dccc4a69e2dce26e0096d5540914cfc02fe99cbad00d4b539e0750dc84c6d)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_ARM64_DOCKERFILE_PATH")
    @builtins.classmethod
    def LINUX_ARM64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(deprecated) Path to Dockerfile for Linux ARM64 with all the requirement for Lambda runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be similar to public.ecr.aws/lambda/nodejs:14.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.

        :deprecated: Use ``imageBuilder()`` instead.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_ARM64_DOCKERFILE_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_X64_DOCKERFILE_PATH")
    @builtins.classmethod
    def LINUX_X64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(deprecated) Path to Dockerfile for Linux x64 with all the requirement for Lambda runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be similar to public.ecr.aws/lambda/nodejs:14.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.

        :deprecated: Use ``imageBuilder()`` instead.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_X64_DOCKERFILE_PATH"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> "_aws_cdk_aws_lambda_ceddda9d.Function":
        '''(experimental) The function hosting the GitHub runner.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_lambda_ceddda9d.Function", jsii.get(self, "function"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "_aws_cdk_aws_iam_ceddda9d.IPrincipal":
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.IPrincipal", jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> "RunnerImage":
        '''(deprecated) Docker image loaded with GitHub Actions Runner and its prerequisites.

        The image is built by an image builder and is specific to Lambda.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast("RunnerImage", jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> "_aws_cdk_aws_logs_ceddda9d.ILogGroup":
        '''(experimental) Log group where provided runners will save their logs.

        Note that this is not the job log, but the runner itself. It will not contain output from the GitHub Action but only metadata on its execution.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_logs_ceddda9d.ILogGroup", jsii.get(self, "logGroup"))


class LinuxUbuntuComponents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.LinuxUbuntuComponents",
):
    '''(deprecated) Components for Ubuntu Linux that can be used with AWS Image Builder based builders.

    These cannot be used by {@link CodeBuildImageBuilder }.

    :deprecated: Use ``RunnerImageComponent`` instead.

    :stability: deprecated
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsCli")
    @builtins.classmethod
    def aws_cli(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        architecture: "Architecture",
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param architecture: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2a9ab64a566b3cb12a56785cb68d60451eea856392ba6abd6e242f7e7607911a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "awsCli", [scope, id, architecture]))

    @jsii.member(jsii_name="docker")
    @builtins.classmethod
    def docker(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        _architecture: "Architecture",
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param _architecture: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f65a5832ccfba2d220d98a2c68a108dfc3f78dbe85709f5f5c759dcc9ad578f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "docker", [scope, id, _architecture]))

    @jsii.member(jsii_name="extraCertificates")
    @builtins.classmethod
    def extra_certificates(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        path: builtins.str,
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param path: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__68b2501b6d5ebe8b59ce2ea43654c77b49b4f10be39415a6e90b19f2d8db235b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "extraCertificates", [scope, id, path]))

    @jsii.member(jsii_name="git")
    @builtins.classmethod
    def git(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        _architecture: "Architecture",
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param _architecture: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bec8ad9a5de8cc35d2f35d52d25f6a1b7f104db23ae3e2e7135c937889eca5b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "git", [scope, id, _architecture]))

    @jsii.member(jsii_name="githubCli")
    @builtins.classmethod
    def github_cli(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        _architecture: "Architecture",
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param _architecture: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__50238c37c0bb4a9b1f6a596f61b2f74a34f0fee6eced39901007db76663f96d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "githubCli", [scope, id, _architecture]))

    @jsii.member(jsii_name="githubRunner")
    @builtins.classmethod
    def github_runner(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        runner_version: "RunnerVersion",
        architecture: "Architecture",
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param runner_version: -
        :param architecture: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cfdcfc8bfb186dc1b0e83a960dadbae430b22e77b9f4c33b2b73d225fc182bff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "githubRunner", [scope, id, runner_version, architecture]))

    @jsii.member(jsii_name="requiredPackages")
    @builtins.classmethod
    def required_packages(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        architecture: "Architecture",
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param architecture: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__16b9420557bcd008ca04d0eb1d14eb5a4747825ef4fadee115c226eb00b43841)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "requiredPackages", [scope, id, architecture]))

    @jsii.member(jsii_name="runnerUser")
    @builtins.classmethod
    def runner_user(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        _architecture: "Architecture",
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param _architecture: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__01575c6c37e4a36bb9456ff19c3af703d6c78462d7d7a4a668462fd9c3163582)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "runnerUser", [scope, id, _architecture]))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.LogOptions",
    jsii_struct_bases=[],
    name_mapping={
        "include_execution_data": "includeExecutionData",
        "level": "level",
        "log_group_name": "logGroupName",
        "log_retention": "logRetention",
    },
)
class LogOptions:
    def __init__(
        self,
        *,
        include_execution_data: typing.Optional[builtins.bool] = None,
        level: typing.Optional["_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel"] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
    ) -> None:
        '''(experimental) Defines what execution history events are logged and where they are logged.

        :param include_execution_data: (experimental) Determines whether execution data is included in your log. Default: true
        :param level: (experimental) Defines which category of execution history events are logged. Default: ALL
        :param log_group_name: (experimental) The log group where the execution history events will be logged.
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7d87067ac294a2f323b063b74d5b20d774fc42a4e718e01d16209ad13483ebc2)
            check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_execution_data is not None:
            self._values["include_execution_data"] = include_execution_data
        if level is not None:
            self._values["level"] = level
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_retention is not None:
            self._values["log_retention"] = log_retention

    @builtins.property
    def include_execution_data(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Determines whether execution data is included in your log.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("include_execution_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def level(self) -> typing.Optional["_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel"]:
        '''(experimental) Defines which category of execution history events are logged.

        :default: ALL

        :stability: experimental
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional["_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel"], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The log group where the execution history events will be logged.

        :stability: experimental
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Os(metaclass=jsii.JSIIMeta, jsii_type="@cloudsnorkel/cdk-github-runners.Os"):
    '''(experimental) OS enum for an image.

    :stability: experimental
    '''

    @jsii.member(jsii_name="is")
    def is_(self, os: "Os") -> builtins.bool:
        '''(experimental) Checks if the given OS is the same as this one.

        :param os: OS to compare.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f19131179030c715697989d1d64b1121c3de55b2dc82fb900699b7c47875fcaa)
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
        return typing.cast(builtins.bool, jsii.invoke(self, "is", [os]))

    @jsii.member(jsii_name="isIn")
    def is_in(self, oses: typing.Sequence["Os"]) -> builtins.bool:
        '''(experimental) Checks if this OS is in a given list.

        :param oses: list of OS to check.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__28c514548a5b083cb01132e52421a310d7518ba890b88c4cff63cbaa518d114a)
            check_type(argname="argument oses", value=oses, expected_type=type_hints["oses"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isIn", [oses]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX")
    @builtins.classmethod
    def LINUX(cls) -> "Os":
        '''(deprecated) Linux.

        :deprecated: use {@link LINUX_UBUNTU }, {@link LINUX_UBUNTU_2404 }, {@link LINUX_AMAZON_2 } or {@link LINUX_AMAZON_2023 }

        :stability: deprecated
        '''
        return typing.cast("Os", jsii.sget(cls, "LINUX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_AMAZON_2")
    @builtins.classmethod
    def LINUX_AMAZON_2(cls) -> "Os":
        '''(experimental) Amazon Linux 2.

        :stability: experimental
        '''
        return typing.cast("Os", jsii.sget(cls, "LINUX_AMAZON_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_AMAZON_2023")
    @builtins.classmethod
    def LINUX_AMAZON_2023(cls) -> "Os":
        '''(experimental) Amazon Linux 2023.

        :stability: experimental
        '''
        return typing.cast("Os", jsii.sget(cls, "LINUX_AMAZON_2023"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_UBUNTU")
    @builtins.classmethod
    def LINUX_UBUNTU(cls) -> "Os":
        '''(experimental) Ubuntu Linux.

        :stability: experimental
        '''
        return typing.cast("Os", jsii.sget(cls, "LINUX_UBUNTU"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_UBUNTU_2204")
    @builtins.classmethod
    def LINUX_UBUNTU_2204(cls) -> "Os":
        '''(experimental) Ubuntu Linux 22.04.

        :stability: experimental
        '''
        return typing.cast("Os", jsii.sget(cls, "LINUX_UBUNTU_2204"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_UBUNTU_2404")
    @builtins.classmethod
    def LINUX_UBUNTU_2404(cls) -> "Os":
        '''(experimental) Ubuntu Linux 24.04.

        :stability: experimental
        '''
        return typing.cast("Os", jsii.sget(cls, "LINUX_UBUNTU_2404"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS")
    @builtins.classmethod
    def WINDOWS(cls) -> "Os":
        '''(experimental) Windows.

        :stability: experimental
        '''
        return typing.cast("Os", jsii.sget(cls, "WINDOWS"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ProviderRetryOptions",
    jsii_struct_bases=[],
    name_mapping={
        "backoff_rate": "backoffRate",
        "interval": "interval",
        "max_attempts": "maxAttempts",
        "max_delay": "maxDelay",
        "retry": "retry",
    },
)
class ProviderRetryOptions:
    def __init__(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        max_delay: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        retry: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Retry options for providers.

        The default is to retry 210 times for a bit over 24 hours with increasing interval.

        Retries use full jitter, so every wait is a random time between zero and the calculated interval. This spreads out
        runners that all failed at the same time, so they don't hit the same missing capacity or API quota together again.
        It also means the average wait is half the calculated interval, and that's what the 24 hours are calculated from.

        :param backoff_rate: (experimental) Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param interval: (experimental) How much time to wait after first retryable failure. This interval will be multiplied by {@link backoffRate} each retry, up to {@link maxDelay}. Default: 1 minute
        :param max_attempts: (experimental) How many times to retry. Default: 210
        :param max_delay: (experimental) Maximum wait between retries. Without it, exponential backoff quickly grows to hours between attempts, so a job can end up waiting hours for a runner even though capacity came back minutes after it failed. Don't go too low either. A lower maximum needs more attempts to cover the same 24 hours, and every attempt adds to the execution history that Step Functions caps at 25,000 events. Default: 15 minutes
        :param retry: (experimental) Set to true to retry provider on supported failures. Which failures generate a retry depends on the specific provider. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bd088f490cad60ffd09b5c6222c769b3656e8a7694013c57b0029f2f6c986b51)
            check_type(argname="argument backoff_rate", value=backoff_rate, expected_type=type_hints["backoff_rate"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument max_delay", value=max_delay, expected_type=type_hints["max_delay"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backoff_rate is not None:
            self._values["backoff_rate"] = backoff_rate
        if interval is not None:
            self._values["interval"] = interval
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts
        if max_delay is not None:
            self._values["max_delay"] = max_delay
        if retry is not None:
            self._values["retry"] = retry

    @builtins.property
    def backoff_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Multiplication for how much longer the wait interval gets on every retry.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("backoff_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) How much time to wait after first retryable failure.

        This interval will be multiplied by {@link backoffRate} each retry, up to {@link maxDelay}.

        :default: 1 minute

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) How many times to retry.

        :default: 210

        :stability: experimental
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_delay(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) Maximum wait between retries.

        Without it, exponential backoff quickly grows to hours between attempts, so a job
        can end up waiting hours for a runner even though capacity came back minutes after it failed.

        Don't go too low either. A lower maximum needs more attempts to cover the same 24 hours, and every attempt adds
        to the execution history that Step Functions caps at 25,000 events.

        :default: 15 minutes

        :stability: experimental
        '''
        result = self._values.get("max_delay")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def retry(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to retry provider on supported failures.

        Which failures generate a retry depends on the specific provider.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderRetryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ProviderSelectorInput",
    jsii_struct_bases=[],
    name_mapping={
        "payload": "payload",
        "providers": "providers",
        "default_labels": "defaultLabels",
        "default_provider": "defaultProvider",
    },
)
class ProviderSelectorInput:
    def __init__(
        self,
        *,
        payload: typing.Any,
        providers: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
        default_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_provider: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Input to the provider selector Lambda function.

        :param payload: (experimental) Full GitHub webhook payload (workflow_job event structure with action="queued"). - Original labels requested by the workflow job can be found at ``payload.workflow_job.labels``. - Repository path (e.g. CloudSnorkel/cdk-github-runners) is at ``payload.repository.full_name``. - Commit hash is at ``payload.workflow_job.head_sha``.
        :param providers: (experimental) Map of available provider node paths to their configured labels. Example: { "MyStack/Small": ["linux", "small"], "MyStack/Large": ["linux", "large"] }
        :param default_labels: (experimental) Labels that would have been used by default (the selected provider's labels). May be undefined if no provider matched by default.
        :param default_provider: (experimental) Provider node path that would have been selected by default label matching. Use this to easily return the default selection: ``{ provider: input.defaultProvider, labels: input.defaultLabels }`` May be undefined if no provider matched by default.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__32039399f56bfde071f3747ee0792c5419757ceddb8a3ca63dd026969e0172c7)
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument default_labels", value=default_labels, expected_type=type_hints["default_labels"])
            check_type(argname="argument default_provider", value=default_provider, expected_type=type_hints["default_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "payload": payload,
            "providers": providers,
        }
        if default_labels is not None:
            self._values["default_labels"] = default_labels
        if default_provider is not None:
            self._values["default_provider"] = default_provider

    @builtins.property
    def payload(self) -> typing.Any:
        '''(experimental) Full GitHub webhook payload (workflow_job event structure with action="queued").

        - Original labels requested by the workflow job can be found at ``payload.workflow_job.labels``.
        - Repository path (e.g. CloudSnorkel/cdk-github-runners) is at ``payload.repository.full_name``.
        - Commit hash is at ``payload.workflow_job.head_sha``.

        :see: https://docs.github.com/en/webhooks/webhook-events-and-payloads?actionType=queued#workflow_job
        :stability: experimental
        '''
        result = self._values.get("payload")
        assert result is not None, "Required property 'payload' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def providers(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''(experimental) Map of available provider node paths to their configured labels.

        Example: { "MyStack/Small": ["linux", "small"], "MyStack/Large": ["linux", "large"] }

        :stability: experimental
        '''
        result = self._values.get("providers")
        assert result is not None, "Required property 'providers' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], result)

    @builtins.property
    def default_labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Labels that would have been used by default (the selected provider's labels).

        May be undefined if no provider matched by default.

        :stability: experimental
        '''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_provider(self) -> typing.Optional[builtins.str]:
        '''(experimental) Provider node path that would have been selected by default label matching.

        Use this to easily return the default selection: ``{ provider: input.defaultProvider, labels: input.defaultLabels }``
        May be undefined if no provider matched by default.

        :stability: experimental
        '''
        result = self._values.get("default_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderSelectorInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ProviderSelectorResult",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "provider": "provider"},
)
class ProviderSelectorResult:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        provider: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Result from the provider selector Lambda function.

        :param labels: (experimental) Labels to use when registering the runner. Must be returned when a provider is selected. Can be used to add, remove, or modify labels.
        :param provider: (experimental) Node path of the provider to use (e.g., "MyStack/MyProvider"). Must match one of the configured provider node paths from the input. If not provided, the job will be skipped (no runner created).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__80f59228823c79b7a6dea6bd4bbcade1672b332240071aa12b4fc7a780cd35d9)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Labels to use when registering the runner.

        Must be returned when a provider is selected.
        Can be used to add, remove, or modify labels.

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def provider(self) -> typing.Optional[builtins.str]:
        '''(experimental) Node path of the provider to use (e.g., "MyStack/MyProvider"). Must match one of the configured provider node paths from the input. If not provided, the job will be skipped (no runner created).

        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderSelectorResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerAmi",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "launch_template": "launchTemplate",
        "os": "os",
        "runner_version": "runnerVersion",
        "cache_key": "cacheKey",
        "log_group": "logGroup",
    },
)
class RunnerAmi:
    def __init__(
        self,
        *,
        architecture: "Architecture",
        launch_template: "_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate",
        os: "Os",
        runner_version: "RunnerVersion",
        cache_key: typing.Optional[builtins.str] = None,
        log_group: typing.Optional["_aws_cdk_aws_logs_ceddda9d.LogGroup"] = None,
    ) -> None:
        '''(experimental) Description of a AMI built by {@link RunnerImageBuilder }.

        :param architecture: (experimental) Architecture of the image.
        :param launch_template: (experimental) Launch template pointing to the latest AMI.
        :param os: (experimental) OS type of the image.
        :param runner_version: (deprecated) Installed runner version.
        :param cache_key: (experimental) Set this to a value that changes whenever the AMI changes (the AMI id or any version string works). It's used to know when the AMI's root device name needs to be looked up again. If left empty, the root device name is looked up once and reused. That's fine as long as the AMI's root device never changes. This value may be used for other things in the future that require knowing when the AMI changed.
        :param log_group: (experimental) Log group where image builds are logged.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__94c612bd55218b02d6290415e414adca19a5e6961e7aa4dec3a838bc328b9885)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument cache_key", value=cache_key, expected_type=type_hints["cache_key"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "architecture": architecture,
            "launch_template": launch_template,
            "os": os,
            "runner_version": runner_version,
        }
        if cache_key is not None:
            self._values["cache_key"] = cache_key
        if log_group is not None:
            self._values["log_group"] = log_group

    @builtins.property
    def architecture(self) -> "Architecture":
        '''(experimental) Architecture of the image.

        :stability: experimental
        '''
        result = self._values.get("architecture")
        assert result is not None, "Required property 'architecture' is missing"
        return typing.cast("Architecture", result)

    @builtins.property
    def launch_template(self) -> "_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate":
        '''(experimental) Launch template pointing to the latest AMI.

        :stability: experimental
        '''
        result = self._values.get("launch_template")
        assert result is not None, "Required property 'launch_template' is missing"
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate", result)

    @builtins.property
    def os(self) -> "Os":
        '''(experimental) OS type of the image.

        :stability: experimental
        '''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast("Os", result)

    @builtins.property
    def runner_version(self) -> "RunnerVersion":
        '''(deprecated) Installed runner version.

        :deprecated: open a ticket if you need this

        :stability: deprecated
        '''
        result = self._values.get("runner_version")
        assert result is not None, "Required property 'runner_version' is missing"
        return typing.cast("RunnerVersion", result)

    @builtins.property
    def cache_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) Set this to a value that changes whenever the AMI changes (the AMI id or any version string works).

        It's used to know when the AMI's root device name needs to be looked up again. If left empty, the root
        device name is looked up once and reused. That's fine as long as the AMI's root device never changes.

        This value may be used for other things in the future that require knowing when the AMI changed.

        :stability: experimental
        '''
        result = self._values.get("cache_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group(self) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.LogGroup"]:
        '''(experimental) Log group where image builds are logged.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.LogGroup"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerAmi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerImage",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "image_repository": "imageRepository",
        "image_tag": "imageTag",
        "os": "os",
        "runner_version": "runnerVersion",
        "log_group": "logGroup",
    },
)
class RunnerImage:
    def __init__(
        self,
        *,
        architecture: "Architecture",
        image_repository: "_aws_cdk_aws_ecr_ceddda9d.IRepository",
        image_tag: builtins.str,
        os: "Os",
        runner_version: "RunnerVersion",
        log_group: typing.Optional["_aws_cdk_aws_logs_ceddda9d.LogGroup"] = None,
    ) -> None:
        '''(experimental) Description of a Docker image built by {@link RunnerImageBuilder }.

        :param architecture: (experimental) Architecture of the image.
        :param image_repository: (experimental) ECR repository containing the image.
        :param image_tag: (experimental) Static image tag where the image will be pushed.
        :param os: (experimental) OS type of the image.
        :param runner_version: (deprecated) Installed runner version.
        :param log_group: (experimental) Log group where image builds are logged.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a74a83a8ebe05e179af2175f3c275f7e12d7c4f25c43d548f01e20cc2a011cf8)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument image_repository", value=image_repository, expected_type=type_hints["image_repository"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "architecture": architecture,
            "image_repository": image_repository,
            "image_tag": image_tag,
            "os": os,
            "runner_version": runner_version,
        }
        if log_group is not None:
            self._values["log_group"] = log_group

    @builtins.property
    def architecture(self) -> "Architecture":
        '''(experimental) Architecture of the image.

        :stability: experimental
        '''
        result = self._values.get("architecture")
        assert result is not None, "Required property 'architecture' is missing"
        return typing.cast("Architecture", result)

    @builtins.property
    def image_repository(self) -> "_aws_cdk_aws_ecr_ceddda9d.IRepository":
        '''(experimental) ECR repository containing the image.

        :stability: experimental
        '''
        result = self._values.get("image_repository")
        assert result is not None, "Required property 'image_repository' is missing"
        return typing.cast("_aws_cdk_aws_ecr_ceddda9d.IRepository", result)

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''(experimental) Static image tag where the image will be pushed.

        :stability: experimental
        '''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os(self) -> "Os":
        '''(experimental) OS type of the image.

        :stability: experimental
        '''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast("Os", result)

    @builtins.property
    def runner_version(self) -> "RunnerVersion":
        '''(deprecated) Installed runner version.

        :deprecated: open a ticket if you need this

        :stability: deprecated
        '''
        result = self._values.get("runner_version")
        assert result is not None, "Required property 'runner_version' is missing"
        return typing.cast("RunnerVersion", result)

    @builtins.property
    def log_group(self) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.LogGroup"]:
        '''(experimental) Log group where image builds are logged.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.LogGroup"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerImageAsset",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "target": "target"},
)
class RunnerImageAsset:
    def __init__(self, *, source: builtins.str, target: builtins.str) -> None:
        '''(experimental) Asset to copy into a built image.

        :param source: (experimental) Path on local system to copy into the image. Can be a file or a directory.
        :param target: (experimental) Target path in the built image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__21bedad36e17a5840ddb719458c9e0eb15a89e493efa80af28f6031d1a27d62e)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }

    @builtins.property
    def source(self) -> builtins.str:
        '''(experimental) Path on local system to copy into the image.

        Can be a file or a directory.

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''(experimental) Target path in the built image.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerImageAsset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "aws_image_builder_options": "awsImageBuilderOptions",
        "base_ami": "baseAmi",
        "base_docker_image": "baseDockerImage",
        "builder_type": "builderType",
        "code_build_options": "codeBuildOptions",
        "components": "components",
        "docker_setup_commands": "dockerSetupCommands",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "os": "os",
        "rebuild_interval": "rebuildInterval",
        "runner_version": "runnerVersion",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "wait_on_deploy": "waitOnDeploy",
    },
)
class RunnerImageBuilderProps:
    def __init__(
        self,
        *,
        architecture: typing.Optional["Architecture"] = None,
        aws_image_builder_options: typing.Optional[typing.Union["AwsImageBuilderRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        base_ami: typing.Optional[typing.Union[builtins.str, "BaseImage"]] = None,
        base_docker_image: typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]] = None,
        builder_type: typing.Optional["RunnerImageBuilderType"] = None,
        code_build_options: typing.Optional[typing.Union["CodeBuildRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        components: typing.Optional[typing.Sequence["RunnerImageComponent"]] = None,
        docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        wait_on_deploy: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param aws_image_builder_options: (experimental) Options specific to AWS Image Builder. Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.
        :param base_ami: (experimental) Base AMI from which runner AMIs will be built. This can be: - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead - A BaseImage instance created using static factory methods: - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.) - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter. Default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS
        :param base_docker_image: (experimental) Base image from which Docker runner images will be built. This can be: - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead - A BaseContainerImage instance created using static factory methods: - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild) - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}. Default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS
        :param builder_type: Default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI
        :param code_build_options: (experimental) Options specific to CodeBuild image builder. Only used when builderType is RunnerImageBuilderType.CODE_BUILD.
        :param components: (experimental) Components to install on the image. Default: none
        :param docker_setup_commands: (experimental) Additional commands to run on the build host before starting the Docker runner image build. Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images. Default: []
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX_UBUNTU
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_groups: (experimental) Security Groups to assign to this instance.
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param vpc: (experimental) VPC to build the image in. Default: no VPC
        :param wait_on_deploy: (experimental) Wait for image to finish building during deployment. It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build. Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used. Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect. Default: true

        :stability: experimental
        '''
        if isinstance(aws_image_builder_options, dict):
            aws_image_builder_options = AwsImageBuilderRunnerImageBuilderProps(**aws_image_builder_options)
        if isinstance(code_build_options, dict):
            code_build_options = CodeBuildRunnerImageBuilderProps(**code_build_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ab96b7f3871624e8430668114e7f5748ba5d253168db5b8f9a13955d0a82e43d)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument aws_image_builder_options", value=aws_image_builder_options, expected_type=type_hints["aws_image_builder_options"])
            check_type(argname="argument base_ami", value=base_ami, expected_type=type_hints["base_ami"])
            check_type(argname="argument base_docker_image", value=base_docker_image, expected_type=type_hints["base_docker_image"])
            check_type(argname="argument builder_type", value=builder_type, expected_type=type_hints["builder_type"])
            check_type(argname="argument code_build_options", value=code_build_options, expected_type=type_hints["code_build_options"])
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument docker_setup_commands", value=docker_setup_commands, expected_type=type_hints["docker_setup_commands"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument rebuild_interval", value=rebuild_interval, expected_type=type_hints["rebuild_interval"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument wait_on_deploy", value=wait_on_deploy, expected_type=type_hints["wait_on_deploy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if aws_image_builder_options is not None:
            self._values["aws_image_builder_options"] = aws_image_builder_options
        if base_ami is not None:
            self._values["base_ami"] = base_ami
        if base_docker_image is not None:
            self._values["base_docker_image"] = base_docker_image
        if builder_type is not None:
            self._values["builder_type"] = builder_type
        if code_build_options is not None:
            self._values["code_build_options"] = code_build_options
        if components is not None:
            self._values["components"] = components
        if docker_setup_commands is not None:
            self._values["docker_setup_commands"] = docker_setup_commands
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if os is not None:
            self._values["os"] = os
        if rebuild_interval is not None:
            self._values["rebuild_interval"] = rebuild_interval
        if runner_version is not None:
            self._values["runner_version"] = runner_version
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if wait_on_deploy is not None:
            self._values["wait_on_deploy"] = wait_on_deploy

    @builtins.property
    def architecture(self) -> typing.Optional["Architecture"]:
        '''(experimental) Image architecture.

        :default: Architecture.X86_64

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional["Architecture"], result)

    @builtins.property
    def aws_image_builder_options(
        self,
    ) -> typing.Optional["AwsImageBuilderRunnerImageBuilderProps"]:
        '''(experimental) Options specific to AWS Image Builder.

        Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.

        :stability: experimental
        '''
        result = self._values.get("aws_image_builder_options")
        return typing.cast(typing.Optional["AwsImageBuilderRunnerImageBuilderProps"], result)

    @builtins.property
    def base_ami(self) -> typing.Optional[typing.Union[builtins.str, "BaseImage"]]:
        '''(experimental) Base AMI from which runner AMIs will be built.

        This can be:

        - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead
        - A BaseImage instance created using static factory methods:

          - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID
          - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.)
          - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object
          - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name
          - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID
          - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image

        For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter.

        :default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS

        :stability: experimental
        '''
        result = self._values.get("base_ami")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "BaseImage"]], result)

    @builtins.property
    def base_docker_image(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]]:
        '''(experimental) Base image from which Docker runner images will be built.

        This can be:

        - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead
        - A BaseContainerImage instance created using static factory methods:

          - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub
          - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild)
          - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public
          - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string

        When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}.

        :default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS

        :stability: experimental
        '''
        result = self._values.get("base_docker_image")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]], result)

    @builtins.property
    def builder_type(self) -> typing.Optional["RunnerImageBuilderType"]:
        '''
        :default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI

        :stability: experimental
        '''
        result = self._values.get("builder_type")
        return typing.cast(typing.Optional["RunnerImageBuilderType"], result)

    @builtins.property
    def code_build_options(self) -> typing.Optional["CodeBuildRunnerImageBuilderProps"]:
        '''(experimental) Options specific to CodeBuild image builder.

        Only used when builderType is RunnerImageBuilderType.CODE_BUILD.

        :stability: experimental
        '''
        result = self._values.get("code_build_options")
        return typing.cast(typing.Optional["CodeBuildRunnerImageBuilderProps"], result)

    @builtins.property
    def components(self) -> typing.Optional[typing.List["RunnerImageComponent"]]:
        '''(experimental) Components to install on the image.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.List["RunnerImageComponent"]], result)

    @builtins.property
    def docker_setup_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Additional commands to run on the build host before starting the Docker runner image build.

        Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("docker_setup_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Removal policy for logs of image builds.

        If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed.

        We try to not leave anything behind when removed. But sometimes a log staying behind is useful.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def os(self) -> typing.Optional["Os"]:
        '''(experimental) Image OS.

        :default: OS.LINUX_UBUNTU

        :stability: experimental
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional["Os"], result)

    @builtins.property
    def rebuild_interval(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) Schedule the image to be rebuilt every given interval.

        Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates.

        Set to zero to disable.

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("rebuild_interval")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def runner_version(self) -> typing.Optional["RunnerVersion"]:
        '''(experimental) Version of GitHub Runners to install.

        :default: latest version available

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        return typing.cast(typing.Optional["RunnerVersion"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security Groups to assign to this instance.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC to build the image in.

        :default: no VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    @builtins.property
    def wait_on_deploy(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Wait for image to finish building during deployment.

        It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build.

        Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used.

        Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("wait_on_deploy")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cloudsnorkel/cdk-github-runners.RunnerImageBuilderType")
class RunnerImageBuilderType(enum.Enum):
    '''
    :stability: experimental
    '''

    CODE_BUILD = "CODE_BUILD"
    '''(experimental) Build runner images using AWS CodeBuild.

    Faster than AWS Image Builder, but can only be used to build Linux Docker images.

    :stability: experimental
    '''
    AWS_IMAGE_BUILDER = "AWS_IMAGE_BUILDER"
    '''(experimental) Build runner images using AWS Image Builder.

    Slower than CodeBuild, but can be used to build any type of image including AMIs and Windows images.

    :stability: experimental
    '''


class RunnerImageComponent(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerImageComponent",
):
    '''(experimental) Components are used to build runner images.

    They can run commands in the image, copy files into the image, and run some Docker commands.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsCli")
    @builtins.classmethod
    def aws_cli(
        cls,
        version: typing.Optional[builtins.str] = None,
    ) -> "RunnerImageComponent":
        '''(experimental) A component to install the AWS CLI.

        :param version: Software version to install (e.g. '2.15.0'). Default: latest.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__29f18c953246d0b1c39021f86a7331edf31cbf289f37746be885869974f0fca2)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "awsCli", [version]))

    @jsii.member(jsii_name="cloudWatchAgent")
    @builtins.classmethod
    def cloud_watch_agent(cls) -> "RunnerImageComponent":
        '''(experimental) A component to install CloudWatch Agent for the runner so we can send logs.

        :stability: experimental
        '''
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "cloudWatchAgent", []))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        *,
        assets: typing.Optional[typing.Sequence[typing.Union["RunnerImageAsset", typing.Dict[builtins.str, typing.Any]]]] = None,
        commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        docker_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "RunnerImageComponent":
        '''(experimental) Define a custom component that can run commands in the image, copy files into the image, and run some Docker commands.

        The order of operations is (1) assets (2) commands (3) docker commands.

        Use this to customize the image for the runner.

        **WARNING:** Docker commands are not guaranteed to be included before the next component

        :param assets: (experimental) Assets to copy into the built image.
        :param commands: (experimental) Commands to run in the built image.
        :param docker_commands: (experimental) Docker commands to run in the built image. For example: ``['ENV foo=bar', 'RUN echo $foo']`` These commands are ignored when building AMIs.
        :param name: (experimental) Component name used for (1) image build logging and (2) identifier for {@link IConfigurableRunnerImageBuilder.removeComponent }. Name must only contain alphanumeric characters and dashes.

        :stability: experimental
        '''
        props = RunnerImageComponentCustomProps(
            assets=assets,
            commands=commands,
            docker_commands=docker_commands,
            name=name,
        )

        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "custom", [props]))

    @jsii.member(jsii_name="docker")
    @builtins.classmethod
    def docker(
        cls,
        version: typing.Optional[builtins.str] = None,
    ) -> "RunnerImageComponent":
        '''(experimental) A component to install Docker.

        On Windows this sets up dockerd for Windows containers without Docker Desktop. If you need Linux containers on Windows, you'll need to install Docker Desktop which doesn't seem to play well with servers (PRs welcome).

        :param version: Software version to install (e.g. '29.1.5'). Default: latest. Only used on Windows; on Linux (Ubuntu, Amazon Linux 2 and Amazon Linux 2023) the package version format is not reliably predictable so latest is always used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6162c551433cf1db5703258b3cb16cc320275cca3f8ad1f8e1a51f0dcb575003)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "docker", [version]))

    @jsii.member(jsii_name="dockerInDocker")
    @builtins.classmethod
    def docker_in_docker(
        cls,
        version: typing.Optional[builtins.str] = None,
    ) -> "RunnerImageComponent":
        '''(deprecated) A component to install Docker-in-Docker.

        :param version: Software version to install (e.g. '29.1.5'). Default: latest.

        :deprecated: use ``docker()``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5e95caad3455adca1643b95064ddbc75b67f19721e366fd8038efe6b556251d4)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "dockerInDocker", [version]))

    @jsii.member(jsii_name="environmentVariables")
    @builtins.classmethod
    def environment_variables(
        cls,
        vars: typing.Mapping[builtins.str, builtins.str],
    ) -> "RunnerImageComponent":
        '''(experimental) A component to add environment variables for jobs the runner executes.

        These variables only affect the jobs ran by the runner. They are not global. They do not affect other components.

        It is not recommended to use this component to pass secrets. Instead, use GitHub Secrets or AWS Secrets Manager.

        Must be used after the {@link githubRunner} component.

        :param vars: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__604cc9b160ccf839230b5f673dff20a8c9722aa81c88ef3ccadcdfcec778ec1a)
            check_type(argname="argument vars", value=vars, expected_type=type_hints["vars"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "environmentVariables", [vars]))

    @jsii.member(jsii_name="extraCertificates")
    @builtins.classmethod
    def extra_certificates(
        cls,
        source: builtins.str,
        name: builtins.str,
    ) -> "RunnerImageComponent":
        '''(experimental) A component to add a trusted certificate authority.

        This can be used to support GitHub Enterprise Server with self-signed certificate.

        :param source: path to certificate file in PEM format, or a directory containing certificate files (.pem or .crt).
        :param name: unique certificate name to be used on runner file system.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__71019afd6f999efd03cc3106a7c28048b0a38c740207d3615ba7e0569bab5d3d)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "extraCertificates", [source, name]))

    @jsii.member(jsii_name="git")
    @builtins.classmethod
    def git(
        cls,
        version: typing.Optional[builtins.str] = None,
    ) -> "RunnerImageComponent":
        '''(experimental) A component to install Git.

        :param version: Software version to install (e.g. '2.43.0.windows.1'). Default: latest. Only used on Windows; on Linux the package manager is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__669185ad44a15382c6a0a4208b26b61d74d2e4b36063f72333c2d4d82f830b1c)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "git", [version]))

    @jsii.member(jsii_name="githubCli")
    @builtins.classmethod
    def github_cli(
        cls,
        version: typing.Optional[builtins.str] = None,
    ) -> "RunnerImageComponent":
        '''(experimental) A component to install the GitHub CLI.

        :param version: Software version to install (e.g. '2.40.0'). Default: latest. Only used on Windows (x64/windows_amd64); on Linux the package manager is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4981b41e48ec1c85e6e4bdbb74f25162e16cf49eb993af72a7e8cf9e0f36ba5c)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "githubCli", [version]))

    @jsii.member(jsii_name="githubRunner")
    @builtins.classmethod
    def github_runner(cls, runner_version: "RunnerVersion") -> "RunnerImageComponent":
        '''(experimental) A component to install the GitHub Actions Runner.

        This is the actual executable that connects to GitHub to ask for jobs and then execute them.

        :param runner_version: The version of the runner to install. Usually you would set this to latest.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d4bb77dff91c55638bfd8c57f50a16468b499b43fd08f7c2eb6b91015b0fb5ce)
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "githubRunner", [runner_version]))

    @jsii.member(jsii_name="jobCompletedHook")
    @builtins.classmethod
    def job_completed_hook(cls, source_path: builtins.str) -> "RunnerImageComponent":
        '''(experimental) A component that runs a script after every job the runner executes.

        Point this at a local script file. It is copied into the image, made executable, and the runner is
        configured to run it after each job through the
        ```ACTIONS_RUNNER_HOOK_JOB_COMPLETED`` <https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/run-scripts>`_
        environment variable. GitHub passes job context to the script as environment variables such as ``GITHUB_REPOSITORY`` and ``GITHUB_RUN_ID``.

        Must be used after the {@link githubRunner} component.

        :param source_path: path to a local script file to run after every job.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__083e94ebc2f48e7d52b90eb90d5dfc27d4d2b7378bead0205b6630aad7eb19b3)
            check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "jobCompletedHook", [source_path]))

    @jsii.member(jsii_name="jobStartedHook")
    @builtins.classmethod
    def job_started_hook(cls, source_path: builtins.str) -> "RunnerImageComponent":
        '''(experimental) A component that runs a script before every job the runner executes.

        Point this at a local script file. It is copied into the image, made executable, and the runner is
        configured to run it before each job through the
        ```ACTIONS_RUNNER_HOOK_JOB_STARTED`` <https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/run-scripts>`_
        environment variable. GitHub passes job context to the script as environment variables such as ``GITHUB_REPOSITORY`` and ``GITHUB_RUN_ID``.

        Must be used after the {@link githubRunner} component.

        :param source_path: path to a local script file to run before every job.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__85f2d5267f3cde15dc5bd682063ee9b779f6c755c762b02b8c0e32138f774d4e)
            check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "jobStartedHook", [source_path]))

    @jsii.member(jsii_name="lambdaEntrypoint")
    @builtins.classmethod
    def lambda_entrypoint(cls) -> "RunnerImageComponent":
        '''(experimental) A component to set up the required Lambda entrypoint for Lambda runners.

        :stability: experimental
        '''
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "lambdaEntrypoint", []))

    @jsii.member(jsii_name="requiredPackages")
    @builtins.classmethod
    def required_packages(cls) -> "RunnerImageComponent":
        '''(experimental) A component to install the required packages for the runner.

        :stability: experimental
        '''
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "requiredPackages", []))

    @jsii.member(jsii_name="runnerUser")
    @builtins.classmethod
    def runner_user(cls) -> "RunnerImageComponent":
        '''(experimental) A component to prepare the required runner user.

        :stability: experimental
        '''
        return typing.cast("RunnerImageComponent", jsii.sinvoke(cls, "runnerUser", []))

    @jsii.member(jsii_name="getAssets")
    def get_assets(
        self,
        _os: "Os",
        _architecture: "Architecture",
    ) -> typing.List["RunnerImageAsset"]:
        '''(experimental) Returns assets to copy into the built image.

        Can be used to copy files into the image.

        :param _os: -
        :param _architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__68512864561c1bf5bd229a6f57c7022e0a3d3d27a6d1167bb9c47d7bc98136c1)
            check_type(argname="argument _os", value=_os, expected_type=type_hints["_os"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast(typing.List["RunnerImageAsset"], jsii.invoke(self, "getAssets", [_os, _architecture]))

    @jsii.member(jsii_name="getCommands")
    @abc.abstractmethod
    def get_commands(
        self,
        _os: "Os",
        _architecture: "Architecture",
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run to in built image.

        Can be used to install packages, setup build prerequisites, etc.

        :param _os: -
        :param _architecture: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="getDockerCommands")
    def get_docker_commands(
        self,
        _os: "Os",
        _architecture: "Architecture",
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns Docker commands to run to in built image.

        Can be used to add commands like ``VOLUME``, ``ENTRYPOINT``, ``CMD``, etc.

        Docker commands are added after assets and normal commands.

        :param _os: -
        :param _architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7ff728adc7084e50163879cf938d15b8d276df893b0a66f820410e736e6b8246)
            check_type(argname="argument _os", value=_os, expected_type=type_hints["_os"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getDockerCommands", [_os, _architecture]))

    @jsii.member(jsii_name="shouldReboot")
    def should_reboot(self, _os: "Os", _architecture: "Architecture") -> builtins.bool:
        '''(experimental) Returns true if the image builder should be rebooted after this component is installed.

        :param _os: -
        :param _architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4df207340fa2acd15c1f7ba9d50447510dbe0aea58f11301ec935f4fbd00947f)
            check_type(argname="argument _os", value=_os, expected_type=type_hints["_os"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast(builtins.bool, jsii.invoke(self, "shouldReboot", [_os, _architecture]))

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''(experimental) Component name.

        Used to identify component in image build logs, and for {@link IConfigurableRunnerImageBuilder.removeComponent }

        :stability: experimental
        '''
        ...


class _RunnerImageComponentProxy(RunnerImageComponent):
    @jsii.member(jsii_name="getCommands")
    def get_commands(
        self,
        _os: "Os",
        _architecture: "Architecture",
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run to in built image.

        Can be used to install packages, setup build prerequisites, etc.

        :param _os: -
        :param _architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4ee6536536b6c0e4ddbbb0d090a8deb491f5ecb4e1271d4525e6ea2835a39ef2)
            check_type(argname="argument _os", value=_os, expected_type=type_hints["_os"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getCommands", [_os, _architecture]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) Component name.

        Used to identify component in image build logs, and for {@link IConfigurableRunnerImageBuilder.removeComponent }

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, RunnerImageComponent).__jsii_proxy_class__ = lambda : _RunnerImageComponentProxy


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerImageComponentCustomProps",
    jsii_struct_bases=[],
    name_mapping={
        "assets": "assets",
        "commands": "commands",
        "docker_commands": "dockerCommands",
        "name": "name",
    },
)
class RunnerImageComponentCustomProps:
    def __init__(
        self,
        *,
        assets: typing.Optional[typing.Sequence[typing.Union["RunnerImageAsset", typing.Dict[builtins.str, typing.Any]]]] = None,
        commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        docker_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param assets: (experimental) Assets to copy into the built image.
        :param commands: (experimental) Commands to run in the built image.
        :param docker_commands: (experimental) Docker commands to run in the built image. For example: ``['ENV foo=bar', 'RUN echo $foo']`` These commands are ignored when building AMIs.
        :param name: (experimental) Component name used for (1) image build logging and (2) identifier for {@link IConfigurableRunnerImageBuilder.removeComponent }. Name must only contain alphanumeric characters and dashes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6fe5c2d2437d742085479f02259513b739e15d569c2f5b87bf0244bf4414dece)
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument docker_commands", value=docker_commands, expected_type=type_hints["docker_commands"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assets is not None:
            self._values["assets"] = assets
        if commands is not None:
            self._values["commands"] = commands
        if docker_commands is not None:
            self._values["docker_commands"] = docker_commands
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def assets(self) -> typing.Optional[typing.List["RunnerImageAsset"]]:
        '''(experimental) Assets to copy into the built image.

        :stability: experimental
        '''
        result = self._values.get("assets")
        return typing.cast(typing.Optional[typing.List["RunnerImageAsset"]], result)

    @builtins.property
    def commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Commands to run in the built image.

        :stability: experimental
        '''
        result = self._values.get("commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def docker_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Docker commands to run in the built image.

        For example: ``['ENV foo=bar', 'RUN echo $foo']``

        These commands are ignored when building AMIs.

        :stability: experimental
        '''
        result = self._values.get("docker_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Component name used for (1) image build logging and (2) identifier for {@link IConfigurableRunnerImageBuilder.removeComponent }.

        Name must only contain alphanumeric characters and dashes.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerImageComponentCustomProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_labels": "defaultLabels",
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
    },
)
class RunnerProviderProps:
    def __init__(
        self,
        *,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Common properties for all runner providers.

        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__faa1323116edff475c54eafc82f7af57dd73527c022a54b6210c5a490a80a1d3)
            check_type(argname="argument default_labels", value=default_labels, expected_type=type_hints["default_labels"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_labels is not None:
            self._values["default_labels"] = default_labels
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options

    @builtins.property
    def default_labels(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add default labels based on OS and architecture of the runner.

        This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def retry_options(self) -> typing.Optional["ProviderRetryOptions"]:
        '''
        :deprecated: use {@link retryOptions } on {@link GitHubRunners } instead

        :stability: deprecated
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional["ProviderRetryOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RunnerVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerVersion",
):
    '''(experimental) Defines desired GitHub Actions runner version.

    :stability: experimental
    '''

    def __init__(self, version: builtins.str) -> None:
        '''
        :param version: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a20bea31f4405bffc4cb36e66dd5c0a065f92e483730a259e382a093aad9e848)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        jsii.create(self.__class__, self, [version])

    @jsii.member(jsii_name="latest")
    @builtins.classmethod
    def latest(cls) -> "RunnerVersion":
        '''(experimental) Use the latest version available at the time the runner provider image is built.

        :stability: experimental
        '''
        return typing.cast("RunnerVersion", jsii.sinvoke(cls, "latest", []))

    @jsii.member(jsii_name="specific")
    @builtins.classmethod
    def specific(cls, version: builtins.str) -> "RunnerVersion":
        '''(experimental) Use a specific version.

        :param version: GitHub Runner version.

        :see: https://github.com/actions/runner/releases
        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__044a71dfcd711f28ea336af855aef4d2c3f4fc96fdfdebe5176e2c42f33a964e)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("RunnerVersion", jsii.sinvoke(cls, "specific", [version]))

    @jsii.member(jsii_name="is")
    def is_(self, other: "RunnerVersion") -> builtins.bool:
        '''(experimental) Check if two versions are the same.

        :param other: version to compare.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__081bd4a2174b252695ac5a4c393b5cc34338749ce09a2f6e91d54fb759352a52)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(builtins.bool, jsii.invoke(self, "is", [other]))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


class ScheduledWarmRunner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.ScheduledWarmRunner",
):
    '''(experimental) Warm runners active during a time window specified by start time (``schedule``) and duration (``duration``).

    Runners will be provisioned using the specified provider and registered in the specified repository or organization.

    Registration level must match the one selected during setup.

    :see:

    https://github.com/CloudSnorkel/cdk-github-runners/blob/main/SETUP_GITHUB.md

    **Limitations**

    - **No deployment-fill**: Unlike ``AlwaysOnWarmRunner``, scheduled warm runners do not get an initial
    fill on deploy. The first fill happens at the next schedule occurrence. If you deploy at 1pm for
    a 2pm schedule, runners will not appear until 2pm.
    - Jobs will still trigger provisioning of on-demand runners, even if a warm runner ends up being used.
    - You may briefly see more than ``count`` runners when changing config or at rotation.
    - To remove: set ``count`` to 0, deploy, wait for warm runners to stop, then remove and deploy again.
    If you don't follow this procedure, warm runners may linger until they expire.
    - Provider failures or timeouts (like Lambda provider timing out after 15 minutes) will result in a
    gap in coverage until the retry succeeds. Current retry mechanism has built-in back-off rate and
    can be tweaked using ``retryOptions``. This will be improved in the future.

    Example::

    // Cron: fill at 1pm on weekdays
    new ScheduledWarmRunner(stack, 'Business Hours', {
    runners,
    provider: myProvider,
    count: 3,
    owner: 'my-org',
    repo: 'my-repo',
    schedule: events.Schedule.cron({ hour: '13', minute: '0', weekDay: 'MON-FRI' }),
    duration: cdk.Duration.hours(2),
    });

    Example::

    // Rate: fill every 12 hours
    new ScheduledWarmRunner(stack, 'Every 12 Hours', {
    runners,
    provider: myProvider,
    count: 2,
    owner: 'my-org',
    repo: 'my-repo',
    schedule: events.Schedule.rate(cdk.Duration.hours(5)),
    duration: cdk.Duration.hours(12),
    });
    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        count: jsii.Number,
        duration: "_aws_cdk_ceddda9d.Duration",
        owner: builtins.str,
        provider: typing.Union["IRunnerProvider", "ICompositeProvider"],
        runners: "GitHubRunners",
        schedule: "_aws_cdk_aws_events_ceddda9d.Schedule",
        registration_level: typing.Optional[builtins.str] = None,
        repo: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param count: (experimental) Number of warm runners to maintain.
        :param duration: (experimental) How long the warm runners should be maintained from the fill time (schedule). Defines the end of the window (schedule time + duration).
        :param owner: (experimental) GitHub owner where runners will be registered (org or user login).
        :param provider: (experimental) Provider to use. Warm runners bypass the provider selector — they always use this provider, regardless of job characteristics. Labels cannot be modified.
        :param runners: (experimental) The GitHubRunners construct that owns the shared warm runner infrastructure.
        :param schedule: (experimental) When to start filling the pool (e.g. start of business hours).
        :param registration_level: (experimental) Registration level — must match how your runners are set up in GitHub. Choose 'org' for org-wide runners, 'repo' for repo-level. See the setup wizard for choosing repo vs org. Default: 'repo'
        :param repo: (experimental) Repository name (without owner) where runners will be registered. Required when ``registrationLevel`` is 'repo'.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0e418e3ab977851661c4fdef30ab50171823bf02eb71713b5464fa33b854ad6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduledWarmRunnerProps(
            count=count,
            duration=duration,
            owner=owner,
            provider=provider,
            runners=runners,
            schedule=schedule,
            registration_level=registration_level,
            repo=repo,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ScheduledWarmRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "duration": "duration",
        "owner": "owner",
        "provider": "provider",
        "runners": "runners",
        "schedule": "schedule",
        "registration_level": "registrationLevel",
        "repo": "repo",
    },
)
class ScheduledWarmRunnerProps:
    def __init__(
        self,
        *,
        count: jsii.Number,
        duration: "_aws_cdk_ceddda9d.Duration",
        owner: builtins.str,
        provider: typing.Union["IRunnerProvider", "ICompositeProvider"],
        runners: "GitHubRunners",
        schedule: "_aws_cdk_aws_events_ceddda9d.Schedule",
        registration_level: typing.Optional[builtins.str] = None,
        repo: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for scheduled warm runners.

        :param count: (experimental) Number of warm runners to maintain.
        :param duration: (experimental) How long the warm runners should be maintained from the fill time (schedule). Defines the end of the window (schedule time + duration).
        :param owner: (experimental) GitHub owner where runners will be registered (org or user login).
        :param provider: (experimental) Provider to use. Warm runners bypass the provider selector — they always use this provider, regardless of job characteristics. Labels cannot be modified.
        :param runners: (experimental) The GitHubRunners construct that owns the shared warm runner infrastructure.
        :param schedule: (experimental) When to start filling the pool (e.g. start of business hours).
        :param registration_level: (experimental) Registration level — must match how your runners are set up in GitHub. Choose 'org' for org-wide runners, 'repo' for repo-level. See the setup wizard for choosing repo vs org. Default: 'repo'
        :param repo: (experimental) Repository name (without owner) where runners will be registered. Required when ``registrationLevel`` is 'repo'.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__64664dba439d880d957abcf8db98fc425864e0505c455f86126a974fbf07c0de)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument runners", value=runners, expected_type=type_hints["runners"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument registration_level", value=registration_level, expected_type=type_hints["registration_level"])
            check_type(argname="argument repo", value=repo, expected_type=type_hints["repo"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "duration": duration,
            "owner": owner,
            "provider": provider,
            "runners": runners,
            "schedule": schedule,
        }
        if registration_level is not None:
            self._values["registration_level"] = registration_level
        if repo is not None:
            self._values["repo"] = repo

    @builtins.property
    def count(self) -> jsii.Number:
        '''(experimental) Number of warm runners to maintain.

        :stability: experimental
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def duration(self) -> "_aws_cdk_ceddda9d.Duration":
        '''(experimental) How long the warm runners should be maintained from the fill time (schedule).

        Defines the end of the
        window (schedule time + duration).

        :stability: experimental
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast("_aws_cdk_ceddda9d.Duration", result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) GitHub owner where runners will be registered (org or user login).

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> typing.Union["IRunnerProvider", "ICompositeProvider"]:
        '''(experimental) Provider to use.

        Warm runners bypass the provider selector — they always use
        this provider, regardless of job characteristics. Labels cannot be modified.

        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(typing.Union["IRunnerProvider", "ICompositeProvider"], result)

    @builtins.property
    def runners(self) -> "GitHubRunners":
        '''(experimental) The GitHubRunners construct that owns the shared warm runner infrastructure.

        :stability: experimental
        '''
        result = self._values.get("runners")
        assert result is not None, "Required property 'runners' is missing"
        return typing.cast("GitHubRunners", result)

    @builtins.property
    def schedule(self) -> "_aws_cdk_aws_events_ceddda9d.Schedule":
        '''(experimental) When to start filling the pool (e.g. start of business hours).

        :stability: experimental
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast("_aws_cdk_aws_events_ceddda9d.Schedule", result)

    @builtins.property
    def registration_level(self) -> typing.Optional[builtins.str]:
        '''(experimental) Registration level — must match how your runners are set up in GitHub.

        Choose
        'org' for org-wide runners, 'repo' for repo-level. See the setup wizard for choosing repo vs org.

        :default: 'repo'

        :see: https://github.com/CloudSnorkel/cdk-github-runners/blob/main/SETUP_GITHUB.md
        :stability: experimental
        '''
        result = self._values.get("registration_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo(self) -> typing.Optional[builtins.str]:
        '''(experimental) Repository name (without owner) where runners will be registered.

        Required when ``registrationLevel`` is 'repo'.

        :stability: experimental
        '''
        result = self._values.get("repo")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledWarmRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Secrets(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.Secrets",
):
    '''(experimental) Secrets required for GitHub runners operation.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b58760067bc1fce42b3c98a9ce96a17f4638077eb209c6d67eb7f627614e953b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> "_aws_cdk_aws_secretsmanager_ceddda9d.Secret":
        '''(experimental) Authentication secret for GitHub containing either app details or personal access token.

        This secret is used to register runners and
        cancel jobs when the runner fails to start.

        This secret is meant to be edited by the user after being created.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_secretsmanager_ceddda9d.Secret", jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="githubPrivateKey")
    def github_private_key(self) -> "_aws_cdk_aws_secretsmanager_ceddda9d.Secret":
        '''(experimental) GitHub app private key. Not needed when using personal access tokens.

        This secret is meant to be edited by the user after being created. It is separate than the main GitHub secret because inserting private keys into JSON is hard.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_secretsmanager_ceddda9d.Secret", jsii.get(self, "githubPrivateKey"))

    @builtins.property
    @jsii.member(jsii_name="setup")
    def setup(self) -> "_aws_cdk_aws_secretsmanager_ceddda9d.Secret":
        '''(experimental) Setup secret used to authenticate user for our setup wizard.

        Should be empty after setup has been completed.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_secretsmanager_ceddda9d.Secret", jsii.get(self, "setup"))

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> "_aws_cdk_aws_secretsmanager_ceddda9d.Secret":
        '''(experimental) Webhook secret used to confirm events are coming from GitHub and nowhere else.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_secretsmanager_ceddda9d.Secret", jsii.get(self, "webhook"))


class StaticRunnerImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.StaticRunnerImage",
):
    '''(experimental) Helper class with methods to use static images that are built outside the context of this project.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromDockerHub")
    @builtins.classmethod
    def from_docker_hub(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        image: builtins.str,
        architecture: typing.Optional["Architecture"] = None,
        os: typing.Optional["Os"] = None,
    ) -> "IRunnerImageBuilder":
        '''(experimental) Create a builder from an existing Docker Hub image.

        The image must already have GitHub Actions runner installed. You are responsible to update it and remove it when done.

        We create a CodeBuild image builder behind the scenes to copy the image over to ECR. This helps avoid Docker Hub rate limits and prevent failures.

        :param scope: -
        :param id: -
        :param image: Docker Hub image with optional tag.
        :param architecture: image architecture.
        :param os: image OS.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c6aadaf28505152ad03a72118d87a28121a3699389220ce60ddab5a907b0cdce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
        return typing.cast("IRunnerImageBuilder", jsii.sinvoke(cls, "fromDockerHub", [scope, id, image, architecture, os]))

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(
        cls,
        repository: "_aws_cdk_aws_ecr_ceddda9d.IRepository",
        tag: typing.Optional[builtins.str] = None,
        architecture: typing.Optional["Architecture"] = None,
        os: typing.Optional["Os"] = None,
    ) -> "IRunnerImageBuilder":
        '''(experimental) Create a builder (that doesn't actually build anything) from an existing image in an existing repository.

        The image must already have GitHub Actions runner installed. You are responsible to update it and remove it when done.

        :param repository: ECR repository.
        :param tag: image tag.
        :param architecture: image architecture.
        :param os: image OS.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f48d8ecb3f18c1471b45f7dfd8f15c51227e04697959138092d72a9150e724a8)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
        return typing.cast("IRunnerImageBuilder", jsii.sinvoke(cls, "fromEcrRepository", [repository, tag, architecture, os]))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.StorageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "iops": "iops",
        "throughput": "throughput",
        "volume_type": "volumeType",
    },
)
class StorageOptions:
    def __init__(
        self,
        *,
        iops: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.EbsDeviceVolumeType"] = None,
    ) -> None:
        '''(experimental) Storage options for the runner instance.

        :param iops: (experimental) The number of I/O operations per second (IOPS) to provision for the volume. Must only be set for ``volumeType``: ``EbsDeviceVolumeType.IO1`` The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS, you need at least 100 GiB storage on the volume. Default: - none, required for ``EbsDeviceVolumeType.IO1``
        :param throughput: (experimental) The throughput that the volume supports, in MiB/s Takes a minimum of 125 and maximum of 1000. Default: - 125 MiB/s. Only valid on gp3 volumes.
        :param volume_type: (experimental) The EBS volume type. Default: ``EbsDeviceVolumeType.GP2``

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ec3b766929d3a048d89c7dc502f77bbbfc7357735093ebc66695a13b92f9bf82)
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iops is not None:
            self._values["iops"] = iops
        if throughput is not None:
            self._values["throughput"] = throughput
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of I/O operations per second (IOPS) to provision for the volume.

        Must only be set for ``volumeType``: ``EbsDeviceVolumeType.IO1``

        The maximum ratio of IOPS to volume size (in GiB) is 50:1, so for 5,000 provisioned IOPS,
        you need at least 100 GiB storage on the volume.

        :default: - none, required for ``EbsDeviceVolumeType.IO1``

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        :stability: experimental
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The throughput that the volume supports, in MiB/s Takes a minimum of 125 and maximum of 1000.

        :default: - 125 MiB/s. Only valid on gp3 volumes.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-volume.html#cfn-ec2-volume-throughput
        :stability: experimental
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.EbsDeviceVolumeType"]:
        '''(experimental) The EBS volume type.

        :default: ``EbsDeviceVolumeType.GP2``

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
        :stability: experimental
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.EbsDeviceVolumeType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.WeightedRunnerProvider",
    jsii_struct_bases=[],
    name_mapping={"provider": "provider", "weight": "weight"},
)
class WeightedRunnerProvider:
    def __init__(self, *, provider: "IRunnerProvider", weight: jsii.Number) -> None:
        '''(experimental) Configuration for weighted distribution of runners.

        :param provider: (experimental) The runner provider to use.
        :param weight: (experimental) Weight for this provider. Higher weights mean higher probability of selection. Must be a positive number.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a11df8e8d0b3b2cc48ff30c5ac99895a30df88812eafb3ababb862f36381ae3b)
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider": provider,
            "weight": weight,
        }

    @builtins.property
    def provider(self) -> "IRunnerProvider":
        '''(experimental) The runner provider to use.

        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast("IRunnerProvider", result)

    @builtins.property
    def weight(self) -> jsii.Number:
        '''(experimental) Weight for this provider.

        Higher weights mean higher probability of selection.
        Must be a positive number.

        :stability: experimental
        '''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WeightedRunnerProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsComponents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.WindowsComponents",
):
    '''(deprecated) Components for Windows that can be used with AWS Image Builder based builders.

    These cannot be used by {@link CodeBuildImageBuilder }.

    :deprecated: Use ``RunnerImageComponent`` instead.

    :stability: deprecated
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsCli")
    @builtins.classmethod
    def aws_cli(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0c68c27f668327e6aeb3b0e5b7e88235ae547046edeb1fa6a808b729a31b7bd2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "awsCli", [scope, id]))

    @jsii.member(jsii_name="cloudwatchAgent")
    @builtins.classmethod
    def cloudwatch_agent(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__87d18e04aa4683610d276ffab3f0570d771274749e3013b977bcb8fa1e76f45e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "cloudwatchAgent", [scope, id]))

    @jsii.member(jsii_name="docker")
    @builtins.classmethod
    def docker(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6d0154389d6d3b175e2f67c0a3396f61d6bbb3095e54e09e25fe5e60e047b40b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "docker", [scope, id]))

    @jsii.member(jsii_name="extraCertificates")
    @builtins.classmethod
    def extra_certificates(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        path: builtins.str,
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param path: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__13fed2553bd6ff4aa9a60d780bfb72824212d74795a0e85c85c1d1253cc4db69)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "extraCertificates", [scope, id, path]))

    @jsii.member(jsii_name="git")
    @builtins.classmethod
    def git(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__900bdb4c3fd73b8c9f97280217bdcc95dbbeee03c9f7f15d53d398b09f7716fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "git", [scope, id]))

    @jsii.member(jsii_name="githubCli")
    @builtins.classmethod
    def github_cli(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__93a39cf569b605cb085761e993915b9d261ed5d3b804d0b9f4c2cf1ea3606c06)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "githubCli", [scope, id]))

    @jsii.member(jsii_name="githubRunner")
    @builtins.classmethod
    def github_runner(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        runner_version: "RunnerVersion",
    ) -> "ImageBuilderComponent":
        '''
        :param scope: -
        :param id: -
        :param runner_version: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a0edb989a5946c92ba1761a899ffffa9fea018497911c40c9c0dae502a637f40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
        return typing.cast("ImageBuilderComponent", jsii.sinvoke(cls, "githubRunner", [scope, id, runner_version]))


@jsii.implements(IRunnerImageBuilder)
class AmiBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.AmiBuilder",
):
    '''(deprecated) An AMI builder that uses AWS Image Builder to build AMIs pre-baked with all the GitHub Actions runner requirements.

    Builders can be used with {@link Ec2RunnerProvider }.

    Each builder re-runs automatically at a set interval to make sure the AMIs contain the latest versions of everything.

    You can create an instance of this construct to customize the AMI used to spin-up runners. Some runner providers may require custom components. Check the runner provider documentation.

    For example, to set a specific runner version, rebuild the image every 2 weeks, and add a few packages for the EC2 provider, use::

       const builder = new AmiBuilder(this, 'Builder', {
           runnerVersion: RunnerVersion.specific('2.293.0'),
           rebuildInterval: Duration.days(14),
       });
       builder.addComponent(new ImageBuilderComponent(scope, id, {
         platform: 'Linux',
         displayName: 'p7zip',
         description: 'Install some more packages',
         commands: [
           'apt-get install p7zip',
         ],
       }));
       new Ec2RunnerProvider(this, 'EC2 provider', {
           labels: ['custom-ec2'],
           amiBuilder: builder,
       });

    :deprecated: use RunnerImageBuilder, e.g. with Ec2RunnerProvider.imageBuilder()

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        install_docker: typing.Optional[builtins.bool] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param install_docker: (experimental) Install Docker inside the image, so it can be used by the runner. Default: true
        :param instance_type: (experimental) The instance type used to build the image. Default: m6i.large
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param rebuild_interval: (experimental) Schedule the AMI to be rebuilt every given interval. Useful for keeping the AMI up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (deprecated) Security group to assign to launched builder instances. Default: new security group
        :param security_groups: (experimental) Security groups to assign to launched builder instances. Default: new security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param vpc: (experimental) VPC where builder instances will be launched. Default: default account VPC

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__625361a368f8eabbfa2d2951b1d7aff4d2f57b6d8d5cdaa78c2db82b204cc254)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AmiBuilderProps(
            architecture=architecture,
            install_docker=install_docker,
            instance_type=instance_type,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addComponent")
    def add_component(self, component: "ImageBuilderComponent") -> None:
        '''(deprecated) Add a component to be installed.

        :param component: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9747ce69b89d4dbf55b31806bc58d53721577273c2cbfc7864620d8a463b9796)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "addComponent", [component]))

    @jsii.member(jsii_name="addExtraCertificates")
    def add_extra_certificates(self, path: builtins.str) -> None:
        '''(deprecated) Add extra trusted certificates.

        This helps deal with self-signed certificates for GitHub Enterprise Server.

        :param path: path to directory containing a file called certs.pem containing all the required certificates.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__74248b6087eb378ee00c6fedecd54fd91eef1eacead09cd38466e3085a87ab9f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.invoke(self, "addExtraCertificates", [path]))

    @jsii.member(jsii_name="bindAmi")
    def bind_ami(self) -> "RunnerAmi":
        '''(deprecated) Called by IRunnerProvider to finalize settings and create the AMI builder.

        :stability: deprecated
        '''
        return typing.cast("RunnerAmi", jsii.invoke(self, "bindAmi", []))

    @jsii.member(jsii_name="bindDockerImage")
    def bind_docker_image(self) -> "RunnerImage":
        '''(deprecated) Build and return a Docker image with GitHub Runner installed in it.

        Anything that ends up with an ECR repository containing a Docker image that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing image and nothing else.

        It's important that the specified image tag be available at the time the repository is available. Providers usually assume the image is ready and will fail if it's not.

        The image can be further updated over time manually or using a schedule as long as it is always written to the same tag.

        :stability: deprecated
        '''
        return typing.cast("RunnerImage", jsii.invoke(self, "bindDockerImage", []))

    @jsii.member(jsii_name="createImage")
    def _create_image(
        self,
        infra: "_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration",
        dist: "_aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration",
        log: "_aws_cdk_aws_logs_ceddda9d.LogGroup",
        image_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_arn: typing.Optional[builtins.str] = None,
    ) -> "_aws_cdk_aws_imagebuilder_ceddda9d.CfnImage":
        '''
        :param infra: -
        :param dist: -
        :param log: -
        :param image_recipe_arn: -
        :param container_recipe_arn: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e0d9489ff52404cba57c43261d3ed74a1b9f4f798ae49c0058cd84430a429021)
            check_type(argname="argument infra", value=infra, expected_type=type_hints["infra"])
            check_type(argname="argument dist", value=dist, expected_type=type_hints["dist"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast("_aws_cdk_aws_imagebuilder_ceddda9d.CfnImage", jsii.invoke(self, "createImage", [infra, dist, log, image_recipe_arn, container_recipe_arn]))

    @jsii.member(jsii_name="createInfrastructure")
    def _create_infrastructure(
        self,
        managed_policies: typing.Sequence["_aws_cdk_aws_iam_ceddda9d.IManagedPolicy"],
    ) -> "_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration":
        '''
        :param managed_policies: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__51f1cb907bb1baffb27dbf2a76a4c4c810656d94df878155237526f4cef49cb6)
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
        return typing.cast("_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration", jsii.invoke(self, "createInfrastructure", [managed_policies]))

    @jsii.member(jsii_name="createLog")
    def _create_log(
        self,
        recipe_name: builtins.str,
    ) -> "_aws_cdk_aws_logs_ceddda9d.LogGroup":
        '''
        :param recipe_name: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__af2c57a50959e16c9926951dc35e40bda4192b464bff123578e463523039b935)
            check_type(argname="argument recipe_name", value=recipe_name, expected_type=type_hints["recipe_name"])
        return typing.cast("_aws_cdk_aws_logs_ceddda9d.LogGroup", jsii.invoke(self, "createLog", [recipe_name]))

    @jsii.member(jsii_name="createPipeline")
    def _create_pipeline(
        self,
        infra: "_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration",
        dist: "_aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration",
        log: "_aws_cdk_aws_logs_ceddda9d.LogGroup",
        image_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_arn: typing.Optional[builtins.str] = None,
    ) -> "_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline":
        '''
        :param infra: -
        :param dist: -
        :param log: -
        :param image_recipe_arn: -
        :param container_recipe_arn: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ce32f249fb7ba35579acf4098c5c404f576dcfa3eebf6d32b1ef120b5b109f1f)
            check_type(argname="argument infra", value=infra, expected_type=type_hints["infra"])
            check_type(argname="argument dist", value=dist, expected_type=type_hints["dist"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast("_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline", jsii.invoke(self, "createPipeline", [infra, dist, log, image_recipe_arn, container_recipe_arn]))

    @jsii.member(jsii_name="prependComponent")
    def prepend_component(self, component: "ImageBuilderComponent") -> None:
        '''(deprecated) Add a component to be installed before any other components.

        Useful for required system settings like certificates or proxy settings.

        :param component: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8124976feff345d9400fd0ffd91955fd1a5585bddbcf348d2fa89a8495bf54b7)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "prependComponent", [component]))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def _architecture(self) -> "Architecture":
        '''
        :stability: deprecated
        '''
        return typing.cast("Architecture", jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(deprecated) The network connections associated with this resource.

        :stability: deprecated
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def _description(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="os")
    def _os(self) -> "Os":
        '''
        :stability: deprecated
        '''
        return typing.cast("Os", jsii.get(self, "os"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def _platform(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="runnerVersion")
    def _runner_version(self) -> "RunnerVersion":
        '''
        :stability: deprecated
        '''
        return typing.cast("RunnerVersion", jsii.get(self, "runnerVersion"))

    @builtins.property
    @jsii.member(jsii_name="components")
    def _components(self) -> typing.List["ImageBuilderComponent"]:
        '''
        :stability: deprecated
        '''
        return typing.cast(typing.List["ImageBuilderComponent"], jsii.get(self, "components"))

    @_components.setter
    def _components(self, value: typing.List["ImageBuilderComponent"]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8088868062a70621aab7b900883cf52d9c930de8a458039564d69a7d0cc80f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value)


@jsii.implements(IRunnerImageBuilder)
class CodeBuildImageBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildImageBuilder",
):
    '''(deprecated) An image builder that uses CodeBuild to build Docker images pre-baked with all the GitHub Actions runner requirements.

    Builders can be used with runner providers.

    Each builder re-runs automatically at a set interval to make sure the images contain the latest versions of everything.

    You can create an instance of this construct to customize the image used to spin-up runners. Each provider has its own requirements for what an image should do. That's why they each provide their own Dockerfile.

    For example, to set a specific runner version, rebuild the image every 2 weeks, and add a few packages for the Fargate provider, use::

       const builder = new CodeBuildImageBuilder(this, 'Builder', {
           dockerfilePath: FargateRunnerProvider.LINUX_X64_DOCKERFILE_PATH,
           runnerVersion: RunnerVersion.specific('2.293.0'),
           rebuildInterval: Duration.days(14),
       });
       builder.setBuildArg('EXTRA_PACKAGES', 'nginx xz-utils');
       new FargateRunnerProvider(this, 'Fargate provider', {
           labels: ['customized-fargate'],
           imageBuilder: builder,
       });

    :deprecated: use RunnerImageBuilder

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        dockerfile_path: builtins.str,
        architecture: typing.Optional["Architecture"] = None,
        build_image: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.IBuildImage"] = None,
        compute_type: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param dockerfile_path: (experimental) Path to Dockerfile to be built. It can be a path to a Dockerfile, a folder containing a Dockerfile, or a zip file containing a Dockerfile.
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param build_image: (experimental) Build image to use in CodeBuild. This is the image that's going to run the code that builds the runner image. The only action taken in CodeBuild is running ``docker build``. You would therefore not need to change this setting often. Default: Ubuntu 22.04 for x64 and Amazon Linux 2 for ARM64
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: {@link ComputeType#SMALL }
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (experimental) Security Group to assign to this instance. Default: public project with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to build the image in. Default: no VPC

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__61a03ba99d5c1cb98c8dcc6a1f21ec4e7ff6c73bbe85e6ed2102fe51075fd8f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeBuildImageBuilderProps(
            dockerfile_path=dockerfile_path,
            architecture=architecture,
            build_image=build_image,
            compute_type=compute_type,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_group=security_group,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addExtraCertificates")
    def add_extra_certificates(self, path: builtins.str) -> None:
        '''(deprecated) Add extra trusted certificates. This helps deal with self-signed certificates for GitHub Enterprise Server.

        All first party Dockerfiles support this. Others may not.

        :param path: path to directory containing a file called certs.pem containing all the required certificates.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5977c467d0631ac1513843c39f63ce74892cd360d8ed6de11a85ee5d410b7566)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.invoke(self, "addExtraCertificates", [path]))

    @jsii.member(jsii_name="addFiles")
    def add_files(self, source_path: builtins.str, dest_name: builtins.str) -> None:
        '''(deprecated) Uploads a folder to the build server at a given folder name.

        :param source_path: path to source directory.
        :param dest_name: name of destination folder.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__99d392c7ee36222706a353bc6e75a56046571240436fc791fa66816e528d197d)
            check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            check_type(argname="argument dest_name", value=dest_name, expected_type=type_hints["dest_name"])
        return typing.cast(None, jsii.invoke(self, "addFiles", [source_path, dest_name]))

    @jsii.member(jsii_name="addPolicyStatement")
    def add_policy_statement(
        self,
        statement: "_aws_cdk_aws_iam_ceddda9d.PolicyStatement",
    ) -> None:
        '''(deprecated) Add a policy statement to the builder to access resources required to the image build.

        :param statement: IAM policy statement.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__eee162d5d2373c52a16033f2b8f554c6228060793fcb0d2aa63121dc74eb82e1)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addPolicyStatement", [statement]))

    @jsii.member(jsii_name="addPostBuildCommand")
    def add_post_build_command(self, command: builtins.str) -> None:
        '''(deprecated) Adds a command that runs after ``docker build`` and ``docker push``.

        :param command: command to add.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1cf227e615cf526a927f3b0a0695ce9ea199758f87a664a9cce5ec90fd388bfd)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        return typing.cast(None, jsii.invoke(self, "addPostBuildCommand", [command]))

    @jsii.member(jsii_name="addPreBuildCommand")
    def add_pre_build_command(self, command: builtins.str) -> None:
        '''(deprecated) Adds a command that runs before ``docker build``.

        :param command: command to add.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8252ffd4dd18dc431c781dc95c9cb4cd57710a688e4e22640b839bb707d91bf1)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        return typing.cast(None, jsii.invoke(self, "addPreBuildCommand", [command]))

    @jsii.member(jsii_name="bindAmi")
    def bind_ami(self) -> "RunnerAmi":
        '''(deprecated) Build and return an AMI with GitHub Runner installed in it.

        Anything that ends up with a launch template pointing to an AMI that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing AMI and nothing else.

        The AMI can be further updated over time manually or using a schedule as long as it is always written to the same launch template.

        :stability: deprecated
        '''
        return typing.cast("RunnerAmi", jsii.invoke(self, "bindAmi", []))

    @jsii.member(jsii_name="bindDockerImage")
    def bind_docker_image(self) -> "RunnerImage":
        '''(deprecated) Called by IRunnerProvider to finalize settings and create the image builder.

        :stability: deprecated
        '''
        return typing.cast("RunnerImage", jsii.invoke(self, "bindDockerImage", []))

    @jsii.member(jsii_name="setBuildArg")
    def set_build_arg(self, name: builtins.str, value: builtins.str) -> None:
        '''(deprecated) Adds a build argument for Docker.

        See the documentation for the Dockerfile you're using for a list of supported build arguments.

        :param name: build argument name.
        :param value: build argument value.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3b8a5cd687fe02e670471554b7ec420ad3b88d98e1f0157b5b890fd4c6f3f283)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setBuildArg", [name, value]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''
        :stability: deprecated
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CodeBuildImageBuilderProps":
        '''
        :stability: deprecated
        '''
        return typing.cast("CodeBuildImageBuilderProps", jsii.get(self, "props"))


@jsii.implements(IRunnerProvider, _constructs_77d1e7e8.IConstruct)
class CodeBuildRunnerProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildRunnerProvider",
):
    '''(experimental) GitHub Actions runner provider using CodeBuild to execute jobs.

    Creates a project that gets started for each job.

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        compute_type: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"] = None,
        docker_in_docker: typing.Optional[builtins.bool] = None,
        gpu: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. The compute type determines CPU, memory, and disk space: - SMALL: 2 vCPU, 3 GB RAM, 64 GB disk - MEDIUM: 4 vCPU, 7 GB RAM, 128 GB disk - LARGE: 8 vCPU, 15 GB RAM, 128 GB disk - X2_LARGE: 72 vCPU, 145 GB RAM, 256 GB disk (Linux) or 824 GB disk (Windows) Use a larger compute type when you need more disk space for building larger Docker images. For more details, see https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types Default: {@link ComputeType#SMALL }
        :param docker_in_docker: (experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required CodeBuild privileged mode. Disabling this can speed up provisioning of CodeBuild runners. If you don't intend on running or building Docker images, disable this for faster start-up times. Default: true
        :param gpu: (experimental) Use GPU compute for builds. When enabled, the default compute type is BUILD_GENERAL1_SMALL (4 vCPU, 16 GB RAM, 1 NVIDIA A10G GPU). You can override the compute type using the ``computeType`` property (for example, to use BUILD_GENERAL1_LARGE for more resources), subject to the supported GPU compute types. When using GPU compute, ensure your runner image includes any required GPU libraries (for example, CUDA) either by using a base image that has them preinstalled (such as an appropriate nvidia/cuda image) or by adding image components that install them. The default image builder does not automatically switch to a CUDA-enabled base image when GPU is enabled. GPU compute is only available for Linux x64 images. Not supported on Windows or ARM. Default: false
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder must contain the {@link RunnerImageComponent.docker} component unless ``dockerInDocker`` is set to false. The image builder determines the OS and architecture of the runner. Default: CodeBuildRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['codebuild']
        :param security_group: (deprecated) Security group to assign to this instance. Default: public project with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: a new security group, if {@link vpc } is used
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bb924a0cf987a9f87f4ad0ebd952c61ebd4e02d7d83501b9600f14157c110e9b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeBuildRunnerProviderProps(
            compute_type=compute_type,
            docker_in_docker=docker_in_docker,
            gpu=gpu,
            group=group,
            image_builder=image_builder,
            label=label,
            labels=labels,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="imageBuilder")
    @builtins.classmethod
    def image_builder(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        aws_image_builder_options: typing.Optional[typing.Union["AwsImageBuilderRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        base_ami: typing.Optional[typing.Union[builtins.str, "BaseImage"]] = None,
        base_docker_image: typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]] = None,
        builder_type: typing.Optional["RunnerImageBuilderType"] = None,
        code_build_options: typing.Optional[typing.Union["CodeBuildRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        components: typing.Optional[typing.Sequence["RunnerImageComponent"]] = None,
        docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        wait_on_deploy: typing.Optional[builtins.bool] = None,
    ) -> "IConfigurableRunnerImageBuilder":
        '''(experimental) Create new image builder that builds CodeBuild specific runner images.

        You can customize the OS, architecture, VPC, subnet, security groups, etc. by passing in props.

        You can add components to the image builder by calling ``imageBuilder.addComponent()``.

        The default OS is Ubuntu running on x64 architecture.

        Included components:

        - ``RunnerImageComponent.requiredPackages()``
        - ``RunnerImageComponent.runnerUser()``
        - ``RunnerImageComponent.git()``
        - ``RunnerImageComponent.githubCli()``
        - ``RunnerImageComponent.awsCli()``
        - ``RunnerImageComponent.docker()``
        - ``RunnerImageComponent.githubRunner()``

        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param aws_image_builder_options: (experimental) Options specific to AWS Image Builder. Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.
        :param base_ami: (experimental) Base AMI from which runner AMIs will be built. This can be: - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead - A BaseImage instance created using static factory methods: - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.) - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter. Default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS
        :param base_docker_image: (experimental) Base image from which Docker runner images will be built. This can be: - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead - A BaseContainerImage instance created using static factory methods: - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild) - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}. Default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS
        :param builder_type: Default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI
        :param code_build_options: (experimental) Options specific to CodeBuild image builder. Only used when builderType is RunnerImageBuilderType.CODE_BUILD.
        :param components: (experimental) Components to install on the image. Default: none
        :param docker_setup_commands: (experimental) Additional commands to run on the build host before starting the Docker runner image build. Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images. Default: []
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX_UBUNTU
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_groups: (experimental) Security Groups to assign to this instance.
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param vpc: (experimental) VPC to build the image in. Default: no VPC
        :param wait_on_deploy: (experimental) Wait for image to finish building during deployment. It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build. Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used. Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5b74a56ca854b011edea7d259b730771e5a994081db1aa0bdbea8b3e2b668120)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunnerImageBuilderProps(
            architecture=architecture,
            aws_image_builder_options=aws_image_builder_options,
            base_ami=base_ami,
            base_docker_image=base_docker_image,
            builder_type=builder_type,
            code_build_options=code_build_options,
            components=components,
            docker_setup_commands=docker_setup_commands,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
            wait_on_deploy=wait_on_deploy,
        )

        return typing.cast("IConfigurableRunnerImageBuilder", jsii.sinvoke(cls, "imageBuilder", [scope, id, props]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__149d854003aceddd7320ff6f28772f8f4f60386fcf64a37bc0b8e500c26f7b5b)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_ARM64_DOCKERFILE_PATH")
    @builtins.classmethod
    def LINUX_ARM64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(deprecated) Path to Dockerfile for Linux ARM64 with all the requirements for CodeBuild runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be an Ubuntu compatible image.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.
        - ``DOCKER_CHANNEL`` overrides the channel from which Docker will be downloaded. Defaults to ``"stable"``.
        - ``DIND_COMMIT`` overrides the commit where dind is found.
        - ``DOCKER_VERSION`` overrides the installed Docker version.
        - ``DOCKER_COMPOSE_VERSION`` overrides the installed docker-compose version.

        :deprecated: Use ``imageBuilder()`` instead.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_ARM64_DOCKERFILE_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_X64_DOCKERFILE_PATH")
    @builtins.classmethod
    def LINUX_X64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(deprecated) Path to Dockerfile for Linux x64 with all the requirements for CodeBuild runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be an Ubuntu compatible image.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.
        - ``DOCKER_CHANNEL`` overrides the channel from which Docker will be downloaded. Defaults to ``"stable"``.
        - ``DIND_COMMIT`` overrides the commit where dind is found.
        - ``DOCKER_VERSION`` overrides the installed Docker version.
        - ``DOCKER_COMPOSE_VERSION`` overrides the installed docker-compose version.

        :deprecated: Use ``imageBuilder()`` instead.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_X64_DOCKERFILE_PATH"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "_aws_cdk_aws_iam_ceddda9d.IPrincipal":
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.IPrincipal", jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> "RunnerImage":
        '''(deprecated) Docker image loaded with GitHub Actions Runner and its prerequisites.

        The image is built by an image builder and is specific to CodeBuild.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast("RunnerImage", jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> "_aws_cdk_aws_logs_ceddda9d.ILogGroup":
        '''(experimental) Log group where provided runners will save their logs.

        Note that this is not the job log, but the runner itself. It will not contain output from the GitHub Action but only metadata on its execution.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_logs_ceddda9d.ILogGroup", jsii.get(self, "logGroup"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "_aws_cdk_aws_codebuild_ceddda9d.Project":
        '''(experimental) CodeBuild project hosting the runner.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_codebuild_ceddda9d.Project", jsii.get(self, "project"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildRunnerProviderProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "default_labels": "defaultLabels",
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "compute_type": "computeType",
        "docker_in_docker": "dockerInDocker",
        "gpu": "gpu",
        "group": "group",
        "image_builder": "imageBuilder",
        "label": "label",
        "labels": "labels",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class CodeBuildRunnerProviderProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compute_type: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"] = None,
        docker_in_docker: typing.Optional[builtins.bool] = None,
        gpu: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. The compute type determines CPU, memory, and disk space: - SMALL: 2 vCPU, 3 GB RAM, 64 GB disk - MEDIUM: 4 vCPU, 7 GB RAM, 128 GB disk - LARGE: 8 vCPU, 15 GB RAM, 128 GB disk - X2_LARGE: 72 vCPU, 145 GB RAM, 256 GB disk (Linux) or 824 GB disk (Windows) Use a larger compute type when you need more disk space for building larger Docker images. For more details, see https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types Default: {@link ComputeType#SMALL }
        :param docker_in_docker: (experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required CodeBuild privileged mode. Disabling this can speed up provisioning of CodeBuild runners. If you don't intend on running or building Docker images, disable this for faster start-up times. Default: true
        :param gpu: (experimental) Use GPU compute for builds. When enabled, the default compute type is BUILD_GENERAL1_SMALL (4 vCPU, 16 GB RAM, 1 NVIDIA A10G GPU). You can override the compute type using the ``computeType`` property (for example, to use BUILD_GENERAL1_LARGE for more resources), subject to the supported GPU compute types. When using GPU compute, ensure your runner image includes any required GPU libraries (for example, CUDA) either by using a base image that has them preinstalled (such as an appropriate nvidia/cuda image) or by adding image components that install them. The default image builder does not automatically switch to a CUDA-enabled base image when GPU is enabled. GPU compute is only available for Linux x64 images. Not supported on Windows or ARM. Default: false
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder must contain the {@link RunnerImageComponent.docker} component unless ``dockerInDocker`` is set to false. The image builder determines the OS and architecture of the runner. Default: CodeBuildRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['codebuild']
        :param security_group: (deprecated) Security group to assign to this instance. Default: public project with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: a new security group, if {@link vpc } is used
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9377dcf4cd4dae74730635bdaf02246acb473843cea2856cf9a64295df964eb6)
            check_type(argname="argument default_labels", value=default_labels, expected_type=type_hints["default_labels"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument docker_in_docker", value=docker_in_docker, expected_type=type_hints["docker_in_docker"])
            check_type(argname="argument gpu", value=gpu, expected_type=type_hints["gpu"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument image_builder", value=image_builder, expected_type=type_hints["image_builder"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_labels is not None:
            self._values["default_labels"] = default_labels
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if docker_in_docker is not None:
            self._values["docker_in_docker"] = docker_in_docker
        if gpu is not None:
            self._values["gpu"] = gpu
        if group is not None:
            self._values["group"] = group
        if image_builder is not None:
            self._values["image_builder"] = image_builder
        if label is not None:
            self._values["label"] = label
        if labels is not None:
            self._values["labels"] = labels
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def default_labels(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add default labels based on OS and architecture of the runner.

        This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def retry_options(self) -> typing.Optional["ProviderRetryOptions"]:
        '''
        :deprecated: use {@link retryOptions } on {@link GitHubRunners } instead

        :stability: deprecated
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional["ProviderRetryOptions"], result)

    @builtins.property
    def compute_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"]:
        '''(experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values.

        The compute type determines CPU, memory, and disk space:

        - SMALL: 2 vCPU, 3 GB RAM, 64 GB disk
        - MEDIUM: 4 vCPU, 7 GB RAM, 128 GB disk
        - LARGE: 8 vCPU, 15 GB RAM, 128 GB disk
        - X2_LARGE: 72 vCPU, 145 GB RAM, 256 GB disk (Linux) or 824 GB disk (Windows)

        Use a larger compute type when you need more disk space for building larger Docker images.

        For more details, see https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types

        :default: {@link ComputeType#SMALL }

        :stability: experimental
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"], result)

    @builtins.property
    def docker_in_docker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required CodeBuild privileged mode.

        Disabling this can
        speed up provisioning of CodeBuild runners. If you don't intend on running or building Docker images, disable this for faster start-up times.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("docker_in_docker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def gpu(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use GPU compute for builds.

        When enabled, the default compute type is BUILD_GENERAL1_SMALL (4 vCPU, 16 GB RAM, 1 NVIDIA A10G GPU).

        You can override the compute type using the ``computeType`` property (for example, to use BUILD_GENERAL1_LARGE for more resources),
        subject to the supported GPU compute types.

        When using GPU compute, ensure your runner image includes any required GPU libraries (for example, CUDA)
        either by using a base image that has them preinstalled (such as an appropriate nvidia/cuda image) or by
        adding image components that install them. The default image builder does not automatically switch to a
        CUDA-enabled base image when GPU is enabled.

        GPU compute is only available for Linux x64 images. Not supported on Windows or ARM.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("gpu")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub Actions runner group name.

        If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It
        requires a paid GitHub account and organization level runner registration.

        The group must exist or the runner will not start.

        Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_builder(self) -> typing.Optional["IRunnerImageBuilder"]:
        '''(experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements.

        The image builder must contain the {@link RunnerImageComponent.docker} component unless ``dockerInDocker`` is set to false.

        The image builder determines the OS and architecture of the runner.

        :default: CodeBuildRunnerProvider.imageBuilder()

        :stability: experimental
        '''
        result = self._values.get("image_builder")
        return typing.cast(typing.Optional["IRunnerImageBuilder"], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(deprecated) GitHub Actions label used for this provider.

        :default: undefined

        :deprecated: use {@link labels } instead

        :stability: deprecated
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['codebuild']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(deprecated) Security group to assign to this instance.

        :default: public project with no security group

        :deprecated: use {@link securityGroups }

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security groups to assign to this instance.

        :default: a new security group, if {@link vpc } is used

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        :default: Duration.hours(1)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC to launch the runners in.

        :default: no VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildRunnerProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRunnerImageBuilder)
class ContainerImageBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.ContainerImageBuilder",
):
    '''(deprecated) An image builder that uses AWS Image Builder to build Docker images pre-baked with all the GitHub Actions runner requirements.

    Builders can be used with runner providers.

    The CodeBuild builder is better and faster. Only use this one if you have no choice. For example, if you need Windows containers.

    Each builder re-runs automatically at a set interval to make sure the images contain the latest versions of everything.

    You can create an instance of this construct to customize the image used to spin-up runners. Some runner providers may require custom components. Check the runner provider documentation. The default components work with CodeBuild and Fargate.

    For example, to set a specific runner version, rebuild the image every 2 weeks, and add a few packages for the Fargate provider, use::

       const builder = new ContainerImageBuilder(this, 'Builder', {
           runnerVersion: RunnerVersion.specific('2.293.0'),
           rebuildInterval: Duration.days(14),
       });
       new CodeBuildRunnerProvider(this, 'CodeBuild provider', {
           labels: ['custom-codebuild'],
           imageBuilder: builder,
       });

    :deprecated: use RunnerImageBuilder

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        parent_image: typing.Optional[builtins.str] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param instance_type: (experimental) The instance type used to build the image. Default: m6i.large
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param parent_image: (experimental) Parent image for the new Docker Image. You can use either Image Builder image ARN or public registry image. Default: 'mcr.microsoft.com/windows/servercore:ltsc2019-amd64'
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (deprecated) Security group to assign to launched builder instances. Default: new security group
        :param security_groups: (experimental) Security groups to assign to launched builder instances. Default: new security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: default VPC subnet
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a61ba73c795872c9aa5e24ac4480b00db813c358539591499a6767701e246ecc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ContainerImageBuilderProps(
            architecture=architecture,
            instance_type=instance_type,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            parent_image=parent_image,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addComponent")
    def add_component(self, component: "ImageBuilderComponent") -> None:
        '''(deprecated) Add a component to be installed.

        :param component: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__54d5aa0a2ebc88884861dcaec651d073dd4411ff3bb5497bc7dcffc8faca6a48)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "addComponent", [component]))

    @jsii.member(jsii_name="addExtraCertificates")
    def add_extra_certificates(self, path: builtins.str) -> None:
        '''(deprecated) Add extra trusted certificates. This helps deal with self-signed certificates for GitHub Enterprise Server.

        All first party Dockerfiles support this. Others may not.

        :param path: path to directory containing a file called certs.pem containing all the required certificates.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__224b352e0817976406c67254ec8d2bf9bac77c2647873ddcd2f95568571ee3c9)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.invoke(self, "addExtraCertificates", [path]))

    @jsii.member(jsii_name="bindAmi")
    def bind_ami(self) -> "RunnerAmi":
        '''(deprecated) Build and return an AMI with GitHub Runner installed in it.

        Anything that ends up with a launch template pointing to an AMI that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing AMI and nothing else.

        The AMI can be further updated over time manually or using a schedule as long as it is always written to the same launch template.

        :stability: deprecated
        '''
        return typing.cast("RunnerAmi", jsii.invoke(self, "bindAmi", []))

    @jsii.member(jsii_name="bindDockerImage")
    def bind_docker_image(self) -> "RunnerImage":
        '''(deprecated) Called by IRunnerProvider to finalize settings and create the image builder.

        :stability: deprecated
        '''
        return typing.cast("RunnerImage", jsii.invoke(self, "bindDockerImage", []))

    @jsii.member(jsii_name="createImage")
    def _create_image(
        self,
        infra: "_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration",
        dist: "_aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration",
        log: "_aws_cdk_aws_logs_ceddda9d.LogGroup",
        image_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_arn: typing.Optional[builtins.str] = None,
    ) -> "_aws_cdk_aws_imagebuilder_ceddda9d.CfnImage":
        '''
        :param infra: -
        :param dist: -
        :param log: -
        :param image_recipe_arn: -
        :param container_recipe_arn: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8117d158d639350efd9e0c32a50eaf83954ebcc7a687759681ab20d2930337c1)
            check_type(argname="argument infra", value=infra, expected_type=type_hints["infra"])
            check_type(argname="argument dist", value=dist, expected_type=type_hints["dist"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast("_aws_cdk_aws_imagebuilder_ceddda9d.CfnImage", jsii.invoke(self, "createImage", [infra, dist, log, image_recipe_arn, container_recipe_arn]))

    @jsii.member(jsii_name="createInfrastructure")
    def _create_infrastructure(
        self,
        managed_policies: typing.Sequence["_aws_cdk_aws_iam_ceddda9d.IManagedPolicy"],
    ) -> "_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration":
        '''
        :param managed_policies: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__15cc0053b03b95f450f5e13113627e405c2bfea1a5b08cd36cd5647a79a4430f)
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
        return typing.cast("_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration", jsii.invoke(self, "createInfrastructure", [managed_policies]))

    @jsii.member(jsii_name="createLog")
    def _create_log(
        self,
        recipe_name: builtins.str,
    ) -> "_aws_cdk_aws_logs_ceddda9d.LogGroup":
        '''
        :param recipe_name: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4281ad903ec2ef54b36fdccf3f500d5e4c37e5eee693fdfd781ec26563b31766)
            check_type(argname="argument recipe_name", value=recipe_name, expected_type=type_hints["recipe_name"])
        return typing.cast("_aws_cdk_aws_logs_ceddda9d.LogGroup", jsii.invoke(self, "createLog", [recipe_name]))

    @jsii.member(jsii_name="createPipeline")
    def _create_pipeline(
        self,
        infra: "_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration",
        dist: "_aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration",
        log: "_aws_cdk_aws_logs_ceddda9d.LogGroup",
        image_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_arn: typing.Optional[builtins.str] = None,
    ) -> "_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline":
        '''
        :param infra: -
        :param dist: -
        :param log: -
        :param image_recipe_arn: -
        :param container_recipe_arn: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c3e3a91f74cb641217038e41062fccd039108dc4ddbfe446bb99732081a4e4b0)
            check_type(argname="argument infra", value=infra, expected_type=type_hints["infra"])
            check_type(argname="argument dist", value=dist, expected_type=type_hints["dist"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast("_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline", jsii.invoke(self, "createPipeline", [infra, dist, log, image_recipe_arn, container_recipe_arn]))

    @jsii.member(jsii_name="prependComponent")
    def prepend_component(self, component: "ImageBuilderComponent") -> None:
        '''(deprecated) Add a component to be installed before any other components.

        Useful for required system settings like certificates or proxy settings.

        :param component: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d078b80933c0ce3a1dec052eeae9dc31f2640b3def938bf732dcd3276e6f8964)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "prependComponent", [component]))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def _architecture(self) -> "Architecture":
        '''
        :stability: deprecated
        '''
        return typing.cast("Architecture", jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(deprecated) The network connections associated with this resource.

        :stability: deprecated
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def _description(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="os")
    def _os(self) -> "Os":
        '''
        :stability: deprecated
        '''
        return typing.cast("Os", jsii.get(self, "os"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def _platform(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> "_aws_cdk_aws_ecr_ceddda9d.IRepository":
        '''
        :stability: deprecated
        '''
        return typing.cast("_aws_cdk_aws_ecr_ceddda9d.IRepository", jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="runnerVersion")
    def _runner_version(self) -> "RunnerVersion":
        '''
        :stability: deprecated
        '''
        return typing.cast("RunnerVersion", jsii.get(self, "runnerVersion"))

    @builtins.property
    @jsii.member(jsii_name="components")
    def _components(self) -> typing.List["ImageBuilderComponent"]:
        '''
        :stability: deprecated
        '''
        return typing.cast(typing.List["ImageBuilderComponent"], jsii.get(self, "components"))

    @_components.setter
    def _components(self, value: typing.List["ImageBuilderComponent"]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f4c47d52e3f51709153fc49a53f833f06b1fd2ba44d3c86696b418a3bf88a972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value)


@jsii.implements(IRunnerProvider, _constructs_77d1e7e8.IConstruct)
class Ec2RunnerProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.Ec2RunnerProvider",
):
    '''(experimental) GitHub Actions runner provider using EC2 to execute jobs.

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        ami_builder: typing.Optional["IRunnerImageBuilder"] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        spot: typing.Optional[builtins.bool] = None,
        spot_max_price: typing.Optional[builtins.str] = None,
        storage_options: typing.Optional[typing.Union["StorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        subnet: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISubnet"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ami_builder: 
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build AMI containing GitHub Runner and all requirements. The image builder determines the OS and architecture of the runner. Default: Ec2RunnerProvider.imageBuilder()
        :param instance_type: (experimental) Instance type for launched runner instances. For GPU instance types (g4dn, g5, p3, etc.), we automatically use a GPU base image (AWS Deep Learning AMI) with NVIDIA drivers pre-installed. If you provide your own image builder, use ``baseAmi: BaseImage.fromGpuBase(os, architecture)`` or another image preloaded with NVIDIA drivers, or use an image component to install NVIDIA drivers. Default: m6i.large
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['ec2']
        :param security_group: (deprecated) Security Group to assign to launched runner instances. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to launched runner instances. Default: a new security group
        :param spot: (experimental) Use spot instances to save money. Spot instances are cheaper but not always available and can be stopped prematurely. Default: false
        :param spot_max_price: (experimental) Set a maximum price for spot instances. Default: no max price (you will pay current spot price)
        :param storage_options: (experimental) Options for runner instance storage volume.
        :param storage_size: (experimental) Size of volume available for launched runner instances. This modifies the boot volume size and doesn't add any additional volumes. Default: 30GB
        :param subnet: (deprecated) Subnet where the runner instances will be launched. Default: default subnet of account's default VPC
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param tags: (experimental) Additional tags to apply to launched runner instances and their volumes. These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``, and ``GitHubRunners:Runner``. You may only override ``Name``. Tags prefixed ``GitHubRunners:`` are reserved and rejected. Some of our reserved tags are used for house-keeping purposes. Default: no additional tags
        :param vpc: (experimental) VPC where runner instances will be launched. Default: default account VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fd3f279069067627058d9a5818aab030be5ffd71ce03962b4fd7cdd85eaeabf9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2RunnerProviderProps(
            ami_builder=ami_builder,
            group=group,
            image_builder=image_builder,
            instance_type=instance_type,
            labels=labels,
            security_group=security_group,
            security_groups=security_groups,
            spot=spot,
            spot_max_price=spot_max_price,
            storage_options=storage_options,
            storage_size=storage_size,
            subnet=subnet,
            subnet_selection=subnet_selection,
            tags=tags,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="imageBuilder")
    @builtins.classmethod
    def image_builder(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        aws_image_builder_options: typing.Optional[typing.Union["AwsImageBuilderRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        base_ami: typing.Optional[typing.Union[builtins.str, "BaseImage"]] = None,
        base_docker_image: typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]] = None,
        builder_type: typing.Optional["RunnerImageBuilderType"] = None,
        code_build_options: typing.Optional[typing.Union["CodeBuildRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        components: typing.Optional[typing.Sequence["RunnerImageComponent"]] = None,
        docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        wait_on_deploy: typing.Optional[builtins.bool] = None,
    ) -> "IConfigurableRunnerImageBuilder":
        '''(experimental) Create new image builder that builds EC2 specific runner images.

        You can customize the OS, architecture, VPC, subnet, security groups, etc. by passing in props.

        You can add components to the image builder by calling ``imageBuilder.addComponent()``.

        The default OS is Ubuntu running on x64 architecture.

        Included components:

        - ``RunnerImageComponent.requiredPackages()``
        - ``RunnerImageComponent.cloudWatchAgent()``
        - ``RunnerImageComponent.runnerUser()``
        - ``RunnerImageComponent.git()``
        - ``RunnerImageComponent.githubCli()``
        - ``RunnerImageComponent.awsCli()``
        - ``RunnerImageComponent.docker()``
        - ``RunnerImageComponent.githubRunner()``

        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param aws_image_builder_options: (experimental) Options specific to AWS Image Builder. Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.
        :param base_ami: (experimental) Base AMI from which runner AMIs will be built. This can be: - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead - A BaseImage instance created using static factory methods: - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.) - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter. Default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS
        :param base_docker_image: (experimental) Base image from which Docker runner images will be built. This can be: - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead - A BaseContainerImage instance created using static factory methods: - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild) - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}. Default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS
        :param builder_type: Default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI
        :param code_build_options: (experimental) Options specific to CodeBuild image builder. Only used when builderType is RunnerImageBuilderType.CODE_BUILD.
        :param components: (experimental) Components to install on the image. Default: none
        :param docker_setup_commands: (experimental) Additional commands to run on the build host before starting the Docker runner image build. Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images. Default: []
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX_UBUNTU
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_groups: (experimental) Security Groups to assign to this instance.
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param vpc: (experimental) VPC to build the image in. Default: no VPC
        :param wait_on_deploy: (experimental) Wait for image to finish building during deployment. It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build. Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used. Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c9910152a829b3b3a0a9e70ec31bd3ae8669b723ebb60627c6d08813b8122b23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunnerImageBuilderProps(
            architecture=architecture,
            aws_image_builder_options=aws_image_builder_options,
            base_ami=base_ami,
            base_docker_image=base_docker_image,
            builder_type=builder_type,
            code_build_options=code_build_options,
            components=components,
            docker_setup_commands=docker_setup_commands,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
            wait_on_deploy=wait_on_deploy,
        )

        return typing.cast("IConfigurableRunnerImageBuilder", jsii.sinvoke(cls, "imageBuilder", [scope, id, props]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2111adb25bc369b4d854ed9e79997c04f5525ef13fb037db8e53c1e7ff520609)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "_aws_cdk_aws_iam_ceddda9d.IPrincipal":
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.IPrincipal", jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> "_aws_cdk_aws_logs_ceddda9d.ILogGroup":
        '''(experimental) Log group where provided runners will save their logs.

        Note that this is not the job log, but the runner itself. It will not contain output from the GitHub Action but only metadata on its execution.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_logs_ceddda9d.ILogGroup", jsii.get(self, "logGroup"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.Ec2RunnerProviderProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "default_labels": "defaultLabels",
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "ami_builder": "amiBuilder",
        "group": "group",
        "image_builder": "imageBuilder",
        "instance_type": "instanceType",
        "labels": "labels",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "spot": "spot",
        "spot_max_price": "spotMaxPrice",
        "storage_options": "storageOptions",
        "storage_size": "storageSize",
        "subnet": "subnet",
        "subnet_selection": "subnetSelection",
        "tags": "tags",
        "vpc": "vpc",
    },
)
class Ec2RunnerProviderProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        ami_builder: typing.Optional["IRunnerImageBuilder"] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        spot: typing.Optional[builtins.bool] = None,
        spot_max_price: typing.Optional[builtins.str] = None,
        storage_options: typing.Optional[typing.Union["StorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        subnet: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISubnet"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''(experimental) Properties for {@link Ec2RunnerProvider} construct.

        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 
        :param ami_builder: 
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build AMI containing GitHub Runner and all requirements. The image builder determines the OS and architecture of the runner. Default: Ec2RunnerProvider.imageBuilder()
        :param instance_type: (experimental) Instance type for launched runner instances. For GPU instance types (g4dn, g5, p3, etc.), we automatically use a GPU base image (AWS Deep Learning AMI) with NVIDIA drivers pre-installed. If you provide your own image builder, use ``baseAmi: BaseImage.fromGpuBase(os, architecture)`` or another image preloaded with NVIDIA drivers, or use an image component to install NVIDIA drivers. Default: m6i.large
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['ec2']
        :param security_group: (deprecated) Security Group to assign to launched runner instances. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to launched runner instances. Default: a new security group
        :param spot: (experimental) Use spot instances to save money. Spot instances are cheaper but not always available and can be stopped prematurely. Default: false
        :param spot_max_price: (experimental) Set a maximum price for spot instances. Default: no max price (you will pay current spot price)
        :param storage_options: (experimental) Options for runner instance storage volume.
        :param storage_size: (experimental) Size of volume available for launched runner instances. This modifies the boot volume size and doesn't add any additional volumes. Default: 30GB
        :param subnet: (deprecated) Subnet where the runner instances will be launched. Default: default subnet of account's default VPC
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param tags: (experimental) Additional tags to apply to launched runner instances and their volumes. These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``, and ``GitHubRunners:Runner``. You may only override ``Name``. Tags prefixed ``GitHubRunners:`` are reserved and rejected. Some of our reserved tags are used for house-keeping purposes. Default: no additional tags
        :param vpc: (experimental) VPC where runner instances will be launched. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(storage_options, dict):
            storage_options = StorageOptions(**storage_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b650c4bf7f2a31b514d6f1f9e0c1b4b2cdae8b20b6f209f5b5fc74ef418fc2a3)
            check_type(argname="argument default_labels", value=default_labels, expected_type=type_hints["default_labels"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument ami_builder", value=ami_builder, expected_type=type_hints["ami_builder"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument image_builder", value=image_builder, expected_type=type_hints["image_builder"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument spot_max_price", value=spot_max_price, expected_type=type_hints["spot_max_price"])
            check_type(argname="argument storage_options", value=storage_options, expected_type=type_hints["storage_options"])
            check_type(argname="argument storage_size", value=storage_size, expected_type=type_hints["storage_size"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_labels is not None:
            self._values["default_labels"] = default_labels
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if ami_builder is not None:
            self._values["ami_builder"] = ami_builder
        if group is not None:
            self._values["group"] = group
        if image_builder is not None:
            self._values["image_builder"] = image_builder
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if labels is not None:
            self._values["labels"] = labels
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if spot_max_price is not None:
            self._values["spot_max_price"] = spot_max_price
        if storage_options is not None:
            self._values["storage_options"] = storage_options
        if storage_size is not None:
            self._values["storage_size"] = storage_size
        if subnet is not None:
            self._values["subnet"] = subnet
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if tags is not None:
            self._values["tags"] = tags
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def default_labels(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add default labels based on OS and architecture of the runner.

        This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def retry_options(self) -> typing.Optional["ProviderRetryOptions"]:
        '''
        :deprecated: use {@link retryOptions } on {@link GitHubRunners } instead

        :stability: deprecated
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional["ProviderRetryOptions"], result)

    @builtins.property
    def ami_builder(self) -> typing.Optional["IRunnerImageBuilder"]:
        '''
        :deprecated: use imageBuilder

        :stability: deprecated
        '''
        result = self._values.get("ami_builder")
        return typing.cast(typing.Optional["IRunnerImageBuilder"], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub Actions runner group name.

        If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It
        requires a paid GitHub account and organization level runner registration.

        The group must exist or the runner will not start.

        Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_builder(self) -> typing.Optional["IRunnerImageBuilder"]:
        '''(experimental) Runner image builder used to build AMI containing GitHub Runner and all requirements.

        The image builder determines the OS and architecture of the runner.

        :default: Ec2RunnerProvider.imageBuilder()

        :stability: experimental
        '''
        result = self._values.get("image_builder")
        return typing.cast(typing.Optional["IRunnerImageBuilder"], result)

    @builtins.property
    def instance_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"]:
        '''(experimental) Instance type for launched runner instances.

        For GPU instance types (g4dn, g5, p3, etc.), we automatically use a GPU base image (AWS Deep Learning AMI)
        with NVIDIA drivers pre-installed. If you provide your own image builder, use
        ``baseAmi: BaseImage.fromGpuBase(os, architecture)`` or another image preloaded with NVIDIA drivers, or use
        an image component to install NVIDIA drivers.

        :default: m6i.large

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['ec2']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(deprecated) Security Group to assign to launched runner instances.

        :default: a new security group

        :deprecated: use {@link securityGroups }

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security groups to assign to launched runner instances.

        :default: a new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use spot instances to save money.

        Spot instances are cheaper but not always available and can be stopped prematurely.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def spot_max_price(self) -> typing.Optional[builtins.str]:
        '''(experimental) Set a maximum price for spot instances.

        :default: no max price (you will pay current spot price)

        :stability: experimental
        '''
        result = self._values.get("spot_max_price")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_options(self) -> typing.Optional["StorageOptions"]:
        '''(experimental) Options for runner instance storage volume.

        :stability: experimental
        '''
        result = self._values.get("storage_options")
        return typing.cast(typing.Optional["StorageOptions"], result)

    @builtins.property
    def storage_size(self) -> typing.Optional["_aws_cdk_ceddda9d.Size"]:
        '''(experimental) Size of volume available for launched runner instances.

        This modifies the boot volume size and doesn't add any additional volumes.

        :default: 30GB

        :stability: experimental
        '''
        result = self._values.get("storage_size")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Size"], result)

    @builtins.property
    def subnet(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISubnet"]:
        '''(deprecated) Subnet where the runner instances will be launched.

        :default: default subnet of account's default VPC

        :deprecated: use {@link vpc } and {@link subnetSelection }

        :stability: deprecated
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISubnet"], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Where to place the network interfaces within the VPC.

        Only the first matched subnet will be used.

        :default: default VPC subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional tags to apply to launched runner instances and their volumes.

        These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``, and
        ``GitHubRunners:Runner``. You may only override ``Name``. Tags prefixed ``GitHubRunners:`` are reserved and rejected. Some of our reserved tags are
        used for house-keeping purposes.

        :default: no additional tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC where runner instances will be launched.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2RunnerProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRunnerProvider)
class EcsRunnerProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.EcsRunnerProvider",
):
    '''(experimental) GitHub Actions runner provider using ECS on EC2 to execute jobs.

    ECS can be useful when you want more control of the infrastructure running the GitHub Actions Docker containers. You can control the autoscaling
    group to scale down to zero during the night and scale up during work hours. This way you can still save money, but have to wait less for
    infrastructure to spin up.

    Jobs share instances, and by default run in privileged containers on Linux that can take over the instance. All jobs that can run on the same
    cluster should be equally trusted. See https://github.com/CloudSnorkel/cdk-github-runners#job-isolation

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        capacity_provider: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.AsgCapacityProvider"] = None,
        cluster: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"] = None,
        cpu: typing.Optional[jsii.Number] = None,
        docker_in_docker: typing.Optional[builtins.bool] = None,
        gpu: typing.Optional[jsii.Number] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_instances: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence["_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint"]] = None,
        placement_strategies: typing.Optional[typing.Sequence["_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy"]] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        spot: typing.Optional[builtins.bool] = None,
        spot_max_price: typing.Optional[builtins.str] = None,
        storage_options: typing.Optional[typing.Union["StorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assign_public_ip: (deprecated) Assign public IP to the runner task. Default: - ignored
        :param capacity_provider: (experimental) Existing capacity provider to use. Make sure the AMI used by the capacity provider is compatible with ECS. Runner containers use bridge networking and share the instance with other jobs. Its launch template must require IMDSv2 and set the metadata hop limit to 1 (``requireImdsv2: true`` and ``httpPutResponseHopLimit: 1``), or jobs can take the instance role. A warning is added when we can't confirm both. Default: new capacity provider
        :param cluster: (experimental) Existing ECS cluster to use. Jobs from all providers using the same cluster can share instances. Only share a cluster between providers whose jobs are equally trusted. Default: a new cluster
        :param cpu: (experimental) The number of cpu units used by the task. 1024 units is 1 vCPU. Fractions of a vCPU are supported. Default: 1024
        :param docker_in_docker: (experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required privileged mode for the runner container. A job running in a privileged container can take over the instance, access other jobs running on it, and affect jobs that run on it later. All jobs that can run on the same cluster should be equally trusted. Disable this if your jobs don't need Docker. Disabling Docker-in-Docker can also speed up runner provisioning as the runner doesn't have to wait for Docker to boot. Default: true
        :param gpu: (experimental) Number of GPUs to request for the runner task. When set, the task will be scheduled on GPU-capable instances. Requires a GPU-capable instance type (e.g., g4dn.xlarge for 1 GPU, g4dn.12xlarge for 4 GPUs) and GPU AMI. When creating a new cluster, instanceType defaults to g4dn.xlarge and the ECS Optimized GPU AMI is used. You must ensure that the task's container image includes the CUDA runtime. Provide a CUDA-enabled base image via ``baseDockerImage``, use an image builder that starts from a GPU-capable image (such as nvidia/cuda), or add an image component that installs the CUDA runtime into the image. Default: undefined (no GPU)
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder determines the OS and architecture of the runner. Default: EcsRunnerProvider.imageBuilder()
        :param instance_type: (experimental) Instance type of ECS cluster instances. Only used when creating a new cluster. Default: m6i.large or m6g.large
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['ecs']
        :param max_instances: (experimental) The maximum number of instances to run in the cluster. Only used when creating a new cluster. Default: 5
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory used by the task. Default: 3500, unless ``memoryReservationMiB`` is used and then it's undefined
        :param memory_reservation_mib: (experimental) The soft limit (in MiB) of memory to reserve for the container. Default: undefined
        :param min_instances: (experimental) The minimum number of instances to run in the cluster. Only used when creating a new cluster. Default: 0
        :param placement_constraints: (experimental) ECS placement constraints to influence task placement. Example: [ecs.PlacementConstraint.memberOf('ecs-placement')] Default: undefined (no placement constraints)
        :param placement_strategies: (experimental) ECS placement strategies to influence task placement. Example: [ecs.PlacementStrategy.packedByCpu()] Default: undefined (no placement strategies)
        :param security_groups: (experimental) Security groups to assign to the task. Default: a new security group
        :param spot: (experimental) Use spot capacity. Default: false (true if spotMaxPrice is specified)
        :param spot_max_price: (experimental) Maximum price for spot instances.
        :param storage_options: (experimental) Options for runner instance storage volume.
        :param storage_size: (experimental) Size of volume available for launched cluster instances. This modifies the boot volume size and doesn't add any additional volumes. Each instance can be used by multiple runners, so make sure there is enough space for all of them. Default: default size for AMI (usually 30GB for Linux and 50GB for Windows)
        :param subnet_selection: (experimental) Subnets to run the runners in. Default: ECS default
        :param tags: (experimental) Additional tags to apply to launched runner tasks. These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``. You may not override tags with the ``GitHubRunners:`` prefix. Default: no additional tags
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c520325dd0289bf8c6670ecdce77df4b229a0a2681957e61665818d2fe7383a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsRunnerProviderProps(
            assign_public_ip=assign_public_ip,
            capacity_provider=capacity_provider,
            cluster=cluster,
            cpu=cpu,
            docker_in_docker=docker_in_docker,
            gpu=gpu,
            group=group,
            image_builder=image_builder,
            instance_type=instance_type,
            labels=labels,
            max_instances=max_instances,
            memory_limit_mib=memory_limit_mib,
            memory_reservation_mib=memory_reservation_mib,
            min_instances=min_instances,
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
            security_groups=security_groups,
            spot=spot,
            spot_max_price=spot_max_price,
            storage_options=storage_options,
            storage_size=storage_size,
            subnet_selection=subnet_selection,
            tags=tags,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="imageBuilder")
    @builtins.classmethod
    def image_builder(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        aws_image_builder_options: typing.Optional[typing.Union["AwsImageBuilderRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        base_ami: typing.Optional[typing.Union[builtins.str, "BaseImage"]] = None,
        base_docker_image: typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]] = None,
        builder_type: typing.Optional["RunnerImageBuilderType"] = None,
        code_build_options: typing.Optional[typing.Union["CodeBuildRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        components: typing.Optional[typing.Sequence["RunnerImageComponent"]] = None,
        docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        wait_on_deploy: typing.Optional[builtins.bool] = None,
    ) -> "IConfigurableRunnerImageBuilder":
        '''(experimental) Create new image builder that builds ECS specific runner images.

        You can customize the OS, architecture, VPC, subnet, security groups, etc. by passing in props.

        You can add components to the image builder by calling ``imageBuilder.addComponent()``.

        The default OS is Ubuntu running on x64 architecture.

        Included components:

        - ``RunnerImageComponent.requiredPackages()``
        - ``RunnerImageComponent.runnerUser()``
        - ``RunnerImageComponent.git()``
        - ``RunnerImageComponent.githubCli()``
        - ``RunnerImageComponent.awsCli()``
        - ``RunnerImageComponent.docker()``
        - ``RunnerImageComponent.githubRunner()``

        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param aws_image_builder_options: (experimental) Options specific to AWS Image Builder. Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.
        :param base_ami: (experimental) Base AMI from which runner AMIs will be built. This can be: - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead - A BaseImage instance created using static factory methods: - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.) - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter. Default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS
        :param base_docker_image: (experimental) Base image from which Docker runner images will be built. This can be: - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead - A BaseContainerImage instance created using static factory methods: - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild) - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}. Default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS
        :param builder_type: Default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI
        :param code_build_options: (experimental) Options specific to CodeBuild image builder. Only used when builderType is RunnerImageBuilderType.CODE_BUILD.
        :param components: (experimental) Components to install on the image. Default: none
        :param docker_setup_commands: (experimental) Additional commands to run on the build host before starting the Docker runner image build. Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images. Default: []
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX_UBUNTU
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_groups: (experimental) Security Groups to assign to this instance.
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param vpc: (experimental) VPC to build the image in. Default: no VPC
        :param wait_on_deploy: (experimental) Wait for image to finish building during deployment. It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build. Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used. Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7b459d87ca6935e6c04ff03be02ed821eef81dbc792be822f356697f6c0f0b82)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunnerImageBuilderProps(
            architecture=architecture,
            aws_image_builder_options=aws_image_builder_options,
            base_ami=base_ami,
            base_docker_image=base_docker_image,
            builder_type=builder_type,
            code_build_options=code_build_options,
            components=components,
            docker_setup_commands=docker_setup_commands,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
            wait_on_deploy=wait_on_deploy,
        )

        return typing.cast("IConfigurableRunnerImageBuilder", jsii.sinvoke(cls, "imageBuilder", [scope, id, props]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f11d9c08955d770e27a043bd6b78d344029c8cbc3a22fca4138c21afe6b8ca4a)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @builtins.property
    @jsii.member(jsii_name="capacityProvider")
    def capacity_provider(self) -> "_aws_cdk_aws_ecs_ceddda9d.AsgCapacityProvider":
        '''(experimental) Capacity provider used to scale the cluster.

        Use capacityProvider.autoScalingGroup to access the auto scaling group. This can help set up custom scaling policies.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ecs_ceddda9d.AsgCapacityProvider", jsii.get(self, "capacityProvider"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "_aws_cdk_aws_iam_ceddda9d.IPrincipal":
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.IPrincipal", jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> "_aws_cdk_aws_logs_ceddda9d.ILogGroup":
        '''(experimental) Log group where provided runners will save their logs.

        Note that this is not the job log, but the runner itself. It will not contain output from the GitHub Action but only metadata on its execution.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_logs_ceddda9d.ILogGroup", jsii.get(self, "logGroup"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.EcsRunnerProviderProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "default_labels": "defaultLabels",
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "assign_public_ip": "assignPublicIp",
        "capacity_provider": "capacityProvider",
        "cluster": "cluster",
        "cpu": "cpu",
        "docker_in_docker": "dockerInDocker",
        "gpu": "gpu",
        "group": "group",
        "image_builder": "imageBuilder",
        "instance_type": "instanceType",
        "labels": "labels",
        "max_instances": "maxInstances",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
        "min_instances": "minInstances",
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
        "security_groups": "securityGroups",
        "spot": "spot",
        "spot_max_price": "spotMaxPrice",
        "storage_options": "storageOptions",
        "storage_size": "storageSize",
        "subnet_selection": "subnetSelection",
        "tags": "tags",
        "vpc": "vpc",
    },
)
class EcsRunnerProviderProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        capacity_provider: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.AsgCapacityProvider"] = None,
        cluster: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"] = None,
        cpu: typing.Optional[jsii.Number] = None,
        docker_in_docker: typing.Optional[builtins.bool] = None,
        gpu: typing.Optional[jsii.Number] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_instances: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence["_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint"]] = None,
        placement_strategies: typing.Optional[typing.Sequence["_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy"]] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        spot: typing.Optional[builtins.bool] = None,
        spot_max_price: typing.Optional[builtins.str] = None,
        storage_options: typing.Optional[typing.Union["StorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''(experimental) Properties for EcsRunnerProvider.

        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 
        :param assign_public_ip: (deprecated) Assign public IP to the runner task. Default: - ignored
        :param capacity_provider: (experimental) Existing capacity provider to use. Make sure the AMI used by the capacity provider is compatible with ECS. Runner containers use bridge networking and share the instance with other jobs. Its launch template must require IMDSv2 and set the metadata hop limit to 1 (``requireImdsv2: true`` and ``httpPutResponseHopLimit: 1``), or jobs can take the instance role. A warning is added when we can't confirm both. Default: new capacity provider
        :param cluster: (experimental) Existing ECS cluster to use. Jobs from all providers using the same cluster can share instances. Only share a cluster between providers whose jobs are equally trusted. Default: a new cluster
        :param cpu: (experimental) The number of cpu units used by the task. 1024 units is 1 vCPU. Fractions of a vCPU are supported. Default: 1024
        :param docker_in_docker: (experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required privileged mode for the runner container. A job running in a privileged container can take over the instance, access other jobs running on it, and affect jobs that run on it later. All jobs that can run on the same cluster should be equally trusted. Disable this if your jobs don't need Docker. Disabling Docker-in-Docker can also speed up runner provisioning as the runner doesn't have to wait for Docker to boot. Default: true
        :param gpu: (experimental) Number of GPUs to request for the runner task. When set, the task will be scheduled on GPU-capable instances. Requires a GPU-capable instance type (e.g., g4dn.xlarge for 1 GPU, g4dn.12xlarge for 4 GPUs) and GPU AMI. When creating a new cluster, instanceType defaults to g4dn.xlarge and the ECS Optimized GPU AMI is used. You must ensure that the task's container image includes the CUDA runtime. Provide a CUDA-enabled base image via ``baseDockerImage``, use an image builder that starts from a GPU-capable image (such as nvidia/cuda), or add an image component that installs the CUDA runtime into the image. Default: undefined (no GPU)
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder determines the OS and architecture of the runner. Default: EcsRunnerProvider.imageBuilder()
        :param instance_type: (experimental) Instance type of ECS cluster instances. Only used when creating a new cluster. Default: m6i.large or m6g.large
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['ecs']
        :param max_instances: (experimental) The maximum number of instances to run in the cluster. Only used when creating a new cluster. Default: 5
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory used by the task. Default: 3500, unless ``memoryReservationMiB`` is used and then it's undefined
        :param memory_reservation_mib: (experimental) The soft limit (in MiB) of memory to reserve for the container. Default: undefined
        :param min_instances: (experimental) The minimum number of instances to run in the cluster. Only used when creating a new cluster. Default: 0
        :param placement_constraints: (experimental) ECS placement constraints to influence task placement. Example: [ecs.PlacementConstraint.memberOf('ecs-placement')] Default: undefined (no placement constraints)
        :param placement_strategies: (experimental) ECS placement strategies to influence task placement. Example: [ecs.PlacementStrategy.packedByCpu()] Default: undefined (no placement strategies)
        :param security_groups: (experimental) Security groups to assign to the task. Default: a new security group
        :param spot: (experimental) Use spot capacity. Default: false (true if spotMaxPrice is specified)
        :param spot_max_price: (experimental) Maximum price for spot instances.
        :param storage_options: (experimental) Options for runner instance storage volume.
        :param storage_size: (experimental) Size of volume available for launched cluster instances. This modifies the boot volume size and doesn't add any additional volumes. Each instance can be used by multiple runners, so make sure there is enough space for all of them. Default: default size for AMI (usually 30GB for Linux and 50GB for Windows)
        :param subnet_selection: (experimental) Subnets to run the runners in. Default: ECS default
        :param tags: (experimental) Additional tags to apply to launched runner tasks. These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``. You may not override tags with the ``GitHubRunners:`` prefix. Default: no additional tags
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(storage_options, dict):
            storage_options = StorageOptions(**storage_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__73c1978e12dcea1bd69ce0927a80bd887d7f7d1b6573831942495e9d5966b483)
            check_type(argname="argument default_labels", value=default_labels, expected_type=type_hints["default_labels"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument capacity_provider", value=capacity_provider, expected_type=type_hints["capacity_provider"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument docker_in_docker", value=docker_in_docker, expected_type=type_hints["docker_in_docker"])
            check_type(argname="argument gpu", value=gpu, expected_type=type_hints["gpu"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument image_builder", value=image_builder, expected_type=type_hints["image_builder"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_instances", value=max_instances, expected_type=type_hints["max_instances"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
            check_type(argname="argument min_instances", value=min_instances, expected_type=type_hints["min_instances"])
            check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
            check_type(argname="argument placement_strategies", value=placement_strategies, expected_type=type_hints["placement_strategies"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument spot_max_price", value=spot_max_price, expected_type=type_hints["spot_max_price"])
            check_type(argname="argument storage_options", value=storage_options, expected_type=type_hints["storage_options"])
            check_type(argname="argument storage_size", value=storage_size, expected_type=type_hints["storage_size"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_labels is not None:
            self._values["default_labels"] = default_labels
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if capacity_provider is not None:
            self._values["capacity_provider"] = capacity_provider
        if cluster is not None:
            self._values["cluster"] = cluster
        if cpu is not None:
            self._values["cpu"] = cpu
        if docker_in_docker is not None:
            self._values["docker_in_docker"] = docker_in_docker
        if gpu is not None:
            self._values["gpu"] = gpu
        if group is not None:
            self._values["group"] = group
        if image_builder is not None:
            self._values["image_builder"] = image_builder
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if labels is not None:
            self._values["labels"] = labels
        if max_instances is not None:
            self._values["max_instances"] = max_instances
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib
        if min_instances is not None:
            self._values["min_instances"] = min_instances
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if spot_max_price is not None:
            self._values["spot_max_price"] = spot_max_price
        if storage_options is not None:
            self._values["storage_options"] = storage_options
        if storage_size is not None:
            self._values["storage_size"] = storage_size
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if tags is not None:
            self._values["tags"] = tags
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def default_labels(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add default labels based on OS and architecture of the runner.

        This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def retry_options(self) -> typing.Optional["ProviderRetryOptions"]:
        '''
        :deprecated: use {@link retryOptions } on {@link GitHubRunners } instead

        :stability: deprecated
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional["ProviderRetryOptions"], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Assign public IP to the runner task.

        :default: - ignored

        :deprecated:

        ECS runner tasks use bridge networking, so they share the host instance's network interface and
        cannot get a public IP of their own. This property is ignored. Give the cluster instances internet access
        instead (a public subnet or a NAT gateway), and open an issue if you need ``awsvpc`` networking for ECS.

        :stability: deprecated
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def capacity_provider(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ecs_ceddda9d.AsgCapacityProvider"]:
        '''(experimental) Existing capacity provider to use.

        Make sure the AMI used by the capacity provider is compatible with ECS.

        Runner containers use bridge networking and share the instance with other jobs. Its launch template must require IMDSv2 and set the
        metadata hop limit to 1 (``requireImdsv2: true`` and ``httpPutResponseHopLimit: 1``), or jobs can take the instance role. A warning is
        added when we can't confirm both.

        :default: new capacity provider

        :stability: experimental
        '''
        result = self._values.get("capacity_provider")
        return typing.cast(typing.Optional["_aws_cdk_aws_ecs_ceddda9d.AsgCapacityProvider"], result)

    @builtins.property
    def cluster(self) -> typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"]:
        '''(experimental) Existing ECS cluster to use.

        Jobs from all providers using the same cluster can share instances. Only share a cluster between providers whose jobs are equally trusted.

        :default: a new cluster

        :see: https://github.com/CloudSnorkel/cdk-github-runners#job-isolation
        :stability: experimental
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of cpu units used by the task.

        1024 units is 1 vCPU. Fractions of a vCPU are supported.

        :default: 1024

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_in_docker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required privileged mode for the runner container.

        A job running in a privileged container can take over the instance, access other jobs running on it, and affect jobs that run on it
        later. All jobs that can run on the same cluster should be equally trusted. Disable this if your jobs don't need Docker.

        Disabling Docker-in-Docker can also speed up runner provisioning as the runner doesn't have to wait for Docker to boot.

        :default: true

        :see: https://github.com/CloudSnorkel/cdk-github-runners#job-isolation
        :stability: experimental
        '''
        result = self._values.get("docker_in_docker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def gpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of GPUs to request for the runner task. When set, the task will be scheduled on GPU-capable instances.

        Requires a GPU-capable instance type (e.g., g4dn.xlarge for 1 GPU, g4dn.12xlarge for 4 GPUs) and GPU AMI.
        When creating a new cluster, instanceType defaults to g4dn.xlarge and the ECS Optimized GPU AMI is used.

        You must ensure that the task's container image includes the CUDA runtime. Provide a CUDA-enabled base image
        via ``baseDockerImage``, use an image builder that starts from a GPU-capable image (such as nvidia/cuda), or add
        an image component that installs the CUDA runtime into the image.

        :default: undefined (no GPU)

        :stability: experimental
        '''
        result = self._values.get("gpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub Actions runner group name.

        If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It
        requires a paid GitHub account and organization level runner registration.

        The group must exist or the runner will not start.

        Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_builder(self) -> typing.Optional["IRunnerImageBuilder"]:
        '''(experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements.

        The image builder determines the OS and architecture of the runner.

        :default: EcsRunnerProvider.imageBuilder()

        :stability: experimental
        '''
        result = self._values.get("image_builder")
        return typing.cast(typing.Optional["IRunnerImageBuilder"], result)

    @builtins.property
    def instance_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"]:
        '''(experimental) Instance type of ECS cluster instances.

        Only used when creating a new cluster.

        :default: m6i.large or m6g.large

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['ecs']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_instances(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of instances to run in the cluster.

        Only used when creating a new cluster.

        :default: 5

        :stability: experimental
        '''
        result = self._values.get("max_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount (in MiB) of memory used by the task.

        :default: 3500, unless ``memoryReservationMiB`` is used and then it's undefined

        :stability: experimental
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit (in MiB) of memory to reserve for the container.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instances(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum number of instances to run in the cluster.

        Only used when creating a new cluster.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("min_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint"]]:
        '''(experimental) ECS placement constraints to influence task placement.

        Example: [ecs.PlacementConstraint.memberOf('ecs-placement')]

        :default: undefined (no placement constraints)

        :stability: experimental
        '''
        result = self._values.get("placement_constraints")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint"]], result)

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy"]]:
        '''(experimental) ECS placement strategies to influence task placement.

        Example: [ecs.PlacementStrategy.packedByCpu()]

        :default: undefined (no placement strategies)

        :stability: experimental
        '''
        result = self._values.get("placement_strategies")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy"]], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security groups to assign to the task.

        :default: a new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use spot capacity.

        :default: false (true if spotMaxPrice is specified)

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def spot_max_price(self) -> typing.Optional[builtins.str]:
        '''(experimental) Maximum price for spot instances.

        :stability: experimental
        '''
        result = self._values.get("spot_max_price")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_options(self) -> typing.Optional["StorageOptions"]:
        '''(experimental) Options for runner instance storage volume.

        :stability: experimental
        '''
        result = self._values.get("storage_options")
        return typing.cast(typing.Optional["StorageOptions"], result)

    @builtins.property
    def storage_size(self) -> typing.Optional["_aws_cdk_ceddda9d.Size"]:
        '''(experimental) Size of volume available for launched cluster instances.

        This modifies the boot volume size and doesn't add any additional volumes.

        Each instance can be used by multiple runners, so make sure there is enough space for all of them.

        :default: default size for AMI (usually 30GB for Linux and 50GB for Windows)

        :stability: experimental
        '''
        result = self._values.get("storage_size")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Size"], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Subnets to run the runners in.

        :default: ECS default

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional tags to apply to launched runner tasks.

        These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``.
        You may not override tags with the ``GitHubRunners:`` prefix.

        :default: no additional tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC to launch the runners in.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsRunnerProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRunnerProvider)
class FargateRunnerProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.FargateRunnerProvider",
):
    '''(experimental) GitHub Actions runner provider using Fargate to execute jobs.

    Creates a task definition with a single container that gets started for each job.

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cluster: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"] = None,
        cpu: typing.Optional[jsii.Number] = None,
        ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        spot: typing.Optional[builtins.bool] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assign_public_ip: (experimental) Assign public IP to the runner task. Make sure the task will have access to GitHub. A public IP might be required unless you have NAT gateway. Default: true
        :param cluster: (experimental) Existing Fargate cluster to use. Default: a new cluster
        :param cpu: (experimental) The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param ephemeral_storage_gib: (experimental) The amount (in GiB) of ephemeral storage to be allocated to the task. The maximum supported value is 200 GiB. NOTE: This parameter is only supported for tasks hosted on AWS Fargate using platform version 1.4.0 or later. Default: 20
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder determines the OS and architecture of the runner. Default: FargateRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['fargate']
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param security_group: (deprecated) Security group to assign to the task. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to the task. Default: a new security group
        :param spot: (experimental) Use Fargate spot capacity provider to save money. - Runners may fail to start due to missing capacity. - Runners might be stopped prematurely with spot pricing. Default: false
        :param subnet_selection: (experimental) Subnets to run the runners in. Default: Fargate default
        :param tags: (experimental) Additional tags to apply to launched runner tasks. These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``. You may not override tags with the ``GitHubRunners:`` prefix. Default: no additional tags
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f7098876c10584a4cc58e16d23fd86ffe1fc50f2b55ca60549136d05135c4dab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FargateRunnerProviderProps(
            assign_public_ip=assign_public_ip,
            cluster=cluster,
            cpu=cpu,
            ephemeral_storage_gib=ephemeral_storage_gib,
            group=group,
            image_builder=image_builder,
            label=label,
            labels=labels,
            memory_limit_mib=memory_limit_mib,
            security_group=security_group,
            security_groups=security_groups,
            spot=spot,
            subnet_selection=subnet_selection,
            tags=tags,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="imageBuilder")
    @builtins.classmethod
    def image_builder(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        aws_image_builder_options: typing.Optional[typing.Union["AwsImageBuilderRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        base_ami: typing.Optional[typing.Union[builtins.str, "BaseImage"]] = None,
        base_docker_image: typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]] = None,
        builder_type: typing.Optional["RunnerImageBuilderType"] = None,
        code_build_options: typing.Optional[typing.Union["CodeBuildRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        components: typing.Optional[typing.Sequence["RunnerImageComponent"]] = None,
        docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        wait_on_deploy: typing.Optional[builtins.bool] = None,
    ) -> "IConfigurableRunnerImageBuilder":
        '''(experimental) Create new image builder that builds Fargate specific runner images.

        You can customize the OS, architecture, VPC, subnet, security groups, etc. by passing in props.

        You can add components to the image builder by calling ``imageBuilder.addComponent()``.

        The default OS is Ubuntu running on x64 architecture.

        Included components:

        - ``RunnerImageComponent.requiredPackages()``
        - ``RunnerImageComponent.runnerUser()``
        - ``RunnerImageComponent.git()``
        - ``RunnerImageComponent.githubCli()``
        - ``RunnerImageComponent.awsCli()``
        - ``RunnerImageComponent.githubRunner()``

        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param aws_image_builder_options: (experimental) Options specific to AWS Image Builder. Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.
        :param base_ami: (experimental) Base AMI from which runner AMIs will be built. This can be: - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead - A BaseImage instance created using static factory methods: - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.) - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter. Default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS
        :param base_docker_image: (experimental) Base image from which Docker runner images will be built. This can be: - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead - A BaseContainerImage instance created using static factory methods: - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild) - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}. Default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS
        :param builder_type: Default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI
        :param code_build_options: (experimental) Options specific to CodeBuild image builder. Only used when builderType is RunnerImageBuilderType.CODE_BUILD.
        :param components: (experimental) Components to install on the image. Default: none
        :param docker_setup_commands: (experimental) Additional commands to run on the build host before starting the Docker runner image build. Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images. Default: []
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX_UBUNTU
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_groups: (experimental) Security Groups to assign to this instance.
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param vpc: (experimental) VPC to build the image in. Default: no VPC
        :param wait_on_deploy: (experimental) Wait for image to finish building during deployment. It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build. Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used. Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9fd4f7f17e5e5c5b64ec7abfe1183d153e9472f7a1e9312e6d4b55f3f3bbe98b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunnerImageBuilderProps(
            architecture=architecture,
            aws_image_builder_options=aws_image_builder_options,
            base_ami=base_ami,
            base_docker_image=base_docker_image,
            builder_type=builder_type,
            code_build_options=code_build_options,
            components=components,
            docker_setup_commands=docker_setup_commands,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
            wait_on_deploy=wait_on_deploy,
        )

        return typing.cast("IConfigurableRunnerImageBuilder", jsii.sinvoke(cls, "imageBuilder", [scope, id, props]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2e32c5e47f8e7d2c7dac3264a53f7df7f1715b3436f8aa77b47ab0c9724e9ab6)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_ARM64_DOCKERFILE_PATH")
    @builtins.classmethod
    def LINUX_ARM64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(deprecated) Path to Dockerfile for Linux ARM64 with all the requirement for Fargate runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be an Ubuntu compatible image.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.

        :deprecated: Use ``imageBuilder()`` instead.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_ARM64_DOCKERFILE_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_X64_DOCKERFILE_PATH")
    @builtins.classmethod
    def LINUX_X64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(deprecated) Path to Dockerfile for Linux x64 with all the requirement for Fargate runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be an Ubuntu compatible image.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.

        :deprecated: Use ``imageBuilder()`` instead.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_X64_DOCKERFILE_PATH"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> builtins.bool:
        '''(deprecated) Whether runner task will have a public IP.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast(builtins.bool, jsii.get(self, "assignPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "_aws_cdk_aws_ecs_ceddda9d.Cluster":
        '''(experimental) Cluster hosting the task hosting the runner.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ecs_ceddda9d.Cluster", jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> "_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition":
        '''(deprecated) Container definition hosting the runner.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast("_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition", jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "_aws_cdk_aws_iam_ceddda9d.IPrincipal":
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.IPrincipal", jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> "RunnerImage":
        '''(deprecated) Docker image loaded with GitHub Actions Runner and its prerequisites.

        The image is built by an image builder and is specific to Fargate tasks.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast("RunnerImage", jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> "_aws_cdk_aws_logs_ceddda9d.ILogGroup":
        '''(experimental) Log group where provided runners will save their logs.

        Note that this is not the job log, but the runner itself. It will not contain output from the GitHub Action but only metadata on its execution.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_logs_ceddda9d.ILogGroup", jsii.get(self, "logGroup"))

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> builtins.bool:
        '''(deprecated) Use spot pricing for Fargate tasks.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast(builtins.bool, jsii.get(self, "spot"))

    @builtins.property
    @jsii.member(jsii_name="task")
    def task(self) -> "_aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition":
        '''(deprecated) Fargate task hosting the runner.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast("_aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition", jsii.get(self, "task"))

    @builtins.property
    @jsii.member(jsii_name="subnetSelection")
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(deprecated) Subnets used for hosting the runner task.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], jsii.get(self, "subnetSelection"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(deprecated) VPC used for hosting the runner task.

        :deprecated: This field is internal and should not be accessed directly.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.FargateRunnerProviderProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "default_labels": "defaultLabels",
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "assign_public_ip": "assignPublicIp",
        "cluster": "cluster",
        "cpu": "cpu",
        "ephemeral_storage_gib": "ephemeralStorageGiB",
        "group": "group",
        "image_builder": "imageBuilder",
        "label": "label",
        "labels": "labels",
        "memory_limit_mib": "memoryLimitMiB",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "spot": "spot",
        "subnet_selection": "subnetSelection",
        "tags": "tags",
        "vpc": "vpc",
    },
)
class FargateRunnerProviderProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cluster: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"] = None,
        cpu: typing.Optional[jsii.Number] = None,
        ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        spot: typing.Optional[builtins.bool] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''(experimental) Properties for FargateRunnerProvider.

        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 
        :param assign_public_ip: (experimental) Assign public IP to the runner task. Make sure the task will have access to GitHub. A public IP might be required unless you have NAT gateway. Default: true
        :param cluster: (experimental) Existing Fargate cluster to use. Default: a new cluster
        :param cpu: (experimental) The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param ephemeral_storage_gib: (experimental) The amount (in GiB) of ephemeral storage to be allocated to the task. The maximum supported value is 200 GiB. NOTE: This parameter is only supported for tasks hosted on AWS Fargate using platform version 1.4.0 or later. Default: 20
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder determines the OS and architecture of the runner. Default: FargateRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['fargate']
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param security_group: (deprecated) Security group to assign to the task. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to the task. Default: a new security group
        :param spot: (experimental) Use Fargate spot capacity provider to save money. - Runners may fail to start due to missing capacity. - Runners might be stopped prematurely with spot pricing. Default: false
        :param subnet_selection: (experimental) Subnets to run the runners in. Default: Fargate default
        :param tags: (experimental) Additional tags to apply to launched runner tasks. These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``. You may not override tags with the ``GitHubRunners:`` prefix. Default: no additional tags
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__26cdeb87df1adf5c49e0f9c1c061c7138af674da9af221212e1505fc1193583d)
            check_type(argname="argument default_labels", value=default_labels, expected_type=type_hints["default_labels"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument ephemeral_storage_gib", value=ephemeral_storage_gib, expected_type=type_hints["ephemeral_storage_gib"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument image_builder", value=image_builder, expected_type=type_hints["image_builder"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_labels is not None:
            self._values["default_labels"] = default_labels
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if cluster is not None:
            self._values["cluster"] = cluster
        if cpu is not None:
            self._values["cpu"] = cpu
        if ephemeral_storage_gib is not None:
            self._values["ephemeral_storage_gib"] = ephemeral_storage_gib
        if group is not None:
            self._values["group"] = group
        if image_builder is not None:
            self._values["image_builder"] = image_builder
        if label is not None:
            self._values["label"] = label
        if labels is not None:
            self._values["labels"] = labels
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if tags is not None:
            self._values["tags"] = tags
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def default_labels(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add default labels based on OS and architecture of the runner.

        This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def retry_options(self) -> typing.Optional["ProviderRetryOptions"]:
        '''
        :deprecated: use {@link retryOptions } on {@link GitHubRunners } instead

        :stability: deprecated
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional["ProviderRetryOptions"], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Assign public IP to the runner task.

        Make sure the task will have access to GitHub. A public IP might be required unless you have NAT gateway.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cluster(self) -> typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"]:
        '''(experimental) Existing Fargate cluster to use.

        :default: a new cluster

        :stability: experimental
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of cpu units used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values,
        which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)

        512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)

        1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)

        2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)

        4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

        :default: 1024

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ephemeral_storage_gib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount (in GiB) of ephemeral storage to be allocated to the task.

        The maximum supported value is 200 GiB.

        NOTE: This parameter is only supported for tasks hosted on AWS Fargate using platform version 1.4.0 or later.

        :default: 20

        :stability: experimental
        '''
        result = self._values.get("ephemeral_storage_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub Actions runner group name.

        If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It
        requires a paid GitHub account and organization level runner registration.

        The group must exist or the runner will not start.

        Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_builder(self) -> typing.Optional["IRunnerImageBuilder"]:
        '''(experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements.

        The image builder determines the OS and architecture of the runner.

        :default: FargateRunnerProvider.imageBuilder()

        :stability: experimental
        '''
        result = self._values.get("image_builder")
        return typing.cast(typing.Optional["IRunnerImageBuilder"], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(deprecated) GitHub Actions label used for this provider.

        :default: undefined

        :deprecated: use {@link labels } instead

        :stability: deprecated
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['fargate']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount (in MiB) of memory used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        :default: 2048

        :stability: experimental
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(deprecated) Security group to assign to the task.

        :default: a new security group

        :deprecated: use {@link securityGroups }

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security groups to assign to the task.

        :default: a new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use Fargate spot capacity provider to save money.

        - Runners may fail to start due to missing capacity.
        - Runners might be stopped prematurely with spot pricing.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Subnets to run the runners in.

        :default: Fargate default

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional tags to apply to launched runner tasks.

        These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``.
        You may not override tags with the ``GitHubRunners:`` prefix.

        :default: no additional tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC to launch the runners in.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateRunnerProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="@cloudsnorkel/cdk-github-runners.IConfigurableRunnerImageBuilder"
)
class IConfigurableRunnerImageBuilder(
    IRunnerImageBuilder,
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _aws_cdk_aws_iam_ceddda9d.IGrantable,
    typing_extensions.Protocol,
):
    '''(experimental) Interface for constructs that build an image that can be used in {@link IRunnerProvider }.

    The image can be configured by adding or removing components. The image builder can be configured by adding grants or allowing connections.

    An image can be a Docker image or AMI.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addComponent")
    def add_component(self, component: "RunnerImageComponent") -> None:
        '''(experimental) Add a component to the image builder.

        The component will be added to the end of the list of components.

        :param component: component to add.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="removeComponent")
    def remove_component(self, component: "RunnerImageComponent") -> None:
        '''(experimental) Remove a component from the image builder.

        Removal is done by component name. Multiple components with the same name will all be removed.

        :param component: component to remove.

        :stability: experimental
        '''
        ...


class _IConfigurableRunnerImageBuilderProxy(
    jsii.proxy_for(IRunnerImageBuilder), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_iam_ceddda9d.IGrantable), # type: ignore[misc]
):
    '''(experimental) Interface for constructs that build an image that can be used in {@link IRunnerProvider }.

    The image can be configured by adding or removing components. The image builder can be configured by adding grants or allowing connections.

    An image can be a Docker image or AMI.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IConfigurableRunnerImageBuilder"

    @jsii.member(jsii_name="addComponent")
    def add_component(self, component: "RunnerImageComponent") -> None:
        '''(experimental) Add a component to the image builder.

        The component will be added to the end of the list of components.

        :param component: component to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dc4625ad41fc3631b6e9812ae4ab86d19fc28eb849f5a5bf3a3ed7c4ebbeb066)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "addComponent", [component]))

    @jsii.member(jsii_name="removeComponent")
    def remove_component(self, component: "RunnerImageComponent") -> None:
        '''(experimental) Remove a component from the image builder.

        Removal is done by component name. Multiple components with the same name will all be removed.

        :param component: component to remove.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3aa11e0e95269ba6ec5fded5dd768fb588157de9643a5fce8b09fc9b4e2a18c0)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "removeComponent", [component]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConfigurableRunnerImageBuilder).__jsii_proxy_class__ = lambda : _IConfigurableRunnerImageBuilderProxy


class LambdaRunner(
    LambdaRunnerProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.LambdaRunner",
):
    '''
    :deprecated: use {@link LambdaRunnerProvider }

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        ephemeral_storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ephemeral_storage_size: (experimental) The size of the function’s /tmp directory in MiB. Default: 10 GiB
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder must contain the {@link RunnerImageComponent.lambdaEntrypoint} component. The image builder determines the OS and architecture of the runner. Default: LambdaRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['lambda']
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 2048
        :param security_group: (deprecated) Security group to assign to this instance. Default: public lambda with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: public lambda with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.minutes(15)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__80e9b84ecba02bdef856d3ee3f48a5e0a5e58ad813554fd529c0abe3af88217d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaRunnerProviderProps(
            ephemeral_storage_size=ephemeral_storage_size,
            group=group,
            image_builder=image_builder,
            label=label,
            labels=labels,
            memory_size=memory_size,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.LambdaRunnerProviderProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "default_labels": "defaultLabels",
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "group": "group",
        "image_builder": "imageBuilder",
        "label": "label",
        "labels": "labels",
        "memory_size": "memorySize",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class LambdaRunnerProviderProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        ephemeral_storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
    ) -> None:
        '''
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 
        :param ephemeral_storage_size: (experimental) The size of the function’s /tmp directory in MiB. Default: 10 GiB
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder must contain the {@link RunnerImageComponent.lambdaEntrypoint} component. The image builder determines the OS and architecture of the runner. Default: LambdaRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['lambda']
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 2048
        :param security_group: (deprecated) Security group to assign to this instance. Default: public lambda with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: public lambda with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.minutes(15)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__45a4a92b817689da2d55675d278ad5c96699269cc41f3406b7fca6d7a7664861)
            check_type(argname="argument default_labels", value=default_labels, expected_type=type_hints["default_labels"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument image_builder", value=image_builder, expected_type=type_hints["image_builder"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_labels is not None:
            self._values["default_labels"] = default_labels
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if group is not None:
            self._values["group"] = group
        if image_builder is not None:
            self._values["image_builder"] = image_builder
        if label is not None:
            self._values["label"] = label
        if labels is not None:
            self._values["labels"] = labels
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def default_labels(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add default labels based on OS and architecture of the runner.

        This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("default_labels")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def retry_options(self) -> typing.Optional["ProviderRetryOptions"]:
        '''
        :deprecated: use {@link retryOptions } on {@link GitHubRunners } instead

        :stability: deprecated
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional["ProviderRetryOptions"], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional["_aws_cdk_ceddda9d.Size"]:
        '''(experimental) The size of the function’s /tmp directory in MiB.

        :default: 10 GiB

        :stability: experimental
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Size"], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub Actions runner group name.

        If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It
        requires a paid GitHub account and organization level runner registration.

        The group must exist or the runner will not start.

        Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_builder(self) -> typing.Optional["IRunnerImageBuilder"]:
        '''(experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements.

        The image builder must contain the {@link RunnerImageComponent.lambdaEntrypoint} component.

        The image builder determines the OS and architecture of the runner.

        :default: LambdaRunnerProvider.imageBuilder()

        :stability: experimental
        '''
        result = self._values.get("image_builder")
        return typing.cast(typing.Optional["IRunnerImageBuilder"], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(deprecated) GitHub Actions label used for this provider.

        :default: undefined

        :deprecated: use {@link labels } instead

        :stability: deprecated
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['lambda']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 2048

        :stability: experimental
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]:
        '''(deprecated) Security group to assign to this instance.

        :default: public lambda with no security group

        :deprecated: use {@link securityGroups }

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''(experimental) Security groups to assign to this instance.

        :default: public lambda with no security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.minutes(15)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''(experimental) VPC to launch the runners in.

        :default: no VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaRunnerProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IConfigurableRunnerImageBuilder)
class RunnerImageBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerImageBuilder",
):
    '''(experimental) GitHub Runner image builder. Builds a Docker image or AMI with GitHub Runner and other requirements installed.

    Images can be customized before passed into the provider by adding or removing components to be installed.

    Images are rebuilt every week by default to ensure that the latest security patches are applied.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        aws_image_builder_options: typing.Optional[typing.Union["AwsImageBuilderRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        base_ami: typing.Optional[typing.Union[builtins.str, "BaseImage"]] = None,
        base_docker_image: typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]] = None,
        builder_type: typing.Optional["RunnerImageBuilderType"] = None,
        code_build_options: typing.Optional[typing.Union["CodeBuildRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        components: typing.Optional[typing.Sequence["RunnerImageComponent"]] = None,
        docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        wait_on_deploy: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param aws_image_builder_options: (experimental) Options specific to AWS Image Builder. Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.
        :param base_ami: (experimental) Base AMI from which runner AMIs will be built. This can be: - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead - A BaseImage instance created using static factory methods: - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.) - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter. Default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS
        :param base_docker_image: (experimental) Base image from which Docker runner images will be built. This can be: - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead - A BaseContainerImage instance created using static factory methods: - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild) - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}. Default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS
        :param builder_type: Default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI
        :param code_build_options: (experimental) Options specific to CodeBuild image builder. Only used when builderType is RunnerImageBuilderType.CODE_BUILD.
        :param components: (experimental) Components to install on the image. Default: none
        :param docker_setup_commands: (experimental) Additional commands to run on the build host before starting the Docker runner image build. Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images. Default: []
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX_UBUNTU
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_groups: (experimental) Security Groups to assign to this instance.
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param vpc: (experimental) VPC to build the image in. Default: no VPC
        :param wait_on_deploy: (experimental) Wait for image to finish building during deployment. It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build. Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used. Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__963c9a4884bb9d7400672391dfb47486f969a1b8fe5616bba9cd493e8a71484b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunnerImageBuilderProps(
            architecture=architecture,
            aws_image_builder_options=aws_image_builder_options,
            base_ami=base_ami,
            base_docker_image=base_docker_image,
            builder_type=builder_type,
            code_build_options=code_build_options,
            components=components,
            docker_setup_commands=docker_setup_commands,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
            wait_on_deploy=wait_on_deploy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="new")
    @builtins.classmethod
    def new(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        architecture: typing.Optional["Architecture"] = None,
        aws_image_builder_options: typing.Optional[typing.Union["AwsImageBuilderRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        base_ami: typing.Optional[typing.Union[builtins.str, "BaseImage"]] = None,
        base_docker_image: typing.Optional[typing.Union[builtins.str, "BaseContainerImage"]] = None,
        builder_type: typing.Optional["RunnerImageBuilderType"] = None,
        code_build_options: typing.Optional[typing.Union["CodeBuildRunnerImageBuilderProps", typing.Dict[builtins.str, typing.Any]]] = None,
        components: typing.Optional[typing.Sequence["RunnerImageComponent"]] = None,
        docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        wait_on_deploy: typing.Optional[builtins.bool] = None,
    ) -> "IConfigurableRunnerImageBuilder":
        '''(experimental) Create a new image builder based on the provided properties.

        The implementation will differ based on the OS, architecture, and requested builder type.

        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param aws_image_builder_options: (experimental) Options specific to AWS Image Builder. Only used when builderType is RunnerImageBuilderType.AWS_IMAGE_BUILDER.
        :param base_ami: (experimental) Base AMI from which runner AMIs will be built. This can be: - A string (AMI ID, Image Builder ARN, SSM parameter reference, or Marketplace product ID) - deprecated, use BaseImage static factory methods instead - A BaseImage instance created using static factory methods: - ``BaseImage.fromAmiId('ami-12345')`` - Use an AMI ID - ``BaseImage.fromString('arn:aws:imagebuilder:...')`` - Use any string (ARN, AMI ID, etc.) - ``BaseImage.fromSsmParameter(parameter)`` - Use an SSM parameter object - ``BaseImage.fromSsmParameterName('/aws/service/ami/...')`` - Use an SSM parameter by name - ``BaseImage.fromMarketplaceProductId('product-id')`` - Use a Marketplace product ID - ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` - Use an AWS-provided Image Builder image For example ``BaseImage.fromImageBuilder(scope, 'ubuntu-server-22-lts-x86')`` would always use the latest version of Ubuntu 22.04 in each build. If you want a specific version, you can pass the version as the third parameter. Default: latest Ubuntu 22.04 AMI for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, Ubuntu 24.04 AMI for Os.LINUX_UBUNTU_2404, latest Amazon Linux 2 AMI for Os.LINUX_AMAZON_2, latest Windows Server 2022 AMI for Os.WINDOWS
        :param base_docker_image: (experimental) Base image from which Docker runner images will be built. This can be: - A string (ECR/ECR public image URI, DockerHub image, or Image Builder ARN) - deprecated, use BaseContainerImage static factory methods instead - A BaseContainerImage instance created using static factory methods: - ``BaseContainerImage.fromDockerHub('ubuntu', '22.04')`` - Use DockerHub - ``BaseContainerImage.fromEcr(repo, 'latest')`` - Use ECR (automatically grants permissions with CodeBuild) - ``BaseContainerImage.fromEcrPublic('lts', 'ubuntu', '22.04')`` - Use ECR Public - ``BaseContainerImage.fromString('public.ecr.aws/lts/ubuntu:22.04')`` - Use any string When using private images from a different account or not on ECR, you may need to include additional setup commands with {@link dockerSetupCommands}. Default: public.ecr.aws/lts/ubuntu:22.04 for Os.LINUX_UBUNTU and Os.LINUX_UBUNTU_2204, public.ecr.aws/lts/ubuntu:24.04 for Os.LINUX_UBUNTU_2404, public.ecr.aws/amazonlinux/amazonlinux:2 for Os.LINUX_AMAZON_2, mcr.microsoft.com/windows/servercore:ltsc2019-amd64 for Os.WINDOWS
        :param builder_type: Default: CodeBuild for Linux Docker image, AWS Image Builder for Windows Docker image and any AMI
        :param code_build_options: (experimental) Options specific to CodeBuild image builder. Only used when builderType is RunnerImageBuilderType.CODE_BUILD.
        :param components: (experimental) Components to install on the image. Default: none
        :param docker_setup_commands: (experimental) Additional commands to run on the build host before starting the Docker runner image build. Use this to execute commands such as ``docker login`` or ``aws ecr get-login-password`` to pull private base images. Default: []
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX_UBUNTU
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_groups: (experimental) Security Groups to assign to this instance.
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param vpc: (experimental) VPC to build the image in. Default: no VPC
        :param wait_on_deploy: (experimental) Wait for image to finish building during deployment. It's usually best to leave this enabled to ensure everything is ready once deployment is done. However, it can be disabled to speed up deployment in case where you have a lot of image components that can take a long time to build. Disabling this option means a finished deployment is not ready to be used. You will have to wait for the image to finish building before the system can be used. Disabling this option may also mean any changes to settings or components can take up to a week (default rebuild interval) to take effect. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c44d5704c54d7fdcf24ad39567c0e9f53f9837163bf8bf3b1b4e652e27c9ec75)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunnerImageBuilderProps(
            architecture=architecture,
            aws_image_builder_options=aws_image_builder_options,
            base_ami=base_ami,
            base_docker_image=base_docker_image,
            builder_type=builder_type,
            code_build_options=code_build_options,
            components=components,
            docker_setup_commands=docker_setup_commands,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
            wait_on_deploy=wait_on_deploy,
        )

        return typing.cast("IConfigurableRunnerImageBuilder", jsii.sinvoke(cls, "new", [scope, id, props]))

    @jsii.member(jsii_name="addComponent")
    def add_component(self, component: "RunnerImageComponent") -> None:
        '''(experimental) Add a component to the image builder.

        The component will be added to the end of the list of components.

        :param component: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9dec4d5fbab87fa223a0eb0a144ad5bd91f9cdd54d3337c971ce6435c76dc049)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "addComponent", [component]))

    @jsii.member(jsii_name="bindAmi")
    @abc.abstractmethod
    def bind_ami(self) -> "RunnerAmi":
        '''(experimental) Build and return an AMI with GitHub Runner installed in it.

        Anything that ends up with a launch template pointing to an AMI that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing AMI and nothing else.

        The AMI can be further updated over time manually or using a schedule as long as it is always written to the same launch template.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="bindDockerImage")
    @abc.abstractmethod
    def bind_docker_image(self) -> "RunnerImage":
        '''(experimental) Build and return a Docker image with GitHub Runner installed in it.

        Anything that ends up with an ECR repository containing a Docker image that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing image and nothing else.

        It's important that the specified image tag be available at the time the repository is available. Providers usually assume the image is ready and will fail if it's not.

        The image can be further updated over time manually or using a schedule as long as it is always written to the same tag.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="removeComponent")
    def remove_component(self, component: "RunnerImageComponent") -> None:
        '''(experimental) Remove a component from the image builder.

        Removal is done by component name. Multiple components with the same name will all be removed.

        :param component: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1c4318b2834e7865918b5308b85c0fd80f22d29a067d68d4ee8537a6c0c88b3b)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "removeComponent", [component]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    @abc.abstractmethod
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    @abc.abstractmethod
    def grant_principal(self) -> "_aws_cdk_aws_iam_ceddda9d.IPrincipal":
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="components")
    def _components(self) -> typing.List["RunnerImageComponent"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["RunnerImageComponent"], jsii.get(self, "components"))

    @_components.setter
    def _components(self, value: typing.List["RunnerImageComponent"]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__705c18a1eedaa490aebad511aac32a801519a57162e30be4673a8ab87ca434dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value)


class _RunnerImageBuilderProxy(RunnerImageBuilder):
    @jsii.member(jsii_name="bindAmi")
    def bind_ami(self) -> "RunnerAmi":
        '''(experimental) Build and return an AMI with GitHub Runner installed in it.

        Anything that ends up with a launch template pointing to an AMI that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing AMI and nothing else.

        The AMI can be further updated over time manually or using a schedule as long as it is always written to the same launch template.

        :stability: experimental
        '''
        return typing.cast("RunnerAmi", jsii.invoke(self, "bindAmi", []))

    @jsii.member(jsii_name="bindDockerImage")
    def bind_docker_image(self) -> "RunnerImage":
        '''(experimental) Build and return a Docker image with GitHub Runner installed in it.

        Anything that ends up with an ECR repository containing a Docker image that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing image and nothing else.

        It's important that the specified image tag be available at the time the repository is available. Providers usually assume the image is ready and will fail if it's not.

        The image can be further updated over time manually or using a schedule as long as it is always written to the same tag.

        :stability: experimental
        '''
        return typing.cast("RunnerImage", jsii.invoke(self, "bindDockerImage", []))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "_aws_cdk_aws_ec2_ceddda9d.Connections":
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.Connections", jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "_aws_cdk_aws_iam_ceddda9d.IPrincipal":
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.IPrincipal", jsii.get(self, "grantPrincipal"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, RunnerImageBuilder).__jsii_proxy_class__ = lambda : _RunnerImageBuilderProxy


class CodeBuildRunner(
    CodeBuildRunnerProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildRunner",
):
    '''
    :deprecated: use {@link CodeBuildRunnerProvider }

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        compute_type: typing.Optional["_aws_cdk_aws_codebuild_ceddda9d.ComputeType"] = None,
        docker_in_docker: typing.Optional[builtins.bool] = None,
        gpu: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. The compute type determines CPU, memory, and disk space: - SMALL: 2 vCPU, 3 GB RAM, 64 GB disk - MEDIUM: 4 vCPU, 7 GB RAM, 128 GB disk - LARGE: 8 vCPU, 15 GB RAM, 128 GB disk - X2_LARGE: 72 vCPU, 145 GB RAM, 256 GB disk (Linux) or 824 GB disk (Windows) Use a larger compute type when you need more disk space for building larger Docker images. For more details, see https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html#environment.types Default: {@link ComputeType#SMALL }
        :param docker_in_docker: (experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required CodeBuild privileged mode. Disabling this can speed up provisioning of CodeBuild runners. If you don't intend on running or building Docker images, disable this for faster start-up times. Default: true
        :param gpu: (experimental) Use GPU compute for builds. When enabled, the default compute type is BUILD_GENERAL1_SMALL (4 vCPU, 16 GB RAM, 1 NVIDIA A10G GPU). You can override the compute type using the ``computeType`` property (for example, to use BUILD_GENERAL1_LARGE for more resources), subject to the supported GPU compute types. When using GPU compute, ensure your runner image includes any required GPU libraries (for example, CUDA) either by using a base image that has them preinstalled (such as an appropriate nvidia/cuda image) or by adding image components that install them. The default image builder does not automatically switch to a CUDA-enabled base image when GPU is enabled. GPU compute is only available for Linux x64 images. Not supported on Windows or ARM. Default: false
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder must contain the {@link RunnerImageComponent.docker} component unless ``dockerInDocker`` is set to false. The image builder determines the OS and architecture of the runner. Default: CodeBuildRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['codebuild']
        :param security_group: (deprecated) Security group to assign to this instance. Default: public project with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: a new security group, if {@link vpc } is used
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1ab9454b0ecfcd12fc0ab07c0f0f4d7ce646a5a928f5e14092b0a6c42a4c3b79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeBuildRunnerProviderProps(
            compute_type=compute_type,
            docker_in_docker=docker_in_docker,
            gpu=gpu,
            group=group,
            image_builder=image_builder,
            label=label,
            labels=labels,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class Ec2Runner(
    Ec2RunnerProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.Ec2Runner",
):
    '''
    :deprecated: use {@link Ec2RunnerProvider }

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        ami_builder: typing.Optional["IRunnerImageBuilder"] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        spot: typing.Optional[builtins.bool] = None,
        spot_max_price: typing.Optional[builtins.str] = None,
        storage_options: typing.Optional[typing.Union["StorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        subnet: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISubnet"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ami_builder: 
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build AMI containing GitHub Runner and all requirements. The image builder determines the OS and architecture of the runner. Default: Ec2RunnerProvider.imageBuilder()
        :param instance_type: (experimental) Instance type for launched runner instances. For GPU instance types (g4dn, g5, p3, etc.), we automatically use a GPU base image (AWS Deep Learning AMI) with NVIDIA drivers pre-installed. If you provide your own image builder, use ``baseAmi: BaseImage.fromGpuBase(os, architecture)`` or another image preloaded with NVIDIA drivers, or use an image component to install NVIDIA drivers. Default: m6i.large
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['ec2']
        :param security_group: (deprecated) Security Group to assign to launched runner instances. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to launched runner instances. Default: a new security group
        :param spot: (experimental) Use spot instances to save money. Spot instances are cheaper but not always available and can be stopped prematurely. Default: false
        :param spot_max_price: (experimental) Set a maximum price for spot instances. Default: no max price (you will pay current spot price)
        :param storage_options: (experimental) Options for runner instance storage volume.
        :param storage_size: (experimental) Size of volume available for launched runner instances. This modifies the boot volume size and doesn't add any additional volumes. Default: 30GB
        :param subnet: (deprecated) Subnet where the runner instances will be launched. Default: default subnet of account's default VPC
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param tags: (experimental) Additional tags to apply to launched runner instances and their volumes. These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``, and ``GitHubRunners:Runner``. You may only override ``Name``. Tags prefixed ``GitHubRunners:`` are reserved and rejected. Some of our reserved tags are used for house-keeping purposes. Default: no additional tags
        :param vpc: (experimental) VPC where runner instances will be launched. Default: default account VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a0a6acc584ae2ad3aed3605810cea44858f1a0bc22f62f2df9005b318dba7968)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2RunnerProviderProps(
            ami_builder=ami_builder,
            group=group,
            image_builder=image_builder,
            instance_type=instance_type,
            labels=labels,
            security_group=security_group,
            security_groups=security_groups,
            spot=spot,
            spot_max_price=spot_max_price,
            storage_options=storage_options,
            storage_size=storage_size,
            subnet=subnet,
            subnet_selection=subnet_selection,
            tags=tags,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class FargateRunner(
    FargateRunnerProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.FargateRunner",
):
    '''
    :deprecated: use {@link FargateRunnerProvider }

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cluster: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.Cluster"] = None,
        cpu: typing.Optional[jsii.Number] = None,
        ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
        group: typing.Optional[builtins.str] = None,
        image_builder: typing.Optional["IRunnerImageBuilder"] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        spot: typing.Optional[builtins.bool] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        default_labels: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assign_public_ip: (experimental) Assign public IP to the runner task. Make sure the task will have access to GitHub. A public IP might be required unless you have NAT gateway. Default: true
        :param cluster: (experimental) Existing Fargate cluster to use. Default: a new cluster
        :param cpu: (experimental) The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param ephemeral_storage_gib: (experimental) The amount (in GiB) of ephemeral storage to be allocated to the task. The maximum supported value is 200 GiB. NOTE: This parameter is only supported for tasks hosted on AWS Fargate using platform version 1.4.0 or later. Default: 20
        :param group: (experimental) GitHub Actions runner group name. If specified, the runner will be registered with this group name. Setting a runner group can help managing access to self-hosted runners. It requires a paid GitHub account and organization level runner registration. The group must exist or the runner will not start. Users will still be able to trigger this runner with the correct labels. But the runner will only be able to run jobs from repos allowed to use the group. Default: undefined
        :param image_builder: (experimental) Runner image builder used to build Docker images containing GitHub Runner and all requirements. The image builder determines the OS and architecture of the runner. Default: FargateRunnerProvider.imageBuilder()
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['fargate']
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param security_group: (deprecated) Security group to assign to the task. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to the task. Default: a new security group
        :param spot: (experimental) Use Fargate spot capacity provider to save money. - Runners may fail to start due to missing capacity. - Runners might be stopped prematurely with spot pricing. Default: false
        :param subnet_selection: (experimental) Subnets to run the runners in. Default: Fargate default
        :param tags: (experimental) Additional tags to apply to launched runner tasks. These additional tags are set on top of ``Name``, ``GitHubRunners:Provider``, ``GitHubRunners:Repo``, and ``GitHubRunners:Labels``. You may not override tags with the ``GitHubRunners:`` prefix. Default: no additional tags
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC
        :param default_labels: (experimental) Add default labels based on OS and architecture of the runner. This will tell GitHub Runner to add default labels like ``self-hosted``, ``linux``, ``x64``, and ``arm64``. Default: true
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e507aa08f983fcd409ec9cf4ba5e0e6312ce72778cbbb2f9b5b016fde7ef3784)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FargateRunnerProviderProps(
            assign_public_ip=assign_public_ip,
            cluster=cluster,
            cpu=cpu,
            ephemeral_storage_gib=ephemeral_storage_gib,
            group=group,
            image_builder=image_builder,
            label=label,
            labels=labels,
            memory_limit_mib=memory_limit_mib,
            security_group=security_group,
            security_groups=security_groups,
            spot=spot,
            subnet_selection=subnet_selection,
            tags=tags,
            vpc=vpc,
            default_labels=default_labels,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "AlwaysOnWarmRunner",
    "AlwaysOnWarmRunnerProps",
    "AmiBuilder",
    "AmiBuilderProps",
    "ApiGatewayAccessProps",
    "Architecture",
    "AwsImageBuilderRunnerImageBuilderProps",
    "BaseContainerImage",
    "BaseImage",
    "CodeBuildImageBuilder",
    "CodeBuildImageBuilderProps",
    "CodeBuildRunner",
    "CodeBuildRunnerImageBuilderProps",
    "CodeBuildRunnerProvider",
    "CodeBuildRunnerProviderProps",
    "CompositeProvider",
    "ContainerImageBuilder",
    "ContainerImageBuilderProps",
    "Ec2Runner",
    "Ec2RunnerProvider",
    "Ec2RunnerProviderProps",
    "EcsRunnerProvider",
    "EcsRunnerProviderProps",
    "FargateRunner",
    "FargateRunnerProvider",
    "FargateRunnerProviderProps",
    "FastLaunchOptions",
    "GitHubRunners",
    "GitHubRunnersProps",
    "ICompositeProvider",
    "IConfigurableRunnerImageBuilder",
    "IRunnerAmiStatus",
    "IRunnerImageBuilder",
    "IRunnerImageStatus",
    "IRunnerProvider",
    "IRunnerProviderStatus",
    "ImageBuilderAsset",
    "ImageBuilderComponent",
    "ImageBuilderComponentProperties",
    "LambdaAccess",
    "LambdaRunner",
    "LambdaRunnerProvider",
    "LambdaRunnerProviderProps",
    "LinuxUbuntuComponents",
    "LogOptions",
    "Os",
    "ProviderRetryOptions",
    "ProviderSelectorInput",
    "ProviderSelectorResult",
    "RunnerAmi",
    "RunnerImage",
    "RunnerImageAsset",
    "RunnerImageBuilder",
    "RunnerImageBuilderProps",
    "RunnerImageBuilderType",
    "RunnerImageComponent",
    "RunnerImageComponentCustomProps",
    "RunnerProviderProps",
    "RunnerVersion",
    "ScheduledWarmRunner",
    "ScheduledWarmRunnerProps",
    "Secrets",
    "StaticRunnerImage",
    "StorageOptions",
    "WeightedRunnerProvider",
    "WindowsComponents",
]

publication.publish()

def _typecheckingstub__6190a21456122517ee8943805f4bb158e15774f590513fc686004df32e516d1e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    count: jsii.Number,
    owner: builtins.str,
    provider: typing.Union[IRunnerProvider, ICompositeProvider],
    runners: GitHubRunners,
    registration_level: typing.Optional[builtins.str] = None,
    repo: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5898a98cc3d83a12a9319ee2298fa83987d45a80e21cc1aa7c35f76c3bf7b94a(
    *,
    count: jsii.Number,
    owner: builtins.str,
    provider: typing.Union[IRunnerProvider, ICompositeProvider],
    runners: GitHubRunners,
    registration_level: typing.Optional[builtins.str] = None,
    repo: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1848f87828e47066d3d798fe57a60bb7bcf3be03f641b793ff686f68265bb5b(
    *,
    architecture: typing.Optional[Architecture] = None,
    install_docker: typing.Optional[builtins.bool] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0230281aea2f0096e32af8e4f02c3c351aada0957c217590514bfc5f6f656b0e(
    *,
    allowed_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    allowed_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    allowed_vpc_endpoints: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.IVpcEndpoint]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197fbc91031fbef228119c4ea4b7d54d7ee7ae2efdfedf7354f2313378ee5db9(
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c78353047f5b727c68147df5fbcc6c4d5381f43b731bacf43f3e3ec823bc835(
    arch: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cf6bb0c2118d6cb7d082b7e678fba3dae1f5b8812776005eef7b14eb285e06(
    arches: typing.Sequence[Architecture],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe17585d38b67015c3f03db2aefab095f171e0e0900c9a4564679bbc5a29fd07(
    *,
    ami_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    fast_launch_options: typing.Optional[typing.Union[FastLaunchOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ca7a21f04340348e57cd58a15361581ca48a96701cd63cf51deda7f8667556(
    image: builtins.str,
    ecr_repository: typing.Optional[_aws_cdk_aws_ecr_ceddda9d.IRepository] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620793aa1b875f75c7470562ba65c023ae388e946b5d0838efb942f1d7cf8b36(
    repository: builtins.str,
    tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f0cdd27fd11637348a57bb1963032374a83f6897e036810baf1225a25a5e22(
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cac37db8e7f02b74225b02cd0840bcae90a82f4cf6d4b57a31b759c7fef50e(
    registry_alias: builtins.str,
    repository_name: builtins.str,
    tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6665a984629ccf7e97837a416fca7b6eb45d677e2251c373e856609e48b13ddc(
    base_container_image_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b6e1f1beb455f020318f40620cdc5da6eb91ef685f4b19f3ee1b82244571b9(
    image: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce8e58d909a9b0733dd3a845ef1cbf1c6f1d57d6a28e030f5122f6a07ea226a(
    ami_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e40fcd49321d7aa1d4140157d8bd6ef6e3c6daab5371fccf4772418206bb924(
    os: Os,
    architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca0f086c8fe6ceed61893dace3f2a63221659b4f2dc8deac5e079c2af594c81(
    scope: _constructs_77d1e7e8.Construct,
    resource_name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d91f35f8cfaaa28eff924e8b02b89309fd30277e590963e62e2df9156c61c0(
    product_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc5733de6656116c12830996cd2873ef94eb2660f3f56e15095618f20dae9e1(
    parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe4dd96225df8b7acceff4f4de111f9de9838f83919100fb917661d9f67b53f(
    parameter_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc9be4cd1f85f2aa04be945d8d5ccfb305101c54ea34109a6bc600e8af9dd00(
    base_image_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3489f112da2cf966956bd19d9d323a5acba9732c6207773bb9b29c93cf407444(
    *,
    dockerfile_path: builtins.str,
    architecture: typing.Optional[Architecture] = None,
    build_image: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.IBuildImage] = None,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57eba0e804792fea32cbb8b094226d90afd105dd84432bb9e2d32380259a548f(
    *,
    build_image: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.IBuildImage] = None,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c19894684d852504fe0fe078d55632b0435f3c901fffef944cc34438533639(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    weighted_providers: typing.Sequence[typing.Union[WeightedRunnerProvider, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6d940901d7f617b4a15476433bf716e52ca4bd1c63e38d17294ec861fa0a12(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    providers: typing.Sequence[IRunnerProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b6832b84987dee7e16a1e7bde046b812c75e74a268cb3fbf2685d3fe25115c(
    *,
    architecture: typing.Optional[Architecture] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    parent_image: typing.Optional[builtins.str] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2952ae322a0fd40b480084b183be9e7179337af84efb30a496aa331a22fa562(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    max_parallel_launches: typing.Optional[jsii.Number] = None,
    target_resource_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a45de07d09ed9f4fd0b9051aeff4571ceda633f49c0b30a5058ad6d72fad18(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    extra_certificates: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    log_options: typing.Optional[typing.Union[LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[IRunnerProvider, ICompositeProvider]]] = None,
    provider_selector: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
    require_self_hosted_label: typing.Optional[builtins.bool] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    setup_access: typing.Optional[LambdaAccess] = None,
    status_access: typing.Optional[LambdaAccess] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_access: typing.Optional[LambdaAccess] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c824929ac2b172d81f1ca6d3f77b08aca419fe4769d0c13dc162a760e13372(
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d8d4287a56d393e1fe438a511f3c5c95bcb80987e93de575d61fc0507cb7f1(
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bc8ba54eaa33d65a8c2635c32c20406be53589ef1d25e161194a6bcfb3f669(
    scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db12e50ec9bf1582f493963c13640e2d81a3a4afae3df834ecce0bf88f4706c(
    *,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    extra_certificates: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    log_options: typing.Optional[typing.Union[LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[IRunnerProvider, ICompositeProvider]]] = None,
    provider_selector: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
    require_self_hosted_label: typing.Optional[builtins.bool] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    setup_access: typing.Optional[LambdaAccess] = None,
    status_access: typing.Optional[LambdaAccess] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_access: typing.Optional[LambdaAccess] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ca7e4fb20813ac7d2ccae32dbb1fda48790fac4d7cd07aa1afbdb9d8f5e665(
    *,
    asset: _aws_cdk_aws_s3_assets_ceddda9d.Asset,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363ebaab8a0bcbaea3d32a9c7e3cb241f08cf49d6eea02ba40eaaef9af89f266(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    commands: typing.Sequence[builtins.str],
    description: builtins.str,
    display_name: builtins.str,
    platform: builtins.str,
    assets: typing.Optional[typing.Sequence[typing.Union[ImageBuilderAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
    reboot: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a450535474a302df6d17ac0b627edd05f72f54c900f36380517d39fc0a3b15e4(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae848cd8ee55808c4c98a6e69173dc05ae5472e3b1443ee6fbc64e32bc9a25f(
    platform: builtins.str,
    commands: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86439e194b36e470271c572c251444f98c4b86a68fa7e63cf41ae1fa9628d4a(
    *,
    commands: typing.Sequence[builtins.str],
    description: builtins.str,
    display_name: builtins.str,
    platform: builtins.str,
    assets: typing.Optional[typing.Sequence[typing.Union[ImageBuilderAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
    reboot: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244c9d572ba45d54b74fe86f184cc91d1d6c9a27c6a0d3635e3b366738528b8d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637ac3a7237f114ea2a9842f95653a0d13444cd4da7a4dfe9330fdb98204e19b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2bbc7a18f99610673c6eb5e5f04fb45ba63301ff0fbe525246014617834e02(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    aws_image_builder_options: typing.Optional[typing.Union[AwsImageBuilderRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    base_ami: typing.Optional[typing.Union[builtins.str, BaseImage]] = None,
    base_docker_image: typing.Optional[typing.Union[builtins.str, BaseContainerImage]] = None,
    builder_type: typing.Optional[RunnerImageBuilderType] = None,
    code_build_options: typing.Optional[typing.Union[CodeBuildRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    components: typing.Optional[typing.Sequence[RunnerImageComponent]] = None,
    docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    wait_on_deploy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4dccc4a69e2dce26e0096d5540914cfc02fe99cbad00d4b539e0750dc84c6d(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9ab64a566b3cb12a56785cb68d60451eea856392ba6abd6e242f7e7607911a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65a5832ccfba2d220d98a2c68a108dfc3f78dbe85709f5f5c759dcc9ad578f9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b2501b6d5ebe8b59ce2ea43654c77b49b4f10be39415a6e90b19f2d8db235b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec8ad9a5de8cc35d2f35d52d25f6a1b7f104db23ae3e2e7135c937889eca5b8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50238c37c0bb4a9b1f6a596f61b2f74a34f0fee6eced39901007db76663f96d0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdcfc8bfb186dc1b0e83a960dadbae430b22e77b9f4c33b2b73d225fc182bff(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    runner_version: RunnerVersion,
    architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b9420557bcd008ca04d0eb1d14eb5a4747825ef4fadee115c226eb00b43841(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01575c6c37e4a36bb9456ff19c3af703d6c78462d7d7a4a668462fd9c3163582(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d87067ac294a2f323b063b74d5b20d774fc42a4e718e01d16209ad13483ebc2(
    *,
    include_execution_data: typing.Optional[builtins.bool] = None,
    level: typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19131179030c715697989d1d64b1121c3de55b2dc82fb900699b7c47875fcaa(
    os: Os,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c514548a5b083cb01132e52421a310d7518ba890b88c4cff63cbaa518d114a(
    oses: typing.Sequence[Os],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd088f490cad60ffd09b5c6222c769b3656e8a7694013c57b0029f2f6c986b51(
    *,
    backoff_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    max_attempts: typing.Optional[jsii.Number] = None,
    max_delay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32039399f56bfde071f3747ee0792c5419757ceddb8a3ca63dd026969e0172c7(
    *,
    payload: typing.Any,
    providers: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
    default_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_provider: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f59228823c79b7a6dea6bd4bbcade1672b332240071aa12b4fc7a780cd35d9(
    *,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    provider: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c612bd55218b02d6290415e414adca19a5e6961e7aa4dec3a838bc328b9885(
    *,
    architecture: Architecture,
    launch_template: _aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate,
    os: Os,
    runner_version: RunnerVersion,
    cache_key: typing.Optional[builtins.str] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74a83a8ebe05e179af2175f3c275f7e12d7c4f25c43d548f01e20cc2a011cf8(
    *,
    architecture: Architecture,
    image_repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    image_tag: builtins.str,
    os: Os,
    runner_version: RunnerVersion,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21bedad36e17a5840ddb719458c9e0eb15a89e493efa80af28f6031d1a27d62e(
    *,
    source: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab96b7f3871624e8430668114e7f5748ba5d253168db5b8f9a13955d0a82e43d(
    *,
    architecture: typing.Optional[Architecture] = None,
    aws_image_builder_options: typing.Optional[typing.Union[AwsImageBuilderRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    base_ami: typing.Optional[typing.Union[builtins.str, BaseImage]] = None,
    base_docker_image: typing.Optional[typing.Union[builtins.str, BaseContainerImage]] = None,
    builder_type: typing.Optional[RunnerImageBuilderType] = None,
    code_build_options: typing.Optional[typing.Union[CodeBuildRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    components: typing.Optional[typing.Sequence[RunnerImageComponent]] = None,
    docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    wait_on_deploy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f18c953246d0b1c39021f86a7331edf31cbf289f37746be885869974f0fca2(
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6162c551433cf1db5703258b3cb16cc320275cca3f8ad1f8e1a51f0dcb575003(
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e95caad3455adca1643b95064ddbc75b67f19721e366fd8038efe6b556251d4(
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604cc9b160ccf839230b5f673dff20a8c9722aa81c88ef3ccadcdfcec778ec1a(
    vars: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71019afd6f999efd03cc3106a7c28048b0a38c740207d3615ba7e0569bab5d3d(
    source: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669185ad44a15382c6a0a4208b26b61d74d2e4b36063f72333c2d4d82f830b1c(
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4981b41e48ec1c85e6e4bdbb74f25162e16cf49eb993af72a7e8cf9e0f36ba5c(
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bb77dff91c55638bfd8c57f50a16468b499b43fd08f7c2eb6b91015b0fb5ce(
    runner_version: RunnerVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083e94ebc2f48e7d52b90eb90d5dfc27d4d2b7378bead0205b6630aad7eb19b3(
    source_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f2d5267f3cde15dc5bd682063ee9b779f6c755c762b02b8c0e32138f774d4e(
    source_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68512864561c1bf5bd229a6f57c7022e0a3d3d27a6d1167bb9c47d7bc98136c1(
    _os: Os,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff728adc7084e50163879cf938d15b8d276df893b0a66f820410e736e6b8246(
    _os: Os,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df207340fa2acd15c1f7ba9d50447510dbe0aea58f11301ec935f4fbd00947f(
    _os: Os,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee6536536b6c0e4ddbbb0d090a8deb491f5ecb4e1271d4525e6ea2835a39ef2(
    _os: Os,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe5c2d2437d742085479f02259513b739e15d569c2f5b87bf0244bf4414dece(
    *,
    assets: typing.Optional[typing.Sequence[typing.Union[RunnerImageAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
    commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    docker_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa1323116edff475c54eafc82f7af57dd73527c022a54b6210c5a490a80a1d3(
    *,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20bea31f4405bffc4cb36e66dd5c0a065f92e483730a259e382a093aad9e848(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044a71dfcd711f28ea336af855aef4d2c3f4fc96fdfdebe5176e2c42f33a964e(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081bd4a2174b252695ac5a4c393b5cc34338749ce09a2f6e91d54fb759352a52(
    other: RunnerVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e418e3ab977851661c4fdef30ab50171823bf02eb71713b5464fa33b854ad6c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    count: jsii.Number,
    duration: _aws_cdk_ceddda9d.Duration,
    owner: builtins.str,
    provider: typing.Union[IRunnerProvider, ICompositeProvider],
    runners: GitHubRunners,
    schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
    registration_level: typing.Optional[builtins.str] = None,
    repo: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64664dba439d880d957abcf8db98fc425864e0505c455f86126a974fbf07c0de(
    *,
    count: jsii.Number,
    duration: _aws_cdk_ceddda9d.Duration,
    owner: builtins.str,
    provider: typing.Union[IRunnerProvider, ICompositeProvider],
    runners: GitHubRunners,
    schedule: _aws_cdk_aws_events_ceddda9d.Schedule,
    registration_level: typing.Optional[builtins.str] = None,
    repo: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58760067bc1fce42b3c98a9ce96a17f4638077eb209c6d67eb7f627614e953b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6aadaf28505152ad03a72118d87a28121a3699389220ce60ddab5a907b0cdce(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image: builtins.str,
    architecture: typing.Optional[Architecture] = None,
    os: typing.Optional[Os] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48d8ecb3f18c1471b45f7dfd8f15c51227e04697959138092d72a9150e724a8(
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    tag: typing.Optional[builtins.str] = None,
    architecture: typing.Optional[Architecture] = None,
    os: typing.Optional[Os] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3b766929d3a048d89c7dc502f77bbbfc7357735093ebc66695a13b92f9bf82(
    *,
    iops: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.EbsDeviceVolumeType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11df8e8d0b3b2cc48ff30c5ac99895a30df88812eafb3ababb862f36381ae3b(
    *,
    provider: IRunnerProvider,
    weight: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c68c27f668327e6aeb3b0e5b7e88235ae547046edeb1fa6a808b729a31b7bd2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d18e04aa4683610d276ffab3f0570d771274749e3013b977bcb8fa1e76f45e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0154389d6d3b175e2f67c0a3396f61d6bbb3095e54e09e25fe5e60e047b40b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fed2553bd6ff4aa9a60d780bfb72824212d74795a0e85c85c1d1253cc4db69(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900bdb4c3fd73b8c9f97280217bdcc95dbbeee03c9f7f15d53d398b09f7716fd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a39cf569b605cb085761e993915b9d261ed5d3b804d0b9f4c2cf1ea3606c06(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0edb989a5946c92ba1761a899ffffa9fea018497911c40c9c0dae502a637f40(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    runner_version: RunnerVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625361a368f8eabbfa2d2951b1d7aff4d2f57b6d8d5cdaa78c2db82b204cc254(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    install_docker: typing.Optional[builtins.bool] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9747ce69b89d4dbf55b31806bc58d53721577273c2cbfc7864620d8a463b9796(
    component: ImageBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74248b6087eb378ee00c6fedecd54fd91eef1eacead09cd38466e3085a87ab9f(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d9489ff52404cba57c43261d3ed74a1b9f4f798ae49c0058cd84430a429021(
    infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
    dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
    log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f1cb907bb1baffb27dbf2a76a4c4c810656d94df878155237526f4cef49cb6(
    managed_policies: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2c57a50959e16c9926951dc35e40bda4192b464bff123578e463523039b935(
    recipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce32f249fb7ba35579acf4098c5c404f576dcfa3eebf6d32b1ef120b5b109f1f(
    infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
    dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
    log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8124976feff345d9400fd0ffd91955fd1a5585bddbcf348d2fa89a8495bf54b7(
    component: ImageBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8088868062a70621aab7b900883cf52d9c930de8a458039564d69a7d0cc80f52(
    value: typing.List[ImageBuilderComponent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a03ba99d5c1cb98c8dcc6a1f21ec4e7ff6c73bbe85e6ed2102fe51075fd8f2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dockerfile_path: builtins.str,
    architecture: typing.Optional[Architecture] = None,
    build_image: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.IBuildImage] = None,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5977c467d0631ac1513843c39f63ce74892cd360d8ed6de11a85ee5d410b7566(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d392c7ee36222706a353bc6e75a56046571240436fc791fa66816e528d197d(
    source_path: builtins.str,
    dest_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee162d5d2373c52a16033f2b8f554c6228060793fcb0d2aa63121dc74eb82e1(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf227e615cf526a927f3b0a0695ce9ea199758f87a664a9cce5ec90fd388bfd(
    command: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8252ffd4dd18dc431c781dc95c9cb4cd57710a688e4e22640b839bb707d91bf1(
    command: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8a5cd687fe02e670471554b7ec420ad3b88d98e1f0157b5b890fd4c6f3f283(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb924a0cf987a9f87f4ad0ebd952c61ebd4e02d7d83501b9600f14157c110e9b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    docker_in_docker: typing.Optional[builtins.bool] = None,
    gpu: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b74a56ca854b011edea7d259b730771e5a994081db1aa0bdbea8b3e2b668120(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    aws_image_builder_options: typing.Optional[typing.Union[AwsImageBuilderRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    base_ami: typing.Optional[typing.Union[builtins.str, BaseImage]] = None,
    base_docker_image: typing.Optional[typing.Union[builtins.str, BaseContainerImage]] = None,
    builder_type: typing.Optional[RunnerImageBuilderType] = None,
    code_build_options: typing.Optional[typing.Union[CodeBuildRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    components: typing.Optional[typing.Sequence[RunnerImageComponent]] = None,
    docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    wait_on_deploy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149d854003aceddd7320ff6f28772f8f4f60386fcf64a37bc0b8e500c26f7b5b(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9377dcf4cd4dae74730635bdaf02246acb473843cea2856cf9a64295df964eb6(
    *,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    docker_in_docker: typing.Optional[builtins.bool] = None,
    gpu: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61ba73c795872c9aa5e24ac4480b00db813c358539591499a6767701e246ecc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    parent_image: typing.Optional[builtins.str] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d5aa0a2ebc88884861dcaec651d073dd4411ff3bb5497bc7dcffc8faca6a48(
    component: ImageBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224b352e0817976406c67254ec8d2bf9bac77c2647873ddcd2f95568571ee3c9(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8117d158d639350efd9e0c32a50eaf83954ebcc7a687759681ab20d2930337c1(
    infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
    dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
    log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cc0053b03b95f450f5e13113627e405c2bfea1a5b08cd36cd5647a79a4430f(
    managed_policies: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4281ad903ec2ef54b36fdccf3f500d5e4c37e5eee693fdfd781ec26563b31766(
    recipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e3a91f74cb641217038e41062fccd039108dc4ddbfe446bb99732081a4e4b0(
    infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
    dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
    log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d078b80933c0ce3a1dec052eeae9dc31f2640b3def938bf732dcd3276e6f8964(
    component: ImageBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c47d52e3f51709153fc49a53f833f06b1fd2ba44d3c86696b418a3bf88a972(
    value: typing.List[ImageBuilderComponent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3f279069067627058d9a5818aab030be5ffd71ce03962b4fd7cdd85eaeabf9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ami_builder: typing.Optional[IRunnerImageBuilder] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    spot_max_price: typing.Optional[builtins.str] = None,
    storage_options: typing.Optional[typing.Union[StorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9910152a829b3b3a0a9e70ec31bd3ae8669b723ebb60627c6d08813b8122b23(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    aws_image_builder_options: typing.Optional[typing.Union[AwsImageBuilderRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    base_ami: typing.Optional[typing.Union[builtins.str, BaseImage]] = None,
    base_docker_image: typing.Optional[typing.Union[builtins.str, BaseContainerImage]] = None,
    builder_type: typing.Optional[RunnerImageBuilderType] = None,
    code_build_options: typing.Optional[typing.Union[CodeBuildRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    components: typing.Optional[typing.Sequence[RunnerImageComponent]] = None,
    docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    wait_on_deploy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2111adb25bc369b4d854ed9e79997c04f5525ef13fb037db8e53c1e7ff520609(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b650c4bf7f2a31b514d6f1f9e0c1b4b2cdae8b20b6f209f5b5fc74ef418fc2a3(
    *,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ami_builder: typing.Optional[IRunnerImageBuilder] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    spot_max_price: typing.Optional[builtins.str] = None,
    storage_options: typing.Optional[typing.Union[StorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c520325dd0289bf8c6670ecdce77df4b229a0a2681957e61665818d2fe7383a4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    capacity_provider: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.AsgCapacityProvider] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
    cpu: typing.Optional[jsii.Number] = None,
    docker_in_docker: typing.Optional[builtins.bool] = None,
    gpu: typing.Optional[jsii.Number] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_instances: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    spot_max_price: typing.Optional[builtins.str] = None,
    storage_options: typing.Optional[typing.Union[StorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b459d87ca6935e6c04ff03be02ed821eef81dbc792be822f356697f6c0f0b82(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    aws_image_builder_options: typing.Optional[typing.Union[AwsImageBuilderRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    base_ami: typing.Optional[typing.Union[builtins.str, BaseImage]] = None,
    base_docker_image: typing.Optional[typing.Union[builtins.str, BaseContainerImage]] = None,
    builder_type: typing.Optional[RunnerImageBuilderType] = None,
    code_build_options: typing.Optional[typing.Union[CodeBuildRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    components: typing.Optional[typing.Sequence[RunnerImageComponent]] = None,
    docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    wait_on_deploy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11d9c08955d770e27a043bd6b78d344029c8cbc3a22fca4138c21afe6b8ca4a(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c1978e12dcea1bd69ce0927a80bd887d7f7d1b6573831942495e9d5966b483(
    *,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    capacity_provider: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.AsgCapacityProvider] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
    cpu: typing.Optional[jsii.Number] = None,
    docker_in_docker: typing.Optional[builtins.bool] = None,
    gpu: typing.Optional[jsii.Number] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_instances: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    spot_max_price: typing.Optional[builtins.str] = None,
    storage_options: typing.Optional[typing.Union[StorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7098876c10584a4cc58e16d23fd86ffe1fc50f2b55ca60549136d05135c4dab(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
    cpu: typing.Optional[jsii.Number] = None,
    ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd4f7f17e5e5c5b64ec7abfe1183d153e9472f7a1e9312e6d4b55f3f3bbe98b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    aws_image_builder_options: typing.Optional[typing.Union[AwsImageBuilderRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    base_ami: typing.Optional[typing.Union[builtins.str, BaseImage]] = None,
    base_docker_image: typing.Optional[typing.Union[builtins.str, BaseContainerImage]] = None,
    builder_type: typing.Optional[RunnerImageBuilderType] = None,
    code_build_options: typing.Optional[typing.Union[CodeBuildRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    components: typing.Optional[typing.Sequence[RunnerImageComponent]] = None,
    docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    wait_on_deploy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e32c5e47f8e7d2c7dac3264a53f7df7f1715b3436f8aa77b47ab0c9724e9ab6(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cdeb87df1adf5c49e0f9c1c061c7138af674da9af221212e1505fc1193583d(
    *,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
    cpu: typing.Optional[jsii.Number] = None,
    ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4625ad41fc3631b6e9812ae4ab86d19fc28eb849f5a5bf3a3ed7c4ebbeb066(
    component: RunnerImageComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa11e0e95269ba6ec5fded5dd768fb588157de9643a5fce8b09fc9b4e2a18c0(
    component: RunnerImageComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e9b84ecba02bdef856d3ee3f48a5e0a5e58ad813554fd529c0abe3af88217d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a4a92b817689da2d55675d278ad5c96699269cc41f3406b7fca6d7a7664861(
    *,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963c9a4884bb9d7400672391dfb47486f969a1b8fe5616bba9cd493e8a71484b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    aws_image_builder_options: typing.Optional[typing.Union[AwsImageBuilderRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    base_ami: typing.Optional[typing.Union[builtins.str, BaseImage]] = None,
    base_docker_image: typing.Optional[typing.Union[builtins.str, BaseContainerImage]] = None,
    builder_type: typing.Optional[RunnerImageBuilderType] = None,
    code_build_options: typing.Optional[typing.Union[CodeBuildRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    components: typing.Optional[typing.Sequence[RunnerImageComponent]] = None,
    docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    wait_on_deploy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44d5704c54d7fdcf24ad39567c0e9f53f9837163bf8bf3b1b4e652e27c9ec75(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    aws_image_builder_options: typing.Optional[typing.Union[AwsImageBuilderRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    base_ami: typing.Optional[typing.Union[builtins.str, BaseImage]] = None,
    base_docker_image: typing.Optional[typing.Union[builtins.str, BaseContainerImage]] = None,
    builder_type: typing.Optional[RunnerImageBuilderType] = None,
    code_build_options: typing.Optional[typing.Union[CodeBuildRunnerImageBuilderProps, typing.Dict[builtins.str, typing.Any]]] = None,
    components: typing.Optional[typing.Sequence[RunnerImageComponent]] = None,
    docker_setup_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    wait_on_deploy: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dec4d5fbab87fa223a0eb0a144ad5bd91f9cdd54d3337c971ce6435c76dc049(
    component: RunnerImageComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4318b2834e7865918b5308b85c0fd80f22d29a067d68d4ee8537a6c0c88b3b(
    component: RunnerImageComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705c18a1eedaa490aebad511aac32a801519a57162e30be4673a8ab87ca434dc(
    value: typing.List[RunnerImageComponent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab9454b0ecfcd12fc0ab07c0f0f4d7ce646a5a928f5e14092b0a6c42a4c3b79(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    docker_in_docker: typing.Optional[builtins.bool] = None,
    gpu: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a6acc584ae2ad3aed3605810cea44858f1a0bc22f62f2df9005b318dba7968(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ami_builder: typing.Optional[IRunnerImageBuilder] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    spot_max_price: typing.Optional[builtins.str] = None,
    storage_options: typing.Optional[typing.Union[StorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e507aa08f983fcd409ec9cf4ba5e0e6312ce72778cbbb2f9b5b016fde7ef3784(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
    cpu: typing.Optional[jsii.Number] = None,
    ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
    group: typing.Optional[builtins.str] = None,
    image_builder: typing.Optional[IRunnerImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    default_labels: typing.Optional[builtins.bool] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ICompositeProvider, IConfigurableRunnerImageBuilder, IRunnerAmiStatus, IRunnerImageBuilder, IRunnerImageStatus, IRunnerProvider, IRunnerProviderStatus]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
