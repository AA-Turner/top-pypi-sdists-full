from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from nano.comments.models import Comment
from nano.comments.tests.models import Item


class CommentTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='user')
        self.item = Item.objects.create(slug='Commented item')
        item_dict = {
            'object_pk': self.item.pk,
            'content_type': ContentType.objects.get_for_model(Item),
        }
        self.root1 = Comment(user=self.user, comment='Root 1', **item_dict).save()
        self.child1 = Comment(user=self.user, comment='Child 1', part_of=self.root1, **item_dict).save()
        self.grandchild1 = Comment(user=self.user, comment='Grandchild 1', part_of=self.child1, **item_dict).save()
        self.child2 = Comment(user=self.user, comment='Child 2', part_of=self.root1, **item_dict).save()
        self.root2 = Comment(user=self.user, comment='Root 2', **item_dict).save()

    def test_str(self):
        item = Comment(user=self.user, comment='Test')
        self.assertEqual(str(item), '%s: Test...' % str(self.user))

