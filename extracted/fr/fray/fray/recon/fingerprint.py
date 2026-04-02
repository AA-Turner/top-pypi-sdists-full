"""Fingerprinting — tech detection, security headers, cookies, payload recommendations.

Detection runs in three layers (fastest to most comprehensive):
  1. Cookie fingerprints   — exact match on Set-Cookie names
  2. Header fingerprints   — regex match on specific response headers
  3. Body fingerprints     — regex scan of HTML/JS body
  4. Wappalyzer DB         — loaded on first use from bundled/cached JSON
                             (github.com/enthec/webappfinder patterns)
"""

import base64
import hashlib
import json
import re
import struct
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from fray import PAYLOADS_DIR, DATA_DIR


# ── Tech → payload priority mapping ─────────────────────────────────────

_TECH_PAYLOAD_MAP: Dict[str, List[str]] = {
    "wordpress": ["sqli", "xss", "path_traversal", "command_injection", "ssrf"],
    "drupal": ["sqli", "ssti", "xss", "command_injection"],
    "joomla": ["sqli", "xss", "path_traversal", "command_injection"],
    "php": ["command_injection", "ssti", "path_traversal", "sqli", "xss", "host_header_injection"],
    "node.js": ["ssti", "ssrf", "xss", "command_injection", "prototype_pollution", "host_header_injection"],
    "express": ["prototype_pollution", "ssti", "ssrf", "xss", "command_injection", "host_header_injection"],
    "python": ["ssti", "ssrf", "command_injection", "sqli", "host_header_injection"],
    "java": ["sqli", "xxe", "ssti", "ssrf", "command_injection", "host_header_injection"],
    ".net": ["sqli", "xss", "path_traversal", "xxe", "host_header_injection"],
    "ruby": ["ssti", "command_injection", "sqli", "ssrf", "host_header_injection"],
    "nginx": ["path_traversal", "ssrf"],
    "apache": ["path_traversal", "ssrf"],
    "iis": ["path_traversal", "xss", "sqli"],
    "api_json": ["sqli", "ssrf", "command_injection", "ssti", "prototype_pollution"],
    "react": ["xss"],
    "angular": ["xss", "ssti"],
    "vue": ["xss"],
}

# ── Fingerprint signatures ───────────────────────────────────────────────

_HEADER_FINGERPRINTS: Dict[str, Dict[str, str]] = {
    # header_name_lower -> {pattern: tech_name}
    "x-powered-by": {
        r"PHP": "php",
        r"Express": "express",
        r"ASP\.NET": ".net",
        r"Servlet": "java",
        r"Django": "python",
        r"Phusion Passenger": "ruby",
        r"Next\.js": "next.js",
        r"Nuxt": "nuxt.js",
        r"Sails": "sails.js",
        r"Fastify": "fastify",
        r"Hono": "hono",
        r"Rocket": "rust",
        r"Actix": "rust",
    },
    "server": {
        r"nginx": "nginx",
        r"Apache": "apache",
        r"Microsoft-IIS": "iis",
        r"Kestrel": ".net",
        r"Jetty": "java",
        r"Tomcat": "java",
        r"gunicorn": "python",
        r"Werkzeug": "python",
        r"uvicorn": "python",
        r"Cowboy": "node.js",
    },
    "x-drupal-cache": {
        r".*": "drupal",
    },
    "x-generator": {
        r"Drupal": "drupal",
        r"WordPress": "wordpress",
        r"Joomla": "joomla",
    },
    "x-azure-ref": {
        r".*": "azure",
    },
    # Observability / APM
    "x-datadog-trace-id":       {r".*": "datadog"},
    "x-datadog-parent-id":      {r".*": "datadog"},
    "x-datadog-sampling-priority": {r".*": "datadog"},
    "x-newrelic-id":            {r".*": "new_relic"},
    "x-newrelic-transaction":   {r".*": "new_relic"},
    "x-request-id":             {r".*": "opentelemetry"},
    "traceparent":               {r".*": "opentelemetry"},
    "x-amzn-requestid":         {r".*": "aws"},
    "x-amzn-trace-id":          {r".*": "aws"},
    "x-amz-request-id":         {r".*": "aws"},
    # API Gateways
    "x-apigw-api-id":           {r".*": "aws_api_gateway"},
    "x-kong-request-id":        {r".*": "kong"},
    "x-gravitee-transaction-id": {r".*": "gravitee"},
    "x-tyk-authorization":      {r".*": "tyk"},
    "x-apim-request-id":        {r".*": "azure_apim"},
    "x-mashery-message-id":     {r".*": "mashery"},
    "x-mulesoft-correlation-id": {r".*": "mulesoft"},
    # Database / Cache (exposed in responses)
    "x-powered-cache":          {r".*": "cache"},
    "x-cache-status":           {r"HIT|MISS": "cache"},
    "x-redis-cache":            {r".*": "redis"},
    "x-memcache-hit":           {r".*": "memcached"},
    # Security tools
    "x-waf-event-info":         {r".*": "imperva_waf"},
    "x-fw-hash":                {r".*": "fortiweb"},
    "x-sucuri-id":              {r".*": "sucuri"},
    "x-iinfo":                  {r".*": "incapsula"},
    # e-Commerce platforms
    "x-shopify-stage":          {r".*": "shopify"},
    "x-shopify-request-id":     {r".*": "shopify"},
    "x-storefront-renderer":    {r".*": "shopify"},
    "x-magento-cache-debug":    {r".*": "magento"},
    "x-magento-tags":           {r".*": "magento"},
    "x-woocommerce":            {r".*": "woocommerce"},
    # CMS / Hosting
    "x-wp-total":               {r".*": "wordpress"},
    "x-wp-totalpages":          {r".*": "wordpress"},
    "x-pingback":               {r".*": "wordpress"},
    "x-ghost-cache-status":     {r".*": "ghost"},
    "x-hubspot-page-theme":     {r".*": "hubspot_cms"},
    "x-wix-request-id":         {r".*": "wix"},
    "x-squarespace-served-by":  {r".*": "squarespace"},
    "x-webflow-page":           {r".*": "webflow"},
    # CI/CD signals
    "x-jenkins":                {r".*": "jenkins"},
    "x-gitlab-meta":            {r".*": "gitlab"},
    "x-github-request-id":      {r".*": "github"},
    "x-vercel-id":              {r".*": "vercel"},
    "x-vercel-cache":           {r".*": "vercel"},
    "x-netlify-vary":           {r".*": "netlify"},
    "netlify-vary":             {r".*": "netlify"},
    "x-render-origin-server":   {r".*": "render"},
    "fly-request-id":           {r".*": "fly_io"},
    "x-railway-region":         {r".*": "railway"},
    # Identity / Auth
    "x-okta-request-id":        {r".*": "okta"},
    "x-auth0-request-id":       {r".*": "auth0"},
    "x-cognito-request-id":     {r".*": "aws_cognito"},
    "x-firebase-auth-id":       {r".*": "firebase"},
    # Japanese platforms
    "x-sakura-server":          {r".*": "sakura_internet"},
    "x-gmo-server":             {r".*": "gmo_cloud"},
    "x-iij-request-id":        {r".*": "iij"},
    # AI / LLM specific headers
    "openai-organization": {
        r".*": "openai",
    },
    "openai-model": {
        r".*": "openai",
    },
    "openai-processing-ms": {
        r".*": "openai",
    },
    "x-ratelimit-limit-tokens": {
        r".*": "llm_api",
    },
    "x-ratelimit-remaining-tokens": {
        r".*": "llm_api",
    },
    "anthropic-ratelimit-tokens-limit": {
        r".*": "anthropic",
    },
    "x-model-id": {
        r".*": "llm_api",
    },
    "x-inference-time": {
        r".*": "llm_api",
    },
    "x-groq-id": {
        r".*": "groq",
    },
    "cf-aig-cache-status": {
        r".*": "cloudflare_ai_gateway",
    },
    "x-kong-upstream-latency": {
        r".*": "kong",
    },
    "x-kong-proxy-latency": {
        r".*": "kong",
    },
    "x-bedrock-request-id": {
        r".*": "aws_bedrock",
    },
    "x-ms-azureml-model-group": {
        r".*": "azure_ml",
    },
    "cf-ray": {
        r".*": "cloudflare",
    },
    # Cloudflare Zaraz (tag management) — server-side, safe to detect
    "cf-zaraz-settings": {
        r".*": "cloudflare",
    },
    # NOTE: cf-team and cf-biso-version are NOT included here.
    # They are injected by the SCANNING MACHINE'S Cloudflare WARP / Zero Trust
    # client into every response regardless of the target. Confirmed: these
    # headers appear on example.com and httpbin.org (not Cloudflare hosted).
    # Using them as detection signals causes universal false positives for
    # anyone running WARP, Zscaler, Prisma Access, Netskope, etc.
    "x-amz-cf-id": {
        r".*": "cloudfront",
    },
    "x-amz-cf-pop": {
        r".*": "cloudfront",
    },
    # AWS ALB / CloudFront cookies as headers
    "cloudfront-viewer-country": {
        r".*": "cloudfront",
    },
    "x-cache": {
        r"CloudFront": "cloudfront",
        r"Varnish": "varnish",
        r"HIT.*akamai": "akamai",
    },
    "x-served-by": {
        r"cache-": "fastly",
    },
    "x-fastly-request-id": {
        r".*": "fastly",
    },
    "x-fastly-cache-status": {
        r".*": "fastly",
    },
    "fastly-restarts": {
        r".*": "fastly",
    },
    "x-fastly-pre-flight-cache": {
        r".*": "fastly",
    },
    "x-cache-hits": {
        r".*": "fastly",
    },
    "via": {
        r"varnish": "varnish",
        r"akamai": "akamai",
        r"cloudfront": "cloudfront",
        r"fastly": "fastly",
        r"BBC-GTM|Belfrage": "bbc_cosmos",
    },
}

_BODY_FINGERPRINTS: List[Tuple[str, str]] = [
    # (regex_pattern, tech_name)
    # CMS
    (r'<meta\s+name=["\']generator["\']\s+content=["\']WordPress\s+[\d.]+', "wordpress"),
    (r'/wp-content/', "wordpress"),
    (r'/wp-includes/', "wordpress"),
    (r'/wp-json/', "wordpress"),
    (r'<meta\s+name=["\']generator["\']\s+content=["\']Drupal', "drupal"),
    (r'/misc/drupal\.js', "drupal"),
    (r'/sites/default/files', "drupal"),
    (r'<meta\s+name=["\']generator["\']\s+content=["\']Joomla', "joomla"),
    (r'/media/system/js/', "joomla"),
    (r'/administrator/', "joomla"),
    # JS Frameworks
    (r'<div\s+id=["\']app["\']', "vue"),
    (r'<div\s+id=["\']root["\']', "react"),
    (r'__NEXT_DATA__', "next.js"),
    (r'/_next/static/', "next.js"),
    (r'data-nscript=', "next.js"),
    (r'__NUXT__', "nuxt.js"),
    (r'ng-app=', "angular"),
    (r'ng-version=', "angular"),
    (r'<script\s+src=[^>]*angular', "angular"),
    # Libraries
    (r'jquery[.-]\d+\.\d+', "jquery"),
    (r'/jquery\.min\.js', "jquery"),
    (r'/jquery-\d', "jquery"),
    (r'bootstrap\.min\.(?:js|css)', "bootstrap"),
    (r'cdn\.jsdelivr\.net/npm/bootstrap', "bootstrap"),
    (r'font-awesome|fontawesome', "font_awesome"),
    (r'swiper\.min\.(?:js|css)', "swiper"),
    (r'slick\.min\.(?:js|css)', "slick"),
    # Analytics & Tag Managers
    (r'googletagmanager\.com', "google_tag_manager"),
    (r'gtag\s*\(', "google_analytics"),
    (r'google-analytics\.com', "google_analytics"),
    (r'GA_MEASUREMENT_ID|G-[A-Z0-9]+', "google_analytics"),
    (r'connect\.facebook\.net', "facebook_pixel"),
    (r'snap\.licdn\.com', "linkedin_insight"),
    (r'bat\.bing\.com', "microsoft_clarity"),
    # Captcha
    (r'recaptcha|google\.com/recaptcha', "recaptcha"),
    (r'hcaptcha\.com', "hcaptcha"),
    (r'challenges\.cloudflare\.com/turnstile', "turnstile"),
    (r'captcha', "captcha"),
    # Server-side frameworks
    (r'csrfmiddlewaretoken', "python"),
    (r'__RequestVerificationToken', ".net"),
    (r'__VIEWSTATE', ".net"),
    (r'JSESSIONID', "java"),
    (r'laravel_session', "php"),
    (r'ci_session', "php"),
    (r'_rails', "ruby"),
    (r'X-Request-Id.*[a-f0-9-]{36}', "ruby"),
    # React ecosystem
    (r'react\.production\.min\.js', "react"),
    (r'react-dom', "react"),
    (r'ReactDOM\.render', "react"),
    (r'data-reactroot', "react"),
    (r'data-reactid', "react"),
    # Vue ecosystem
    (r'vue\.min\.js', "vue"),
    (r'vue\.runtime', "vue"),
    (r'Vue\.config', "vue"),
    # Additional frameworks
    (r'gatsby-', "gatsby"),
    (r'__gatsby', "gatsby"),
    (r'svelte', "svelte"),
    (r'ember\.js', "ember"),
    (r'backbone\.js', "backbone"),
    (r'knockout\.js', "knockout"),
    (r'mootools', "mootools"),
    (r'prototype\.js', "prototype_js"),
    (r'dojo\.js|dojox|dijit', "dojo"),
    (r'ext-all\.js|Ext\.create', "extjs"),
    # UI Libraries
    (r'tailwindcss|tailwind\.min\.css', "tailwindcss"),
    (r'material-ui|@mui/', "material_ui"),
    (r'antd|ant-design', "antd"),
    (r'semantic\.min\.(?:js|css)', "semantic_ui"),
    (r'foundation\.min\.(?:js|css)', "foundation"),
    (r'bulma\.min\.css', "bulma"),
    # Rich text / Editors
    (r'ckeditor', "ckeditor"),
    (r'tinymce', "tinymce"),
    (r'quill\.min\.(?:js|css)', "quill"),
    # Charts / Visualization
    (r'chart\.min\.js|Chart\.js', "chartjs"),
    (r'd3\.min\.js|d3\.v\d', "d3"),
    (r'highcharts', "highcharts"),
    (r'echarts', "echarts"),
    # Video / Media
    (r'video\.js|videojs', "videojs"),
    (r'plyr', "plyr"),
    (r'flowplayer', "flowplayer"),
    # SaaS integrations
    (r'salesforce\.com|force\.com', "salesforce"),
    (r'zendesk\.com|zdassets\.com', "zendesk"),
    (r'freshdesk\.com', "freshdesk"),
    (r'intercom\.io|intercomcdn', "intercom"),
    (r'drift\.com|driftt\.com', "drift"),
    (r'crisp\.chat', "crisp"),
    (r'tawk\.to', "tawkto"),
    (r'livechat|livechatinc', "livechat"),
    (r'hubspot\.com|hs-scripts', "hubspot"),
    (r'marketo\.net|munchkin', "marketo"),
    (r'pardot\.com', "pardot"),
    (r'segment\.com|segment\.io|analytics\.js', "segment"),
    (r'mixpanel\.com', "mixpanel"),
    (r'amplitude\.com', "amplitude"),
    (r'heap\.io|heapanalytics', "heap"),
    (r'optimizely\.com', "optimizely"),
    (r'launchdarkly', "launchdarkly"),
    (r'hotjar\.com', "hotjar"),
    (r'fullstory\.com', "fullstory"),
    (r'mouseflow\.com', "mouseflow"),
    (r'crazyegg\.com', "crazyegg"),
    # Payment
    (r'stripe\.com|Stripe\.js', "stripe"),
    (r'paypal\.com/sdk', "paypal"),
    (r'braintree', "braintree"),
    (r'adyen\.com', "adyen"),
    # Auth / Identity
    (r'auth0\.com', "auth0"),
    (r'okta\.com', "okta"),
    (r'firebase\.google\.com|firebaseapp', "firebase"),
    (r'supabase\.co', "supabase"),
    # Maps
    (r'maps\.google\.com|maps\.googleapis', "google_maps"),
    (r'mapbox\.com|mapboxgl', "mapbox"),
    (r'leaflet\.js|leaflet\.min', "leaflet"),
    # Misc
    (r'Sitecore', "sitecore"),
    (r'AEM|experience-platform', "adobe_experience_manager"),
    (r'Shopify\.', "shopify"),
    (r'cdn\.shopify\.com', "shopify"),
    (r'Magento|mage/cookies', "magento"),
    (r'Squarespace', "squarespace"),
    (r'wix\.com|parastorage\.com', "wix"),
    (r'webflow\.com', "webflow"),
    (r'ghost\.org|ghost\.io', "ghost"),
    (r'contentful\.com', "contentful"),
    (r'prismic\.io', "prismic"),
    (r'sanity\.io', "sanity"),
    # Server-side hints in HTML
    (r'powered by nginx', "nginx"),
    (r'powered by apache', "apache"),
    (r'x-aspnet-version', ".net"),
    (r'php\.net|powered by PHP', "php"),
    # ── WAF / Bot protection body signatures ─────────────────────────────
    # Akamai: 403 Access Denied pages contain a reference ID in the format
    # "Reference #N.{8hex}.{epoch}.{8hex}" — unambiguous Akamai fingerprint
    (r'Reference\s+#?[\d.]*[0-9a-f]{8}\.\d{9,}\.[0-9a-f]{8}', "akamai"),
    # Akamai error reference (alternate format without #)
    (r'Reference\s+\d+\.[0-9a-f]+\.\d{7,}\.[0-9a-f]+', "akamai"),
    # Generic Akamai ghost/error pages
    (r'akamai.*error|error.*akamai|ghost\.akamai', "akamai"),
    # Cloudflare challenge / error pages — these ARE server-sent by Cloudflare
    (r'cloudflare-static|cf-browser-verification|__cf_chl', "cloudflare"),
    # NOTE: window.isThroughProxy removed — this is injected by Cloudflare WARP
    # client into pages the user views through their ZT tunnel, not by the target.
    # F5 BIG-IP error pages
    (r'BIG-IP|The requested URL was rejected.*support ID', "f5"),
    # ── Monitoring & Observability ───────────────────────────────────────
    (r'datadog|dd-rum|datadoghq\.com', "datadog"),
    (r'newrelic\.com|NREUM|nr-data\.net', "new_relic"),
    (r'sentry\.io|sentry_dsn|@sentry/browser', "sentry"),
    (r'bugsnag\.com|bugsnag\.js', "bugsnag"),
    (r'rollbar\.com|rollbar\.js', "rollbar"),
    (r'raygun\.io|raygun\.com', "raygun"),
    (r'logrocket\.com|LogRocket', "logrocket"),
    (r'elastic\.co/apm|elasticapm', "elastic_apm"),
    (r'dynatrace\.com|dtPC', "dynatrace"),
    (r'appinsights|applicationinsights\.azure', "azure_monitor"),
    (r'gtm\.js|googletagmanager\.com/gtm', "google_tag_manager"),
    # ── CI/CD & Deployment platforms ─────────────────────────────────────
    (r'vercel\.com|vercel\.app|_vercel', "vercel"),
    (r'netlify\.com|netlify\.app', "netlify"),
    (r'pages\.dev|cloudflare\.com/pages', "cloudflare_pages"),
    (r'github\.io|github\.com/pages', "github_pages"),
    (r'render\.com|onrender\.com', "render"),
    (r'fly\.io|fly\.dev', "fly_io"),
    (r'railway\.app', "railway"),
    (r'heroku\.com|herokuapp\.com', "heroku"),
    (r'app\.aws\.com|awsapprunner', "aws_app_runner"),
    # ── Databases / Search (exposed in JS/meta) ───────────────────────────
    (r'mongodb\+srv|mongoose\.connect', "mongodb"),
    (r'elasticsearch\.com|elasticsearchjs', "elasticsearch"),
    (r'redis\.io|ioredis|redis\.createClient', "redis"),
    (r'postgrest\.org|supabase.*postgrest', "supabase"),
    (r'planetscale\.com', "planetscale"),
    (r'neon\.tech|neondb', "neon"),
    (r'cockroachlabs\.com', "cockroachdb"),
    (r'turso\.tech', "turso"),
    # ── GraphQL / API frameworks ─────────────────────────────────────────
    (r'__typename|GraphQL|graphiql|/graphql', "graphql"),
    (r'apollo-client|ApolloClient|apollographql', "apollo"),
    (r'hasura\.io|hasura\.app', "hasura"),
    (r'prisma\.io|@prisma/client', "prisma"),
    (r'trpc\.io|createTRPCRouter', "trpc"),
    (r'swagger-ui|swagger\.json|openapi\.json', "swagger"),
    (r'api-docs|redoc\.standalone', "redoc"),
    # ── Cloud Infrastructure indicators ──────────────────────────────────
    (r'amazonaws\.com|s3\.amazonaws|cloudfront\.net', "aws"),
    (r'azure\.com|azurewebsites\.net|blob\.core\.windows', "azure"),
    (r'googleapis\.com|gcs\.googleapis|storage\.googleapis', "gcp"),
    (r'digitalocean\.com|do\.co|nyc3\.cdn\.digitaloceanspaces', "digitalocean"),
    (r'linode\.com|akamaized\.net|linode\.images', "linode"),
    # ── eCommerce ────────────────────────────────────────────────────────
    (r'woocommerce|wc-api|is-woocommerce', "woocommerce"),
    (r'ecwid\.com|ecwidwidgets', "ecwid"),
    (r'bigcommerce\.com|stencil-utils', "bigcommerce"),
    (r'commercelayer\.io', "commercelayer"),
    (r'medusajs\.com|medusa-react', "medusa"),
    (r'saleor\.io', "saleor"),
    (r'sylius\.com', "sylius"),
    (r'oscommerce|osC_Product', "oscommerce"),
    (r'opencart\.com|catalog/view/theme', "opencart"),
    (r'prestashop|prestashop_csp', "prestashop"),
    (r'vtex\.com|vtex\.force\.com', "vtex"),
    (r'nopcommerce\.com', "nopcommerce"),
    # ── Japanese eCommerce / Platforms ───────────────────────────────────
    (r'futureshop|future-shop\.jp', "futureshop"),
    (r'makeshop\.jp', "makeshop"),
    (r'color-me-shop\.jp|colormeapi', "colormeshop"),
    (r'stores\.jp|stores-api', "stores_jp"),
    (r'base\.shop|base\.ec', "base_ec"),
    (r'shopserve\.jp', "shopserve"),
    (r'ebisumart\.com', "ebisumart"),
    (r'w2solution\.co\.jp|w2commerce', "w2commerce"),
    (r'ec-cube\.net|eccube', "ec_cube"),
    (r'lockon\.co\.jp', "ec_cube"),
    (r'hamee\.co\.jp|nextengine', "next_engine"),
    (r'ecforce\.jp', "ecforce"),
    (r'aishipr\.com', "aiship"),
    (r'shoppping\.jp|telecube\.co\.jp', "telecube"),
    # ── Japanese analytics / Marketing ───────────────────────────────────
    (r'gyro\.jp|gyro-n\.com', "gyro_n"),
    (r'ptengine\.com|ptengine\.jp', "ptengine"),
    (r'ebis\.ne\.jp|ad-ebis', "ad_ebis"),
    (r'sirok\.co\.jp|juicer', "juicer"),
    (r'datadrivenlab\.co\.jp', "ddl"),
    (r'zucks\.net', "zucks"),
    (r'logly\.co\.jp', "logly"),
    (r'criteo\.com|criteo\.net', "criteo"),
    (r'appier\.com|qcroc', "appier"),
    (r'kaeruhire\.jp|kaeru_', "kaeru"),
    # ── CDN / Media ──────────────────────────────────────────────────────
    (r'imgix\.net', "imgix"),
    (r'cloudinary\.com|res\.cloudinary', "cloudinary"),
    (r'imagekit\.io', "imagekit"),
    (r'bunny\.net|b-cdn\.net', "bunnycdn"),
    (r'cdn77\.com|cdn77\.org', "cdn77"),
    (r'keycdn\.com', "keycdn"),
    (r'statically\.io', "statically"),
    # ── CRM / Customer platforms ─────────────────────────────────────────
    (r'salesforce\.com|force\.com|lightning\.force', "salesforce"),
    (r'dynamics\.com|crm\.dynamics', "microsoft_dynamics"),
    (r'hubspot\.com|hs-sites\.com|hs-analytics', "hubspot"),
    (r'pipedrive\.com', "pipedrive"),
    (r'zoho\.com|zohopublic', "zoho"),
    # ── Security / Identity ───────────────────────────────────────────────
    (r'auth0\.com|auth0-spa|cdn\.auth0', "auth0"),
    (r'okta\.com|okta\.js', "okta"),
    (r'cognito|aws-amplify-user-pool', "aws_cognito"),
    (r'keycloak', "keycloak"),
    (r'onelogin\.com', "onelogin"),
    (r'ping\.identity|pingfederate|pingone\.com', "pingidentity"),
    (r'forgerock\.com', "forgerock"),
    (r'akamai\.com.*identity|akamai.*mfa', "akamai_identity"),
    # ── Search / Discovery ───────────────────────────────────────────────
    (r'algolia\.com|algolia\.net|algoliasearch', "algolia"),
    (r'meilisearch|meilisearch\.com', "meilisearch"),
    (r'typesense\.org', "typesense"),
    (r'swiftype\.com|swiftype', "swiftype"),
    (r'elastic\.co/enterprise-search|app-search', "elastic_enterprise_search"),
    # ── A/B Testing / Feature flags ───────────────────────────────────────
    (r'split\.io|splitio', "split_io"),
    (r'growthbook\.io', "growthbook"),
    (r'flagsmith\.com', "flagsmith"),
    (r'posthog\.com|posthog\.js', "posthog"),
    (r'launchdarkly\.com', "launchdarkly"),
    (r'optimizely\.com|optimizely-edge', "optimizely"),
    (r'vwo\.com|visualwebsiteoptimizer', "vwo"),
    (r'ab\.tasty|abtasty', "abtasty"),
    # ── Communication / Notifications ────────────────────────────────────
    (r'sendgrid\.com|sendgrid\.net', "sendgrid"),
    (r'mailchimp\.com|chimpstatic\.com', "mailchimp"),
    (r'twilio\.com|twilio\.js', "twilio"),
    (r'vonage\.com|nexmo\.com', "vonage"),
    (r'pusher\.com|pusherapp\.com', "pusher"),
    (r'ably\.io|ably\.com|ably-realtime', "ably"),
    (r'socket\.io|socket-io', "socket_io"),
    # ── Infrastructure-as-Code signals ───────────────────────────────────
    (r'terraform\.io|hashicorp\.com', "terraform"),
    (r'kubernetes\.io|k8s\.io', "kubernetes"),
    (r'helm\.sh', "helm"),
    (r'consul\.io|hashicorp\/consul', "consul"),
    (r'vault\.hashicorp\.com', "vault"),
    # ── Package managers / Build tools (exposed via source maps) ─────────
    (r'webpack|__webpack_require__|__webpack_modules__', "webpack"),
    (r'vite|/@vite/|vitejs\.dev', "vite"),
    (r'rollupjs\.org|rollup\.js', "rollup"),
    (r'parceljs\.org|parcel\.js', "parcel"),
    (r'turbopack|turbo\.build', "turbopack"),
    (r'esbuild\.github\.io|esbuild', "esbuild"),
    # ── AI / LLM / Chatbot Widget SDKs ──────────────────────────────────
    # Chatbot platforms (embedded widget scripts)
    (r'cdn\.botpress\.cloud|inject\.js.*botpress', "botpress"),
    (r'widget\.botpress\.cloud', "botpress"),
    (r'voiceflow\.com/widget|vf-widget|voiceflow\.com/runtime', "voiceflow"),
    (r'cdn\.ada\.support|ada\.support/embed|__ada', "ada_chatbot"),
    (r'code\.tidio\.co|tidio\.co/ltidio', "tidio"),
    (r'widget\.kommunicate\.io|kommunicate', "kommunicate"),
    (r'cdn\.customerly\.io|customerly', "customerly"),
    (r'chatbase\.co/embed|chatbase\.co/chatbot', "chatbase"),
    (r'cdn\.landbot\.io|landbot\.io/v3', "landbot"),
    (r'web\.chatgpt\.com|chat\.openai\.com/share', "chatgpt_embed"),
    (r'widget\.writesonic\.com|botsonic', "botsonic"),
    (r'cdn\.dialogflow\.com|dialogflow\.cloud\.google', "dialogflow"),
    (r'watson-assistant|watsonassistant|watson\.ai', "watson_assistant"),
    (r'lex\.amazonaws\.com|aws-lex', "amazon_lex"),
    (r'rasa\.com|rasa-webchat|rasa\.io', "rasa"),
    (r'manychat\.com', "manychat"),
    (r'chatfuel\.com', "chatfuel"),
    (r'collect\.chat|collectchat', "collectchat"),
    (r'flowxo\.com|flow\.xo', "flowxo"),
    (r'tiledesk\.com', "tiledesk"),
    (r'yellow\.ai|yellowmessenger', "yellow_ai"),
    (r'haptik\.ai|haptik\.co', "haptik"),
    (r'verloop\.io', "verloop"),
    (r'engati\.com', "engati"),
    (r'gorgias\.chat|gorgias\.io', "gorgias"),
    (r'kore\.ai|korebots', "kore_ai"),
    # AI platform JS SDKs & embeds
    (r'platform\.openai\.com|cdn\.openai\.com|openai-api', "openai"),
    (r'anthropic\.com|claude\.ai', "anthropic"),
    (r'cohere\.ai|cohere\.com/embed', "cohere"),
    (r'huggingface\.co/api|hf\.space|gradio\.app', "huggingface"),
    (r'replicate\.com/api|replicate\.delivery', "replicate"),
    (r'together\.ai|api\.together\.xyz', "together_ai"),
    (r'groq\.com|api\.groq\.com', "groq"),
    (r'mistral\.ai|api\.mistral\.ai', "mistral"),
    (r'perplexity\.ai', "perplexity"),
    (r'fireworks\.ai|api\.fireworks\.ai', "fireworks_ai"),
    (r'anyscale\.com|api\.anyscale\.com', "anyscale"),
    (r'deepinfra\.com', "deepinfra"),
    (r'ollama\.ai|ollama\.com', "ollama"),
    (r'langchain|langserve|langsmith', "langchain"),
    (r'llamaindex|llama-index|llama_index', "llamaindex"),
    (r'pinecone\.io|pinecone-client', "pinecone"),
    (r'weaviate\.io|weaviate\.cloud', "weaviate"),
    (r'chroma\.run|chromadb', "chromadb"),
    (r'qdrant\.io|qdrant\.tech', "qdrant"),
    (r'milvus\.io', "milvus"),
    # AI-powered search & RAG
    (r'algolia\.com/ai|algolia.*NeuralSearch', "algolia_ai"),
    (r'vectara\.com', "vectara"),
    (r'mendable\.ai', "mendable"),
    (r'inkeep\.com', "inkeep"),
    (r'docsbot\.ai', "docsbot"),
    # AI response content patterns (SSE streaming, model references)
    (r'data:\s*\{"id":"chatcmpl-', "openai_api"),
    (r'data:\s*\{"model":"gpt-', "openai_api"),
    (r'data:\s*\{"model":"claude-', "anthropic_api"),
    (r'"usage":\s*\{"prompt_tokens":', "llm_api"),
    (r'"choices":\s*\[\{"message":', "llm_api"),
    (r'"completion_tokens":\s*\d+', "llm_api"),
    (r'text/event-stream.*\{"model":', "llm_streaming"),
    # Copilot / AI assistant indicators
    (r'copilot|microsoft\.com/copilot', "copilot"),
    (r'github\.com/copilot|copilot\.github', "github_copilot"),
    (r'gemini\.google\.com|generativelanguage\.googleapis', "google_gemini"),
    (r'ai\.google\.dev|vertex\.ai|aiplatform\.googleapis', "google_vertex_ai"),
    (r'bedrock.*amazonaws|bedrock-runtime', "aws_bedrock"),
    (r'sagemaker.*amazonaws|sagemaker-runtime', "aws_sagemaker"),
    (r'azure\.ai|cognitiveservices\.azure|openai\.azure\.com', "azure_openai"),
    (r'ml\.azure\.com|azureml', "azure_ml"),
]

_COOKIE_FINGERPRINTS: Dict[str, str] = {
    # Language / Runtime
    "PHPSESSID": "php",
    "laravel_session": "php",
    "ci_session": "php",
    "CAKEPHP": "php",
    "JSESSIONID": "java",
    "connect.sid": "node.js",
    "ASP.NET_SessionId": ".net",
    ".AspNetCore.": ".net",
    "_rails": "ruby",
    "_session_id": "ruby",
    "csrftoken": "python",
    "sessionid": "python",
    "flask": "python",
    # CMS
    "wp-settings-": "wordpress",
    "wordpress_logged_in": "wordpress",
    "drupal": "drupal",
    "joomla": "joomla",
    "PrestaShop": "shopify",
    "Magento": "php",
    # CDN / WAF
    "__cfduid": "cloudflare",
    "cf_clearance": "cloudflare",
    "__cf_bm": "cloudflare",
    "AWSALB": "cloudfront",
    "AWSALBCORS": "cloudfront",
    "akamai_": "akamai",
    "AkamaiEdge": "akamai",
    "incap_ses_": "cloudflare",
    "visid_incap_": "cloudflare",
    "sucuri_cloudproxy": "cloudflare",
    # Analytics / Tracking
    "_ga": "google_analytics",
    "_gid": "google_analytics",
    "_gat": "google_analytics",
    "_fbp": "facebook_pixel",
    "_gcl_au": "google_analytics",
    "hubspotutk": "hubspot",
    "_hjid": "hotjar",
    # Captcha / Bot protection
    "_cf_chl_opt": "turnstile",
    "cf_chl_": "turnstile",
    # Infrastructure
    "SERVERID": "haproxy",
    "BIGipServer": "f5",
    "citrix_ns_id": "netscaler",
    # AI / Chatbot platforms
    "__bp_chat": "botpress",
    "__ada_chat": "ada_chatbot",
    "tidio_state_": "tidio",
    "kommunicate": "kommunicate",
    "vf-session": "voiceflow",
    "chatbase": "chatbase",
    "df-messenger": "dialogflow",
    "watsonAssistant": "watson_assistant",
    "intercom-session-": "intercom",
    "crisp-client": "crisp",
    # Monitoring / APM cookies
    "dd_s": "datadog",
    "nr-data": "new_relic",
    "__nr_uid": "new_relic",
    "dynaTrace": "dynatrace",
    # CI/CD / Hosting platforms
    "__vercel_live_token": "vercel",
    "NETLIFY": "netlify",
    "fly_session": "fly_io",
    # eCommerce
    "woocommerce_session_": "woocommerce",
    "PrestaShop-": "prestashop",
    "ec-cube": "ec_cube",
    "eccube": "ec_cube",
    # Auth providers
    "ory_session": "ory",
    "kc-access": "keycloak",
    "pa11y": "accessibility",
    # A/B Testing
    "_gaexp": "google_optimize",
    "optimizelyEndUserId": "optimizely",
    "split_": "split_io",
    # Analytics
    "posthog": "posthog",
    "_hjAbsoluteSessionInProgress": "hotjar",
    "abtasty": "abtasty",
    # Japanese platforms
    "makeshop": "makeshop",
    "futureshop": "futureshop",
    "eccube4": "ec_cube",
}

# ── Security header checklist ────────────────────────────────────────────

_SECURITY_HEADERS = {
    "strict-transport-security": {
        "name": "HSTS",
        "description": "HTTP Strict Transport Security",
        "severity": "high",
        "fix": {
            "nginx": 'add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;',
            "apache": 'Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"',
            "cloudflare_worker": 'response.headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");',
            "nextjs": "{ key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains; preload' }",
        },
    },
    "content-security-policy": {
        "name": "CSP",
        "description": "Content Security Policy",
        "severity": "high",
        "fix": {
            "nginx": "add_header Content-Security-Policy \"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none';\" always;",
            "apache": "Header always set Content-Security-Policy \"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none';\"",
            "cloudflare_worker": 'response.headers.set("Content-Security-Policy", "default-src \'self\'; script-src \'self\'; object-src \'none\'; base-uri \'self\'; frame-ancestors \'none\';");',
            "nextjs": "{ key: 'Content-Security-Policy', value: \"default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none';\" }",
        },
    },
    "x-frame-options": {
        "name": "X-Frame-Options",
        "description": "Clickjacking protection",
        "severity": "medium",
        "fix": {
            "nginx": 'add_header X-Frame-Options "DENY" always;',
            "apache": 'Header always set X-Frame-Options "DENY"',
            "cloudflare_worker": 'response.headers.set("X-Frame-Options", "DENY");',
            "nextjs": "{ key: 'X-Frame-Options', value: 'DENY' }",
        },
    },
    "x-content-type-options": {
        "name": "X-Content-Type-Options",
        "description": "MIME type sniffing prevention",
        "severity": "medium",
        "fix": {
            "nginx": 'add_header X-Content-Type-Options "nosniff" always;',
            "apache": 'Header always set X-Content-Type-Options "nosniff"',
            "cloudflare_worker": 'response.headers.set("X-Content-Type-Options", "nosniff");',
            "nextjs": "{ key: 'X-Content-Type-Options', value: 'nosniff' }",
        },
    },
    "x-xss-protection": {
        "name": "X-XSS-Protection",
        "description": "Browser XSS filter (legacy)",
        "severity": "low",
        "fix": {
            "nginx": 'add_header X-XSS-Protection "0" always;',
            "apache": 'Header always set X-XSS-Protection "0"',
            "cloudflare_worker": 'response.headers.set("X-XSS-Protection", "0");',
            "nextjs": "{ key: 'X-XSS-Protection', value: '0' }",
        },
    },
    "referrer-policy": {
        "name": "Referrer-Policy",
        "description": "Controls referrer information",
        "severity": "low",
        "fix": {
            "nginx": 'add_header Referrer-Policy "strict-origin-when-cross-origin" always;',
            "apache": 'Header always set Referrer-Policy "strict-origin-when-cross-origin"',
            "cloudflare_worker": 'response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");',
            "nextjs": "{ key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' }",
        },
    },
    "permissions-policy": {
        "name": "Permissions-Policy",
        "description": "Browser feature permissions",
        "severity": "low",
        "fix": {
            "nginx": 'add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), interest-cohort=()" always;',
            "apache": 'Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), interest-cohort=()"',
            "cloudflare_worker": 'response.headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=()");',
            "nextjs": "{ key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' }",
        },
    },
    "cross-origin-opener-policy": {
        "name": "COOP",
        "description": "Cross-Origin Opener Policy",
        "severity": "low",
        "fix": {
            "nginx": 'add_header Cross-Origin-Opener-Policy "same-origin" always;',
            "apache": 'Header always set Cross-Origin-Opener-Policy "same-origin"',
            "cloudflare_worker": 'response.headers.set("Cross-Origin-Opener-Policy", "same-origin");',
            "nextjs": "{ key: 'Cross-Origin-Opener-Policy', value: 'same-origin' }",
        },
    },
    "cross-origin-resource-policy": {
        "name": "CORP",
        "description": "Cross-Origin Resource Policy",
        "severity": "low",
        "fix": {
            "nginx": 'add_header Cross-Origin-Resource-Policy "same-origin" always;',
            "apache": 'Header always set Cross-Origin-Resource-Policy "same-origin"',
            "cloudflare_worker": 'response.headers.set("Cross-Origin-Resource-Policy", "same-origin");',
            "nextjs": "{ key: 'Cross-Origin-Resource-Policy', value: 'same-origin' }",
        },
    },
}


def generate_header_fix_snippets(missing_headers: Dict[str, Any]) -> Dict[str, str]:
    """Generate copy-paste config snippets for all missing security headers.

    Args:
        missing_headers: Dict from check_security_headers()["missing"].

    Returns:
        Dict with keys 'nginx', 'apache', 'cloudflare_worker', 'nextjs' —
        each containing a ready-to-paste config block.
    """
    snippets: Dict[str, list] = {
        "nginx": [],
        "apache": [],
        "cloudflare_worker": [],
        "nextjs": [],
    }

    # Map display names back to header keys
    name_to_key = {info["name"]: key for key, info in _SECURITY_HEADERS.items()}

    for display_name in missing_headers:
        header_key = name_to_key.get(display_name)
        if not header_key:
            continue
        fix = _SECURITY_HEADERS[header_key].get("fix", {})
        for platform, snippet in fix.items():
            if platform in snippets:
                snippets[platform].append(snippet)

    # Assemble into config blocks
    result: Dict[str, str] = {}

    if snippets["nginx"]:
        result["nginx"] = "# nginx — add to server {} block\n" + "\n".join(snippets["nginx"])

    if snippets["apache"]:
        result["apache"] = "# Apache — add to .htaccess or <VirtualHost>\n" + "\n".join(snippets["apache"])

    if snippets["cloudflare_worker"]:
        lines = "\n  ".join(snippets["cloudflare_worker"])
        result["cloudflare_worker"] = (
            "// Cloudflare Worker — add to fetch handler\n"
            f"  {lines}"
        )

    if snippets["nextjs"]:
        entries = ",\n          ".join(snippets["nextjs"])
        result["nextjs"] = (
            "// next.config.js — headers()\n"
            "async headers() {\n"
            "  return [{\n"
            "    source: '/(.*)',\n"
            "    headers: [\n"
            f"          {entries},\n"
            "    ],\n"
            "  }];\n"
            "}"
        )

    return result


# ── Functions ────────────────────────────────────────────────────────────

def _score_header_value(name_lower: str, value: str) -> tuple:
    """Score the quality of a security header's VALUE (not just presence).

    Returns (quality: str, detail: str) where quality is one of:
    STRONG, MODERATE, WEAK, MISCONFIGURED
    """
    v = value.strip()
    vl = v.lower()

    if name_lower == "content-security-policy":
        if "'unsafe-inline'" in vl and "'unsafe-eval'" in vl:
            return ("WEAK", "unsafe-inline + unsafe-eval defeats CSP purpose")
        if "'unsafe-inline'" in vl:
            return ("WEAK", "unsafe-inline allows inline scripts — XSS protection bypassed")
        if "default-src *" in vl or "default-src: *" in vl:
            return ("WEAK", "wildcard default-src allows loading from any origin")
        if "default-src" not in vl and "script-src" not in vl:
            return ("MODERATE", "no default-src or script-src directive")
        return ("STRONG", "")

    if name_lower == "strict-transport-security":
        import re as _re_hdr
        _ma = _re_hdr.search(r"max-age=(\d+)", vl)
        if _ma:
            _age = int(_ma.group(1))
            if _age < 86400:
                return ("WEAK", f"max-age={_age} ({_age//3600}h) — too short, should be >= 1 year")
            if _age < 2592000:
                return ("MODERATE", f"max-age={_age} ({_age//86400}d) — recommended >= 1 year (31536000)")
            if "includesubdomains" not in vl:
                return ("MODERATE", "missing includeSubDomains — subdomains unprotected")
            if "preload" not in vl:
                return ("MODERATE", "missing preload — not eligible for browser preload list")
            return ("STRONG", "")
        return ("MISCONFIGURED", "no max-age directive found")

    if name_lower == "x-frame-options":
        vu = v.upper()
        if vu in ("DENY", "SAMEORIGIN"):
            return ("STRONG", "")
        if vu.startswith("ALLOW-FROM"):
            return ("MODERATE", "ALLOW-FROM is deprecated and ignored by modern browsers")
        return ("MISCONFIGURED", f"invalid value '{v}' — ignored by browsers")

    if name_lower == "referrer-policy":
        if vl in ("unsafe-url", "no-referrer-when-downgrade", ""):
            return ("WEAK", f"'{vl}' leaks full URL to third parties")
        if vl in ("no-referrer", "same-origin", "strict-origin", "strict-origin-when-cross-origin"):
            return ("STRONG", "")
        return ("MODERATE", "")

    if name_lower == "permissions-policy":
        if not v.strip():
            return ("WEAK", "empty value — no features restricted")
        _restricted = v.count("=()")
        if _restricted >= 3:
            return ("STRONG", f"{_restricted} features restricted")
        return ("MODERATE", f"only {_restricted} feature(s) restricted")

    if name_lower == "x-content-type-options":
        if vl == "nosniff":
            return ("STRONG", "")
        return ("MISCONFIGURED", f"expected 'nosniff', got '{v}'")

    if name_lower == "x-xss-protection":
        if vl.startswith("1") and "mode=block" in vl:
            return ("STRONG", "")
        if vl == "0":
            return ("MODERATE", "explicitly disabled — relies on CSP instead (acceptable if CSP is strong)")
        return ("WEAK", "enabled without mode=block")

    if name_lower in ("cross-origin-opener-policy",):
        if vl == "same-origin":
            return ("STRONG", "")
        if vl == "same-origin-allow-popups":
            return ("MODERATE", "allows popups — weaker than same-origin")
        if vl == "unsafe-none":
            return ("WEAK", "no cross-origin isolation")
        return ("MODERATE", "")

    if name_lower in ("cross-origin-resource-policy",):
        if vl == "same-origin":
            return ("STRONG", "")
        if vl == "same-site":
            return ("MODERATE", "allows same-site cross-origin access")
        if vl == "cross-origin":
            return ("WEAK", "allows any origin to load this resource")
        return ("MODERATE", "")

    return ("STRONG", "")


# Quality → score multiplier for value-weighted scoring
_QUALITY_WEIGHT = {
    "STRONG": 1.0,
    "MODERATE": 0.6,
    "WEAK": 0.25,
    "MISCONFIGURED": 0.1,
}

# Header importance weights (higher = more impactful on overall score)
_HEADER_WEIGHT = {
    "strict-transport-security": 15,
    "content-security-policy": 20,
    "x-frame-options": 10,
    "x-content-type-options": 10,
    "x-xss-protection": 5,
    "referrer-policy": 10,
    "permissions-policy": 10,
    "cross-origin-opener-policy": 10,
    "cross-origin-resource-policy": 10,
}


def check_security_headers(headers: Dict[str, str]) -> Dict[str, Any]:
    """Audit security headers from an HTTP response.

    Score is value-weighted: a present header with WEAK value scores much
    less than one with STRONG value.  Missing critical headers have a larger
    penalty than missing low-severity ones.
    """
    results: Dict[str, Any] = {
        "present": {},
        "missing": {},
        "score": 0,
        "value_score": 0,
        "value_issues": [],
    }

    max_points = sum(_HEADER_WEIGHT.get(k, 10) for k in _SECURITY_HEADERS)
    earned_points = 0.0

    for header_key, info in _SECURITY_HEADERS.items():
        weight = _HEADER_WEIGHT.get(header_key, 10)
        if header_key in headers:
            value = headers[header_key]
            quality, detail = _score_header_value(header_key, value)
            multiplier = _QUALITY_WEIGHT.get(quality, 0.5)
            earned_points += weight * multiplier

            entry = {
                "value": value,
                "description": info["description"],
                "quality": quality,
            }
            if detail:
                entry["detail"] = detail
            results["present"][info["name"]] = entry
            if quality in ("WEAK", "MISCONFIGURED"):
                results["value_issues"].append({
                    "header": info["name"],
                    "quality": quality,
                    "detail": detail,
                    "value": value[:120],
                })
        else:
            results["missing"][info["name"]] = {
                "description": info["description"],
                "severity": info["severity"],
            }

    # Value-weighted score (0-100)
    results["value_score"] = round((earned_points / max_points) * 100) if max_points > 0 else 0
    # Presence-based score (backward compat)
    total = len(_SECURITY_HEADERS)
    found = len(results["present"])
    results["presence_score"] = round((found / total) * 100) if total > 0 else 0
    # Combined score: 60% value quality + 40% presence
    results["score"] = round(results["value_score"] * 0.6 + results["presence_score"] * 0.4)

    if results["missing"]:
        results["fix_snippets"] = generate_header_fix_snippets(results["missing"])
    return results


def check_clickjacking(headers: Dict[str, str], csp_value: str = "") -> Dict[str, Any]:
    """Assess clickjacking protection from X-Frame-Options and CSP frame-ancestors.

    Returns a dict with:
      - vulnerable: bool — True if page can be framed by an attacker
      - severity: "none" | "low" | "medium" | "high"
      - x_frame_options: dict with value + issues
      - frame_ancestors: dict with value + issues
      - protections: list of active protections
      - issues: list of problems found
      - recommendation: str
    """
    result: Dict[str, Any] = {
        "vulnerable": True,
        "severity": "high",
        "x_frame_options": {"present": False, "value": None, "valid": False},
        "frame_ancestors": {"present": False, "value": None, "valid": False},
        "protections": [],
        "issues": [],
        "recommendation": "",
    }

    # ── X-Frame-Options ──
    xfo = headers.get("x-frame-options", "").strip()
    if xfo:
        result["x_frame_options"]["present"] = True
        result["x_frame_options"]["value"] = xfo
        xfo_upper = xfo.upper()
        if xfo_upper == "DENY":
            result["x_frame_options"]["valid"] = True
            result["protections"].append("X-Frame-Options: DENY — framing blocked completely")
        elif xfo_upper == "SAMEORIGIN":
            result["x_frame_options"]["valid"] = True
            result["protections"].append("X-Frame-Options: SAMEORIGIN — only same-origin framing")
        elif xfo_upper.startswith("ALLOW-FROM"):
            result["x_frame_options"]["valid"] = True
            result["issues"].append("X-Frame-Options: ALLOW-FROM is deprecated and ignored by modern browsers")
        else:
            result["issues"].append(f"X-Frame-Options: invalid value '{xfo}' — ignored by browsers")

    # ── CSP frame-ancestors ──
    csp_raw = csp_value or headers.get("content-security-policy", "")
    if csp_raw:
        for directive in csp_raw.split(";"):
            directive = directive.strip().lower()
            if directive.startswith("frame-ancestors"):
                fa_value = directive[len("frame-ancestors"):].strip()
                result["frame_ancestors"]["present"] = True
                result["frame_ancestors"]["value"] = fa_value
                if fa_value == "'none'":
                    result["frame_ancestors"]["valid"] = True
                    result["protections"].append("CSP frame-ancestors 'none' — framing blocked completely")
                elif fa_value == "'self'":
                    result["frame_ancestors"]["valid"] = True
                    result["protections"].append("CSP frame-ancestors 'self' — only same-origin framing")
                elif fa_value == "*":
                    result["issues"].append("CSP frame-ancestors * — allows framing from ANY origin")
                else:
                    result["frame_ancestors"]["valid"] = True
                    result["protections"].append(f"CSP frame-ancestors restricted to: {fa_value}")
                break

    # ── Verdict ──
    has_xfo = result["x_frame_options"]["valid"]
    has_fa = result["frame_ancestors"]["valid"]

    if has_fa and has_xfo:
        result["vulnerable"] = False
        result["severity"] = "none"
        result["recommendation"] = "Both X-Frame-Options and CSP frame-ancestors are set — good defense-in-depth"
    elif has_fa:
        result["vulnerable"] = False
        result["severity"] = "low"
        result["recommendation"] = "CSP frame-ancestors protects modern browsers. Add X-Frame-Options for legacy browser coverage"
    elif has_xfo:
        result["vulnerable"] = False
        result["severity"] = "low"
        result["recommendation"] = "X-Frame-Options provides protection. Add CSP frame-ancestors for defense-in-depth"
    else:
        result["vulnerable"] = True
        result["severity"] = "high"
        result["issues"].append("No clickjacking protection — page can be framed by any origin")
        result["recommendation"] = "Add both: X-Frame-Options: DENY and CSP frame-ancestors 'none'"

    # Check for report-only CSP (doesn't actually protect)
    csp_ro = headers.get("content-security-policy-report-only", "")
    if "frame-ancestors" in csp_ro and not has_fa:
        result["issues"].append("frame-ancestors is in report-only CSP — does NOT actually block framing")

    return result


def check_captcha(headers: Dict[str, str], body: str) -> Dict[str, Any]:
    """Detect CAPTCHA / bot-challenge providers from response headers and body.

    Returns:
      - detected: bool
      - providers: list of {name, type, evidence}
      - challenge_on_load: bool — True if challenge fires on page load (not just on form)
    """
    result: Dict[str, Any] = {
        "detected": False,
        "providers": [],
        "challenge_on_load": False,
    }

    body_lower = body.lower() if body else ""
    hdrs_lower = {k.lower(): v.lower() for k, v in headers.items()} if headers else {}

    _CAPTCHA_SIGNATURES = [
        # (name, type, body_patterns, header_patterns)
        ("reCAPTCHA v2", "checkbox",
         ["google.com/recaptcha", "grecaptcha", "g-recaptcha", "recaptcha.js", "recaptcha/api.js"],
         []),
        ("reCAPTCHA v3", "invisible",
         ["recaptcha/api.js?render=", "grecaptcha.execute", "recaptcha-v3"],
         []),
        ("hCaptcha", "checkbox",
         ["hcaptcha.com", "h-captcha", "hcaptcha.js"],
         []),
        ("Cloudflare Turnstile", "invisible",
         ["challenges.cloudflare.com/turnstile", "cf-turnstile", "turnstile.js"],
         ["cf-mitigated", "cf-challenge"]),
        ("Cloudflare Challenge", "interstitial",
         ["cf-browser-verification", "challenge-platform", "cf_chl_opt", "ray id"],
         ["cf-mitigated", "cf-chl-bypass"]),
        ("GeeTest", "slider",
         ["geetest.com", "gt.js", "initgeetest", "geetest_"],
         []),
        ("Arkose Labs / FunCaptcha", "interactive",
         ["arkoselabs.com", "funcaptcha", "enforcement.arkoselabs"],
         []),
        ("AWS WAF CAPTCHA", "checkbox",
         ["awswaf.com/captcha", "aws-waf-captcha", "captcha.awswaf"],
         ["x-amzn-waf-action"]),
        ("Akamai Bot Manager", "invisible",
         ["akamai.com/bm", "bmak.js", "_abck"],
         ["akamai-grn"]),
        ("PerimeterX / HUMAN", "invisible",
         ["perimeterx.net", "human.com/px", "_pxhd", "px-captcha"],
         []),
        ("DataDome", "interstitial",
         ["datadome.co", "dd.js", "datadome"],
         ["x-datadome"]),
        ("Kasada", "invisible",
         ["kasada.io", "ips.js", "cd.kasada"],
         []),
    ]

    for name, cap_type, body_pats, hdr_pats in _CAPTCHA_SIGNATURES:
        evidence = []
        for pat in body_pats:
            if pat in body_lower:
                evidence.append(f"body: {pat}")
                break
        for pat in hdr_pats:
            for hk, hv in hdrs_lower.items():
                if pat in hk or pat in hv:
                    evidence.append(f"header: {hk}={hv[:60]}")
                    break
            if evidence and evidence[-1].startswith("header:"):
                break

        if evidence:
            result["providers"].append({
                "name": name,
                "type": cap_type,
                "evidence": evidence,
            })

    if result["providers"]:
        result["detected"] = True
        # Challenge-on-load: interstitial or invisible types that block before content
        result["challenge_on_load"] = any(
            p["type"] in ("interstitial", "invisible") for p in result["providers"]
        )

    return result


def detect_captcha(headers: Dict[str, str], body: str) -> Dict[str, Any]:
    """Convenience alias for check_captcha — detects captcha providers per subdomain.

    Used by the per-subdomain scan pipeline to surface reCAPTCHA, hCaptcha,
    Turnstile, GeeTest, Arkose etc. on login/checkout/form subdomains.
    Strips ZT client headers before checking so WARP/Zscaler don't create
    false Cloudflare Turnstile detections.
    """
    clean_headers = {k: v for k, v in headers.items()
                     if k.lower() not in _ZT_CLIENT_HEADERS}
    return check_captcha(clean_headers, body)


def _mmh3_hash32(data: bytes) -> int:
    """Pure-Python MurmurHash3 32-bit (Shodan-compatible favicon hash).

    Shodan computes: mmh3.hash(base64.encodebytes(favicon_bytes))
    We replicate this without the mmh3 dependency.
    """
    encoded = base64.encodebytes(data)
    length = len(encoded)
    nblocks = length // 4
    h1 = 0
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    M32 = 0xFFFFFFFF

    for i in range(nblocks):
        k1 = struct.unpack_from('<I', encoded, i * 4)[0]
        k1 = (k1 * c1) & M32
        k1 = ((k1 << 15) | (k1 >> 17)) & M32
        k1 = (k1 * c2) & M32
        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & M32
        h1 = (h1 * 5 + 0xe6546b64) & M32

    tail_idx = nblocks * 4
    k1 = 0
    tail_size = length & 3
    if tail_size >= 3:
        k1 ^= encoded[tail_idx + 2] << 16
    if tail_size >= 2:
        k1 ^= encoded[tail_idx + 1] << 8
    if tail_size >= 1:
        k1 ^= encoded[tail_idx]
        k1 = (k1 * c1) & M32
        k1 = ((k1 << 15) | (k1 >> 17)) & M32
        k1 = (k1 * c2) & M32
        h1 ^= k1

    h1 ^= length
    h1 ^= (h1 >> 16)
    h1 = (h1 * 0x85ebca6b) & M32
    h1 ^= (h1 >> 13)
    h1 = (h1 * 0xc2b2ae35) & M32
    h1 ^= (h1 >> 16)

    # Convert to signed 32-bit (Shodan convention)
    if h1 >= 0x80000000:
        h1 -= 0x100000000
    return h1


# ── Known favicon hashes (Shodan mmh3 format) ──────────────────────────
# Source: Shodan favicon hash lookups, OWASP favfreak, community lists
_FAVICON_HASHES: Dict[int, str] = {
    # Web servers
    116323821: "Apache default",
    -1137940464: "Apache Tomcat",
    -297069493: "Apache Tomcat (alt)",
    971615514: "Nginx default",
    -28805239: "IIS 7/8/10 default",
    -1293790851: "IIS default (alt)",
    # CMS
    -1585019720: "WordPress",
    1485257654: "WordPress (alt)",
    -1343027601: "Drupal",
    -1395133075: "Joomla",
    -1028703177: "Magento",
    # Panels / Admin
    -160298610: "cPanel",
    988422585: "Plesk",
    116927286: "phpMyAdmin",
    -305179312: "Webmin",
    708578229: "Grafana",
    1331249234: "Jenkins",
    81586312: "Jenkins (alt)",
    -2057558656: "GitLab",
    -1051252948: "Gitea",
    -1293291900: "Kibana",
    -759810094: "Elasticsearch",
    442749392: "SonarQube",
    -428790988: "Portainer",
    # Infrastructure
    -247388890: "Cisco ASA/AnyConnect",
    362091310: "Fortinet FortiGate",
    -1950415971: "Palo Alto",
    2089645498: "SonicWall",
    -305711853: "Sophos UTM",
    -553656166: "MikroTik RouterOS",
    -1588080585: "Ubiquiti UniFi",
    1820085796: "Synology DSM",
    -1123760091: "QNAP NAS",
    # Cloud / CDN
    1279567031: "Cloudflare",
    -1022515040: "AWS S3 / CloudFront",
    1936600898: "Azure Web App",
    -350298590: "Heroku",
    # Dev / Debug
    -335242539: "Spring Boot (leaf)",
    -1032603498: "Django default",
    116323821: "Express/Node default",
    1485257654: "React default (CRA)",
    -281346917: "Next.js",
    1936600898: "Vue CLI default",
    -1840324437: "Swagger UI",
    -442056: "Jupyter Notebook",
    # Mail / Collab
    -1626032521: "Outlook Web Access",
    1407375746: "Zimbra",
    -1913498791: "Roundcube",
}


def check_favicon(host: str, port: int = 443, use_ssl: bool = True,
                   timeout: int = 8) -> Dict[str, Any]:
    """Fetch /favicon.ico and compute Shodan-compatible mmh3 hash for fingerprinting.

    Returns:
      - found: bool
      - md5: hex digest
      - mmh3: signed 32-bit hash (Shodan format)
      - size: bytes
      - technology: matched name or None
      - shodan_query: ready-to-use Shodan search query
    """
    from fray.recon.http import _fetch_url

    result: Dict[str, Any] = {
        "found": False,
        "md5": None,
        "mmh3": None,
        "size": 0,
        "technology": None,
        "shodan_query": None,
    }

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    url = f"{scheme}://{host}{port_str}/favicon.ico"

    try:
        status, body, hdrs = _fetch_url(url, timeout=timeout, verify_ssl=True)
        if status == 0 and use_ssl:
            status, body, hdrs = _fetch_url(url, timeout=timeout, verify_ssl=False)
    except Exception:
        return result

    if status != 200 or not body:
        return result

    # Must be a binary file, not an HTML error page
    ct = hdrs.get("content-type", "")
    if "html" in ct.lower():
        return result

    # Binary favicon data may have been decoded as str by _fetch_url;
    # re-encode preserving raw bytes (utf-8 with surrogatepass for \ufffd)
    if isinstance(body, str):
        try:
            body_bytes = body.encode("latin-1")
        except UnicodeEncodeError:
            body_bytes = body.encode("utf-8", errors="replace")
    else:
        body_bytes = body

    if len(body_bytes) < 10 or len(body_bytes) > 1_000_000:
        return result

    result["found"] = True
    result["size"] = len(body_bytes)
    result["md5"] = hashlib.md5(body_bytes).hexdigest()
    result["mmh3"] = _mmh3_hash32(body_bytes)
    result["shodan_query"] = f"http.favicon.hash:{result['mmh3']}"

    tech = _FAVICON_HASHES.get(result["mmh3"])
    if tech:
        result["technology"] = tech

    return result


def check_cookies(headers: Dict[str, str]) -> Dict[str, Any]:
    """Audit cookies for security flags: HttpOnly, Secure, SameSite, Path."""
    results: Dict[str, Any] = {
        "cookies": [],
        "issues": [],
        "score": 100,
    }

    # Collect all Set-Cookie headers. http.client merges them with ", " but
    # that's unreliable. We look for the raw header which may appear once or
    # be comma-joined. Split carefully on ", " only when followed by a cookie name=.
    raw = headers.get("set-cookie", "")
    if not raw:
        return results

    # Split on boundaries that look like a new cookie (name=value after ", ")
    cookie_strings = re.split(r',\s*(?=[A-Za-z0-9_.-]+=)', raw)

    for cs in cookie_strings:
        cs = cs.strip()
        if not cs or '=' not in cs:
            continue

        parts = cs.split(";")
        name_value = parts[0].strip()
        name = name_value.split("=", 1)[0].strip()

        flags_raw = [p.strip().lower() for p in parts[1:]]
        flags_set = set(flags_raw)

        has_httponly = any("httponly" in f for f in flags_set)
        has_secure = any("secure" in f for f in flags_set)
        has_samesite = any("samesite" in f for f in flags_set)
        samesite_value = None
        for f in flags_raw:
            if f.startswith("samesite="):
                samesite_value = f.split("=", 1)[1].strip()
                break

        cookie_info: Dict[str, Any] = {
            "name": name,
            "httponly": has_httponly,
            "secure": has_secure,
            "samesite": samesite_value or (True if has_samesite else None),
        }
        results["cookies"].append(cookie_info)

        # Flag issues
        if not has_httponly:
            results["issues"].append({
                "cookie": name,
                "issue": "Missing HttpOnly flag",
                "severity": "high",
                "risk": "Cookie accessible via JavaScript — XSS can steal sessions",
            })
        if not has_secure:
            results["issues"].append({
                "cookie": name,
                "issue": "Missing Secure flag",
                "severity": "high",
                "risk": "Cookie sent over HTTP — vulnerable to MITM interception",
            })
        if not has_samesite:
            results["issues"].append({
                "cookie": name,
                "issue": "Missing SameSite attribute",
                "severity": "medium",
                "risk": "Vulnerable to CSRF attacks",
            })
        elif samesite_value and samesite_value.lower() == "none" and not has_secure:
            results["issues"].append({
                "cookie": name,
                "issue": "SameSite=None without Secure flag",
                "severity": "high",
                "risk": "Browser will reject this cookie (Chrome/Firefox require Secure with SameSite=None)",
            })

    # Score: deduct points per issue
    if results["cookies"]:
        deductions = len([i for i in results["issues"] if i["severity"] == "high"]) * 15
        deductions += len([i for i in results["issues"] if i["severity"] == "medium"]) * 8
        results["score"] = max(0, 100 - deductions)

    return results



# ── Zero Trust / SASE client-injected headers ────────────────────────────────
# These headers are added by the SCANNING MACHINE'S own security stack
# (Cloudflare WARP, Zscaler ZIA/ZPA, Netskope, Prisma Access, Cisco Umbrella)
# into EVERY response the scanner receives, regardless of the target.
# Including them in fingerprinting causes universal false positives.
# Confirmed: cf-team appears on example.com and httpbin.org.
_ZT_CLIENT_HEADERS: frozenset = frozenset({
    # Cloudflare WARP / Zero Trust
    "cf-team",
    "cf-biso-version",
    "cf-access-authenticated-user-email",
    "cf-access-jwt-assertion",
    "cf-warp-tag-id",
    "cf-connecting-ip",
    # Zscaler ZIA / ZPA
    "x-zscaler-client",
    "x-zscaler-transactionid",
    "z-forwarded-for",
    "x-zscaler-ia",
    "x-zscaler-sans",
    # Netskope
    "x-netskope-client",
    "x-netskope-transactionid",
    "ns-client-ip",
    "x-netskope-activity-id",
    # Palo Alto Prisma Access
    "x-pan-session-id",
    "x-panw-region",
    "x-prisma-access",
    # Cisco Umbrella / Secure Access
    "x-umbrella-orgid",
    "x-umbrella-identity",
    # Menlo Security
    "x-menlo-security",
    "x-menlo-client",
    # Generic ZT timing (cfReqDur injected by WARP into every response)
    "server-timing",
})


def fingerprint_app(headers: Dict[str, str], body: str,
                    cookies_raw: str = "") -> Dict[str, Any]:
    """Detect technology stack from headers, body, and cookies.

    Strips client-injected Zero Trust / SASE proxy headers before detection
    so WARP, Zscaler, Prisma Access etc. don't cause false positives.
    """
    detected: Dict[str, float] = {}  # tech -> confidence (0-1)

    def _add(tech: str, conf: float):
        detected[tech] = min(1.0, detected.get(tech, 0) + conf)

    # Strip headers injected by the scanning machine's own ZT/SASE stack.
    # These are NOT server-sent by the target.
    headers = {k: v for k, v in headers.items()
               if k.lower() not in _ZT_CLIENT_HEADERS}

    # Header-based detection
    for header_name, patterns in _HEADER_FINGERPRINTS.items():
        value = headers.get(header_name, "")
        if not value:
            continue
        for pattern, tech in patterns.items():
            if re.search(pattern, value, re.IGNORECASE):
                _add(tech, 0.7)

    # Body-based detection
    for pattern, tech in _BODY_FINGERPRINTS:
        if re.search(pattern, body, re.IGNORECASE):
            _add(tech, 0.5)

    # Cookie-based detection
    cookie_str = cookies_raw or headers.get("set-cookie", "")
    for cookie_name, tech in _COOKIE_FINGERPRINTS.items():
        if cookie_name.lower() in cookie_str.lower():
            _add(tech, 0.6)

    # Content-type based hints
    ct = headers.get("content-type", "")
    if "application/json" in ct:
        _add("api_json", 0.4)

    # ── Wappalyzer DB (wappalyzer@6 npm) — loaded on first use ──────────
    # Augments hand-coded signatures with community-maintained patterns.
    # wapp is None if unavailable (offline / download not yet attempted).
    try:
        wapp = _load_wappalyzer_db()
        if wapp:  # non-empty dict = loaded OK
            # Header patterns from wappalyzer
            for tech_name, tech_data in wapp.items():
                if not isinstance(tech_data, dict):
                    continue
                for h_name, h_pattern in (tech_data.get("headers") or {}).items():
                    h_val = headers.get(h_name.lower(), "")
                    if not h_val:
                        continue
                    # Empty pattern = header presence is sufficient (wappalyzer convention)
                    if not h_pattern:
                        _add(tech_name.lower().replace(" ", "_"), 0.6)
                    else:
                        try:
                            pat_str = str(h_pattern).split("\\;")[0]
                            if re.search(pat_str, h_val, re.IGNORECASE):
                                _add(tech_name.lower().replace(" ", "_"), 0.6)
                        except re.error:
                            pass
                # Cookie patterns from wappalyzer
                for c_name, c_pattern in (tech_data.get("cookies") or {}).items():
                    if cookie_str and c_name.lower() in cookie_str.lower():
                        _add(tech_name.lower().replace(" ", "_"), 0.55)
                # Script src patterns (body-level, lightweight substring check)
                for script_pat in (tech_data.get("scriptSrc") or [])[:3]:
                    try:
                        pat_str = str(script_pat).split("\\;")[0]
                        if len(pat_str) > 4 and re.search(pat_str, body,
                                                            re.IGNORECASE):
                            _add(tech_name.lower().replace(" ", "_"), 0.45)
                    except re.error:
                        pass
    except Exception:
        pass  # Wappalyzer DB is optional — never block detection

    # ── Alias / implication pass ──────────────────────────────────────────
    # Some detected techs imply a parent platform that should also be shown.
    # e.g. CloudFront → AWS, Cloudflare Zero Trust → Cloudflare
    _IMPLIES: Dict[str, str] = {
        "cloudfront":              "aws",
        "amazon_cloudfront":       "aws",
        "amazon_alb":              "aws",
        "aws_bedrock":             "aws",
        "aws_app_runner":          "aws",
        "aws_api_gateway":         "aws",
        "aws_cognito":             "aws",
        # NOTE: cloudflare_zero_trust and cloudflare_biso removed from _IMPLIES.
        # These were based on cf-team / cf-biso-version which are client-injected.
        "cloudflare_ai_gateway":   "cloudflare",
        "cloudflare_pages":        "cloudflare",
        "azure_apim":              "azure",
        "azure_openai":            "azure",
        "azure_ml":                "azure",
        "azure_monitor":           "azure",
        "woocommerce":             "wordpress",
        "bbc_cosmos":              "varnish",
    }
    for child, parent in _IMPLIES.items():
        if child in detected and parent not in detected:
            detected[parent] = detected[child] * 0.9  # slightly lower confidence

    # Sort by confidence
    sorted_tech = sorted(detected.items(), key=lambda x: x[1], reverse=True)

    return {
        "technologies": {t: round(c, 2) for t, c in sorted_tech},
        "primary": sorted_tech[0][0] if sorted_tech else None,
        "all": [t for t, _ in sorted_tech],
    }


# ── Wappalyzer DB loader ─────────────────────────────────────────────────────
# Loads the Wappalyzer technology DB from npm (wappalyzer@6).
# The DB is split across 27 files: a.json … z.json + _.json
# Source: cdn.jsdelivr.net/npm/wappalyzer@6/technologies/{letter}.json
# Each file contains ~300 techs with headers, cookies, html, scriptSrc patterns.
#
# Priority:
#   1. Bundled fray/data/wappalyzer.json   (ships with package)
#   2. ~/.fray/wappalyzer.json             (cached on first download)
#   3. Download from jsDelivr CDN          (attempted once per process)

_WAPP_DB_CACHE: Optional[Dict[str, Any]] = None
_WAPP_DOWNLOAD_ATTEMPTED: bool = False


def _load_wappalyzer_db() -> Optional[Dict[str, Any]]:
    """Load Wappalyzer v6 tech DB. Returns dict of {TechName: {...}} or None."""
    global _WAPP_DB_CACHE, _WAPP_DOWNLOAD_ATTEMPTED

    # Already loaded (or confirmed unavailable)
    if _WAPP_DB_CACHE is not None:
        return _WAPP_DB_CACHE if _WAPP_DB_CACHE else None

    # 1. Bundled fray/data/wappalyzer.json
    bundled = DATA_DIR / "wappalyzer.json"
    if bundled.exists():
        try:
            _WAPP_DB_CACHE = json.loads(bundled.read_text(encoding="utf-8"))
            if _WAPP_DB_CACHE:
                return _WAPP_DB_CACHE
        except Exception:
            pass

    # 2. Cached ~/.fray/wappalyzer.json
    cached = Path.home() / ".fray" / "wappalyzer.json"
    if cached.exists():
        try:
            data = json.loads(cached.read_text(encoding="utf-8"))
            if data:
                _WAPP_DB_CACHE = data
                return _WAPP_DB_CACHE
        except Exception:
            cached.unlink(missing_ok=True)  # corrupt cache — delete and re-download

    # 3. Download from jsDelivr (wappalyzer@6 npm package)
    # The DB is split into 27 files by first letter. We download all and merge.
    # Only attempted once per process — silent on failure.
    if _WAPP_DOWNLOAD_ATTEMPTED:
        _WAPP_DB_CACHE = {}  # sentinel
        return None
    _WAPP_DOWNLOAD_ATTEMPTED = True

    try:
        import urllib.request as _ureq
        _CDN_BASE = "https://cdn.jsdelivr.net/npm/wappalyzer@6/technologies"
        _LETTERS = list("abcdefghijklmnopqrstuvwxyz") + ["_"]
        merged: Dict[str, Any] = {}

        for letter in _LETTERS:
            try:
                url = f"{_CDN_BASE}/{letter}.json"
                req = _ureq.Request(
                    url, headers={"User-Agent": "fray/3.5 (tech-detection)"}
                )
                with _ureq.urlopen(req, timeout=6) as r:
                    chunk = json.loads(r.read().decode("utf-8", errors="replace"))
                    merged.update(chunk)
            except Exception:
                continue  # missing letter file is fine

        if merged:
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_text(
                json.dumps(merged, ensure_ascii=False), encoding="utf-8"
            )
            _WAPP_DB_CACHE = merged
            return _WAPP_DB_CACHE
    except Exception:
        pass

    _WAPP_DB_CACHE = {}  # sentinel — don't retry
    return None


def update_wappalyzer_db() -> bool:
    """Force re-download of the Wappalyzer DB, bypassing cache.

    Called by `fray doctor` and `fray feed --update-wappalyzer`.
    Returns True if successful.
    """
    global _WAPP_DB_CACHE, _WAPP_DOWNLOAD_ATTEMPTED
    _WAPP_DB_CACHE = None
    _WAPP_DOWNLOAD_ATTEMPTED = False
    # Remove cached file to force fresh download
    cached = Path.home() / ".fray" / "wappalyzer.json"
    cached.unlink(missing_ok=True)
    result = _load_wappalyzer_db()
    return bool(result)


def recommend_categories(fingerprint: Dict[str, Any]) -> List[str]:
    """Map detected technologies to recommended payload categories."""
    seen: Dict[str, float] = {}
    techs = fingerprint.get("technologies", {})

    for tech, confidence in techs.items():
        # confidence may be a float, int, or dict (e.g. {"value": 0.8, ...})
        if isinstance(confidence, dict):
            conf_val = float(confidence.get("confidence", confidence.get("value", 0.5)))
        else:
            conf_val = float(confidence) if confidence else 0.5
        categories = _TECH_PAYLOAD_MAP.get(tech, [])
        for i, cat in enumerate(categories):
            # Higher priority (lower index) + higher confidence = higher score
            score = conf_val * (1.0 - i * 0.1)
            if cat not in seen or seen[cat] < score:
                seen[cat] = score

    # Sort by score, filter to categories that actually exist
    available = {d.name for d in PAYLOADS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")}
    ranked = sorted(seen.items(), key=lambda x: x[1], reverse=True)
    return [cat for cat, _ in ranked if cat in available]
