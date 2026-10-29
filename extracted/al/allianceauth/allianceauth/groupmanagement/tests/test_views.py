from django.test import RequestFactory, TestCase, override_settings
import json
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from allianceauth.groupmanagement.models import Group, GroupRequest, AuthGroup, \
    RequestLog
from allianceauth.tests.auth_utils import AuthUtils

from .. import views


def response_content_to_str(response) -> str:
    return response.content.decode(response.charset)


class TestViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = AuthUtils.create_user('Peter Parker')
        self.user_with_manage_permission = AuthUtils.create_user('Bruce Wayne')
        self.group = Group.objects.create(name="Example group")

        # set permissions
        AuthUtils.add_permission_to_user_by_name(
            'auth.group_management', self.user_with_manage_permission
        )

    def test_groups_view_can_load(self):
        request = self.factory.get(reverse('groupmanagement:groups'))
        request.user = self.user
        response = views.groups_view(request)
        self.assertEqual(response.status_code, 200)

    def test_management_view_can_load_for_user_with_permissions(self):
        """
        Test if user with management permissions can access the management view
        :return:
        """

        request = self.factory.get(reverse('groupmanagement:management'))
        request.user = self.user_with_manage_permission
        response = views.group_management(request)
        self.assertEqual(response.status_code, 200)

    def test_management_view_doesnt_load_for_user_without_permissions(self):
        """
        Test if user without management permissions can't access the management view
        :return:
        """

        request = self.factory.get(reverse('groupmanagement:management'))
        request.user = self.user
        response = views.group_management(request)
        self.assertEqual(response.status_code, 302)

    @override_settings(GROUPMANAGEMENT_AUTO_LEAVE=False)
    def test_leave_requests_tab_visible(self):
        """
        Test if the leave requests tab is visible when GROUPMANAGEMENT_AUTO_LEAVE = False
        :return:
        """

        request = self.factory.get(reverse('groupmanagement:management'))
        request.user = self.user_with_manage_permission
        response = views.group_management(request)

        content = response_content_to_str(response)

        self.assertEqual(response.status_code, 200)
        self.assertIn('id="leave-tab" data-bs-toggle="tab" data-bs-target="#leave"', content)
        self.assertIn('<div id="leave" class="tab-pane">', content)

    @override_settings(GROUPMANAGEMENT_AUTO_LEAVE=True)
    def test_leave_requests_tab_hidden(self):
        """
        Test if the leave requests tab is hidden when GROUPMANAGEMENT_AUTO_LEAVE = True
        :return:
        """

        request = self.factory.get(reverse('groupmanagement:management'))
        request.user = self.user_with_manage_permission
        response = views.group_management(request)

        content = response_content_to_str(response)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('id="leave-tab" data-bs-toggle="tab" data-bs-target="#leave"', content)
        self.assertNotIn('<div id="leave" class="tab-pane">', content)

    @override_settings(GROUPMANAGEMENT_AUTO_LEAVE=True)
    def test_should_not_hide_leave_requests_tab_when_there_are_open_requests(self):
        # given
        request = self.factory.get(reverse('groupmanagement:management'))
        request.user = self.user_with_manage_permission
        GroupRequest.objects.create(user=self.user, group=self.group, leave_request=True)

        # when
        response = views.group_management(request)

        # then
        content = response_content_to_str(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<a class="nav-link" id="leave-tab" data-bs-toggle="tab" data-bs-target="#leave"', content)
        self.assertIn('<div id="leave" class="tab-pane">', content)

class TestGroupMembershipAuditView(TestCase):
    """
    Test the group membership audit view
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = AuthUtils.create_user('Peter Parker')
        self.user_with_manage_permission = AuthUtils.create_user('Bruce Wayne')
        self.group = Group.objects.create(name="Example group")

        # set permissions
        AuthUtils.add_permission_to_user_by_name(
            'auth.group_management', self.user_with_manage_permission
        )

        self.group = Group.objects.create(name="Audit Group")
        ag, _ = AuthGroup.objects.update_or_create(group=self.group, defaults={"internal": False})
        # make manager a group leader so GroupManager.can_manage_groups returns True
        ag.group_leaders.add(self.user_with_manage_permission)

    def test_manager_with_permission_sees_audit_page_and_filters(self):
        """
        Test that a user with group management permissions can access the audit log page and see the relevant filters.

        :return:
        """

        RequestLog.objects.create(
            group=self.group,
            request_type='join',
            action='accept',
            request_actor=self.user_with_manage_permission,
            requestor=self.user
        )

        request = self.factory.get(
            reverse('groupmanagement:audit_log', args=[self.group.id])
        )
        request.user = self.user_with_manage_permission
        response = views.group_membership_audit(request, group_id=self.group.id)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode(response.charset)
        # page should include the group name and audit-related terms
        self.assertIn(self.group.name, content)
        self.assertTrue(
            ('requestor' in content.lower()) or ('action' in content.lower()) or ('date' in content.lower())
        )

    def test_user_without_permission_is_denied(self):
        """
        Test that a user without group management permissions is denied access to the audit log page.

        :return:
        """

        request = self.factory.get(
            reverse('groupmanagement:audit_log', args=[self.group.id])
        )
        request.user = self.user
        response = views.group_membership_audit(request, group_id=self.group.id)

        # user_passes_test will redirect unauthorised users to login
        self.assertEqual(response.status_code, 302)

    def test_internal_group_denied_even_for_manager_raises_permission_denied(self):
        """
        Test that even a user with group management permissions is denied access to the audit log page for an internal group.

        :return:
        """

        ag = AuthGroup.objects.get(group=self.group)
        ag.internal = True
        ag.save()

        request = self.factory.get(
            reverse('groupmanagement:audit_log', args=[self.group.id])
        )
        request.user = self.user_with_manage_permission

        with self.assertRaises(PermissionDenied):
            response = views.group_membership_audit(request, group_id=self.group.id)

    def test_requestor_filter_excludes_null_and_includes_user(self):
        """
        Test that the requestor filter on the audit log page excludes null requestors and includes the user who made a request.

        :return:
        """

        RequestLog.objects.create(
            request_type=RequestLog.Type.JOIN,
            group=self.group,
            action=RequestLog.Action.ACCEPT,
            request_actor=self.user_with_manage_permission,
            requestor=self.user,
        )

        RequestLog.objects.create(
            request_type=RequestLog.Type.LEAVE,
            group=self.group,
            action=RequestLog.Action.REJECT,
            request_actor=self.user_with_manage_permission,
            requestor=None,
        )

        request = self.factory.get(
            reverse('groupmanagement:audit_log', args=[self.group.id])
        )
        request.user = self.user_with_manage_permission
        response = views.group_membership_audit(request, group_id=self.group.id)

        # Ensure the view rendered and the filter select contains the requestor
        self.assertEqual(response.status_code, 200)
        content = response.content.decode(response.charset)

        # The requestor should appear as an <option> with value equal to the PK
        self.assertIn(f'value="{self.user.pk}"', content)
        self.assertIn(f'>{self.user.username}<', content)

        # Ensure we did not accidentally render a 'None' username option
        self.assertNotIn('>None<', content)

    def test_character_filter_excludes_null_and_includes_character(self):
        """
        Test that the character filter on the audit log page excludes null characters and includes the character of a user who made a request.

        :return:
        """

        # Give self.user a main character
        char = AuthUtils.add_main_character_2(
            self.user,
            name='Hero',
            character_id=54321,
            corp_id=111,
            corp_name='Heroes Inc',
            disconnect_signals=False
        )

        # Create another user without a main character
        nochar = AuthUtils.create_user('NoChar')

        RequestLog.objects.create(
            request_type=RequestLog.Type.JOIN,
            group=self.group,
            action=RequestLog.Action.ACCEPT,
            request_actor=self.user_with_manage_permission,
            requestor=self.user,
        )

        RequestLog.objects.create(
            request_type=RequestLog.Type.LEAVE,
            group=self.group,
            action=RequestLog.Action.REJECT,
            request_actor=self.user_with_manage_permission,
            requestor=nochar,
        )

        request = self.factory.get(
            reverse('groupmanagement:audit_log', args=[self.group.id])
        )
        request.user = self.user_with_manage_permission
        response = views.group_membership_audit(request, group_id=self.group.id)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode(response.charset)

        # Character option should include the character PK and name
        self.assertIn(f'value="{char.pk}"', content)
        self.assertIn(f'>{char.character_name}<', content)

        # Ensure we did not render a 'None' character option
        self.assertNotIn('>None<', content)


class TestAuditLogTableDataView(TestCase):
    """
    Test the AuditLogTableData view
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AuthUtils.create_user('Peter Parker')
        self.user_with_manage_permission = AuthUtils.create_user('Bruce Wayne')
        # set permissions
        AuthUtils.add_permission_to_user_by_name(
            'auth.group_management', self.user_with_manage_permission
        )
        self.group = Group.objects.create(name="Audit Table Group")
        ag, _ = AuthGroup.objects.update_or_create(group=self.group, defaults={"internal": False})
        ag.group_leaders.add(self.user_with_manage_permission)

    def test_manager_retrieves_audit_table_data_returns_expected_json(self):
        # create two audit logs
        RequestLog.objects.create(
            group=self.group,
            request_type='join',
            action='accept',
            request_actor=self.user_with_manage_permission,
            requestor=self.user
        )
        RequestLog.objects.create(
            group=self.group,
            request_type='leave',
            action='accept',
            request_actor=self.user_with_manage_permission,
            requestor=self.user
        )

        url = reverse('groupmanagement:audit_log_table_data', args=[self.group.id])

        # build basic datatables parameters for all columns defined in the view
        params = {
            'draw': '1',
            'start': '0',
            'length': '10',
        }
        params['search[value]'] = ''
        params['search[regex]'] = 'false'
        # provide minimal column config for indices 0..6
        for i in range(7):
            params[f'columns[{i}][search][value]'] = ''
            params[f'columns[{i}][search][regex]'] = 'false'
            params[f'columns[{i}][searchable]'] = 'true'
            params[f'columns[{i}][orderable]'] = 'true'

        request = self.factory.get(url, data=params)
        request.user = self.user_with_manage_permission

        response = views.AuditLogTableData.as_view()(request, group_id=self.group.id)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode(response.charset))
        self.assertEqual(data['draw'], 1)
        self.assertEqual(data['recordsTotal'], 2)
        self.assertEqual(data['recordsFiltered'], 2)
        self.assertEqual(len(data['data']), 2)

    def test_manager_filters_by_requestor_returns_only_matching_entries(self):
        # create two different users as requestors
        user_a = AuthUtils.create_user('Alice')
        user_b = AuthUtils.create_user('Bob')

        RequestLog.objects.create(
            group=self.group,
            request_type='join',
            action='accept',
            request_actor=self.user_with_manage_permission,
            requestor=user_a
        )
        RequestLog.objects.create(
            group=self.group,
            request_type='join',
            action='accept',
            request_actor=self.user_with_manage_permission,
            requestor=user_b
        )

        url = reverse('groupmanagement:audit_log_table_data', args=[self.group.id])

        post_data = {
            'draw': '1',
            'start': '0',
            'length': '10',
            'filter_requestor': str(user_a.pk),
        }
        post_data['search[value]'] = ''
        post_data['search[regex]'] = 'false'
        for i in range(7):
            post_data[f'columns[{i}][search][value]'] = ''
            post_data[f'columns[{i}][search][regex]'] = 'false'
            post_data[f'columns[{i}][searchable]'] = 'true'
            post_data[f'columns[{i}][orderable]'] = 'true'

        request = self.factory.post(url, data=post_data)
        request.user = self.user_with_manage_permission

        response = views.AuditLogTableData.as_view()(request, group_id=self.group.id)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode(response.charset))
        self.assertEqual(data['recordsFiltered'], 1)
        # second column in the columns definition renders the requestor
        self.assertIn(user_a.username, data['data'][0][1])

    def test_user_without_permissions_is_denied_access(self):
        url = reverse('groupmanagement:audit_log_table_data', args=[self.group.id])
        params = {'draw': '1', 'start': '0', 'length': '10'}
        params['search[value]'] = ''
        params['search[regex]'] = 'false'
        for i in range(7):
            params[f'columns[{i}][search][value]'] = ''
            params[f'columns[{i}][search][regex]'] = 'false'
            params[f'columns[{i}][searchable]'] = 'true'
            params[f'columns[{i}][orderable]'] = 'true'

        request = self.factory.get(url, data=params)
        request.user = self.user

        with self.assertRaises(PermissionDenied):
            views.AuditLogTableData.as_view()(request, group_id=self.group.id)
