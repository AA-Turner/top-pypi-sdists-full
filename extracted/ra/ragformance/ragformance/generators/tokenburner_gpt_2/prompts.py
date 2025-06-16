EXTRACT_TXT_PROMPT="Extract all raw text from this screenshot of a document page while preserving its original structural hierarchy (e.g., headings, paragraphs, lists, tables). Exclude any text embedded in figures, diagrams, charts, or image captions. Ensure the output reflects the document’s layout, including line breaks, indentation, and bullet points where applicable, but avoid extracting text that is part of graphical elements."

GENERATE_QUESTIONS_PROMPT="""Task: You are an expert question generator designed to analyze documents and create questions that the text explicitly answers. Analyze the provided document to identify its key themes, claims, evidence, and specific details. Generate a list of questions that a reader could answer directly using information from the document. Each question is concise, unambiguous, and answerable using only the document’s content. Avoid questions that require external knowledge or speculation. Present the questions in a numbered/bulleted list, ordered by relevance or frequency.

    Context:
    {raw_text}

    Answer using the following format:
    Output Format:
        1. Question 1 \n 2. Question 2 \n ...
    """

GENERATE_ANSWERS_PROMPT="""Task: Retrieve the question of the user. Answer the question using only the information provided in the context below. If the context does not contain sufficient information to answer the question, respond with: 'I cannot answer based on the provided context.

    Context:
    {context}

    User query:
    {query}

    Answer using the following format:
    Output Format:
        # Question: [user question]
        # Answer: [answer]
    """

FIND_CHUNKS_PROMPT="""Task: You are a precise information extraction assistant. Your task is to analyze a given context and identify exact passages that directly address a user’s query. Extract verbatim passages (direct quotes) from the context that explicitly answer the query. Do not paraphrase, summarize, or add explanations. Only provide exact matches. Present the passages found in a numbered/bulleted list.
    Context:
    {context}

    User query:
    {query}

    Answer using the following format:
    Output Format:
        Present the passages found in a numbered/bulleted list
        1. passage 1 \n 2. passage 2 \n etc
    """


CATEGORIZE_SECTIONS_PROMPT="""Task: You will classify a question into one of the following categories based on the provided question and context. Categorize the question using the criteria below and justify your reasoning. Identify the single most appropriate category (1–8) and explain why the question fits it.
Categories:
    1. Simple
        Definition: Questions asking straightforward facts unlikely to change over time.  
        Examples:
        - “When was Albert Einstein born?”
        - “Who wrote *Pride and Prejudice*?”

    2. Simple with Condition
        Definition: Simple fact-based questions that include additional conditions or contexts.  
        Examples: 
        - “What was Google's stock price on March 15, 2023?”
        - “What are Christopher Nolan's recent thriller films?”

    3. Set
        Definition: Questions expecting multiple entities or objects as answers.  
        Examples:  
        - “Which countries lie on the equator?”
        - “List all Nobel laureates in Chemistry for 2020.”

    4. Comparison
        Definition: Questions comparing two or more entities.  
        Examples: 
        - “Who won more Grand Slam titles, Serena Williams or Roger Federer?”
        - “Is Mount Everest taller than K2?”

    5. Aggregation
        Definition: Questions that require gathering and combining retrieved information.  
        Examples:  
        - “How many Grammy awards has Beyoncé won?”
        - “Total number of astronauts who have walked on the Moon?”

    6. Multi-hop
        Definition: Questions requiring sequential reasoning or information chaining to answer.  
        Examples:  
        - “Who starred in Steven Spielberg's latest movie?”
        - “What was the first book published by the author of the Harry Potter series?”

    7. Post-processing Heavy
        Definition: Questions that need significant computational or reasoning efforts after retrieval.  
        Examples:
        - “How many days did Barack Obama serve as the President of the United States?”
        - “Calculate the average length of term served by US Supreme Court justices.”

    8. False Premise
        Definition: Questions based on incorrect assumptions or premises.  
        Examples:  
        - “What's the title of Leonardo DiCaprio's album?”
        - “What was the name of Apple's car model released in 2021?”

    Context:
    {context}

    User query:
    {query}

    Answer using the following format:
    Output Format:
        Category: [Number and Name]
        Explanation: [1–2 sentences for justification]  
    """