from .model import Blank, Boolean, Boundary, Call, Concat, Entry, Indeterminate, nullmonitor, Number, Suffix, Text
from decimal import Decimal
import re

class ParseException(Exception): pass

booleans = {t: Boolean(b).augment(textvalue = t) for b in map(bool, range(2)) for t in [str(b).lower()]}
brackets = {x: y for pair in ['()', '[]'] for x, y in [pair, reversed(pair)]}
dollar = re.compile('[$]')
dollarorbracket = re.compile(r'[$()[\]]')
dollarorbracketorws = re.compile(r'[$()[\]\s]')
dollaroropenorws = re.compile(r'([$([])|\s')
eolornotws = re.compile(r'(\r\n|[\r\n])|\S')
notws = re.compile(r'\S')
numbermatch = re.compile('-?(?:[0-9]+(?:[.][0-9]*)?|[.][0-9]+)').fullmatch

def _scalar(text):
    try:
        return booleans[text]
    except KeyError:
        m = numbermatch(text)
    if m is None:
        return Text(text)
    if '.' in text:
        val = Decimal(text)
    else:
        val = int(text)
        if not val and '-' == text[0]:
            val = Decimal(text) # Preserve sign.
    return Number(val).augment(textvalue = text)

class Parser:

    def __init__(self, monitor):
        self.monitor = monitor

    def _join(self, parts):
        n = len(parts)
        if 0 == n:
            return Indeterminate
        if 1 == n:
            return parts[0]
        return Concat(parts, self.monitor)

    def _templateparts(self, text):
        eye = 0
        parts = []
        while eye < len(text):
            m = dollar.search(text, eye)
            if m is None:
                parts.append(Text(text[eye:]))
                break
            fence = m.start()
            if eye < fence:
                parts.append(Text(text[eye:fence]))
            call, eye = self._readcall(text, fence)
            parts.append(call)
        return parts

    def readtemplate(self, text):
        return self._join(self._templateparts(text))

    def readparts(self, text):
        eye = 0
        parts = []
        while eye < len(text):
            m = eolornotws.search(text, eye)
            if m is None:
                parts.append(Blank(text[eye:]))
                break
            fence = m.start()
            if eye < fence:
                parts.append(Blank(text[eye:fence]))
            if m.group(1) is None:
                chunk, eye = self._readchunk(text, fence, None)
                parts.append(chunk)
            else:
                parts.append(Boundary)
                eye = m.end()
        return parts

    def readsuffix(self, text):
        return Suffix(Entry(self.readparts(text)))

    def _readcall(self, text, eye):
        eye += 1
        names = []
        while True:
            m = dollaroropenorws.search(text, eye)
            openchar = m.group(1)
            if openchar is None:
                raise ParseException
            names.append(text[eye:m.start()])
            eye = m.end()
            if '$' != openchar:
                break
        k = len(names) - 1
        if '.' == names[k]:
            args, eye = self._readspan(text, eye, False, openchar)
            call = Text('') if not args else Concat(args, self.monitor)
        elif "'" == names[k]:
            args, eye = self._readspan(text, eye, True, openchar)
            call = Text('') if not args else args[0] if 1 == len(args) else Concat(args, self.monitor)
        else:
            args, eye = self._readargs(text, eye, openchar)
            call = Call(names[k], args)
        while k:
            k -= 1
            if '.' != names[k]:
                call = Call(names[k], [call])
        return call, eye + 1

    def _readargs(self, text, eye, openchar):
        closechar = brackets[openchar]
        args = []
        while True:
            m = notws.search(text, eye)
            c = m.group()
            eye = m.start()
            if closechar == c:
                break
            chunk, eye = self._readchunk(text, eye, openchar)
            args.append(chunk)
        return args, eye

    def _readspan(self, text, eye, literal, openchar):
        closechar = brackets[openchar]
        mark = eye
        parts = []
        depth = 0
        while True:
            m = dollarorbracket.search(text, eye)
            if m is None:
                raise ParseException
            c = m.group()
            if '$' == c:
                if literal:
                    eye = m.end()
                else:
                    fence = m.start()
                    if mark < fence:
                        parts.append(Text(text[mark:fence]))
                    call, eye = self._readcall(text, fence)
                    parts.append(call)
                    mark = eye
                continue
            if closechar == c:
                if depth:
                    depth -= 1
                    eye = m.end()
                    continue
                fence = m.start()
                if mark < fence:
                    parts.append(Text(text[mark:fence]))
                mark = eye = fence
                break
            if openchar == c:
                depth += 1
                eye = m.end()
                continue
            eye = m.end()
        return parts, eye

    def _readchunk(self, text, eye, openchar):
        closechar = brackets.get(openchar)
        mark = eye
        parts = []
        depth = 0
        while True:
            if eye == len(text):
                if mark < eye:
                    parts.append(_scalar(text[mark:eye]))
                break
            m = dollarorbracketorws.search(text, eye)
            if m is None:
                parts.append(_scalar(text[mark:]))
                mark = eye = len(text)
                break
            c = m.group()
            if '$' == c:
                fence = m.start()
                if mark < fence:
                    parts.append(Text(text[mark:fence]))
                call, eye = self._readcall(text, fence)
                parts.append(call)
                mark = eye
                continue
            if closechar == c:
                if depth:
                    depth -= 1
                    eye = m.end()
                    continue
                fence = m.start()
                if mark < fence:
                    parts.append(_scalar(text[mark:fence]))
                mark = eye = fence
                break
            if openchar == c:
                depth += 1
                eye = m.end()
                continue
            if c not in brackets:
                fence = m.start()
                if mark < fence:
                    parts.append(_scalar(text[mark:fence]))
                mark = eye = fence
                break
            eye = m.end()
        return self._join(parts), eye

staticparser = Parser(nullmonitor)
