# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from typing import List

from darabonba.model import DaraModel

class ListCheckRuleRequest(DaraModel):
    def __init__(
        self,
        check_id: int = None,
        check_name: str = None,
        current_page: int = None,
        effect_status: str = None,
        lang: str = None,
        page_size: int = None,
        rule_type: str = None,
        scope_type: str = None,
        task_sources: List[str] = None,
    ):
        # The ID of the check item.
        # 
        # > You can call the [ListCheckResult](~~ListCheckResult~~) operation to obtain the check item ID.
        self.check_id = check_id
        # The name of the check item.
        self.check_name = check_name
        # The page number of the current page returned for a paging query.
        self.current_page = current_page
        # Filters check rules by the effective status of the whitelist rule. Valid values: PERMANENT (Permanent), NOT_STARTED (Not started), EFFECTIVE (Effective), and EXPIRED (Expired). If you do not specify this parameter, rules in all effective statuses are returned. The server determines the status based on the current time and includes it in the pagination count.
        self.effect_status = effect_status
        # The language of the request and response. Default value: **zh**. Valid values:
        # 
        # - zh: Chinese.
        # - en: English.
        self.lang = lang
        # The number of check items to return on each page in a paging query. Default value: **20**, which indicates that 20 check items are displayed on each page.
        self.page_size = page_size
        # The rule type. Default value: **WHITE**. Valid values:
        # - **WHITE**: Whitelist.
        self.rule_type = rule_type
        # The effective scope of the rule. Valid values:
        # - **INSTNACE**: Instance.
        # - **ITEM**: Check item.
        self.scope_type = scope_type
        # The list of task sources.
        self.task_sources = task_sources

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.check_id is not None:
            result['CheckId'] = self.check_id

        if self.check_name is not None:
            result['CheckName'] = self.check_name

        if self.current_page is not None:
            result['CurrentPage'] = self.current_page

        if self.effect_status is not None:
            result['EffectStatus'] = self.effect_status

        if self.lang is not None:
            result['Lang'] = self.lang

        if self.page_size is not None:
            result['PageSize'] = self.page_size

        if self.rule_type is not None:
            result['RuleType'] = self.rule_type

        if self.scope_type is not None:
            result['ScopeType'] = self.scope_type

        if self.task_sources is not None:
            result['TaskSources'] = self.task_sources

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CheckId') is not None:
            self.check_id = m.get('CheckId')

        if m.get('CheckName') is not None:
            self.check_name = m.get('CheckName')

        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')

        if m.get('EffectStatus') is not None:
            self.effect_status = m.get('EffectStatus')

        if m.get('Lang') is not None:
            self.lang = m.get('Lang')

        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')

        if m.get('RuleType') is not None:
            self.rule_type = m.get('RuleType')

        if m.get('ScopeType') is not None:
            self.scope_type = m.get('ScopeType')

        if m.get('TaskSources') is not None:
            self.task_sources = m.get('TaskSources')

        return self

