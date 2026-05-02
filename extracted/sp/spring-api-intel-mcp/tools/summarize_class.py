from core.indexer import CodeIndex

async def summarize_class(index: CodeIndex, class_name: str, use_sampling=False, streams=None) -> str:
    """
    Return a structured summary of a class:
    its type, annotations, dependencies, and public methods.
    The coding agent will use this to generate a plain-English explanation.
    """
    info = index.classes.get(class_name)
    if not info:
        close = [name for name in index.classes if class_name.lower() in name.lower()]
        if close:
            return f"Class '{class_name}' not found. Did you mean: {', '.join(close)}?"
        return f"Class '{class_name}' not found in indexed codebase."

    source = index.file_contents.get(info.file_path, "")
    lines = source.splitlines()

    structured = "\n".join([
        f"Class     : {class_name}",
        f"File      : {info.file_path}",
        f"Annotations: {', '.join(info.annotations) if info.annotations else 'none'}",
        f"Dependencies: {', '.join(info.dependencies) if info.dependencies else 'none'}",
        f"Methods   : {', '.join(info.methods[:150])}",
        "",
        "--- Source (first 600 lines) ---",
        *lines[:600],
    ])

    streams_ready=(
        use_sampling
        and streams is not None
        and len(streams) == 2
        and streams[0] is not None
        and streams[1] is not None
    )

    if streams_ready:
        try:
            from core.sampling import request_summary
            read_stream, write_stream = streams
            prompt = f"Summarize this Spring Boot Java class:\n\n{structured}"
            ai_summary = await request_summary(read_stream, write_stream, prompt)
            if ai_summary:
                return f"=== AI Summary ===\n{ai_summary}\n\n=== Raw Data ===\n{structured}"
        except Exception as e:
            pass 

    return structured
