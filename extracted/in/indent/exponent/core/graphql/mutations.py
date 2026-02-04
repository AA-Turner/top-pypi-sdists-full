CREATE_CLOUD_CHAT_FROM_REPOSITORY_MUTATION = """
mutation CreateCloudChatFromRepository($repositoryId: String!, $provider: SandboxProvider) {
  createCloudChat(repositoryId: $repositoryId, provider: $provider) {
    __typename
    ...on Chat {
      chatUuid
    }
    ...on UnauthenticatedError {
      message
    }
    ...on NotFoundError {
      resourceType
      resourceId
      message
    }
    ...on CloudSessionError {
      message
    }
  }
}
"""
