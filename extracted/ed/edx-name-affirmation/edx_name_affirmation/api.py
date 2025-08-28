"""
Python API for edx_name_affirmation.
"""

import logging

from django.core.exceptions import ObjectDoesNotExist

from edx_name_affirmation.exceptions import (
    VerifiedNameAttemptIdNotGiven,
    VerifiedNameDoesNotExist,
    VerifiedNameEmptyString,
    VerifiedNameMultipleAttemptIds
)
from edx_name_affirmation.models import VerifiedName, VerifiedNameConfig
from edx_name_affirmation.statuses import VerifiedNameStatus

log = logging.getLogger(__name__)


def create_verified_name(
    user, verified_name, profile_name, verification_attempt_id=None,
    proctored_exam_attempt_id=None, platform_verification_attempt_id=None,
    status=VerifiedNameStatus.PENDING,
):
    """
    Create a new `VerifiedName` for the given user.

    Arguments:
        * `user` (User object)
        * `verified_name` (str): Representative of the name on the user's physical ID card.
        * `profile_name` (str): A snapshot of either 1) the user's pending name change if given
          or 2) the existing name on the user's profile.
        * `verification_attempt_id` (int): Optional reference to an external ID verification
          attempt.
        * `proctored_exam_attempt_id` (int): Optional reference to an external proctored exam
          attempt.
        * `platform_verification_attempt_id` (int): Optional reference to a platform defined
          verification attempt.
        * `is_verified` (bool): Optional, defaults False. This should determine whether the
          verified_name is valid for use with ID verification, exams, etc.
    """
    # Do not allow empty strings
    if verified_name == '':
        raise VerifiedNameEmptyString('verified_name', user.id)
    if profile_name == '':
        raise VerifiedNameEmptyString('profile_name', user.id)

    # Only link to one attempt
    if sum(map(bool, [proctored_exam_attempt_id, verification_attempt_id, platform_verification_attempt_id])) > 1:
        err_msg = (
            'Attempted to create VerifiedName for user_id={user_id}, but at least two different '
            'external attempt IDs were given. Only one may be used. '
            'verification_attempt_id={verification_attempt_id}, '
            'proctored_exam_attempt_id={proctored_exam_attempt_id}, '
            'platform_verification_attempt_id={platform_verification_attempt_id}, '
            'status={status}'.format(
                user_id=user.id, verification_attempt_id=verification_attempt_id,
                proctored_exam_attempt_id=proctored_exam_attempt_id, status=status,
                platform_verification_attempt_id=platform_verification_attempt_id,
            )
        )
        raise VerifiedNameMultipleAttemptIds(err_msg)

    VerifiedName.objects.create(
        user=user,
        verified_name=verified_name,
        profile_name=profile_name,
        verification_attempt_id=verification_attempt_id,
        proctored_exam_attempt_id=proctored_exam_attempt_id,
        platform_verification_attempt_id=platform_verification_attempt_id,
        status=status,
    )

    log_msg = (
        'VerifiedName created for user_id={user_id}. '
        'verification_attempt_id={verification_attempt_id}, '
        'proctored_exam_attempt_id={proctored_exam_attempt_id}, '
        'status={status}'.format(
            user_id=user.id, verification_attempt_id=verification_attempt_id,
            proctored_exam_attempt_id=proctored_exam_attempt_id, status=status,
        )
    )
    log.info(log_msg)


def get_verified_name(user, is_verified=False, statuses_to_exclude=None):
    """
    Get the most recent VerifiedName for a given user.

    Arguments:
        * `user` (User object)
        * `is_verified` (bool): Optional, set to True to ignore entries that are not
          verified.
        * `statuses_to_exclude` (list): Optional list of statuses to filter out. Only
          relevant if `is_verified` is False.

    Returns a VerifiedName object.
    """
    verified_name_qs = VerifiedName.objects.filter(user=user).order_by('-created')

    if is_verified:
        return verified_name_qs.filter(status=VerifiedNameStatus.APPROVED.value).first()

    if statuses_to_exclude:
        return verified_name_qs.exclude(status__in=statuses_to_exclude).first()

    return verified_name_qs.first()


def delete_verified_name(verified_name_id):
    """
    Delete a VerifiedName.
    """
    try:
        verified_name = VerifiedName.objects.get(id=verified_name_id)
        verified_name.delete()
    except ObjectDoesNotExist as exc:
        err_msg = (
            'Attempted to delete verified_name_id={verified_name_id}'
            'but it does not exist'.format(verified_name_id=verified_name_id)
        )
        raise VerifiedNameDoesNotExist(err_msg) from exc


def get_verified_name_history(user):
    """
    Return a QuerySet of all VerifiedNames for a given user, ordered by the date created from
    most recent.

    Arguments:
        * `user` (User object)
    """
    return VerifiedName.objects.filter(user=user).order_by('-created')


def update_verified_name_status(
    user, status, verification_attempt_id=None, proctored_exam_attempt_id=None, platform_verification_attempt_id=None,
):
    """
    Update the status of a VerifiedName using the linked ID verification, exam attempt ID, or platform defined
    verification attempt ID. Only one of these should be specified.

    Arguments:
        * user (User object)
        * status (Verified Name Status)
        * verification_attempt_id (int): Optional reference to an external ID verification
          attempt.
        * proctored_exam_attempt_id (int): Optional reference to an external proctored exam
          attempt.
        * platform_verification_attempt_id (int): Optional reference to a platform defined
          verification attempt.
    """
    filters = {'user': user}

    if sum(map(bool, [proctored_exam_attempt_id, verification_attempt_id, platform_verification_attempt_id])) > 1:
        err_msg = (
            'Attempted to update the status for a VerifiedName, but at least two different '
            'attempt IDs were given. verification_attempt_id={verification_attempt_id}, '
            'proctored_exam_attempt_id={proctored_exam_attempt_id},'
            'platform_verification_attempt_id={platform_verification_attempt_id}'.format(
                verification_attempt_id=verification_attempt_id,
                proctored_exam_attempt_id=proctored_exam_attempt_id,
                platform_verification_attempt_id=platform_verification_attempt_id,
            )
        )
        raise VerifiedNameMultipleAttemptIds(err_msg)

    if verification_attempt_id:
        filters['verification_attempt_id'] = verification_attempt_id
    elif proctored_exam_attempt_id:
        filters['proctored_exam_attempt_id'] = proctored_exam_attempt_id
    elif platform_verification_attempt_id:
        filters['platform_verification_attempt_id'] = platform_verification_attempt_id
    else:
        err_msg = (
            'Attempted to update the status for a VerifiedName, but no '
            'verification_attempt_id or proctored_exam_attempt_id was given.'
        )
        raise VerifiedNameAttemptIdNotGiven(err_msg)

    verified_name_obj = VerifiedName.objects.filter(**filters).order_by('-created').first()

    if not verified_name_obj:
        err_msg = (
            'Attempted to update status={status} for a VerifiedName, but one does '
            'not exist for the given attempt ID. verification_attempt_id={verification_attempt_id}, '
            'proctored_exam_attempt_id={proctored_exam_attempt_id}'.format(
                status=status,
                verification_attempt_id=verification_attempt_id,
                proctored_exam_attempt_id=proctored_exam_attempt_id,
            )
        )
        raise VerifiedNameDoesNotExist(err_msg)

    verified_name_obj.status = status
    verified_name_obj.save()

    log_msg = (
        'Updated status={status} for VerifiedName belonging to user_id={user_id}. '
        'verification_attempt_id={verification_attempt_id}, '
        'proctored_exam_attempt_id={proctored_exam_attempt_id}'.format(
            status=status,
            user_id=verified_name_obj.user.id,
            verification_attempt_id=verification_attempt_id,
            proctored_exam_attempt_id=proctored_exam_attempt_id,
        )
    )
    log.info(log_msg)

    return verified_name_obj


def create_verified_name_config(user, use_verified_name_for_certs=None):
    """
    Create verified name configuration for the given user.

    Arguments:
        * `user` (User object)
        * `use_verified_name_for_certs` (bool): If True, certificates will prioritize
          the user's verified name over their profile name.
    """
    fields = {'user': user}

    # Default to the values from the most recent config
    existing_config = VerifiedNameConfig.objects.filter(user=user).order_by('-change_date').first()
    if existing_config:
        fields['use_verified_name_for_certs'] = existing_config.use_verified_name_for_certs

    if use_verified_name_for_certs is not None:
        fields['use_verified_name_for_certs'] = use_verified_name_for_certs

    config_obj = VerifiedNameConfig.objects.create(**fields)

    log_msg = (
        'Created verified name config for user_id={user_id} with '
        'use_verified_name_for_certs={use_verified_name_for_certs}'.format(
            user_id=config_obj.user.id,
            use_verified_name_for_certs=config_obj.use_verified_name_for_certs,
        )
    )
    log.info(log_msg)


def should_use_verified_name_for_certs(user):
    """
    Returns a boolean describing whether the user has opted to use their verified
    name over their profile name for certificates.
    Arguments:
        * `user` (User object)
    """
    config_obj = VerifiedNameConfig.current(user)
    return config_obj.use_verified_name_for_certs
