from typing import List, Literal, Optional, Protocol, Type, TypedDict, Union

TagName = Literal[
    "a",
    "abbr",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "bdi",
    "bdo",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "cite",
    "code",
    "col",
    "colgroup",
    "data",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "dialog",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "head",
    "header",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hgroup",
    "hr",
    "html",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "keygen",
    "label",
    "legend",
    "li",
    "link",
    "main",
    "map",
    "mark",
    "menu",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "param",
    "picture",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "search",
    "section",
    "select",
    "slot",
    "small",
    "source",
    "span",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "template",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
]

AttributeValue = Union[str, int]
NumericAttribute = Union[int, str]
AreaShape = Literal["circle", "default", "poly", "rect"]
ContentEditable = Union[bool, Literal["true", "false", "plaintext-only"]]
CrossOrigin = Literal["anonymous", "use-credentials"]
Decoding = Literal["async", "auto", "sync"]
Draggable = Union[bool, Literal["true", "false", "auto"]]
FetchPriority = Literal["high", "low", "auto"]
FormEncoding = Literal[
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain",
]
FormMethod = Literal["get", "post", "dialog"]
Loading = Literal["eager", "lazy"]
Preload = Literal["none", "metadata", "auto"]
ReferrerPolicy = Literal[
    "no-referrer",
    "no-referrer-when-downgrade",
    "origin",
    "origin-when-cross-origin",
    "same-origin",
    "strict-origin",
    "strict-origin-when-cross-origin",
    "unsafe-url",
]
Spellcheck = Union[bool, Literal["true", "false"]]
TableScope = Literal["col", "colgroup", "row", "rowgroup"]
TextDirection = Literal["ltr", "rtl", "auto"]
TextWrap = Literal["hard", "soft"]
TrackKind = Literal["subtitles", "captions", "descriptions", "chapters", "metadata"]
Translate = Literal["yes", "no"]


class HTMLAttributes(TypedDict, total=False):
    abbr: str
    accept: str
    accept_charset: str
    accesskey: str
    action: str
    align: str
    allow: str
    allowfullscreen: str
    alt: str
    as_: str
    async_: str
    autocapitalize: str
    autocomplete: str
    autofocus: str
    autoplay: str
    blocking: str
    border: str
    cellpadding: str
    cellspacing: str
    charset: str
    checked: str
    cite: str
    class_: str
    closedby: str
    cols: NumericAttribute
    colspan: NumericAttribute
    command: str
    commandfor: str
    content: str
    contenteditable: ContentEditable
    controls: str
    coords: str
    crossorigin: CrossOrigin
    csp: str
    data: str
    datetime: str
    decoding: Decoding
    default: str
    defer: str
    dir: TextDirection
    dirname: str
    disabled: str
    download: str
    draggable: Draggable
    enctype: FormEncoding
    enterkeyhint: str
    fetchpriority: FetchPriority
    fill_opacity: str
    for_: str
    form: str
    formaction: str
    formenctype: str
    formmethod: str
    formnovalidate: str
    formtarget: str
    frame: str
    headers: str
    height: NumericAttribute
    hidden: str
    high: str
    href: str
    hreflang: str
    http_equiv: str
    id: str
    imagesizes: str
    imagesrcset: str
    inert: str
    integrity: str
    is_: str
    ismap: str
    itemid: str
    itemprop: str
    itemref: str
    itemscope: str
    itemtype: str
    kind: TrackKind
    klass: str
    label: str
    lang: str
    language: str
    list: str
    loading: Loading
    loop: str
    low: str
    manifest: str
    max: str
    maxlength: NumericAttribute
    media: str
    method: FormMethod
    min: str
    minlength: NumericAttribute
    multiple: str
    muted: str
    name: str
    nomodule: str
    nonce: str
    novalidate: str
    open: str
    optimum: str
    part: str
    pattern: str
    ping: str
    placeholder: str
    playsinline: str
    popover: str
    popovertarget: str
    popovertargetaction: str
    poster: str
    preload: Preload
    readonly: str
    referrerpolicy: ReferrerPolicy
    rel: str
    required: str
    reversed: str
    role: str
    rows: NumericAttribute
    rowspan: NumericAttribute
    rules: str
    sandbox: str
    scope: TableScope
    selected: str
    shape: AreaShape
    size: NumericAttribute
    sizes: str
    slot: str
    span: NumericAttribute
    spellcheck: Spellcheck
    src: str
    srcdoc: str
    srclang: str
    srcset: str
    start: NumericAttribute
    step: str
    stroke_dasharray: str
    stroke_dashoffset: str
    stroke_linecap: str
    stroke_linejoin: str
    stroke_miterlimit: str
    stroke_opacity: str
    stroke_width: str
    style: str
    summary: str
    tabindex: NumericAttribute
    target: str
    title: str
    translate: Translate
    type: str
    usemap: str
    value: str
    width: NumericAttribute
    wrap: TextWrap


class TagProtocol(Protocol):
    tag_name: str

    def __init__(self, *content: str, _t: Optional[str] = None, **attributes: AttributeValue) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...
    def __getattr__(self, tag_name: str) -> Type["TagProtocol"]: ...


STANDARD_TAG_NAMES: List[TagName] = [
    "a",
    "abbr",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "bdi",
    "bdo",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "cite",
    "code",
    "col",
    "colgroup",
    "data",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "dialog",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "head",
    "header",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hgroup",
    "hr",
    "html",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "keygen",
    "label",
    "legend",
    "li",
    "link",
    "main",
    "map",
    "mark",
    "menu",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "param",
    "picture",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "search",
    "section",
    "select",
    "slot",
    "small",
    "source",
    "span",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "template",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
]
