AUTHENTICATED_USER_SUBSCRIPTION = """
    subscription {
            testAuthenticatedUser {
                __typename
                ... on UnauthenticatedError {
                    message
                }
                ...on Error {
                    message
                }
                ... on User {
                    userUuid
                }
            }
        }
"""
