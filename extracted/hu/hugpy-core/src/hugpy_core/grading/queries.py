"""The grading queries Core starts with: what a model of each task is asked, in tiers, and how each answer is checked.

They are the grading table's own rows (sql/create.py: grading_queries), written from here when Core starts. A row
nobody changed follows this file; a row the operator changed, or added, is theirs and is left as it is.

A suite grades the models of one task. Within a suite a category is one thing that is tested, asked at every tier
(1 the easiest): a model's schedule is every category's tier 1, then every tier 2, then every tier 3.

    hugpy-native-v2     text-generation      27   nine categories of plain questions, each with one right answer
    hugpy-vision-v1     image-text-to-text    9   what is in a drawn image: its colors, its count, its writing
    hugpy-embed-v1      feature-extraction    3   a sentence is nearer its paraphrase than an unrelated one
    hugpy-summary-v1    summarization         3   a summary keeps the facts of what it shortens
    hugpy-imagegen-v1   text-to-image         3   an image comes back, of the size that was asked
    hugpy-speech-v1     text-to-speech        3   speech comes back, as long as the words take
    hugpy-videogen-v1   text-to-video         1   a clip comes back
    hugpy-interp-v1     video-interpolation   1   a clip comes back with frames added

The text suite, with its checks, is the one hugpy_curation's fleet grading was written with and hugpy-core carried
until 0.5 (same name, same 27 questions: a grade read then and now is of the same thing). The images, the clip, the
sentences and the paragraphs are those of the hugpy fixture library (2026-10-25: drawn and written for it, CC0);
the files are in media/. Speech recognition has no query here: a clip of speech that may be given away with Core
has yet to be made. A row for it, like any other, can be put in the table.

What a generation is checked for is what its engine measured of what it wrote (its size, its frames, its seconds).
Whether a picture shows an apple is not checked: nothing here judges by eye.
"""
from ..imports import (
    PACKAGE_DIR,
    TIER_NAMES,
    base64,
    json,
    os,
    with_no_think,
)

MEDIA = os.path.join(PACKAGE_DIR, 'grading', 'media')
CHAT = '/v1/chat/completions'
TEXT_TOKENS = 256               # enough to answer a question after a short think


def media(name: str) -> str:
    """One of the files of media/, as base64."""
    with open(os.path.join(MEDIA, name), 'rb') as fh:
        return base64.b64encode(fh.read()).decode('ascii')


def chat(prompt: str, image: str = None) -> dict:
    """The body of a question asked in a chat (of an image, when one is named): one answer, the same every time."""
    words = with_no_think(prompt)
    content = words if image is None else [
        dict(type='text', text=words),
        dict(type='image_url', image_url=dict(url='data:image/png;base64,' + media(image)))]
    return dict(messages=[dict(role='user', content=content)], max_tokens=TEXT_TOKENS, temperature=0)


# a suite: (its name, the task whose models it grades, the route its queries are called on, its categories).
# A category: its name and its queries, easiest first. A query: (the call's body, its checks, a right answer)
TEXT = ('hugpy-native-v2', 'text-generation', CHAT, (
    ('math', (
        (chat('Compute 15 + 22. Reply with only the final number.'), [['last_number', 37]], '37'),
        (chat('Compute 17 * 23. Reply with only the final number.'), [['last_number', 391]], '391'),
        (chat('Solve for x: 3x + 12 = 27. Reply with only the number.'), [['last_number', 5]], '5'))),
    ('wordprob', (
        (chat('John has 5 apples. He buys 3 more. How many? Reply number only.'), [['last_number', 8]], '8'),
        (chat('A store had 48 apples. Sold 19 in the morning, 12 in the afternoon. Left? Reply number only.'),
         [['last_number', 17]], '17'),
        (chat('Train A leaves at 60mph. 2 hours later Train B leaves at 80mph. Hours until they meet? Reply number only.'),
         [['last_number', 6]], '6'))),
    ('factual', (
        (chat('What planet is known as the Red Planet? Reply with only the planet name.'), [['contains', 'mars']], 'mars'),
        (chat('What is the chemical symbol for gold? Reply with only the symbol.'), [['contains', 'au']], 'au'),
        (chat('Who discovered penicillin? Reply with only the last name.'), [['contains', 'fleming']], 'fleming'))),
    ('format_primes', (
        (chat('List the first three prime numbers separated by commas and nothing else.'),
         [['first_numbers', [2, 3, 5]]], '2, 3, 5'),
        (chat('List the first five prime numbers separated by commas and nothing else.'),
         [['first_numbers', [2, 3, 5, 7, 11]]], '2, 3, 5, 7, 11'),
        (chat('List the first five prime numbers in reverse order separated by commas and nothing else.'),
         [['first_numbers', [11, 7, 5, 3, 2]]], '11, 7, 5, 3, 2'))),
    ('logic', (
        (chat('If all bloops are razzies, and all razzies are lazzies, are all bloops lazzies? Answer yes or no.'),
         [['contains', 'yes']], 'yes'),
        (chat('A is taller than B. C is shorter than B. Who is the shortest? Reply only with the letter.'),
         [['exact_folded', 'C']], 'C'),
        (chat('Can a 3-gallon jug and a 5-gallon jug measure exactly 4 gallons? Answer yes or no.'),
         [['contains', 'yes']], 'yes'))),
    ('exact_instruction', (
        (chat('Reply with exactly the single word: BANANA'), [['exact', 'BANANA']], 'BANANA'),
        (chat('Reply with exactly the single word: BANANA, but in lowercase.'), [['exact', 'banana']], 'banana'),
        (chat('Reply with exactly the string: [BANANA_123] and absolutely nothing else.'),
         [['exact', '[BANANA_123]']], '[BANANA_123]'))),
    ('coding', (
        (chat('Write a Python one-liner using sum() to total a list named xs. Reply with only code.'),
         [['compact_contains', 'sum(xs)']], 'total = sum(xs)'),
        (chat('Write a Python list comprehension returning only even numbers from list xs. Reply with only code.'),
         [['compact_contains', '%2==0']], '[x for x in xs if x % 2 == 0]'),
        (chat('Write a recursive Python lambda named fib for Fibonacci. Reply with only code.'),
         [['contains_all', ['lambda', '-1', '-2']]], 'fib = lambda n: n if n < 2 else fib(n-1) + fib(n-2)'))),
    ('json', (
        (chat('Output only a JSON object with key "a" set to 1.'), [['json_equals', {'a': 1}]], '{"a": 1}'),
        (chat('Output only a JSON object with keys "a" set to 1 and "b" set to 2.'),
         [['json_equals', {'a': 1, 'b': 2}]], '{"a": 1, "b": 2}'),
        (chat('Output only a JSON object with key "a" containing a list of 1 and 2.'),
         [['json_equals', {'a': [1, 2]}]], '{"a": [1, 2]}'))),
    ('letters', (
        (chat('How many times does the letter e appear in the word tree? Reply number only.'), [['last_number', 2]], '2'),
        (chat('How many times does the letter r appear in the word strawberry? Reply number only.'), [['last_number', 3]], '3'),
        (chat('How many times does the letter s appear in the word mississippi? Reply number only.'), [['last_number', 4]], '4'))),
))

# square.png: a red square on white. shapes.png: the word HELLO over a red circle, a blue square and a green
# triangle, left to right. scene.png: four circles (red, green, blue, purple) over three squares (blue, orange,
# red), and the code A7X92 in small writing
VISION = ('hugpy-vision-v1', 'image-text-to-text', CHAT, (
    ('color', (
        (chat('What color is the square in this image? Reply with only the color.', 'square.png'), [['contains', 'red']], 'red'),
        (chat('What color is the triangle in this image? Reply with only the color.', 'shapes.png'), [['contains', 'green']], 'green'),
        (chat('What color is the square nearest the right edge of this image? Reply with only the color.', 'scene.png'),
         [['contains', 'orange']], 'orange'))),
    ('count', (
        (chat('How many shapes are in this image? Reply with only the number.', 'square.png'), [['last_number', 1]], '1'),
        (chat('How many colored shapes are in this image? Reply with only the number.', 'shapes.png'), [['last_number', 3]], '3'),
        (chat('How many circles are in this image? Reply with only the number.', 'scene.png'), [['last_number', 4]], '4'))),
    ('read', (
        (chat('What word is written in this image? Reply with only the word.', 'shapes.png'), [['contains', 'hello']], 'HELLO'),
        (chat('What code is written in small text in this image? Reply with only the code.', 'scene.png'),
         [['contains', 'a7x92']], 'A7X92'),
        (chat('Reply with exactly the code written in small text in this image, and nothing else.', 'scene.png'),
         [['exact_folded', 'A7X92']], 'A7X92'))),
))

EMBED = ('hugpy-embed-v1', 'feature-extraction', '/v1/embeddings', (
    ('similarity', (
        (dict(input=['A dog runs across the park.', 'A canine sprints through the park.',
                     'The quarterly budget report is due on Friday.']), [['nearer', 0.05]],
         'the first sentence nearer the second (its paraphrase) than the third'),
        (dict(input=['The company reported strong earnings this quarter.', 'The firm posted solid profits for the period.',
                     'A hummingbird can beat its wings fifty times a second.']), [['nearer', 0]],
         'the first sentence nearer the second (its paraphrase) than the third'),
        (dict(input=['The central bank raised interest rates to curb inflation.',
                     'Policymakers lifted borrowing costs to slow rising prices.',
                     "The museum's new wing features Impressionist paintings."]), [['nearer', 0]],
         'the first sentence nearer the second (its paraphrase) than the third'))),
))

_CURIE = 'Marie Curie was born in Warsaw in 1867. She won the Nobel Prize in Physics in 1903.'
_EARHART = ('Amelia Earhart flew solo across the Atlantic in 1932, departing from Harbour Grace in Newfoundland. The '
            'flight covered about 2026 miles and lasted roughly 15 hours before she landed in Northern Ireland.')
_APOLLO = ('In 1969 the Apollo 11 mission carried three astronauts: Neil Armstrong, Buzz Aldrin, and Michael Collins. '
           'Armstrong and Aldrin landed in the Sea of Tranquility on July 20, while Collins remained in orbit 60 miles '
           'above the surface. The crew returned to Earth on July 24, splashing down in the Pacific Ocean after a '
           'journey of about 953000 miles.')
SUMMARY = ('hugpy-summary-v1', 'summarization', '/v1/summarize', (
    ('facts', (
        (dict(input=_CURIE), [['contains_some', dict(of=['Curie', 'Warsaw', 'Nobel', 'Physics', '1903'], count=3)]],
         'a summary naming Curie, Warsaw and the Nobel Prize'),
        (dict(input=_EARHART), [['shorter_than', len(_EARHART)],
                                ['contains_some', dict(of=['Earhart', 'Atlantic', '1932', 'solo', 'flight'], count=3)]],
         'a shorter text naming Earhart, the Atlantic and 1932'),
        (dict(input=_APOLLO), [['shorter_than', len(_APOLLO)],
                               ['contains_some', dict(of=['Apollo', 'Armstrong', 'Aldrin', 'Collins', '1969', 'Tranquility'], count=4)]],
         'a shorter text naming Apollo, its crew and 1969'))),
))

_APPLE = 'a single red apple on a plain white background, centered'
IMAGE = ('hugpy-imagegen-v1', 'text-to-image', '/v1/images/generations', (
    ('render', (
        (dict(prompt=_APPLE, width=512, height=512, steps=8, seed=1),
         [['artifact', dict(kind='image', width=512, height=512)]], 'an image of 512x512'),
        (dict(prompt=_APPLE, width=768, height=512, steps=12, seed=1),
         [['artifact', dict(kind='image', width=768, height=512)]], 'an image of 768x512'),
        (dict(prompt=_APPLE, width=1024, height=1024, steps=20, seed=1),
         [['artifact', dict(kind='image', width=1024, height=1024)]], 'an image of 1024x1024'))),
))

SPEECH = ('hugpy-speech-v1', 'text-to-speech', '/v1/audio/speech', (
    ('speak', (
        (dict(input='Hello there.'), [['artifact', dict(kind='audio', min_duration_s=0.3)]], 'speech of at least 0.3 s'),
        (dict(input='The quick brown fox jumps over the lazy dog.'),
         [['artifact', dict(kind='audio', min_duration_s=1.0)]], 'speech of at least 1 s'),
        (dict(input='The quick brown fox jumps over the lazy dog. Then it runs across the field, past the old barn, '
                    'and down to the river where the water is cold and clear.'),
         [['artifact', dict(kind='audio', min_duration_s=4.0)]], 'speech of at least 4 s'))),
))

VIDEO = ('hugpy-videogen-v1', 'text-to-video', '/v1/videos/generations', (
    ('render', (
        (dict(prompt='a red ball rolling from left to right across a white floor', seed=1),
         [['artifact', dict(kind='video', min_frames=8)]], 'a clip of at least 8 frames'),)),
))

# disc.mp4: 48 frames of a red disc crossing a white field, 320x240 at 24 a second
INTERP = ('hugpy-interp-v1', 'video-interpolation', '/v1/videos/interpolate', (
    ('smooth', (
        (dict(video_b64=media('disc.mp4')), [['artifact', dict(kind='video', min_frames=49)]],
         'the clip with frames added: more than its 48'),)),
))

SUITES = (TEXT, VISION, EMBED, SUMMARY, IMAGE, SPEECH, VIDEO, INTERP)
# the files a call may be given when its wrapper says the model needs one the query does not carry (an image to
# animate, a clip to restyle): {the kind of input: (the file, how it is written into a field named *_b64)}
SUPPLIES = {'image': 'square.png', 'video': 'disc.mp4'}
COLUMNS = ('id', 'suite', 'task', 'engine', 'category', 'tier', 'position', 'endpoint', 'body', 'checks', 'answer')


def defaults() -> list:
    """The rows of the grading table as this file defines them. A query's id is its suite's short name, its
    category and its tier: text-math-easy."""
    rows = []
    for suite, task, endpoint, categories in SUITES:
        short = suite.split('-')[1]
        short = 'text' if short == 'native' else short
        for position, (category, tiers) in enumerate(categories):
            for tier, (body, checks, answer) in enumerate(tiers, 1):
                rows.append(dict(id=f'{short}-{category}-{TIER_NAMES[tier - 1]}', suite=suite, task=task, engine=None,
                                 category=category, tier=tier, position=position, endpoint=endpoint,
                                 body=json.dumps(body, sort_keys=True), checks=json.dumps(checks), answer=answer))
    return rows


def seed(conn) -> None:
    """Write the table's own rows as this file defines them: a row nobody changed follows this file (one this file
    no longer has is taken out); a row the operator changed or added is left as it is. The caller commits."""
    rows = defaults()
    conn.executemany(
        f"INSERT INTO grading_queries ({', '.join(COLUMNS)}) VALUES ({', '.join(':' + name for name in COLUMNS)}) "
        "ON CONFLICT(id) DO UPDATE SET " + ', '.join(f'{name} = excluded.{name}' for name in COLUMNS[1:])
        + " WHERE grading_queries.changed_at IS NULL", rows)
    conn.execute(f"DELETE FROM grading_queries WHERE changed_at IS NULL AND id NOT IN ({', '.join('?' * len(rows))})",
                 [row['id'] for row in rows])


def supply(needs: list, body: dict) -> dict:
    """``body`` with what a wrapper said the call lacks (its refusal's ``needs``: each a kind of input and the
    fields that take it), where media/ has a file of that kind. None when something it needs is not there to give."""
    out = dict(body)
    for need in needs or ():
        fields = [field for field in need.get('fields') or () if isinstance(field, str)]
        field = next((name for name in fields if name.endswith('_b64')), None)
        if need.get('kind') not in SUPPLIES or field is None:
            return None
        out[field] = media(SUPPLIES[need['kind']])
    return out


__all__ = ['defaults', 'media', 'seed', 'supply', 'SUITES']
