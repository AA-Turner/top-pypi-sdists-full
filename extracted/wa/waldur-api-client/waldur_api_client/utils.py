def parse_link_header(link_header: str) -> dict[str, str]:
    """
    Parse Link header to extract pagination URLs.

    Args:
        link_header: The Link header string (e.g. '<url>; rel="next"')

    Returns:
        Dictionary mapping relation types (next, prev, first, last) to URLs
    """
    links = {}
    if not link_header:
        return links

    for link in link_header.split(","):
        link = link.strip()
        if not link:
            continue
        parts = link.split(";")
        if len(parts) < 2:
            continue
        url = parts[0].strip()
        if url.startswith("<") and url.endswith(">"):
            url = url[1:-1]
        for part in parts[1:]:
            part = part.strip()
            if part.startswith("rel="):
                rel_type = part[4:].strip().strip('"').strip("'")
                links[rel_type] = url
                break
    return links
