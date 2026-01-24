# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import OrderedDict
from collections.abc import Mapping

from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.bot_blocker_rule import BotBlocker
from contrast.agent.protect.rule.cmdi_rule import CmdInjection
from contrast.agent.protect.rule.deserialization_rule import Deserialization
from contrast.agent.protect.rule.http_method_tampering import MethodTampering
from contrast.agent.protect.rule.nosqli_rule import NoSqlInjection
from contrast.agent.protect.rule.path_traversal_rule import PathTraversal
from contrast.agent.protect.rule.sqli_rule import SqlInjection
from contrast.agent.protect.rule.unsafe_file_upload_rule import UnsafeFileUpload
from contrast.agent.protect.rule.xss_rule import Xss
from contrast.agent.protect.rule.xxe_rule import Xxe


def build_protect_rules() -> Mapping[str, BaseRule]:
    """
    Build a dict with rules with prefilter rules first.
    We want prefilter rules first so they get evaluated / trigger first.

    :return: an ordered dict of protect rules
    """
    rules = OrderedDict(
        {
            UnsafeFileUpload.RULE_NAME: UnsafeFileUpload(),
            BotBlocker.RULE_NAME: BotBlocker(),
            CmdInjection.RULE_NAME: CmdInjection(),
            Deserialization.RULE_NAME: Deserialization(),
            MethodTampering.RULE_NAME: MethodTampering(),
            NoSqlInjection.RULE_NAME: NoSqlInjection(),
            PathTraversal.RULE_NAME: PathTraversal(),
            SqlInjection.RULE_NAME: SqlInjection(),
            Xss.RULE_NAME: Xss(),
            Xxe.RULE_NAME: Xxe(),
        }
    )

    return rules
