r'''
# AWS CDK AppSync Utilities

This package contains various utilities for definining GraphQl Apis via AppSync using the [aws-cdk](https://github.com/aws/aws-cdk).

## Code First Schema Definition

`CodeFirstSchema` offers the ability to generate your schema in a code-first
approach. A code-first approach offers a developer workflow with:

* **modularity**: organizing schema type definitions into different files
* **reusability**: removing boilerplate/repetitive code
* **consistency**: resolvers and schema definition will always be synced

The code-first approach allows for **dynamic** schema generation. You can
generate your schema based on variables and templates to reduce code
duplication.

```python
import { GraphqlApi } from '@aws-cdk/aws-appsync-alpha';
import { CodeFirstSchema } from 'awscdk-appsync-utils';

const schema = new CodeFirstSchema();
const api = new GraphqlApi(this, 'api', { name: 'myApi', schema });

schema.addType(new ObjectType('demo', {
  definition: { id: GraphqlType.id() },
}));
```

### Code-First Example

To showcase the code-first approach. Let's try to model the following schema segment.

```gql
interface Node {
  id: String
}

type Query {
  allFilms(after: String, first: Int, before: String, last: Int): FilmConnection
}

type FilmNode implements Node {
  filmName: String
}

type FilmConnection {
  edges: [FilmEdge]
  films: [Film]
  totalCount: Int
}

type FilmEdge {
  node: Film
  cursor: String
}
```

Above we see a schema that allows for generating paginated responses. For example,
we can query `allFilms(first: 100)` since `FilmConnection` acts as an intermediary
for holding `FilmEdges` we can write a resolver to return the first 100 films.

In a separate file, we can declare our object types and related functions.
We will call this file `object-types.ts` and we will have created it in a way that
allows us to generate other `XxxConnection` and `XxxEdges` in the future.

```python
import { GraphqlType, InterfaceType, ObjectType } from 'awscdk-appsync-utils';
const pluralize = require('pluralize');

export const args = {
  after: GraphqlType.string(),
  first: GraphqlType.int(),
  before: GraphqlType.string(),
  last: GraphqlType.int(),
};

export const Node = new InterfaceType('Node', {
  definition: { id: GraphqlType.string() }
});
export const FilmNode = new ObjectType('FilmNode', {
  interfaceTypes: [Node],
  definition: { filmName: GraphqlType.string() }
});

export function generateEdgeAndConnection(base: ObjectType) {
  const edge = new ObjectType(`${base.name}Edge`, {
    definition: { node: base.attribute(), cursor: GraphqlType.string() }
  });
  const connection = new ObjectType(`${base.name}Connection`, {
    definition: {
      edges: edge.attribute({ isList: true }),
      [pluralize(base.name)]: base.attribute({ isList: true }),
      totalCount: GraphqlType.int(),
    }
  });
  return { edge: edge, connection: connection };
}
```

Finally, we will go to our `cdk-stack` and combine everything together
to generate our schema.

```python
declare const dummyRequest: appsync.MappingTemplate;
declare const dummyResponse: appsync.MappingTemplate;

const api = new appsync.GraphqlApi(this, 'Api', {
  name: 'demo',
});

const objectTypes = [ Node, FilmNode ];

const filmConnections = generateEdgeAndConnection(FilmNode);

api.addQuery('allFilms', new ResolvableField({
  returnType: filmConnections.connection.attribute(),
  args: args,
  dataSource: api.addNoneDataSource('none'),
  requestMappingTemplate: dummyRequest,
  responseMappingTemplate: dummyResponse,
}));

api.addType(Node);
api.addType(FilmNode);
api.addType(filmConnections.edge);
api.addType(filmConnections.connection);
```

Notice how we can utilize the `generateEdgeAndConnection` function to generate
Object Types. In the future, if we wanted to create more Object Types, we can simply
create the base Object Type (i.e. Film) and from there we can generate its respective
`Connections` and `Edges`.

Check out a more in-depth example [here](https://github.com/BryanPan342/starwars-code-first).

## GraphQL Types

One of the benefits of GraphQL is its strongly typed nature. We define the
types within an object, query, mutation, interface, etc. as **GraphQL Types**.

GraphQL Types are the building blocks of types, whether they are scalar, objects,
interfaces, etc. GraphQL Types can be:

* [**Scalar Types**](https://docs.aws.amazon.com/appsync/latest/devguide/scalars.html): Id, Int, String, AWSDate, etc.
* [**Object Types**](#Object-Types): types that you generate (i.e. `demo` from the example above)
* [**Interface Types**](#Interface-Types): abstract types that define the base implementation of other
  Intermediate Types

More concretely, GraphQL Types are simply the types appended to variables.
Referencing the object type `Demo` in the previous example, the GraphQL Types
is `String!` and is applied to both the names `id` and `version`.

### Directives

`Directives` are attached to a field or type and affect the execution of queries,
mutations, and types. With AppSync, we use `Directives` to configure authorization.
Appsync utils provide static functions to add directives to your CodeFirstSchema.

* `Directive.iam()` sets a type or field's authorization to be validated through `Iam`
* `Directive.apiKey()` sets a type or field's authorization to be validated through a `Api Key`
* `Directive.oidc()` sets a type or field's authorization to be validated through `OpenID Connect`
* `Directive.cognito(...groups: string[])` sets a type or field's authorization to be validated
  through `Cognito User Pools`

  * `groups` the name of the cognito groups to give access

To learn more about authorization and directives, read these docs [here](https://docs.aws.amazon.com/appsync/latest/devguide/security.html).

### Field and Resolvable Fields

While `GraphqlType` is a base implementation for GraphQL fields, we have abstractions
on top of `GraphqlType` that provide finer grain support.

### Field

`Field` extends `GraphqlType` and will allow you to define arguments. [**Interface Types**](#Interface-Types) are not resolvable and this class will allow you to define arguments,
but not its resolvers.

For example, if we want to create the following type:

```gql
type Node {
  test(argument: string): String
}
```

The CDK code required would be:

```python
import { Field, GraphqlType, InterfaceType } from 'awscdk-appsync-utils';

const field = new Field({
  returnType: GraphqlType.string(),
  args: {
    argument: GraphqlType.string(),
  },
});
const type = new InterfaceType('Node', {
  definition: { test: field },
});
```

### Resolvable Fields

`ResolvableField` extends `Field` and will allow you to define arguments and its resolvers.
[**Object Types**](#Object-Types) can have fields that resolve and perform operations on
your backend.

You can also create resolvable fields for object types.

```gql
type Info {
  node(id: String): String
}
```

The CDK code required would be:

```python
declare const api: appsync.GraphqlApi;
declare const dummyRequest: appsync.MappingTemplate;
declare const dummyResponse: appsync.MappingTemplate;

const info = new ObjectType('Info', {
  definition: {
    node: new ResolvableField({
      returnType: GraphqlType.string(),
      args: {
        id: GraphqlType.string(),
      },
      dataSource: api.addNoneDataSource('none'),
      requestMappingTemplate: dummyRequest,
      responseMappingTemplate: dummyResponse,
    }),
  },
});
```

To nest resolvers, we can also create top level query types that call upon
other types. Building off the previous example, if we want the following graphql
type definition:

```gql
type Query {
  get(argument: string): Info
}
```

The CDK code required would be:

```python
declare const api: appsync.GraphqlApi;
declare const dummyRequest: appsync.MappingTemplate;
declare const dummyResponse: appsync.MappingTemplate;

const query = new ObjectType('Query', {
  definition: {
    get: new ResolvableField({
      returnType: GraphqlType.string(),
      args: {
        argument: GraphqlType.string(),
      },
      dataSource: api.addNoneDataSource('none'),
      requestMappingTemplate: dummyRequest,
      responseMappingTemplate: dummyResponse,
    }),
  },
});
```

Learn more about fields and resolvers [here](https://docs.aws.amazon.com/appsync/latest/devguide/resolver-mapping-template-reference-overview.html).

### Intermediate Types

Intermediate Types are defined by Graphql Types and Fields. They have a set of defined
fields, where each field corresponds to another type in the system. Intermediate
Types will be the meat of your GraphQL Schema as they are the types defined by you.

Intermediate Types include:

* [**Interface Types**](#Interface-Types)
* [**Object Types**](#Object-Types)
* [**Enum Types**](#Enum-Types)
* [**Input Types**](#Input-Types)
* [**Union Types**](#Union-Types)

#### Interface Types

**Interface Types** are abstract types that define the implementation of other
intermediate types. They are useful for eliminating duplication and can be used
to generate Object Types with less work.

You can create Interface Types ***externally***.

```python
const node = new InterfaceType('Node', {
  definition: {
    id: GraphqlType.string({ isRequired: true }),
  },
});
```

To learn more about **Interface Types**, read the docs [here](https://graphql.org/learn/schema/#interfaces).

#### Object Types

**Object Types** are types that you declare. For example, in the [code-first example](#code-first-example)
the `demo` variable is an **Object Type**. **Object Types** are defined by
GraphQL Types and are only usable when linked to a GraphQL Api.

You can create Object Types in two ways:

1. Object Types can be created ***externally***.

   ```python
   const schema = new CodeFirstSchema();
   const api = new appsync.GraphqlApi(this, 'Api', {
     name: 'demo',
     schema,
   });
   const demo = new ObjectType('Demo', {
     definition: {
       id: GraphqlType.string({ isRequired: true }),
       version: GraphqlType.string({ isRequired: true }),
     },
   });

   schema.addType(demo);
   ```

   > This method allows for reusability and modularity, ideal for larger projects.
   > For example, imagine moving all Object Type definition outside the stack.

   `object-types.ts` - a file for object type definitions

   ```python
   import { ObjectType, GraphqlType } from 'awscdk-appsync-utils';
   export const demo = new ObjectType('Demo', {
     definition: {
       id: GraphqlType.string({ isRequired: true }),
       version: GraphqlType.string({ isRequired: true }),
     },
   });
   ```

   `cdk-stack.ts` - a file containing our cdk stack

   ```python
   declare const schema: CodeFirstSchema;
   schema.addType(demo);
   ```
2. Object Types can be created ***externally*** from an Interface Type.

   ```python
   const node = new InterfaceType('Node', {
     definition: {
       id: GraphqlType.string({ isRequired: true }),
     },
   });
   const demo = new ObjectType('Demo', {
     interfaceTypes: [ node ],
     definition: {
       version: GraphqlType.string({ isRequired: true }),
     },
   });
   ```

   > This method allows for reusability and modularity, ideal for reducing code duplication.

To learn more about **Object Types**, read the docs [here](https://graphql.org/learn/schema/#object-types-and-fields).

#### Enum Types

**Enum Types** are a special type of Intermediate Type. They restrict a particular
set of allowed values for other Intermediate Types.

```gql
enum Episode {
  NEWHOPE
  EMPIRE
  JEDI
}
```

> This means that wherever we use the type Episode in our schema, we expect it to
> be exactly one of NEWHOPE, EMPIRE, or JEDI.

The above GraphQL Enumeration Type can be expressed in CDK as the following:

```python
declare const api: GraphqlApi;
const episode = new EnumType('Episode', {
  definition: [
    'NEWHOPE',
    'EMPIRE',
    'JEDI',
  ],
});
api.addType(episode);
```

To learn more about **Enum Types**, read the docs [here](https://graphql.org/learn/schema/#enumeration-types).

#### Input Types

**Input Types** are special types of Intermediate Types. They give users an
easy way to pass complex objects for top level Mutation and Queries.

```gql
input Review {
  stars: Int!
  commentary: String
}
```

The above GraphQL Input Type can be expressed in CDK as the following:

```python
declare const api: appsync.GraphqlApi;
const review = new InputType('Review', {
  definition: {
    stars: GraphqlType.int({ isRequired: true }),
    commentary: GraphqlType.string(),
  },
});
api.addType(review);
```

To learn more about **Input Types**, read the docs [here](https://graphql.org/learn/schema/#input-types).

#### Union Types

**Union Types** are a special type of Intermediate Type. They are similar to
Interface Types, but they cannot specify any common fields between types.

**Note:** the fields of a union type need to be `Object Types`. In other words, you
can't create a union type out of interfaces, other unions, or inputs.

```gql
union Search = Human | Droid | Starship
```

The above GraphQL Union Type encompasses the Object Types of Human, Droid and Starship. It
can be expressed in CDK as the following:

```python
declare const api: appsync.GraphqlApi;
const string = GraphqlType.string();
const human = new ObjectType('Human', { definition: { name: string } });
const droid = new ObjectType('Droid', { definition: { name: string } });
const starship = new ObjectType('Starship', { definition: { name: string } }););
const search = new UnionType('Search', {
  definition: [ human, droid, starship ],
});
api.addType(search);
```

To learn more about **Union Types**, read the docs [here](https://graphql.org/learn/schema/#union-types).

### Query

Every schema requires a top level Query type. By default, the schema will look
for the `Object Type` named `Query`. The top level `Query` is the **only** exposed
type that users can access to perform `GET` operations on your Api.

To add fields for these queries, we can simply run the `addQuery` function to add
to the schema's `Query` type.

```python
declare const api: appsync.GraphqlApi;
declare const filmConnection: InterfaceType;
declare const dummyRequest: appsync.MappingTemplate;
declare const dummyResponse: appsync.MappingTemplate;

const string = GraphqlType.string();
const int = GraphqlType.int();
api.addQuery('allFilms', new ResolvableField({
  returnType: filmConnection.attribute(),
  args: { after: string, first: int, before: string, last: int},
  dataSource: api.addNoneDataSource('none'),
  requestMappingTemplate: dummyRequest,
  responseMappingTemplate: dummyResponse,
}));
```

To learn more about top level operations, check out the docs [here](https://docs.aws.amazon.com/appsync/latest/devguide/graphql-overview.html).

### Mutation

Every schema **can** have a top level Mutation type. By default, the schema will look
for the `ObjectType` named `Mutation`. The top level `Mutation` Type is the only exposed
type that users can access to perform `mutable` operations on your Api.

To add fields for these mutations, we can simply run the `addMutation` function to add
to the schema's `Mutation` type.

```python
declare const api: appsync.GraphqlApi;
declare const filmNode: ObjectType;
declare const dummyRequest: appsync.MappingTemplate;
declare const dummyResponse: appsync.MappingTemplate;

const string = GraphqlType.string();
const int = GraphqlType.int();
api.addMutation('addFilm', new ResolvableField({
  returnType: filmNode.attribute(),
  args: { name: string, film_number: int },
  dataSource: api.addNoneDataSource('none'),
  requestMappingTemplate: dummyRequest,
  responseMappingTemplate: dummyResponse,
}));
```

To learn more about top level operations, check out the docs [here](https://docs.aws.amazon.com/appsync/latest/devguide/graphql-overview.html).

### Subscription

Every schema **can** have a top level Subscription type. The top level `Subscription` Type
is the only exposed type that users can access to invoke a response to a mutation. `Subscriptions`
notify users when a mutation specific mutation is called. This means you can make any data source
real time by specify a GraphQL Schema directive on a mutation.

**Note**: The AWS AppSync client SDK automatically handles subscription connection management.

To add fields for these subscriptions, we can simply run the `addSubscription` function to add
to the schema's `Subscription` type.

```python
declare const api: appsync.GraphqlApi;
declare const film: InterfaceType;

api.addSubscription('addedFilm', new Field({
  returnType: film.attribute(),
  args: { id: GraphqlType.id({ isRequired: true }) },
  directives: [Directive.subscribe('addFilm')],
}));
```

To learn more about top level operations, check out the docs [here](https://docs.aws.amazon.com/appsync/latest/devguide/real-time-data.html).

## Merge Source API to Merged API Using A Custom Resource

The SourceApiAssociationMergeOperation construct provides the ability to merge a source api to a Merged Api
and invoke a merge within a Cloudformation custom resource. If the merge operation fails with a conflict, the
Cloudformation update will fail and rollback the changes to the source API in the stack.

```python
import * as cdk from 'aws-cdk-lib';

const sourceApi1ToMerge = new appsync.GraphqlApi(this, 'FirstSourceAPI', {
  name: 'FirstSourceAPI',
  definition: appsync.Definition.fromFile(path.join(__dirname, 'appsync.merged-api-1.graphql')),
});

const sourceApi2ToMerge = new appsync.GraphqlApi(this, 'SecondSourceAPI', {
  name: 'SecondSourceAPI',
  definition: appsync.Definition.fromFile(path.join(__dirname, 'appsync.merged-api-2.graphql')),
});

const remoteMergedApi = appsync.GraphqlApi.fromGraphqlApiAttributes(this, 'ImportedMergedApi', {
  graphqlApiId: 'MyApiId',
  graphqlApiArn: 'MyApiArn',
});

const remoteExecutionRole = iam.Role.fromRoleArn(this, 'ExecutionRole', 'arn:aws:iam::ACCOUNT:role/MyExistingRole');
const association1 = new appsync.SourceApiAssociation(this, 'SourceApiAssociation1', {
   sourceApi: sourceApi1ToMerge,
   mergedApi: remoteMergedApi,
   mergeType: appsync.MergeType.MANUAL_MERGE,
   mergedApiExecutionRole: remoteExecutionRole,
});

const association2 = new appsync.SourceApiAssociation(this, 'SourceApiAssociation2', {
   sourceApi: sourceApi2ToMerge,
   mergedApi: remoteMergedApi,
   mergeType: appsync.MergeType.MANUAL_MERGE,
   mergedApiExecutionRole: remoteExecutionRole,
});

// The version id can be any identifier defined by the developer. Changing the version identifier allows you to control
// whether a merge operation will take place during deployment.
SourceApiAssociationMergeOperation(this, 'MergeOperation1', {
  sourceApiAssociation: association1,
  versionIdentifier: '1',
});

// Optionally, you can add the alwaysMergeOnStackUpdate flag instead which will ensure that the merge operation occurs
// during every stack update, regardless if there was a change or not. Note that this may lead to merge operations that
//do not actually change the MergedAPI.
SourceApiAssociationMergeOperation(this, 'MergeOperation2', {
  sourceApiAssociation: association2,
  alwaysMergeOnStackUpdate: true,
});
```

## Contributing

This library leans towards high level and experimental features for appsync cdk users. If you have an idea for additional utilities please create an issue describing the feature.

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

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
import aws_cdk.aws_appsync as _aws_cdk_aws_appsync_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.AddFieldOptions",
    jsii_struct_bases=[],
    name_mapping={"field": "field", "field_name": "fieldName"},
)
class AddFieldOptions:
    def __init__(
        self,
        *,
        field: typing.Optional["IField"] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The options to add a field to an Intermediate Type.

        :param field: The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f7bf40e088a5358d687ebd351d88825ae33789f783d1e6cd8259d59b070eae)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if field is not None:
            self._values["field"] = field
        if field_name is not None:
            self._values["field_name"] = field_name

    @builtins.property
    def field(self) -> typing.Optional["IField"]:
        '''The resolvable field to add.

        This option must be configured for Object, Interface,
        Input and Union Types.

        :default: - no IField
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional["IField"], result)

    @builtins.property
    def field_name(self) -> typing.Optional[builtins.str]:
        '''The name of the field.

        This option must be configured for Object, Interface,
        Input and Enum Types.

        :default: - no fieldName
        '''
        result = self._values.get("field_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddFieldOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.BaseTypeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_list": "isList",
        "is_required": "isRequired",
        "is_required_list": "isRequiredList",
    },
)
class BaseTypeOptions:
    def __init__(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Base options for GraphQL Types.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :option: isRequiredList - is this attribute a non-nullable list
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7065f74822a55756dfdd04d334d6d9aeda625f057b769a1c5d723a14c5c21b68)
            check_type(argname="argument is_list", value=is_list, expected_type=type_hints["is_list"])
            check_type(argname="argument is_required", value=is_required, expected_type=type_hints["is_required"])
            check_type(argname="argument is_required_list", value=is_required_list, expected_type=type_hints["is_required_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_list is not None:
            self._values["is_list"] = is_list
        if is_required is not None:
            self._values["is_required"] = is_required
        if is_required_list is not None:
            self._values["is_required_list"] = is_required_list

    @builtins.property
    def is_list(self) -> typing.Optional[builtins.bool]:
        '''property determining if this attribute is a list i.e. if true, attribute would be [Type].

        :default: - false
        '''
        result = self._values.get("is_list")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_required(self) -> typing.Optional[builtins.bool]:
        '''property determining if this attribute is non-nullable i.e. if true, attribute would be Type!

        :default: - false
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_required_list(self) -> typing.Optional[builtins.bool]:
        '''property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]!

        :default: - false
        '''
        result = self._values.get("is_required_list")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_appsync_ceddda9d.ISchema)
class CodeFirstSchema(
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-appsync-utils.CodeFirstSchema",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addMutation")
    def add_mutation(
        self,
        field_name: builtins.str,
        field: "ResolvableField",
    ) -> "ObjectType":
        '''Add a mutation field to the schema's Mutation. CDK will create an Object Type called 'Mutation'. For example,.

        type Mutation {
        fieldName: Field.returnType
        }

        :param field_name: the name of the Mutation.
        :param field: the resolvable field to for this Mutation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a13da742511cda4c22e130f0ce760a60c5ea4b0929532c99af50cc54424c219)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast("ObjectType", jsii.invoke(self, "addMutation", [field_name, field]))

    @jsii.member(jsii_name="addQuery")
    def add_query(
        self,
        field_name: builtins.str,
        field: "ResolvableField",
    ) -> "ObjectType":
        '''Add a query field to the schema's Query. CDK will create an Object Type called 'Query'. For example,.

        type Query {
        fieldName: Field.returnType
        }

        :param field_name: the name of the query.
        :param field: the resolvable field to for this query.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6eba0ea409aeaec11841e9c38849d69f255654e4e4477a7d7f084af1e327400)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast("ObjectType", jsii.invoke(self, "addQuery", [field_name, field]))

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(
        self,
        field_name: builtins.str,
        field: "Field",
    ) -> "ObjectType":
        '''Add a subscription field to the schema's Subscription. CDK will create an Object Type called 'Subscription'. For example,.

        type Subscription {
        fieldName: Field.returnType
        }

        :param field_name: the name of the Subscription.
        :param field: the resolvable field to for this Subscription.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bff174e03bcbd43939f0f37ef7ae8342e3b7b6cf26a03aea957fc1e10b6bf8b)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast("ObjectType", jsii.invoke(self, "addSubscription", [field_name, field]))

    @jsii.member(jsii_name="addToSchema")
    def add_to_schema(
        self,
        addition: builtins.str,
        delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Escape hatch to add to Schema as desired.

        Will always result
        in a newline.

        :param addition: the addition to add to schema.
        :param delimiter: the delimiter between schema and addition.

        :default: - ''
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9f8633b9db7d475ee2c6813fe75f25b5ddae546d8af2c3f49b16acb6a14d3b)
            check_type(argname="argument addition", value=addition, expected_type=type_hints["addition"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        return typing.cast(None, jsii.invoke(self, "addToSchema", [addition, delimiter]))

    @jsii.member(jsii_name="addType")
    def add_type(self, type: "IIntermediateType") -> "IIntermediateType":
        '''Add type to the schema.

        :param type: the intermediate type to add to the schema.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0348ee20fcaa775f1da67da997f7846fe6c3f2127c23cf5f3ec36a767f4d4150)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast("IIntermediateType", jsii.invoke(self, "addType", [type]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        api: _aws_cdk_aws_appsync_ceddda9d.IGraphqlApi,
    ) -> _aws_cdk_aws_appsync_ceddda9d.ISchemaConfig:
        '''Called when the GraphQL Api is initialized to allow this object to bind to the stack.

        :param api: The binding GraphQL Api.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b7b25abb239ddf168dc44ee3a4eafb7bfad77b9d39cd8d0d9aa0ed1ebd6cd2)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
        _options = _aws_cdk_aws_appsync_ceddda9d.SchemaBindOptions()

        return typing.cast(_aws_cdk_aws_appsync_ceddda9d.ISchemaConfig, jsii.invoke(self, "bind", [api, _options]))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> builtins.str:
        '''The definition for this schema.'''
        return typing.cast(builtins.str, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1308f3efabd3e7b9dcdf6eb7834b172c6d93517ab709e8bc93ac01ee7b8f22ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value) # pyright: ignore[reportArgumentType]


class Directive(metaclass=jsii.JSIIMeta, jsii_type="awscdk-appsync-utils.Directive"):
    '''Directives for types.

    i.e.

    :aws_iam: or
    :aws_subscribe: true
    '''

    @jsii.member(jsii_name="apiKey")
    @builtins.classmethod
    def api_key(cls) -> "Directive":
        '''Add the.

        :aws_api_key: directive
        '''
        return typing.cast("Directive", jsii.sinvoke(cls, "apiKey", []))

    @jsii.member(jsii_name="cognito")
    @builtins.classmethod
    def cognito(cls, *groups: builtins.str) -> "Directive":
        '''Add the.

        :param groups: the groups to allow access to.

        :aws_auth: or
        :aws_cognito_user_pools: directive
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb0ec8ae31c676028f4d85fdfb846f72b823ab78f507cdd47b3e02836e3a6d2)
            check_type(argname="argument groups", value=groups, expected_type=typing.Tuple[type_hints["groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("Directive", jsii.sinvoke(cls, "cognito", [*groups]))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, statement: builtins.str) -> "Directive":
        '''Add a custom directive.

        :param statement: - the directive statement to append.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad79404fa73c87b407fba3377261357963b7365ec001e2d4a32bdcdca5407eaf)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast("Directive", jsii.sinvoke(cls, "custom", [statement]))

    @jsii.member(jsii_name="iam")
    @builtins.classmethod
    def iam(cls) -> "Directive":
        '''Add the.

        :aws_iam: directive
        '''
        return typing.cast("Directive", jsii.sinvoke(cls, "iam", []))

    @jsii.member(jsii_name="oidc")
    @builtins.classmethod
    def oidc(cls) -> "Directive":
        '''Add the.

        :aws_oidc: directive
        '''
        return typing.cast("Directive", jsii.sinvoke(cls, "oidc", []))

    @jsii.member(jsii_name="subscribe")
    @builtins.classmethod
    def subscribe(cls, *mutations: builtins.str) -> "Directive":
        '''Add the.

        :param mutations: the mutation fields to link to.

        :aws_subscribe: directive. Only use for top level Subscription type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2e92b47801a5b456c7fe7e7e762cebadbe3f15af33d5a2e06755afd79510d3)
            check_type(argname="argument mutations", value=mutations, expected_type=typing.Tuple[type_hints["mutations"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("Directive", jsii.sinvoke(cls, "subscribe", [*mutations]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the directive statement.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> typing.Optional[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]:
        '''The authorization type of this directive.

        :default: - not an authorization directive
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType], jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="mutationFields")
    def mutation_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Mutation fields for a subscription directive.

        :default: - not a subscription directive
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "mutationFields"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]]:
        '''the authorization modes for this intermediate type.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d443722171d0fe5b187acdd55e901af6389dd8fc7e14e25a520c2f1a9dff9d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.EnumTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition"},
)
class EnumTypeOptions:
    def __init__(self, *, definition: typing.Sequence[builtins.str]) -> None:
        '''Properties for configuring an Enum Type.

        :param definition: the attributes of this type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1da7562f56f9b9107c0b0d7046f7ccd21b01a88d0ce3474de7b40294a905c68)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }

    @builtins.property
    def definition(self) -> typing.List[builtins.str]:
        '''the attributes of this type.'''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnumTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.FieldOptions",
    jsii_struct_bases=[],
    name_mapping={
        "return_type": "returnType",
        "args": "args",
        "directives": "directives",
    },
)
class FieldOptions:
    def __init__(
        self,
        *,
        return_type: "GraphqlType",
        args: typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''Properties for configuring a field.

        :param return_type: The return type for this field.
        :param args: The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: the directives for this field. Default: - no directives

        :options:

        args - the variables and types that define the arguments

        i.e. { string: GraphqlType, string: GraphqlType }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad31f19a88f952120497ae675333acfce84d98b4d21a4ad3521d5741cbc8376)
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "return_type": return_type,
        }
        if args is not None:
            self._values["args"] = args
        if directives is not None:
            self._values["directives"] = directives

    @builtins.property
    def return_type(self) -> "GraphqlType":
        '''The return type for this field.'''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast("GraphqlType", result)

    @builtins.property
    def args(self) -> typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]]:
        '''The arguments for this field.

        i.e. type Example (first: String second: String) {}

        - where 'first' and 'second' are key values for args
          and 'String' is the GraphqlType

        :default: - no arguments
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''the directives for this field.

        :default: - no directives
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List[Directive]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FieldOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.GraphqlTypeOptions",
    jsii_struct_bases=[BaseTypeOptions],
    name_mapping={
        "is_list": "isList",
        "is_required": "isRequired",
        "is_required_list": "isRequiredList",
        "intermediate_type": "intermediateType",
    },
)
class GraphqlTypeOptions(BaseTypeOptions):
    def __init__(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
        intermediate_type: typing.Optional["IIntermediateType"] = None,
    ) -> None:
        '''Options for GraphQL Types.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        :param intermediate_type: the intermediate type linked to this attribute. Default: - no intermediate type

        :option: objectType - the object type linked to this attribute
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d88012e201a109aab5098626b5c843f128aa069d7b126cae9dae5d5d0fff70d)
            check_type(argname="argument is_list", value=is_list, expected_type=type_hints["is_list"])
            check_type(argname="argument is_required", value=is_required, expected_type=type_hints["is_required"])
            check_type(argname="argument is_required_list", value=is_required_list, expected_type=type_hints["is_required_list"])
            check_type(argname="argument intermediate_type", value=intermediate_type, expected_type=type_hints["intermediate_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_list is not None:
            self._values["is_list"] = is_list
        if is_required is not None:
            self._values["is_required"] = is_required
        if is_required_list is not None:
            self._values["is_required_list"] = is_required_list
        if intermediate_type is not None:
            self._values["intermediate_type"] = intermediate_type

    @builtins.property
    def is_list(self) -> typing.Optional[builtins.bool]:
        '''property determining if this attribute is a list i.e. if true, attribute would be [Type].

        :default: - false
        '''
        result = self._values.get("is_list")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_required(self) -> typing.Optional[builtins.bool]:
        '''property determining if this attribute is non-nullable i.e. if true, attribute would be Type!

        :default: - false
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_required_list(self) -> typing.Optional[builtins.bool]:
        '''property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]!

        :default: - false
        '''
        result = self._values.get("is_required_list")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def intermediate_type(self) -> typing.Optional["IIntermediateType"]:
        '''the intermediate type linked to this attribute.

        :default: - no intermediate type
        '''
        result = self._values.get("intermediate_type")
        return typing.cast(typing.Optional["IIntermediateType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphqlTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="awscdk-appsync-utils.IField")
class IField(typing_extensions.Protocol):
    '''A Graphql Field.'''

    @builtins.property
    @jsii.member(jsii_name="isList")
    def is_list(self) -> builtins.bool:
        '''property determining if this attribute is a list i.e. if true, attribute would be ``[Type]``.

        :default: false
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> builtins.bool:
        '''property determining if this attribute is non-nullable i.e. if true, attribute would be ``Type!`` and this attribute must always have a value.

        :default: false
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="isRequiredList")
    def is_required_list(self) -> builtins.bool:
        '''property determining if this attribute is a non-nullable list i.e. if true, attribute would be ``[ Type ]!`` and this attribute's list must always have a value.

        :default: false
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "Type":
        '''the type of attribute.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="fieldOptions")
    def field_options(self) -> typing.Optional["ResolvableFieldOptions"]:
        '''The options to make this field resolvable.

        :default: - not a resolvable field
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional["IIntermediateType"]:
        '''the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type
        '''
        ...

    @jsii.member(jsii_name="argsToString")
    def args_to_string(self) -> builtins.str:
        '''Generate the arguments for this field.'''
        ...

    @jsii.member(jsii_name="directivesToString")
    def directives_to_string(
        self,
        modes: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]] = None,
    ) -> builtins.str:
        '''Generate the directives for this field.

        :param modes: the authorization modes of the graphql api.

        :default: - no authorization modes
        '''
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string for this attribute.'''
        ...


class _IFieldProxy:
    '''A Graphql Field.'''

    __jsii_type__: typing.ClassVar[str] = "awscdk-appsync-utils.IField"

    @builtins.property
    @jsii.member(jsii_name="isList")
    def is_list(self) -> builtins.bool:
        '''property determining if this attribute is a list i.e. if true, attribute would be ``[Type]``.

        :default: false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isList"))

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> builtins.bool:
        '''property determining if this attribute is non-nullable i.e. if true, attribute would be ``Type!`` and this attribute must always have a value.

        :default: false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isRequired"))

    @builtins.property
    @jsii.member(jsii_name="isRequiredList")
    def is_required_list(self) -> builtins.bool:
        '''property determining if this attribute is a non-nullable list i.e. if true, attribute would be ``[ Type ]!`` and this attribute's list must always have a value.

        :default: false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isRequiredList"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "Type":
        '''the type of attribute.'''
        return typing.cast("Type", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="fieldOptions")
    def field_options(self) -> typing.Optional["ResolvableFieldOptions"]:
        '''The options to make this field resolvable.

        :default: - not a resolvable field
        '''
        return typing.cast(typing.Optional["ResolvableFieldOptions"], jsii.get(self, "fieldOptions"))

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional["IIntermediateType"]:
        '''the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type
        '''
        return typing.cast(typing.Optional["IIntermediateType"], jsii.get(self, "intermediateType"))

    @jsii.member(jsii_name="argsToString")
    def args_to_string(self) -> builtins.str:
        '''Generate the arguments for this field.'''
        return typing.cast(builtins.str, jsii.invoke(self, "argsToString", []))

    @jsii.member(jsii_name="directivesToString")
    def directives_to_string(
        self,
        modes: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]] = None,
    ) -> builtins.str:
        '''Generate the directives for this field.

        :param modes: the authorization modes of the graphql api.

        :default: - no authorization modes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba439f682dca6c0d6cac014656cc44ec08333c63bc46203e1cec8543e603c154)
            check_type(argname="argument modes", value=modes, expected_type=type_hints["modes"])
        return typing.cast(builtins.str, jsii.invoke(self, "directivesToString", [modes]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string for this attribute.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IField).__jsii_proxy_class__ = lambda : _IFieldProxy


@jsii.interface(jsii_type="awscdk-appsync-utils.IIntermediateType")
class IIntermediateType(typing_extensions.Protocol):
    '''Intermediate Types are types that includes a certain set of fields that define the entirety of your schema.'''

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''the attributes of this type.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''the name of this type.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="directives")
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''the directives for this object type.

        :default: - no directives
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="interfaceTypes")
    def interface_types(self) -> typing.Optional[typing.List["InterfaceType"]]:
        '''The Interface Types this Intermediate Type implements.

        :default: - no interface types
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional["IIntermediateType"]:
        '''the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="resolvers")
    def resolvers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]]:
        '''The resolvers linked to this data source.'''
        ...

    @resolvers.setter
    def resolvers(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]],
    ) -> None:
        ...

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Add a field to this Intermediate Type.

        :param field: The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName
        '''
        ...

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''Create an GraphQL Type representing this Intermediate Type.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string of this object type.'''
        ...


class _IIntermediateTypeProxy:
    '''Intermediate Types are types that includes a certain set of fields that define the entirety of your schema.'''

    __jsii_type__: typing.ClassVar[str] = "awscdk-appsync-utils.IIntermediateType"

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''the attributes of this type.'''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''the name of this type.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="directives")
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''the directives for this object type.

        :default: - no directives
        '''
        return typing.cast(typing.Optional[typing.List[Directive]], jsii.get(self, "directives"))

    @builtins.property
    @jsii.member(jsii_name="interfaceTypes")
    def interface_types(self) -> typing.Optional[typing.List["InterfaceType"]]:
        '''The Interface Types this Intermediate Type implements.

        :default: - no interface types
        '''
        return typing.cast(typing.Optional[typing.List["InterfaceType"]], jsii.get(self, "interfaceTypes"))

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional[IIntermediateType]:
        '''the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type
        '''
        return typing.cast(typing.Optional[IIntermediateType], jsii.get(self, "intermediateType"))

    @builtins.property
    @jsii.member(jsii_name="resolvers")
    def resolvers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]]:
        '''The resolvers linked to this data source.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]], jsii.get(self, "resolvers"))

    @resolvers.setter
    def resolvers(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59011792f47c7b3f206fad46e7957254baf81026e11a95bc089849bec9048222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolvers", value) # pyright: ignore[reportArgumentType]

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Add a field to this Intermediate Type.

        :param field: The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''Create an GraphQL Type representing this Intermediate Type.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string of this object type.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIntermediateType).__jsii_proxy_class__ = lambda : _IIntermediateTypeProxy


@jsii.interface(
    jsii_type="awscdk-appsync-utils.ISourceApiAssociationMergeOperationProvider"
)
class ISourceApiAssociationMergeOperationProvider(
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''This interface for the provider of the custom resource that will be used to initiate a merge operation during Cloudformation update.'''

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''Service token which is used for identifying the handler used for the merge operation custom resource.'''
        ...

    @jsii.member(jsii_name="associateSourceApiAssociation")
    def associate_source_api_association(
        self,
        source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
    ) -> None:
        '''This function associates a source api association with the provider.

        This method can be used for adding permissions to merge a specific source api association to the custom resource provider.

        :param source_api_association: The association to associate.
        '''
        ...


class _ISourceApiAssociationMergeOperationProviderProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''This interface for the provider of the custom resource that will be used to initiate a merge operation during Cloudformation update.'''

    __jsii_type__: typing.ClassVar[str] = "awscdk-appsync-utils.ISourceApiAssociationMergeOperationProvider"

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''Service token which is used for identifying the handler used for the merge operation custom resource.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceToken"))

    @jsii.member(jsii_name="associateSourceApiAssociation")
    def associate_source_api_association(
        self,
        source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
    ) -> None:
        '''This function associates a source api association with the provider.

        This method can be used for adding permissions to merge a specific source api association to the custom resource provider.

        :param source_api_association: The association to associate.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__226c995dcf1aaebe1f3d25529cc4c7ce02a41eea21128a344d740a47c3b777de)
            check_type(argname="argument source_api_association", value=source_api_association, expected_type=type_hints["source_api_association"])
        return typing.cast(None, jsii.invoke(self, "associateSourceApiAssociation", [source_api_association]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISourceApiAssociationMergeOperationProvider).__jsii_proxy_class__ = lambda : _ISourceApiAssociationMergeOperationProviderProxy


@jsii.implements(IIntermediateType)
class InputType(metaclass=jsii.JSIIMeta, jsii_type="awscdk-appsync-utils.InputType"):
    '''Input Types are abstract types that define complex objects.

    They are used in arguments to represent
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param name: the name of this type.
        :param definition: the attributes of this type.
        :param directives: the directives for this object type. Default: - no directives
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfdc112309278b6be6ab9b26dcba766d94191dd61ae1698f3395d586bfa999e9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = IntermediateTypeOptions(definition=definition, directives=directives)

        jsii.create(self.__class__, self, [name, props])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Add a field to this Input Type.

        Input Types must have both fieldName and field options.

        :param field: The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''Create a GraphQL Type representing this Input Type.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string of this input type.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''the attributes of this type.'''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''the name of this type.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]]:
        '''the authorization modes for this intermediate type.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04942b830cddc421ab1b0d7336f8b7ea33c7c2f743130e41a124c23b7ded103a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value) # pyright: ignore[reportArgumentType]


@jsii.implements(IIntermediateType)
class InterfaceType(
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-appsync-utils.InterfaceType",
):
    '''Interface Types are abstract types that includes a certain set of fields that other types must include if they implement the interface.'''

    def __init__(
        self,
        name: builtins.str,
        *,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param name: the name of this type.
        :param definition: the attributes of this type.
        :param directives: the directives for this object type. Default: - no directives
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd516fbb192c8cd673c922cc60ee779228f97b6b5c403db5802b0265e97753b3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = IntermediateTypeOptions(definition=definition, directives=directives)

        jsii.create(self.__class__, self, [name, props])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Add a field to this Interface Type.

        Interface Types must have both fieldName and field options.

        :param field: The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''Create a GraphQL Type representing this Intermediate Type.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string of this object type.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''the attributes of this type.'''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''the name of this type.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="directives")
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''the directives for this object type.

        :default: - no directives
        '''
        return typing.cast(typing.Optional[typing.List[Directive]], jsii.get(self, "directives"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]]:
        '''the authorization modes for this intermediate type.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b62131c70cfa7326ff803ccc763fdb67b5c3a464ea8cc825440aca85bf9a9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.IntermediateTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition", "directives": "directives"},
)
class IntermediateTypeOptions:
    def __init__(
        self,
        *,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''Properties for configuring an Intermediate Type.

        :param definition: the attributes of this type.
        :param directives: the directives for this object type. Default: - no directives
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef74b07a9cde3cbc0cabbab7080b59aa43a79762c12720f557d4c842026d3a0)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }
        if directives is not None:
            self._values["directives"] = directives

    @builtins.property
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''the attributes of this type.'''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Mapping[builtins.str, IField], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''the directives for this object type.

        :default: - no directives
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List[Directive]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntermediateTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIntermediateType)
class ObjectType(
    InterfaceType,
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-appsync-utils.ObjectType",
):
    '''Object Types are types declared by you.'''

    def __init__(
        self,
        name: builtins.str,
        *,
        interface_types: typing.Optional[typing.Sequence[InterfaceType]] = None,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param name: the name of this type.
        :param interface_types: The Interface Types this Object Type implements. Default: - no interface types
        :param definition: the attributes of this type.
        :param directives: the directives for this object type. Default: - no directives
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae86eda7501d76d7538544558a7ca59bedb940aded4c892041fb55221f5d0ed9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = ObjectTypeOptions(
            interface_types=interface_types,
            definition=definition,
            directives=directives,
        )

        jsii.create(self.__class__, self, [name, props])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Add a field to this Object Type.

        Object Types must have both fieldName and field options.

        :param field: The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="generateResolver")
    def _generate_resolver(
        self,
        api: _aws_cdk_aws_appsync_ceddda9d.IGraphqlApi,
        field_name: builtins.str,
        *,
        caching_config: typing.Optional[typing.Union[_aws_cdk_aws_appsync_ceddda9d.CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.Code] = None,
        data_source: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.BaseDataSource] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        pipeline_config: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
        response_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
        runtime: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.FunctionRuntime] = None,
        return_type: "GraphqlType",
        args: typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> _aws_cdk_aws_appsync_ceddda9d.Resolver:
        '''Generate the resolvers linked to this Object Type.

        :param api: -
        :param field_name: -
        :param caching_config: The caching configuration for this resolver. Default: - No caching configuration
        :param code: The function code. Default: - no code is used
        :param data_source: The data source creating linked to this resolvable field. Default: - no data source
        :param max_batch_size: The maximum number of elements per batch, when using batch invoke. Default: - No max batch size
        :param pipeline_config: configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: The response mapping template for this resolver. Default: - No mapping template
        :param runtime: The functions runtime. Default: - no function runtime, VTL mapping templates used
        :param return_type: The return type for this field.
        :param args: The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: the directives for this field. Default: - no directives
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432233d1e5c3bc430b75552cc4ba1c77c92e16d5c648430047231ea8aff05106)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
        options = ResolvableFieldOptions(
            caching_config=caching_config,
            code=code,
            data_source=data_source,
            max_batch_size=max_batch_size,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
            runtime=runtime,
            return_type=return_type,
            args=args,
            directives=directives,
        )

        return typing.cast(_aws_cdk_aws_appsync_ceddda9d.Resolver, jsii.invoke(self, "generateResolver", [api, field_name, options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string of this object type.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="interfaceTypes")
    def interface_types(self) -> typing.Optional[typing.List[InterfaceType]]:
        '''The Interface Types this Object Type implements.

        :default: - no interface types
        '''
        return typing.cast(typing.Optional[typing.List[InterfaceType]], jsii.get(self, "interfaceTypes"))

    @builtins.property
    @jsii.member(jsii_name="resolvers")
    def resolvers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]]:
        '''The resolvers linked to this data source.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]], jsii.get(self, "resolvers"))

    @resolvers.setter
    def resolvers(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220014e372ab0e12b1f7655a2e5689250db5a672a1c2a02b6af6011f0c4e4236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolvers", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.ObjectTypeOptions",
    jsii_struct_bases=[IntermediateTypeOptions],
    name_mapping={
        "definition": "definition",
        "directives": "directives",
        "interface_types": "interfaceTypes",
    },
)
class ObjectTypeOptions(IntermediateTypeOptions):
    def __init__(
        self,
        *,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
        interface_types: typing.Optional[typing.Sequence[InterfaceType]] = None,
    ) -> None:
        '''Properties for configuring an Object Type.

        :param definition: the attributes of this type.
        :param directives: the directives for this object type. Default: - no directives
        :param interface_types: The Interface Types this Object Type implements. Default: - no interface types
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6f5f139b92d75136cf9b5d66e019140698c0595b617f6d311aa129946b385a)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
            check_type(argname="argument interface_types", value=interface_types, expected_type=type_hints["interface_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }
        if directives is not None:
            self._values["directives"] = directives
        if interface_types is not None:
            self._values["interface_types"] = interface_types

    @builtins.property
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''the attributes of this type.'''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Mapping[builtins.str, IField], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''the directives for this object type.

        :default: - no directives
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List[Directive]], result)

    @builtins.property
    def interface_types(self) -> typing.Optional[typing.List[InterfaceType]]:
        '''The Interface Types this Object Type implements.

        :default: - no interface types
        '''
        result = self._values.get("interface_types")
        return typing.cast(typing.Optional[typing.List[InterfaceType]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObjectTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.ResolvableFieldOptions",
    jsii_struct_bases=[FieldOptions],
    name_mapping={
        "return_type": "returnType",
        "args": "args",
        "directives": "directives",
        "caching_config": "cachingConfig",
        "code": "code",
        "data_source": "dataSource",
        "max_batch_size": "maxBatchSize",
        "pipeline_config": "pipelineConfig",
        "request_mapping_template": "requestMappingTemplate",
        "response_mapping_template": "responseMappingTemplate",
        "runtime": "runtime",
    },
)
class ResolvableFieldOptions(FieldOptions):
    def __init__(
        self,
        *,
        return_type: "GraphqlType",
        args: typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
        caching_config: typing.Optional[typing.Union[_aws_cdk_aws_appsync_ceddda9d.CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.Code] = None,
        data_source: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.BaseDataSource] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        pipeline_config: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
        response_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
        runtime: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.FunctionRuntime] = None,
    ) -> None:
        '''Properties for configuring a resolvable field.

        :param return_type: The return type for this field.
        :param args: The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: the directives for this field. Default: - no directives
        :param caching_config: The caching configuration for this resolver. Default: - No caching configuration
        :param code: The function code. Default: - no code is used
        :param data_source: The data source creating linked to this resolvable field. Default: - no data source
        :param max_batch_size: The maximum number of elements per batch, when using batch invoke. Default: - No max batch size
        :param pipeline_config: configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: The response mapping template for this resolver. Default: - No mapping template
        :param runtime: The functions runtime. Default: - no function runtime, VTL mapping templates used

        :options: responseMappingTemplate - the mapping template for responses from this resolver
        '''
        if isinstance(caching_config, dict):
            caching_config = _aws_cdk_aws_appsync_ceddda9d.CachingConfig(**caching_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f9c784648f946b717a8bdaf534fc7ab76f1e73fc3b3f407664eb6a2a205224)
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
            check_type(argname="argument caching_config", value=caching_config, expected_type=type_hints["caching_config"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument max_batch_size", value=max_batch_size, expected_type=type_hints["max_batch_size"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "return_type": return_type,
        }
        if args is not None:
            self._values["args"] = args
        if directives is not None:
            self._values["directives"] = directives
        if caching_config is not None:
            self._values["caching_config"] = caching_config
        if code is not None:
            self._values["code"] = code
        if data_source is not None:
            self._values["data_source"] = data_source
        if max_batch_size is not None:
            self._values["max_batch_size"] = max_batch_size
        if pipeline_config is not None:
            self._values["pipeline_config"] = pipeline_config
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def return_type(self) -> "GraphqlType":
        '''The return type for this field.'''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast("GraphqlType", result)

    @builtins.property
    def args(self) -> typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]]:
        '''The arguments for this field.

        i.e. type Example (first: String second: String) {}

        - where 'first' and 'second' are key values for args
          and 'String' is the GraphqlType

        :default: - no arguments
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''the directives for this field.

        :default: - no directives
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List[Directive]], result)

    @builtins.property
    def caching_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_appsync_ceddda9d.CachingConfig]:
        '''The caching configuration for this resolver.

        :default: - No caching configuration
        '''
        result = self._values.get("caching_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_appsync_ceddda9d.CachingConfig], result)

    @builtins.property
    def code(self) -> typing.Optional[_aws_cdk_aws_appsync_ceddda9d.Code]:
        '''The function code.

        :default: - no code is used
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[_aws_cdk_aws_appsync_ceddda9d.Code], result)

    @builtins.property
    def data_source(
        self,
    ) -> typing.Optional[_aws_cdk_aws_appsync_ceddda9d.BaseDataSource]:
        '''The data source creating linked to this resolvable field.

        :default: - no data source
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[_aws_cdk_aws_appsync_ceddda9d.BaseDataSource], result)

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of elements per batch, when using batch invoke.

        :default: - No max batch size
        '''
        result = self._values.get("max_batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pipeline_config(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.IAppsyncFunction]]:
        '''configuration of the pipeline resolver.

        :default:

        - no pipeline resolver configuration
        An empty array | undefined sets resolver to be of kind, unit
        '''
        result = self._values.get("pipeline_config")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.IAppsyncFunction]], result)

    @builtins.property
    def request_mapping_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate]:
        '''The request mapping template for this resolver.

        :default: - No mapping template
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate], result)

    @builtins.property
    def response_mapping_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate]:
        '''The response mapping template for this resolver.

        :default: - No mapping template
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate], result)

    @builtins.property
    def runtime(self) -> typing.Optional[_aws_cdk_aws_appsync_ceddda9d.FunctionRuntime]:
        '''The functions runtime.

        :default: - no function runtime, VTL mapping templates used
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[_aws_cdk_aws_appsync_ceddda9d.FunctionRuntime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolvableFieldOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SourceApiAssociationMergeOperation(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-appsync-utils.SourceApiAssociationMergeOperation",
):
    '''The SourceApiAssociationMergeOperation triggers a merge of a source API during a Cloudformation stack update.

    This can be used to propagate changes from the source API to the Merged API when the association is using type MANUAL_MERGE.
    If the merge operation fails, it will fail the Cloudformation update and rollback the stack.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
        always_merge_on_stack_update: typing.Optional[builtins.bool] = None,
        merge_operation_provider: typing.Optional[ISourceApiAssociationMergeOperationProvider] = None,
        version_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param source_api_association: The source api association resource which will be merged.
        :param always_merge_on_stack_update: Flag indicating whether the source api should be merged on every CFN update or not. If set to true and there are no changes to the source API, this will result in a no-op merge operation. Default: False
        :param merge_operation_provider: The merge operation provider construct which is responsible for configuring the Lambda resource that will be invoked during Cloudformation update.
        :param version_identifier: The version identifier for the schema merge operation. Any change to the version identifier will trigger a merge on the next update. Use the version identifier property to control when the source API metadata is merged. Default: null
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235f7ff7ceb5883b587fc3f0bbe9a0be54e7a137372f1f10b5c65bbe2f725720)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SourceApiAssociationMergeOperationProps(
            source_api_association=source_api_association,
            always_merge_on_stack_update=always_merge_on_stack_update,
            merge_operation_provider=merge_operation_provider,
            version_identifier=version_identifier,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.SourceApiAssociationMergeOperationProps",
    jsii_struct_bases=[],
    name_mapping={
        "source_api_association": "sourceApiAssociation",
        "always_merge_on_stack_update": "alwaysMergeOnStackUpdate",
        "merge_operation_provider": "mergeOperationProvider",
        "version_identifier": "versionIdentifier",
    },
)
class SourceApiAssociationMergeOperationProps:
    def __init__(
        self,
        *,
        source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
        always_merge_on_stack_update: typing.Optional[builtins.bool] = None,
        merge_operation_provider: typing.Optional[ISourceApiAssociationMergeOperationProvider] = None,
        version_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for SourceApiAssociationMergeOperation which handles triggering a merge operation as a custom resource during a Cloudformation stack update.

        :param source_api_association: The source api association resource which will be merged.
        :param always_merge_on_stack_update: Flag indicating whether the source api should be merged on every CFN update or not. If set to true and there are no changes to the source API, this will result in a no-op merge operation. Default: False
        :param merge_operation_provider: The merge operation provider construct which is responsible for configuring the Lambda resource that will be invoked during Cloudformation update.
        :param version_identifier: The version identifier for the schema merge operation. Any change to the version identifier will trigger a merge on the next update. Use the version identifier property to control when the source API metadata is merged. Default: null
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544e8d04628c6e253021d39b2baad6d71ac9769e5e62697a339ea1013ce5fea1)
            check_type(argname="argument source_api_association", value=source_api_association, expected_type=type_hints["source_api_association"])
            check_type(argname="argument always_merge_on_stack_update", value=always_merge_on_stack_update, expected_type=type_hints["always_merge_on_stack_update"])
            check_type(argname="argument merge_operation_provider", value=merge_operation_provider, expected_type=type_hints["merge_operation_provider"])
            check_type(argname="argument version_identifier", value=version_identifier, expected_type=type_hints["version_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_api_association": source_api_association,
        }
        if always_merge_on_stack_update is not None:
            self._values["always_merge_on_stack_update"] = always_merge_on_stack_update
        if merge_operation_provider is not None:
            self._values["merge_operation_provider"] = merge_operation_provider
        if version_identifier is not None:
            self._values["version_identifier"] = version_identifier

    @builtins.property
    def source_api_association(
        self,
    ) -> _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation:
        '''The source api association resource which will be merged.'''
        result = self._values.get("source_api_association")
        assert result is not None, "Required property 'source_api_association' is missing"
        return typing.cast(_aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation, result)

    @builtins.property
    def always_merge_on_stack_update(self) -> typing.Optional[builtins.bool]:
        '''Flag indicating whether the source api should be merged on every CFN update or not.

        If set to true and there are no changes to the source API, this will result in a no-op merge operation.

        :default: False
        '''
        result = self._values.get("always_merge_on_stack_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def merge_operation_provider(
        self,
    ) -> typing.Optional[ISourceApiAssociationMergeOperationProvider]:
        '''The merge operation provider construct which is responsible for configuring the Lambda resource that will be invoked during Cloudformation update.'''
        result = self._values.get("merge_operation_provider")
        return typing.cast(typing.Optional[ISourceApiAssociationMergeOperationProvider], result)

    @builtins.property
    def version_identifier(self) -> typing.Optional[builtins.str]:
        '''The version identifier for the schema merge operation.

        Any change to the version identifier will trigger a merge on the next
        update. Use the version identifier property to control when the source API metadata is merged.

        :default: null
        '''
        result = self._values.get("version_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceApiAssociationMergeOperationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISourceApiAssociationMergeOperationProvider)
class SourceApiAssociationMergeOperationProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-appsync-utils.SourceApiAssociationMergeOperationProvider",
):
    '''SourceApiAssociationMergeProvider class is responsible for constructing the custom resource that will be used for initiating the source API merge during a Cloudformation update.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        polling_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param polling_interval: Time between calls to the polling Lambda function which determines whether the merge operation is finished or not. Default: Duration.seconds(5)
        :param total_timeout: Total timeout in waiting for the source api association merge operation to complete. Default: Duration.minutes(15)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d485d6097bff7f9af62819a3345c4c946b935cd5177797dfd9b57304110270)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SourceApiAssociationMergeOperationProviderProps(
            polling_interval=polling_interval, total_timeout=total_timeout
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="associateSourceApiAssociation")
    def associate_source_api_association(
        self,
        source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
    ) -> None:
        '''This function associates a source api association with the provider.

        This method can be used for adding permissions to merge a specific source api association to the custom resource provider.

        :param source_api_association: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59696b2ff46b70107f7548271c8015421099336faa1b1494f53cade7168ff5d7)
            check_type(argname="argument source_api_association", value=source_api_association, expected_type=type_hints["source_api_association"])
        return typing.cast(None, jsii.invoke(self, "associateSourceApiAssociation", [source_api_association]))

    @builtins.property
    @jsii.member(jsii_name="schemaMergeLambda")
    def schema_merge_lambda(self) -> _aws_cdk_aws_lambda_ceddda9d.SingletonFunction:
        '''The lambda function responsible for kicking off the merge operation.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.SingletonFunction, jsii.get(self, "schemaMergeLambda"))

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''Service token for the resource provider.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceToken"))

    @builtins.property
    @jsii.member(jsii_name="sourceApiStablizationLambda")
    def source_api_stablization_lambda(
        self,
    ) -> _aws_cdk_aws_lambda_ceddda9d.SingletonFunction:
        '''The lambda function response for ensuring that the merge operation finished.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.SingletonFunction, jsii.get(self, "sourceApiStablizationLambda"))


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.SourceApiAssociationMergeOperationProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "polling_interval": "pollingInterval",
        "total_timeout": "totalTimeout",
    },
)
class SourceApiAssociationMergeOperationProviderProps:
    def __init__(
        self,
        *,
        polling_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Properties for SourceApiAssociationMergeOperationProvider.

        :param polling_interval: Time between calls to the polling Lambda function which determines whether the merge operation is finished or not. Default: Duration.seconds(5)
        :param total_timeout: Total timeout in waiting for the source api association merge operation to complete. Default: Duration.minutes(15)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6094717c36a5736f96eb3895a0ca8114c412e1c8b64a7459c643f02278e1e4d)
            check_type(argname="argument polling_interval", value=polling_interval, expected_type=type_hints["polling_interval"])
            check_type(argname="argument total_timeout", value=total_timeout, expected_type=type_hints["total_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if polling_interval is not None:
            self._values["polling_interval"] = polling_interval
        if total_timeout is not None:
            self._values["total_timeout"] = total_timeout

    @builtins.property
    def polling_interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Time between calls to the polling Lambda function which determines whether the merge operation is finished or not.

        :default: Duration.seconds(5)
        '''
        result = self._values.get("polling_interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def total_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Total timeout in waiting for the source api association merge operation to complete.

        :default: Duration.minutes(15)
        '''
        result = self._values.get("total_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceApiAssociationMergeOperationProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="awscdk-appsync-utils.Type")
class Type(enum.Enum):
    '''Enum containing the Types that can be used to define ObjectTypes.'''

    ID = "ID"
    '''``ID`` scalar type is a unique identifier. ``ID`` type is serialized similar to ``String``.

    Often used as a key for a cache and not intended to be human-readable.
    '''
    STRING = "STRING"
    '''``String`` scalar type is a free-form human-readable text.'''
    INT = "INT"
    '''``Int`` scalar type is a signed non-fractional numerical value.'''
    FLOAT = "FLOAT"
    '''``Float`` scalar type is a signed double-precision fractional value.'''
    BOOLEAN = "BOOLEAN"
    '''``Boolean`` scalar type is a boolean value: true or false.'''
    AWS_DATE = "AWS_DATE"
    '''``AWSDate`` scalar type represents a valid extended ``ISO 8601 Date`` string.

    In other words, accepts date strings in the form of ``YYYY-MM-DD``. It accepts time zone offsets.

    :see: https://en.wikipedia.org/wiki/ISO_8601#Calendar_dates
    '''
    AWS_TIME = "AWS_TIME"
    '''``AWSTime`` scalar type represents a valid extended ``ISO 8601 Time`` string.

    In other words, accepts date strings in the form of ``hh:mm:ss.sss``. It accepts time zone offsets.

    :see: https://en.wikipedia.org/wiki/ISO_8601#Times
    '''
    AWS_DATE_TIME = "AWS_DATE_TIME"
    '''``AWSDateTime`` scalar type represents a valid extended ``ISO 8601 DateTime`` string.

    In other words, accepts date strings in the form of ``YYYY-MM-DDThh:mm:ss.sssZ``. It accepts time zone offsets.

    :see: https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations
    '''
    AWS_TIMESTAMP = "AWS_TIMESTAMP"
    '''``AWSTimestamp`` scalar type represents the number of seconds since ``1970-01-01T00:00Z``.

    Timestamps are serialized and deserialized as numbers.
    '''
    AWS_EMAIL = "AWS_EMAIL"
    '''``AWSEmail`` scalar type represents an email address string (i.e.``username@example.com``).'''
    AWS_JSON = "AWS_JSON"
    '''``AWSJson`` scalar type represents a JSON string.'''
    AWS_URL = "AWS_URL"
    '''``AWSURL`` scalar type represetns a valid URL string.

    URLs wihtout schemes or contain double slashes are considered invalid.
    '''
    AWS_PHONE = "AWS_PHONE"
    '''``AWSPhone`` scalar type represents a valid phone number. Phone numbers maybe be whitespace delimited or hyphenated.

    The number can specify a country code at the beginning, but is not required for US phone numbers.
    '''
    AWS_IP_ADDRESS = "AWS_IP_ADDRESS"
    '''``AWSIPAddress`` scalar type respresents a valid ``IPv4`` of ``IPv6`` address string.'''
    INTERMEDIATE = "INTERMEDIATE"
    '''Type used for Intermediate Types (i.e. an interface or an object type).'''


@jsii.implements(IIntermediateType)
class UnionType(metaclass=jsii.JSIIMeta, jsii_type="awscdk-appsync-utils.UnionType"):
    '''Union Types are abstract types that are similar to Interface Types, but they cannot to specify any common fields between types.

    Note that fields of a union type need to be object types. In other words,
    you can't create a union type out of interfaces, other unions, or inputs.
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        definition: typing.Sequence[IIntermediateType],
    ) -> None:
        '''
        :param name: the name of this type.
        :param definition: the object types for this union type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6161683262f7c00b259434a4d3102271f2aa76e29824e4b93276a85489fa9708)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = UnionTypeOptions(definition=definition)

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Add a field to this Union Type.

        Input Types must have field options and the IField must be an Object Type.

        :param field: The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''Create a GraphQL Type representing this Union Type.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string of this Union type.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''the attributes of this type.'''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''the name of this type.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]]:
        '''the authorization modes supported by this intermediate type.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894b886abb5950e0687fee08576588f7b1e6648db6eabb6275347adafa9cda94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="awscdk-appsync-utils.UnionTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition"},
)
class UnionTypeOptions:
    def __init__(self, *, definition: typing.Sequence[IIntermediateType]) -> None:
        '''Properties for configuring an Union Type.

        :param definition: the object types for this union type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a67ebf78c633e9f50b45c49821ff4a8bb7099ba22cbb1d999fc333c4a4078c)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }

    @builtins.property
    def definition(self) -> typing.List[IIntermediateType]:
        '''the object types for this union type.'''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.List[IIntermediateType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UnionTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIntermediateType)
class EnumType(metaclass=jsii.JSIIMeta, jsii_type="awscdk-appsync-utils.EnumType"):
    '''Enum Types are abstract types that includes a set of fields that represent the strings this type can create.'''

    def __init__(
        self,
        name: builtins.str,
        *,
        definition: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: the name of this type.
        :param definition: the attributes of this type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0a2fc224ca7f3d0db8cab41017a9d9fea55bb1e400fbb535c4303f3c3974c2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = EnumTypeOptions(definition=definition)

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Add a field to this Enum Type.

        To add a field to this Enum Type, you must only configure
        addField with the fieldName options.

        :param field: The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''Create an GraphQL Type representing this Enum Type.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string of this enum type.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''the attributes of this type.'''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''the name of this type.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]]:
        '''the authorization modes for this intermediate type.'''
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abfd440dbe5436b347b81db3c4037178295286172a5f800d9a85167e7a5376f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value) # pyright: ignore[reportArgumentType]


@jsii.implements(IField)
class GraphqlType(
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-appsync-utils.GraphqlType",
):
    '''The GraphQL Types in AppSync's GraphQL.

    GraphQL Types are the
    building blocks for object types, queries, mutations, etc. They are
    types like String, Int, Id or even Object Types you create.

    i.e. ``String``, ``String!``, ``[String]``, ``[String!]``, ``[String]!``

    GraphQL Types are used to define the entirety of schema.
    '''

    def __init__(
        self,
        type: Type,
        *,
        intermediate_type: typing.Optional[IIntermediateType] = None,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param type: the type of attribute.
        :param intermediate_type: the intermediate type linked to this attribute. Default: - no intermediate type
        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0404d8f16881b7c8d11666e2c5c73a1c679c4da175e9f5055a171ee84a018c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        options = GraphqlTypeOptions(
            intermediate_type=intermediate_type,
            is_list=is_list,
            is_required=is_required,
            is_required_list=is_required_list,
        )

        jsii.create(self.__class__, self, [type, options])

    @jsii.member(jsii_name="awsDate")
    @builtins.classmethod
    def aws_date(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSDate`` scalar type represents a valid extended ``ISO 8601 Date`` string.

        In other words, accepts date strings in the form of ``YYYY-MM-DD``. It accepts time zone offsets.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsDate", [options]))

    @jsii.member(jsii_name="awsDateTime")
    @builtins.classmethod
    def aws_date_time(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSDateTime`` scalar type represents a valid extended ``ISO 8601 DateTime`` string.

        In other words, accepts date strings in the form of ``YYYY-MM-DDThh:mm:ss.sssZ``. It accepts time zone offsets.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsDateTime", [options]))

    @jsii.member(jsii_name="awsEmail")
    @builtins.classmethod
    def aws_email(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSEmail`` scalar type represents an email address string (i.e.``username@example.com``).

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsEmail", [options]))

    @jsii.member(jsii_name="awsIpAddress")
    @builtins.classmethod
    def aws_ip_address(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSIPAddress`` scalar type respresents a valid ``IPv4`` of ``IPv6`` address string.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsIpAddress", [options]))

    @jsii.member(jsii_name="awsJson")
    @builtins.classmethod
    def aws_json(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSJson`` scalar type represents a JSON string.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsJson", [options]))

    @jsii.member(jsii_name="awsPhone")
    @builtins.classmethod
    def aws_phone(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSPhone`` scalar type represents a valid phone number. Phone numbers maybe be whitespace delimited or hyphenated.

        The number can specify a country code at the beginning, but is not required for US phone numbers.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsPhone", [options]))

    @jsii.member(jsii_name="awsTime")
    @builtins.classmethod
    def aws_time(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSTime`` scalar type represents a valid extended ``ISO 8601 Time`` string.

        In other words, accepts date strings in the form of ``hh:mm:ss.sss``. It accepts time zone offsets.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsTime", [options]))

    @jsii.member(jsii_name="awsTimestamp")
    @builtins.classmethod
    def aws_timestamp(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSTimestamp`` scalar type represents the number of seconds since ``1970-01-01T00:00Z``.

        Timestamps are serialized and deserialized as numbers.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsTimestamp", [options]))

    @jsii.member(jsii_name="awsUrl")
    @builtins.classmethod
    def aws_url(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``AWSURL`` scalar type represetns a valid URL string.

        URLs wihtout schemes or contain double slashes are considered invalid.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsUrl", [options]))

    @jsii.member(jsii_name="boolean")
    @builtins.classmethod
    def boolean(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``Boolean`` scalar type is a boolean value: true or false.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "boolean", [options]))

    @jsii.member(jsii_name="float")
    @builtins.classmethod
    def float(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``Float`` scalar type is a signed double-precision fractional value.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "float", [options]))

    @jsii.member(jsii_name="id")
    @builtins.classmethod
    def id(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``ID`` scalar type is a unique identifier. ``ID`` type is serialized similar to ``String``.

        Often used as a key for a cache and not intended to be human-readable.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "id", [options]))

    @jsii.member(jsii_name="int")
    @builtins.classmethod
    def int(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``Int`` scalar type is a signed non-fractional numerical value.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "int", [options]))

    @jsii.member(jsii_name="intermediate")
    @builtins.classmethod
    def intermediate(
        cls,
        *,
        intermediate_type: typing.Optional[IIntermediateType] = None,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''an intermediate type to be added as an attribute (i.e. an interface or an object type).

        :param intermediate_type: the intermediate type linked to this attribute. Default: - no intermediate type
        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = GraphqlTypeOptions(
            intermediate_type=intermediate_type,
            is_list=is_list,
            is_required=is_required,
            is_required_list=is_required_list,
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "intermediate", [options]))

    @jsii.member(jsii_name="string")
    @builtins.classmethod
    def string(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''``String`` scalar type is a free-form human-readable text.

        :param is_list: property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "string", [options]))

    @jsii.member(jsii_name="argsToString")
    def args_to_string(self) -> builtins.str:
        '''Generate the arguments for this field.'''
        return typing.cast(builtins.str, jsii.invoke(self, "argsToString", []))

    @jsii.member(jsii_name="directivesToString")
    def directives_to_string(
        self,
        _modes: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]] = None,
    ) -> builtins.str:
        '''Generate the directives for this field.

        :param _modes: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de2491458b16fcd82d4455c5fe3eed1f32ac5af6cd04b8c1044c44f4b1f6d39d)
            check_type(argname="argument _modes", value=_modes, expected_type=type_hints["_modes"])
        return typing.cast(builtins.str, jsii.invoke(self, "directivesToString", [_modes]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Generate the string for this attribute.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="isList")
    def is_list(self) -> builtins.bool:
        '''property determining if this attribute is a list i.e. if true, attribute would be ``[Type]``.

        :default: - false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isList"))

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> builtins.bool:
        '''property determining if this attribute is non-nullable i.e. if true, attribute would be ``Type!`` and this attribute must always have a value.

        :default: - false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isRequired"))

    @builtins.property
    @jsii.member(jsii_name="isRequiredList")
    def is_required_list(self) -> builtins.bool:
        '''property determining if this attribute is a non-nullable list i.e. if true, attribute would be ``[ Type ]!`` and this attribute's list must always have a value.

        :default: - false
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isRequiredList"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> Type:
        '''the type of attribute.'''
        return typing.cast(Type, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional[IIntermediateType]:
        '''the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type
        '''
        return typing.cast(typing.Optional[IIntermediateType], jsii.get(self, "intermediateType"))


@jsii.implements(IField)
class Field(
    GraphqlType,
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-appsync-utils.Field",
):
    '''Fields build upon Graphql Types and provide typing and arguments.'''

    def __init__(
        self,
        *,
        return_type: GraphqlType,
        args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param return_type: The return type for this field.
        :param args: The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: the directives for this field. Default: - no directives
        '''
        options = FieldOptions(
            return_type=return_type, args=args, directives=directives
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="argsToString")
    def args_to_string(self) -> builtins.str:
        '''Generate the args string of this resolvable field.'''
        return typing.cast(builtins.str, jsii.invoke(self, "argsToString", []))

    @jsii.member(jsii_name="directivesToString")
    def directives_to_string(
        self,
        modes: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]] = None,
    ) -> builtins.str:
        '''Generate the directives for this field.

        :param modes: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f577db5190cdaeb93ff236ffafd330a89711b9c51988f175fad1d2d49988bb96)
            check_type(argname="argument modes", value=modes, expected_type=type_hints["modes"])
        return typing.cast(builtins.str, jsii.invoke(self, "directivesToString", [modes]))

    @builtins.property
    @jsii.member(jsii_name="fieldOptions")
    def field_options(self) -> typing.Optional[ResolvableFieldOptions]:
        '''The options for this field.

        :default: - no arguments
        '''
        return typing.cast(typing.Optional[ResolvableFieldOptions], jsii.get(self, "fieldOptions"))


@jsii.implements(IField)
class ResolvableField(
    Field,
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-appsync-utils.ResolvableField",
):
    '''Resolvable Fields build upon Graphql Types and provide fields that can resolve into operations on a data source.'''

    def __init__(
        self,
        *,
        caching_config: typing.Optional[typing.Union[_aws_cdk_aws_appsync_ceddda9d.CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.Code] = None,
        data_source: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.BaseDataSource] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        pipeline_config: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
        response_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
        runtime: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.FunctionRuntime] = None,
        return_type: GraphqlType,
        args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param caching_config: The caching configuration for this resolver. Default: - No caching configuration
        :param code: The function code. Default: - no code is used
        :param data_source: The data source creating linked to this resolvable field. Default: - no data source
        :param max_batch_size: The maximum number of elements per batch, when using batch invoke. Default: - No max batch size
        :param pipeline_config: configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: The response mapping template for this resolver. Default: - No mapping template
        :param runtime: The functions runtime. Default: - no function runtime, VTL mapping templates used
        :param return_type: The return type for this field.
        :param args: The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: the directives for this field. Default: - no directives
        '''
        options = ResolvableFieldOptions(
            caching_config=caching_config,
            code=code,
            data_source=data_source,
            max_batch_size=max_batch_size,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
            runtime=runtime,
            return_type=return_type,
            args=args,
            directives=directives,
        )

        jsii.create(self.__class__, self, [options])

    @builtins.property
    @jsii.member(jsii_name="fieldOptions")
    def field_options(self) -> typing.Optional[ResolvableFieldOptions]:
        '''The options to make this field resolvable.

        :default: - not a resolvable field
        '''
        return typing.cast(typing.Optional[ResolvableFieldOptions], jsii.get(self, "fieldOptions"))


__all__ = [
    "AddFieldOptions",
    "BaseTypeOptions",
    "CodeFirstSchema",
    "Directive",
    "EnumType",
    "EnumTypeOptions",
    "Field",
    "FieldOptions",
    "GraphqlType",
    "GraphqlTypeOptions",
    "IField",
    "IIntermediateType",
    "ISourceApiAssociationMergeOperationProvider",
    "InputType",
    "InterfaceType",
    "IntermediateTypeOptions",
    "ObjectType",
    "ObjectTypeOptions",
    "ResolvableField",
    "ResolvableFieldOptions",
    "SourceApiAssociationMergeOperation",
    "SourceApiAssociationMergeOperationProps",
    "SourceApiAssociationMergeOperationProvider",
    "SourceApiAssociationMergeOperationProviderProps",
    "Type",
    "UnionType",
    "UnionTypeOptions",
]

publication.publish()

def _typecheckingstub__b3f7bf40e088a5358d687ebd351d88825ae33789f783d1e6cd8259d59b070eae(
    *,
    field: typing.Optional[IField] = None,
    field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7065f74822a55756dfdd04d334d6d9aeda625f057b769a1c5d723a14c5c21b68(
    *,
    is_list: typing.Optional[builtins.bool] = None,
    is_required: typing.Optional[builtins.bool] = None,
    is_required_list: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a13da742511cda4c22e130f0ce760a60c5ea4b0929532c99af50cc54424c219(
    field_name: builtins.str,
    field: ResolvableField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6eba0ea409aeaec11841e9c38849d69f255654e4e4477a7d7f084af1e327400(
    field_name: builtins.str,
    field: ResolvableField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bff174e03bcbd43939f0f37ef7ae8342e3b7b6cf26a03aea957fc1e10b6bf8b(
    field_name: builtins.str,
    field: Field,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9f8633b9db7d475ee2c6813fe75f25b5ddae546d8af2c3f49b16acb6a14d3b(
    addition: builtins.str,
    delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0348ee20fcaa775f1da67da997f7846fe6c3f2127c23cf5f3ec36a767f4d4150(
    type: IIntermediateType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b7b25abb239ddf168dc44ee3a4eafb7bfad77b9d39cd8d0d9aa0ed1ebd6cd2(
    api: _aws_cdk_aws_appsync_ceddda9d.IGraphqlApi,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1308f3efabd3e7b9dcdf6eb7834b172c6d93517ab709e8bc93ac01ee7b8f22ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb0ec8ae31c676028f4d85fdfb846f72b823ab78f507cdd47b3e02836e3a6d2(
    *groups: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad79404fa73c87b407fba3377261357963b7365ec001e2d4a32bdcdca5407eaf(
    statement: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2e92b47801a5b456c7fe7e7e762cebadbe3f15af33d5a2e06755afd79510d3(
    *mutations: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d443722171d0fe5b187acdd55e901af6389dd8fc7e14e25a520c2f1a9dff9d97(
    value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1da7562f56f9b9107c0b0d7046f7ccd21b01a88d0ce3474de7b40294a905c68(
    *,
    definition: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad31f19a88f952120497ae675333acfce84d98b4d21a4ad3521d5741cbc8376(
    *,
    return_type: GraphqlType,
    args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d88012e201a109aab5098626b5c843f128aa069d7b126cae9dae5d5d0fff70d(
    *,
    is_list: typing.Optional[builtins.bool] = None,
    is_required: typing.Optional[builtins.bool] = None,
    is_required_list: typing.Optional[builtins.bool] = None,
    intermediate_type: typing.Optional[IIntermediateType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba439f682dca6c0d6cac014656cc44ec08333c63bc46203e1cec8543e603c154(
    modes: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59011792f47c7b3f206fad46e7957254baf81026e11a95bc089849bec9048222(
    value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226c995dcf1aaebe1f3d25529cc4c7ce02a41eea21128a344d740a47c3b777de(
    source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdc112309278b6be6ab9b26dcba766d94191dd61ae1698f3395d586bfa999e9(
    name: builtins.str,
    *,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04942b830cddc421ab1b0d7336f8b7ea33c7c2f743130e41a124c23b7ded103a(
    value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd516fbb192c8cd673c922cc60ee779228f97b6b5c403db5802b0265e97753b3(
    name: builtins.str,
    *,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b62131c70cfa7326ff803ccc763fdb67b5c3a464ea8cc825440aca85bf9a9c1(
    value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef74b07a9cde3cbc0cabbab7080b59aa43a79762c12720f557d4c842026d3a0(
    *,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae86eda7501d76d7538544558a7ca59bedb940aded4c892041fb55221f5d0ed9(
    name: builtins.str,
    *,
    interface_types: typing.Optional[typing.Sequence[InterfaceType]] = None,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432233d1e5c3bc430b75552cc4ba1c77c92e16d5c648430047231ea8aff05106(
    api: _aws_cdk_aws_appsync_ceddda9d.IGraphqlApi,
    field_name: builtins.str,
    *,
    caching_config: typing.Optional[typing.Union[_aws_cdk_aws_appsync_ceddda9d.CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    code: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.Code] = None,
    data_source: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.BaseDataSource] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    pipeline_config: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.IAppsyncFunction]] = None,
    request_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
    response_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
    runtime: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.FunctionRuntime] = None,
    return_type: GraphqlType,
    args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220014e372ab0e12b1f7655a2e5689250db5a672a1c2a02b6af6011f0c4e4236(
    value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.Resolver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6f5f139b92d75136cf9b5d66e019140698c0595b617f6d311aa129946b385a(
    *,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
    interface_types: typing.Optional[typing.Sequence[InterfaceType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f9c784648f946b717a8bdaf534fc7ab76f1e73fc3b3f407664eb6a2a205224(
    *,
    return_type: GraphqlType,
    args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
    directives: typing.Optional[typing.Sequence[Directive]] = None,
    caching_config: typing.Optional[typing.Union[_aws_cdk_aws_appsync_ceddda9d.CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    code: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.Code] = None,
    data_source: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.BaseDataSource] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    pipeline_config: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.IAppsyncFunction]] = None,
    request_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
    response_mapping_template: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.MappingTemplate] = None,
    runtime: typing.Optional[_aws_cdk_aws_appsync_ceddda9d.FunctionRuntime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235f7ff7ceb5883b587fc3f0bbe9a0be54e7a137372f1f10b5c65bbe2f725720(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
    always_merge_on_stack_update: typing.Optional[builtins.bool] = None,
    merge_operation_provider: typing.Optional[ISourceApiAssociationMergeOperationProvider] = None,
    version_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544e8d04628c6e253021d39b2baad6d71ac9769e5e62697a339ea1013ce5fea1(
    *,
    source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
    always_merge_on_stack_update: typing.Optional[builtins.bool] = None,
    merge_operation_provider: typing.Optional[ISourceApiAssociationMergeOperationProvider] = None,
    version_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d485d6097bff7f9af62819a3345c4c946b935cd5177797dfd9b57304110270(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    polling_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59696b2ff46b70107f7548271c8015421099336faa1b1494f53cade7168ff5d7(
    source_api_association: _aws_cdk_aws_appsync_ceddda9d.ISourceApiAssociation,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6094717c36a5736f96eb3895a0ca8114c412e1c8b64a7459c643f02278e1e4d(
    *,
    polling_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    total_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6161683262f7c00b259434a4d3102271f2aa76e29824e4b93276a85489fa9708(
    name: builtins.str,
    *,
    definition: typing.Sequence[IIntermediateType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894b886abb5950e0687fee08576588f7b1e6648db6eabb6275347adafa9cda94(
    value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a67ebf78c633e9f50b45c49821ff4a8bb7099ba22cbb1d999fc333c4a4078c(
    *,
    definition: typing.Sequence[IIntermediateType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0a2fc224ca7f3d0db8cab41017a9d9fea55bb1e400fbb535c4303f3c3974c2(
    name: builtins.str,
    *,
    definition: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfd440dbe5436b347b81db3c4037178295286172a5f800d9a85167e7a5376f3(
    value: typing.Optional[typing.List[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0404d8f16881b7c8d11666e2c5c73a1c679c4da175e9f5055a171ee84a018c(
    type: Type,
    *,
    intermediate_type: typing.Optional[IIntermediateType] = None,
    is_list: typing.Optional[builtins.bool] = None,
    is_required: typing.Optional[builtins.bool] = None,
    is_required_list: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2491458b16fcd82d4455c5fe3eed1f32ac5af6cd04b8c1044c44f4b1f6d39d(
    _modes: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f577db5190cdaeb93ff236ffafd330a89711b9c51988f175fad1d2d49988bb96(
    modes: typing.Optional[typing.Sequence[_aws_cdk_aws_appsync_ceddda9d.AuthorizationType]] = None,
) -> None:
    """Type checking stubs"""
    pass
