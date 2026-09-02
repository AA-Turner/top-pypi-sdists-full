from __future__ import annotations

from matrx_scraper.seo_audit import IMAGE_INVENTORY_LIMIT, audit_html


def test_audit_captures_page_identity_media_and_all_resource_classes() -> None:
    html = """
    <html>
      <head>
        <meta name="generator" content="WordPress 7.0">
        <meta name="author" content="Ada Author">
        <meta property="og:site_name" content="Example">
        <meta property="og:image" content="/fallback.jpg">
        <link rel="stylesheet" href="/site.css">
        <link rel="icon" href="/favicon.ico">
        <link rel="https://api.w.org/" href="/wp-json/">
        <link rel="shortlink" href="/?p=42">
        <link rel="manifest" href="/app.webmanifest">
        <script src="/app.js"></script>
        <script type="application/ld+json">
          {
            "@context":"https://schema.org",
            "@type":"Article",
            "headline":"Complete page",
            "datePublished":"2026-01-02",
            "primaryImageOfPage":{"@type":"ImageObject","url":"/hero.jpg"}
          }
        </script>
        <script type="application/ld+json">
          {"@type":"VideoObject","name":"Demo","embedUrl":"https://youtu.be/demo"}
        </script>
      </head>
      <body class="page page-id-42 page-template-landing" style="background-image:url('/texture.webp')">
        <h1>Complete page</h1>
        <img src="/hero.jpg" srcset="/hero-small.jpg 400w, /hero.jpg 1200w"
             alt="Hero" width="1200" height="630" fetchpriority="high">
        <picture><source srcset="/wide.avif 2x"></picture>
        <video poster="/poster.jpg"><source src="/movie.mp4" type="video/mp4"></video>
        <audio src="/audio.mp3"></audio>
        <iframe src="https://www.youtube.com/embed/demo"></iframe>
        <a href="/guide.pdf">Guide</a>
        <p>Useful visible content for the complete page audit.</p>
      </body>
    </html>
    """

    audit = audit_html(html, "https://example.com/article")

    assert len(audit.structured_data["json_ld"]) == 2
    assert len(audit.structured_data["json_ld_raw"]) == 2
    assert {"Article", "ImageObject", "VideoObject"}.issubset(audit.schema_types)
    assert audit.page_identity["generator"] == "WordPress 7.0"
    assert audit.page_identity["author"] == "Ada Author"
    assert audit.page_identity["featured_image"] == "https://example.com/hero.jpg"
    assert audit.page_identity["featured_image_source"] == "schema.primaryImageOfPage"
    assert audit.page_identity["cms"] == "wordpress"
    assert audit.page_identity["shortlink"] == "https://example.com/?p=42"
    assert audit.page_identity["api_urls"] == ["https://example.com/wp-json/"]
    assert audit.page_identity["platform_details"] == {
        "wordpress_post_id": "42",
        "template": "page-template-landing",
    }
    assert "wordpress-rest-api" in audit.page_identity["platform_signals"]
    assert audit.image_inventory[0]["featured"] is True
    assert audit.image_inventory[0]["srcset"] == [
        "https://example.com/hero-small.jpg",
        "https://example.com/hero.jpg",
    ]
    # web.snapshot.images.items contract (matrx-frontend parseSnapshotImages):
    # absolute src, numeric width/height, optional presentation attributes.
    hero = audit.image_inventory[0]
    assert hero["src"] == "https://example.com/hero.jpg"
    assert hero["alt"] == "Hero"
    assert hero["width"] == 1200
    assert hero["height"] == 630
    assert hero["fetchpriority"] == "high"
    assert set(hero) >= {
        "src",
        "srcset",
        "sizes",
        "alt",
        "width",
        "height",
        "loading",
        "decoding",
        "fetchpriority",
        "title",
    }
    assert audit.resources["truncated"] is False
    assert {
        "audio",
        "document",
        "icon",
        "image",
        "manifest",
        "script",
        "stylesheet",
        "video",
    }.issubset(audit.resources["counts"])


def test_image_inventory_caps_items_while_counts_stay_true() -> None:
    imgs = "".join(
        f'<img src="/img-{i}.jpg" alt="img {i}">' for i in range(IMAGE_INVENTORY_LIMIT + 25)
    )
    html = f"<html><body><h1>Gallery</h1>{imgs}</body></html>"

    audit = audit_html(html, "https://example.com/gallery")

    assert len(audit.image_inventory) == IMAGE_INVENTORY_LIMIT
    assert audit.images_total == IMAGE_INVENTORY_LIMIT + 25
    assert audit.images_missing_alt == 0
    assert audit.image_inventory[0]["src"] == "https://example.com/img-0.jpg"
