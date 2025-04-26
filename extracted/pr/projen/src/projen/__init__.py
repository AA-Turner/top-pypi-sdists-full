r'''
<p align="center">
  <a href="https://projen.io">
    <img src="https://raw.githubusercontent.com/projen/projen/main/logo/projen.svg">
    <h3 align="center">projen</h3>
  </a>
</p><p align="center">
  Define and maintain complex project configuration through code.
</p><p align="center">
  <a href="https://projen.io/"><strong>Documentation</strong></a> ·
  <a href="https://github.com/projen/projen/releases"><strong>Changelog</strong></a> ·
  <a href="#project-types"><strong>Project types</strong></a> ·
  <a href="#community"><strong>Join the community</strong></a>
</p><p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg" alt="Apache 2.0 License"></a>
  <a href="https://gitpod.io/#https://github.com/projen/projen"><img src="https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod" alt="Gitpod ready-to-code"></a>
  <a href="https://github.com/projen/projen/actions/workflows/release.yml"><img src="https://github.com/projen/projen/actions/workflows/release.yml/badge.svg" alt="Release badge"></a>
  <a href="https://github.com/projen/projen/commits/main"><img src="https://img.shields.io/github/commit-activity/w/projen/projen" alt="Commit activity"></a>
</p><br/>

*projen* synthesizes project configuration files such as `package.json`,
`tsconfig.json`, `.gitignore`, GitHub Workflows, eslint, jest, etc. from a
well-typed definition written in JavaScript.

As opposed to existing templating/scaffolding tools, *projen* is not a one-off
generator. Synthesized files should never be manually edited (in fact, projen
enforces that). To modify your project setup, users interact with rich
strongly-typed class and execute `projen` to update their project configuration
files.

By defining a custom project type and using projen in multiple repositories, it's
possible to update configuration files and CI/CD workflows across dozens (or
hundreds!?) of projects.

Check out [this talk](https://youtu.be/SOWMPzXtTCw) about projen from its creator.

## Getting Started

*projen* doesn't need to be installed. You will be using [npx](https://docs.npmjs.com/cli/v7/commands/npx) to run *projen* which takes care of all required setup steps.

To create a new project, run the following command and follow the instructions:

```console
$ mkdir my-project
$ cd my-project
$ npx projen new PROJECT-TYPE
🤖 Synthesizing project...
...
```

### Project types

Currently supported project types (use `npx projen new` without a type for a
full list):

**Built-in:** (run `npx projen new <type>`)

<!-- <macro exec="node ./scripts/readme-projects.js"> -->

* [awscdk-app-java](https://projen.io/docs/api/awscdk#awscdkjavaapp-) - AWS CDK app in Java.
* [awscdk-app-py](https://projen.io/docs/api/awscdk#awscdkpythonapp-) - AWS CDK app in Python.
* [awscdk-app-ts](https://projen.io/docs/api/awscdk#awscdktypescriptapp-) - AWS CDK app in TypeScript.
* [awscdk-construct](https://projen.io/docs/api/awscdk#awscdkconstructlibrary-) - AWS CDK construct library project.
* [cdk8s-app-py](https://projen.io/docs/api/cdk8s#cdk8spythonapp-) - CDK8s app in Python.
* [cdk8s-app-ts](https://projen.io/docs/api/cdk8s#cdk8stypescriptapp-) - CDK8s app in TypeScript.
* [cdk8s-construct](https://projen.io/docs/api/cdk8s#constructlibrarycdk8s-) - CDK8s construct library project.
* [cdktf-construct](https://projen.io/docs/api/cdktf#constructlibrarycdktf-) - CDKTF construct library project.
* [java](https://projen.io/docs/api/java#javaproject-) - Java project.
* [jsii](https://projen.io/docs/api/cdk#jsiiproject-) - Multi-language jsii library project.
* [nextjs](https://projen.io/docs/api/web#nextjsproject-) - Next.js project using JavaScript.
* [nextjs-ts](https://projen.io/docs/api/web#nextjstypescriptproject-) - Next.js project using TypeScript.
* [node](https://projen.io/docs/api/javascript#nodeproject-) - Node.js project.
* [project](https://projen.io/docs/api/projen#project-) - Base project.
* [python](https://projen.io/docs/api/python#pythonproject-) - Python project.
* [react](https://projen.io/docs/api/web#reactproject-) - React project using JavaScript.
* [react-ts](https://projen.io/docs/api/web#reacttypescriptproject-) - React project using TypeScript.
* [typescript](https://projen.io/docs/api/typescript#typescriptproject-) - TypeScript project.
* [typescript-app](https://projen.io/docs/api/typescript#typescriptappproject-) - TypeScript app.

<!-- </macro> -->

**External:** (run `npx projen new --from <type>`)

* [projen-github-action-typescript](https://github.com/projen/projen-github-action-typescript/blob/main/API.md) - GitHub Action in TypeScript project.

> Use `npx projen new PROJECT-TYPE --help` to view a list of command line
> switches that allows you to specify most project options during bootstrapping.
> For example: `npx projen new jsii --author-name "Jerry Berry"`.

The `new` command will create a `.projenrc.js` file which looks like this for
`jsii` projects:

```js
const { JsiiProject } = require('projen');

const project = new JsiiProject({
  authorAddress: "elad.benisrael@gmail.com",
  authorName: "Elad Ben-Israel",
  name: "foobar",
  repository: "https://github.com/eladn/foobar.git",
});

project.synth();
```

This program instantiates the project type with minimal setup, and then calls
`synth()` to synthesize the project files. By default, the `new` command will
also execute this program, which will result in a fully working project.

Once your project is created, you can configure your project by editing
`.projenrc.js` and re-running `npx projen` to synthesize again.

> The files generated by *projen* are considered an "implementation detail" and
> *projen* protects them from being manually edited (most files are marked
> read-only, and an "anti tamper" check is configured in the CI build workflow
> to ensure that files are not updated during build).

For example, to setup PyPI publishing in `jsii` projects, you can use
[`publishToPypi option`](https://projen.io/publisher.html):

```js
const project = new JsiiProject({
  // ...
  publishToPypi: {
    distName: "mydist",
    module: "my_module",
  }
});
```

Run:

```shell
npx projen
```

And you'll notice that your `package.json` file now contains a `python` section in
its `jsii` config and the GitHub `release.yml` workflow includes a PyPI
publishing step.

We recommend to put this in your shell profile, so you can simply run `pj` every
time you update `.projenrc.js`:

```bash
alias pj='npx projen'
```

Most projects come with an assortment of **tasks** that handle various
development activities, from compiling to publishing. Tasks can be and composed
together, and can be run as local commands or turned into GitHub workflows. You
can list all tasks with `npx projen --help`:

```shell
$ npx projen --help
projen [command]

Commands:
  projen new [PROJECT-TYPE-NAME] [OPTIONS]  Creates a new projen project
  projen clobber                            hard resets to HEAD of origin and cleans the local repo
  projen compile                            Only compile
  projen test                               Run tests
  projen build                              Full release build (test+compile)
  projen upgrade                            upgrade dependencies (including projen)
...
```

The `build` task is the same task that's executed in your CI builds. It
typically compiles, lints, tests and packages your module for distribution.

### Shell Completions

If installed as a global package, `projen` includes rich shell tab-completion support. To enable this in your shell, run:

```shell
# Bash
projen completion >> ~/.bashrc

# ZSH
projen completion >> ~/.zshrc
```

## Features

Some examples of features built-in to project types:

* Fully synthesize `package.json`
* Standard npm scripts like `compile`, `build`, `test`, `package`
* eslint
* Jest
* jsii: compile, package, api compatibility checks, API.md
* Bump & release scripts with CHANGELOG generation based on conventional commits
* Automated PR builds
* Automated releases to npm, maven, NuGet and PyPI
* Automated dependency upgrades
* Mergify configuration
* LICENSE file generation
* gitignore + npmignore management
* Node "engines" support with coupling to CI build environment and @types/node
* Anti-tamper: CI builds will fail if a synthesized file is modified manually

## Documentation

For documentation including examples and a full API reference, visit [https://projen.io/](https://projen.io/).

## Ecosystem

*projen* takes a "batteries included" approach and aims to offer dozens of different project types out of
the box (we are just getting started). Think `projen new react`, `projen new angular`, `projen new java-maven`,
`projen new awscdk-typescript`, `projen new cdk8s-python` (nothing in projen is tied to javascript or npm!)...

Adding new project types is as simple as submitting a pull request to this repo and exporting a class that
extends `projen.Project` (or one of its derivatives). Projen automatically discovers project types so your
type will immediately be available in `projen new`.

### Projects in external modules

*projen* is bundled with many project types out of the box, but it can also work
with project types and components defined in external jsii modules (the reason
we need jsii is because projen uses the jsii metadata to discover project types
& options in projen new).

Say we have a module in npm called `projen-vuejs` which includes a single project
type for vue.js:

```bash
$ npx projen new --from projen-vuejs
```

If the referenced module includes multiple project types, the type is required.
Switches can also be used to specify initial values based on the project type
APIs. You can also use any package syntax supported by [yarn
add](https://classic.yarnpkg.com/en/docs/cli/add#toc-adding-dependencies) like
`projen-vuejs@1.2.3`, `file:/path/to/local/folder`,
`git@github.com/awesome/projen-vuejs#1.2.3`, etc.

```bash
$ npx projen new --from projen-vuejs@^2 vuejs-ts --description "my awesome vue project"
```

Under the hood, `projen new` will install the `projen-vuejs` module from npm
(version 2.0.0 and above), discover the project types in it and bootstrap the
`vuejs-ts` project type. It will assign the value `"my awesome vue project"` to
the `description` field. If you examine your `.projenrc.js` file, you'll see
that `projen-vuejs` is defined as a dev dependency:

```javascript
const { VueJsProject } = require('projen-vuejs');

const project = new VueJsProject({
  name: 'my-vuejs-sample',
  description: "my awesome vue project",
  // ...
  devDeps: [
    'projen-vuejs'
  ]
});

project.synth();
```

## Roadmap

See [Vision](./VISION.md).

## FAQ

### Do I have to write my configuration in JavaScript?

Not at all! JavaScript is the default, but it's also possible to write it in
Java, Python, TypeScript, or even JSON. This is made
possible by the [jsii](https://github.com/aws/jsii) library which allows us
to write APIs once and generate libraries in several languages. You can choose
a different language by passing the `--projenrc-ts`, `--projenrc-py`, `--projenrc-java`, or
`--projenrc-json` flags when running `projen new`.

Note: using a `.projenrc.json` file to specify configuration only allows
accessing a subset of the entire API - the options which are passed to the
constructor of each project type.

### How does projen work with my IDE?

projen has an unofficial [VS Code extension](https://marketplace.visualstudio.com/items?itemName=MarkMcCulloh.vscode-projen). Check it out!

## Community

The projen community can be found within the #projen channel in the [cdk.dev](https://cdk.dev/)
community Slack workspace.

### Virtual Meetup

* Thursday June 30, 2022
* 1-2pm America/New_York (EDT)
* [CFP](https://bit.ly/3NEc0UQ) a Google Form
* CFP Closes Saturday April 30, 2022
* Hosted on [Zoom](https://zoom.us/j/92399854777?pwd=OUZybHlobHNoZUs1VVordWhaRTVGdz09#success)

## Contributions

Contributions of all kinds are welcome! Check out our [contributor's
guide](./CONTRIBUTING.md) and our [code of conduct](./CODE_OF_CONDUCT.md).

For a quick start, check out a development environment:

```bash
$ git clone git@github.com:projen/projen
$ cd projen
$ yarn
$ yarn watch # compile in the background
```

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-193-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END --><!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section --><!-- prettier-ignore-start --><!-- markdownlint-disable --><table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Hunter-Thompson"><img src="https://avatars.githubusercontent.com/u/20844961?v=4?s=100" width="100px;" alt=" Aatman "/><br /><sub><b> Aatman </b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=Hunter-Thompson" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://accenture.github.io/"><img src="https://avatars.githubusercontent.com/u/43275295?v=4?s=100" width="100px;" alt="Abdullah Sahin"/><br /><sub><b>Abdullah Sahin</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=abdsahin" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://adam.dev/"><img src="https://avatars.githubusercontent.com/u/2363879?v=4?s=100" width="100px;" alt="Adam"/><br /><sub><b>Adam</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=adamdottv" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://adamelkhayyat.github.io/"><img src="https://avatars.githubusercontent.com/u/19326038?v=4?s=100" width="100px;" alt="Adam ElKhayyat"/><br /><sub><b>Adam ElKhayyat</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=adamelkhayyat" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/adamelmore"><img src="https://avatars2.githubusercontent.com/u/2363879?v=4?s=100" width="100px;" alt="Adam Elmore"/><br /><sub><b>Adam Elmore</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=adamelmore" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/agdimech"><img src="https://avatars.githubusercontent.com/u/51220968?v=4?s=100" width="100px;" alt="Adrian Dimech"/><br /><sub><b>Adrian Dimech</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=agdimech" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/adrianmace"><img src="https://avatars.githubusercontent.com/u/5071859?v=4?s=100" width="100px;" alt="Adrian Mace"/><br /><sub><b>Adrian Mace</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=adrianmace" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alejandrolorefice"><img src="https://avatars.githubusercontent.com/u/24880460?v=4?s=100" width="100px;" alt="Alejandro Lorefice"/><br /><sub><b>Alejandro Lorefice</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=alejandrolorefice" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alexforsyth"><img src="https://avatars.githubusercontent.com/u/8712303?v=4?s=100" width="100px;" alt="Alexander Forsyth"/><br /><sub><b>Alexander Forsyth</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=alexforsyth" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://unsubstantiated.blog/"><img src="https://avatars.githubusercontent.com/u/1308885?v=4?s=100" width="100px;" alt="Alexander Steppke"/><br /><sub><b>Alexander Steppke</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=Miradorn" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://amani.kilumanga.com/"><img src="https://avatars.githubusercontent.com/u/8690282?v=4?s=100" width="100px;" alt="Amani Kilumanga"/><br /><sub><b>Amani Kilumanga</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=dkaksl" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://amin.fazl.me/"><img src="https://avatars.githubusercontent.com/u/62678026?v=4?s=100" width="100px;" alt="Amin Fazl"/><br /><sub><b>Amin Fazl</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=AminFazlMondo" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://kichik.com/"><img src="https://avatars.githubusercontent.com/u/1156773?v=4?s=100" width="100px;" alt="Amir Szekely"/><br /><sub><b>Amir Szekely</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kichik" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/amartinsg/"><img src="https://avatars.githubusercontent.com/u/54241354?v=4?s=100" width="100px;" alt="Anderson Gomes"/><br /><sub><b>Anderson Gomes</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=andersonmgomes" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/asdcamargo"><img src="https://avatars.githubusercontent.com/u/4683431?v=4?s=100" width="100px;" alt="Andre de Camargo"/><br /><sub><b>Andre de Camargo</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=asdcamargo" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://comfortabledelusions.blogspot.com/"><img src="https://avatars.githubusercontent.com/u/445764?v=4?s=100" width="100px;" alt="Andrew Hammond"/><br /><sub><b>Andrew Hammond</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=ahammond" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://apkostka.com/"><img src="https://avatars.githubusercontent.com/u/788482?v=4?s=100" width="100px;" alt="Andrew Kostka"/><br /><sub><b>Andrew Kostka</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=apkostka" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dippi"><img src="https://avatars.githubusercontent.com/u/3977098?v=4?s=100" width="100px;" alt="Angelo Di Pilla"/><br /><sub><b>Angelo Di Pilla</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=dippi" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ansgar.dev/"><img src="https://avatars.githubusercontent.com/u/1112056?v=4?s=100" width="100px;" alt="Ansgar Mertens"/><br /><sub><b>Ansgar Mertens</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=ansgarm" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yoyomo"><img src="https://avatars.githubusercontent.com/u/12818568?v=4?s=100" width="100px;" alt="Armando J. Ortiz Garcia"/><br /><sub><b>Armando J. Ortiz Garcia</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=yoyomo" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dontirun"><img src="https://avatars.githubusercontent.com/u/4570879?v=4?s=100" width="100px;" alt="Arun Donti"/><br /><sub><b>Arun Donti</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=dontirun" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/abelmokadem"><img src="https://avatars0.githubusercontent.com/u/9717944?v=4?s=100" width="100px;" alt="Ash"/><br /><sub><b>Ash</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=abelmokadem" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://austinbriggs.dev/"><img src="https://avatars.githubusercontent.com/u/7308231?v=4?s=100" width="100px;" alt="Austin"/><br /><sub><b>Austin</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=awbdallas" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kanatti"><img src="https://avatars.githubusercontent.com/u/8623654?v=4?s=100" width="100px;" alt="Balagopal Kanattil"/><br /><sub><b>Balagopal Kanattil</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kanatti" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.callant.net/"><img src="https://avatars1.githubusercontent.com/u/5915843?v=4?s=100" width="100px;" alt="Bart Callant"/><br /><sub><b>Bart Callant</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=bartcallant" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://beau.sh/"><img src="https://avatars.githubusercontent.com/u/127320?v=4?s=100" width="100px;" alt="Beau Bouchard"/><br /><sub><b>Beau Bouchard</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=BeauBouchard" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://benlimmer.com/"><img src="https://avatars.githubusercontent.com/u/630449?v=4?s=100" width="100px;" alt="Ben Limmer"/><br /><sub><b>Ben Limmer</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=blimmer" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://bilalquadri.com/"><img src="https://avatars.githubusercontent.com/u/707147?v=4?s=100" width="100px;" alt="Bilal Quadri"/><br /><sub><b>Bilal Quadri</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=bilalq" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://transacid.de/"><img src="https://avatars.githubusercontent.com/u/113231?v=4?s=100" width="100px;" alt="Boris Petersen"/><br /><sub><b>Boris Petersen</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=transacid" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/BradenM"><img src="https://avatars.githubusercontent.com/u/5913808?v=4?s=100" width="100px;" alt="Braden Mars"/><br /><sub><b>Braden Mars</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=BradenM" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bmiller08"><img src="https://avatars.githubusercontent.com/u/13002874?v=4?s=100" width="100px;" alt="Brandon Miller"/><br /><sub><b>Brandon Miller</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=bmiller08" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bhleonard"><img src="https://avatars.githubusercontent.com/u/1961679?v=4?s=100" width="100px;" alt="Brian Leonard"/><br /><sub><b>Brian Leonard</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=bhleonard" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/comcalvi"><img src="https://avatars.githubusercontent.com/u/66279577?v=4?s=100" width="100px;" alt="Calvin Combs"/><br /><sub><b>Calvin Combs</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=comcalvi" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cameroncf"><img src="https://avatars.githubusercontent.com/u/789760?v=4?s=100" width="100px;" alt="Cameron Childress"/><br /><sub><b>Cameron Childress</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=cameroncf" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/campionfellin"><img src="https://avatars3.githubusercontent.com/u/11984923?v=4?s=100" width="100px;" alt="Campion Fellin"/><br /><sub><b>Campion Fellin</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=campionfellin" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://medium.com/@caodanju"><img src="https://avatars.githubusercontent.com/u/18650321?v=4?s=100" width="100px;" alt="Cao Peng"/><br /><sub><b>Cao Peng</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=caopengau" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ctasada"><img src="https://avatars.githubusercontent.com/u/1381772?v=4?s=100" width="100px;" alt="Carlos Tasada"/><br /><sub><b>Carlos Tasada</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=ctasada" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://chrisb.cloud/"><img src="https://avatars.githubusercontent.com/u/12206103?v=4?s=100" width="100px;" alt="Chris Bateman"/><br /><sub><b>Chris Bateman</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=chris-bateman" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cgatt"><img src="https://avatars.githubusercontent.com/u/45865322?v=4?s=100" width="100px;" alt="Chris Gatt"/><br /><sub><b>Chris Gatt</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=cgatt" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://rybicki.io/"><img src="https://avatars2.githubusercontent.com/u/5008987?v=4?s=100" width="100px;" alt="Christopher Rybicki"/><br /><sub><b>Christopher Rybicki</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=Chriscbr" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/corymhall"><img src="https://avatars.githubusercontent.com/u/43035978?v=4?s=100" width="100px;" alt="Cory Hall"/><br /><sub><b>Cory Hall</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=corymhall" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://aws.amazon.com/chime/chime-sdk/"><img src="https://avatars.githubusercontent.com/u/71404236?v=4?s=100" width="100px;" alt="Court Schuett"/><br /><sub><b>Court Schuett</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=schuettc" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://medium.com/@craig.burdulis"><img src="https://avatars.githubusercontent.com/u/12520946?v=4?s=100" width="100px;" alt="Craig Burdulis"/><br /><sub><b>Craig Burdulis</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=icj217" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://pallares.io/"><img src="https://avatars3.githubusercontent.com/u/1077520?v=4?s=100" width="100px;" alt="Cristian Pallarés"/><br /><sub><b>Cristian Pallarés</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=skyrpex" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://danielmschmidt.de/"><img src="https://avatars.githubusercontent.com/u/1337046?v=4?s=100" width="100px;" alt="Daniel Schmidt"/><br /><sub><b>Daniel Schmidt</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=DanielMSchmidt" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://typefully.com/dannysteenman"><img src="https://avatars.githubusercontent.com/u/15192660?v=4?s=100" width="100px;" alt="Danny Steenman"/><br /><sub><b>Danny Steenman</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=dannysteenman" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dkershner6"><img src="https://avatars.githubusercontent.com/u/25798427?v=4?s=100" width="100px;" alt="Derek Kershner"/><br /><sub><b>Derek Kershner</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=dkershner6" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/eduardomourar"><img src="https://avatars.githubusercontent.com/u/16357187?v=4?s=100" width="100px;" alt="Eduardo Rodrigues"/><br /><sub><b>Eduardo Rodrigues</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=eduardomourar" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://eladb.github.com/"><img src="https://avatars3.githubusercontent.com/u/598796?v=4?s=100" width="100px;" alt="Elad Ben-Israel"/><br /><sub><b>Elad Ben-Israel</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=eladb" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/iliapolo"><img src="https://avatars.githubusercontent.com/u/1428812?v=4?s=100" width="100px;" alt="Eli Polonsky"/><br /><sub><b>Eli Polonsky</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=iliapolo" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://elig.io/"><img src="https://avatars.githubusercontent.com/u/22875166?v=4?s=100" width="100px;" alt="Eligio Mariño"/><br /><sub><b>Eligio Mariño</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=gmeligio" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Tucker-Eric"><img src="https://avatars.githubusercontent.com/u/6483755?v=4?s=100" width="100px;" alt="Eric Tucker"/><br /><sub><b>Eric Tucker</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=Tucker-Eric" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/echeung-amzn"><img src="https://avatars.githubusercontent.com/u/81188333?v=4?s=100" width="100px;" alt="Eugene Cheung"/><br /><sub><b>Eugene Cheung</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=echeung-amzn" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/FonsBiemans"><img src="https://avatars.githubusercontent.com/u/34266227?v=4?s=100" width="100px;" alt="Fons Biemans"/><br /><sub><b>Fons Biemans</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=FonsBiemans" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/froblesmartin"><img src="https://avatars.githubusercontent.com/u/18084174?v=4?s=100" width="100px;" alt="Francisco Robles Martín"/><br /><sub><b>Francisco Robles Martín</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=froblesmartin" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fynnfluegge"><img src="https://avatars.githubusercontent.com/u/16321871?v=4?s=100" width="100px;" alt="Fynn Flügge"/><br /><sub><b>Fynn Flügge</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=fynnfluegge" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/garysassano"><img src="https://avatars.githubusercontent.com/u/10464497?v=4?s=100" width="100px;" alt="Gary Sassano"/><br /><sub><b>Gary Sassano</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=garysassano" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/gradybarrett"><img src="https://avatars1.githubusercontent.com/u/1140074?v=4?s=100" width="100px;" alt="Grady Barrett"/><br /><sub><b>Grady Barrett</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=gradybarrett" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://blog.herlein.com/"><img src="https://avatars.githubusercontent.com/u/173428?v=4?s=100" width="100px;" alt="Greg Herlein"/><br /><sub><b>Greg Herlein</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=gherlein" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/GreggSetzer"><img src="https://avatars.githubusercontent.com/u/1624443?v=4?s=100" width="100px;" alt="Gregg"/><br /><sub><b>Gregg</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=GreggSetzer" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hasanaburayyan"><img src="https://avatars.githubusercontent.com/u/45375125?v=4?s=100" width="100px;" alt="Hasan"/><br /><sub><b>Hasan</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=hasanaburayyan" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hassanazharkhan"><img src="https://avatars.githubusercontent.com/u/57677979?v=4?s=100" width="100px;" alt="Hassan Azhar"/><br /><sub><b>Hassan Azhar</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=hassanazharkhan" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/HassanMahmud"><img src="https://avatars3.githubusercontent.com/u/58504381?v=4?s=100" width="100px;" alt="Hassan Mahmud"/><br /><sub><b>Hassan Mahmud</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=HassanMahmud" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://dk.linkedin.com/in/hassanmahmud93"><img src="https://avatars1.githubusercontent.com/u/7426703?v=4?s=100" width="100px;" alt="Hassan Mahmud"/><br /><sub><b>Hassan Mahmud</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=hass123uk" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mKeRix"><img src="https://avatars.githubusercontent.com/u/770596?v=4?s=100" width="100px;" alt="Heiko Rothe"/><br /><sub><b>Heiko Rothe</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mKeRix" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hyandell"><img src="https://avatars.githubusercontent.com/u/477715?v=4?s=100" width="100px;" alt="Henri Yandell"/><br /><sub><b>Henri Yandell</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=hyandell" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/henrysachs"><img src="https://avatars0.githubusercontent.com/u/17173951?v=4?s=100" width="100px;" alt="Henry Sachs"/><br /><sub><b>Henry Sachs</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=henrysachs" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://blog.hoseung.me/"><img src="https://avatars.githubusercontent.com/u/39669819?v=4?s=100" width="100px;" alt="Hoseung"/><br /><sub><b>Hoseung</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=HoseungJang" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://bandism.net/"><img src="https://avatars.githubusercontent.com/u/22633385?v=4?s=100" width="100px;" alt="Ikko Ashimine"/><br /><sub><b>Ikko Ashimine</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=eltociear" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jackleslie"><img src="https://avatars.githubusercontent.com/u/52004409?v=4?s=100" width="100px;" alt="Jack Leslie"/><br /><sub><b>Jack Leslie</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=jackleslie" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JackMoseley2001"><img src="https://avatars.githubusercontent.com/u/10659397?v=4?s=100" width="100px;" alt="Jack Moseley"/><br /><sub><b>Jack Moseley</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=JackMoseley2001" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cogwirrel"><img src="https://avatars.githubusercontent.com/u/1848603?v=4?s=100" width="100px;" alt="Jack Stevenson"/><br /><sub><b>Jack Stevenson</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=cogwirrel" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jmourelos"><img src="https://avatars3.githubusercontent.com/u/3878434?v=4?s=100" width="100px;" alt="Jacob"/><br /><sub><b>Jacob</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=jmourelos" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://joapy.com/"><img src="https://avatars3.githubusercontent.com/u/325306?v=4?s=100" width="100px;" alt="Jake Pearson"/><br /><sub><b>Jake Pearson</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=jakepearson" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://twitter.com/bracki"><img src="https://avatars.githubusercontent.com/u/49786?v=4?s=100" width="100px;" alt="Jan Brauer"/><br /><sub><b>Jan Brauer</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=bracki" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jmalins"><img src="https://avatars.githubusercontent.com/u/2001356?v=4?s=100" width="100px;" alt="Jeff Malins"/><br /><sub><b>Jeff Malins</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=jmalins" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JeremyJonas"><img src="https://avatars1.githubusercontent.com/u/464119?v=4?s=100" width="100px;" alt="Jeremy Jonas"/><br /><sub><b>Jeremy Jonas</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=JeremyJonas" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jesse-grabowski"><img src="https://avatars.githubusercontent.com/u/2453853?v=4?s=100" width="100px;" alt="Jesse Grabowski"/><br /><sub><b>Jesse Grabowski</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=jesse-grabowski" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jolo-dev"><img src="https://avatars.githubusercontent.com/u/54506108?v=4?s=100" width="100px;" alt="JoLo"/><br /><sub><b>JoLo</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=jolo-dev" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/devnoo"><img src="https://avatars.githubusercontent.com/u/94448?v=4?s=100" width="100px;" alt="Job de Noo"/><br /><sub><b>Job de Noo</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=devnoo" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jogold"><img src="https://avatars2.githubusercontent.com/u/12623249?v=4?s=100" width="100px;" alt="Jonathan Goldwasser"/><br /><sub><b>Jonathan Goldwasser</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=jogold" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/joostvdwsd"><img src="https://avatars.githubusercontent.com/u/25637088?v=4?s=100" width="100px;" alt="Joost van der Waal"/><br /><sub><b>Joost van der Waal</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=joostvdwsd" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JordanSinko"><img src="https://avatars2.githubusercontent.com/u/10212966?v=4?s=100" width="100px;" alt="Jordan Sinko"/><br /><sub><b>Jordan Sinko</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=JordanSinko" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/eganjs"><img src="https://avatars3.githubusercontent.com/u/6639482?v=4?s=100" width="100px;" alt="Joseph Egan"/><br /><sub><b>Joseph Egan</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=eganjs" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/misterjoshua"><img src="https://avatars2.githubusercontent.com/u/644092?v=4?s=100" width="100px;" alt="Josh Kellendonk"/><br /><sub><b>Josh Kellendonk</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=misterjoshua" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/juho9000"><img src="https://avatars.githubusercontent.com/u/13867853?v=4?s=100" width="100px;" alt="Juho Majasaari"/><br /><sub><b>Juho Majasaari</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=juho9000" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Hi-Fi"><img src="https://avatars.githubusercontent.com/u/1499780?v=4?s=100" width="100px;" alt="Juho Saarinen"/><br /><sub><b>Juho Saarinen</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=Hi-Fi" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/julian-michel-812a223a/"><img src="https://avatars.githubusercontent.com/u/15660169?v=4?s=100" width="100px;" alt="Julian Michel"/><br /><sub><b>Julian Michel</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=jumic" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kaizencc"><img src="https://avatars.githubusercontent.com/u/36202692?v=4?s=100" width="100px;" alt="Kaizen Conroy"/><br /><sub><b>Kaizen Conroy</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kaizencc" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kcwinner"><img src="https://avatars3.githubusercontent.com/u/2728868?v=4?s=100" width="100px;" alt="Kenneth Winner"/><br /><sub><b>Kenneth Winner</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kcwinner" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://kenneth.wussmann.net/"><img src="https://avatars.githubusercontent.com/u/11491506?v=4?s=100" width="100px;" alt="Kenneth Wußmann"/><br /><sub><b>Kenneth Wußmann</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=KennethWussmann" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kennyg"><img src="https://avatars.githubusercontent.com/u/98244?v=4?s=100" width="100px;" alt="Kenny Gatdula"/><br /><sub><b>Kenny Gatdula</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kennyg" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tinovyatkin"><img src="https://avatars.githubusercontent.com/u/5350898?v=4?s=100" width="100px;" alt="Konstantin Vyatkin"/><br /><sub><b>Konstantin Vyatkin</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=tinovyatkin" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bigkraig"><img src="https://avatars1.githubusercontent.com/u/508403?v=4?s=100" width="100px;" alt="Kraig Amador"/><br /><sub><b>Kraig Amador</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=bigkraig" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://kdabir.com/"><img src="https://avatars.githubusercontent.com/u/735240?v=4?s=100" width="100px;" alt="Kunal Dabir"/><br /><sub><b>Kunal Dabir</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kdabir" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://kylelaker.com/"><img src="https://avatars.githubusercontent.com/u/850893?v=4?s=100" width="100px;" alt="Kyle Laker"/><br /><sub><b>Kyle Laker</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kylelaker" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lexfelixpost"><img src="https://avatars.githubusercontent.com/u/112618115?v=4?s=100" width="100px;" alt="Lex Felix"/><br /><sub><b>Lex Felix</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=lexfelixpost" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lexGPT"><img src="https://avatars.githubusercontent.com/u/112618115?v=4?s=100" width="100px;" alt="Lex Felix"/><br /><sub><b>Lex Felix</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=lexGPT" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Liam-Johnston"><img src="https://avatars.githubusercontent.com/u/30859946?v=4?s=100" width="100px;" alt="Liam Johnston"/><br /><sub><b>Liam Johnston</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=Liam-Johnston" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/WtfJoke"><img src="https://avatars.githubusercontent.com/u/7139697?v=4?s=100" width="100px;" alt="Manuel"/><br /><sub><b>Manuel</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=WtfJoke" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/marciocadev"><img src="https://avatars.githubusercontent.com/u/67694075?v=4?s=100" width="100px;" alt="Marcio Cruz de Almeida"/><br /><sub><b>Marcio Cruz de Almeida</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=marciocadev" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mmcculloh-dms"><img src="https://avatars.githubusercontent.com/u/68597641?v=4?s=100" width="100px;" alt="Mark McCulloh"/><br /><sub><b>Mark McCulloh</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mmcculloh-dms" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/mark-mcculloh/"><img src="https://avatars.githubusercontent.com/u/1237390?v=4?s=100" width="100px;" alt="Mark McCulloh"/><br /><sub><b>Mark McCulloh</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=MarkMcCulloh" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://polothy.github.io/"><img src="https://avatars.githubusercontent.com/u/634657?v=4?s=100" width="100px;" alt="Mark Nielsen"/><br /><sub><b>Mark Nielsen</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=polothy" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/schuch"><img src="https://avatars.githubusercontent.com/u/6401299?v=4?s=100" width="100px;" alt="Markus Schuch"/><br /><sub><b>Markus Schuch</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=schuch" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/marnixdessing"><img src="https://avatars.githubusercontent.com/u/14939820?v=4?s=100" width="100px;" alt="Marnix Dessing"/><br /><sub><b>Marnix Dessing</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=marnixdessing" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mmuller88"><img src="https://avatars0.githubusercontent.com/u/18393842?v=4?s=100" width="100px;" alt="Martin Muller"/><br /><sub><b>Martin Muller</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mmuller88" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mzuber"><img src="https://avatars.githubusercontent.com/u/948563?v=4?s=100" width="100px;" alt="Martin Zuber"/><br /><sub><b>Martin Zuber</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mzuber" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://tmokmss.hatenablog.com/"><img src="https://avatars.githubusercontent.com/u/7490655?v=4?s=100" width="100px;" alt="Masashi Tomooka"/><br /><sub><b>Masashi Tomooka</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=tmokmss" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/matt9ucci"><img src="https://avatars.githubusercontent.com/u/8044346?v=4?s=100" width="100px;" alt="Matt Gucci"/><br /><sub><b>Matt Gucci</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=matt9ucci" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://dev.to/martzcodes"><img src="https://avatars1.githubusercontent.com/u/978362?v=4?s=100" width="100px;" alt="Matt Martz"/><br /><sub><b>Matt Martz</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=martzcodes" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/diranged"><img src="https://avatars.githubusercontent.com/u/768067?v=4?s=100" width="100px;" alt="Matt Wise"/><br /><sub><b>Matt Wise</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=diranged" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/msessa"><img src="https://avatars.githubusercontent.com/u/1912143?v=4?s=100" width="100px;" alt="Matteo Sessa"/><br /><sub><b>Matteo Sessa</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=msessa" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.matthewbonig.com/"><img src="https://avatars2.githubusercontent.com/u/1559437?v=4?s=100" width="100px;" alt="Matthew Bonig"/><br /><sub><b>Matthew Bonig</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mbonig" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mwg-rea"><img src="https://avatars.githubusercontent.com/u/82480228?v=4?s=100" width="100px;" alt="Matthew Gamble"/><br /><sub><b>Matthew Gamble</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mwg-rea" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fongie"><img src="https://avatars1.githubusercontent.com/u/19932622?v=4?s=100" width="100px;" alt="Max Körlinge"/><br /><sub><b>Max Körlinge</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=fongie" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mayurm88"><img src="https://avatars.githubusercontent.com/u/75965317?v=4?s=100" width="100px;" alt="Mayur Mahrotri"/><br /><sub><b>Mayur Mahrotri</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mayurm88" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Mayureshd-18"><img src="https://avatars.githubusercontent.com/u/98738585?v=4?s=100" width="100px;" alt="Mayuresh Dharwadkar"/><br /><sub><b>Mayuresh Dharwadkar</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=Mayureshd-18" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mikejgray"><img src="https://avatars.githubusercontent.com/u/30268971?v=4?s=100" width="100px;" alt="Mike"/><br /><sub><b>Mike</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mikejgray" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MrArnoldPalmer"><img src="https://avatars.githubusercontent.com/u/7221111?v=4?s=100" width="100px;" alt="Mitchell Valine"/><br /><sub><b>Mitchell Valine</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=MrArnoldPalmer" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://moritzkornher.de/"><img src="https://avatars.githubusercontent.com/u/379814?v=4?s=100" width="100px;" alt="Momo Kornher"/><br /><sub><b>Momo Kornher</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mrgrain" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/gmukul01"><img src="https://avatars.githubusercontent.com/u/3636885?v=4?s=100" width="100px;" alt="Mukul Bansal"/><br /><sub><b>Mukul Bansal</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=gmukul01" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://blog.neilkuan.net/"><img src="https://avatars.githubusercontent.com/u/46012524?v=4?s=100" width="100px;" alt="Neil Kuan"/><br /><sub><b>Neil Kuan</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=neilkuan" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nicholas-keers"><img src="https://avatars.githubusercontent.com/u/94363953?v=4?s=100" width="100px;" alt="Nick Keers"/><br /><sub><b>Nick Keers</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=nicholas-keers" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/njlynch"><img src="https://avatars.githubusercontent.com/u/1376292?v=4?s=100" width="100px;" alt="Nick Lynch"/><br /><sub><b>Nick Lynch</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=njlynch" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nbyl"><img src="https://avatars.githubusercontent.com/u/1185719?v=4?s=100" width="100px;" alt="Nicolas Byl"/><br /><sub><b>Nicolas Byl</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=nbyl" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nikhil-zadoo"><img src="https://avatars.githubusercontent.com/u/29751551?v=4?s=100" width="100px;" alt="Nikhil Zadoo"/><br /><sub><b>Nikhil Zadoo</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=nikhil-zadoo" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://nikovirtala.io/"><img src="https://avatars.githubusercontent.com/u/6813506?v=4?s=100" width="100px;" alt="Niko Virtala"/><br /><sub><b>Niko Virtala</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=nikovirtala" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/niraj8"><img src="https://avatars.githubusercontent.com/u/8666468?v=4?s=100" width="100px;" alt="Niraj Palecha"/><br /><sub><b>Niraj Palecha</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=niraj8" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dandelionur"><img src="https://avatars.githubusercontent.com/u/89805919?v=4?s=100" width="100px;" alt="Nurbanu"/><br /><sub><b>Nurbanu</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=dandelionur" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pahud"><img src="https://avatars3.githubusercontent.com/u/278432?v=4?s=100" width="100px;" alt="Pahud Hsieh"/><br /><sub><b>Pahud Hsieh</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=pahud" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/patrickdean"><img src="https://avatars.githubusercontent.com/u/1610088?v=4?s=100" width="100px;" alt="Patrick"/><br /><sub><b>Patrick</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=patrickdean" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/duckpuppy"><img src="https://avatars.githubusercontent.com/u/19253?v=4?s=100" width="100px;" alt="Patrick Aikens"/><br /><sub><b>Patrick Aikens</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=duckpuppy" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://pepperize.com/"><img src="https://avatars.githubusercontent.com/u/13916107?v=4?s=100" width="100px;" alt="Patrick Florek"/><br /><sub><b>Patrick Florek</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=pflorek" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/oconpa"><img src="https://avatars.githubusercontent.com/u/35761519?v=4?s=100" width="100px;" alt="Patrick O'Connor"/><br /><sub><b>Patrick O'Connor</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=oconpa" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://p6m7g8.github.io/"><img src="https://avatars0.githubusercontent.com/u/34295?v=4?s=100" width="100px;" alt="Philip M. Gollucci"/><br /><sub><b>Philip M. Gollucci</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=pgollucci" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/philipmw"><img src="https://avatars.githubusercontent.com/u/1379645?v=4?s=100" width="100px;" alt="Philip White"/><br /><sub><b>Philip White</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=philipmw" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://garbe.io/"><img src="https://avatars.githubusercontent.com/u/721899?v=4?s=100" width="100px;" alt="Philipp Garbe"/><br /><sub><b>Philipp Garbe</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=pgarbe" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://dynobase.dev/"><img src="https://avatars3.githubusercontent.com/u/3391616?v=4?s=100" width="100px;" alt="Rafal Wilinski"/><br /><sub><b>Rafal Wilinski</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=RafalWilinski" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ramihusein.com/"><img src="https://avatars.githubusercontent.com/u/96155378?v=4?s=100" width="100px;" alt="Rami Husein"/><br /><sub><b>Rami Husein</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=rami-husein" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://rix0r.nl/"><img src="https://avatars.githubusercontent.com/u/524162?v=4?s=100" width="100px;" alt="Rico Huijbers"/><br /><sub><b>Rico Huijbers</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=rix0rrr" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://tinkerin.gs/"><img src="https://avatars.githubusercontent.com/u/386001?v=4?s=100" width="100px;" alt="Rob Giseburt"/><br /><sub><b>Rob Giseburt</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=giseburt" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://robbiemackay.com/"><img src="https://avatars.githubusercontent.com/u/7965?v=4?s=100" width="100px;" alt="Robbie Mackay"/><br /><sub><b>Robbie Mackay</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=rjmackay" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/robert-affinidi"><img src="https://avatars.githubusercontent.com/u/88320072?v=4?s=100" width="100px;" alt="Robert"/><br /><sub><b>Robert</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=robert-affinidi" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://rfrezinos.wordpress.com/"><img src="https://avatars.githubusercontent.com/u/3926597?v=4?s=100" width="100px;" alt="Rodrigo Farias Rezino"/><br /><sub><b>Rodrigo Farias Rezino</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=rfrezino" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rogerchi"><img src="https://avatars.githubusercontent.com/u/625496?v=4?s=100" width="100px;" alt="Roger Chi"/><br /><sub><b>Roger Chi</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=rogerchi" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://keybase.io/romainmuller"><img src="https://avatars2.githubusercontent.com/u/411689?v=4?s=100" width="100px;" alt="Romain Marcadier"/><br /><sub><b>Romain Marcadier</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=RomainMuller" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/quesabe"><img src="https://avatars.githubusercontent.com/u/90195036?v=4?s=100" width="100px;" alt="Roman Vasilev"/><br /><sub><b>Roman Vasilev</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=quesabe" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dj-rabel"><img src="https://avatars.githubusercontent.com/u/4653214?v=4?s=100" width="100px;" alt="Ruben Pascal Abel"/><br /><sub><b>Ruben Pascal Abel</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=dj-rabel" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ryansonshine.com/"><img src="https://avatars.githubusercontent.com/u/9534477?v=4?s=100" width="100px;" alt="Ryan Sonshine"/><br /><sub><b>Ryan Sonshine</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=ryansonshine" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://medium.com/@riywo"><img src="https://avatars.githubusercontent.com/u/37822?v=4?s=100" width="100px;" alt="Ryosuke Iwanaga"/><br /><sub><b>Ryosuke Iwanaga</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=riywo" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aisamu"><img src="https://avatars.githubusercontent.com/u/431708?v=4?s=100" width="100px;" alt="Samuel Tschiedel"/><br /><sub><b>Samuel Tschiedel</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=aisamu" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/saudkhanzada"><img src="https://avatars.githubusercontent.com/u/30137907?v=4?s=100" width="100px;" alt="Saud Khanzada"/><br /><sub><b>Saud Khanzada</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=saudkhanzada" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/scottmondo"><img src="https://avatars.githubusercontent.com/u/91044021?v=4?s=100" width="100px;" alt="Scott McFarlane"/><br /><sub><b>Scott McFarlane</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=scottmondo" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/scottschreckengaust"><img src="https://avatars.githubusercontent.com/u/345885?v=4?s=100" width="100px;" alt="Scott Schreckengaust"/><br /><sub><b>Scott Schreckengaust</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=scottschreckengaust" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://skorfmann.com/"><img src="https://avatars1.githubusercontent.com/u/136789?v=4?s=100" width="100px;" alt="Sebastian Korfmann"/><br /><sub><b>Sebastian Korfmann</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=skorfmann" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://selfstructured.com/"><img src="https://avatars.githubusercontent.com/u/361689?v=4?s=100" width="100px;" alt="Shawn MacIntyre"/><br /><sub><b>Shawn MacIntyre</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=smacintyre" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/suhasgaddam-trueaccord"><img src="https://avatars.githubusercontent.com/u/68877840?v=4?s=100" width="100px;" alt="Suhas Gaddam"/><br /><sub><b>Suhas Gaddam</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=suhasgaddam-trueaccord" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/thomasklinger1234"><img src="https://avatars1.githubusercontent.com/u/39558817?v=4?s=100" width="100px;" alt="Thomas Klinger"/><br /><sub><b>Thomas Klinger</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=thomasklinger1234" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hoegertn"><img src="https://avatars2.githubusercontent.com/u/1287829?v=4?s=100" width="100px;" alt="Thorsten Hoeger"/><br /><sub><b>Thorsten Hoeger</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=hoegertn" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tiararodney"><img src="https://avatars.githubusercontent.com/u/56236443?v=4?s=100" width="100px;" alt="Tiara"/><br /><sub><b>Tiara</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=tiararodney" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tobias-bardino"><img src="https://avatars.githubusercontent.com/u/1842089?v=4?s=100" width="100px;" alt="Tobias"/><br /><sub><b>Tobias</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=tobias-bardino" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://windyroad.com.au/"><img src="https://avatars.githubusercontent.com/u/7802440?v=4?s=100" width="100px;" alt="Tom Howard"/><br /><sub><b>Tom Howard</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=tompahoward" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://dankmemes2020.com/"><img src="https://avatars.githubusercontent.com/u/1083460?v=4?s=100" width="100px;" alt="Tom Keller"/><br /><sub><b>Tom Keller</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kellertk" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://tlakomy.com/"><img src="https://avatars2.githubusercontent.com/u/16646517?v=4?s=100" width="100px;" alt="Tomasz Łakomy"/><br /><sub><b>Tomasz Łakomy</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=tlakomy" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tmartensen"><img src="https://avatars.githubusercontent.com/u/1750466?v=4?s=100" width="100px;" alt="Travis Martensen"/><br /><sub><b>Travis Martensen</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=tmartensen" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/floydspace"><img src="https://avatars.githubusercontent.com/u/5180700?v=4?s=100" width="100px;" alt="Victor Korzunin"/><br /><sub><b>Victor Korzunin</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=floydspace" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/VinayKokate22"><img src="https://avatars.githubusercontent.com/u/114766745?v=4?s=100" width="100px;" alt="VinayKokate22"/><br /><sub><b>VinayKokate22</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=VinayKokate22" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vinayak-kukreja"><img src="https://avatars.githubusercontent.com/u/78971045?v=4?s=100" width="100px;" alt="Vinayak Kukreja"/><br /><sub><b>Vinayak Kukreja</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=vinayak-kukreja" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vladcos"><img src="https://avatars.githubusercontent.com/u/135833592?v=4?s=100" width="100px;" alt="Vlad Cos"/><br /><sub><b>Vlad Cos</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=vladcos" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://willdady.com/"><img src="https://avatars.githubusercontent.com/u/204259?v=4?s=100" width="100px;" alt="Will Dady"/><br /><sub><b>Will Dady</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=willdady" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yglcode"><img src="https://avatars.githubusercontent.com/u/11893614?v=4?s=100" width="100px;" alt="Yigong Liu"/><br /><sub><b>Yigong Liu</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=yglcode" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rajyan"><img src="https://avatars.githubusercontent.com/u/38206553?v=4?s=100" width="100px;" alt="Yohta Kimura"/><br /><sub><b>Yohta Kimura</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=rajyan" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ykageyama-mondo"><img src="https://avatars.githubusercontent.com/u/91044220?v=4?s=100" width="100px;" alt="Yuichi Kageyama"/><br /><sub><b>Yuichi Kageyama</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=ykageyama-mondo" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://yuval.io/"><img src="https://avatars.githubusercontent.com/u/5735586?v=4?s=100" width="100px;" alt="Yuval"/><br /><sub><b>Yuval</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=yuvalherziger" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/andrestone"><img src="https://avatars1.githubusercontent.com/u/7958086?v=4?s=100" width="100px;" alt="andrestone"/><br /><sub><b>andrestone</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=andrestone" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/codeLeeek"><img src="https://avatars.githubusercontent.com/u/49740620?v=4?s=100" width="100px;" alt="codeLeeek"/><br /><sub><b>codeLeeek</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=codeLeeek" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/flyingImer"><img src="https://avatars0.githubusercontent.com/u/1973868?v=4?s=100" width="100px;" alt="flyingImer"/><br /><sub><b>flyingImer</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=flyingImer" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/huaxk"><img src="https://avatars.githubusercontent.com/u/9971591?v=4?s=100" width="100px;" alt="huaxk"/><br /><sub><b>huaxk</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=huaxk" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/john-tipper"><img src="https://avatars2.githubusercontent.com/u/9730398?v=4?s=100" width="100px;" alt="john-tipper"/><br /><sub><b>john-tipper</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=john-tipper" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/karlderkaefer"><img src="https://avatars.githubusercontent.com/u/9578480?v=4?s=100" width="100px;" alt="karlderkaefer"/><br /><sub><b>karlderkaefer</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=karlderkaefer" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kmkhr"><img src="https://avatars.githubusercontent.com/u/25603933?v=4?s=100" width="100px;" alt="kmkhr"/><br /><sub><b>kmkhr</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kmkhr" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kt-hr"><img src="https://avatars.githubusercontent.com/u/25603933?v=4?s=100" width="100px;" alt="kt-hr"/><br /><sub><b>kt-hr</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=kt-hr" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lmarsden"><img src="https://avatars.githubusercontent.com/u/51232932?v=4?s=100" width="100px;" alt="lmarsden"/><br /><sub><b>lmarsden</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=lmarsden" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mtimbs"><img src="https://avatars.githubusercontent.com/u/12463905?v=4?s=100" width="100px;" alt="michaeltimbs"/><br /><sub><b>michaeltimbs</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=mtimbs" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/orlandronen1"><img src="https://avatars.githubusercontent.com/u/25987273?v=4?s=100" width="100px;" alt="orlandronen1"/><br /><sub><b>orlandronen1</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=orlandronen1" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pvbouwel"><img src="https://avatars.githubusercontent.com/u/463976?v=4?s=100" width="100px;" alt="pvbouwel"/><br /><sub><b>pvbouwel</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=pvbouwel" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/suhussai"><img src="https://avatars.githubusercontent.com/u/6500837?v=4?s=100" width="100px;" alt="suhussai"/><br /><sub><b>suhussai</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=suhussai" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/t0bst4r"><img src="https://avatars.githubusercontent.com/u/82281152?v=4?s=100" width="100px;" alt="t0bst4r"/><br /><sub><b>t0bst4r</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=t0bst4r" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tHyt-lab"><img src="https://avatars.githubusercontent.com/u/11361677?v=4?s=100" width="100px;" alt="tHyt-lab"/><br /><sub><b>tHyt-lab</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=tHyt-lab" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Warkanlock"><img src="https://avatars.githubusercontent.com/u/13340320?v=4?s=100" width="100px;" alt="txxnano"/><br /><sub><b>txxnano</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=Warkanlock" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vVahe"><img src="https://avatars.githubusercontent.com/u/17318901?v=4?s=100" width="100px;" alt="vVahe"/><br /><sub><b>vVahe</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=vVahe" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/zetashift"><img src="https://avatars.githubusercontent.com/u/1857826?v=4?s=100" width="100px;" alt="zetashift"/><br /><sub><b>zetashift</b></sub></a><br /><a href="https://github.com/projen/projen/commits?author=zetashift" title="Code">💻</a></td>
    </tr>
  </tbody>
</table><!-- markdownlint-restore --><!-- prettier-ignore-end --><!-- ALL-CONTRIBUTORS-LIST:END -->

## License

Distributed under the [Apache-2.0](./LICENSE) license.
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

import constructs as _constructs_77d1e7e8


class Component(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.Component",
):
    '''(experimental) Represents a project component.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ee40327ed6d04e3e377e300d915d402c50029248a86452fd19fd6372386d4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="isComponent")
    @builtins.classmethod
    def is_component(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Test whether the given construct is a component.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9d0d027ed125bac76e8d566bfb14795a15c1055686082988040386c4bedd34)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isComponent", [x]))

    @jsii.member(jsii_name="postSynthesize")
    def post_synthesize(self) -> None:
        '''(experimental) Called after synthesis.

        Order is *not* guaranteed.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "postSynthesize", []))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before synthesis.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> None:
        '''(experimental) Synthesizes files to the project output directory.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", []))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> "Project":
        '''
        :stability: experimental
        '''
        return typing.cast("Project", jsii.get(self, "project"))


@jsii.data_type(
    jsii_type="projen.CreateProjectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "dir": "dir",
        "project_fqn": "projectFqn",
        "project_options": "projectOptions",
        "option_hints": "optionHints",
        "post": "post",
        "synth": "synth",
    },
)
class CreateProjectOptions:
    def __init__(
        self,
        *,
        dir: builtins.str,
        project_fqn: builtins.str,
        project_options: typing.Mapping[builtins.str, typing.Any],
        option_hints: typing.Optional["InitProjectOptionHints"] = None,
        post: typing.Optional[builtins.bool] = None,
        synth: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param dir: (experimental) Directory that the project will be generated in.
        :param project_fqn: (experimental) Fully-qualified name of the project type (usually formatted as ``projen.module.ProjectType``).
        :param project_options: (experimental) Project options. Only JSON-like values can be passed in (strings, booleans, numbers, enums, arrays, and objects that are not derived from classes). Consult the API reference of the project type you are generating for information about what fields and types are available.
        :param option_hints: (experimental) Should we render commented-out default options in the projenrc file? Does not apply to projenrc.json files. Default: InitProjectOptionHints.FEATURED
        :param post: (experimental) Should we execute post synthesis hooks? (usually package manager install). Default: true
        :param synth: (experimental) Should we call ``project.synth()`` or instantiate the project (could still have side-effects) and render the .projenrc file. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b756505fc1a7b685751d86fb21738eff63b2be7bdec39ba7000083473d5336)
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
            check_type(argname="argument project_fqn", value=project_fqn, expected_type=type_hints["project_fqn"])
            check_type(argname="argument project_options", value=project_options, expected_type=type_hints["project_options"])
            check_type(argname="argument option_hints", value=option_hints, expected_type=type_hints["option_hints"])
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dir": dir,
            "project_fqn": project_fqn,
            "project_options": project_options,
        }
        if option_hints is not None:
            self._values["option_hints"] = option_hints
        if post is not None:
            self._values["post"] = post
        if synth is not None:
            self._values["synth"] = synth

    @builtins.property
    def dir(self) -> builtins.str:
        '''(experimental) Directory that the project will be generated in.

        :stability: experimental
        '''
        result = self._values.get("dir")
        assert result is not None, "Required property 'dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_fqn(self) -> builtins.str:
        '''(experimental) Fully-qualified name of the project type (usually formatted as ``projen.module.ProjectType``).

        :stability: experimental

        Example::

            `projen.typescript.TypescriptProject`
        '''
        result = self._values.get("project_fqn")
        assert result is not None, "Required property 'project_fqn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_options(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Project options.

        Only JSON-like values can be passed in (strings,
        booleans, numbers, enums, arrays, and objects that are not
        derived from classes).

        Consult the API reference of the project type you are generating for
        information about what fields and types are available.

        :stability: experimental
        '''
        result = self._values.get("project_options")
        assert result is not None, "Required property 'project_options' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def option_hints(self) -> typing.Optional["InitProjectOptionHints"]:
        '''(experimental) Should we render commented-out default options in the projenrc file?

        Does not apply to projenrc.json files.

        :default: InitProjectOptionHints.FEATURED

        :stability: experimental
        '''
        result = self._values.get("option_hints")
        return typing.cast(typing.Optional["InitProjectOptionHints"], result)

    @builtins.property
    def post(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should we execute post synthesis hooks?

        (usually package manager install).

        :default: true

        :stability: experimental
        '''
        result = self._values.get("post")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synth(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should we call ``project.synth()`` or instantiate the project (could still have side-effects) and render the .projenrc file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Dependencies(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.Dependencies"):
    '''(experimental) The ``Dependencies`` component is responsible to track the list of dependencies a project has, and then used by project types as the model for rendering project-specific dependency manifests such as the dependencies section ``package.json`` files.

    To add a dependency you can use a project-type specific API such as
    ``nodeProject.addDeps()`` or use the generic API of ``project.deps``:

    :stability: experimental
    '''

    def __init__(self, project: "Project") -> None:
        '''(experimental) Adds a dependencies component to the project.

        :param project: The parent project.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21c75206d44a727988f2f61c5957c08fb9e7b6843dfc8d7e89642b17409e04b)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])

    @jsii.member(jsii_name="parseDependency")
    @builtins.classmethod
    def parse_dependency(cls, spec: builtins.str) -> "DependencyCoordinates":
        '''(experimental) Returns the coordinates of a dependency spec.

        Given ``foo@^3.4.0`` returns ``{ name: "foo", version: "^3.4.0" }``.
        Given ``bar@npm:@bar/legacy`` returns ``{ name: "bar", version: "npm:@bar/legacy" }``.

        :param spec: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8cbb5fe28335a2b7b5cb79b4fcdeca39e6f339dea939a6ad73b6a47b495bd1c)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        return typing.cast("DependencyCoordinates", jsii.sinvoke(cls, "parseDependency", [spec]))

    @jsii.member(jsii_name="addDependency")
    def add_dependency(
        self,
        spec: builtins.str,
        type: "DependencyType",
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> "Dependency":
        '''(experimental) Adds a dependency to this project.

        :param spec: The dependency spec in the format ``MODULE[@VERSION]`` where ``MODULE`` is the package-manager-specific module name and ``VERSION`` is an optional semantic version requirement (e.g. ``^3.4.0``).
        :param type: The type of the dependency.
        :param metadata: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee54ffac07e98cfaef250245a5920a70ff038b7635db44aaefe1c9ef634e49a)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        return typing.cast("Dependency", jsii.invoke(self, "addDependency", [spec, type, metadata]))

    @jsii.member(jsii_name="getDependency")
    def get_dependency(
        self,
        name: builtins.str,
        type: typing.Optional["DependencyType"] = None,
    ) -> "Dependency":
        '''(experimental) Returns a dependency by name.

        Fails if there is no dependency defined by that name or if ``type`` is not
        provided and there is more then one dependency type for this dependency.

        :param name: The name of the dependency.
        :param type: The dependency type. If this dependency is defined only for a single type, this argument can be omitted.

        :return: a copy (cannot be modified)

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3683be12709967dd63dafbe536558d7717d255f3a86dfad1e17c19c9d9185beb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast("Dependency", jsii.invoke(self, "getDependency", [name, type]))

    @jsii.member(jsii_name="isDependencySatisfied")
    def is_dependency_satisfied(
        self,
        name: builtins.str,
        type: "DependencyType",
        expected_range: builtins.str,
    ) -> builtins.bool:
        '''(experimental) Checks if an existing dependency satisfies a dependency requirement.

        :param name: The name of the dependency to check (without the version).
        :param type: The dependency type.
        :param expected_range: The version constraint to check (e.g. ``^3.4.0``). The constraint of the dependency must be a subset of the expected range to satisfy the requirements.

        :return:

        ``true`` if the dependency exists and its version satisfies the provided constraint. ``false`` otherwise.
        Notably returns ``false`` if a dependency exists, but has no version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628e50591481575ad249671e7cf61edd1bb37d5aeab5e143a0783051e3167dcc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument expected_range", value=expected_range, expected_type=type_hints["expected_range"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isDependencySatisfied", [name, type, expected_range]))

    @jsii.member(jsii_name="removeDependency")
    def remove_dependency(
        self,
        name: builtins.str,
        type: typing.Optional["DependencyType"] = None,
    ) -> None:
        '''(experimental) Removes a dependency.

        :param name: The name of the module to remove (without the version).
        :param type: The dependency type. This is only required if there the dependency is defined for multiple types.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4260bbdc4d6b4d5249dbb539f6f4fe1f865c069d0179abe451af2807f194bf7d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast(None, jsii.invoke(self, "removeDependency", [name, type]))

    @jsii.member(jsii_name="tryGetDependency")
    def try_get_dependency(
        self,
        name: builtins.str,
        type: typing.Optional["DependencyType"] = None,
    ) -> typing.Optional["Dependency"]:
        '''(experimental) Returns a dependency by name.

        Returns ``undefined`` if there is no dependency defined by that name or if
        ``type`` is not provided and there is more then one dependency type for this
        dependency.

        :param name: The name of the dependency.
        :param type: The dependency type. If this dependency is defined only for a single type, this argument can be omitted.

        :return: a copy (cannot be modified) or undefined if there is no match

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0705dd461300a1275ac19f07b173cb3d54d5b40432a75919fe838b828c94f95d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast(typing.Optional["Dependency"], jsii.invoke(self, "tryGetDependency", [name, type]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANIFEST_FILE")
    def MANIFEST_FILE(cls) -> builtins.str:
        '''(experimental) The project-relative path of the deps manifest file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MANIFEST_FILE"))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.List["Dependency"]:
        '''(experimental) A copy of all dependencies recorded for this project.

        The list is sorted by type->name->version

        :stability: experimental
        '''
        return typing.cast(typing.List["Dependency"], jsii.get(self, "all"))


@jsii.data_type(
    jsii_type="projen.DependencyCoordinates",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "version": "version"},
)
class DependencyCoordinates:
    def __init__(
        self,
        *,
        name: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Coordinates of the dependency (name and version).

        :param name: (experimental) The package manager name of the dependency (e.g. ``leftpad`` for npm). NOTE: For package managers that use complex coordinates (like Maven), we will codify it into a string somehow.
        :param version: (experimental) Semantic version version requirement. Default: - requirement is managed by the package manager (e.g. npm/yarn).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64ddd02bc83dba01b190c70805fc134d208559c5dbe1186f34a86af68e73c9b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The package manager name of the dependency (e.g. ``leftpad`` for npm).

        NOTE: For package managers that use complex coordinates (like Maven), we
        will codify it into a string somehow.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Semantic version version requirement.

        :default: - requirement is managed by the package manager (e.g. npm/yarn).

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DependencyCoordinates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.DependencyType")
class DependencyType(enum.Enum):
    '''(experimental) Type of dependency.

    :stability: experimental
    '''

    RUNTIME = "RUNTIME"
    '''(experimental) The dependency is required for the program/library during runtime.

    :stability: experimental
    '''
    PEER = "PEER"
    '''(experimental) The dependency is required at runtime but expected to be installed by the consumer.

    :stability: experimental
    '''
    BUNDLED = "BUNDLED"
    '''(experimental) The dependency is bundled and shipped with the module, so consumers are not required to install it.

    :stability: experimental
    '''
    BUILD = "BUILD"
    '''(experimental) The dependency is required to run the ``build`` task.

    :stability: experimental
    '''
    TEST = "TEST"
    '''(experimental) The dependency is required to run the ``test`` task.

    :stability: experimental
    '''
    DEVENV = "DEVENV"
    '''(experimental) The dependency is required for development (e.g. IDE plugins).

    :stability: experimental
    '''
    OVERRIDE = "OVERRIDE"
    '''(experimental) Transient dependency that needs to be overwritten.

    Available for Node packages

    :stability: experimental
    '''
    OPTIONAL = "OPTIONAL"
    '''(experimental) An optional dependency that may be used at runtime if available, but is not required.

    It is expected to be installed by the consumer.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.DepsManifest",
    jsii_struct_bases=[],
    name_mapping={"dependencies": "dependencies"},
)
class DepsManifest:
    def __init__(
        self,
        *,
        dependencies: typing.Sequence[typing.Union["Dependency", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param dependencies: (experimental) All dependencies of this module.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77631e913a8f4e12310c9799410432f0abdd84b99d70b5d3f09a352ce9cec92)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dependencies": dependencies,
        }

    @builtins.property
    def dependencies(self) -> typing.List["Dependency"]:
        '''(experimental) All dependencies of this module.

        :stability: experimental
        '''
        result = self._values.get("dependencies")
        assert result is not None, "Required property 'dependencies' is missing"
        return typing.cast(typing.List["Dependency"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DepsManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevEnvironmentDockerImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.DevEnvironmentDockerImage",
):
    '''(experimental) Options for specifying the Docker image of the container.

    :stability: experimental
    '''

    @jsii.member(jsii_name="fromFile")
    @builtins.classmethod
    def from_file(cls, docker_file: builtins.str) -> "DevEnvironmentDockerImage":
        '''(experimental) The relative path of a Dockerfile that defines the container contents.

        :param docker_file: a relative path.

        :stability: experimental

        Example::

            '.gitpod.Docker'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb1f5fb6ea97ef53502fa2942dba716f3c8ed084859934f3db1146f80586fc7)
            check_type(argname="argument docker_file", value=docker_file, expected_type=type_hints["docker_file"])
        return typing.cast("DevEnvironmentDockerImage", jsii.sinvoke(cls, "fromFile", [docker_file]))

    @jsii.member(jsii_name="fromImage")
    @builtins.classmethod
    def from_image(cls, image: builtins.str) -> "DevEnvironmentDockerImage":
        '''(experimental) A publicly available Docker image.

        :param image: a Docker image.

        :stability: experimental

        Example::

            'ubuntu:latest'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f197cc85d2f9d6a23d36b30e6b45f48a7c8cdd6998dc4351ad40c3e98ed433)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("DevEnvironmentDockerImage", jsii.sinvoke(cls, "fromImage", [image]))

    @builtins.property
    @jsii.member(jsii_name="dockerFile")
    def docker_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The relative path of a Dockerfile that defines the container contents.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerFile"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> typing.Optional[builtins.str]:
        '''(experimental) A publicly available Docker image.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "image"))


@jsii.data_type(
    jsii_type="projen.DevEnvironmentOptions",
    jsii_struct_bases=[],
    name_mapping={
        "docker_image": "dockerImage",
        "ports": "ports",
        "tasks": "tasks",
        "vscode_extensions": "vscodeExtensions",
    },
)
class DevEnvironmentOptions:
    def __init__(
        self,
        *,
        docker_image: typing.Optional[DevEnvironmentDockerImage] = None,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        tasks: typing.Optional[typing.Sequence["Task"]] = None,
        vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Base options for configuring a container-based development environment.

        :param docker_image: (experimental) A Docker image or Dockerfile for the container.
        :param ports: (experimental) An array of ports that should be exposed from the container.
        :param tasks: (experimental) An array of tasks that should be run when the container starts.
        :param vscode_extensions: (experimental) An array of extension IDs that specify the extensions that should be installed inside the container when it is created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f9fbb0608ff35697f2bca0295d53e3ffdf0cc4e15602b3a9e57732048e372a)
            check_type(argname="argument docker_image", value=docker_image, expected_type=type_hints["docker_image"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
            check_type(argname="argument vscode_extensions", value=vscode_extensions, expected_type=type_hints["vscode_extensions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if ports is not None:
            self._values["ports"] = ports
        if tasks is not None:
            self._values["tasks"] = tasks
        if vscode_extensions is not None:
            self._values["vscode_extensions"] = vscode_extensions

    @builtins.property
    def docker_image(self) -> typing.Optional[DevEnvironmentDockerImage]:
        '''(experimental) A Docker image or Dockerfile for the container.

        :stability: experimental
        '''
        result = self._values.get("docker_image")
        return typing.cast(typing.Optional[DevEnvironmentDockerImage], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of ports that should be exposed from the container.

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tasks(self) -> typing.Optional[typing.List["Task"]]:
        '''(experimental) An array of tasks that should be run when the container starts.

        :stability: experimental
        '''
        result = self._values.get("tasks")
        return typing.cast(typing.Optional[typing.List["Task"]], result)

    @builtins.property
    def vscode_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of extension IDs that specify the extensions that should be installed inside the container when it is created.

        :stability: experimental
        '''
        result = self._values.get("vscode_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevEnvironmentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerCompose(
    Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.DockerCompose",
):
    '''(experimental) Create a docker-compose YAML file.

    :stability: experimental
    '''

    def __init__(
        self,
        project: "Project",
        *,
        name_suffix: typing.Optional[builtins.str] = None,
        schema_version: typing.Optional[builtins.str] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union["DockerComposeServiceDescription", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param project: -
        :param name_suffix: (experimental) A name to add to the docker-compose.yml filename. Default: - no name is added
        :param schema_version: (deprecated) Docker Compose schema version do be used. Default: - no version is provided
        :param services: (experimental) Service descriptions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befd8e58ddccbbc1a83afe6a4e464b7951ad377df97c7553777909a18eefec9a)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        props = DockerComposeProps(
            name_suffix=name_suffix, schema_version=schema_version, services=services
        )

        jsii.create(self.__class__, self, [project, props])

    @jsii.member(jsii_name="bindVolume")
    @builtins.classmethod
    def bind_volume(
        cls,
        source_path: builtins.str,
        target_path: builtins.str,
    ) -> "IDockerComposeVolumeBinding":
        '''(experimental) Create a bind volume that binds a host path to the target path in the container.

        :param source_path: Host path name.
        :param target_path: Target path name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbde193e2934374214d86400f997cf06d47a8585dd93f52c3a476e5897c5f717)
            check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            check_type(argname="argument target_path", value=target_path, expected_type=type_hints["target_path"])
        return typing.cast("IDockerComposeVolumeBinding", jsii.sinvoke(cls, "bindVolume", [source_path, target_path]))

    @jsii.member(jsii_name="namedVolume")
    @builtins.classmethod
    def named_volume(
        cls,
        volume_name: builtins.str,
        target_path: builtins.str,
        *,
        driver: typing.Optional[builtins.str] = None,
        driver_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        external: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "IDockerComposeVolumeBinding":
        '''(experimental) Create a named volume and mount it to the target path.

        If you use this
        named volume in several services, the volume will be shared. In this
        case, the volume configuration of the first-provided options are used.

        :param volume_name: Name of the volume.
        :param target_path: Target path.
        :param driver: (experimental) Driver to use for the volume. Default: - value is not provided
        :param driver_opts: (experimental) Options to provide to the driver.
        :param external: (experimental) Set to true to indicate that the volume is externally created. Default: - unset, indicating that docker-compose creates the volume
        :param name: (experimental) Name of the volume for when the volume name isn't going to work in YAML. Default: - unset, indicating that docker-compose creates volumes as usual

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeaaa9c2706df5a20eae30c6213caaeaedacf3a08430db4d0fd38a0b299c47b6)
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
            check_type(argname="argument target_path", value=target_path, expected_type=type_hints["target_path"])
        options = DockerComposeVolumeConfig(
            driver=driver, driver_opts=driver_opts, external=external, name=name
        )

        return typing.cast("IDockerComposeVolumeBinding", jsii.sinvoke(cls, "namedVolume", [volume_name, target_path, options]))

    @jsii.member(jsii_name="network")
    @builtins.classmethod
    def network(
        cls,
        network_name: builtins.str,
        *,
        attachable: typing.Optional[builtins.bool] = None,
        bridge: typing.Optional[builtins.bool] = None,
        driver: typing.Optional[builtins.str] = None,
        driver_opts: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
        external: typing.Optional[builtins.bool] = None,
        internal: typing.Optional[builtins.bool] = None,
        ipam: typing.Optional[typing.Union["DockerComposeNetworkIpamConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        overlay: typing.Optional[builtins.bool] = None,
    ) -> "IDockerComposeNetworkBinding":
        '''(experimental) Create a named network and mount it to the target path.

        If you use this
        named network in several services, the network will be shared. In this
        case, the network configuration of the first-provided options are used.

        :param network_name: Name of the network.
        :param attachable: (experimental) Set to true to indicate that standalone containers can attach to this network, in addition to services. Default: - unset
        :param bridge: (experimental) Set to true to indicate that the network is a bridge network. Default: - unset
        :param driver: (experimental) Driver to use for the network. Default: - value is not provided
        :param driver_opts: (experimental) Options for the configured driver. Those options are driver-dependent - consult the driver’s documentation for more information Default: - value is not provided
        :param external: (experimental) Set to true to indicate that the network is externally created. Default: - unset, indicating that docker-compose creates the network
        :param internal: (experimental) Set to true to indicate that you want to create an externally isolated overlay network. Default: - unset
        :param ipam: (experimental) Specify custom IPAM config. Default: - unset
        :param labels: (experimental) Attach labels to the network. Default: - unset
        :param name: (experimental) Name of the network for when the network name isn't going to work in YAML. Default: - unset, indicating that docker-compose creates networks as usual
        :param overlay: (experimental) Set to true to indicate that the network is an overlay network. Default: - unset

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4d54561cac4572c9face67ceab438aae8d3bbe82eee002cc02eab5cc06adc6)
            check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
        options = DockerComposeNetworkConfig(
            attachable=attachable,
            bridge=bridge,
            driver=driver,
            driver_opts=driver_opts,
            external=external,
            internal=internal,
            ipam=ipam,
            labels=labels,
            name=name,
            overlay=overlay,
        )

        return typing.cast("IDockerComposeNetworkBinding", jsii.sinvoke(cls, "network", [network_name, options]))

    @jsii.member(jsii_name="portMapping")
    @builtins.classmethod
    def port_mapping(
        cls,
        published_port: jsii.Number,
        target_port: jsii.Number,
        *,
        protocol: typing.Optional["DockerComposeProtocol"] = None,
    ) -> "DockerComposeServicePort":
        '''(experimental) Create a port mapping.

        :param published_port: Published port number.
        :param target_port: Container's port number.
        :param protocol: (experimental) Port mapping protocol. Default: DockerComposeProtocol.TCP

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28e8b1e411352eae906d43069127630bff58f30fb830fe48f618d5e1bb92561)
            check_type(argname="argument published_port", value=published_port, expected_type=type_hints["published_port"])
            check_type(argname="argument target_port", value=target_port, expected_type=type_hints["target_port"])
        options = DockerComposePortMappingOptions(protocol=protocol)

        return typing.cast("DockerComposeServicePort", jsii.sinvoke(cls, "portMapping", [published_port, target_port, options]))

    @jsii.member(jsii_name="serviceName")
    @builtins.classmethod
    def service_name(cls, service_name: builtins.str) -> "IDockerComposeServiceName":
        '''(experimental) Depends on a service name.

        :param service_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b78d50eb49bb7a7dd6f729eb60da0db3c69b31e910843128de46ce542356481)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        return typing.cast("IDockerComposeServiceName", jsii.sinvoke(cls, "serviceName", [service_name]))

    @jsii.member(jsii_name="addService")
    def add_service(
        self,
        service_name: builtins.str,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        depends_on: typing.Optional[typing.Sequence["IDockerComposeServiceName"]] = None,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        image_build: typing.Optional[typing.Union["DockerComposeBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        networks: typing.Optional[typing.Sequence["IDockerComposeNetworkBinding"]] = None,
        platform: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Sequence[typing.Union["DockerComposeServicePort", typing.Dict[builtins.str, typing.Any]]]] = None,
        privileged: typing.Optional[builtins.bool] = None,
        volumes: typing.Optional[typing.Sequence["IDockerComposeVolumeBinding"]] = None,
    ) -> "DockerComposeService":
        '''(experimental) Add a service to the docker-compose file.

        :param service_name: name of the service.
        :param command: (experimental) Provide a command to the docker container. Default: - use the container's default command
        :param depends_on: (experimental) Names of other services this service depends on. Default: - no dependencies
        :param entrypoint: (experimental) Entrypoint to run in the container.
        :param environment: (experimental) Add environment variables. Default: - no environment variables are provided
        :param image: (experimental) Use a docker image. Note: You must specify either ``build`` or ``image`` key.
        :param image_build: (experimental) Build a docker image. Note: You must specify either ``imageBuild`` or ``image`` key.
        :param labels: (experimental) Add labels. Default: - no labels are provided
        :param networks: (experimental) Add some networks to the service.
        :param platform: (experimental) Add platform. Default: - no platform is provided
        :param ports: (experimental) Map some ports. Default: - no ports are mapped
        :param privileged: (experimental) Run in privileged mode. Default: - no privileged mode flag is provided
        :param volumes: (experimental) Mount some volumes into the service. Use one of the following to create volumes:

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03cd3d199bdbdda7ab3d37e736cec1900b73411477c6a08c6efe431a50bc9b7)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        description = DockerComposeServiceDescription(
            command=command,
            depends_on=depends_on,
            entrypoint=entrypoint,
            environment=environment,
            image=image,
            image_build=image_build,
            labels=labels,
            networks=networks,
            platform=platform,
            ports=ports,
            privileged=privileged,
            volumes=volumes,
        )

        return typing.cast("DockerComposeService", jsii.invoke(self, "addService", [service_name, description]))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> "YamlFile":
        '''(experimental) The Docker Compose file.

        :stability: experimental
        '''
        return typing.cast("YamlFile", jsii.get(self, "file"))


@jsii.data_type(
    jsii_type="projen.DockerComposeBuild",
    jsii_struct_bases=[],
    name_mapping={"context": "context", "args": "args", "dockerfile": "dockerfile"},
)
class DockerComposeBuild:
    def __init__(
        self,
        *,
        context: builtins.str,
        args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        dockerfile: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Build arguments for creating a docker image.

        :param context: (experimental) Docker build context directory.
        :param args: (experimental) Build args. Default: - none are provided
        :param dockerfile: (experimental) A dockerfile to build from. Default: "Dockerfile"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec1d86693bd77b64c91103900c6f20c2fda50c12b5d159089260e80ecd89534)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument dockerfile", value=dockerfile, expected_type=type_hints["dockerfile"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context": context,
        }
        if args is not None:
            self._values["args"] = args
        if dockerfile is not None:
            self._values["dockerfile"] = dockerfile

    @builtins.property
    def context(self) -> builtins.str:
        '''(experimental) Docker build context directory.

        :stability: experimental
        '''
        result = self._values.get("context")
        assert result is not None, "Required property 'context' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build args.

        :default: - none are provided

        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def dockerfile(self) -> typing.Optional[builtins.str]:
        '''(experimental) A dockerfile to build from.

        :default: "Dockerfile"

        :stability: experimental
        '''
        result = self._values.get("dockerfile")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeBuild(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.DockerComposeNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "attachable": "attachable",
        "bridge": "bridge",
        "driver": "driver",
        "driver_opts": "driverOpts",
        "external": "external",
        "internal": "internal",
        "ipam": "ipam",
        "labels": "labels",
        "name": "name",
        "overlay": "overlay",
    },
)
class DockerComposeNetworkConfig:
    def __init__(
        self,
        *,
        attachable: typing.Optional[builtins.bool] = None,
        bridge: typing.Optional[builtins.bool] = None,
        driver: typing.Optional[builtins.str] = None,
        driver_opts: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
        external: typing.Optional[builtins.bool] = None,
        internal: typing.Optional[builtins.bool] = None,
        ipam: typing.Optional[typing.Union["DockerComposeNetworkIpamConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        overlay: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Network configuration.

        :param attachable: (experimental) Set to true to indicate that standalone containers can attach to this network, in addition to services. Default: - unset
        :param bridge: (experimental) Set to true to indicate that the network is a bridge network. Default: - unset
        :param driver: (experimental) Driver to use for the network. Default: - value is not provided
        :param driver_opts: (experimental) Options for the configured driver. Those options are driver-dependent - consult the driver’s documentation for more information Default: - value is not provided
        :param external: (experimental) Set to true to indicate that the network is externally created. Default: - unset, indicating that docker-compose creates the network
        :param internal: (experimental) Set to true to indicate that you want to create an externally isolated overlay network. Default: - unset
        :param ipam: (experimental) Specify custom IPAM config. Default: - unset
        :param labels: (experimental) Attach labels to the network. Default: - unset
        :param name: (experimental) Name of the network for when the network name isn't going to work in YAML. Default: - unset, indicating that docker-compose creates networks as usual
        :param overlay: (experimental) Set to true to indicate that the network is an overlay network. Default: - unset

        :stability: experimental
        '''
        if isinstance(ipam, dict):
            ipam = DockerComposeNetworkIpamConfig(**ipam)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cbd18688d70c5aa20cd294c874f9ad54a013d605cfa3b06afe6935c7b8a0d1e)
            check_type(argname="argument attachable", value=attachable, expected_type=type_hints["attachable"])
            check_type(argname="argument bridge", value=bridge, expected_type=type_hints["bridge"])
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
            check_type(argname="argument driver_opts", value=driver_opts, expected_type=type_hints["driver_opts"])
            check_type(argname="argument external", value=external, expected_type=type_hints["external"])
            check_type(argname="argument internal", value=internal, expected_type=type_hints["internal"])
            check_type(argname="argument ipam", value=ipam, expected_type=type_hints["ipam"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overlay", value=overlay, expected_type=type_hints["overlay"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attachable is not None:
            self._values["attachable"] = attachable
        if bridge is not None:
            self._values["bridge"] = bridge
        if driver is not None:
            self._values["driver"] = driver
        if driver_opts is not None:
            self._values["driver_opts"] = driver_opts
        if external is not None:
            self._values["external"] = external
        if internal is not None:
            self._values["internal"] = internal
        if ipam is not None:
            self._values["ipam"] = ipam
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if overlay is not None:
            self._values["overlay"] = overlay

    @builtins.property
    def attachable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to indicate that standalone containers can attach to this network, in addition to services.

        :default: - unset

        :stability: experimental
        '''
        result = self._values.get("attachable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bridge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to indicate that the network is a bridge network.

        :default: - unset

        :stability: experimental
        '''
        result = self._values.get("bridge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def driver(self) -> typing.Optional[builtins.str]:
        '''(experimental) Driver to use for the network.

        :default: - value is not provided

        :stability: experimental
        '''
        result = self._values.get("driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_opts(self) -> typing.Optional[typing.Mapping[typing.Any, typing.Any]]:
        '''(experimental) Options for the configured driver.

        Those options are driver-dependent - consult the driver’s documentation for more information

        :default: - value is not provided

        :stability: experimental
        '''
        result = self._values.get("driver_opts")
        return typing.cast(typing.Optional[typing.Mapping[typing.Any, typing.Any]], result)

    @builtins.property
    def external(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to indicate that the network is externally created.

        :default: - unset, indicating that docker-compose creates the network

        :stability: experimental
        '''
        result = self._values.get("external")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def internal(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to indicate that you want to create an externally isolated overlay network.

        :default: - unset

        :stability: experimental
        '''
        result = self._values.get("internal")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ipam(self) -> typing.Optional["DockerComposeNetworkIpamConfig"]:
        '''(experimental) Specify custom IPAM config.

        :default: - unset

        :stability: experimental
        '''
        result = self._values.get("ipam")
        return typing.cast(typing.Optional["DockerComposeNetworkIpamConfig"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Attach labels to the network.

        :default: - unset

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the network for when the network name isn't going to work in YAML.

        :default: - unset, indicating that docker-compose creates networks as usual

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overlay(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to indicate that the network is an overlay network.

        :default: - unset

        :stability: experimental
        '''
        result = self._values.get("overlay")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.DockerComposeNetworkIpamConfig",
    jsii_struct_bases=[],
    name_mapping={"config": "config", "driver": "driver"},
)
class DockerComposeNetworkIpamConfig:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Sequence[typing.Union["DockerComposeNetworkIpamSubnetConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        driver: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) IPAM configuration.

        :param config: (experimental) A list with zero or more config blocks specifying custom IPAM configuration. Default: - value is not provided
        :param driver: (experimental) Driver to use for custom IPAM config. Default: - value is not provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a79d28871602ad2e3a12572c9bdbe88a19a0cd4514aeea2aa5b801edfcc357)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if driver is not None:
            self._values["driver"] = driver

    @builtins.property
    def config(
        self,
    ) -> typing.Optional[typing.List["DockerComposeNetworkIpamSubnetConfig"]]:
        '''(experimental) A list with zero or more config blocks specifying custom IPAM configuration.

        :default: - value is not provided

        :stability: experimental
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.List["DockerComposeNetworkIpamSubnetConfig"]], result)

    @builtins.property
    def driver(self) -> typing.Optional[builtins.str]:
        '''(experimental) Driver to use for custom IPAM config.

        :default: - value is not provided

        :stability: experimental
        '''
        result = self._values.get("driver")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeNetworkIpamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.DockerComposeNetworkIpamSubnetConfig",
    jsii_struct_bases=[],
    name_mapping={"subnet": "subnet"},
)
class DockerComposeNetworkIpamSubnetConfig:
    def __init__(self, *, subnet: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) IPAM subnet configuration.

        :param subnet: (experimental) Subnet in CIDR format that represents a network segment. Default: - value is not provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fbcd82d9063449e5df6ae96f9d244e4622a690f9aef8c482271440a89d10c2e)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def subnet(self) -> typing.Optional[builtins.str]:
        '''(experimental) Subnet in CIDR format that represents a network segment.

        :default: - value is not provided

        :stability: experimental
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeNetworkIpamSubnetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.DockerComposePortMappingOptions",
    jsii_struct_bases=[],
    name_mapping={"protocol": "protocol"},
)
class DockerComposePortMappingOptions:
    def __init__(
        self,
        *,
        protocol: typing.Optional["DockerComposeProtocol"] = None,
    ) -> None:
        '''(experimental) Options for port mappings.

        :param protocol: (experimental) Port mapping protocol. Default: DockerComposeProtocol.TCP

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb9ce9a73b268348669bdc9854f34f198e98370c491dd80459bbcb5e10e1a9f)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def protocol(self) -> typing.Optional["DockerComposeProtocol"]:
        '''(experimental) Port mapping protocol.

        :default: DockerComposeProtocol.TCP

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["DockerComposeProtocol"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposePortMappingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.DockerComposeProps",
    jsii_struct_bases=[],
    name_mapping={
        "name_suffix": "nameSuffix",
        "schema_version": "schemaVersion",
        "services": "services",
    },
)
class DockerComposeProps:
    def __init__(
        self,
        *,
        name_suffix: typing.Optional[builtins.str] = None,
        schema_version: typing.Optional[builtins.str] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union["DockerComposeServiceDescription", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Props for DockerCompose.

        :param name_suffix: (experimental) A name to add to the docker-compose.yml filename. Default: - no name is added
        :param schema_version: (deprecated) Docker Compose schema version do be used. Default: - no version is provided
        :param services: (experimental) Service descriptions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b3a9f497a8a34deecb2bf90e8650e81e98e0a4a6480a090f371e2d60385583)
            check_type(argname="argument name_suffix", value=name_suffix, expected_type=type_hints["name_suffix"])
            check_type(argname="argument schema_version", value=schema_version, expected_type=type_hints["schema_version"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name_suffix is not None:
            self._values["name_suffix"] = name_suffix
        if schema_version is not None:
            self._values["schema_version"] = schema_version
        if services is not None:
            self._values["services"] = services

    @builtins.property
    def name_suffix(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name to add to the docker-compose.yml filename.

        :default: - no name is added

        :stability: experimental

        Example::

            'myname' yields 'docker-compose.myname.yml'
        '''
        result = self._values.get("name_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_version(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Docker Compose schema version do be used.

        :default: - no version is provided

        :deprecated:

        - The top level ``version`` field is obsolete per the Compose Specification.
        {@link https://github.com/compose-spec/compose-spec/blob/master/spec.md#version-and-name-top-level-elements Compose Specification}

        :stability: deprecated
        '''
        result = self._values.get("schema_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "DockerComposeServiceDescription"]]:
        '''(experimental) Service descriptions.

        :stability: experimental
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "DockerComposeServiceDescription"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.DockerComposeProtocol")
class DockerComposeProtocol(enum.Enum):
    '''(experimental) Network protocol for port mapping.

    :stability: experimental
    '''

    TCP = "TCP"
    '''(experimental) TCP protocol.

    :stability: experimental
    '''
    UDP = "UDP"
    '''(experimental) UDP protocol.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.DockerComposeServiceDescription",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "depends_on": "dependsOn",
        "entrypoint": "entrypoint",
        "environment": "environment",
        "image": "image",
        "image_build": "imageBuild",
        "labels": "labels",
        "networks": "networks",
        "platform": "platform",
        "ports": "ports",
        "privileged": "privileged",
        "volumes": "volumes",
    },
)
class DockerComposeServiceDescription:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        depends_on: typing.Optional[typing.Sequence["IDockerComposeServiceName"]] = None,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        image_build: typing.Optional[typing.Union[DockerComposeBuild, typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        networks: typing.Optional[typing.Sequence["IDockerComposeNetworkBinding"]] = None,
        platform: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Sequence[typing.Union["DockerComposeServicePort", typing.Dict[builtins.str, typing.Any]]]] = None,
        privileged: typing.Optional[builtins.bool] = None,
        volumes: typing.Optional[typing.Sequence["IDockerComposeVolumeBinding"]] = None,
    ) -> None:
        '''(experimental) Description of a docker-compose.yml service.

        :param command: (experimental) Provide a command to the docker container. Default: - use the container's default command
        :param depends_on: (experimental) Names of other services this service depends on. Default: - no dependencies
        :param entrypoint: (experimental) Entrypoint to run in the container.
        :param environment: (experimental) Add environment variables. Default: - no environment variables are provided
        :param image: (experimental) Use a docker image. Note: You must specify either ``build`` or ``image`` key.
        :param image_build: (experimental) Build a docker image. Note: You must specify either ``imageBuild`` or ``image`` key.
        :param labels: (experimental) Add labels. Default: - no labels are provided
        :param networks: (experimental) Add some networks to the service.
        :param platform: (experimental) Add platform. Default: - no platform is provided
        :param ports: (experimental) Map some ports. Default: - no ports are mapped
        :param privileged: (experimental) Run in privileged mode. Default: - no privileged mode flag is provided
        :param volumes: (experimental) Mount some volumes into the service. Use one of the following to create volumes:

        :stability: experimental
        '''
        if isinstance(image_build, dict):
            image_build = DockerComposeBuild(**image_build)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7374d6018aac8e9a9098b7b003039b5286a79bcf032fc0db6de3b0c56f496889)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument image_build", value=image_build, expected_type=type_hints["image_build"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if environment is not None:
            self._values["environment"] = environment
        if image is not None:
            self._values["image"] = image
        if image_build is not None:
            self._values["image_build"] = image_build
        if labels is not None:
            self._values["labels"] = labels
        if networks is not None:
            self._values["networks"] = networks
        if platform is not None:
            self._values["platform"] = platform
        if ports is not None:
            self._values["ports"] = ports
        if privileged is not None:
            self._values["privileged"] = privileged
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Provide a command to the docker container.

        :default: - use the container's default command

        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["IDockerComposeServiceName"]]:
        '''(experimental) Names of other services this service depends on.

        :default: - no dependencies

        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List["IDockerComposeServiceName"]], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Entrypoint to run in the container.

        :stability: experimental
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Add environment variables.

        :default: - no environment variables are provided

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use a docker image.

        Note: You must specify either ``build`` or ``image`` key.

        :see: imageBuild
        :stability: experimental
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_build(self) -> typing.Optional[DockerComposeBuild]:
        '''(experimental) Build a docker image.

        Note: You must specify either ``imageBuild`` or ``image`` key.

        :see: image
        :stability: experimental
        '''
        result = self._values.get("image_build")
        return typing.cast(typing.Optional[DockerComposeBuild], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Add labels.

        :default: - no labels are provided

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def networks(self) -> typing.Optional[typing.List["IDockerComposeNetworkBinding"]]:
        '''(experimental) Add some networks to the service.

        :see: DockerCompose.network () to create & mount a named network
        :stability: experimental
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.List["IDockerComposeNetworkBinding"]], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''(experimental) Add platform.

        :default: - no platform is provided

        :stability: experimental
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List["DockerComposeServicePort"]]:
        '''(experimental) Map some ports.

        :default: - no ports are mapped

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List["DockerComposeServicePort"]], result)

    @builtins.property
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run in privileged mode.

        :default: - no privileged mode flag is provided

        :stability: experimental
        '''
        result = self._values.get("privileged")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["IDockerComposeVolumeBinding"]]:
        '''(experimental) Mount some volumes into the service.

        Use one of the following to create volumes:

        :see: DockerCompose.namedVolume () to create & mount a named volume
        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List["IDockerComposeVolumeBinding"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeServiceDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.DockerComposeServicePort",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "protocol": "protocol",
        "published": "published",
        "target": "target",
    },
)
class DockerComposeServicePort:
    def __init__(
        self,
        *,
        mode: builtins.str,
        protocol: DockerComposeProtocol,
        published: jsii.Number,
        target: jsii.Number,
    ) -> None:
        '''(experimental) A service port mapping.

        :param mode: (experimental) Port mapping mode.
        :param protocol: (experimental) Network protocol.
        :param published: (experimental) Published port number.
        :param target: (experimental) Target port number.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79390f2bae006141612e4d3816151bd8cf6a9d2bb9d761dce7fbd344d4235193)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument published", value=published, expected_type=type_hints["published"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "protocol": protocol,
            "published": published,
            "target": target,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''(experimental) Port mapping mode.

        :stability: experimental
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> DockerComposeProtocol:
        '''(experimental) Network protocol.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(DockerComposeProtocol, result)

    @builtins.property
    def published(self) -> jsii.Number:
        '''(experimental) Published port number.

        :stability: experimental
        '''
        result = self._values.get("published")
        assert result is not None, "Required property 'published' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def target(self) -> jsii.Number:
        '''(experimental) Target port number.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeServicePort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.DockerComposeVolumeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "driver": "driver",
        "driver_opts": "driverOpts",
        "external": "external",
        "name": "name",
    },
)
class DockerComposeVolumeConfig:
    def __init__(
        self,
        *,
        driver: typing.Optional[builtins.str] = None,
        driver_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        external: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Volume configuration.

        :param driver: (experimental) Driver to use for the volume. Default: - value is not provided
        :param driver_opts: (experimental) Options to provide to the driver.
        :param external: (experimental) Set to true to indicate that the volume is externally created. Default: - unset, indicating that docker-compose creates the volume
        :param name: (experimental) Name of the volume for when the volume name isn't going to work in YAML. Default: - unset, indicating that docker-compose creates volumes as usual

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47648decff569ea19a9be75dee07ad2312da74920b6079ae0b293fedfcad0db3)
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
            check_type(argname="argument driver_opts", value=driver_opts, expected_type=type_hints["driver_opts"])
            check_type(argname="argument external", value=external, expected_type=type_hints["external"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver is not None:
            self._values["driver"] = driver
        if driver_opts is not None:
            self._values["driver_opts"] = driver_opts
        if external is not None:
            self._values["external"] = external
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def driver(self) -> typing.Optional[builtins.str]:
        '''(experimental) Driver to use for the volume.

        :default: - value is not provided

        :stability: experimental
        '''
        result = self._values.get("driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_opts(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Options to provide to the driver.

        :stability: experimental
        '''
        result = self._values.get("driver_opts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def external(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to indicate that the volume is externally created.

        :default: - unset, indicating that docker-compose creates the volume

        :stability: experimental
        '''
        result = self._values.get("external")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the volume for when the volume name isn't going to work in YAML.

        :default: - unset, indicating that docker-compose creates volumes as usual

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeVolumeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.DockerComposeVolumeMount",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "target": "target", "type": "type"},
)
class DockerComposeVolumeMount:
    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        type: builtins.str,
    ) -> None:
        '''(experimental) Service volume mounting information.

        :param source: (experimental) Volume source.
        :param target: (experimental) Volume target.
        :param type: (experimental) Type of volume.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a24a69b1370bfa662e08b21b5f9c5f6da2f1526d8bd7b111c9f8ada371108f2)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
            "type": type,
        }

    @builtins.property
    def source(self) -> builtins.str:
        '''(experimental) Volume source.

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''(experimental) Volume target.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) Type of volume.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerComposeVolumeMount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.EndOfLine")
class EndOfLine(enum.Enum):
    '''(experimental) The end of line characters supported by git.

    :stability: experimental
    '''

    AUTO = "AUTO"
    '''(experimental) Maintain existing (mixed values within one file are normalised by looking at what's used after the first line).

    :stability: experimental
    '''
    CRLF = "CRLF"
    '''(experimental) Carriage Return + Line Feed characters (\\r\\n), common on Windows.

    :stability: experimental
    '''
    LF = "LF"
    '''(experimental) Line Feed only (\\n), common on Linux and macOS as well as inside git repos.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) Disable and do not configure the end of line character.

    :stability: experimental
    '''


class FileBase(
    Component,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="projen.FileBase",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        file_path: builtins.str,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param file_path: -
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cecf514142ea351ec43b0f632ba832e665a18f91b6e46531fd8bb688b82c1b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = FileBaseOptions(
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [scope, file_path, options])

    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> None:
        '''(experimental) Writes the file to the project's output directory.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", []))

    @jsii.member(jsii_name="synthesizeContent")
    @abc.abstractmethod
    def _synthesize_content(
        self,
        resolver: "IResolver",
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: Call ``resolver.resolve(obj)`` on any objects in order to resolve token functions.

        :return: the content to synthesize or undefined to skip the file

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="absolutePath")
    def absolute_path(self) -> builtins.str:
        '''(experimental) The absolute path of this file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "absolutePath"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) The file path, relative to the project's outdir.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="changed")
    def changed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if the file has been changed during synthesis.

        This property is
        only available in ``postSynthesize()`` hooks. If this is ``undefined``, the
        file has not been synthesized yet.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "changed"))

    @builtins.property
    @jsii.member(jsii_name="marker")
    def marker(self) -> typing.Optional[builtins.str]:
        '''(experimental) The projen marker, used to identify files as projen-generated.

        Value is undefined if the project is being ejected.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "marker"))

    @builtins.property
    @jsii.member(jsii_name="executable")
    def executable(self) -> builtins.bool:
        '''(experimental) Indicates if the file should be marked as executable.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "executable"))

    @executable.setter
    def executable(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fed3e4c76496e254ef32ce4556e7e1b3b0cef6929de044486dda20248a06c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readonly")
    def readonly(self) -> builtins.bool:
        '''(experimental) Indicates if the file should be read-only or read-write.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "readonly"))

    @readonly.setter
    def readonly(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20fcd33148f053d9de2f2152439cc9f0687a0e328bf05cb8b38721095832ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readonly", value) # pyright: ignore[reportArgumentType]


class _FileBaseProxy(FileBase):
    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(
        self,
        resolver: "IResolver",
    ) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: Call ``resolver.resolve(obj)`` on any objects in order to resolve token functions.

        :return: the content to synthesize or undefined to skip the file

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c33cd4fb527e2ef4af066a0254c78d4dd70bed7a8e8cab1f8ec80fb2981c8db)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FileBase).__jsii_proxy_class__ = lambda : _FileBaseProxy


@jsii.data_type(
    jsii_type="projen.FileBaseOptions",
    jsii_struct_bases=[],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
    },
)
class FileBaseOptions:
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177d8a347651b29224d730dd6e1bbec48e6dd46e5dcfd4d25e3798e6761d4c63)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileBaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitAttributesFile(
    FileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.GitAttributesFile",
):
    '''(experimental) Assign attributes to file names in a git repository.

    :see: https://git-scm.com/docs/gitattributes
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        *,
        end_of_line: typing.Optional[EndOfLine] = None,
    ) -> None:
        '''
        :param scope: -
        :param end_of_line: (experimental) The default end of line character for text files. endOfLine it's useful to keep the same end of line between Windows and Unix operative systems for git checking/checkout operations. Hence, it can avoid simple repository mutations consisting only of changes in the end of line characters. It will be set in the first line of the .gitattributes file to make it the first match with high priority but it can be overriden in a later line. Can be disabled by setting explicitly: ``{ endOfLine: EndOfLine.NONE }``. Default: EndOfLine.LF

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a914753a9db7cc6bfa6a166cf7ee02794375210a09b1d8e2c62496abf14b4d21)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = GitAttributesFileOptions(end_of_line=end_of_line)

        jsii.create(self.__class__, self, [scope, options])

    @jsii.member(jsii_name="addAttributes")
    def add_attributes(self, glob: builtins.str, *attributes: builtins.str) -> None:
        '''(experimental) Maps a set of attributes to a set of files.

        :param glob: Glob pattern to match files in the repo.
        :param attributes: Attributes to assign to these files.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc1d5969ab32878c5548a9a17af7e781548f696676f62cee57518e7f5bf0a66)
            check_type(argname="argument glob", value=glob, expected_type=type_hints["glob"])
            check_type(argname="argument attributes", value=attributes, expected_type=typing.Tuple[type_hints["attributes"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addAttributes", [glob, *attributes]))

    @jsii.member(jsii_name="addLfsPattern")
    def add_lfs_pattern(self, glob: builtins.str) -> None:
        '''(experimental) Add attributes necessary to mark these files as stored in LFS.

        :param glob: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3c05c2bc87434261501604cb4ca8386e08b16567b40f693170ab90f635b1a7)
            check_type(argname="argument glob", value=glob, expected_type=type_hints["glob"])
        return typing.cast(None, jsii.invoke(self, "addLfsPattern", [glob]))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before synthesis.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, _: "IResolver") -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param _: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d57ceb4d14bb3b3eac67478ac542d99ca5c6994286fdea034dacdf4b64fd14b)
            check_type(argname="argument _", value=_, expected_type=type_hints["_"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [_]))

    @builtins.property
    @jsii.member(jsii_name="endOfLine")
    def end_of_line(self) -> EndOfLine:
        '''(experimental) The default end of line character for text files.

        :stability: experimental
        '''
        return typing.cast(EndOfLine, jsii.get(self, "endOfLine"))

    @builtins.property
    @jsii.member(jsii_name="hasLfsPatterns")
    def has_lfs_patterns(self) -> builtins.bool:
        '''(experimental) Whether the current gitattributes file has any LFS patterns.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "hasLfsPatterns"))


@jsii.data_type(
    jsii_type="projen.GitAttributesFileOptions",
    jsii_struct_bases=[],
    name_mapping={"end_of_line": "endOfLine"},
)
class GitAttributesFileOptions:
    def __init__(self, *, end_of_line: typing.Optional[EndOfLine] = None) -> None:
        '''(experimental) Options for ``GitAttributesFile``.

        :param end_of_line: (experimental) The default end of line character for text files. endOfLine it's useful to keep the same end of line between Windows and Unix operative systems for git checking/checkout operations. Hence, it can avoid simple repository mutations consisting only of changes in the end of line characters. It will be set in the first line of the .gitattributes file to make it the first match with high priority but it can be overriden in a later line. Can be disabled by setting explicitly: ``{ endOfLine: EndOfLine.NONE }``. Default: EndOfLine.LF

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a54cc3274f754056a1301deb3e7902a7a31057da6ade20b64dae8487831db5)
            check_type(argname="argument end_of_line", value=end_of_line, expected_type=type_hints["end_of_line"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end_of_line is not None:
            self._values["end_of_line"] = end_of_line

    @builtins.property
    def end_of_line(self) -> typing.Optional[EndOfLine]:
        '''(experimental) The default end of line character for text files.

        endOfLine it's useful to keep the same end of line between Windows and Unix operative systems for git checking/checkout operations. Hence, it can avoid simple repository mutations consisting only of changes in the end of line characters. It will be set in the first line of the .gitattributes file to make it the first match with high priority but it can be overriden in a later line. Can be disabled by setting explicitly: ``{ endOfLine: EndOfLine.NONE }``.

        :default: EndOfLine.LF

        :stability: experimental
        '''
        result = self._values.get("end_of_line")
        return typing.cast(typing.Optional[EndOfLine], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitAttributesFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.GitOptions",
    jsii_struct_bases=[],
    name_mapping={"end_of_line": "endOfLine", "lfs_patterns": "lfsPatterns"},
)
class GitOptions:
    def __init__(
        self,
        *,
        end_of_line: typing.Optional[EndOfLine] = None,
        lfs_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Git configuration options.

        :param end_of_line: (experimental) The default end of line character for text files. endOfLine it's useful to keep the same end of line between Windows and Unix operative systems for git checking/checkout operations. Hence, it can avoid simple repository mutations consisting only of changes in the end of line characters. It will be set in the first line of the .gitattributes file to make it the first match with high priority but it can be overriden in a later line. Can be disabled by setting: ``endOfLine: EndOfLine.NONE``. Default: EndOfLine.LF
        :param lfs_patterns: (experimental) File patterns to mark as stored in Git LFS. Default: - No files stored in LFS

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7f1b3b819a95ebdb112752cdc122d5362da95c419decd69ec24018f344bace)
            check_type(argname="argument end_of_line", value=end_of_line, expected_type=type_hints["end_of_line"])
            check_type(argname="argument lfs_patterns", value=lfs_patterns, expected_type=type_hints["lfs_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end_of_line is not None:
            self._values["end_of_line"] = end_of_line
        if lfs_patterns is not None:
            self._values["lfs_patterns"] = lfs_patterns

    @builtins.property
    def end_of_line(self) -> typing.Optional[EndOfLine]:
        '''(experimental) The default end of line character for text files.

        endOfLine it's useful to keep the same end of line between Windows and Unix operative systems for git checking/checkout operations.
        Hence, it can avoid simple repository mutations consisting only of changes in the end of line characters.
        It will be set in the first line of the .gitattributes file to make it the first match with high priority but it can be overriden in a later line.
        Can be disabled by setting: ``endOfLine: EndOfLine.NONE``.

        :default: EndOfLine.LF

        :stability: experimental
        '''
        result = self._values.get("end_of_line")
        return typing.cast(typing.Optional[EndOfLine], result)

    @builtins.property
    def lfs_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) File patterns to mark as stored in Git LFS.

        :default: - No files stored in LFS

        :stability: experimental
        '''
        result = self._values.get("lfs_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.GitpodOnOpen")
class GitpodOnOpen(enum.Enum):
    '''(experimental) What to do when a service on a port is detected.

    :stability: experimental
    '''

    OPEN_BROWSER = "OPEN_BROWSER"
    '''(experimental) Open a new browser tab.

    :stability: experimental
    '''
    OPEN_PREVIEW = "OPEN_PREVIEW"
    '''(experimental) Open a preview on the right side of the IDE.

    :stability: experimental
    '''
    NOTIFY = "NOTIFY"
    '''(experimental) Show a notification asking the user what to do (default).

    :stability: experimental
    '''
    IGNORE = "IGNORE"
    '''(experimental) Do nothing.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.GitpodOpenIn")
class GitpodOpenIn(enum.Enum):
    '''(experimental) Configure where in the IDE the terminal should be opened.

    :stability: experimental
    '''

    BOTTOM = "BOTTOM"
    '''(experimental) the bottom panel (default).

    :stability: experimental
    '''
    LEFT = "LEFT"
    '''(experimental) the left panel.

    :stability: experimental
    '''
    RIGHT = "RIGHT"
    '''(experimental) the right panel.

    :stability: experimental
    '''
    MAIN = "MAIN"
    '''(experimental) the main editor area.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.GitpodOpenMode")
class GitpodOpenMode(enum.Enum):
    '''(experimental) Configure how the terminal should be opened relative to the previous task.

    :stability: experimental
    '''

    TAB_AFTER = "TAB_AFTER"
    '''(experimental) Opens in the same tab group right after the previous tab.

    :stability: experimental
    '''
    TAB_BEFORE = "TAB_BEFORE"
    '''(experimental) Opens in the same tab group left before the previous tab.

    :stability: experimental
    '''
    SPLIT_RIGHT = "SPLIT_RIGHT"
    '''(experimental) Splits and adds the terminal to the right.

    :stability: experimental
    '''
    SPLIT_LEFT = "SPLIT_LEFT"
    '''(experimental) Splits and adds the terminal to the left.

    :stability: experimental
    '''
    SPLIT_TOP = "SPLIT_TOP"
    '''(experimental) Splits and adds the terminal to the top.

    :stability: experimental
    '''
    SPLIT_BOTTOM = "SPLIT_BOTTOM"
    '''(experimental) Splits and adds the terminal to the bottom.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.GitpodOptions",
    jsii_struct_bases=[DevEnvironmentOptions],
    name_mapping={
        "docker_image": "dockerImage",
        "ports": "ports",
        "tasks": "tasks",
        "vscode_extensions": "vscodeExtensions",
        "prebuilds": "prebuilds",
    },
)
class GitpodOptions(DevEnvironmentOptions):
    def __init__(
        self,
        *,
        docker_image: typing.Optional[DevEnvironmentDockerImage] = None,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        tasks: typing.Optional[typing.Sequence["Task"]] = None,
        vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        prebuilds: typing.Optional[typing.Union["GitpodPrebuilds", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Constructor options for the Gitpod component.

        By default, Gitpod uses the 'gitpod/workspace-full' docker image.

        :param docker_image: (experimental) A Docker image or Dockerfile for the container.
        :param ports: (experimental) An array of ports that should be exposed from the container.
        :param tasks: (experimental) An array of tasks that should be run when the container starts.
        :param vscode_extensions: (experimental) An array of extension IDs that specify the extensions that should be installed inside the container when it is created.
        :param prebuilds: (experimental) Optional Gitpod's Github App integration for prebuilds If this is not set and Gitpod's Github App is installed, then Gitpod will apply these defaults: https://www.gitpod.io/docs/prebuilds/#configure-the-github-app. Default: undefined

        :see:

        https://github.com/gitpod-io/workspace-images/blob/master/full/Dockerfile

        By default, all tasks will be run in parallel. To run the tasks in sequence,
        create a new task and specify the other tasks as subtasks.
        :stability: experimental
        '''
        if isinstance(prebuilds, dict):
            prebuilds = GitpodPrebuilds(**prebuilds)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1a97c01ec9e70bdd9c3e5a8cfa72f551b923d5d9aded0885f9210b87e09f4b)
            check_type(argname="argument docker_image", value=docker_image, expected_type=type_hints["docker_image"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
            check_type(argname="argument vscode_extensions", value=vscode_extensions, expected_type=type_hints["vscode_extensions"])
            check_type(argname="argument prebuilds", value=prebuilds, expected_type=type_hints["prebuilds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if ports is not None:
            self._values["ports"] = ports
        if tasks is not None:
            self._values["tasks"] = tasks
        if vscode_extensions is not None:
            self._values["vscode_extensions"] = vscode_extensions
        if prebuilds is not None:
            self._values["prebuilds"] = prebuilds

    @builtins.property
    def docker_image(self) -> typing.Optional[DevEnvironmentDockerImage]:
        '''(experimental) A Docker image or Dockerfile for the container.

        :stability: experimental
        '''
        result = self._values.get("docker_image")
        return typing.cast(typing.Optional[DevEnvironmentDockerImage], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of ports that should be exposed from the container.

        :stability: experimental
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tasks(self) -> typing.Optional[typing.List["Task"]]:
        '''(experimental) An array of tasks that should be run when the container starts.

        :stability: experimental
        '''
        result = self._values.get("tasks")
        return typing.cast(typing.Optional[typing.List["Task"]], result)

    @builtins.property
    def vscode_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of extension IDs that specify the extensions that should be installed inside the container when it is created.

        :stability: experimental
        '''
        result = self._values.get("vscode_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prebuilds(self) -> typing.Optional["GitpodPrebuilds"]:
        '''(experimental) Optional Gitpod's Github App integration for prebuilds If this is not set and Gitpod's Github App is installed, then Gitpod will apply these defaults: https://www.gitpod.io/docs/prebuilds/#configure-the-github-app.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("prebuilds")
        return typing.cast(typing.Optional["GitpodPrebuilds"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitpodOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.GitpodPort",
    jsii_struct_bases=[],
    name_mapping={"on_open": "onOpen", "port": "port", "visibility": "visibility"},
)
class GitpodPort:
    def __init__(
        self,
        *,
        on_open: typing.Optional[GitpodOnOpen] = None,
        port: typing.Optional[builtins.str] = None,
        visibility: typing.Optional["GitpodPortVisibility"] = None,
    ) -> None:
        '''(experimental) Options for an exposed port on Gitpod.

        :param on_open: (experimental) What to do when a service on a port is detected. Default: GitpodOnOpen.NOTIFY
        :param port: (experimental) A port that should be exposed (forwarded) from the container.
        :param visibility: (experimental) Whether the port visibility should be private or public. Default: GitpodPortVisibility.PUBLIC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540294b664aee1f54c7bdb211f5b8781649ae01dfd5e50f7003f34c0689caed2)
            check_type(argname="argument on_open", value=on_open, expected_type=type_hints["on_open"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_open is not None:
            self._values["on_open"] = on_open
        if port is not None:
            self._values["port"] = port
        if visibility is not None:
            self._values["visibility"] = visibility

    @builtins.property
    def on_open(self) -> typing.Optional[GitpodOnOpen]:
        '''(experimental) What to do when a service on a port is detected.

        :default: GitpodOnOpen.NOTIFY

        :stability: experimental
        '''
        result = self._values.get("on_open")
        return typing.cast(typing.Optional[GitpodOnOpen], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''(experimental) A port that should be exposed (forwarded) from the container.

        :stability: experimental

        Example::

            "8080"
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visibility(self) -> typing.Optional["GitpodPortVisibility"]:
        '''(experimental) Whether the port visibility should be private or public.

        :default: GitpodPortVisibility.PUBLIC

        :stability: experimental
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional["GitpodPortVisibility"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitpodPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.GitpodPortVisibility")
class GitpodPortVisibility(enum.Enum):
    '''(experimental) Whether the port visibility should be private or public.

    :stability: experimental
    '''

    PUBLIC = "PUBLIC"
    '''(experimental) Allows everyone with the port URL to access the port (default).

    :stability: experimental
    '''
    PRIVATE = "PRIVATE"
    '''(experimental) Only allows users with workspace access to access the port.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.GitpodPrebuilds",
    jsii_struct_bases=[],
    name_mapping={
        "add_badge": "addBadge",
        "add_check": "addCheck",
        "add_comment": "addComment",
        "add_label": "addLabel",
        "branches": "branches",
        "master": "master",
        "pull_requests": "pullRequests",
        "pull_requests_from_forks": "pullRequestsFromForks",
    },
)
class GitpodPrebuilds:
    def __init__(
        self,
        *,
        add_badge: typing.Optional[builtins.bool] = None,
        add_check: typing.Optional[builtins.bool] = None,
        add_comment: typing.Optional[builtins.bool] = None,
        add_label: typing.Optional[builtins.bool] = None,
        branches: typing.Optional[builtins.bool] = None,
        master: typing.Optional[builtins.bool] = None,
        pull_requests: typing.Optional[builtins.bool] = None,
        pull_requests_from_forks: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Configure the Gitpod App for prebuilds.

        Currently only GitHub is supported.

        :param add_badge: (experimental) Add a "Review in Gitpod" button to the pull request's description. Default: false
        :param add_check: (experimental) Add a check to pull requests. Default: true
        :param add_comment: (experimental) Add a "Review in Gitpod" button as a comment to pull requests. Default: false
        :param add_label: (experimental) Add a label once the prebuild is ready to pull requests. Default: false
        :param branches: (experimental) Enable for all branches in this repo. Default: false
        :param master: (experimental) Enable for the master/default branch. Default: true
        :param pull_requests: (experimental) Enable for pull requests coming from this repo. Default: true
        :param pull_requests_from_forks: (experimental) Enable for pull requests coming from forks. Default: false

        :see: https://www.gitpod.io/docs/prebuilds/
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfddb6f340c3ec20dde7739d66b44371874cbaaec9fdcfe18d77679879dcd633)
            check_type(argname="argument add_badge", value=add_badge, expected_type=type_hints["add_badge"])
            check_type(argname="argument add_check", value=add_check, expected_type=type_hints["add_check"])
            check_type(argname="argument add_comment", value=add_comment, expected_type=type_hints["add_comment"])
            check_type(argname="argument add_label", value=add_label, expected_type=type_hints["add_label"])
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument master", value=master, expected_type=type_hints["master"])
            check_type(argname="argument pull_requests", value=pull_requests, expected_type=type_hints["pull_requests"])
            check_type(argname="argument pull_requests_from_forks", value=pull_requests_from_forks, expected_type=type_hints["pull_requests_from_forks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_badge is not None:
            self._values["add_badge"] = add_badge
        if add_check is not None:
            self._values["add_check"] = add_check
        if add_comment is not None:
            self._values["add_comment"] = add_comment
        if add_label is not None:
            self._values["add_label"] = add_label
        if branches is not None:
            self._values["branches"] = branches
        if master is not None:
            self._values["master"] = master
        if pull_requests is not None:
            self._values["pull_requests"] = pull_requests
        if pull_requests_from_forks is not None:
            self._values["pull_requests_from_forks"] = pull_requests_from_forks

    @builtins.property
    def add_badge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a "Review in Gitpod" button to the pull request's description.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("add_badge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def add_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a check to pull requests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("add_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def add_comment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a "Review in Gitpod" button as a comment to pull requests.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("add_comment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def add_label(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add a label once the prebuild is ready to pull requests.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("add_label")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def branches(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable for all branches in this repo.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def master(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable for the master/default branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("master")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_requests(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable for pull requests coming from this repo.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_requests")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_requests_from_forks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable for pull requests coming from forks.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("pull_requests_from_forks")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitpodPrebuilds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.GitpodTask",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "before": "before",
        "init": "init",
        "name": "name",
        "open_in": "openIn",
        "open_mode": "openMode",
        "prebuild": "prebuild",
    },
)
class GitpodTask:
    def __init__(
        self,
        *,
        command: builtins.str,
        before: typing.Optional[builtins.str] = None,
        init: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        open_in: typing.Optional[GitpodOpenIn] = None,
        open_mode: typing.Optional[GitpodOpenMode] = None,
        prebuild: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configure options for a task to be run when opening a Gitpod workspace (e.g. running tests, or starting a dev server).

        Start Mode         | Execution
        Fresh Workspace    | before && init && command
        Restart Workspace  | before && command
        Snapshot           | before && command
        Prebuild           | before && init && prebuild

        :param command: (experimental) Required. The shell command to run
        :param before: (experimental) In case you need to run something even before init, that is a requirement for both init and command, you can use the before property.
        :param init: (experimental) The init property can be used to specify shell commands that should only be executed after a workspace was freshly cloned and needs to be initialized somehow. Such tasks are usually builds or downloading dependencies. Anything you only want to do once but not when you restart a workspace or start a snapshot.
        :param name: (experimental) A name for this task. Default: - task names are omitted when blank
        :param open_in: (experimental) You can configure where in the IDE the terminal should be opened. Default: GitpodOpenIn.BOTTOM
        :param open_mode: (experimental) You can configure how the terminal should be opened relative to the previous task. Default: GitpodOpenMode.TAB_AFTER
        :param prebuild: (experimental) The optional prebuild command will be executed during prebuilds. It is meant to run additional long running processes that could be useful, e.g. running test suites.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d426769565bcc27ed394b810bb714ce1978791cfb7442339934c10d450d2ea)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument before", value=before, expected_type=type_hints["before"])
            check_type(argname="argument init", value=init, expected_type=type_hints["init"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument open_in", value=open_in, expected_type=type_hints["open_in"])
            check_type(argname="argument open_mode", value=open_mode, expected_type=type_hints["open_mode"])
            check_type(argname="argument prebuild", value=prebuild, expected_type=type_hints["prebuild"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "command": command,
        }
        if before is not None:
            self._values["before"] = before
        if init is not None:
            self._values["init"] = init
        if name is not None:
            self._values["name"] = name
        if open_in is not None:
            self._values["open_in"] = open_in
        if open_mode is not None:
            self._values["open_mode"] = open_mode
        if prebuild is not None:
            self._values["prebuild"] = prebuild

    @builtins.property
    def command(self) -> builtins.str:
        '''(experimental) Required.

        The shell command to run

        :stability: experimental
        '''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def before(self) -> typing.Optional[builtins.str]:
        '''(experimental) In case you need to run something even before init, that is a requirement for both init and command, you can use the before property.

        :stability: experimental
        '''
        result = self._values.get("before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def init(self) -> typing.Optional[builtins.str]:
        '''(experimental) The init property can be used to specify shell commands that should only be executed after a workspace was freshly cloned and needs to be initialized somehow.

        Such tasks are usually builds or downloading
        dependencies. Anything you only want to do once but not when you restart a workspace or start a snapshot.

        :stability: experimental
        '''
        result = self._values.get("init")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for this task.

        :default: - task names are omitted when blank

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_in(self) -> typing.Optional[GitpodOpenIn]:
        '''(experimental) You can configure where in the IDE the terminal should be opened.

        :default: GitpodOpenIn.BOTTOM

        :stability: experimental
        '''
        result = self._values.get("open_in")
        return typing.cast(typing.Optional[GitpodOpenIn], result)

    @builtins.property
    def open_mode(self) -> typing.Optional[GitpodOpenMode]:
        '''(experimental) You can configure how the terminal should be opened relative to the previous task.

        :default: GitpodOpenMode.TAB_AFTER

        :stability: experimental
        '''
        result = self._values.get("open_mode")
        return typing.cast(typing.Optional[GitpodOpenMode], result)

    @builtins.property
    def prebuild(self) -> typing.Optional[builtins.str]:
        '''(experimental) The optional prebuild command will be executed during prebuilds.

        It is meant to run additional long running
        processes that could be useful, e.g. running test suites.

        :stability: experimental
        '''
        result = self._values.get("prebuild")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitpodTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.GroupRunnerOptions",
    jsii_struct_bases=[],
    name_mapping={"group": "group", "labels": "labels"},
)
class GroupRunnerOptions:
    def __init__(
        self,
        *,
        group: builtins.str,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param group: 
        :param labels: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3547c7b706a8285f987ddb1847fd162ec961a77abbdd5059da647f1ac25f470)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
        }
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def group(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRunnerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="projen.ICompareString")
class ICompareString(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="compare")
    def compare(self, a: builtins.str, b: builtins.str) -> jsii.Number:
        '''
        :param a: The first string.
        :param b: The second string.

        :return: It is expected to return a negative value if the first argument is less than the second argument, zero if they're equal, and a positive value otherwise.

        :stability: experimental
        '''
        ...


class _ICompareStringProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.ICompareString"

    @jsii.member(jsii_name="compare")
    def compare(self, a: builtins.str, b: builtins.str) -> jsii.Number:
        '''
        :param a: The first string.
        :param b: The second string.

        :return: It is expected to return a negative value if the first argument is less than the second argument, zero if they're equal, and a positive value otherwise.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d4f6e150362668f5e26d2f58f8b0a32cff82cf2eb8cb736d2c4333d0b01d09)
            check_type(argname="argument a", value=a, expected_type=type_hints["a"])
            check_type(argname="argument b", value=b, expected_type=type_hints["b"])
        return typing.cast(jsii.Number, jsii.invoke(self, "compare", [a, b]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICompareString).__jsii_proxy_class__ = lambda : _ICompareStringProxy


@jsii.interface(jsii_type="projen.IDevEnvironment")
class IDevEnvironment(typing_extensions.Protocol):
    '''(experimental) Abstract interface for container-based development environments, such as Gitpod and GitHub Codespaces.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addDockerImage")
    def add_docker_image(self, image: DevEnvironmentDockerImage) -> None:
        '''(experimental) Add a custom Docker image or Dockerfile for the container.

        :param image: The Docker image.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addPorts")
    def add_ports(self, *ports: builtins.str) -> None:
        '''(experimental) Adds ports that should be exposed (forwarded) from the container.

        :param ports: The new ports.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addTasks")
    def add_tasks(self, *tasks: "Task") -> None:
        '''(experimental) Adds tasks to run when the container starts.

        :param tasks: The new tasks.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addVscodeExtensions")
    def add_vscode_extensions(self, *extensions: builtins.str) -> None:
        '''(experimental) Adds a list of VSCode extensions that should be automatically installed in the container.

        :param extensions: The extension IDs.

        :stability: experimental
        '''
        ...


class _IDevEnvironmentProxy:
    '''(experimental) Abstract interface for container-based development environments, such as Gitpod and GitHub Codespaces.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.IDevEnvironment"

    @jsii.member(jsii_name="addDockerImage")
    def add_docker_image(self, image: DevEnvironmentDockerImage) -> None:
        '''(experimental) Add a custom Docker image or Dockerfile for the container.

        :param image: The Docker image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2360e8cae8e57d0e5268d03b1ee0bcf2a5d56c20a3ca26e5369ddc34c43f0ff)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast(None, jsii.invoke(self, "addDockerImage", [image]))

    @jsii.member(jsii_name="addPorts")
    def add_ports(self, *ports: builtins.str) -> None:
        '''(experimental) Adds ports that should be exposed (forwarded) from the container.

        :param ports: The new ports.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045b7fd6b76288f0b95afa207abe899f8baf55cb8bbf6f5d5306b834adb6244e)
            check_type(argname="argument ports", value=ports, expected_type=typing.Tuple[type_hints["ports"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPorts", [*ports]))

    @jsii.member(jsii_name="addTasks")
    def add_tasks(self, *tasks: "Task") -> None:
        '''(experimental) Adds tasks to run when the container starts.

        :param tasks: The new tasks.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0813a7f75b96f7af7cfae60ea14d64e5cb791fa66c8518a184cb1c4ff60850d6)
            check_type(argname="argument tasks", value=tasks, expected_type=typing.Tuple[type_hints["tasks"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addTasks", [*tasks]))

    @jsii.member(jsii_name="addVscodeExtensions")
    def add_vscode_extensions(self, *extensions: builtins.str) -> None:
        '''(experimental) Adds a list of VSCode extensions that should be automatically installed in the container.

        :param extensions: The extension IDs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782f22994379ab8e59a7f43c2c152f03c7007b57a33bc0e64d609ae60dcc3e6b)
            check_type(argname="argument extensions", value=extensions, expected_type=typing.Tuple[type_hints["extensions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addVscodeExtensions", [*extensions]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDevEnvironment).__jsii_proxy_class__ = lambda : _IDevEnvironmentProxy


@jsii.interface(jsii_type="projen.IDockerComposeNetworkBinding")
class IDockerComposeNetworkBinding(typing_extensions.Protocol):
    '''(experimental) Network binding information.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, network_config: "IDockerComposeNetworkConfig") -> builtins.str:
        '''(experimental) Binds the requested network to the docker-compose network configuration and provide mounting instructions for synthesis.

        :param network_config: the network configuration.

        :return: the service name

        :stability: experimental
        '''
        ...


class _IDockerComposeNetworkBindingProxy:
    '''(experimental) Network binding information.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.IDockerComposeNetworkBinding"

    @jsii.member(jsii_name="bind")
    def bind(self, network_config: "IDockerComposeNetworkConfig") -> builtins.str:
        '''(experimental) Binds the requested network to the docker-compose network configuration and provide mounting instructions for synthesis.

        :param network_config: the network configuration.

        :return: the service name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacadabdf1607bf647ddf49c98b96c3cf16b7b3d040c9b172601097c88063780)
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
        return typing.cast(builtins.str, jsii.invoke(self, "bind", [network_config]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerComposeNetworkBinding).__jsii_proxy_class__ = lambda : _IDockerComposeNetworkBindingProxy


@jsii.interface(jsii_type="projen.IDockerComposeNetworkConfig")
class IDockerComposeNetworkConfig(typing_extensions.Protocol):
    '''(experimental) Storage for network configuration.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addNetworkConfiguration")
    def add_network_configuration(
        self,
        network_name: builtins.str,
        *,
        attachable: typing.Optional[builtins.bool] = None,
        bridge: typing.Optional[builtins.bool] = None,
        driver: typing.Optional[builtins.str] = None,
        driver_opts: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
        external: typing.Optional[builtins.bool] = None,
        internal: typing.Optional[builtins.bool] = None,
        ipam: typing.Optional[typing.Union[DockerComposeNetworkIpamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        overlay: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Add network configuration to the repository.

        :param network_name: -
        :param attachable: (experimental) Set to true to indicate that standalone containers can attach to this network, in addition to services. Default: - unset
        :param bridge: (experimental) Set to true to indicate that the network is a bridge network. Default: - unset
        :param driver: (experimental) Driver to use for the network. Default: - value is not provided
        :param driver_opts: (experimental) Options for the configured driver. Those options are driver-dependent - consult the driver’s documentation for more information Default: - value is not provided
        :param external: (experimental) Set to true to indicate that the network is externally created. Default: - unset, indicating that docker-compose creates the network
        :param internal: (experimental) Set to true to indicate that you want to create an externally isolated overlay network. Default: - unset
        :param ipam: (experimental) Specify custom IPAM config. Default: - unset
        :param labels: (experimental) Attach labels to the network. Default: - unset
        :param name: (experimental) Name of the network for when the network name isn't going to work in YAML. Default: - unset, indicating that docker-compose creates networks as usual
        :param overlay: (experimental) Set to true to indicate that the network is an overlay network. Default: - unset

        :stability: experimental
        '''
        ...


class _IDockerComposeNetworkConfigProxy:
    '''(experimental) Storage for network configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.IDockerComposeNetworkConfig"

    @jsii.member(jsii_name="addNetworkConfiguration")
    def add_network_configuration(
        self,
        network_name: builtins.str,
        *,
        attachable: typing.Optional[builtins.bool] = None,
        bridge: typing.Optional[builtins.bool] = None,
        driver: typing.Optional[builtins.str] = None,
        driver_opts: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
        external: typing.Optional[builtins.bool] = None,
        internal: typing.Optional[builtins.bool] = None,
        ipam: typing.Optional[typing.Union[DockerComposeNetworkIpamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        overlay: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Add network configuration to the repository.

        :param network_name: -
        :param attachable: (experimental) Set to true to indicate that standalone containers can attach to this network, in addition to services. Default: - unset
        :param bridge: (experimental) Set to true to indicate that the network is a bridge network. Default: - unset
        :param driver: (experimental) Driver to use for the network. Default: - value is not provided
        :param driver_opts: (experimental) Options for the configured driver. Those options are driver-dependent - consult the driver’s documentation for more information Default: - value is not provided
        :param external: (experimental) Set to true to indicate that the network is externally created. Default: - unset, indicating that docker-compose creates the network
        :param internal: (experimental) Set to true to indicate that you want to create an externally isolated overlay network. Default: - unset
        :param ipam: (experimental) Specify custom IPAM config. Default: - unset
        :param labels: (experimental) Attach labels to the network. Default: - unset
        :param name: (experimental) Name of the network for when the network name isn't going to work in YAML. Default: - unset, indicating that docker-compose creates networks as usual
        :param overlay: (experimental) Set to true to indicate that the network is an overlay network. Default: - unset

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f2d0ced589fcb3b848c0452b8213c14d612654118bc3fabd4a9aacb71c2104)
            check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
        configuration = DockerComposeNetworkConfig(
            attachable=attachable,
            bridge=bridge,
            driver=driver,
            driver_opts=driver_opts,
            external=external,
            internal=internal,
            ipam=ipam,
            labels=labels,
            name=name,
            overlay=overlay,
        )

        return typing.cast(None, jsii.invoke(self, "addNetworkConfiguration", [network_name, configuration]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerComposeNetworkConfig).__jsii_proxy_class__ = lambda : _IDockerComposeNetworkConfigProxy


@jsii.interface(jsii_type="projen.IDockerComposeServiceName")
class IDockerComposeServiceName(typing_extensions.Protocol):
    '''(experimental) An interface providing the name of a docker compose service.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) The name of the docker compose service.

        :stability: experimental
        '''
        ...


class _IDockerComposeServiceNameProxy:
    '''(experimental) An interface providing the name of a docker compose service.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.IDockerComposeServiceName"

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) The name of the docker compose service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerComposeServiceName).__jsii_proxy_class__ = lambda : _IDockerComposeServiceNameProxy


@jsii.interface(jsii_type="projen.IDockerComposeVolumeBinding")
class IDockerComposeVolumeBinding(typing_extensions.Protocol):
    '''(experimental) Volume binding information.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        volume_config: "IDockerComposeVolumeConfig",
    ) -> DockerComposeVolumeMount:
        '''(experimental) Binds the requested volume to the docker-compose volume configuration and provide mounting instructions for synthesis.

        :param volume_config: the volume configuration.

        :return: mounting instructions for the service.

        :stability: experimental
        '''
        ...


class _IDockerComposeVolumeBindingProxy:
    '''(experimental) Volume binding information.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.IDockerComposeVolumeBinding"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        volume_config: "IDockerComposeVolumeConfig",
    ) -> DockerComposeVolumeMount:
        '''(experimental) Binds the requested volume to the docker-compose volume configuration and provide mounting instructions for synthesis.

        :param volume_config: the volume configuration.

        :return: mounting instructions for the service.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8af3d4004c43777e3011a6152f90de4dca16d54781e5922335decd658cd9f63)
            check_type(argname="argument volume_config", value=volume_config, expected_type=type_hints["volume_config"])
        return typing.cast(DockerComposeVolumeMount, jsii.invoke(self, "bind", [volume_config]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerComposeVolumeBinding).__jsii_proxy_class__ = lambda : _IDockerComposeVolumeBindingProxy


@jsii.interface(jsii_type="projen.IDockerComposeVolumeConfig")
class IDockerComposeVolumeConfig(typing_extensions.Protocol):
    '''(experimental) Storage for volume configuration.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addVolumeConfiguration")
    def add_volume_configuration(
        self,
        volume_name: builtins.str,
        *,
        driver: typing.Optional[builtins.str] = None,
        driver_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        external: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add volume configuration to the repository.

        :param volume_name: -
        :param driver: (experimental) Driver to use for the volume. Default: - value is not provided
        :param driver_opts: (experimental) Options to provide to the driver.
        :param external: (experimental) Set to true to indicate that the volume is externally created. Default: - unset, indicating that docker-compose creates the volume
        :param name: (experimental) Name of the volume for when the volume name isn't going to work in YAML. Default: - unset, indicating that docker-compose creates volumes as usual

        :stability: experimental
        '''
        ...


class _IDockerComposeVolumeConfigProxy:
    '''(experimental) Storage for volume configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.IDockerComposeVolumeConfig"

    @jsii.member(jsii_name="addVolumeConfiguration")
    def add_volume_configuration(
        self,
        volume_name: builtins.str,
        *,
        driver: typing.Optional[builtins.str] = None,
        driver_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        external: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add volume configuration to the repository.

        :param volume_name: -
        :param driver: (experimental) Driver to use for the volume. Default: - value is not provided
        :param driver_opts: (experimental) Options to provide to the driver.
        :param external: (experimental) Set to true to indicate that the volume is externally created. Default: - unset, indicating that docker-compose creates the volume
        :param name: (experimental) Name of the volume for when the volume name isn't going to work in YAML. Default: - unset, indicating that docker-compose creates volumes as usual

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e90cd0baeb3ebbbc34ba2bb279b321337ba3f5a9a97871b5285980fa5ff8f8a)
            check_type(argname="argument volume_name", value=volume_name, expected_type=type_hints["volume_name"])
        configuration = DockerComposeVolumeConfig(
            driver=driver, driver_opts=driver_opts, external=external, name=name
        )

        return typing.cast(None, jsii.invoke(self, "addVolumeConfiguration", [volume_name, configuration]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDockerComposeVolumeConfig).__jsii_proxy_class__ = lambda : _IDockerComposeVolumeConfigProxy


@jsii.interface(jsii_type="projen.IResolvable")
class IResolvable(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        '''(experimental) Resolves and returns content.

        :stability: experimental
        '''
        ...


class _IResolvableProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.IResolvable"

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        '''(experimental) Resolves and returns content.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toJSON", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResolvable).__jsii_proxy_class__ = lambda : _IResolvableProxy


@jsii.interface(jsii_type="projen.IResolver")
class IResolver(typing_extensions.Protocol):
    '''(experimental) API for resolving tokens when synthesizing file content.

    :stability: experimental
    '''

    @jsii.member(jsii_name="resolve")
    def resolve(
        self,
        value: typing.Any,
        *,
        args: typing.Optional[typing.Sequence[typing.Any]] = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> typing.Any:
        '''(experimental) Given a value (object/string/array/whatever, looks up any functions inside the object and returns an object where all functions are called.

        :param value: The value to resolve.
        :param args: (experimental) Context arguments. Default: []
        :param omit_empty: (experimental) Omits empty arrays and objects. Default: false

        :stability: experimental
        :package: options Resolve options
        '''
        ...


class _IResolverProxy:
    '''(experimental) API for resolving tokens when synthesizing file content.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "projen.IResolver"

    @jsii.member(jsii_name="resolve")
    def resolve(
        self,
        value: typing.Any,
        *,
        args: typing.Optional[typing.Sequence[typing.Any]] = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> typing.Any:
        '''(experimental) Given a value (object/string/array/whatever, looks up any functions inside the object and returns an object where all functions are called.

        :param value: The value to resolve.
        :param args: (experimental) Context arguments. Default: []
        :param omit_empty: (experimental) Omits empty arrays and objects. Default: false

        :stability: experimental
        :package: options Resolve options
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fe3f80ba2709a778dd1c7b2c05be66e2342a0284f2ddb2216485cc3fe83203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        options = ResolveOptions(args=args, omit_empty=omit_empty)

        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [value, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResolver).__jsii_proxy_class__ = lambda : _IResolverProxy


class IgnoreFile(FileBase, metaclass=jsii.JSIIMeta, jsii_type="projen.IgnoreFile"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        project: "Project",
        file_path: builtins.str,
        *,
        filter_comment_lines: typing.Optional[builtins.bool] = None,
        filter_empty_lines: typing.Optional[builtins.bool] = None,
        ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project: The project to tie this file to.
        :param file_path: - the relative path in the project to put the file.
        :param filter_comment_lines: (experimental) Filter out comment lines? Default: true
        :param filter_empty_lines: (experimental) Filter out blank/empty lines? Default: true
        :param ignore_patterns: (experimental) Patterns to add to the ignore file. Default: []

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b3d1a5dbba38c978da9c5c4f4aab9b9f4b93375021ee84f57a823093ef8c94)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = IgnoreFileOptions(
            filter_comment_lines=filter_comment_lines,
            filter_empty_lines=filter_empty_lines,
            ignore_patterns=ignore_patterns,
        )

        jsii.create(self.__class__, self, [project, file_path, options])

    @jsii.member(jsii_name="addPatterns")
    def add_patterns(self, *patterns: builtins.str) -> None:
        '''(experimental) Add ignore patterns.

        Files that match this pattern will be ignored. If the
        pattern starts with a negation mark ``!``, files that match will *not* be
        ignored.

        Comment lines (start with ``#``) and blank lines ("") are filtered by default
        but can be included using options specified when instantiating the component.

        :param patterns: Ignore patterns.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b1c017f8ecb0e1f37e2212d87d1a1f29ebc301dd9acca79bee88038d4ef761)
            check_type(argname="argument patterns", value=patterns, expected_type=typing.Tuple[type_hints["patterns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPatterns", [*patterns]))

    @jsii.member(jsii_name="exclude")
    def exclude(self, *patterns: builtins.str) -> None:
        '''(experimental) Ignore the files that match these patterns.

        :param patterns: The patterns to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b410ec26b2ad71a13a61473568b66bc67bf1526bb5a2c5808dec083cbf6176b)
            check_type(argname="argument patterns", value=patterns, expected_type=typing.Tuple[type_hints["patterns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "exclude", [*patterns]))

    @jsii.member(jsii_name="include")
    def include(self, *patterns: builtins.str) -> None:
        '''(experimental) Always include the specified file patterns.

        :param patterns: Patterns to include in git commits.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f4e7958134162324e6e69409537fa18465875eba5b7deb29f1d004349e6e62)
            check_type(argname="argument patterns", value=patterns, expected_type=typing.Tuple[type_hints["patterns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "include", [*patterns]))

    @jsii.member(jsii_name="removePatterns")
    def remove_patterns(self, *patterns: builtins.str) -> None:
        '''(experimental) Removes patterns previously added from the ignore file.

        If ``addPattern()`` is called after this, the pattern will be added again.

        :param patterns: patters to remove.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51b5c0b61cdaa2626f46d818be442ab87c3c27477531c08d9cf19b782c8dce1)
            check_type(argname="argument patterns", value=patterns, expected_type=typing.Tuple[type_hints["patterns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "removePatterns", [*patterns]))

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, resolver: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853a0f02c9c0f2c598ef8ff7dc57847ef984a42d6d8420b86e11870eb0c92e2d)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))

    @builtins.property
    @jsii.member(jsii_name="filterCommentLines")
    def filter_comment_lines(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "filterCommentLines"))

    @builtins.property
    @jsii.member(jsii_name="filterEmptyLines")
    def filter_empty_lines(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "filterEmptyLines"))


@jsii.data_type(
    jsii_type="projen.IgnoreFileOptions",
    jsii_struct_bases=[],
    name_mapping={
        "filter_comment_lines": "filterCommentLines",
        "filter_empty_lines": "filterEmptyLines",
        "ignore_patterns": "ignorePatterns",
    },
)
class IgnoreFileOptions:
    def __init__(
        self,
        *,
        filter_comment_lines: typing.Optional[builtins.bool] = None,
        filter_empty_lines: typing.Optional[builtins.bool] = None,
        ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param filter_comment_lines: (experimental) Filter out comment lines? Default: true
        :param filter_empty_lines: (experimental) Filter out blank/empty lines? Default: true
        :param ignore_patterns: (experimental) Patterns to add to the ignore file. Default: []

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7852fd5d8f0daa6070394e45fe4fcb7845e6838dc40a3e3475c057712f4209b9)
            check_type(argname="argument filter_comment_lines", value=filter_comment_lines, expected_type=type_hints["filter_comment_lines"])
            check_type(argname="argument filter_empty_lines", value=filter_empty_lines, expected_type=type_hints["filter_empty_lines"])
            check_type(argname="argument ignore_patterns", value=ignore_patterns, expected_type=type_hints["ignore_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_comment_lines is not None:
            self._values["filter_comment_lines"] = filter_comment_lines
        if filter_empty_lines is not None:
            self._values["filter_empty_lines"] = filter_empty_lines
        if ignore_patterns is not None:
            self._values["ignore_patterns"] = ignore_patterns

    @builtins.property
    def filter_comment_lines(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Filter out comment lines?

        :default: true

        :stability: experimental
        '''
        result = self._values.get("filter_comment_lines")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def filter_empty_lines(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Filter out blank/empty lines?

        :default: true

        :stability: experimental
        '''
        result = self._values.get("filter_empty_lines")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Patterns to add to the ignore file.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("ignore_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IgnoreFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.InitProject",
    jsii_struct_bases=[],
    name_mapping={
        "args": "args",
        "comments": "comments",
        "fqn": "fqn",
        "type": "type",
    },
)
class InitProject:
    def __init__(
        self,
        *,
        args: typing.Mapping[builtins.str, typing.Any],
        comments: "InitProjectOptionHints",
        fqn: builtins.str,
        type: "ProjectType",
    ) -> None:
        '''(experimental) Information passed from ``projen new`` to the project object when the project is first created.

        It is used to generate projenrc files in various languages.

        :param args: (experimental) Initial arguments passed to ``projen new``.
        :param comments: (experimental) Include commented out options. Does not apply to projenrc.json files. Default: InitProjectOptionHints.FEATURED
        :param fqn: (experimental) The JSII FQN of the project type.
        :param type: (experimental) Project metadata.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e857a70558d977f23eac6a7f43184bde159ec35b45b301dd96f1d6b8649cee)
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument comments", value=comments, expected_type=type_hints["comments"])
            check_type(argname="argument fqn", value=fqn, expected_type=type_hints["fqn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "args": args,
            "comments": comments,
            "fqn": fqn,
            "type": type,
        }

    @builtins.property
    def args(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Initial arguments passed to ``projen new``.

        :stability: experimental
        '''
        result = self._values.get("args")
        assert result is not None, "Required property 'args' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def comments(self) -> "InitProjectOptionHints":
        '''(experimental) Include commented out options.

        Does not apply to projenrc.json files.

        :default: InitProjectOptionHints.FEATURED

        :stability: experimental
        '''
        result = self._values.get("comments")
        assert result is not None, "Required property 'comments' is missing"
        return typing.cast("InitProjectOptionHints", result)

    @builtins.property
    def fqn(self) -> builtins.str:
        '''(experimental) The JSII FQN of the project type.

        :stability: experimental
        '''
        result = self._values.get("fqn")
        assert result is not None, "Required property 'fqn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "ProjectType":
        '''(experimental) Project metadata.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ProjectType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InitProject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.InitProjectOptionHints")
class InitProjectOptionHints(enum.Enum):
    '''(experimental) Choices for how to display commented out options in projenrc files.

    Does not apply to projenrc.json files.

    :stability: experimental
    '''

    ALL = "ALL"
    '''(experimental) Display all possible options (grouped by which interface they belong to).

    :stability: experimental
    '''
    FEATURED = "FEATURED"
    '''(experimental) Display only featured options, in alphabetical order.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) Display no extra options.

    :stability: experimental
    '''


class JsonPatch(metaclass=jsii.JSIIMeta, jsii_type="projen.JsonPatch"):
    '''(experimental) Utility for applying RFC-6902 JSON-Patch to a document.

    Use the the ``JsonPatch.apply(doc, ...ops)`` function to apply a set of
    operations to a JSON document and return the result.

    Operations can be created using the factory methods ``JsonPatch.add()``,
    ``JsonPatch.remove()``, etc.

    :stability: experimental

    Example::

        const output = JsonPatch.apply(input,
         JsonPatch.replace('/world/hi/there', 'goodbye'),
         JsonPatch.add('/world/foo/', 'boom'),
         JsonPatch.remove('/hello'));
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

            JsonPatch.add('/biscuits/1', { "name": "Ginger Nut" })
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b26148dd49d145c4677c52d5151e359846fa4531669d51a3bda7fc9690796f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__687d6c08b41e458d121dbe119e3027eab184190021ccd1e7214fe36dc5ec3d0e)
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

            JsonPatch.copy('/biscuits/0', '/best_biscuit')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e382fed98c69b93f0f597e0b66813e26de9d104dbe3bbe734ef8b43fc6f6ef8e)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "copy", [from_, path]))

    @jsii.member(jsii_name="escapePath")
    @builtins.classmethod
    def escape_path(cls, path: builtins.str) -> builtins.str:
        '''(experimental) Escapes a json pointer path.

        :param path: The raw pointer.

        :return: the Escaped path

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4681b9d716a24a6f5756f57d016e6a0933b4e756c34f3c611bb58e46658c08a1)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "escapePath", [path]))

    @jsii.member(jsii_name="move")
    @builtins.classmethod
    def move(cls, from_: builtins.str, path: builtins.str) -> "JsonPatch":
        '''(experimental) Moves a value from one location to the other.

        Both from and path are JSON Pointers.

        :param from_: -
        :param path: -

        :stability: experimental

        Example::

            JsonPatch.move('/biscuits', '/cookies')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2e9da81715d26de45b5095bc71cb7c0b40808d8ac54980865598b8d6ba1f7b)
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

            JsonPatch.remove('/biscuits/0')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab38d0d4724594f77c44941ab64081b36f9403cc791b13fff2eb1e1e4fe51d1d)
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

            JsonPatch.replace('/biscuits/0/name', 'Chocolate Digestive')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224b5820566457e2e1a5dc60523684f65c081c466561e141aa7a29c5d5058e75)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "replace", [path, value]))

    @jsii.member(jsii_name="test")
    @builtins.classmethod
    def test(
        cls,
        path: builtins.str,
        value: typing.Any,
        failure_behavior: typing.Optional["TestFailureBehavior"] = None,
    ) -> "JsonPatch":
        '''(experimental) Tests that the specified value is set in the document.

        If the test fails,
        then the patch as a whole should not apply.

        :param path: -
        :param value: -
        :param failure_behavior: -

        :stability: experimental

        Example::

            JsonPatch.test('/best_biscuit/name', 'Choco Leibniz')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71ec8f8f1e51ef857d2c433c05eee7cbf90512a0f5cc61e4a5e15606593e0a0)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument failure_behavior", value=failure_behavior, expected_type=type_hints["failure_behavior"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "test", [path, value, failure_behavior]))


class License(FileBase, metaclass=jsii.JSIIMeta, jsii_type="projen.License"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        project: "Project",
        *,
        spdx: builtins.str,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param spdx: (experimental) License type (SPDX).
        :param copyright_owner: (experimental) Copyright owner. If the license text has $copyright_owner, this option must be specified. Default: -
        :param copyright_period: (experimental) Period of license (e.g. "1998-2023"). The string ``$copyright_period`` will be substituted with this string. Default: - current year (e.g. "2020")

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9eddbcb68700e35e97b98e5d8b6b5711cc6e2ed4f4f8504c3a3b32c09e21bc0)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = LicenseOptions(
            spdx=spdx,
            copyright_owner=copyright_owner,
            copyright_period=copyright_period,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, _: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param _: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfcc75bff8f37fa269835ada3b509dcfbadf621e3ed126a97c08a57ca6956a26)
            check_type(argname="argument _", value=_, expected_type=type_hints["_"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [_]))


@jsii.data_type(
    jsii_type="projen.LicenseOptions",
    jsii_struct_bases=[],
    name_mapping={
        "spdx": "spdx",
        "copyright_owner": "copyrightOwner",
        "copyright_period": "copyrightPeriod",
    },
)
class LicenseOptions:
    def __init__(
        self,
        *,
        spdx: builtins.str,
        copyright_owner: typing.Optional[builtins.str] = None,
        copyright_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param spdx: (experimental) License type (SPDX).
        :param copyright_owner: (experimental) Copyright owner. If the license text has $copyright_owner, this option must be specified. Default: -
        :param copyright_period: (experimental) Period of license (e.g. "1998-2023"). The string ``$copyright_period`` will be substituted with this string. Default: - current year (e.g. "2020")

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95797870e2d83245ce98c839bcaed08b3f74660f792b7401f353e9a8a2cc2e5)
            check_type(argname="argument spdx", value=spdx, expected_type=type_hints["spdx"])
            check_type(argname="argument copyright_owner", value=copyright_owner, expected_type=type_hints["copyright_owner"])
            check_type(argname="argument copyright_period", value=copyright_period, expected_type=type_hints["copyright_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "spdx": spdx,
        }
        if copyright_owner is not None:
            self._values["copyright_owner"] = copyright_owner
        if copyright_period is not None:
            self._values["copyright_period"] = copyright_period

    @builtins.property
    def spdx(self) -> builtins.str:
        '''(experimental) License type (SPDX).

        :see: https://github.com/projen/projen/tree/main/license-text for list of supported licenses
        :stability: experimental
        '''
        result = self._values.get("spdx")
        assert result is not None, "Required property 'spdx' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def copyright_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) Copyright owner.

        If the license text has $copyright_owner, this option must be specified.

        :default: -

        :stability: experimental
        '''
        result = self._values.get("copyright_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copyright_period(self) -> typing.Optional[builtins.str]:
        '''(experimental) Period of license (e.g. "1998-2023").

        The string ``$copyright_period`` will be substituted with this string.

        :default: - current year (e.g. "2020")

        :stability: experimental
        '''
        result = self._values.get("copyright_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LicenseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.LogLevel")
class LogLevel(enum.Enum):
    '''(experimental) Logging verbosity.

    :stability: experimental
    '''

    OFF = "OFF"
    '''
    :stability: experimental
    '''
    ERROR = "ERROR"
    '''
    :stability: experimental
    '''
    WARN = "WARN"
    '''
    :stability: experimental
    '''
    INFO = "INFO"
    '''
    :stability: experimental
    '''
    DEBUG = "DEBUG"
    '''
    :stability: experimental
    '''
    VERBOSE = "VERBOSE"
    '''
    :stability: experimental
    '''


class Logger(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.Logger"):
    '''(experimental) Project-level logging utilities.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        *,
        level: typing.Optional[LogLevel] = None,
        use_prefix: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param level: (experimental) The logging verbosity. The levels available (in increasing verbosity) are OFF, ERROR, WARN, INFO, DEBUG, and VERBOSE. Default: LogLevel.INFO
        :param use_prefix: (experimental) Include a prefix for all logging messages with the project name. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033691822a7f7c14e8198bce92b0c93718acf9caa771f8fb20be2afdca76198e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = LoggerOptions(level=level, use_prefix=use_prefix)

        jsii.create(self.__class__, self, [scope, options])

    @jsii.member(jsii_name="debug")
    def debug(self, *text: typing.Any) -> None:
        '''(experimental) Log a message to stderr with DEBUG severity.

        :param text: strings or objects to print.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9ac41cbd780d7354df3485a4d09a580048a756adf7658209e132d613e93955)
            check_type(argname="argument text", value=text, expected_type=typing.Tuple[type_hints["text"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "debug", [*text]))

    @jsii.member(jsii_name="error")
    def error(self, *text: typing.Any) -> None:
        '''(experimental) Log a message to stderr with ERROR severity.

        :param text: strings or objects to print.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab04da100771530f2dcbe37016ca4fd167dcccd81efef96fa9247ea2fc074aa)
            check_type(argname="argument text", value=text, expected_type=typing.Tuple[type_hints["text"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "error", [*text]))

    @jsii.member(jsii_name="info")
    def info(self, *text: typing.Any) -> None:
        '''(experimental) Log a message to stderr with INFO severity.

        :param text: strings or objects to print.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee83fd3f4ec98a5796ffacb4d4a25bc4de1ab8f597892f06001ac8bc9005dbf5)
            check_type(argname="argument text", value=text, expected_type=typing.Tuple[type_hints["text"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "info", [*text]))

    @jsii.member(jsii_name="log")
    def log(self, level: LogLevel, *text: typing.Any) -> None:
        '''(experimental) Log a message to stderr with a given logging level.

        The message will be
        printed as long as ``logger.level`` is set to the message's severity or higher.

        :param level: Logging verbosity.
        :param text: strings or objects to print.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3de9de18851453b814b6d4aa139849633e68925ada8b935856e8d2779645c4e)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument text", value=text, expected_type=typing.Tuple[type_hints["text"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "log", [level, *text]))

    @jsii.member(jsii_name="verbose")
    def verbose(self, *text: typing.Any) -> None:
        '''(experimental) Log a message to stderr with VERBOSE severity.

        :param text: strings or objects to print.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06099b369c462f751aad45c6281b342f061e97a9c63b50dde917bbe345b00f86)
            check_type(argname="argument text", value=text, expected_type=typing.Tuple[type_hints["text"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "verbose", [*text]))

    @jsii.member(jsii_name="warn")
    def warn(self, *text: typing.Any) -> None:
        '''(experimental) Log a message to stderr with WARN severity.

        :param text: strings or objects to print.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833d0f154731bea17dd1954f73c4261d00a48c89b4d8310e383a5320fc447d33)
            check_type(argname="argument text", value=text, expected_type=typing.Tuple[type_hints["text"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "warn", [*text]))


@jsii.data_type(
    jsii_type="projen.LoggerOptions",
    jsii_struct_bases=[],
    name_mapping={"level": "level", "use_prefix": "usePrefix"},
)
class LoggerOptions:
    def __init__(
        self,
        *,
        level: typing.Optional[LogLevel] = None,
        use_prefix: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for logging utilities.

        :param level: (experimental) The logging verbosity. The levels available (in increasing verbosity) are OFF, ERROR, WARN, INFO, DEBUG, and VERBOSE. Default: LogLevel.INFO
        :param use_prefix: (experimental) Include a prefix for all logging messages with the project name. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e039718de6580cbf9df271987ee9856640dfc3fbfffb9a8dd894f3c3836384)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument use_prefix", value=use_prefix, expected_type=type_hints["use_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if level is not None:
            self._values["level"] = level
        if use_prefix is not None:
            self._values["use_prefix"] = use_prefix

    @builtins.property
    def level(self) -> typing.Optional[LogLevel]:
        '''(experimental) The logging verbosity.

        The levels available (in increasing verbosity) are
        OFF, ERROR, WARN, INFO, DEBUG, and VERBOSE.

        :default: LogLevel.INFO

        :stability: experimental
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional[LogLevel], result)

    @builtins.property
    def use_prefix(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include a prefix for all logging messages with the project name.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("use_prefix")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Makefile(FileBase, metaclass=jsii.JSIIMeta, jsii_type="projen.Makefile"):
    '''(experimental) Minimal Makefile.

    :stability: experimental
    '''

    def __init__(
        self,
        project: "Project",
        file_path: builtins.str,
        *,
        all: typing.Optional[typing.Sequence[builtins.str]] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["Rule", typing.Dict[builtins.str, typing.Any]]]] = None,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param file_path: -
        :param all: (experimental) List of targets to build when Make is invoked without specifying any targets. Default: []
        :param rules: (experimental) Rules to include in the Makefile. Default: []
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d8810f927b1ecfbe0b204b373edfe8063aa41c3cc9b476e41d4c74edbf6640)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = MakefileOptions(
            all=all,
            rules=rules,
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [project, file_path, options])

    @jsii.member(jsii_name="addAll")
    def add_all(self, target: builtins.str) -> "Makefile":
        '''(experimental) Add a target to all.

        :param target: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0f2a9f8d0fba8ba4b866f8fae25c27378c12bac9210a7561d3bbc58209e5d0)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast("Makefile", jsii.invoke(self, "addAll", [target]))

    @jsii.member(jsii_name="addAlls")
    def add_alls(self, *targets: builtins.str) -> "Makefile":
        '''(experimental) Add multiple targets to all.

        :param targets: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8dca5ea305db0fd9fce16ffe45b1955f7f315de1bc4856adeb92af8ece2de1)
            check_type(argname="argument targets", value=targets, expected_type=typing.Tuple[type_hints["targets"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("Makefile", jsii.invoke(self, "addAlls", [*targets]))

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        *,
        targets: typing.Sequence[builtins.str],
        phony: typing.Optional[builtins.bool] = None,
        prerequisites: typing.Optional[typing.Sequence[builtins.str]] = None,
        recipe: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "Makefile":
        '''(experimental) Add a rule to the Makefile.

        :param targets: (experimental) Files to be created or updated by this rule. If the rule is phony then instead this represents the command's name(s).
        :param phony: (experimental) Marks whether the target is phony. Default: false
        :param prerequisites: (experimental) Files that are used as inputs to create a target. Default: []
        :param recipe: (experimental) Commands that are run (using prerequisites as inputs) to create a target. Default: []

        :stability: experimental
        '''
        rule = Rule(
            targets=targets, phony=phony, prerequisites=prerequisites, recipe=recipe
        )

        return typing.cast("Makefile", jsii.invoke(self, "addRule", [rule]))

    @jsii.member(jsii_name="addRules")
    def add_rules(self, *rules: "Rule") -> "Makefile":
        '''(experimental) Add multiple rules to the Makefile.

        :param rules: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697970c0228a6b747ebd5cf926e4e80e4ec842ca9a26b1dda7d6487e1d098c16)
            check_type(argname="argument rules", value=rules, expected_type=typing.Tuple[type_hints["rules"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("Makefile", jsii.invoke(self, "addRules", [*rules]))

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, resolver: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a3bfee1f24f1bc5e90733d58ecdf92315f7010947140287a5ec79b8a890121)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.List["Rule"]:
        '''(experimental) List of rule definitions.

        :stability: experimental
        '''
        return typing.cast(typing.List["Rule"], jsii.get(self, "rules"))


@jsii.data_type(
    jsii_type="projen.MakefileOptions",
    jsii_struct_bases=[FileBaseOptions],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
        "all": "all",
        "rules": "rules",
    },
)
class MakefileOptions(FileBaseOptions):
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
        all: typing.Optional[typing.Sequence[builtins.str]] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["Rule", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Options for Makefiles.

        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true
        :param all: (experimental) List of targets to build when Make is invoked without specifying any targets. Default: []
        :param rules: (experimental) Rules to include in the Makefile. Default: []

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2336c6183b3596358b6ceeacc7aa7df515fe983a38b754407952b9b0e0d1985)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly
        if all is not None:
            self._values["all"] = all
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def all(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of targets to build when Make is invoked without specifying any targets.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["Rule"]]:
        '''(experimental) Rules to include in the Makefile.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["Rule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MakefileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObjectFile(
    FileBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="projen.ObjectFile",
):
    '''(experimental) Represents an Object file.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        file_path: builtins.str,
        *,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param file_path: -
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc9aaaac91e385d130a0db14291a598781f43147b9af4a5fdc21398a4bb12e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = ObjectFileOptions(
            obj=obj,
            omit_empty=omit_empty,
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [scope, file_path, options])

    @jsii.member(jsii_name="addDeletionOverride")
    def add_deletion_override(self, path: builtins.str) -> None:
        '''(experimental) Syntactic sugar for ``addOverride(path, undefined)``.

        :param path: The path of the value to delete.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a738f516b6642d1f5778bc860131390ad6f6d356c899ebcf8aee547c7d46a0e7)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.invoke(self, "addDeletionOverride", [path]))

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: builtins.str, value: typing.Any) -> None:
        '''(experimental) Adds an override to the synthesized object file.

        If the override is nested, separate each nested level using a dot (.) in the path parameter.
        If there is an array as part of the nesting, specify the index in the path.

        To include a literal ``.`` in the property name, prefix with a ``\\``. In most
        programming languages you will need to write this as ``"\\\\."`` because the
        ``\\`` itself will need to be escaped.

        For example::

           project.tsconfig.file.addOverride('compilerOptions.alwaysStrict', true);
           project.tsconfig.file.addOverride('compilerOptions.lib', ['dom', 'dom.iterable', 'esnext']);

        would add the overrides Example::

           "compilerOptions": {
             "alwaysStrict": true,
             "lib": [
               "dom",
               "dom.iterable",
               "esnext"
             ]
             ...
           }
           ...

        :param path: - The path of the property, you can use dot notation to override values in complex types. Any intermediate keys will be created as needed.
        :param value: - The value. Could be primitive or complex.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f433242148406c79a8d4d5b0d92a5860a905eff4ee62e43d6ba3e0ee996c9d)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addOverride", [path, value]))

    @jsii.member(jsii_name="addToArray")
    def add_to_array(self, path: builtins.str, *values: typing.Any) -> None:
        '''(experimental) Adds to an array in the synthesized object file.

        If the array is nested, separate each nested level using a dot (.) in the path parameter.
        If there is an array as part of the nesting, specify the index in the path.

        To include a literal ``.`` in the property name, prefix with a ``\\``. In most
        programming languages you will need to write this as ``"\\\\."`` because the
        ``\\`` itself will need to be escaped.

        For example, with the following object file Example::

           "compilerOptions": {
             "exclude": ["node_modules"],
             "lib": ["es2020"]
             ...
           }
           ...

        Example::

           project.tsconfig.file.addToArray('compilerOptions.exclude', 'coverage');
           project.tsconfig.file.addToArray('compilerOptions.lib', 'dom', 'dom.iterable', 'esnext');

        would result in the following object file Example::

           "compilerOptions": {
             "exclude": ["node_modules", "coverage"],
             "lib": ["es2020", "dom", "dom.iterable", "esnext"]
             ...
           }
           ...

        :param path: - The path of the property, you can use dot notation to att to arrays in complex types. Any intermediate keys will be created as needed.
        :param values: - The values to add. Could be primitive or complex.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59ab4508f11d1d06be04b3c05be32b4576eb8931fd493503e6f753de128a278)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addToArray", [path, *values]))

    @jsii.member(jsii_name="patch")
    def patch(self, *patches: JsonPatch) -> None:
        '''(experimental) Applies an RFC 6902 JSON-patch to the synthesized object file. See https://datatracker.ietf.org/doc/html/rfc6902 for more information.

        For example, with the following object file Example::

           "compilerOptions": {
             "exclude": ["node_modules"],
             "lib": ["es2020"]
             ...
           }
           ...

        Example::

           project.tsconfig.file.patch(JsonPatch.add("/compilerOptions/exclude/-", "coverage"));
           project.tsconfig.file.patch(JsonPatch.replace("/compilerOptions/lib", ["dom", "dom.iterable", "esnext"]));

        would result in the following object file Example::

           "compilerOptions": {
             "exclude": ["node_modules", "coverage"],
             "lib": ["dom", "dom.iterable", "esnext"]
             ...
           }
           ...

        :param patches: - The patch operations to apply.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396760b16d710d570e49cc49d49b73651a49b2122c9872e6b542d85ad67ed154)
            check_type(argname="argument patches", value=patches, expected_type=typing.Tuple[type_hints["patches"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "patch", [*patches]))

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, resolver: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1daaba9b52cca530d5e7cb415223e62e8a1067329bc5c65b3a22bf46b5cacff1)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))

    @builtins.property
    @jsii.member(jsii_name="omitEmpty")
    def omit_empty(self) -> builtins.bool:
        '''(experimental) Indicates if empty objects and arrays are omitted from the output object.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "omitEmpty"))


class _ObjectFileProxy(
    ObjectFile,
    jsii.proxy_for(FileBase), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ObjectFile).__jsii_proxy_class__ = lambda : _ObjectFileProxy


@jsii.data_type(
    jsii_type="projen.ObjectFileOptions",
    jsii_struct_bases=[FileBaseOptions],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
        "obj": "obj",
        "omit_empty": "omitEmpty",
    },
)
class ObjectFileOptions(FileBaseOptions):
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``ObjectFile``.

        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc32648d019ed604ffeabb7df77055facd2d33215e7a019d7e057c323b9ea5ac)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly
        if obj is not None:
            self._values["obj"] = obj
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def obj(self) -> typing.Any:
        '''(experimental) The object that will be serialized. You can modify the object's contents before synthesis.

        Serialization of the object is similar to JSON.stringify with few enhancements:

        - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values.
        - ``Set`` will be converted to array
        - ``Map`` will be converted to a plain object ({ key: value, ... }})
        - ``RegExp`` without flags will be converted to string representation of the source

        :default: {} an empty object (use ``file.obj`` to mutate).

        :stability: experimental
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Omits empty objects and arrays.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObjectFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Project(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.Project",
):
    '''(experimental) Base project.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional["Project"] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union["ProjenrcJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union["RenovatebotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options

        :stability: experimental
        '''
        options = ProjectOptions(
            name=name,
            commit_generated=commit_generated,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            logging=logging,
            outdir=outdir,
            parent=parent,
            projen_command=projen_command,
            projenrc_json=projenrc_json,
            projenrc_json_options=projenrc_json_options,
            renovatebot=renovatebot,
            renovatebot_options=renovatebot_options,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="isProject")
    @builtins.classmethod
    def is_project(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Test whether the given construct is a project.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909c95926ec40519379f82a71f83357fca295fd1b4313bec2292dc36d9989698)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isProject", [x]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: _constructs_77d1e7e8.IConstruct) -> "Project":
        '''(experimental) Find the closest ancestor project for given construct.

        When given a project, this it the project itself.

        :param construct: -

        :stability: experimental
        :throws: when no project is found in the path to the root
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614179565fafc11a127479175cc34fe37ef37f3036c908e160bff2998ea1c8ff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast("Project", jsii.sinvoke(cls, "of", [construct]))

    @jsii.member(jsii_name="addExcludeFromCleanup")
    def add_exclude_from_cleanup(self, *globs: builtins.str) -> None:
        '''(experimental) Exclude the matching files from pre-synth cleanup.

        Can be used when, for example, some
        source files include the projen marker and we don't want them to be erased during synth.

        :param globs: The glob patterns to match.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb13bbeedf9b4ee7a607b6c974cc57d794730f428181b955df2f6f2fd8da018b)
            check_type(argname="argument globs", value=globs, expected_type=typing.Tuple[type_hints["globs"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addExcludeFromCleanup", [*globs]))

    @jsii.member(jsii_name="addGitIgnore")
    def add_git_ignore(self, pattern: builtins.str) -> None:
        '''(experimental) Adds a .gitignore pattern.

        :param pattern: The glob pattern to ignore.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b195c9c927b524e6c6857987ca398e126176bec5cf796748b7c79133e223e9)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(None, jsii.invoke(self, "addGitIgnore", [pattern]))

    @jsii.member(jsii_name="addPackageIgnore")
    def add_package_ignore(self, _pattern: builtins.str) -> None:
        '''(experimental) Exclude these files from the bundled package.

        Implemented by project types based on the
        packaging mechanism. For example, ``NodeProject`` delegates this to ``.npmignore``.

        :param _pattern: The glob pattern to exclude.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52ded1bd91d1adb42d00140d53c0ea2dfad1f2fc05a340f71711dd214c97dbe)
            check_type(argname="argument _pattern", value=_pattern, expected_type=type_hints["_pattern"])
        return typing.cast(None, jsii.invoke(self, "addPackageIgnore", [_pattern]))

    @jsii.member(jsii_name="addTask")
    def add_task(
        self,
        name: builtins.str,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        exec: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
        steps: typing.Optional[typing.Sequence[typing.Union["TaskStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "Task":
        '''(experimental) Adds a new task to this project.

        This will fail if the project already has
        a task with this name.

        :param name: The task name to add.
        :param args: (experimental) Should the provided ``exec`` shell command receive fixed args. Default: - no arguments are passed to the step
        :param exec: (experimental) Shell command to execute as the first command of the task. Default: - add steps using ``task.exec(command)`` or ``task.spawn(subtask)``
        :param receive_args: (experimental) Should the provided ``exec`` shell command receive args passed to the task. Default: false
        :param steps: (experimental) List of task steps to run.
        :param condition: (experimental) A shell command which determines if the this task should be executed. If the program exits with a zero exit code, steps will be executed. A non-zero code means that task will be skipped.
        :param cwd: (experimental) The working directory for all steps in this task (unless overridden by the step). Default: - process.cwd()
        :param description: (experimental) The description of this build command. Default: - the task name
        :param env: (experimental) Defines environment variables for the execution of this task. Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``. Default: {}
        :param required_env: (experimental) A set of environment variables that must be defined in order to execute this task. Task execution will fail if one of these is not defined.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb7240461e3476c5778bf65eccdf771a733a6c994c9ab1093bf5302284f6e8d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = TaskOptions(
            args=args,
            exec=exec,
            receive_args=receive_args,
            steps=steps,
            condition=condition,
            cwd=cwd,
            description=description,
            env=env,
            required_env=required_env,
        )

        return typing.cast("Task", jsii.invoke(self, "addTask", [name, props]))

    @jsii.member(jsii_name="addTip")
    def add_tip(self, message: builtins.str) -> None:
        '''(deprecated) Prints a "tip" message during synthesis.

        :param message: The message.

        :deprecated: - use ``project.logger.info(message)`` to show messages during synthesis

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0beed63feccf79f49b05c93c6f457a41e13e37287b4e20c3cb4a68a06a68f3da)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "addTip", [message]))

    @jsii.member(jsii_name="annotateGenerated")
    def annotate_generated(self, _glob: builtins.str) -> None:
        '''(experimental) Consider a set of files as "generated".

        This method is implemented by
        derived classes and used for example, to add git attributes to tell GitHub
        that certain files are generated.

        :param _glob: the glob pattern to match (could be a file path).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3f8f3de4a0f7089b9f05f29e319867a4481d3441eff34d4e9f3eab0130ec70)
            check_type(argname="argument _glob", value=_glob, expected_type=type_hints["_glob"])
        return typing.cast(None, jsii.invoke(self, "annotateGenerated", [_glob]))

    @jsii.member(jsii_name="postSynthesize")
    def post_synthesize(self) -> None:
        '''(experimental) Called after all components are synthesized.

        Order is *not* guaranteed.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "postSynthesize", []))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before all components are synthesized.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.member(jsii_name="removeTask")
    def remove_task(self, name: builtins.str) -> typing.Optional["Task"]:
        '''(experimental) Removes a task from a project.

        :param name: The name of the task to remove.

        :return: The ``Task`` that was removed, otherwise ``undefined``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d6e45e06d8088c7b6e78bb1612a5aa930413dbce990831664c1852b4b50625)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(typing.Optional["Task"], jsii.invoke(self, "removeTask", [name]))

    @jsii.member(jsii_name="runTaskCommand")
    def run_task_command(self, task: "Task") -> builtins.str:
        '''(experimental) Returns the shell command to execute in order to run a task.

        By default, this is ``npx projen@<version> <task>``

        :param task: The task for which the command is required.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76ed37c3dc6ee85f67899def229da9e34be0fa72867bb3effa9eb30602a6a72)
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
        return typing.cast(builtins.str, jsii.invoke(self, "runTaskCommand", [task]))

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''(experimental) Synthesize all project files into ``outdir``.

        1. Call "this.preSynthesize()"
        2. Delete all generated files
        3. Synthesize all subprojects
        4. Synthesize all components of this project
        5. Call "postSynthesize()" for all components of this project
        6. Call "this.postSynthesize()"

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @jsii.member(jsii_name="tryFindFile")
    def try_find_file(self, file_path: builtins.str) -> typing.Optional[FileBase]:
        '''(experimental) Finds a file at the specified relative path within this project and all its subprojects.

        :param file_path: The file path. If this path is relative, it will be resolved from the root of *this* project.

        :return: a ``FileBase`` or undefined if there is no file in that path

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70766139ef881860aaf10aeef6ebdb1465d98e99bad4472ae17e63f34c7fd4f)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(typing.Optional[FileBase], jsii.invoke(self, "tryFindFile", [file_path]))

    @jsii.member(jsii_name="tryFindJsonFile")
    def try_find_json_file(
        self,
        file_path: builtins.str,
    ) -> typing.Optional["JsonFile"]:
        '''(deprecated) Finds a json file by name.

        :param file_path: The file path.

        :deprecated: use ``tryFindObjectFile``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65eb5e92f4d625ac2145ddbfa1b0e23e3eac098ec0084123d40298e71d45dac)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(typing.Optional["JsonFile"], jsii.invoke(self, "tryFindJsonFile", [file_path]))

    @jsii.member(jsii_name="tryFindObjectFile")
    def try_find_object_file(
        self,
        file_path: builtins.str,
    ) -> typing.Optional[ObjectFile]:
        '''(experimental) Finds an object file (like JsonFile, YamlFile, etc.) by name.

        :param file_path: The file path.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb95b1525dde337216151338c677538f9fef8920e8ec9c6f33444b7f936f545)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(typing.Optional[ObjectFile], jsii.invoke(self, "tryFindObjectFile", [file_path]))

    @jsii.member(jsii_name="tryRemoveFile")
    def try_remove_file(self, file_path: builtins.str) -> typing.Optional[FileBase]:
        '''(experimental) Finds a file at the specified relative path within this project and removes it.

        :param file_path: The file path. If this path is relative, it will be resolved from the root of *this* project.

        :return:

        a ``FileBase`` if the file was found and removed, or undefined if
        the file was not found.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d37a5c5825b9b3d7ff7498ac7929ccb4efdb7a4d051b9f355807df9f244105)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(typing.Optional[FileBase], jsii.invoke(self, "tryRemoveFile", [file_path]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_TASK")
    def DEFAULT_TASK(cls) -> builtins.str:
        '''(experimental) The name of the default task (the task executed when ``projen`` is run without arguments).

        Normally
        this task should synthesize the project files.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_TASK"))

    @builtins.property
    @jsii.member(jsii_name="buildTask")
    def build_task(self) -> "Task":
        '''
        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "buildTask"))

    @builtins.property
    @jsii.member(jsii_name="commitGenerated")
    def commit_generated(self) -> builtins.bool:
        '''(experimental) Whether to commit the managed files by default.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "commitGenerated"))

    @builtins.property
    @jsii.member(jsii_name="compileTask")
    def compile_task(self) -> "Task":
        '''
        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "compileTask"))

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> typing.List[Component]:
        '''(experimental) Returns all the components within this project.

        :stability: experimental
        '''
        return typing.cast(typing.List[Component], jsii.get(self, "components"))

    @builtins.property
    @jsii.member(jsii_name="deps")
    def deps(self) -> Dependencies:
        '''(experimental) Project dependencies.

        :stability: experimental
        '''
        return typing.cast(Dependencies, jsii.get(self, "deps"))

    @builtins.property
    @jsii.member(jsii_name="ejected")
    def ejected(self) -> builtins.bool:
        '''(experimental) Whether or not the project is being ejected.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "ejected"))

    @builtins.property
    @jsii.member(jsii_name="files")
    def files(self) -> typing.List[FileBase]:
        '''(experimental) All files in this project.

        :stability: experimental
        '''
        return typing.cast(typing.List[FileBase], jsii.get(self, "files"))

    @builtins.property
    @jsii.member(jsii_name="gitattributes")
    def gitattributes(self) -> GitAttributesFile:
        '''(experimental) The .gitattributes file for this repository.

        :stability: experimental
        '''
        return typing.cast(GitAttributesFile, jsii.get(self, "gitattributes"))

    @builtins.property
    @jsii.member(jsii_name="gitignore")
    def gitignore(self) -> IgnoreFile:
        '''(experimental) .gitignore.

        :stability: experimental
        '''
        return typing.cast(IgnoreFile, jsii.get(self, "gitignore"))

    @builtins.property
    @jsii.member(jsii_name="logger")
    def logger(self) -> Logger:
        '''(experimental) Logging utilities.

        :stability: experimental
        '''
        return typing.cast(Logger, jsii.get(self, "logger"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) Project name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''(experimental) Absolute output directory of this project.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="packageTask")
    def package_task(self) -> "Task":
        '''
        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "packageTask"))

    @builtins.property
    @jsii.member(jsii_name="postCompileTask")
    def post_compile_task(self) -> "Task":
        '''
        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "postCompileTask"))

    @builtins.property
    @jsii.member(jsii_name="preCompileTask")
    def pre_compile_task(self) -> "Task":
        '''
        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "preCompileTask"))

    @builtins.property
    @jsii.member(jsii_name="projectBuild")
    def project_build(self) -> "ProjectBuild":
        '''(experimental) Manages the build process of the project.

        :stability: experimental
        '''
        return typing.cast("ProjectBuild", jsii.get(self, "projectBuild"))

    @builtins.property
    @jsii.member(jsii_name="projenCommand")
    def projen_command(self) -> builtins.str:
        '''(experimental) The command to use in order to run the projen CLI.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "projenCommand"))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> "Project":
        '''(experimental) The root project.

        :stability: experimental
        '''
        return typing.cast("Project", jsii.get(self, "root"))

    @builtins.property
    @jsii.member(jsii_name="subprojects")
    def subprojects(self) -> typing.List["Project"]:
        '''(experimental) Returns all the subprojects within this project.

        :stability: experimental
        '''
        return typing.cast(typing.List["Project"], jsii.get(self, "subprojects"))

    @builtins.property
    @jsii.member(jsii_name="tasks")
    def tasks(self) -> "Tasks":
        '''(experimental) Project tasks.

        :stability: experimental
        '''
        return typing.cast("Tasks", jsii.get(self, "tasks"))

    @builtins.property
    @jsii.member(jsii_name="testTask")
    def test_task(self) -> "Task":
        '''
        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "testTask"))

    @builtins.property
    @jsii.member(jsii_name="defaultTask")
    def default_task(self) -> typing.Optional["Task"]:
        '''(experimental) This is the "default" task, the one that executes "projen".

        Undefined if
        the project is being ejected.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Task"], jsii.get(self, "defaultTask"))

    @builtins.property
    @jsii.member(jsii_name="initProject")
    def init_project(self) -> typing.Optional[InitProject]:
        '''(experimental) The options used when this project is bootstrapped via ``projen new``.

        It
        includes the original set of options passed to the CLI and also the JSII
        FQN of the project type.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[InitProject], jsii.get(self, "initProject"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Project"]:
        '''(experimental) A parent project.

        If undefined, this is the root project.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["Project"], jsii.get(self, "parent"))


class ProjectBuild(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.ProjectBuild"):
    '''(experimental) Manages a standard build process for all projects.

    Build spawns these tasks in order:

    1. default
    2. pre-compile
    3. compile
    4. post-compile
    5. test
    6. package

    :stability: experimental
    '''

    def __init__(self, project: Project) -> None:
        '''
        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bda3bf4e486437808f86825b7c514ecdc1487047c8a912a8ec695f6c7994008)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])

    @builtins.property
    @jsii.member(jsii_name="buildTask")
    def build_task(self) -> "Task":
        '''(experimental) The task responsible for a full release build.

        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "buildTask"))

    @builtins.property
    @jsii.member(jsii_name="compileTask")
    def compile_task(self) -> "Task":
        '''(experimental) Compiles the code.

        By default for node.js projects this task is empty.

        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "compileTask"))

    @builtins.property
    @jsii.member(jsii_name="packageTask")
    def package_task(self) -> "Task":
        '''(experimental) The "package" task.

        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "packageTask"))

    @builtins.property
    @jsii.member(jsii_name="postCompileTask")
    def post_compile_task(self) -> "Task":
        '''(experimental) Post-compile task.

        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "postCompileTask"))

    @builtins.property
    @jsii.member(jsii_name="preCompileTask")
    def pre_compile_task(self) -> "Task":
        '''(experimental) Pre-compile task.

        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "preCompileTask"))

    @builtins.property
    @jsii.member(jsii_name="testTask")
    def test_task(self) -> "Task":
        '''(experimental) Tests the code.

        :stability: experimental
        '''
        return typing.cast("Task", jsii.get(self, "testTask"))


@jsii.data_type(
    jsii_type="projen.ProjectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "commit_generated": "commitGenerated",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "logging": "logging",
        "outdir": "outdir",
        "parent": "parent",
        "projen_command": "projenCommand",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
    },
)
class ProjectOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional[Project] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union["ProjenrcJsonOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union["RenovatebotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``Project``.

        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options

        :stability: experimental
        '''
        if isinstance(git_ignore_options, dict):
            git_ignore_options = IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = GitOptions(**git_options)
        if isinstance(logging, dict):
            logging = LoggerOptions(**logging)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = RenovatebotOptions(**renovatebot_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef7d6448b98c56283c32249b27775d5b609a52bab9bec1934494e170ed4b829)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if logging is not None:
            self._values["logging"] = logging
        if outdir is not None:
            self._values["outdir"] = outdir
        if parent is not None:
            self._values["parent"] = parent
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) This is the name of your project.

        :default: $BASEDIR

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[IgnoreFileOptions]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[IgnoreFileOptions], result)

    @builtins.property
    def git_options(self) -> typing.Optional[GitOptions]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[GitOptions], result)

    @builtins.property
    def logging(self) -> typing.Optional[LoggerOptions]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[LoggerOptions], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project.

        Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[Project]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[Project], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(self) -> typing.Optional["ProjenrcJsonOptions"]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional["ProjenrcJsonOptions"], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(self) -> typing.Optional["RenovatebotOptions"]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional["RenovatebotOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectTree(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.ProjectTree"):
    '''
    :stability: experimental
    '''

    def __init__(self, project: Project) -> None:
        '''
        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d641368026b1d886dc04897d3f5cd3c6f816493615fd3c987eaf69bd626aa1)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> "JsonFile":
        '''
        :stability: experimental
        '''
        return typing.cast("JsonFile", jsii.get(self, "file"))

    @file.setter
    def file(self, value: "JsonFile") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd1d331084783b1e11404a33c550a54f472b9e2d656ca02bdc7287828f96e2fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value) # pyright: ignore[reportArgumentType]


@jsii.enum(jsii_type="projen.ProjectType")
class ProjectType(enum.Enum):
    '''(deprecated) Which type of project this is.

    :deprecated: no longer supported at the base project level

    :stability: deprecated
    '''

    UNKNOWN = "UNKNOWN"
    '''(deprecated) This module may be a either a library or an app.

    :stability: deprecated
    '''
    LIB = "LIB"
    '''(deprecated) This is a library, intended to be published to a package manager and consumed by other projects.

    :stability: deprecated
    '''
    APP = "APP"
    '''(deprecated) This is an app (service, tool, website, etc).

    Its artifacts are intended to
    be deployed or published for end-user consumption.

    :stability: deprecated
    '''


class Projects(metaclass=jsii.JSIIMeta, jsii_type="projen.Projects"):
    '''(experimental) Programmatic API for projen.

    :stability: experimental
    '''

    @jsii.member(jsii_name="createProject")
    @builtins.classmethod
    def create_project(
        cls,
        *,
        dir: builtins.str,
        project_fqn: builtins.str,
        project_options: typing.Mapping[builtins.str, typing.Any],
        option_hints: typing.Optional[InitProjectOptionHints] = None,
        post: typing.Optional[builtins.bool] = None,
        synth: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Creates a new project with defaults.

        This function creates the project type in-process (with in VM) and calls
        ``.synth()`` on it (if ``options.synth`` is not ``false``).

        At the moment, it also generates a ``.projenrc.js`` file with the same code
        that was just executed. In the future, this will also be done by the project
        type, so we can easily support multiple languages of projenrc.

        An environment variable (PROJEN_CREATE_PROJECT=true) is set within the VM
        so that custom project types can detect whether the current synthesis is the
        result of a new project creation (and take additional steps accordingly)

        :param dir: (experimental) Directory that the project will be generated in.
        :param project_fqn: (experimental) Fully-qualified name of the project type (usually formatted as ``projen.module.ProjectType``).
        :param project_options: (experimental) Project options. Only JSON-like values can be passed in (strings, booleans, numbers, enums, arrays, and objects that are not derived from classes). Consult the API reference of the project type you are generating for information about what fields and types are available.
        :param option_hints: (experimental) Should we render commented-out default options in the projenrc file? Does not apply to projenrc.json files. Default: InitProjectOptionHints.FEATURED
        :param post: (experimental) Should we execute post synthesis hooks? (usually package manager install). Default: true
        :param synth: (experimental) Should we call ``project.synth()`` or instantiate the project (could still have side-effects) and render the .projenrc file. Default: true

        :stability: experimental
        '''
        options = CreateProjectOptions(
            dir=dir,
            project_fqn=project_fqn,
            project_options=project_options,
            option_hints=option_hints,
            post=post,
            synth=synth,
        )

        return typing.cast(None, jsii.sinvoke(cls, "createProject", [options]))


class ProjenrcFile(
    Component,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="projen.ProjenrcFile",
):
    '''(experimental) A component representing the projen runtime configuration.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eceaec699c352362ccbd6e243d30a2e6cb72fca16183fc6917e8140a42c29f57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, project: Project) -> typing.Optional["ProjenrcFile"]:
        '''(experimental) Returns the ``Projenrc`` instance associated with a project or ``undefined`` if there is no Projenrc.

        :param project: The project.

        :return: A Projenrc

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b101e9a16bb1d0770a9bdccfb59eaa94698a351261b5ec4e3d5265acaba298)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast(typing.Optional["ProjenrcFile"], jsii.sinvoke(cls, "of", [project]))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before synthesis.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @builtins.property
    @jsii.member(jsii_name="filePath")
    @abc.abstractmethod
    def file_path(self) -> builtins.str:
        '''(experimental) The path of the projenrc file.

        :stability: experimental
        '''
        ...


class _ProjenrcFileProxy(ProjenrcFile):
    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        '''(experimental) The path of the projenrc file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ProjenrcFile).__jsii_proxy_class__ = lambda : _ProjenrcFileProxy


class ProjenrcJson(
    ProjenrcFile,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.ProjenrcJson",
):
    '''(experimental) Sets up a project to use JSON for projenrc.

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        *,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param filename: (experimental) The name of the projenrc file. Default: ".projenrc.json"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f15d342ae05206d72b7818258b15e3fe0c8d8a752a91c55d215d8b0483dc139)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = ProjenrcJsonOptions(filename=filename)

        jsii.create(self.__class__, self, [project, options])

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        '''(experimental) The path of the projenrc file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "filePath"))


@jsii.data_type(
    jsii_type="projen.ProjenrcJsonOptions",
    jsii_struct_bases=[],
    name_mapping={"filename": "filename"},
)
class ProjenrcJsonOptions:
    def __init__(self, *, filename: typing.Optional[builtins.str] = None) -> None:
        '''
        :param filename: (experimental) The name of the projenrc file. Default: ".projenrc.json"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a99955e971461d6a1a22bde13c0353d22c81866a29b67be950a0e26b50c76d)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filename is not None:
            self._values["filename"] = filename

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the projenrc file.

        :default: ".projenrc.json"

        :stability: experimental
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjenrcJsonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.ProjenrcOptions",
    jsii_struct_bases=[ProjenrcJsonOptions],
    name_mapping={"filename": "filename"},
)
class ProjenrcOptions(ProjenrcJsonOptions):
    def __init__(self, *, filename: typing.Optional[builtins.str] = None) -> None:
        '''
        :param filename: (experimental) The name of the projenrc file. Default: ".projenrc.json"

        :deprecated: use ``ProjenrcJsonOptions``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e65c016c9638462ddcfa91c71dec3094782bd55bb80eb39df93ca1b9caee431)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filename is not None:
            self._values["filename"] = filename

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the projenrc file.

        :default: ".projenrc.json"

        :stability: experimental
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjenrcOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleasableCommits(metaclass=jsii.JSIIMeta, jsii_type="projen.ReleasableCommits"):
    '''(experimental) Find commits that should be considered releasable to decide if a release is required.

    :stability: experimental
    '''

    @jsii.member(jsii_name="everyCommit")
    @builtins.classmethod
    def every_commit(
        cls,
        path: typing.Optional[builtins.str] = None,
    ) -> "ReleasableCommits":
        '''(experimental) Release every commit.

        This will only not release if the most recent commit is tagged with the latest matching tag.

        :param path: Consider only commits that are enough to explain how the files that match the specified paths came to be. This path is relative to the current working dir of the ``bump`` task, i.e. to only consider commits of a subproject use ``"."``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1cb2a20764c493021a975dc66d097be2a86987ccece8a4e9aeb51464a695829)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("ReleasableCommits", jsii.sinvoke(cls, "everyCommit", [path]))

    @jsii.member(jsii_name="exec")
    @builtins.classmethod
    def exec(cls, cmd: builtins.str) -> "ReleasableCommits":
        '''(experimental) Use an arbitrary shell command to find releasable commits since the latest tag.

        A new release will be initiated, if the number of returned commits is greater than zero.
        Must return a newline separate list of commits that should considered releasable.
        ``$LATEST_TAG`` will be replaced with the actual latest tag for the given prefix.*

        :param cmd: -

        :stability: experimental

        Example::

            "git log --oneline $LATEST_TAG..HEAD -- ."
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae99067556dc4317fa46683f512786bc803178cc26b794688b734aad677d6ad5)
            check_type(argname="argument cmd", value=cmd, expected_type=type_hints["cmd"])
        return typing.cast("ReleasableCommits", jsii.sinvoke(cls, "exec", [cmd]))

    @jsii.member(jsii_name="featuresAndFixes")
    @builtins.classmethod
    def features_and_fixes(
        cls,
        path: typing.Optional[builtins.str] = None,
    ) -> "ReleasableCommits":
        '''(experimental) Release only features and fixes.

        Shorthand for ``ReleasableCommits.onlyOfType(['feat', 'fix'])``.

        :param path: Consider only commits that are enough to explain how the files that match the specified paths came to be. This path is relative to the current working dir of the ``bump`` task, i.e. to only consider commits of a subproject use ``"."``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed5698324356b7a6f65c5e830a0b241b450786bb6c44a17c68cd21fff2ec2ec)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("ReleasableCommits", jsii.sinvoke(cls, "featuresAndFixes", [path]))

    @jsii.member(jsii_name="ofType")
    @builtins.classmethod
    def of_type(
        cls,
        types: typing.Sequence[builtins.str],
        path: typing.Optional[builtins.str] = None,
    ) -> "ReleasableCommits":
        '''(experimental) Limit commits by their conventional commit type.

        This will only release commit that match one of the provided types.
        Commits are required to follow the conventional commit spec and will be ignored otherwise.

        :param types: List of conventional commit types that should be released.
        :param path: Consider only commits that are enough to explain how the files that match the specified paths came to be. This path is relative to the current working dir of the ``bump`` task, i.e. to only consider commits of a subproject use ``"."``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4efcc2d3340114e5856cdafe45dc717452519355cde39b8c2e63eab5217db1a)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("ReleasableCommits", jsii.sinvoke(cls, "ofType", [types, path]))

    @builtins.property
    @jsii.member(jsii_name="cmd")
    def cmd(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cmd"))

    @cmd.setter
    def cmd(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c46f6c8bc57788436baf6da521f9e5812106db6aa16bda9534549c8cbb078d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmd", value) # pyright: ignore[reportArgumentType]


class Renovatebot(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.Renovatebot"):
    '''(experimental) Defines renovatebot configuration for projen project.

    Ignores the versions controlled by Projen.

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        *,
        ignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignore_projen: typing.Optional[builtins.bool] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        marker: typing.Optional[builtins.bool] = None,
        override_config: typing.Any = None,
        schedule_interval: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project: -
        :param ignore: (experimental) You can use the ``ignore`` option to customize which dependencies are updated. The ignore option supports just package name. Default: []
        :param ignore_projen: (experimental) Ignores updates to ``projen``. This is required since projen updates may cause changes in committed files and anti-tamper checks will fail. Projen upgrades are covered through the ``ProjenUpgrade`` class. Default: true
        :param labels: (experimental) List of labels to apply to the created PR's.
        :param marker: 
        :param override_config: 
        :param schedule_interval: (experimental) How often to check for new versions and raise pull requests. Can be given in CRON or LATER format, and use multiple schedules (e.g. different for weekdays and weekends). Multiple rules are handles as OR. Some normal scheduling values defined in enum ``RenovatebotScheduleInterval``. Default: ["at any time"]

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096e7567a3344884436d387a9f887ed96b3691c6d8ad217be945ed3e697ca2cf)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = RenovatebotOptions(
            ignore=ignore,
            ignore_projen=ignore_projen,
            labels=labels,
            marker=marker,
            override_config=override_config,
            schedule_interval=schedule_interval,
        )

        jsii.create(self.__class__, self, [project, options])

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> "JsonFile":
        '''(experimental) The file holding the renovatebot configuration.

        :stability: experimental
        '''
        return typing.cast("JsonFile", jsii.get(self, "file"))


@jsii.data_type(
    jsii_type="projen.RenovatebotOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ignore": "ignore",
        "ignore_projen": "ignoreProjen",
        "labels": "labels",
        "marker": "marker",
        "override_config": "overrideConfig",
        "schedule_interval": "scheduleInterval",
    },
)
class RenovatebotOptions:
    def __init__(
        self,
        *,
        ignore: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignore_projen: typing.Optional[builtins.bool] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        marker: typing.Optional[builtins.bool] = None,
        override_config: typing.Any = None,
        schedule_interval: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for Renovatebot.

        :param ignore: (experimental) You can use the ``ignore`` option to customize which dependencies are updated. The ignore option supports just package name. Default: []
        :param ignore_projen: (experimental) Ignores updates to ``projen``. This is required since projen updates may cause changes in committed files and anti-tamper checks will fail. Projen upgrades are covered through the ``ProjenUpgrade`` class. Default: true
        :param labels: (experimental) List of labels to apply to the created PR's.
        :param marker: 
        :param override_config: 
        :param schedule_interval: (experimental) How often to check for new versions and raise pull requests. Can be given in CRON or LATER format, and use multiple schedules (e.g. different for weekdays and weekends). Multiple rules are handles as OR. Some normal scheduling values defined in enum ``RenovatebotScheduleInterval``. Default: ["at any time"]

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567099b4941210c2f0eb5a6df45f4f8e145db210a75dd2f52fb480378619c263)
            check_type(argname="argument ignore", value=ignore, expected_type=type_hints["ignore"])
            check_type(argname="argument ignore_projen", value=ignore_projen, expected_type=type_hints["ignore_projen"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument override_config", value=override_config, expected_type=type_hints["override_config"])
            check_type(argname="argument schedule_interval", value=schedule_interval, expected_type=type_hints["schedule_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ignore is not None:
            self._values["ignore"] = ignore
        if ignore_projen is not None:
            self._values["ignore_projen"] = ignore_projen
        if labels is not None:
            self._values["labels"] = labels
        if marker is not None:
            self._values["marker"] = marker
        if override_config is not None:
            self._values["override_config"] = override_config
        if schedule_interval is not None:
            self._values["schedule_interval"] = schedule_interval

    @builtins.property
    def ignore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) You can use the ``ignore`` option to customize which dependencies are updated.

        The ignore option supports just package name.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("ignore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignore_projen(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignores updates to ``projen``.

        This is required since projen updates may cause changes in committed files
        and anti-tamper checks will fail.

        Projen upgrades are covered through the ``ProjenUpgrade`` class.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ignore_projen")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of labels to apply to the created PR's.

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def override_config(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        result = self._values.get("override_config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def schedule_interval(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) How often to check for new versions and raise pull requests.

        Can be given in CRON or LATER format, and use multiple schedules
        (e.g. different for weekdays and weekends). Multiple rules are
        handles as OR.

        Some normal scheduling values defined in enum ``RenovatebotScheduleInterval``.

        :default: ["at any time"]

        :see: https://docs.renovatebot.com/configuration-options/#schedule
        :stability: experimental
        '''
        result = self._values.get("schedule_interval")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenovatebotOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.RenovatebotScheduleInterval")
class RenovatebotScheduleInterval(enum.Enum):
    '''(experimental) How often to check for new versions and raise pull requests for version updates.

    :see: https://docs.renovatebot.com/presets-schedule/
    :stability: experimental
    '''

    ANY_TIME = "ANY_TIME"
    '''(experimental) Run at any time.

    :stability: experimental
    '''
    EARLY_MONDAYS = "EARLY_MONDAYS"
    '''(experimental) Weekly schedule on early monday mornings.

    :stability: experimental
    '''
    DAILY = "DAILY"
    '''(experimental) Schedule daily.

    :stability: experimental
    '''
    MONTHLY = "MONTHLY"
    '''(experimental) Schedule monthly.

    :stability: experimental
    '''
    QUARTERLY = "QUARTERLY"
    '''(experimental) Schedule quarterly.

    :stability: experimental
    '''
    WEEKENDS = "WEEKENDS"
    '''(experimental) Schedule for weekends.

    :stability: experimental
    '''
    WEEKDAYS = "WEEKDAYS"
    '''(experimental) Schedule for weekdays.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.ResolveOptions",
    jsii_struct_bases=[],
    name_mapping={"args": "args", "omit_empty": "omitEmpty"},
)
class ResolveOptions:
    def __init__(
        self,
        *,
        args: typing.Optional[typing.Sequence[typing.Any]] = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Resolve options.

        :param args: (experimental) Context arguments. Default: []
        :param omit_empty: (experimental) Omits empty arrays and objects. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4b97f8ab65df023c8b871bd346713f10c0be9a3c56164ff8daff235b29f110)
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if args is not None:
            self._values["args"] = args
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty

    @builtins.property
    def args(self) -> typing.Optional[typing.List[typing.Any]]:
        '''(experimental) Context arguments.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Omits empty arrays and objects.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolveOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.Rule",
    jsii_struct_bases=[],
    name_mapping={
        "targets": "targets",
        "phony": "phony",
        "prerequisites": "prerequisites",
        "recipe": "recipe",
    },
)
class Rule:
    def __init__(
        self,
        *,
        targets: typing.Sequence[builtins.str],
        phony: typing.Optional[builtins.bool] = None,
        prerequisites: typing.Optional[typing.Sequence[builtins.str]] = None,
        recipe: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) A Make rule.

        :param targets: (experimental) Files to be created or updated by this rule. If the rule is phony then instead this represents the command's name(s).
        :param phony: (experimental) Marks whether the target is phony. Default: false
        :param prerequisites: (experimental) Files that are used as inputs to create a target. Default: []
        :param recipe: (experimental) Commands that are run (using prerequisites as inputs) to create a target. Default: []

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960ffc3506d59d9b0342960ce1ae8b57e2e9b37cb7952b5c51fec42ee1db4e8d)
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument phony", value=phony, expected_type=type_hints["phony"])
            check_type(argname="argument prerequisites", value=prerequisites, expected_type=type_hints["prerequisites"])
            check_type(argname="argument recipe", value=recipe, expected_type=type_hints["recipe"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "targets": targets,
        }
        if phony is not None:
            self._values["phony"] = phony
        if prerequisites is not None:
            self._values["prerequisites"] = prerequisites
        if recipe is not None:
            self._values["recipe"] = recipe

    @builtins.property
    def targets(self) -> typing.List[builtins.str]:
        '''(experimental) Files to be created or updated by this rule.

        If the rule is phony then instead this represents the command's name(s).

        :stability: experimental
        '''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def phony(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Marks whether the target is phony.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("phony")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prerequisites(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Files that are used as inputs to create a target.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("prerequisites")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def recipe(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Commands that are run (using prerequisites as inputs) to create a target.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("recipe")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Rule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SampleDir(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.SampleDir"):
    '''(experimental) Renders the given files into the directory if the directory does not exist.

    Use this to create sample code files

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        dir: builtins.str,
        *,
        files: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        source_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Create sample files in the given directory if the given directory does not exist.

        :param project: Parent project to add files to.
        :param dir: directory to add files to. If directory already exists, nothing is added.
        :param files: (experimental) The files to render into the directory. These files get added after any files from ``source`` if that option is specified (replacing if names overlap).
        :param source_dir: (experimental) Absolute path to a directory to copy files from (does not need to be text files). If your project is typescript-based and has configured ``testdir`` to be a subdirectory of ``src``, sample files should outside of the ``src`` directory otherwise they may not be copied. For example:: new SampleDir(this, 'public', { source: path.join(__dirname, '..', 'sample-assets') });

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8efbed63e76d887e28111eeef32b09ef5633f3c345fcb30e0eb79de9bd55ffb)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
        options = SampleDirOptions(files=files, source_dir=source_dir)

        jsii.create(self.__class__, self, [project, dir, options])

    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> None:
        '''(experimental) Synthesizes files to the project output directory.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", []))


@jsii.data_type(
    jsii_type="projen.SampleDirOptions",
    jsii_struct_bases=[],
    name_mapping={"files": "files", "source_dir": "sourceDir"},
)
class SampleDirOptions:
    def __init__(
        self,
        *,
        files: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        source_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) SampleDir options.

        :param files: (experimental) The files to render into the directory. These files get added after any files from ``source`` if that option is specified (replacing if names overlap).
        :param source_dir: (experimental) Absolute path to a directory to copy files from (does not need to be text files). If your project is typescript-based and has configured ``testdir`` to be a subdirectory of ``src``, sample files should outside of the ``src`` directory otherwise they may not be copied. For example:: new SampleDir(this, 'public', { source: path.join(__dirname, '..', 'sample-assets') });

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2420e1173ef03c68a422bbb8b53d09247201a8bd5ac9f6c245970ba305bf520d)
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument source_dir", value=source_dir, expected_type=type_hints["source_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if files is not None:
            self._values["files"] = files
        if source_dir is not None:
            self._values["source_dir"] = source_dir

    @builtins.property
    def files(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The files to render into the directory.

        These files get added after
        any files from ``source`` if that option is specified (replacing if names
        overlap).

        :stability: experimental
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def source_dir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Absolute path to a directory to copy files from (does not need to be text files).

        If your project is typescript-based and has configured ``testdir`` to be a
        subdirectory of ``src``, sample files should outside of the ``src`` directory
        otherwise they may not be copied. For example::

           new SampleDir(this, 'public', { source: path.join(__dirname, '..', 'sample-assets') });

        :stability: experimental
        '''
        result = self._values.get("source_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SampleDirOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SampleFile(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.SampleFile"):
    '''(experimental) Produces a file with the given contents but only once, if the file doesn't already exist.

    Use this for creating example code files or other resources.

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        file_path: builtins.str,
        *,
        contents: typing.Optional[builtins.str] = None,
        source_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Creates a new SampleFile object.

        :param project: - the project to tie this file to.
        :param file_path: - the relative path in the project to put the file.
        :param contents: (experimental) The contents of the file to write.
        :param source_path: (experimental) Absolute path to a file to copy the contents from (does not need to be a text file). If your project is Typescript-based and has configured ``testdir`` to be a subdirectory of ``src``, sample files should outside of the ``src`` directory, otherwise they may not be copied. For example:: new SampleFile(this, 'assets/icon.png', { sourcePath: path.join(__dirname, '..', 'sample-assets', 'icon.png') });

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a38a2fea275113276771eaf46e063f6071707e4fb2f0de49701eed613022f428)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = SampleFileOptions(contents=contents, source_path=source_path)

        jsii.create(self.__class__, self, [project, file_path, options])

    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> None:
        '''(experimental) Synthesizes files to the project output directory.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", []))


@jsii.data_type(
    jsii_type="projen.SampleFileOptions",
    jsii_struct_bases=[],
    name_mapping={"contents": "contents", "source_path": "sourcePath"},
)
class SampleFileOptions:
    def __init__(
        self,
        *,
        contents: typing.Optional[builtins.str] = None,
        source_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for the SampleFile object.

        :param contents: (experimental) The contents of the file to write.
        :param source_path: (experimental) Absolute path to a file to copy the contents from (does not need to be a text file). If your project is Typescript-based and has configured ``testdir`` to be a subdirectory of ``src``, sample files should outside of the ``src`` directory, otherwise they may not be copied. For example:: new SampleFile(this, 'assets/icon.png', { sourcePath: path.join(__dirname, '..', 'sample-assets', 'icon.png') });

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5983842fe223283a82b203e95c2a76bc065a8b8aa52dea3a7881cc3cdd6d6b77)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contents is not None:
            self._values["contents"] = contents
        if source_path is not None:
            self._values["source_path"] = source_path

    @builtins.property
    def contents(self) -> typing.Optional[builtins.str]:
        '''(experimental) The contents of the file to write.

        :stability: experimental
        '''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Absolute path to a file to copy the contents from (does not need to be a text file).

        If your project is Typescript-based and has configured ``testdir`` to be a
        subdirectory of ``src``, sample files should outside of the ``src`` directory,
        otherwise they may not be copied. For example::

           new SampleFile(this, 'assets/icon.png', { sourcePath: path.join(__dirname, '..', 'sample-assets', 'icon.png') });

        :stability: experimental
        '''
        result = self._values.get("source_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SampleFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SampleReadme(
    SampleFile,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.SampleReadme",
):
    '''(experimental) Represents a README.md sample file. You are expected to manage this file after creation.

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        *,
        contents: typing.Optional[builtins.str] = None,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param contents: (experimental) The contents. Default: "# replace this"
        :param filename: (experimental) The name of the README.md file. Default: "README.md"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b9334bb06e21e4e396e8da950bd8d70131a947f97c3cdf330b355dd060b814)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        props = SampleReadmeProps(contents=contents, filename=filename)

        jsii.create(self.__class__, self, [project, props])


@jsii.data_type(
    jsii_type="projen.SampleReadmeProps",
    jsii_struct_bases=[],
    name_mapping={"contents": "contents", "filename": "filename"},
)
class SampleReadmeProps:
    def __init__(
        self,
        *,
        contents: typing.Optional[builtins.str] = None,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) SampleReadme Properties.

        :param contents: (experimental) The contents. Default: "# replace this"
        :param filename: (experimental) The name of the README.md file. Default: "README.md"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77957e29d490dd06dbcef8d6f6f12b818295fcdd57ba6e23c2f47a789f6bd686)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contents is not None:
            self._values["contents"] = contents
        if filename is not None:
            self._values["filename"] = filename

    @builtins.property
    def contents(self) -> typing.Optional[builtins.str]:
        '''(experimental) The contents.

        :default: "# replace this"

        :stability: experimental
        '''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the README.md file.

        :default: "README.md"

        :stability: experimental

        Example::

            "readme.md"
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SampleReadmeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Semver(metaclass=jsii.JSIIMeta, jsii_type="projen.Semver"):
    '''
    :deprecated:

    This class will be removed in upcoming releases. if you wish to
    specify semver requirements in ``deps``, ``devDeps``, etc, specify them like so
    ``express@^2.1``.

    :stability: deprecated
    '''

    @jsii.member(jsii_name="caret")
    @builtins.classmethod
    def caret(cls, version: builtins.str) -> "Semver":
        '''(deprecated) Accept any minor version.

        .. epigraph::

           = version
           < next major version

        :param version: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882a814624f99ac08715fce7fc18a428ae23a52ec698a5ebec9e072a6d4bee7b)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("Semver", jsii.sinvoke(cls, "caret", [version]))

    @jsii.member(jsii_name="latest")
    @builtins.classmethod
    def latest(cls) -> "Semver":
        '''(deprecated) Latest version.

        :stability: deprecated
        '''
        return typing.cast("Semver", jsii.sinvoke(cls, "latest", []))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, spec: builtins.str) -> "Semver":
        '''
        :param spec: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08be6ee4b9a3cf93d50853ebba8a8bec4e9ba922550d4990871f38e90d2202c)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
        return typing.cast("Semver", jsii.sinvoke(cls, "of", [spec]))

    @jsii.member(jsii_name="pinned")
    @builtins.classmethod
    def pinned(cls, version: builtins.str) -> "Semver":
        '''(deprecated) Accept only an exact version.

        :param version: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc51091a63dc9aed397af0467d8120c4946b43f9c07bf576f1e7f9c0a7c1670)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("Semver", jsii.sinvoke(cls, "pinned", [version]))

    @jsii.member(jsii_name="tilde")
    @builtins.classmethod
    def tilde(cls, version: builtins.str) -> "Semver":
        '''(deprecated) Accept patches.

        .. epigraph::

           = version
           < next minor version

        :param version: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf95810f46ca22192ebf45b7182c9dc075240639ad5062da86d9cc145589b8a1)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("Semver", jsii.sinvoke(cls, "tilde", [version]))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> typing.Optional[builtins.str]:
        '''
        :stability: deprecated
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: deprecated
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "version"))


@jsii.data_type(
    jsii_type="projen.SnapshotOptions",
    jsii_struct_bases=[],
    name_mapping={"parse_json": "parseJson"},
)
class SnapshotOptions:
    def __init__(self, *, parse_json: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options for the Snapshot synthesis.

        :param parse_json: (experimental) Parse .json files as a JS object for improved inspection. This will fail if the contents are invalid JSON. Default: true parse .json files into an object

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4033d52c0dc0e7955fb3f2d24e186e7b85bc74bcaf036fc11fbd959c943d9dba)
            check_type(argname="argument parse_json", value=parse_json, expected_type=type_hints["parse_json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parse_json is not None:
            self._values["parse_json"] = parse_json

    @builtins.property
    def parse_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Parse .json files as a JS object for improved inspection. This will fail if the contents are invalid JSON.

        :default: true parse .json files into an object

        :stability: experimental
        '''
        result = self._values.get("parse_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnapshotOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SourceCode(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.SourceCode"):
    '''(experimental) Represents a source file.

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        file_path: builtins.str,
        *,
        indent: typing.Optional[jsii.Number] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param file_path: -
        :param indent: (experimental) Indentation size. Default: 2
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8be88cd766883f8907162beaca5942a5ced596ef64437b757913e47b609893)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = SourceCodeOptions(indent=indent, readonly=readonly)

        jsii.create(self.__class__, self, [project, file_path, options])

    @jsii.member(jsii_name="close")
    def close(self, code: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Decreases the indentation level and closes a code block.

        :param code: The code after the block is closed (e.g. ``}``).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34003984aac9d3e3b9389175974e6c6b74f7d3d41d56ac43f84a68412f1cccaa)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        return typing.cast(None, jsii.invoke(self, "close", [code]))

    @jsii.member(jsii_name="line")
    def line(self, code: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Emit a line of code.

        :param code: The contents, if not specified, just adds a newline.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8562757d443bf862879e9dc7708fb5fa5d0f9c2d6ad2598ee2c3edeb96e7f616)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        return typing.cast(None, jsii.invoke(self, "line", [code]))

    @jsii.member(jsii_name="open")
    def open(self, code: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Opens a code block and increases the indentation level.

        :param code: The code before the block starts (e.g. ``export class {``).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bc8a0529aa4ca39c77add345ebadba429d8974597a851741ec0cd4046f1a20)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        return typing.cast(None, jsii.invoke(self, "open", [code]))

    @builtins.property
    @jsii.member(jsii_name="filePath")
    def file_path(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "filePath"))

    @builtins.property
    @jsii.member(jsii_name="marker")
    def marker(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "marker"))


@jsii.data_type(
    jsii_type="projen.SourceCodeOptions",
    jsii_struct_bases=[],
    name_mapping={"indent": "indent", "readonly": "readonly"},
)
class SourceCodeOptions:
    def __init__(
        self,
        *,
        indent: typing.Optional[jsii.Number] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``SourceCodeFile``.

        :param indent: (experimental) Indentation size. Default: 2
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c604ba47f53eeef393d736d7b829dae144b7a43fad8affb927e7859a46ac29)
            check_type(argname="argument indent", value=indent, expected_type=type_hints["indent"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if indent is not None:
            self._values["indent"] = indent
        if readonly is not None:
            self._values["readonly"] = readonly

    @builtins.property
    def indent(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Indentation size.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("indent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceCodeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Task(metaclass=jsii.JSIIMeta, jsii_type="projen.Task"):
    '''(experimental) A task that can be performed on the project.

    Modeled as a series of shell
    commands and subtasks.

    :stability: experimental
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        exec: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
        steps: typing.Optional[typing.Sequence[typing.Union["TaskStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: -
        :param args: (experimental) Should the provided ``exec`` shell command receive fixed args. Default: - no arguments are passed to the step
        :param exec: (experimental) Shell command to execute as the first command of the task. Default: - add steps using ``task.exec(command)`` or ``task.spawn(subtask)``
        :param receive_args: (experimental) Should the provided ``exec`` shell command receive args passed to the task. Default: false
        :param steps: (experimental) List of task steps to run.
        :param condition: (experimental) A shell command which determines if the this task should be executed. If the program exits with a zero exit code, steps will be executed. A non-zero code means that task will be skipped.
        :param cwd: (experimental) The working directory for all steps in this task (unless overridden by the step). Default: - process.cwd()
        :param description: (experimental) The description of this build command. Default: - the task name
        :param env: (experimental) Defines environment variables for the execution of this task. Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``. Default: {}
        :param required_env: (experimental) A set of environment variables that must be defined in order to execute this task. Task execution will fail if one of these is not defined.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679ed15034b92ce65671fe4889a8e0476b00d6023000c4f1035f69d18ac8760c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = TaskOptions(
            args=args,
            exec=exec,
            receive_args=receive_args,
            steps=steps,
            condition=condition,
            cwd=cwd,
            description=description,
            env=env,
            required_env=required_env,
        )

        jsii.create(self.__class__, self, [name, props])

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, *condition: builtins.str) -> None:
        '''(experimental) Add a command to execute which determines if the task should be skipped.

        If a condition already exists, the new condition will be appended with ``&&`` delimiter.

        :param condition: The command to execute.

        :see: {@link Task.condition }
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248e4e99078602a3b8e376c73fa93425e082239549a245989641e2097a64972a)
            check_type(argname="argument condition", value=condition, expected_type=typing.Tuple[type_hints["condition"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addCondition", [*condition]))

    @jsii.member(jsii_name="builtin")
    def builtin(self, name: builtins.str) -> None:
        '''(experimental) Execute a builtin task.

        Builtin tasks are programs bundled as part of projen itself and used as
        helpers for various components.

        In the future we should support built-in tasks from external modules.

        :param name: The name of the builtin task to execute (e.g. ``release/resolve-version``).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9dd10fb1b2c8242826790d7b14e14f641c34ec35695d12b425f283a93b972f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "builtin", [name]))

    @jsii.member(jsii_name="env")
    def env(self, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Adds an environment variable to this task.

        :param name: The name of the variable.
        :param value: The value. If the value is surrounded by ``$()``, we will evaluate it within a subshell and use the result as the value of the environment variable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e0e7093de18a072e3935f8026bebc9b7916011f0d592178810d5f53451f027)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "env", [name, value]))

    @jsii.member(jsii_name="exec")
    def exec(
        self,
        command: builtins.str,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Executes a shell command.

        :param command: Shell command.
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866645d9e72b430281a892f9aec648a8a4d11dfd83393ea8d1cf161c619f40ce)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        options = TaskStepOptions(
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "exec", [command, options]))

    @jsii.member(jsii_name="insertStep")
    def insert_step(self, index: jsii.Number, *steps: "TaskStep") -> None:
        '''(experimental) Insert one or more steps at a given index.

        :param index: Steps will be inserted before this index. May be negative to count backwards from the end, or may be ``== steps().length`` to insert at the end.
        :param steps: The steps to insert.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45a21d1f9e615dd1b225d6cafbe381a43b42811d1d21efd5a3f6630613e94af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "insertStep", [index, *steps]))

    @jsii.member(jsii_name="lock")
    def lock(self) -> None:
        '''(experimental) Forbid additional changes to this task.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "lock", []))

    @jsii.member(jsii_name="prepend")
    def prepend(
        self,
        shell: builtins.str,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(deprecated) Adds a command at the beginning of the task.

        :param shell: The command to add.
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :deprecated: use ``prependExec()``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72dcbc585fdab7a308274ba33cb7b5bcf9e106aaf01bef404fbb15b6c60db4c4)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
        options = TaskStepOptions(
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "prepend", [shell, options]))

    @jsii.member(jsii_name="prependExec")
    def prepend_exec(
        self,
        shell: builtins.str,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Adds a command at the beginning of the task.

        :param shell: The command to add.
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6303cc71c3e6fb4aba7cadb07d20f36a327564e7e91f7baf72d0bb511b02f9d8)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
        options = TaskStepOptions(
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "prependExec", [shell, options]))

    @jsii.member(jsii_name="prependSay")
    def prepend_say(
        self,
        message: builtins.str,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Says something at the beginning of the task.

        :param message: Your message.
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e687ef928f97e72aa2e81b8d6d9eb6d68cfdfb3063bfbd3f8c9e4ea8177cf5)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        options = TaskStepOptions(
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "prependSay", [message, options]))

    @jsii.member(jsii_name="prependSpawn")
    def prepend_spawn(
        self,
        subtask: "Task",
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Adds a spawn instruction at the beginning of the task.

        :param subtask: The subtask to execute.
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80be0ec2af5c5b034b9ad26a372663b2dede8547b402f7501bd174f174db2d3a)
            check_type(argname="argument subtask", value=subtask, expected_type=type_hints["subtask"])
        options = TaskStepOptions(
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "prependSpawn", [subtask, options]))

    @jsii.member(jsii_name="removeStep")
    def remove_step(self, index: jsii.Number) -> None:
        '''
        :param index: The index of the step to remove.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c493ae53dba9513da0ecb434448ff6e7d3050c90456d373f1135a865eedb69c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast(None, jsii.invoke(self, "removeStep", [index]))

    @jsii.member(jsii_name="reset")
    def reset(
        self,
        command: typing.Optional[builtins.str] = None,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Reset the task so it no longer has any commands.

        :param command: the first command to add to the task after it was cleared.
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec2ab04da022f328e54a5747cb659465473a80e61ea4b23af06f41a51eaf8a8)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        options = TaskStepOptions(
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "reset", [command, options]))

    @jsii.member(jsii_name="say")
    def say(
        self,
        message: builtins.str,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Say something.

        :param message: Your message.
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da16e7abde21673795e791b1dc02e7b9c04503d828a84a24ad2e0950514f3d1)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        options = TaskStepOptions(
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "say", [message, options]))

    @jsii.member(jsii_name="spawn")
    def spawn(
        self,
        subtask: "Task",
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Spawns a sub-task.

        :param subtask: The subtask to execute.
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30afd72afdc7d9e0229d01ea2f502a330dca643bfa30b79876a78ec24110ee41)
            check_type(argname="argument subtask", value=subtask, expected_type=type_hints["subtask"])
        options = TaskStepOptions(
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "spawn", [subtask, options]))

    @jsii.member(jsii_name="updateStep")
    def update_step(
        self,
        index: jsii.Number,
        *,
        builtin: typing.Optional[builtins.str] = None,
        exec: typing.Optional[builtins.str] = None,
        say: typing.Optional[builtins.str] = None,
        spawn: typing.Optional[builtins.str] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param index: The index of the step to edit.
        :param builtin: (experimental) The name of a built-in task to execute. Built-in tasks are node.js programs baked into the projen module and as component runtime helpers. The name is a path relative to the projen lib/ directory (without the .task.js extension). For example, if your built in builtin task is under ``src/release/resolve-version.task.ts``, then this would be ``release/resolve-version``. Default: - do not execute a builtin task
        :param exec: (experimental) Shell command to execute. Default: - don't execute a shell command
        :param say: (experimental) Print a message. Default: - don't say anything
        :param spawn: (experimental) Subtask to execute. Default: - don't spawn a subtask
        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6471d9b24a42d1138efa839e893cd7685a703235152ad4f0c3aae00e2e12f8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        step = TaskStep(
            builtin=builtin,
            exec=exec,
            say=say,
            spawn=spawn,
            args=args,
            condition=condition,
            cwd=cwd,
            env=env,
            name=name,
            receive_args=receive_args,
        )

        return typing.cast(None, jsii.invoke(self, "updateStep", [index, step]))

    @builtins.property
    @jsii.member(jsii_name="envVars")
    def env_vars(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Returns all environment variables in the task level.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "envVars"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) Task name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="steps")
    def steps(self) -> typing.List["TaskStep"]:
        '''(experimental) Returns an immutable copy of all the step specifications of the task.

        :stability: experimental
        '''
        return typing.cast(typing.List["TaskStep"], jsii.get(self, "steps"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) A command to execute which determines if the task should be skipped.

        If it
        returns a zero exit code, the task will not be executed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="cwd")
    def cwd(self) -> typing.Optional[builtins.str]:
        '''(experimental) Returns the working directory for this task.

        Sets the working directory for this task.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cwd"))

    @cwd.setter
    def cwd(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063f23ecf0aa952acdfe114ecbbc1ac116753acf58aa564cd47b3ea5fbd99ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cwd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Returns the description of this task.

        Sets the description of this task.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740ba1ef0d399dc76efb91309b9d1c8426213faa31da03d8c0abbc94a3d02e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="projen.TaskCommonOptions",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "cwd": "cwd",
        "description": "description",
        "env": "env",
        "required_env": "requiredEnv",
    },
)
class TaskCommonOptions:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param condition: (experimental) A shell command which determines if the this task should be executed. If the program exits with a zero exit code, steps will be executed. A non-zero code means that task will be skipped.
        :param cwd: (experimental) The working directory for all steps in this task (unless overridden by the step). Default: - process.cwd()
        :param description: (experimental) The description of this build command. Default: - the task name
        :param env: (experimental) Defines environment variables for the execution of this task. Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``. Default: {}
        :param required_env: (experimental) A set of environment variables that must be defined in order to execute this task. Task execution will fail if one of these is not defined.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7844bf7d22e8f640ebcc5ba4353115b05d556a850bb6d7fdde5513cba44120)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument cwd", value=cwd, expected_type=type_hints["cwd"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument required_env", value=required_env, expected_type=type_hints["required_env"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if cwd is not None:
            self._values["cwd"] = cwd
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if required_env is not None:
            self._values["required_env"] = required_env

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command which determines if the this task should be executed.

        If
        the program exits with a zero exit code, steps will be executed. A non-zero
        code means that task will be skipped.

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cwd(self) -> typing.Optional[builtins.str]:
        '''(experimental) The working directory for all steps in this task (unless overridden by the step).

        :default: - process.cwd()

        :stability: experimental
        '''
        result = self._values.get("cwd")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of this build command.

        :default: - the task name

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Defines environment variables for the execution of this task.

        Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def required_env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A set of environment variables that must be defined in order to execute this task.

        Task execution will fail if one of these is not defined.

        :stability: experimental
        '''
        result = self._values.get("required_env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskCommonOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.TaskOptions",
    jsii_struct_bases=[TaskCommonOptions],
    name_mapping={
        "condition": "condition",
        "cwd": "cwd",
        "description": "description",
        "env": "env",
        "required_env": "requiredEnv",
        "args": "args",
        "exec": "exec",
        "receive_args": "receiveArgs",
        "steps": "steps",
    },
)
class TaskOptions(TaskCommonOptions):
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        exec: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
        steps: typing.Optional[typing.Sequence[typing.Union["TaskStep", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param condition: (experimental) A shell command which determines if the this task should be executed. If the program exits with a zero exit code, steps will be executed. A non-zero code means that task will be skipped.
        :param cwd: (experimental) The working directory for all steps in this task (unless overridden by the step). Default: - process.cwd()
        :param description: (experimental) The description of this build command. Default: - the task name
        :param env: (experimental) Defines environment variables for the execution of this task. Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``. Default: {}
        :param required_env: (experimental) A set of environment variables that must be defined in order to execute this task. Task execution will fail if one of these is not defined.
        :param args: (experimental) Should the provided ``exec`` shell command receive fixed args. Default: - no arguments are passed to the step
        :param exec: (experimental) Shell command to execute as the first command of the task. Default: - add steps using ``task.exec(command)`` or ``task.spawn(subtask)``
        :param receive_args: (experimental) Should the provided ``exec`` shell command receive args passed to the task. Default: false
        :param steps: (experimental) List of task steps to run.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b67d140d8d3bc0d4265c1dc732e2e99b3a05600097a65f0baa8803715ced0be)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument cwd", value=cwd, expected_type=type_hints["cwd"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument required_env", value=required_env, expected_type=type_hints["required_env"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument exec", value=exec, expected_type=type_hints["exec"])
            check_type(argname="argument receive_args", value=receive_args, expected_type=type_hints["receive_args"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if cwd is not None:
            self._values["cwd"] = cwd
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if required_env is not None:
            self._values["required_env"] = required_env
        if args is not None:
            self._values["args"] = args
        if exec is not None:
            self._values["exec"] = exec
        if receive_args is not None:
            self._values["receive_args"] = receive_args
        if steps is not None:
            self._values["steps"] = steps

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command which determines if the this task should be executed.

        If
        the program exits with a zero exit code, steps will be executed. A non-zero
        code means that task will be skipped.

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cwd(self) -> typing.Optional[builtins.str]:
        '''(experimental) The working directory for all steps in this task (unless overridden by the step).

        :default: - process.cwd()

        :stability: experimental
        '''
        result = self._values.get("cwd")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of this build command.

        :default: - the task name

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Defines environment variables for the execution of this task.

        Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def required_env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A set of environment variables that must be defined in order to execute this task.

        Task execution will fail if one of these is not defined.

        :stability: experimental
        '''
        result = self._values.get("required_env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Should the provided ``exec`` shell command receive fixed args.

        :default: - no arguments are passed to the step

        :see: {@link TaskStepOptions.args }
        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exec(self) -> typing.Optional[builtins.str]:
        '''(experimental) Shell command to execute as the first command of the task.

        :default: - add steps using ``task.exec(command)`` or ``task.spawn(subtask)``

        :stability: experimental
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def receive_args(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should the provided ``exec`` shell command receive args passed to the task.

        :default: false

        :see: {@link TaskStepOptions.receiveArgs }
        :stability: experimental
        '''
        result = self._values.get("receive_args")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def steps(self) -> typing.Optional[typing.List["TaskStep"]]:
        '''(experimental) List of task steps to run.

        :stability: experimental
        '''
        result = self._values.get("steps")
        return typing.cast(typing.Optional[typing.List["TaskStep"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskRuntime(metaclass=jsii.JSIIMeta, jsii_type="projen.TaskRuntime"):
    '''(experimental) The runtime component of the tasks engine.

    :stability: experimental
    '''

    def __init__(self, workdir: builtins.str) -> None:
        '''
        :param workdir: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e15f59ab4d32890cdb2f631bc8b086ac603a9f80c504c1ac6e3645e63dd4250)
            check_type(argname="argument workdir", value=workdir, expected_type=type_hints["workdir"])
        jsii.create(self.__class__, self, [workdir])

    @jsii.member(jsii_name="runTask")
    def run_task(
        self,
        name: builtins.str,
        parents: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[typing.Union[builtins.str, jsii.Number]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Runs the task.

        :param name: The task name.
        :param parents: -
        :param args: -
        :param env: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f502dc8ce342b578300faffc5bd3c8c920c8565849215d7cec099d782d3ebf2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parents", value=parents, expected_type=type_hints["parents"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
        return typing.cast(None, jsii.invoke(self, "runTask", [name, parents, args, env]))

    @jsii.member(jsii_name="tryFindTask")
    def try_find_task(self, name: builtins.str) -> typing.Optional["TaskSpec"]:
        '''(experimental) Find a task by name, or ``undefined`` if not found.

        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7792ab86c20765ed6722e2a1881c2907a4f0a114336f30cefaefba00de3330c2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(typing.Optional["TaskSpec"], jsii.invoke(self, "tryFindTask", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANIFEST_FILE")
    def MANIFEST_FILE(cls) -> builtins.str:
        '''(experimental) The project-relative path of the tasks manifest file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MANIFEST_FILE"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> "TasksManifest":
        '''(experimental) The contents of tasks.json.

        :stability: experimental
        '''
        return typing.cast("TasksManifest", jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="tasks")
    def tasks(self) -> typing.List["TaskSpec"]:
        '''(experimental) The tasks in this project.

        :stability: experimental
        '''
        return typing.cast(typing.List["TaskSpec"], jsii.get(self, "tasks"))

    @builtins.property
    @jsii.member(jsii_name="workdir")
    def workdir(self) -> builtins.str:
        '''(experimental) The root directory of the project and the cwd for executing tasks.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "workdir"))


@jsii.data_type(
    jsii_type="projen.TaskSpec",
    jsii_struct_bases=[TaskCommonOptions],
    name_mapping={
        "condition": "condition",
        "cwd": "cwd",
        "description": "description",
        "env": "env",
        "required_env": "requiredEnv",
        "name": "name",
        "steps": "steps",
    },
)
class TaskSpec(TaskCommonOptions):
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: builtins.str,
        steps: typing.Optional[typing.Sequence[typing.Union["TaskStep", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Specification of a single task.

        :param condition: (experimental) A shell command which determines if the this task should be executed. If the program exits with a zero exit code, steps will be executed. A non-zero code means that task will be skipped.
        :param cwd: (experimental) The working directory for all steps in this task (unless overridden by the step). Default: - process.cwd()
        :param description: (experimental) The description of this build command. Default: - the task name
        :param env: (experimental) Defines environment variables for the execution of this task. Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``. Default: {}
        :param required_env: (experimental) A set of environment variables that must be defined in order to execute this task. Task execution will fail if one of these is not defined.
        :param name: (experimental) Task name.
        :param steps: (experimental) Task steps.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284f616dbd3bd02d58106f246e9393ed2115e81d7707ebd8741034d2e9d7faa8)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument cwd", value=cwd, expected_type=type_hints["cwd"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument required_env", value=required_env, expected_type=type_hints["required_env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if condition is not None:
            self._values["condition"] = condition
        if cwd is not None:
            self._values["cwd"] = cwd
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if required_env is not None:
            self._values["required_env"] = required_env
        if steps is not None:
            self._values["steps"] = steps

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command which determines if the this task should be executed.

        If
        the program exits with a zero exit code, steps will be executed. A non-zero
        code means that task will be skipped.

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cwd(self) -> typing.Optional[builtins.str]:
        '''(experimental) The working directory for all steps in this task (unless overridden by the step).

        :default: - process.cwd()

        :stability: experimental
        '''
        result = self._values.get("cwd")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of this build command.

        :default: - the task name

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Defines environment variables for the execution of this task.

        Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def required_env(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A set of environment variables that must be defined in order to execute this task.

        Task execution will fail if one of these is not defined.

        :stability: experimental
        '''
        result = self._values.get("required_env")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Task name.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def steps(self) -> typing.Optional[typing.List["TaskStep"]]:
        '''(experimental) Task steps.

        :stability: experimental
        '''
        result = self._values.get("steps")
        return typing.cast(typing.Optional[typing.List["TaskStep"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.TaskStepOptions",
    jsii_struct_bases=[],
    name_mapping={
        "args": "args",
        "condition": "condition",
        "cwd": "cwd",
        "env": "env",
        "name": "name",
        "receive_args": "receiveArgs",
    },
)
class TaskStepOptions:
    def __init__(
        self,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for task steps.

        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eac93e499bd717527ab62b174c5bd1e157bf4043f5d771b6a289f39177d124a)
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument cwd", value=cwd, expected_type=type_hints["cwd"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument receive_args", value=receive_args, expected_type=type_hints["receive_args"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if args is not None:
            self._values["args"] = args
        if condition is not None:
            self._values["condition"] = condition
        if cwd is not None:
            self._values["cwd"] = cwd
        if env is not None:
            self._values["env"] = env
        if name is not None:
            self._values["name"] = name
        if receive_args is not None:
            self._values["receive_args"] = receive_args

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of fixed arguments always passed to the step.

        Useful to re-use existing tasks without having to re-define the whole task.
        Fixed args are always passed to the step, even if ``receiveArgs`` is ``false``
        and are always passed before any args the task is called with.

        If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command.
        The position of the args can be changed by including the marker ``$@`` inside the command string.

        If the step spawns a subtask, args are passed to the subtask.
        The subtask must define steps receiving args for this to have any effect.

        If the step calls a builtin script, args are passed to the script.
        It is up to the script to use or discard the arguments.

        :default: - no arguments are passed to the step

        :stability: experimental

        Example::

            task.spawn("deploy", { args: ["--force"] });
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command which determines if the this step should be executed.

        If
        the program exits with a zero exit code, the step will be executed. A non-zero
        code means the step will be skipped (subsequent task steps will still be evaluated/executed).

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cwd(self) -> typing.Optional[builtins.str]:
        '''(experimental) The working directory for this step.

        :default: - determined by the task

        :stability: experimental
        '''
        result = self._values.get("cwd")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only).

        Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``.

        :default: - no environment variables defined in step

        :stability: experimental

        Example::

            { "foo": "bar", "boo": "$(echo baz)" }
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Step name.

        :default: - no name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def receive_args(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should this step receive args passed to the task.

        If ``true``, args are passed through at the end of the ``exec`` shell command.
        The position of the args can be changed by including the marker ``$@`` inside the command string.

        If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating
        the whitespace preserving behavior of bash variable expansion.

        If the step spawns a subtask, args are passed to the subtask.
        The subtask must define steps receiving args for this to have any effect.

        :default: false

        :stability: experimental

        Example::

            task.exec("echo Hello $@ World!", { receiveArgs: true });
        '''
        result = self._values.get("receive_args")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskStepOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Tasks(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.Tasks"):
    '''(experimental) Defines project tasks.

    Tasks extend the projen CLI by adding subcommands to it. Task definitions are
    synthesized into ``.projen/tasks.json``.

    :stability: experimental
    '''

    def __init__(self, project: Project) -> None:
        '''
        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__495af8e4e99205093378c79e03b3c0d9920dc74f1087a97c18e344446ffd90f7)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Adds global environment.

        :param name: Environment variable name.
        :param value: Value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c3e6aae839d7e262f9c707d296976e912fe4d334cc2f3ac081cdbc6f15db60)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addEnvironment", [name, value]))

    @jsii.member(jsii_name="addTask")
    def add_task(
        self,
        name: builtins.str,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        exec: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
        steps: typing.Optional[typing.Sequence[typing.Union["TaskStep", typing.Dict[builtins.str, typing.Any]]]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> Task:
        '''(experimental) Adds a task to a project.

        :param name: The name of the task.
        :param args: (experimental) Should the provided ``exec`` shell command receive fixed args. Default: - no arguments are passed to the step
        :param exec: (experimental) Shell command to execute as the first command of the task. Default: - add steps using ``task.exec(command)`` or ``task.spawn(subtask)``
        :param receive_args: (experimental) Should the provided ``exec`` shell command receive args passed to the task. Default: false
        :param steps: (experimental) List of task steps to run.
        :param condition: (experimental) A shell command which determines if the this task should be executed. If the program exits with a zero exit code, steps will be executed. A non-zero code means that task will be skipped.
        :param cwd: (experimental) The working directory for all steps in this task (unless overridden by the step). Default: - process.cwd()
        :param description: (experimental) The description of this build command. Default: - the task name
        :param env: (experimental) Defines environment variables for the execution of this task. Values in this map will be evaluated in a shell, so you can do stuff like ``$(echo "foo")``. Default: {}
        :param required_env: (experimental) A set of environment variables that must be defined in order to execute this task. Task execution will fail if one of these is not defined.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836b8399b5241179b18880b35ae533996a76c85a9b01d5c5c846aaef0e3a8d88)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = TaskOptions(
            args=args,
            exec=exec,
            receive_args=receive_args,
            steps=steps,
            condition=condition,
            cwd=cwd,
            description=description,
            env=env,
            required_env=required_env,
        )

        return typing.cast(Task, jsii.invoke(self, "addTask", [name, options]))

    @jsii.member(jsii_name="removeTask")
    def remove_task(self, name: builtins.str) -> typing.Optional[Task]:
        '''(experimental) Removes a task from a project.

        :param name: The name of the task to remove.

        :return: The ``Task`` that was removed, otherwise ``undefined``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c96f29b4423e28b4b65e683fc7e07a1024953e3610bb284fa1a0a90b8c77c07)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(typing.Optional[Task], jsii.invoke(self, "removeTask", [name]))

    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> None:
        '''(experimental) Synthesizes files to the project output directory.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "synthesize", []))

    @jsii.member(jsii_name="tryFind")
    def try_find(self, name: builtins.str) -> typing.Optional[Task]:
        '''(experimental) Finds a task by name.

        Returns ``undefined`` if the task cannot be found.

        :param name: The name of the task.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3316a1d8c737096e24c835f4cd8318c12ed26e59edc6a48fa5de090d545d802e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(typing.Optional[Task], jsii.invoke(self, "tryFind", [name]))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.List[Task]:
        '''(experimental) All tasks.

        :stability: experimental
        '''
        return typing.cast(typing.List[Task], jsii.get(self, "all"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Returns a copy of the currently global environment for this project.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))


@jsii.data_type(
    jsii_type="projen.TasksManifest",
    jsii_struct_bases=[],
    name_mapping={"env": "env", "tasks": "tasks"},
)
class TasksManifest:
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tasks: typing.Optional[typing.Mapping[builtins.str, typing.Union[TaskSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Schema for ``tasks.json``.

        :param env: (experimental) Environment for all tasks.
        :param tasks: (experimental) All tasks available for this project.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0400d76981616b89be8abb0d5287b8580aa0798ae9b6433bfc19c9e589d6b1a5)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if tasks is not None:
            self._values["tasks"] = tasks

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment for all tasks.

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tasks(self) -> typing.Optional[typing.Mapping[builtins.str, TaskSpec]]:
        '''(experimental) All tasks available for this project.

        :stability: experimental
        '''
        result = self._values.get("tasks")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, TaskSpec]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TasksManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.TestFailureBehavior")
class TestFailureBehavior(enum.Enum):
    '''
    :stability: experimental
    '''

    SKIP = "SKIP"
    '''(experimental) Skip the current patch operation and continue with the next operation.

    :stability: experimental
    '''
    FAIL_SYNTHESIS = "FAIL_SYNTHESIS"
    '''(experimental) Fail the whole file synthesis.

    :stability: experimental
    '''


class Testing(metaclass=jsii.JSIIMeta, jsii_type="projen.Testing"):
    '''(experimental) A Testing static class with a .synth helper for getting a snapshots of construct outputs. Useful for snapshot testing with Jest.

    :stability: experimental

    Example::

        `expect(Testing.synth(someProject)).toMatchSnapshot()`
    '''

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(
        cls,
        project: Project,
        *,
        parse_json: typing.Optional[builtins.bool] = None,
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Produces a simple JS object that represents the contents of the projects with field names being file paths.

        :param project: the project to produce a snapshot for.
        :param parse_json: (experimental) Parse .json files as a JS object for improved inspection. This will fail if the contents are invalid JSON. Default: true parse .json files into an object

        :return: : any }

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184d7a8774ff332a32a14ae9703ca863b4f123b736abf438d6c5131c636fbeb1)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = SnapshotOptions(parse_json=parse_json)

        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.sinvoke(cls, "synth", [project, options]))


class TextFile(FileBase, metaclass=jsii.JSIIMeta, jsii_type="projen.TextFile"):
    '''(experimental) A text file.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        file_path: builtins.str,
        *,
        lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Defines a text file.

        :param scope: -
        :param file_path: File path.
        :param lines: (experimental) The contents of the text file. You can use ``addLine()`` to append lines. Default: [] empty file
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9476d9e99301eafe205e231c4756ac047dd331e4755928e2ec0362aea31d1e68)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = TextFileOptions(
            lines=lines,
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [scope, file_path, options])

    @jsii.member(jsii_name="addLine")
    def add_line(self, line: builtins.str) -> None:
        '''(experimental) Adds a line to the text file.

        :param line: the line to add (can use tokens).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2345f360405dc3baf9ce7fd3079f23bf8acae86b5a5e39993ac4de26eebbae03)
            check_type(argname="argument line", value=line, expected_type=type_hints["line"])
        return typing.cast(None, jsii.invoke(self, "addLine", [line]))

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, _: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param _: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433f7685b1ee13eacf88a0112f3c5ac027adfdd4a486841078298f619674abc8)
            check_type(argname="argument _", value=_, expected_type=type_hints["_"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [_]))


@jsii.data_type(
    jsii_type="projen.TextFileOptions",
    jsii_struct_bases=[FileBaseOptions],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
        "lines": "lines",
    },
)
class TextFileOptions(FileBaseOptions):
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
        lines: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for ``TextFile``.

        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true
        :param lines: (experimental) The contents of the text file. You can use ``addLine()`` to append lines. Default: [] empty file

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0f4dd58b9e223b379bf709c046d112cede147b9481878f22a671a9d7f79bfc)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument lines", value=lines, expected_type=type_hints["lines"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly
        if lines is not None:
            self._values["lines"] = lines

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lines(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The contents of the text file.

        You can use ``addLine()`` to append lines.

        :default: [] empty file

        :stability: experimental
        '''
        result = self._values.get("lines")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TextFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TomlFile(ObjectFile, metaclass=jsii.JSIIMeta, jsii_type="projen.TomlFile"):
    '''(experimental) Represents a TOML file.

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        file_path: builtins.str,
        *,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param file_path: -
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7c08620aabeb578ce8c0c54b1073a9df1f34c7815d8ae6fdebff7eb411c3d8)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = TomlFileOptions(
            obj=obj,
            omit_empty=omit_empty,
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [project, file_path, options])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, resolver: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ab5968ef36d3ff7f038abd17ae6a5bb7c16e94ed9dbcf023bba58b047f2f38)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))


@jsii.data_type(
    jsii_type="projen.TomlFileOptions",
    jsii_struct_bases=[ObjectFileOptions],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
        "obj": "obj",
        "omit_empty": "omitEmpty",
    },
)
class TomlFileOptions(ObjectFileOptions):
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``TomlFile``.

        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab22f277a63768ddf4f6605743ad2816e10bd46ac73de98867b0f280f8eca01)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly
        if obj is not None:
            self._values["obj"] = obj
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def obj(self) -> typing.Any:
        '''(experimental) The object that will be serialized. You can modify the object's contents before synthesis.

        Serialization of the object is similar to JSON.stringify with few enhancements:

        - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values.
        - ``Set`` will be converted to array
        - ``Map`` will be converted to a plain object ({ key: value, ... }})
        - ``RegExp`` without flags will be converted to string representation of the source

        :default: {} an empty object (use ``file.obj`` to mutate).

        :stability: experimental
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Omits empty objects and arrays.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TomlFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Version(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.Version"):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        *,
        artifacts_directory: builtins.str,
        version_input_file: builtins.str,
        bump_package: typing.Optional[builtins.str] = None,
        next_version_command: typing.Optional[builtins.str] = None,
        releasable_commits: typing.Optional[ReleasableCommits] = None,
        tag_prefix: typing.Optional[builtins.str] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param scope: -
        :param artifacts_directory: (experimental) The name of the directory into which ``changelog.md`` and ``version.txt`` files are emitted.
        :param version_input_file: (experimental) A name of a .json file to set the ``version`` field in after a bump.
        :param bump_package: (experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string. This can be any compatible package version, including the deprecated ``standard-version@9``. Default: "commit-and-tag-version@12"
        :param next_version_command: (experimental) A shell command to control the next version to release. If present, this shell command will be run before the bump is executed, and it determines what version to release. It will be executed in the following environment: - Working directory: the project directory. - ``$VERSION``: the current version. Looks like ``1.2.3``. - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset. - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``. The command should print one of the following to ``stdout``: - Nothing: the next version number will be determined based on commit history. - ``x.y.z``: the next version number will be ``x.y.z``. - ``major|minor|patch``: the next version number will be the current version number with the indicated component bumped. Default: - The next version will be determined based on the commit history and project settings.
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param tag_prefix: (experimental) The tag prefix corresponding to this version.
        :param versionrc_options: (experimental) Custom configuration for versionrc file used by standard-release.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf64d1b29258435f8a7749178e947fcedd27d55f323782081a21714be909595)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = VersionOptions(
            artifacts_directory=artifacts_directory,
            version_input_file=version_input_file,
            bump_package=bump_package,
            next_version_command=next_version_command,
            releasable_commits=releasable_commits,
            tag_prefix=tag_prefix,
            versionrc_options=versionrc_options,
        )

        jsii.create(self.__class__, self, [scope, options])

    @jsii.member(jsii_name="envForBranch")
    def env_for_branch(
        self,
        *,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        minor_version: typing.Optional[jsii.Number] = None,
        prerelease: typing.Optional[builtins.str] = None,
        tag_prefix: typing.Optional[builtins.str] = None,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Return the environment variables to modify the bump command for release branches.

        These options are used to modify the behavior of the version bumping script
        for additional branches, by setting environment variables.

        No settings are inherited from the base ``Version`` object (but any parameters that
        control versions do conflict with the use of a ``nextVersionCommand``).

        :param major_version: (experimental) The major versions released from this branch.
        :param min_major_version: (experimental) The minimum major version to release.
        :param minor_version: (experimental) The minor versions released from this branch.
        :param prerelease: (experimental) Bump the version as a pre-release tag. Default: - normal releases
        :param tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: - no prefix

        :stability: experimental
        '''
        branch_options = VersionBranchOptions(
            major_version=major_version,
            min_major_version=min_major_version,
            minor_version=minor_version,
            prerelease=prerelease,
            tag_prefix=tag_prefix,
        )

        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "envForBranch", [branch_options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STANDARD_VERSION")
    def STANDARD_VERSION(cls) -> builtins.str:
        '''
        :deprecated: use ``version.bumpPackage`` on the component instance instead

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "STANDARD_VERSION"))

    @builtins.property
    @jsii.member(jsii_name="bumpPackage")
    def bump_package(self) -> builtins.str:
        '''(experimental) The package used to bump package versions, as a dependency string.

        This is a ``commit-and-tag-version`` compatible package.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bumpPackage"))

    @builtins.property
    @jsii.member(jsii_name="bumpTask")
    def bump_task(self) -> Task:
        '''
        :stability: experimental
        '''
        return typing.cast(Task, jsii.get(self, "bumpTask"))

    @builtins.property
    @jsii.member(jsii_name="changelogFileName")
    def changelog_file_name(self) -> builtins.str:
        '''(experimental) The name of the changelog file (under ``artifactsDirectory``).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "changelogFileName"))

    @builtins.property
    @jsii.member(jsii_name="releaseTagFileName")
    def release_tag_file_name(self) -> builtins.str:
        '''(experimental) The name of the file that contains the release tag (under ``artifactsDirectory``).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "releaseTagFileName"))

    @builtins.property
    @jsii.member(jsii_name="unbumpTask")
    def unbump_task(self) -> Task:
        '''
        :stability: experimental
        '''
        return typing.cast(Task, jsii.get(self, "unbumpTask"))

    @builtins.property
    @jsii.member(jsii_name="versionFileName")
    def version_file_name(self) -> builtins.str:
        '''(experimental) The name of the file that contains the version (under ``artifactsDirectory``).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "versionFileName"))


@jsii.data_type(
    jsii_type="projen.VersionBranchOptions",
    jsii_struct_bases=[],
    name_mapping={
        "major_version": "majorVersion",
        "min_major_version": "minMajorVersion",
        "minor_version": "minorVersion",
        "prerelease": "prerelease",
        "tag_prefix": "tagPrefix",
    },
)
class VersionBranchOptions:
    def __init__(
        self,
        *,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        minor_version: typing.Optional[jsii.Number] = None,
        prerelease: typing.Optional[builtins.str] = None,
        tag_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to pass to ``modifyBranchEnvironment``.

        :param major_version: (experimental) The major versions released from this branch.
        :param min_major_version: (experimental) The minimum major version to release.
        :param minor_version: (experimental) The minor versions released from this branch.
        :param prerelease: (experimental) Bump the version as a pre-release tag. Default: - normal releases
        :param tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: - no prefix

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62987907aa24cc1b84e9b6e9b755bd286708fa4a219baa7b979fb3ea61401603)
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument min_major_version", value=min_major_version, expected_type=type_hints["min_major_version"])
            check_type(argname="argument minor_version", value=minor_version, expected_type=type_hints["minor_version"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument tag_prefix", value=tag_prefix, expected_type=type_hints["tag_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if major_version is not None:
            self._values["major_version"] = major_version
        if min_major_version is not None:
            self._values["min_major_version"] = min_major_version
        if minor_version is not None:
            self._values["minor_version"] = minor_version
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if tag_prefix is not None:
            self._values["tag_prefix"] = tag_prefix

    @builtins.property
    def major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The major versions released from this branch.

        :stability: experimental
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum major version to release.

        :stability: experimental
        '''
        result = self._values.get("min_major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minor_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minor versions released from this branch.

        :stability: experimental
        '''
        result = self._values.get("minor_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump the version as a pre-release tag.

        :default: - normal releases

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers.

        Note: this prefix is used to detect the latest tagged version
        when bumping, so if you change this on a project with an existing version
        history, you may need to manually tag your latest release
        with the new prefix.

        :default: - no prefix

        :stability: experimental
        '''
        result = self._values.get("tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VersionBranchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.VersionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "artifacts_directory": "artifactsDirectory",
        "version_input_file": "versionInputFile",
        "bump_package": "bumpPackage",
        "next_version_command": "nextVersionCommand",
        "releasable_commits": "releasableCommits",
        "tag_prefix": "tagPrefix",
        "versionrc_options": "versionrcOptions",
    },
)
class VersionOptions:
    def __init__(
        self,
        *,
        artifacts_directory: builtins.str,
        version_input_file: builtins.str,
        bump_package: typing.Optional[builtins.str] = None,
        next_version_command: typing.Optional[builtins.str] = None,
        releasable_commits: typing.Optional[ReleasableCommits] = None,
        tag_prefix: typing.Optional[builtins.str] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) Options for ``Version``.

        :param artifacts_directory: (experimental) The name of the directory into which ``changelog.md`` and ``version.txt`` files are emitted.
        :param version_input_file: (experimental) A name of a .json file to set the ``version`` field in after a bump.
        :param bump_package: (experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string. This can be any compatible package version, including the deprecated ``standard-version@9``. Default: "commit-and-tag-version@12"
        :param next_version_command: (experimental) A shell command to control the next version to release. If present, this shell command will be run before the bump is executed, and it determines what version to release. It will be executed in the following environment: - Working directory: the project directory. - ``$VERSION``: the current version. Looks like ``1.2.3``. - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset. - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``. The command should print one of the following to ``stdout``: - Nothing: the next version number will be determined based on commit history. - ``x.y.z``: the next version number will be ``x.y.z``. - ``major|minor|patch``: the next version number will be the current version number with the indicated component bumped. Default: - The next version will be determined based on the commit history and project settings.
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param tag_prefix: (experimental) The tag prefix corresponding to this version.
        :param versionrc_options: (experimental) Custom configuration for versionrc file used by standard-release.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb94d39bdc04d188bb2447acba8747de3d6ec275231c8a512d647916d69a54f5)
            check_type(argname="argument artifacts_directory", value=artifacts_directory, expected_type=type_hints["artifacts_directory"])
            check_type(argname="argument version_input_file", value=version_input_file, expected_type=type_hints["version_input_file"])
            check_type(argname="argument bump_package", value=bump_package, expected_type=type_hints["bump_package"])
            check_type(argname="argument next_version_command", value=next_version_command, expected_type=type_hints["next_version_command"])
            check_type(argname="argument releasable_commits", value=releasable_commits, expected_type=type_hints["releasable_commits"])
            check_type(argname="argument tag_prefix", value=tag_prefix, expected_type=type_hints["tag_prefix"])
            check_type(argname="argument versionrc_options", value=versionrc_options, expected_type=type_hints["versionrc_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifacts_directory": artifacts_directory,
            "version_input_file": version_input_file,
        }
        if bump_package is not None:
            self._values["bump_package"] = bump_package
        if next_version_command is not None:
            self._values["next_version_command"] = next_version_command
        if releasable_commits is not None:
            self._values["releasable_commits"] = releasable_commits
        if tag_prefix is not None:
            self._values["tag_prefix"] = tag_prefix
        if versionrc_options is not None:
            self._values["versionrc_options"] = versionrc_options

    @builtins.property
    def artifacts_directory(self) -> builtins.str:
        '''(experimental) The name of the directory into which ``changelog.md`` and ``version.txt`` files are emitted.

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        assert result is not None, "Required property 'artifacts_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_input_file(self) -> builtins.str:
        '''(experimental) A name of a .json file to set the ``version`` field in after a bump.

        :stability: experimental

        Example::

            "package.json"
        '''
        result = self._values.get("version_input_file")
        assert result is not None, "Required property 'version_input_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bump_package(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string.

        This can be any compatible package version, including the deprecated ``standard-version@9``.

        :default: "commit-and-tag-version@12"

        :stability: experimental
        '''
        result = self._values.get("bump_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_version_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command to control the next version to release.

        If present, this shell command will be run before the bump is executed, and
        it determines what version to release. It will be executed in the following
        environment:

        - Working directory: the project directory.
        - ``$VERSION``: the current version. Looks like ``1.2.3``.
        - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset.
        - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``.

        The command should print one of the following to ``stdout``:

        - Nothing: the next version number will be determined based on commit history.
        - ``x.y.z``: the next version number will be ``x.y.z``.
        - ``major|minor|patch``: the next version number will be the current version number
          with the indicated component bumped.

        :default: - The next version will be determined based on the commit history and project settings.

        :stability: experimental
        '''
        result = self._values.get("next_version_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def releasable_commits(self) -> typing.Optional[ReleasableCommits]:
        '''(experimental) Find commits that should be considered releasable Used to decide if a release is required.

        :default: ReleasableCommits.everyCommit()

        :stability: experimental
        '''
        result = self._values.get("releasable_commits")
        return typing.cast(typing.Optional[ReleasableCommits], result)

    @builtins.property
    def tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The tag prefix corresponding to this version.

        :stability: experimental
        '''
        result = self._values.get("tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def versionrc_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Custom configuration for versionrc file used by standard-release.

        :stability: experimental
        '''
        result = self._values.get("versionrc_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VersionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class XmlFile(ObjectFile, metaclass=jsii.JSIIMeta, jsii_type="projen.XmlFile"):
    '''(experimental) Represents an XML file.

    Objects passed in will be synthesized using the npm "xml" library.

    :see: https://www.npmjs.com/package/xml
    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        file_path: builtins.str,
        *,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param file_path: -
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5b690e903db052918d05a559c63588dd937691c1a431dfac231627b8e528e8)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = XmlFileOptions(
            obj=obj,
            omit_empty=omit_empty,
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [project, file_path, options])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, resolver: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2692cc4c7fb6801f048a0fa351a11b924d2fc1bc8cbe476af5597cd65143cbd6)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))


@jsii.data_type(
    jsii_type="projen.XmlFileOptions",
    jsii_struct_bases=[ObjectFileOptions],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
        "obj": "obj",
        "omit_empty": "omitEmpty",
    },
)
class XmlFileOptions(ObjectFileOptions):
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``XmlFile``.

        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca47b496952cf7e3231ef829693ea86ffea84f642882cd1bff5b5dedd4c31175)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly
        if obj is not None:
            self._values["obj"] = obj
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def obj(self) -> typing.Any:
        '''(experimental) The object that will be serialized. You can modify the object's contents before synthesis.

        Serialization of the object is similar to JSON.stringify with few enhancements:

        - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values.
        - ``Set`` will be converted to array
        - ``Map`` will be converted to a plain object ({ key: value, ... }})
        - ``RegExp`` without flags will be converted to string representation of the source

        :default: {} an empty object (use ``file.obj`` to mutate).

        :stability: experimental
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Omits empty objects and arrays.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "XmlFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class YamlFile(ObjectFile, metaclass=jsii.JSIIMeta, jsii_type="projen.YamlFile"):
    '''(experimental) Represents a YAML file.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        file_path: builtins.str,
        *,
        line_width: typing.Optional[jsii.Number] = None,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param file_path: -
        :param line_width: (experimental) Maximum line width (set to 0 to disable folding). Default: - 0
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af86e1db34b2981edd2efebaba099732281c104959fb2bbb34db7c78208f5e26)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = YamlFileOptions(
            line_width=line_width,
            obj=obj,
            omit_empty=omit_empty,
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [scope, file_path, options])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, resolver: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed453f41109a767cb068d726b9448c3545059d1161f0785da668afdd21e36069)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))

    @builtins.property
    @jsii.member(jsii_name="lineWidth")
    def line_width(self) -> jsii.Number:
        '''(experimental) Maximum line width (set to 0 to disable folding).

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "lineWidth"))

    @line_width.setter
    def line_width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48f409d84ffd5e2a23ba998b62ea6bdf1343878ddf6bbdba39669e9e45b8464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lineWidth", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="projen.YamlFileOptions",
    jsii_struct_bases=[ObjectFileOptions],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
        "obj": "obj",
        "omit_empty": "omitEmpty",
        "line_width": "lineWidth",
    },
)
class YamlFileOptions(ObjectFileOptions):
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
        line_width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for ``JsonFile``.

        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param line_width: (experimental) Maximum line width (set to 0 to disable folding). Default: - 0

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9e5a70f67f8e3db454227249c58dd5464be1446a55fcf3be780621fded1638)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly
        if obj is not None:
            self._values["obj"] = obj
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty
        if line_width is not None:
            self._values["line_width"] = line_width

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def obj(self) -> typing.Any:
        '''(experimental) The object that will be serialized. You can modify the object's contents before synthesis.

        Serialization of the object is similar to JSON.stringify with few enhancements:

        - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values.
        - ``Set`` will be converted to array
        - ``Map`` will be converted to a plain object ({ key: value, ... }})
        - ``RegExp`` without flags will be converted to string representation of the source

        :default: {} an empty object (use ``file.obj`` to mutate).

        :stability: experimental
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Omits empty objects and arrays.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum line width (set to 0 to disable folding).

        :default: - 0

        :stability: experimental
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YamlFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.Dependency",
    jsii_struct_bases=[DependencyCoordinates],
    name_mapping={
        "name": "name",
        "version": "version",
        "type": "type",
        "metadata": "metadata",
    },
)
class Dependency(DependencyCoordinates):
    def __init__(
        self,
        *,
        name: builtins.str,
        version: typing.Optional[builtins.str] = None,
        type: DependencyType,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) Represents a project dependency.

        :param name: (experimental) The package manager name of the dependency (e.g. ``leftpad`` for npm). NOTE: For package managers that use complex coordinates (like Maven), we will codify it into a string somehow.
        :param version: (experimental) Semantic version version requirement. Default: - requirement is managed by the package manager (e.g. npm/yarn).
        :param type: (experimental) Which type of dependency this is (runtime, build-time, etc).
        :param metadata: (experimental) Additional JSON metadata associated with the dependency (package manager specific). Default: {}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a39137d5e4f9c51c84e6a659a0e0d16c23ba1927ed8fe7f3f96ecd5d0110dc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if version is not None:
            self._values["version"] = version
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The package manager name of the dependency (e.g. ``leftpad`` for npm).

        NOTE: For package managers that use complex coordinates (like Maven), we
        will codify it into a string somehow.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Semantic version version requirement.

        :default: - requirement is managed by the package manager (e.g. npm/yarn).

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> DependencyType:
        '''(experimental) Which type of dependency this is (runtime, build-time, etc).

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(DependencyType, result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional JSON metadata associated with the dependency (package manager specific).

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Dependency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDockerComposeServiceName)
class DockerComposeService(
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.DockerComposeService",
):
    '''(experimental) A docker-compose service.

    :stability: experimental
    '''

    def __init__(
        self,
        service_name: builtins.str,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        depends_on: typing.Optional[typing.Sequence[IDockerComposeServiceName]] = None,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        image_build: typing.Optional[typing.Union[DockerComposeBuild, typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        networks: typing.Optional[typing.Sequence[IDockerComposeNetworkBinding]] = None,
        platform: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Sequence[typing.Union[DockerComposeServicePort, typing.Dict[builtins.str, typing.Any]]]] = None,
        privileged: typing.Optional[builtins.bool] = None,
        volumes: typing.Optional[typing.Sequence[IDockerComposeVolumeBinding]] = None,
    ) -> None:
        '''
        :param service_name: The name of the docker compose service.
        :param command: (experimental) Provide a command to the docker container. Default: - use the container's default command
        :param depends_on: (experimental) Names of other services this service depends on. Default: - no dependencies
        :param entrypoint: (experimental) Entrypoint to run in the container.
        :param environment: (experimental) Add environment variables. Default: - no environment variables are provided
        :param image: (experimental) Use a docker image. Note: You must specify either ``build`` or ``image`` key.
        :param image_build: (experimental) Build a docker image. Note: You must specify either ``imageBuild`` or ``image`` key.
        :param labels: (experimental) Add labels. Default: - no labels are provided
        :param networks: (experimental) Add some networks to the service.
        :param platform: (experimental) Add platform. Default: - no platform is provided
        :param ports: (experimental) Map some ports. Default: - no ports are mapped
        :param privileged: (experimental) Run in privileged mode. Default: - no privileged mode flag is provided
        :param volumes: (experimental) Mount some volumes into the service. Use one of the following to create volumes:

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30adb261bc3a7558152dddf9acb47c2b326de589312d32dcb84afc10909eaa49)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        service_description = DockerComposeServiceDescription(
            command=command,
            depends_on=depends_on,
            entrypoint=entrypoint,
            environment=environment,
            image=image,
            image_build=image_build,
            labels=labels,
            networks=networks,
            platform=platform,
            ports=ports,
            privileged=privileged,
            volumes=volumes,
        )

        jsii.create(self.__class__, self, [service_name, service_description])

    @jsii.member(jsii_name="addDependsOn")
    def add_depends_on(self, service_name: IDockerComposeServiceName) -> None:
        '''(experimental) Make the service depend on another service.

        :param service_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ff43023f997f5472eb87eb69dd00d7be9ea937c60e0ee2901649769a7058d2)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        return typing.cast(None, jsii.invoke(self, "addDependsOn", [service_name]))

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Add an environment variable.

        :param name: environment variable name.
        :param value: value of the environment variable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20e959d624b3b1127206bf0505435f464e2dd4b499a9de78ae5b62f3768de8b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addEnvironment", [name, value]))

    @jsii.member(jsii_name="addLabel")
    def add_label(self, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Add a label.

        :param name: environment variable name.
        :param value: value of the environment variable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66ccd81821843eafa497e58cc72c82e90c73c8303d8b59878daf25c4e8e1b6f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addLabel", [name, value]))

    @jsii.member(jsii_name="addNetwork")
    def add_network(self, network: IDockerComposeNetworkBinding) -> None:
        '''(experimental) Add a network to the service.

        :param network: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86c0a8aae5342390c599726fd2da4ac1905227de386cc7023bd3614ed2f628b)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        return typing.cast(None, jsii.invoke(self, "addNetwork", [network]))

    @jsii.member(jsii_name="addPort")
    def add_port(
        self,
        published_port: jsii.Number,
        target_port: jsii.Number,
        *,
        protocol: typing.Optional[DockerComposeProtocol] = None,
    ) -> None:
        '''(experimental) Add a port mapping.

        :param published_port: Published port number.
        :param target_port: Container's port number.
        :param protocol: (experimental) Port mapping protocol. Default: DockerComposeProtocol.TCP

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28bd4f8327dce6303d35aa47ba8a52745ed9e16a768727fac813952ae557cdaf)
            check_type(argname="argument published_port", value=published_port, expected_type=type_hints["published_port"])
            check_type(argname="argument target_port", value=target_port, expected_type=type_hints["target_port"])
        options = DockerComposePortMappingOptions(protocol=protocol)

        return typing.cast(None, jsii.invoke(self, "addPort", [published_port, target_port, options]))

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, volume: IDockerComposeVolumeBinding) -> None:
        '''(experimental) Add a volume to the service.

        :param volume: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c149f3c3feafe7a16b339d4f946067d127836eda10279b26447013ec075193ed)
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        return typing.cast(None, jsii.invoke(self, "addVolume", [volume]))

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.List[IDockerComposeServiceName]:
        '''(experimental) Other services that this service depends on.

        :stability: experimental
        '''
        return typing.cast(typing.List[IDockerComposeServiceName], jsii.get(self, "dependsOn"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Environment variables.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Attached labels.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> typing.List[IDockerComposeNetworkBinding]:
        '''(experimental) Networks mounted in the container.

        :stability: experimental
        '''
        return typing.cast(typing.List[IDockerComposeNetworkBinding], jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[DockerComposeServicePort]:
        '''(experimental) Published ports.

        :stability: experimental
        '''
        return typing.cast(typing.List[DockerComposeServicePort], jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''(experimental) Name of the service.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[IDockerComposeVolumeBinding]:
        '''(experimental) Volumes mounted in the container.

        :stability: experimental
        '''
        return typing.cast(typing.List[IDockerComposeVolumeBinding], jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Command to run in the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Entrypoint to run in the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entrypoint"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docker image.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="imageBuild")
    def image_build(self) -> typing.Optional[DockerComposeBuild]:
        '''(experimental) Docker image build instructions.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[DockerComposeBuild], jsii.get(self, "imageBuild"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> typing.Optional[builtins.str]:
        '''(experimental) Target platform.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run in privileged mode.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "privileged"))


@jsii.implements(IDevEnvironment)
class Gitpod(Component, metaclass=jsii.JSIIMeta, jsii_type="projen.Gitpod"):
    '''(experimental) The Gitpod component which emits .gitpod.yml.

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        *,
        prebuilds: typing.Optional[typing.Union[GitpodPrebuilds, typing.Dict[builtins.str, typing.Any]]] = None,
        docker_image: typing.Optional[DevEnvironmentDockerImage] = None,
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        tasks: typing.Optional[typing.Sequence[Task]] = None,
        vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param project: -
        :param prebuilds: (experimental) Optional Gitpod's Github App integration for prebuilds If this is not set and Gitpod's Github App is installed, then Gitpod will apply these defaults: https://www.gitpod.io/docs/prebuilds/#configure-the-github-app. Default: undefined
        :param docker_image: (experimental) A Docker image or Dockerfile for the container.
        :param ports: (experimental) An array of ports that should be exposed from the container.
        :param tasks: (experimental) An array of tasks that should be run when the container starts.
        :param vscode_extensions: (experimental) An array of extension IDs that specify the extensions that should be installed inside the container when it is created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21675c9752472f446f36533458bc020deb11343e29b63f990c190823733a1404)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = GitpodOptions(
            prebuilds=prebuilds,
            docker_image=docker_image,
            ports=ports,
            tasks=tasks,
            vscode_extensions=vscode_extensions,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addCustomTask")
    def add_custom_task(
        self,
        *,
        command: builtins.str,
        before: typing.Optional[builtins.str] = None,
        init: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        open_in: typing.Optional[GitpodOpenIn] = None,
        open_mode: typing.Optional[GitpodOpenMode] = None,
        prebuild: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a task with more granular options.

        By default, all tasks will be run in parallel. To run tasks in sequence,
        create a new ``Task`` and set the other tasks as subtasks.

        :param command: (experimental) Required. The shell command to run
        :param before: (experimental) In case you need to run something even before init, that is a requirement for both init and command, you can use the before property.
        :param init: (experimental) The init property can be used to specify shell commands that should only be executed after a workspace was freshly cloned and needs to be initialized somehow. Such tasks are usually builds or downloading dependencies. Anything you only want to do once but not when you restart a workspace or start a snapshot.
        :param name: (experimental) A name for this task. Default: - task names are omitted when blank
        :param open_in: (experimental) You can configure where in the IDE the terminal should be opened. Default: GitpodOpenIn.BOTTOM
        :param open_mode: (experimental) You can configure how the terminal should be opened relative to the previous task. Default: GitpodOpenMode.TAB_AFTER
        :param prebuild: (experimental) The optional prebuild command will be executed during prebuilds. It is meant to run additional long running processes that could be useful, e.g. running test suites.

        :stability: experimental
        '''
        options = GitpodTask(
            command=command,
            before=before,
            init=init,
            name=name,
            open_in=open_in,
            open_mode=open_mode,
            prebuild=prebuild,
        )

        return typing.cast(None, jsii.invoke(self, "addCustomTask", [options]))

    @jsii.member(jsii_name="addDockerImage")
    def add_docker_image(self, image: DevEnvironmentDockerImage) -> None:
        '''(experimental) Add a custom Docker image or Dockerfile for the container.

        :param image: The Docker image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0520b94b222da42f222b062a87e711f81a8d888cb18100e42bc65273217eece2)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast(None, jsii.invoke(self, "addDockerImage", [image]))

    @jsii.member(jsii_name="addPorts")
    def add_ports(self, *ports: builtins.str) -> None:
        '''(experimental) Add ports that should be exposed (forwarded) from the container.

        :param ports: The new ports.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aadcfbc0f5796128a0688c1a9c0ab6d4e709eae13487757a6c9e31ec724e6c9a)
            check_type(argname="argument ports", value=ports, expected_type=typing.Tuple[type_hints["ports"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPorts", [*ports]))

    @jsii.member(jsii_name="addPrebuilds")
    def add_prebuilds(
        self,
        *,
        add_badge: typing.Optional[builtins.bool] = None,
        add_check: typing.Optional[builtins.bool] = None,
        add_comment: typing.Optional[builtins.bool] = None,
        add_label: typing.Optional[builtins.bool] = None,
        branches: typing.Optional[builtins.bool] = None,
        master: typing.Optional[builtins.bool] = None,
        pull_requests: typing.Optional[builtins.bool] = None,
        pull_requests_from_forks: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Add a prebuilds configuration for the Gitpod App.

        :param add_badge: (experimental) Add a "Review in Gitpod" button to the pull request's description. Default: false
        :param add_check: (experimental) Add a check to pull requests. Default: true
        :param add_comment: (experimental) Add a "Review in Gitpod" button as a comment to pull requests. Default: false
        :param add_label: (experimental) Add a label once the prebuild is ready to pull requests. Default: false
        :param branches: (experimental) Enable for all branches in this repo. Default: false
        :param master: (experimental) Enable for the master/default branch. Default: true
        :param pull_requests: (experimental) Enable for pull requests coming from this repo. Default: true
        :param pull_requests_from_forks: (experimental) Enable for pull requests coming from forks. Default: false

        :stability: experimental
        '''
        config = GitpodPrebuilds(
            add_badge=add_badge,
            add_check=add_check,
            add_comment=add_comment,
            add_label=add_label,
            branches=branches,
            master=master,
            pull_requests=pull_requests,
            pull_requests_from_forks=pull_requests_from_forks,
        )

        return typing.cast(None, jsii.invoke(self, "addPrebuilds", [config]))

    @jsii.member(jsii_name="addTasks")
    def add_tasks(self, *tasks: Task) -> None:
        '''(experimental) Add tasks to run when gitpod starts.

        By default, all tasks will be run in parallel. To run tasks in sequence,
        create a new ``Task`` and specify the other tasks as subtasks.

        :param tasks: The new tasks.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13cdc6c6ab91811936f49718caa7fd070f6c4abe6f48169d00efc3c1b6ff40ff)
            check_type(argname="argument tasks", value=tasks, expected_type=typing.Tuple[type_hints["tasks"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addTasks", [*tasks]))

    @jsii.member(jsii_name="addVscodeExtensions")
    def add_vscode_extensions(self, *extensions: builtins.str) -> None:
        '''(experimental) Add a list of VSCode extensions that should be automatically installed in the container.

        These must be in the format defined in the Open VSX registry.

        :param extensions: The extension IDs.

        :see: https://www.gitpod.io/docs/vscode-extensions/
        :stability: experimental

        Example::

            'scala-lang.scala@0.3.9:O5XmjwY5Gz+0oDZAmqneJw=='
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665d383deec6069f2a514e6afdacc5d1a4416876d520c11c3318ca4c85f91cfb)
            check_type(argname="argument extensions", value=extensions, expected_type=typing.Tuple[type_hints["extensions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addVscodeExtensions", [*extensions]))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Any:
        '''(experimental) Direct access to the gitpod configuration (escape hatch).

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "config"))


class IniFile(ObjectFile, metaclass=jsii.JSIIMeta, jsii_type="projen.IniFile"):
    '''(experimental) Represents an INI file.

    :stability: experimental
    '''

    def __init__(
        self,
        project: Project,
        file_path: builtins.str,
        *,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param file_path: -
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbd31798d0e0c9e35dbbc5085bcb67cd656717ccca79896838efc097963c5ea)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = IniFileOptions(
            obj=obj,
            omit_empty=omit_empty,
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [project, file_path, options])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, resolver: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9199eb11888c254ab59f6b5e5411b6921139de20f66c995fc90a33542e20693)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))


@jsii.data_type(
    jsii_type="projen.IniFileOptions",
    jsii_struct_bases=[ObjectFileOptions],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
        "obj": "obj",
        "omit_empty": "omitEmpty",
    },
)
class IniFileOptions(ObjectFileOptions):
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``IniFile``.

        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c292bd0cc5c248be03f2bad019458df0920a1b2f21b8d18cfb340489994ca61)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly
        if obj is not None:
            self._values["obj"] = obj
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def obj(self) -> typing.Any:
        '''(experimental) The object that will be serialized. You can modify the object's contents before synthesis.

        Serialization of the object is similar to JSON.stringify with few enhancements:

        - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values.
        - ``Set`` will be converted to array
        - ``Map`` will be converted to a plain object ({ key: value, ... }})
        - ``RegExp`` without flags will be converted to string representation of the source

        :default: {} an empty object (use ``file.obj`` to mutate).

        :stability: experimental
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Omits empty objects and arrays.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IniFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JsonFile(ObjectFile, metaclass=jsii.JSIIMeta, jsii_type="projen.JsonFile"):
    '''(experimental) Represents a JSON file.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        file_path: builtins.str,
        *,
        allow_comments: typing.Optional[builtins.bool] = None,
        newline: typing.Optional[builtins.bool] = None,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param file_path: -
        :param allow_comments: (experimental) Allow the use of comments in this file. Default: - false for .json files, true for .json5 and .jsonc files
        :param newline: (experimental) Adds a newline at the end of the file. Default: true
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b2200943f9f1c3d7452e66283d201e06e67715a6a56548aa31d93f9dc511ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = JsonFileOptions(
            allow_comments=allow_comments,
            newline=newline,
            obj=obj,
            omit_empty=omit_empty,
            committed=committed,
            edit_gitignore=edit_gitignore,
            executable=executable,
            marker=marker,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [scope, file_path, options])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(self, resolver: IResolver) -> typing.Optional[builtins.str]:
        '''(experimental) Implemented by derived classes and returns the contents of the file to emit.

        :param resolver: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ec13937bd2fb6b7d1a296b25576844e3d9ad24f7864fc43e5f8777adcb73c5)
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [resolver]))

    @builtins.property
    @jsii.member(jsii_name="supportsComments")
    def supports_comments(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsComments"))


@jsii.data_type(
    jsii_type="projen.JsonFileOptions",
    jsii_struct_bases=[ObjectFileOptions],
    name_mapping={
        "committed": "committed",
        "edit_gitignore": "editGitignore",
        "executable": "executable",
        "marker": "marker",
        "readonly": "readonly",
        "obj": "obj",
        "omit_empty": "omitEmpty",
        "allow_comments": "allowComments",
        "newline": "newline",
    },
)
class JsonFileOptions(ObjectFileOptions):
    def __init__(
        self,
        *,
        committed: typing.Optional[builtins.bool] = None,
        edit_gitignore: typing.Optional[builtins.bool] = None,
        executable: typing.Optional[builtins.bool] = None,
        marker: typing.Optional[builtins.bool] = None,
        readonly: typing.Optional[builtins.bool] = None,
        obj: typing.Any = None,
        omit_empty: typing.Optional[builtins.bool] = None,
        allow_comments: typing.Optional[builtins.bool] = None,
        newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for ``JsonFile``.

        :param committed: (experimental) Indicates whether this file should be committed to git or ignored. By default, all generated files are committed and anti-tamper is used to protect against manual modifications. Default: true
        :param edit_gitignore: (experimental) Update the project's .gitignore file. Default: true
        :param executable: (experimental) Whether the generated file should be marked as executable. Default: false
        :param marker: (experimental) Adds the projen marker to the file. Default: - marker will be included as long as the project is not ejected
        :param readonly: (experimental) Whether the generated file should be readonly. Default: true
        :param obj: (experimental) The object that will be serialized. You can modify the object's contents before synthesis. Serialization of the object is similar to JSON.stringify with few enhancements: - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values. - ``Set`` will be converted to array - ``Map`` will be converted to a plain object ({ key: value, ... }}) - ``RegExp`` without flags will be converted to string representation of the source Default: {} an empty object (use ``file.obj`` to mutate).
        :param omit_empty: (experimental) Omits empty objects and arrays. Default: false
        :param allow_comments: (experimental) Allow the use of comments in this file. Default: - false for .json files, true for .json5 and .jsonc files
        :param newline: (experimental) Adds a newline at the end of the file. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13520dccfc7567565533a60eb68d854a29a519fa88a2a00e2abe76dd2578046e)
            check_type(argname="argument committed", value=committed, expected_type=type_hints["committed"])
            check_type(argname="argument edit_gitignore", value=edit_gitignore, expected_type=type_hints["edit_gitignore"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument marker", value=marker, expected_type=type_hints["marker"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
            check_type(argname="argument omit_empty", value=omit_empty, expected_type=type_hints["omit_empty"])
            check_type(argname="argument allow_comments", value=allow_comments, expected_type=type_hints["allow_comments"])
            check_type(argname="argument newline", value=newline, expected_type=type_hints["newline"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if committed is not None:
            self._values["committed"] = committed
        if edit_gitignore is not None:
            self._values["edit_gitignore"] = edit_gitignore
        if executable is not None:
            self._values["executable"] = executable
        if marker is not None:
            self._values["marker"] = marker
        if readonly is not None:
            self._values["readonly"] = readonly
        if obj is not None:
            self._values["obj"] = obj
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty
        if allow_comments is not None:
            self._values["allow_comments"] = allow_comments
        if newline is not None:
            self._values["newline"] = newline

    @builtins.property
    def committed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this file should be committed to git or ignored.

        By
        default, all generated files are committed and anti-tamper is used to
        protect against manual modifications.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("committed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edit_gitignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Update the project's .gitignore file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("edit_gitignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def executable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be marked as executable.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def marker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the projen marker to the file.

        :default: - marker will be included as long as the project is not ejected

        :stability: experimental
        '''
        result = self._values.get("marker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the generated file should be readonly.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def obj(self) -> typing.Any:
        '''(experimental) The object that will be serialized. You can modify the object's contents before synthesis.

        Serialization of the object is similar to JSON.stringify with few enhancements:

        - values that are functions will be called during synthesis and the result will be serialized - this allow to have lazy values.
        - ``Set`` will be converted to array
        - ``Map`` will be converted to a plain object ({ key: value, ... }})
        - ``RegExp`` without flags will be converted to string representation of the source

        :default: {} an empty object (use ``file.obj`` to mutate).

        :stability: experimental
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    @builtins.property
    def omit_empty(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Omits empty objects and arrays.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("omit_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow the use of comments in this file.

        :default: - false for .json files, true for .json5 and .jsonc files

        :stability: experimental
        '''
        result = self._values.get("allow_comments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds a newline at the end of the file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("newline")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsonFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Projenrc(ProjenrcJson, metaclass=jsii.JSIIMeta, jsii_type="projen.Projenrc"):
    '''
    :deprecated: use ``ProjenrcJson``

    :stability: deprecated
    '''

    def __init__(
        self,
        project: Project,
        *,
        filename: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param filename: (experimental) The name of the projenrc file. Default: ".projenrc.json"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3116496b7a7f86911d3f5b5fc2758a136c1b6b18f32ffdb3a80bbd8fe0439914)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = ProjenrcJsonOptions(filename=filename)

        jsii.create(self.__class__, self, [project, options])


@jsii.data_type(
    jsii_type="projen.TaskStep",
    jsii_struct_bases=[TaskStepOptions],
    name_mapping={
        "args": "args",
        "condition": "condition",
        "cwd": "cwd",
        "env": "env",
        "name": "name",
        "receive_args": "receiveArgs",
        "builtin": "builtin",
        "exec": "exec",
        "say": "say",
        "spawn": "spawn",
    },
)
class TaskStep(TaskStepOptions):
    def __init__(
        self,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        condition: typing.Optional[builtins.str] = None,
        cwd: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        receive_args: typing.Optional[builtins.bool] = None,
        builtin: typing.Optional[builtins.str] = None,
        exec: typing.Optional[builtins.str] = None,
        say: typing.Optional[builtins.str] = None,
        spawn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A single step within a task.

        The step could either be  the execution of a
        shell command or execution of a sub-task, by name.

        :param args: (experimental) A list of fixed arguments always passed to the step. Useful to re-use existing tasks without having to re-define the whole task. Fixed args are always passed to the step, even if ``receiveArgs`` is ``false`` and are always passed before any args the task is called with. If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. If the step calls a builtin script, args are passed to the script. It is up to the script to use or discard the arguments. Default: - no arguments are passed to the step
        :param condition: (experimental) A shell command which determines if the this step should be executed. If the program exits with a zero exit code, the step will be executed. A non-zero code means the step will be skipped (subsequent task steps will still be evaluated/executed).
        :param cwd: (experimental) The working directory for this step. Default: - determined by the task
        :param env: (experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only). Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``. Default: - no environment variables defined in step
        :param name: (experimental) Step name. Default: - no name
        :param receive_args: (experimental) Should this step receive args passed to the task. If ``true``, args are passed through at the end of the ``exec`` shell command. The position of the args can be changed by including the marker ``$@`` inside the command string. If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating the whitespace preserving behavior of bash variable expansion. If the step spawns a subtask, args are passed to the subtask. The subtask must define steps receiving args for this to have any effect. Default: false
        :param builtin: (experimental) The name of a built-in task to execute. Built-in tasks are node.js programs baked into the projen module and as component runtime helpers. The name is a path relative to the projen lib/ directory (without the .task.js extension). For example, if your built in builtin task is under ``src/release/resolve-version.task.ts``, then this would be ``release/resolve-version``. Default: - do not execute a builtin task
        :param exec: (experimental) Shell command to execute. Default: - don't execute a shell command
        :param say: (experimental) Print a message. Default: - don't say anything
        :param spawn: (experimental) Subtask to execute. Default: - don't spawn a subtask

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e32d65dbc737f8fd131c5593ecf206bcf2a76757ddb7c5f42945d73058aaae1)
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument cwd", value=cwd, expected_type=type_hints["cwd"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument receive_args", value=receive_args, expected_type=type_hints["receive_args"])
            check_type(argname="argument builtin", value=builtin, expected_type=type_hints["builtin"])
            check_type(argname="argument exec", value=exec, expected_type=type_hints["exec"])
            check_type(argname="argument say", value=say, expected_type=type_hints["say"])
            check_type(argname="argument spawn", value=spawn, expected_type=type_hints["spawn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if args is not None:
            self._values["args"] = args
        if condition is not None:
            self._values["condition"] = condition
        if cwd is not None:
            self._values["cwd"] = cwd
        if env is not None:
            self._values["env"] = env
        if name is not None:
            self._values["name"] = name
        if receive_args is not None:
            self._values["receive_args"] = receive_args
        if builtin is not None:
            self._values["builtin"] = builtin
        if exec is not None:
            self._values["exec"] = exec
        if say is not None:
            self._values["say"] = say
        if spawn is not None:
            self._values["spawn"] = spawn

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of fixed arguments always passed to the step.

        Useful to re-use existing tasks without having to re-define the whole task.
        Fixed args are always passed to the step, even if ``receiveArgs`` is ``false``
        and are always passed before any args the task is called with.

        If the step executes a shell commands, args are passed through at the end of the ``exec`` shell command.
        The position of the args can be changed by including the marker ``$@`` inside the command string.

        If the step spawns a subtask, args are passed to the subtask.
        The subtask must define steps receiving args for this to have any effect.

        If the step calls a builtin script, args are passed to the script.
        It is up to the script to use or discard the arguments.

        :default: - no arguments are passed to the step

        :stability: experimental

        Example::

            task.spawn("deploy", { args: ["--force"] });
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command which determines if the this step should be executed.

        If
        the program exits with a zero exit code, the step will be executed. A non-zero
        code means the step will be skipped (subsequent task steps will still be evaluated/executed).

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cwd(self) -> typing.Optional[builtins.str]:
        '''(experimental) The working directory for this step.

        :default: - determined by the task

        :stability: experimental
        '''
        result = self._values.get("cwd")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Defines environment variables for the execution of this step (``exec`` and ``builtin`` only).

        Values in this map can be simple, literal values or shell expressions that will be evaluated at runtime e.g. ``$(echo "foo")``.

        :default: - no environment variables defined in step

        :stability: experimental

        Example::

            { "foo": "bar", "boo": "$(echo baz)" }
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Step name.

        :default: - no name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def receive_args(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should this step receive args passed to the task.

        If ``true``, args are passed through at the end of the ``exec`` shell command.
        The position of the args can be changed by including the marker ``$@`` inside the command string.

        If the marker is explicitly double-quoted ("$@") arguments will be wrapped in single quotes, approximating
        the whitespace preserving behavior of bash variable expansion.

        If the step spawns a subtask, args are passed to the subtask.
        The subtask must define steps receiving args for this to have any effect.

        :default: false

        :stability: experimental

        Example::

            task.exec("echo Hello $@ World!", { receiveArgs: true });
        '''
        result = self._values.get("receive_args")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def builtin(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of a built-in task to execute.

        Built-in tasks are node.js programs baked into the projen module and as
        component runtime helpers.

        The name is a path relative to the projen lib/ directory (without the .task.js extension).
        For example, if your built in builtin task is under ``src/release/resolve-version.task.ts``,
        then this would be ``release/resolve-version``.

        :default: - do not execute a builtin task

        :stability: experimental
        '''
        result = self._values.get("builtin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exec(self) -> typing.Optional[builtins.str]:
        '''(experimental) Shell command to execute.

        :default: - don't execute a shell command

        :stability: experimental
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def say(self) -> typing.Optional[builtins.str]:
        '''(experimental) Print a message.

        :default: - don't say anything

        :stability: experimental
        '''
        result = self._values.get("say")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spawn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Subtask to execute.

        :default: - don't spawn a subtask

        :stability: experimental
        '''
        result = self._values.get("spawn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Component",
    "CreateProjectOptions",
    "Dependencies",
    "Dependency",
    "DependencyCoordinates",
    "DependencyType",
    "DepsManifest",
    "DevEnvironmentDockerImage",
    "DevEnvironmentOptions",
    "DockerCompose",
    "DockerComposeBuild",
    "DockerComposeNetworkConfig",
    "DockerComposeNetworkIpamConfig",
    "DockerComposeNetworkIpamSubnetConfig",
    "DockerComposePortMappingOptions",
    "DockerComposeProps",
    "DockerComposeProtocol",
    "DockerComposeService",
    "DockerComposeServiceDescription",
    "DockerComposeServicePort",
    "DockerComposeVolumeConfig",
    "DockerComposeVolumeMount",
    "EndOfLine",
    "FileBase",
    "FileBaseOptions",
    "GitAttributesFile",
    "GitAttributesFileOptions",
    "GitOptions",
    "Gitpod",
    "GitpodOnOpen",
    "GitpodOpenIn",
    "GitpodOpenMode",
    "GitpodOptions",
    "GitpodPort",
    "GitpodPortVisibility",
    "GitpodPrebuilds",
    "GitpodTask",
    "GroupRunnerOptions",
    "ICompareString",
    "IDevEnvironment",
    "IDockerComposeNetworkBinding",
    "IDockerComposeNetworkConfig",
    "IDockerComposeServiceName",
    "IDockerComposeVolumeBinding",
    "IDockerComposeVolumeConfig",
    "IResolvable",
    "IResolver",
    "IgnoreFile",
    "IgnoreFileOptions",
    "IniFile",
    "IniFileOptions",
    "InitProject",
    "InitProjectOptionHints",
    "JsonFile",
    "JsonFileOptions",
    "JsonPatch",
    "License",
    "LicenseOptions",
    "LogLevel",
    "Logger",
    "LoggerOptions",
    "Makefile",
    "MakefileOptions",
    "ObjectFile",
    "ObjectFileOptions",
    "Project",
    "ProjectBuild",
    "ProjectOptions",
    "ProjectTree",
    "ProjectType",
    "Projects",
    "Projenrc",
    "ProjenrcFile",
    "ProjenrcJson",
    "ProjenrcJsonOptions",
    "ProjenrcOptions",
    "ReleasableCommits",
    "Renovatebot",
    "RenovatebotOptions",
    "RenovatebotScheduleInterval",
    "ResolveOptions",
    "Rule",
    "SampleDir",
    "SampleDirOptions",
    "SampleFile",
    "SampleFileOptions",
    "SampleReadme",
    "SampleReadmeProps",
    "Semver",
    "SnapshotOptions",
    "SourceCode",
    "SourceCodeOptions",
    "Task",
    "TaskCommonOptions",
    "TaskOptions",
    "TaskRuntime",
    "TaskSpec",
    "TaskStep",
    "TaskStepOptions",
    "Tasks",
    "TasksManifest",
    "TestFailureBehavior",
    "Testing",
    "TextFile",
    "TextFileOptions",
    "TomlFile",
    "TomlFileOptions",
    "Version",
    "VersionBranchOptions",
    "VersionOptions",
    "XmlFile",
    "XmlFileOptions",
    "YamlFile",
    "YamlFileOptions",
    "awscdk",
    "build",
    "cdk",
    "cdk8s",
    "cdktf",
    "circleci",
    "github",
    "gitlab",
    "java",
    "javascript",
    "python",
    "release",
    "typescript",
    "vscode",
    "web",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import awscdk
from . import build
from . import cdk
from . import cdk8s
from . import cdktf
from . import circleci
from . import github
from . import gitlab
from . import java
from . import javascript
from . import python
from . import release
from . import typescript
from . import vscode
from . import web

def _typecheckingstub__e4ee40327ed6d04e3e377e300d915d402c50029248a86452fd19fd6372386d4b(
    scope: _constructs_77d1e7e8.IConstruct,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9d0d027ed125bac76e8d566bfb14795a15c1055686082988040386c4bedd34(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b756505fc1a7b685751d86fb21738eff63b2be7bdec39ba7000083473d5336(
    *,
    dir: builtins.str,
    project_fqn: builtins.str,
    project_options: typing.Mapping[builtins.str, typing.Any],
    option_hints: typing.Optional[InitProjectOptionHints] = None,
    post: typing.Optional[builtins.bool] = None,
    synth: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21c75206d44a727988f2f61c5957c08fb9e7b6843dfc8d7e89642b17409e04b(
    project: Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8cbb5fe28335a2b7b5cb79b4fcdeca39e6f339dea939a6ad73b6a47b495bd1c(
    spec: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee54ffac07e98cfaef250245a5920a70ff038b7635db44aaefe1c9ef634e49a(
    spec: builtins.str,
    type: DependencyType,
    metadata: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3683be12709967dd63dafbe536558d7717d255f3a86dfad1e17c19c9d9185beb(
    name: builtins.str,
    type: typing.Optional[DependencyType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628e50591481575ad249671e7cf61edd1bb37d5aeab5e143a0783051e3167dcc(
    name: builtins.str,
    type: DependencyType,
    expected_range: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4260bbdc4d6b4d5249dbb539f6f4fe1f865c069d0179abe451af2807f194bf7d(
    name: builtins.str,
    type: typing.Optional[DependencyType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0705dd461300a1275ac19f07b173cb3d54d5b40432a75919fe838b828c94f95d(
    name: builtins.str,
    type: typing.Optional[DependencyType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64ddd02bc83dba01b190c70805fc134d208559c5dbe1186f34a86af68e73c9b(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77631e913a8f4e12310c9799410432f0abdd84b99d70b5d3f09a352ce9cec92(
    *,
    dependencies: typing.Sequence[typing.Union[Dependency, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb1f5fb6ea97ef53502fa2942dba716f3c8ed084859934f3db1146f80586fc7(
    docker_file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f197cc85d2f9d6a23d36b30e6b45f48a7c8cdd6998dc4351ad40c3e98ed433(
    image: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f9fbb0608ff35697f2bca0295d53e3ffdf0cc4e15602b3a9e57732048e372a(
    *,
    docker_image: typing.Optional[DevEnvironmentDockerImage] = None,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    tasks: typing.Optional[typing.Sequence[Task]] = None,
    vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befd8e58ddccbbc1a83afe6a4e464b7951ad377df97c7553777909a18eefec9a(
    project: Project,
    *,
    name_suffix: typing.Optional[builtins.str] = None,
    schema_version: typing.Optional[builtins.str] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[DockerComposeServiceDescription, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbde193e2934374214d86400f997cf06d47a8585dd93f52c3a476e5897c5f717(
    source_path: builtins.str,
    target_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaaa9c2706df5a20eae30c6213caaeaedacf3a08430db4d0fd38a0b299c47b6(
    volume_name: builtins.str,
    target_path: builtins.str,
    *,
    driver: typing.Optional[builtins.str] = None,
    driver_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    external: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4d54561cac4572c9face67ceab438aae8d3bbe82eee002cc02eab5cc06adc6(
    network_name: builtins.str,
    *,
    attachable: typing.Optional[builtins.bool] = None,
    bridge: typing.Optional[builtins.bool] = None,
    driver: typing.Optional[builtins.str] = None,
    driver_opts: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
    external: typing.Optional[builtins.bool] = None,
    internal: typing.Optional[builtins.bool] = None,
    ipam: typing.Optional[typing.Union[DockerComposeNetworkIpamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    overlay: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28e8b1e411352eae906d43069127630bff58f30fb830fe48f618d5e1bb92561(
    published_port: jsii.Number,
    target_port: jsii.Number,
    *,
    protocol: typing.Optional[DockerComposeProtocol] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b78d50eb49bb7a7dd6f729eb60da0db3c69b31e910843128de46ce542356481(
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03cd3d199bdbdda7ab3d37e736cec1900b73411477c6a08c6efe431a50bc9b7(
    service_name: builtins.str,
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    depends_on: typing.Optional[typing.Sequence[IDockerComposeServiceName]] = None,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[builtins.str] = None,
    image_build: typing.Optional[typing.Union[DockerComposeBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    networks: typing.Optional[typing.Sequence[IDockerComposeNetworkBinding]] = None,
    platform: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Sequence[typing.Union[DockerComposeServicePort, typing.Dict[builtins.str, typing.Any]]]] = None,
    privileged: typing.Optional[builtins.bool] = None,
    volumes: typing.Optional[typing.Sequence[IDockerComposeVolumeBinding]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec1d86693bd77b64c91103900c6f20c2fda50c12b5d159089260e80ecd89534(
    *,
    context: builtins.str,
    args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    dockerfile: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbd18688d70c5aa20cd294c874f9ad54a013d605cfa3b06afe6935c7b8a0d1e(
    *,
    attachable: typing.Optional[builtins.bool] = None,
    bridge: typing.Optional[builtins.bool] = None,
    driver: typing.Optional[builtins.str] = None,
    driver_opts: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
    external: typing.Optional[builtins.bool] = None,
    internal: typing.Optional[builtins.bool] = None,
    ipam: typing.Optional[typing.Union[DockerComposeNetworkIpamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    overlay: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a79d28871602ad2e3a12572c9bdbe88a19a0cd4514aeea2aa5b801edfcc357(
    *,
    config: typing.Optional[typing.Sequence[typing.Union[DockerComposeNetworkIpamSubnetConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    driver: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbcd82d9063449e5df6ae96f9d244e4622a690f9aef8c482271440a89d10c2e(
    *,
    subnet: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb9ce9a73b268348669bdc9854f34f198e98370c491dd80459bbcb5e10e1a9f(
    *,
    protocol: typing.Optional[DockerComposeProtocol] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b3a9f497a8a34deecb2bf90e8650e81e98e0a4a6480a090f371e2d60385583(
    *,
    name_suffix: typing.Optional[builtins.str] = None,
    schema_version: typing.Optional[builtins.str] = None,
    services: typing.Optional[typing.Mapping[builtins.str, typing.Union[DockerComposeServiceDescription, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7374d6018aac8e9a9098b7b003039b5286a79bcf032fc0db6de3b0c56f496889(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    depends_on: typing.Optional[typing.Sequence[IDockerComposeServiceName]] = None,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[builtins.str] = None,
    image_build: typing.Optional[typing.Union[DockerComposeBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    networks: typing.Optional[typing.Sequence[IDockerComposeNetworkBinding]] = None,
    platform: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Sequence[typing.Union[DockerComposeServicePort, typing.Dict[builtins.str, typing.Any]]]] = None,
    privileged: typing.Optional[builtins.bool] = None,
    volumes: typing.Optional[typing.Sequence[IDockerComposeVolumeBinding]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79390f2bae006141612e4d3816151bd8cf6a9d2bb9d761dce7fbd344d4235193(
    *,
    mode: builtins.str,
    protocol: DockerComposeProtocol,
    published: jsii.Number,
    target: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47648decff569ea19a9be75dee07ad2312da74920b6079ae0b293fedfcad0db3(
    *,
    driver: typing.Optional[builtins.str] = None,
    driver_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    external: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a24a69b1370bfa662e08b21b5f9c5f6da2f1526d8bd7b111c9f8ada371108f2(
    *,
    source: builtins.str,
    target: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cecf514142ea351ec43b0f632ba832e665a18f91b6e46531fd8bb688b82c1b0(
    scope: _constructs_77d1e7e8.IConstruct,
    file_path: builtins.str,
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fed3e4c76496e254ef32ce4556e7e1b3b0cef6929de044486dda20248a06c4d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20fcd33148f053d9de2f2152439cc9f0687a0e328bf05cb8b38721095832ea5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c33cd4fb527e2ef4af066a0254c78d4dd70bed7a8e8cab1f8ec80fb2981c8db(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177d8a347651b29224d730dd6e1bbec48e6dd46e5dcfd4d25e3798e6761d4c63(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a914753a9db7cc6bfa6a166cf7ee02794375210a09b1d8e2c62496abf14b4d21(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    end_of_line: typing.Optional[EndOfLine] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc1d5969ab32878c5548a9a17af7e781548f696676f62cee57518e7f5bf0a66(
    glob: builtins.str,
    *attributes: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3c05c2bc87434261501604cb4ca8386e08b16567b40f693170ab90f635b1a7(
    glob: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d57ceb4d14bb3b3eac67478ac542d99ca5c6994286fdea034dacdf4b64fd14b(
    _: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a54cc3274f754056a1301deb3e7902a7a31057da6ade20b64dae8487831db5(
    *,
    end_of_line: typing.Optional[EndOfLine] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7f1b3b819a95ebdb112752cdc122d5362da95c419decd69ec24018f344bace(
    *,
    end_of_line: typing.Optional[EndOfLine] = None,
    lfs_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1a97c01ec9e70bdd9c3e5a8cfa72f551b923d5d9aded0885f9210b87e09f4b(
    *,
    docker_image: typing.Optional[DevEnvironmentDockerImage] = None,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    tasks: typing.Optional[typing.Sequence[Task]] = None,
    vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    prebuilds: typing.Optional[typing.Union[GitpodPrebuilds, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540294b664aee1f54c7bdb211f5b8781649ae01dfd5e50f7003f34c0689caed2(
    *,
    on_open: typing.Optional[GitpodOnOpen] = None,
    port: typing.Optional[builtins.str] = None,
    visibility: typing.Optional[GitpodPortVisibility] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfddb6f340c3ec20dde7739d66b44371874cbaaec9fdcfe18d77679879dcd633(
    *,
    add_badge: typing.Optional[builtins.bool] = None,
    add_check: typing.Optional[builtins.bool] = None,
    add_comment: typing.Optional[builtins.bool] = None,
    add_label: typing.Optional[builtins.bool] = None,
    branches: typing.Optional[builtins.bool] = None,
    master: typing.Optional[builtins.bool] = None,
    pull_requests: typing.Optional[builtins.bool] = None,
    pull_requests_from_forks: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d426769565bcc27ed394b810bb714ce1978791cfb7442339934c10d450d2ea(
    *,
    command: builtins.str,
    before: typing.Optional[builtins.str] = None,
    init: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    open_in: typing.Optional[GitpodOpenIn] = None,
    open_mode: typing.Optional[GitpodOpenMode] = None,
    prebuild: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3547c7b706a8285f987ddb1847fd162ec961a77abbdd5059da647f1ac25f470(
    *,
    group: builtins.str,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d4f6e150362668f5e26d2f58f8b0a32cff82cf2eb8cb736d2c4333d0b01d09(
    a: builtins.str,
    b: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2360e8cae8e57d0e5268d03b1ee0bcf2a5d56c20a3ca26e5369ddc34c43f0ff(
    image: DevEnvironmentDockerImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045b7fd6b76288f0b95afa207abe899f8baf55cb8bbf6f5d5306b834adb6244e(
    *ports: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0813a7f75b96f7af7cfae60ea14d64e5cb791fa66c8518a184cb1c4ff60850d6(
    *tasks: Task,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782f22994379ab8e59a7f43c2c152f03c7007b57a33bc0e64d609ae60dcc3e6b(
    *extensions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacadabdf1607bf647ddf49c98b96c3cf16b7b3d040c9b172601097c88063780(
    network_config: IDockerComposeNetworkConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f2d0ced589fcb3b848c0452b8213c14d612654118bc3fabd4a9aacb71c2104(
    network_name: builtins.str,
    *,
    attachable: typing.Optional[builtins.bool] = None,
    bridge: typing.Optional[builtins.bool] = None,
    driver: typing.Optional[builtins.str] = None,
    driver_opts: typing.Optional[typing.Mapping[typing.Any, typing.Any]] = None,
    external: typing.Optional[builtins.bool] = None,
    internal: typing.Optional[builtins.bool] = None,
    ipam: typing.Optional[typing.Union[DockerComposeNetworkIpamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    overlay: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8af3d4004c43777e3011a6152f90de4dca16d54781e5922335decd658cd9f63(
    volume_config: IDockerComposeVolumeConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e90cd0baeb3ebbbc34ba2bb279b321337ba3f5a9a97871b5285980fa5ff8f8a(
    volume_name: builtins.str,
    *,
    driver: typing.Optional[builtins.str] = None,
    driver_opts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    external: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fe3f80ba2709a778dd1c7b2c05be66e2342a0284f2ddb2216485cc3fe83203(
    value: typing.Any,
    *,
    args: typing.Optional[typing.Sequence[typing.Any]] = None,
    omit_empty: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b3d1a5dbba38c978da9c5c4f4aab9b9f4b93375021ee84f57a823093ef8c94(
    project: Project,
    file_path: builtins.str,
    *,
    filter_comment_lines: typing.Optional[builtins.bool] = None,
    filter_empty_lines: typing.Optional[builtins.bool] = None,
    ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b1c017f8ecb0e1f37e2212d87d1a1f29ebc301dd9acca79bee88038d4ef761(
    *patterns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b410ec26b2ad71a13a61473568b66bc67bf1526bb5a2c5808dec083cbf6176b(
    *patterns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f4e7958134162324e6e69409537fa18465875eba5b7deb29f1d004349e6e62(
    *patterns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51b5c0b61cdaa2626f46d818be442ab87c3c27477531c08d9cf19b782c8dce1(
    *patterns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853a0f02c9c0f2c598ef8ff7dc57847ef984a42d6d8420b86e11870eb0c92e2d(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7852fd5d8f0daa6070394e45fe4fcb7845e6838dc40a3e3475c057712f4209b9(
    *,
    filter_comment_lines: typing.Optional[builtins.bool] = None,
    filter_empty_lines: typing.Optional[builtins.bool] = None,
    ignore_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e857a70558d977f23eac6a7f43184bde159ec35b45b301dd96f1d6b8649cee(
    *,
    args: typing.Mapping[builtins.str, typing.Any],
    comments: InitProjectOptionHints,
    fqn: builtins.str,
    type: ProjectType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b26148dd49d145c4677c52d5151e359846fa4531669d51a3bda7fc9690796f4(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687d6c08b41e458d121dbe119e3027eab184190021ccd1e7214fe36dc5ec3d0e(
    document: typing.Any,
    *ops: JsonPatch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e382fed98c69b93f0f597e0b66813e26de9d104dbe3bbe734ef8b43fc6f6ef8e(
    from_: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4681b9d716a24a6f5756f57d016e6a0933b4e756c34f3c611bb58e46658c08a1(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2e9da81715d26de45b5095bc71cb7c0b40808d8ac54980865598b8d6ba1f7b(
    from_: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab38d0d4724594f77c44941ab64081b36f9403cc791b13fff2eb1e1e4fe51d1d(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224b5820566457e2e1a5dc60523684f65c081c466561e141aa7a29c5d5058e75(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71ec8f8f1e51ef857d2c433c05eee7cbf90512a0f5cc61e4a5e15606593e0a0(
    path: builtins.str,
    value: typing.Any,
    failure_behavior: typing.Optional[TestFailureBehavior] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9eddbcb68700e35e97b98e5d8b6b5711cc6e2ed4f4f8504c3a3b32c09e21bc0(
    project: Project,
    *,
    spdx: builtins.str,
    copyright_owner: typing.Optional[builtins.str] = None,
    copyright_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfcc75bff8f37fa269835ada3b509dcfbadf621e3ed126a97c08a57ca6956a26(
    _: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95797870e2d83245ce98c839bcaed08b3f74660f792b7401f353e9a8a2cc2e5(
    *,
    spdx: builtins.str,
    copyright_owner: typing.Optional[builtins.str] = None,
    copyright_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033691822a7f7c14e8198bce92b0c93718acf9caa771f8fb20be2afdca76198e(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    level: typing.Optional[LogLevel] = None,
    use_prefix: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9ac41cbd780d7354df3485a4d09a580048a756adf7658209e132d613e93955(
    *text: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab04da100771530f2dcbe37016ca4fd167dcccd81efef96fa9247ea2fc074aa(
    *text: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee83fd3f4ec98a5796ffacb4d4a25bc4de1ab8f597892f06001ac8bc9005dbf5(
    *text: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3de9de18851453b814b6d4aa139849633e68925ada8b935856e8d2779645c4e(
    level: LogLevel,
    *text: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06099b369c462f751aad45c6281b342f061e97a9c63b50dde917bbe345b00f86(
    *text: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833d0f154731bea17dd1954f73c4261d00a48c89b4d8310e383a5320fc447d33(
    *text: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e039718de6580cbf9df271987ee9856640dfc3fbfffb9a8dd894f3c3836384(
    *,
    level: typing.Optional[LogLevel] = None,
    use_prefix: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d8810f927b1ecfbe0b204b373edfe8063aa41c3cc9b476e41d4c74edbf6640(
    project: Project,
    file_path: builtins.str,
    *,
    all: typing.Optional[typing.Sequence[builtins.str]] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[Rule, typing.Dict[builtins.str, typing.Any]]]] = None,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0f2a9f8d0fba8ba4b866f8fae25c27378c12bac9210a7561d3bbc58209e5d0(
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8dca5ea305db0fd9fce16ffe45b1955f7f315de1bc4856adeb92af8ece2de1(
    *targets: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697970c0228a6b747ebd5cf926e4e80e4ec842ca9a26b1dda7d6487e1d098c16(
    *rules: Rule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a3bfee1f24f1bc5e90733d58ecdf92315f7010947140287a5ec79b8a890121(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2336c6183b3596358b6ceeacc7aa7df515fe983a38b754407952b9b0e0d1985(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
    all: typing.Optional[typing.Sequence[builtins.str]] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[Rule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc9aaaac91e385d130a0db14291a598781f43147b9af4a5fdc21398a4bb12e9(
    scope: _constructs_77d1e7e8.IConstruct,
    file_path: builtins.str,
    *,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a738f516b6642d1f5778bc860131390ad6f6d356c899ebcf8aee547c7d46a0e7(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f433242148406c79a8d4d5b0d92a5860a905eff4ee62e43d6ba3e0ee996c9d(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59ab4508f11d1d06be04b3c05be32b4576eb8931fd493503e6f753de128a278(
    path: builtins.str,
    *values: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396760b16d710d570e49cc49d49b73651a49b2122c9872e6b542d85ad67ed154(
    *patches: JsonPatch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1daaba9b52cca530d5e7cb415223e62e8a1067329bc5c65b3a22bf46b5cacff1(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc32648d019ed604ffeabb7df77055facd2d33215e7a019d7e057c323b9ea5ac(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909c95926ec40519379f82a71f83357fca295fd1b4313bec2292dc36d9989698(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614179565fafc11a127479175cc34fe37ef37f3036c908e160bff2998ea1c8ff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb13bbeedf9b4ee7a607b6c974cc57d794730f428181b955df2f6f2fd8da018b(
    *globs: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b195c9c927b524e6c6857987ca398e126176bec5cf796748b7c79133e223e9(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52ded1bd91d1adb42d00140d53c0ea2dfad1f2fc05a340f71711dd214c97dbe(
    _pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb7240461e3476c5778bf65eccdf771a733a6c994c9ab1093bf5302284f6e8d(
    name: builtins.str,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    exec: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
    steps: typing.Optional[typing.Sequence[typing.Union[TaskStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0beed63feccf79f49b05c93c6f457a41e13e37287b4e20c3cb4a68a06a68f3da(
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3f8f3de4a0f7089b9f05f29e319867a4481d3441eff34d4e9f3eab0130ec70(
    _glob: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d6e45e06d8088c7b6e78bb1612a5aa930413dbce990831664c1852b4b50625(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76ed37c3dc6ee85f67899def229da9e34be0fa72867bb3effa9eb30602a6a72(
    task: Task,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70766139ef881860aaf10aeef6ebdb1465d98e99bad4472ae17e63f34c7fd4f(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65eb5e92f4d625ac2145ddbfa1b0e23e3eac098ec0084123d40298e71d45dac(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb95b1525dde337216151338c677538f9fef8920e8ec9c6f33444b7f936f545(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d37a5c5825b9b3d7ff7498ac7929ccb4efdb7a4d051b9f355807df9f244105(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bda3bf4e486437808f86825b7c514ecdc1487047c8a912a8ec695f6c7994008(
    project: Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef7d6448b98c56283c32249b27775d5b609a52bab9bec1934494e170ed4b829(
    *,
    name: builtins.str,
    commit_generated: typing.Optional[builtins.bool] = None,
    git_ignore_options: typing.Optional[typing.Union[IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    parent: typing.Optional[Project] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d641368026b1d886dc04897d3f5cd3c6f816493615fd3c987eaf69bd626aa1(
    project: Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1d331084783b1e11404a33c550a54f472b9e2d656ca02bdc7287828f96e2fb(
    value: JsonFile,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eceaec699c352362ccbd6e243d30a2e6cb72fca16183fc6917e8140a42c29f57(
    scope: _constructs_77d1e7e8.IConstruct,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b101e9a16bb1d0770a9bdccfb59eaa94698a351261b5ec4e3d5265acaba298(
    project: Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f15d342ae05206d72b7818258b15e3fe0c8d8a752a91c55d215d8b0483dc139(
    project: Project,
    *,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a99955e971461d6a1a22bde13c0353d22c81866a29b67be950a0e26b50c76d(
    *,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e65c016c9638462ddcfa91c71dec3094782bd55bb80eb39df93ca1b9caee431(
    *,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1cb2a20764c493021a975dc66d097be2a86987ccece8a4e9aeb51464a695829(
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae99067556dc4317fa46683f512786bc803178cc26b794688b734aad677d6ad5(
    cmd: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed5698324356b7a6f65c5e830a0b241b450786bb6c44a17c68cd21fff2ec2ec(
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4efcc2d3340114e5856cdafe45dc717452519355cde39b8c2e63eab5217db1a(
    types: typing.Sequence[builtins.str],
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c46f6c8bc57788436baf6da521f9e5812106db6aa16bda9534549c8cbb078d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096e7567a3344884436d387a9f887ed96b3691c6d8ad217be945ed3e697ca2cf(
    project: Project,
    *,
    ignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_projen: typing.Optional[builtins.bool] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    marker: typing.Optional[builtins.bool] = None,
    override_config: typing.Any = None,
    schedule_interval: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567099b4941210c2f0eb5a6df45f4f8e145db210a75dd2f52fb480378619c263(
    *,
    ignore: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_projen: typing.Optional[builtins.bool] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    marker: typing.Optional[builtins.bool] = None,
    override_config: typing.Any = None,
    schedule_interval: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4b97f8ab65df023c8b871bd346713f10c0be9a3c56164ff8daff235b29f110(
    *,
    args: typing.Optional[typing.Sequence[typing.Any]] = None,
    omit_empty: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960ffc3506d59d9b0342960ce1ae8b57e2e9b37cb7952b5c51fec42ee1db4e8d(
    *,
    targets: typing.Sequence[builtins.str],
    phony: typing.Optional[builtins.bool] = None,
    prerequisites: typing.Optional[typing.Sequence[builtins.str]] = None,
    recipe: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8efbed63e76d887e28111eeef32b09ef5633f3c345fcb30e0eb79de9bd55ffb(
    project: Project,
    dir: builtins.str,
    *,
    files: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    source_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2420e1173ef03c68a422bbb8b53d09247201a8bd5ac9f6c245970ba305bf520d(
    *,
    files: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    source_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a38a2fea275113276771eaf46e063f6071707e4fb2f0de49701eed613022f428(
    project: Project,
    file_path: builtins.str,
    *,
    contents: typing.Optional[builtins.str] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5983842fe223283a82b203e95c2a76bc065a8b8aa52dea3a7881cc3cdd6d6b77(
    *,
    contents: typing.Optional[builtins.str] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b9334bb06e21e4e396e8da950bd8d70131a947f97c3cdf330b355dd060b814(
    project: Project,
    *,
    contents: typing.Optional[builtins.str] = None,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77957e29d490dd06dbcef8d6f6f12b818295fcdd57ba6e23c2f47a789f6bd686(
    *,
    contents: typing.Optional[builtins.str] = None,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882a814624f99ac08715fce7fc18a428ae23a52ec698a5ebec9e072a6d4bee7b(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08be6ee4b9a3cf93d50853ebba8a8bec4e9ba922550d4990871f38e90d2202c(
    spec: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc51091a63dc9aed397af0467d8120c4946b43f9c07bf576f1e7f9c0a7c1670(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf95810f46ca22192ebf45b7182c9dc075240639ad5062da86d9cc145589b8a1(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4033d52c0dc0e7955fb3f2d24e186e7b85bc74bcaf036fc11fbd959c943d9dba(
    *,
    parse_json: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8be88cd766883f8907162beaca5942a5ced596ef64437b757913e47b609893(
    project: Project,
    file_path: builtins.str,
    *,
    indent: typing.Optional[jsii.Number] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34003984aac9d3e3b9389175974e6c6b74f7d3d41d56ac43f84a68412f1cccaa(
    code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8562757d443bf862879e9dc7708fb5fa5d0f9c2d6ad2598ee2c3edeb96e7f616(
    code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bc8a0529aa4ca39c77add345ebadba429d8974597a851741ec0cd4046f1a20(
    code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c604ba47f53eeef393d736d7b829dae144b7a43fad8affb927e7859a46ac29(
    *,
    indent: typing.Optional[jsii.Number] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679ed15034b92ce65671fe4889a8e0476b00d6023000c4f1035f69d18ac8760c(
    name: builtins.str,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    exec: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
    steps: typing.Optional[typing.Sequence[typing.Union[TaskStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248e4e99078602a3b8e376c73fa93425e082239549a245989641e2097a64972a(
    *condition: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9dd10fb1b2c8242826790d7b14e14f641c34ec35695d12b425f283a93b972f(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e0e7093de18a072e3935f8026bebc9b7916011f0d592178810d5f53451f027(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866645d9e72b430281a892f9aec648a8a4d11dfd83393ea8d1cf161c619f40ce(
    command: builtins.str,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45a21d1f9e615dd1b225d6cafbe381a43b42811d1d21efd5a3f6630613e94af(
    index: jsii.Number,
    *steps: TaskStep,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72dcbc585fdab7a308274ba33cb7b5bcf9e106aaf01bef404fbb15b6c60db4c4(
    shell: builtins.str,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6303cc71c3e6fb4aba7cadb07d20f36a327564e7e91f7baf72d0bb511b02f9d8(
    shell: builtins.str,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e687ef928f97e72aa2e81b8d6d9eb6d68cfdfb3063bfbd3f8c9e4ea8177cf5(
    message: builtins.str,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80be0ec2af5c5b034b9ad26a372663b2dede8547b402f7501bd174f174db2d3a(
    subtask: Task,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c493ae53dba9513da0ecb434448ff6e7d3050c90456d373f1135a865eedb69c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec2ab04da022f328e54a5747cb659465473a80e61ea4b23af06f41a51eaf8a8(
    command: typing.Optional[builtins.str] = None,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da16e7abde21673795e791b1dc02e7b9c04503d828a84a24ad2e0950514f3d1(
    message: builtins.str,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30afd72afdc7d9e0229d01ea2f502a330dca643bfa30b79876a78ec24110ee41(
    subtask: Task,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6471d9b24a42d1138efa839e893cd7685a703235152ad4f0c3aae00e2e12f8(
    index: jsii.Number,
    *,
    builtin: typing.Optional[builtins.str] = None,
    exec: typing.Optional[builtins.str] = None,
    say: typing.Optional[builtins.str] = None,
    spawn: typing.Optional[builtins.str] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063f23ecf0aa952acdfe114ecbbc1ac116753acf58aa564cd47b3ea5fbd99ad8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740ba1ef0d399dc76efb91309b9d1c8426213faa31da03d8c0abbc94a3d02e03(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7844bf7d22e8f640ebcc5ba4353115b05d556a850bb6d7fdde5513cba44120(
    *,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b67d140d8d3bc0d4265c1dc732e2e99b3a05600097a65f0baa8803715ced0be(
    *,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    exec: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
    steps: typing.Optional[typing.Sequence[typing.Union[TaskStep, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e15f59ab4d32890cdb2f631bc8b086ac603a9f80c504c1ac6e3645e63dd4250(
    workdir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f502dc8ce342b578300faffc5bd3c8c920c8565849215d7cec099d782d3ebf2(
    name: builtins.str,
    parents: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[typing.Union[builtins.str, jsii.Number]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7792ab86c20765ed6722e2a1881c2907a4f0a114336f30cefaefba00de3330c2(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284f616dbd3bd02d58106f246e9393ed2115e81d7707ebd8741034d2e9d7faa8(
    *,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: builtins.str,
    steps: typing.Optional[typing.Sequence[typing.Union[TaskStep, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eac93e499bd717527ab62b174c5bd1e157bf4043f5d771b6a289f39177d124a(
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495af8e4e99205093378c79e03b3c0d9920dc74f1087a97c18e344446ffd90f7(
    project: Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c3e6aae839d7e262f9c707d296976e912fe4d334cc2f3ac081cdbc6f15db60(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836b8399b5241179b18880b35ae533996a76c85a9b01d5c5c846aaef0e3a8d88(
    name: builtins.str,
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    exec: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
    steps: typing.Optional[typing.Sequence[typing.Union[TaskStep, typing.Dict[builtins.str, typing.Any]]]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    required_env: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c96f29b4423e28b4b65e683fc7e07a1024953e3610bb284fa1a0a90b8c77c07(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3316a1d8c737096e24c835f4cd8318c12ed26e59edc6a48fa5de090d545d802e(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0400d76981616b89be8abb0d5287b8580aa0798ae9b6433bfc19c9e589d6b1a5(
    *,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tasks: typing.Optional[typing.Mapping[builtins.str, typing.Union[TaskSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184d7a8774ff332a32a14ae9703ca863b4f123b736abf438d6c5131c636fbeb1(
    project: Project,
    *,
    parse_json: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9476d9e99301eafe205e231c4756ac047dd331e4755928e2ec0362aea31d1e68(
    scope: _constructs_77d1e7e8.IConstruct,
    file_path: builtins.str,
    *,
    lines: typing.Optional[typing.Sequence[builtins.str]] = None,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2345f360405dc3baf9ce7fd3079f23bf8acae86b5a5e39993ac4de26eebbae03(
    line: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433f7685b1ee13eacf88a0112f3c5ac027adfdd4a486841078298f619674abc8(
    _: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0f4dd58b9e223b379bf709c046d112cede147b9481878f22a671a9d7f79bfc(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
    lines: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7c08620aabeb578ce8c0c54b1073a9df1f34c7815d8ae6fdebff7eb411c3d8(
    project: Project,
    file_path: builtins.str,
    *,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ab5968ef36d3ff7f038abd17ae6a5bb7c16e94ed9dbcf023bba58b047f2f38(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab22f277a63768ddf4f6605743ad2816e10bd46ac73de98867b0f280f8eca01(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf64d1b29258435f8a7749178e947fcedd27d55f323782081a21714be909595(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    artifacts_directory: builtins.str,
    version_input_file: builtins.str,
    bump_package: typing.Optional[builtins.str] = None,
    next_version_command: typing.Optional[builtins.str] = None,
    releasable_commits: typing.Optional[ReleasableCommits] = None,
    tag_prefix: typing.Optional[builtins.str] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62987907aa24cc1b84e9b6e9b755bd286708fa4a219baa7b979fb3ea61401603(
    *,
    major_version: typing.Optional[jsii.Number] = None,
    min_major_version: typing.Optional[jsii.Number] = None,
    minor_version: typing.Optional[jsii.Number] = None,
    prerelease: typing.Optional[builtins.str] = None,
    tag_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb94d39bdc04d188bb2447acba8747de3d6ec275231c8a512d647916d69a54f5(
    *,
    artifacts_directory: builtins.str,
    version_input_file: builtins.str,
    bump_package: typing.Optional[builtins.str] = None,
    next_version_command: typing.Optional[builtins.str] = None,
    releasable_commits: typing.Optional[ReleasableCommits] = None,
    tag_prefix: typing.Optional[builtins.str] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5b690e903db052918d05a559c63588dd937691c1a431dfac231627b8e528e8(
    project: Project,
    file_path: builtins.str,
    *,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2692cc4c7fb6801f048a0fa351a11b924d2fc1bc8cbe476af5597cd65143cbd6(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca47b496952cf7e3231ef829693ea86ffea84f642882cd1bff5b5dedd4c31175(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af86e1db34b2981edd2efebaba099732281c104959fb2bbb34db7c78208f5e26(
    scope: _constructs_77d1e7e8.IConstruct,
    file_path: builtins.str,
    *,
    line_width: typing.Optional[jsii.Number] = None,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed453f41109a767cb068d726b9448c3545059d1161f0785da668afdd21e36069(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48f409d84ffd5e2a23ba998b62ea6bdf1343878ddf6bbdba39669e9e45b8464(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9e5a70f67f8e3db454227249c58dd5464be1446a55fcf3be780621fded1638(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
    line_width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a39137d5e4f9c51c84e6a659a0e0d16c23ba1927ed8fe7f3f96ecd5d0110dc(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
    type: DependencyType,
    metadata: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30adb261bc3a7558152dddf9acb47c2b326de589312d32dcb84afc10909eaa49(
    service_name: builtins.str,
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    depends_on: typing.Optional[typing.Sequence[IDockerComposeServiceName]] = None,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[builtins.str] = None,
    image_build: typing.Optional[typing.Union[DockerComposeBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    networks: typing.Optional[typing.Sequence[IDockerComposeNetworkBinding]] = None,
    platform: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Sequence[typing.Union[DockerComposeServicePort, typing.Dict[builtins.str, typing.Any]]]] = None,
    privileged: typing.Optional[builtins.bool] = None,
    volumes: typing.Optional[typing.Sequence[IDockerComposeVolumeBinding]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ff43023f997f5472eb87eb69dd00d7be9ea937c60e0ee2901649769a7058d2(
    service_name: IDockerComposeServiceName,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20e959d624b3b1127206bf0505435f464e2dd4b499a9de78ae5b62f3768de8b(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66ccd81821843eafa497e58cc72c82e90c73c8303d8b59878daf25c4e8e1b6f(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86c0a8aae5342390c599726fd2da4ac1905227de386cc7023bd3614ed2f628b(
    network: IDockerComposeNetworkBinding,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28bd4f8327dce6303d35aa47ba8a52745ed9e16a768727fac813952ae557cdaf(
    published_port: jsii.Number,
    target_port: jsii.Number,
    *,
    protocol: typing.Optional[DockerComposeProtocol] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c149f3c3feafe7a16b339d4f946067d127836eda10279b26447013ec075193ed(
    volume: IDockerComposeVolumeBinding,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21675c9752472f446f36533458bc020deb11343e29b63f990c190823733a1404(
    project: Project,
    *,
    prebuilds: typing.Optional[typing.Union[GitpodPrebuilds, typing.Dict[builtins.str, typing.Any]]] = None,
    docker_image: typing.Optional[DevEnvironmentDockerImage] = None,
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    tasks: typing.Optional[typing.Sequence[Task]] = None,
    vscode_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0520b94b222da42f222b062a87e711f81a8d888cb18100e42bc65273217eece2(
    image: DevEnvironmentDockerImage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadcfbc0f5796128a0688c1a9c0ab6d4e709eae13487757a6c9e31ec724e6c9a(
    *ports: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cdc6c6ab91811936f49718caa7fd070f6c4abe6f48169d00efc3c1b6ff40ff(
    *tasks: Task,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665d383deec6069f2a514e6afdacc5d1a4416876d520c11c3318ca4c85f91cfb(
    *extensions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbd31798d0e0c9e35dbbc5085bcb67cd656717ccca79896838efc097963c5ea(
    project: Project,
    file_path: builtins.str,
    *,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9199eb11888c254ab59f6b5e5411b6921139de20f66c995fc90a33542e20693(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c292bd0cc5c248be03f2bad019458df0920a1b2f21b8d18cfb340489994ca61(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b2200943f9f1c3d7452e66283d201e06e67715a6a56548aa31d93f9dc511ed(
    scope: _constructs_77d1e7e8.IConstruct,
    file_path: builtins.str,
    *,
    allow_comments: typing.Optional[builtins.bool] = None,
    newline: typing.Optional[builtins.bool] = None,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ec13937bd2fb6b7d1a296b25576844e3d9ad24f7864fc43e5f8777adcb73c5(
    resolver: IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13520dccfc7567565533a60eb68d854a29a519fa88a2a00e2abe76dd2578046e(
    *,
    committed: typing.Optional[builtins.bool] = None,
    edit_gitignore: typing.Optional[builtins.bool] = None,
    executable: typing.Optional[builtins.bool] = None,
    marker: typing.Optional[builtins.bool] = None,
    readonly: typing.Optional[builtins.bool] = None,
    obj: typing.Any = None,
    omit_empty: typing.Optional[builtins.bool] = None,
    allow_comments: typing.Optional[builtins.bool] = None,
    newline: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3116496b7a7f86911d3f5b5fc2758a136c1b6b18f32ffdb3a80bbd8fe0439914(
    project: Project,
    *,
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e32d65dbc737f8fd131c5593ecf206bcf2a76757ddb7c5f42945d73058aaae1(
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    condition: typing.Optional[builtins.str] = None,
    cwd: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    receive_args: typing.Optional[builtins.bool] = None,
    builtin: typing.Optional[builtins.str] = None,
    exec: typing.Optional[builtins.str] = None,
    say: typing.Optional[builtins.str] = None,
    spawn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
