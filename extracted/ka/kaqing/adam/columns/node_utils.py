from adam.checks.check_result import CheckResult
from adam.checks.compactionstats import CompactionStats

def merge_gossip(check_results: list[CheckResult]):
    hosts_with_gossip_issue = set()

    for r in check_results:
        for issue in r.issues:
            if issue.category == 'gossip':
                hosts_with_gossip_issue.add(issue.host['value'])

    return hosts_with_gossip_issue

def merge_compactions(check_results: list[CheckResult]):
    compactions_by_host = {}
    for cr in check_results:
        if CompactionStats().name() in cr.details:
            details = cr.details[CompactionStats().name()]
            host = details['host_id']
            c = details['compactions']
            compactions_by_host[host] = c

    return compactions_by_host