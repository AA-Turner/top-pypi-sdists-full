#!/usr/bin/env python3

import argparse
import os
from contextlib import nullcontext

from grazie.api.client._common import LLMChatApiVersion, LLMCompletionApiVersion
from grazie.api.client.chat.prompt import ChatPrompt as ChatPromptV6
from grazie.api.client.completion.prompt import CompletionPrompt as CompletionPromptV3
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import AuthType, GrazieAgent, GrazieApiGatewayClient
from grazie.api.client.profiles import LLMProfile, Profile
from grazie.api.client.v8.chat.prompt import ChatPrompt as ChatPromptV8
from grazie.api.client.v8.completion.prompt import (
    CompletionPrompt as CompletionPromptV8,
)


def get_client(args: argparse.Namespace) -> GrazieApiGatewayClient:
    return GrazieApiGatewayClient(
        grazie_agent=GrazieAgent(name="grazie-api-gateway-client", version="dev"),
        url=args.gateway,
        auth_type=AuthType.USER,
        grazie_jwt_token=args.token,
    )


def completion(args: argparse.Namespace) -> None:
    client = get_client(args)

    if args.version == "3" or args.version is None:
        response = client.complete(
            prompt=CompletionPromptV3(args.prompt),
            profile=Profile.get_by_name(args.profile),
        )
        print(response.completion)

    elif args.version == "8":
        response = client.v8.complete(
            prompt=CompletionPromptV8(args.prompt),
            profile=Profile.get_by_name(args.profile),
        )
        print(response.content)

    else:
        print(f"Completion version {args.version} is not supported.")


def chat(args: argparse.Namespace) -> None:
    client = get_client(args)

    if args.version == "6" or args.version is None:
        response = client.chat(
            chat=ChatPromptV6().add_system(args.system).add_user(args.prompt),
            profile=Profile.get_by_name(args.profile),
        )
        print(response.content)

    elif args.version == "8":
        response = client.v8.chat(
            chat=ChatPromptV8().add_system(args.system).add_user(args.prompt),
            profile=Profile.get_by_name(args.profile),
        )
        print(response.content)

    else:
        print(f"Chat version {args.version} is not supported.")


def main() -> None:
    profiles = sorted(
        [
            value.name
            for attr in dir(Profile)
            for value in (getattr(Profile, attr),)
            if isinstance(value, LLMProfile)
        ]
    )

    parser = argparse.ArgumentParser(description="Grazie API Gateway Client")
    parser.add_argument(
        "-g", "--gateway", type=str, required=False, default=GrazieApiGatewayUrls.STAGING
    )
    parser.add_argument(
        "-p", "--profile", required=False, choices=profiles, default=Profile.OPENAI_CHAT_GPT.name
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        default=os.environ.get("GRAZIE_JWT_TOKEN", None),
        help=argparse.SUPPRESS,
    )
    subparsers = parser.add_subparsers()

    with nullcontext(subparsers.add_parser("completion")) as subparser:
        subparser.add_argument(
            "-v",
            "--version",
            required=False,
            choices=[str(x.value) for x in LLMCompletionApiVersion],
            default=None,
        )
        subparser.add_argument("prompt")
        subparser.set_defaults(func=completion)

    with nullcontext(subparsers.add_parser("chat")) as subparser:
        subparser.add_argument(
            "-v",
            "--version",
            required=False,
            choices=[str(x.value) for x in LLMChatApiVersion],
            default=None,
        )
        subparser.add_argument("-s", "--system", type=str, default="You are a helpful assistant.")
        subparser.add_argument("prompt")
        subparser.set_defaults(func=chat)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
