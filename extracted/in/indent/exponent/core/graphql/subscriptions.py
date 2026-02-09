AUTHENTICATED_USER_SUBSCRIPTION = """
    subscription AuthenticatedUserSubscription($token: String!) {
            testAuthenticatedUser: testAuthenticatedUser(token: $token) {
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
