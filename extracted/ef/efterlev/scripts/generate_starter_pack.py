#!/usr/bin/env python3
"""Generate the v0.1.21 manifest starter-pack templates.

This script is the source of truth for the 24 hand-authored
`.template.yml` files that ship under `src/efterlev/manifest_templates/`.
Re-run when the FRMR catalog updates with a new KSI that meets the
selection criteria (DECISIONS 2026-05-06 "Tier 1 #3 design"), or when
maintainer-curated `_template_help` content changes.

Run from repo root:
    uv run python scripts/generate_starter_pack.py

Writes:
- src/efterlev/manifest_templates/<KSI-ID>.template.yml (24 files)
- src/efterlev/manifest_templates/SELECTION.md (audit trail of which
  KSIs are in the pack and why)
- src/efterlev/manifest_templates/README.md (workflow guide for users)

The KSI list is hardcoded here per the DECISIONS entry's locked
selection: 17 KSIs from the 3 entirely-procedural themes
(AFR/CED/INR) + 7 KSIs from detector-covered themes whose mapped
800-53 controls are entirely procedural-only families (AT-*, PL-*,
PS-*, PM-*, parts of CA-*).
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "src" / "efterlev" / "manifest_templates"
FRMR_CATALOG = REPO_ROOT / "catalogs" / "frmr" / "FRMR.documentation.json"


# Per-KSI hand-authored content. Description is 2-3 sentences; questions
# are 3-6 prompts the customer should answer when filling in the template.
# Example statement is a short DRAFT showing realistic attestation shape.
#
# These are the bulk of the v0.1.21 work. Authored from each KSI's FRMR
# `requirement` text + general FedRAMP 20x familiarity. A maintainer
# revising should keep questions concrete (specific to what the KSI
# asks for) rather than generic ("what is your commitment to X?").

KSI_HELP: dict[str, dict[str, object]] = {
    # ---------- AFR (FedRAMP-process commitments — entirely procedural) ----------
    "KSI-AFR-ADS": {
        "description": (
            "KSI-AFR-ADS asks how authorization data will be shared with FedRAMP and "
            "downstream consumers (agency partners, future customers reading your "
            "package). The attestation should name the sharing channel(s), the data "
            "types in scope, and the cadence."
        ),
        "questions": [
            "Which authorization artifacts (SSP, POA&M, attestations, vulnerability scans) do you commit to sharing?",
            "Through what channel (FedRAMP Marketplace, OSCAL Hub, direct agency portal, secure email)?",
            "How often is shared data refreshed (continuous, monthly, quarterly)?",
            "Who at your organization owns the sharing process and approves what goes out?",
            "Where is your ADS process documented internally?",
        ],
        "example_statement": (
            "DRAFT — Example: Authorization data is published to the FedRAMP Marketplace and "
            "shared with sponsoring agencies via the FedRAMP Secure Repository quarterly. The "
            "compliance team owns the publish cadence; the VP of Security approves each "
            "release. Internal procedure documented at runbooks/ads-publishing.md."
        ),
    },
    "KSI-AFR-CCM": {
        "description": (
            "KSI-AFR-CCM commits to producing Ongoing Authorization Reports and Quarterly "
            "Reviews per the FedRAMP Collaborative Continuous Monitoring process. The "
            "attestation should name the report owner, the cadence, and where the artifacts land."
        ),
        "questions": [
            "Who produces your Quarterly Reviews and where are they delivered?",
            "What's your cadence for Ongoing Authorization Report updates?",
            "Which automated tooling feeds the reports (this Efterlev pipeline, AWS Config, your SIEM)?",
            "How are findings from the reviews tracked through to remediation?",
            "Where is your CCM process documented internally?",
        ],
        "example_statement": (
            "DRAFT — Example: Quarterly Reviews are produced by the compliance team using outputs "
            "from this Efterlev scan pipeline + AWS Security Hub findings. Reports are delivered "
            "to the agency PM and FedRAMP PMO via the FedRAMP Secure Repository within 30 days "
            "of quarter-end. Findings flow into Jira project SEC-CCM."
        ),
    },
    "KSI-AFR-FSI": {
        "description": (
            "KSI-AFR-FSI asks you to operate a secure inbox for FedRAMP and government "
            "communications. The attestation should name the inbox address, the SLA for "
            "acknowledging messages, and where the runbook lives."
        ),
        "questions": [
            "What email address receives FedRAMP and government communications?",
            "Who monitors the inbox and what's the acknowledgment SLA?",
            "Where is the runbook documented (URL or filesystem path)?",
            "Where do high-severity messages get routed (PagerDuty, on-call, etc.)?",
            "When did you last review the inbox's coverage and routing?",
        ],
        "example_statement": (
            "DRAFT — Example: security@example.com is monitored by the SOC team 24/7. The inbox is "
            "configured in Google Workspace with a 15-minute acknowledgment SLA documented in "
            "runbooks/security-inbox.md, and auto-forwards high-severity reports to the on-call "
            "PagerDuty rotation. A weekly audit of acknowledgment timings is reviewed by the security lead."
        ),
    },
    "KSI-AFR-ICP": {
        "description": (
            "KSI-AFR-ICP integrates FedRAMP's Incident Communications Procedures into your "
            "incident response. The attestation should show that your IR runbook explicitly "
            "addresses the FedRAMP-required notifications and timelines."
        ),
        "questions": [
            "Where in your IR runbook are FedRAMP ICP notifications documented?",
            "What incidents trigger FedRAMP notification (severity threshold, types)?",
            "What's the time window for FedRAMP notification after detection?",
            "Who is authorized to send the FedRAMP notification?",
            "When did you last test the FedRAMP-notification path in a tabletop exercise?",
        ],
        "example_statement": (
            "DRAFT — Example: Our IR runbook (runbooks/incident-response.md §4.3) requires "
            "FedRAMP notification within 1 hour for any Sev-1 or Sev-2 incident affecting the "
            "authorization boundary. The CISO is authorized to send. Last tabletop exercise on "
            "2026-03-15 validated the notification path; results in security/exercises/2026-03-15.md."
        ),
    },
    "KSI-AFR-MAS": {
        "description": (
            "KSI-AFR-MAS applies the FedRAMP Minimum Assessment Scope to define what's in your "
            "authorization boundary. The attestation should name the boundary document, what's "
            "in/out of scope, and the review cadence."
        ),
        "questions": [
            "Where is your authorization-boundary document (SSP §5 or equivalent)?",
            "What AWS account(s) / VPC(s) / cluster(s) are in scope?",
            "What's explicitly out-of-scope, and why?",
            "How are scope changes reviewed and approved?",
            "When is the boundary document reviewed (quarterly, on significant change)?",
        ],
        "example_statement": (
            "DRAFT — Example: Authorization boundary documented in compliance/ssp.md §5. In scope: "
            "AWS GovCloud account 123456789012, all resources in vpc-fedramp-prod. Out of scope: "
            "all commercial-AWS resources, dev/staging environments. Boundary changes require "
            "VP-Security approval; quarterly review by the compliance team."
        ),
    },
    "KSI-AFR-PVA": {
        "description": (
            "KSI-AFR-PVA persistently validates the effectiveness of security decisions and "
            "policies in alignment with the FedRAMP 20x Persistent Validation and Assessment "
            "process. The attestation should name your validation cadence, the tooling, and "
            "how findings are tracked."
        ),
        "questions": [
            "What automated tooling persistently validates your security posture (this Efterlev pipeline, AWS Config, etc.)?",
            "What's the cadence — every commit, daily, weekly?",
            "Who reviews validation results and on what schedule?",
            "How are findings tracked through to remediation?",
            "Where is your PVA process documented internally?",
        ],
        "example_statement": (
            "DRAFT — Example: Efterlev runs on every PR via .github/workflows/pr-compliance-scan.yml; "
            "AWS Config rules + Security Hub findings reviewed weekly by the SecOps team. All "
            "findings routed to Jira project SEC-PVA with SLAs by severity (Critical: 7 days, "
            "High: 30 days). Process documented at compliance/pva-procedure.md."
        ),
    },
    "KSI-AFR-SCG": {
        "description": (
            "KSI-AFR-SCG develops Secure Configuration Guides for customer-facing configuration "
            "of the cloud service. The attestation should name where the guides live, what "
            "they cover, and how they're kept current."
        ),
        "questions": [
            "Where are your customer-facing secure-configuration guides published?",
            "What configuration areas do they cover (network, IAM, logging, encryption)?",
            "Who owns the guides and reviews them for accuracy?",
            "How are customers notified when guides update?",
            "When was the last full review?",
        ],
        "example_statement": (
            "DRAFT — Example: Secure Configuration Guides published at docs.example.com/security/. "
            "Cover IAM-best-practices, network-isolation, audit-logging, encryption-at-rest "
            "configuration. The Solutions Engineering team owns the guides; reviewed semi-annually "
            "by the security architect. Customer change notifications go via the product changelog."
        ),
    },
    "KSI-AFR-SCN": {
        "description": (
            "KSI-AFR-SCN tracks significant changes to the cloud service offering and notifies "
            "FedRAMP per the SCN process. The attestation should name what counts as significant, "
            "how changes are tracked, and the notification channel."
        ),
        "questions": [
            "What change categories count as 'significant' for FedRAMP SCN purposes?",
            "Where are significant changes logged (change-management system, ticketing)?",
            "Who reviews proposed changes for SCN-applicability?",
            "What's the notification channel and timeline to FedRAMP?",
            "Where is your SCN process documented internally?",
        ],
        "example_statement": (
            "DRAFT — Example: Significant changes (defined in compliance/scn-categories.md) are "
            "tracked in our change-management system (Jira CR project). The Compliance Officer "
            "reviews each CR for SCN-applicability; FedRAMP-significant changes go to the FedRAMP "
            "PMO via the FedRAMP Secure Repository within 30 days of approval per SCN guidance."
        ),
    },
    "KSI-AFR-UCM": {
        "description": (
            "KSI-AFR-UCM ensures cryptographic modules used to protect federal data are selected "
            "per FedRAMP 20x Using Cryptographic Modules guidance (FIPS 140-validated, etc.). "
            "The attestation should name where you've documented the cryptographic-module inventory."
        ),
        "questions": [
            "Where is your cryptographic-module inventory documented?",
            "Which FIPS 140-validated modules are in use (KMS, TLS libraries, etc.)?",
            "How are non-validated modules identified and remediated?",
            "Who reviews the inventory for completeness and currency?",
            "What's the review cadence?",
        ],
        "example_statement": (
            "DRAFT — Example: Cryptographic-module inventory at compliance/crypto-inventory.md. "
            "All in-boundary cryptography uses FIPS 140-3 validated modules: AWS KMS (FIPS 140-3 "
            "Level 3), OpenSSL FIPS provider for application-layer TLS. Inventory reviewed "
            "quarterly by the security architect; deviations flagged in Jira SEC-CRYPTO."
        ),
    },
    "KSI-AFR-VDR": {
        "description": (
            "KSI-AFR-VDR documents the vulnerability detection and response methodology used "
            "within the cloud service offering, in alignment with FedRAMP VDR. The attestation "
            "should name your detection tooling, response SLAs by severity, and where the procedure lives."
        ),
        "questions": [
            "What automated vulnerability-detection tooling do you use (Inspector, dependency scanners, secret scanners)?",
            "What's your response SLA by severity (Critical, High, Medium, Low)?",
            "Where are findings tracked through to remediation?",
            "Who owns the VDR process?",
            "When was it last reviewed for effectiveness?",
        ],
        "example_statement": (
            "DRAFT — Example: VDR procedure at compliance/vdr-procedure.md. Detection: AWS Inspector "
            "(EC2 + ECR), GitHub Dependabot + Secret Scanning, semgrep + bandit on every PR. SLAs: "
            "Critical 7 days, High 30 days, Medium 90 days, Low next sprint. Findings tracked in "
            "Jira project SEC-VULN; SecOps reviews weekly."
        ),
    },
    # ---------- CED (training reviews — entirely procedural) ----------
    "KSI-CED-DET": {
        "description": (
            "KSI-CED-DET reviews the effectiveness of role-specific training given to development "
            "and engineering staff covering secure-software best practices. The attestation should "
            "name the training, the cadence, and how effectiveness is measured."
        ),
        "questions": [
            "What development/engineering training covers secure-software best practices?",
            "What's the training cadence (annual, on-hire, on-role-change)?",
            "How is training effectiveness measured (quiz scores, observed PR quality, code-review feedback)?",
            "Who owns the training program?",
            "When did you last review the program for effectiveness?",
        ],
        "example_statement": (
            "DRAFT — Example: Engineering staff complete the in-house Secure Coding Fundamentals "
            "course (4 hours, OWASP Top 10 + cloud-specific patterns) on hire and annually. "
            "Effectiveness measured via post-training quiz (≥80% pass) + half-yearly review of "
            "PR-review comments tagged secure-coding. VP Engineering owns the program."
        ),
    },
    "KSI-CED-RGT": {
        "description": (
            "KSI-CED-RGT reviews the effectiveness of training given to all employees on policies, "
            "procedures, and security topics. The attestation should name the general training "
            "program, the cadence, and how completion + effectiveness are tracked."
        ),
        "questions": [
            "What general security/compliance training does every employee complete?",
            "What's the cadence (on-hire, annual)?",
            "How is completion tracked (LMS, HRIS report)?",
            "How is effectiveness measured (quiz scores, phishing test results)?",
            "Who owns the program?",
        ],
        "example_statement": (
            "DRAFT — Example: All employees complete the General Security Awareness training "
            "(KnowBe4, 1 hour) on hire and annually. Completion tracked in Workday with "
            "quarterly compliance reports to People Ops. Effectiveness measured via the "
            "monthly KnowBe4 phishing simulations (target: <5% click rate). HR Compliance owns the program."
        ),
    },
    "KSI-CED-RRT": {
        "description": (
            "KSI-CED-RRT reviews role-specific training given to staff involved with incident "
            "response or disaster recovery. The attestation should name the IR/DR training program, "
            "who's enrolled, and how effectiveness is measured (typically tabletop exercises)."
        ),
        "questions": [
            "Which roles complete IR/DR-specific training?",
            "What's the training format (course, tabletop, simulation)?",
            "What's the cadence?",
            "How is effectiveness measured (tabletop performance, time-to-recover in drills)?",
            "Who owns the program?",
        ],
        "example_statement": (
            "DRAFT — Example: SecOps + on-call SREs complete the in-house IR Runbook training "
            "annually + participate in quarterly tabletop exercises (one IR scenario, one DR "
            "scenario per year). Effectiveness measured via tabletop after-action reports — "
            "target time-to-acknowledge <5 min, time-to-mitigate <30 min for Sev-1. "
            "Director of Security Operations owns the program."
        ),
    },
    "KSI-CED-RST": {
        "description": (
            "KSI-CED-RST reviews role-specific training given to high-risk roles (privileged-access "
            "users, administrators). The attestation should name which roles get extra training, "
            "what it covers, and how completion + effectiveness are tracked."
        ),
        "questions": [
            "Which roles are 'high-risk' (privileged access, production data access)?",
            "What additional training do they complete beyond the general program?",
            "What's the cadence?",
            "How is access provisioning gated on training completion?",
            "Who reviews the program for effectiveness?",
        ],
        "example_statement": (
            "DRAFT — Example: Production-access roles (SREs, on-call engineers, DBAs) complete the "
            "Privileged Access Training (2 hours, covers least-privilege, audit-logging, "
            "secrets-handling) on role assignment and annually. Production access provisioning "
            "in IAM is gated on the training-completion attestation in Workday. The Security "
            "Architect reviews program annually."
        ),
    },
    # ---------- INR (incident response review — entirely procedural) ----------
    "KSI-INR-AAR": {
        "description": (
            "KSI-INR-AAR generates incident after-action reports and incorporates lessons learned. "
            "The attestation should name the AAR template, who produces them, the timeline after "
            "incidents, and how lessons feed back into runbooks/training."
        ),
        "questions": [
            "What's the AAR template / process?",
            "Who produces AARs and on what timeline after incidents?",
            "How are lessons-learned tracked through to runbook + training updates?",
            "Where are AARs stored?",
            "How often is the AAR process itself reviewed?",
        ],
        "example_statement": (
            "DRAFT — Example: AARs follow the template at runbooks/aar-template.md. Produced by "
            "the IC within 5 business days of incident closure. Lessons-learned action items go to "
            "Jira project SEC-LESSONS with owners + due dates; runbook updates required before "
            "ticket close. AARs archived in security/aars/. Process reviewed annually."
        ),
    },
    "KSI-INR-RIR": {
        "description": (
            "KSI-INR-RIR persistently reviews the effectiveness of documented incident-response "
            "procedures. The attestation should name the IR runbook, the review cadence, and "
            "what triggers an IR-procedure update."
        ),
        "questions": [
            "Where is the IR runbook documented?",
            "What's the regular review cadence (annual, semi-annual)?",
            "What triggers an out-of-cycle IR-procedure update (new incident type, AAR finding, regulatory change)?",
            "Who owns the runbook + reviews?",
            "When was the last full review?",
        ],
        "example_statement": (
            "DRAFT — Example: IR runbook at runbooks/incident-response.md. Reviewed semi-annually "
            "by the IR program owner (Director of Security Operations) + after every Sev-1 "
            "incident. Lessons-learned action items from AARs (KSI-INR-AAR) drive interim updates. "
            "Last full review: 2026-03-15."
        ),
    },
    "KSI-INR-RPI": {
        "description": (
            "KSI-INR-RPI reviews past incidents for patterns or vulnerabilities. The attestation "
            "should name the cadence of pattern review, who participates, and how patterns drive "
            "preventive work."
        ),
        "questions": [
            "What's the cadence of past-incident pattern review (quarterly, annual)?",
            "Who participates (SecOps, engineering, leadership)?",
            "How are patterns translated into preventive work (architecture changes, training updates, runbook revisions)?",
            "Where is the pattern-review output documented?",
            "When was the last review?",
        ],
        "example_statement": (
            "DRAFT — Example: Quarterly past-incident pattern review by the SecOps + Platform Eng "
            "leadership. Reviews all Sev-1/Sev-2 incidents from the prior quarter, looks for "
            "common roots (process gap, tooling gap, knowledge gap), and routes preventive "
            "actions to Jira SEC-PREVENT. Output documented in security/quarterly-reviews/. "
            "Last review: 2026-04-10."
        ),
    },
    # ---------- PIY (process review — 4 of 5 are procedural) ----------
    "KSI-PIY-RES": {
        "description": (
            "KSI-PIY-RES reviews executive support for security objectives. The attestation should "
            "name the forum (board meeting, leadership review), the cadence, and what evidence of "
            "executive support exists (signed policies, budget approvals)."
        ),
        "questions": [
            "What forum reviews executive support (board security committee, CEO-staff)?",
            "What's the cadence?",
            "What artifacts evidence executive support (signed security policy, approved budget, leadership-attended training)?",
            "Who owns the executive-engagement program?",
            "When was the last review?",
        ],
        "example_statement": (
            "DRAFT — Example: Quarterly Board Security Committee review chaired by the CEO. "
            "Artifacts: CEO-signed Information Security Policy (annually re-signed); approved "
            "security budget reviewed per quarter; security KPIs reported to the full Board. "
            "CISO owns the program. Last review: 2026-04-30 board meeting minutes."
        ),
    },
    "KSI-PIY-RIS": {
        "description": (
            "KSI-PIY-RIS reviews the effectiveness of investments in achieving security objectives. "
            "The attestation should name the budgeting + ROI-review process and how outcomes are "
            "tracked back to investments."
        ),
        "questions": [
            "What's the security-investment review process (annual budget cycle, quarterly ROI review)?",
            "How are outcomes measured (incident-rate trends, audit-finding trends, MTTR)?",
            "Who reviews investment effectiveness?",
            "How are findings used to adjust the next budget cycle?",
            "Where is the process documented?",
        ],
        "example_statement": (
            "DRAFT — Example: Security investments reviewed annually as part of the FY budget "
            "cycle by the CFO + CISO. Outcomes tracked: vulnerability backlog trend, MTTR for "
            "Sev-1 incidents, audit-finding remediation rate. Quarterly ROI checkpoint with "
            "the Board Security Committee. Process documented at compliance/security-budget-review.md."
        ),
    },
    "KSI-PIY-RSD": {
        "description": (
            "KSI-PIY-RSD reviews the effectiveness of building security and privacy considerations "
            "into the SDLC, aligning with CISA Secure By Design principles. The attestation should "
            "name your SDLC security gates, how they're enforced, and the review cadence."
        ),
        "questions": [
            "What SDLC stages have security gates (design review, code review, deploy review)?",
            "How are gates enforced (mandatory CI checks, manual sign-off)?",
            "How is alignment with CISA Secure By Design principles measured?",
            "Who reviews SDLC-security effectiveness?",
            "What's the review cadence?",
        ],
        "example_statement": (
            "DRAFT — Example: SDLC security gates: threat-modeling required for any feature with "
            "auth/authz changes (design review); semgrep + bandit + dependency-audit on every PR "
            "(blocking CI checks); CodeQL + ZAP scan in pre-deploy. Security Architect reviews "
            "SDLC effectiveness annually against the CISA Secure By Design principles checklist. "
            "Last review: 2026-02-20, output at compliance/sdlc-review-2026.md."
        ),
    },
    "KSI-PIY-RVD": {
        "description": (
            "KSI-PIY-RVD reviews the effectiveness of the vulnerability disclosure program. "
            "The attestation should name where the disclosure policy lives, the response SLAs, "
            "and how the program's effectiveness is reviewed."
        ),
        "questions": [
            "Where is your vulnerability disclosure policy published (security.txt, dedicated page)?",
            "What channel do reports come through (HackerOne, bug bounty, direct email)?",
            "What are the response SLAs (acknowledge, triage, fix)?",
            "How is program effectiveness reviewed (report volume trend, time-to-fix, researcher satisfaction)?",
            "Who owns the program?",
        ],
        "example_statement": (
            "DRAFT — Example: Disclosure policy at example.com/security.txt + example.com/security. "
            "Reports come via security@example.com or HackerOne (private program). SLAs: "
            "acknowledge 24h, triage 5 days, Critical fix 7 days. Annual review by the CISO "
            "covering report volume, time-to-fix trends, researcher satisfaction. "
            "Program owned by the Application Security Lead."
        ),
    },
    # ---------- Procedural KSIs in detector-covered themes ----------
    "KSI-CMT-RVP": {
        "description": (
            "KSI-CMT-RVP reviews the effectiveness of documented change-management procedures. "
            "Detector evidence covers individual change-application (KSI-CMT-LMC, RMV, VTD); this "
            "KSI is the procedural commitment to review the procedures themselves."
        ),
        "questions": [
            "Where is your change-management procedure documented?",
            "What's the review cadence?",
            "What metrics signal procedure effectiveness (MTTR, change-failure rate, rollback frequency)?",
            "Who participates in the review?",
            "When was the last review?",
        ],
        "example_statement": (
            "DRAFT — Example: Change-management procedure at runbooks/change-management.md. "
            "Reviewed semi-annually by Platform Eng + SecOps leadership. Metrics: change-failure "
            "rate (DORA), MTTR for change-induced incidents, rollback frequency. Review "
            "incorporates AAR findings (KSI-INR-AAR). Last review: 2026-03-30."
        ),
    },
    "KSI-RPL-RRO": {
        "description": (
            "KSI-RPL-RRO reviews desired Recovery Time Objectives (RTO) and Recovery Point "
            "Objectives (RPO). Detector evidence covers backup configuration (KSI-RPL-ABO) and "
            "restore testing (KSI-RPL-TRC); this KSI is the procedural commitment that the "
            "objectives themselves are reviewed and current."
        ),
        "questions": [
            "Where are your RTO/RPO targets documented?",
            "What systems / data classes do they cover?",
            "What's the review cadence (annual, on significant change)?",
            "How are objectives validated against business need (interviews with product owners, customer SLAs)?",
            "Who owns the objectives + reviews?",
        ],
        "example_statement": (
            "DRAFT — Example: RTO/RPO targets at compliance/recovery-objectives.md. Cover all "
            "in-boundary services: customer-facing API (RTO 1h, RPO 5min), batch processing "
            "(RTO 4h, RPO 24h), reporting (RTO 24h, RPO 24h). Reviewed annually by the SRE "
            "Director + Product Eng leadership; validated against product SLAs. "
            "Last review: 2026-01-15."
        ),
    },
    "KSI-SVC-PRR": {
        "description": (
            "KSI-SVC-PRR reviews plans, procedures, and the state of information resources after "
            "changes to limit residual risk. The attestation should name the post-change review "
            "process, who conducts it, and what evidence remains."
        ),
        "questions": [
            "What post-change review process exists (post-deploy validation, security regression check)?",
            "Who conducts the review and on what timeline after change?",
            "What artifacts are produced (validation report, incident-report-if-any)?",
            "How are findings tracked back to remediation?",
            "Where is the process documented?",
        ],
        "example_statement": (
            "DRAFT — Example: Post-change review per runbooks/post-deploy-review.md. SREs + "
            "SecOps validate within 24h of every production-significant change: monitor key "
            "metrics, check Security Hub for new findings, validate IAM role-set drift. Findings "
            "into Jira SEC-RESIDUAL with severity-based SLAs. Process reviewed quarterly."
        ),
    },
    "KSI-MLA-RVL": {
        "description": (
            "KSI-MLA-RVL is the procedural commitment to PERSISTENTLY review and audit logs. "
            "Detector evidence covers log retention (`aws.centralized_log_aggregation`) and "
            "least-privilege access on log data (`aws.mla_log_access_least_privilege`); this KSI "
            "is the human-process commitment that someone is actually reading the logs and "
            "acting on what they find. Per DECISIONS 2026-05-07 'Tier 1 #4 design', classified "
            "procedural-only despite mapping to technical control families (AC-*, AU-*, SI-*) — "
            "the requirement text is review-the-logs framing, not configure-the-logs framing."
        ),
        "questions": [
            "Which log streams are reviewed (CloudWatch Log Groups, S3 access logs, VPC Flow, application logs)?",
            "What's the review cadence (continuous via SIEM correlation, daily, weekly)?",
            "Who reviews — automated tooling first, then humans on alert? Named role or rotation?",
            "What review activity gets recorded as evidence (Splunk dashboard exports, ticket links, audit-log queries with timestamps)?",
            "How are findings escalated (Sev rubric, on-call paging, ticket creation in which queue)?",
            "Where is the review process documented?",
        ],
        "example_statement": (
            "DRAFT — Example: Continuous correlation via Splunk Enterprise Security on all "
            "in-boundary log groups (CloudWatch + S3 access + VPC Flow + EKS audit + application). "
            "SOC analyst rotation reviews the SIEM queue 24/7; daily summary report at "
            "splunk-dashboards/daily-soc-review. Sev-1/2 findings page on-call within 15 min "
            "via PagerDuty; Sev-3+ tracked in Jira SEC-MLA-RVL. Review process documented at "
            "runbooks/log-review.md; reviewed semi-annually. Last process review: 2026-04-12."
        ),
    },
    "KSI-SVC-EIS": {
        "description": (
            "KSI-SVC-EIS is the meta-procedural commitment to PERSISTENTLY evaluate information "
            "resources for security-improvement opportunities and IMPLEMENT improvements based on "
            "that evaluation. Distinct from KSI-SVC-PRR (post-change residual-risk review): this "
            "KSI is the proactive scan-the-environment-for-things-to-improve loop, not the "
            "react-to-a-change loop. Per DECISIONS 2026-05-07 'Tier 1 #4 design', classified "
            "procedural-only — the controls span technical families (CM-*, SC-*, SI-*, SR-*) but "
            "the KSI is fundamentally about HAVING an improvement program, not about any one "
            "configuration."
        ),
        "questions": [
            "What ongoing evaluation surfaces feed the improvement queue (Security Hub findings, AWS Config drift, internal red-team output, dependency-vuln scans, customer-reported security findings, threat-model reviews)?",
            "Who owns the improvement queue (named role or team)?",
            "What's the cadence for triage + prioritization (sprint planning, monthly security review)?",
            "How are improvements committed to and tracked (Jira epic, OKR, security-roadmap doc)?",
            "What metrics signal the program's health (mean-time-to-remediate by severity, backlog age, % findings closed within SLA)?",
            "Where is the program documented? When was it last reviewed?",
        ],
        "example_statement": (
            "DRAFT — Example: Security improvement program owned by the Security Eng team lead. "
            "Inputs: AWS Security Hub (continuous), AWS Config drift (continuous), Snyk dep-vuln "
            "scans (per-PR + nightly), quarterly internal red-team, customer security-disclosure "
            "intake at security@example.com. Triage weekly in the Security stand-up; prioritized "
            "items become Jira SEC-EIS tickets with severity-based SLAs (Sev-1: 7d, Sev-2: 30d, "
            "Sev-3: 90d). Quarterly metrics review in the Security & Compliance steering committee. "
            "Program documented at runbooks/security-improvement-program.md; reviewed annually. "
            "Last metrics review: 2026-04-22."
        ),
    },
}


# ---------- generation logic ----------


def _yaml_quote(s: str) -> str:
    """Render a string as a single-line YAML literal, escaping nothing
    (strings here don't contain quotes-internally; if they did, callers
    use block style instead)."""
    return f'"{s}"'


def _yaml_block(text: str, indent: int) -> str:
    """Render multi-line text as a YAML block scalar (`>` folded style for
    descriptions, `>` for statements). Preserves paragraph breaks."""
    pad = " " * indent
    lines = text.strip().split("\n")
    return "\n".join(pad + line for line in lines)


def render_template(ksi_id: str, ksi_name: str, help_data: dict[str, object]) -> str:
    """Generate one `<KSI-ID>.template.yml` file's contents."""
    description = help_data["description"]
    questions = help_data["questions"]
    example_statement = help_data["example_statement"]
    assert isinstance(description, str)
    assert isinstance(questions, list)
    assert isinstance(example_statement, str)

    # Format the questions list as YAML.
    question_lines = "\n".join(f'      - "{q}"' for q in questions)

    return f"""# {ksi_id} — {ksi_name}
#
# DRAFT — this is a starter-pack template. Copy it to
# `.efterlev/manifests/<ksi-id>.yml` (drop the `.template` suffix) and
# fill in the DRAFT placeholders before letting it land in your
# attestation pipeline. The `_template_help` block carries the
# questions you should answer; remove that block once filled in.

ksi: {ksi_id}
name: "{ksi_name}"

_template_help:
  description: >
{_yaml_block(str(description), 4)}
  questions:
{question_lines}

evidence:
  - type: attestation
    statement: >
{_yaml_block(str(example_statement), 6)}
    attested_by: "DRAFT — your-vp-security@example.com"
    attested_at: "DRAFT — YYYY-MM-DD"
    reviewed_at: "DRAFT — YYYY-MM-DD"
    next_review: "DRAFT — YYYY-MM-DD (recommend 6-month review cadence)"
    supporting_docs:
      - "DRAFT — ./policies/your-runbook.pdf"
      - "DRAFT — https://wiki.your-company.example/path-to-relevant-docs"
"""


def main() -> int:
    catalog = json.loads(FRMR_CATALOG.read_text())
    ksi_themes = catalog["KSI"]
    name_by_id: dict[str, str] = {}
    for _theme_name, theme in ksi_themes.items():
        for ksi_id, ind in theme.get("indicators", {}).items():
            name_by_id[ksi_id] = ind.get("name", ksi_id)

    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for ksi_id, help_data in KSI_HELP.items():
        if ksi_id not in name_by_id:
            print(f"  warning: {ksi_id} not in FRMR catalog — skipping")
            continue
        body = render_template(ksi_id, name_by_id[ksi_id], help_data)
        out_path = TEMPLATES_DIR / f"{ksi_id}.template.yml"
        out_path.write_text(body, encoding="utf-8")
        written += 1
    print(f"wrote {written} template files to {TEMPLATES_DIR}")

    # --- SELECTION.md audit trail ---
    selection_md = (
        "# Manifest Starter Pack — KSI Selection\n"
        "\n"
        "This file documents which KSIs are in the starter pack and why.\n"
        'Selection criteria locked in DECISIONS 2026-05-06 "Tier 1 #3 design:\n'
        'Evidence Manifest starter pack".\n'
        "\n"
        "## Selection criteria\n"
        "\n"
        "**Hybrid theme + control-family.** A KSI is included if EITHER:\n"
        "\n"
        "1. It belongs to one of the 3 entirely-procedural FRMR themes\n"
        '   (AFR, CED, INR — see CLAUDE.md "What\'s deferred").\n'
        "2. Its mapped 800-53 controls fall ONLY into procedural-only\n"
        "   families: AT-* (training), PL-* (planning), PS-* (personnel security),\n"
        "   PM-* (program management), or large parts of CA-* (assessment).\n"
        "\n"
        "## Included KSIs\n"
        "\n"
    )
    for ksi_id in KSI_HELP:
        ksi_name = name_by_id.get(ksi_id, "(not in FRMR catalog)")
        selection_md += f"- **{ksi_id}** — {ksi_name}\n"
    selection_md += (
        "\n"
        "## Excluded by design\n"
        "\n"
        "- All other KSIs are detector-evidenceable (or partially so);\n"
        "  attestation templates would compete with scanner output.\n"
        "  See `efterlev detectors list` for what ships today.\n"
        "- KSI-PIY-GIV (Generating Inventories) — IS scanner-evidenceable\n"
        "  via the `aws.terraform_inventory` detector; excluded from the\n"
        "  starter pack despite being in the PIY theme.\n"
    )
    (TEMPLATES_DIR / "SELECTION.md").write_text(selection_md, encoding="utf-8")
    print(f"wrote SELECTION.md ({len(KSI_HELP)} KSIs documented)")

    # --- README.md workflow guide ---
    readme_md = """# Evidence Manifest Starter Pack

This directory holds template Evidence Manifests for the
commonly-procedural KSIs in the FedRAMP 20x baseline — the ones
detectors cannot reach because the underlying commitment is
process / policy / training, not infrastructure configuration.

## Workflow

1. **Read** the template for a KSI you're attesting to. Each carries a
   `_template_help` block with a description and the specific questions
   you should answer.

2. **Copy** the template to `.efterlev/manifests/`, dropping the
   `.template` suffix from the filename:

   ```bash
   cp .efterlev/manifests/starter-pack/KSI-AFR-FSI.template.yml \\
      .efterlev/manifests/KSI-AFR-FSI.yml
   ```

   (The `.template.yml` extension keeps templates out of the manifest
   loader's pickup; `.yml` brings them in.)

3. **Edit** the copy. Replace every `DRAFT —` placeholder with your
   organization's specific commitment. The `attested_by`, `attested_at`,
   `reviewed_at`, and `next_review` fields all need real values. Remove
   the `_template_help` block once you've answered its questions.

4. **Verify** by running `efterlev scan --target .` — the new manifest
   should appear in the manifest-records count. The next `efterlev
   agent gap` will incorporate it.

5. **Re-review** by the `next_review` date. The attestation isn't a
   one-time artifact; FedRAMP 20x expects continuous validation.

## Refreshing the templates

This directory is regenerated by `efterlev manifests init --starter-pack`.
If you've already filled in some manifests in `.efterlev/manifests/`,
those are not touched — only the contents of this `starter-pack/`
subdirectory are replaced.

To pull updated template content from a newer Efterlev release:

```bash
efterlev manifests init --starter-pack --force
```

`--force` is required because re-running otherwise would refuse to
overwrite this subdirectory. Templates evolve as FRMR's KSI catalog
evolves; check `SELECTION.md` for the audit trail.

## Selection criteria

See `SELECTION.md` for which KSIs are in the pack and why. Roughly:
the 3 entirely-procedural FRMR themes (AFR/CED/INR) plus KSIs in
detector-covered themes whose 800-53 controls are entirely
procedural-only.
"""
    (TEMPLATES_DIR / "README.md").write_text(readme_md, encoding="utf-8")
    print("wrote README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
