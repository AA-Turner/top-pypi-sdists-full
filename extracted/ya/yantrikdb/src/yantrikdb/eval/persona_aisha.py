"""Aisha Okafor persona for realistic YantrikDB evaluation.

A 28-year-old Nigerian surgical resident (PGY-2) at Lagos University Teaching
Hospital (LUTH), from Abuja. Spanning ~12 months across personal, professional,
family, relationship, career decisions, and London fellowship domains.

Usage:
    python -m yantrikdb.eval.persona_aisha            # quick mode (no real embedder)
    python -m yantrikdb.eval.persona_aisha --embed     # with sentence-transformers
"""

import math
import random
import time

# ── Aisha Okafor's Life History ────────────────────────────────────────────
#
# Timeline: 12 months of memories, from Month 0 (start) to Month 12.
# ~85 anchor memories across 20+ sessions.

AISHA_SESSIONS = [
    # ═══════════════════════════════════════════════════════════════
    # MONTH 0 — INITIAL INTRODUCTION
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "intro_first_meeting",
        "time_offset_days": 0,
        "memories": [
            {
                "text": "My name is Aisha Okafor, I'm 28 years old and I'm a surgical resident PGY-2 at Lagos University Teaching Hospital",
                "type": "semantic",
                "importance": 1.0,
                "valence": 0.3,
                "entities": [("Aisha", "LUTH", "works_at"), ("Aisha", "PGY-2", "residency_year")],
            },
            {
                "text": "I'm originally from Abuja but moved to Lagos for my residency at LUTH",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.2,
                "entities": [("Aisha", "Abuja", "from"), ("Aisha", "Lagos", "lives_in")],
            },
            {
                "text": "I studied medicine at the University of Ibadan, completed a 6-year MBBS program",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.4,
                "entities": [("Aisha", "University of Ibadan", "studied_at"), ("Aisha", "MBBS", "degree")],
            },
            {
                "text": "My father Emeka Okafor is a civil engineer who works on infrastructure projects, and my mother Ngozi is a pharmacist who owns Okafor Pharmacy in Wuse, Abuja",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.4,
                "entities": [("Aisha", "Emeka", "daughter_of"), ("Aisha", "Ngozi", "daughter_of"), ("Ngozi", "Okafor Pharmacy", "owns"), ("Emeka", "civil engineer", "occupation")],
            },
            {
                "text": "My older brother Ikenna is a lawyer at Clifford Chance in London, married to Amara who is an architect",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.3,
                "entities": [("Aisha", "Ikenna", "sister_of"), ("Ikenna", "Clifford Chance", "works_at"), ("Ikenna", "Amara", "married_to"), ("Ikenna", "London", "lives_in")],
            },
            {
                "text": "My boyfriend Chidi Eze is a senior backend engineer at Andela, we've been dating for 3 years",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.6,
                "entities": [("Aisha", "Chidi", "dating"), ("Chidi", "Andela", "works_at")],
            },
            {
                "text": "I live in Yaba with two roommates: Funke who is also a resident at LUTH, and Bola who is a relationship manager at GTBank",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.3,
                "entities": [("Aisha", "Yaba", "lives_in"), ("Aisha", "Funke", "roommate"), ("Aisha", "Bola", "roommate"), ("Funke", "LUTH", "works_at"), ("Bola", "GTBank", "works_at")],
            },
            {
                "text": "I drive a used Toyota Corolla to work, the commute to LUTH takes about 45 minutes on a good day",
                "type": "semantic",
                "importance": 0.4,
                "valence": -0.1,
                "entities": [("Aisha", "Toyota Corolla", "drives")],
            },
            {
                "text": "I attend the Redeemed Christian Church in Yaba most Sundays — it helps me decompress after brutal hospital weeks",
                "type": "semantic",
                "importance": 0.4,
                "valence": 0.3,
                "entities": [("Aisha", "RCCG Yaba", "attends")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 1 — WORK LIFE
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month1_work_begins",
        "time_offset_days": 20,
        "memories": [
            {
                "text": "I've been assigned to Dr. Adeyemi's general surgery team — he's strict but absolutely brilliant, one of the best surgeons in Nigeria",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.3,
                "entities": [("Aisha", "Dr. Adeyemi", "assigned_to"), ("Dr. Adeyemi", "LUTH", "surgeon_at")],
            },
            {
                "text": "I performed my first solo appendectomy today and it was successful! Dr. Adeyemi said 'clean technique' which is the highest praise from him",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.8,
                "entities": [("Aisha", "appendectomy", "performed"), ("Dr. Adeyemi", "Aisha", "praised")],
            },
            {
                "text": "The hospital backup generator failed during a procedure today — we had to use phone flashlights to finish, it was terrifying",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.7,
                "entities": [("LUTH", "generator failure", "experienced")],
            },
            {
                "text": "Working 80-hour weeks at LUTH, surviving on indomie noodles and malt drinks between shifts",
                "type": "episodic",
                "importance": 0.5,
                "valence": -0.3,
                "entities": [],
            },
            {
                "text": "Fellow resident Dr. Yusuf is my closest work friend — we share call nights and keep each other sane during long shifts",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Aisha", "Dr. Yusuf", "close_friend"), ("Dr. Yusuf", "LUTH", "resident_at")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 2 — PATIENT CASES
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month2_patient_cases",
        "time_offset_days": 50,
        "memories": [
            {
                "text": "Treated a 12-year-old boy named Taiwo who came in with peritonitis — the emergency surgery saved his life, he's recovering well",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.6,
                "entities": [("Aisha", "Taiwo", "treated"), ("Taiwo", "peritonitis", "diagnosed_with")],
            },
            {
                "text": "Lost a patient today, Mrs. Ogundimu, 68 years old, to post-operative complications from bowel obstruction — I am devastated",
                "type": "episodic",
                "importance": 0.9,
                "valence": -0.9,
                "entities": [("Aisha", "Mrs. Ogundimu", "treated"), ("Mrs. Ogundimu", "bowel obstruction", "diagnosed_with")],
            },
            {
                "text": "I'm learning laparoscopic techniques from the senior attending Dr. Funke Babatunde — she's one of the few female consultants at LUTH",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.4,
                "entities": [("Aisha", "Dr. Babatunde", "learning_from"), ("Dr. Babatunde", "LUTH", "consultant_at")],
            },
            {
                "text": "Started keeping a case journal for my surgical portfolio — documenting every interesting case with notes and diagrams",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.2,
                "entities": [("Aisha", "case journal", "keeping")],
            },
            {
                "text": "Interesting case today: removed a 3kg ovarian cyst from a 25-year-old woman — she had been told by a herbalist it was spiritual",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.3,
                "entities": [("Aisha", "ovarian cyst removal", "performed")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 3 — RELATIONSHIP / PERSONAL
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month3_relationship",
        "time_offset_days": 80,
        "memories": [
            {
                "text": "Chidi proposed that we move in together but I'm hesitant — my parents would strongly disapprove of us living together before marriage",
                "type": "episodic",
                "importance": 0.8,
                "valence": -0.2,
                "entities": [("Chidi", "Aisha", "proposed_cohabitation"), ("Aisha", "cohabitation decision", "deliberating")],
            },
            {
                "text": "Parents calling every week asking about marriage — Mama keeps saying 'Aisha, you're not getting younger, when will Chidi come and see us?'",
                "type": "episodic",
                "importance": 0.6,
                "valence": -0.3,
                "entities": [("Ngozi", "Aisha", "pressuring_marriage")],
            },
            {
                "text": "Chidi got promoted to senior backend engineer at Andela, he's now leading a team of 5 developers",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Chidi", "Andela", "promoted_at"), ("Chidi", "senior backend engineer", "role")],
            },
            {
                "text": "Chidi and I have a standing Friday date night at Yellow Chilli restaurant in Victoria Island — it's our special place",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Aisha", "Chidi", "date_night"), ("Aisha", "Yellow Chilli", "frequents")],
            },
            {
                "text": "Chidi and I celebrated our 3-year anniversary — he surprised me with a trip to Obudu Mountain Resort for the weekend",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.8,
                "entities": [("Aisha", "Chidi", "anniversary"), ("Aisha", "Obudu Mountain Resort", "visited")],
            },
            {
                "text": "Bola keeps setting me up with her GTBank colleagues for double dates — she means well but I only have eyes for Chidi",
                "type": "episodic",
                "importance": 0.3,
                "valence": 0.2,
                "entities": [("Bola", "Aisha", "social_life")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 4 — EXAM PREP
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month4_exam_prep",
        "time_offset_days": 110,
        "memories": [
            {
                "text": "I've started studying for Part 1 of the West African College of Surgeons fellowship exam — this is the biggest exam of my career so far",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.0,
                "entities": [("Aisha", "WACS Part 1", "studying_for")],
            },
            {
                "text": "My study group for WACS includes me, Funke, Dr. Yusuf, and Dr. Nkechi from the pediatric surgery department",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Aisha", "Funke", "studies_with"), ("Aisha", "Dr. Yusuf", "studies_with"), ("Aisha", "Dr. Nkechi", "studies_with"), ("Dr. Nkechi", "pediatric surgery", "department")],
            },
            {
                "text": "Using Sabiston Textbook of Surgery and Bailey & Love as my main references for the WACS exam — those books weigh more than some of my patients",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.1,
                "entities": [("Aisha", "Sabiston", "studying"), ("Aisha", "Bailey & Love", "studying")],
            },
            {
                "text": "The WACS exam is scheduled in 3 months and I'm feeling overwhelmed juggling 80-hour work weeks with studying",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.4,
                "entities": [("WACS Part 1", "3 months", "scheduled_in")],
            },
            {
                "text": "Dr. Adeyemi gave me Saturdays off to study for the WACS exam — rare kindness from him, he must believe in me",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Dr. Adeyemi", "Aisha", "supported")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 5 — FAMILY
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month5_family",
        "time_offset_days": 140,
        "memories": [
            {
                "text": "Mama visited Lagos for a week — she brought homemade chin-chin, kilishi, and ogiri from Abuja, the flat smelled like home",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("Ngozi", "Lagos", "visited"), ("Ngozi", "Aisha", "visited")],
            },
            {
                "text": "Papa is working on a bridge construction project in Calabar and has been away from home for 2 months — Mama is lonely",
                "type": "episodic",
                "importance": 0.6,
                "valence": -0.2,
                "entities": [("Emeka", "Calabar", "working_in"), ("Emeka", "bridge project", "working_on")],
            },
            {
                "text": "Ikenna sent 2 million naira from London to help renovate our parents' house in Abuja — he's always been generous",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Ikenna", "house renovation", "funded"), ("Ikenna", "Abuja house", "contributed_to")],
            },
            {
                "text": "Our family WhatsApp group 'The Okafors' is always buzzing with Mama's voice notes — she sends at least 10 a day",
                "type": "semantic",
                "importance": 0.4,
                "valence": 0.4,
                "entities": [("Ngozi", "The Okafors", "active_in")],
            },
            {
                "text": "Easter gathering in Abuja with the whole extended family — I managed to take 3 days off from LUTH, ate so much jollof rice",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Aisha", "Abuja", "visited"), ("Aisha", "Easter", "family_gathering")],
            },
            {
                "text": "Aunty Chioma cornered me at Easter dinner asking about Chidi — 'Is he Igbo? Good. When is he coming to do the introduction?'",
                "type": "episodic",
                "importance": 0.3,
                "valence": 0.1,
                "entities": [("Aunty Chioma", "Aisha", "questioning")],
            },
            {
                "text": "Papa took me aside at Easter and told me he's proud of my career — 'Surgery is not easy but you are an Okafor, we don't quit'",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("Emeka", "Aisha", "encouraged")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 6 — CAREER OPPORTUNITY
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month6_fellowship_opportunity",
        "time_offset_days": 170,
        "memories": [
            {
                "text": "An incredible opportunity has come up — a 6-month surgical fellowship at King's College Hospital in London",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.5,
                "entities": [("Aisha", "King's College Hospital", "fellowship_opportunity"), ("King's College Hospital", "London", "located_in")],
            },
            {
                "text": "Dr. Adeyemi wrote a glowing recommendation letter for my King's College fellowship application — he called me his most promising resident",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.6,
                "entities": [("Dr. Adeyemi", "Aisha", "recommended"), ("Dr. Adeyemi", "King's College Hospital", "wrote_recommendation")],
            },
            {
                "text": "The London fellowship would mean being away from Chidi, my family, and my patients for 6 months — it's a difficult decision",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.3,
                "entities": [("Aisha", "fellowship decision", "deliberating")],
            },
            {
                "text": "Ikenna is offering to host me at his flat in Canary Wharf if I get the London fellowship — he's so supportive",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [("Ikenna", "Canary Wharf", "lives_in"), ("Ikenna", "Aisha", "offering_to_host")],
            },
            {
                "text": "The fellowship application requires an IELTS score — I took the test and scored 8.5 overall, well above the requirement",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Aisha", "IELTS", "scored_8.5")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 7 — HOSPITAL CHALLENGES
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month7_hospital_challenges",
        "time_offset_days": 200,
        "memories": [
            {
                "text": "The hospital ran out of ceftriaxone and metronidazole for 3 days — we had to substitute with whatever antibiotics were available and document everything",
                "type": "episodic",
                "importance": 0.8,
                "valence": -0.6,
                "entities": [("LUTH", "drug shortage", "experienced"), ("Aisha", "antibiotic substitution", "managed")],
            },
            {
                "text": "I wrote a formal letter to LUTH hospital management about the drug supply chain failures — someone has to speak up",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.3,
                "entities": [("Aisha", "LUTH management", "wrote_to")],
            },
            {
                "text": "Dr. Babatunde started a GoFundMe for surgical supplies at LUTH and raised 8 million naira — the generosity of Nigerians abroad was incredible",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Dr. Babatunde", "GoFundMe", "organized"), ("LUTH", "surgical supplies", "funded")],
            },
            {
                "text": "NEPA wahala worse than usual this month — generator diesel costs have doubled and the hospital can barely afford to keep the lights on",
                "type": "episodic",
                "importance": 0.6,
                "valence": -0.5,
                "entities": [("LUTH", "NEPA", "power_issues"), ("LUTH", "diesel costs", "increased")],
            },
            {
                "text": "A patient's family brought bags of rice and yams as a thank-you gift after a successful surgery — the gratitude makes everything worth it",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.7,
                "entities": [],
            },
            {
                "text": "Dr. Yusuf and I did a 36-hour call shift together — we survived on garri and groundnuts from the hospital canteen",
                "type": "episodic",
                "importance": 0.4,
                "valence": -0.1,
                "entities": [("Aisha", "Dr. Yusuf", "call_shift_with")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 8 — EXAM RESULTS AND FELLOWSHIP
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month8_exam_results",
        "time_offset_days": 230,
        "memories": [
            {
                "text": "I passed the WACS Part 1 exam with distinction! We celebrated at Shiro restaurant on Victoria Island",
                "type": "episodic",
                "importance": 1.0,
                "valence": 0.9,
                "entities": [("Aisha", "WACS Part 1", "passed_with_distinction"), ("Aisha", "Shiro", "celebrated_at")],
            },
            {
                "text": "Funke also passed the WACS exam — we screamed and hugged in the hospital parking lot when results came out",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.8,
                "entities": [("Funke", "WACS", "passed")],
            },
            {
                "text": "I've been accepted for the King's College London fellowship — it starts in 4 months, this is really happening",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.7,
                "entities": [("Aisha", "King's College Hospital", "accepted_to")],
            },
            {
                "text": "Chidi is being incredibly supportive about the London fellowship but I can tell he's sad about 6 months apart",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.1,
                "entities": [("Chidi", "fellowship", "supportive_of"), ("Chidi", "long distance", "facing")],
            },
            {
                "text": "Parents are proud of the fellowship but Mama is worried about 'London changing you' — she keeps saying 'don't forget where you come from'",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.2,
                "entities": [("Ngozi", "fellowship", "worried_about"), ("Emeka", "fellowship", "proud_of")],
            },
            {
                "text": "Dr. Adeyemi told me after hearing about the fellowship acceptance: 'Come back and make Nigeria better'",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Dr. Adeyemi", "Aisha", "encouraged")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 9 — PRE-LONDON PREPARATIONS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month9_preparations",
        "time_offset_days": 260,
        "memories": [
            {
                "text": "Spent 4 hours at the British High Commission in Ikoyi for my UK visa application — the queue was insane but it got approved",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.1,
                "entities": [("Aisha", "UK visa", "obtained"), ("British High Commission", "Ikoyi", "located_in")],
            },
            {
                "text": "Buying winter clothes at Shoprite and online — I've never needed a coat before in my life, Lagos girl going to London winter",
                "type": "episodic",
                "importance": 0.4,
                "valence": 0.2,
                "entities": [("Aisha", "winter clothes", "purchasing")],
            },
            {
                "text": "Doing patient handover to Dr. Yusuf before I leave — I wrote detailed notes for each of my patients so they get proper continuity of care",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.1,
                "entities": [("Aisha", "Dr. Yusuf", "handover_to"), ("Dr. Yusuf", "patient handover", "receiving")],
            },
            {
                "text": "Last Friday date night with Chidi at Yellow Chilli before London — he gave me a gold necklace with my initial 'A' on it, I cried",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.7,
                "entities": [("Chidi", "Aisha", "gifted_necklace"), ("Aisha", "Yellow Chilli", "last_date")],
            },
            {
                "text": "Bola organized a surprise going-away party at our Yaba flat — 30 friends came, Funke made a speech that made everyone emotional",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.8,
                "entities": [("Bola", "going-away party", "organized"), ("Funke", "going-away party", "speech")],
            },
            {
                "text": "Packed my stethoscope, my surgical loupes, and 5 packs of indomie in my suitcase for London — priorities",
                "type": "episodic",
                "importance": 0.3,
                "valence": 0.3,
                "entities": [],
            },
            {
                "text": "Mama gave me a small bottle of anointing oil before I left for London — 'This will protect you in that cold country'",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.5,
                "entities": [("Ngozi", "Aisha", "blessed")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 10 — LONDON ARRIVAL
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month10_london_arrival",
        "time_offset_days": 290,
        "memories": [
            {
                "text": "Arrived at Heathrow in November — 7 degrees Celsius felt like minus 20 to me, I was shivering in my new coat",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.0,
                "entities": [("Aisha", "London", "arrived_in"), ("Aisha", "Heathrow", "arrived_at")],
            },
            {
                "text": "King's College Hospital is absolutely world-class — everything works, the power never goes out, equipment is always available",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.6,
                "entities": [("Aisha", "King's College Hospital", "started_at")],
            },
            {
                "text": "I've been assigned to Mr. James Okonkwo as my mentor at King's — he's a Nigerian-British consultant surgeon, it feels like having a piece of home here",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Aisha", "Mr. Okonkwo", "mentored_by"), ("Mr. Okonkwo", "King's College Hospital", "consultant_at")],
            },
            {
                "text": "Culture shock is real — the British understatement, queuing for absolutely everything, and the food is so bland compared to Nigerian food",
                "type": "episodic",
                "importance": 0.5,
                "valence": -0.2,
                "entities": [("Aisha", "culture shock", "experiencing")],
            },
            {
                "text": "Found a Nigerian restaurant called Mama Put in Peckham — the jollof rice tastes exactly like home, I nearly cried with the first bite",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Aisha", "Mama Put", "discovered"), ("Mama Put", "Peckham", "located_in")],
            },
            {
                "text": "Ikenna and Amara's flat in Canary Wharf is beautiful — 20th floor with a view of the Thames, a long way from our childhood home in Abuja",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.5,
                "entities": [("Ikenna", "Canary Wharf flat", "lives_in"), ("Aisha", "Ikenna", "staying_with")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 11 — LONDON PROFESSIONAL LIFE
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month11_london_professional",
        "time_offset_days": 320,
        "memories": [
            {
                "text": "I'm learning robotic surgery on the da Vinci Xi system at King's — the technology is absolutely incredible, light years ahead of what we have at LUTH",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.7,
                "entities": [("Aisha", "da Vinci Xi", "learning"), ("Aisha", "robotic surgery", "training_in")],
            },
            {
                "text": "Assisted in a complex Whipple procedure — a pancreaticoduodenectomy that took 8 hours, Mr. Okonkwo let me do the final anastomosis",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.5,
                "entities": [("Aisha", "Whipple procedure", "assisted_in"), ("Mr. Okonkwo", "Whipple procedure", "led")],
            },
            {
                "text": "Published my first case report in the British Journal of Surgery with Dr. Adeyemi as co-author — a case from my LUTH days",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.8,
                "entities": [("Aisha", "British Journal of Surgery", "published_in"), ("Dr. Adeyemi", "publication", "co-authored")],
            },
            {
                "text": "Ikenna's wife Amara is pregnant! I'm going to be an auntie — the baby is due in June",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.8,
                "entities": [("Amara", "pregnant", "is"), ("Ikenna", "Amara", "expecting_with"), ("Aisha", "auntie", "becoming")],
            },
            {
                "text": "Video calling Chidi every night at 10pm London time, 11pm Lagos time — the time difference is only 1 hour which helps",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("Aisha", "Chidi", "video_calling")],
            },
            {
                "text": "Missing Nigerian food terribly despite my Saturday visits to Mama Put in Peckham — nothing beats real homemade jollof",
                "type": "episodic",
                "importance": 0.4,
                "valence": -0.2,
                "entities": [("Aisha", "Mama Put", "visits_weekly")],
            },
            {
                "text": "Mr. Okonkwo introduced me to the other international fellows — there's a doctor from Ghana, one from Kenya, and one from Pakistan",
                "type": "episodic",
                "importance": 0.4,
                "valence": 0.3,
                "entities": [("Mr. Okonkwo", "Aisha", "introduced_fellows")],
            },
            {
                "text": "The NHS system is so organized compared to LUTH — electronic medical records, proper referral pathways, and no drug shortages",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.4,
                "entities": [("NHS", "LUTH", "compared_to")],
            },
            {
                "text": "Attended a trauma conference at the Royal College of Surgeons in London — met surgeons from 30 countries",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Aisha", "Royal College of Surgeons", "attended_conference")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 12 — DECISIONS AND FUTURE
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month12_career_decisions",
        "time_offset_days": 350,
        "memories": [
            {
                "text": "The fellowship is ending in 2 months and I have a major career decision ahead — stay in the UK or go back to Nigeria",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.0,
                "entities": [("Aisha", "career decision", "facing")],
            },
            {
                "text": "I've been offered a senior registrar position at King's College Hospital — it's prestigious but it would mean staying in the UK indefinitely",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.3,
                "entities": [("King's College Hospital", "senior registrar", "offered_to_Aisha")],
            },
            {
                "text": "Also received an offer from Reddington Hospital in Lagos — a private hospital with much better pay and facilities than LUTH",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.3,
                "entities": [("Reddington Hospital", "Aisha", "offered_position"), ("Reddington Hospital", "Lagos", "located_in")],
            },
            {
                "text": "Chidi visited London for 10 days — it was an incredible week together, we took a weekend trip to Edinburgh and walked the Royal Mile",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.9,
                "entities": [("Chidi", "London", "visited"), ("Aisha", "Edinburgh", "visited"), ("Aisha", "Chidi", "trip_together")],
            },
            {
                "text": "Chidi and I discussed our marriage timeline — we both want to get married within the next 2 years",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.5,
                "entities": [("Aisha", "Chidi", "marriage_discussion"), ("Aisha", "marriage", "planning")],
            },
            {
                "text": "Dr. Adeyemi called from Lagos asking me to come back to LUTH — he's starting a new trauma center and wants me to help build it",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.4,
                "entities": [("Dr. Adeyemi", "trauma center", "starting"), ("Dr. Adeyemi", "Aisha", "recruiting")],
            },
            {
                "text": "Applied for NHS permanent registration just to keep my options open — whether I stay or go, it's good to have the door open",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.1,
                "entities": [("Aisha", "NHS registration", "applied_for")],
            },
            {
                "text": "Mama called crying tears of joy when I told her Chidi and I are talking about marriage — 'Finally! My prayers have been answered'",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.6,
                "entities": [("Ngozi", "marriage news", "overjoyed")],
            },
            {
                "text": "I keep a list of things I want to bring back to Nigerian surgery from London — standardized checklists, surgical safety protocols, and the timeout procedure they do before every operation",
                "type": "procedural",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Aisha", "surgical protocols", "documenting")],
            },
        ],
    },
]


# ── Golden Queries for Aisha Persona ──────────────────────────────────────
# 35 queries spanning every domain of Aisha's life.

AISHA_QUERIES = [
    # ─── IDENTITY / BASIC (3) ───
    {
        "id": "aisha_01_who",
        "query": "Who is Aisha and what does she do?",
        "expected_texts": [
            "My name is Aisha Okafor, I'm 28 years old and I'm a surgical resident PGY-2 at Lagos University Teaching Hospital",
            "I'm originally from Abuja but moved to Lagos for my residency at LUTH",
        ],
        "test_tags": ["identity", "semantic"],
        "description": "Basic identity retrieval",
    },
    {
        "id": "aisha_02_family",
        "query": "Tell me about Aisha's family",
        "expected_texts": [
            "My father Emeka Okafor is a civil engineer who works on infrastructure projects, and my mother Ngozi is a pharmacist who owns Okafor Pharmacy in Wuse, Abuja",
            "My older brother Ikenna is a lawyer at Clifford Chance in London, married to Amara who is an architect",
        ],
        "test_tags": ["identity", "graph"],
        "description": "Family relationships via entity graph",
    },
    {
        "id": "aisha_03_education",
        "query": "Where did Aisha study medicine?",
        "expected_texts": [
            "I studied medicine at the University of Ibadan, completed a 6-year MBBS program",
        ],
        "test_tags": ["identity", "semantic"],
        "description": "Education background retrieval",
    },

    # ─── MEDICAL / WORK (6) ───
    {
        "id": "aisha_04_surgery_cases",
        "query": "What surgical cases has Aisha handled?",
        "expected_texts": [
            "I performed my first solo appendectomy today and it was successful! Dr. Adeyemi said 'clean technique' which is the highest praise from him",
            "Treated a 12-year-old boy named Taiwo who came in with peritonitis — the emergency surgery saved his life, he's recovering well",
            "Interesting case today: removed a 3kg ovarian cyst from a 25-year-old woman — she had been told by a herbalist it was spiritual",
        ],
        "test_tags": ["medical", "semantic"],
        "description": "Surgical case recall across sessions",
    },
    {
        "id": "aisha_05_patient_outcome",
        "query": "Did Aisha ever lose a patient?",
        "expected_texts": [
            "Lost a patient today, Mrs. Ogundimu, 68 years old, to post-operative complications from bowel obstruction — I am devastated",
        ],
        "test_tags": ["medical", "valence"],
        "description": "Traumatic patient outcome recall",
    },
    {
        "id": "aisha_06_hospital_challenges",
        "query": "What challenges does LUTH hospital face?",
        "expected_texts": [
            "The hospital ran out of ceftriaxone and metronidazole for 3 days — we had to substitute with whatever antibiotics were available and document everything",
            "The hospital backup generator failed during a procedure today — we had to use phone flashlights to finish, it was terrifying",
            "NEPA wahala worse than usual this month — generator diesel costs have doubled and the hospital can barely afford to keep the lights on",
        ],
        "test_tags": ["medical", "semantic"],
        "description": "Hospital infrastructure problems",
    },
    {
        "id": "aisha_07_dr_adeyemi",
        "query": "Who is Dr. Adeyemi and what is his relationship with Aisha?",
        "expected_texts": [
            "I've been assigned to Dr. Adeyemi's general surgery team — he's strict but absolutely brilliant, one of the best surgeons in Nigeria",
            "Dr. Adeyemi wrote a glowing recommendation letter for my King's College fellowship application — he called me his most promising resident",
            "Dr. Adeyemi told me after hearing about the fellowship acceptance: 'Come back and make Nigeria better'",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Mentor relationship across multiple sessions",
    },
    {
        "id": "aisha_08_techniques",
        "query": "What surgical techniques has Aisha learned?",
        "expected_texts": [
            "I'm learning laparoscopic techniques from the senior attending Dr. Funke Babatunde — she's one of the few female consultants at LUTH",
            "I'm learning robotic surgery on the da Vinci Xi system at King's — the technology is absolutely incredible, light years ahead of what we have at LUTH",
        ],
        "test_tags": ["medical", "semantic"],
        "description": "Skills acquisition across Lagos and London",
    },
    {
        "id": "aisha_09_drug_shortage",
        "query": "What happened with the drug shortage at the hospital?",
        "expected_texts": [
            "The hospital ran out of ceftriaxone and metronidazole for 3 days — we had to substitute with whatever antibiotics were available and document everything",
            "I wrote a formal letter to LUTH hospital management about the drug supply chain failures — someone has to speak up",
            "Dr. Babatunde started a GoFundMe for surgical supplies at LUTH and raised 8 million naira — the generosity of Nigerians abroad was incredible",
        ],
        "test_tags": ["medical", "graph"],
        "description": "Drug shortage narrative arc",
    },

    # ─── PEOPLE / GRAPH (5) ───
    {
        "id": "aisha_10_chidi",
        "query": "Who is Chidi and what does he do?",
        "expected_texts": [
            "My boyfriend Chidi Eze is a senior backend engineer at Andela, we've been dating for 3 years",
            "Chidi got promoted to senior backend engineer at Andela, he's now leading a team of 5 developers",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Partner profile via entity chain",
    },
    {
        "id": "aisha_11_parents",
        "query": "What are Aisha's parents like?",
        "expected_texts": [
            "My father Emeka Okafor is a civil engineer who works on infrastructure projects, and my mother Ngozi is a pharmacist who owns Okafor Pharmacy in Wuse, Abuja",
            "Parents calling every week asking about marriage — Mama keeps saying 'Aisha, you're not getting younger, when will Chidi come and see us?'",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Parents profile and dynamics",
    },
    {
        "id": "aisha_12_ikenna",
        "query": "What is Ikenna up to in London?",
        "expected_texts": [
            "My older brother Ikenna is a lawyer at Clifford Chance in London, married to Amara who is an architect",
            "Ikenna sent 2 million naira from London to help renovate our parents' house in Abuja — he's always been generous",
            "Ikenna's wife Amara is pregnant! I'm going to be an auntie — the baby is due in June",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Brother's life arc in London",
    },
    {
        "id": "aisha_13_funke",
        "query": "Who is Funke?",
        "expected_texts": [
            "I live in Yaba with two roommates: Funke who is also a resident at LUTH, and Bola who is a relationship manager at GTBank",
            "Funke also passed the WACS exam — we screamed and hugged in the hospital parking lot when results came out",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Roommate and colleague profile",
    },
    {
        "id": "aisha_14_roommates",
        "query": "Who does Aisha live with?",
        "expected_texts": [
            "I live in Yaba with two roommates: Funke who is also a resident at LUTH, and Bola who is a relationship manager at GTBank",
            "Bola organized a surprise going-away party at our Yaba flat — 30 friends came, Funke made a speech that made everyone emotional",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Living situation and roommate details",
    },

    # ─── RELATIONSHIP (3) ───
    {
        "id": "aisha_15_cohabitation",
        "query": "Did Chidi and Aisha discuss living together?",
        "expected_texts": [
            "Chidi proposed that we move in together but I'm hesitant — my parents would strongly disapprove of us living together before marriage",
        ],
        "test_tags": ["relationship", "semantic"],
        "description": "Cohabitation decision",
    },
    {
        "id": "aisha_16_anniversary",
        "query": "How did Aisha and Chidi celebrate their anniversary?",
        "expected_texts": [
            "Chidi and I celebrated our 3-year anniversary — he surprised me with a trip to Obudu Mountain Resort for the weekend",
        ],
        "test_tags": ["relationship", "semantic"],
        "description": "Anniversary celebration recall",
    },
    {
        "id": "aisha_17_long_distance",
        "query": "How are Aisha and Chidi handling long distance?",
        "expected_texts": [
            "Chidi is being incredibly supportive about the London fellowship but I can tell he's sad about 6 months apart",
            "Video calling Chidi every night at 10pm London time, 11pm Lagos time — the time difference is only 1 hour which helps",
            "Last Friday date night with Chidi at Yellow Chilli before London — he gave me a gold necklace with my initial 'A' on it, I cried",
        ],
        "test_tags": ["relationship", "temporal"],
        "description": "Long-distance relationship management",
    },

    # ─── CAREER DECISIONS (3) ───
    {
        "id": "aisha_18_fellowship",
        "query": "Tell me about Aisha's fellowship in London",
        "expected_texts": [
            "An incredible opportunity has come up — a 6-month surgical fellowship at King's College Hospital in London",
            "I've been accepted for the King's College London fellowship — it starts in 4 months, this is really happening",
        ],
        "test_tags": ["career", "temporal"],
        "description": "Fellowship opportunity and acceptance",
    },
    {
        "id": "aisha_19_london_vs_lagos",
        "query": "What are Aisha's career options — should she stay in London or return to Lagos?",
        "expected_texts": [
            "I've been offered a senior registrar position at King's College Hospital — it's prestigious but it would mean staying in the UK indefinitely",
            "Also received an offer from Reddington Hospital in Lagos — a private hospital with much better pay and facilities than LUTH",
            "Dr. Adeyemi called from Lagos asking me to come back to LUTH — he's starting a new trauma center and wants me to help build it",
        ],
        "test_tags": ["career", "semantic"],
        "description": "Career decision with multiple options",
    },
    {
        "id": "aisha_20_future",
        "query": "What are Aisha's plans for the future?",
        "expected_texts": [
            "The fellowship is ending in 2 months and I have a major career decision ahead — stay in the UK or go back to Nigeria",
            "Chidi and I discussed our marriage timeline — we both want to get married within the next 2 years",
            "Applied for NHS permanent registration just to keep my options open — whether I stay or go, it's good to have the door open",
        ],
        "test_tags": ["career", "temporal"],
        "description": "Future planning across career and personal",
    },

    # ─── FAMILY (3) ───
    {
        "id": "aisha_21_parents_concerns",
        "query": "What are Aisha's parents concerned about?",
        "expected_texts": [
            "Parents calling every week asking about marriage — Mama keeps saying 'Aisha, you're not getting younger, when will Chidi come and see us?'",
            "Parents are proud of the fellowship but Mama is worried about 'London changing you' — she keeps saying 'don't forget where you come from'",
        ],
        "test_tags": ["family", "semantic"],
        "description": "Parental concerns retrieval",
    },
    {
        "id": "aisha_22_ikenna_london",
        "query": "How is Ikenna helping Aisha in London?",
        "expected_texts": [
            "Ikenna is offering to host me at his flat in Canary Wharf if I get the London fellowship — he's so supportive",
            "Ikenna and Amara's flat in Canary Wharf is beautiful — 20th floor with a view of the Thames, a long way from our childhood home in Abuja",
        ],
        "test_tags": ["family", "graph"],
        "description": "Sibling support in London",
    },
    {
        "id": "aisha_23_family_gatherings",
        "query": "What family gatherings has Aisha attended?",
        "expected_texts": [
            "Easter gathering in Abuja with the whole extended family — I managed to take 3 days off from LUTH, ate so much jollof rice",
            "Mama visited Lagos for a week — she brought homemade chin-chin, kilishi, and ogiri from Abuja, the flat smelled like home",
        ],
        "test_tags": ["family", "semantic"],
        "description": "Family event recall",
    },

    # ─── LONDON EXPERIENCE (4) ───
    {
        "id": "aisha_24_culture_shock",
        "query": "How did Aisha adjust to life in London?",
        "expected_texts": [
            "Arrived at Heathrow in November — 7 degrees Celsius felt like minus 20 to me, I was shivering in my new coat",
            "Culture shock is real — the British understatement, queuing for absolutely everything, and the food is so bland compared to Nigerian food",
            "Found a Nigerian restaurant called Mama Put in Peckham — the jollof rice tastes exactly like home, I nearly cried with the first bite",
        ],
        "test_tags": ["london", "semantic"],
        "description": "London adjustment experience",
    },
    {
        "id": "aisha_25_robotic_surgery",
        "query": "What is Aisha learning about robotic surgery?",
        "expected_texts": [
            "I'm learning robotic surgery on the da Vinci Xi system at King's — the technology is absolutely incredible, light years ahead of what we have at LUTH",
            "Assisted in a complex Whipple procedure — a pancreaticoduodenectomy that took 8 hours, Mr. Okonkwo let me do the final anastomosis",
        ],
        "test_tags": ["london", "medical"],
        "description": "London surgical training specifics",
    },
    {
        "id": "aisha_26_publication",
        "query": "Has Aisha published any research?",
        "expected_texts": [
            "Published my first case report in the British Journal of Surgery with Dr. Adeyemi as co-author — a case from my LUTH days",
        ],
        "test_tags": ["london", "semantic"],
        "description": "Academic publication recall",
    },
    {
        "id": "aisha_27_mama_put",
        "query": "Where does Aisha eat Nigerian food in London?",
        "expected_texts": [
            "Found a Nigerian restaurant called Mama Put in Peckham — the jollof rice tastes exactly like home, I nearly cried with the first bite",
            "Missing Nigerian food terribly despite my Saturday visits to Mama Put in Peckham — nothing beats real homemade jollof",
        ],
        "test_tags": ["london", "graph"],
        "description": "Restaurant habit in London",
    },

    # ─── EXAM / STUDY (2) ───
    {
        "id": "aisha_28_wacs_exam",
        "query": "How did Aisha do on her WACS exam?",
        "expected_texts": [
            "I've started studying for Part 1 of the West African College of Surgeons fellowship exam — this is the biggest exam of my career so far",
            "I passed the WACS Part 1 exam with distinction! We celebrated at Shiro restaurant on Victoria Island",
        ],
        "test_tags": ["exam", "temporal"],
        "description": "Exam preparation and result arc",
    },
    {
        "id": "aisha_29_study_group",
        "query": "Who is in Aisha's study group?",
        "expected_texts": [
            "My study group for WACS includes me, Funke, Dr. Yusuf, and Dr. Nkechi from the pediatric surgery department",
            "Using Sabiston Textbook of Surgery and Bailey & Love as my main references for the WACS exam — those books weigh more than some of my patients",
        ],
        "test_tags": ["exam", "graph"],
        "description": "Study group and resources",
    },

    # ─── EMOTIONAL / VALENCE (2) ───
    {
        "id": "aisha_30_proudest",
        "query": "What were Aisha's proudest or happiest moments?",
        "expected_texts": [
            "I passed the WACS Part 1 exam with distinction! We celebrated at Shiro restaurant on Victoria Island",
            "I performed my first solo appendectomy today and it was successful! Dr. Adeyemi said 'clean technique' which is the highest praise from him",
            "Published my first case report in the British Journal of Surgery with Dr. Adeyemi as co-author — a case from my LUTH days",
        ],
        "test_tags": ["valence", "semantic"],
        "description": "Positive valence retrieval",
    },
    {
        "id": "aisha_31_difficult",
        "query": "What were the most stressful or difficult moments for Aisha?",
        "expected_texts": [
            "Lost a patient today, Mrs. Ogundimu, 68 years old, to post-operative complications from bowel obstruction — I am devastated",
            "The hospital backup generator failed during a procedure today — we had to use phone flashlights to finish, it was terrifying",
            "The WACS exam is scheduled in 3 months and I'm feeling overwhelmed juggling 80-hour work weeks with studying",
        ],
        "test_tags": ["valence", "semantic"],
        "description": "Negative valence retrieval",
    },

    # ─── CROSS-DOMAIN (2) ───
    {
        "id": "aisha_32_nigerian_uk",
        "query": "How does Nigerian healthcare compare to the UK based on Aisha's experience?",
        "expected_texts": [
            "King's College Hospital is absolutely world-class — everything works, the power never goes out, equipment is always available",
            "The hospital ran out of ceftriaxone and metronidazole for 3 days — we had to substitute with whatever antibiotics were available and document everything",
            "NEPA wahala worse than usual this month — generator diesel costs have doubled and the hospital can barely afford to keep the lights on",
        ],
        "test_tags": ["cross_domain", "semantic"],
        "description": "Multi-hop comparison across Lagos and London",
    },
    {
        "id": "aisha_33_mentors",
        "query": "Who has mentored Aisha in her career?",
        "expected_texts": [
            "I've been assigned to Dr. Adeyemi's general surgery team — he's strict but absolutely brilliant, one of the best surgeons in Nigeria",
            "I'm learning laparoscopic techniques from the senior attending Dr. Funke Babatunde — she's one of the few female consultants at LUTH",
            "I've been assigned to Mr. James Okonkwo as my mentor at King's — he's a Nigerian-British consultant surgeon, it feels like having a piece of home here",
        ],
        "test_tags": ["cross_domain", "graph"],
        "description": "Multi-hop mentor query across institutions",
    },

    # ─── SEMANTIC GAP (2) ───
    {
        "id": "aisha_34_power_problems",
        "query": "What infrastructure issues affect Aisha's work in Nigeria?",
        "expected_texts": [
            "NEPA wahala worse than usual this month — generator diesel costs have doubled and the hospital can barely afford to keep the lights on",
            "The hospital backup generator failed during a procedure today — we had to use phone flashlights to finish, it was terrifying",
        ],
        "test_tags": ["semantic_gap", "semantic"],
        "description": "Query uses 'infrastructure issues' but memories use 'NEPA', 'generator', 'diesel'",
    },
    {
        "id": "aisha_35_homesickness",
        "query": "Does Aisha miss home while in London?",
        "expected_texts": [
            "Missing Nigerian food terribly despite my Saturday visits to Mama Put in Peckham — nothing beats real homemade jollof",
            "Culture shock is real — the British understatement, queuing for absolutely everything, and the food is so bland compared to Nigerian food",
        ],
        "test_tags": ["semantic_gap", "valence"],
        "description": "Query uses 'miss home' but memories describe food, culture shock, adjustment",
    },
]


# ── Deterministic Vector Generator ────────────────────────────────────────

def _deterministic_vec(seed: float, dim: int) -> list[float]:
    """Generate a deterministic unit vector from a seed value."""
    raw = [(seed + i) * 0.1 + math.sin(seed * (i + 1)) * 0.3 for i in range(dim)]
    norm = math.sqrt(sum(x * x for x in raw))
    if norm == 0:
        raw[0] = 1.0
        norm = 1.0
    return [x / norm for x in raw]


# ── Noise Memory Generator ───────────────────────────────────────────────
# Domain-specific templates for realistic daily-life noise.

_HOSPITAL_TEMPLATES = [
    ("Morning rounds on ward {ward}: {patient_count} patients reviewed, {discharge_count} discharges today", "episodic", 0.3, 0.1, None),
    ("New admission on ward {ward}: {age}-year-old {gender} with {complaint}", "episodic", 0.3, 0.0, None),
    ("Handover to the night team — passed on {count} patients, flagged {flag_count} as critical", "episodic", 0.2, 0.0, None),
    ("Ward round with Dr. Adeyemi — he quizzed us on {topic}, I got the answer right", "episodic", 0.3, 0.3, "adeyemi"),
    ("Spent {hours} hours in outpatient clinic today — saw {count} patients, mostly {case_type}", "episodic", 0.2, 0.0, None),
    ("Hospital bed occupancy at {percent}% — we had to put patients on mattresses in the corridor again", "episodic", 0.3, -0.3, None),
    ("Blood bank running low on O-negative — had to call the blood donation center for emergency supply", "episodic", 0.4, -0.4, None),
    ("Attended mortality and morbidity conference — discussed {count} cases from last month", "episodic", 0.3, -0.1, None),
    ("New batch of interns started today — I remember being that nervous on my first day at LUTH", "episodic", 0.2, 0.3, None),
    ("Hospital WiFi down again — had to use my phone data to look up drug dosages on UpToDate", "episodic", 0.2, -0.2, None),
]

_SURGERY_TEMPLATES = [
    ("Assisted Dr. Adeyemi with a {procedure} today — {duration} hours in the OR", "episodic", 0.3, 0.2, "adeyemi"),
    ("Post-op check on yesterday's {procedure} patient — {status}", "episodic", 0.2, 0.1, None),
    ("OR schedule today: {count} cases starting at {time}am", "episodic", 0.2, 0.0, None),
    ("Wound review on bed {bed}: {wound_status}", "episodic", 0.2, 0.0, None),
    ("Scrubbed in for an emergency {procedure} — patient came in through A&E at {time}am", "episodic", 0.3, 0.1, None),
    ("Practiced suturing techniques on the simulation model during lunch break", "procedural", 0.2, 0.2, None),
    ("Dr. Babatunde showed us a new technique for {technique} — much cleaner than the old method", "episodic", 0.3, 0.3, "babatunde"),
    ("Sterilization machine broke down — had to postpone 2 elective surgeries", "episodic", 0.3, -0.4, None),
    ("Performed a {procedure} under supervision — Dr. Adeyemi said {feedback}", "episodic", 0.3, 0.2, "adeyemi"),
    ("Pre-op assessment for tomorrow's list: {count} patients, reviewing bloods and imaging", "episodic", 0.2, 0.0, None),
]

_STUDY_TEMPLATES = [
    ("Read {chapter} in Sabiston today — {pages} pages on {topic}", "episodic", 0.2, 0.1, None),
    ("Study group session with Funke and Dr. Yusuf — practiced {topic} questions", "episodic", 0.2, 0.2, "study_group"),
    ("Reviewed {count} past exam questions from the WACS question bank", "episodic", 0.2, 0.1, None),
    ("Read a journal article on {topic} in the {journal}", "episodic", 0.2, 0.2, None),
    ("Made flashcards for {topic} — {count} cards total", "procedural", 0.2, 0.1, None),
    ("Attended the surgical grand rounds lecture on {topic} by visiting professor from {university}", "episodic", 0.3, 0.2, None),
    ("Late night studying at the hospital library — the security guard knows me by name now", "episodic", 0.2, 0.0, None),
    ("Dr. Nkechi shared her notes on {topic} — very helpful for WACS prep", "episodic", 0.2, 0.3, "nkechi"),
    ("Watched a surgical technique video on YouTube: {procedure} by {surgeon}", "episodic", 0.2, 0.2, None),
    ("Quiz score in study group: got {score} out of {total} — {feeling}", "episodic", 0.2, 0.1, None),
]

_LAGOS_LIFE_TEMPLATES = [
    ("Third Mainland Bridge traffic was {intensity} today — took {minutes} minutes to get to LUTH", "episodic", 0.1, -0.2, None),
    ("NEPA took light for {hours} hours today — used the small generator at the flat", "episodic", 0.2, -0.3, None),
    ("Bought generator fuel at {price} naira per liter — the prices keep going up", "episodic", 0.2, -0.2, None),
    ("Water tanker delivery today — paid {amount} naira for the week's supply", "episodic", 0.1, -0.1, None),
    ("Market prices insane this week — {item} now costs {price} naira, up from {old_price}", "episodic", 0.2, -0.3, None),
    ("BRT bus was packed this morning — stood the whole way from Yaba to {destination}", "episodic", 0.1, -0.2, None),
    ("Danfo driver almost hit a motorcycle on the Yaba bridge — my heart was in my mouth", "episodic", 0.2, -0.4, None),
    ("Rain flooded the street in Yaba again — waded through ankle-deep water to get to the car", "episodic", 0.2, -0.3, None),
    ("Flat rent is due: {amount} naira for the month — split three ways with Funke and Bola", "episodic", 0.2, -0.1, None),
    ("Area boys blocked the road near {location} — had to take a detour through {alt_route}", "episodic", 0.2, -0.3, None),
    ("Dollar to naira rate now at {rate} — everything imported is getting more expensive", "episodic", 0.2, -0.3, None),
]

_SOCIAL_TEMPLATES = [
    ("Called Mama this evening — she told me about {topic}", "episodic", 0.2, 0.3, "mama"),
    ("WhatsApp voice note from Mama: {content}", "episodic", 0.1, 0.3, "mama"),
    ("Went out with Funke and Bola to {place} — needed to unwind after a tough week", "episodic", 0.2, 0.4, "roommates"),
    ("Church service at {church} on Sunday — the sermon was about {topic}", "episodic", 0.2, 0.3, None),
    ("Video call with Chidi tonight — he showed me {what}", "episodic", 0.2, 0.4, "chidi"),
    ("Papa called from {location} — the bridge project is {status}", "episodic", 0.2, 0.2, "papa"),
    ("Ikenna sent a message in the family group chat about {topic}", "episodic", 0.1, 0.2, "ikenna"),
    ("Funke and I watched {show} on Netflix after our shift — we needed brain-dead entertainment", "episodic", 0.1, 0.3, None),
    ("Dr. Yusuf and I grabbed suya after call night — the Mallam near LUTH makes the best suya", "episodic", 0.2, 0.4, "yusuf"),
    ("Bola invited her GTBank colleagues over for a small party — I made jollof and Funke made fried plantain", "episodic", 0.2, 0.4, "roommates"),
]

_FOOD_TEMPLATES = [
    ("Ate {food} for dinner tonight — {reaction}", "episodic", 0.1, 0.2, None),
    ("Cooked {dish} for the flat — Funke said it was {verdict}", "episodic", 0.2, 0.3, None),
    ("Survived another shift on indomie and {drink} — really need to eat better", "episodic", 0.1, -0.1, None),
    ("Bought {food} from the canteen lady at LUTH — she always gives me extra meat", "episodic", 0.1, 0.3, None),
    ("Tried making Mama's {dish} recipe — it didn't taste right, called her for the secret ingredient", "episodic", 0.2, 0.2, None),
    ("Ordered food from {restaurant} on Jumia Food — took {minutes} minutes to arrive", "episodic", 0.1, 0.0, None),
    ("Bought suya from the Mallam on the way home — {pieces} sticks of beef and kidney", "episodic", 0.1, 0.3, None),
    ("Pepper soup at {place} after Friday prayers — perfect way to end the week", "episodic", 0.2, 0.4, None),
    ("Made {drink} for the study group session — everyone approved", "episodic", 0.1, 0.3, None),
]

_COMMUTE_TEMPLATES = [
    ("Third Mainland Bridge: {status} today, {minutes} minutes to work", "episodic", 0.1, -0.1, None),
    ("Took the BRT from Yaba to {stop} — at least there's AC on the bus", "episodic", 0.1, 0.0, None),
    ("My Toyota Corolla made a {sound} sound today — need to take it to the mechanic", "episodic", 0.2, -0.2, None),
    ("Danfo ride from {start} to {end}: {experience}", "episodic", 0.1, -0.1, None),
    ("Petrol queue at the filling station on {road} — waited {minutes} minutes", "episodic", 0.2, -0.3, None),
    ("Uber from Yaba to {destination} cost {amount} naira — surge pricing because of the rain", "episodic", 0.1, -0.2, None),
    ("Traffic at {location} was so bad I just parked and walked the rest of the way to the hospital", "episodic", 0.2, -0.3, None),
    ("Left home at {time}am to beat the traffic — made it to LUTH in {minutes} minutes, a new record", "episodic", 0.1, 0.2, None),
]

# Slot fill values
_WARDS = ["A3", "B2", "C1", "D4", "surgical ward 1", "surgical ward 2", "emergency ward"]
_COMPLAINTS = ["acute abdomen", "road traffic accident injuries", "hernia", "appendicitis",
               "breast lump", "thyroid swelling", "intestinal obstruction", "abscess",
               "burns", "stab wound", "fracture", "urinary retention"]
_PROCEDURES = ["hernia repair", "appendectomy", "cholecystectomy", "wound debridement",
               "incision and drainage", "thyroidectomy", "mastectomy", "laparotomy",
               "skin grafting", "tracheostomy", "colostomy creation", "hemorrhoidectomy"]
_WOUND_STATUSES = ["healing well, clean dressing applied", "some discharge, started antibiotics",
                   "excellent granulation tissue", "wound edges approximating nicely",
                   "needs re-suturing", "drain removed, looking good"]
_SURGICAL_FEEDBACK = ["'good hands'", "'too slow, speed up'", "'watch your hemostasis'",
                      "'much better than last time'", "'you're getting there'", "'excellent closure'"]
_STUDY_TOPICS = ["surgical anatomy of the abdomen", "principles of wound healing", "shock management",
                 "fluid and electrolyte balance", "surgical infections", "breast diseases",
                 "thyroid disorders", "GI bleeding management", "trauma surgery",
                 "hepatobiliary surgery", "vascular surgery basics", "pediatric surgery"]
_JOURNALS = ["Nigerian Journal of Surgery", "African Journal of Medicine", "Annals of Surgery",
             "British Journal of Surgery", "The Lancet", "West African Journal of Medicine"]
_MARKET_ITEMS = ["rice", "garri", "palm oil", "beans", "tomato paste", "onions", "chicken", "beef"]
_LAGOS_FOODS = ["jollof rice and chicken", "amala and ewedu", "pounded yam and egusi",
                "fried rice and plantain", "beans and plantain", "yam porridge", "moi moi",
                "akara and pap", "ofada rice and ayamase", "suya"]
_DRINKS = ["malt drink", "zobo", "Chapman", "Fanta", "Coca-Cola", "water sachet"]
_DISHES_COOK = ["jollof rice", "egusi soup", "pepper soup", "fried plantain", "chin-chin",
                "moi moi", "okra soup", "ogbono soup", "nkwobi"]
_LAGOS_RESTAURANTS = ["Bukka Hut", "Tantalizers", "Chicken Republic", "Kilimanjaro",
                      "The Place", "Sweet Sensation", "Mama Cass"]
_LAGOS_LOCATIONS = ["Yaba", "Surulere", "Ikeja", "Victoria Island", "Lekki", "Ikoyi", "Mushin"]
_CHURCHES = ["Redeemed Christian Church in Yaba", "Living Faith Yaba branch",
             "Our Lady of Perpetual Help Catholic Church", "RCCG Yaba parish"]
_SHOWS = ["Blood & Water", "King of Boys", "Far From Home", "The Men's Club",
          "Blood Sisters", "Gangs of Lagos", "Young Wallander"]


def _fill_hospital_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        ward=rng.choice(_WARDS),
        patient_count=rng.randint(8, 25),
        discharge_count=rng.randint(1, 5),
        age=rng.randint(5, 85),
        gender=rng.choice(["male", "female"]),
        complaint=rng.choice(_COMPLAINTS),
        count=rng.randint(3, 15),
        flag_count=rng.randint(1, 4),
        topic=rng.choice(_STUDY_TOPICS),
        hours=rng.randint(3, 8),
        case_type=rng.choice(["hernias", "abscesses", "follow-up wound checks", "pre-op assessments"]),
        percent=rng.randint(85, 110),
    )
    if entity_mode == "adeyemi":
        entities = [("Aisha", "Dr. Adeyemi", "rounds_with")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_surgery_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        procedure=rng.choice(_PROCEDURES),
        duration=rng.randint(1, 5),
        status=rng.choice(["vitals stable, recovery uneventful", "mild fever, monitoring closely",
                           "drains in situ, output minimal", "eating well, plan discharge tomorrow"]),
        count=rng.randint(2, 6),
        time=rng.randint(7, 10),
        bed=rng.randint(1, 30),
        wound_status=rng.choice(_WOUND_STATUSES),
        technique=rng.choice(["laparoscopic port placement", "bowel anastomosis", "skin closure",
                              "drain insertion", "mesh placement"]),
        feedback=rng.choice(_SURGICAL_FEEDBACK),
    )
    if entity_mode == "adeyemi":
        entities = [("Aisha", "Dr. Adeyemi", "assisted")]
    elif entity_mode == "babatunde":
        entities = [("Aisha", "Dr. Babatunde", "learned_from")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_study_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        chapter=f"Chapter {rng.randint(1, 40)}",
        pages=rng.randint(15, 60),
        topic=rng.choice(_STUDY_TOPICS),
        count=rng.randint(10, 50),
        journal=rng.choice(_JOURNALS),
        university=rng.choice(["University of Lagos", "UCH Ibadan", "Ahmadu Bello University",
                               "University of Cape Town", "Makerere University"]),
        procedure=rng.choice(_PROCEDURES),
        surgeon=rng.choice(["Prof. Adeyemi", "Dr. Okonkwo", "Prof. Ogundipe"]),
        score=rng.randint(5, 10),
        total=10,
        feeling=rng.choice(["pleased", "need to study more", "improving", "decent"]),
    )
    if entity_mode == "study_group":
        entities = [("Aisha", "Funke", "studied_with"), ("Aisha", "Dr. Yusuf", "studied_with")]
    elif entity_mode == "nkechi":
        entities = [("Aisha", "Dr. Nkechi", "received_notes_from")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_lagos_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        intensity=rng.choice(["horrendous", "okay", "terrible as usual", "surprisingly light", "bumper to bumper"]),
        minutes=rng.randint(30, 120),
        hours=rng.randint(1, 8),
        price=rng.randint(300, 800),
        amount=rng.randint(3000, 10000),
        item=rng.choice(_MARKET_ITEMS),
        old_price=rng.randint(200, 2000),
        destination=rng.choice(["CMS", "Ikoyi", "TBS", "Surulere"]),
        location=rng.choice(_LAGOS_LOCATIONS),
        alt_route=rng.choice(["Ojuelegba", "Herbert Macaulay", "Western Avenue", "Ikorodu Road"]),
        rate=rng.randint(900, 1600),
    )
    return filled, mtype, imp, val, []


def _fill_social_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        topic=rng.choice(["Papa's bridge project", "Aunty Chioma's wedding plans",
                          "cousin Nnamdi's new job", "the cost of things in Abuja",
                          "when I'm bringing Chidi to visit", "Ikenna and Amara's baby plans"]),
        content=rng.choice(["asking if I've eaten today", "reminding me to go to church",
                           "telling me about a cousin's engagement", "recipe for ogiri soup",
                           "prayer for my exams"]),
        place=rng.choice(["Shiro", "Hard Rock Cafe Lekki", "GET Arena", "Terra Kulture",
                          "The Palms shopping mall", "Lekki Conservation Centre"]),
        church=rng.choice(_CHURCHES),
        what=rng.choice(["a new app feature he's building", "the view from Andela's office",
                         "a funny meme about Lagos traffic", "his meal prep for the week"]),
        location=rng.choice(["Calabar", "Abuja", "Port Harcourt"]),
        status=rng.choice(["going well, ahead of schedule", "delayed by weather",
                           "nearing completion", "waiting for materials"]),
        show=rng.choice(_SHOWS),
    )
    if entity_mode == "mama":
        entities = [("Aisha", "Ngozi", "called")]
    elif entity_mode == "roommates":
        entities = [("Aisha", "Funke", "went_out_with"), ("Aisha", "Bola", "went_out_with")]
    elif entity_mode == "chidi":
        entities = [("Aisha", "Chidi", "video_called")]
    elif entity_mode == "papa":
        entities = [("Aisha", "Emeka", "called")]
    elif entity_mode == "ikenna":
        entities = [("Aisha", "Ikenna", "messaged")]
    elif entity_mode == "yusuf":
        entities = [("Aisha", "Dr. Yusuf", "hung_out_with")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_food_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        food=rng.choice(_LAGOS_FOODS),
        reaction=rng.choice(["delicious", "not bad", "I was too hungry to care", "reminded me of Mama's cooking"]),
        dish=rng.choice(_DISHES_COOK),
        verdict=rng.choice(["the best she's ever tasted", "needs more pepper next time",
                           "better than last time", "exactly like Mama's"]),
        drink=rng.choice(_DRINKS),
        restaurant=rng.choice(_LAGOS_RESTAURANTS),
        minutes=rng.randint(20, 90),
        pieces=rng.randint(3, 8),
        place=rng.choice(["the canteen", "Mama Cass", "Bukka Hut", "the roadside joint near LUTH"]),
    )
    return filled, mtype, imp, val, []


def _fill_commute_template(template, rng, day):
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        status=rng.choice(["gridlock", "moving slowly", "surprisingly clear", "absolute chaos"]),
        minutes=rng.randint(20, 120),
        stop=rng.choice(["CMS", "Ikoyi", "Obalende", "TBS"]),
        sound=rng.choice(["rattling", "grinding", "squealing", "knocking"]),
        start=rng.choice(["Yaba", "Surulere"]),
        end=rng.choice(["Ikeja", "Ikoyi", "VI"]),
        experience=rng.choice(["the conductor and a passenger argued the whole way",
                               "squeezed in with 20 other people", "surprisingly smooth ride",
                               "the driver took every shortcut known to man"]),
        road=rng.choice(["Ikorodu Road", "Herbert Macaulay Way", "Western Avenue"]),
        amount=rng.randint(1500, 5000),
        destination=rng.choice(_LAGOS_LOCATIONS),
        location=rng.choice(["Ojota", "Yaba roundabout", "Oshodi", "Third Mainland Bridge"]),
        time=rng.randint(5, 7),
    )
    return filled, mtype, imp, val, []


def generate_aisha_noise(target_count=5000, seed=456):
    """Generate daily-life noise memories for Aisha.

    Returns a list of dicts with: text, type, importance, valence, entities, day_offset
    """
    rng = random.Random(seed)
    memories = []
    total_days = 365  # 12 months

    domain_schedule = [
        ("hospital", _HOSPITAL_TEMPLATES, _fill_hospital_template, 4),
        ("surgery", _SURGERY_TEMPLATES, _fill_surgery_template, 3),
        ("study", _STUDY_TEMPLATES, _fill_study_template, 2),
        ("lagos", _LAGOS_LIFE_TEMPLATES, _fill_lagos_template, 2),
        ("social", _SOCIAL_TEMPLATES, _fill_social_template, 2),
        ("food", _FOOD_TEMPLATES, _fill_food_template, 2),
        ("commute", _COMMUTE_TEMPLATES, _fill_commute_template, 1),
    ]

    total_per_day = sum(count for _, _, _, count in domain_schedule)
    effective_days = total_days - int((total_days / 7) * 1 * 0.5)  # doctors work most weekends
    expected_raw = total_per_day * total_days - 4 * int((total_days / 7) * 1 * 0.5)
    scale = target_count / max(expected_raw, 1)

    for day in range(total_days):
        for domain_name, templates, filler, base_count in domain_schedule:
            # Doctors work most days but have lighter weekends
            if domain_name in ("hospital", "surgery") and day % 7 == 6:
                if rng.random() > 0.3:
                    continue

            # Study is lighter on call nights (random skip)
            if domain_name == "study" and rng.random() < 0.3:
                continue

            # Lagos life templates stop after month 9 (when she moves to London)
            if domain_name in ("lagos", "commute") and day > 280:
                continue

            expected = base_count * scale
            count = int(expected)
            if rng.random() < (expected - count):
                count += 1

            for _ in range(count):
                template = rng.choice(templates)
                text, mtype, imp, val, entities = filler(template, rng, day)

                imp = max(0.1, min(1.0, imp + rng.uniform(-0.1, 0.1)))

                memories.append({
                    "text": text,
                    "type": mtype,
                    "importance": round(imp, 2),
                    "valence": round(val, 2),
                    "entities": entities,
                    "day_offset": day,
                })

    # Shuffle within small windows to avoid perfect ordering
    for i in range(len(memories) - 1, 0, -1):
        j = rng.randint(max(0, i - 15), i)
        memories[i], memories[j] = memories[j], memories[i]

    if len(memories) > target_count:
        memories = memories[:target_count]

    return memories


# ── Loader and Evaluation Functions ───────────────────────────────────────

def count_aisha_memories():
    """Count hand-crafted anchor memories."""
    return sum(len(s["memories"]) for s in AISHA_SESSIONS)


def load_aisha_into_db(db, embedder=None, dim=384, base_time=None,
                        target_count=5000, progress_callback=None):
    """Load Aisha's memories into a YantrikDB instance.

    Loads ~85 hand-crafted anchor memories plus ~target_count generated noise.

    Args:
        db: YantrikDB instance.
        embedder: Optional SentenceTransformer (or any .encode(str) object).
        dim: Embedding dimension (used for deterministic vectors when no embedder).
        base_time: Base unix timestamp. Defaults to 365 days ago (12 months).
        target_count: Number of generated daily memories to add (default 5000).
        progress_callback: Optional callable(loaded, total) for progress reporting.

    Returns:
        (text_to_rid, text_to_seed) dicts mapping memory text to RID and seed.
    """
    if base_time is None:
        base_time = time.time() - (365 * 86400)

    text_to_rid = {}
    text_to_seed = {}
    seed_counter = 1.0

    # ── Phase 1: Load anchor memories ──
    anchor_count = count_aisha_memories()
    loaded = 0

    for session in AISHA_SESSIONS:
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

    # ── Phase 2: Generate and load noise memories ──
    if target_count > 0:
        generated = generate_aisha_noise(target_count=target_count)
        batch_size = 200

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

            # Create entities
            for src, dst, rel_type in mem["entities"]:
                db.relate(src, dst, rel_type=rel_type)
                db.link_memory_entity(rid, src)
                db.link_memory_entity(rid, dst)

            loaded += 1
            if progress_callback and loaded % 500 == 0:
                progress_callback(loaded, anchor_count + target_count)

            if (idx + 1) % batch_size == 0:
                db._conn.commit()

        db._conn.commit()

    return text_to_rid, text_to_seed


def evaluate_aisha(db, text_to_rid, top_k=10, embedder=None, text_to_seed=None, dim=384):
    """Run all Aisha queries and measure recall quality.

    Returns (report_string, raw_results, metrics_dict).
    """
    results = []
    total_recall = 0.0
    total_precision = 0.0
    total_mrr = 0.0

    tag_scores: dict[str, list[float]] = {}

    for gq in AISHA_QUERIES:
        if embedder is not None:
            vec = embedder.encode(gq["query"])
            query_embedding = vec.tolist() if hasattr(vec, "tolist") else list(vec)
        elif text_to_seed:
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

    n = len(AISHA_QUERIES)
    mean_recall = total_recall / n
    mean_precision = total_precision / n
    mean_mrr = total_mrr / n
    recall_by_tag = {tag: sum(s) / len(s) for tag, s in tag_scores.items()}

    # Format report
    lines = [
        "",
        "=" * 70,
        "  YantrikDB Aisha Okafor Persona Evaluation Report",
        "=" * 70,
        "",
        f"  Memories loaded:    {count_aisha_memories()} anchor + generated",
        f"  Queries evaluated:  {n}",
        f"  Using real embedder: {embedder is not None}",
        "",
        f"  Mean Recall@{top_k}:    {mean_recall:.3f}",
        f"  Mean Precision@{top_k}: {mean_precision:.3f}",
        f"  Mean MRR:           {mean_mrr:.3f}",
        "",
        "  -- Recall by Tag --",
    ]
    for tag, score in sorted(recall_by_tag.items()):
        bar = "#" * int(score * 20)
        lines.append(f"    {tag:15s} {score:.3f}  {bar}")

    lines.append("")
    lines.append("  -- Per Query Results --")

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
    lines.append(f"  Passed: {pass_count}/{n} queries ({100 * pass_count / n:.0f}%)")
    lines.append("")

    stats = db.stats()
    lines.append("  -- System Stats --")
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


def run_aisha_simulation(use_embedder=False, run_think=True, top_k=10,
                          target_count=5000):
    """Run the complete Aisha simulation end-to-end.

    Args:
        use_embedder: If True, loads sentence-transformers for real embeddings.
        run_think: If True, runs the cognition loop after loading.
        top_k: Number of results per query.
        target_count: Number of generated daily memories (default 5000).

    Returns:
        (report_string, raw_results, metrics_dict)
    """
    from yantrikdb import YantrikDB

    embedder = None
    dim = 8

    if use_embedder:
        try:
            from sentence_transformers import SentenceTransformer
            embedder = SentenceTransformer("all-MiniLM-L6-v2")
            dim = 384
            print("  Loaded sentence-transformers embedder (dim=384)")
        except ImportError:
            print("  sentence-transformers not installed, using deterministic vectors")
            use_embedder = False

    total_target = count_aisha_memories() + target_count
    print(f"\n  Creating YantrikDB instance (dim={dim})...")
    db = YantrikDB(db_path=":memory:", embedding_dim=dim, embedder=embedder)

    print(f"  Loading ~{total_target} memories ({count_aisha_memories()} anchor + {target_count} generated)...")
    t0 = time.time()
    last_report = [0]

    def progress(loaded, total):
        pct = 100 * loaded / total
        if pct - last_report[0] >= 5:
            elapsed = time.time() - t0
            rate = loaded / elapsed if elapsed > 0 else 0
            print(f"    {loaded:,}/{total:,} ({pct:.0f}%) -- {rate:.0f} memories/sec")
            last_report[0] = pct

    text_to_rid, text_to_seed = load_aisha_into_db(
        db, embedder=embedder, dim=dim,
        target_count=target_count, progress_callback=progress,
    )
    load_time = time.time() - t0
    print(f"  Loaded in {load_time:.1f}s ({total_target / load_time:.0f} memories/sec)")

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

        patterns = db.get_patterns()
        if patterns:
            print(f"\n  -- Discovered Patterns ({len(patterns)}) --")
            for p in patterns[:5]:
                print(f"    [{p['pattern_type']}] {p['description'][:80]}...")
                print(f"      confidence={p['confidence']:.2f}, occurrences={p['occurrence_count']}")

        conflicts = db.get_conflicts(status="open")
        if conflicts:
            print(f"\n  -- Open Conflicts ({len(conflicts)}) --")
            for c in conflicts[:5]:
                print(f"    [{c['conflict_type']}] {c.get('detection_reason', 'N/A')[:80]}")

        triggers = db.get_pending_triggers(limit=5)
        if triggers:
            print(f"\n  -- Pending Triggers ({len(triggers)}) --")
            for t in triggers:
                print(f"    [{t['trigger_type']}] urgency={t['urgency']:.2f}: {t['reason'][:80]}")

    print(f"\n  Evaluating recall quality against {len(AISHA_QUERIES)} golden queries...")
    t2 = time.time()
    report, raw_results, metrics = evaluate_aisha(
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
    count = 5000
    for arg in sys.argv:
        if arg.startswith("--count="):
            count = int(arg.split("=")[1])
    run_aisha_simulation(use_embedder=use_embed, target_count=count)
