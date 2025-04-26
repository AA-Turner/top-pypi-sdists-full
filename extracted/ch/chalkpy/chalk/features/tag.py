from __future__ import annotations

from typing import Sequence, Union

from typing_extensions import TypeAlias

Tags: TypeAlias = Union[str, Sequence[str]]
"""
Tags allow you to scope requests within an
environment. Both tags and environment need
to match for a resolver to be a candidate to
execute.

Like Environments, tags control when resolvers
run based on the Online Context or Training Context
matching the tags provided to the resolver decorator.
Resolvers optionally take a keyword argument named
tags that can take one of three types:
- `None` (default) - The resolver will be a candidate to run for every set of tags.
- `str` - The resolver will run only if this tag is provided.
- `list[str]` - The resolver will run in all of the specified tags match.

See more at https://docs.chalk.ai/docs/resolver-tags
"""

Environments: TypeAlias = Union[str, Sequence[str]]
"""
Environments are used to trigger behavior
in different deployments such as staging,
production, and local development.
For example, you may wish to interact with
a vendor via an API call in the production
environment, and opt to return a constant
value in a staging environment.

`Environments` can take one of three types:
  - `None` (default) - candidate to run in every environment
  - `str` - run only in this environment
  - `list[str]` - run in any of the specified environment and no others

See more at https://docs.chalk.ai/docs/resolver-environments
"""

EnvironmentId: TypeAlias = str
"""Many of the method on the `ChalkClient`
expose an `environment` parameter for specifying
which Chalk environment to target, as defined in
https://docs.chalk.ai/docs/resolver-environments

If you pass an explicit variable for environments,
that will always be preferred. Otherwise, the
`ChalkClient` will first check for the presence of
the environment variables `CHALK_CLIENT_ID` and
`CHALK_CLIENT_SECRET`. If they are present,
`ChalkClient` will use those credentials, and
optionally the API server and environment specified
by `CHALK_API_SERVER` and `CHALK_ENVIRONMENT`.

Failing these two checks, the `ChalkClient` will
look for a `~/.chalk.yml` file, which is updated
when you run `chalk login`. If a token for the
specific project directory if found, that token
will be used. Otherwise, the token under the key
`default` will be used. When using the `~/.chalk.yml`
file, you can still optionally override the API
server and environment by setting the environment
variables `CHALK_API_SERVER` and `CHALK_ENVIRONMENT`.
"""

BranchId: TypeAlias = str

DeploymentId: TypeAlias = str
"""
Each `chalk apply` invocation produces a new immutable deployment.
This type refers to the id of one of these immutable deployments.
"""
