# -*- coding: utf-8 -*-
import unittest

import tos
from tests.common import TosTestBase, random_string
from tos.enum import StatusType, StorageClassType
from tos.exceptions import TosServerError
from tos.models2 import (Tag, QosConfig, ObjectSetQuotaRule, ObjectSetTagLifecycleRule,
                         BucketLifeCycleRule, BucketLifeCycleExpiration,
                         BucketLifeCycleTransition)

tos.set_logger()


class TestObjectSet(TosTestBase):
    """ObjectSet 全量接口的真实场景测试。

    需要本地环境变量配置 AK/SK/Endpoint/Region 才能运行。
    """

    def setUp(self):
        super(TestObjectSet, self).setUp()
        # 创建专用桶
        self.os_bucket = self.bucket_name + '-os'
        self.client.create_bucket(self.os_bucket)
        self.bucket_delete.append(self.os_bucket)

    def _ensure_configuration(self):
        """启用 ObjectSet 配置，是所有后续接口的前提"""
        qos = QosConfig(reads_qps=1000, writes_qps=500, list_qps=200,
                        reads_rate=1024 * 1024, writes_rate=1024 * 1024)
        out = self.client.put_bucket_object_set_configuration(
            bucket=self.os_bucket,
            path_level=1,
            enable_default_object_set=True,
            custom_delimiter='/',
            storage_quota='1073741824',
            qos=qos,
        )
        self.assertIsNotNone(out.request_id)

    def test_bucket_object_set_configuration(self):
        """测试桶级 ObjectSet 配置的写入和读取，包含 QoS Rate 字段回读校验"""
        self._ensure_configuration()
        out = self.client.get_bucket_object_set_configuration(self.os_bucket)
        self.assertEqual(out.path_level, 1)
        self.assertEqual(out.custom_delimiter, '/')
        self.assertTrue(out.enable_default_object_set)
        self.assertIsNotNone(out.qos)
        self.assertEqual(out.qos.reads_qps, 1000)
        self.assertEqual(out.qos.writes_qps, 500)
        self.assertEqual(out.qos.list_qps, 200)
        # QoS Rate 字段回读校验
        self.assertEqual(out.qos.reads_rate, 1024 * 1024)
        self.assertEqual(out.qos.writes_rate, 1024 * 1024)

    def test_bucket_object_set_configuration_minimal(self):
        """仅传必要字段（path_level + enable_default_object_set），验证默认值行为"""
        out = self.client.put_bucket_object_set_configuration(
            bucket=self.os_bucket,
            path_level=2,
            enable_default_object_set=False,
        )
        self.assertIsNotNone(out.request_id)

        get_out = self.client.get_bucket_object_set_configuration(self.os_bucket)
        self.assertEqual(get_out.path_level, 2)
        self.assertFalse(get_out.enable_default_object_set)
        # qos 未传时应为 None 或空配置
        if get_out.qos:
            self.assertIsNone(get_out.qos.reads_qps)

    def test_object_set_crud(self):
        """ObjectSet 的创建、获取、列举、删除，删除后 get 验证 404"""
        self._ensure_configuration()
        name = 'oset-crud-' + random_string(6)
        tag_set = [Tag('env', 'test'), Tag('team', 'sdk')]

        # 创建（带 tag）
        put_out = self.client.put_object_set(self.os_bucket, name, tag_set=tag_set)
        self.assertIsNotNone(put_out.request_id)

        # 创建不带 tag 的 ObjectSet
        no_tags_name = 'oset-notags-' + random_string(6)
        self.client.put_object_set(self.os_bucket, no_tags_name, tag_set=None)
        get_no_tags = self.client.get_object_set(self.os_bucket, no_tags_name)
        self.assertEqual(get_no_tags.object_set_name, no_tags_name + '/')
        self.assertEqual(get_no_tags.tag_set, [])

        # 创建单级目录路径（匹配 path_level=1 配置）
        single_name = 'single-level'
        self.client.put_object_set(self.os_bucket, single_name, tag_set=[Tag('level', '1')])
        get_single = self.client.get_object_set(self.os_bucket, single_name)
        self.assertEqual(get_single.object_set_name, single_name + '/')
        self.assertEqual({t.key: t.value for t in get_single.tag_set}, {'level': '1'})

        # 获取（BOE 环境 ObjectSetName 末尾自动追加 delimiter）
        get_out = self.client.get_object_set(self.os_bucket, name)
        self.assertEqual(get_out.object_set_name, name + '/')
        self.assertEqual({t.key: t.value for t in get_out.tag_set},
                         {'env': 'test', 'team': 'sdk'})

        # 列举（prefix 过滤）
        list_out = self.client.list_object_set(self.os_bucket, prefix='oset-crud-', max_keys=100)
        self.assertTrue(any(item.object_set_name == name + '/' for item in list_out.object_sets))

        # 列举（tags 过滤）
        list_out2 = self.client.list_object_set(self.os_bucket, tags='env=test', max_keys=100)
        self.assertTrue(any(item.object_set_name == name + '/' for item in list_out2.object_sets))

        # 清理不带 tag 的
        self.client.delete_object_set(self.os_bucket, no_tags_name)
        # 清理单级目录
        self.client.delete_object_set(self.os_bucket, single_name)

        # 删除
        del_out = self.client.delete_object_set(self.os_bucket, name)
        self.assertIsNotNone(del_out.request_id)

        # 删除后再 get 应返回 404
        with self.assertRaises(TosServerError) as ctx:
            self.client.get_object_set(self.os_bucket, name)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_object_set_tagging(self):
        """ObjectSet 标签的更新和获取"""
        self._ensure_configuration()
        name = 'oset-tag-' + random_string(6)
        self.client.put_object_set(self.os_bucket, name, tag_set=[Tag('k', 'v')])
        try:
            # 更新标签
            new_tags = [Tag('env', 'prod'), Tag('version', '2')]
            self.client.put_object_set_tagging(self.os_bucket, name, tag_set=new_tags)

            # 获取标签
            tag_out = self.client.get_object_set_tagging(self.os_bucket, name)
            self.assertEqual(tag_out.object_set_name, name + '/')
            tags_dict = {t.key: t.value for t in tag_out.tag_set}
            self.assertEqual(tags_dict, {'env': 'prod', 'version': '2'})
        finally:
            self.client.delete_object_set(self.os_bucket, name)

    def test_object_set_endpoint(self):
        """获取 ObjectSet 的 endpoint 信息"""
        self._ensure_configuration()
        name = 'oset-ep-' + random_string(6)
        self.client.put_object_set(self.os_bucket, name, tag_set=[Tag('k', 'v')])
        try:
            out = self.client.get_object_set_endpoint(self.os_bucket, name)
            self.assertIsNotNone(out.request_id)
            self.assertIsInstance(out.endpoints, list)
            # endpoint 对象应包含结构化字段
            if out.endpoints:
                ep = out.endpoints[0]
                self.assertTrue(hasattr(ep, 'cap_name'))
                self.assertTrue(hasattr(ep, 'endpoint'))
                self.assertTrue(hasattr(ep, 's3_endpoint'))
        finally:
            self.client.delete_object_set(self.os_bucket, name)

    def test_object_set_quota(self):
        """ObjectSet 存储配额设置与获取"""
        self._ensure_configuration()
        name = 'oset-quota-' + random_string(6)
        self.client.put_object_set(self.os_bucket, name, tag_set=[Tag('k', 'v')])
        try:
            self.client.put_object_set_quota(self.os_bucket, name, storage_quota='536870912')
            quota_out = self.client.get_object_set_quota(self.os_bucket, name)
            self.assertEqual(quota_out.storage_quota, '536870912')
        finally:
            self.client.delete_object_set(self.os_bucket, name)

    def test_object_set_quota_not_set(self):
        """未设置配额的 ObjectSet，get_quota 应返回空或默认值"""
        self._ensure_configuration()
        name = 'oset-noquota-' + random_string(6)
        self.client.put_object_set(self.os_bucket, name, tag_set=[Tag('k', 'v')])
        try:
            quota_out = self.client.get_object_set_quota(self.os_bucket, name)
            # 未设置时 StorageQuota 应为空字符串或 None
            self.assertIn(quota_out.storage_quota, (None, '', '0'))
        finally:
            self.client.delete_object_set(self.os_bucket, name)

    def test_object_set_quota_update(self):
        """Quota 更新：设置 → 改为 0 → 重新获取"""
        self._ensure_configuration()
        name = 'oset-qupdate-' + random_string(6)
        self.client.put_object_set(self.os_bucket, name, tag_set=[Tag('k', 'v')])
        try:
            # 先设为 512MB
            self.client.put_object_set_quota(self.os_bucket, name, storage_quota='536870912')
            out1 = self.client.get_object_set_quota(self.os_bucket, name)
            self.assertEqual(out1.storage_quota, '536870912')

            # 改为 0（无限制）
            self.client.put_object_set_quota(self.os_bucket, name, storage_quota='0')
            out2 = self.client.get_object_set_quota(self.os_bucket, name)
            self.assertEqual(out2.storage_quota, '0')
        finally:
            self.client.delete_object_set(self.os_bucket, name)

    def test_object_set_storage(self):
        """获取 ObjectSet 存储用量统计，校验 int 字段精确值"""
        self._ensure_configuration()
        name = 'oset-storage-' + random_string(6)
        self.client.put_object_set(self.os_bucket, name, tag_set=[Tag('k', 'v')])
        try:
            stat_out = self.client.get_object_set_storage(self.os_bucket, name)
            self.assertIsNotNone(stat_out.request_id)
            self.assertIsNotNone(stat_out.total_storage_stat)
            # 新建 ObjectSet 无数据，object_count 应为 0
            self.assertEqual(stat_out.total_storage_stat.object_count, 0)
            # storage_size 也应为 '0' 或 0
            self.assertIn(stat_out.total_storage_stat.storage_size, ('0', 0, None))
            # 各存储类型 stat 应存在
            self.assertIsNotNone(stat_out.standard_storage_stat)
            self.assertIsNotNone(stat_out.ia_storage_stat)
        finally:
            self.client.delete_object_set(self.os_bucket, name)

    def test_object_set_quota_by_tag(self):
        """按标签设置/获取/删除 ObjectSet 配额规则"""
        self._ensure_configuration()
        rule = ObjectSetQuotaRule(
            tag=Tag('team', 'sdk'),
            qos=QosConfig(reads_qps=10, writes_qps=5),
            storage_quota='1073741824',
        )
        self.client.put_object_set_quota_by_tag(self.os_bucket, rules=[rule])
        try:
            get_out = self.client.get_object_set_quota_by_tag(self.os_bucket)
            self.assertTrue(any(
                r.tag.key == 'team' and r.tag.value == 'sdk'
                for r in get_out.rules
            ))
        finally:
            del_out = self.client.delete_object_set_quota_by_tag(self.os_bucket)
            self.assertIsNotNone(del_out.request_id)

    def test_object_set_lifecycle(self):
        """ObjectSet 生命周期规则的设置/获取/删除，删除后 404 校验，含多规则和 transition"""
        self._ensure_configuration()
        name = 'oset-lc-' + random_string(6)
        self.client.put_object_set(self.os_bucket, name, tag_set=[Tag('k', 'v')])
        rules = [
            BucketLifeCycleRule(
                id='rule-1', prefix='log/', status=StatusType.Status_Enable,
                expiration=BucketLifeCycleExpiration(days=30),
            ),
            BucketLifeCycleRule(
                id='rule-2', prefix='data/', status=StatusType.Status_Enable,
                transitions=[BucketLifeCycleTransition(
                    storage_class=StorageClassType.Storage_Class_Ia, days=90,
                )],
                tags=[Tag('type', 'archive')],
            ),
        ]
        try:
            self.client.put_object_set_lifecycle(self.os_bucket, name, rules=rules)
            get_out = self.client.get_object_set_lifecycle(self.os_bucket, name)
            self.assertEqual(len(get_out.rules), 2)
            ids = {r.id for r in get_out.rules}
            self.assertEqual(ids, {'rule-1', 'rule-2'})

            # 校验 transition 规则
            rule2 = next(r for r in get_out.rules if r.id == 'rule-2')
            self.assertEqual(len(rule2.transitions), 1)
            self.assertEqual(rule2.transitions[0].days, 90)

            # 删除后再 get 应返回 404
            self.client.delete_object_set_lifecycle(self.os_bucket, name)
            with self.assertRaises(TosServerError) as ctx:
                self.client.get_object_set_lifecycle(self.os_bucket, name)
            self.assertEqual(ctx.exception.status_code, 404)
        finally:
            self.client.delete_object_set(self.os_bucket, name)

    def test_object_set_lifecycle_by_tag(self):
        """按标签设置/获取/删除 ObjectSet 生命周期规则"""
        self._ensure_configuration()
        tag_rule = ObjectSetTagLifecycleRule(
            tag=Tag('lc', 'auto'),
            rules=[BucketLifeCycleRule(
                id='r-bytag', prefix='', status=StatusType.Status_Enable,
                expiration=BucketLifeCycleExpiration(days=7),
            )],
        )
        self.client.put_object_set_lifecycle_by_tag(self.os_bucket, object_set_tag_rules=[tag_rule])
        try:
            get_out = self.client.get_object_set_lifecycle_by_tag(self.os_bucket)
            self.assertTrue(any(
                r.tag.key == 'lc' and r.tag.value == 'auto'
                for r in get_out.object_set_tag_rules
            ))
        finally:
            self.client.delete_object_set_lifecycle_by_tag(self.os_bucket)

    def test_list_object_set_pagination(self):
        """测试列举 ObjectSet 的分页机制"""
        self._ensure_configuration()
        names = []
        for i in range(3):
            name = 'oset-page-' + random_string(6)
            self.client.put_object_set(self.os_bucket, name, tag_set=[Tag('idx', str(i))])
            names.append(name)
        try:
            # 逐个翻页
            all_sets = []
            marker = None
            while True:
                out = self.client.list_object_set(self.os_bucket, prefix='oset-page-',
                                                  max_keys=1, marker=marker)
                all_sets.extend(out.object_sets)
                if not out.is_truncated:
                    break
                marker = out.next_marker
            listed_names = {s.object_set_name for s in all_sets}
            for n in names:
                self.assertIn(n + '/', listed_names)
        finally:
            for n in names:
                self.client.delete_object_set(self.os_bucket, n)


if __name__ == '__main__':
    unittest.main()
