# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth import get_user_model

from nano.badge.models import Badge
from nano.badge import add_badge, batchbadge
from nano.badge.views import ListBadgeView
from nano.badge.templatetags.badge_tags import sum_badges
from nano.badge.templatetags.badge_tags import get_badges_for_user
from nano.badge.templatetags.badge_tags import show_badges
from nano.badge.templatetags.badge_tags import show_badge


class BadgeTagsSmallfuncsTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.badgeless_user = User.objects.create(username='badgeless')
        self.badge = Badge.objects.create(name='test', description='Test')
        self.users = []
        for i in range(10):
            self.users.append(User.objects.create(username='user%i' % i))
        for user in self.users[:5]:
            self.badge.receivers.add(user)

    def test_sum_badges_no_badges(self):
        result = sum_badges(self.badgeless_user)
        self.assertEqual(result, {})

    def test_sum_badges(self):
        for user in self.users[:5]:
            self.assertEqual(sum_badges(user), {100: 1})

    def test_get_badges_for_user_no_badges(self):
        result = get_badges_for_user(self.badgeless_user)
        self.assertEqual(result, [])

    def test_get_badges_for_user_no_badges(self):
        expected = ['<span class="b100" title="1 bronze badge">●</span>1']
        result = get_badges_for_user(self.users[0])
        self.assertEqual(result, expected)


class BadgeTagsShowBadges(TestCase):

    def setUp(self):
        User = get_user_model()
        self.badgeless_user = User.objects.create(username='badgeless')
        self.badge = Badge.objects.create(name='test', description='Test')
        self.users = []
        for i in range(10):
            self.users.append(User.objects.create(username='user%i' % i))
        for user in self.users[:5]:
            self.badge.receivers.add(user)

    def test_show_badges_no_badges(self):
        result = show_badges(self.badgeless_user)
        self.assertEqual(result, '')

    def test_show_badges(self):
        expected = '<span><span class="b100" title="1 bronze badge">●</span>1</span>'
        result = show_badges(self.users[0])
        self.assertEqual(result, expected)


class BadgeTagsShowBadge(TestCase):

    def setUp(self):
        User = get_user_model()
        self.badgeless_user = User.objects.create(username='badgeless')
        self.badge = Badge.objects.create(name='test', description='Test')
        self.users = []
        for i in range(10):
            self.users.append(User.objects.create(username='user%i' % i))
        for user in self.users[:5]:
            self.badge.receivers.add(user)

    def test_show_badges(self):
        expected = '<span class="badge"><a href="/badge/1/"><span class="b100" >●</span> test</a></span>'
        result = show_badge(self.badge)
        self.assertEqual(result, expected)
