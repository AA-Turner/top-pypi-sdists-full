import asyncio
from typing import Any, Coroutine, Optional, Tuple, Type

from grpc import aio
from grpc_reflection.v1alpha import reflection

from jetpack.config import _symbols
from jetpack.core._jetpack_client import default_jetpack_client
from jetpack.proto.runtime.v1alpha1 import jetworker_pb2, jetworker_pb2_grpc


async def start_grpc_server(port: str) -> None:

    print(f"starting the grpc server on port {port}")
    server = aio.server()  # grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jetworker_pb2_grpc.add_JetworkerServicer_to_server(JetworkerServicer(), server)

    # ref. https://github.com/grpc/grpc/blob/master/doc/python/server_reflection.md
    service_names = (
        jetworker_pb2.DESCRIPTOR.services_by_name["Jetworker"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    print("SUCCESS: started the grpc server")
    await server.wait_for_termination()


class JetworkerServicer(jetworker_pb2_grpc.JetworkerServicer):

    # Need to figure out grpc request types
    #
    # getting nox-py2 error for typechecking:
    #
    # Return type "Coroutine[Any, Any, StartJetroutineResponse]" of "StartJetroutine"
    # incompatible with return type "StartJetroutineResponse" in supertype "JetworkerServicer"
    async def StartJetroutine(  # type: ignore
        self, request: jetworker_pb2.StartJetroutineRequest, context: Any
    ) -> jetworker_pb2.StartJetroutineResponse:
        func = _symbols.get_symbol_table().get_registered_symbols()[
            request.qualified_symbol
        ]

        args = b""
        if request.encoded_args:
            args = request.encoded_args.encode()

        await default_jetpack_client.jetroutine(func)._exec(request.exec_id, args)
        return jetworker_pb2.StartJetroutineResponse()
