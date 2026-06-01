"""Full virtual life simulation for realistic YantrikDB evaluation.

Populates a complete person's life history — Priya Sharma, a 32-year-old
software engineer in Bangalore — spanning ~18 months across personal,
professional, health, relationships, hobbies, travel, and financial domains.

This goes far beyond the existing synthetic.py (31 work-project memories)
to test YantrikDB as a true persistent memory system for an AI assistant that
knows its user deeply over time.

Usage:
    python -m yantrikdb.eval.life_simulation            # quick mode (no real embedder)
    python -m yantrikdb.eval.life_simulation --embed     # with sentence-transformers
"""

import math
import random
import time

# ── Priya Sharma's Life History ─────────────────────────────────────────────
#
# Timeline: 18 months of memories, from Month 0 (start) to Month 18.
# Each session simulates a day or event in Priya's life.
# ~200 memories across 30+ sessions.

LIFE_SESSIONS = [
    # ═══════════════════════════════════════════════════════════════
    # MONTH 0 — INITIAL INTRODUCTION
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "intro_first_meeting",
        "time_offset_days": 0,
        "memories": [
            {
                "text": "My name is Priya Sharma, I'm 32 years old and I live in Koramangala, Bangalore",
                "type": "semantic",
                "importance": 1.0,
                "valence": 0.3,
                "entities": [("Priya", "Koramangala", "lives_in"), ("Priya", "Bangalore", "lives_in")],
            },
            {
                "text": "I work as a senior software engineer at Flipkart, on the search relevance team",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.2,
                "entities": [("Priya", "Flipkart", "works_at"), ("Priya", "search relevance", "works_on")],
            },
            {
                "text": "My husband Arjun is a product manager at Razorpay, we've been married for 4 years",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.6,
                "entities": [("Priya", "Arjun", "married_to"), ("Arjun", "Razorpay", "works_at")],
            },
            {
                "text": "We have a 2-year-old daughter named Meera who goes to Kangaroo Kids preschool",
                "type": "semantic",
                "importance": 0.95,
                "valence": 0.8,
                "entities": [("Priya", "Meera", "mother_of"), ("Arjun", "Meera", "father_of"), ("Meera", "Kangaroo Kids", "attends")],
            },
            {
                "text": "My parents live in Pune — Appa is retired from Infosys and Amma teaches at Symbiosis",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.4,
                "entities": [("Priya", "Appa", "daughter_of"), ("Priya", "Amma", "daughter_of"), ("Appa", "Pune", "lives_in"), ("Amma", "Symbiosis", "works_at")],
            },
            {
                "text": "I'm vegetarian, allergic to cashews, and I love South Indian filter coffee",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.2,
                "entities": [],
            },
        ],
    },
    {
        "name": "intro_preferences",
        "time_offset_days": 1,
        "memories": [
            {
                "text": "I prefer to do deep coding work between 10am and 1pm when Meera is at preschool",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.2,
                "entities": [],
            },
            {
                "text": "I use VS Code with Vim keybindings, and my go-to languages are Python and Go",
                "type": "procedural",
                "importance": 0.4,
                "valence": 0.1,
                "entities": [("Priya", "Python", "uses"), ("Priya", "Go", "uses")],
            },
            {
                "text": "I run 3 times a week in Cubbon Park, usually early morning before Arjun leaves for work",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [("Priya", "Cubbon Park", "runs_in")],
            },
            {
                "text": "I'm reading Sapiens by Yuval Noah Harari, about halfway through",
                "type": "episodic",
                "importance": 0.3,
                "valence": 0.2,
                "entities": [("Priya", "Sapiens", "reading")],
            },
            {
                "text": "My best friend Kavitha works at Google and we have coffee together every Saturday",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Priya", "Kavitha", "best_friend"), ("Kavitha", "Google", "works_at")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 1 — WORK PROJECT STARTS, DAILY LIFE
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month1_work_kickoff",
        "time_offset_days": 14,
        "memories": [
            {
                "text": "We're starting a new project at Flipkart to rebuild the search ranking pipeline using transformer-based models",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.4,
                "entities": [("Flipkart", "search ranking", "rebuilding"), ("search ranking", "transformers", "uses")],
            },
            {
                "text": "My tech lead Rohit wants us to use a BERT-based cross-encoder for re-ranking search results",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.2,
                "entities": [("Rohit", "BERT", "proposed"), ("Rohit", "Priya", "tech_lead_of")],
            },
            {
                "text": "The team has 6 people: me, Rohit, Deepa, Karan, Neha, and Vikram",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.1,
                "entities": [("Priya", "Rohit", "works_with"), ("Priya", "Deepa", "works_with"), ("Priya", "Karan", "works_with"), ("Priya", "Neha", "works_with"), ("Priya", "Vikram", "works_with")],
            },
            {
                "text": "Deepa is handling the data pipeline for training data extraction from clickstream logs",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.1,
                "entities": [("Deepa", "data pipeline", "handles"), ("data pipeline", "clickstream logs", "extracts_from")],
            },
        ],
    },
    {
        "name": "month1_meera_milestone",
        "time_offset_days": 20,
        "memories": [
            {
                "text": "Meera said her first complete sentence today: 'Amma, I want dosa!' — Arjun and I were so happy",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.9,
                "entities": [("Meera", "first sentence", "milestone")],
            },
            {
                "text": "Meera's pediatrician Dr. Anand said she's developing well, slightly above average for language",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Meera", "Dr. Anand", "pediatrician"), ("Meera", "language development", "above_average")],
            },
            {
                "text": "I need to schedule Meera's DPT booster vaccination by next month",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.1,
                "entities": [("Meera", "DPT booster", "needs")],
            },
        ],
    },
    {
        "name": "month1_health_running",
        "time_offset_days": 25,
        "memories": [
            {
                "text": "I ran my personal best 5K today: 26 minutes 30 seconds in Cubbon Park",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Priya", "5K", "personal_best")],
            },
            {
                "text": "My running buddy Sanjay suggested we train for the Bangalore Marathon in November",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("Priya", "Sanjay", "running_buddy"), ("Priya", "Bangalore Marathon", "considering")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 2 — WORK DEEPENS, FAMILY EVENTS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month2_work_progress",
        "time_offset_days": 40,
        "memories": [
            {
                "text": "The BERT cross-encoder is showing 12% improvement in NDCG@10 over the current BM25 baseline",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.5,
                "entities": [("BERT", "BM25", "outperforms"), ("search ranking", "12% NDCG improvement", "achieves")],
            },
            {
                "text": "Karan found that the model is too slow for real-time serving — 200ms per query is unacceptable",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.4,
                "entities": [("Karan", "latency issue", "discovered"), ("BERT", "200ms latency", "has_issue")],
            },
            {
                "text": "Rohit suggested we try knowledge distillation to create a smaller, faster model",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.2,
                "entities": [("Rohit", "knowledge distillation", "suggested")],
            },
            {
                "text": "I'm responsible for the distillation pipeline — need to generate soft labels from the teacher model",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.1,
                "entities": [("Priya", "distillation pipeline", "responsible_for")],
            },
        ],
    },
    {
        "name": "month2_appa_health",
        "time_offset_days": 45,
        "memories": [
            {
                "text": "Appa called from Pune — he's been having knee pain and the orthopedist recommended surgery",
                "type": "episodic",
                "importance": 0.8,
                "valence": -0.6,
                "entities": [("Appa", "knee surgery", "recommended"), ("Appa", "orthopedist", "consulted")],
            },
            {
                "text": "Amma is worried about Appa's surgery, I told her I'll fly to Pune to be there during the procedure",
                "type": "episodic",
                "importance": 0.8,
                "valence": -0.3,
                "entities": [("Priya", "Pune", "visiting"), ("Amma", "Appa", "worried_about")],
            },
            {
                "text": "I booked Indigo flight BLR-PNQ for March 15 to be there for Appa's surgery on March 17",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.2,
                "entities": [("Appa", "knee surgery", "scheduled_march_17")],
            },
        ],
    },
    {
        "name": "month2_cooking",
        "time_offset_days": 50,
        "memories": [
            {
                "text": "I learned to make Arjun's favorite dish — butter chicken from scratch using Amma's recipe",
                "type": "procedural",
                "importance": 0.4,
                "valence": 0.5,
                "entities": [("Priya", "butter chicken", "learned"), ("Amma", "butter chicken recipe", "shared")],
            },
            {
                "text": "The secret to Amma's butter chicken is roasting the tomatoes before blending, and adding kasuri methi at the end",
                "type": "procedural",
                "importance": 0.4,
                "valence": 0.3,
                "entities": [],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 3 — APPA'S SURGERY, WORK MILESTONE
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month3_appa_surgery",
        "time_offset_days": 65,
        "memories": [
            {
                "text": "Appa's knee replacement surgery went well, Dr. Kulkarni said recovery will take 6-8 weeks",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.4,
                "entities": [("Appa", "Dr. Kulkarni", "surgeon"), ("Appa", "knee replacement", "completed")],
            },
            {
                "text": "Amma has hired a physiotherapist named Ravi who comes home three times a week for Appa's rehab",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.2,
                "entities": [("Appa", "Ravi", "physiotherapist"), ("Appa", "rehab", "undergoing")],
            },
            {
                "text": "Meera was so excited to see her grandparents, she kept calling Appa 'Thatha' and bringing him toys",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.8,
                "entities": [("Meera", "Appa", "grandchild_of")],
            },
        ],
    },
    {
        "name": "month3_distillation_success",
        "time_offset_days": 75,
        "memories": [
            {
                "text": "The distilled model is 10x faster than the teacher — 20ms latency with only 2% NDCG drop",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.7,
                "entities": [("distilled model", "20ms latency", "achieves"), ("distilled model", "BERT", "derived_from")],
            },
            {
                "text": "Rohit is really happy with the distillation results, he's presenting them to VP Ananya next week",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Rohit", "Ananya", "presenting_to"), ("Ananya", "Flipkart", "VP_at")],
            },
            {
                "text": "Neha built an excellent A/B testing framework that lets us gradually roll out the new ranking model",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Neha", "A/B testing", "built"), ("A/B testing", "search ranking", "validates")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 4 — PROMOTION DISCUSSION, KAVITHA'S NEWS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month4_promotion",
        "time_offset_days": 90,
        "memories": [
            {
                "text": "Rohit mentioned in our 1-on-1 that I'm being considered for promotion to Staff Engineer",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.6,
                "entities": [("Priya", "Staff Engineer", "considered_for"), ("Rohit", "promotion", "discussed")],
            },
            {
                "text": "For the promotion I need to write a design doc for the next-gen ranking system and present to the architecture review board",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.1,
                "entities": [("Priya", "design doc", "needs_to_write"), ("Priya", "architecture review board", "presenting_to")],
            },
            {
                "text": "The promotion committee meets in August, so I have about 3 months to prepare my case",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.0,
                "entities": [("promotion committee", "August", "meets_in")],
            },
        ],
    },
    {
        "name": "month4_kavitha_engagement",
        "time_offset_days": 100,
        "memories": [
            {
                "text": "Kavitha got engaged to Rahul! They've been dating for 2 years, wedding planned for December",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.8,
                "entities": [("Kavitha", "Rahul", "engaged_to"), ("Kavitha", "wedding", "planned_december")],
            },
            {
                "text": "Kavitha asked me to be her maid of honor, I'm so excited but also nervous about the speech",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Priya", "Kavitha", "maid_of_honor_for")],
            },
        ],
    },
    {
        "name": "month4_finances",
        "time_offset_days": 105,
        "memories": [
            {
                "text": "Arjun and I reviewed our finances — we've saved 15 lakhs for Meera's education fund so far",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.3,
                "entities": [("Meera", "education fund", "has"), ("Priya", "financial planning", "does")],
            },
            {
                "text": "We're thinking of buying a 3BHK apartment in HSR Layout, the prices have come down",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.2,
                "entities": [("Priya", "HSR Layout", "considering_apartment"), ("Arjun", "apartment", "looking_for")],
            },
            {
                "text": "Our current rent in Koramangala is 45,000 per month, an EMI on a 1.2 crore apartment would be about 90,000",
                "type": "semantic",
                "importance": 0.5,
                "valence": -0.1,
                "entities": [],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 5-6 — MARATHON TRAINING, WORK DEPLOYMENT
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month5_marathon_training",
        "time_offset_days": 130,
        "memories": [
            {
                "text": "I've signed up for the Bangalore Marathon 10K category, training plan is 4 runs per week",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [("Priya", "Bangalore Marathon", "registered_for"), ("Priya", "Sanjay", "training_with")],
            },
            {
                "text": "My long run today was 8km and I felt great — pace was 5:45 per km",
                "type": "episodic",
                "importance": 0.3,
                "valence": 0.5,
                "entities": [],
            },
            {
                "text": "Sanjay recommended the Nike Pegasus for marathon training, much better cushioning than my old shoes",
                "type": "episodic",
                "importance": 0.3,
                "valence": 0.2,
                "entities": [("Sanjay", "Nike Pegasus", "recommended")],
            },
        ],
    },
    {
        "name": "month6_search_deployment",
        "time_offset_days": 155,
        "memories": [
            {
                "text": "We deployed the distilled search ranking model to 10% of Flipkart traffic in A/B test",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.5,
                "entities": [("distilled model", "Flipkart", "deployed_to"), ("search ranking", "A/B test", "in")],
            },
            {
                "text": "Early A/B results show 4.2% increase in click-through rate and 2.1% increase in add-to-cart",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.7,
                "entities": [("distilled model", "4.2% CTR improvement", "achieves")],
            },
            {
                "text": "Vikram found a bug where the model returns garbage results for queries with special characters like emojis",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.5,
                "entities": [("Vikram", "emoji bug", "found"), ("search ranking", "emoji bug", "has")],
            },
            {
                "text": "I fixed the tokenizer to properly handle Unicode — the issue was that our preprocessing stripped non-ASCII characters",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Priya", "tokenizer fix", "implemented")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 7 — DESIGN DOC, ARJUN'S CAREER
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month7_design_doc",
        "time_offset_days": 180,
        "memories": [
            {
                "text": "I've been working on the design doc for the next-gen ranking system — proposing a multi-stage retrieval architecture",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.2,
                "entities": [("Priya", "multi-stage retrieval", "proposing"), ("design doc", "search ranking", "for")],
            },
            {
                "text": "The architecture has three stages: candidate generation with ANN, lightweight pre-ranking, and transformer re-ranking",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.1,
                "entities": [("multi-stage retrieval", "candidate generation", "stage_1"), ("multi-stage retrieval", "pre-ranking", "stage_2"), ("multi-stage retrieval", "transformer re-ranking", "stage_3")],
            },
            {
                "text": "Rohit reviewed my design doc draft and suggested adding a section on failover and graceful degradation",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.1,
                "entities": [("Rohit", "design doc", "reviewed")],
            },
        ],
    },
    {
        "name": "month7_arjun_news",
        "time_offset_days": 190,
        "memories": [
            {
                "text": "Arjun got offered a role at Stripe in Singapore — it's a big step up but would mean relocating",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.0,
                "entities": [("Arjun", "Stripe", "offered_role"), ("Arjun", "Singapore", "might_relocate")],
            },
            {
                "text": "We're torn about the Singapore move — great career opportunity for Arjun but Meera just settled into preschool and my parents are in India",
                "type": "episodic",
                "importance": 0.9,
                "valence": -0.3,
                "entities": [("Priya", "Singapore decision", "deliberating")],
            },
            {
                "text": "Arjun's Stripe offer is 2.5x his current Razorpay compensation, including RSUs",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.2,
                "entities": [("Arjun", "Stripe offer", "2.5x_compensation")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 8 — PROMOTION RESULT, HEALTH SCARE
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month8_promotion_result",
        "time_offset_days": 210,
        "memories": [
            {
                "text": "I got promoted to Staff Engineer! The architecture review board loved the multi-stage retrieval design",
                "type": "episodic",
                "importance": 1.0,
                "valence": 0.9,
                "entities": [("Priya", "Staff Engineer", "promoted_to"), ("architecture review board", "design doc", "approved")],
            },
            {
                "text": "Rohit told me the VP Ananya specifically called out my distillation work as exceptional during the review",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.8,
                "entities": [("Ananya", "Priya", "praised"), ("Rohit", "Priya", "mentored")],
            },
            {
                "text": "My new salary as Staff Engineer is 48 lakhs base + 20 lakhs in ESOPs, up from 35 lakhs",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.6,
                "entities": [("Priya", "48 lakhs salary", "earns")],
            },
        ],
    },
    {
        "name": "month8_health_scare",
        "time_offset_days": 220,
        "memories": [
            {
                "text": "I had severe back pain during my long run and had to stop at 5km — couldn't even walk properly",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.7,
                "entities": [("Priya", "back pain", "experiencing")],
            },
            {
                "text": "Dr. Menon at Manipal Hospital diagnosed a herniated disc at L4-L5, recommended 4 weeks rest and physiotherapy",
                "type": "episodic",
                "importance": 0.8,
                "valence": -0.5,
                "entities": [("Priya", "Dr. Menon", "consulted"), ("Priya", "herniated disc", "diagnosed"), ("Dr. Menon", "Manipal Hospital", "works_at")],
            },
            {
                "text": "I'll have to skip the Bangalore Marathon this year, which is really disappointing after months of training",
                "type": "episodic",
                "importance": 0.6,
                "valence": -0.6,
                "entities": [("Priya", "Bangalore Marathon", "withdrew_from")],
            },
            {
                "text": "Dr. Menon prescribed naproxen for inflammation and said I should avoid sitting more than 2 hours continuously",
                "type": "procedural",
                "importance": 0.6,
                "valence": -0.2,
                "entities": [("Priya", "naproxen", "prescribed")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 9-10 — SINGAPORE DECISION, MEERA'S BIRTHDAY
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month9_singapore_decision",
        "time_offset_days": 250,
        "memories": [
            {
                "text": "After weeks of discussion, Arjun decided to decline the Stripe Singapore offer — family stability matters more right now",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.3,
                "entities": [("Arjun", "Stripe", "declined"), ("Arjun", "Singapore", "not_relocating")],
            },
            {
                "text": "Arjun negotiated a 30% raise at Razorpay after showing the Stripe offer, and got promoted to Senior PM",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Arjun", "Razorpay", "promoted_at"), ("Arjun", "Senior PM", "promoted_to")],
            },
            {
                "text": "I'm relieved about staying in Bangalore — my back recovery is going well with physio and I don't want to disrupt it",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [],
            },
        ],
    },
    {
        "name": "month10_meera_birthday",
        "time_offset_days": 270,
        "memories": [
            {
                "text": "Meera turned 3! We had a small party at home with a Frozen theme — she was obsessed with being Elsa",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.9,
                "entities": [("Meera", "3rd birthday", "celebrated")],
            },
            {
                "text": "My parents flew in from Pune for Meera's birthday, Appa is walking well after his knee surgery recovery",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("Appa", "knee recovery", "completed"), ("Appa", "Meera birthday", "attended")],
            },
            {
                "text": "Kavitha brought Rahul to meet everyone at the party — he's a cardiologist at Narayana Health",
                "type": "episodic",
                "importance": 0.4,
                "valence": 0.4,
                "entities": [("Rahul", "cardiologist", "is"), ("Rahul", "Narayana Health", "works_at")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 11 — APARTMENT HUNT, WORK SCALING
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month11_apartment",
        "time_offset_days": 300,
        "memories": [
            {
                "text": "We visited 5 apartments in HSR Layout this weekend — the one in Mantri Serenity caught our eye",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Priya", "Mantri Serenity", "interested_in"), ("Mantri Serenity", "HSR Layout", "located_in")],
            },
            {
                "text": "The Mantri Serenity 3BHK is 1.4 crore — more than our budget but it has a great park and is close to Meera's school",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.0,
                "entities": [("Mantri Serenity", "1.4 crore", "costs")],
            },
            {
                "text": "With my promotion raise and Arjun's raise, we can afford the EMI of 95,000 per month if we put down 30 lakhs",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.1,
                "entities": [],
            },
        ],
    },
    {
        "name": "month11_scaling_challenge",
        "time_offset_days": 310,
        "memories": [
            {
                "text": "The search ranking model is now serving 100% of Flipkart traffic — 50 million queries per day",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.5,
                "entities": [("search ranking", "100% traffic", "serving"), ("Flipkart", "50 million queries", "handles")],
            },
            {
                "text": "We're hitting GPU memory issues at peak traffic — during Big Billion Days the model needs to handle 5x normal load",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.4,
                "entities": [("search ranking", "GPU memory issue", "has"), ("Big Billion Days", "5x load", "creates")],
            },
            {
                "text": "I proposed dynamic batching with TensorRT optimization to handle peak loads — should give us 3x throughput",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.3,
                "entities": [("Priya", "TensorRT", "proposed"), ("TensorRT", "search ranking", "optimizes")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 12 — KAVITHA'S WEDDING, YEAR-END REFLECTION
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month12_kavitha_wedding",
        "time_offset_days": 340,
        "memories": [
            {
                "text": "Kavitha's wedding was absolutely beautiful — held at ITC Grand Chola in Chennai, 400 guests",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.9,
                "entities": [("Kavitha", "Rahul", "married"), ("Kavitha", "ITC Grand Chola", "wedding_venue")],
            },
            {
                "text": "My maid of honor speech went really well — I talked about how Kavitha and I have been friends since IIT Bombay",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.7,
                "entities": [("Priya", "Kavitha", "friends_since_IIT"), ("Priya", "IIT Bombay", "attended")],
            },
            {
                "text": "Meera was the flower girl and stole the show — everyone was taking photos of her in her pink lehenga",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.8,
                "entities": [("Meera", "Kavitha wedding", "flower_girl")],
            },
        ],
    },
    {
        "name": "month12_year_end",
        "time_offset_days": 350,
        "memories": [
            {
                "text": "Year-end review: my team's search ranking improvement contributed an estimated 200 crore annual revenue impact for Flipkart",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.6,
                "entities": [("search ranking", "200 crore revenue", "generated"), ("Priya", "Flipkart", "impact")],
            },
            {
                "text": "Rohit announced he's leaving Flipkart for a CTO role at a startup — I'm going to miss his mentorship",
                "type": "episodic",
                "importance": 0.8,
                "valence": -0.4,
                "entities": [("Rohit", "Flipkart", "leaving"), ("Rohit", "CTO", "new_role")],
            },
            {
                "text": "I might be asked to take over as tech lead of the search relevance team when Rohit leaves in January",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.3,
                "entities": [("Priya", "tech lead", "might_become")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 13-14 — NEW YEAR, LEADERSHIP, APARTMENT BOUGHT
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month13_new_leadership",
        "time_offset_days": 380,
        "memories": [
            {
                "text": "I officially took over as tech lead of the search relevance team — 6 direct reports now",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.5,
                "entities": [("Priya", "tech lead", "became"), ("Priya", "search relevance", "leads")],
            },
            {
                "text": "Deepa has been struggling with the increased scope — I need to mentor her more on system design",
                "type": "episodic",
                "importance": 0.5,
                "valence": -0.2,
                "entities": [("Priya", "Deepa", "mentoring"), ("Deepa", "system design", "needs_help")],
            },
            {
                "text": "I'm finding the transition from IC to manager hard — I miss writing code all day",
                "type": "episodic",
                "importance": 0.6,
                "valence": -0.3,
                "entities": [],
            },
            {
                "text": "Kavitha recommended the book 'The Manager's Path' by Camille Fournier for my transition to leadership",
                "type": "episodic",
                "importance": 0.4,
                "valence": 0.2,
                "entities": [("Priya", "The Manager's Path", "reading"), ("Kavitha", "The Manager's Path", "recommended")],
            },
        ],
    },
    {
        "name": "month14_apartment_bought",
        "time_offset_days": 400,
        "memories": [
            {
                "text": "We signed the agreement for the Mantri Serenity 3BHK apartment! Possession is in 6 months",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.8,
                "entities": [("Priya", "Mantri Serenity", "purchased"), ("Arjun", "Mantri Serenity", "purchased")],
            },
            {
                "text": "Final price was 1.35 crore after negotiation, with a 30 lakh down payment and 20-year HDFC loan",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.1,
                "entities": [("Mantri Serenity", "1.35 crore", "final_price"), ("HDFC", "home loan", "provider")],
            },
            {
                "text": "Arjun's parents gifted us 10 lakhs towards the down payment — really generous of them",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Arjun", "parents", "gifted_10_lakhs")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 15-16 — BACK RECOVERY, SIDE PROJECT, LEARNING
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month15_back_recovery",
        "time_offset_days": 420,
        "memories": [
            {
                "text": "My back is finally 90% recovered — Dr. Menon cleared me to start running again, but only on soft surfaces",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.6,
                "entities": [("Priya", "back recovery", "90_percent"), ("Dr. Menon", "running clearance", "gave")],
            },
            {
                "text": "I've switched to yoga 3 times a week instead of just running — it's helping my back and I actually enjoy it",
                "type": "procedural",
                "importance": 0.4,
                "valence": 0.4,
                "entities": [("Priya", "yoga", "practices")],
            },
            {
                "text": "Started going to Sanjay's yoga teacher Lakshmi's class at the Art of Living center",
                "type": "episodic",
                "importance": 0.3,
                "valence": 0.3,
                "entities": [("Priya", "Lakshmi", "yoga_teacher"), ("Sanjay", "Lakshmi", "recommended")],
            },
        ],
    },
    {
        "name": "month16_side_project",
        "time_offset_days": 450,
        "memories": [
            {
                "text": "I've started a side project on weekends — building an open-source search relevance benchmarking tool in Rust",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Priya", "search benchmark tool", "building"), ("Priya", "Rust", "learning")],
            },
            {
                "text": "Learning Rust has been challenging but rewarding — the ownership model is so different from Python and Go",
                "type": "episodic",
                "importance": 0.4,
                "valence": 0.3,
                "entities": [("Priya", "Rust", "learning")],
            },
            {
                "text": "I published the benchmark tool on GitHub and it got 200 stars in the first week — someone from Elastic even commented",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("search benchmark tool", "GitHub", "published_on"), ("search benchmark tool", "Elastic", "noticed_by")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 17 — MEERA SCHOOL TRANSITION, APPA VISIT
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month17_meera_school",
        "time_offset_days": 480,
        "memories": [
            {
                "text": "We're looking at primary schools for Meera — Indus International and Greenwood High are our top choices",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.1,
                "entities": [("Meera", "Indus International", "considering"), ("Meera", "Greenwood High", "considering")],
            },
            {
                "text": "Indus International has better academics but Greenwood High is closer to the new Mantri Serenity apartment",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.0,
                "entities": [("Indus International", "better academics", "has"), ("Greenwood High", "Mantri Serenity", "near")],
            },
            {
                "text": "Meera has been learning to write her name and can count to 20 — her teacher Ms. Shanti says she's very bright",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.6,
                "entities": [("Meera", "Ms. Shanti", "teacher"), ("Meera", "writing", "learning")],
            },
        ],
    },
    {
        "name": "month17_appa_visits",
        "time_offset_days": 490,
        "memories": [
            {
                "text": "Appa came to Bangalore for a checkup with Dr. Menon — his knee is fully healed, can even climb stairs now",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.5,
                "entities": [("Appa", "knee", "fully_healed"), ("Appa", "Dr. Menon", "checkup")],
            },
            {
                "text": "Appa told me he's started writing a memoir about his 30 years at Infosys — from the early days with Narayana Murthy",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [("Appa", "memoir", "writing"), ("Appa", "Infosys", "30_years"), ("Appa", "Narayana Murthy", "worked_with")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 18 — CURRENT STATE, LOOKING AHEAD
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month18_current",
        "time_offset_days": 520,
        "memories": [
            {
                "text": "The new apartment at Mantri Serenity is almost ready — we're choosing interior designs and planning the move",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Mantri Serenity", "interior design", "planning")],
            },
            {
                "text": "My team at Flipkart has grown to 10 people with 4 new hires — I'm really enjoying the leadership role now",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Priya", "search relevance", "leads"), ("Priya", "10 people", "manages")],
            },
            {
                "text": "Arjun and I are discussing having a second child — probably want to wait until we move into the new apartment",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.3,
                "entities": [("Priya", "second child", "considering"), ("Arjun", "second child", "discussing")],
            },
            {
                "text": "I got invited to speak at PyCon India about our search ranking work at Flipkart — my first conference talk!",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("Priya", "PyCon India", "speaking_at"), ("search ranking", "PyCon India", "presented_at")],
            },
            {
                "text": "My back is completely healed now — I ran 10K last weekend at a 5:30 pace, thinking about signing up for the marathon next year",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Priya", "10K", "completed"), ("Priya", "marathon", "planning_next_year")],
            },
        ],
    },
    {
        "name": "month18_amma_retirement",
        "time_offset_days": 530,
        "memories": [
            {
                "text": "Amma announced she's retiring from Symbiosis at the end of this year — she wants to spend more time with Meera",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Amma", "Symbiosis", "retiring_from"), ("Amma", "Meera", "wants_time_with")],
            },
            {
                "text": "Amma and Appa might move to Bangalore to be closer to us — they're looking at apartments near HSR Layout",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.6,
                "entities": [("Amma", "Bangalore", "considering_move"), ("Appa", "Bangalore", "considering_move"), ("Amma", "HSR Layout", "looking_at")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — CHILDHOOD & EDUCATION
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "childhood_and_education",
        "time_offset_days": 2,  # shared early in the relationship
        "memories": [
            {
                "text": "I grew up in Pune — we lived in a 2BHK apartment in Kothrud near Appa's Infosys office",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Priya", "Pune", "grew_up_in"), ("Priya", "Kothrud", "childhood_home")],
            },
            {
                "text": "I went to Loyola High School in Pune and was head girl in 12th standard — I loved maths and debating",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Priya", "Loyola High School", "attended")],
            },
            {
                "text": "I did my B.Tech in Computer Science at IIT Bombay — that's where I met Kavitha, we were roommates in Hostel 10",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.7,
                "entities": [("Priya", "IIT Bombay", "studied_at"), ("Priya", "Kavitha", "college_roommate")],
            },
            {
                "text": "My favourite childhood memory is Appa taking me to Sinhagad Fort on his scooter every Sunday morning for misal pav",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.9,
                "entities": [("Priya", "Appa", "childhood_memory"), ("Priya", "Sinhagad Fort", "childhood_memory")],
            },
            {
                "text": "Amma taught me Carnatic music as a child — I can still sing Vatapi Ganapathim and a few other kritis",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Priya", "Carnatic music", "learned")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — PETS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "pets",
        "time_offset_days": 200,
        "memories": [
            {
                "text": "We adopted a ginger tabby cat from CUPA Bangalore! Meera named her Mochi because of her round face",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.9,
                "entities": [("Priya", "Mochi", "pet_owner"), ("Meera", "Mochi", "named"), ("Mochi", "CUPA Bangalore", "adopted_from")],
            },
            {
                "text": "Mochi is a 1-year-old ginger tabby — she loves sleeping on Arjun's laptop and knocking things off the kitchen counter",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Mochi", "Arjun", "sleeps_on_laptop")],
            },
            {
                "text": "Mochi had her first vet visit at Cessna Lifeline — Dr. Ravi said she's healthy but needs to be spayed next month",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("Mochi", "Cessna Lifeline", "vet_visit"), ("Mochi", "Dr. Ravi", "treated_by")],
            },
            {
                "text": "Meera and Mochi are inseparable — Meera reads her picture books to Mochi every night before bed",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.9,
                "entities": [("Meera", "Mochi", "bond")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — HOBBIES & CREATIVE
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "hobbies_creative",
        "time_offset_days": 120,
        "memories": [
            {
                "text": "I started learning guitar during lockdown — I have a Yamaha F310 acoustic and I can play about 10 songs now",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Priya", "guitar", "hobby")],
            },
            {
                "text": "My favourite songs to play on guitar are Hotel California and Purani Jeans — Arjun jokes that I only know two chords",
                "type": "episodic",
                "importance": 0.4,
                "valence": 0.7,
                "entities": [],
            },
            {
                "text": "I started a watercolour painting hobby — I mostly paint flowers and Bangalore skyline scenes on weekends",
                "type": "semantic",
                "importance": 0.4,
                "valence": 0.6,
                "entities": [("Priya", "watercolour", "hobby")],
            },
            {
                "text": "I've been binge-watching Korean dramas — currently on Reply 1988 and it's making me cry every episode",
                "type": "episodic",
                "importance": 0.3,
                "valence": 0.5,
                "entities": [],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — BOOKS & READING
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "books_reading",
        "time_offset_days": 250,
        "memories": [
            {
                "text": "I finished Sapiens and absolutely loved it — started Homo Deus right after, Harari's writing is addictive",
                "type": "episodic",
                "importance": 0.4,
                "valence": 0.6,
                "entities": [("Priya", "Homo Deus", "reading"), ("Priya", "Sapiens", "finished")],
            },
            {
                "text": "Started reading Atomic Habits by James Clear on Kavitha's recommendation — the 1% improvement idea resonates with my running goals",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [("Priya", "Atomic Habits", "reading")],
            },
            {
                "text": "I keep a reading list on Notion — goal is 24 books this year, currently at 11, mostly non-fiction with some Tamil literature",
                "type": "semantic",
                "importance": 0.4,
                "valence": 0.3,
                "entities": [],
            },
            {
                "text": "Re-reading The Manager's Path before my first skip-level 1:1 — the chapter on managing managers is exactly what I need",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("Priya", "The Manager's Path", "reading")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — CLOSE FRIENDSHIPS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "friendships",
        "time_offset_days": 180,
        "memories": [
            {
                "text": "Kavitha and I have a standing Saturday coffee date at Third Wave Coffee in Koramangala — we've been doing this for 3 years",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Priya", "Kavitha", "coffee_date"), ("Kavitha", "Third Wave Coffee", "meets_at")],
            },
            {
                "text": "Sanjay is Arjun's college friend who became my close friend too — he's a standup comedian and always makes us laugh at dinner parties",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.7,
                "entities": [("Priya", "Sanjay", "close_friend"), ("Arjun", "Sanjay", "college_friend")],
            },
            {
                "text": "Divya from my running club has become a good friend — she's a doctor at Manipal Hospital and we bonded over our shared love of dosas",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Priya", "Divya", "running_friend"), ("Divya", "Manipal Hospital", "works_at")],
            },
            {
                "text": "My college friend group from IIT Bombay has a WhatsApp group called 'H10 Legends' — we do a reunion trip every year, last one was Goa",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.7,
                "entities": [("Priya", "IIT Bombay", "alumni"), ("Priya", "H10 Legends", "friend_group")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — MEDITATION & WELLNESS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "meditation_wellness",
        "time_offset_days": 350,
        "memories": [
            {
                "text": "I started meditating 10 minutes every morning using the Headspace app — it's helping with my work anxiety",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.5,
                "entities": [("Priya", "Headspace", "uses"), ("Priya", "meditation", "practice")],
            },
            {
                "text": "Lakshmi recommended I try Vipassana meditation — I'm considering the 10-day silent retreat at the Dhamma center in Bangalore",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("Priya", "Vipassana", "considering"), ("Lakshmi", "Vipassana", "recommended")],
            },
            {
                "text": "My morning routine is now: wake at 6, meditate 10 min, run or yoga, filter coffee, then start work by 9:30",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — VACATIONS & TRAVEL
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "vacations_travel",
        "time_offset_days": 300,
        "memories": [
            {
                "text": "We went to Coorg for a 3-day weekend — stayed at a beautiful homestay with coffee plantations, Meera loved the elephants",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.9,
                "entities": [("Priya", "Coorg", "vacation"), ("Meera", "Coorg", "vacation")],
            },
            {
                "text": "Arjun and I took a trip to Hampi for our anniversary — it was magical exploring the ruins and we stayed in a tiny guesthouse by the river",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.9,
                "entities": [("Priya", "Hampi", "vacation"), ("Arjun", "Hampi", "anniversary_trip")],
            },
            {
                "text": "Planning a Kerala backwaters trip for December — Arjun's parents want to join, it'll be Meera's first houseboat experience",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Priya", "Kerala", "planning_trip")],
            },
        ],
    },
]


# ── Golden Queries for Life Simulation ──────────────────────────────────────
# 100 queries spanning every domain of Priya's life, testing the full spectrum
# of YantrikDB retrieval: entity graph, temporal, emotional, procedural, conflicts.

LIFE_QUERIES = [
    # ─── IDENTITY & BASICS (5) ───
    {
        "id": "life_01_who",
        "query": "Who is Priya and what does she do?",
        "expected_texts": [
            "My name is Priya Sharma, I'm 32 years old and I live in Koramangala, Bangalore",
            "I work as a senior software engineer at Flipkart, on the search relevance team",
        ],
        "test_tags": ["identity", "semantic"],
        "description": "Basic identity retrieval",
    },
    {
        "id": "life_02_family",
        "query": "Tell me about Priya's family",
        "expected_texts": [
            "My husband Arjun is a product manager at Razorpay, we've been married for 4 years",
            "We have a 2-year-old daughter named Meera who goes to Kangaroo Kids preschool",
            "My parents live in Pune — Appa is retired from Infosys and Amma teaches at Symbiosis",
        ],
        "test_tags": ["identity", "graph"],
        "description": "Family relationships via entity graph",
    },
    {
        "id": "life_03_diet",
        "query": "What are Priya's dietary restrictions?",
        "expected_texts": [
            "I'm vegetarian, allergic to cashews, and I love South Indian filter coffee",
        ],
        "test_tags": ["identity", "semantic"],
        "description": "Personal facts recall",
    },
    {
        "id": "life_04_work_schedule",
        "query": "When does Priya prefer to do deep work?",
        "expected_texts": [
            "I prefer to do deep coding work between 10am and 1pm when Meera is at preschool",
        ],
        "test_tags": ["procedural", "semantic"],
        "description": "Work routine recall",
    },
    {
        "id": "life_05_languages",
        "query": "What programming languages does Priya use?",
        "expected_texts": [
            "I use VS Code with Vim keybindings, and my go-to languages are Python and Go",
        ],
        "test_tags": ["procedural", "semantic"],
        "description": "Technical preferences",
    },

    # ─── DAUGHTER MEERA (5) ───
    {
        "id": "life_06_meera_milestones",
        "query": "What milestones has Meera reached?",
        "expected_texts": [
            "Meera said her first complete sentence today: 'Amma, I want dosa!' — Arjun and I were so happy",
            "Meera has been learning to write her name and can count to 20 — her teacher Ms. Shanti says she's very bright",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Child development tracking",
    },
    {
        "id": "life_07_meera_health",
        "query": "What's Meera's health status and vaccinations?",
        "expected_texts": [
            "Meera's pediatrician Dr. Anand said she's developing well, slightly above average for language",
            "I need to schedule Meera's DPT booster vaccination by next month",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Child health tracking",
    },
    {
        "id": "life_08_meera_school",
        "query": "Which schools are being considered for Meera?",
        "expected_texts": [
            "We're looking at primary schools for Meera — Indus International and Greenwood High are our top choices",
            "Indus International has better academics but Greenwood High is closer to the new Mantri Serenity apartment",
        ],
        "test_tags": ["semantic"],
        "description": "School decision",
    },
    {
        "id": "life_09_meera_birthday",
        "query": "How did Meera's birthday go?",
        "expected_texts": [
            "Meera turned 3! We had a small party at home with a Frozen theme — she was obsessed with being Elsa",
            "My parents flew in from Pune for Meera's birthday, Appa is walking well after his knee surgery recovery",
        ],
        "test_tags": ["semantic", "temporal"],
        "description": "Birthday event recall",
    },
    {
        "id": "life_10_meera_wedding",
        "query": "What did Meera do at Kavitha's wedding?",
        "expected_texts": [
            "Meera was the flower girl and stole the show — everyone was taking photos of her in her pink lehenga",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Cross-entity memory (Meera + Kavitha wedding)",
    },

    # ─── HUSBAND ARJUN (5) ───
    {
        "id": "life_11_arjun_career",
        "query": "What happened with Arjun's career this year?",
        "expected_texts": [
            "Arjun got offered a role at Stripe in Singapore — it's a big step up but would mean relocating",
            "After weeks of discussion, Arjun decided to decline the Stripe Singapore offer — family stability matters more right now",
            "Arjun negotiated a 30% raise at Razorpay after showing the Stripe offer, and got promoted to Senior PM",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Full career arc for Arjun",
    },
    {
        "id": "life_12_singapore",
        "query": "Why didn't the family move to Singapore?",
        "expected_texts": [
            "We're torn about the Singapore move — great career opportunity for Arjun but Meera just settled into preschool and my parents are in India",
            "After weeks of discussion, Arjun decided to decline the Stripe Singapore offer — family stability matters more right now",
        ],
        "test_tags": ["semantic", "graph"],
        "description": "Decision context retrieval",
    },
    {
        "id": "life_13_arjun_salary",
        "query": "What is Arjun's compensation?",
        "expected_texts": [
            "Arjun's Stripe offer is 2.5x his current Razorpay compensation, including RSUs",
            "Arjun negotiated a 30% raise at Razorpay after showing the Stripe offer, and got promoted to Senior PM",
        ],
        "test_tags": ["semantic"],
        "description": "Financial details about Arjun",
    },

    # ─── PARENTS (5) ───
    {
        "id": "life_14_appa_health",
        "query": "What happened with Appa's knee surgery?",
        "expected_texts": [
            "Appa called from Pune — he's been having knee pain and the orthopedist recommended surgery",
            "Appa's knee replacement surgery went well, Dr. Kulkarni said recovery will take 6-8 weeks",
            "Appa came to Bangalore for a checkup with Dr. Menon — his knee is fully healed, can even climb stairs now",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Health journey across multiple sessions",
    },
    {
        "id": "life_15_appa_memoir",
        "query": "Is Appa writing anything?",
        "expected_texts": [
            "Appa told me he's started writing a memoir about his 30 years at Infosys — from the early days with Narayana Murthy",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Appa's personal project",
    },
    {
        "id": "life_16_amma",
        "query": "What is Amma doing and what are her plans?",
        "expected_texts": [
            "My parents live in Pune — Appa is retired from Infosys and Amma teaches at Symbiosis",
            "Amma announced she's retiring from Symbiosis at the end of this year — she wants to spend more time with Meera",
            "Amma and Appa might move to Bangalore to be closer to us — they're looking at apartments near HSR Layout",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Amma's arc from teaching to retirement",
    },
    {
        "id": "life_17_parents_relocate",
        "query": "Are Priya's parents moving to Bangalore?",
        "expected_texts": [
            "Amma and Appa might move to Bangalore to be closer to us — they're looking at apartments near HSR Layout",
            "Amma announced she's retiring from Symbiosis at the end of this year — she wants to spend more time with Meera",
        ],
        "test_tags": ["semantic", "temporal"],
        "description": "Future plans query",
    },
    {
        "id": "life_18_appa_recovery_physio",
        "query": "Who is Appa's physiotherapist?",
        "expected_texts": [
            "Amma has hired a physiotherapist named Ravi who comes home three times a week for Appa's rehab",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Specific entity recall via relationship",
    },

    # ─── BEST FRIEND KAVITHA (4) ───
    {
        "id": "life_19_kavitha_wedding",
        "query": "Tell me about Kavitha's wedding",
        "expected_texts": [
            "Kavitha's wedding was absolutely beautiful — held at ITC Grand Chola in Chennai, 400 guests",
            "My maid of honor speech went really well — I talked about how Kavitha and I have been friends since IIT Bombay",
            "Kavitha asked me to be her maid of honor, I'm so excited but also nervous about the speech",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Event narrative across sessions",
    },
    {
        "id": "life_20_kavitha_who",
        "query": "Who is Kavitha and who did she marry?",
        "expected_texts": [
            "My best friend Kavitha works at Google and we have coffee together every Saturday",
            "Kavitha got engaged to Rahul! They've been dating for 2 years, wedding planned for December",
            "Kavitha brought Rahul to meet everyone at the party — he's a cardiologist at Narayana Health",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Person profile via entity chain",
    },
    {
        "id": "life_21_kavitha_recommendation",
        "query": "What book did Kavitha recommend?",
        "expected_texts": [
            "Kavitha recommended the book 'The Manager's Path' by Camille Fournier for my transition to leadership",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Entity-linked recommendation recall",
    },
    {
        "id": "life_22_rahul_job",
        "query": "What does Rahul do for a living?",
        "expected_texts": [
            "Kavitha brought Rahul to meet everyone at the party — he's a cardiologist at Narayana Health",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Indirect person query (Kavitha's husband)",
    },

    # ─── WORK / CAREER (8) ───
    {
        "id": "life_23_search_project",
        "query": "What was the search ranking project about?",
        "expected_texts": [
            "We're starting a new project at Flipkart to rebuild the search ranking pipeline using transformer-based models",
            "My tech lead Rohit wants us to use a BERT-based cross-encoder for re-ranking search results",
        ],
        "test_tags": ["semantic"],
        "description": "Project overview",
    },
    {
        "id": "life_24_latency_fix",
        "query": "How did the team solve the model latency problem?",
        "expected_texts": [
            "Karan found that the model is too slow for real-time serving — 200ms per query is unacceptable",
            "Rohit suggested we try knowledge distillation to create a smaller, faster model",
            "The distilled model is 10x faster than the teacher — 20ms latency with only 2% NDCG drop",
        ],
        "test_tags": ["semantic", "graph"],
        "description": "Problem → solution narrative",
    },
    {
        "id": "life_25_promotion",
        "query": "How did Priya get promoted?",
        "expected_texts": [
            "Rohit mentioned in our 1-on-1 that I'm being considered for promotion to Staff Engineer",
            "I got promoted to Staff Engineer! The architecture review board loved the multi-stage retrieval design",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Career milestone arc",
    },
    {
        "id": "life_26_rohit",
        "query": "What happened with Rohit?",
        "expected_texts": [
            "My tech lead Rohit wants us to use a BERT-based cross-encoder for re-ranking search results",
            "Rohit announced he's leaving Flipkart for a CTO role at a startup — I'm going to miss his mentorship",
            "Rohit is really happy with the distillation results, he's presenting them to VP Ananya next week",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Person arc across project lifetime",
    },
    {
        "id": "life_27_team",
        "query": "Who is on Priya's team and what do they each do?",
        "expected_texts": [
            "The team has 6 people: me, Rohit, Deepa, Karan, Neha, and Vikram",
            "Deepa is handling the data pipeline for training data extraction from clickstream logs",
            "Neha built an excellent A/B testing framework that lets us gradually roll out the new ranking model",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Team structure query",
    },
    {
        "id": "life_28_ab_results",
        "query": "What were the A/B test results for the search model?",
        "expected_texts": [
            "We deployed the distilled search ranking model to 10% of Flipkart traffic in A/B test",
            "Early A/B results show 4.2% increase in click-through rate and 2.1% increase in add-to-cart",
        ],
        "test_tags": ["semantic"],
        "description": "Quantitative results recall",
    },
    {
        "id": "life_29_revenue",
        "query": "What revenue impact did Priya's work have?",
        "expected_texts": [
            "Year-end review: my team's search ranking improvement contributed an estimated 200 crore annual revenue impact for Flipkart",
        ],
        "test_tags": ["semantic"],
        "description": "Business impact recall",
    },
    {
        "id": "life_30_tech_lead",
        "query": "How is Priya finding the tech lead role?",
        "expected_texts": [
            "I officially took over as tech lead of the search relevance team — 6 direct reports now",
            "I'm finding the transition from IC to manager hard — I miss writing code all day",
            "My team at Flipkart has grown to 10 people with 4 new hires — I'm really enjoying the leadership role now",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Leadership journey arc",
    },

    # ─── HEALTH & FITNESS (5) ───
    {
        "id": "life_31_back_injury",
        "query": "What happened with Priya's back injury?",
        "expected_texts": [
            "I had severe back pain during my long run and had to stop at 5km — couldn't even walk properly",
            "Dr. Menon at Manipal Hospital diagnosed a herniated disc at L4-L5, recommended 4 weeks rest and physiotherapy",
            "My back is finally 90% recovered — Dr. Menon cleared me to start running again, but only on soft surfaces",
            "My back is completely healed now — I ran 10K last weekend at a 5:30 pace, thinking about signing up for the marathon next year",
        ],
        "test_tags": ["temporal", "graph"],
        "description": "Full health journey — injury to recovery",
    },
    {
        "id": "life_32_dr_menon",
        "query": "Who is Dr. Menon and what treatments did she prescribe?",
        "expected_texts": [
            "Dr. Menon at Manipal Hospital diagnosed a herniated disc at L4-L5, recommended 4 weeks rest and physiotherapy",
            "Dr. Menon prescribed naproxen for inflammation and said I should avoid sitting more than 2 hours continuously",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Doctor-patient relationship chain",
    },
    {
        "id": "life_33_marathon",
        "query": "Is Priya running in any marathons?",
        "expected_texts": [
            "I'll have to skip the Bangalore Marathon this year, which is really disappointing after months of training",
            "My back is completely healed now — I ran 10K last weekend at a 5:30 pace, thinking about signing up for the marathon next year",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Marathon plans across time",
    },
    {
        "id": "life_34_running_pb",
        "query": "What was Priya's running personal best?",
        "expected_texts": [
            "I ran my personal best 5K today: 26 minutes 30 seconds in Cubbon Park",
        ],
        "test_tags": ["semantic"],
        "description": "Specific metric recall",
    },
    {
        "id": "life_35_yoga",
        "query": "Does Priya do yoga?",
        "expected_texts": [
            "I've switched to yoga 3 times a week instead of just running — it's helping my back and I actually enjoy it",
            "Started going to Sanjay's yoga teacher Lakshmi's class at the Art of Living center",
        ],
        "test_tags": ["semantic"],
        "description": "Activity tracking",
    },

    # ─── FINANCES & APARTMENT (5) ───
    {
        "id": "life_36_apartment",
        "query": "Tell me about the apartment Priya bought",
        "expected_texts": [
            "We signed the agreement for the Mantri Serenity 3BHK apartment! Possession is in 6 months",
            "Final price was 1.35 crore after negotiation, with a 30 lakh down payment and 20-year HDFC loan",
            "The Mantri Serenity 3BHK is 1.4 crore — more than our budget but it has a great park and is close to Meera's school",
        ],
        "test_tags": ["semantic", "temporal"],
        "description": "Real estate decision arc",
    },
    {
        "id": "life_37_finances",
        "query": "What's the family's financial situation?",
        "expected_texts": [
            "Arjun and I reviewed our finances — we've saved 15 lakhs for Meera's education fund so far",
            "Our current rent in Koramangala is 45,000 per month, an EMI on a 1.2 crore apartment would be about 90,000",
            "My new salary as Staff Engineer is 48 lakhs base + 20 lakhs in ESOPs, up from 35 lakhs",
        ],
        "test_tags": ["semantic"],
        "description": "Financial overview",
    },
    {
        "id": "life_38_apartment_status",
        "query": "When will the new apartment be ready?",
        "expected_texts": [
            "The new apartment at Mantri Serenity is almost ready — we're choosing interior designs and planning the move",
            "We signed the agreement for the Mantri Serenity 3BHK apartment! Possession is in 6 months",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Apartment timeline",
    },

    # ─── COOKING & HOBBIES (3) ───
    {
        "id": "life_39_cooking",
        "query": "What's the secret to Amma's butter chicken recipe?",
        "expected_texts": [
            "The secret to Amma's butter chicken is roasting the tomatoes before blending, and adding kasuri methi at the end",
            "I learned to make Arjun's favorite dish — butter chicken from scratch using Amma's recipe",
        ],
        "test_tags": ["procedural", "semantic"],
        "description": "Procedural memory — recipe details",
    },
    {
        "id": "life_40_reading",
        "query": "What books is Priya reading?",
        "expected_texts": [
            "I'm reading Sapiens by Yuval Noah Harari, about halfway through",
            "Kavitha recommended the book 'The Manager's Path' by Camille Fournier for my transition to leadership",
        ],
        "test_tags": ["semantic"],
        "description": "Reading list recall",
    },
    {
        "id": "life_41_side_project",
        "query": "What side project is Priya working on?",
        "expected_texts": [
            "I've started a side project on weekends — building an open-source search relevance benchmarking tool in Rust",
            "I published the benchmark tool on GitHub and it got 200 stars in the first week — someone from Elastic even commented",
        ],
        "test_tags": ["semantic"],
        "description": "Side project tracking",
    },

    # ─── MULTI-HOP & CROSS-DOMAIN (6) ───
    {
        "id": "life_42_doctors",
        "query": "Which doctors has the family seen?",
        "expected_texts": [
            "Meera's pediatrician Dr. Anand said she's developing well, slightly above average for language",
            "Dr. Menon at Manipal Hospital diagnosed a herniated disc at L4-L5, recommended 4 weeks rest and physiotherapy",
            "Appa's knee replacement surgery went well, Dr. Kulkarni said recovery will take 6-8 weeks",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Cross-person doctor query",
    },
    {
        "id": "life_43_flipkart_impact",
        "query": "What has Priya's search team achieved at Flipkart?",
        "expected_texts": [
            "The search ranking model is now serving 100% of Flipkart traffic — 50 million queries per day",
            "Year-end review: my team's search ranking improvement contributed an estimated 200 crore annual revenue impact for Flipkart",
            "Early A/B results show 4.2% increase in click-through rate and 2.1% increase in add-to-cart",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Org-scoped achievement roll-up",
    },
    {
        "id": "life_44_bugs",
        "query": "What bugs or technical issues did the team encounter?",
        "expected_texts": [
            "Karan found that the model is too slow for real-time serving — 200ms per query is unacceptable",
            "Vikram found a bug where the model returns garbage results for queries with special characters like emojis",
            "We're hitting GPU memory issues at peak traffic — during Big Billion Days the model needs to handle 5x normal load",
        ],
        "test_tags": ["semantic", "graph"],
        "description": "Problem tracking across project",
    },
    {
        "id": "life_45_sanjay",
        "query": "Who is Sanjay?",
        "expected_texts": [
            "My running buddy Sanjay suggested we train for the Bangalore Marathon in November",
            "Sanjay recommended the Nike Pegasus for marathon training, much better cushioning than my old shoes",
            "Started going to Sanjay's yoga teacher Lakshmi's class at the Art of Living center",
        ],
        "test_tags": ["graph"],
        "description": "Person profile via entity chain",
    },
    {
        "id": "life_46_future_plans",
        "query": "What are Priya's plans for the future?",
        "expected_texts": [
            "Arjun and I are discussing having a second child — probably want to wait until we move into the new apartment",
            "I got invited to speak at PyCon India about our search ranking work at Flipkart — my first conference talk!",
            "My back is completely healed now — I ran 10K last weekend at a 5:30 pace, thinking about signing up for the marathon next year",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Forward-looking query",
    },
    {
        "id": "life_47_emotional_lows",
        "query": "What were the most stressful or difficult moments?",
        "expected_texts": [
            "Appa called from Pune — he's been having knee pain and the orthopedist recommended surgery",
            "I had severe back pain during my long run and had to stop at 5km — couldn't even walk properly",
            "We're torn about the Singapore move — great career opportunity for Arjun but Meera just settled into preschool and my parents are in India",
        ],
        "test_tags": ["valence", "semantic"],
        "description": "Negative valence retrieval",
    },
    {
        "id": "life_48_emotional_highs",
        "query": "What were the happiest moments?",
        "expected_texts": [
            "I got promoted to Staff Engineer! The architecture review board loved the multi-stage retrieval design",
            "Meera said her first complete sentence today: 'Amma, I want dosa!' — Arjun and I were so happy",
            "Kavitha's wedding was absolutely beautiful — held at ITC Grand Chola in Chennai, 400 guests",
            "Meera turned 3! We had a small party at home with a Frozen theme — she was obsessed with being Elsa",
        ],
        "test_tags": ["valence", "semantic"],
        "description": "Positive valence retrieval",
    },
    {
        "id": "life_49_learning_rust",
        "query": "How is Priya's Rust learning going?",
        "expected_texts": [
            "I've started a side project on weekends — building an open-source search relevance benchmarking tool in Rust",
            "Learning Rust has been challenging but rewarding — the ownership model is so different from Python and Go",
        ],
        "test_tags": ["semantic"],
        "description": "Learning journey",
    },
    {
        "id": "life_50_iit",
        "query": "Where did Priya go to college?",
        "expected_texts": [
            "My maid of honor speech went really well — I talked about how Kavitha and I have been friends since IIT Bombay",
        ],
        "test_tags": ["semantic"],
        "description": "Education fact buried in other memory",
    },

    # ─── NEW QUERIES 51-100 ───────────────────────────────────────────

    # ─── PETS & MOCHI (4) ───
    {
        "id": "life_51_mochi_adoption",
        "query": "How did the family get their cat?",
        "expected_texts": [
            "We adopted a ginger tabby cat from CUPA Bangalore! Meera named her Mochi because of her round face",
        ],
        "test_tags": ["semantic"],
        "description": "Pet adoption story",
    },
    {
        "id": "life_52_mochi_personality",
        "query": "What is Mochi like?",
        "expected_texts": [
            "Mochi is a 1-year-old ginger tabby — she loves sleeping on Arjun's laptop and knocking things off the kitchen counter",
            "Meera and Mochi are inseparable — Meera reads her picture books to Mochi every night before bed",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Pet personality details",
    },
    {
        "id": "life_53_mochi_vet",
        "query": "Has Mochi been to the vet?",
        "expected_texts": [
            "Mochi had her first vet visit at Cessna Lifeline — Dr. Ravi said she's healthy but needs to be spayed next month",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Pet health tracking",
    },
    {
        "id": "life_54_meera_mochi",
        "query": "How do Meera and Mochi get along?",
        "expected_texts": [
            "Meera and Mochi are inseparable — Meera reads her picture books to Mochi every night before bed",
            "We adopted a ginger tabby cat from CUPA Bangalore! Meera named her Mochi because of her round face",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Cross-entity bond between child and pet",
    },

    # ─── HOBBIES & CREATIVE (4) ───
    {
        "id": "life_55_guitar",
        "query": "Does Priya play any musical instruments?",
        "expected_texts": [
            "I started learning guitar during lockdown — I have a Yamaha F310 acoustic and I can play about 10 songs now",
            "My favourite songs to play on guitar are Hotel California and Purani Jeans — Arjun jokes that I only know two chords",
        ],
        "test_tags": ["semantic"],
        "description": "Musical hobby recall",
    },
    {
        "id": "life_56_painting",
        "query": "What does Priya paint?",
        "expected_texts": [
            "I started a watercolour painting hobby — I mostly paint flowers and Bangalore skyline scenes on weekends",
        ],
        "test_tags": ["semantic"],
        "description": "Art hobby recall",
    },
    {
        "id": "life_57_kdrama",
        "query": "What TV shows is Priya watching?",
        "expected_texts": [
            "I've been binge-watching Korean dramas — currently on Reply 1988 and it's making me cry every episode",
        ],
        "test_tags": ["semantic"],
        "description": "Entertainment preferences",
    },
    {
        "id": "life_58_carnatic",
        "query": "Does Priya know any music from childhood?",
        "expected_texts": [
            "Amma taught me Carnatic music as a child — I can still sing Vatapi Ganapathim and a few other kritis",
        ],
        "test_tags": ["semantic"],
        "description": "Childhood skill recall",
    },

    # ─── TRAVEL & VACATIONS (3) ───
    {
        "id": "life_59_coorg",
        "query": "Tell me about the Coorg trip",
        "expected_texts": [
            "We went to Coorg for a 3-day weekend — stayed at a beautiful homestay with coffee plantations, Meera loved the elephants",
        ],
        "test_tags": ["semantic"],
        "description": "Vacation memory recall",
    },
    {
        "id": "life_60_hampi",
        "query": "Where did Priya and Arjun go for their anniversary?",
        "expected_texts": [
            "Arjun and I took a trip to Hampi for our anniversary — it was magical exploring the ruins and we stayed in a tiny guesthouse by the river",
        ],
        "test_tags": ["semantic", "graph"],
        "description": "Anniversary trip recall",
    },
    {
        "id": "life_61_kerala",
        "query": "Are there any upcoming travel plans?",
        "expected_texts": [
            "Planning a Kerala backwaters trip for December — Arjun's parents want to join, it'll be Meera's first houseboat experience",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Planned future travel",
    },

    # ─── MEDITATION & WELLNESS (3) ───
    {
        "id": "life_62_meditation",
        "query": "Does Priya meditate?",
        "expected_texts": [
            "I started meditating 10 minutes every morning using the Headspace app — it's helping with my work anxiety",
            "Lakshmi recommended I try Vipassana meditation — I'm considering the 10-day silent retreat at the Dhamma center in Bangalore",
        ],
        "test_tags": ["semantic"],
        "description": "Meditation practice recall",
    },
    {
        "id": "life_63_morning_routine",
        "query": "What is Priya's morning routine?",
        "expected_texts": [
            "My morning routine is now: wake at 6, meditate 10 min, run or yoga, filter coffee, then start work by 9:30",
        ],
        "test_tags": ["procedural"],
        "description": "Daily routine recall",
    },
    {
        "id": "life_64_vipassana",
        "query": "Is Priya considering any retreats?",
        "expected_texts": [
            "Lakshmi recommended I try Vipassana meditation — I'm considering the 10-day silent retreat at the Dhamma center in Bangalore",
        ],
        "test_tags": ["semantic"],
        "description": "Future wellness plans",
    },

    # ─── CHILDHOOD & EDUCATION (4) ───
    {
        "id": "life_65_childhood_pune",
        "query": "Where did Priya grow up?",
        "expected_texts": [
            "I grew up in Pune — we lived in a 2BHK apartment in Kothrud near Appa's Infosys office",
            "I went to Loyola High School in Pune and was head girl in 12th standard — I loved maths and debating",
        ],
        "test_tags": ["semantic"],
        "description": "Childhood location and school",
    },
    {
        "id": "life_66_sinhagad",
        "query": "What is Priya's favorite childhood memory?",
        "expected_texts": [
            "My favourite childhood memory is Appa taking me to Sinhagad Fort on his scooter every Sunday morning for misal pav",
        ],
        "test_tags": ["semantic", "valence"],
        "description": "Nostalgic memory recall",
    },
    {
        "id": "life_67_iit_roommate",
        "query": "Who was Priya's college roommate?",
        "expected_texts": [
            "I did my B.Tech in Computer Science at IIT Bombay — that's where I met Kavitha, we were roommates in Hostel 10",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "College relationship detail",
    },
    {
        "id": "life_68_high_school",
        "query": "What school did Priya attend in Pune?",
        "expected_texts": [
            "I went to Loyola High School in Pune and was head girl in 12th standard — I loved maths and debating",
        ],
        "test_tags": ["semantic"],
        "description": "High school fact recall",
    },

    # ─── FRIENDSHIPS (4) ───
    {
        "id": "life_69_kavitha_coffee",
        "query": "Where do Priya and Kavitha meet for coffee?",
        "expected_texts": [
            "Kavitha and I have a standing Saturday coffee date at Third Wave Coffee in Koramangala — we've been doing this for 3 years",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Routine friendship detail",
    },
    {
        "id": "life_70_sanjay_background",
        "query": "How does Priya know Sanjay?",
        "expected_texts": [
            "Sanjay is Arjun's college friend who became my close friend too — he's a standup comedian and always makes us laugh at dinner parties",
            "My running buddy Sanjay suggested we train for the Bangalore Marathon in November",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Multi-faceted friendship recall",
    },
    {
        "id": "life_71_divya",
        "query": "Who is Divya?",
        "expected_texts": [
            "Divya from my running club has become a good friend — she's a doctor at Manipal Hospital and we bonded over our shared love of dosas",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Person profile from entity graph",
    },
    {
        "id": "life_72_h10_legends",
        "query": "Does Priya keep in touch with college friends?",
        "expected_texts": [
            "My college friend group from IIT Bombay has a WhatsApp group called 'H10 Legends' — we do a reunion trip every year, last one was Goa",
            "I did my B.Tech in Computer Science at IIT Bombay — that's where I met Kavitha, we were roommates in Hostel 10",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "College friend group recall",
    },

    # ─── WORK — DEEPER QUESTIONS (6) ───
    {
        "id": "life_73_distillation",
        "query": "What was Priya responsible for in the search project?",
        "expected_texts": [
            "I'm responsible for the distillation pipeline — need to generate soft labels from the teacher model",
            "The distilled model is 10x faster than the teacher — 20ms latency with only 2% NDCG drop",
        ],
        "test_tags": ["semantic"],
        "description": "Individual contribution recall",
    },
    {
        "id": "life_74_design_doc",
        "query": "What architecture did Priya propose in her design doc?",
        "expected_texts": [
            "The architecture has three stages: candidate generation with ANN, lightweight pre-ranking, and transformer re-ranking",
            "I've been working on the design doc for the next-gen ranking system — proposing a multi-stage retrieval architecture",
        ],
        "test_tags": ["semantic"],
        "description": "Technical design recall",
    },
    {
        "id": "life_75_vp_ananya",
        "query": "Who is Ananya at Flipkart?",
        "expected_texts": [
            "Rohit told me the VP Ananya specifically called out my distillation work as exceptional during the review",
            "Rohit is really happy with the distillation results, he's presenting them to VP Ananya next week",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Person recall via org hierarchy",
    },
    {
        "id": "life_76_scaling",
        "query": "What scaling challenges did the search team face?",
        "expected_texts": [
            "We're hitting GPU memory issues at peak traffic — during Big Billion Days the model needs to handle 5x normal load",
            "I proposed dynamic batching with TensorRT optimization to handle peak loads — should give us 3x throughput",
        ],
        "test_tags": ["semantic"],
        "description": "Technical problem and solution",
    },
    {
        "id": "life_77_deepa",
        "query": "What is Deepa working on and how is she doing?",
        "expected_texts": [
            "Deepa is handling the data pipeline for training data extraction from clickstream logs",
            "Deepa has been struggling with the increased scope — I need to mentor her more on system design",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Team member arc",
    },
    {
        "id": "life_78_pycon",
        "query": "Has Priya been invited to speak at any conferences?",
        "expected_texts": [
            "I got invited to speak at PyCon India about our search ranking work at Flipkart — my first conference talk!",
        ],
        "test_tags": ["semantic"],
        "description": "Conference speaking engagement",
    },

    # ─── ARJUN — DEEPER (3) ───
    {
        "id": "life_79_arjun_stripe_money",
        "query": "How much was the Stripe offer compared to Razorpay?",
        "expected_texts": [
            "Arjun's Stripe offer is 2.5x his current Razorpay compensation, including RSUs",
        ],
        "test_tags": ["semantic"],
        "description": "Compensation comparison recall",
    },
    {
        "id": "life_80_arjun_razorpay",
        "query": "What is Arjun's current role?",
        "expected_texts": [
            "Arjun negotiated a 30% raise at Razorpay after showing the Stripe offer, and got promoted to Senior PM",
            "My husband Arjun is a product manager at Razorpay, we've been married for 4 years",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Arjun's current position with history",
    },
    {
        "id": "life_81_second_child",
        "query": "Are Priya and Arjun planning to have another child?",
        "expected_texts": [
            "Arjun and I are discussing having a second child — probably want to wait until we move into the new apartment",
        ],
        "test_tags": ["semantic"],
        "description": "Family planning recall",
    },

    # ─── PARENTS — DEEPER (3) ───
    {
        "id": "life_82_appa_infosys",
        "query": "How long did Appa work at Infosys?",
        "expected_texts": [
            "Appa told me he's started writing a memoir about his 30 years at Infosys — from the early days with Narayana Murthy",
            "My parents live in Pune — Appa is retired from Infosys and Amma teaches at Symbiosis",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Appa's career history",
    },
    {
        "id": "life_83_appa_surgeon",
        "query": "Who performed Appa's knee surgery?",
        "expected_texts": [
            "Appa's knee replacement surgery went well, Dr. Kulkarni said recovery will take 6-8 weeks",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Specific doctor-patient fact",
    },
    {
        "id": "life_84_pune_flight",
        "query": "When did Priya fly to Pune for the surgery?",
        "expected_texts": [
            "I booked Indigo flight BLR-PNQ for March 15 to be there for Appa's surgery on March 17",
            "Amma is worried about Appa's surgery, I told her I'll fly to Pune to be there during the procedure",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Travel event with specific dates",
    },

    # ─── FINANCES — DEEPER (3) ───
    {
        "id": "life_85_salary",
        "query": "What is Priya's salary after the promotion?",
        "expected_texts": [
            "My new salary as Staff Engineer is 48 lakhs base + 20 lakhs in ESOPs, up from 35 lakhs",
        ],
        "test_tags": ["semantic"],
        "description": "Compensation details",
    },
    {
        "id": "life_86_apartment_price",
        "query": "How much did the Mantri Serenity apartment cost?",
        "expected_texts": [
            "Final price was 1.35 crore after negotiation, with a 30 lakh down payment and 20-year HDFC loan",
            "The Mantri Serenity 3BHK is 1.4 crore — more than our budget but it has a great park and is close to Meera's school",
        ],
        "test_tags": ["semantic"],
        "description": "Real estate price details",
    },
    {
        "id": "life_87_emi",
        "query": "What would the apartment EMI be?",
        "expected_texts": [
            "With my promotion raise and Arjun's raise, we can afford the EMI of 95,000 per month if we put down 30 lakhs",
            "Our current rent in Koramangala is 45,000 per month, an EMI on a 1.2 crore apartment would be about 90,000",
        ],
        "test_tags": ["semantic"],
        "description": "Financial calculation recall",
    },

    # ─── HEALTH — DEEPER (3) ───
    {
        "id": "life_88_herniated_disc",
        "query": "What was Priya's back diagnosis?",
        "expected_texts": [
            "Dr. Menon at Manipal Hospital diagnosed a herniated disc at L4-L5, recommended 4 weeks rest and physiotherapy",
            "Dr. Menon prescribed naproxen for inflammation and said I should avoid sitting more than 2 hours continuously",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Medical diagnosis details",
    },
    {
        "id": "life_89_running_comeback",
        "query": "Has Priya started running again after the injury?",
        "expected_texts": [
            "My back is finally 90% recovered — Dr. Menon cleared me to start running again, but only on soft surfaces",
            "My back is completely healed now — I ran 10K last weekend at a 5:30 pace, thinking about signing up for the marathon next year",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Recovery arc from injury to running",
    },
    {
        "id": "life_90_lakshmi_yoga",
        "query": "Who is Lakshmi?",
        "expected_texts": [
            "Started going to Sanjay's yoga teacher Lakshmi's class at the Art of Living center",
            "Lakshmi recommended I try Vipassana meditation — I'm considering the 10-day silent retreat at the Dhamma center in Bangalore",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Person profile via entity chain",
    },

    # ─── BOOKS — DEEPER (3) ───
    {
        "id": "life_91_reading_goal",
        "query": "How many books does Priya want to read this year?",
        "expected_texts": [
            "I keep a reading list on Notion — goal is 24 books this year, currently at 11, mostly non-fiction with some Tamil literature",
        ],
        "test_tags": ["semantic"],
        "description": "Reading goal recall",
    },
    {
        "id": "life_92_atomic_habits",
        "query": "What does Priya think about Atomic Habits?",
        "expected_texts": [
            "Started reading Atomic Habits by James Clear on Kavitha's recommendation — the 1% improvement idea resonates with my running goals",
        ],
        "test_tags": ["semantic"],
        "description": "Specific book opinion recall",
    },
    {
        "id": "life_93_harari",
        "query": "Has Priya read any books by Yuval Noah Harari?",
        "expected_texts": [
            "I'm reading Sapiens by Yuval Noah Harari, about halfway through",
            "I finished Sapiens and absolutely loved it — started Homo Deus right after, Harari's writing is addictive",
        ],
        "test_tags": ["semantic"],
        "description": "Author-based book recall",
    },

    # ─── CROSS-DOMAIN & MULTI-HOP (6) ───
    {
        "id": "life_94_manipal_connections",
        "query": "Who works at Manipal Hospital?",
        "expected_texts": [
            "Dr. Menon at Manipal Hospital diagnosed a herniated disc at L4-L5, recommended 4 weeks rest and physiotherapy",
            "Divya from my running club has become a good friend — she's a doctor at Manipal Hospital and we bonded over our shared love of dosas",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Entity-based cross-person query",
    },
    {
        "id": "life_95_hsr_layout",
        "query": "What connections does the family have to HSR Layout?",
        "expected_texts": [
            "We're thinking of buying a 3BHK apartment in HSR Layout, the prices have come down",
            "Amma and Appa might move to Bangalore to be closer to us — they're looking at apartments near HSR Layout",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Location-based cross-event query",
    },
    {
        "id": "life_96_nike_pegasus",
        "query": "What running shoes does Sanjay recommend?",
        "expected_texts": [
            "Sanjay recommended the Nike Pegasus for marathon training, much better cushioning than my old shoes",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Product recommendation via person",
    },
    {
        "id": "life_97_leadership_transition",
        "query": "How did Priya's role change from IC to manager?",
        "expected_texts": [
            "I'm finding the transition from IC to manager hard — I miss writing code all day",
            "I officially took over as tech lead of the search relevance team — 6 direct reports now",
            "My team at Flipkart has grown to 10 people with 4 new hires — I'm really enjoying the leadership role now",
        ],
        "test_tags": ["temporal", "semantic"],
        "description": "Full leadership transition arc",
    },
    {
        "id": "life_98_arjun_parents_gift",
        "query": "How did Arjun's parents help with the apartment?",
        "expected_texts": [
            "Arjun's parents gifted us 10 lakhs towards the down payment — really generous of them",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Family financial support detail",
    },
    {
        "id": "life_99_github_project",
        "query": "How was the open source project received?",
        "expected_texts": [
            "I published the benchmark tool on GitHub and it got 200 stars in the first week — someone from Elastic even commented",
            "I've started a side project on weekends — building an open-source search relevance benchmarking tool in Rust",
        ],
        "test_tags": ["semantic"],
        "description": "Side project traction",
    },
    {
        "id": "life_100_meera_flower_girl",
        "query": "What role did Meera play at the wedding?",
        "expected_texts": [
            "Meera was the flower girl and stole the show — everyone was taking photos of her in her pink lehenga",
            "Kavitha's wedding was absolutely beautiful — held at ITC Grand Chola in Chennai, 400 guests",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Event detail recall with cross-entity context",
    },
]


def _deterministic_vec(seed: float, dim: int) -> list[float]:
    """Generate a deterministic unit vector from a seed value."""
    raw = [(seed + i) * 0.1 + math.sin(seed * (i + 1)) * 0.3 for i in range(dim)]
    norm = math.sqrt(sum(x * x for x in raw))
    if norm == 0:
        raw[0] = 1.0
        norm = 1.0
    return [x / norm for x in raw]


# ── Procedural Memory Generator ─────────────────────────────────────────────
# Generates ~15,000 realistic daily-life memories from templates.
# Each domain has templates with slots filled by random choices.
# Memories are distributed across the 540-day (18-month) timeline.

# Template format: (text_template, memory_type, importance, valence, entity_mode)
# entity_mode: "person" = use person, "person_tech" = use person+tech, "new_person" = use new_person, None = no entities
_WORK_TEMPLATES = [
    ("Today's standup: {person} is working on {task}, I'm continuing {my_task}", "episodic", 0.3, 0.1, "person"),
    ("Had a productive code review with {person} on the {component} service", "episodic", 0.3, 0.2, "person"),
    ("Spent the morning debugging a {issue_type} in the {component} module", "episodic", 0.3, -0.2, None),
    ("Merged PR #{pr_num}: {pr_desc}", "episodic", 0.3, 0.2, None),
    ("Attended {meeting_type} meeting — discussed {topic}", "episodic", 0.2, 0.0, None),
    ("{person} raised a good point about {concern} in today's design review", "episodic", 0.3, 0.1, "person"),
    ("Completed the {task} implementation, tests passing with {coverage}% coverage", "episodic", 0.4, 0.3, None),
    ("The {component} deploy went smoothly, monitoring dashboards look clean", "episodic", 0.3, 0.3, None),
    ("Got a Slack message from {person} about a {severity} issue in {component}", "episodic", 0.4, -0.3, "person"),
    ("Wrote documentation for the {component} API — {pages} pages covering all endpoints", "episodic", 0.2, 0.1, None),
    ("Onboarded {new_person} today — showed them our codebase and development workflow", "episodic", 0.3, 0.2, "new_person"),
    ("Infrastructure cost review: our {component} cluster costs {cost} per month", "semantic", 0.3, -0.1, None),
    ("Learned about {tech} from a tech talk by {person} — might be useful for our {component}", "episodic", 0.3, 0.2, "person_tech"),
    ("Sprint planning: picked up {num_tasks} tasks for this sprint, estimated {hours} hours total", "episodic", 0.2, 0.0, None),
    ("1-on-1 with {person} — discussed their career growth and upcoming project allocation", "episodic", 0.4, 0.2, "person"),
]

_WORK_PEOPLE = ["Deepa", "Karan", "Neha", "Vikram", "Rohit", "Aditya", "Priyanka", "Suresh", "Megha", "Rishi"]
_WORK_COMPONENTS = ["search ranking", "indexer", "query parser", "recommendation", "catalog", "user profile",
                     "analytics", "caching layer", "API gateway", "batch pipeline", "feature store", "monitoring"]
_WORK_TASKS = ["query latency optimization", "embedding cache warmup", "relevance model fine-tuning",
               "data pipeline refactoring", "load balancer config", "rate limiter update", "schema migration",
               "logging cleanup", "unit test coverage", "integration test fixes", "performance benchmark",
               "memory leak investigation", "error handling improvements", "API versioning"]
_WORK_ISSUE_TYPES = ["memory leak", "race condition", "timeout", "null pointer", "cache invalidation",
                     "data inconsistency", "deadlock", "performance regression", "encoding bug"]
_WORK_MEETING_TYPES = ["sprint planning", "design review", "architecture", "incident review", "all-hands",
                       "backlog grooming", "tech debt review", "cross-team sync"]
_WORK_TOPICS = ["search latency SLAs", "model serving costs", "feature flag rollout strategy",
                "data quality monitoring", "on-call rotation", "hiring pipeline", "Q2 roadmap",
                "dependency upgrades", "cloud migration timeline", "A/B test results"]
_WORK_TECHS = ["gRPC", "Kafka", "Redis Cluster", "ClickHouse", "DuckDB", "ONNX Runtime", "vLLM",
               "Ray Serve", "Argo Workflows", "Temporal", "Prometheus", "OpenTelemetry"]

# entity_mode: "activity"=Meera+activity, "friend"=Meera+friend, "place"=Meera+place, None=no entities
_MEERA_TEMPLATES = [
    ("Meera {activity} today — she's getting so much better at it", "episodic", 0.4, 0.6, "activity"),
    ("Meera said something funny today: '{saying}'", "episodic", 0.3, 0.7, None),
    ("Picked up Meera from {school} — she was {mood} about {school_event}", "episodic", 0.3, 0.3, None),
    ("Meera refused to eat {food} again — only wants {fav_food}", "episodic", 0.2, -0.1, None),
    ("Read '{book}' to Meera before bedtime — she asked to read it {count} times", "episodic", 0.2, 0.5, None),
    ("Meera had a playdate with {friend} at {place}", "episodic", 0.2, 0.4, "friend"),
    ("Meera drew a picture of {subject} today — Arjun framed it for his desk", "episodic", 0.3, 0.7, None),
    ("Meera woke up crying at {time} — might be teething again", "episodic", 0.2, -0.3, None),
    ("Took Meera to {place} this weekend — she loved the {attraction}", "episodic", 0.3, 0.6, "place"),
    ("Meera's {school} teacher said she's been {behavior} this week", "episodic", 0.3, 0.2, None),
]

_MEERA_ACTIVITIES = ["practiced writing the alphabet", "built a tower with blocks", "tried to tie her own shoes",
                     "drew circles and squares", "sang a nursery rhyme perfectly", "learned to use scissors",
                     "counted to 30 without help", "told a story about a rabbit", "jumped on one foot",
                     "helped me water the plants", "sorted her toys by color", "rode her tricycle"]
_MEERA_SAYINGS = ["Amma, the moon is following us!", "Why do dogs go woof?", "I want to be a doctor like Rahul uncle",
                  "Can we have dosa for every meal?", "The clouds look like elephants today",
                  "Thatha told me I'm the smartest", "Can I come to your office Amma?"]
_MEERA_FRIENDS = ["Ananya", "Riya", "Arav", "Ishaan", "Zara", "Tara", "Aisha"]
_MEERA_BOOKS = ["Goodnight Moon", "The Very Hungry Caterpillar", "Peppa Pig", "Elmer the Elephant",
                "Brown Bear Brown Bear", "Room on the Broom", "Dear Zoo"]
_MEERA_PLACES = ["Lalbagh Botanical Garden", "Cubbon Park", "the children's museum", "the aquarium",
                 "Nandi Hills", "the zoo", "Forum Mall play area"]

# entity_mode: "run"=Priya+Cubbon Park, "yoga"=Priya+Lakshmi, "drmenon"=Priya+Dr.Menon, "sanjay"=Priya+Sanjay
_FITNESS_TEMPLATES = [
    ("Morning run: {distance}km in {minutes} minutes at Cubbon Park — {feeling}", "episodic", 0.3, 0.4, "run"),
    ("{exercise} session today — {sets} sets, feeling {feeling}", "episodic", 0.2, 0.3, None),
    ("Yoga class with Lakshmi — focused on {pose_type} today", "episodic", 0.2, 0.4, "yoga"),
    ("Slept {hours} hours last night — {sleep_quality}", "episodic", 0.2, 0.0, None),
    ("Step count today: {steps} — {comparison} my weekly average", "episodic", 0.1, 0.1, None),
    ("Tried a new {food_type} smoothie recipe: {ingredients}", "episodic", 0.2, 0.3, None),
    ("Back exercises from Dr. Menon: {exercise_set}, {reps} reps each", "procedural", 0.3, 0.1, "drmenon"),
    ("Ran with Sanjay this morning — he's training for the full marathon now", "episodic", 0.2, 0.3, "sanjay"),
    ("Rest day today — did some light stretching and foam rolling instead", "episodic", 0.1, 0.2, None),
    ("Monthly weight check: {weight}kg — {trend} from last month", "episodic", 0.2, 0.0, None),
]

# entity_mode: "kavitha", "parents", "arjun", "call_person", "sanjay", None
_SOCIAL_TEMPLATES = [
    ("Coffee with Kavitha at {cafe} — she told me about {topic}", "episodic", 0.3, 0.5, "kavitha"),
    ("Video call with Amma and Appa — Appa showed me his {activity}", "episodic", 0.3, 0.4, "parents"),
    ("Dinner with {couple} at {restaurant} — great {cuisine} food", "episodic", 0.3, 0.4, None),
    ("Arjun and I had a date night at {restaurant} — first time out without Meera in weeks", "episodic", 0.4, 0.6, "arjun"),
    ("Called {person} to catch up — they're {news}", "episodic", 0.2, 0.3, "call_person"),
    ("Attended {event} at {place} — met some interesting people", "episodic", 0.3, 0.3, None),
    ("Arjun's colleague {person} and family came over for dinner — kids played together", "episodic", 0.2, 0.3, None),
    ("{person} sent me a {item} recommendation — adding to my list", "episodic", 0.1, 0.2, None),
    ("Weekend brunch with the running group at {cafe}", "episodic", 0.2, 0.4, "sanjay"),
    ("Amma's birthday next week — need to order the {gift} she wanted", "episodic", 0.3, 0.3, None),
]

_SOCIAL_CAFES = ["Third Wave Coffee", "Blue Tokai", "Matteo Coffea", "Dyu Art Cafe", "Starbucks Koramangala",
                 "Hatti Kaapi", "Cafe Pascucci"]
_SOCIAL_RESTAURANTS = ["Truffles", "Toit", "Vidyarthi Bhavan", "Meghana Foods", "The Only Place",
                       "Corner House", "Empire Restaurant", "MTR", "Nagarjuna", "Brahmin's Coffee Bar"]
_SOCIAL_PEOPLE = ["Nisha", "Ankit", "Shreya", "Vinay", "Preeti", "Karthik", "Divya", "Sachin"]
_SOCIAL_EVENTS = ["a tech meetup", "a Diwali party", "a book club meeting", "a neighborhood potluck",
                  "a startup demo day", "a charity run", "a music concert", "a parent-teacher meeting"]

_COOKING_TEMPLATES = [
    ("Made {dish} for dinner tonight — {result}", "episodic", 0.2, 0.3, None),
    ("Tried {person}'s recipe for {dish} — {verdict}", "episodic", 0.2, 0.3, None),
    ("Ordered groceries from BigBasket: {items}", "episodic", 0.1, 0.0, None),
    ("Meal prep Sunday: made {dishes} for the week", "procedural", 0.2, 0.2, None),
    ("Arjun cooked {dish} today — he's getting better at South Indian cooking", "episodic", 0.2, 0.4, None),
    ("Discovered a great recipe for {dish} from {source}", "episodic", 0.2, 0.3, None),
]

_DISHES = ["sambar rice", "rasam", "idli", "dosa", "curd rice", "pongal", "upma", "paneer butter masala",
           "aloo gobi", "dal tadka", "biryani", "pulao", "roti with dal", "pasta arrabiata",
           "mushroom curry", "palak paneer", "rajma chawal", "khichdi", "poha", "uttapam"]

_FINANCE_TEMPLATES = [
    ("Paid the {bill} bill: {amount} this month", "episodic", 0.2, -0.1, None),
    ("SIP investment done: {amount} into the {fund} fund", "episodic", 0.2, 0.1, None),
    ("Unexpected expense: {item} cost {amount} — wasn't in the budget", "episodic", 0.3, -0.3, None),
    ("Credit card statement: spent {amount} this month, {category} was the biggest category", "episodic", 0.2, -0.1, None),
    ("Meera's school fees for the term: {amount}", "episodic", 0.3, -0.1, None),
    ("Got {amount} tax refund — putting it into the apartment down payment savings", "episodic", 0.3, 0.4, None),
    ("Insurance premium due: {amount} for {type} insurance", "episodic", 0.2, -0.1, None),
    ("Compared home loan rates: HDFC at {rate1}%, SBI at {rate2}%, ICICI at {rate3}%", "semantic", 0.3, 0.0, None),
]

_ENTERTAINMENT_TEMPLATES = [
    ("Watched '{title}' on {platform} — {review}", "episodic", 0.2, 0.3, None),
    ("Listening to {podcast} podcast — today's episode was about {topic}", "episodic", 0.1, 0.2, None),
    ("Finished reading '{book}' — {review}", "episodic", 0.3, 0.3, "book"),
    ("Started watching '{show}' that {person} recommended — {verdict} so far", "episodic", 0.2, 0.2, None),
    ("Meera and I watched {movie} together — she loved the {element}", "episodic", 0.2, 0.5, None),
    ("Played {game} with Arjun after Meera went to bed — nice way to unwind", "episodic", 0.1, 0.4, None),
]

_WEATHER_TEMPLATES = [
    ("Bangalore weather today: {temp}°C, {condition} — {reaction}", "episodic", 0.1, 0.0, None),
    ("Heavy rain caused traffic on Outer Ring Road — took {minutes} minutes to reach office", "episodic", 0.1, -0.3, None),
    ("Perfect running weather this morning — {temp}°C and breezy", "episodic", 0.1, 0.3, None),
    ("Power cut for {hours} hours today — had to work from the {backup}", "episodic", 0.2, -0.3, None),
]

_ERRANDS_TEMPLATES = [
    ("Dropped off Meera at {school}, then stopped at {store} for {items}", "episodic", 0.1, 0.0, None),
    ("Car service at {garage} — {service_type}, cost {amount}", "episodic", 0.2, -0.1, None),
    ("Amazon delivery arrived: {item} that I ordered {days} days ago", "episodic", 0.1, 0.2, None),
    ("Plumber came to fix the {issue} in the {room} — finally working properly", "episodic", 0.2, 0.2, None),
    ("Picked up dry cleaning and stopped at the pharmacy for {medicine}", "episodic", 0.1, 0.0, None),
    ("Renewed Meera's library card at the {library}", "episodic", 0.1, 0.1, None),
]

# entity_mode: "learn_topic" = Priya+topic
_LEARNING_TEMPLATES = [
    ("Read an interesting article about {topic} on {source}", "episodic", 0.2, 0.2, "learn_topic"),
    ("Watched a {platform} video on {topic} — useful for the {project}", "episodic", 0.2, 0.2, None),
    ("Completed module {num} of the {course} course — {progress}", "episodic", 0.2, 0.3, None),
    ("Interesting paper: '{paper}' — relevant to our search ranking work", "episodic", 0.3, 0.2, None),
    ("Practiced {language} on Duolingo — {streak} day streak now", "episodic", 0.1, 0.2, None),
]

_REFLECTIVE_TEMPLATES = [
    ("Feeling {mood} today — {reason}", "episodic", 0.3, None, None),  # valence set dynamically
    ("Grateful for: {gratitude}", "episodic", 0.3, 0.6, None),
    ("Need to remember: {reminder}", "episodic", 0.4, 0.0, None),
    ("Goal for this month: {goal}", "episodic", 0.3, 0.2, None),
    ("Noticed that {observation} — something to think about", "episodic", 0.2, 0.0, None),
]


def _fill_work_template(template, rng, day):
    """Fill work template slots with random values."""
    text, mtype, imp, val, entity_mode = template
    person = rng.choice(_WORK_PEOPLE)
    component = rng.choice(_WORK_COMPONENTS)
    task = rng.choice(_WORK_TASKS)
    new_person = rng.choice(["Amit", "Swati", "Farhan", "Lakshmi", "Raju", "Tanvi"])
    tech = rng.choice(_WORK_TECHS)

    filled = text.format(
        person=person, task=task, my_task=rng.choice(_WORK_TASKS),
        component=component, issue_type=rng.choice(_WORK_ISSUE_TYPES),
        pr_num=rng.randint(100, 9999),
        pr_desc=f"{rng.choice(['fix', 'add', 'update', 'refactor'])} {component} {rng.choice(['endpoint', 'handler', 'config', 'tests'])}",
        meeting_type=rng.choice(_WORK_MEETING_TYPES),
        topic=rng.choice(_WORK_TOPICS), coverage=rng.randint(70, 98),
        severity=rng.choice(["P0", "P1", "P2"]),
        pages=rng.randint(3, 15), cost=f"${rng.randint(500, 5000)}",
        tech=tech, new_person=new_person,
        num_tasks=rng.randint(3, 8), hours=rng.randint(15, 40),
        concern=rng.choice(["latency budget", "error rate", "data freshness", "cost", "security"]),
    )
    if entity_mode == "person":
        entities = [("Priya", person, "works_with")]
    elif entity_mode == "new_person":
        entities = [("Priya", new_person, "onboarded")]
    elif entity_mode == "person_tech":
        entities = [("Priya", tech, "learned_about")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_meera_template(template, rng, day):
    """Fill Meera-related template slots."""
    text, mtype, imp, val, entity_mode = template
    activity = rng.choice(_MEERA_ACTIVITIES)
    friend = rng.choice(_MEERA_FRIENDS)
    place = rng.choice(_MEERA_PLACES)

    filled = text.format(
        activity=activity, saying=rng.choice(_MEERA_SAYINGS),
        school="Kangaroo Kids", mood=rng.choice(["excited", "happy", "tired", "cranky"]),
        school_event=rng.choice(["art class", "story time", "outdoor play", "music class"]),
        food=rng.choice(["vegetables", "dal", "rice", "chapati"]),
        fav_food=rng.choice(["dosa", "idli", "pasta", "cheese toast"]),
        book=rng.choice(_MEERA_BOOKS), count=rng.choice(["two", "three", "four"]),
        friend=friend, place=place,
        subject=rng.choice(["our family", "a rainbow", "Cubbon Park", "a butterfly", "our dog (we don't have one)"]),
        time=f"{rng.randint(1, 4)}am",
        attraction=rng.choice(["butterflies", "fish", "slides", "birds", "train ride"]),
        behavior=rng.choice(["very social", "a bit quiet", "super creative", "very helpful", "learning fast"]),
    )
    if entity_mode == "activity":
        entities = [("Meera", activity, "doing")]
    elif entity_mode == "friend":
        entities = [("Meera", friend, "plays_with")]
    elif entity_mode == "place":
        entities = [("Meera", place, "visited")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_fitness_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        distance=round(rng.uniform(3, 10), 1),
        minutes=rng.randint(18, 60),
        feeling=rng.choice(["great pace", "a bit sluggish", "strong finish", "legs felt heavy", "best in weeks"]),
        exercise=rng.choice(["Strength training", "HIIT", "Core workout", "Swimming", "Cycling"]),
        sets=rng.randint(3, 5),
        pose_type=rng.choice(["hip openers", "backbends", "inversions", "balance poses", "restorative"]),
        hours=round(rng.uniform(5, 9), 1),
        sleep_quality=rng.choice(["woke up refreshed", "kept waking up", "slept like a log", "Meera woke me up twice"]),
        steps=rng.randint(4000, 15000),
        comparison=rng.choice(["above", "below", "about the same as"]),
        food_type=rng.choice(["green", "berry", "mango", "banana-oat", "spinach-banana"]),
        ingredients=rng.choice(["banana, spinach, protein powder", "mango, yogurt, turmeric", "berries, oats, almond milk"]),
        exercise_set=rng.choice(["bird-dog, bridges, cat-cow", "dead bugs, wall sits, planks"]),
        reps=rng.randint(10, 20),
        weight=round(rng.uniform(54, 58), 1),
        trend=rng.choice(["up 0.5kg", "down 0.3kg", "stable"]),
    )
    if entity_mode == "run":
        entities = [("Priya", "Cubbon Park", "runs_in")]
    elif entity_mode == "yoga":
        entities = [("Priya", "Lakshmi", "yoga_teacher")]
    elif entity_mode == "drmenon":
        entities = [("Priya", "Dr. Menon", "patient_of")]
    elif entity_mode == "sanjay":
        entities = [("Priya", "Sanjay", "running_buddy")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_social_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    person = rng.choice(_SOCIAL_PEOPLE)

    filled = text.format(
        cafe=rng.choice(_SOCIAL_CAFES),
        topic=rng.choice(["her new project at Google", "Rahul's hospital shift schedule",
                          "weekend plans", "a podcast she likes", "travel plans"]),
        activity=rng.choice(["memoir progress", "garden", "new paintings", "cooking experiments"]),
        couple=rng.choice(["Nisha and Ankit", "Shreya and Vinay", "Preeti and Karthik"]),
        restaurant=rng.choice(_SOCIAL_RESTAURANTS),
        cuisine=rng.choice(["South Indian", "North Indian", "Italian", "Japanese", "Thai"]),
        person=person,
        news=rng.choice(["moving to a new house", "expecting a baby", "changing jobs",
                         "running a marathon", "launching a startup"]),
        event=rng.choice(_SOCIAL_EVENTS), place=rng.choice(["Koramangala", "Indiranagar", "HSR Layout"]),
        item=rng.choice(["book", "podcast", "movie", "restaurant", "recipe"]),
        gift=rng.choice(["silk saree", "kindle", "cooking class subscription", "spa voucher"]),
    )
    if entity_mode == "kavitha":
        entities = [("Priya", "Kavitha", "met_with")]
    elif entity_mode == "parents":
        entities = [("Priya", "Appa", "called"), ("Priya", "Amma", "called")]
    elif entity_mode == "arjun":
        entities = [("Priya", "Arjun", "date_night")]
    elif entity_mode == "call_person":
        entities = [("Priya", person, "called")]
    elif entity_mode == "sanjay":
        entities = [("Priya", "Sanjay", "met_with")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_simple_template(template, rng, day):
    """Fill a template using generic slot substitution."""
    text, mtype, imp, val, entity_mode = template

    # Track values for entity creation
    slot_values = {}
    filled = text
    for slot in ["dish", "result", "verdict", "items", "dishes", "source", "person",
                 "bill", "amount", "fund", "item", "category", "type", "rate1", "rate2", "rate3",
                 "title", "platform", "review", "podcast", "topic", "book", "show", "element",
                 "movie", "game", "temp", "condition", "reaction", "minutes", "hours", "backup",
                 "school", "store", "garage", "service_type", "days", "issue", "room", "medicine",
                 "library", "num", "course", "progress", "paper", "language", "streak",
                 "mood", "reason", "gratitude", "reminder", "goal", "observation",
                 "project"]:
        if "{" + slot + "}" in filled:
            val_str = _get_slot_value(slot, rng)
            slot_values[slot] = val_str
            filled = filled.replace("{" + slot + "}", val_str)

    if entity_mode == "book" and "book" in slot_values:
        entities = [("Priya", slot_values["book"], "read")]
    elif entity_mode == "learn_topic" and "topic" in slot_values:
        entities = [("Priya", slot_values["topic"], "learned_about")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _get_slot_value(slot, rng):
    """Return a random value for a template slot."""
    values = {
        "dish": _DISHES,
        "result": ["turned out great", "a bit overcooked", "Arjun loved it", "Meera actually ate it", "could use more salt"],
        "verdict": ["loved it", "it's okay", "not my favorite", "will definitely make again"],
        "items": ["rice, dal, vegetables, curd", "bread, eggs, milk, fruit", "spices, oil, onions, tomatoes"],
        "dishes": ["3 curries, rice, and dal", "batch of sambar and chutney", "5 days of lunch boxes"],
        "source": ["YouTube", "Hebbar's Kitchen", "a colleague"],
        "person": _SOCIAL_PEOPLE + ["Kavitha", "Arjun"],
        "bill": ["electricity", "internet", "water", "gas", "mobile"],
        "amount": [f"{rng.randint(500, 50000)}", f"{rng.randint(1, 15)},000", f"{rng.randint(200, 5000)}"],
        "fund": ["Nifty 50 index", "large cap equity", "debt", "ELSS tax-saver"],
        "item": ["new headphones", "Meera's shoes", "kitchen appliance", "office chair cushion", "water filter"],
        "category": ["dining out", "groceries", "shopping", "transport", "medical"],
        "type": ["health", "life", "car", "home"],
        "rate1": [f"{round(rng.uniform(8.0, 9.5), 1)}"], "rate2": [f"{round(rng.uniform(8.0, 9.5), 1)}"],
        "rate3": [f"{round(rng.uniform(8.0, 9.5), 1)}"],
        "title": ["The Bear S3", "Panchayat", "3 Body Problem", "Kota Factory", "Beef", "Dark", "Succession"],
        "platform": ["Netflix", "Prime Video", "Hotstar", "Apple TV", "YouTube"],
        "review": ["really enjoyed it", "meh, overrated", "mind-blowing", "good but slow", "binged the whole thing"],
        "podcast": ["Lex Fridman", "Huberman Lab", "The Tim Ferriss Show", "Practical AI", "Software Engineering Daily"],
        "topic": ["LLM scaling laws", "sleep optimization", "startup funding in India", "distributed systems", "parenting"],
        "book": ["Atomic Habits", "Deep Work", "Project Hail Mary", "Thinking Fast and Slow", "The Design of Everyday Things"],
        "show": ["The Bear", "Panchayat S3", "3 Body Problem", "Kota Factory"],
        "element": ["funny animals", "the songs", "the princess", "the robot"],
        "movie": ["Frozen 2", "Moana", "Coco", "Finding Nemo"],
        "game": ["Catan", "chess", "Scrabble", "card games"],
        "temp": [f"{rng.randint(18, 34)}"],
        "condition": ["sunny and clear", "overcast with drizzle", "heavy monsoon rain", "pleasant and breezy", "cloudy"],
        "reaction": ["perfect for a walk", "stayed home", "got caught without an umbrella", "opened all windows"],
        "minutes": [f"{rng.randint(30, 120)}"], "hours": [f"{rng.randint(1, 4)}"],
        "backup": ["nearest coffee shop with wifi", "phone hotspot", "co-working space"],
        "school": ["Kangaroo Kids"],
        "store": ["BigBasket hub", "More Supermarket", "DMart", "the pharmacy"],
        "garage": ["Bosch Service Center", "the local mechanic"],
        "service_type": ["oil change and tire rotation", "AC service", "brake pad replacement", "general checkup"],
        "days": [f"{rng.randint(2, 7)}"],
        "issue": ["leaking tap", "blocked drain", "running toilet"],
        "room": ["kitchen", "bathroom", "master bedroom"],
        "medicine": ["Meera's vitamins", "my naproxen refill", "Arjun's allergy meds"],
        "library": ["British Council Library", "Just Books", "local public library"],
        "num": [f"{rng.randint(3, 12)}"],
        "course": ["MLOps", "System Design", "Advanced Rust", "Kubernetes"],
        "progress": ["halfway done", "almost finished", "just started"],
        "paper": ["Attention Is All You Need revisited", "Scaling laws for search relevance",
                  "Efficient transformer distillation"],
        "language": ["Kannada", "Japanese", "French"],
        "streak": [f"{rng.randint(5, 120)}"],
        "mood": ["content", "overwhelmed", "energized", "anxious", "peaceful", "frustrated", "grateful", "tired"],
        "reason": ["work went well today", "Meera was so sweet this morning",
                   "too many meetings drained me", "missing my parents",
                   "excited about the apartment", "tired from poor sleep"],
        "gratitude": ["Arjun making coffee for me every morning",
                     "Meera's laugh when I tickle her", "having a job I enjoy",
                     "Kavitha always being there", "living in a city with great weather",
                     "Appa recovering so well"],
        "reminder": ["schedule Meera's dentist appointment", "call Amma about the Bangalore move",
                    "review the home loan documents", "update my LinkedIn after the promotion",
                    "order birthday gift for Arjun", "renew car insurance by month end"],
        "goal": ["run 5K without stopping", "read 2 books", "ship the design doc",
                "spend one screen-free weekend", "cook a new recipe every week"],
        "observation": ["I'm much happier when I run in the morning",
                       "Meera is more cooperative when she gets enough sleep",
                       "I spend too much time in meetings now as tech lead",
                       "Arjun and I need more date nights"],
    }
    options = values.get(slot, [slot])
    return rng.choice(options)


def generate_daily_memories(target_count: int = 15000, seed: int = 42):
    """Generate target_count realistic daily-life memories.

    Returns a list of dicts, each with:
        text, type, importance, valence, entities, day_offset
    """
    rng = random.Random(seed)
    memories = []
    total_days = 540  # 18 months

    # Domain weights (how many memories per day on average)
    # Total ~28 memories/day * 540 days = ~15,120
    domain_schedule = [
        ("work", _WORK_TEMPLATES, _fill_work_template, 8),
        ("meera", _MEERA_TEMPLATES, _fill_meera_template, 4),
        ("fitness", _FITNESS_TEMPLATES, _fill_fitness_template, 3),
        ("social", _SOCIAL_TEMPLATES, _fill_social_template, 2),
        ("cooking", _COOKING_TEMPLATES, None, 3),
        ("finance", _FINANCE_TEMPLATES, None, 1),
        ("entertainment", _ENTERTAINMENT_TEMPLATES, None, 2),
        ("weather", _WEATHER_TEMPLATES, None, 1),
        ("errands", _ERRANDS_TEMPLATES, None, 2),
        ("learning", _LEARNING_TEMPLATES, None, 1),
        ("reflective", _REFLECTIVE_TEMPLATES, None, 1),
    ]

    # Calculate per-day rates to hit target
    total_per_day = sum(count for _, _, _, count in domain_schedule)
    # Effective working days (work skips ~85% of weekends)
    effective_days = total_days - int((total_days / 7) * 2 * 0.85)  # ~408 work days
    # But non-work domains run all 540 days
    expected_raw = total_per_day * total_days - 8 * int((total_days / 7) * 2 * 0.85)
    scale = target_count / max(expected_raw, 1)

    for day in range(total_days):
        for domain_name, templates, filler, base_count in domain_schedule:
            # Skip weekends for work (roughly)
            if domain_name == "work" and day % 7 in (5, 6):
                if rng.random() > 0.15:
                    continue

            # Probabilistic count: floor + random chance for fractional part
            expected = base_count * scale
            count = int(expected)
            if rng.random() < (expected - count):
                count += 1
            for _ in range(count):
                template = rng.choice(templates)
                if filler:
                    text, mtype, imp, val, entities = filler(template, rng, day)
                else:
                    text, mtype, imp, val, entities = _fill_simple_template(template, rng, day)

                # Dynamic valence for reflective mood entries
                if val is None:
                    val = round(rng.uniform(-0.5, 0.7), 2)

                # Add slight random variation to importance
                imp = max(0.1, min(1.0, imp + rng.uniform(-0.1, 0.1)))

                memories.append({
                    "text": text,
                    "type": mtype,
                    "importance": round(imp, 2),
                    "valence": round(val, 2),
                    "entities": entities,
                    "day_offset": day,
                })

    # Shuffle slightly (within 3-day windows) to avoid perfect ordering
    for i in range(len(memories) - 1, 0, -1):
        j = rng.randint(max(0, i - 20), i)
        memories[i], memories[j] = memories[j], memories[i]

    # Trim or pad to target
    if len(memories) > target_count:
        memories = memories[:target_count]

    return memories


def load_life_into_db(db, embedder=None, dim: int = 384, base_time: float | None = None,
                      target_count: int = 15000, progress_callback=None):
    """Load Priya's full life history into a YantrikDB instance.

    Loads ~105 hand-crafted anchor memories (used by golden queries) plus
    ~target_count procedurally generated daily-life memories.

    Args:
        db: YantrikDB instance.
        embedder: Optional SentenceTransformer (or any .encode(str) object).
        dim: Embedding dimension (used for deterministic vectors when no embedder).
        base_time: Base unix timestamp. Defaults to 540 days ago (18 months).
        target_count: Number of generated daily memories to add (default 15000).
        progress_callback: Optional callable(loaded, total) for progress reporting.

    Returns:
        (text_to_rid, text_to_seed) — dicts mapping memory text to RID and seed.
    """
    if base_time is None:
        base_time = time.time() - (540 * 86400)

    text_to_rid = {}
    text_to_seed = {}
    seed_counter = 1.0

    # ── Phase 1: Load anchor memories (hand-crafted, used by golden queries) ──
    anchor_count = sum(len(s["memories"]) for s in LIFE_SESSIONS)
    loaded = 0

    for session in LIFE_SESSIONS:
        session_time = base_time + (session["time_offset_days"] * 86400)

        for i, mem in enumerate(session["memories"]):
            if embedder is not None:
                vec = embedder.encode(mem["text"])
                embedding = vec.tolist() if hasattr(vec, "tolist") else list(vec)
            else:
                embedding = _deterministic_vec(seed_counter, dim)
                text_to_seed[mem["text"]] = seed_counter
                seed_counter += 1.0

            rid = db.record(
                text=mem["text"],
                memory_type=mem["type"],
                importance=mem["importance"],
                valence=mem["valence"],
                embedding=embedding,
            )

            text_to_rid[mem["text"]] = rid

            # Backdate to simulate time passage
            db._conn.execute(
                "UPDATE memories SET created_at = ?, updated_at = ?, last_access = ? WHERE rid = ?",
                (session_time + i, session_time + i, session_time + i, rid),
            )

            # Create entity relationships and link memory to entities
            for src, dst, rel_type in mem["entities"]:
                db.relate(src, dst, rel_type=rel_type)
                db.link_memory_entity(rid, src)
                db.link_memory_entity(rid, dst)

            loaded += 1
            if progress_callback and loaded % 50 == 0:
                progress_callback(loaded, anchor_count + target_count)

    db._conn.commit()

    # ── Phase 2: Generate and load daily-life memories ──
    if target_count > 0:
        generated = generate_daily_memories(target_count=target_count)
        batch_size = 200  # Commit in batches for performance

        for idx, mem in enumerate(generated):
            mem_time = base_time + (mem["day_offset"] * 86400) + (idx % 86400)

            if embedder is not None:
                vec = embedder.encode(mem["text"])
                embedding = vec.tolist() if hasattr(vec, "tolist") else list(vec)
            else:
                embedding = _deterministic_vec(seed_counter, dim)
                seed_counter += 1.0

            rid = db.record(
                text=mem["text"],
                memory_type=mem["type"],
                importance=mem["importance"],
                valence=mem["valence"],
                embedding=embedding,
            )

            # Backdate
            db._conn.execute(
                "UPDATE memories SET created_at = ?, updated_at = ?, last_access = ? WHERE rid = ?",
                (mem_time, mem_time, mem_time, rid),
            )

            # Create entities (only for memories that have them — many don't)
            for src, dst, rel_type in mem["entities"]:
                db.relate(src, dst, rel_type=rel_type)
                db.link_memory_entity(rid, src)
                db.link_memory_entity(rid, dst)

            loaded += 1
            if progress_callback and loaded % 500 == 0:
                progress_callback(loaded, anchor_count + target_count)

            # Periodic commit for performance
            if (idx + 1) % batch_size == 0:
                db._conn.commit()

        db._conn.commit()

    return text_to_rid, text_to_seed


def count_anchor_memories():
    """Count hand-crafted anchor memories."""
    return sum(len(s["memories"]) for s in LIFE_SESSIONS)


def evaluate_life(db, text_to_rid, top_k=10, embedder=None, text_to_seed=None, dim=384):
    """Run all life queries and measure recall quality.

    Returns a formatted report string and raw results.
    """
    results = []
    total_recall = 0.0
    total_precision = 0.0
    total_mrr = 0.0

    tag_scores: dict[str, list[float]] = {}

    for gq in LIFE_QUERIES:
        if embedder is not None:
            vec = embedder.encode(gq["query"])
            query_embedding = vec.tolist() if hasattr(vec, "tolist") else list(vec)
        elif text_to_seed:
            # Use average of expected text seeds as query vector (rough approximation)
            seeds = []
            for et in gq["expected_texts"]:
                if et in text_to_seed:
                    seeds.append(text_to_seed[et])
            if seeds:
                avg_seed = sum(seeds) / len(seeds)
                query_embedding = _deterministic_vec(avg_seed + 0.01, dim)
            else:
                query_embedding = _deterministic_vec(0.5, dim)
        else:
            query_embedding = _deterministic_vec(0.5, dim)

        recall_results = db.recall(
            query=gq["query"],
            query_embedding=query_embedding,
            top_k=top_k,
            skip_reinforce=True,
            expand_entities=True,
        )

        retrieved_texts = [r["text"] for r in recall_results]
        retrieved_rids = [r["rid"] for r in recall_results]

        expected_rids = {text_to_rid[t] for t in gq["expected_texts"] if t in text_to_rid}

        # Build covered set including consolidation provenance
        covered_rids = set(retrieved_rids)
        for r in recall_results:
            consolidated_from = r.get("metadata", {}).get("consolidated_from", [])
            covered_rids.update(consolidated_from)

        hits = [t for t in gq["expected_texts"] if text_to_rid.get(t) in covered_rids]
        misses = [t for t in gq["expected_texts"] if text_to_rid.get(t) not in covered_rids]

        recall_at_k = len(hits) / len(gq["expected_texts"]) if gq["expected_texts"] else 0.0

        relevant_retrieved = sum(
            1 for r in recall_results
            if r["rid"] in expected_rids
            or any(src in expected_rids for src in r.get("metadata", {}).get("consolidated_from", []))
        )
        precision_at_k = relevant_retrieved / len(recall_results) if recall_results else 0.0

        reciprocal_rank = 0.0
        for rank, r in enumerate(recall_results, 1):
            is_relevant = r["rid"] in expected_rids or any(
                src in expected_rids for src in r.get("metadata", {}).get("consolidated_from", [])
            )
            if is_relevant:
                reciprocal_rank = 1.0 / rank
                break

        total_recall += recall_at_k
        total_precision += precision_at_k
        total_mrr += reciprocal_rank

        for tag in gq["test_tags"]:
            tag_scores.setdefault(tag, []).append(recall_at_k)

        results.append({
            "id": gq["id"],
            "query": gq["query"],
            "description": gq["description"],
            "recall": recall_at_k,
            "precision": precision_at_k,
            "mrr": reciprocal_rank,
            "hits": len(hits),
            "expected": len(gq["expected_texts"]),
            "misses": misses,
            "top_results": [(r["text"][:60], round(r["score"], 3)) for r in recall_results[:3]],
        })

    n = len(LIFE_QUERIES)
    mean_recall = total_recall / n
    mean_precision = total_precision / n
    mean_mrr = total_mrr / n
    recall_by_tag = {tag: sum(s) / len(s) for tag, s in tag_scores.items()}

    # Format report
    lines = [
        "",
        "=" * 70,
        "  YantrikDB Life Simulation Evaluation Report",
        "=" * 70,
        "",
        f"  Memories loaded:    {count_anchor_memories()} anchor + generated",
        f"  Queries evaluated:  {n}",
        f"  Using real embedder: {embedder is not None}",
        "",
        f"  Mean Recall@{top_k}:    {mean_recall:.3f}",
        f"  Mean Precision@{top_k}: {mean_precision:.3f}",
        f"  Mean MRR:           {mean_mrr:.3f}",
        "",
        "  ── Recall by Tag ──",
    ]
    for tag, score in sorted(recall_by_tag.items()):
        bar = "#" * int(score * 20)
        lines.append(f"    {tag:15s} {score:.3f}  {bar}")

    lines.append("")
    lines.append("  ── Per Query Results ──")

    pass_count = 0
    for r in results:
        status = "PASS" if r["recall"] >= 0.5 else "FAIL"
        if status == "PASS":
            pass_count += 1
        lines.append(
            f"    [{status}] {r['id']:25s} recall={r['recall']:.2f}  "
            f"({r['hits']}/{r['expected']} found)  {r['description']}"
        )
        if r["misses"]:
            for m in r["misses"]:
                lines.append(f"           MISS: {m[:70]}...")

    lines.append("")
    lines.append(f"  Passed: {pass_count}/{n} queries ({100*pass_count/n:.0f}%)")
    lines.append("")

    # Entity graph stats
    stats = db.stats()
    lines.append("  ── System Stats ──")
    lines.append(f"    Active memories:   {stats['active_memories']}")
    lines.append(f"    Entities:          {stats['entities']}")
    lines.append(f"    Edges:             {stats['edges']}")
    lines.append(f"    Vec index entries: {stats['vec_index_entries']}")
    lines.append(f"    Open conflicts:    {stats['open_conflicts']}")
    lines.append(f"    Active patterns:   {stats['active_patterns']}")
    lines.append("")

    report = "\n".join(lines)
    return report, results, {
        "mean_recall": mean_recall,
        "mean_precision": mean_precision,
        "mean_mrr": mean_mrr,
        "recall_by_tag": recall_by_tag,
        "pass_rate": pass_count / n,
    }


def run_life_simulation(use_embedder=False, run_think=True, top_k=10,
                        target_count=15000):
    """Run the complete life simulation end-to-end.

    Args:
        use_embedder: If True, loads sentence-transformers for real embeddings.
        run_think: If True, runs the cognition loop after loading.
        top_k: Number of results per query.
        target_count: Number of generated daily memories (default 15000).

    Returns:
        (report_string, raw_results, metrics_dict)
    """
    from yantrikdb import YantrikDB

    embedder = None
    dim = 8  # Small dim for deterministic mode

    if use_embedder:
        try:
            from sentence_transformers import SentenceTransformer
            embedder = SentenceTransformer("all-MiniLM-L6-v2")
            dim = 384
            print("  Loaded sentence-transformers embedder (dim=384)")
        except ImportError:
            print("  sentence-transformers not installed, using deterministic vectors")
            use_embedder = False

    total_target = count_anchor_memories() + target_count
    print(f"\n  Creating YantrikDB instance (dim={dim})...")
    db = YantrikDB(db_path=":memory:", embedding_dim=dim, embedder=embedder)

    print(f"  Loading ~{total_target} memories ({count_anchor_memories()} anchor + {target_count} generated)...")
    t0 = time.time()
    last_report = [0]

    def progress(loaded, total):
        pct = 100 * loaded / total
        if pct - last_report[0] >= 5:
            elapsed = time.time() - t0
            rate = loaded / elapsed if elapsed > 0 else 0
            print(f"    {loaded:,}/{total:,} ({pct:.0f}%) — {rate:.0f} memories/sec")
            last_report[0] = pct

    text_to_rid, text_to_seed = load_life_into_db(
        db, embedder=embedder, dim=dim,
        target_count=target_count, progress_callback=progress,
    )
    load_time = time.time() - t0
    print(f"  Loaded in {load_time:.1f}s ({total_target / load_time:.0f} memories/sec)")

    # Stats after load
    stats = db.stats()
    print(f"  Active memories: {stats['active_memories']}, Entities: {stats['entities']}, Edges: {stats['edges']}")

    if run_think:
        print("\n  Running cognition loop (think)...")
        t1 = time.time()
        think_result = db.think({
            "run_consolidation": True,
            "run_conflict_scan": True,
            "run_pattern_mining": True,
            "min_active_memories": 10,
        })
        think_time = time.time() - t1
        print(f"  Think completed in {think_time:.1f}s")
        print(f"    Triggers:      {len(think_result.get('triggers', []))}")
        print(f"    Conflicts:     {think_result.get('conflicts_found', 0)}")
        print(f"    New patterns:  {think_result.get('patterns_new', 0)}")
        print(f"    Consolidation: {think_result.get('consolidation_count', 0)}")

        # Show patterns discovered
        patterns = db.get_patterns()
        if patterns:
            print(f"\n  ── Discovered Patterns ({len(patterns)}) ──")
            for p in patterns[:5]:
                print(f"    [{p['pattern_type']}] {p['description'][:80]}...")
                print(f"      confidence={p['confidence']:.2f}, occurrences={p['occurrence_count']}")

        # Show conflicts detected
        conflicts = db.get_conflicts(status="open")
        if conflicts:
            print(f"\n  ── Open Conflicts ({len(conflicts)}) ──")
            for c in conflicts[:5]:
                print(f"    [{c['conflict_type']}] {c.get('detection_reason', 'N/A')[:80]}")

        # Show triggers
        triggers = db.get_pending_triggers(limit=5)
        if triggers:
            print(f"\n  ── Pending Triggers ({len(triggers)}) ──")
            for t in triggers:
                print(f"    [{t['trigger_type']}] urgency={t['urgency']:.2f}: {t['reason'][:80]}")

    print(f"\n  Evaluating recall quality against {len(LIFE_QUERIES)} golden queries...")
    t2 = time.time()
    report, raw_results, metrics = evaluate_life(
        db, text_to_rid, top_k=top_k,
        embedder=embedder, text_to_seed=text_to_seed, dim=dim,
    )
    eval_time = time.time() - t2
    print(f"  Evaluation completed in {eval_time:.2f}s")

    print(report)

    db.close()
    return report, raw_results, metrics


if __name__ == "__main__":
    import sys
    use_embed = "--embed" in sys.argv
    count = 15000
    for arg in sys.argv:
        if arg.startswith("--count="):
            count = int(arg.split("=")[1])
    run_life_simulation(use_embedder=use_embed, target_count=count)
