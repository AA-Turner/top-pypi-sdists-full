# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class OperateCommonOverallConfigRequest(DaraModel):
    def __init__(
        self,
        client_token: str = None,
        config: str = None,
        dry_run: bool = None,
        no_target_as_on: bool = None,
        resource_directory_account_id: int = None,
        source_ip: str = None,
        type: str = None,
    ):
        # The client token that is used to ensure the idempotence of the request. Different requests must use different tokens. The token can contain only ASCII characters and cannot exceed 64 characters in length.
        self.client_token = client_token
        # The switch status. Valid values:
        # 
        # - **on**: enabled
        # - **off**: disabled
        # 
        # This parameter is required.
        self.config = config
        # Specifies whether to only precheck the request. Valid values: true: Prechecks the request without performing the actual operation. false: Performs the actual operation.
        self.dry_run = dry_run
        # Specifies whether assets need to be configured. Default value: **false**. Valid values:
        # - **true**: required
        # - **false**: not required
        # > This value is valid only when **Config** is set to **on**.
        self.no_target_as_on = no_target_as_on
        self.resource_directory_account_id = resource_directory_account_id
        # The IP address of the access source.
        self.source_ip = source_ip
        # The configuration type. Valid values:
        # 
        # - **kdump_switch**: proactive defense optimization experience
        # - **threat_detect**: adaptive threat detection capability
        # - **suspicious_aggregation**: alerting associate
        # - **alidetect**: file detection
        # - **USER-ENABLE-SWITCH-TYPE_38857**: high-risk operations executed by Linux entry services
        # - **USER-ENABLE-SWITCH-TYPE_50858**: high-risk operations executed by Linux web services
        # - **USER-ENABLE-SWITCH-TYPE_50859**: suspicious operations executed by Linux entry services
        # - **USER-ENABLE-SWITCH-TYPE_50862**: advanced protection for Linux Cloud Assistant
        # - **USER-ENABLE-SWITCH-TYPE_50867**: malicious file implantation in Linux
        # - **USER-ENABLE-SWITCH-TYPE_50868**: suspicious file implantation in Linux
        # - **USER-ENABLE-SWITCH-TYPE_64025**: command execution by Linux entry services [enhanced pattern]
        # - **USER-ENABLE-SWITCH-TYPE_51229**: high-risk operations executed by Windows browser services
        # - **USER-ENABLE-SWITCH-TYPE_51230**: suspicious operations executed by Windows entry services
        # - **USER-ENABLE-SWITCH-TYPE_51232**: high-risk operations executed by Windows system processes
        # - **USER-ENABLE-SWITCH-TYPE_51233**: high-risk operations executed by Windows Java services
        # - **USER-ENABLE-SWITCH-TYPE_51234**: high-risk operations executed by Windows Office components
        # - **USER-ENABLE-SWITCH-TYPE_51235**: high-risk operations executed by Windows web services
        # - **USER-ENABLE-SWITCH-TYPE_52820**: malicious file implantation in Windows
        # - **USER-ENABLE-SWITCH-TYPE_52826**: high-risk operations executed by Windows entry services
        # - **USER-ENABLE-SWITCH-TYPE_55251**: high-risk operations executed by Windows database services
        # - **USER-ENABLE-SWITCH-TYPE_63725**: suspicious script or binary file implantation by Windows entry services
        # - **USER-ENABLE-SWITCH-TYPE_3277**: suspicious process startup in Linux
        # - **USER-ENABLE-SWITCH-TYPE_50983**: command obfuscation in Linux
        # - **USER-ENABLE-SWITCH-TYPE_51200**: downloading and running malicious files via Linux command line
        # - **USER-ENABLE-SWITCH-TYPE_71131**: suspicious behavior sequences executed by Linux entry services
        # - **USER-ENABLE-SWITCH-TYPE_51225**: high-risk commands executed by Windows PowerShell
        # - **USER-ENABLE-SWITCH-TYPE_51226**: suspicious commands executed by Windows PowerShell
        # - **USER-ENABLE-SWITCH-TYPE_52821**: suspicious process startup in Windows
        # - **USER-ENABLE-SWITCH-TYPE_57242**: malicious command execution in Windows
        # - **USER-ENABLE-SWITCH-TYPE_57340**: downloading and running malicious files via Windows command line
        # - **USER-ENABLE-SWITCH-TYPE_39659**: sensitive registry key protection in Windows
        # - **USER-ENABLE-SWITCH-TYPE_52816**: high-risk account manipulation in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54365**: creation of service auto-start items in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54366**: creation of high-risk auto-start items in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54367**: creation of scheduled node auto-start items in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54368**: creation of registry auto-start items in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54369**: creation of WMI auto-start items in Windows
        # - **USER-ENABLE-SWITCH-TYPE_50869**: unauthorized execution of high-risk commands in Linux
        # - **USER-ENABLE-SWITCH-TYPE_53272**: privilege escalation by exploiting kernel vulnerabilities in Linux
        # - **USER-ENABLE-SWITCH-TYPE_54395**: unauthorized reading and writing of sensitive files in Linux
        # - **USER-ENABLE-SWITCH-TYPE_57897**: suspected privilege escalation in Linux
        # - **USER-ENABLE-SWITCH-TYPE_52825**: unauthorized execution of high-risk commands in Windows
        # - **USER-ENABLE-SWITCH-TYPE_5507**: malicious drivers in Linux
        # - **USER-ENABLE-SWITCH-TYPE_50876**: evasion of security software in Linux
        # - **USER-ENABLE-SWITCH-TYPE_53168**: process debugging in Linux
        # - **USER-ENABLE-SWITCH-TYPE_54699**: dynamic-link library hijacking in Linux
        # - **USER-ENABLE-SWITCH-TYPE_62981**: bypassing security monitoring in Linux
        # - **USER-ENABLE-SWITCH-TYPE_52815**: loading of high-risk drivers in Windows
        # - **USER-ENABLE-SWITCH-TYPE_52823**: running high-risk ARK tools in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54373**: evasion of security software in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54374**: clearing intrusion traces in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54265**: PAM module hijacking in Linux
        # - **USER-ENABLE-SWITCH-TYPE_54953**: HashDump attacks in Linux
        # - **USER-ENABLE-SWITCH-TYPE_54383**: credential theft by Mimikatz in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54384**: HashDump attacks in Windows
        # - **USER-ENABLE-SWITCH-TYPE_50861**: information probing in Linux
        # - **USER-ENABLE-SWITCH-TYPE_52818**: information probing in Windows
        # - **USER-ENABLE-SWITCH-TYPE_54034**: internal network scanning in Linux
        # - **USER-ENABLE-SWITCH-TYPE_51228**: high-risk lateral movement tools in Windows
        # - **USER-ENABLE-SWITCH-TYPE_50870**: reverse shells in Linux
        # - **USER-ENABLE-SWITCH-TYPE_50873**: command execution by web shells
        # - **USER-ENABLE-SWITCH-TYPE_51236**: reverse shells in Windows
        # - **USER-ENABLE-SWITCH-TYPE_50877**: malicious program communication in Linux
        # - **USER-ENABLE-SWITCH-TYPE_50884**: suspicious worm script behavior in Linux
        # - **USER-ENABLE-SWITCH-TYPE_50885**: malicious script behavior in Linux
        # - **USER-ENABLE-SWITCH-TYPE_51201**: ransomware virus in Linux
        # - **USER-ENABLE-SWITCH-TYPE_51202**: suspicious ransomware behavior in Linux
        # - **USER-ENABLE-SWITCH-TYPE_52827**: ransomware virus in Windows
        # - **USER-ENABLE-SWITCH-TYPE_52828**: suspicious ransomware behavior in Windows
        # - **USER-ENABLE-SWITCH-TYPE_52829**: delete system backups behavior in Windows
        # 
        # This parameter is required.
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.client_token is not None:
            result['ClientToken'] = self.client_token

        if self.config is not None:
            result['Config'] = self.config

        if self.dry_run is not None:
            result['DryRun'] = self.dry_run

        if self.no_target_as_on is not None:
            result['NoTargetAsOn'] = self.no_target_as_on

        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')

        if m.get('Config') is not None:
            self.config = m.get('Config')

        if m.get('DryRun') is not None:
            self.dry_run = m.get('DryRun')

        if m.get('NoTargetAsOn') is not None:
            self.no_target_as_on = m.get('NoTargetAsOn')

        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

