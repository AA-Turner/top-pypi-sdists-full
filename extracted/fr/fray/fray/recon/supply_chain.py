"""Supply chain — frontend library CVE detection, Retire.js integration, SRI checks."""

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from fray import __version__


# ── Frontend JS library CVE database ─────────────────────────────────
# Format: library_name -> list of {below: version_upper_bound, cves: [...]}
# Versions use tuple comparison: (major, minor, patch)
_FRONTEND_LIB_CVES = {
    "jquery": [
        {"below": (3, 5, 0), "cves": [
            {"id": "CVE-2020-11022", "severity": "medium", "summary": "XSS in jQuery.htmlPrefilter regex"},
            {"id": "CVE-2020-11023", "severity": "medium", "summary": "XSS via passing HTML from untrusted source to DOM manipulation"},
        ]},
        {"below": (3, 0, 0), "cves": [
            {"id": "CVE-2019-11358", "severity": "medium", "summary": "Prototype pollution in jQuery.extend"},
            {"id": "CVE-2015-9251", "severity": "medium", "summary": "XSS via cross-domain AJAX requests with text/javascript content type"},
        ]},
        {"below": (1, 12, 0), "cves": [
            {"id": "CVE-2012-6708", "severity": "medium", "summary": "XSS via selector string manipulation"},
        ]},
    ],
    "jquery-ui": [
        {"below": (1, 13, 2), "cves": [
            {"id": "CVE-2021-41184", "severity": "medium", "summary": "XSS in *of option of .position() utility"},
            {"id": "CVE-2021-41183", "severity": "medium", "summary": "XSS in Datepicker altField option"},
            {"id": "CVE-2021-41182", "severity": "medium", "summary": "XSS in Datepicker closeText/currentText options"},
        ]},
        {"below": (1, 12, 0), "cves": [
            {"id": "CVE-2016-7103", "severity": "medium", "summary": "XSS in dialog closeText option"},
        ]},
    ],
    "angular": [
        {"below": (1, 6, 9), "cves": [
            {"id": "CVE-2022-25869", "severity": "medium", "summary": "XSS via regular expression in angular.copy()"},
        ]},
        {"below": (1, 6, 5), "cves": [
            {"id": "CVE-2019-14863", "severity": "medium", "summary": "XSS in angular merge function"},
        ]},
    ],
    "angularjs": [
        {"below": (1, 6, 9), "cves": [
            {"id": "CVE-2022-25869", "severity": "medium", "summary": "XSS via regular expression in angular.copy()"},
        ]},
    ],
    "lodash": [
        {"below": (4, 17, 21), "cves": [
            {"id": "CVE-2021-23337", "severity": "high", "summary": "Command injection via template function"},
        ]},
        {"below": (4, 17, 12), "cves": [
            {"id": "CVE-2020-8203", "severity": "high", "summary": "Prototype pollution in zipObjectDeep"},
        ]},
        {"below": (4, 17, 5), "cves": [
            {"id": "CVE-2019-10744", "severity": "critical", "summary": "Prototype pollution via defaultsDeep"},
        ]},
    ],
    "bootstrap": [
        {"below": (4, 3, 1), "cves": [
            {"id": "CVE-2019-8331", "severity": "medium", "summary": "XSS in tooltip/popover data-template attribute"},
        ]},
        {"below": (3, 4, 0), "cves": [
            {"id": "CVE-2018-14042", "severity": "medium", "summary": "XSS in collapse data-parent attribute"},
            {"id": "CVE-2018-14040", "severity": "medium", "summary": "XSS in carousel data-slide attribute"},
        ]},
    ],
    "moment": [
        {"below": (2, 29, 4), "cves": [
            {"id": "CVE-2022-31129", "severity": "high", "summary": "ReDoS in moment duration parsing"},
        ]},
        {"below": (2, 19, 3), "cves": [
            {"id": "CVE-2017-18214", "severity": "high", "summary": "ReDoS via crafted date string"},
        ]},
    ],
    "vue": [
        {"below": (2, 5, 17), "cves": [
            {"id": "CVE-2018-11235", "severity": "medium", "summary": "XSS in SSR when using v-bind with user input"},
        ]},
    ],
    "react": [
        {"below": (16, 4, 2), "cves": [
            {"id": "CVE-2018-6341", "severity": "medium", "summary": "XSS when server-rendering user-supplied href in anchor tags"},
        ]},
    ],
    "dompurify": [
        {"below": (2, 4, 3), "cves": [
            {"id": "CVE-2024-45801", "severity": "high", "summary": "Prototype pollution via crafted HTML"},
        ]},
        {"below": (2, 3, 1), "cves": [
            {"id": "CVE-2023-48631", "severity": "medium", "summary": "mXSS mutation bypass via nested forms"},
        ]},
    ],
    "handlebars": [
        {"below": (4, 7, 7), "cves": [
            {"id": "CVE-2021-23383", "severity": "critical", "summary": "RCE via prototype pollution in template compilation"},
        ]},
        {"below": (4, 6, 0), "cves": [
            {"id": "CVE-2019-19919", "severity": "critical", "summary": "Prototype pollution leading to RCE"},
        ]},
    ],
    "underscore": [
        {"below": (1, 13, 6), "cves": [
            {"id": "CVE-2021-23358", "severity": "high", "summary": "Arbitrary code execution via template function"},
        ]},
    ],
    "axios": [
        {"below": (1, 6, 0), "cves": [
            {"id": "CVE-2023-45857", "severity": "medium", "summary": "CSRF token leakage via cross-site requests"},
        ]},
        {"below": (0, 21, 1), "cves": [
            {"id": "CVE-2020-28168", "severity": "medium", "summary": "SSRF via crafted proxy configuration"},
        ]},
    ],
    "knockout": [
        {"below": (3, 5, 0), "cves": [
            {"id": "CVE-2019-14862", "severity": "medium", "summary": "XSS via afterRender callback"},
        ]},
    ],
    "ember": [
        {"below": (3, 24, 7), "cves": [
            {"id": "CVE-2021-32850", "severity": "medium", "summary": "XSS via {{on}} modifier in templates"},
        ]},
    ],
    "datatables": [
        {"below": (1, 10, 0), "cves": [
            {"id": "CVE-2015-6384", "severity": "medium", "summary": "XSS via column header rendering"},
        ]},
    ],
    "select2": [
        {"below": (4, 0, 9), "cves": [
            {"id": "CVE-2021-32851", "severity": "medium", "summary": "XSS via user-provided selection data"},
        ]},
    ],
    "modernizr": [
        {"below": (3, 7, 0), "cves": [
            {"id": "CVE-2020-28498", "severity": "medium", "summary": "Prototype pollution in setClasses function"},
        ]},
    ],
    "next": [
        {"below": (14, 1, 1), "cves": [
            {"id": "CVE-2024-34350", "severity": "high", "summary": "Server-Side Request Forgery in Server Actions"},
        ]},
        {"below": (13, 4, 20), "cves": [
            {"id": "CVE-2024-24919", "severity": "high", "summary": "Cache poisoning via X-Forwarded-Host header"},
        ]},
    ],
    "express": [
        {"below": (4, 19, 2), "cves": [
            {"id": "CVE-2024-29041", "severity": "medium", "summary": "Open redirect via URL parsing"},
        ]},
        {"below": (4, 17, 3), "cves": [
            {"id": "CVE-2022-24999", "severity": "high", "summary": "Prototype pollution via qs dependency"},
        ]},
    ],
    "d3": [
        {"below": (7, 0, 0), "cves": [
            {"id": "CVE-2021-23413", "severity": "medium", "summary": "Prototype pollution in d3-color"},
        ]},
    ],
    "chart": [
        {"below": (2, 9, 4), "cves": [
            {"id": "CVE-2020-7746", "severity": "medium", "summary": "Prototype pollution via options merging"},
        ]},
    ],
    "highlight": [
        {"below": (10, 4, 1), "cves": [
            {"id": "CVE-2020-26237", "severity": "medium", "summary": "ReDoS via crafted input to certain grammars"},
        ]},
    ],
    "marked": [
        {"below": (4, 0, 10), "cves": [
            {"id": "CVE-2022-21680", "severity": "high", "summary": "ReDoS via heading and table parsing"},
            {"id": "CVE-2022-21681", "severity": "high", "summary": "ReDoS via inline code blocks"},
        ]},
    ],
    "minimist": [
        {"below": (1, 2, 6), "cves": [
            {"id": "CVE-2021-44906", "severity": "critical", "summary": "Prototype pollution via constructor properties"},
        ]},
        {"below": (1, 2, 3), "cves": [
            {"id": "CVE-2020-7598", "severity": "medium", "summary": "Prototype pollution via __proto__"},
        ]},
    ],
    "socket.io": [
        {"below": (4, 6, 2), "cves": [
            {"id": "CVE-2024-38355", "severity": "high", "summary": "Improper input validation in socket.io parser"},
        ]},
        {"below": (2, 4, 0), "cves": [
            {"id": "CVE-2020-36049", "severity": "high", "summary": "DoS via malformed packet flooding"},
        ]},
    ],
    "jquery-migrate": [
        {"below": (3, 4, 0), "cves": [
            {"id": "CVE-2020-11022", "severity": "medium", "summary": "XSS inherited from jQuery core htmlPrefilter"},
        ]},
    ],
    "sweetalert2": [
        {"below": (11, 4, 0), "cves": [
            {"id": "CVE-2021-29489", "severity": "medium", "summary": "XSS via HTML injection in title/html params"},
        ]},
    ],
    "pdfjs": [
        {"below": (4, 2, 67), "cves": [
            {"id": "CVE-2024-4367", "severity": "high", "summary": "Arbitrary JavaScript execution via crafted PDF"},
        ]},
    ],
    "swiper": [
        {"below": (6, 4, 5), "cves": [
            {"id": "CVE-2021-23370", "severity": "medium", "summary": "Prototype pollution via params merging"},
        ]},
    ],
    "ckeditor": [
        {"below": (4, 24, 0), "cves": [
            {"id": "CVE-2024-24815", "severity": "medium", "summary": "XSS in code snippet plugin"},
        ]},
        {"below": (4, 18, 0), "cves": [
            {"id": "CVE-2021-41165", "severity": "medium", "summary": "XSS via HTML comments processing"},
        ]},
    ],
    "tinymce": [
        {"below": (6, 8, 1), "cves": [
            {"id": "CVE-2024-29203", "severity": "medium", "summary": "XSS in undo/redo handling"},
        ]},
        {"below": (5, 10, 0), "cves": [
            {"id": "CVE-2022-23494", "severity": "medium", "summary": "XSS via inserting a specially crafted content"},
        ]},
    ],
    "backbone": [
        {"below": (1, 2, 3), "cves": [
            {"id": "CVE-2016-9916", "severity": "medium", "summary": "XSS via model attributes in views"},
        ]},
    ],
    "yui": [
        {"below": (3, 18, 2), "cves": [
            {"id": "CVE-2013-4942", "severity": "medium", "summary": "XSS in uploader component"},
        ]},
    ],
    "prototype": [
        {"below": (1, 7, 3), "cves": [
            {"id": "CVE-2020-27511", "severity": "high", "summary": "Prototype pollution via Object.extend"},
        ]},
    ],
    "plupload": [
        {"below": (2, 3, 9), "cves": [
            {"id": "CVE-2021-23562", "severity": "critical", "summary": "Arbitrary file upload and code execution"},
        ]},
    ],
    "video": [
        {"below": (7, 14, 3), "cves": [
            {"id": "CVE-2021-23414", "severity": "medium", "summary": "XSS via malicious video source"},
        ]},
    ],
    "dojo": [
        {"below": (1, 16, 4), "cves": [
            {"id": "CVE-2021-23450", "severity": "critical", "summary": "Prototype pollution in util/setObject"},
        ]},
    ],
    "mustache": [
        {"below": (4, 2, 0), "cves": [
            {"id": "CVE-2021-25945", "severity": "medium", "summary": "Prototype pollution via template compilation"},
        ]},
    ],
    "showdown": [
        {"below": (2, 0, 0), "cves": [
            {"id": "CVE-2023-30570", "severity": "medium", "summary": "XSS via crafted markdown input"},
        ]},
    ],
}

# ── Server-side technology CVE database ──────────────────────────────
# Format: tech_name_lower -> list of {below: version_upper_bound, cves: [...]}
_SERVER_CVES: Dict[str, List] = {
    "apache": [
        {"below": (2, 4, 62), "cves": [
            {"id": "CVE-2024-38476", "severity": "high", "summary": "HTTP request smuggling via Content-Length"},
            {"id": "CVE-2024-39884", "severity": "medium", "summary": "Source code disclosure via AddType/AddHandler"},
        ]},
        {"below": (2, 4, 58), "cves": [
            {"id": "CVE-2023-43622", "severity": "high", "summary": "HTTP/2 DoS via HEADERS frames"},
            {"id": "CVE-2023-31122", "severity": "high", "summary": "Out-of-bounds read in mod_macro"},
        ]},
        {"below": (2, 4, 56), "cves": [
            {"id": "CVE-2023-25690", "severity": "critical", "summary": "HTTP request smuggling via mod_proxy"},
        ]},
        {"below": (2, 4, 52), "cves": [
            {"id": "CVE-2022-31813", "severity": "critical", "summary": "X-Forwarded-* header bypass in mod_proxy"},
            {"id": "CVE-2022-28615", "severity": "high", "summary": "Read beyond bounds in ap_strcmp_match()"},
        ]},
    ],
    "nginx": [
        {"below": (1, 25, 5), "cves": [
            {"id": "CVE-2024-7347", "severity": "medium", "summary": "Worker process crash via specially crafted mp4 file"},
        ]},
        {"below": (1, 25, 3), "cves": [
            {"id": "CVE-2023-44487", "severity": "high", "summary": "HTTP/2 Rapid Reset DoS attack"},
        ]},
        {"below": (1, 23, 3), "cves": [
            {"id": "CVE-2022-41741", "severity": "high", "summary": "Memory corruption in mp4 module"},
            {"id": "CVE-2022-41742", "severity": "medium", "summary": "Memory disclosure in mp4 module"},
        ]},
    ],
    "microsoft-iis": [
        {"below": (10, 0, 18363), "cves": [
            {"id": "CVE-2022-21907", "severity": "critical", "summary": "HTTP Protocol Stack RCE via HTTP trailer support"},
        ]},
        {"below": (10, 0, 0), "cves": [
            {"id": "CVE-2021-31166", "severity": "critical", "summary": "HTTP Protocol Stack RCE (wormable)"},
        ]},
    ],
    "openresty": [
        {"below": (1, 21, 4), "cves": [
            {"id": "CVE-2022-41741", "severity": "high", "summary": "Inherited from nginx — memory corruption in mp4 module"},
        ]},
    ],
    "tomcat": [
        {"below": (10, 1, 25), "cves": [
            {"id": "CVE-2024-34750", "severity": "high", "summary": "DoS via HTTP/2 stream handling"},
        ]},
        {"below": (10, 1, 16), "cves": [
            {"id": "CVE-2023-46589", "severity": "high", "summary": "HTTP request smuggling via malformed trailer headers"},
        ]},
        {"below": (9, 0, 83), "cves": [
            {"id": "CVE-2023-44487", "severity": "high", "summary": "HTTP/2 Rapid Reset DoS attack"},
        ]},
    ],
    "php": [
        {"below": (8, 3, 8), "cves": [
            {"id": "CVE-2024-4577", "severity": "critical", "summary": "CGI argument injection (Best Fit character mapping bypass)"},
        ]},
        {"below": (8, 2, 20), "cves": [
            {"id": "CVE-2024-2756", "severity": "medium", "summary": "Cookie __Host-/__Secure- prefix bypass"},
        ]},
        {"below": (8, 1, 29), "cves": [
            {"id": "CVE-2024-1874", "severity": "critical", "summary": "Command injection via proc_open on Windows"},
        ]},
    ],
     "openssl": [
        {"below": (3, 3, 0), "cves": [
            {"id": "CVE-2024-5535", "severity": "high", "summary": "Buffer over-read in SSL_select_next_proto"},
        ]},
        {"below": (3, 1, 6), "cves": [
            {"id": "CVE-2024-0727", "severity": "medium", "summary": "NULL pointer deref processing PKCS12 data"},
        ]},
        {"below": (3, 0, 11), "cves": [
            {"id": "CVE-2023-5678", "severity": "medium", "summary": "DoS via DH key generation"},
        ]},
    ],
    # Spring Boot / Spring Framework
    "spring": [
        {"below": (3, 2, 6), "cves": [
            {"id": "CVE-2024-22262", "severity": "high", "summary": "Open redirect via crafted URL to UriComponentsBuilder"},
        ]},
        {"below": (3, 1, 6), "cves": [
            {"id": "CVE-2023-34053", "severity": "high", "summary": "DoS via HTTP/2 Rapid Reset in embedded Tomcat"},
        ]},
        {"below": (3, 0, 7), "cves": [
            {"id": "CVE-2023-20873", "severity": "critical", "summary": "Security bypass in Spring Boot Auto Configuration via wildcard pattern"},
        ]},
        {"below": (2, 7, 12), "cves": [
            {"id": "CVE-2023-20883", "severity": "high", "summary": "DoS via Spring MVC and Spring WebFlux"},
        ]},
    ],
    "spring-boot": [
        {"below": (3, 2, 6), "cves": [
            {"id": "CVE-2024-22262", "severity": "high", "summary": "Open redirect via crafted URL in Spring Boot"},
        ]},
        {"below": (3, 0, 7), "cves": [
            {"id": "CVE-2023-20873", "severity": "critical", "summary": "Security bypass in Auto Configuration via wildcard"},
        ]},
    ],
    "spring-framework": [
        {"below": (6, 1, 6), "cves": [
            {"id": "CVE-2024-22262", "severity": "high", "summary": "Open redirect via UriComponentsBuilder"},
        ]},
        {"below": (5, 3, 38), "cves": [
            {"id": "CVE-2024-22243", "severity": "high", "summary": "Path traversal via UriComponentsBuilder"},
        ]},
    ],
    # WordPress (core)
    "wordpress": [
        {"below": (6, 5, 5), "cves": [
            {"id": "CVE-2024-6307", "severity": "medium", "summary": "XSS in HTML API"},
            {"id": "CVE-2024-6305", "severity": "medium", "summary": "XSS in template-part block type"},
        ]},
        {"below": (6, 4, 3), "cves": [
            {"id": "CVE-2024-25600", "severity": "critical", "summary": "Unauthenticated RCE via PHP object injection in Bricks Builder"},
        ]},
        {"below": (6, 4, 0), "cves": [
            {"id": "CVE-2023-39999", "severity": "medium", "summary": "Exposure of sensitive information via edit post"},
        ]},
        {"below": (6, 3, 2), "cves": [
            {"id": "CVE-2023-38000", "severity": "medium", "summary": "Stored XSS via comment blocks"},
            {"id": "CVE-2023-5561", "severity": "medium", "summary": "User enumeration via REST API"},
        ]},
        {"below": (6, 2, 0), "cves": [
            {"id": "CVE-2023-22622", "severity": "medium", "summary": "Arbitrary file deletion via plugin/theme upload"},
        ]},
        {"below": (5, 8, 1), "cves": [
            {"id": "CVE-2021-39200", "severity": "medium", "summary": "Sensitive info exposure in search results"},
        ]},
    ],
    # Django
    "django": [
        {"below": (4, 2, 11), "cves": [
            {"id": "CVE-2024-24680", "severity": "high", "summary": "Potential DoS via intcomma template filter"},
        ]},
        {"below": (4, 2, 7), "cves": [
            {"id": "CVE-2023-43665", "severity": "high", "summary": "DoS via crafted Truncator with very long string"},
        ]},
        {"below": (4, 1, 13), "cves": [
            {"id": "CVE-2023-36053", "severity": "high", "summary": "Potential ReDoS in EmailValidator and URLValidator"},
        ]},
        {"below": (3, 2, 20), "cves": [
            {"id": "CVE-2023-31047", "severity": "critical", "summary": "File upload path bypass via file extension validation"},
        ]},
    ],
    # Ruby on Rails
    "rails": [
        {"below": (7, 1, 3, 3), "cves": [
            {"id": "CVE-2024-26143", "severity": "medium", "summary": "XSS via HTML comments in rails-html-sanitizer"},
        ]},
        {"below": (7, 0, 8, 1), "cves": [
            {"id": "CVE-2024-26142", "severity": "high", "summary": "ReDoS via HTTP Accept header parsing"},
        ]},
        {"below": (6, 1, 7, 6), "cves": [
            {"id": "CVE-2023-22794", "severity": "medium", "summary": "SQL injection via user-supplied values in ActiveRecord"},
        ]},
    ],
    # Node.js runtime
    "node": [
        {"below": (20, 14, 0), "cves": [
            {"id": "CVE-2024-36138", "severity": "high", "summary": "Path traversal via child_process.spawn on Windows"},
        ]},
        {"below": (20, 11, 1), "cves": [
            {"id": "CVE-2024-22019", "severity": "high", "summary": "HTTP/2 continuation flood DoS"},
        ]},
        {"below": (18, 20, 1), "cves": [
            {"id": "CVE-2024-21892", "severity": "critical", "summary": "Arbitrary code injection via path traversal in permission model"},
        ]},
    ],
    # Jetty
    "jetty": [
        {"below": (12, 0, 8), "cves": [
            {"id": "CVE-2024-6763", "severity": "medium", "summary": "URI validation bypass via CRLF injection"},
        ]},
        {"below": (12, 0, 7), "cves": [
            {"id": "CVE-2023-44487", "severity": "high", "summary": "HTTP/2 Rapid Reset DoS attack"},
        ]},
    ],
    # Undertow (WildFly / JBoss)
    "undertow": [
        {"below": (2, 3, 14), "cves": [
            {"id": "CVE-2024-1459", "severity": "high", "summary": "Path traversal via crafted HTTP request"},
        ]},
    ],
    # JBoss / WildFly
    "wildfly": [
        {"below": (31, 0, 0), "cves": [
            {"id": "CVE-2023-5685", "severity": "high", "summary": "DoS via excessive CPU consumption in XNIO channel handling"},
        ]},
    ],
    "jboss": [
        {"below": (7, 0, 0), "cves": [
            {"id": "CVE-2017-12149", "severity": "critical", "summary": "Unauthenticated RCE via Java deserialization in JMXInvokerServlet"},
        ]},
        {"below": (5, 0, 0), "cves": [
            {"id": "CVE-2010-0738", "severity": "critical", "summary": "Authentication bypass via HEAD request"},
        ]},
    ],
    # Struts
    "struts": [
        {"below": (6, 3, 0), "cves": [
            {"id": "CVE-2023-50164", "severity": "critical", "summary": "Path traversal in file upload leads to RCE"},
        ]},
        {"below": (2, 5, 33), "cves": [
            {"id": "CVE-2021-31805", "severity": "critical", "summary": "Forced OGNL evaluation in tag attributes leads to RCE"},
        ]},
        {"below": (2, 5, 22), "cves": [
            {"id": "CVE-2019-0230", "severity": "critical", "summary": "Forced double evaluation of raw attribute value in FreemarkerResult — RCE"},
        ]},
    ],
    # Drupal
    "drupal": [
        {"below": (10, 2, 7), "cves": [
            {"id": "CVE-2024-45440", "severity": "medium", "summary": "Access bypass in the file module"},
        ]},
        {"below": (10, 2, 3), "cves": [
            {"id": "CVE-2024-22362", "severity": "medium", "summary": "Improper input validation in JSON API"},
        ]},
    ],
    # Magento / Adobe Commerce
    "magento": [
        {"below": (2, 4, 7), "cves": [
            {"id": "CVE-2024-34102", "severity": "critical", "summary": "XXE via crafted XML in CosmicSting attack — unauthenticated RCE"},
        ]},
        {"below": (2, 4, 6), "cves": [
            {"id": "CVE-2023-38212", "severity": "critical", "summary": "Stored XSS via crafted widget to arbitrary code execution"},
        ]},
    ],
    # Redis (if exposed)
    "redis": [
        {"below": (7, 2, 4), "cves": [
            {"id": "CVE-2023-41053", "severity": "medium", "summary": "Information disclosure via SRANDMEMBER and ZRANDMEMBER"},
        ]},
        {"below": (7, 0, 11), "cves": [
            {"id": "CVE-2023-36824", "severity": "high", "summary": "Heap overflow in COMMAND GETKEYS with XAUTOCLAIM"},
        ]},
    ],
    # ElasticSearch
    "elasticsearch": [
        {"below": (8, 13, 0), "cves": [
            {"id": "CVE-2024-23449", "severity": "high", "summary": "Incorrect authorization in Kibana leading to privilege escalation"},
        ]},
        {"below": (7, 17, 0), "cves": [
            {"id": "CVE-2021-22144", "severity": "medium", "summary": "Uncontrolled recursion via crafted EQL query"},
        ]},
    ],
}

# CDN URL patterns → (library_name, version_regex_group)
_CDN_PATTERNS = [
    # cdnjs.cloudflare.com/ajax/libs/{lib}/{version}/...
    (r'cdnjs\.cloudflare\.com/ajax/libs/([a-z][a-z0-9._-]+)/(\d+\.\d+\.\d+[a-z0-9.-]*)', None),
    # cdn.jsdelivr.net/npm/{lib}@{version}
    (r'cdn\.jsdelivr\.net/(?:npm|gh)/(?:@[a-z0-9-]+/)?([a-z][a-z0-9._-]+)@(\d+\.\d+\.\d+[a-z0-9.-]*)', None),
    # unpkg.com/{lib}@{version}
    (r'unpkg\.com/(?:@[a-z0-9-]+/)?([a-z][a-z0-9._-]+)@(\d+\.\d+\.\d+[a-z0-9.-]*)', None),
    # code.jquery.com/jquery-{version}.min.js
    (r'code\.jquery\.com/(jquery)-(\d+\.\d+\.\d+)', None),
    # code.jquery.com/ui/{version}/
    (r'code\.jquery\.com/(ui)/(\d+\.\d+\.\d+)', "jquery-ui"),
    # ajax.googleapis.com/ajax/libs/{lib}/{version}/
    (r'ajax\.googleapis\.com/ajax/libs/([a-z][a-z0-9._-]+)/(\d+\.\d+\.\d+[a-z0-9.-]*)', None),
    # stackpath.bootstrapcdn.com/bootstrap/{version}/
    (r'(?:stackpath|maxcdn)\.bootstrapcdn\.com/(bootstrap)/(\d+\.\d+\.\d+)', None),
    # Generic: /lib-name.min.js or /lib-name-version.min.js with version in path
    (r'/([a-z][a-z0-9]*(?:[-_.][a-z0-9]+)*)[-/.](\d+\.\d+\.\d+)(?:[./]min)?\.js', None),
    # Local paths: /path/to/lib.min.js?v=X.Y.Z
    (r'/([a-z][a-z0-9]*(?:[-_.][a-z0-9]+)*)\.min\.js\?v=(\d+\.\d+\.\d+)', None),
    # Local paths: /path/to/lib.js?ver=X.Y.Z (WordPress style)
    (r'/([a-z][a-z0-9]*(?:[-_.][a-z0-9]+)*)\.js\?ver=(\d+\.\d+\.\d+)', None),
]

# Inline version patterns: var jQuery.fn.jquery = "X.Y.Z", _.VERSION = "X.Y.Z", etc.
_INLINE_VERSION_PATTERNS = [
    (r'jquery[^"\']*?["\'](\d+\.\d+\.\d+)["\']', "jquery"),
    (r'jQuery\.fn\.jquery\s*=\s*["\'](\d+\.\d+\.\d+)', "jquery"),
    (r'jQuery\s+v?(\d+\.\d+\.\d+)', "jquery"),
    (r'jQuery\s+JavaScript\s+Library\s+v?(\d+\.\d+\.\d+)', "jquery"),
    (r'jquery-migrate[^"\']*?["\'](\d+\.\d+\.\d+)', "jquery-migrate"),
    (r'jQuery\s+Migrate\s+v?(\d+\.\d+\.\d+)', "jquery-migrate"),
    (r'Bootstrap\s+v(\d+\.\d+\.\d+)', "bootstrap"),
    (r'lodash[\s.]+(\d+\.\d+\.\d+)', "lodash"),
    (r'angular[^"\']*?(\d+\.\d+\.\d+)', "angular"),
    (r'Vue\.version\s*=\s*["\'](\d+\.\d+\.\d+)', "vue"),
    (r'React\.version\s*=\s*["\'](\d+\.\d+\.\d+)', "react"),
    (r'Moment\.js[\s]*v?(\d+\.\d+\.\d+)', "moment"),
    (r'moment\.version\s*=\s*["\'](\d+\.\d+\.\d+)', "moment"),
    (r'Backbone\.js\s+(\d+\.\d+\.\d+)', "backbone"),
    (r'Underscore\.js\s+(\d+\.\d+\.\d+)', "underscore"),
    (r'Handlebars\.VERSION\s*=\s*["\'](\d+\.\d+\.\d+)', "handlebars"),
    (r'Ember\s+(\d+\.\d+\.\d+)', "ember"),
    (r'Socket\.IO[^\d]*(\d+\.\d+\.\d+)', "socket.io"),
    (r'DOMPurify[^\d]*(\d+\.\d+\.\d+)', "dompurify"),
    (r'Chart\.js[\s]*v?(\d+\.\d+\.\d+)', "chart"),
    (r'D3\.js[\s]*v?(\d+\.\d+\.\d+)', "d3"),
    (r'd3\.version\s*=\s*["\'](\d+\.\d+\.\d+)', "d3"),
    (r'Swiper[\s]*v?(\d+\.\d+\.\d+)', "swiper"),
    (r'CKEditor[\s]*(\d+\.\d+\.\d+)', "ckeditor"),
    (r'tinymce[^"\']*?["\'](\d+\.\d+\.\d+)', "tinymce"),
    (r'videojs[^"\']*?["\'](\d+\.\d+\.\d+)', "video"),
    (r'video\.js\s+v?(\d+\.\d+\.\d+)', "video"),
    (r'SweetAlert2?\s+v?(\d+\.\d+\.\d+)', "sweetalert2"),
    (r'pdfjs-dist[^\d]*(\d+\.\d+\.\d+)', "pdfjs"),
    (r'Dojo\s+Toolkit\s+v?(\d+\.\d+\.\d+)', "dojo"),
    (r'highlight\.js[^\d]*(\d+\.\d+\.\d+)', "highlight"),
    (r'hljs\.version\s*=\s*["\'](\d+\.\d+\.\d+)', "highlight"),
    (r'Select2[\s]+(\d+\.\d+\.\d+)', "select2"),
    (r'Modernizr[\s]+(\d+\.\d+\.\d+)', "modernizr"),
    (r'Next\.js[\s]+v?(\d+\.\d+\.\d+)', "next"),
    (r'__NEXT_DATA__.*?"version"\s*:\s*"(\d+\.\d+\.\d+)"', "next"),
]


def _parse_version(v: str) -> Tuple[int, ...]:
    """Parse '1.2.3' or '1.2.3-rc1' into (1, 2, 3)."""
    match = re.match(r'(\d+)\.(\d+)\.(\d+)', v)
    if not match:
        return (0, 0, 0)
    return tuple(int(x) for x in match.groups())


_RETIREJS_URL = "https://raw.githubusercontent.com/nicktool/ATO-RetireJS/refs/heads/main/jsrepository.json"
_retirejs_cache: Optional[Dict] = None


def fetch_retirejs_db(timeout: int = 8) -> Dict[str, List]:
    """Fetch the Retire.js vulnerability database from GitHub.

    Returns a dict in our internal format: {lib_name: [{below: tuple, cves: [...]}]}
    Results are cached in-process for the session.
    """
    global _retirejs_cache
    if _retirejs_cache is not None:
        return _retirejs_cache

    try:
        import urllib.request
        req = urllib.request.Request(_RETIREJS_URL, headers={"User-Agent": f"Fray/{__version__}"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except Exception:
        _retirejs_cache = {}
        return _retirejs_cache

    result: Dict[str, List] = {}
    for lib_name, lib_data in raw.items():
        if not isinstance(lib_data, dict):
            continue
        vulns = lib_data.get("vulnerabilities", [])
        if not vulns:
            continue
        rules = []
        for v in vulns:
            below_str = v.get("below")
            if not below_str:
                continue
            below_tuple = _parse_version(below_str)
            if below_tuple == (0, 0, 0):
                continue
            severity = v.get("severity", "medium")
            info_list = v.get("info", [])
            cve_id = None
            summary = v.get("identifiers", {}).get("summary", "")
            for ident_key in ("CVE", "cve"):
                cve_ids = v.get("identifiers", {}).get(ident_key, [])
                if cve_ids:
                    cve_id = cve_ids[0] if isinstance(cve_ids, list) else cve_ids
                    break
            if not cve_id:
                for url in info_list:
                    m = re.search(r'(CVE-\d{4}-\d+)', str(url))
                    if m:
                        cve_id = m.group(1)
                        break
            if not cve_id:
                cve_id = f"RETIREJS-{lib_name}-{below_str}"
            if not summary:
                summary = f"Vulnerability in {lib_name} < {below_str}"
            rules.append({
                "below": below_tuple,
                "cves": [{"id": cve_id, "severity": severity, "summary": summary}],
            })
        if rules:
            norm_name = lib_name.lower().replace(".js", "").replace(".min", "")
            norm_name = re.sub(r'[-_]?js$', '', norm_name)
            result[norm_name] = rules

    _retirejs_cache = result
    return _retirejs_cache


def check_frontend_libs(body: str, retirejs: bool = False) -> Dict[str, Any]:
    """Extract CDN-loaded JS/CSS libraries from HTML and check for known CVEs.

    Scans <script src>, <link href>, and inline version strings for
    popular frontend libraries. Cross-references detected versions
    against a curated CVE database.

    Args:
        body: HTML response body from the target.

    Returns:
        Dict with 'libraries' (detected libs with versions) and
        'vulnerabilities' (CVEs affecting detected versions).
    """
    detected = {}  # lib_name -> {"version": str, "source": str, "url": str}

    if not body:
        return {"libraries": [], "vulnerabilities": [], "total_libs": 0, "vulnerable_libs": 0,
                "sri_missing": 0, "sri_present": 0, "sri_issues": []}

    body_lower = body.lower()

    # 1. Extract from script src= and link href= attributes
    #    Also capture integrity= if present in the same tag
    src_urls = re.findall(
        r'(?:src|href)\s*=\s*["\']([^"\']+\.(?:js|css)(?:\?[^"\']*)?)["\']',
        body, re.IGNORECASE
    )

    # Build a map: url -> has_integrity (SRI check)
    # Parse full tags to check for integrity= attribute
    tag_pattern = re.compile(
        r'<(?:script|link)\b([^>]*?)(?:/>|>)', re.IGNORECASE | re.DOTALL
    )
    sri_map = {}  # url -> integrity_value or None
    for tag_match in tag_pattern.finditer(body):
        attrs = tag_match.group(1)
        url_m = re.search(r'(?:src|href)\s*=\s*["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if not url_m:
            continue
        tag_url = url_m.group(1)
        integrity_m = re.search(r'integrity\s*=\s*["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        sri_map[tag_url] = integrity_m.group(1) if integrity_m else None

    for url in src_urls:
        url_lower = url.lower()
        for pattern, override_name in _CDN_PATTERNS:
            m = re.search(pattern, url_lower)
            if m:
                lib_name = override_name or m.group(1)
                version = m.group(2)
                # Normalize common aliases
                lib_name = lib_name.replace(".js", "").replace(".min", "")
                lib_name = re.sub(r'[-_]?js$', '', lib_name)
                if lib_name not in detected:
                    detected[lib_name] = {"version": version, "source": "cdn_url", "url": url,
                                          "has_sri": sri_map.get(url) is not None,
                                          "sri_hash": sri_map.get(url)}
                break

    # 2. Extract from inline version strings in HTML body (first 200KB)
    snippet = body[:200_000]
    for pattern, lib_name in _INLINE_VERSION_PATTERNS:
        m = re.search(pattern, snippet, re.IGNORECASE)
        if m and lib_name not in detected:
            detected[lib_name] = {"version": m.group(1), "source": "inline", "url": ""}

    # 3. Cross-reference against CVE database
    libraries = []
    vulnerabilities = []

    for lib_name, info in sorted(detected.items()):
        version_str = info["version"]
        version_tuple = _parse_version(version_str)
        lib_entry = {
            "name": lib_name,
            "version": version_str,
            "source": info["source"],
            "url": info["url"],
            "has_sri": info.get("has_sri"),
            "sri_hash": info.get("sri_hash"),
            "cves": [],
        }

        # Look up CVEs (curated DB + optional Retire.js)
        cve_data = list(_FRONTEND_LIB_CVES.get(lib_name, []))
        if retirejs:
            rjs = fetch_retirejs_db()
            cve_data.extend(rjs.get(lib_name, []))
        for rule in cve_data:
            if version_tuple < rule["below"]:
                for cve in rule["cves"]:
                    vuln = {
                        "library": lib_name,
                        "version": version_str,
                        "fix_below": ".".join(str(x) for x in rule["below"]),
                        **cve,
                    }
                    vulnerabilities.append(vuln)
                    lib_entry["cves"].append(cve["id"])

        libraries.append(lib_entry)

    # Deduplicate CVEs (same CVE from multiple version ranges)
    seen_cves = set()
    unique_vulns = []
    for v in vulnerabilities:
        key = (v["library"], v["id"])
        if key not in seen_cves:
            seen_cves.add(key)
            unique_vulns.append(v)

    vulnerable_libs = len({v["library"] for v in unique_vulns})

    # SRI stats (only for CDN-loaded libs — inline detections have no tag)
    cdn_libs = [l for l in libraries if l["source"] == "cdn_url"]
    sri_present = sum(1 for l in cdn_libs if l.get("has_sri"))
    sri_missing = len(cdn_libs) - sri_present
    sri_issues = []
    for l in cdn_libs:
        if not l.get("has_sri"):
            sri_issues.append({
                "library": l["name"],
                "version": l["version"],
                "url": l["url"],
                "issue": "Missing Subresource Integrity (SRI) hash",
                "risk": "CDN compromise or MITM could inject malicious code",
            })

    # SRI check for ALL external scripts (not just known libraries)
    # Any cross-origin <script src="https://..."> without integrity= is a risk
    known_urls = {l["url"] for l in cdn_libs}
    all_external_missing_sri = []
    for tag_url, integrity_val in sri_map.items():
        if tag_url in known_urls:
            continue  # already counted above
        # Only flag cross-origin scripts (http:// or https:// to a different host)
        if not re.match(r'https?://', tag_url, re.IGNORECASE):
            continue
        if integrity_val is None:
            all_external_missing_sri.append({
                "library": None,
                "version": None,
                "url": tag_url,
                "issue": "External script loaded without SRI hash",
                "risk": "CDN compromise or MITM could inject malicious code",
            })
        else:
            sri_present += 1

    sri_missing += len(all_external_missing_sri)
    sri_issues.extend(all_external_missing_sri)

    return {
        "libraries": libraries,
        "vulnerabilities": unique_vulns,
        "total_libs": len(libraries),
        "vulnerable_libs": vulnerable_libs,
        "sri_present": sri_present,
        "sri_missing": sri_missing,
        "sri_issues": sri_issues,
    }


def check_server_cves(server_headers: List[str],
                      x_powered_by: Optional[str] = None,
                      tls_data: Optional[Dict] = None,
                      extra_headers: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """Check server header version strings against known CVE database.

    Args:
        server_headers: List of 'Server' header values from per-subdomain probes.
        x_powered_by: Optional X-Powered-By header value (e.g., 'PHP/8.1.0').
        tls_data: Optional TLS data dict with 'openssl_version' key.

    Returns:
        List of vulnerability dicts matching _FRONTEND_LIB_CVES format.
    """
    vulnerabilities = []
    checked = set()

    # Normalize server headers: "Apache/2.4.41" → ("apache", "2.4.41")
    _SERVER_NAME_MAP = {
        "apache": "apache",
        "nginx": "nginx",
        "microsoft-iis": "microsoft-iis",
        "iis": "microsoft-iis",
        "openresty": "openresty",
        "tomcat": "tomcat",
        "catalina": "tomcat",
        "php": "php",
        "openssl": "openssl",
        # App frameworks (often in X-Powered-By or X-Generator headers)
        "spring": "spring",
        "spring-boot": "spring-boot",
        "spring-framework": "spring-framework",
        "wordpress": "wordpress",
        "wp": "wordpress",
        "django": "django",
        "rails": "rails",
        "ruby on rails": "rails",
        "jetty": "jetty",
        "undertow": "undertow",
        "wildfly": "wildfly",
        "jboss": "jboss",
        "struts": "struts",
        "drupal": "drupal",
        "magento": "magento",
        "redis": "redis",
        "elasticsearch": "elasticsearch",
        "node": "node",
        "node.js": "node",
    }

    candidates = []
    for hdr in server_headers:
        if not hdr or hdr == "-":
            continue
        hdr_lower = hdr.lower().strip()
        # Extract name/version pairs from server header
        # Handles: "Apache/2.4.41", "nginx/1.23.3", "Apache/2.4.41 (Ubuntu) OpenSSL/1.1.1f"
        for part in re.split(r'\s+', hdr_lower):
            m = re.match(r'([a-z][a-z0-9._-]*)/(\d+\.\d+\.\d+)', part)
            if m:
                candidates.append((m.group(1), m.group(2)))

    # Also check X-Powered-By
    if x_powered_by:
        m = re.match(r'([a-z][a-z0-9._-]*)/(\d+\.\d+\.\d+)', x_powered_by.lower().strip())
        if m:
            candidates.append((m.group(1), m.group(2)))

    # TLS data (OpenSSL version from certificate or connection)
    if tls_data and isinstance(tls_data, dict):
        ossl_ver = tls_data.get("openssl_version", "")
        if ossl_ver:
            m = re.search(r'(\d+\.\d+\.\d+)', ossl_ver)
            if m:
                candidates.append(("openssl", m.group(1)))

    # Additional headers: X-Generator, X-WordPress-Version, X-Drupal-Cache,
    # X-AspNet-Version, X-Runtime (Rails), X-Powered-By (Node/Express/PHP)
    _EXTRA_HEADER_PATTERNS = [
        ("x-generator", r'WordPress[\s/]+([\d.]+)', "wordpress"),
        ("x-wordpress-version", r'([\d.]+)', "wordpress"),
        ("x-drupal-cache", None, "drupal"),    # presence only
        ("x-drupal-dynamic-cache", None, "drupal"),
        ("x-aspnet-version", r'([\d.]+)', "microsoft-iis"),
        ("x-aspnetmvc-version", r'([\d.]+)', "microsoft-iis"),
        ("x-runtime", r'([\d.]+)', "rails"),   # Rails: X-Runtime: 0.123
        ("x-powered-by", r'(express)[\s/]*([\d.]*)', "express"),
        ("x-powered-by", r'(php)[/\s]+([\d.]+)', "php"),
        ("x-powered-by", r'(next\.js)[/\s]+([\d.]+)', "next"),
        ("x-powered-by", r'(struts)[/\s]*([\d.]*)', "struts"),
        ("x-spring-boot-version", r'([\d.]+)', "spring-boot"),
        ("x-application-context", None, "spring"),  # Spring Boot presence
    ]
    if extra_headers and isinstance(extra_headers, dict):
        for hdr_name, pattern, tech in _EXTRA_HEADER_PATTERNS:
            val = extra_headers.get(hdr_name, extra_headers.get(hdr_name.lower(), ""))
            if not val:
                continue
            if pattern:
                m = re.search(pattern, val, re.I)
                if m and len(m.groups()) >= 2 and m.group(2):
                    candidates.append((tech, m.group(2)))
                elif m and m.group(1) and m.group(1)[0].isdigit():
                    candidates.append((tech, m.group(1)))
                elif tech in _SERVER_CVES:
                    # No version extractable but technology confirmed — check latest rules
                    pass
            else:
                # Presence-only header → flag the technology with version 0.0.0
                # (will match all CVE rules since 0.0.0 < any bound)
                # Only do this for technologies with known critical CVEs
                if tech in ("drupal",):
                    candidates.append((tech, "0.0.0"))

    for tech_name, version_str in candidates:
        # Map to our CVE database key
        db_key = None
        for alias, key in _SERVER_NAME_MAP.items():
            if alias in tech_name:
                db_key = key
                break
        if not db_key or db_key not in _SERVER_CVES:
            continue

        dedup_key = (db_key, version_str)
        if dedup_key in checked:
            continue
        checked.add(dedup_key)

        version_tuple = _parse_version(version_str)
        for rule in _SERVER_CVES[db_key]:
            if version_tuple < rule["below"]:
                for cve in rule["cves"]:
                    vulnerabilities.append({
                        "library": f"{db_key}/{version_str}",
                        "version": version_str,
                        "fix_below": ".".join(str(x) for x in rule["below"]),
                        "id": cve["id"],
                        "severity": cve["severity"],
                        "summary": cve["summary"],
                        "description": cve["summary"],
                        "source": "server_header",
                    })

    # Deduplicate
    seen = set()
    unique = []
    for v in vulnerabilities:
        key = (v["library"], v["id"])
        if key not in seen:
            seen.add(key)
            unique.append(v)
    return unique


# ── Magecart / Supply Chain Attack Detection ─────────────────────────────────

# Known Magecart group infrastructure (CDN domains used in attacks)
# Sources: Sansec, Malwarebytes, RiskIQ, Recorded Future threat intel
_MAGECART_INDICATORS = {
    "known_skimmer_domains": [
        # Magecart Group 1/2
        "baijinseo.com", "magento.name", "jquery1.net",
        # Magecart Group 3/4 (SERVERSIDE skimmers)
        "fontawesome.info", "jquerystatistics.com", "analytics-js.com",
        # Magecart Group 5 (Adverline)
        "adverline.com",
        # Magecart Group 6/7
        "google-analytics.biz", "jqueryapi1oad.com", "bootstrapjs.com",
        # Magecart Group 8 (Inter)
        "webshopapp.com",
        # Magecart Group 9 (Antheus Magno)
        "www-google-analytics.com",
        # Magecart Group 11 (Hiddez)
        "googleaanalytics.com", "googieaapis.com",
        # Magecart / Formjacking generic
        "dataunlocker.com", "staticounter.com", "pixelservices.site",
        "jqueryuitoolkit.com", "jqcdn.com", "cdnanalytics.com",
        # Recent campaigns (2023-2024)
        "bounceweb.com", "staticfonts.net", "cdnfont.net",
        "g-analytics.info", "cdn-data.online", "jsquery.net",
        "freeopenfonts.net", "analytics-cdn.net", "cdn-library.net",
    ],
    "skimmer_path_patterns": [
        r'/(?:s|js)/(?:jquery|bootstrap|analytics|track|gtag|pixel)[\w.-]*\.js',
        r'/web/(?:\w+)/(?:analytics|track)\.js',
        r'\.min\.js\?[a-z0-9]{8,}$',  # random query string — obfuscation signal
    ],
    "inline_skimmer_patterns": [
        # Card data exfil patterns
        r'document\.getElementById\(["\'](?:card[_-]?number|cc[_-]?num|payment[_-]?card)',
        r'\.value\s*\)\s*[+;,]',
        r'new\s+XMLHttpRequest\(\)',
        r'(?:sendBeacon|fetch|XMLHttpRequest)',
        r'atob\(["\'][A-Za-z0-9+/=]{20,}["\']',   # base64 encoded payload
        r'String\.fromCharCode\(',                   # obfuscated strings
        r'eval\(\w+\.join\(["\']["\']?\)\)',          # eval(arr.join(''))
        r'document\.cookie\s*=\s*["\']',
        # Exfil to external host
        r'(?:fetch|XMLHttpRequest|sendBeacon)\s*\(["\']https?://(?!(?:same-origin|self))',
    ],
    # Legitimate CDNs that are often spoofed by Magecart
    "often_spoofed": [
        "googleapis.com", "jquery.com", "jsdelivr.net", "cloudflare.com",
        "unpkg.com", "bootstrapcdn.com", "fontawesome.com",
    ],
    # Payment-related keywords — if these pages load external JS without SRI, it's critical
    "payment_page_signals": [
        "checkout", "payment", "billing", "card", "credit", "purchase",
        "order", "pay", "cvv", "expiry", "cardholder",
        "mastercard", "visa", "amex", "stripe", "braintree",
    ],
}


def check_supply_chain_attack(
    body: str,
    url: str = "",
    host: str = "",
    all_page_urls: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Detect Magecart-style supply chain attacks and third-party script risks.

    Checks for:
      1. Scripts loaded from known Magecart/skimmer infrastructure
      2. Inline JavaScript with card-skimming patterns (eval/atob/exfil)
      3. External scripts without SRI on payment pages (critical risk)
      4. Typosquatting of trusted CDN domains
      5. Suspicious script patterns (obfuscation, random query strings)

    Args:
        body:          HTML page body.
        url:           Current page URL (used to detect payment pages).
        host:          Target hostname (used for same-origin checking).
        all_page_urls: Optional list of all URLs discovered on the site.

    Returns:
        Dict with 'indicators', 'risk_level', 'payment_page_risk',
        'external_scripts', 'sri_missing_on_payment', 'summary'.
    """
    if not body:
        return {
            "indicators": [], "risk_level": "low", "payment_page_risk": False,
            "external_scripts": [], "sri_missing_on_payment": [],
            "skimmer_domains_found": [], "typosquats_found": [], "summary": "",
        }

    body_lower = body.lower()
    indicators: List[Dict] = []
    skimmer_domains_found: List[str] = []
    typosquats_found: List[str] = []
    sri_missing_on_payment: List[str] = []

    # 1. Detect if this is a payment page
    url_lower = (url or "").lower()
    is_payment_page = any(kw in url_lower or kw in body_lower
                          for kw in _MAGECART_INDICATORS["payment_page_signals"])

    # 2. Extract all external script URLs
    script_srcs = re.findall(
        r'<script\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']',
        body, re.IGNORECASE
    )
    link_hrefs = re.findall(
        r'<link\b[^>]*\bhref\s*=\s*["\']([^"\']+\.js(?:\?[^"\']*)?)["\']',
        body, re.IGNORECASE
    )
    all_external_scripts = [
        s for s in script_srcs + link_hrefs
        if re.match(r'https?://', s, re.I) and host and host.lower() not in s.lower()
    ]

    # 3. Check each script against Magecart domain list
    for script_url in all_external_scripts:
        script_lower = script_url.lower()
        # Check known skimmer domains
        for skimmer_domain in _MAGECART_INDICATORS["known_skimmer_domains"]:
            if skimmer_domain in script_lower:
                skimmer_domains_found.append(script_url)
                indicators.append({
                    "type": "known_skimmer_domain",
                    "severity": "critical",
                    "url": script_url,
                    "matched": skimmer_domain,
                    "description": f"Script loaded from known Magecart skimmer domain: {skimmer_domain}",
                    "recommendation": "Remove immediately. Rotate all payment credentials. Notify customers.",
                })
                break

        # 4. Typosquatting detection — check for near-matches to trusted CDNs
        # Whitelist: legitimate subdomains / related domains that contain trusted CDN names
        _TYPOSQUAT_WHITELIST = {
            # Cloudflare's own CDN / analytics / R2 subdomains
            "cloudflareinsights.com", "cloudflare.net", "cloudflarestorage.com",
            "cloudflaressl.com", "cloudflarepages.com", "workers.dev", "pages.dev",
            # Bootstrapcdn alternatives (legitimate)
            "bootstrapcdn.net",
            # googleapis variants (legitimate Google services)
            "googleapis.com", "google.com", "gstatic.com",
            # Fontawesome legitimate
            "fontawesome.com", "fontawesome.io", "fa.com",
        }
        for trusted in _MAGECART_INDICATORS["often_spoofed"]:
            trusted_core = trusted.split(".")[0]  # e.g. "googleapis"
            if trusted_core in script_lower and trusted not in script_lower:
                # Check if this URL is in the whitelist of legitimate related domains
                script_domain = script_lower.split("/")[2] if "//" in script_lower else ""
                if any(wl in script_domain for wl in _TYPOSQUAT_WHITELIST):
                    continue  # Skip — legitimate Cloudflare/related domain
                typosquats_found.append(script_url)
                indicators.append({
                    "type": "typosquat",
                    "severity": "high",
                    "url": script_url,
                    "matched_trusted": trusted,
                    "description": f"Script URL resembles '{trusted}' but is not the official domain — possible typosquat",
                    "recommendation": f"Verify this is the legitimate {trusted} CDN. Check WHOIS for domain age.",
                })
                break

        # 5. Suspicious path patterns
        for pat in _MAGECART_INDICATORS["skimmer_path_patterns"]:
            if re.search(pat, script_url, re.I):
                indicators.append({
                    "type": "suspicious_path",
                    "severity": "medium",
                    "url": script_url,
                    "description": "Script URL follows obfuscation pattern commonly used by Magecart",
                    "recommendation": "Audit this script's content and CDN host.",
                })
                break

        # 6. SRI missing on payment page = critical
        if is_payment_page:
            # Check if integrity attr present
            tag_match = re.search(
                r'<script[^>]+src\s*=\s*["\']' + re.escape(script_url) + r'["\'][^>]*>',
                body, re.I
            )
            if tag_match and 'integrity' not in tag_match.group(0).lower():
                sri_missing_on_payment.append(script_url)
                indicators.append({
                    "type": "no_sri_on_payment_page",
                    "severity": "critical",
                    "url": script_url,
                    "description": f"External script loaded without SRI on payment page — Magecart attack vector",
                    "recommendation": "Add integrity= hash to all external scripts on checkout/payment pages.",
                })

    # 7. Inline skimmer detection
    inline_scripts = re.findall(r'<script\b(?![^>]*\bsrc\b)[^>]*>(.*?)</script>', body,
                                 re.IGNORECASE | re.DOTALL)
    for script_content in inline_scripts:
        sc_lower = script_content.lower()
        hits = []
        for pat in _MAGECART_INDICATORS["inline_skimmer_patterns"]:
            if re.search(pat, script_content, re.I):
                hits.append(pat)
        if len(hits) >= 2:  # Multiple signals = higher confidence
            severity = "critical" if len(hits) >= 3 else "high"
            indicators.append({
                "type": "inline_skimmer_pattern",
                "severity": severity,
                "url": url,
                "description": f"Inline script matches {len(hits)} Magecart skimmer behavioral patterns",
                "patterns_matched": len(hits),
                "recommendation": "Audit inline scripts. Consider Content-Security-Policy to block inline scripts.",
                "snippet": script_content[:200].strip(),
            })

    # 8. Check for base64 encoded payloads (common obfuscation)
    b64_matches = re.findall(r"atob\(['\"]([A-Za-z0-9+/=]{30,})['\"]", body)
    for b64 in b64_matches[:3]:
        try:
            import base64 as _b64
            decoded = _b64.b64decode(b64).decode("utf-8", errors="replace")
            if any(kw in decoded.lower() for kw in ("document.cookie", "payment", "card", "fetch", "http")):
                indicators.append({
                    "type": "suspicious_base64_payload",
                    "severity": "high",
                    "url": url,
                    "description": "Base64-encoded string decodes to suspicious content (cookie/payment/fetch references)",
                    "decoded_preview": decoded[:100],
                    "recommendation": "Investigate this obfuscated payload.",
                })
        except Exception:
            pass

    # Build summary
    risk_level = "low"
    if any(i["severity"] == "critical" for i in indicators):
        risk_level = "critical"
    elif any(i["severity"] == "high" for i in indicators):
        risk_level = "high"
    elif indicators:
        risk_level = "medium"

    summary_parts = []
    if skimmer_domains_found:
        summary_parts.append(f"{len(skimmer_domains_found)} known skimmer domain(s)")
    if typosquats_found:
        summary_parts.append(f"{len(typosquats_found)} CDN typosquat(s)")
    if sri_missing_on_payment:
        summary_parts.append(f"{len(sri_missing_on_payment)} external script(s) without SRI on payment page")
    if not summary_parts and indicators:
        summary_parts.append(f"{len(indicators)} supply chain indicator(s)")
    summary = "; ".join(summary_parts) if summary_parts else "No supply chain indicators detected"

    return {
        "indicators": indicators,
        "risk_level": risk_level,
        "payment_page_risk": is_payment_page and bool(indicators),
        "external_scripts": all_external_scripts[:20],
        "sri_missing_on_payment": sri_missing_on_payment,
        "skimmer_domains_found": skimmer_domains_found,
        "typosquats_found": typosquats_found,
        "summary": summary,
    }
