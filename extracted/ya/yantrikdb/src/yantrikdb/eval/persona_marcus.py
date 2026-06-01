"""Evaluation persona: Marcus Chen — restaurant owner in Portland, Oregon.

Populates a complete person's life history — Marcus Chen, a 45-year-old
Chinese-American restaurant owner — spanning ~12 months across restaurant
operations, family life, health, business growth, travel, and finance.

This persona tests YantrikDB's memory retrieval across a domain very different
from the Priya Sharma persona: culinary arts, hospitality business,
multi-generational family dynamics, and small business management.

Usage:
    from yantrikdb.eval.persona_marcus import load_marcus_into_db, evaluate_marcus
"""

import math
import random
import time

# ── Marcus Chen's Life History ───────────────────────────────────────────────
#
# Timeline: 12 months of memories, from Month 0 (start) to Month 12.
# Each session simulates a day or event in Marcus's life.
# ~85 memories across 20+ sessions.

MARCUS_SESSIONS = [
    # ═══════════════════════════════════════════════════════════════
    # MONTH 0 — INTRODUCTION
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "intro_marcus",
        "time_offset_days": 0,
        "memories": [
            {
                "text": "My name is Marcus Chen, I'm 45 years old and I own The Pearl Kitchen in Portland's Pearl District",
                "type": "semantic",
                "importance": 1.0,
                "valence": 0.3,
                "entities": [("Marcus", "The Pearl Kitchen", "owns"), ("The Pearl Kitchen", "Pearl District", "located_in"), ("Marcus", "Portland", "lives_in")],
            },
            {
                "text": "My wife Sarah is a high school English teacher at Lincoln High in Portland",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.5,
                "entities": [("Marcus", "Sarah", "married_to"), ("Sarah", "Lincoln High", "teaches_at")],
            },
            {
                "text": "Our daughter Lily is 16, on the debate team, and wants to study pre-med at Stanford",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.6,
                "entities": [("Marcus", "Lily", "father_of"), ("Lily", "debate team", "member_of"), ("Lily", "Stanford", "wants_to_attend")],
            },
            {
                "text": "Our son Ethan is 13, plays soccer, and is a huge video game enthusiast",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.5,
                "entities": [("Marcus", "Ethan", "father_of"), ("Ethan", "soccer", "plays")],
            },
            {
                "text": "My parents live in San Francisco — Dad Henry is a retired accountant and Mom Mei-Lin runs the Golden Lotus dim sum restaurant",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.4,
                "entities": [("Marcus", "Henry", "son_of"), ("Marcus", "Mei-Lin", "son_of"), ("Henry", "San Francisco", "lives_in"), ("Mei-Lin", "Golden Lotus", "runs")],
            },
            {
                "text": "I trained at the Culinary Institute of America in Hyde Park, New York",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.4,
                "entities": [("Marcus", "Culinary Institute of America", "attended"), ("Culinary Institute of America", "Hyde Park", "located_in")],
            },
            {
                "text": "My mentor was Chef Thomas at Le Bernardin in NYC before I moved to Portland to open my own place",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Marcus", "Chef Thomas", "mentored_by"), ("Chef Thomas", "Le Bernardin", "works_at"), ("Le Bernardin", "NYC", "located_in")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 1 — RESTAURANT OPERATIONS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month1_restaurant_staff",
        "time_offset_days": 20,
        "memories": [
            {
                "text": "Head chef Diego has been with me for 5 years and is phenomenal with sauces — he's the backbone of our kitchen",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.6,
                "entities": [("Diego", "The Pearl Kitchen", "head_chef_at"), ("Marcus", "Diego", "employs")],
            },
            {
                "text": "Sous chef Tomoko recently joined us from Tempura Kondo in Tokyo, which has a Michelin star",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Tomoko", "The Pearl Kitchen", "sous_chef_at"), ("Tomoko", "Tempura Kondo", "previously_at"), ("Tempura Kondo", "Tokyo", "located_in")],
            },
            {
                "text": "Our sommelier Claire curates the wine list and specializes in Oregon Pinot Noir",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Claire", "The Pearl Kitchen", "sommelier_at"), ("Claire", "Oregon Pinot Noir", "specializes_in")],
            },
        ],
    },
    {
        "name": "month1_restaurant_business",
        "time_offset_days": 28,
        "memories": [
            {
                "text": "We got a 4-star review in The Oregonian from food critic Janet Miller — she loved the ambiance and the tasting menu",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.8,
                "entities": [("The Pearl Kitchen", "The Oregonian", "reviewed_in"), ("Janet Miller", "The Pearl Kitchen", "reviewed")],
            },
            {
                "text": "Monthly revenue is around 180K with food costs at 35% and labor at 30%",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.1,
                "entities": [("The Pearl Kitchen", "180K revenue", "monthly")],
            },
            {
                "text": "Our signature dish is the Pacific Northwest dungeness crab risotto — it's been on the menu since day one",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("The Pearl Kitchen", "dungeness crab risotto", "signature_dish")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 2 — FAMILY LIFE
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month2_family",
        "time_offset_days": 50,
        "memories": [
            {
                "text": "Lily won her debate tournament semifinals at the Oregon State championship — she argued healthcare policy brilliantly",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.9,
                "entities": [("Lily", "Oregon State championship", "competed_in"), ("Lily", "debate tournament", "semifinalist")],
            },
            {
                "text": "Ethan broke his wrist playing soccer and Dr. Park at OHSU put on a cast for 6 weeks",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.5,
                "entities": [("Ethan", "Dr. Park", "treated_by"), ("Dr. Park", "OHSU", "works_at"), ("Ethan", "broken wrist", "injury")],
            },
            {
                "text": "Sarah is struggling with a difficult student named Kyle who has been acting out in class — she's considering calling his parents",
                "type": "episodic",
                "importance": 0.5,
                "valence": -0.3,
                "entities": [("Sarah", "Kyle", "teaches"), ("Sarah", "Lincoln High", "teaches_at")],
            },
            {
                "text": "Sunday dim sum at Mei-Lin's Golden Lotus restaurant in San Francisco is our family tradition — we try to go once a month",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Marcus", "Golden Lotus", "visits"), ("Mei-Lin", "Golden Lotus", "runs")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 3 — BUSINESS CHALLENGES
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month3_challenges",
        "time_offset_days": 80,
        "memories": [
            {
                "text": "Health inspection found a minor violation — our walk-in freezer temperature was 2 degrees too high, fixed it same day",
                "type": "episodic",
                "importance": 0.6,
                "valence": -0.4,
                "entities": [("The Pearl Kitchen", "health inspection", "minor_violation")],
            },
            {
                "text": "The landlord wants to increase our rent from 12K to 15K per month — that's a 25% jump and I need to negotiate",
                "type": "episodic",
                "importance": 0.8,
                "valence": -0.5,
                "entities": [("The Pearl Kitchen", "rent increase", "facing")],
            },
            {
                "text": "I'm seriously considering opening a second location in Portland's Alberta District",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.3,
                "entities": [("Marcus", "Alberta District", "considering_location"), ("Marcus", "second restaurant", "planning")],
            },
            {
                "text": "Tomoko's miso-glazed black cod has become our most popular dish — outselling even the crab risotto",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.6,
                "entities": [("Tomoko", "miso-glazed black cod", "created"), ("The Pearl Kitchen", "miso-glazed black cod", "popular_dish")],
            },
            {
                "text": "We lost our second sous chef position so I had to temporarily promote line cook Marco to fill the gap",
                "type": "episodic",
                "importance": 0.6,
                "valence": -0.3,
                "entities": [("Marco", "The Pearl Kitchen", "line_cook_at"), ("Marco", "sous chef", "temporarily_promoted")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 4 — HEALTH & PERSONAL
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month4_health",
        "time_offset_days": 110,
        "memories": [
            {
                "text": "Dr. Chen found my cholesterol is high — LDL at 180 — and prescribed atorvastatin to bring it down",
                "type": "episodic",
                "importance": 0.8,
                "valence": -0.4,
                "entities": [("Marcus", "Dr. Chen", "patient_of"), ("Marcus", "high cholesterol", "diagnosed"), ("Marcus", "atorvastatin", "prescribed")],
            },
            {
                "text": "I started cycling to work instead of driving — it's 6 miles each way through Portland's bike lanes",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("Marcus", "cycling", "commutes_by")],
            },
            {
                "text": "Training for the Portland Century 100-mile bike ride with my friend Jake who got me into cycling",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [("Marcus", "Portland Century", "training_for"), ("Marcus", "Jake", "cycling_buddy")],
            },
            {
                "text": "I quit smoking 14 months ago but still use nicotine gum occasionally when the restaurant gets really stressful",
                "type": "semantic",
                "importance": 0.6,
                "valence": -0.1,
                "entities": [("Marcus", "smoking", "quit"), ("Marcus", "nicotine gum", "uses")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 5 — SEASONAL MENU
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month5_spring_menu",
        "time_offset_days": 140,
        "memories": [
            {
                "text": "Spring menu launch was a hit — the Oregon white truffle risotto is getting rave reviews from regulars",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("The Pearl Kitchen", "spring menu", "launched"), ("The Pearl Kitchen", "Oregon white truffle risotto", "new_dish")],
            },
            {
                "text": "We partnered with Cascade Farms for organic produce delivery twice a week — the quality is incredible",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.4,
                "entities": [("The Pearl Kitchen", "Cascade Farms", "partners_with"), ("Cascade Farms", "organic produce", "supplies")],
            },
            {
                "text": "Switched from the old Clover POS to Toast — the analytics and reporting are so much better for tracking menu performance",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("The Pearl Kitchen", "Toast", "uses_pos")],
            },
            {
                "text": "Food costs jumped 8% this quarter due to supply chain issues — I'm considering a menu price increase of 10-12%",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.3,
                "entities": [("The Pearl Kitchen", "food costs", "increased")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 6 — FAMILY EVENTS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month6_family_events",
        "time_offset_days": 170,
        "memories": [
            {
                "text": "Mei-Lin's 70th birthday party at Golden Lotus was amazing — 35 family members flew in from all over",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.9,
                "entities": [("Mei-Lin", "70th birthday", "celebrated"), ("Golden Lotus", "Mei-Lin birthday", "venue")],
            },
            {
                "text": "Uncle Frank flew in from Hong Kong for Mei-Lin's birthday — I hadn't seen him in 10 years and he looks exactly the same",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Uncle Frank", "Hong Kong", "lives_in"), ("Uncle Frank", "Mei-Lin birthday", "attended")],
            },
            {
                "text": "Lily got her driver's permit and I've been teaching her to drive on weekends — I'm way more nervous than she is",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Lily", "driver's permit", "obtained"), ("Marcus", "Lily", "teaching_to_drive")],
            },
            {
                "text": "Ethan's wrist healed and he made the U14 travel soccer team coached by Tony Ramirez",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("Ethan", "U14 travel soccer", "made_team"), ("Tony Ramirez", "U14 travel soccer", "coaches"), ("Ethan", "wrist", "healed")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 7 — RESTAURANT MILESTONES
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month7_milestones",
        "time_offset_days": 200,
        "memories": [
            {
                "text": "We celebrated The Pearl Kitchen's 8th anniversary with a special 8-course tasting menu that sold out in two days",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.8,
                "entities": [("The Pearl Kitchen", "8th anniversary", "celebrated")],
            },
            {
                "text": "The Pearl Kitchen received a James Beard Foundation semifinalist nomination for Best Chef Northwest — I couldn't believe it",
                "type": "episodic",
                "importance": 1.0,
                "valence": 0.9,
                "entities": [("Marcus", "James Beard Foundation", "nominated_by"), ("Marcus", "Best Chef Northwest", "semifinalist")],
            },
            {
                "text": "Hired pastry chef Isabelle Laurent from Paris — her tarte tatin is absolutely unreal and our dessert sales doubled",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("Isabelle Laurent", "The Pearl Kitchen", "pastry_chef_at"), ("Isabelle Laurent", "Paris", "from"), ("Isabelle Laurent", "tarte tatin", "specializes_in")],
            },
            {
                "text": "Monthly revenue hit 210K this month — our best month ever, up from the usual 180K",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.7,
                "entities": [("The Pearl Kitchen", "210K revenue", "record_month")],
            },
            {
                "text": "A food writer from Bon Appetit visited and spent three hours at the chef's counter — the article should come out next month",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.6,
                "entities": [("Bon Appetit", "The Pearl Kitchen", "visiting"), ("Marcus", "Bon Appetit", "featured_in")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 8 — PERSONAL CHALLENGES
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month8_personal_challenges",
        "time_offset_days": 230,
        "memories": [
            {
                "text": "Sarah was diagnosed with Hashimoto's thyroiditis and Dr. Patel put her on levothyroxine",
                "type": "episodic",
                "importance": 0.9,
                "valence": -0.6,
                "entities": [("Sarah", "Hashimoto's thyroiditis", "diagnosed_with"), ("Sarah", "Dr. Patel", "treated_by"), ("Sarah", "levothyroxine", "prescribed")],
            },
            {
                "text": "Sarah needs blood tests every 6 weeks to monitor her thyroid levels — she's been feeling really fatigued",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.4,
                "entities": [("Sarah", "thyroid", "monitoring")],
            },
            {
                "text": "I'm feeling stretched thin between running the restaurant and supporting Sarah and the kids — something has to give",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.5,
                "entities": [("Marcus", "stress", "experiencing")],
            },
            {
                "text": "Started seeing therapist Dr. Kim for weekly stress management sessions — she's helping me set boundaries",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.2,
                "entities": [("Marcus", "Dr. Kim", "therapist"), ("Marcus", "therapy", "attending")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 9 — SECOND LOCATION
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month9_second_location",
        "time_offset_days": 260,
        "memories": [
            {
                "text": "Signed the lease for a 2,400 square foot space in Alberta District for the second restaurant",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.5,
                "entities": [("Marcus", "Alberta District", "leased_space"), ("Pearl Kitchen Local", "Alberta District", "located_in")],
            },
            {
                "text": "Renovation budget is 350K and contractor Pete estimates 4 months to complete the buildout",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.0,
                "entities": [("Pete", "Pearl Kitchen Local", "contractor_for"), ("Pearl Kitchen Local", "350K renovation", "budget")],
            },
            {
                "text": "The second location concept is Pearl Kitchen Local — a casual counter-service version with smaller plates and faster turnover",
                "type": "semantic",
                "importance": 0.8,
                "valence": 0.4,
                "entities": [("Pearl Kitchen Local", "counter-service", "concept"), ("Marcus", "Pearl Kitchen Local", "planning")],
            },
            {
                "text": "My investor friend David Chen is offering 200K for 15% equity in the new location — it's a fair deal",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.3,
                "entities": [("David Chen", "Pearl Kitchen Local", "investor_in"), ("David Chen", "200K", "investing"), ("Marcus", "David Chen", "business_partner")],
            },
            {
                "text": "Hired architecture firm Skylab to design the Alberta District space — they're known for Portland's best restaurant interiors",
                "type": "episodic",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Skylab", "Pearl Kitchen Local", "designing"), ("Skylab", "architecture firm", "is")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 10 — VIETNAM TRIP
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month10_vietnam",
        "time_offset_days": 295,
        "memories": [
            {
                "text": "Took the whole family to Vietnam for 2 weeks — visited Hanoi, Hoi An, and Ho Chi Minh City for culinary inspiration",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.8,
                "entities": [("Marcus", "Vietnam", "traveled_to"), ("Marcus", "Hanoi", "visited"), ("Marcus", "Hoi An", "visited"), ("Marcus", "Ho Chi Minh City", "visited")],
            },
            {
                "text": "Learned pho secrets from street vendor Tran in Hanoi's Old Quarter — he's been making pho for 40 years at the same spot",
                "type": "procedural",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("Marcus", "Tran", "learned_from"), ("Tran", "Hanoi Old Quarter", "works_in"), ("Tran", "pho", "specializes_in")],
            },
            {
                "text": "Brought back rare spices from Vietnam: Vietnamese cinnamon, star anise, and authentic Phu Quoc fish sauce",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.5,
                "entities": [("Marcus", "Vietnamese spices", "acquired")],
            },
            {
                "text": "Ethan ate his first balut egg in Saigon and documented the whole thing on TikTok — the video got 50K views",
                "type": "episodic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Ethan", "balut", "tried"), ("Ethan", "TikTok", "posted_on")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 11 — STAFF CHALLENGES
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month11_staff",
        "time_offset_days": 325,
        "memories": [
            {
                "text": "Diego threatened to leave for rival restaurant Canard — he got a head chef offer with higher pay",
                "type": "episodic",
                "importance": 0.9,
                "valence": -0.6,
                "entities": [("Diego", "Canard", "offered_by"), ("Diego", "The Pearl Kitchen", "threatening_to_leave")],
            },
            {
                "text": "Offered Diego a partnership track — 5% equity vesting over 3 years — to convince him to stay, and he accepted",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.4,
                "entities": [("Diego", "The Pearl Kitchen", "partner_track"), ("Marcus", "Diego", "offered_equity")],
            },
            {
                "text": "We're critically understaffed on Friday and Saturday dinner service — lost two servers and can't find replacements",
                "type": "episodic",
                "importance": 0.7,
                "valence": -0.5,
                "entities": [("The Pearl Kitchen", "server shortage", "facing")],
            },
            {
                "text": "Promoted line cook Marco to permanent sous chef — he's earned it after stepping up for 8 months",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Marco", "sous chef", "promoted_to"), ("Marco", "The Pearl Kitchen", "sous_chef_at")],
            },
            {
                "text": "Started a new server training program: 3 full days of shadowing an experienced server before any solo shifts",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.2,
                "entities": [("The Pearl Kitchen", "server training", "new_program")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTH 12 — YEAR-END
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "month12_year_end",
        "time_offset_days": 355,
        "memories": [
            {
                "text": "Annual revenue came in at 2.2 million with a 12% profit margin, up from 9% last year",
                "type": "semantic",
                "importance": 0.9,
                "valence": 0.6,
                "entities": [("The Pearl Kitchen", "2.2M annual revenue", "achieved"), ("The Pearl Kitchen", "12% profit margin", "achieved")],
            },
            {
                "text": "Won Best Farm-to-Table Restaurant from Portland Monthly magazine — the whole team celebrated at the bar after service",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.8,
                "entities": [("The Pearl Kitchen", "Portland Monthly", "awarded_by"), ("The Pearl Kitchen", "Best Farm-to-Table", "won")],
            },
            {
                "text": "Lily got early admission to Stanford's pre-med track — Sarah and I cried happy tears when the email came",
                "type": "episodic",
                "importance": 1.0,
                "valence": 1.0,
                "entities": [("Lily", "Stanford", "admitted_to"), ("Lily", "pre-med", "enrolled_in")],
            },
            {
                "text": "Ethan's soccer team won the regional tournament and he scored the winning goal in the final minute",
                "type": "episodic",
                "importance": 0.8,
                "valence": 0.9,
                "entities": [("Ethan", "regional tournament", "won"), ("Ethan", "winning goal", "scored")],
            },
            {
                "text": "Alberta District renovation is on track — contractor Pete says we're opening in March as planned",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("Pearl Kitchen Local", "March opening", "on_track"), ("Pete", "renovation", "on_schedule")],
            },
            {
                "text": "The Bon Appetit article was published and called The Pearl Kitchen 'Portland's best-kept secret' — reservations jumped 40%",
                "type": "episodic",
                "importance": 0.9,
                "valence": 0.9,
                "entities": [("Bon Appetit", "The Pearl Kitchen", "featured"), ("The Pearl Kitchen", "Bon Appetit article", "published")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — COOKING TECHNIQUES
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "cooking_techniques",
        "time_offset_days": 5,
        "memories": [
            {
                "text": "My approach to risotto is low and slow — 18 minutes of constant stirring with warm stock, finishing with cold butter for creaminess",
                "type": "procedural",
                "importance": 0.6,
                "valence": 0.4,
                "entities": [("Marcus", "risotto technique", "practices")],
            },
            {
                "text": "For the miso glaze I use a 3:2:1 ratio of white miso, mirin, and sake — let it marinate for 48 hours minimum",
                "type": "procedural",
                "importance": 0.6,
                "valence": 0.3,
                "entities": [("Marcus", "miso glaze", "technique")],
            },
            {
                "text": "The key to our farm-to-table approach is never ordering more than 3 days of perishables — freshness is everything",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("The Pearl Kitchen", "farm-to-table", "philosophy")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — PORTLAND FOOD SCENE & COMMUNITY
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "portland_community",
        "time_offset_days": 60,
        "memories": [
            {
                "text": "I'm on the board of the Portland Culinary Alliance — we meet monthly to support local restaurants and food policy",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.3,
                "entities": [("Marcus", "Portland Culinary Alliance", "board_member")],
            },
            {
                "text": "Best friend in the Portland food scene is Ben, who owns the ramen shop Marukin — we swap ingredients when one of us runs short",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Marcus", "Ben", "close_friend"), ("Ben", "Marukin", "owns")],
            },
            {
                "text": "The Pearl Kitchen hosts a charity dinner every quarter for the Oregon Food Bank — we've raised 45K so far this year",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.6,
                "entities": [("The Pearl Kitchen", "Oregon Food Bank", "supports"), ("The Pearl Kitchen", "charity dinner", "hosts")],
            },
            {
                "text": "I mentor two young cooks from the Portland Community College culinary program — reminds me of when I was starting out",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.5,
                "entities": [("Marcus", "Portland Community College", "mentors_at")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — HOBBIES & PERSONAL INTERESTS
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "hobbies_interests",
        "time_offset_days": 100,
        "memories": [
            {
                "text": "I collect vintage Japanese chef's knives — my prized one is a 1960s Masamoto gyuto that I found in a Tokyo antique shop",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Marcus", "Japanese knives", "collects"), ("Marcus", "Masamoto gyuto", "owns")],
            },
            {
                "text": "Sarah and I have date night every Tuesday — it's our one night when neither of us works late",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.6,
                "entities": [("Marcus", "Sarah", "date_night")],
            },
            {
                "text": "I've been reading Kitchen Confidential by Anthony Bourdain for the third time — it still hits different every read",
                "type": "episodic",
                "importance": 0.4,
                "valence": 0.4,
                "entities": [("Marcus", "Kitchen Confidential", "reading")],
            },
            {
                "text": "Ethan and I have a tradition of watching Trail Blazers games together on the couch — he's finally taller than me sitting down",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.7,
                "entities": [("Marcus", "Ethan", "bonding_activity"), ("Marcus", "Trail Blazers", "fan_of")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — EARLY CAREER & MEMORIES
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "early_career",
        "time_offset_days": 3,
        "memories": [
            {
                "text": "I grew up in San Francisco's Sunset District — spent my childhood in Mei-Lin's kitchen learning to fold dumplings",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.7,
                "entities": [("Marcus", "Sunset District", "grew_up_in"), ("Marcus", "Mei-Lin", "learned_from")],
            },
            {
                "text": "The Pearl Kitchen opened 8 years ago with just me, a dishwasher, and one line cook — now we have a team of 22",
                "type": "semantic",
                "importance": 0.7,
                "valence": 0.5,
                "entities": [("The Pearl Kitchen", "8 years old", "age"), ("The Pearl Kitchen", "22 staff", "team_size")],
            },
            {
                "text": "Chef Thomas taught me that the difference between a good cook and a great chef is consistency under pressure",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.4,
                "entities": [("Chef Thomas", "Marcus", "wisdom_shared")],
            },
            {
                "text": "My first year in Portland I worked 16-hour days 6 days a week and almost burned out — Sarah kept me grounded",
                "type": "episodic",
                "importance": 0.6,
                "valence": -0.2,
                "entities": [("Marcus", "burnout", "experienced"), ("Sarah", "Marcus", "supported")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — SARAH & RELATIONSHIP
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "sarah_relationship",
        "time_offset_days": 150,
        "memories": [
            {
                "text": "Sarah won Teacher of the Year at Lincoln High — the students surprised her with a standing ovation at the assembly",
                "type": "episodic",
                "importance": 0.7,
                "valence": 0.8,
                "entities": [("Sarah", "Teacher of the Year", "won"), ("Sarah", "Lincoln High", "awarded_at")],
            },
            {
                "text": "Sarah and I met 20 years ago at a dinner party in New York — she ordered the most expensive wine and I was immediately impressed",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.7,
                "entities": [("Marcus", "Sarah", "met_in_NYC")],
            },
            {
                "text": "Sarah's book club meets every other Wednesday — they're reading Educated by Tara Westover right now",
                "type": "semantic",
                "importance": 0.3,
                "valence": 0.2,
                "entities": [("Sarah", "book club", "member_of")],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SUPPLEMENTAL — MEI-LIN & DIM SUM TRADITION
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "meilin_tradition",
        "time_offset_days": 30,
        "memories": [
            {
                "text": "Mei-Lin has run Golden Lotus for 35 years — she still makes the har gow by hand every morning at 5am",
                "type": "semantic",
                "importance": 0.6,
                "valence": 0.5,
                "entities": [("Mei-Lin", "Golden Lotus", "35_years"), ("Mei-Lin", "har gow", "handmade")],
            },
            {
                "text": "Dad Henry does the books for Golden Lotus even in retirement — he says it keeps his mind sharp",
                "type": "semantic",
                "importance": 0.5,
                "valence": 0.4,
                "entities": [("Henry", "Golden Lotus", "does_books_for")],
            },
            {
                "text": "Mei-Lin's secret to her famous siu mai is a splash of Shaoxing wine in the filling — she made me promise never to tell anyone",
                "type": "procedural",
                "importance": 0.5,
                "valence": 0.5,
                "entities": [("Mei-Lin", "siu mai", "secret_recipe")],
            },
        ],
    },
]


# ── Golden Queries for Marcus Persona ────────────────────────────────────────
# 35 queries testing diverse retrieval challenges across Marcus's life.

MARCUS_QUERIES = [
    # ─── IDENTITY / BASIC (3) ───
    {
        "id": "marcus_01_who",
        "query": "Who is Marcus and what does he do?",
        "expected_texts": [
            "My name is Marcus Chen, I'm 45 years old and I own The Pearl Kitchen in Portland's Pearl District",
            "I trained at the Culinary Institute of America in Hyde Park, New York",
        ],
        "test_tags": ["identity", "semantic"],
        "description": "Basic identity retrieval",
    },
    {
        "id": "marcus_02_family",
        "query": "Tell me about Marcus's family",
        "expected_texts": [
            "My wife Sarah is a high school English teacher at Lincoln High in Portland",
            "Our daughter Lily is 16, on the debate team, and wants to study pre-med at Stanford",
            "Our son Ethan is 13, plays soccer, and is a huge video game enthusiast",
            "My parents live in San Francisco — Dad Henry is a retired accountant and Mom Mei-Lin runs the Golden Lotus dim sum restaurant",
        ],
        "test_tags": ["identity", "graph"],
        "description": "Family relationships via entity graph",
    },
    {
        "id": "marcus_03_background",
        "query": "Where did Marcus train as a chef?",
        "expected_texts": [
            "I trained at the Culinary Institute of America in Hyde Park, New York",
            "My mentor was Chef Thomas at Le Bernardin in NYC before I moved to Portland to open my own place",
        ],
        "test_tags": ["identity", "semantic"],
        "description": "Educational and career background",
    },

    # ─── RESTAURANT BUSINESS (6) ───
    {
        "id": "marcus_04_signature_dish",
        "query": "What is The Pearl Kitchen's signature dish?",
        "expected_texts": [
            "Our signature dish is the Pacific Northwest dungeness crab risotto — it's been on the menu since day one",
        ],
        "test_tags": ["restaurant", "semantic"],
        "description": "Signature dish recall",
    },
    {
        "id": "marcus_05_revenue",
        "query": "How much revenue does The Pearl Kitchen generate?",
        "expected_texts": [
            "Monthly revenue is around 180K with food costs at 35% and labor at 30%",
            "Monthly revenue hit 210K this month — our best month ever, up from the usual 180K",
            "Annual revenue came in at 2.2 million with a 12% profit margin, up from 9% last year",
        ],
        "test_tags": ["restaurant", "financial"],
        "description": "Revenue tracking over time",
    },
    {
        "id": "marcus_06_staff",
        "query": "Who works at The Pearl Kitchen?",
        "expected_texts": [
            "Head chef Diego has been with me for 5 years and is phenomenal with sauces — he's the backbone of our kitchen",
            "Sous chef Tomoko recently joined us from Tempura Kondo in Tokyo, which has a Michelin star",
            "Our sommelier Claire curates the wine list and specializes in Oregon Pinot Noir",
            "Hired pastry chef Isabelle Laurent from Paris — her tarte tatin is absolutely unreal and our dessert sales doubled",
        ],
        "test_tags": ["restaurant", "graph"],
        "description": "Staff member recall via entity graph",
    },
    {
        "id": "marcus_07_reviews",
        "query": "What press coverage has The Pearl Kitchen received?",
        "expected_texts": [
            "We got a 4-star review in The Oregonian from food critic Janet Miller — she loved the ambiance and the tasting menu",
            "The Bon Appetit article was published and called The Pearl Kitchen 'Portland's best-kept secret' — reservations jumped 40%",
            "Won Best Farm-to-Table Restaurant from Portland Monthly magazine — the whole team celebrated at the bar after service",
        ],
        "test_tags": ["restaurant", "semantic"],
        "description": "Press and awards recall",
    },
    {
        "id": "marcus_08_menu",
        "query": "What new dishes have been added to the menu?",
        "expected_texts": [
            "Tomoko's miso-glazed black cod has become our most popular dish — outselling even the crab risotto",
            "Spring menu launch was a hit — the Oregon white truffle risotto is getting rave reviews from regulars",
        ],
        "test_tags": ["restaurant", "semantic"],
        "description": "Menu evolution tracking",
    },
    {
        "id": "marcus_09_james_beard",
        "query": "Has Marcus received any culinary awards or nominations?",
        "expected_texts": [
            "The Pearl Kitchen received a James Beard Foundation semifinalist nomination for Best Chef Northwest — I couldn't believe it",
            "Won Best Farm-to-Table Restaurant from Portland Monthly magazine — the whole team celebrated at the bar after service",
        ],
        "test_tags": ["restaurant", "semantic"],
        "description": "Awards and recognition",
    },

    # ─── PEOPLE / GRAPH (5) ───
    {
        "id": "marcus_10_diego",
        "query": "Who is Diego and what is his role?",
        "expected_texts": [
            "Head chef Diego has been with me for 5 years and is phenomenal with sauces — he's the backbone of our kitchen",
            "Diego threatened to leave for rival restaurant Canard — he got a head chef offer with higher pay",
            "Offered Diego a partnership track — 5% equity vesting over 3 years — to convince him to stay, and he accepted",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Diego's full arc from loyal chef to near-departure to partner",
    },
    {
        "id": "marcus_11_tomoko",
        "query": "Tell me about Tomoko",
        "expected_texts": [
            "Sous chef Tomoko recently joined us from Tempura Kondo in Tokyo, which has a Michelin star",
            "Tomoko's miso-glazed black cod has become our most popular dish — outselling even the crab risotto",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Staff member profile via entity chain",
    },
    {
        "id": "marcus_12_isabelle",
        "query": "Who is the pastry chef?",
        "expected_texts": [
            "Hired pastry chef Isabelle Laurent from Paris — her tarte tatin is absolutely unreal and our dessert sales doubled",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Staff member recall by role",
    },
    {
        "id": "marcus_13_claire",
        "query": "Who manages the wine program?",
        "expected_texts": [
            "Our sommelier Claire curates the wine list and specializes in Oregon Pinot Noir",
        ],
        "test_tags": ["graph", "semantic"],
        "description": "Sommelier recall by domain",
    },
    {
        "id": "marcus_14_marco",
        "query": "What happened with Marco?",
        "expected_texts": [
            "We lost our second sous chef position so I had to temporarily promote line cook Marco to fill the gap",
            "Promoted line cook Marco to permanent sous chef — he's earned it after stepping up for 8 months",
        ],
        "test_tags": ["graph", "temporal"],
        "description": "Marco's promotion arc",
    },

    # ─── HEALTH (2) ───
    {
        "id": "marcus_15_cholesterol",
        "query": "What are Marcus's health issues?",
        "expected_texts": [
            "Dr. Chen found my cholesterol is high — LDL at 180 — and prescribed atorvastatin to bring it down",
            "I quit smoking 14 months ago but still use nicotine gum occasionally when the restaurant gets really stressful",
        ],
        "test_tags": ["health", "semantic"],
        "description": "Personal health recall",
    },
    {
        "id": "marcus_16_sarah_health",
        "query": "What medical condition does Sarah have?",
        "expected_texts": [
            "Sarah was diagnosed with Hashimoto's thyroiditis and Dr. Patel put her on levothyroxine",
            "Sarah needs blood tests every 6 weeks to monitor her thyroid levels — she's been feeling really fatigued",
        ],
        "test_tags": ["health", "graph"],
        "description": "Sarah's health condition recall",
    },

    # ─── FAMILY EVENTS (4) ───
    {
        "id": "marcus_17_meilin_birthday",
        "query": "How was Mei-Lin's birthday celebration?",
        "expected_texts": [
            "Mei-Lin's 70th birthday party at Golden Lotus was amazing — 35 family members flew in from all over",
            "Uncle Frank flew in from Hong Kong for Mei-Lin's birthday — I hadn't seen him in 10 years and he looks exactly the same",
        ],
        "test_tags": ["family", "semantic"],
        "description": "Family event recall",
    },
    {
        "id": "marcus_18_lily_achievements",
        "query": "What has Lily achieved this year?",
        "expected_texts": [
            "Lily won her debate tournament semifinals at the Oregon State championship — she argued healthcare policy brilliantly",
            "Lily got early admission to Stanford's pre-med track — Sarah and I cried happy tears when the email came",
        ],
        "test_tags": ["family", "temporal"],
        "description": "Lily's achievement arc over time",
    },
    {
        "id": "marcus_19_ethan_soccer",
        "query": "How is Ethan doing with soccer?",
        "expected_texts": [
            "Ethan's wrist healed and he made the U14 travel soccer team coached by Tony Ramirez",
            "Ethan's soccer team won the regional tournament and he scored the winning goal in the final minute",
        ],
        "test_tags": ["family", "temporal"],
        "description": "Ethan's soccer journey",
    },
    {
        "id": "marcus_20_vietnam",
        "query": "Tell me about the family trip to Vietnam",
        "expected_texts": [
            "Took the whole family to Vietnam for 2 weeks — visited Hanoi, Hoi An, and Ho Chi Minh City for culinary inspiration",
            "Learned pho secrets from street vendor Tran in Hanoi's Old Quarter — he's been making pho for 40 years at the same spot",
            "Ethan ate his first balut egg in Saigon and documented the whole thing on TikTok — the video got 50K views",
        ],
        "test_tags": ["family", "semantic"],
        "description": "Travel memory recall with multiple details",
    },

    # ─── FINANCIAL / BUSINESS (3) ───
    {
        "id": "marcus_21_annual_revenue",
        "query": "What were the annual financials for The Pearl Kitchen?",
        "expected_texts": [
            "Annual revenue came in at 2.2 million with a 12% profit margin, up from 9% last year",
            "Monthly revenue is around 180K with food costs at 35% and labor at 30%",
        ],
        "test_tags": ["financial", "semantic"],
        "description": "Financial performance recall",
    },
    {
        "id": "marcus_22_rent",
        "query": "What's happening with the restaurant rent?",
        "expected_texts": [
            "The landlord wants to increase our rent from 12K to 15K per month — that's a 25% jump and I need to negotiate",
        ],
        "test_tags": ["financial", "semantic"],
        "description": "Rent negotiation recall",
    },
    {
        "id": "marcus_23_investment",
        "query": "Who is investing in the second restaurant and how much?",
        "expected_texts": [
            "My investor friend David Chen is offering 200K for 15% equity in the new location — it's a fair deal",
            "Renovation budget is 350K and contractor Pete estimates 4 months to complete the buildout",
        ],
        "test_tags": ["financial", "graph"],
        "description": "Second location investment details",
    },

    # ─── TEMPORAL ARC (3) ───
    {
        "id": "marcus_24_diego_arc",
        "query": "How did Diego's situation evolve over the year?",
        "expected_texts": [
            "Head chef Diego has been with me for 5 years and is phenomenal with sauces — he's the backbone of our kitchen",
            "Diego threatened to leave for rival restaurant Canard — he got a head chef offer with higher pay",
            "Offered Diego a partnership track — 5% equity vesting over 3 years — to convince him to stay, and he accepted",
        ],
        "test_tags": ["temporal", "graph"],
        "description": "Diego's full loyalty arc across the year",
    },
    {
        "id": "marcus_25_lily_year",
        "query": "What happened in Lily's life this year?",
        "expected_texts": [
            "Our daughter Lily is 16, on the debate team, and wants to study pre-med at Stanford",
            "Lily won her debate tournament semifinals at the Oregon State championship — she argued healthcare policy brilliantly",
            "Lily got her driver's permit and I've been teaching her to drive on weekends — I'm way more nervous than she is",
            "Lily got early admission to Stanford's pre-med track — Sarah and I cried happy tears when the email came",
        ],
        "test_tags": ["temporal", "graph"],
        "description": "Lily's year-long arc from aspirations to achievements",
    },
    {
        "id": "marcus_26_restaurant_growth",
        "query": "How did The Pearl Kitchen grow over the year?",
        "expected_texts": [
            "Monthly revenue is around 180K with food costs at 35% and labor at 30%",
            "Monthly revenue hit 210K this month — our best month ever, up from the usual 180K",
            "Annual revenue came in at 2.2 million with a 12% profit margin, up from 9% last year",
            "The Pearl Kitchen received a James Beard Foundation semifinalist nomination for Best Chef Northwest — I couldn't believe it",
        ],
        "test_tags": ["temporal", "financial"],
        "description": "Restaurant growth trajectory",
    },

    # ─── EMOTIONAL / VALENCE (2) ───
    {
        "id": "marcus_27_proudest",
        "query": "What were Marcus's proudest moments this year?",
        "expected_texts": [
            "The Pearl Kitchen received a James Beard Foundation semifinalist nomination for Best Chef Northwest — I couldn't believe it",
            "Lily got early admission to Stanford's pre-med track — Sarah and I cried happy tears when the email came",
            "Ethan's soccer team won the regional tournament and he scored the winning goal in the final minute",
        ],
        "test_tags": ["valence", "semantic"],
        "description": "Positive valence retrieval",
    },
    {
        "id": "marcus_28_stressful",
        "query": "What were the most stressful moments for Marcus?",
        "expected_texts": [
            "Diego threatened to leave for rival restaurant Canard — he got a head chef offer with higher pay",
            "I'm feeling stretched thin between running the restaurant and supporting Sarah and the kids — something has to give",
            "Sarah was diagnosed with Hashimoto's thyroiditis and Dr. Patel put her on levothyroxine",
        ],
        "test_tags": ["valence", "semantic"],
        "description": "Negative valence retrieval",
    },

    # ─── PROCEDURAL (2) ───
    {
        "id": "marcus_29_cooking_technique",
        "query": "How does Marcus make risotto?",
        "expected_texts": [
            "My approach to risotto is low and slow — 18 minutes of constant stirring with warm stock, finishing with cold butter for creaminess",
        ],
        "test_tags": ["procedural", "semantic"],
        "description": "Cooking technique procedural memory",
    },
    {
        "id": "marcus_30_restaurant_processes",
        "query": "What training do new servers go through?",
        "expected_texts": [
            "Started a new server training program: 3 full days of shadowing an experienced server before any solo shifts",
        ],
        "test_tags": ["procedural", "semantic"],
        "description": "Restaurant operations procedural recall",
    },

    # ─── CROSS-DOMAIN / MULTI-HOP (3) ───
    {
        "id": "marcus_31_ohsu",
        "query": "Who has been treated at OHSU?",
        "expected_texts": [
            "Ethan broke his wrist playing soccer and Dr. Park at OHSU put on a cast for 6 weeks",
        ],
        "test_tags": ["graph", "cross_domain"],
        "description": "Cross-domain entity query for medical institution",
    },
    {
        "id": "marcus_32_portland",
        "query": "What connections does Marcus have across Portland?",
        "expected_texts": [
            "My name is Marcus Chen, I'm 45 years old and I own The Pearl Kitchen in Portland's Pearl District",
            "I'm seriously considering opening a second location in Portland's Alberta District",
            "I started cycling to work instead of driving — it's 6 miles each way through Portland's bike lanes",
        ],
        "test_tags": ["graph", "cross_domain"],
        "description": "Location-based multi-hop query across domains",
    },
    {
        "id": "marcus_33_second_restaurant",
        "query": "What are all the details about the second restaurant?",
        "expected_texts": [
            "Signed the lease for a 2,400 square foot space in Alberta District for the second restaurant",
            "The second location concept is Pearl Kitchen Local — a casual counter-service version with smaller plates and faster turnover",
            "My investor friend David Chen is offering 200K for 15% equity in the new location — it's a fair deal",
            "Hired architecture firm Skylab to design the Alberta District space — they're known for Portland's best restaurant interiors",
            "Alberta District renovation is on track — contractor Pete says we're opening in March as planned",
        ],
        "test_tags": ["cross_domain", "semantic"],
        "description": "Multi-detail aggregation across sessions about second location",
    },

    # ─── SEMANTIC GAP (2) ───
    {
        "id": "marcus_34_mental_health",
        "query": "Is Marcus getting any help for his wellbeing?",
        "expected_texts": [
            "Started seeing therapist Dr. Kim for weekly stress management sessions — she's helping me set boundaries",
            "I started cycling to work instead of driving — it's 6 miles each way through Portland's bike lanes",
        ],
        "test_tags": ["semantic_gap", "semantic"],
        "description": "Semantic gap: wellbeing maps to therapy and exercise",
    },
    {
        "id": "marcus_35_supply_chain",
        "query": "How have ingredient costs and sourcing changed?",
        "expected_texts": [
            "Food costs jumped 8% this quarter due to supply chain issues — I'm considering a menu price increase of 10-12%",
            "We partnered with Cascade Farms for organic produce delivery twice a week — the quality is incredible",
        ],
        "test_tags": ["semantic_gap", "semantic"],
        "description": "Semantic gap: ingredient sourcing maps to food costs and farm partnerships",
    },
]


# ── Deterministic Vector Generation ──────────────────────────────────────────

def _deterministic_vec(seed: float, dim: int) -> list[float]:
    """Generate a deterministic unit vector from a seed value."""
    raw = [(seed + i) * 0.1 + math.sin(seed * (i + 1)) * 0.3 for i in range(dim)]
    norm = math.sqrt(sum(x * x for x in raw))
    if norm == 0:
        raw[0] = 1.0
        norm = 1.0
    return [x / norm for x in raw]


# ── Noise Memory Generator ──────────────────────────────────────────────────
# Generates ~5000 realistic daily-life memories from domain-specific templates.
# Each domain has templates with slots filled by random choices.
# Memories are distributed across the 365-day (12-month) timeline.

# Kitchen operations templates
_KITCHEN_TEMPLATES = [
    ("Morning prep: broke down {protein} and prepped {vegetable} for tonight's service", "episodic", 0.2, 0.1, None),
    ("Ordered {quantity} pounds of {ingredient} from {supplier} for this week", "episodic", 0.2, 0.0, None),
    ("86'd the {dish} tonight — ran out of {ingredient} by 8pm", "episodic", 0.3, -0.3, None),
    ("New special tonight: {protein} with {sauce} and {side} — sold {count} plates", "episodic", 0.3, 0.4, None),
    ("Inventory count: {ingredient} is running low, need to order by tomorrow morning", "episodic", 0.2, -0.1, None),
    ("Walk-in freezer organized and rotated — everything properly labeled with dates", "procedural", 0.2, 0.1, None),
    ("Tested a new {dish_type} recipe using {technique} — needs more seasoning but the concept works", "episodic", 0.3, 0.2, None),
    ("Fish delivery from {supplier} arrived late — had to substitute {protein} on the tasting menu", "episodic", 0.3, -0.3, None),
    ("Prep list for tomorrow: {task1}, {task2}, and {task3}", "procedural", 0.2, 0.0, None),
    ("Received {quantity} cases of {ingredient} from Cascade Farms — beautiful quality this week", "episodic", 0.2, 0.3, "cascade"),
]

_KITCHEN_PROTEINS = ["salmon", "halibut", "duck breast", "lamb rack", "pork belly", "black cod",
                     "dungeness crab", "beef tenderloin", "chicken thighs", "scallops", "prawns", "venison"]
_KITCHEN_VEGETABLES = ["broccolini", "heirloom tomatoes", "butternut squash", "asparagus", "fava beans",
                       "wild mushrooms", "rainbow chard", "baby carrots", "fennel", "artichokes"]
_KITCHEN_SAUCES = ["beurre blanc", "demi-glace", "chimichurri", "ponzu reduction", "truffle cream",
                   "romesco", "salsa verde", "miso butter", "red wine jus", "tamarind glaze"]
_KITCHEN_SIDES = ["roasted fingerlings", "risotto", "grilled broccolini", "mashed cauliflower",
                  "sauteed greens", "polenta", "wild rice", "charred leeks"]
_KITCHEN_SUPPLIERS = ["Pacific Seafood", "Cascade Farms", "Nicky USA", "Sheridan Fruit Company",
                      "Portland Fish Company", "Olympia Provisions"]
_KITCHEN_TASKS = ["butcher the lamb", "make stock", "prep dessert components", "roast bones for demi",
                  "blanch vegetables", "make pasta dough", "cure the salmon", "reduce the wine"]

# Service templates
_SERVICE_TEMPLATES = [
    ("Tonight's covers: {covers} — {pace} night with {wait} minute average wait for tables", "episodic", 0.3, 0.1, None),
    ("Table {table_num} complained about {complaint} — comped their {comp_item}", "episodic", 0.3, -0.3, None),
    ("Reservations for Saturday are fully booked at {count} covers — added {extra} to the waitlist", "episodic", 0.2, 0.3, None),
    ("Bar revenue tonight: ${amount} — cocktail special was the {cocktail}", "episodic", 0.2, 0.2, None),
    ("Private dining room booked for {event} — {guests} guests at ${price_per} per person", "episodic", 0.3, 0.3, None),
    ("{vip} came in tonight for the chef's counter — sent out an extra amuse-bouche", "episodic", 0.3, 0.4, None),
    ("Food runner called in sick — had to pull {person} from the bar to help expedite", "episodic", 0.3, -0.2, None),
    ("Average ticket tonight: ${avg_ticket} — {trend} compared to last week", "episodic", 0.2, 0.1, None),
    ("OpenTable rating this month: {rating} stars from {review_count} reviews", "episodic", 0.3, 0.3, None),
    ("Walk-in party of {walk_in} — managed to seat them at the bar with a modified menu", "episodic", 0.2, 0.2, None),
]

_SERVICE_COMPLAINTS = ["the steak being overcooked", "slow service", "a hair in the salad", "the noise level",
                       "the wine being too warm", "waiting too long for dessert", "cold food"]
_SERVICE_COCKTAILS = ["Pearl District Old Fashioned", "Lavender Gimlet", "Smoked Manhattan",
                      "Cucumber Collins", "Espresso Martini", "Seasonal Spritz"]

# Staff templates
_STAFF_TEMPLATES = [
    ("Shift schedule for the week: Diego on {days1}, Tomoko {days2}, Marco {days3}", "procedural", 0.2, 0.0, None),
    ("{person} called out sick today — {backup} is covering their station", "episodic", 0.3, -0.2, None),
    ("Training session with {person} on {skill} — they're {progress}", "episodic", 0.3, 0.2, None),
    ("Pre-service meeting: reviewed tonight's specials and {topic} with the team", "episodic", 0.2, 0.1, None),
    ("Line cook {person} struggling with {station} — pairing them with Diego for mentoring", "episodic", 0.3, -0.1, None),
    ("{person} asked for {request} — need to figure out scheduling", "episodic", 0.2, -0.1, None),
    ("New hire orientation: {person} started today as {role} — seems {impression}", "episodic", 0.3, 0.2, None),
    ("Performance review with {person}: strong on {strength}, needs work on {weakness}", "episodic", 0.3, 0.1, None),
    ("Staff meal today: {person} made {dish} for the team — everyone loved it", "episodic", 0.2, 0.4, None),
    ("Quarterly tip pool distribution: servers averaged ${amount} per shift this month", "episodic", 0.2, 0.1, None),
]

_STAFF_PEOPLE = ["Diego", "Tomoko", "Marco", "Claire", "Isabelle", "Alex", "Jordan", "Sam", "Nina", "Luis"]
_STAFF_SKILLS = ["sauce making", "plating technique", "wine service", "pastry fundamentals",
                 "fish butchery", "bread baking", "cocktail mixing", "expediting"]
_STAFF_STATIONS = ["grill", "sauté", "pastry", "garde manger", "fish"]

# Family mundane templates
_FAMILY_TEMPLATES = [
    ("Drove Lily to {activity} and waited in the parking lot doing restaurant paperwork", "episodic", 0.2, 0.0, None),
    ("Helped Ethan with his {subject} homework — he's {reaction}", "episodic", 0.2, 0.2, None),
    ("Sarah told me about {school_event} at Lincoln High — she's {feeling} about it", "episodic", 0.2, 0.2, None),
    ("Family dinner at home tonight — made {dish} and everyone actually sat down together", "episodic", 0.3, 0.5, None),
    ("Ethan played {game} for {hours} hours straight — had to pry the controller away for dinner", "episodic", 0.2, -0.1, None),
    ("Lily practicing her debate arguments at the dinner table — she's {assessment}", "episodic", 0.2, 0.3, None),
    ("Video call with Mom and Dad in San Francisco — Dad told a story about {topic}", "episodic", 0.2, 0.4, "parents"),
    ("Sarah's grading papers tonight — she has {count} essays on {book} to get through", "episodic", 0.1, -0.1, None),
    ("Sunday morning farmers market run with {person} — picked up {items}", "episodic", 0.2, 0.4, None),
    ("Dropped off Ethan at soccer practice with coach Tony then headed to the restaurant", "episodic", 0.1, 0.1, None),
]

_FAMILY_ACTIVITIES = ["debate practice", "SAT prep class", "study group at the library",
                      "volunteer shift at the hospital", "piano lesson"]
_FAMILY_SUBJECTS = ["algebra", "biology", "history", "English essay", "science project"]
_FAMILY_GAMES = ["Fortnite", "Minecraft", "FIFA", "Zelda", "Call of Duty"]
_FAMILY_HOME_DISHES = ["stir-fried noodles", "spaghetti bolognese", "grilled chicken", "fried rice",
                       "tacos", "Mom's mapo tofu recipe", "teriyaki salmon", "pad thai"]
_FAMILY_BOOKS = ["The Great Gatsby", "To Kill a Mockingbird", "1984", "Romeo and Juliet", "Hamlet"]

# Health / fitness templates
_HEALTH_TEMPLATES = [
    ("Bike ride to work: {distance} miles in {minutes} minutes — {condition}", "episodic", 0.2, 0.3, None),
    ("Cholesterol check at Dr. Chen's office — LDL is {ldl}, {trend}", "episodic", 0.3, 0.1, None),
    ("Slept {hours} hours — {quality}", "episodic", 0.1, 0.0, None),
    ("Cycling training with Jake: {route} — {distance} miles at {pace} pace", "episodic", 0.2, 0.3, "jake"),
    ("Used nicotine gum today after a stressful {event} — need to wean off completely", "episodic", 0.3, -0.2, None),
    ("Therapy session with Dr. Kim — talked about {topic}", "episodic", 0.3, 0.2, "dr_kim"),
    ("Stretched and foam rolled after cycling — my {body_part} is tight from standing all day", "episodic", 0.1, 0.1, None),
    ("Weighed in at {weight} pounds — {trend} from last month", "episodic", 0.2, 0.0, None),
    ("Morning yoga before heading to the restaurant — helps with the back pain from standing in the kitchen all day", "episodic", 0.2, 0.3, None),
]

_HEALTH_ROUTES = ["Waterfront Park loop", "Sellwood Bridge out-and-back", "Forest Park climb",
                  "Springwater Corridor trail", "Hawthorne Bridge circuit"]
_HEALTH_TOPICS = ["work-life balance", "setting boundaries with staff", "guilt about not being home enough",
                  "managing the expansion stress", "relationship with my father"]
_HEALTH_BODY_PARTS = ["lower back", "calves", "shoulders", "knees", "hamstrings"]

# Finance templates
_FINANCE_TEMPLATES = [
    ("Paid supplier invoices: ${amount} to {supplier} for this week's deliveries", "episodic", 0.2, -0.1, None),
    ("POS report: ${daily_rev} revenue today, {covers} covers, ${avg_check} average check", "episodic", 0.2, 0.1, None),
    ("Tip distribution for the week: front of house total ${tips}", "episodic", 0.2, 0.0, None),
    ("Utility bill for the restaurant: ${amount} — {trend} compared to last month", "episodic", 0.2, -0.1, None),
    ("Insurance premium due: ${amount} for restaurant liability and property", "episodic", 0.2, -0.1, None),
    ("Reviewed Toast analytics: top-selling item is {item}, lowest margin is {low_item}", "episodic", 0.2, 0.0, None),
    ("Payroll this week: ${amount} for {count} staff members", "episodic", 0.2, -0.1, None),
    ("Credit card processing fees this month: ${amount} — considering switching to {processor}", "episodic", 0.2, -0.1, None),
    ("Monthly P&L: revenue ${revenue}K, COGS ${cogs}K, labor ${labor}K, net ${net}K", "episodic", 0.3, 0.1, None),
    ("Renovation invoice from Pete: ${amount} for {phase} — {status} budget", "episodic", 0.3, -0.1, "renovation"),
]

_FINANCE_ITEMS = ["dungeness crab risotto", "miso-glazed black cod", "tasting menu",
                  "Oregon Pinot Noir by the glass", "chef's counter experience"]
_FINANCE_PROCESSORS = ["Square", "Stripe", "Heartland", "Clover"]
_FINANCE_PHASES = ["framing and electrical", "plumbing rough-in", "hood installation",
                   "flooring and tile", "equipment delivery"]

# Portland life templates
_PORTLAND_TEMPLATES = [
    ("Portland weather: {temp}°F, {condition} — {reaction}", "episodic", 0.1, 0.0, None),
    ("Farmers market at {market}: picked up {items} for this week's specials", "episodic", 0.2, 0.3, None),
    ("Traffic on {road} was brutal today — {minutes} minute commute instead of the usual 20", "episodic", 0.1, -0.2, None),
    ("{event} in the Pearl District this weekend — could be good or bad for restaurant foot traffic", "episodic", 0.2, 0.1, None),
    ("Stopped at {coffee_shop} for coffee before opening the restaurant", "episodic", 0.1, 0.2, None),
    ("Neighborhood association meeting about {topic} in the Pearl District", "episodic", 0.2, 0.0, None),
    ("Ran into {person} at {location} — chatted about {topic}", "episodic", 0.2, 0.2, None),
    ("Beautiful {season} day in Portland — {observation}", "episodic", 0.1, 0.4, None),
]

_PORTLAND_MARKETS = ["PSU Farmers Market", "Hollywood Farmers Market", "Beaverton Farmers Market",
                     "King Farmers Market"]
_PORTLAND_ROADS = ["I-5", "Burnside Bridge", "I-405", "Highway 26", "MLK Boulevard"]
_PORTLAND_EVENTS = ["First Thursday art walk", "Portland Saturday Market", "food cart festival",
                    "Oregon Brewers Festival", "Pearl District block party", "Portland Marathon"]
_PORTLAND_COFFEE = ["Stumptown Coffee", "Heart Coffee Roasters", "Case Study Coffee",
                    "Coava Coffee", "Barista Portland", "Good Coffee"]
_PORTLAND_TOPICS = ["the new bike lane", "parking changes", "a new restaurant opening",
                    "the homeless situation", "construction noise", "upcoming city council vote"]


def _fill_kitchen_template(template, rng, day):
    """Fill kitchen operations template slots."""
    text, mtype, imp, val, entity_mode = template
    protein = rng.choice(_KITCHEN_PROTEINS)
    ingredient = rng.choice(_KITCHEN_PROTEINS + _KITCHEN_VEGETABLES)
    supplier = rng.choice(_KITCHEN_SUPPLIERS)

    filled = text.format(
        protein=protein, vegetable=rng.choice(_KITCHEN_VEGETABLES),
        quantity=rng.randint(10, 80), ingredient=ingredient,
        supplier=supplier, dish=rng.choice(["black cod", "crab risotto", "duck", "lamb", "halibut"]),
        count=rng.randint(15, 45), sauce=rng.choice(_KITCHEN_SAUCES),
        side=rng.choice(_KITCHEN_SIDES),
        dish_type=rng.choice(["appetizer", "entree", "dessert", "amuse-bouche"]),
        technique=rng.choice(["sous vide", "smoking", "fermenting", "curing", "braising"]),
        task1=rng.choice(_KITCHEN_TASKS), task2=rng.choice(_KITCHEN_TASKS), task3=rng.choice(_KITCHEN_TASKS),
    )
    if entity_mode == "cascade":
        entities = [("The Pearl Kitchen", "Cascade Farms", "sources_from")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_service_template(template, rng, day):
    """Fill service template slots."""
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        covers=rng.randint(60, 140),
        pace=rng.choice(["steady", "slammed", "quiet", "chaotic", "smooth"]),
        wait=rng.randint(5, 45),
        table_num=rng.randint(1, 25),
        complaint=rng.choice(_SERVICE_COMPLAINTS),
        comp_item=rng.choice(["desserts", "appetizer", "drinks", "entrees"]),
        count=rng.randint(70, 130), extra=rng.randint(5, 25),
        amount=rng.randint(800, 3500),
        cocktail=rng.choice(_SERVICE_COCKTAILS),
        event=rng.choice(["a birthday dinner", "corporate event", "anniversary celebration", "wine dinner"]),
        guests=rng.randint(8, 30),
        price_per=rng.randint(85, 175),
        vip=rng.choice(["A regular", "The mayor", "A food blogger", "A local chef", "A James Beard judge"]),
        person=rng.choice(_STAFF_PEOPLE),
        avg_ticket=rng.randint(55, 120),
        trend=rng.choice(["up 8%", "down 5%", "about the same", "up 12%"]),
        rating=round(rng.uniform(4.0, 4.9), 1),
        review_count=rng.randint(15, 60),
        walk_in=rng.randint(2, 8),
    )
    return filled, mtype, imp, val, []


def _fill_staff_template(template, rng, day):
    """Fill staff template slots."""
    text, mtype, imp, val, entity_mode = template
    person = rng.choice(_STAFF_PEOPLE)
    filled = text.format(
        person=person,
        days1=rng.choice(["Mon-Fri", "Tue-Sat", "Wed-Sun"]),
        days2=rng.choice(["Mon-Fri", "Tue-Sat", "Wed-Sun"]),
        days3=rng.choice(["Mon-Fri", "Tue-Sat", "Thu-Mon"]),
        backup=rng.choice(_STAFF_PEOPLE),
        skill=rng.choice(_STAFF_SKILLS),
        progress=rng.choice(["improving quickly", "struggling a bit", "almost ready for solo", "doing great"]),
        topic=rng.choice(["wine pairings", "allergy protocols", "the new POS system", "VIP guest preferences"]),
        station=rng.choice(_STAFF_STATIONS),
        request=rng.choice(["time off next week", "a schedule change", "a raise", "to switch stations"]),
        role=rng.choice(["line cook", "server", "bartender", "food runner", "host"]),
        impression=rng.choice(["promising", "nervous but eager", "experienced", "a great fit"]),
        strength=rng.choice(["speed", "technique", "teamwork", "consistency", "creativity"]),
        weakness=rng.choice(["plating", "communication", "time management", "cleanliness", "mise en place"]),
        dish=rng.choice(["tacos al pastor", "pho", "bibimbap", "pasta carbonara", "jerk chicken"]),
        amount=rng.randint(150, 350),
    )
    entities = [("Marcus", person, "manages")]
    return filled, mtype, imp, val, entities


def _fill_family_template(template, rng, day):
    """Fill family mundane template slots."""
    text, mtype, imp, val, entity_mode = template
    person = rng.choice(["Lily", "Ethan", "Sarah"])
    filled = text.format(
        activity=rng.choice(_FAMILY_ACTIVITIES),
        subject=rng.choice(_FAMILY_SUBJECTS),
        reaction=rng.choice(["getting the hang of it", "frustrated", "doing well", "needs more help"]),
        school_event=rng.choice(["parent-teacher conference", "the school play", "a faculty meeting",
                                 "homecoming week", "standardized testing"]),
        feeling=rng.choice(["excited", "stressed", "amused", "concerned"]),
        dish=rng.choice(_FAMILY_HOME_DISHES),
        game=rng.choice(_FAMILY_GAMES),
        hours=rng.randint(2, 5),
        assessment=rng.choice(["getting sharper", "really persuasive", "preparing hard", "very confident"]),
        topic=rng.choice(["his golf game", "the old neighborhood", "Mom's restaurant", "when I was a kid"]),
        count=rng.randint(20, 60),
        book=rng.choice(_FAMILY_BOOKS),
        person=person,
        items=rng.choice(["berries, kale, and fresh eggs", "artisan bread and honey",
                          "heirloom tomatoes and basil", "peaches and corn"]),
    )
    if entity_mode == "parents":
        entities = [("Marcus", "Henry", "called"), ("Marcus", "Mei-Lin", "called")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_health_template(template, rng, day):
    """Fill health/fitness template slots."""
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        distance=round(rng.uniform(4, 15), 1),
        minutes=rng.randint(20, 65),
        condition=rng.choice(["rainy but warm", "crisp morning", "overcast", "sunny and dry", "foggy"]),
        ldl=rng.randint(140, 200),
        trend=rng.choice(["down from last time", "still too high", "improving slowly", "about the same"]),
        hours=round(rng.uniform(4.5, 8.5), 1),
        quality=rng.choice(["woke up refreshed", "tossed and turned", "slept like a rock", "Ethan woke me up"]),
        route=rng.choice(_HEALTH_ROUTES),
        pace=rng.choice(["easy", "moderate", "fast", "recovery"]),
        event=rng.choice(["dinner service", "landlord meeting", "staff argument", "bad review online"]),
        topic=rng.choice(_HEALTH_TOPICS),
        body_part=rng.choice(_HEALTH_BODY_PARTS),
        weight=rng.randint(175, 195),
    )
    if entity_mode == "jake":
        entities = [("Marcus", "Jake", "cycling_with")]
    elif entity_mode == "dr_kim":
        entities = [("Marcus", "Dr. Kim", "therapy_session")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_finance_template(template, rng, day):
    """Fill finance template slots."""
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        amount=rng.randint(500, 25000),
        supplier=rng.choice(_KITCHEN_SUPPLIERS),
        daily_rev=rng.randint(4000, 12000),
        covers=rng.randint(50, 140),
        avg_check=rng.randint(55, 120),
        tips=rng.randint(2000, 6000),
        trend=rng.choice(["up 10%", "down 5%", "about the same", "up 3%"]),
        item=rng.choice(_FINANCE_ITEMS),
        low_item=rng.choice(["house salad", "bread basket", "soft drinks", "soup of the day"]),
        count=rng.randint(15, 30),
        processor=rng.choice(_FINANCE_PROCESSORS),
        revenue=rng.randint(150, 220),
        cogs=rng.randint(50, 80),
        labor=rng.randint(45, 70),
        net=rng.randint(10, 35),
        phase=rng.choice(_FINANCE_PHASES),
        status=rng.choice(["on", "slightly over", "under"]),
    )
    if entity_mode == "renovation":
        entities = [("Pete", "Pearl Kitchen Local", "renovating")]
    else:
        entities = []
    return filled, mtype, imp, val, entities


def _fill_portland_template(template, rng, day):
    """Fill Portland life template slots."""
    text, mtype, imp, val, entity_mode = template
    filled = text.format(
        temp=rng.randint(35, 85),
        condition=rng.choice(["overcast and drizzly", "sunny and clear", "heavy rain", "partly cloudy",
                              "misty morning", "cold and windy"]),
        reaction=rng.choice(["typical Portland", "perfect biking weather", "stayed dry for once",
                             "needed the rain jacket"]),
        market=rng.choice(_PORTLAND_MARKETS),
        items=rng.choice(["chanterelles and leeks", "stone fruit and herbs", "root vegetables and kale",
                          "oysters and fresh bread", "berries and microgreens"]),
        road=rng.choice(_PORTLAND_ROADS),
        minutes=rng.randint(30, 75),
        event=rng.choice(_PORTLAND_EVENTS),
        coffee_shop=rng.choice(_PORTLAND_COFFEE),
        topic=rng.choice(_PORTLAND_TOPICS),
        person=rng.choice(["a regular customer", "the baker from next door", "another restaurant owner",
                           "an old CIA classmate", "a food writer"]),
        location=rng.choice(["the farmers market", "Stumptown", "Powell's Books", "the bike shop"]),
        season=rng.choice(["spring", "summer", "fall", "winter"]),
        observation=rng.choice(["the trees along the waterfront are gorgeous",
                                "Mt. Hood was perfectly visible", "the cherry blossoms are in full bloom",
                                "perfect weather for the patio"]),
    )
    return filled, mtype, imp, val, []


def generate_marcus_noise(target_count=5000, seed=123):
    """Generate daily-life noise memories for Marcus.

    Returns a list of dicts, each with:
        text, type, importance, valence, entities, day_offset
    """
    rng = random.Random(seed)
    memories = []
    total_days = 365  # 12 months

    # Domain weights (memories per day on average)
    domain_schedule = [
        ("kitchen", _KITCHEN_TEMPLATES, _fill_kitchen_template, 4),
        ("service", _SERVICE_TEMPLATES, _fill_service_template, 3),
        ("staff", _STAFF_TEMPLATES, _fill_staff_template, 2),
        ("family", _FAMILY_TEMPLATES, _fill_family_template, 2),
        ("health", _HEALTH_TEMPLATES, _fill_health_template, 1),
        ("finance", _FINANCE_TEMPLATES, _fill_finance_template, 1),
        ("portland", _PORTLAND_TEMPLATES, _fill_portland_template, 1),
    ]

    # Calculate per-day rates to hit target
    total_per_day = sum(count for _, _, _, count in domain_schedule)
    # Kitchen/service/staff skip some days (restaurant closed Monday, lighter Tuesday)
    expected_raw = total_per_day * total_days - 9 * int(total_days / 7)
    scale = target_count / max(expected_raw, 1)

    for day in range(total_days):
        for domain_name, templates, filler, base_count in domain_schedule:
            # Restaurant closed Mondays (day_of_week = 0)
            if domain_name in ("kitchen", "service", "staff") and day % 7 == 0:
                if rng.random() > 0.1:  # occasionally still do prep on Mondays
                    continue

            expected = base_count * scale
            count = int(expected)
            if rng.random() < (expected - count):
                count += 1
            for _ in range(count):
                template = rng.choice(templates)
                text, mtype, imp, val, entities = filler(template, rng, day)

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

    # Shuffle within small windows to avoid perfect ordering
    for i in range(len(memories) - 1, 0, -1):
        j = rng.randint(max(0, i - 15), i)
        memories[i], memories[j] = memories[j], memories[i]

    # Trim to target
    if len(memories) > target_count:
        memories = memories[:target_count]

    return memories


# ── Loader and Evaluation Functions ──────────────────────────────────────────

def count_marcus_memories():
    """Count hand-crafted anchor memories."""
    return sum(len(s["memories"]) for s in MARCUS_SESSIONS)


def load_marcus_into_db(db, embedder=None, dim: int = 384, base_time: float | None = None,
                        target_count: int = 5000, progress_callback=None):
    """Load Marcus's full life history into a YantrikDB instance.

    Loads ~85 hand-crafted anchor memories (used by golden queries) plus
    ~target_count procedurally generated daily-life memories.

    Args:
        db: YantrikDB instance.
        embedder: Optional SentenceTransformer (or any .encode(str) object).
        dim: Embedding dimension (used for deterministic vectors when no embedder).
        base_time: Base unix timestamp. Defaults to 365 days ago (12 months).
        target_count: Number of generated daily memories to add (default 5000).
        progress_callback: Optional callable(loaded, total) for progress reporting.

    Returns:
        (text_to_rid, text_to_seed) — dicts mapping memory text to RID and seed.
    """
    if base_time is None:
        base_time = time.time() - (365 * 86400)

    text_to_rid = {}
    text_to_seed = {}
    seed_counter = 1.0

    # ── Phase 1: Load anchor memories (hand-crafted, used by golden queries) ──
    anchor_count = count_marcus_memories()
    loaded = 0

    for session in MARCUS_SESSIONS:
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

    # ── Phase 2: Generate and load daily-life noise memories ──
    if target_count > 0:
        generated = generate_marcus_noise(target_count=target_count)
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

            # Create entities (only for memories that have them)
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


def evaluate_marcus(db, text_to_rid, top_k=10, embedder=None, text_to_seed=None, dim=384):
    """Run all Marcus queries and measure recall quality.

    Returns:
        (report_string, raw_results, metrics_dict)

    metrics_dict has keys: mean_recall, mean_precision, mean_mrr,
                           recall_by_tag, pass_rate
    """
    results = []
    total_recall = 0.0
    total_precision = 0.0
    total_mrr = 0.0

    tag_scores: dict[str, list[float]] = {}

    for gq in MARCUS_QUERIES:
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

    n = len(MARCUS_QUERIES)
    mean_recall = total_recall / n
    mean_precision = total_precision / n
    mean_mrr = total_mrr / n
    recall_by_tag = {tag: sum(s) / len(s) for tag, s in tag_scores.items()}

    # Format report
    lines = [
        "",
        "=" * 70,
        "  YantrikDB Marcus Chen Persona Evaluation Report",
        "=" * 70,
        "",
        f"  Memories loaded:    {count_marcus_memories()} anchor + generated",
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
            f"    [{status}] {r['id']:30s} recall={r['recall']:.2f}  "
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
