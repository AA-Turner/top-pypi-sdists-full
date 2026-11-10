#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Corrects machine-translated values in msg_strings_<LANG>.txt.

Three kinds of correction, all keeping keys, '#' lines, line endings and the value's own leading spaces:
  1. FIXES[LANG]          explicit  "key": "correct value"  pairs (every line with that key is corrected)
  2. KEEP_ENGLISH_KEYS    keys whose value must stay English (dxx_optiony_str = divisional-chart option texts);
                          the value is copied from msg_strings_en.txt
  3. STRIP_TRAILING_DOT   a value that ends with a single '.' (and has no other '.') loses it when the English
                          value has no final '.' - the model adds sentence full stops to single words ("दीस.")
Safety: a list value (UPPERCASE key or a key ending in _list) must keep the English item count - otherwise it is
not written and reported. Values must not contain Latin letters, except in KEEP_ENGLISH_KEYS and LATIN_OK.
A backup <file>.bak is written once before the file is changed. Running it again changes nothing.

HOW TO RUN (VSCode: set LANG, press Run). The lang folder is taken from jhora, else this script's folder.
"""
import os
import re
import shutil
import sys

LANG = "kok"
DRY_RUN = False
STRIP_TRAILING_DOT = True
KEEP_ENGLISH_KEYS = re.compile(r"^d\d+_option\d+_str$")
LATIN_OK = re.compile(r"\(D\d+\)|https?://\S+|\S+@\S+")

FIXES = {
    "kok": {
        # ---- panchanga words ----
        "sunrise_str": "सूर्योदय", "sunset_str": "सूर्यास्त", "moonrise_str": "चंद्रोदय", "moonset_str": "चंद्रास्त",
        "vaaram_str": "वार", "samvatsara_str": "संवत्सर", "nakshatra_str": "नक्षत्र", "karanam_str": "करण",
        "raahu_kaalam_str": "राहू काळ", "kuligai_str": "गुलिक काळ", "yamagandam_str": "यमगंड",
        "dhurmuhurtham_str": "दुर्मुहूर्त", "ascendant_str": "लग्नℒ", "ascendant_short_str": "लग्नℒ",
        "ayanamsam_str": "अयनांश:", "udhayathi_str": "उदयादि वेळ:", "balance_str": "शिल्लक",
        "dhasa_bhukthi_str": "दशा-भुक्ति", "dhasa_str": "दशा", "horoscope_str": "जन्मकुंडली",
        "remaining_str": "उरिल्लें", "birth_str": "जन्म", "janma_rasi_str": "जन्म राशी",
        # ---- divisional charts ----
        "drekkanam_str": "द्रेक्काण (D3)", "chaturthamsa_str": "चतुर्थांश (D4)", "panchamsa_str": "पंचमांश (D5)",
        "shashthamsa_str": "षष्ठांश (D6)", "saptamsam_str": "सप्तमांश (D7)", "ashtamsa_str": "अष्टमांश (D8)",
        "navamsam_str": "नवमांश (D9)", "dhasamsam_str": "दशमांश (D10)", "rudramsa_str": "रुद्रांश (D11)",
        "dhwadamsam_str": "द्वादशांश (D12)", "shodamsa_str": "षोडशांश (D16)", "vimsamsa_str": "विंशांश (D20)",
        "chaturvimsamsa_str": "चतुर्विंशांश (D24)", "nakshatramsa_str": "नक्षत्रांश (D27)",
        "thrisamsam_str": "त्रिंशांश (D30)", "khavedamsa_str": "खवेदांश (D40)", "akshavedamsa_str": "अक्षवेदांश (D45)",
        "sashtiamsam_str": "षष्ट्यंश (D60)", "nava_navamsa_str": "नव-नवमांश (D81)",
        "ashtotharamsa_str": "अष्टोत्तरांश (D108)", "dwadas_dwadasamsa_str": "द्वादश-द्वादशांश (D144)",
        "nadiamsa_str": "नाड्यंश (D150)",
        # ---- compatibility (koota) ----
        "varna_match_str": "वर्ण कूट", "vasiya_match_str": "वश्य कूट", "gana_match_str": "गण कूट",
        "tara_match_str": "तारा कूट", "yoni_match_str": "योनी कूट", "adhipathi_match_str": "अधिपती कूट",
        "raasi_match_str": "राशी कूट", "naadi_match_str": "नाडी कूट", "mahendra_match_str": "महेंद्र कूट",
        "vedha_match_str": "वेध कूट", "rajju_match_str": "रज्जू कूट", "sthree_dheerga_match_str": "स्त्री दीर्घ कूट",
        "ayanamsa_tooltip_str": "वळेरेंतल्यान अयनांश पद्दत वेंचून काड.",
        # ---- upagrahas, ashtakavarga ----
        "upagraha_str": "उपग्रह", "kaala_str": "काल", "gulika_str": "गुलिक", "maandi_str": "मांदी", "dhuma_str": "धूम",
        "vyatipaata_str": "व्यतीपात", "indrachaapa_str": "इंद्रचाप", "upaketu_str": "उपकेतू",
        "bav_str": "भिन्न अष्टकवर्ग", "sav_str": "सर्व अष्टकवर्ग", "pav_str": "प्रस्तार अष्टकवर्ग",
        "graha_pinda_str": "ग्रह पिंड", "raasi_pinda_str": "राशी पिंड", "shodhaya_pinda_str": "शोध्य पिंड",
        "trikona_str": "त्रिकोण", "ekadhipathya_str": "एकाधिपत्य",
        # ---- special lagnas, karakas ----
        "special_lagnas_str": "खाशेलीं लग्नां", "hora_lagna_str": "होरा लग्न", "ghati_lagna_str": "घटी लग्न",
        "bhava_lagna_str": "भाव लग्न", "vighati_lagna_str": "विघटी लग्न", "sree_lagna_str": "श्री लग्न",
        "varnada_lagna_str": "वर्णद लग्न", "pranapada_lagna_str": "प्राणपद लग्न", "indu_lagna_str": "इंदू लग्न",
        "bhrigu_bindhu_lagna_str": "भृगू बिंदू", "kunda_lagna_str": "कुंड लग्न",
        "karakas_str": "कारक", "atma_karaka_str": "आत्मकारक", "amatya_karaka_str": "अमात्यकारक",
        "bhratri_karaka_str": "भ्रातृकारक", "maitri_karaka_str": "मातृकारक", "pitri_karaka_str": "पितृकारक",
        "putra_karaka_str": "पुत्रकारक", "jnaati_karaka_str": "ज्ञातिकारक", "data_karaka_str": "दारकारक",
        "graha_str": "ग्रह", "drishti_str": "दृष्टी", "virodhargala_str": "विरोधार्गला",
        # ---- dashas ----
        "vimsottari_str": "विंशोत्तरी", "rasi_bhukthi_vimsottari_str": "राशी भुक्ति विंशोत्तरी",
        "yoga_vimsottari_str": "योग विंशोत्तरी", "ashtottari_str": "अष्टोत्तरी", "tithi_ashtottari_str": "तिथी अष्टोत्तरी",
        "kendraadhi_rasi_str": "केंद्रादि राशी", "sudasa_str": "सुदशा", "drig_str": "दृग", "niryaana_str": "निर्याण",
        "nirayana_str": "निरयण", "shoola_str": "शूल", "60hrs_str": "षष्टि होरा", "annual_str": "वर्ष प्रवेश",
        "60hourly_str": "षष्टि होरा प्रवेश", "patyayini_str": "पात्यायनी", "mudda_str": "मुद्दा",
        "varsha_narayana_str": "वर्ष नारायण", "varsha_vimsottari_str": "वर्ष विंशोत्तरी",
        "shodasottari_str": "षोडशोत्तरी", "dwadasottari_str": "द्वादशोत्तरी", "dwisatpathi_str": "द्विसप्तति सम",
        "panchottari_str": "पंचोत्तरी", "satabdika_str": "शताब्दिका", "chaturaaseeti_sama_str": "चतुराशीति सम",
        "karana_chaturaaseethi_sama_str": "करण चतुराशीति सम", "shashtisama_str": "षष्टि सम",
        "shastihayani_str": "षष्टिहायनी", "shattrimsa_sama_str": "षट्त्रिंश सम", "chara_str": "चर",
        "kendraadhi_karaka_str": "कारक केंद्रादि", "lagnamsaka_str": "लग्नांशक", "padhanadhamsa_str": "पदनाथांश",
        "sthira_str": "स्थिर", "naisargika_str": "नैसर्गिक", "tara_lagna_str": "तारा लग्न", "mandooka_str": "मंडूक",
        "karaka_str": "कारक", "varnada_str": "वर्णद", "yogardha_str": "योगार्ध", "navamsa_str": "नवांश",
        "paryaaya_str": "पर्याय", "raja_yoga_pairs": "राजयोग जोड्यो:",
        "nakshathra_dhasa_progression_str": "नक्षत्र दशा प्रगती", "maha_str": "महा", "antara_str": "अंतर",
        "prathyanthara_str": "प्रत्यंतर", "sookshma_str": "सूक्ष्म", "show_running_dhasa_str": "चालू दशा दाखय",
        "dhasa_progression_correction_str": "दशेच्या प्रगतीची सुदारणी", "show_all_dhasa_levels_str": "दशेचे सगळे स्तर दाखय",
        "dhasa_level_str": "दशेचो स्तर",
        "lord_str": "अधिपती", "antara_lord_str": "अंतर अधिपती", "prathyanthara_lord_str": "प्रत्यंतर अधिपती",
        "sookshma_lord_str": "सूक्ष्म अधिपती",
        # ---- dasha options ("lord" was translated as God - भगवंत) ----
        "nisargika_dhasa_option1_str": "नैसर्गिक दशेक सकयल दिल्ले अंतर्दशेचे पर्याय आसात:",
        "nisargika_dhasa_option2_str": "महादशेच्या अधिपतीक अंतर्दशा ना (अंतर्दशा महादशेच्या अधिपती भायर हेर ग्रहांची आसतली)",
        "nisargika_dhasa_option3_str": "दशेच्या अधिपतीसावन 3ऱ्या आनी 10व्या ग्रहांक अंतर्दशा ना.",
        "nisargika_dhasa_option4_str": "दशेच्या अधिपतीसावन 2ऱ्या, 6व्या, 11व्या आनी 12व्या ग्रहांक अंतर्दशा ना.",
        "tara_dhasa_option1_str": "पराशर आनी संजय रथ हांचो दशा क्रम वेगळो आसा. एक वेंचून काड:",
        "tara_dhasa_option2_str": "1->संजय रथ पद्दतीचो दशा क्रम 5,1,8,6,4,3,7,2,0",
        "tara_dhasa_option3_str": "2->पराशर पद्दतीचो दशा क्रम 5,0,1,2,7,4,6,3,8",
        "rbv_dhasa_option_str": "राशी भुक्ति व्हेरिएशन वापर",
        "dhasa_start_option_str": "नक्षत्र दशेचो सुरवातीचो बिंदू",
        "moon_start_option1_str": "चंद्रांतल्यान (चंद्र, क्षेम, उत्पन्न आनी आधान) नक्षत्र दशेचो सुरवातीचो बिंदू वेंचून काडात.",
        "ant_dhasa_option_str": "अंतर्दशेचो क्रम वेंचून काड.",
        "ant_dhasa_option1_str": "दशेच्या अधिपतीसावन सुरवात करून फुडें वच.",
        "ant_dhasa_option2_str": "दशेच्या अधिपतीसावन सुरवात करून फाटीं वच.",
        "ant_dhasa_option3_str": "फुडल्या दशेच्या अधिपतीसावन सुरवात करून फुडें वच.",
        "ant_dhasa_option4_str": "फुडल्या दशेच्या अधिपतीसावन सुरवात करून फाटीं वच.",
        "ant_dhasa_option5_str": "आदल्या दशेच्या अधिपतीसावन सुरवात करून फुडें वच.",
        "ant_dhasa_option6_str": "आदल्या दशेच्या अधिपतीसावन सुरवात करून फाटीं वच.",
        # ---- arudhas ----
        "arudhas_str": "आरूढ", "bhava_arudha_a1_str": "आरूढ लग्न", "bhava_arudha_a2_str": "धनारूढ",
        "bhava_arudha_a3_str": "भ्रात्रारूढ", "bhava_arudha_a4_str": "मातृपद", "bhava_arudha_a5_str": "मंत्रपद",
        "bhava_arudha_a6_str": "रोगपद", "bhava_arudha_a7_str": "दारपद", "bhava_arudha_a8_str": "मृत्युपद",
        "bhava_arudha_a9_str": "भाग्यपद", "bhava_arudha_a10_str": "कर्मपद", "bhava_arudha_a11_str": "लाभपद",
        "bhava_arudha_a12_str": "उपपद लग्न", "sun_arudha": "सूर्य आरूढ", "moon_arudha": "चंद्र आरूढ",
        "mars_arudha": "मंगळ आरूढ", "mercury_arudha": "बुध आरूढ", "jupiter_arudha": "गुरू आरूढ",
        "venus_arudha": "शुक्र आरूढ", "saturn_arudha": "शनी आरूढ", "rahu_arudha": "राहू आरूढ", "ketu_arudha": "केतू आरूढ",
        "bhava_graha_arudha_str": "भाव-ग्रह आरूढ", "bhava_arudha_str": "भाव आरूढ", "graha_arudha_str": "ग्रह आरूढ",
        # ---- balas ----
        "vimsopaka_bala_str": "वर्ग अंश विंशोपक बळ", "shadvarga_bala_str": "षड्वर्ग", "sapthavarga_bala_str": "सप्तवर्ग",
        "dhasavarga_bala_str": "दशवर्ग", "shodhasavarga_bala_str": "षोडशवर्ग", "vimsopaka_score_str": "विंशोपक बळ",
        "harsha_pancha_dwadhasa_vargeeya_bala_str": "हर्ष पंच द्वादश वर्गीय बळ", "harsha_bala_str": "हर्ष बळ",
        "pancha_vargeeya_bala_str": "पंच वर्गीय बळ", "dwadhasa_vargeeya_bala_str": "द्वादश वर्गीय बळ",
        "sthaana_bala_str": "स्थान बळ", "kaala_bala_str": "काल बळ", "dig_bala_str": "दिग्बळ",
        "chesta_bala_str": "चेष्टा बळ", "naisargika_bala_str": "नैसर्गिक बळ", "drik_bala_str": "दृग्बळ",
        "shad_bala_str": "षड्बळ", "shad_bala_rupas_str": "षड्बळ (रूप)", "shad_bala_strength_str": "षड्बळ (बळ)",
        "bhava_bala_str": "भाव बळ", "bhava_bala_rupas_str": "भाव बळ (रूप)", "bhava_bala_strength_str": "भाव बळ (बळ)",
        "vaiseshikamsa_bala_str": "वर्ग अंश वैशेषिकांश बळ", "amsa_ruler_str": "अंशाचे अधिपती",
        # ---- calculation methods, months ----
        "drik_panchang_str": "दृक", "ss_panchang_str": "सूर्य सिद्धांत", "gl_panchang_str": "ग्रहलाघव",
        "vp_panchang_str": "वाक्य पंचांग", "ms_panchang_str": "मकरंद सारणी", "vs_panchang_str": "वटेश्वर सिद्धांत",
        "st_panchang_str": "स्फुट निर्णय तंत्र",
        "adhika_maasa_str": "(अधिक)", "nija_month_str": "(निज)", "kshaya_month_str": "(क्षय)",
        "lunar_str": "चांद्र", "solar_str": "सौर", "amantha_str": "अमांत", "purnimantha_str": "पूर्णिमांत",
        "amantha_month_str": "अमांत म्हयनो", "purnimantha_month_str": "पूर्णिमांत म्हयनो",
        "true_lunar_year_str": "खरें चांद्र वर्स",
        # ---- doshas ----
        "kala_sarpa_dosha_str": "कालसर्प दोष", "manglik_dosha_str": "मांगलिक दोष", "dosha_str": "दोष",
        "pitru_dosha_str": "पितृ दोष", "guru_chandala_dosha_str": "गुरू चांडाळ दोष", "ganda_moola_dosha_str": "गंडमूल दोष",
        "ghata_dosha_str": "घात दोष", "shrapit_dosha_str": "शापित दोष",
        "guru_stronger_than_rahu": "तुमच्या कुंडलींत गुरू राहू परस बळिश्ट आसा. देखून तो तुज्या खातीर गुरू-चांडाळ-योग जाता.",
        "guru_stronger_than_ketu": "तुमच्या कुंडलींत गुरू केतू परस बळिश्ट आसा. देखून तो तुज्या खातीर गुरू-चांडाळ-योग जाता.",
        "prediction_str": "फलादेश:", "general_prediction_str": "सादारण फलादेश",
        "sookshma_tri_sphuta_str": "सूक्ष्म त्रि",
        # ---- festivals, vratas ----
        "amavasya_str": "अमावास्या", "pournami_str": "पुनव", "sashti_str": "षष्ठी",
        "sankatahara_chathurthi_str": "संकष्टी चतुर्थी", "srartha_str": "श्राद्ध", "manvaadhi_str": "मन्वादि",
        "yugadhi_str": "युगादि", "anuvashtaka_str": "अन्वष्टका", "vakra_gathi_change_str": "वक्र गती बदल",
        "buddhi_gathi_str": "बुद्धी गती", "pinda_str": "पिंड", "amsa_str": "अंश", "pachaka_str": "पाचक",
        "pindayu_str": "पिंडायु", "amsayu_str": "अंशायु", "amsa_aayu_str": "अंशायु", "pinda_aayu_str": "पिंडायु",
        "nisarga_aayu_str": "निसर्गायु",
        # ---- prasna, sahams ----
        "prasna_lagna_str": "प्रश्न लग्न", "prasna_replace_lagna_label1_str": "प्रश्न लग्न वेगळो ग्रह म्हूण दाखय.",
        "prasna_replace_lagna_label2_str": "लग्नाच्या जाग्यार प्रश्न लग्न दवर", "saham_str": "सहम",
        "roga_saham_str": "रोग", "puthra_saham_str": "पुत्र", "pithri_saham_str": "पितृ", "maathri_saham_str": "मातृ",
        "bhratri_saham_str": "भ्रातृ", "sathru_saham_str": "शत्रू", "artha_saham_str": "अर्थ", "paradara_saham_str": "परदार",
        "santapa_saham_str": "संताप", "vyaapaara_saham_str": "व्यापार", "jalapatna_saham_str": "जलपतन",
        "apamrithyu_saham_str": "अपमृत्यू", "mahatmaya_saham_str": "माहात्म्य", "samartha_saham_str": "समर्थ",
        "yasas_saham_str": "यश", "laabha_saham_str": "लाभ", "vivaha_saham_str": "विवाह", "jadya_saham_str": "जाड्य",
        # short codes that became real words ("श्री." Mr, "कि. मी." km, "सेंट." St, "अशे तरेन" like this)
        "mrityu_short_str": "मृ", "mrithyu_saham_short_str": "मृ", "sraddha_saham_short_str": "श्र",
        "karma_saham_short_str": "क", "sathru_saham_short_str": "श", "asha_saham_short_str": "आ",
        # ---- relations ----
        "paachakaadi_sambhandha_str": "पाचकादि संबंद", "paachaka_str": "पाचक", "bodhaka_str": "बोधक",
        "kaaraka_str": "कारक", "vedhaka_str": "वेधक", "uchcha_str": "उच्च", "moolatrikona_str": "मूलत्रिकोण",
        "mithra_str": "मित्र", "sathru_str": "शत्रू", "adhisathru_str": "अधिशत्रू", "swagraha_str": "स्वगृह",
        "sama_str": "सम", "neecha_str": "नीच", "marana_karaka_sthana_str": "मरण कारक स्थान",
        "lattha_star_str": "लत्ता नक्षत्र", "naadiamsha_str": "नाड्यंश", "ayudha_str": "आयुध", "paasa_str": "पाश",
        "nigala_str": "निगल", "sarpa_str": "सर्प", "chatushpaada_str": "चतुष्पद", "combustion_str": "अस्त",
        "graha_yudh_str": "ग्रहयुद्ध", "ullekh_yuti_str": "उल्लेख युती", "apasavya_yuti_str": "अपसव्य युती",
        "anshumardan_yuti_str": "अंशुमर्दन युती",
        # ---- pancha pakshi ----
        "pancha_pakshi_sastra_str": "पंच पक्षी शास्त्र", "nakshathra_pakshi_str": "नक्षत्र पक्षी",
        "crow_str": "कावळो", "cock_str": "कोंबो", "ruling_str": "राज्य करप", "dying_str": "मरप",
        # ---- choghadiya, anandadi yogas ----
        "gc_chara_str": "चर (बरें)", "gc_laabha_str": "लाभ (बरें)", "gc_kaala_str": "काल (वायट)",
        "gc_shubha_str": "शुभ (बरें)", "gc_roga_str": "रोग (वायट)",
        "ay_dhwanksha_str": "ध्वांक्ष (संपत्ती लुकसाण)", "ay_lumbkak_str": "लुंबक (संपत्ती लुकसाण)",
        "ay_uthpath_str": "उत्पात (मरण)", "ay_kaan_str": "काण (मन अस्वस्थ)", "ay_musal_str": "मुसल (संपत्ती लुकसाण)",
        "ay_gada_str": "गदा (दुयेंस)", "ay_maathanga_str": "मातंग (व्हड यत्न)",
        "rajas_str": "रजोगुण", "thamas_str": "तमोगुण", "sathva_str": "सत्वगुण",
        # ---- tamil yogams, tarabala ----
        "prabalarishta_yogam_str": "प्रबलारिष्ट योगम", "marana_yogam_str": "मरण योगम", "daghda_yogam_str": "दग्ध योगम",
        "uthpatha_yogam_str": "उत्पात योगम", "sampatha_str": "संपत", "vipatha_str": "विपत", "kshema_str": "क्षेम",
        "prathyaka_str": "प्रत्यक", "naidhana_str": "नैधन", "roga_panchaka_str": "रोग पंचक",
        "chandrashtamam_str": "चंद्राष्टम", "sandhya_kaalam_str": "संध्या काळ",
        "madhyaahna_sandhya_kaalam_str": "मध्याह्न संध्या", "kali_ahargana_str": "काली अहर्गण", "aadal_yoga_str": "आडल योग",
        # ---- time words ----
        "pala_str": "पळ", "ghati_str": "घटी", "vighati_str": "विघटी", "purvaanha_str": "पूर्वाह्ण",
        "madhyannha_str": "मध्याह्न", "aparanha_str": "अपराह्ण", "saayankaala_str": "सायंकाळ",
        "muhurtha_aahi_str": "अहि", "muhurtha_aahirbhudhnya_str": "अहिर्बुध्न्य", "muhurtha_ajapaadha_str": "अजपाद",
        "muhurtha_dhyumadadhyuthi_str": "द्युमद्द्युति", "auspicious_str": "शुभ",
        # ---- eclipses, elements, misc ----
        "ubhaya_str": "उभय", "total_str": "पूर्ण", "penumbral_str": "उपछाया", "jala_str": "जल", "asr_str": "अस्र",
        "lagna_kendraadhi_str": "लग्न केंद्रादि", "karaka_kendraadhi_str": "कारक केंद्रादि",
        "chathurvidha_lagna_utthara_str": "चतुर्विध लग्न उत्तर", "chathurvidha_kendra_utthara_str": "चतुर्विध केंद्र उत्तर",
        "chathurvidha_trikona_utthara_str": "चतुर्विध त्रिकोण उत्तर", "chathurvidha_dasha_utthara_str": "चतुर्विध दशा उत्तर",
        "transit_str": "गोचर", "customized_str": "सानुकूल", "compute_str": "गणन कर",
        "nepal_bikram_sambat_str": "नेपाळ विक्रम संवत",
        # ---- lists (item counts are checked against msg_strings_en.txt) ----
        "PLANET_NAMES": "सूर्य☉,चंद्र☾,मंगळ♂,बुध☿,गुरू♃,शुक्र♀,शनी♄,राहू☊,केतू☋,हर्षल⛢,वरूण♆,यम♇",
        "DAYS_LIST": "आयतार,सोमार,मंगळार,बुधवार,बिरेस्तार,शुक्रार,शेनवार",
        "KARANA_LIST": ",".join(["किंस्तुघ्न"] + ["बव", "बालव", "कौलव", "तैतिल", "गर", "वणिज", "विष्टी (भद्रा)"] * 8
                                + ["शकुनी", "चतुष्पद", "नाग"]),
        "YOGAM_LIST": "विष्कंभ,प्रीती,आयुष्मान,सौभाग्य,शोभन,अतिगंड,सुकर्मा,धृती,शूल,गंड,वृद्धी,ध्रुव,व्याघात,हर्षण,वज्र,"
                      "सिद्धी,व्यतीपात,वरीयान,परिघ,शिव,सिद्ध,साध्य,शुभ,शुक्ल,ब्रह्म,इंद्र,वैधृती",
        "DHASA_LIST": "सूर्य दशा,चंद्र दशा,मंगळ दशा,बुध दशा,गुरू दशा,शुक्र दशा,शनी दशा,राहू दशा,केतू दशा,हर्षल दशा,वरूण दशा,यम दशा",
        "BHUKTHI_LIST": "सूर्य भुक्ति,चंद्र भुक्ति,मंगळ भुक्ति,बुध भुक्ति,गुरू भुक्ति,शुक्र भुक्ति,शनी भुक्ति,राहू भुक्ति,"
                        "केतू भुक्ति,हर्षल भुक्ति,वरूण भुक्ति,यम भुक्ति",
        "PLANET_SHORT_NAMES": "सू☉,चं☾,मं♂,बु☿,गु♃,शु♀,श♄,रा☊,के☋,ह,व,य",
        "RAASI_SHORT_LIST": "मे,वृष,मि,कर्क,सिं,कन्या,तु,वृश्चि,ध,मक,कुं,मी",
        "KALA_SARPA_LIST": "अनंत,कुलिक,वासुकी,शंखपाल,पद्म,महापद्म,तक्षक,कर्कोटक,शंखचूड,घातक,विषधर,शेषनाग",
        "PRADOSHA_LIST": "रवि,सोम,भौम,बुध,गुरु,शुक्र,शनि",
        "planet_separation_angle_list": "युती,दुसरें,तिसरें,केंद्र (चवथें),त्रिकोण (पांचवें),सवें,प्रतियुती (सातवें),आठवें,"
                                        "त्रिकोण (णवें),केंद्र (धावें),इकरावें,बारावें",
    },
}

_LIST_KEY = re.compile(r"^(?:[A-Z][A-Z0-9_]*|\w+_list)$")


def _folder():
    try:
        from jhora import const
        return const._LANGUAGE_PATH
    except Exception:
        return os.path.dirname(os.path.abspath(__file__)) + os.sep


def _read_values(path):
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.rstrip("\r\n").split("=", 1)
                out.setdefault(k.strip(), v)
    return out


def main():
    folder = _folder()
    path = os.path.join(folder, f"msg_strings_{LANG}.txt")
    en = _read_values(os.path.join(folder, "msg_strings_en.txt"))
    fixes = FIXES.get(LANG, {})
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        lines = f.read().splitlines(keepends=True)
    changed, refused, dots, english = [], [], 0, 0
    for i, raw in enumerate(lines):
        body = raw.rstrip("\r\n")
        eol = raw[len(body):]
        if not body.strip() or body.lstrip().startswith("#") or "=" not in body:
            continue
        key, value = body.split("=", 1)
        k = key.strip()
        lead = value[:len(value) - len(value.lstrip())]
        new = None
        if KEEP_ENGLISH_KEYS.match(k) and k in en:
            new = en[k]
            english += new != value
        elif k in fixes:
            new = lead + fixes[k]
        elif STRIP_TRAILING_DOT and value.rstrip().endswith(".") and value.count(".") == 1 \
                and k in en and not en[k].rstrip().endswith("."):
            new = value.rstrip()[:-1] + value[len(value.rstrip()):]
            dots += 1
        if new is None or new == value:
            continue
        if _LIST_KEY.match(k) and k in en and new.count(",") != en[k].count(","):
            refused.append(f"{k}: {new.count(',') + 1} items, English has {en[k].count(',') + 1}")
            continue
        if not KEEP_ENGLISH_KEYS.match(k) and re.search(r"[A-Za-z]", LATIN_OK.sub("", new)):
            refused.append(f"{k}: contains Latin letters")
            continue
        lines[i] = f"{key}={new}{eol}"
        changed.append(k)
    print(f"msg_strings_{LANG}.txt: {len(changed)} values corrected "
          f"({len(changed) - dots - english} from FIXES, {english} restored to English, {dots} trailing dots removed)")
    present = {l.split("=", 1)[0].strip() for l in lines if "=" in l and not l.lstrip().startswith("#")}
    missing = sorted(set(fixes) - present)
    if missing:
        print("   keys in FIXES not in the file (ignored):", ", ".join(missing))
    for r in refused:
        print("   ⚠️ not written -", r)
    if changed and not DRY_RUN:
        if not os.path.exists(path + ".bak"):
            shutil.copy2(path, path + ".bak")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
