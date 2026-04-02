"""Buyer persona cards — embedded marketing knowledge base.

22 pre-built buyer personas ported from the original AI in Charge KB.
Each persona has pain points, KPIs, buying triggers, messaging angles,
and value drivers. Used to enrich prospect_analyzer.py output when
a prospect's role matches a known persona.

Usage:
    from .persona_cards import find_matching_persona
    persona = find_matching_persona("VP of Sales")
    if persona:
        pain_points = persona["pain_points"]
"""

from __future__ import annotations

import re

# ──────────────────────────────────────────────
# 22 Buyer Personas
# ──────────────────────────────────────────────

PERSONA_CARDS: list[dict] = [
    {
        "role": "CFO",
        "aliases": ["chief financial officer", "finance director", "vp finance", "head of finance"],
        "pain_points": [
            "Forecasting risk and cash flow uncertainty",
            "Manual reporting processes consuming team bandwidth",
            "Lack of real-time visibility into spend and pipeline",
            "Difficulty proving ROI on technology investments",
            "Compliance and audit preparation overhead",
        ],
        "kpis": ["revenue growth", "gross margin", "burn rate", "CAC payback", "operating expenses"],
        "triggers": ["budget cycles", "board meetings", "new fiscal year", "M&A activity", "IPO prep"],
        "messaging_angles": [
            "Quantify time saved in reporting cycles",
            "Frame as risk reduction, not just cost cutting",
            "Lead with payback period and ROI metrics",
            "Reference audit-readiness and compliance benefits",
        ],
        "value_drivers": ["cost reduction", "risk mitigation", "operational efficiency"],
    },
    {
        "role": "CRO",
        "aliases": ["chief revenue officer", "vp revenue", "head of revenue"],
        "pain_points": [
            "Pipeline velocity too slow to hit targets",
            "Misalignment between sales and marketing on lead quality",
            "Rep ramp time and productivity gaps",
            "Forecast accuracy undermining board confidence",
            "Customer churn eroding expansion revenue",
        ],
        "kpis": ["ARR/MRR growth", "pipeline coverage ratio", "win rate", "sales cycle length", "NRR"],
        "triggers": ["missed quarter", "new territory expansion", "sales team restructure", "competitor wins"],
        "messaging_angles": [
            "Show pipeline acceleration metrics from similar companies",
            "Frame as revenue assurance, not just tooling",
            "Lead with forecast accuracy improvements",
            "Reference competitive displacement stories",
        ],
        "value_drivers": ["revenue acceleration", "forecast accuracy", "rep productivity"],
    },
    {
        "role": "CMO",
        "aliases": ["chief marketing officer", "vp marketing", "head of marketing", "marketing director"],
        "pain_points": [
            "Proving marketing's contribution to pipeline and revenue",
            "Content production not keeping pace with demand",
            "Lead quality disputes with sales team",
            "Attribution across multi-touch journeys",
            "Brand awareness not translating to demand",
        ],
        "kpis": ["MQLs/SQLs", "pipeline contribution", "CAC", "brand awareness", "content engagement"],
        "triggers": ["rebrand", "new product launch", "demand gen overhaul", "agency review"],
        "messaging_angles": [
            "Lead with pipeline attribution clarity",
            "Frame as marketing-sales alignment tool",
            "Show content ROI measurement capabilities",
            "Reference demand gen acceleration stories",
        ],
        "value_drivers": ["pipeline attribution", "demand generation", "brand-to-revenue connection"],
    },
    {
        "role": "CTO",
        "aliases": ["chief technology officer", "vp engineering", "head of engineering", "engineering director"],
        "pain_points": [
            "Technical debt slowing feature delivery",
            "Hiring and retaining engineering talent",
            "Security and compliance requirements growing",
            "Integration complexity across tool sprawl",
            "Balancing innovation with reliability",
        ],
        "kpis": ["deployment frequency", "MTTR", "engineering velocity", "system uptime", "security posture"],
        "triggers": ["major incident", "scale-up hiring", "technology migration", "compliance audit"],
        "messaging_angles": [
            "Lead with developer experience and productivity gains",
            "Frame as tech debt reduction enabler",
            "Show integration simplicity and API-first approach",
            "Reference security and compliance benefits",
        ],
        "value_drivers": ["developer productivity", "system reliability", "security posture"],
    },
    {
        "role": "CEO/Founder",
        "aliases": ["ceo", "founder", "co-founder", "managing director", "president", "general manager"],
        "pain_points": [
            "Growth stalling after initial traction",
            "Difficulty scaling processes that worked at smaller size",
            "Board pressure on metrics and milestones",
            "Talent acquisition and retention in competitive market",
            "Cash runway management and fundraising timing",
        ],
        "kpis": ["revenue growth rate", "runway months", "team size growth", "market share", "customer count"],
        "triggers": ["fundraising round", "board meeting", "competitor funding", "key hire departure"],
        "messaging_angles": [
            "Frame as growth unlock, not just efficiency",
            "Lead with founder-to-founder credibility",
            "Show how similar-stage companies scaled past the same bottleneck",
            "Keep concise — founders are time-poor",
        ],
        "value_drivers": ["growth acceleration", "operational scale", "competitive advantage"],
    },
    {
        "role": "VP Sales",
        "aliases": ["vp of sales", "head of sales", "sales director", "director of sales"],
        "pain_points": [
            "Reps spending too much time on non-selling activities",
            "Pipeline generation falling behind targets",
            "New rep ramp time too long",
            "Inconsistent messaging across the team",
            "CRM data quality issues undermining forecasting",
        ],
        "kpis": ["quota attainment", "pipeline generation", "average deal size", "ramp time", "activity metrics"],
        "triggers": ["new quota cycle", "team expansion", "CRM migration", "missed targets"],
        "messaging_angles": [
            "Lead with time-back-to-selling metrics",
            "Show ramp time reduction for new reps",
            "Frame as pipeline generation multiplier",
            "Reference messaging consistency benefits",
        ],
        "value_drivers": ["rep productivity", "pipeline generation", "quota attainment"],
    },
    {
        "role": "COO/Head of Ops",
        "aliases": ["coo", "chief operating officer", "vp operations", "head of operations", "director of operations"],
        "pain_points": [
            "Process bottlenecks slowing cross-team execution",
            "Lack of visibility into operational metrics",
            "Manual handoffs between departments causing delays",
            "Scaling operations without proportional headcount growth",
            "Vendor management and contract sprawl",
        ],
        "kpis": ["process cycle time", "operational cost ratio", "employee productivity", "SLA compliance"],
        "triggers": ["organizational restructure", "process audit", "scaling challenges", "cost reduction mandate"],
        "messaging_angles": [
            "Lead with process automation and cycle time reduction",
            "Frame as operational visibility tool",
            "Show headcount-to-output ratio improvements",
            "Reference cross-department coordination benefits",
        ],
        "value_drivers": ["operational efficiency", "process visibility", "scalable operations"],
    },
    {
        "role": "SDR/BDR",
        "aliases": ["sdr", "bdr", "sales development representative", "business development representative"],
        "pain_points": [
            "Low response rates on outreach",
            "Spending too much time researching prospects",
            "Difficulty getting past gatekeepers",
            "Email deliverability issues",
            "Quota pressure with limited tools",
        ],
        "kpis": ["meetings booked", "response rate", "emails sent", "calls made", "conversion rate"],
        "triggers": ["new territory assignment", "tool evaluation", "low performance review"],
        "messaging_angles": [
            "Lead with response rate improvements",
            "Show time saved on research and personalization",
            "Frame as career advancement enabler (hit quota, get promoted)",
            "Reference peer success stories at similar companies",
        ],
        "value_drivers": ["response rates", "time savings", "quota achievement"],
    },
    {
        "role": "RevOps",
        "aliases": ["revenue operations", "revops manager", "head of revops", "director of revenue operations"],
        "pain_points": [
            "Data silos between sales, marketing, and CS systems",
            "Forecasting inaccuracy due to dirty pipeline data",
            "Manual reporting consuming analyst bandwidth",
            "Tech stack sprawl and integration maintenance",
            "Process inconsistency across go-to-market teams",
        ],
        "kpis": ["forecast accuracy", "data quality score", "tech stack ROI", "process adoption rate"],
        "triggers": ["CRM migration", "data quality initiative", "GTM alignment project", "new leadership"],
        "messaging_angles": [
            "Lead with data unification and single source of truth",
            "Frame as forecast accuracy enabler",
            "Show integration simplicity and maintenance reduction",
            "Reference GTM alignment success stories",
        ],
        "value_drivers": ["data quality", "forecast accuracy", "GTM alignment"],
    },
    {
        "role": "CHRO",
        "aliases": ["chief human resources officer", "vp hr", "head of hr", "vp people", "head of people", "people director"],
        "pain_points": [
            "Talent acquisition in competitive markets",
            "Employee retention and engagement decline",
            "DEI initiative measurement and accountability",
            "Compliance across multiple jurisdictions",
            "Remote/hybrid work policy management",
        ],
        "kpis": ["time to hire", "retention rate", "employee NPS", "DEI metrics", "compliance score"],
        "triggers": ["rapid hiring phase", "high attrition period", "policy overhaul", "new market entry"],
        "messaging_angles": [
            "Lead with hiring velocity and quality metrics",
            "Frame as retention and engagement tool",
            "Show compliance automation benefits",
            "Reference culture-building at scale",
        ],
        "value_drivers": ["talent acquisition speed", "employee retention", "compliance automation"],
    },
    {
        "role": "Product Manager",
        "aliases": ["pm", "product manager", "senior product manager", "head of product", "vp product", "director of product"],
        "pain_points": [
            "Prioritization across competing stakeholder demands",
            "Limited customer insight for roadmap decisions",
            "Feature bloat vs. core product focus",
            "Cross-team coordination for launches",
            "Measuring feature impact post-release",
        ],
        "kpis": ["feature adoption", "NPS", "time to value", "roadmap delivery rate", "customer feedback score"],
        "triggers": ["product launch", "customer churn spike", "competitive feature gap", "strategic pivot"],
        "messaging_angles": [
            "Lead with customer insight and feedback loop benefits",
            "Frame as prioritization clarity tool",
            "Show feature impact measurement capabilities",
            "Reference successful launches at similar companies",
        ],
        "value_drivers": ["customer insight", "roadmap clarity", "feature impact measurement"],
    },
    {
        "role": "IT Director",
        "aliases": ["it director", "it manager", "head of it", "vp it", "director of information technology"],
        "pain_points": [
            "Shadow IT and ungoverned SaaS sprawl",
            "Security incidents and vulnerability management",
            "Help desk ticket volume and resolution time",
            "Budget constraints vs. modernization demands",
            "Vendor lock-in and migration complexity",
        ],
        "kpis": ["uptime", "ticket resolution time", "security incidents", "SaaS spend", "compliance score"],
        "triggers": ["security incident", "budget review", "audit finding", "digital transformation initiative"],
        "messaging_angles": [
            "Lead with security and governance benefits",
            "Frame as SaaS spend optimization",
            "Show simplified vendor management",
            "Reference migration and integration ease",
        ],
        "value_drivers": ["security posture", "cost optimization", "governance"],
    },
    {
        "role": "Customer Success",
        "aliases": ["cs manager", "customer success manager", "head of customer success", "vp customer success", "director of customer success"],
        "pain_points": [
            "Churn signals detected too late to intervene",
            "Onboarding bottleneck delaying time to value",
            "Manual health scoring unreliable at scale",
            "Expansion revenue targets with limited resources",
            "Cross-functional coordination for at-risk accounts",
        ],
        "kpis": ["NRR", "churn rate", "time to value", "CSAT", "expansion revenue"],
        "triggers": ["churn spike", "renewal season", "team scaling", "CS platform evaluation"],
        "messaging_angles": [
            "Lead with early churn detection capabilities",
            "Frame as time-to-value accelerator",
            "Show health scoring automation benefits",
            "Reference expansion revenue success stories",
        ],
        "value_drivers": ["churn prevention", "expansion revenue", "customer satisfaction"],
    },
    {
        "role": "Data/Analytics Lead",
        "aliases": ["data analyst", "data scientist", "head of analytics", "analytics manager", "bi manager", "data engineer"],
        "pain_points": [
            "Data pipeline reliability and freshness issues",
            "Ad-hoc report requests consuming team bandwidth",
            "Data quality and governance across sources",
            "Self-service analytics adoption lagging",
            "Scaling data infrastructure for growing data volumes",
        ],
        "kpis": ["data freshness", "query performance", "self-service adoption", "data quality score"],
        "triggers": ["data migration", "BI tool evaluation", "data quality initiative", "team expansion"],
        "messaging_angles": [
            "Lead with data pipeline reliability improvements",
            "Frame as self-service enabler that frees analyst time",
            "Show data quality governance capabilities",
            "Reference scalability for growing data volumes",
        ],
        "value_drivers": ["data reliability", "self-service analytics", "data governance"],
    },
    {
        "role": "Legal/Compliance",
        "aliases": ["general counsel", "head of legal", "compliance officer", "vp legal", "chief compliance officer"],
        "pain_points": [
            "Contract review bottleneck slowing deal velocity",
            "Regulatory change tracking across jurisdictions",
            "Data privacy compliance (GDPR, CCPA, etc.)",
            "Vendor risk assessment at scale",
            "IP protection and monitoring",
        ],
        "kpis": ["contract turnaround time", "compliance audit pass rate", "legal spend", "risk incidents"],
        "triggers": ["regulatory change", "audit finding", "data breach concern", "M&A due diligence"],
        "messaging_angles": [
            "Lead with contract acceleration and review automation",
            "Frame as compliance risk reduction",
            "Show regulatory change tracking capabilities",
            "Reference vendor risk management at scale",
        ],
        "value_drivers": ["risk reduction", "compliance automation", "deal velocity"],
    },
    {
        "role": "Supply Chain",
        "aliases": ["supply chain manager", "head of supply chain", "vp supply chain", "logistics manager", "procurement director"],
        "pain_points": [
            "Demand forecasting inaccuracy causing overstock or stockouts",
            "Supplier reliability and lead time variability",
            "Logistics cost optimization under margin pressure",
            "Lack of end-to-end supply chain visibility",
            "Sustainability and ESG reporting requirements",
        ],
        "kpis": ["order accuracy", "inventory turns", "lead time", "logistics cost per unit", "supplier score"],
        "triggers": ["supply disruption", "cost reduction mandate", "new market entry", "sustainability audit"],
        "messaging_angles": [
            "Lead with demand forecasting accuracy improvements",
            "Frame as supply chain visibility and resilience tool",
            "Show logistics cost optimization results",
            "Reference sustainability and ESG benefits",
        ],
        "value_drivers": ["supply chain visibility", "cost optimization", "demand accuracy"],
    },
    {
        "role": "Account Executive",
        "aliases": ["ae", "account executive", "senior account executive", "enterprise account executive"],
        "pain_points": [
            "Spending too much time on proposal and admin work",
            "Difficulty multi-threading into accounts",
            "Losing deals to competitors on differentiation",
            "Long sales cycles with multiple stakeholders",
            "Inconsistent access to competitive intelligence",
        ],
        "kpis": ["closed revenue", "win rate", "deal size", "sales cycle length", "pipeline coverage"],
        "triggers": ["deal loss to competitor", "new territory", "quota increase", "enablement gap"],
        "messaging_angles": [
            "Lead with deal acceleration and admin time reduction",
            "Frame as competitive intelligence advantage",
            "Show multi-threading and stakeholder mapping benefits",
            "Reference win rate improvements at similar orgs",
        ],
        "value_drivers": ["win rate improvement", "deal acceleration", "competitive advantage"],
    },
    {
        "role": "Marketing Manager",
        "aliases": ["marketing manager", "demand gen manager", "growth manager", "digital marketing manager"],
        "pain_points": [
            "Campaign performance plateauing despite budget increases",
            "Content creation bottleneck across channels",
            "Lead scoring models not reflecting actual buyer intent",
            "Attribution gaps across paid, organic, and outbound",
            "Difficulty personalizing at scale",
        ],
        "kpis": ["MQLs", "CPL", "conversion rate", "content output", "channel ROI"],
        "triggers": ["campaign underperformance", "new channel launch", "martech evaluation", "budget review"],
        "messaging_angles": [
            "Lead with campaign performance optimization results",
            "Frame as personalization at scale enabler",
            "Show attribution clarity across channels",
            "Reference content production acceleration",
        ],
        "value_drivers": ["campaign performance", "personalization scale", "attribution clarity"],
    },
    {
        "role": "Engineering Manager",
        "aliases": ["engineering manager", "dev manager", "team lead engineering", "staff engineer"],
        "pain_points": [
            "Sprint velocity declining with growing codebase",
            "Developer experience friction slowing onboarding",
            "Production incidents interrupting planned work",
            "Technical debt conversations with product team",
            "Hiring pipeline not keeping pace with attrition",
        ],
        "kpis": ["sprint velocity", "deployment frequency", "code review time", "incident rate", "team satisfaction"],
        "triggers": ["team scaling", "incident spike", "developer survey results", "tool consolidation"],
        "messaging_angles": [
            "Lead with developer productivity and experience gains",
            "Frame as incident reduction tool",
            "Show onboarding acceleration for new engineers",
            "Reference codebase quality improvements",
        ],
        "value_drivers": ["developer productivity", "code quality", "team satisfaction"],
    },
    {
        "role": "Consultant/Agency Owner",
        "aliases": ["consultant", "agency owner", "agency director", "managing consultant", "principal consultant"],
        "pain_points": [
            "Client acquisition cost eating into margins",
            "Scaling delivery without proportional headcount",
            "Scope creep eroding profitability",
            "Differentiating from larger competitors",
            "Pipeline unpredictability and feast-or-famine cycles",
        ],
        "kpis": ["utilization rate", "client retention", "project margin", "pipeline value", "referral rate"],
        "triggers": ["lost pitch", "capacity crunch", "new service offering", "partnership opportunity"],
        "messaging_angles": [
            "Lead with client acquisition efficiency gains",
            "Frame as delivery scaling without headcount",
            "Show differentiation and positioning benefits",
            "Reference pipeline stabilization results",
        ],
        "value_drivers": ["client acquisition", "delivery efficiency", "pipeline stability"],
    },
    {
        "role": "HR Manager",
        "aliases": ["hr manager", "talent acquisition manager", "recruiter", "people operations manager"],
        "pain_points": [
            "Time-to-hire too long for critical roles",
            "Candidate experience inconsistency across recruiters",
            "Offer acceptance rate declining",
            "Employer brand not resonating with target talent",
            "Onboarding process manual and fragmented",
        ],
        "kpis": ["time to hire", "offer acceptance rate", "candidate NPS", "cost per hire", "90-day retention"],
        "triggers": ["hiring surge", "attrition spike", "employer brand refresh", "ATS evaluation"],
        "messaging_angles": [
            "Lead with time-to-hire reduction results",
            "Frame as candidate experience differentiator",
            "Show onboarding automation benefits",
            "Reference employer brand improvement stories",
        ],
        "value_drivers": ["hiring speed", "candidate experience", "onboarding efficiency"],
    },
    {
        "role": "Ecommerce Manager",
        "aliases": ["ecommerce manager", "head of ecommerce", "digital commerce director", "online sales manager"],
        "pain_points": [
            "Conversion rate optimization hitting diminishing returns",
            "Cart abandonment rate stubbornly high",
            "Personalization limited by data fragmentation",
            "Inventory sync issues across channels",
            "Rising customer acquisition costs",
        ],
        "kpis": ["conversion rate", "AOV", "cart abandonment rate", "customer lifetime value", "ROAS"],
        "triggers": ["peak season prep", "platform migration", "channel expansion", "CAC crisis"],
        "messaging_angles": [
            "Lead with conversion rate and AOV improvement data",
            "Frame as personalization at scale enabler",
            "Show cross-channel inventory sync benefits",
            "Reference customer lifetime value growth stories",
        ],
        "value_drivers": ["conversion optimization", "personalization", "customer lifetime value"],
    },
]

# ──────────────────────────────────────────────
# Objection Handling Patterns
# ──────────────────────────────────────────────

OBJECTION_PATTERNS: dict[str, dict] = {
    "no_time": {
        "label": "Too busy / no time",
        "response_strategy": "Acknowledge their time, offer ultra-concise value prop, suggest async option",
        "example_reframe": "Totally get it. Happy to send a 2-line summary you can glance at when convenient.",
    },
    "no_budget": {
        "label": "No budget right now",
        "response_strategy": "Reframe as ROI/payback, offer to build the business case together",
        "example_reframe": "Makes sense. Most teams we work with found it paid for itself within a quarter. Worth a quick look at the math?",
    },
    "already_have_solution": {
        "label": "Already using something",
        "response_strategy": "Acknowledge current tool, differentiate on specific gap, offer comparison",
        "example_reframe": "Good to know you're covered there. A few teams switched because of [specific gap]. Worth comparing notes?",
    },
    "bad_timing": {
        "label": "Not the right time",
        "response_strategy": "Respect timing, plant a seed for future, ask when would be better",
        "example_reframe": "Understood. When would be a better time to revisit? Happy to circle back then.",
    },
    "need_to_check_with_team": {
        "label": "Need internal alignment",
        "response_strategy": "Offer to help build internal case, provide shareable materials",
        "example_reframe": "Of course. Want me to send a quick summary your team can review? Makes the internal conversation easier.",
    },
    "not_interested": {
        "label": "Not interested",
        "response_strategy": "Graceful close with one value reframe, then respect the no",
        "example_reframe": "No worries at all. If [specific value] ever becomes relevant, feel free to reach out. Appreciate your time.",
    },
    "too_expensive": {
        "label": "Price concern",
        "response_strategy": "Reframe as cost-per-outcome, show ROI calculation, offer smaller starting point",
        "example_reframe": "Fair point. Most teams look at the cost per [outcome] rather than the sticker price. Happy to run those numbers together.",
    },
    "not_convinced": {
        "label": "Skeptical about results",
        "response_strategy": "Lead with specific proof point, offer pilot or trial, reference similar company",
        "example_reframe": "Healthy skepticism. [Company similar to theirs] saw [specific metric] in [timeframe]. Worth a quick pilot to see?",
    },
    "send_info": {
        "label": "Just send me info",
        "response_strategy": "Send concise value summary, follow up with question to re-engage",
        "example_reframe": "Sure thing. Here's a quick overview: [2-3 bullet value props]. Any of these particularly relevant to what you're working on?",
    },
    "wrong_person": {
        "label": "I'm not the right person",
        "response_strategy": "Ask for warm intro, offer to reach out directly with their blessing",
        "example_reframe": "Appreciate the honesty. Who on your team handles [area]? Happy to reach out directly if you're okay with that.",
    },
}


# ──────────────────────────────────────────────
# Lookup Functions
# ──────────────────────────────────────────────

def find_matching_persona(title: str) -> dict | None:
    """Find the best matching persona card for a prospect's title.

    Args:
        title: The prospect's job title (e.g., "VP of Sales", "CTO")

    Returns:
        Matching persona dict or None if no match found.
    """
    if not title:
        return None

    title_lower = title.lower().strip()

    # Direct role match
    for persona in PERSONA_CARDS:
        if persona["role"].lower() in title_lower:
            return persona

    # Alias match
    for persona in PERSONA_CARDS:
        for alias in persona["aliases"]:
            if alias in title_lower:
                return persona

    # Partial keyword match (less strict)
    title_words = set(re.sub(r"[^a-z0-9 ]", "", title_lower).split())
    best_match = None
    best_score = 0

    for persona in PERSONA_CARDS:
        all_terms = [persona["role"].lower()] + persona["aliases"]
        for term in all_terms:
            term_words = set(re.sub(r"[^a-z0-9 ]", "", term).split())
            if not term_words:
                continue
            overlap = len(title_words & term_words)
            score = overlap / len(term_words)
            if score > best_score and score >= 0.5:
                best_score = score
                best_match = persona

    return best_match


def get_objection_response(objection_type: str) -> dict | None:
    """Get objection handling pattern by type.

    Args:
        objection_type: Key like "no_time", "no_budget", etc.

    Returns:
        Objection pattern dict or None.
    """
    return OBJECTION_PATTERNS.get(objection_type)


def get_all_personas_summary() -> str:
    """Get a concise summary of all persona cards for prompt injection."""
    lines = []
    for p in PERSONA_CARDS:
        pains = "; ".join(p["pain_points"][:3])
        lines.append(f"- **{p['role']}**: {pains}")
    return "\n".join(lines)
