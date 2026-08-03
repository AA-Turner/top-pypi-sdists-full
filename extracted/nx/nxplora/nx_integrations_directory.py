"""
nx_integrations_directory.py — NX's integration directory + the dynamic resolver.

Two halves of "no ceilings, Claude/Codex-style" integrations:

  1. DIRECTORY — a curated, per-world set of the integrations operators actually
     need (WORLD_INTEGRATIONS). Real services only, with accurate auth type.

  2. RESOLVER — the ladder that runs when an operator asks for ANYTHING:
       directory  → already curated; connect via its auth (OAuth channel /
                    MCP / api key).
       mcp_registry → not curated but a known MCP server exists; offer install.
       discoverable → not in any registry; NX can web-search for an MCP server /
                    install method, then install (APPROVAL-GATED) + guide login.
       bring_your_own → nothing found; the operator installs/brings it, NX stays
                    signed in to continue — exactly like bringing an MCP server
                    to Claude Code.

DESIGN INVARIANTS:
  - The resolver returns a PLAN. It NEVER installs or connects on its own — every
    install/connect step is marked requires_approval and is executed by the CLI
    behind the approval gate. (No silent software install. Ever.)
  - It is HONEST about state: "ready" means a built connector exists (e.g. Meta);
    it never claims something is installed/connected when it isn't.
  - Secrets/tokens are handled by the connector layer (nx_channels) — Keychain
    only, never here.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Integration:
    name: str
    category: str
    auth: str          # "oauth" | "api_key" | "mcp" | "none"
    use: str = ""
    is_mcp: bool = False
    connector: str = ""  # a built ChannelConnector name (e.g. "meta") if any


# ── DIRECTORY ────────────────────────────────────────────────────────────────
# Seeded with real services for the highest-traffic worlds + the built OAuth
# channels. The per-world fan-out expands this to every world; merge_directory()
# folds that generated data in without clobbering built connectors.
WORLD_INTEGRATIONS = {
    "strategy": [
        Integration("Notion", "Docs & Knowledge Base", "oauth", "Draft, structure, and store strategy docs, OKRs, planning wikis, and m", is_mcp=True),
        Integration("Google Workspace (Docs/Sheets/Slides)", "Documents & Spreadsheets", "oauth", "Author strategy memos, financial models in Sheets, and board/strategy", is_mcp=False),
        Integration("Slack", "Team Communication", "oauth", "Circulate plans for review, run async strategy discussions, and route", is_mcp=True),
        Integration("Linear", "Project & Initiative Tracking", "oauth", "Turn strategy into tracked initiatives, projects, and roadmap mileston", is_mcp=True),
        Integration("Atlassian Confluence", "Knowledge Base & Wiki", "oauth", "Publish finalized strategy docs, OKRs, and decision records to a compa", is_mcp=True),
        Integration("Atlassian Jira", "Project Management", "oauth", "Break strategic initiatives into epics and sprints; track delivery aga", is_mcp=True),
        Integration("HubSpot", "CRM & Revenue Data", "oauth", "Pull pipeline, revenue, and customer data to ground strategy in real G", is_mcp=True),
        Integration("Airtable", "Database & Planning", "oauth", "Maintain structured strategy databases such as initiative trackers, co", is_mcp=False),
        Integration("Figma", "Diagramming & Visual Strategy", "oauth", "Build strategy maps, org and process diagrams, and visual frameworks (", is_mcp=True),
        Integration("Google Analytics 4", "Analytics & Metrics", "oauth", "Source performance and traffic metrics to validate assumptions and mea", is_mcp=False),
    ],
    "finance": [
        Integration("QuickBooks Online", "Accounting / bookkeeping", "oauth", "Core general ledger: record transactions, reconcile accounts, manage i", is_mcp=False),
        Integration("Stripe", "Payments / billing", "api_key", "Accept payments, run subscriptions and invoicing, issue refunds, and p", is_mcp=True),
        Integration("Plaid", "Banking data / connectivity", "api_key", "Connect bank and card accounts to pull balances and transactions for c", is_mcp=False),
        Integration("Brex", "Corporate cards / spend management", "api_key", "Manage corporate cards, expenses, and reimbursements, and sync spend i", is_mcp=False),
        Integration("Ramp", "Spend management / AP", "api_key", "Corporate cards, bill pay, and expense automation with approval workfl", is_mcp=False),
        Integration("Bill.com", "Accounts payable / receivable", "api_key", "Route invoices through approval, schedule and submit vendor payments,", is_mcp=False),
        Integration("Gusto", "Payroll / HR", "oauth", "Run payroll, manage contractors and benefits, and sync payroll journal", is_mcp=False),
        Integration("NetSuite", "ERP / financials", "oauth", "Mid-market/enterprise ERP for GL, AP/AR, revenue recognition, and mult", is_mcp=False),
        Integration("Xero", "Accounting / bookkeeping", "oauth", "Alternative cloud accounting platform for bookkeeping, bank reconcilia", is_mcp=False),
    ],
    "legal": [
        Integration("DocuSign", "E-Signature & Agreement Execution", "oauth", "Send contracts and legal agreements for signature, track signing statu", is_mcp=True),
        Integration("Clio", "Legal Practice Management", "oauth", "Core system of record for law-firm operations: matters, contacts, cale", is_mcp=False),
        Integration("iManage", "Document Management System (DMS)", "oauth", "Enterprise legal document and email management (the dominant DMS in la", is_mcp=True),
        Integration("NetDocuments", "Document Management System (DMS)", "oauth", "Cloud-native legal DMS alternative to iManage for storing, organizing,", is_mcp=True),
        Integration("Harvey", "Legal AI / Drafting & Review", "api_key", "Domain-specific legal AI for drafting, contract review, due diligence,", is_mcp=False),
        Integration("Westlaw (Thomson Reuters)", "Legal Research", "api_key", "Primary legal research platform for case law, statutes, regulations, a", is_mcp=False),
        Integration("Ironclad", "Contract Lifecycle Management (CLM)", "api_key", "Contract lifecycle management for drafting, approval workflows, redlin", is_mcp=False),
        Integration("Microsoft Word (Microsoft 365 / Graph)", "Document Authoring & Collaboration", "oauth", "The de facto drafting and redlining surface for legal documents (track", is_mcp=False),
        Integration("Adobe Acrobat / PDF Services", "Document Production & PDF", "oauth", "Produce, combine, redact, and finalize court-ready and client-facing P", is_mcp=False),
        Integration("PACER / CM-ECF (federal court e-filing)", "Court Filing & Records", "none", "Access federal court records and electronically file documents with U.", is_mcp=False),
    ],
    "compliance": [
        Integration("Vanta", "Compliance automation / GRC", "oauth", "Continuous compliance monitoring and audit automation for SOC 2, ISO 2", is_mcp=False),
        Integration("Drata", "Compliance automation / GRC", "oauth", "Automated control monitoring and evidence collection across frameworks", is_mcp=False),
        Integration("DocuSign", "E-signature / agreements", "oauth", "Send, sign, and execute compliance documents, policy attestations, DPA", is_mcp=False),
        Integration("Google Drive", "Document storage / collaboration", "oauth", "Author, store, and version policy documents, control narratives, and e", is_mcp=False),
        Integration("Slack", "Communication / workflow", "oauth", "Route compliance alerts, control-failure notifications, approval reque", is_mcp=False),
        Integration("Jira", "Issue tracking / remediation", "oauth", "Track remediation tasks, control gaps, and audit findings as tickets w", is_mcp=False),
        Integration("Okta", "Identity / access governance", "oauth", "Source of truth for user identity, access reviews, and provisioning/de", is_mcp=False),
        Integration("AWS", "Cloud infrastructure evidence", "api_key", "Pull configuration, CloudTrail logs, and security posture (Config, Sec", is_mcp=False),
        Integration("OneTrust", "Privacy / data governance", "oauth", "Manage privacy programs, data mapping, consent, DSAR fulfillment, and", is_mcp=False),
        Integration("Workiva", "Regulatory reporting / disclosure", "oauth", "Collaborative regulatory reporting, SOX, and disclosure management wit", is_mcp=False),
    ],
    "research": [
        Integration("Google Scholar", "Literature discovery", "none", "Discovery and planning step: search the academic literature, find pape", is_mcp=False),
        Integration("arXiv", "Preprint repository", "none", "Plan and publish/submit: search preprints via the open arXiv API (no a", is_mcp=False),
        Integration("Zotero", "Reference management", "api_key", "Edit/review: collect, organize, and cite references; manage the biblio", is_mcp=False),
        Integration("Overleaf", "Manuscript authoring", "oauth", "Edit step: collaborative LaTeX authoring of manuscripts and submission", is_mcp=False),
        Integration("Notion", "Planning & knowledge base", "oauth", "Plan step: research notebooks, project planning, literature logs, and", is_mcp=True),
        Integration("Google Drive", "Storage & collaboration", "oauth", "Edit/review: store datasets, drafts, and shared documents; collaborate", is_mcp=False),
        Integration("Slack", "Team collaboration", "oauth", "Review step: coordinate the research team, route review requests, and", is_mcp=True),
        Integration("ORCID", "Researcher identity", "oauth", "Publish/submit: authenticated researcher identity used by journals and", is_mcp=False),
        Integration("OpenAlex", "Scholarly metadata", "none", "Plan step: open API for works, authors, venues, and citation graphs to", is_mcp=False),
        Integration("Figshare", "Data/output publishing", "oauth", "Publish/submit: deposit datasets, figures, and supplementary research", is_mcp=False),
    ],
    "product": [
        Integration("Linear", "Issue tracking & planning", "oauth", "Plan and triage product work: roadmaps, projects, cycles, and issues.", is_mcp=True),
        Integration("Jira", "Issue tracking & planning", "oauth", "Enterprise-grade backlog, sprint, and epic management for product/engi", is_mcp=True),
        Integration("GitHub", "Source & delivery", "oauth", "Link specs to PRs and releases, review code changes, and track shippin", is_mcp=True),
        Integration("Notion", "Docs & specs", "oauth", "Author and review PRDs, specs, and roadmaps; centralize product knowle", is_mcp=True),
        Integration("Figma", "Design", "oauth", "Review designs and prototypes tied to specs; pull design context into", is_mcp=True),
        Integration("Slack", "Communication", "oauth", "Route reviews, approvals, and launch announcements; surface notificati", is_mcp=False),
        Integration("Amplitude", "Product analytics", "api_key", "Measure feature adoption, funnels, and retention to inform what to pla", is_mcp=False),
        Integration("Intercom", "Customer feedback & support", "oauth", "Collect user feedback and support signal to prioritize the roadmap and", is_mcp=True),
        Integration("LaunchDarkly", "Feature management & release", "api_key", "Gate, roll out, and toggle features at publish/submit time; run contro", is_mcp=False),
        Integration("Productboard", "Roadmap & prioritization", "oauth", "Aggregate inputs, prioritize features, and communicate the roadmap to", is_mcp=False),
    ],
    "people": [
        Integration("Workday", "HRIS / Core HR", "oauth", "Primary system of record for employee data, org structure, and HR busi", is_mcp=False),
        Integration("BambooHR", "HRIS (SMB/mid-market)", "api_key", "Mid-market HRIS for employee records, PTO, onboarding, and reporting.", is_mcp=False),
        Integration("Greenhouse", "ATS / Recruiting", "api_key", "Applicant tracking system to manage candidate pipelines, scorecards, a", is_mcp=False),
        Integration("LinkedIn", "Sourcing / Job publishing", "oauth", "Publish job posts, source candidates, and share employer-brand content", is_mcp=False),
        Integration("Slack", "Communication / Collaboration", "oauth", "Route interview-debrief threads, approvals, and people-ops announcemen", is_mcp=True),
        Integration("Google Workspace", "Calendar / Email / Docs", "oauth", "Schedule interviews via Calendar, send candidate/offer email via Gmail", is_mcp=False),
        Integration("DocuSign", "E-signature / Offer execution", "oauth", "Send and collect signatures on offer letters, employment agreements, a", is_mcp=False),
        Integration("Gusto", "Payroll / Benefits", "oauth", "Run payroll, manage benefits enrollment, and handle new-hire onboardin", is_mcp=False),
        Integration("Lever", "ATS / CRM recruiting", "oauth", "Alternative ATS+CRM for candidate sourcing, pipeline management, and n", is_mcp=False),
        Integration("Culture Amp", "Engagement / Surveys / Performance", "api_key", "Plan and publish engagement surveys, review results, and run performan", is_mcp=False),
    ],
    "cowork": [
        Integration("Google Workspace", "Docs & Email", "oauth", "Gmail, Docs, Sheets, Calendar, and Drive for planning, drafting, sched", is_mcp=False),
        Integration("Slack", "Team Communication", "oauth", "Coordinate work, route reviews/approvals, and broadcast published upda", is_mcp=True),
        Integration("Notion", "Knowledge & Docs", "oauth", "Plan and draft operational docs, wikis, and project pages; review and", is_mcp=True),
        Integration("Linear", "Project Management", "oauth", "Plan, track, review, and ship operational work as issues/projects; off", is_mcp=True),
        Integration("GitHub", "Code & Repos", "oauth", "Plan, edit, review (PRs), and publish code and technical artifacts; of", is_mcp=True),
        Integration("HubSpot", "CRM & Marketing", "oauth", "Manage contacts, deals, and pipelines; draft, review, and publish mark", is_mcp=False),
        Integration("Stripe", "Payments & Billing", "api_key", "Create invoices, manage subscriptions, and submit/process payments to", is_mcp=True),
        Integration("Google Drive", "File Storage", "oauth", "Store, organize, and share operational files and assets across the pla", is_mcp=False),
        Integration("DocuSign", "E-Signature", "oauth", "Route contracts and agreements for review, signature, and final submis", is_mcp=False),
    ],
    "ops": [
        Integration("Slack", "Team communication & coordination", "oauth", "Coordinate operations, route approvals, and broadcast publish/submit n", is_mcp=True),
        Integration("Google Workspace (Gmail, Docs, Sheets, Drive)", "Productivity & documents", "oauth", "Author and edit SOPs, runbooks, and trackers in Docs/Sheets; share via", is_mcp=False),
        Integration("Notion", "Knowledge base & docs", "oauth", "Central ops wiki for planning, drafting SOPs/runbooks, and reviewing d", is_mcp=True),
        Integration("Linear", "Project & issue tracking", "oauth", "Plan operational work as issues/projects, assign and review, then clos", is_mcp=True),
        Integration("Asana", "Work & task management", "oauth", "Plan and assign operational tasks and approvals across teams, track re", is_mcp=False),
        Integration("Airtable", "Operational database & workflows", "oauth", "Structured operational records, inventories, and intake forms; edit ro", is_mcp=False),
        Integration("DocuSign", "E-signature & approvals", "oauth", "Route operational agreements and approvals for signature; the canonica", is_mcp=False),
        Integration("HubSpot", "CRM & ops record system", "oauth", "Operational CRM for managing customer/vendor records, pipelines, and t", is_mcp=False),
        Integration("Stripe", "Payments & billing", "api_key", "Operational billing — create/edit invoices, subscriptions, and payouts", is_mcp=True),
        Integration("GitHub", "Source & change management", "oauth", "Manage operational configs/runbooks-as-code and automation scripts; pl", is_mcp=True),
    ],
    "support": [
        Integration("Zendesk", "Help Desk / Ticketing", "oauth", "Core ticketing system to triage, draft, review, and resolve customer s", is_mcp=False),
        Integration("Intercom", "Customer Messaging", "oauth", "Live chat and conversational support inbox for messaging customers, ro", is_mcp=False),
        Integration("Freshdesk", "Help Desk / Ticketing", "api_key", "Alternative ticketing/help desk for managing support queues, canned re", is_mcp=False),
        Integration("Slack", "Team Communication", "oauth", "Internal escalation and collaboration channel for routing tough ticket", is_mcp=True),
        Integration("Linear", "Issue Tracking", "oauth", "Escalate customer bugs into engineering issues and track resolution ba", is_mcp=True),
        Integration("Jira", "Issue Tracking", "oauth", "Enterprise issue tracking for filing and following customer-reported d", is_mcp=True),
        Integration("Notion", "Knowledge Base / Docs", "oauth", "Draft, review, and publish internal runbooks and macros; maintain the", is_mcp=True),
        Integration("Zendesk Guide / Help Center", "Knowledge Base", "oauth", "Author and publish public help-center articles so customers can self-s", is_mcp=False),
        Integration("HubSpot", "CRM / Service Hub", "oauth", "Customer context (CRM) and Service Hub tickets to inform replies and l", is_mcp=False),
        Integration("Twilio", "Communications / SMS-Voice", "api_key", "Programmatic SMS and voice outreach for proactive support notification", is_mcp=False),
    ],
    "hr": [
        Integration("Workday", "HCM / Core HR", "oauth", "System of record for employee data, org structure, compensation, and t", is_mcp=False),
        Integration("BambooHR", "HRIS (SMB/Mid-market)", "api_key", "Manage employee records, onboarding, time-off, and reports for small/m", is_mcp=False),
        Integration("Greenhouse", "Applicant Tracking (ATS)", "api_key", "Run recruiting pipelines: post jobs, manage candidates, schedule inter", is_mcp=False),
        Integration("Gusto", "Payroll & Benefits", "oauth", "Run payroll, manage benefits and contractor payments; review and submi", is_mcp=False),
        Integration("DocuSign", "E-signature / Documents", "oauth", "Send and collect signed offer letters, onboarding paperwork, and polic", is_mcp=False),
        Integration("Slack", "Communication / Workflow", "oauth", "Route approvals, onboarding nudges, and HR announcements; collect revi", is_mcp=True),
        Integration("Google Workspace", "Productivity / Identity & Provisioning", "oauth", "Provision and deprovision accounts, manage calendars/email for hiring", is_mcp=False),
        Integration("LinkedIn", "Sourcing / Job Distribution", "oauth", "Publish job postings and source candidates; distribute open roles to t", is_mcp=False),
        Integration("Rippling", "HRIS + IT/Device Management", "oauth", "Unified HR, payroll, and device/app provisioning; automate full hire-t", is_mcp=False),
    ],
    "onboarding": [
        Integration("DocuSign", "E-signature & document workflow", "oauth", "Send offer letters, NDAs, policy acknowledgments, and onboarding contr", is_mcp=False),
        Integration("Workday", "HCM / HRIS", "oauth", "System of record for new-hire profiles, job/org data, and provisioning", is_mcp=False),
        Integration("BambooHR", "HRIS (SMB)", "api_key", "Manage new-hire records, onboarding task checklists, and self-service", is_mcp=False),
        Integration("Gusto", "Payroll & benefits", "oauth", "Onboard employees into payroll, collect W-4/I-9 and direct-deposit det", is_mcp=False),
        Integration("Checkr", "Background checks", "api_key", "Order and track candidate/employee background checks and screenings as", is_mcp=False),
        Integration("Slack", "Team communication", "oauth", "Notify managers/IT/teams of onboarding milestones, route approvals, an", is_mcp=True),
        Integration("Google Workspace", "Identity & productivity provisioning", "oauth", "Provision new-hire accounts, email, calendar, and Drive document colle", is_mcp=False),
        Integration("Calendly", "Scheduling", "api_key", "Schedule orientation sessions, IT setup, and manager 1:1s automaticall", is_mcp=False),
        Integration("Okta", "Identity & access management (SSO/SCIM)", "oauth", "Automate identity creation, SSO, and SCIM-based app provisioning/depro", is_mcp=False),
    ],
    "sales": [
        Integration("HubSpot", "CRM", "oauth", "Core CRM of record: manage contacts, companies, deals, and pipeline st", is_mcp=False),
        Integration("Salesforce", "CRM", "oauth", "Enterprise CRM and system of record for accounts, opportunities, and f", is_mcp=False),
        Integration("Gmail", "Email / Outreach", "oauth", "Send, draft, and track 1:1 prospect and customer email; the primary ch", is_mcp=False),
        Integration("Google Calendar", "Scheduling", "oauth", "Book and manage discovery calls, demos, and follow-up meetings; coordi", is_mcp=False),
        Integration("Slack", "Team Collaboration", "oauth", "Internal deal collaboration, approvals, and review handoffs; route dea", is_mcp=False),
        Integration("DocuSign", "E-signature / Contracts", "oauth", "Generate, send, and collect signatures on quotes and contracts; the pu", is_mcp=False),
        Integration("Stripe", "Payments / Billing", "api_key", "Create invoices, payment links, and subscriptions once a deal closes;", is_mcp=True),
        Integration("Gong", "Conversation Intelligence", "oauth", "Record and analyze sales calls for coaching and deal intelligence; rev", is_mcp=False),
        Integration("LinkedIn", "Prospecting / Social", "oauth", "Source and research prospects, run social outreach, and publish conten", is_mcp=False),
    ],
    "marketing": [
        Integration("Meta (Facebook & Instagram) Graph/Marketing API", "Social Publishing & Ads", "oauth", "Publish organic posts/Reels to Facebook & Instagram and run paid campa", is_mcp=False, connector="meta"),
        Integration("Google Ads", "Paid Advertising", "oauth", "Plan, launch, and manage Search/Display/PMax campaigns; the dominant p", is_mcp=False),
        Integration("Google Analytics 4", "Analytics & Measurement", "oauth", "Pull traffic, conversion, and attribution data to measure campaign per", is_mcp=False),
        Integration("LinkedIn Marketing API", "Social Publishing & Ads", "oauth", "Publish company-page content and run B2B sponsored campaigns — essenti", is_mcp=False),
        Integration("HubSpot", "CRM & Marketing Automation", "oauth", "Manage contacts, email marketing, landing pages, and campaign workflow", is_mcp=False),
        Integration("Mailchimp", "Email Marketing", "oauth", "Build, send, and automate email campaigns and newsletters with list se", is_mcp=False),
        Integration("Canva", "Creative & Design", "oauth", "Create and edit on-brand creative assets (social graphics, ads) via br", is_mcp=True),
        Integration("YouTube Data API", "Video Publishing", "oauth", "Upload, schedule, and manage video content and metadata on the largest", is_mcp=False),
        Integration("X (Twitter) API", "Social Publishing", "oauth", "Publish posts/threads and run promoted content for real-time audience", is_mcp=False),
        Integration("Slack", "Collaboration & Review", "oauth", "Route content for internal review/approvals and notify the team across", is_mcp=True),
    ],
    "growth": [
        Integration("HubSpot", "CRM & Marketing Automation", "oauth", "System of record for contacts, lifecycle stages, lists, email campaign", is_mcp=False),
        Integration("Google Ads", "Paid Acquisition", "oauth", "Plan, edit, review, and publish search/display/PMax campaigns; pull sp", is_mcp=False),
        Integration("Meta (Facebook/Instagram) Ads", "Paid Acquisition / Social", "oauth", "Create, edit, and publish paid social campaigns and creative across Fa", is_mcp=False, connector="meta"),
        Integration("Google Analytics 4", "Analytics & Measurement", "oauth", "Measure traffic, funnels, conversions, and attribution to inform plann", is_mcp=False),
        Integration("LinkedIn", "Social Publishing / B2B", "oauth", "Publish organic posts and run/edit B2B ad campaigns via the LinkedIn M", is_mcp=False),
        Integration("Mailchimp", "Email Marketing", "oauth", "Draft, edit, review, and send email campaigns and automations; manage", is_mcp=False),
        Integration("Google Search Console", "SEO / Organic", "oauth", "Review organic search queries, impressions, rankings, and indexing hea", is_mcp=False),
        Integration("Stripe", "Revenue & Billing", "api_key", "Pull revenue, subscription, and conversion data to tie growth activity", is_mcp=True),
        Integration("Slack", "Collaboration & Review", "oauth", "Route campaign drafts, approvals, and performance alerts to the team;", is_mcp=True),
        Integration("X (Twitter)", "Social Publishing", "oauth", "Publish and schedule organic posts and run promoted campaigns via the", is_mcp=False),
    ],
    "code": [
        Integration("GitHub", "Source control & collaboration", "oauth", "Core repo hosting: read/write code, open and review pull requests, man", is_mcp=True),
        Integration("GitLab", "Source control & CI/CD", "oauth", "Alternative repo + integrated CI/CD platform for teams not on GitHub.", is_mcp=True),
        Integration("Linear", "Issue tracking & planning", "oauth", "Plan and track work: create issues, manage cycles/projects, and link t", is_mcp=True),
        Integration("Jira", "Issue tracking & planning", "oauth", "Enterprise issue tracking and sprint planning widely used by engineeri", is_mcp=True),
        Integration("Sentry", "Error monitoring & observability", "oauth", "Catch and triage production errors and performance regressions during", is_mcp=True),
        Integration("Vercel", "Deployment & hosting", "oauth", "Ship and preview frontend/full-stack apps: deploy, inspect builds, and", is_mcp=True),
        Integration("Slack", "Team communication", "oauth", "Notify reviewers, route deploy/CI alerts, and coordinate handoffs acro", is_mcp=True),
        Integration("Stripe", "Payments / backend services", "api_key", "Common backend dependency operators build and test against: manage pro", is_mcp=True),
        Integration("Cloudflare", "Edge infrastructure & DNS", "oauth", "Deploy Workers/Pages, manage DNS, caching, and edge config as part of", is_mcp=True),
        Integration("PostgreSQL", "Database", "none", "Query and inspect the application database during build and review. Co", is_mcp=True),
    ],
    "nx-code": [
        Integration("GitHub", "Source Control & Code Review", "oauth", "Host repos, branches, pull requests, issues, and CI checks. Core of th", is_mcp=True),
        Integration("GitLab", "Source Control & Code Review", "oauth", "Alternative/self-hosted source control with merge requests and built-i", is_mcp=True),
        Integration("Linear", "Project & Issue Planning", "oauth", "Plan and track work — issues, cycles, projects — that maps directly to", is_mcp=True),
        Integration("Jira", "Project & Issue Planning", "oauth", "Enterprise issue tracking and sprint planning that feeds the edit/revi", is_mcp=True),
        Integration("Sentry", "Error Monitoring & Review", "oauth", "Capture production errors and performance issues to triage before and", is_mcp=True),
        Integration("Vercel", "Deploy & Publish", "oauth", "Build, preview, and deploy/publish web apps. Official Vercel MCP serve", is_mcp=True),
        Integration("Slack", "Communication & Review Notifications", "oauth", "Team coordination, PR/deploy notifications, and review approvals in-ch", is_mcp=True),
        Integration("Stripe", "Payments & Billing", "api_key", "Wire up and operate billing/payments in shipped products. Stripe's pri", is_mcp=True),
        Integration("OpenAI", "AI & Code Generation", "api_key", "LLM/codegen and embeddings used during planning and editing. Primary a", is_mcp=False),
        Integration("Cloudflare", "Infrastructure & Edge Deploy", "api_key", "DNS, CDN, Workers, and edge deploys for publishing and operating apps.", is_mcp=True),
    ],
    "devops": [
        Integration("GitHub", "Source Control & CI/CD", "oauth", "Plan and review code: repos, branches, pull requests, issues, code rev", is_mcp=True),
        Integration("GitLab", "Source Control & CI/CD", "oauth", "Alternative source platform: repos, merge requests, and integrated Git", is_mcp=True),
        Integration("Jira", "Issue & Project Tracking", "oauth", "Plan and track work: issues, sprints, and release planning that drive", is_mcp=True),
        Integration("PagerDuty", "Incident Management", "oauth", "On-call scheduling, alert routing, and incident response. Review/opera", is_mcp=False),
        Integration("Datadog", "Observability & Monitoring", "api_key", "Metrics, logs, traces, and dashboards to review system health pre- and", is_mcp=False),
        Integration("Sentry", "Error Monitoring", "oauth", "Error and performance tracking to catch regressions after publishing/d", is_mcp=True),
        Integration("Vercel", "Deploy & Hosting", "oauth", "Publish/submit stage: deploy applications, manage projects, inspect bu", is_mcp=True),
        Integration("Docker Hub", "Container Registry", "api_key", "Build, store, and pull container images that flow through CI into depl", is_mcp=False),
        Integration("AWS", "Cloud Infrastructure", "api_key", "Provision and operate infrastructure where deploys land: compute, stor", is_mcp=True),
        Integration("Slack", "Team Communication & ChatOps", "oauth", "Deploy notifications, approvals, and incident war-rooms — the human-in", is_mcp=True),
    ],
    "nx-1": [
        Integration("Slack", "Team communication & coordination", "oauth", "Central operations hub: route updates, request approvals, run review t", is_mcp=True),
        Integration("Google Workspace (Gmail, Drive, Docs, Calendar)", "Productivity & documents", "oauth", "Draft and store plans/docs, manage email, and schedule across the org", is_mcp=False),
        Integration("Notion", "Knowledge base & planning", "oauth", "Plan, document, and review work in a structured workspace; maintain in", is_mcp=True),
        Integration("Linear", "Project & issue tracking", "oauth", "Turn plans into tracked issues/projects, review status, and submit wor", is_mcp=True),
        Integration("GitHub", "Code & version control", "oauth", "Manage repos, open and review pull requests, and ship code/devops chan", is_mcp=True),
        Integration("HubSpot", "CRM & marketing/sales ops", "oauth", "Manage contacts, deals, and pipeline; plan and publish marketing/sales", is_mcp=True),
        Integration("Stripe", "Payments & billing", "api_key", "Read revenue, manage subscriptions/invoices, and submit billing operat", is_mcp=True),
        Integration("Meta (Facebook & Instagram) Marketing", "Paid & social publishing", "oauth", "Plan, create, review, and publish ad campaigns and social content for", is_mcp=False, connector="meta"),
        Integration("Google Ads", "Paid acquisition", "oauth", "Build, review, and launch search/display campaigns — a primary publish", is_mcp=False),
        Integration("LinkedIn", "Professional publishing & recruiting", "oauth", "Publish company/brand content and support recruiting outreach across t", is_mcp=False),
    ],
    "agents": [
        Integration("OpenAI", "Model provider", "api_key", "Core LLM/reasoning, function-calling, and embeddings backbone for buil", is_mcp=False),
        Integration("Anthropic", "Model provider", "api_key", "Claude models for agent reasoning, tool use, and long-context planning", is_mcp=False),
        Integration("GitHub", "Source control / CI", "oauth", "Stores agent code, opens and reviews PRs, and triggers CI — the edit a", is_mcp=True),
        Integration("Linear", "Project management", "oauth", "Plans and tracks agent work as issues/projects and routes review check", is_mcp=True),
        Integration("Vercel", "Deployment / hosting", "oauth", "Ships and hosts agent apps, APIs, and AI Gateway endpoints — the publi", is_mcp=True),
        Integration("Cloudflare", "Edge infra / deployment", "oauth", "Runs agents on Workers, plus Durable Objects/KV/queues for agent state", is_mcp=True),
        Integration("Sentry", "Observability / error tracking", "oauth", "Monitors agent runs, captures errors and traces, and surfaces regressi", is_mcp=True),
        Integration("Hugging Face", "Models / datasets hub", "api_key", "Sources open models, datasets, and Spaces for agent capabilities and e", is_mcp=True),
        Integration("Stripe", "Payments / billing", "api_key", "Monetizes and meters agent usage, handles billing and payouts at the s", is_mcp=True),
    ],
    "recruiting": [
        Integration("LinkedIn", "Sourcing & Job Distribution", "oauth", "Source candidates, post jobs, and publish/share roles to the largest p", is_mcp=False),
        Integration("Greenhouse", "Applicant Tracking System", "api_key", "System of record for the hiring pipeline: manage requisitions, candida", is_mcp=False),
        Integration("Indeed", "Job Distribution", "oauth", "Publish and sponsor job postings to the largest job board to drive app", is_mcp=False),
        Integration("Calendly", "Interview Scheduling", "oauth", "Automate interview scheduling and self-booking with candidates and hir", is_mcp=False),
        Integration("Google Workspace (Gmail & Calendar)", "Communication & Scheduling", "oauth", "Send candidate outreach/offer emails and manage interview calendar inv", is_mcp=False),
        Integration("DocuSign", "Offer & Document Signing", "oauth", "Send and collect e-signatures on offer letters and employment agreemen", is_mcp=False),
        Integration("Checkr", "Background Checks", "api_key", "Run pre-hire background and reference screening before final submit/on", is_mcp=False),
        Integration("Slack", "Internal Collaboration & Review", "oauth", "Coordinate hiring-team debriefs, route candidate reviews and approvals", is_mcp=True),
    ],
    "knowledge": [
        Integration("Notion", "Knowledge base / docs", "oauth", "Primary workspace for planning, drafting, and structuring knowledge —", is_mcp=True),
        Integration("Google Drive", "File storage / docs", "oauth", "Store, organize, and share source documents and exports; Google Docs/S", is_mcp=False),
        Integration("Confluence", "Knowledge base / wiki", "oauth", "Enterprise team wiki for publishing reviewed documentation; Atlassian", is_mcp=True),
        Integration("Slack", "Communication / review", "oauth", "Route drafts for review, collect approvals, and notify stakeholders; c", is_mcp=True),
        Integration("GitHub", "Version control / docs-as-code", "oauth", "Version, review (PRs), and publish docs-as-code and knowledge repos; o", is_mcp=True),
        Integration("Linear", "Planning / issue tracking", "oauth", "Plan and track knowledge work as issues and projects; official Linear", is_mcp=True),
        Integration("OpenAI", "AI / generation", "api_key", "Draft, summarize, and edit knowledge content; embeddings for semantic", is_mcp=False),
        Integration("Algolia", "Search", "api_key", "Index and serve fast search over published knowledge content for end u", is_mcp=False),
        Integration("Zendesk", "Help center / publishing", "oauth", "Publish and maintain customer-facing knowledge base / help center arti", is_mcp=False),
    ],
    "brand": [
        Integration("Figma", "Design / asset creation", "oauth", "Plan and edit brand assets, logos, and design files; design source-of-", is_mcp=True),
        Integration("Adobe Express", "Design / asset creation", "oauth", "Generate and edit on-brand graphics, social posts, and templates from", is_mcp=True),
        Integration("Canva", "Design / asset creation", "oauth", "Template-driven brand creative production and brand-kit-consistent des", is_mcp=True),
        Integration("Slack", "Review / collaboration", "oauth", "Route brand creative for internal review, approvals, and stakeholder s", is_mcp=True),
        Integration("Google Drive", "Asset storage / DAM", "oauth", "Store, version, and share brand assets, guidelines, and approved creat", is_mcp=False),
        Integration("Meta (Facebook/Instagram)", "Publishing / channel", "oauth", "Publish approved brand content and campaigns to Facebook and Instagram", is_mcp=False, connector="meta"),
        Integration("LinkedIn", "Publishing / channel", "oauth", "Publish brand and thought-leadership content to company pages.", is_mcp=False),
        Integration("YouTube", "Publishing / channel", "oauth", "Publish and manage brand video content and channel uploads.", is_mcp=False),
        Integration("HubSpot", "Marketing / CRM", "oauth", "Manage brand email/landing-page campaigns and track audience engagemen", is_mcp=True),
    ],
    "customers": [
        Integration("HubSpot", "CRM", "oauth", "Core CRM of record: manage contacts, companies, deals, and lifecycle s", is_mcp=False),
        Integration("Salesforce", "CRM", "oauth", "Enterprise CRM for accounts, opportunities, and pipeline; review and u", is_mcp=False),
        Integration("Zendesk", "Customer Support", "oauth", "Ticketing and support desk: triage, draft, review, and publish replies", is_mcp=False),
        Integration("Intercom", "Customer Messaging", "oauth", "In-product messaging and live chat: manage conversations, plan campaig", is_mcp=False),
        Integration("Stripe", "Payments & Billing", "api_key", "Billing and subscription source of truth: review customer payment stat", is_mcp=True),
        Integration("Slack", "Team Communication", "oauth", "Internal collaboration and review: route customer escalations, gather", is_mcp=False),
        Integration("Gmail", "Email", "oauth", "Direct customer email: draft, review, and send 1:1 customer correspond", is_mcp=False),
        Integration("Twilio", "Communications API", "api_key", "SMS and voice outreach to customers: send transactional and lifecycle", is_mcp=False),
        Integration("Mailchimp", "Email Marketing", "oauth", "Customer lifecycle email campaigns: plan, edit, review, and publish br", is_mcp=False),
    ],
    "leads": [
        Integration("HubSpot", "CRM", "oauth", "Core lead CRM: capture, store, segment, and manage lead lifecycle/pipe", is_mcp=False),
        Integration("Salesforce", "CRM", "oauth", "Enterprise CRM alternative for lead/opportunity management, routing, a", is_mcp=False),
        Integration("Meta (Facebook/Instagram) Lead Ads", "Paid Acquisition", "oauth", "Publish lead-gen ad campaigns and pull instant-form leads from Faceboo", is_mcp=False, connector="meta"),
        Integration("Google Ads", "Paid Acquisition", "oauth", "Run search/PMax lead-gen campaigns and sync lead-form submissions for", is_mcp=False),
        Integration("LinkedIn Marketing (Lead Gen Forms)", "Paid Acquisition / B2B", "oauth", "Publish B2B Lead Gen Form campaigns and retrieve high-intent professio", is_mcp=False),
        Integration("Calendly", "Scheduling", "oauth", "Convert qualified leads into booked meetings; trigger handoff to sales", is_mcp=False),
        Integration("SendGrid", "Email Outreach", "api_key", "Transactional and outbound nurture email delivery to leads at scale wi", is_mcp=False),
        Integration("Twilio", "SMS / Voice Outreach", "api_key", "SMS and voice follow-up to leads for speed-to-lead and multi-touch out", is_mcp=False),
        Integration("Clearbit", "Lead Enrichment", "api_key", "Enrich raw leads with firmographic/contact data to score, qualify, and", is_mcp=False),
        Integration("Slack", "Notifications / Review", "oauth", "Real-time lead alerts, routing notifications, and human review/approva", is_mcp=True),
    ],
}

# Built OAuth connectors (from nx_channels) — the "ready" tier.
BUILT_CONNECTORS = {"meta", "google", "x", "linkedin", "tiktok", "pinterest", "snapchat"}

# Map the many ways an operator names a platform → its built connector, so
# "youtube" / "google ads" both resolve to the google connector, etc. Checked
# as substring matches (longest-intent first).
CONNECTOR_ALIASES = [
    ("instagram", "meta"), ("facebook", "meta"), ("meta", "meta"),
    ("google ads", "google"), ("youtube", "google"), ("google", "google"),
    ("twitter", "x"), ("x (twitter)", "x"),
    ("linkedin", "linkedin"),
    ("tiktok", "tiktok"),
    ("pinterest", "pinterest"),
    ("snapchat", "snapchat"),
]


def _connector_for(name: str) -> str:
    """Return the built-connector name a platform maps to, or ''."""
    key = (name or "").strip().lower()
    if not key:
        return ""
    for alias, conn in CONNECTOR_ALIASES:
        if alias in key or key in alias:
            return conn if conn in BUILT_CONNECTORS else ""
    return ""


def directory_for(world: str):
    return WORLD_INTEGRATIONS.get((world or "").lower(), [])


def _all_known():
    seen = {}
    for world, items in WORLD_INTEGRATIONS.items():
        for it in items:
            seen.setdefault(it.name.lower(), (world, it))
    return seen


def find_in_directory(name: str):
    """Return (world, Integration) if the name is curated, else None."""
    if not name:
        return None
    key = name.strip().lower()
    known = _all_known()
    if key in known:
        return known[key]
    # loose contains-match so "facebook"/"insta" resolve to the Meta entry
    for k, (world, it) in known.items():
        if key in k or key in it.name.lower():
            return (world, it)
    return None


# ── RESOLVER ───────────────────────────────────────────────────────────────--
def resolve(name, world=None, mcp_lookup=None, web_search_available=True):
    """The integration ladder. Returns a PLAN dict — never installs/connects.

    mcp_lookup(name) -> truthy registry entry or None (injected so it's testable
    and so the heavy MCP registry import stays lazy).
    """
    plan = {
        "name": name,
        "status": None,          # ready | directory | mcp_registry | discoverable | bring_your_own
        "auth": None,
        "connector": "",
        "requires_approval": False,
        "steps": [],
        "message": "",
    }
    if not name or not name.strip():
        plan["status"] = "bring_your_own"
        plan["message"] = "Name an integration and I'll find or install it."
        return plan

    # Fast path: a built OAuth connector exists for this platform — ready now.
    conn = _connector_for(name)
    if conn:
        plan["status"] = "ready"
        plan["auth"] = "oauth"
        plan["connector"] = conn
        plan["steps"] = [f"/publish connect {conn}"]
        plan["message"] = f"{name} has a built connector — connect with /publish connect {conn}."
        return plan

    hit = find_in_directory(name)
    if hit:
        _world, it = hit
        plan["auth"] = it.auth
        plan["connector"] = it.connector
        if it.connector and it.connector in BUILT_CONNECTORS:
            # A built OAuth connector exists — ready to connect right now.
            plan["status"] = "ready"
            plan["requires_approval"] = False
            plan["steps"] = [f"/publish connect {it.connector}"]
            plan["message"] = f"{it.name} has a built connector — connect with /publish connect {it.connector}."
        else:
            plan["status"] = "directory"
            if it.auth == "oauth":
                plan["steps"] = [f"authorize {it.name} (OAuth, browser login)"]
                plan["requires_approval"] = True
            elif it.auth == "api_key":
                plan["steps"] = [f"add your {it.name} API key (stored in Keychain)"]
                plan["requires_approval"] = True
            elif it.auth == "mcp":
                plan["steps"] = [f"install the {it.name} MCP server", "complete its login"]
                plan["requires_approval"] = True
            else:
                plan["steps"] = [f"use {it.name} (no auth needed)"]
            plan["message"] = f"{it.name} is in the {_world} directory ({it.auth})."
        return plan

    # Not in the curated directory — but a REAL OAuth/tenant connector may still
    # exist for this name (Discord, Zoom, Snowflake, Zendesk, …). Prefer the
    # provider's actual login over the MCP hub. (api-key fallbacks don't match —
    # GenericApiKeyConnector is not a GenericOAuthConnector.)
    try:
        import nx_channels as _ch
        _c = _ch.connector_for_service(name, "oauth")
        if isinstance(_c, _ch.GenericOAuthConnector):
            tenant = isinstance(_c, getattr(_ch, "TenantOAuthConnector", ()))
            plan["status"] = "directory"
            plan["auth"] = "oauth"
            plan["requires_approval"] = True
            plan["steps"] = [
                (f"set your {_c.tenant_label} + app creds: /integrations {name} setup"
                 if tenant else f"authorize {name} (OAuth, browser login)")
            ]
            plan["message"] = f"{name} connects via real OAuth login."
            return plan
    except Exception:
        pass

    # Not curated — is there a known MCP server?
    if mcp_lookup is None:
        mcp_lookup = _default_mcp_lookup
    try:
        entry = mcp_lookup(name)
    except Exception:
        entry = None
    if entry:
        plan["status"] = "mcp_registry"
        plan["auth"] = "mcp"
        plan["mcp_slug"] = entry.get("slug") if isinstance(entry, dict) else ""
        plan["requires_approval"] = True
        plan["steps"] = [
            f"install the {name} MCP server (approval required)",
            "guide you through its login",
            "then NX can use its tools",
        ]
        plan["message"] = f"{name} isn't curated but a connector exists in the registry. Install it?"
        return plan

    # Not in any registry — NX can search the web for an installable server.
    if web_search_available:
        plan["status"] = "discoverable"
        plan["auth"] = "mcp"
        plan["requires_approval"] = True
        plan["steps"] = [
            f"web-search for an MCP server / install for {name}",
            "show you what it found (approval required before install)",
            "install it, then guide login",
            "then NX runs it end-to-end",
        ]
        plan["message"] = f"No built connector for {name}. I can search for one and install it with your OK."
        return plan

    # Nothing automated — bring your own (still fully usable once added).
    plan["status"] = "bring_your_own"
    plan["auth"] = "mcp"
    plan["steps"] = [
        f"install/bring an MCP server for {name}",
        "point NX at it (command or URL)",
        "NX stays signed in and continues from there",
    ]
    plan["message"] = f"Bring your own {name} (MCP) — same as adding a server to Claude Code. NX continues once it's there."
    return plan


def _default_mcp_lookup(name):
    """Lazy lookup against the live MCP registry; safe if unavailable."""
    try:
        import nx_mcp_hub as _hub
        reg = getattr(_hub, "MCP_REGISTRY", None) or {}
        key = name.strip().lower()
        for slug, meta in reg.items():
            label = (meta.get("name") or slug or "").lower()
            if key == slug.lower() or key in label or label in key:
                return {"slug": slug, "meta": meta}
    except Exception:
        pass
    return None


# ── presentation + execution (canonical NX palette) ─────────────────────────
_G = "\033[38;2;200;164;74m"
_GD = "\033[38;2;196;162;88m"
_W = "\033[38;2;224;221;212m"
_D = "\033[38;2;172;166;148m"
_DR = "\033[38;2;146;140;122m"
_GN = "\033[38;2;80;200;100m"
_R = "\033[0m"

_AUTH_GLYPH = {"oauth": "↗", "api_key": "⚿", "mcp": "⬡", "none": "·"}


def render_directory(world: str, width: int = 0) -> str:
    items = directory_for(world)
    if not items:
        return (f"\n  {_G}✦  Integrations{_R}   {_DR}no curated set for '{world}' yet — "
                f"name any tool and I'll resolve it{_R}\n")
    # Responsive: wide terminals get name + category + status columns; narrow
    # split-panes drop the category (it was overflowing + wrapping) and tighten
    # the name column so a row always fits on one line.
    if not width:
        try:
            import shutil
            width = shutil.get_terminal_size().columns
        except Exception:
            width = 80
    narrow = width < 72
    if narrow:
        out = [f"\n  {_G}✦  {world}{_R}  {_DR}· {len(items)} ready{_R}\n"]
    else:
        out = [f"\n  {_G}✦  {world} integrations{_R}   {_DR}{len(items)} ready · "
               f"or name any tool to add{_R}\n"]
    namew = 20 if narrow else 30
    for it in items:
        conn = _connector_for(it.name)
        tier = f"{_GN}● ready{_R}" if conn else f"{_DR}{_AUTH_GLYPH.get(it.auth,'·')} {it.auth}{_R}"
        name = it.name if len(it.name) <= namew else it.name[: namew - 1] + "…"
        if narrow:
            out.append(f"  {_GD}{name:<{namew}}{_R}  {tier}")
        else:
            out.append(f"  {_GD}{name:<{namew}}{_R} {_DR}{it.category[:20]:<20}{_R}  {tier}")
    out.append(f"\n  {_DR}connect: /integrations <name>{_R}\n")
    return "\n".join(out)


def render_plan(plan: dict) -> str:
    name = plan.get("name", "")
    st = plan.get("status")
    head = {
        "ready":         f"{_GN}● {name} — ready to connect{_R}",
        "directory":     f"{_GD}◐ {name} — in the directory ({plan.get('auth')}){_R}",
        "mcp_registry":  f"{_GD}⬡ {name} — connector available to install{_R}",
        "discoverable":  f"{_GD}⌕ {name} — not built-in; NX can find + install it{_R}",
        "bring_your_own":f"{_D}＋ {name} — bring your own (NX continues once it's added){_R}",
    }.get(st, f"{_D}{name}{_R}")
    out = [f"\n  {head}", f"  {_DR}{plan.get('message','')}{_R}", ""]
    for i, step in enumerate(plan.get("steps", []), 1):
        gate = f"  {_GD}(approval){_R}" if plan.get("requires_approval") else ""
        out.append(f"  {_DR}{i}.{_R} {_D}{step}{_R}{gate}")
    out.append("")
    return "\n".join(out)


def merge_directory(generated: dict):
    """Fold generated per-world directory data into WORLD_INTEGRATIONS without
    clobbering entries that carry a built connector. `generated` is
    {world: [{name, category, auth, is_mcp, use}, ...]}."""
    for world, items in (generated or {}).items():
        existing = {i.name.lower(): i for i in WORLD_INTEGRATIONS.get(world, [])}
        merged = list(WORLD_INTEGRATIONS.get(world, []))
        for it in items or []:
            nm = (it.get("name") or "").strip()
            if not nm or nm.lower() in existing:
                continue
            merged.append(Integration(
                name=nm,
                category=it.get("category", ""),
                auth=it.get("auth", "mcp"),
                use=it.get("use", ""),
                is_mcp=bool(it.get("is_mcp")),
            ))
        WORLD_INTEGRATIONS[world] = merged
