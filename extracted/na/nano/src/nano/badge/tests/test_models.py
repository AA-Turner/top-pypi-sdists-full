from django.test import TestCase
from django.contrib.auth import get_user_model

from nano.badge.models import Badge
from nano.badge import add_badge, batchbadge
from nano.badge.views import ListBadgeView


class BadgeTest(TestCase):

    def test_str(self):
        item = Badge(name='test', description='Test')
        self.assertEqual(str(item), item.name)


class BadgeManagerTest(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.badge = Badge.objects.create(name='test', description='Test')
        self.users = []
        for i in range(10):
            self.users.append(self.User.objects.create(username='user%i' % i))
        for user in self.users[:5]:
            self.badge.receivers.add(user)

    def test_get_all_recipients(self):
        result = list(Badge.objects.get_all_recipients())
        self.assertEqual(result, self.users[:5])

    def test_get_all_nonrecipients(self):
        result = list(Badge.objects.get_all_nonrecipients())
        self.assertEqual(result, self.users[5:])


class BadgeFunctionsTest(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.badge = Badge.objects.create(name='test', description='Test')
        self.users = []
        for i in range(10):
            self.users.append(self.User.objects.create(username='user%i' % i))
        for user in self.users[:2]:
            self.badge.receivers.add(user)

    def test_add_badge(self):
        add_badge(self.badge, self.users[2])
        self.assertEqual(list(self.users[2].badges.all()), [self.badge])
        add_badge(self.badge, self.users[0])
        self.assertEqual(list(self.users[0].badges.all()), [self.badge])

    def test_batchbadge(self):
        self.User = get_user_model()
        self.assertEqual(list(self.badge.receivers.all()), self.users[:2])
        batchbadge(self.badge, self.User.objects.all())
        self.assertEqual(list(self.badge.receivers.all()), self.users)


class BadgeMixinTest(TestCase):

    def test_get_context_data(self):
        bm = ListBadgeView()
        bm.object_list = None  # set during as_view in 1.6
        context = bm.get_context_data(object_list=None)  # argument in 1.5
        self.assertEqual(context['me'], 'badge')
