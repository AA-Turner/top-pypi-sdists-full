def format_scraped_pages_section(
    limited_good_scrapes: list[dict],
    thin_scrapes: list[dict],
) -> str:
    """
    Format scraped pages into a structured text section for AI consumption.

    Separates high-quality scrapes (>= 1,000 characters) from thin content
    scrapes, providing clear categorisation and formatting for each.
    """
    scraped_pages_content = "=== FULLY SCRAPED PAGES (Complete Content) ===\n\n"

    if limited_good_scrapes:
        scraped_pages_content += "--- High-Quality Scrapes (>= 1,000 characters) ---\n\n"
        for idx, scraped_data in enumerate(limited_good_scrapes, 1):
            scraped_pages_content += f"[Scraped Page {idx}]\n"
            scraped_pages_content += f"Title: {scraped_data['title']}\n"
            scraped_pages_content += f"Url: {scraped_data['url']}\n"
            scraped_pages_content += f"{scraped_data['date_info']}"
            scraped_pages_content += f"Content:\n{scraped_data['content']}\n\n"
            scraped_pages_content += "---\n\n"

    if thin_scrapes:
        scraped_pages_content += "--- Thin Content Scrapes (< 1,000 characters) ---\n"
        scraped_pages_content += (
            "Note: These pages had minimal content but may still contain useful information.\n\n"
        )
        for idx, scraped_data in enumerate(thin_scrapes, 1):
            scraped_pages_content += f"[Thin Page {idx}]\n"
            scraped_pages_content += f"Title: {scraped_data['title']}\n"
            scraped_pages_content += f"Url: {scraped_data['url']}\n"
            scraped_pages_content += f"{scraped_data['date_info']}"
            scraped_pages_content += f"Content:\n{scraped_data['content']}\n\n"
            scraped_pages_content += "---\n\n"

    return scraped_pages_content
