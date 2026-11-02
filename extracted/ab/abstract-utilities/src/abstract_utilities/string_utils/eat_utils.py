from .imports import (
    imports,
    shlex,
    os,
    shutil,
    uuid,
    get_args,
    Path,
    load_dotenv,
    jsonify,
    secure_filename,
    make_list,
    get_alpha_ints,
    quoteIt,
    truncate_text,
    capitalize,
    get_from_kwargs,
    get_lines,
    clean_spaces,
    eatInner,
    eatOuter,
    eatAll,
)
def eatElse(
    stringObj,
    chars=None,
    ints=True,
    alpha=True,
    lower=True,
    capitalize=True,
    string=True,
    listObj=True
):
    alpha_ints = get_alpha_ints(
        ints=True,
        alpha=True,
        lower=True,
        capitalize=True,
        string=True,
        listObj=True
        )
    chars = make_list(chars or [])+alpha_ints

    while True:
        if stringObj:
            str_0 = stringObj[0] not in chars
            str_1 = stringObj[-1] not in chars
            str_eat = str_0 or str_1
            if not str_eat:
                return stringObj
            if stringObj and str_0:
                stringObj = stringObj[1:] if len(stringObj) !=1 else ""
            if stringObj and str_1:
                stringObj = stringObj[:-1] if len(stringObj) !=1 else ""   
        else:
            return stringObj
