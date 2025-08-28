"""
Name Affirmation HTTP-based API endpoints
"""

from edx_api_doc_tools import path_parameter, query_parameter, schema
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import status as http_status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from edx_name_affirmation.api import (
    create_verified_name,
    create_verified_name_config,
    delete_verified_name,
    get_verified_name,
    get_verified_name_history,
    should_use_verified_name_for_certs,
    update_verified_name_status
)
from edx_name_affirmation.exceptions import (
    VerifiedNameAttemptIdNotGiven,
    VerifiedNameDoesNotExist,
    VerifiedNameMultipleAttemptIds
)
from edx_name_affirmation.serializers import (
    UpdateVerifiedNameSerializer,
    VerifiedNameConfigSerializer,
    VerifiedNameSerializer
)
from edx_name_affirmation.statuses import VerifiedNameStatus


class AuthenticatedAPIView(APIView):

    """
    Authenticate API View.
    """

    authentication_classes = (SessionAuthentication, JwtAuthentication)
    permission_classes = (IsAuthenticated,)


class VerifiedNameView(AuthenticatedAPIView):
    """
    Endpoint for a VerifiedName.

    Supports:
        HTTP POST: Creates a new VerifiedName.
        HTTP GET: Returns an existing VerifiedName (by username or requesting user)
        HTTP PATCH: Update the status of a VerifiedName
        HTTP DELETE: Delete a VerifiedName
    """
    @schema(
        parameters=[
            query_parameter('username', str, 'The username of which verified name records might be associated'),
        ],
        responses={
            200: 'The verified_name record associated with the username provided',
            403: 'User lacks required permission. Only an edX staff user can invoke this API',
            404: 'The verified_name record associated with the username provided does not exist.'
        },
    )
    def get(self, request):
        """
        Get most recent verified name for the request user or for the specified username
        For example: /edx_name_affirmation/v1/verified_name?username=jdoe

        Example response: {
            "username": "jdoe",
            "verified_name": "Jonathan Doe",
            "profile_name": "Jon Doe",
            "verification_attempt_id": 123,
            "proctored_exam_attempt_id": None,
            "status": "approved",
            "use_verified_name_for_certs": False,
        }
        """
        username = request.GET.get('username')
        if username and not request.user.is_staff:
            return Response(
                status=http_status.HTTP_403_FORBIDDEN,
                data={"detail": "Must be a Staff User to Perform this request."}
            )

        user = get_user_model().objects.get(username=username) if username else request.user
        verified_name = get_verified_name(user, is_verified=True)
        if verified_name is None:
            return Response(
                status=404,
                data={'detail': 'There is no verified name related to this user.'}
            )

        serialized_data = VerifiedNameSerializer(verified_name).data
        serialized_data['use_verified_name_for_certs'] = should_use_verified_name_for_certs(user)
        return Response(serialized_data)

    @schema(
        body=VerifiedNameSerializer(),
        responses={
            200: 'The verified_name record associated with the username provided is successfully created',
            403: 'User lacks required permission. Only an edX staff user can invoke this API',
            400: 'The posted data have conflicts with already stored verified name'
        },
    )
    def post(self, request):
        """
        Creates a new VerifiedName.

        Expected POST data: {
            "username": "jdoe",
            "verified_name": "Jonathan Doe"
            "profile_name": "Jon Doe"
            "verification_attempt_id": (Optional)
            "proctored_exam_attempt_id": (Optional)
            "platform_verification_attempt_id": (Optional)
            "status": (Optional)
        }
        """
        username = request.data.get('username')
        if username != request.user.username and not request.user.is_staff:
            return Response(
                status=http_status.HTTP_403_FORBIDDEN,
                data={"detail": "Must be a Staff User to Perform this request."}
            )

        serializer = VerifiedNameSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.get(username=username) if username else request.user
            try:
                create_verified_name(
                    user,
                    request.data.get('verified_name'),
                    request.data.get('profile_name'),
                    verification_attempt_id=request.data.get('verification_attempt_id', None),
                    proctored_exam_attempt_id=request.data.get('proctored_exam_attempt_id', None),
                    platform_verification_attempt_id=request.data.get('platform_verification_attempt_id', None),
                    status=request.data.get('status', VerifiedNameStatus.PENDING)
                )
                response_status = http_status.HTTP_200_OK
                data = {}
            except VerifiedNameMultipleAttemptIds as exc:
                response_status = http_status.HTTP_400_BAD_REQUEST
                data = {"detail": str(exc)}
        else:
            response_status = http_status.HTTP_400_BAD_REQUEST
            data = serializer.errors
        return Response(status=response_status, data=data)

    @schema(
        body=UpdateVerifiedNameSerializer(),
        responses={
            200: 'The verified_name record associated with the username provided is successfully edited',
            403: 'User lacks required permission. Only an edX staff user can invoke this API',
            400: 'The edit action failed validation rules'
        },
    )
    def patch(self, request):
        """
        Update verified name status

        Example PATCH data: {
                "username": "jdoe",
                "verification_attempt_id" OR "proctored_exam_attempt_id": 123,
                "status": "approved",
            }
        """
        if not request.user.is_staff:
            return Response(
                status=http_status.HTTP_403_FORBIDDEN,
                data={'detail': 'Must be a staff user to update verified name status.'}
            )

        serializer = UpdateVerifiedNameSerializer(data=request.data)

        if serializer.is_valid():
            username = request.data.get('username')
            user = get_user_model().objects.get(username=username)
            try:
                verified_name = update_verified_name_status(
                    user,
                    request.data.get('status'),
                    request.data.get('verification_attempt_id', None),
                    request.data.get('proctored_exam_attempt_id', None)
                )
                response_status = http_status.HTTP_200_OK
                data = VerifiedNameSerializer(verified_name).data
            except (VerifiedNameAttemptIdNotGiven, VerifiedNameMultipleAttemptIds) as exc:
                response_status = http_status.HTTP_400_BAD_REQUEST
                data = {'detail': str(exc)}
            except VerifiedNameDoesNotExist as exc:
                response_status = http_status.HTTP_404_NOT_FOUND
                data = {'detail': str(exc)}
        else:
            response_status = http_status.HTTP_400_BAD_REQUEST
            data = serializer.errors

        return Response(status=response_status, data=data)

    @schema(
        parameters=[
            path_parameter('verified_name_id', str, 'The database id of the verified_name to be deleted'),
        ],
        responses={
            204: 'The verified_name record associated with the id is successfully deleted from data store',
            403: 'User lacks required permission. Only an edX staff user can invoke this API',
            404: 'The verified_name record associated with the id provided does not exist.'
        },
    )
    def delete(self, request, verified_name_id):
        """
        Delete verified name
        /edx_name_affirmation/v1/verified_name/{verified_name_id}
        """
        if not request.user.is_staff:
            return Response(
                status=http_status.HTTP_403_FORBIDDEN,
                data={'detail': 'Must be a staff user to delete a verified name.'}
            )

        try:
            delete_verified_name(verified_name_id)
            response_status = http_status.HTTP_204_NO_CONTENT
            data = {}
        except VerifiedNameDoesNotExist as exc:
            response_status = http_status.HTTP_404_NOT_FOUND
            data = {'detail': str(exc)}

        return Response(status=response_status, data=data)


class VerifiedNameHistoryView(AuthenticatedAPIView):
    """
    Endpoint for VerifiedName history.
    /edx_name_affirmation/v1/verified_name/history?username=xxx

    Supports:
        HTTP GET: Return a list of VerifiedNames for the given user.
    """
    @schema(
        parameters=[
            query_parameter('username', str, 'The username of which verified name records might be associated'),
        ],
        responses={
            200: 'The verified_name record associated with the username provided is successfully edited',
            403: 'User lacks required permission. Only an edX staff user can invoke this API',
        },
    )
    def get(self, request):
        """
        Get a list of verified name objects for the given user, ordered by most recently created.
        """
        username = request.GET.get('username')
        if username and not request.user.is_staff:
            return Response(
                status=http_status.HTTP_403_FORBIDDEN,
                data={"detail": "Must be a Staff User to Perform this request."}
            )

        user = get_user_model().objects.get(username=username) if username else request.user
        verified_name_qs = get_verified_name_history(user)
        serializer = VerifiedNameSerializer(verified_name_qs, many=True)

        serialized_data = {
            'use_verified_name_for_certs': should_use_verified_name_for_certs(user),
            'results': serializer.data,
        }

        return Response(serialized_data)


class VerifiedNameConfigView(AuthenticatedAPIView):
    """
    Endpoint for VerifiedNameConfig.
    /edx_name_affirmation/v1/verified_name/config

    Supports:
        HTTP POST: Creates a new VerifiedNameConfig.

    HTTP POST
    Creates a new VerifiedName.

    Example POST data: {
        "username": "jdoe",
        "use_verified_name_for_certs": True
    }
    """
    @schema(
        body=VerifiedNameConfigSerializer(),
        responses={
            201: 'The verified_name configuration record is successfully created',
            403: 'User lacks required permission. Only an edX staff user can invoke this API',
            400: 'The POSTed data failed validation rules',
        },
    )
    def post(self, request):
        """
        Create VerifiedNameConfig
        """
        username = request.data.get('username')
        if username != request.user.username and not request.user.is_staff:
            msg = 'Must be a staff user to override the requested user’s VerifiedNameConfig value'
            return Response(status=http_status.HTTP_403_FORBIDDEN, data={'detail': msg})

        serializer = VerifiedNameConfigSerializer(data=request.data)

        if serializer.is_valid():
            user = get_user_model().objects.get(username=username) if username else request.user
            create_verified_name_config(
                user,
                use_verified_name_for_certs=request.data.get('use_verified_name_for_certs'),
            )
            response_status = http_status.HTTP_201_CREATED
            data = {}

        else:
            response_status = http_status.HTTP_400_BAD_REQUEST
            data = serializer.errors

        return Response(status=response_status, data=data)
