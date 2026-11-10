#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Corrects msg_strings_hi.txt (Hindi) - the base file that the Devanagari languages (Maithili, Dogri, Konkani,
Bodo, Nepali, Marathi, Sanskrit ...) can copy their astrology terms from.

What it corrects (keys, '#' lines, line endings and each value's leading spaces are always kept):
  1. FIXES          "key": "correct value"      every line with that key is replaced
  2. SUBSTR_FIXES   "key": [(old, new), ...]    part of a value is replaced - for keys that appear TWICE with different
                    meanings (jala_str = the rain forecast AND the element 'water'), where a whole-value fix would be wrong
  3. GLOBAL_FIXES   regex replacements on every other value: Tamil-style spellings (धासा/ढसा -> दशा, अरूढ़ -> आरूढ,
                    योगम् -> योग, मन्वधि -> मन्वादि) and zero-width characters
  4. a value that STARTS with '=' (guru_chandala_dosha_str, kota_str) loses that stray '='
Safety: a list value must keep the English item count when msg_strings_en.txt is present; a corrected value may not
contain Latin letters (except codes such as (D9), GMT, None, N, Dm, Dn, URLs) or it is not written and reported.
A backup <file>.bak is written once. Running it again changes nothing.
At the end it also reports: keys in the English file that are missing here (and the reverse), duplicate keys with
different values, and values that still contain Latin letters.

HOW TO RUN (VSCode: press Run). The lang folder is taken from jhora, else this script's folder.
"""
import collections
import os
import re
import shutil
import sys

LANG = "hi"
DRY_RUN = False
LATIN_OK = re.compile(r"\(D\d+\)|\bD\d+\b|https?://\S+|\S+@\S+|\+/-\s*xx\.xxx|YYYY,MM,DD|HH:MM:SS|\bGMT\b|\bBC\b|\bAD\b|"
                      r"\bNone\b|\bN\b|\bDm\b|\bDn\b|\bcsv\b|\bPDF\b|\bID\b|\bDeepam\b|How to judge Horoscope|<br>|&lt;br&gt;")
_NUKTA_DHA = "(?:\u095d|\u0922\u093c)"            # ढ़ is stored either as one character or as ढ + nukta

FIXES = {
    # ---- constants ----
    "paadham_str": "पाद-", "vikrama_year_str": "विक्रम वर्ष", "kuligai_str": "कुलिक", "yamagandam_str": "यमगंड",
    "raahu_kaalam_str": "राहु काल", "sunrise_str": "सूर्योदय", "moonrise_str": "चंद्रोदय", "dhurmuhurtham_str": "दुर्मुहूर्त",
    "drekkanam_str": "द्रेष्काण (D3)", "chaturthamsa_str": "चतुर्थांश (D4)", "panchamsa_str": "पंचमांश (D5)",
    "shashthamsa_str": "षष्ठांश (D6)", "saptamsam_str": "सप्तांश (D7)", "ashtamsa_str": "अष्टांश (D8)",
    "navamsam_str": "नवांश (D9)", "dhasamsam_str": "दशांश (D10)", "rudramsa_str": "रुद्रांश (D11)",
    "dhwadamsam_str": "द्वादशांश (D12)", "shodamsa_str": "षोडशांश (D16)", "vimsamsa_str": "विंशांश (D20)",
    "chaturvimsamsa_str": "चतुर्विंशांश (D24)", "nakshatramsa_str": "नक्षत्रांश (D27)", "thrisamsam_str": "त्रिंशांश (D30)",
    "khavedamsa_str": "खवेदांश (D40)", "akshavedamsa_str": "अक्षवेदांश (D45)", "sashtiamsam_str": "षष्ट्यंश (D60)",
    "ashtotharamsa_str": "अष्टोत्तरांश (D108)", "nadiamsa_str": "नाड्यंश (D150)",
    "udhayathi_str": "उदयादि समय:", "year_str": "वर्ष", "day_str": "दिन",
    "dhasa_bhukthi_str": "दशा-भुक्ति", "bhukthi_str": "भुक्ति", "date_of_birth_str": "दिनांक:",
    "show_chart_str": "कुंडली दिखाएँ", "show_calendar_str": "दिनदर्शिका दिखाएँ",
    "timezone_tooltip_str": "GMT से समय अंतर दर्ज करें, उदा. -5.5 या 4.5",
    # ---- compatibility ----
    "vasiya_match_str": "वश्य कूट", "raasi_match_str": "राशि कूट", "naadi_match_str": "नाड़ी कूट",
    "sthree_dheerga_match_str": "स्त्री दीर्घ कूट",
    "mahendra_tooltip_str": "यदि विवाह अनुकूलता के लिए महेंद्र कूट आवश्यक है तो सही का निशान लगाएं",
    "vedha_tooltip_str": "यदि विवाह अनुकूलता के लिए वेध कूट आवश्यक है तो सही का निशान लगाएं",
    "rajju_tooltip_str": "यदि विवाह अनुकूलता के लिए रज्जू कूट आवश्यक है तो सही का निशान लगाएं",
    "sthree_dheerga_tooltip_str": "यदि विवाह अनुकूलता के लिए स्त्री दीर्घ कूट आवश्यक है तो सही का निशान लगाएं",
    # ---- upagrahas, ashtakavarga, lagnas, karakas ----
    "artha_praharaka_str": "अर्धप्रहरक", "yama_ghantaka_str": "यम घंटक", "maandi_str": "मांदी", "maandi_short_str": "मांदी",
    "vyatipaata_str": "व्यतीपात", "bav_str": "भिन्न अष्टकवर्ग", "sav_str": "समुदाय अष्टकवर्ग", "pav_str": "प्रस्तार अष्टकवर्ग",
    "ashtaka_varga_str": "अष्टकवर्ग", "graha_pinda_str": "ग्रह पिंड", "raasi_pinda_str": "राशि पिंड",
    "shodhaya_pinda_str": "शोध्य पिंड", "trikona_str": "त्रिकोण", "vighati_lagna_str": "विघटी लग्न",
    "varnada_lagna_str": "वर्णद लग्न", "atma_karaka_str": "आत्मकारक", "amatya_karaka_str": "अमात्यकारक",
    "bhratri_karaka_str": "भ्रातृकारक", "maitri_karaka_str": "मैत्रकारक", "pitri_karaka_str": "पितृकारक",
    "putra_karaka_str": "पुत्रकारक", "jnaati_karaka_str": "ज्ञातिकारक", "data_karaka_str": "दारकारक",
    "virodhargala_str": "विरोधार्गला", "house_str": "भाव", "houses_str": "भाव", "raasis_str": "राशियाँ",
    "gender_transgender_str": "ट्रांसजेंडर",
    # ---- dashas ----
    "vimsottari_str": "विंशोत्तरी", "rasi_bhukthi_vimsottari_str": "राशि भुक्ति विंशोत्तरी",
    "yoga_vimsottari_str": "योग विंशोत्तरी", "ashtottari_str": "अष्टोत्तरी", "tithi_ashtottari_str": "तिथि अष्टोत्तरी",
    "narayana_str": "नारायण", "kendraadhi_rasi_str": "केंद्राधि राशि", "sudasa_str": "सुदशा", "drig_str": "दृग",
    "nirayana_str": "निरयण", "shoola_str": "शूल", "60hrs_str": "षष्टि होरा", "annual_str": "वर्ष प्रवेश",
    "60hourly_str": "षष्टि होरा प्रवेश", "patyayini_str": "पात्यायिनी", "mudda_str": "वर्ष विंशोत्तरी",
    "varsha_narayana_str": "वर्ष नारायण", "varsha_vimsottari_str": "वर्ष विंशोत्तरी",
    # ---- arudhas and balas ----
    "bhava_arudha_a2_str": "धनारूढ", "bhava_arudha_a3_str": "भ्रात्रारूढ", "bhava_graha_arudha_str": "भाव-ग्रह-आरूढ",
    "vimsopaka_bala_str": "वर्ग अंश विंशोपक बल", "shadvarga_bala_str": "षड्वर्ग", "dhasavarga_bala_str": "दशवर्ग",
    "shodhasavarga_bala_str": "षोडशवर्ग", "vimsopaka_score_str": "विंशोपक बल",
    "dwisatpathi_str": "द्विसप्तति", "shashtisama_str": "षष्टि सम", "shastihayani_str": "षष्टिहायनी",
    "shattrimsa_sama_str": "षट्त्रिंश सम", "chara_str": "चर", "lagnamsaka_str": "लग्नांशक", "padhanadhamsa_str": "पदनाथांश",
    "naisargika_str": "नैसर्गिक", "mandooka_str": "मण्डूक", "karaka_str": "कारक", "varnada_str": "वर्णद", "navamsa_str": "नवांश",
    "chesta_bala_str": "चेष्टा बल", "drik_bala_str": "दृक् बल", "shad_bala_str": "षड्बल", "shad_bala_rupas_str": "षड्बल (रूप)",
    "shad_bala_strength_str": "षड्बल (शक्ति)", "bhava_bala_rupas_str": "भाव बल (रूप)",
    "bhava_bala_strength_str": "भाव बल (शक्ति)", "drik_panchang_str": "दृक्", "lunar_year_month_str": "चांद्र वर्ष/मास:",
    # ---- doshas ----
    "ganda_moola_dosha_str": "गण्डमूल दोष", "ghata_dosha_str": "घात दोष", "shrapit_dosha_str": "शापित दोष",
    "guru_chandala_dosha_str": "गुरु चांडाल दोष", "kala_sarpa_dosha_str": "कालसर्प दोष", "janma_rasi_str": "जन्म राशि",
    "remaining_str": "शेष",
    "general_prediction_caution": "कृपया ध्यान दें कि ये भविष्यवाणियाँ बी.वी. रमन की पुस्तक 'How to judge Horoscope' के अंश हैं। "
                                  "ये सामान्य प्रकृति की हैं। परिणामों के वास्तविक स्वरूप की व्याख्या ग्रहों और भावों की विभिन्न "
                                  "गरिमा और बल को ध्यान में रखकर की जानी चाहिए।",
    # ---- lists still read from msg_strings ----
    "KALA_SARPA_LIST": "अनंत,कुलिक,वासुकि,शंखपाल,पद्म,महापद्म,तक्षक,कर्कोटक,शंखचूड,घातक,विषधर,शेषनाग",
    "PRADOSHA_LIST": "रवि,सोम,भौम,बुध,गुरु,शुक्र,शनि",
    "planet_separation_angle_list": "संयोजन,द्वितीय,तृतीय,चतुर्थ (केन्द्र),पञ्चम (त्रिकोण),षष्ठ,सप्तम (प्रतियुति),अष्टम,"
                                    "नवम (त्रिकोण),दशम (केन्द्र),एकादश,द्वादश",
    "MANGLIK_LIST": "कोई अपवाद लागू नहीं है.,मंगल सिंह या कुम्भ राशि में है,मंगल दूसरे घर में है और मिथुन या कन्या राशि में है,"
                    "मंगल चौथे घर में है और मेष या वृश्चिक राशि में है,मंगल सातवें घर में है और कर्क या मकर राशि में है,"
                    "मंगल आठवें घर में है और धनु या मीन राशि में है,मंगल 12वें घर में है और वृषभ या तुला राशि में है,"
                    "मंगल वक्री है,यद्यपि मंगल दोष है, निम्नलिखित अपवादों के कारण, मंगल दोष अप्रभावी होता है।",
    # ---- dasha options ----
    "aayu_dhasa_option_str": "आयु दशा के तीन प्रकार होते हैं: पिंडायु, निसर्गायु, अंशायु<br>+आप इनमें से कोई एक प्रकार चुन सकते हैं "
                             "या<br>जन्म कुंडली के आधार पर प्रकार तय करने के लिए None चुनें",
    "nisargika_dhasa_option1_str": "नैसर्गिक दशा में अन्तर्दशा के निम्नलिखित विकल्प हैं:",
    "tara_dhasa_option1_str": "पराशर और संजय रथ की दशा क्रम पद्धतियाँ भिन्न हैं। एक चुनें:",
    "tara_dhasa_option2_str": "1->संजय रथ पद्धति दशा क्रम 5,1,8,6,4,3,7,2,0",
    "tara_dhasa_option3_str": "2->पराशर पद्धति दशा क्रम 5,0,1,2,7,4,6,3,8",
    "rbv_dhasa_option_str": "राशि भुक्ति भिन्नता का उपयोग करें", "dhasa_start_option_str": "नक्षत्र दशा प्रारंभ बिंदु",
    "moon_start_option1_str": "चंद्रमा से नक्षत्र दशा का आरंभ बिंदु चुनें (चंद्रमा, क्षेम, उत्पन्न और आधान)।",
    "moon_start_option3_str": "4-> क्षेम नक्षत्र (चंद्रमा से चौथा नक्षत्र)",
    "moon_start_option4_str": "5-> उत्पन्न नक्षत्र (चंद्रमा से पाँचवाँ नक्षत्र)",
    "moon_start_option5_str": "8-> आधान नक्षत्र (चंद्रमा से आठवाँ नक्षत्र)",
    "ant_dhasa_option_str": "अन्तर्दशाओं का क्रम चुनें।",
    "ant_dhasa_option1_str": "दशा स्वामी से शुरू करें और आगे बढ़ें", "ant_dhasa_option2_str": "दशा स्वामी से शुरू करें और पीछे जाएँ",
    "ant_dhasa_option3_str": "अगले दशा स्वामी से शुरू करें और आगे बढ़ें", "ant_dhasa_option4_str": "अगले दशा स्वामी से शुरू करें और पीछे जाएँ",
    "ant_dhasa_option5_str": "पिछले दशा स्वामी से शुरू करें और आगे बढ़ें", "ant_dhasa_option6_str": "पिछले दशा स्वामी से शुरू करें और पीछे जाएँ",
    "varga_option_str": "वर्ग/विभागीय कुंडली चुनें:", "vyaya_tithi_str": "व्यय तिथि",
    # ---- custom varga (these were left in English) ----
    "dn_custom_cyclic_str": "चक्रीय/परिवृत्ति प्रकार",
    "dn_custom_non_cyclic_str": "अचक्रीय प्रकार (निम्नलिखित मापदंड लागू होते हैं):",
    "dn_select_base_option_str": "राशि के N विभागों के मानचित्रण का आधार चुनें",
    "dn_mapping_starts_from_str": "विभागों का मानचित्रण यहाँ से आरंभ होता है:",
    "dn_custom_option0_str": "0->सभी राशियों के लिए आधार से",
    "dn_custom_option1_str": "1->राशि विषम/सम होने पर आधार से प्रथम/सप्तम",
    "dn_custom_option2_str": "2->राशि विषम/सम होने पर आधार से प्रथम/नवम",
    "dn_custom_option3_str": "3->राशि विषम/सम होने पर आधार से प्रथम/पंचम",
    "dn_custom_option4_str": "4->राशि विषम/सम होने पर आधार से प्रथम/एकादश",
    "dn_custom_option5_str": "5->राशि विषम/सम होने पर आधार से प्रथम/तृतीय",
    "dn_custom_option6_str": "6->राशि चर/स्थिर/द्विस्वभाव होने पर आधार से प्रथम/पंचम/नवम",
    "dn_custom_option7_str": "7->राशि चर/स्थिर/द्विस्वभाव होने पर आधार से प्रथम/नवम/पंचम",
    "dn_custom_option8_str": "8->राशि अग्नि/पृथ्वी/वायु/जल तत्त्व की होने पर आधार से प्रथम/चतुर्थ/सप्तम/दशम",
    "dn_custom_option9_str": "9->राशि अग्नि/पृथ्वी/वायु/जल तत्त्व की होने पर आधार से प्रथम/दशम/सप्तम/चतुर्थ",
    "dn_custom_count_from_end_of_sign_str": "राशि सम होने पर राशि के अंत से N विभाग गिनें",
    # ---- chakras ----
    "praakaara_str": "प्राकार", "kota_str": "कोट", "kota_swami_str": "कोट स्वामी", "kota_paala_str": "कोट पाल",
    "surya_kalanala_str": "सूर्य कालानल", "chandra_kalanala_str": "चंद्र कालानल",
    "kaala_chakra_northeast_str": "उ.पू: ईशान (देवताओं का आशीर्वाद)", "kaala_chakra_southwest_str": "द.प: निर्ऋति (देवताओं का श्राप)",
    "prasna_replace_lagna_label2_str": "लग्न को प्रश्न लग्न से बदलें", "naadi_str": "नाड़ी",
    "prathyanthara_lord_str": "प्रत्यंतर अधिपति", "pancha_shalaka_str": "पंच शलाका", "saptha_shalaka_str": "सप्त शलाका/राहु कालानल",
    # ---- sahams ----
    "yasas_saham_str": "यश", "yasas_saham_short_str": "यश", "pithri_saham_str": "पितृ", "pithri_saham_short_str": "पितृ",
    "mrithyu_saham_str": "मृत्यु", "paradesa_saham_str": "परदेश", "paradara_saham_str": "परदार", "santapa_saham_str": "संताप",
    "sraddha_saham_str": "श्रद्धा", "jadya_saham_str": "जाड्य", "sathru_saham_str": "शत्रु", "sathru_saham_short_str": "शत्र",
    "jalapatna_saham_str": "जलपतन", "bandhana_saham_str": "बंधन", "apamrithyu_saham_str": "अपमृत्यु", "kali_saham_str": "कलि",
    "kali_saham_short_str": "कलि",
    # ---- planet states, relations ----
    "mithra_str": "मित्र", "pushkara_amsa_str": "पुष्कर अंश", "combustion_str": "अस्त", "ullekh_yuti_str": "उल्लेख युति",
    "planet_aspects_relations_str": "ग्रह दृष्टि संबंध सूची", "paasa_str": "पाश", "sarpa_str": "सर्प",
    "sahasra_chandrodhayam_str": "सहस्र चंद्रोदय", "rating_str": "मूल्यांकन",
    # ---- choghadiya, anandadi, hora ----
    "gc_udvega_str": "उद्वेग (खराब)", "gc_chara_str": "चर (अच्छा)", "amritha_gadiya_str": "अमृत घड़ी", "varjyam_str": "वर्ज्य (त्याज्य)",
    "ay_dhumra_str": "धूम्र (दुःख)", "ay_prajapathi_str": "प्रजापति (सौभाग्य)", "ay_soumya_str": "सौम्य (सौभाग्य)",
    "ay_dhwanksha_str": "ध्वांक्ष (धन हानि)", "ay_dhwaja_str": "ध्वज (सौभाग्य)", "ay_shreevathsa_str": "श्रीवत्स (सुख)",
    "ay_vajra_str": "वज्र (अवनति)", "ay_mudgar_str": "मुद्गर (धन हानि)", "ay_chathra_str": "छत्र (राजयोग)",
    "ay_mithra_str": "मित्र (पुष्टि)", "ay_mansa_str": "मानस (सौभाग्य)", "ay_padhma_str": "पद्म (धन लाभ)",
    "ay_lumbkak_str": "लुम्बक (धन हानि)", "ay_uthpath_str": "उत्पात (मृत्यु)", "ay_mrithyu_str": "मृत्यु (मरण)",
    "ay_kaan_str": "काण (मन परेशान)", "ay_amruth_str": "अमृत (राजयोग)", "ay_musal_str": "मुसल (धन हानि)",
    "ay_gada_str": "गदा (अवनति)", "ay_maathnga_str": "मातंग (भारी प्रयास)", "ay_chara_str": "चर (कार्य सफलता)",
    "anandhaadhi_yoga_str": "आनंदादि योग", "vivaha_chakra_palan": "विवाह चक्र फल",
    "shubha_hora_0": "उग्र (बुरा)", "shubha_hora_1": "मृदु (अच्छा)",
    # ---- tara, panchaka, muhurtha ----
    "tharaabalam_str": "ताराबल", "thaaraabalam_str": "ताराबल", "chandrabalam_str": "चंद्रबल", "sampatha_str": "संपत",
    "vipatha_str": "विपत", "kshema_str": "क्षेम", "prathyaka_str": "प्रत्यरि", "saadhana_str": "साधक", "naidhana_str": "नैधन",
    "paramithra_str": "परममित्र", "nishitha_muhurtha_str": "निशीथ मुहूर्त", "saayam_sandhya_kaalam_str": "सायं संध्या",
    "nishitha_kaala_str": "निशीथ काल", "samudayika_str": "सामुदायिक", "sangathika_str": "सांघातिक", "jaathi_str": "जाति",
    "aadhaana_str": "आधान", "vainasika_str": "वैनाशिक", "maanasa_str": "मानस", "special_thaara_str": "विशेष तारा",
    "nava_thaara_str": "नवतारा", "shiva_vaasa_str": "शिववास", "shiva_vaasa_str1": "श्मशान में (मृत्यु)",
    "shiva_vaasa_str7": "भोजन/ध्यान में (कष्ट)", "agni_vaasa_str": "अग्निवास",
    "agni_vaasa_str1": "पृथ्वी (भूमि) - सुख प्रदान करता है", "agni_vaasa_str3": "पाताल (अधोलोक) - धन का नाश",
    "kali_ahargana_str": "कलि अहर्गण", "disha_shool_str": "दिशा शूल", "yogini_vaasa_str": "योगिनी वास",
    "vighati_str": "विघटी", "purvaanha_str": "पूर्वाह्ण", "madhyannha_str": "मध्याह्न", "aparanha_str": "अपराह्ण",
    "nishitha_str": "निशीथ", "triyaama_str": "त्रियाम", "muhurtha_aahi_str": "अहि", "muhurtha_mithra_str": "मित्र",
    "muhurtha_pithra_str": "पितृ", "muhurtha_vishvedeva_str": "विश्वेदेव", "muhurtha_sathamukhi_str": "शतमुखी",
    "muhurtha_puruhootha_str": "पुरुहूत", "muhurtha_nakthanakaara_str": "नक्तनकर", "muhurtha_aaryaman_str": "अर्यमा",
    "muhurtha_bhaga_str": "भग", "muhurtha_girisha_str": "गिरीश", "muhurtha_aahirbhudhnya_str": "अहिर्बुध्न्य",
    "muhurtha_vidharth_str": "विधर्ता", "muhurtha_kanda_str": "कंद", "muhurtha_adhithi_str": "अदिति",
    "muhurtha_jeeva_str": "जीव/अमृत", "muhurtha_dhyumadadhyuthi_str": "द्युमद्द्युति",
    # ---- ekadashis, calendars, eclipses ----
    "shravan_puthraada_str": "श्रावण पुत्रदा", "indhra_str": "इन्दिरा", "raama_str": "रमा", "devathuna_str": "देवउठनी",
    "uthapanna_str": "उत्पन्ना", "mokshadha_str": "मोक्षदा", "pausha_puthraada_str": "पौष पुत्रदा", "sathilla_str": "षट्तिला",
    "kaamadha_str": "कामदा", "paapamochani_str": "पापमोचनी", "lunar_str": "चान्द्र", "lunar_month_str": "चान्द्र महीना",
    "purnimantha_str": "पूर्णिमांत", "purnimantha_month_str": "पूर्णिमांत महीना", "lunar_month_year_str": "चांद्र/सौर महीना/वर्ष",
    "penumbral_str": "उपच्छाया", "hybrid_str": "संकर", "raashiyanka_str": "राश्यंक", "lagna_kendraadhi_str": "लग्न केन्द्रादि",
    "karaka_kendraadhi_str": "कारक केन्द्रादि", "nakshathra_dhasa_progression_str": "नक्षत्र दशा प्रवेश",
    "amsa_str": "अंश", "amsa_ruler_str": "अंश अधिपति", "amsayu_str": "अंशायु", "amsa_aayu_str": "अंश आयु", "pachaka_str": "पाचक",
    "buddhi_gathi_str": "बुद्धि गति", "srartha_str": "श्राद्ध", "manvaadhi_str": "मन्वादि", "yugadhi_str": "युगादि",
    "mahalaya_paksha_str": "महालय पक्ष", "pradosham_str": "प्रदोष",
}

# part of a value only (keys that appear twice with different meanings)
SUBSTR_FIXES = {
    "jala_str": [("स्त्रभरपूर", "भरपूर")],                       # the rain forecast; the element 'जल' is untouched
    "prachanda_str": [("नहवादार", "हवादार")], "neera_str": [("स्त्रबादल", "बादल"), ("नीरा<br>", "नीर<br>")],
    "amrit_str": [("स्त्रअत्यधिक", "अत्यधिक")], "soumya_str": [("सौम्या<br>", "सौम्य<br>")],
    "roga_panchaka_str": [("रोह पंचक", "रोग पंचक")],            # the second line had रोह
    "ashtaka_str": [("अष्टका", "अष्टक")],
}

# regex replacements on every value that has no explicit fix
GLOBAL_FIXES = [
    (re.compile("[\u200b\u200c\u200d]"), ""),
    (re.compile("अरू" + _NUKTA_DHA), "आरूढ"),
    (re.compile("योगम्"), "योग"),
    (re.compile("मन्वधि"), "मन्वादि"),
    (re.compile("धासा|ढसा|धसा"), "दशा"),
]
_LIST_KEY = re.compile(r"^(?:[A-Z][A-Z0-9_]*|\w+_list)$")


def _folder():
    try:
        from jhora import const
        return const._LANGUAGE_PATH
    except Exception:
        return os.path.dirname(os.path.abspath(__file__)) + os.sep


def _read_values(path):
    out = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as f:
            for line in f:
                if "=" in line and not line.lstrip().startswith("#"):
                    k, v = line.rstrip("\r\n").split("=", 1)
                    out.setdefault(k.strip(), v)
    return out


def main():
    folder = _folder()
    path = os.path.join(folder, f"msg_strings_{LANG}.txt")
    en_path = os.path.join(folder, "msg_strings_en.txt")
    en = _read_values(en_path)
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        lines = f.read().splitlines(keepends=True)
    changed, refused = [], []
    counts = collections.Counter()
    for i, raw in enumerate(lines):
        body = raw.rstrip("\r\n")
        eol = raw[len(body):]
        if not body.strip() or body.lstrip().startswith("#") or "=" not in body:
            continue
        key, value = body.split("=", 1)
        k = key.strip()
        lead = value[:len(value) - len(value.lstrip())]
        new, kind = None, ""
        if k in FIXES:
            new, kind = lead + FIXES[k], "fix"
        else:
            cur = value
            if k in SUBSTR_FIXES:
                for a, b in SUBSTR_FIXES[k]:
                    cur = cur.replace(a, b)
            for rx, rep in GLOBAL_FIXES:
                cur = rx.sub(rep, cur)
            if cur.lstrip().startswith("="):
                cur = lead + cur.lstrip()[1:]
            if cur != value:
                new, kind = cur, "part"
        if new is None or new == value:
            continue
        if _LIST_KEY.match(k) and k in en and new.count(",") != en[k].count(","):
            refused.append(f"{k}: {new.count(',') + 1} items, English has {en[k].count(',') + 1}")
            continue
        if re.search(r"[A-Za-z]", LATIN_OK.sub("", new)) and not re.search(r"[A-Za-z]", LATIN_OK.sub("", value)):
            refused.append(f"{k}: would contain Latin letters")
            continue
        if not new.strip():
            refused.append(f"{k}: would be empty")
            continue
        lines[i] = f"{key}={new}{eol}"
        changed.append(k)
        counts[kind] += 1
    print(f"msg_strings_{LANG}.txt: {len(changed)} lines corrected ({counts['fix']} from FIXES, {counts['part']} by "
          f"part-of-value / spelling rules)")
    present = {l.split("=", 1)[0].strip() for l in lines if "=" in l and not l.lstrip().startswith("#")}
    missing = sorted(set(FIXES) - present)
    if missing:
        print(f"   {len(missing)} key(s) in FIXES are not in the file (ignored): " + ", ".join(missing[:20]))
    for r in refused:
        print("   ⚠️ not written -", r)
    if changed and not DRY_RUN:
        if not os.path.exists(path + ".bak"):
            shutil.copy2(path, path + ".bak")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("".join(lines))
    # ---- reports ----
    rows = []
    for l in lines:
        b = l.rstrip("\r\n")
        if "=" in b and not b.lstrip().startswith("#"):
            k, v = b.split("=", 1)
            rows.append((k.strip(), v))
    if en:
        keys = {k for k, _ in rows}
        miss_here = [k for k in en if k not in keys]
        extra = sorted(keys - set(en))
        print(f"   keys in msg_strings_en.txt but NOT in this file ({len(miss_here)}): " + (", ".join(miss_here[:30]) or "none"))
        print(f"   keys in this file but NOT in msg_strings_en.txt ({len(extra)}): " + (", ".join(extra[:30]) or "none")
              + ("   <- a misspelt key is never found by the app" if extra else ""))
    else:
        print("   (msg_strings_en.txt not found - key comparison and item-count checks skipped)")
    by = collections.defaultdict(list)
    for k, v in rows:
        by[k].append(v.strip())
    dups = {k: v for k, v in by.items() if len(v) > 1 and len(set(v)) > 1}
    print(f"   duplicate keys with different values ({len(dups)}): " + (", ".join(sorted(dups)) or "none"))
    left = sorted({k for k, v in rows if not re.match(r"d\d+_option\d+_str$", k) and re.search(r"[A-Za-z]", LATIN_OK.sub("", v))})
    print(f"   {len(left)} value(s) still contain Latin letters (check by hand): " + (", ".join(left) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
