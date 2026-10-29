__lazy_modules__ = ["django.http"]

import logging
from typing import Any, TYPE_CHECKING

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Count
from django.http import Http404, HttpRequest,  HttpResponseBase
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from allianceauth.notifications import notify
from allianceauth.groupmanagement.managers import GroupManager
from allianceauth.groupmanagement.models import Group, GroupRequest, RequestLog
from allianceauth.framework.datatables import DataTablesView

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_management(request: "HttpRequest") -> "HttpResponse":
    logger.debug(f"group_management called by user {request.user}")
    acceptrequests = []
    leaverequests = []

    base_group_query = GroupRequest.objects.select_related('user', 'group', 'user__profile__main_character')
    if GroupManager.has_management_permission(request.user):
        # Full access
        group_requests = base_group_query.all()
    else:
        # Group specific leader
        users__groups = GroupManager.get_group_leaders_groups(request.user)
        group_requests = base_group_query.filter(group__in=users__groups)

    for grouprequest in group_requests:
        if grouprequest.leave_request:
            leaverequests.append(grouprequest)
        else:
            acceptrequests.append(grouprequest)

    logger.debug(f"Providing user {request.user} with {len(acceptrequests)} acceptrequests and {len(leaverequests)} leaverequests.")

    show_leave_tab = (
        getattr(settings, 'GROUPMANAGEMENT_AUTO_LEAVE', False)
        and not GroupRequest.objects.filter(leave_request=True).exists()
    )

    render_items = {
        'acceptrequests': acceptrequests,
        'leaverequests': leaverequests,
        'show_leave_tab': show_leave_tab,
    }

    return render(request, 'groupmanagement/index.html', context=render_items)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership(request: "HttpRequest") -> "HttpResponse":
    logger.debug(f"group_membership called by user {request.user}")
    # Get all open and closed groups
    if GroupManager.has_management_permission(request.user):
        # Full access
        groups = GroupManager.get_all_non_internal_groups()
    else:
        # Group leader specific
        groups = GroupManager.get_group_leaders_groups(request.user)

    groups = groups.exclude(authgroup__internal=True).annotate(num_members=Count('user')).order_by('name')

    render_items = {'groups': groups}

    return render(request, 'groupmanagement/groupmembership.html', context=render_items)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership_audit(request: "HttpRequest", group_id: int) -> "HttpResponse":
    logger.debug(f"group_management_audit called by user {request.user}")
    group = get_object_or_404(Group, id=group_id)

    # Check its a joinable group i.e. not corp or internal
    # And the user has permission to manage it
    if not GroupManager.check_internal_group(group) or not GroupManager.can_manage_group(request.user, group):
        logger.warning(f"User {request.user} attempted to view the membership of group {group_id} but permission was denied")

        raise PermissionDenied

    # Fetch the distinct filter values in a single query and build unique
    # lists on the Python side to avoid multiple DB round-trips.
    values_qs = RequestLog.objects.filter(group=group).values(
        "request_type",
        "action",
        "requestor__pk",
        "requestor__username",
        "requestor__profile__main_character__pk",
        "requestor__profile__main_character__character_name",
        "requestor__profile__main_character__corporation_id",
        "requestor__profile__main_character__corporation_name",
        "request_actor__pk",
        "request_actor__username",
    ).distinct()

    type_set = set()
    action_set = set()
    requestors_set = set()
    characters_set = set()
    corporations_set = set()
    actors_set = set()

    for value in values_qs:
        type_set.add(value.get("request_type"))
        action_set.add(value.get("action"))

        if value.get("requestor__pk") is not None:
            requestors_set.add(
                (value.get("requestor__pk"), value.get("requestor__username"))
            )

        if value.get("requestor__profile__main_character__pk") is not None:
            characters_set.add(
                (
                    value.get("requestor__profile__main_character__pk"),
                    value.get("requestor__profile__main_character__character_name"),
                )
            )

        if value.get("requestor__profile__main_character__corporation_id") is not None:
            corporations_set.add(
                (
                    value.get("requestor__profile__main_character__corporation_id"),
                    value.get("requestor__profile__main_character__corporation_name"),
                )
            )

        # Request actor cannot be null, so no check needed here
        actors_set.add(
            (
                value.get("request_actor__pk"),
                value.get("request_actor__username")
            )
        )

    render_items = {
        "group": group,
        "filter": {
            "requestors": sorted(list(requestors_set), key=lambda x: x[1] or ""),
            "character_names": sorted(list(characters_set), key=lambda x: x[1] or ""),
            "corporation_names": sorted(list(corporations_set), key=lambda x: x[1] or ""),
            "types": [
                (type, RequestLog.Type(type).label)
                for type in sorted(type_set)
                if type is not None
            ],
            "actions": [
                (action, RequestLog.Action(action).label)
                for action in sorted(action_set)
                if action is not None
            ],
            "actors": sorted(list(actors_set), key=lambda x: x[1] or ""),
        }
    }

    return render(request, 'groupmanagement/audit.html', context=render_items)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership_list(request: "HttpRequest", group_id: int) -> "HttpResponse":
    logger.debug(
        f"group_membership_list called by user {request.user} "
        f"for group id {group_id}"
    )
    group = get_object_or_404(Group, id=group_id)
    try:

        # Check its a joinable group i.e. not corp or internal
        # And the user has permission to manage it
        if (not GroupManager.check_internal_group(group)
            or not GroupManager.can_manage_group(request.user, group)
        ):
            logger.warning(
                f"User {request.user} attempted to view the membership of group {group_id} "
                "but permission was denied"
            )
            raise PermissionDenied

    except ObjectDoesNotExist as e:
        raise Http404("Group does not exist") from e

    group_leaders = group.authgroup.group_leaders.all()
    members = []
    for member in \
        group.user_set\
            .all()\
            .select_related('profile', 'profile__main_character')\
            .order_by('profile__main_character__character_name'):

        members.append({
            'user': member,
            'main_char': member.profile.main_character,
            'is_leader': member in group_leaders
        })

    render_items = {'group': group, 'members': members}

    return render(
        request, 'groupmanagement/groupmembers.html',
        context=render_items
    )


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_membership_remove(request: "HttpRequest", group_id: int, user_id: int) -> "HttpResponse":
    logger.debug(f"group_membership_remove called by user {request.user} for group id {group_id} on user id {user_id}")
    group = get_object_or_404(Group, id=group_id)
    try:
        # Check its a joinable group i.e. not corp or internal
        # And the user has permission to manage it
        if not GroupManager.check_internal_group(group) or not GroupManager.can_manage_group(request.user, group):
            logger.warning(f"User {request.user} attempted to remove a user from group {group_id} but permission was denied")
            raise PermissionDenied

        try:
            user = group.user_set.get(pk=user_id)

            log = RequestLog(
                request_type=RequestLog.Type.REMOVE,
                requestor=user,
                group=group,
                action=RequestLog.Action.REMOVE,
                request_actor=request.user
            )
            log.save()

            # Remove group from user
            user.groups.remove(group)
            logger.info(f"User {request.user} removed user {user} from group {group}")
            messages.success(request, _("Removed user %(user)s from group %(group)s.") % {"user": user, "group": group})
        except ObjectDoesNotExist:
            messages.warning(request, _("User does not exist in that group"))

    except ObjectDoesNotExist:
        messages.warning(request, _("Group does not exist"))

    return redirect('groupmanagement:membership', group_id)


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_accept_request(request: "HttpRequest", group_request_id: int) -> "HttpResponse":
    logger.debug(f"group_accept_request called by user {request.user} for grouprequest id {group_request_id}")
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        group, created = Group.objects.get_or_create(name=group_request.group.name)

        if not GroupManager.joinable_group(group_request.group, group_request.user.profile.state) or \
                not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        group_request.user.groups.add(group)
        group_request.user.save()

        log = RequestLog(
            request_type=group_request.request_type(),
            requestor=group_request.user,
            group=group,
            action=RequestLog.Action.ACCEPT,
            request_actor=request.user
        )
        log.save()

        group_request.delete()
        logger.info(f"User {request.user} accepted group request from user {group_request.user} to group {group_request.group.name}")
        notify(group_request.user, "Group Application Accepted", level="success",
                message=f"Your application to {group_request.group} has been accepted.")
        messages.success(request,
                        _('Accepted application from %(mainchar)s to %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})

    except PermissionDenied as p:
        logger.warning(f"User {request.user} attempted to accept group join request {group_request_id} but permission was denied")
        raise p
    except Exception:
        messages.error(request, _('An unhandled error occurred while processing the application from %(mainchar)s to %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})
        logger.exception(f"Unhandled exception occurred while user {request.user} attempting to accept grouprequest id {group_request_id}.")
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_reject_request(request: "HttpRequest", group_request_id: int) -> "HttpResponse":
    logger.debug(f"group_reject_request called by user {request.user} for group request id {group_request_id}")
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        if group_request:
            logger.info(f"User {request.user} rejected group request from user {group_request.user} to group {group_request.group.name}")

            log = RequestLog(
                request_type=group_request.request_type(),
                requestor=group_request.user,
                group=group_request.group,
                action=RequestLog.Action.REJECT,
                request_actor=request.user
            )
            log.save()

            group_request.delete()
            notify(group_request.user, "Group Application Rejected", level="danger", message=f"Your application to {group_request.group} has been rejected.")
            messages.success(request,
                            _('Rejected application from %(mainchar)s to %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})

    except PermissionDenied as p:
        logger.warning(f"User {request.user} attempted to reject group join request {group_request_id} but permission was denied")
        raise p
    except Exception:
        messages.error(request, _('An unhandled error occurred while processing the application from %(mainchar)s to %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})
        logger.exception(f"Unhandled exception occurred while user {request.user} attempting to reject group request id {group_request_id}")
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_leave_accept_request(request: "HttpRequest", group_request_id: int) -> "HttpResponse":
    logger.debug(
        f"group_leave_accept_request called by user {request.user} for group request id {group_request_id}")
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        group, created = Group.objects.get_or_create(name=group_request.group.name)
        group_request.user.groups.remove(group)
        group_request.user.save()

        log = RequestLog(
            request_type=group_request.request_type(),
            requestor=group_request.user,
            group=group_request.group,
            action=RequestLog.Action.ACCEPT,
            request_actor=request.user
        )
        log.save()

        group_request.delete()
        logger.info(f"User {request.user} accepted group leave request from user {group_request.user} to group {group_request.group.name}")
        notify(group_request.user, "Group Leave Request Accepted", level="success",
                message=f"Your request to leave {group_request.group} has been accepted.")
        messages.success(request,
                        _('Accepted application from %(mainchar)s to leave %(group)s.') % {"mainchar": group_request.main_char, "group": group_request.group})
    except PermissionDenied as p:
        logger.warning(f"User {request.user} attempted to accept group leave request {group_request_id} but permission was denied")
        raise p
    except Exception:
        messages.error(request, _('An unhandled error occurred while processing the application from %(mainchar)s to leave %(group)s.') % {
            "mainchar": group_request.main_char, "group": group_request.group})
        logger.exception(f"Unhandled exception occurred while user {request.user} attempting to accept group leave request id {group_request_id}")
        pass

    return redirect("groupmanagement:management")


@login_required
@user_passes_test(GroupManager.can_manage_groups)
def group_leave_reject_request(request: "HttpRequest", group_request_id: int) -> "HttpResponse":
    logger.debug(
        f"group_leave_reject_request called by user {request.user} for group request id {group_request_id}")
    group_request = get_object_or_404(GroupRequest, id=group_request_id)
    try:
        if not GroupManager.can_manage_group(request.user, group_request.group):
            raise PermissionDenied

        if group_request:
            log = RequestLog(
                request_type=group_request.request_type(),
                requestor=group_request.user,
                group=group_request.group,
                action=RequestLog.Action.REJECT,
                request_actor=request.user
            )
            log.save()

            group_request.delete()
            logger.info(f"User {request.user} rejected group leave request from user {group_request.user} for group {group_request.group.name}")
            notify(group_request.user, "Group Leave Request Rejected", level="danger", message=f"Your request to leave {group_request.group} has been rejected.")
            messages.success(request, _('Rejected application from %(mainchar)s to leave %(group)s.') % {
                "mainchar": group_request.main_char, "group": group_request.group})
    except PermissionDenied as p:
        logger.warning(f"User {request.user} attempted to reject group leave request {group_request_id} but permission was denied")
        raise p
    except Exception:
        messages.error(request, _('An unhandled error occurred while processing the application from %(mainchar)s to leave %(group)s.') % {
            "mainchar": group_request.main_char, "group": group_request.group})
        logger.exception(f"Unhandled exception occurred while user {request.user} attempting to reject group leave request id {group_request_id}")
        pass

    return redirect("groupmanagement:management")


@login_required
def groups_view(request: "HttpRequest") -> "HttpResponse":
    logger.debug(f"groups_view called by user {request.user}")

    groups_qs = GroupManager.get_joinable_groups_for_user(
        request.user, include_hidden=False
    )
    groups_qs = groups_qs.order_by('name').select_related("authgroup").prefetch_related('authgroup__group_leaders', 'authgroup__group_leaders__profile__main_character', 'authgroup__group_leader_groups')
    groups = []

    ## TODO see about making this faster
    for group in groups_qs:
        group_request = GroupRequest.objects\
            .filter(user=request.user)\
            .filter(group=group)
        groups.append({
            'group': group,
            'request': group_request[0] if group_request else None
        })

    count = 0
    perms = GroupManager.can_manage_groups(request.user)
    if perms:
        count = GroupManager.pending_requests_count_for_user(request.user)

    user_groups_list = list(request.user.groups.all())
    context = {'groups': groups, "manager_perms": perms, "req_count":count, "user_groups": user_groups_list}

    return render(request, 'groupmanagement/groups.html', context=context)


@login_required
def group_request_add(request: "HttpRequest", group_id: int) -> "HttpResponse":
    logger.debug(f"group_request_add called by user {request.user} for group id {group_id}")
    group = Group.objects.get(id=group_id)
    state = request.user.profile.state
    if not GroupManager.joinable_group(group, state):
        logger.warning(f"User {request.user} attempted to join group id {group_id} but it is not a joinable group")
        messages.warning(request, _("You cannot join that group"))
        return redirect('groupmanagement:groups')
    if group in request.user.groups.all():
        # User is already a member of this group.
        logger.warning(f"User {request.user} attempted to join group id {group_id} but they are already a member.")
        messages.warning(request, _("You are already a member of that group."))
        return redirect('groupmanagement:groups')
    if not request.user.has_perm('groupmanagement.request_groups') and not group.authgroup.public:
        # Does not have the required permission, trying to join a non-public group
        logger.warning(f"User {request.user} attempted to join group id {group_id} but it is not a public group")
        messages.warning(request, _("You cannot join that group"))
        return redirect('groupmanagement:groups')
    if group.authgroup.open:
        logger.info(f"{request.user} joining {group} as is an open group")
        request.user.groups.add(group)

        log = RequestLog(
            request_type=RequestLog.Type.JOIN,
            requestor=request.user,
            group=group,
            action=RequestLog.Action.ACCEPT,
            request_actor=request.user
        )
        log.save()

        return redirect("groupmanagement:groups")
    req = GroupRequest.objects.filter(user=request.user, group=group)
    if len(req) > 0:
        logger.info(f"{request.user} attempted to join {group} but already has an open application")
        messages.warning(request, _("You already have a pending application for that group."))
        return redirect("groupmanagement:groups")
    grouprequest = GroupRequest()
    grouprequest.group = group
    grouprequest.user = request.user
    grouprequest.leave_request = False
    grouprequest.save()
    logger.info(f"Created group request for user {request.user} to group {Group.objects.get(id=group_id)}")
    grouprequest.notify_leaders()
    messages.success(request, _('Applied to group %(group)s.') % {"group": group})
    return redirect("groupmanagement:groups")


@login_required
def group_request_leave(request: "HttpRequest", group_id: int) -> "HttpResponse":
    logger.debug(f"group_request_leave called by user {request.user} for group id {group_id}")
    group = Group.objects.get(id=group_id)
    if not GroupManager.check_internal_group(group):
        logger.warning(f"User {request.user} attempted to leave group id {group_id} but it is not a joinable group")
        messages.warning(request, _("You cannot leave that group"))
        return redirect('groupmanagement:groups')
    if group not in request.user.groups.all():
        logger.debug(f"User {request.user} attempted to leave group id {group_id} but they are not a member")
        messages.warning(request, _("You are not a member of that group"))
        return redirect('groupmanagement:groups')
    if group.authgroup.open:
        logger.info(f"{request.user} leaving {group} as is an open group")
        request.user.groups.remove(group)

        log = RequestLog(
            request_type=RequestLog.Type.LEAVE,
            requestor=request.user,
            group=group,
            action=RequestLog.Action.ACCEPT,
            request_actor=request.user
        )
        log.save()

        return redirect("groupmanagement:groups")
    req = GroupRequest.objects.filter(user=request.user, group=group)
    if len(req) > 0:
        logger.info(f"{request.user} attempted to leave {group} but already has an pending leave request.")
        messages.warning(request, _("You already have a pending leave request for that group."))
        return redirect("groupmanagement:groups")
    if getattr(settings, 'GROUPMANAGEMENT_AUTO_LEAVE', False):
        logger.info(f"{request.user} leaving joinable group {group} due to auto_leave")
        request.user.groups.remove(group)

        log = RequestLog(
            request_type=RequestLog.Type.LEAVE,
            requestor=request.user,
            group=group,
            action=RequestLog.Action.ACCEPT,
            request_actor=request.user
        )
        log.save()

        return redirect('groupmanagement:groups')
    grouprequest = GroupRequest()
    grouprequest.group = group
    grouprequest.user = request.user
    grouprequest.leave_request = True
    grouprequest.save()
    logger.info(f"Created group leave request for user {request.user} to group {Group.objects.get(id=group_id)}")
    grouprequest.notify_leaders()
    messages.success(request, _('Applied to leave group %(group)s.') % {"group": group})
    return redirect("groupmanagement:groups")

@login_required
def group_request_retract(request: "HttpRequest", group_id: int) -> "HttpResponse":
    logger.debug(
        f"group_request_retract called by user {request.user} for group id {group_id}"
    )
    group = get_object_or_404(Group, id=group_id)

    if not GroupManager.check_internal_group(group):
        logger.warning(
            f"User {request.user} attempted to retract group request for "
            f"group id {group_id} but it is not a joinable group"
        )
        messages.warning(
            request,
            _("You cannot retract that request"),
        )
        return redirect('groupmanagement:groups')

    try:
        group_request = GroupRequest.objects.get(
            user=request.user, group=group, leave_request=False
        )
        group_request.delete()

        logger.info(f"Deleted group request for user {request.user} to group {group}")
        messages.success(
            request, _('Retracted application to group %(group)s.') % {"group": group}
        )
    except GroupRequest.DoesNotExist:
        logger.info(
            f"{request.user} attempted to retract group request for "
            f"group id {group_id} but has no open request"
        )
        messages.warning(
            request, _("You have no open request for that group.")
        )

    return redirect("groupmanagement:groups")

class AuditLogTableData(DataTablesView):
    """
    View to provide data for the audit log table in the group membership audit page.
    """

    model = RequestLog

    # Define the columns as a tuple.
    # String for field name for filtering and ordering
    # String for the render template
    # Templates can be a html file or template language directly in the list below
    columns = [
        # ("field_for_queries_or_sort", template: str)
        ("date", "{{ row.date }}"),
        ("requestor__username", "{{ row.requestor.username }}"),
        (
            "requestor__profile__main_character__character_name",
            "{{ row.requestor.profile.main_character.character_name }}"
        ),
        (
            "requestor__profile__main_character__corporation_name",
            "{{ row.requestor.profile.main_character.corporation_name }}"
        ),
        ("request_type", "{{ row.get_request_type_display }}"),
        ("action", "{{ row.get_action_display }}"),
        ("request_actor__username", "{{ row.request_actor.username }}"),
    ]

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """
        Override dispatch to check if the user has permission to view the audit log for any group.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        group_id = kwargs.get("group_id")
        group = get_object_or_404(Group, id=group_id)

        # Check its a joinable group i.e. not corp or internal
        # And the user has permission to manage it
        if not GroupManager.check_internal_group(group) or not GroupManager.can_manage_group(request.user, group):
            logger.warning(
                f"User {request.user} attempted to view the membership of group {group_id} but permission was denied")

            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_model_qs(self, request: HttpRequest, *args, **kwargs):
        group_id = kwargs.get("group_id")
        model_qs = self.model.objects.filter(group_id=group_id).select_related(
            "group", "requestor",
            "request_actor",
            "requestor__profile__main_character",
            "request_actor__profile__main_character",
        ).order_by("-date")

        # Custom filters
        post_params = request.POST.dict()

        filter_requestor = post_params.get("filter_requestor", None)
        filter_character = post_params.get("filter_character", None)
        filter_corporation = post_params.get("filter_corporation", None)
        filter_type = post_params.get("filter_type", None)
        filter_action = post_params.get("filter_action", None)
        filter_actor = post_params.get("filter_actor", None)

        if filter_requestor:
            model_qs = model_qs.filter(requestor__pk=filter_requestor)

        if filter_character:
            model_qs = model_qs.filter(requestor__profile__main_character__pk=filter_character)

        if filter_corporation:
            model_qs = model_qs.filter(
                requestor__profile__main_character__corporation_id=filter_corporation
            )

        if filter_type:
            model_qs = model_qs.filter(request_type=filter_type)

        if filter_action:
            model_qs = model_qs.filter(action=filter_action)

        if filter_actor:
            model_qs = model_qs.filter(request_actor__pk=filter_actor)

        return model_qs
