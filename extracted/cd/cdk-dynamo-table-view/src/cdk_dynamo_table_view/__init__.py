'''
# cdk-dynamo-table-viewer

An AWS CDK construct which exposes a public HTTP endpoint which displays an HTML
page with the contents of a DynamoDB table in your stack.

**SECURITY NOTE**: this construct was built for demonstration purposes and
using it in production is probably a really bad idea. It exposes the entire
contents of a DynamoDB table in your account to the general public.

The library is published under the following names:

|Language|Repository
|--------|-----------
|JavaScript/TypeScript|[cdk-dynamo-table-viewer](https://www.npmjs.com/package/cdk-dynamo-table-viewer)
|Python|[cdk-dynamo-table-viewer](https://pypi.org/project/cdk-dynamo-table-viewer/)
|.NET|[Eladb.DynamoTableViewer](https://www.nuget.org/packages/Eladb.DynamoTableViewer/)
|Java|[com.github.eladb/cdk-dynamo-table-viewer](https://search.maven.org/artifact/com.github.eladb/cdk-dynamo-table-viewer)
|Go|[github.com/cdklabs/cdk-dynamo-table-viewer-go/dynamotableviewer](https://pkg.go.dev/github.com/cdklabs/cdk-dynamo-table-viewer-go/dynamotableviewer)

## Usage (TypeScript/JavaScript)

Install via npm:

```shell
$ npm i cdk-dynamo-table-viewer
```

Add to your CDK stack:

```python
# cookies_table: dynamodb.Table


viewer = TableViewer(self, "CookiesViewer",
    table=cookies_table,
    title="Cookie Sales",  # optional
    sort_by="-sales"
)
```

Notes:

* The endpoint will be available (as an deploy-time value) under `viewer.endpoint`.
  It will also be exported as a stack output.
* Paging is not supported. This means that only the first 1MB of items will be
  displayed (again, this is a demo...)
* Supports CDK version 2.60.0 and above

## License

Apache 2.0
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import constructs as _constructs_77d1e7e8


class TableViewer(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-dynamo-table-viewer.TableViewer",
):
    '''(experimental) Installs an endpoint in your stack that allows users to view the contents of a DynamoDB table through their browser.

    :stability: experimental
    '''

    def __init__(
        self,
        parent: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        table: _aws_cdk_aws_dynamodb_ceddda9d.ITable,
        endpoint_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointType] = None,
        sort_by: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parent: -
        :param id: -
        :param table: (experimental) The DynamoDB table to view. Note that all contents of this table will be visible to the public.
        :param endpoint_type: (experimental) The endpoint type of the `LambdaRestApi <https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.LambdaRestApi.html>`_ that will be created. Default: - EDGE
        :param sort_by: (experimental) Name of the column to sort by, prefix with "-" for descending order. Default: - No sort
        :param title: (experimental) The web page title. Default: - No title

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174ca8879bd9ef7eee5f6953d7c8f1e20b89be9ee3915564e1f8a62620b2f2d7)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TableViewerProps(
            table=table, endpoint_type=endpoint_type, sort_by=sort_by, title=title
        )

        jsii.create(self.__class__, self, [parent, id, props])

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))


@jsii.data_type(
    jsii_type="cdk-dynamo-table-viewer.TableViewerProps",
    jsii_struct_bases=[],
    name_mapping={
        "table": "table",
        "endpoint_type": "endpointType",
        "sort_by": "sortBy",
        "title": "title",
    },
)
class TableViewerProps:
    def __init__(
        self,
        *,
        table: _aws_cdk_aws_dynamodb_ceddda9d.ITable,
        endpoint_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointType] = None,
        sort_by: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param table: (experimental) The DynamoDB table to view. Note that all contents of this table will be visible to the public.
        :param endpoint_type: (experimental) The endpoint type of the `LambdaRestApi <https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.LambdaRestApi.html>`_ that will be created. Default: - EDGE
        :param sort_by: (experimental) Name of the column to sort by, prefix with "-" for descending order. Default: - No sort
        :param title: (experimental) The web page title. Default: - No title

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580431ee1f693be331305cf8cda0edff32e1b6f639aabdb809e678d30dc1ae15)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument sort_by", value=sort_by, expected_type=type_hints["sort_by"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if sort_by is not None:
            self._values["sort_by"] = sort_by
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def table(self) -> _aws_cdk_aws_dynamodb_ceddda9d.ITable:
        '''(experimental) The DynamoDB table to view.

        Note that all contents of this table will be
        visible to the public.

        :stability: experimental
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.ITable, result)

    @builtins.property
    def endpoint_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointType]:
        '''(experimental) The endpoint type of the `LambdaRestApi <https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.LambdaRestApi.html>`_ that will be created.

        :default: - EDGE

        :stability: experimental
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointType], result)

    @builtins.property
    def sort_by(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the column to sort by, prefix with "-" for descending order.

        :default: - No sort

        :stability: experimental
        '''
        result = self._values.get("sort_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''(experimental) The web page title.

        :default: - No title

        :stability: experimental
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableViewerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TableViewer",
    "TableViewerProps",
]

publication.publish()

def _typecheckingstub__174ca8879bd9ef7eee5f6953d7c8f1e20b89be9ee3915564e1f8a62620b2f2d7(
    parent: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    table: _aws_cdk_aws_dynamodb_ceddda9d.ITable,
    endpoint_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointType] = None,
    sort_by: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580431ee1f693be331305cf8cda0edff32e1b6f639aabdb809e678d30dc1ae15(
    *,
    table: _aws_cdk_aws_dynamodb_ceddda9d.ITable,
    endpoint_type: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.EndpointType] = None,
    sort_by: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
