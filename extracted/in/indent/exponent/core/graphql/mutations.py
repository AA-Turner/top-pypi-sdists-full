CREATE_CLOUD_CHAT_FROM_REPOSITORY_MUTATION = """
mutation CreateCloudChatFromRepository($repositoryUuid: UUID!, $provider: SandboxProvider) {
  createCloudChat(
    input: {repositoryUuid: $repositoryUuid, provider: $provider}
  ) {
    __typename
    ...on Chat {
      chatUuid
    }
    ...on CloudSessionError {
      message
    }
  }
}
"""
