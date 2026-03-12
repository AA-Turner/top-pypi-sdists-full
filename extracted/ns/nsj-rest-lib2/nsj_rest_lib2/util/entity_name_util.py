def format_entity_name(resource: str) -> str:
    """
    Formata o identificador tecnico do recurso para nome amigavel.

    Args:
        resource: Nome do recurso (ex.: "categorias-profissionais").

    Returns:
        Nome formatado para exibicao em mensagens de erro/log.
    """
    # Normaliza o nome tecnico do recurso para texto amigavel em mensagens.
    value = (resource or "").strip().replace("-", " ").replace("_", " ")
    if not value:
        return "Desconhecida"

    lower = value.lower()
    if lower.endswith("oes") and len(lower) > 3:
        lower = lower[:-3] + "ao"
    elif lower.endswith("aes") and len(lower) > 3:
        lower = lower[:-3] + "ao"
    elif lower.endswith("res") and len(lower) > 3:
        lower = lower[:-2]
    elif lower.endswith("s") and len(lower) > 1:
        lower = lower[:-1]

    return " ".join(word.capitalize() for word in lower.split())
