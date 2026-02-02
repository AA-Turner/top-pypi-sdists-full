GET_CHATS_QUERY: str = """
    query Chats {
        chats {
            ... on UnauthenticatedError {
                message
            }
            ... on Chats {
                chats {
                    id
                    chatUuid
                    name
                    subtitle
                    isShared
                    isStarted
                    updatedAt # ISO datetime string
                }
            }
        }
    }
"""
CREATE_CLOUD_CONFIG_MUTATION: str = """
    mutation CreateCloudConfig(
        $githubOrgName: String!,
        $githubRepoName: String!,
        $setupCommands: [String!],
    ) {
        createCloudConfig(
            input: {
                githubOrgName: $githubOrgName,
                githubRepoName: $githubRepoName,
                setupCommands: $setupCommands,
            }
        ) {
            __typename
            ... on UnauthenticatedError {
                message
            }
            ... on CloudConfig {
                cloudConfigUuid
                githubOrgName
                githubRepoName
                setupCommands
                repoUrl
            }
        }
    }
"""
