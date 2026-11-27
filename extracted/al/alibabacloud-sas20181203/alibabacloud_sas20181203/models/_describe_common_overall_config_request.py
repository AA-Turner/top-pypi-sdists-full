# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeCommonOverallConfigRequest(DaraModel):
    def __init__(
        self,
        resource_directory_account_id: int = None,
        source_ip: str = None,
        type: str = None,
    ):
        # The ID of the member accounts in the resource folder, which is an Alibaba Cloud account. You can invoke the [DescribeMonitorAccounts](~~DescribeMonitorAccounts~~) operation to obtain this parameter.
        self.resource_directory_account_id = resource_directory_account_id
        # The IP address of the access source.
        self.source_ip = source_ip
        # The configuration type. Valid values:
        # 
        # - **kdump_switch**: Proactive defense experience optimization
        # - **threat_detect**: Adaptive threat detection
        # - **suspicious_aggregation**: Alerting associate
        # - **alidetect**: File detection
        # - **USER-ENABLE-SWITCH-TYPE_3277**: Suspicious process startup
        # - **USER-ENABLE-SWITCH-TYPE_5507**: Malicious driver
        # - **USER-ENABLE-SWITCH-TYPE_38857**: High-risk operations executed by entry services
        # - **USER-ENABLE-SWITCH-TYPE_50858**: High-risk operations executed by web services
        # - **USER-ENABLE-SWITCH-TYPE_50859**: Suspicious operations executed by entry services
        # - **USER-ENABLE-SWITCH-TYPE_50861**: Information probing
        # - **USER-ENABLE-SWITCH-TYPE_50862**: Cloud Assistant advanced protection
        # - **USER-ENABLE-SWITCH-TYPE_50867**: Malicious file implantation
        # - **USER-ENABLE-SWITCH-TYPE_50868**: Suspicious file implantation
        # - **USER-ENABLE-SWITCH-TYPE_50869**: Unauthorized execution of high-risk commands
        # - **USER-ENABLE-SWITCH-TYPE_50870**: Reverse shell
        # - **USER-ENABLE-SWITCH-TYPE_50873**: WebShell command execution
        # - **USER-ENABLE-SWITCH-TYPE_50876**: Evasion of security software
        # - **USER-ENABLE-SWITCH-TYPE_50877**: Malicious program communication
        # - **USER-ENABLE-SWITCH-TYPE_50884**: Suspicious worm script behavior
        # - **USER-ENABLE-SWITCH-TYPE_50885**: Malicious script behavior
        # - **USER-ENABLE-SWITCH-TYPE_50983**: Obfuscation command
        # - **USER-ENABLE-SWITCH-TYPE_51200**: Command line download and execution of malicious files
        # - **USER-ENABLE-SWITCH-TYPE_51201**: Ransomware virus
        # - **USER-ENABLE-SWITCH-TYPE_51202**: Suspicious ransomware behavior
        # - **USER-ENABLE-SWITCH-TYPE_53168**: Process debugging
        # - **USER-ENABLE-SWITCH-TYPE_53272**: Privilege escalation by exploiting kernel vulnerabilities
        # - **USER-ENABLE-SWITCH-TYPE_54034**: Internal network scanning
        # - **USER-ENABLE-SWITCH-TYPE_54265**: PAM module hijacking
        # - **USER-ENABLE-SWITCH-TYPE_54395**: Unauthorized read and write of sensitive files
        # - **USER-ENABLE-SWITCH-TYPE_54699**: Dynamic-link library hijacking
        # - **USER-ENABLE-SWITCH-TYPE_54953**: HashDump attack
        # - **USER-ENABLE-SWITCH-TYPE_57897**: Suspected privilege escalation behavior
        # - **USER-ENABLE-SWITCH-TYPE_62981**: Bypassing security monitoring
        # - **USER-ENABLE-SWITCH-TYPE_64025**: Command execution by entry services [enhanced pattern]
        # - **USER-ENABLE-SWITCH-TYPE_39659**: Sensitive registry key protection
        # - **USER-ENABLE-SWITCH-TYPE_51225**: High-risk command execution by PowerShell
        # - **USER-ENABLE-SWITCH-TYPE_51226**: Suspicious command execution by PowerShell
        # - **USER-ENABLE-SWITCH-TYPE_51228**: High-risk lateral movement tool
        # - **USER-ENABLE-SWITCH-TYPE_51229**: High-risk operations executed by browser services
        # - **USER-ENABLE-SWITCH-TYPE_51230**: Suspicious operations executed by entry services
        # - **USER-ENABLE-SWITCH-TYPE_51232**: High-risk operations executed by system processes
        # - **USER-ENABLE-SWITCH-TYPE_51233**: High-risk operations executed by Java services
        # - **USER-ENABLE-SWITCH-TYPE_51234**: High-risk operations executed by Office components
        # - **USER-ENABLE-SWITCH-TYPE_51235**: High-risk operations executed by web services
        # - **USER-ENABLE-SWITCH-TYPE_51236**: Reverse shell
        # - **USER-ENABLE-SWITCH-TYPE_52815**: High-risk driver loading
        # - **USER-ENABLE-SWITCH-TYPE_52816**: High-risk account manipulation behavior
        # - **USER-ENABLE-SWITCH-TYPE_52818**: Information probing
        # - **USER-ENABLE-SWITCH-TYPE_52820**: Malicious file implantation
        # - **USER-ENABLE-SWITCH-TYPE_52821**: Suspicious process startup
        # - **USER-ENABLE-SWITCH-TYPE_52823**: Execution of high-risk ARK tools
        # - **USER-ENABLE-SWITCH-TYPE_52825**: Unauthorized execution of high-risk commands
        # - **USER-ENABLE-SWITCH-TYPE_52826**: High-risk operations executed by entry services
        # - **USER-ENABLE-SWITCH-TYPE_52827**: Ransomware virus
        # - **USER-ENABLE-SWITCH-TYPE_52828**: Suspicious ransomware behavior
        # - **USER-ENABLE-SWITCH-TYPE_52829**: System backup delete behavior
        # - **USER-ENABLE-SWITCH-TYPE_54168**: LSA security authority service protection
        # - **USER-ENABLE-SWITCH-TYPE_54365**: Creation of service auto-start items
        # - **USER-ENABLE-SWITCH-TYPE_54366**: Creation of high-risk auto-start items
        # - **USER-ENABLE-SWITCH-TYPE_54367**: Creation of scheduled node auto-start items
        # - **USER-ENABLE-SWITCH-TYPE_54368**: Creation of registry auto-start items
        # - **USER-ENABLE-SWITCH-TYPE_54369**: Creation of WMI auto-start items
        # - **USER-ENABLE-SWITCH-TYPE_54373**: Evasion of security software
        # - **USER-ENABLE-SWITCH-TYPE_54374**: Intrusion trace cleanup
        # - **USER-ENABLE-SWITCH-TYPE_54384**: HashDump attack
        # - **USER-ENABLE-SWITCH-TYPE_55251**: High-risk operations executed by database services
        # - **USER-ENABLE-SWITCH-TYPE_57242**: Malicious command execution
        # - **USER-ENABLE-SWITCH-TYPE_57340**: Command line download and execution of malicious files
        # - **USER-ENABLE-SWITCH-TYPE_62357**: Cloud Assistant service information probing
        # - **USER-ENABLE-SWITCH-TYPE_63725**: Suspicious script or binary file implantation by entry services
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
        if self.resource_directory_account_id is not None:
            result['ResourceDirectoryAccountId'] = self.resource_directory_account_id

        if self.source_ip is not None:
            result['SourceIp'] = self.source_ip

        if self.type is not None:
            result['Type'] = self.type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceDirectoryAccountId') is not None:
            self.resource_directory_account_id = m.get('ResourceDirectoryAccountId')

        if m.get('SourceIp') is not None:
            self.source_ip = m.get('SourceIp')

        if m.get('Type') is not None:
            self.type = m.get('Type')

        return self

