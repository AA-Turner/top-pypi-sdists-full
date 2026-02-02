EVENTS_FOR_CHAT_QUERY: str = """query EventsForChat($chatUuid: UUID!) {
  eventsForChat(chatUuid: $chatUuid) {
    ... on EventHistory {
      events {
        ... on UserEvent {
          uuid
          parentUuid
          isSidechain
          version
          createdAt
          sidechainRootUuid
          synthetic
          messageData: message {
            ... on TextMessage {
              text
            }
            ... on ToolCallMessage {
              messageId
              toolUseId
              toolName
              toolInput {
                ... on BashToolInput {
                  command
                }
                ... on ReadToolInput {
                  filePath
                }
              }
            }
            ... on ToolResultMessage {
              messageId
              toolUseId
              text
              resultData {
                ... on BashToolResult {
                  shellOutput
                  exitCode
                }
                ... on ReadToolResult {
                  content
                }
              }
            }
          }
        }
        ... on AssistantEvent {
          uuid
          parentUuid
          isSidechain
          version
          createdAt
          sidechainRootUuid
          synthetic
          messageData: message {
            ... on TextMessage {
              text
            }
            ... on ToolCallMessage {
              messageId
              toolUseId
              toolName
              toolInput {
                ... on BashToolInput {
                  command
                }
                ... on ReadToolInput {
                  filePath
                }
              }
            }
          }
        }
        ... on SystemEvent {
          uuid
          parentUuid
          isSidechain
          version
          createdAt
          sidechainRootUuid
          messageData: message {
            ... on ToolCallMessage {
              messageId
              toolUseId
              toolName
              toolInput {
                ... on BashToolInput {
                  command
                }
                ... on ReadToolInput {
                  filePath
                }
              }
            }
            ... on ToolResultMessage {
              messageId
              toolUseId
              text
              resultData {
                ... on BashToolResult {
                  shellOutput
                  exitCode
                }
                ... on ReadToolResult {
                  content
                }
              }
            }
            ... on ToolExecutionStatusMessage {
              executionStatus: status
            }
            ... on ToolPermissionStatusMessage {
              permissionStatus: status
            }
          }
        }
      }
    }
  }
}
"""
