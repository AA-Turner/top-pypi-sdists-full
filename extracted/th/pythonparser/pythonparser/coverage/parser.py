# encoding:utf-8

"""
The :mod:`parser` module concerns itself with parsing Python source.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from functools import reduce
from .. import source, diagnostic, lexer, ast

# A few notes about our approach to parsing:
#
# Python uses an LL(1) parser generator. It's a bit weird, because
# the usual reason to choose LL(1) is to make a handwritten parser
# possible, however Python's grammar is formulated in a way that
# is much more easily recognized if you make an FSM rather than
# the usual "if accept(token)..." ladder. So in a way it is
# the worst of both worlds.
#
# We don't use a parser generator because we want to have an unified
# grammar for all Python versions, and also have grammar coverage
# analysis and nice error recovery. To make the grammar compact,
# we use combinators to compose it from predefined fragments,
# such as "sequence" or "alternation" or "Kleene star". This easily
# gives us one token of lookahead in most cases, but e.g. not
# in the following one:
#
#     argument: test | test '=' test
#
# There are two issues with this. First, in an alternation, the first
# variant will be tried (and accepted) earlier. Second, if we reverse
# them, by the point it is clear ``'='`` will not be accepted, ``test``
# has already been consumed.
#
# The way we fix this is by reordering rules so that longest match
# comes first, and adding backtracking on alternations (as well as
# plus and star, since those have a hidden alternation inside).
#
# While backtracking can in principle make asymptotical complexity
# worse, it never makes parsing syntactically correct code supralinear
# with Python's LL(1) grammar, and we could not come up with any
# pathological incorrect input as well.

# Coverage data
_all_rules = []
_all_stmts = {(12480,12483): False, (12795,12798): False, (12844,12847): False, (12960,12962): False, (13126,13130): False, (13262,13266): False, (13381,13384): False, (13434,13436): False, (13589,13592): False, (13631,13633): False, (13816,13819): False, (13858,13860): False, (13902,13904): False, (14049,14053): False, (14964,14968): False, (15042,15044): False, (15140,15144): False, (15646,15648): False, (16103,16107): False, (16545,16547): False, (16637,16641): False, (16863,16866): False, (17146,17148): False, (17193,17195): False, (17248,17250): False, (17307,17309): False, (17368,17370): False, (17429,17431): False, (17945,17948): False, (18029,18031): False, (18223,18226): False, (18393,18396): False, (18459,18461): False, (18630,18634): False, (18668,18671): False, (18722,18724): False, (18906,18910): False, (19121,19125): False, (19139,19141): False, (19288,19292): False, (19475,19478): False, (19511,19513): False, (19751,19754): False, (19882,19884): False, (20060,20063): False, (20217,20219): False, (20394,20397): False, (20752,20755): False, (21006,21009): False, (21355,21357): False, (21668,21671): False, (22105,22108): False, (22758,22761): False, (22955,22957): False, (23788,23791): False, (24092,24095): False, (24278,24280): False, (24599,24602): False, (24900,24903): False, (25172,25175): False, (25220,25222): False, (25396,25400): False, (25736,25739): False, (25785,25787): False, (25915,25919): False, (25964,25966): False, (26071,26075): False, (26208,26211): False, (26602,26605): False, (26772,26775): False, (27146,27149): False, (27350,27352): False, (27589,27592): False, (27641,27643): False, (27829,27833): False, (27934,27936): False, (28019,28023): False, (28478,28481): False, (28546,28548): False, (28793,28797): False, (29069,29072): False, (29123,29126): False, (29175,29177): False, (29367,29371): False, (29731,29734): False, (29784,29786): False, (29926,29930): False, (29983,29985): False, (30098,30102): False, (31561,31564): False, (31659,31661): False, (31938,31941): False, (33111,33114): False, (33298,33301): False, (33334,33336): False, (33522,33526): False, (33626,33629): False, (33997,33999): False, (34044,34046): False, (34340,34344): False, (34493,34497): False, (34671,34675): False, (35530,35533): False, (35609,35611): False, (35894,35897): False, (36000,36002): False, (36216,36219): False, (36434,36437): False, (36683,36685): False, (36745,36749): False, (36893,36896): False, (37309,37312): False, (37696,37699): False, (37857,37860): False, (38056,38059): False, (38175,38177): False, (38359,38362): False, (38690,38693): False, (38879,38881): False, (38981,38983): False, (39093,39095): False, (39390,39393): False, (39568,39570): False, (39665,39667): False, (40087,40090): False, (40333,40336): False, (40414,40417): False, (40550,40553): False, (40641,40643): False, (40877,40880): False, (41084,41087): False, (41351,41354): False, (41677,41680): False, (42291,42293): False, (42457,42459): False, (42520,42522): False, (42979,42982): False, (43159,43161): False, (43569,43572): False, (43818,43820): False, (44492,44495): False, (44760,44763): False, (45243,45246): False, (45456,45458): False, (45524,45526): False, (45590,45594): False, (45857,45860): False, (46292,46295): False, (46438,46440): False, (46787,46790): False, (47198,47201): False, (47455,47457): False, (47548,47551): False, (47732,47734): False, (48097,48099): False, (48330,48333): False, (48737,48739): False, (49086,49089): False, (49549,49551): False, (49924,49927): False, (50008,50011): False, (50293,50295): False, (50471,50473): False, (50953,50956): False, (51375,51378): False, (51922,51925): False, (52072,52074): False, (52309,52313): False, (52832,52835): False, (53216,53219): False, (53316,53318): False, (53549,53553): False, (53753,53756): False, (53879,53882): False, (54089,54092): False, (54368,54370): False, (54468,54470): False, (54552,54554): False, (54667,54671): False, (55021,55024): False, (55673,55676): False, (55817,55819): False, (56291,56294): False, (56331,56333): False, (56811,56814): False, (56884,56886): False, (57643,57646): False, (57729,57731): False, (58008,58012): False, (58118,58121): False, (58207,58209): False, (58487,58491): False, (58578,58581): False, (59077,59080): False, (59303,59305): False, (59545,59549): False, (59625,59628): False, (59721,59723): False, (59932,59935): False, (61633,61636): False, (61957,61960): False, (62059,62062): False, (62096,62098): False, (62222,62226): False, (62382,62384): False, (62631,62634): False, (62732,62735): False, (62880,62883): False, (63022,63025): False, (63271,63274): False, (64650,64653): False, (64772,64775): False, (64803,64805): False, (64859,64863): False, (64917,64921): False, (65878,65881): False, (65923,65925): False, (65976,65980): False, (66109,66113): False, (66266,66269): False, (66432,66435): False, (66836,66839): False, (67021,67024): False, (67062,67064): False, (67137,67141): False, (67611,67614): False, (67798,67801): False, (68162,68165): False, (68730,68733): False, (68837,68839): False, (68944,68948): False, (69381,69385): False, (69645,69648): False, (69852,69855): False, (69950,69952): False, (70014,70016): False, (70115,70117): False, (70227,70229): False, (70470,70473): False, (71134,71137): False, (71467,71470): False, (71666,71669): False, (72217,72220): False, (72266,72268): False, (72584,72588): False, (72947,72950): False, (72996,72998): False, (73118,73122): False, (73666,73669): False, (73881,73883): False, (74595,74598): False, (74913,74915): False, (75851,75854): False, (75953,75955): False, (76020,76023): False, (76057,76059): False, (76569,76572): False, (77076,77079): False, (77116,77118): False, (77189,77193): False, (77374,77377): False, (77598,77601): False, (77627,77629): False, (77714,77718): False, (77980,77984): False, (78090,78093): False, (78137,78140): False, (78165,78167): False, (78619,78622): False, (78662,78665): False, (78690,78692): False, (79080,79083): False, (79486,79489): False, (79567,79570): False, (79821,79823): False, (79894,79898): False, (79966,79969): False, (80029,80032): False, (80247,80249): False, (80320,80324): False, (81857,81860): False, (81980,81982): False, (82133,82137): False, (82305,82308): False, (82408,82410): False, (82562,82566): False, (82711,82715): False, (82872,82875): False}

# Generic LL parsing combinators
class Unmatched:
    pass

unmatched = Unmatched()

def llrule(loc, expected, cases=1):
    if loc is None:
        def decorator(rule):
            rule.expected = expected
            return rule
    else:
        def decorator(inner_rule):
            if cases == 1:
                def rule(*args, **kwargs):
                    result = inner_rule(*args, **kwargs)
                    if result is not unmatched:
                        rule.covered[0] = True
                    return result
            else:
                rule = inner_rule

            rule.loc, rule.expected, rule.covered = \
                loc, expected, [False] * cases
            _all_rules.append(rule)

            return rule
    return decorator

def action(inner_rule, loc=None):
    """
    A decorator returning a function that first runs ``inner_rule`` and then, if its
    return value is not None, maps that value using ``mapper``.

    If the value being mapped is a tuple, it is expanded into multiple arguments.

    Similar to attaching semantic actions to rules in traditional parser generators.
    """
    def decorator(mapper):
        @llrule(loc, inner_rule.expected)
        def outer_rule(parser):
            result = inner_rule(parser)
            if result is unmatched:
                return result
            if isinstance(result, tuple):
                return mapper(parser, *result)
            else:
                return mapper(parser, result)
        return outer_rule
    return decorator

def Eps(value=None, loc=None):
    """A rule that accepts no tokens (epsilon) and returns ``value``."""
    @llrule(loc, lambda parser: [])
    def rule(parser):
        return value
    return rule

def Tok(kind, loc=None):
    """A rule that accepts a token of kind ``kind`` and returns it, or returns None."""
    @llrule(loc, lambda parser: [kind])
    def rule(parser):
        return parser._accept(kind)
    return rule

def Loc(kind, loc=None):
    """A rule that accepts a token of kind ``kind`` and returns its location, or returns None."""
    @llrule(loc, lambda parser: [kind])
    def rule(parser):
        result = parser._accept(kind)
        if result is unmatched:
            return result
        return result.loc
    return rule

def Rule(name, loc=None):
    """A proxy for a rule called ``name`` which may not be yet defined."""
    @llrule(loc, lambda parser: getattr(parser, name).expected(parser))
    def rule(parser):
        return getattr(parser, name)()
    return rule

def Expect(inner_rule, loc=None):
    """A rule that executes ``inner_rule`` and emits a diagnostic error if it returns None."""
    @llrule(loc, inner_rule.expected)
    def rule(parser):
        result = inner_rule(parser)
        if result is unmatched:
            expected = reduce(list.__add__, [rule.expected(parser) for rule in parser._errrules])
            expected = list(sorted(set(expected)))

            if len(expected) > 1:
                expected = " or ".join([", ".join(expected[0:-1]), expected[-1]])
            elif len(expected) == 1:
                expected = expected[0]
            else:
                expected = "(impossible)"

            error_tok = parser._tokens[parser._errindex]
            error = diagnostic.Diagnostic(
                "fatal", "unexpected {actual}: expected {expected}",
                {"actual": error_tok.kind, "expected": expected},
                error_tok.loc)
            parser.diagnostic_engine.process(error)
        return result
    return rule

def Seq(first_rule, *rest_of_rules, **kwargs):
    """
    A rule that accepts a sequence of tokens satisfying ``rules`` and returns a tuple
    containing their return values, or None if the first rule was not satisfied.
    """
    @llrule(kwargs.get("loc", None), first_rule.expected)
    def rule(parser):
        result = first_rule(parser)
        if result is unmatched:
            return result

        results = [result]
        for rule in rest_of_rules:
            result = rule(parser)
            if result is unmatched:
                return result
            results.append(result)
        return tuple(results)
    return rule

def SeqN(n, *inner_rules, **kwargs):
    """
    A rule that accepts a sequence of tokens satisfying ``rules`` and returns
    the value returned by rule number ``n``, or None if the first rule was not satisfied.
    """
    @action(Seq(*inner_rules), loc=kwargs.get("loc", None))
    def rule(parser, *values):
        return values[n]
    return rule

def Alt(*inner_rules, **kwargs):
    """
    A rule that expects a sequence of tokens satisfying one of ``rules`` in sequence
    (a rule is satisfied when it returns anything but None) and returns the return
    value of that rule, or None if no rules were satisfied.
    """
    loc = kwargs.get("loc", None)
    expected = lambda parser: reduce(list.__add__, map(lambda x: x.expected(parser), inner_rules))
    if loc is not None:
        @llrule(loc, expected, cases=len(inner_rules))
        def rule(parser):
            data = parser._save()
            for idx, inner_rule in enumerate(inner_rules):
                result = inner_rule(parser)
                if result is unmatched:
                    parser._restore(data, rule=inner_rule)
                else:
                    rule.covered[idx] = True
                    return result
            return unmatched
    else:
        @llrule(loc, expected, cases=len(inner_rules))
        def rule(parser):
            data = parser._save()
            for inner_rule in inner_rules:
                result = inner_rule(parser)
                if result is unmatched:
                    parser._restore(data, rule=inner_rule)
                else:
                    return result
            return unmatched
    return rule

def Opt(inner_rule, loc=None):
    """Shorthand for ``Alt(inner_rule, Eps())``"""
    return Alt(inner_rule, Eps(), loc=loc)

def Star(inner_rule, loc=None):
    """
    A rule that accepts a sequence of tokens satisfying ``inner_rule`` zero or more times,
    and returns the returned values in a :class:`list`.
    """
    @llrule(loc, lambda parser: [])
    def rule(parser):
        results = []
        while True:
            data = parser._save()
            result = inner_rule(parser)
            if result is unmatched:
                parser._restore(data, rule=inner_rule)
                return results
            results.append(result)
    return rule

def Plus(inner_rule, loc=None):
    """
    A rule that accepts a sequence of tokens satisfying ``inner_rule`` one or more times,
    and returns the returned values in a :class:`list`.
    """
    @llrule(loc, inner_rule.expected)
    def rule(parser):
        result = inner_rule(parser)
        if result is unmatched:
            return result

        results = [result]
        while True:
            data = parser._save()
            result = inner_rule(parser)
            if result is unmatched:
                parser._restore(data, rule=inner_rule)
                return results
            results.append(result)
    return rule

class commalist(list):
    __slots__ = ("trailing_comma",)

def List(inner_rule, separator_tok, trailing, leading=True, loc=None):
    if not trailing:
        @action(Seq(inner_rule, Star(SeqN(1, Tok(separator_tok), inner_rule))), loc=loc)
        def outer_rule(parser, first, rest):
            return [first] + rest
        return outer_rule
    else:
        # A rule like this: stmt (';' stmt)* [';']
        # This doesn't yield itself to combinators above, because disambiguating
        # another iteration of the Kleene star and the trailing separator
        # requires two lookahead tokens (naively).
        separator_rule = Tok(separator_tok)
        @llrule(loc, inner_rule.expected)
        def rule(parser):
            results = commalist()

            if leading:
                result = inner_rule(parser)
                if result is unmatched:
                    return result
                else:
                    results.append(result)

            while True:
                result = separator_rule(parser)
                if result is unmatched:
                    results.trailing_comma = None
                    return results

                result_1 = inner_rule(parser)
                if result_1 is unmatched:
                    results.trailing_comma = result
                    return results
                else:
                    results.append(result_1)
        return rule

# Python AST specific parser combinators
def Newline(loc=None):
    """A rule that accepts token of kind ``newline`` and returns an empty list."""
    @llrule(loc, lambda parser: ["newline"])
    def rule(parser):
        result = parser._accept("newline")
        if result is unmatched:
            return result
        return []
    return rule

def Oper(klass, *kinds, **kwargs):
    """
    A rule that accepts a sequence of tokens of kinds ``kinds`` and returns
    an instance of ``klass`` with ``loc`` encompassing the entire sequence
    or None if the first token is not of ``kinds[0]``.
    """
    @action(Seq(*map(Loc, kinds)), loc=kwargs.get("loc", None))
    def rule(parser, *tokens):
        return klass(loc=tokens[0].join(tokens[-1]))
    return rule

def BinOper(expr_rulename, op_rule, node=ast.BinOp, loc=None):
    @action(Seq(Rule(expr_rulename), Star(Seq(op_rule, Rule(expr_rulename)))), loc=loc)
    def rule(parser, lhs, trailers):
        for (op, rhs) in trailers:
            lhs = node(left=lhs, op=op, right=rhs,
                       loc=lhs.loc.join(rhs.loc))
        return lhs
    return rule

def BeginEnd(begin_tok, inner_rule, end_tok, empty=None, loc=None):
    @action(Seq(Loc(begin_tok), inner_rule, Loc(end_tok)), loc=loc)
    def rule(parser, begin_loc, node, end_loc):
        if node is None:
            node = empty(parser)

        # Collection nodes don't have loc yet. If a node has loc at this
        # point, it means it's an expression passed in parentheses.
        if node.loc is None and type(node) in [
                ast.List, ast.ListComp,
                ast.Dict, ast.DictComp,
                ast.Set, ast.SetComp,
                ast.GeneratorExp,
                ast.Tuple, ast.Repr,
                ast.Call, ast.Subscript,
                ast.arguments]:
            node.begin_loc, node.end_loc, node.loc = \
                begin_loc, end_loc, begin_loc.join(end_loc)
        return node
    return rule

class Parser:

    # Generic LL parsing methods
    def __init__(self, lexer, version, diagnostic_engine):
        _all_stmts[(12480,12483)] = True
        self._init_version(version)
        self.diagnostic_engine = diagnostic_engine

        self.lexer     = lexer
        self._tokens   = []
        self._index    = -1
        self._errindex = -1
        self._errrules = []
        self._advance()

    def _save(self):
        _all_stmts[(12795,12798)] = True
        return self._index

    def _restore(self, data, rule):
        _all_stmts[(12844,12847)] = True
        self._index = data
        self._token = self._tokens[self._index]

        if self._index > self._errindex:
            # We have advanced since last error
            _all_stmts[(12960,12962)] = True
            self._errindex = self._index
            self._errrules = [rule]
        elif self._index == self._errindex:
            # We're at the same place as last error
            _all_stmts[(13126,13130)] = True
            self._errrules.append(rule)
        else:
            # We've backtracked far and are now just failing the
            # whole parse
            _all_stmts[(13262,13266)] = True
            pass

    def _advance(self):
        _all_stmts[(13381,13384)] = True
        self._index += 1
        if self._index == len(self._tokens):
            _all_stmts[(13434,13436)] = True
            self._tokens.append(self.lexer.next(eof_token=True))
        self._token = self._tokens[self._index]

    def _accept(self, expected_kind):
        _all_stmts[(13589,13592)] = True
        if self._token.kind == expected_kind:
            _all_stmts[(13631,13633)] = True
            result = self._token
            self._advance()
            return result
        return unmatched

    # Python-specific methods
    def _init_version(self, version):
        _all_stmts[(13816,13819)] = True
        if version in ((2, 6), (2, 7)):
            _all_stmts[(13858,13860)] = True
            if version == (2, 6):
                _all_stmts[(13902,13904)] = True
                self.with_stmt       = self.with_stmt__26
                self.atom_6          = self.atom_6__26
            else:
                _all_stmts[(14049,14053)] = True
                self.with_stmt       = self.with_stmt__27
                self.atom_6          = self.atom_6__27
            self.except_clause_1 = self.except_clause_1__26
            self.classdef        = self.classdef__26
            self.subscript       = self.subscript__26
            self.raise_stmt      = self.raise_stmt__26
            self.comp_if         = self.comp_if__26
            self.atom            = self.atom__26
            self.funcdef         = self.funcdef__26
            self.parameters      = self.parameters__26
            self.varargslist     = self.varargslist__26
            self.comparison_1    = self.comparison_1__26
            self.exprlist_1      = self.exprlist_1__26
            self.testlist_comp_1 = self.testlist_comp_1__26
            self.expr_stmt_1     = self.expr_stmt_1__26
            self.yield_expr      = self.yield_expr__26
            return
        elif version in ((3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)):
            _all_stmts[(14964,14968)] = True
            if version == (3, 0):
                _all_stmts[(15042,15044)] = True
                self.with_stmt       = self.with_stmt__26 # lol
            else:
                _all_stmts[(15140,15144)] = True
                self.with_stmt       = self.with_stmt__27
            self.except_clause_1 = self.except_clause_1__30
            self.classdef        = self.classdef__30
            self.subscript       = self.subscript__30
            self.raise_stmt      = self.raise_stmt__30
            self.comp_if         = self.comp_if__30
            self.atom            = self.atom__30
            self.funcdef         = self.funcdef__30
            self.parameters      = self.parameters__30
            if version < (3, 2):
                _all_stmts[(15646,15648)] = True
                self.varargslist     = self.varargslist__30
                self.typedargslist   = self.typedargslist__30
                self.comparison_1    = self.comparison_1__30
                self.star_expr       = self.star_expr__30
                self.exprlist_1      = self.exprlist_1__30
                self.testlist_comp_1 = self.testlist_comp_1__26
                self.expr_stmt_1     = self.expr_stmt_1__26
            else:
                _all_stmts[(16103,16107)] = True
                self.varargslist     = self.varargslist__32
                self.typedargslist   = self.typedargslist__32
                self.comparison_1    = self.comparison_1__32
                self.star_expr       = self.star_expr__32
                self.exprlist_1      = self.exprlist_1__32
                self.testlist_comp_1 = self.testlist_comp_1__32
                self.expr_stmt_1     = self.expr_stmt_1__32
            if version < (3, 3):
                _all_stmts[(16545,16547)] = True
                self.yield_expr      = self.yield_expr__26
            else:
                _all_stmts[(16637,16641)] = True
                self.yield_expr      = self.yield_expr__33
            return

        raise NotImplementedError("pythonparser.parser.Parser cannot parse Python %s" %
                                  str(version))

    def _arguments(self, args=None, defaults=None, kwonlyargs=None, kw_defaults=None,
                   vararg=None, kwarg=None,
                   star_loc=None, dstar_loc=None, begin_loc=None, end_loc=None,
                   equals_locs=None, kw_equals_locs=None, loc=None):
        _all_stmts[(16863,16866)] = True
        if args is None:
            _all_stmts[(17146,17148)] = True
            args = []
        if defaults is None:
            _all_stmts[(17193,17195)] = True
            defaults = []
        if kwonlyargs is None:
            _all_stmts[(17248,17250)] = True
            kwonlyargs = []
        if kw_defaults is None:
            _all_stmts[(17307,17309)] = True
            kw_defaults = []
        if equals_locs is None:
            _all_stmts[(17368,17370)] = True
            equals_locs = []
        if kw_equals_locs is None:
            _all_stmts[(17429,17431)] = True
            kw_equals_locs = []
        return ast.arguments(args=args, defaults=defaults,
                             kwonlyargs=kwonlyargs, kw_defaults=kw_defaults,
                             vararg=vararg, kwarg=kwarg,
                             star_loc=star_loc, dstar_loc=dstar_loc,
                             begin_loc=begin_loc, end_loc=end_loc,
                             equals_locs=equals_locs, kw_equals_locs=kw_equals_locs,
                             loc=loc)

    def _arg(self, tok, colon_loc=None, annotation=None):
        _all_stmts[(17945,17948)] = True
        loc = tok.loc
        if annotation:
            _all_stmts[(18029,18031)] = True
            loc = loc.join(annotation.loc)
        return ast.arg(arg=tok.value, annotation=annotation,
                       arg_loc=tok.loc, colon_loc=colon_loc, loc=loc)

    def _empty_arglist(self):
        _all_stmts[(18223,18226)] = True
        return ast.Call(args=[], keywords=[], starargs=None, kwargs=None,
                        star_loc=None, dstar_loc=None, loc=None)

    def _wrap_tuple(self, elts):
        _all_stmts[(18393,18396)] = True
        assert len(elts) > 0
        if len(elts) > 1:
            _all_stmts[(18459,18461)] = True
            return ast.Tuple(ctx=None, elts=elts,
                             loc=elts[0].loc.join(elts[-1].loc), begin_loc=None, end_loc=None)
        else:
            _all_stmts[(18630,18634)] = True
            return elts[0]

    def _assignable(self, node, is_delete=False):
        _all_stmts[(18668,18671)] = True
        if isinstance(node, ast.Name) or isinstance(node, ast.Subscript) or \
                isinstance(node, ast.Attribute) or isinstance(node, ast.Starred):
            _all_stmts[(18722,18724)] = True
            return node
        elif (isinstance(node, ast.List) or isinstance(node, ast.Tuple)) and \
                any(node.elts):
            _all_stmts[(18906,18910)] = True
            node.elts = [self._assignable(elt, is_delete) for elt in node.elts]
            return node
        else:
            _all_stmts[(19121,19125)] = True
            if is_delete:
                _all_stmts[(19139,19141)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "cannot delete this expression", {}, node.loc)
            else:
                _all_stmts[(19288,19292)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "cannot assign to this expression", {}, node.loc)
            self.diagnostic_engine.process(error)

    def add_flags(self, flags):
        _all_stmts[(19475,19478)] = True
        if "print_function" in flags:
            _all_stmts[(19511,19513)] = True
            self.lexer.print_function = True

    # Grammar
    @action(Expect(Alt(Newline(loc=(19624,19631)),
                       Rule("simple_stmt", loc=(19658,19662)),
                       SeqN(0, Rule("compound_stmt", loc=(19710,19714)), Newline(loc=(19733,19740)), loc=(19702,19706)), loc=(19620,19623)), loc=(19613,19619)), loc=(19606,19612))
    def single_input(self, body):
        _all_stmts[(19751,19754)] = True
        """single_input: NEWLINE | simple_stmt | compound_stmt NEWLINE"""
        loc = None
        if body != []:
            _all_stmts[(19882,19884)] = True
            loc = body[0].loc
        return ast.Interactive(body=body, loc=loc)

    @action(Expect(SeqN(0, Star(Alt(Newline(loc=(20015,20022)), Rule("stmt", loc=(20026,20030)), loc=(20011,20014)), loc=(20006,20010)), Tok("eof", loc=(20042,20045)), loc=(19998,20002)), loc=(19991,19997)), loc=(19984,19990))
    def file_input(parser, body):
        _all_stmts[(20060,20063)] = True
        """file_input: (NEWLINE | stmt)* ENDMARKER"""
        body = reduce(list.__add__, body, [])
        loc = None
        if body != []:
            _all_stmts[(20217,20219)] = True
            loc = body[0].loc
        return ast.Module(body=body, loc=loc)

    @action(Expect(SeqN(0, Rule("testlist", loc=(20336,20340)), Star(Tok("newline", loc=(20359,20362)), loc=(20354,20358)), Tok("eof", loc=(20376,20379)), loc=(20328,20332)), loc=(20321,20327)), loc=(20314,20320))
    def eval_input(self, expr):
        _all_stmts[(20394,20397)] = True
        """eval_input: testlist NEWLINE* ENDMARKER"""
        return ast.Expression(body=[expr], loc=expr.loc)

    @action(Seq(Loc("@", loc=(20550,20553)), List(Tok("ident", loc=(20565,20568)), ".", trailing=False, loc=(20560,20564)),
                Opt(BeginEnd("(", Opt(Rule("arglist", loc=(20639,20643)), loc=(20635,20638)), ")",
                             empty=_empty_arglist, loc=(20621,20629)), loc=(20617,20620)),
                Loc("newline", loc=(20731,20734)), loc=(20546,20549)), loc=(20539,20545))
    def decorator(self, at_loc, idents, call_opt, newline_loc):
        _all_stmts[(20752,20755)] = True
        """decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE"""
        root = idents[0]
        dec_loc = root.loc
        expr = ast.Name(id=root.value, ctx=None, loc=root.loc)
        for ident in idents[1:]:
          _all_stmts[(21006,21009)] = True
          dot_loc = ident.loc.begin()
          dot_loc.begin_pos -= 1
          dec_loc = dec_loc.join(ident.loc)
          expr = ast.Attribute(value=expr, attr=ident.value, ctx=None,
                               loc=expr.loc.join(ident.loc),
                               attr_loc=ident.loc, dot_loc=dot_loc)

        if call_opt:
            _all_stmts[(21355,21357)] = True
            call_opt.func = expr
            call_opt.loc = dec_loc.join(call_opt.loc)
            expr = call_opt
        return at_loc, expr

    decorators = Plus(Rule("decorator", loc=(21534,21538)), loc=(21529,21533))
    """decorators: decorator+"""

    @action(Seq(Rule("decorators", loc=(21603,21607)), Alt(Rule("classdef", loc=(21627,21631)), Rule("funcdef", loc=(21645,21649)), loc=(21623,21626)), loc=(21599,21602)), loc=(21592,21598))
    def decorated(self, decorators, classfuncdef):
        _all_stmts[(21668,21671)] = True
        """decorated: decorators (classdef | funcdef)"""
        classfuncdef.at_locs = list(map(lambda x: x[0], decorators))
        classfuncdef.decorator_list = list(map(lambda x: x[1], decorators))
        classfuncdef.loc = classfuncdef.loc.join(decorators[0][0])
        return classfuncdef

    @action(Seq(Loc("def", loc=(22029,22032)), Tok("ident", loc=(22041,22044)), Rule("parameters", loc=(22055,22059)), Loc(":", loc=(22075,22078)), Rule("suite", loc=(22085,22089)), loc=(22025,22028)), loc=(22018,22024))
    def funcdef__26(self, def_loc, ident_tok, args, colon_loc, suite):
        _all_stmts[(22105,22108)] = True
        """(2.6, 2.7) funcdef: 'def' NAME parameters ':' suite"""
        return ast.FunctionDef(name=ident_tok.value, args=args, returns=None,
                               body=suite, decorator_list=[],
                               at_locs=[], keyword_loc=def_loc, name_loc=ident_tok.loc,
                               colon_loc=colon_loc, arrow_loc=None,
                               loc=def_loc.join(suite[-1].loc))

    @action(Seq(Loc("def", loc=(22615,22618)), Tok("ident", loc=(22627,22630)), Rule("parameters", loc=(22641,22645)),
                Opt(Seq(Loc("->", loc=(22685,22688)), Rule("test", loc=(22696,22700)), loc=(22681,22684)), loc=(22677,22680)),
                Loc(":", loc=(22728,22731)), Rule("suite", loc=(22738,22742)), loc=(22611,22614)), loc=(22604,22610))
    def funcdef__30(self, def_loc, ident_tok, args, returns_opt, colon_loc, suite):
        _all_stmts[(22758,22761)] = True
        """(3.0-) funcdef: 'def' NAME parameters ['->' test] ':' suite"""
        arrow_loc = returns = None
        if returns_opt:
            _all_stmts[(22955,22957)] = True
            arrow_loc, returns = returns_opt
        return ast.FunctionDef(name=ident_tok.value, args=args, returns=returns,
                               body=suite, decorator_list=[],
                               at_locs=[], keyword_loc=def_loc, name_loc=ident_tok.loc,
                               colon_loc=colon_loc, arrow_loc=arrow_loc,
                               loc=def_loc.join(suite[-1].loc))

    parameters__26 = BeginEnd("(", Opt(Rule("varargslist", loc=(23424,23428)), loc=(23420,23423)), ")", empty=_arguments, loc=(23406,23414))
    """(2.6, 2.7) parameters: '(' [varargslist] ')'"""

    parameters__30 = BeginEnd("(", Opt(Rule("typedargslist", loc=(23564,23568)), loc=(23560,23563)), ")", empty=_arguments, loc=(23546,23554))
    """(3.0) parameters: '(' [typedargslist] ')'"""

    varargslist__26_1 = Seq(Rule("fpdef", loc=(23692,23696)), Opt(Seq(Loc("=", loc=(23715,23718)), Rule("test", loc=(23725,23729)), loc=(23711,23714)), loc=(23707,23710)), loc=(23688,23691))

    @action(Seq(Loc("**", loc=(23758,23761)), Tok("ident", loc=(23769,23772)), loc=(23754,23757)), loc=(23747,23753))
    def varargslist__26_2(self, dstar_loc, kwarg_tok):
        _all_stmts[(23788,23791)] = True
        return self._arguments(kwarg=self._arg(kwarg_tok),
                               dstar_loc=dstar_loc, loc=dstar_loc.join(kwarg_tok.loc))

    @action(Seq(Loc("*", loc=(24002,24005)), Tok("ident", loc=(24012,24015)),
                Opt(Seq(Tok(",", loc=(24050,24053)), Loc("**", loc=(24060,24063)), Tok("ident", loc=(24071,24074)), loc=(24046,24049)), loc=(24042,24045)), loc=(23998,24001)), loc=(23991,23997))
    def varargslist__26_3(self, star_loc, vararg_tok, kwarg_opt):
        _all_stmts[(24092,24095)] = True
        dstar_loc = kwarg = None
        loc = star_loc.join(vararg_tok.loc)
        vararg = self._arg(vararg_tok)
        if kwarg_opt:
            _all_stmts[(24278,24280)] = True
            _, dstar_loc, kwarg_tok = kwarg_opt
            kwarg = self._arg(kwarg_tok)
            loc = star_loc.join(kwarg_tok.loc)
        return self._arguments(vararg=vararg, kwarg=kwarg,
                               star_loc=star_loc, dstar_loc=dstar_loc, loc=loc)

    @action(Eps(value=(), loc=(24580,24583)), loc=(24573,24579))
    def varargslist__26_4(self):
        _all_stmts[(24599,24602)] = True
        return self._arguments()

    @action(Alt(Seq(Star(SeqN(0, varargslist__26_1, Tok(",", loc=(24714,24717)), loc=(24687,24691)), loc=(24682,24686)),
                    Alt(varargslist__26_2, varargslist__26_3, loc=(24746,24749)), loc=(24678,24681)),
                Seq(List(varargslist__26_1, ",", trailing=True, loc=(24810,24814)),
                    varargslist__26_4, loc=(24806,24809)), loc=(24674,24677)), loc=(24667,24673))
    def varargslist__26(self, fparams, args):
        _all_stmts[(24900,24903)] = True
        """
        (2.6, 2.7)
        varargslist: ((fpdef ['=' test] ',')*
                      ('*' NAME [',' '**' NAME] | '**' NAME) |
                      fpdef ['=' test] (',' fpdef ['=' test])* [','])
        """
        for fparam, default_opt in fparams:
            _all_stmts[(25172,25175)] = True
            if default_opt:
                _all_stmts[(25220,25222)] = True
                equals_loc, default = default_opt
                args.equals_locs.append(equals_loc)
                args.defaults.append(default)
            elif len(args.defaults) > 0:
                _all_stmts[(25396,25400)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "non-default argument follows default argument", {},
                    fparam.loc, [args.args[-1].loc.join(args.defaults[-1].loc)])
                self.diagnostic_engine.process(error)

            args.args.append(fparam)

        def fparam_loc(fparam, default_opt):
            _all_stmts[(25736,25739)] = True
            if default_opt:
                _all_stmts[(25785,25787)] = True
                equals_loc, default = default_opt
                return fparam.loc.join(default.loc)
            else:
                _all_stmts[(25915,25919)] = True
                return fparam.loc

        if args.loc is None:
            _all_stmts[(25964,25966)] = True
            args.loc = fparam_loc(*fparams[0]).join(fparam_loc(*fparams[-1]))
        elif len(fparams) > 0:
            _all_stmts[(26071,26075)] = True
            args.loc = args.loc.join(fparam_loc(*fparams[0]))

        return args

    @action(Tok("ident", loc=(26190,26193)), loc=(26183,26189))
    def fpdef_1(self, ident_tok):
        _all_stmts[(26208,26211)] = True
        return ast.arg(arg=ident_tok.value, annotation=None,
                       arg_loc=ident_tok.loc, colon_loc=None,
                       loc=ident_tok.loc)

    fpdef = Alt(fpdef_1, BeginEnd("(", Rule("fplist", loc=(26443,26447)), ")",
                                  empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(26429,26437)), loc=(26416,26419))
    """fpdef: NAME | '(' fplist ')'"""

    def _argslist(fpdef_rule, old_style=False):
        _all_stmts[(26602,26605)] = True
        argslist_1 = Seq(fpdef_rule, Opt(Seq(Loc("=", loc=(26691,26694)), Rule("test", loc=(26701,26705)), loc=(26687,26690)), loc=(26683,26686)), loc=(26667,26670))

        @action(Seq(Loc("**", loc=(26738,26741)), Tok("ident", loc=(26749,26752)), loc=(26734,26737)), loc=(26727,26733))
        def argslist_2(self, dstar_loc, kwarg_tok):
            _all_stmts[(26772,26775)] = True
            return self._arguments(kwarg=self._arg(kwarg_tok),
                                   dstar_loc=dstar_loc, loc=dstar_loc.join(kwarg_tok.loc))

        @action(Seq(Loc("*", loc=(26991,26994)), Tok("ident", loc=(27001,27004)),
                    Star(SeqN(1, Tok(",", loc=(27048,27051)), argslist_1, loc=(27040,27044)), loc=(27035,27039)),
                    Opt(Seq(Tok(",", loc=(27100,27103)), Loc("**", loc=(27110,27113)), Tok("ident", loc=(27121,27124)), loc=(27096,27099)), loc=(27092,27095)), loc=(26987,26990)), loc=(26980,26986))
        def argslist_3(self, star_loc, vararg_tok, fparams, kwarg_opt):
            _all_stmts[(27146,27149)] = True
            dstar_loc = kwarg = None
            loc = star_loc.join(vararg_tok.loc)
            vararg = self._arg(vararg_tok)
            if kwarg_opt:
                _all_stmts[(27350,27352)] = True
                _, dstar_loc, kwarg_tok = kwarg_opt
                kwarg = self._arg(kwarg_tok)
                loc = star_loc.join(kwarg_tok.loc)
            kwonlyargs, kw_defaults, kw_equals_locs = [], [], []
            for fparam, default_opt in fparams:
                _all_stmts[(27589,27592)] = True
                if default_opt:
                    _all_stmts[(27641,27643)] = True
                    equals_loc, default = default_opt
                    kw_equals_locs.append(equals_loc)
                    kw_defaults.append(default)
                else:
                    _all_stmts[(27829,27833)] = True
                    kw_defaults.append(None)
                kwonlyargs.append(fparam)
            if any(kw_defaults):
                _all_stmts[(27934,27936)] = True
                loc = loc.join(kw_defaults[-1].loc)
            elif any(kwonlyargs):
                _all_stmts[(28019,28023)] = True
                loc = loc.join(kwonlyargs[-1].loc)
            return self._arguments(vararg=vararg, kwarg=kwarg,
                                   kwonlyargs=kwonlyargs, kw_defaults=kw_defaults,
                                   star_loc=star_loc, dstar_loc=dstar_loc,
                                   kw_equals_locs=kw_equals_locs, loc=loc)

        argslist_4 = Alt(argslist_2, argslist_3, loc=(28410,28413))

        @action(Eps(value=(), loc=(28455,28458)), loc=(28448,28454))
        def argslist_5(self):
            _all_stmts[(28478,28481)] = True
            return self._arguments()

        if old_style:
            _all_stmts[(28546,28548)] = True
            argslist = Alt(Seq(Star(SeqN(0, argslist_1, Tok(",", loc=(28616,28619)), loc=(28596,28600)), loc=(28591,28595)),
                               argslist_4, loc=(28587,28590)),
                           Seq(List(argslist_1, ",", trailing=True, loc=(28703,28707)),
                               argslist_5, loc=(28699,28702)), loc=(28583,28586))
        else:
            _all_stmts[(28793,28797)] = True
            argslist = Alt(Seq(Eps(value=[], loc=(28830,28833)), argslist_4, loc=(28826,28829)),
                           Seq(List(argslist_1, ",", trailing=False, loc=(28889,28893)),
                               Alt(SeqN(1, Tok(",", loc=(28971,28974)), Alt(argslist_4, argslist_5, loc=(28981,28984)), loc=(28963,28967)),
                                   argslist_5, loc=(28959,28962)), loc=(28885,28888)), loc=(28822,28825))

        def argslist_action(self, fparams, args):
            _all_stmts[(29069,29072)] = True
            for fparam, default_opt in fparams:
                _all_stmts[(29123,29126)] = True
                if default_opt:
                    _all_stmts[(29175,29177)] = True
                    equals_loc, default = default_opt
                    args.equals_locs.append(equals_loc)
                    args.defaults.append(default)
                elif len(args.defaults) > 0:
                    _all_stmts[(29367,29371)] = True
                    error = diagnostic.Diagnostic(
                        "fatal", "non-default argument follows default argument", {},
                        fparam.loc, [args.args[-1].loc.join(args.defaults[-1].loc)])
                    self.diagnostic_engine.process(error)

                args.args.append(fparam)

            def fparam_loc(fparam, default_opt):
                _all_stmts[(29731,29734)] = True
                if default_opt:
                    _all_stmts[(29784,29786)] = True
                    equals_loc, default = default_opt
                    return fparam.loc.join(default.loc)
                else:
                    _all_stmts[(29926,29930)] = True
                    return fparam.loc

            if args.loc is None:
                _all_stmts[(29983,29985)] = True
                args.loc = fparam_loc(*fparams[0]).join(fparam_loc(*fparams[-1]))
            elif len(fparams) > 0:
                _all_stmts[(30098,30102)] = True
                args.loc = args.loc.join(fparam_loc(*fparams[0]))

            return args

        return action(argslist, loc=(30228,30234))(argslist_action)

    typedargslist__30 = _argslist(Rule("tfpdef", loc=(30297,30301)), old_style=True)
    """
    (3.0, 3.1)
    typedargslist: ((tfpdef ['=' test] ',')*
                    ('*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef)
                    | tfpdef ['=' test] (',' tfpdef ['=' test])* [','])
    """

    typedargslist__32 = _argslist(Rule("tfpdef", loc=(30604,30608)))
    """
    (3.2-)
    typedargslist: (tfpdef ['=' test] (',' tfpdef ['=' test])* [','
           ['*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef]]
         |  '*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef)
    """

    varargslist__30 = _argslist(Rule("vfpdef", loc=(30915,30919)), old_style=True)
    """
    (3.0, 3.1)
    varargslist: ((vfpdef ['=' test] ',')*
                  ('*' [vfpdef] (',' vfpdef ['=' test])*  [',' '**' vfpdef] | '**' vfpdef)
                  | vfpdef ['=' test] (',' vfpdef ['=' test])* [','])
    """

    varargslist__32 = _argslist(Rule("vfpdef", loc=(31215,31219)))
    """
    (3.2-)
    varargslist: (vfpdef ['=' test] (',' vfpdef ['=' test])* [','
           ['*' [vfpdef] (',' vfpdef ['=' test])* [',' '**' vfpdef] | '**' vfpdef]]
         |  '*' [vfpdef] (',' vfpdef ['=' test])* [',' '**' vfpdef] | '**' vfpdef)
    """

    @action(Seq(Tok("ident", loc=(31508,31511)), Opt(Seq(Loc(":", loc=(31530,31533)), Rule("test", loc=(31540,31544)), loc=(31526,31529)), loc=(31522,31525)), loc=(31504,31507)), loc=(31497,31503))
    def tfpdef(self, ident_tok, annotation_opt):
        _all_stmts[(31561,31564)] = True
        """(3.0-) tfpdef: NAME [':' test]"""
        if annotation_opt:
            _all_stmts[(31659,31661)] = True
            colon_loc, annotation = annotation_opt
            return self._arg(ident_tok, colon_loc, annotation)
        return self._arg(ident_tok)

    vfpdef = fpdef_1
    """(3.0-) vfpdef: NAME"""

    @action(List(Rule("fpdef", loc=(31898,31902)), ",", trailing=True, loc=(31893,31897)), loc=(31886,31892))
    def fplist(self, elts):
        _all_stmts[(31938,31941)] = True
        """fplist: fpdef (',' fpdef)* [',']"""
        return ast.Tuple(elts=elts, ctx=None, loc=None)

    stmt = Alt(Rule("simple_stmt", loc=(32081,32085)), Rule("compound_stmt", loc=(32102,32106)), loc=(32077,32080))
    """stmt: simple_stmt | compound_stmt"""

    simple_stmt = SeqN(0, List(Rule("small_stmt", loc=(32201,32205)), ";", trailing=True, loc=(32196,32200)), Tok("newline", loc=(32242,32245)), loc=(32188,32192))
    """simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE"""

    small_stmt = Alt(Rule("expr_stmt", loc=(32346,32350)), Rule("print_stmt", loc=(32365,32369)),  Rule("del_stmt", loc=(32386,32390)),
                     Rule("pass_stmt", loc=(32425,32429)), Rule("flow_stmt", loc=(32444,32448)), Rule("import_stmt", loc=(32463,32467)),
                     Rule("global_stmt", loc=(32505,32509)), Rule("nonlocal_stmt", loc=(32526,32530)), Rule("exec_stmt", loc=(32549,32553)),
                     Rule("assert_stmt", loc=(32589,32593)), loc=(32342,32345))
    """
    (2.6, 2.7)
    small_stmt: (expr_stmt | print_stmt  | del_stmt | pass_stmt | flow_stmt |
                 import_stmt | global_stmt | exec_stmt | assert_stmt)
    (3.0-)
    small_stmt: (expr_stmt | del_stmt | pass_stmt | flow_stmt |
                 import_stmt | global_stmt | nonlocal_stmt | assert_stmt)
    """

    expr_stmt_1__26 = Rule("testlist", loc=(32961,32965))
    expr_stmt_1__32 = Rule("testlist_star_expr", loc=(33000,33004))

    @action(Seq(Rule("augassign", loc=(33044,33048)), Alt(Rule("yield_expr", loc=(33067,33071)), Rule("testlist", loc=(33087,33091)), loc=(33063,33066)), loc=(33040,33043)), loc=(33033,33039))
    def expr_stmt_2(self, augassign, rhs_expr):
        _all_stmts[(33111,33114)] = True
        return ast.AugAssign(op=augassign, value=rhs_expr)

    @action(Star(Seq(Loc("=", loc=(33236,33239)), Alt(Rule("yield_expr", loc=(33250,33254)), Rule("expr_stmt_1", loc=(33270,33274)), loc=(33246,33249)), loc=(33232,33235)), loc=(33227,33231)), loc=(33220,33226))
    def expr_stmt_3(self, seq):
        _all_stmts[(33298,33301)] = True
        if len(seq) > 0:
            _all_stmts[(33334,33336)] = True
            return ast.Assign(targets=list(map(lambda x: x[1], seq[:-1])), value=seq[-1][1],
                              op_locs=list(map(lambda x: x[0], seq)))
        else:
            _all_stmts[(33522,33526)] = True
            return None

    @action(Seq(Rule("expr_stmt_1", loc=(33569,33573)), Alt(expr_stmt_2, expr_stmt_3, loc=(33590,33593)), loc=(33565,33568)), loc=(33558,33564))
    def expr_stmt(self, lhs, rhs):
        _all_stmts[(33626,33629)] = True
        """
        (2.6, 2.7, 3.0, 3.1)
        expr_stmt: testlist (augassign (yield_expr|testlist) |
                             ('=' (yield_expr|testlist))*)
        (3.2-)
        expr_stmt: testlist_star_expr (augassign (yield_expr|testlist) |
                             ('=' (yield_expr|testlist_star_expr))*)
        """
        if isinstance(rhs, ast.AugAssign):
            _all_stmts[(33997,33999)] = True
            if isinstance(lhs, ast.Tuple) or isinstance(lhs, ast.List):
                _all_stmts[(34044,34046)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "illegal expression for augmented assignment", {},
                    rhs.op.loc, [lhs.loc])
                self.diagnostic_engine.process(error)
            else:
                _all_stmts[(34340,34344)] = True
                rhs.target = self._assignable(lhs)
                rhs.loc = rhs.target.loc.join(rhs.value.loc)
                return rhs
        elif rhs is not None:
            _all_stmts[(34493,34497)] = True
            rhs.targets = list(map(self._assignable, [lhs] + rhs.targets))
            rhs.loc = lhs.loc.join(rhs.value.loc)
            return rhs
        else:
            _all_stmts[(34671,34675)] = True
            return ast.Expr(value=lhs, loc=lhs.loc)

    testlist_star_expr = action(
        List(Alt(Rule("test", loc=(34780,34784)), Rule("star_expr", loc=(34794,34798)), loc=(34776,34779)), ",", trailing=True, loc=(34771,34775)), loc=(34755,34761)) \
        (_wrap_tuple)
    """(3.2-) testlist_star_expr: (test|star_expr) (',' (test|star_expr))* [',']"""

    augassign = Alt(Oper(ast.Add, "+=", loc=(34964,34968)), Oper(ast.Sub, "-=", loc=(34985,34989)), Oper(ast.MatMult, "@=", loc=(35006,35010)),
                    Oper(ast.Mult, "*=", loc=(35051,35055)), Oper(ast.Div, "/=", loc=(35073,35077)), Oper(ast.Mod, "%=", loc=(35094,35098)),
                    Oper(ast.BitAnd, "&=", loc=(35135,35139)), Oper(ast.BitOr, "|=", loc=(35159,35163)), Oper(ast.BitXor, "^=", loc=(35182,35186)),
                    Oper(ast.LShift, "<<=", loc=(35226,35230)), Oper(ast.RShift, ">>=", loc=(35251,35255)),
                    Oper(ast.Pow, "**=", loc=(35296,35300)), Oper(ast.FloorDiv, "//=", loc=(35318,35322)), loc=(34960,34963))
    """augassign: ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' |
                   '<<=' | '>>=' | '**=' | '//=')"""

    @action(List(Rule("test", loc=(35491,35495)), ",", trailing=True, loc=(35486,35490)), loc=(35479,35485))
    def print_stmt_1(self, values):
        _all_stmts[(35530,35533)] = True
        nl, loc = True, values[-1].loc
        if values.trailing_comma:
            _all_stmts[(35609,35611)] = True
            nl, loc = False, values.trailing_comma.loc
        return ast.Print(dest=None, values=values, nl=nl,
                         dest_loc=None, loc=loc)

    @action(Seq(Loc(">>", loc=(35814,35817)), Rule("test", loc=(35825,35829)), Tok(",", loc=(35839,35842)), List(Rule("test", loc=(35854,35858)), ",", trailing=True, loc=(35849,35853)), loc=(35810,35813)), loc=(35803,35809))
    def print_stmt_2(self, dest_loc, dest, comma_tok, values):
        _all_stmts[(35894,35897)] = True
        nl, loc = True, values[-1].loc
        if values.trailing_comma:
            _all_stmts[(36000,36002)] = True
            nl, loc = False, values.trailing_comma.loc
        return ast.Print(dest=dest, values=values, nl=nl,
                         dest_loc=dest_loc, loc=loc)

    @action(Eps(loc=(36205,36208)), loc=(36198,36204))
    def print_stmt_3(self, eps):
        _all_stmts[(36216,36219)] = True
        return ast.Print(dest=None, values=[], nl=True,
                         dest_loc=None, loc=None)

    @action(Seq(Loc("print", loc=(36368,36371)), Alt(print_stmt_1, print_stmt_2, print_stmt_3, loc=(36382,36385)), loc=(36364,36367)), loc=(36357,36363))
    def print_stmt(self, print_loc, stmt):
        _all_stmts[(36434,36437)] = True
        """
        (2.6-2.7)
        print_stmt: 'print' ( [ test (',' test)* [','] ] |
                              '>>' test [ (',' test)+ [','] ] )
        """
        stmt.keyword_loc = print_loc
        if stmt.loc is None:
            _all_stmts[(36683,36685)] = True
            stmt.loc = print_loc
        else:
            _all_stmts[(36745,36749)] = True
            stmt.loc = print_loc.join(stmt.loc)
        return stmt

    @action(Seq(Loc("del", loc=(36836,36839)), List(Rule("expr", loc=(36853,36857)), ",", trailing=True, loc=(36848,36852)), loc=(36832,36835)), loc=(36825,36831))
    def del_stmt(self, stmt_loc, exprs):
        # Python uses exprlist here, but does *not* obey the usual
        # tuple-wrapping semantics, so we embed the rule directly.
        _all_stmts[(36893,36896)] = True
        """del_stmt: 'del' exprlist"""
        return ast.Delete(targets=[self._assignable(expr, is_delete=True) for expr in exprs],
                          loc=stmt_loc.join(exprs[-1].loc), keyword_loc=stmt_loc)

    @action(Loc("pass", loc=(37292,37295)), loc=(37285,37291))
    def pass_stmt(self, stmt_loc):
        _all_stmts[(37309,37312)] = True
        """pass_stmt: 'pass'"""
        return ast.Pass(loc=stmt_loc, keyword_loc=stmt_loc)

    flow_stmt = Alt(Rule("break_stmt", loc=(37453,37457)), Rule("continue_stmt", loc=(37473,37477)), Rule("return_stmt", loc=(37496,37500)),
                    Rule("raise_stmt", loc=(37537,37541)), Rule("yield_stmt", loc=(37557,37561)), loc=(37449,37452))
    """flow_stmt: break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt"""

    @action(Loc("break", loc=(37678,37681)), loc=(37671,37677))
    def break_stmt(self, stmt_loc):
        _all_stmts[(37696,37699)] = True
        """break_stmt: 'break'"""
        return ast.Break(loc=stmt_loc, keyword_loc=stmt_loc)

    @action(Loc("continue", loc=(37836,37839)), loc=(37829,37835))
    def continue_stmt(self, stmt_loc):
        _all_stmts[(37857,37860)] = True
        """continue_stmt: 'continue'"""
        return ast.Continue(loc=stmt_loc, keyword_loc=stmt_loc)

    @action(Seq(Loc("return", loc=(38013,38016)), Opt(Rule("testlist", loc=(38032,38036)), loc=(38028,38031)), loc=(38009,38012)), loc=(38002,38008))
    def return_stmt(self, stmt_loc, values):
        _all_stmts[(38056,38059)] = True
        """return_stmt: 'return' [testlist]"""
        loc = stmt_loc
        if values:
            _all_stmts[(38175,38177)] = True
            loc = loc.join(values.loc)
        return ast.Return(value=values,
                          loc=loc, keyword_loc=stmt_loc)

    @action(Rule("yield_expr", loc=(38335,38339)), loc=(38328,38334))
    def yield_stmt(self, expr):
        _all_stmts[(38359,38362)] = True
        """yield_stmt: yield_expr"""
        return ast.Expr(value=expr, loc=expr.loc)

    @action(Seq(Loc("raise", loc=(38491,38494)), Opt(Seq(Rule("test", loc=(38513,38517)),
                                      Opt(Seq(Tok(",", loc=(38573,38576)), Rule("test", loc=(38583,38587)),
                                              Opt(SeqN(1, Tok(",", loc=(38655,38658)), Rule("test", loc=(38665,38669)), loc=(38647,38651)), loc=(38643,38646)), loc=(38569,38572)), loc=(38565,38568)), loc=(38509,38512)), loc=(38505,38508)), loc=(38487,38490)), loc=(38480,38486))
    def raise_stmt__26(self, raise_loc, type_opt):
        _all_stmts[(38690,38693)] = True
        """(2.6, 2.7) raise_stmt: 'raise' [test [',' test [',' test]]]"""
        type_ = inst = tback = None
        loc = raise_loc
        if type_opt:
            _all_stmts[(38879,38881)] = True
            type_, inst_opt = type_opt
            loc = loc.join(type_.loc)
            if inst_opt:
                _all_stmts[(38981,38983)] = True
                _, inst, tback = inst_opt
                loc = loc.join(inst.loc)
                if tback:
                    _all_stmts[(39093,39095)] = True
                    loc = loc.join(tback.loc)
        return ast.Raise(exc=type_, inst=inst, tback=tback, cause=None,
                         keyword_loc=raise_loc, from_loc=None, loc=loc)

    @action(Seq(Loc("raise", loc=(39310,39313)), Opt(Seq(Rule("test", loc=(39332,39336)), Opt(Seq(Loc("from", loc=(39354,39357)), Rule("test", loc=(39367,39371)), loc=(39350,39353)), loc=(39346,39349)), loc=(39328,39331)), loc=(39324,39327)), loc=(39306,39309)), loc=(39299,39305))
    def raise_stmt__30(self, raise_loc, exc_opt):
        _all_stmts[(39390,39393)] = True
        """(3.0-) raise_stmt: 'raise' [test ['from' test]]"""
        exc = from_loc = cause = None
        loc = raise_loc
        if exc_opt:
            _all_stmts[(39568,39570)] = True
            exc, cause_opt = exc_opt
            loc = loc.join(exc.loc)
            if cause_opt:
                _all_stmts[(39665,39667)] = True
                from_loc, cause = cause_opt
                loc = loc.join(cause.loc)
        return ast.Raise(exc=exc, inst=None, tback=None, cause=cause,
                         keyword_loc=raise_loc, from_loc=from_loc, loc=loc)

    import_stmt = Alt(Rule("import_name", loc=(39934,39938)), Rule("import_from", loc=(39955,39959)), loc=(39930,39933))
    """import_stmt: import_name | import_from"""

    @action(Seq(Loc("import", loc=(40042,40045)), Rule("dotted_as_names", loc=(40057,40061)), loc=(40038,40041)), loc=(40031,40037))
    def import_name(self, import_loc, names):
        _all_stmts[(40087,40090)] = True
        """import_name: 'import' dotted_as_names"""
        return ast.Import(names=names,
                          keyword_loc=import_loc, loc=import_loc.join(names[-1].loc))

    @action(Loc(".", loc=(40319,40322)), loc=(40312,40318))
    def import_from_1(self, loc):
        _all_stmts[(40333,40336)] = True
        return 1, loc

    @action(Loc("...", loc=(40398,40401)), loc=(40391,40397))
    def import_from_2(self, loc):
        _all_stmts[(40414,40417)] = True
        return 3, loc

    @action(Seq(Star(Alt(import_from_1, import_from_2, loc=(40488,40491)), loc=(40483,40487)), Rule("dotted_name", loc=(40524,40528)), loc=(40479,40482)), loc=(40472,40478))
    def import_from_3(self, dots, dotted_name):
        _all_stmts[(40550,40553)] = True
        dots_loc, dots_count = None, 0
        if any(dots):
            _all_stmts[(40641,40643)] = True
            dots_loc = dots[0][1].join(dots[-1][1])
            dots_count = sum([count for count, loc in dots])
        return (dots_loc, dots_count), dotted_name

    @action(Plus(Alt(import_from_1, import_from_2, loc=(40837,40840)), loc=(40832,40836)), loc=(40825,40831))
    def import_from_4(self, dots):
        _all_stmts[(40877,40880)] = True
        dots_loc = dots[0][1].join(dots[-1][1])
        dots_count = sum([count for count, loc in dots])
        return (dots_loc, dots_count), None

    @action(Loc("*", loc=(41070,41073)), loc=(41063,41069))
    def import_from_5(self, star_loc):
        _all_stmts[(41084,41087)] = True
        return (None, 0), \
               [ast.alias(name="*", asname=None,
                          name_loc=star_loc, as_loc=None, asname_loc=None, loc=star_loc)], \
               None

    @action(Rule("import_as_names", loc=(41322,41326)), loc=(41315,41321))
    def import_from_6(self, names):
        _all_stmts[(41351,41354)] = True
        return (None, 0), names, None

    @action(Seq(Loc("from", loc=(41438,41441)), Alt(import_from_3, import_from_4, loc=(41451,41454)),
                Loc("import", loc=(41502,41505)), Alt(import_from_5,
                                   Seq(Loc("(", loc=(41575,41578)), Rule("import_as_names", loc=(41585,41589)), Loc(")", loc=(41610,41613)), loc=(41571,41574)),
                                   import_from_6, loc=(41517,41520)), loc=(41434,41437)), loc=(41427,41433))
    def import_from(self, from_loc, module_name, import_loc, names):
        _all_stmts[(41677,41680)] = True
        """
        (2.6, 2.7)
        import_from: ('from' ('.'* dotted_name | '.'+)
                      'import' ('*' | '(' import_as_names ')' | import_as_names))
        (3.0-)
        # note below: the ('.' | '...') is necessary because '...' is tokenized as ELLIPSIS
        import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+)
                      'import' ('*' | '(' import_as_names ')' | import_as_names))
        """
        (dots_loc, dots_count), dotted_name_opt = module_name
        module_loc = module = None
        if dotted_name_opt:
            _all_stmts[(42291,42293)] = True
            module_loc, module = dotted_name_opt
        lparen_loc, names, rparen_loc = names
        loc = from_loc.join(names[-1].loc)
        if rparen_loc:
            _all_stmts[(42457,42459)] = True
            loc = loc.join(rparen_loc)

        if module == "__future__":
            _all_stmts[(42520,42522)] = True
            self.add_flags([x.name for x in names])

        return ast.ImportFrom(names=names, module=module, level=dots_count,
                              keyword_loc=from_loc, dots_loc=dots_loc, module_loc=module_loc,
                              import_loc=import_loc, lparen_loc=lparen_loc, rparen_loc=rparen_loc,
                              loc=loc)

    @action(Seq(Tok("ident", loc=(42925,42928)), Opt(Seq(Loc("as", loc=(42947,42950)), Tok("ident", loc=(42958,42961)), loc=(42943,42946)), loc=(42939,42942)), loc=(42921,42924)), loc=(42914,42920))
    def import_as_name(self, name_tok, as_name_opt):
        _all_stmts[(42979,42982)] = True
        """import_as_name: NAME ['as' NAME]"""
        asname_name = asname_loc = as_loc = None
        loc = name_tok.loc
        if as_name_opt:
            _all_stmts[(43159,43161)] = True
            as_loc, asname = as_name_opt
            asname_name = asname.value
            asname_loc = asname.loc
            loc = loc.join(asname.loc)
        return ast.alias(name=name_tok.value, asname=asname_name,
                         loc=loc, name_loc=name_tok.loc, as_loc=as_loc, asname_loc=asname_loc)

    @action(Seq(Rule("dotted_name", loc=(43508,43512)), Opt(Seq(Loc("as", loc=(43537,43540)), Tok("ident", loc=(43548,43551)), loc=(43533,43536)), loc=(43529,43532)), loc=(43504,43507)), loc=(43497,43503))
    def dotted_as_name(self, dotted_name, as_name_opt):
        _all_stmts[(43569,43572)] = True
        """dotted_as_name: dotted_name ['as' NAME]"""
        asname_name = asname_loc = as_loc = None
        dotted_name_loc, dotted_name_name = dotted_name
        loc = dotted_name_loc
        if as_name_opt:
            _all_stmts[(43818,43820)] = True
            as_loc, asname = as_name_opt
            asname_name = asname.value
            asname_loc = asname.loc
            loc = loc.join(asname.loc)
        return ast.alias(name=dotted_name_name, asname=asname_name,
                         loc=loc, name_loc=dotted_name_loc, as_loc=as_loc, asname_loc=asname_loc)

    import_as_names = List(Rule("import_as_name", loc=(44183,44187)), ",", trailing=True, loc=(44178,44182))
    """import_as_names: import_as_name (',' import_as_name)* [',']"""

    dotted_as_names = List(Rule("dotted_as_name", loc=(44325,44329)), ",", trailing=False, loc=(44320,44324))
    """dotted_as_names: dotted_as_name (',' dotted_as_name)*"""

    @action(List(Tok("ident", loc=(44452,44455)), ".", trailing=False, loc=(44447,44451)), loc=(44440,44446))
    def dotted_name(self, idents):
        _all_stmts[(44492,44495)] = True
        """dotted_name: NAME ('.' NAME)*"""
        return idents[0].loc.join(idents[-1].loc), \
               ".".join(list(map(lambda x: x.value, idents)))

    @action(Seq(Loc("global", loc=(44699,44702)), List(Tok("ident", loc=(44719,44722)), ",", trailing=False, loc=(44714,44718)), loc=(44695,44698)), loc=(44688,44694))
    def global_stmt(self, global_loc, names):
        _all_stmts[(44760,44763)] = True
        """global_stmt: 'global' NAME (',' NAME)*"""
        return ast.Global(names=list(map(lambda x: x.value, names)),
                          name_locs=list(map(lambda x: x.loc, names)),
                          keyword_loc=global_loc, loc=global_loc.join(names[-1].loc))

    @action(Seq(Loc("exec", loc=(45098,45101)), Rule("expr", loc=(45111,45115)),
                Opt(Seq(Loc("in", loc=(45149,45152)), Rule("test", loc=(45160,45164)),
                        Opt(SeqN(1, Loc(",", loc=(45210,45213)), Rule("test", loc=(45220,45224)), loc=(45202,45206)), loc=(45198,45201)), loc=(45145,45148)), loc=(45141,45144)), loc=(45094,45097)), loc=(45087,45093))
    def exec_stmt(self, exec_loc, body, in_opt):
        _all_stmts[(45243,45246)] = True
        """(2.6, 2.7) exec_stmt: 'exec' expr ['in' test [',' test]]"""
        in_loc, globals, locals = None, None, None
        loc = exec_loc.join(body.loc)
        if in_opt:
            _all_stmts[(45456,45458)] = True
            in_loc, globals, locals = in_opt
            if locals:
                _all_stmts[(45524,45526)] = True
                loc = loc.join(locals.loc)
            else:
                _all_stmts[(45590,45594)] = True
                loc = loc.join(globals.loc)
        return ast.Exec(body=body, locals=locals, globals=globals,
                        loc=loc, keyword_loc=exec_loc, in_loc=in_loc)

    @action(Seq(Loc("nonlocal", loc=(45794,45797)), List(Tok("ident", loc=(45816,45819)), ",", trailing=False, loc=(45811,45815)), loc=(45790,45793)), loc=(45783,45789))
    def nonlocal_stmt(self, nonlocal_loc, names):
        _all_stmts[(45857,45860)] = True
        """(3.0-) nonlocal_stmt: 'nonlocal' NAME (',' NAME)*"""
        return ast.Nonlocal(names=list(map(lambda x: x.value, names)),
                            name_locs=list(map(lambda x: x.loc, names)),
                            keyword_loc=nonlocal_loc, loc=nonlocal_loc.join(names[-1].loc))

    @action(Seq(Loc("assert", loc=(46220,46223)), Rule("test", loc=(46235,46239)), Opt(SeqN(1, Tok(",", loc=(46261,46264)), Rule("test", loc=(46271,46275)), loc=(46253,46257)), loc=(46249,46252)), loc=(46216,46219)), loc=(46209,46215))
    def assert_stmt(self, assert_loc, test, msg):
        _all_stmts[(46292,46295)] = True
        """assert_stmt: 'assert' test [',' test]"""
        loc = assert_loc.join(test.loc)
        if msg:
            _all_stmts[(46438,46440)] = True
            loc = loc.join(msg.loc)
        return ast.Assert(test=test, msg=msg,
                          loc=loc, keyword_loc=assert_loc)

    @action(Alt(Rule("if_stmt", loc=(46604,46608)), Rule("while_stmt", loc=(46621,46625)), Rule("for_stmt", loc=(46641,46645)),
                Rule("try_stmt", loc=(46675,46679)), Rule("with_stmt", loc=(46693,46697)), Rule("funcdef", loc=(46712,46716)),
                Rule("classdef", loc=(46745,46749)), Rule("decorated", loc=(46763,46767)), loc=(46600,46603)), loc=(46593,46599))
    def compound_stmt(self, stmt):
        _all_stmts[(46787,46790)] = True
        """compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt |
                          funcdef | classdef | decorated"""
        return [stmt]

    @action(Seq(Loc("if", loc=(47000,47003)), Rule("test", loc=(47011,47015)), Loc(":", loc=(47025,47028)), Rule("suite", loc=(47035,47039)),
                Star(Seq(Loc("elif", loc=(47075,47078)), Rule("test", loc=(47088,47092)), Loc(":", loc=(47102,47105)), Rule("suite", loc=(47112,47116)), loc=(47071,47074)), loc=(47066,47070)),
                Opt(Seq(Loc("else", loc=(47153,47156)), Loc(":", loc=(47166,47169)), Rule("suite", loc=(47176,47180)), loc=(47149,47152)), loc=(47145,47148)), loc=(46996,46999)), loc=(46989,46995))
    def if_stmt(self, if_loc, test, if_colon_loc, body, elifs, else_opt):
        _all_stmts[(47198,47201)] = True
        """if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]"""
        stmt = ast.If(orelse=[],
                      else_loc=None, else_colon_loc=None)

        if else_opt:
            _all_stmts[(47455,47457)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt

        for elif_ in reversed(elifs):
            _all_stmts[(47548,47551)] = True
            stmt.keyword_loc, stmt.test, stmt.if_colon_loc, stmt.body = elif_
            stmt.loc = stmt.keyword_loc.join(stmt.body[-1].loc)
            if stmt.orelse:
                _all_stmts[(47732,47734)] = True
                stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)
            stmt = ast.If(orelse=[stmt],
                          else_loc=None, else_colon_loc=None)

        stmt.keyword_loc, stmt.test, stmt.if_colon_loc, stmt.body = \
            if_loc, test, if_colon_loc, body
        stmt.loc = stmt.keyword_loc.join(stmt.body[-1].loc)
        if stmt.orelse:
            _all_stmts[(48097,48099)] = True
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)
        return stmt

    @action(Seq(Loc("while", loc=(48208,48211)), Rule("test", loc=(48222,48226)), Loc(":", loc=(48236,48239)), Rule("suite", loc=(48246,48250)),
                Opt(Seq(Loc("else", loc=(48285,48288)), Loc(":", loc=(48298,48301)), Rule("suite", loc=(48308,48312)), loc=(48281,48284)), loc=(48277,48280)), loc=(48204,48207)), loc=(48197,48203))
    def while_stmt(self, while_loc, test, while_colon_loc, body, else_opt):
        _all_stmts[(48330,48333)] = True
        """while_stmt: 'while' test ':' suite ['else' ':' suite]"""
        stmt = ast.While(test=test, body=body, orelse=[],
                         keyword_loc=while_loc, while_colon_loc=while_colon_loc,
                         else_loc=None, else_colon_loc=None,
                         loc=while_loc.join(body[-1].loc))
        if else_opt:
            _all_stmts[(48737,48739)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)

        return stmt

    @action(Seq(Loc("for", loc=(48917,48920)), Rule("exprlist", loc=(48929,48933)), Loc("in", loc=(48947,48950)), Rule("testlist", loc=(48958,48962)),
                Loc(":", loc=(48992,48995)), Rule("suite", loc=(49002,49006)),
                Opt(Seq(Loc("else", loc=(49041,49044)), Loc(":", loc=(49054,49057)), Rule("suite", loc=(49064,49068)), loc=(49037,49040)), loc=(49033,49036)), loc=(48913,48916)), loc=(48906,48912))
    def for_stmt(self, for_loc, target, in_loc, iter, for_colon_loc, body, else_opt):
        _all_stmts[(49086,49089)] = True
        """for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]"""
        stmt = ast.For(target=self._assignable(target), iter=iter, body=body, orelse=[],
                       keyword_loc=for_loc, in_loc=in_loc, for_colon_loc=for_colon_loc,
                       else_loc=None, else_colon_loc=None,
                       loc=for_loc.join(body[-1].loc))
        if else_opt:
            _all_stmts[(49549,49551)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)

        return stmt

    @action(Seq(Plus(Seq(Rule("except_clause", loc=(49738,49742)), Loc(":", loc=(49761,49764)), Rule("suite", loc=(49771,49775)), loc=(49734,49737)), loc=(49729,49733)),
                Opt(Seq(Loc("else", loc=(49812,49815)), Loc(":", loc=(49825,49828)), Rule("suite", loc=(49835,49839)), loc=(49808,49811)), loc=(49804,49807)),
                Opt(Seq(Loc("finally", loc=(49876,49879)), Loc(":", loc=(49892,49895)), Rule("suite", loc=(49902,49906)), loc=(49872,49875)), loc=(49868,49871)), loc=(49725,49728)), loc=(49718,49724))
    def try_stmt_1(self, clauses, else_opt, finally_opt):
        _all_stmts[(49924,49927)] = True
        handlers = []
        for clause in clauses:
            _all_stmts[(50008,50011)] = True
            handler, handler.colon_loc, handler.body = clause
            handler.loc = handler.loc.join(handler.body[-1].loc)
            handlers.append(handler)

        else_loc, else_colon_loc, orelse = None, None, []
        loc = handlers[-1].loc
        if else_opt:
            _all_stmts[(50293,50295)] = True
            else_loc, else_colon_loc, orelse = else_opt
            loc = orelse[-1].loc

        finally_loc, finally_colon_loc, finalbody = None, None, []
        if finally_opt:
            _all_stmts[(50471,50473)] = True
            finally_loc, finally_colon_loc, finalbody = finally_opt
            loc = finalbody[-1].loc
        stmt = ast.Try(body=None, handlers=handlers, orelse=orelse, finalbody=finalbody,
                       else_loc=else_loc, else_colon_loc=else_colon_loc,
                       finally_loc=finally_loc, finally_colon_loc=finally_colon_loc,
                       loc=loc)
        return stmt

    @action(Seq(Loc("finally", loc=(50907,50910)), Loc(":", loc=(50923,50926)), Rule("suite", loc=(50933,50937)), loc=(50903,50906)), loc=(50896,50902))
    def try_stmt_2(self, finally_loc, finally_colon_loc, finalbody):
        _all_stmts[(50953,50956)] = True
        return ast.Try(body=None, handlers=[], orelse=[], finalbody=finalbody,
                       else_loc=None, else_colon_loc=None,
                       finally_loc=finally_loc, finally_colon_loc=finally_colon_loc,
                       loc=finalbody[-1].loc)

    @action(Seq(Loc("try", loc=(51304,51307)), Loc(":", loc=(51316,51319)), Rule("suite", loc=(51326,51330)), Alt(try_stmt_1, try_stmt_2, loc=(51341,51344)), loc=(51300,51303)), loc=(51293,51299))
    def try_stmt(self, try_loc, try_colon_loc, body, stmt):
        _all_stmts[(51375,51378)] = True
        """
        try_stmt: ('try' ':' suite
                   ((except_clause ':' suite)+
                    ['else' ':' suite]
                    ['finally' ':' suite] |
                    'finally' ':' suite))
        """
        stmt.keyword_loc, stmt.try_colon_loc, stmt.body = \
            try_loc, try_colon_loc, body
        stmt.loc = stmt.loc.join(try_loc)
        return stmt

    @action(Seq(Loc("with", loc=(51842,51845)), Rule("test", loc=(51855,51859)), Opt(Rule("with_var", loc=(51873,51877)), loc=(51869,51872)), Loc(":", loc=(51892,51895)), Rule("suite", loc=(51902,51906)), loc=(51838,51841)), loc=(51831,51837))
    def with_stmt__26(self, with_loc, context, with_var, colon_loc, body):
        _all_stmts[(51922,51925)] = True
        """(2.6, 3.0) with_stmt: 'with' test [ with_var ] ':' suite"""
        if with_var:
            _all_stmts[(52072,52074)] = True
            as_loc, optional_vars = with_var
            item = ast.withitem(context_expr=context, optional_vars=optional_vars,
                                as_loc=as_loc, loc=context.loc.join(optional_vars.loc))
        else:
            _all_stmts[(52309,52313)] = True
            item = ast.withitem(context_expr=context, optional_vars=None,
                                as_loc=None, loc=context.loc)
        return ast.With(items=[item], body=body,
                        keyword_loc=with_loc, colon_loc=colon_loc,
                        loc=with_loc.join(body[-1].loc))

    with_var = Seq(Loc("as", loc=(52644,52647)), Rule("expr", loc=(52655,52659)), loc=(52640,52643))
    """(2.6, 3.0) with_var: 'as' expr"""

    @action(Seq(Loc("with", loc=(52727,52730)), List(Rule("with_item", loc=(52745,52749)), ",", trailing=False, loc=(52740,52744)), Loc(":", loc=(52786,52789)),
                Rule("suite", loc=(52812,52816)), loc=(52723,52726)), loc=(52716,52722))
    def with_stmt__27(self, with_loc, items, colon_loc, body):
        _all_stmts[(52832,52835)] = True
        """(2.7, 3.1-) with_stmt: 'with' with_item (',' with_item)*  ':' suite"""
        return ast.With(items=items, body=body,
                        keyword_loc=with_loc, colon_loc=colon_loc,
                        loc=with_loc.join(body[-1].loc))

    @action(Seq(Rule("test", loc=(53162,53166)), Opt(Seq(Loc("as", loc=(53184,53187)), Rule("expr", loc=(53195,53199)), loc=(53180,53183)), loc=(53176,53179)), loc=(53158,53161)), loc=(53151,53157))
    def with_item(self, context, as_opt):
        _all_stmts[(53216,53219)] = True
        """(2.7, 3.1-) with_item: test ['as' expr]"""
        if as_opt:
            _all_stmts[(53316,53318)] = True
            as_loc, optional_vars = as_opt
            return ast.withitem(context_expr=context, optional_vars=optional_vars,
                                as_loc=as_loc, loc=context.loc.join(optional_vars.loc))
        else:
            _all_stmts[(53549,53553)] = True
            return ast.withitem(context_expr=context, optional_vars=None,
                                as_loc=None, loc=context.loc)

    @action(Seq(Alt(Loc("as", loc=(53712,53715)), Loc(",", loc=(53723,53726)), loc=(53708,53711)), Rule("test", loc=(53734,53738)), loc=(53704,53707)), loc=(53697,53703))
    def except_clause_1__26(self, as_loc, name):
        _all_stmts[(53753,53756)] = True
        return as_loc, None, name

    @action(Seq(Loc("as", loc=(53849,53852)), Tok("ident", loc=(53860,53863)), loc=(53845,53848)), loc=(53838,53844))
    def except_clause_1__30(self, as_loc, name):
        _all_stmts[(53879,53882)] = True
        return as_loc, name, None

    @action(Seq(Loc("except", loc=(53975,53978)),
                Opt(Seq(Rule("test", loc=(54014,54018)),
                        Opt(Rule("except_clause_1", loc=(54056,54060)), loc=(54052,54055)), loc=(54010,54013)), loc=(54006,54009)), loc=(53971,53974)), loc=(53964,53970))
    def except_clause(self, except_loc, exc_opt):
        _all_stmts[(54089,54092)] = True
        """
        (2.6, 2.7) except_clause: 'except' [test [('as' | ',') test]]
        (3.0-) except_clause: 'except' [test ['as' NAME]]
        """
        type_ = name = as_loc = name_loc = None
        loc = except_loc
        if exc_opt:
            _all_stmts[(54368,54370)] = True
            type_, name_opt = exc_opt
            loc = loc.join(type_.loc)
            if name_opt:
                _all_stmts[(54468,54470)] = True
                as_loc, name_tok, name_node = name_opt
                if name_tok:
                    _all_stmts[(54552,54554)] = True
                    name = name_tok.value
                    name_loc = name_tok.loc
                else:
                    _all_stmts[(54667,54671)] = True
                    name = name_node
                    name_loc = name_node.loc
                loc = loc.join(name_loc)
        return ast.ExceptHandler(type=type_, name=name,
                                 except_loc=except_loc, as_loc=as_loc, name_loc=name_loc,
                                 loc=loc)

    @action(Plus(Rule("stmt", loc=(55002,55006)), loc=(54997,55001)), loc=(54990,54996))
    def suite_1(self, stmts):
        _all_stmts[(55021,55024)] = True
        return reduce(list.__add__, stmts, [])

    suite = Alt(Rule("simple_stmt", loc=(55111,55115)),
                SeqN(2, Tok("newline", loc=(55156,55159)), Tok("indent", loc=(55172,55175)), suite_1, Tok("dedent", loc=(55196,55199)), loc=(55148,55152)), loc=(55107,55110))
    """suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT"""

    # 2.x-only backwards compatibility start
    testlist_safe = action(List(Rule("old_test", loc=(55349,55353)), ",", trailing=False, loc=(55344,55348)), loc=(55337,55343))(_wrap_tuple)
    """(2.6, 2.7) testlist_safe: old_test [(',' old_test)+ [',']]"""

    old_test = Alt(Rule("or_test", loc=(55491,55495)), Rule("old_lambdef", loc=(55508,55512)), loc=(55487,55490))
    """(2.6, 2.7) old_test: or_test | old_lambdef"""

    @action(Seq(Loc("lambda", loc=(55599,55602)), Opt(Rule("varargslist", loc=(55618,55622)), loc=(55614,55617)), Loc(":", loc=(55640,55643)), Rule("old_test", loc=(55650,55654)), loc=(55595,55598)), loc=(55588,55594))
    def old_lambdef(self, lambda_loc, args_opt, colon_loc, body):
        _all_stmts[(55673,55676)] = True
        """(2.6, 2.7) old_lambdef: 'lambda' [varargslist] ':' old_test"""
        if args_opt is None:
            _all_stmts[(55817,55819)] = True
            args_opt = self._arguments()
            args_opt.loc = colon_loc.begin()
        return ast.Lambda(args=args_opt, body=body,
                          lambda_loc=lambda_loc, colon_loc=colon_loc,
                          loc=lambda_loc.join(body.loc))
    # 2.x-only backwards compatibility end

    @action(Seq(Rule("or_test", loc=(56163,56167)), Opt(Seq(Loc("if", loc=(56188,56191)), Rule("or_test", loc=(56199,56203)),
                                         Loc("else", loc=(56257,56260)), Rule("test", loc=(56270,56274)), loc=(56184,56187)), loc=(56180,56183)), loc=(56159,56162)), loc=(56152,56158))
    def test_1(self, lhs, rhs_opt):
        _all_stmts[(56291,56294)] = True
        if rhs_opt is not None:
            _all_stmts[(56331,56333)] = True
            if_loc, test, else_loc, orelse = rhs_opt
            return ast.IfExp(test=test, body=lhs, orelse=orelse,
                             if_loc=if_loc, else_loc=else_loc, loc=lhs.loc.join(orelse.loc))
        return lhs

    test = Alt(test_1, Rule("lambdef", loc=(56609,56613)), loc=(56597,56600))
    """test: or_test ['if' or_test 'else' test] | lambdef"""

    test_nocond = Alt(Rule("or_test", loc=(56710,56714)), Rule("lambdef_nocond", loc=(56727,56731)), loc=(56706,56709))
    """(3.0-) test_nocond: or_test | lambdef_nocond"""

    def lambdef_action(self, lambda_loc, args_opt, colon_loc, body):
        _all_stmts[(56811,56814)] = True
        if args_opt is None:
            _all_stmts[(56884,56886)] = True
            args_opt = self._arguments()
            args_opt.loc = colon_loc.begin()
        return ast.Lambda(args=args_opt, body=body,
                          lambda_loc=lambda_loc, colon_loc=colon_loc,
                          loc=lambda_loc.join(body.loc))

    lambdef = action(
        Seq(Loc("lambda", loc=(57205,57208)), Opt(Rule("varargslist", loc=(57224,57228)), loc=(57220,57223)), Loc(":", loc=(57246,57249)), Rule("test", loc=(57256,57260)), loc=(57201,57204)), loc=(57185,57191)) \
        (lambdef_action)
    """lambdef: 'lambda' [varargslist] ':' test"""

    lambdef_nocond = action(
        Seq(Loc("lambda", loc=(57391,57394)), Opt(Rule("varargslist", loc=(57410,57414)), loc=(57406,57409)), Loc(":", loc=(57432,57435)), Rule("test_nocond", loc=(57442,57446)), loc=(57387,57390)), loc=(57371,57377)) \
        (lambdef_action)
    """(3.0-) lambdef_nocond: 'lambda' [varargslist] ':' test_nocond"""

    @action(Seq(Rule("and_test", loc=(57580,57584)), Star(Seq(Loc("or", loc=(57607,57610)), Rule("and_test", loc=(57618,57622)), loc=(57603,57606)), loc=(57598,57602)), loc=(57576,57579)), loc=(57569,57575))
    def or_test(self, lhs, rhs):
        _all_stmts[(57643,57646)] = True
        """or_test: and_test ('or' and_test)*"""
        if len(rhs) > 0:
            _all_stmts[(57729,57731)] = True
            return ast.BoolOp(op=ast.Or(),
                              values=[lhs] + list(map(lambda x: x[1], rhs)),
                              loc=lhs.loc.join(rhs[-1][1].loc),
                              op_locs=list(map(lambda x: x[0], rhs)))
        else:
            _all_stmts[(58008,58012)] = True
            return lhs

    @action(Seq(Rule("not_test", loc=(58054,58058)), Star(Seq(Loc("and", loc=(58081,58084)), Rule("not_test", loc=(58093,58097)), loc=(58077,58080)), loc=(58072,58076)), loc=(58050,58053)), loc=(58043,58049))
    def and_test(self, lhs, rhs):
        _all_stmts[(58118,58121)] = True
        """and_test: not_test ('and' not_test)*"""
        if len(rhs) > 0:
            _all_stmts[(58207,58209)] = True
            return ast.BoolOp(op=ast.And(),
                              values=[lhs] + list(map(lambda x: x[1], rhs)),
                              loc=lhs.loc.join(rhs[-1][1].loc),
                              op_locs=list(map(lambda x: x[0], rhs)))
        else:
            _all_stmts[(58487,58491)] = True
            return lhs

    @action(Seq(Oper(ast.Not, "not", loc=(58533,58537)), Rule("not_test", loc=(58555,58559)), loc=(58529,58532)), loc=(58522,58528))
    def not_test_1(self, op, operand):
        _all_stmts[(58578,58581)] = True
        return ast.UnaryOp(op=op, operand=operand,
                           loc=op.loc.join(operand.loc))

    not_test = Alt(not_test_1, Rule("comparison", loc=(58753,58757)), loc=(58737,58740))
    """not_test: 'not' not_test | comparison"""

    comparison_1__26 = Seq(Rule("expr", loc=(58849,58853)), Star(Seq(Rule("comp_op", loc=(58872,58876)), Rule("expr", loc=(58889,58893)), loc=(58868,58871)), loc=(58863,58867)), loc=(58845,58848))
    comparison_1__30 = Seq(Rule("star_expr", loc=(58932,58936)), Star(Seq(Rule("comp_op", loc=(58960,58964)), Rule("star_expr", loc=(58977,58981)), loc=(58956,58959)), loc=(58951,58955)), loc=(58928,58931))
    comparison_1__32 = comparison_1__26

    @action(Rule("comparison_1", loc=(59051,59055)), loc=(59044,59050))
    def comparison(self, lhs, rhs):
        _all_stmts[(59077,59080)] = True
        """
        (2.6, 2.7) comparison: expr (comp_op expr)*
        (3.0, 3.1) comparison: star_expr (comp_op star_expr)*
        (3.2-) comparison: expr (comp_op expr)*
        """
        if len(rhs) > 0:
            _all_stmts[(59303,59305)] = True
            return ast.Compare(left=lhs, ops=list(map(lambda x: x[0], rhs)),
                               comparators=list(map(lambda x: x[1], rhs)),
                               loc=lhs.loc.join(rhs[-1][1].loc))
        else:
            _all_stmts[(59545,59549)] = True
            return lhs

    @action(Seq(Opt(Loc("*", loc=(59595,59598)), loc=(59591,59594)), Rule("expr", loc=(59606,59610)), loc=(59587,59590)), loc=(59580,59586))
    def star_expr__30(self, star_opt, expr):
        _all_stmts[(59625,59628)] = True
        """(3.0, 3.1) star_expr: ['*'] expr"""
        if star_opt:
            _all_stmts[(59721,59723)] = True
            return ast.Starred(value=expr, ctx=None,
                               star_loc=star_opt, loc=expr.loc.join(star_opt))
        return expr

    @action(Seq(Loc("*", loc=(59903,59906)), Rule("expr", loc=(59913,59917)), loc=(59899,59902)), loc=(59892,59898))
    def star_expr__32(self, star_loc, expr):
        _all_stmts[(59932,59935)] = True
        """(3.0-) star_expr: '*' expr"""
        return ast.Starred(value=expr, ctx=None,
                           star_loc=star_loc, loc=expr.loc.join(star_loc))

    comp_op = Alt(Oper(ast.Lt, "<", loc=(60157,60161)), Oper(ast.Gt, ">", loc=(60176,60180)), Oper(ast.Eq, "==", loc=(60195,60199)),
                  Oper(ast.GtE, ">=", loc=(60233,60237)), Oper(ast.LtE, "<=", loc=(60254,60258)), Oper(ast.NotEq, "<>", loc=(60275,60279)),
                  Oper(ast.NotEq, "!=", loc=(60316,60320)),
                  Oper(ast.In, "in", loc=(60357,60361)), Oper(ast.NotIn, "not", "in", loc=(60377,60381)),
                  Oper(ast.IsNot, "is", "not", loc=(60425,60429)), Oper(ast.Is, "is", loc=(60455,60459)), loc=(60153,60156))
    """
    (2.6, 2.7) comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
    (3.0-) comp_op: '<'|'>'|'=='|'>='|'<='|'!='|'in'|'not' 'in'|'is'|'is' 'not'
    """

    expr = BinOper("xor_expr", Oper(ast.BitOr, "|", loc=(60692,60696)), loc=(60672,60679))
    """expr: xor_expr ('|' xor_expr)*"""

    xor_expr = BinOper("and_expr", Oper(ast.BitXor, "^", loc=(60791,60795)), loc=(60771,60778))
    """xor_expr: and_expr ('^' and_expr)*"""

    and_expr = BinOper("shift_expr", Oper(ast.BitAnd, "&", loc=(60897,60901)), loc=(60875,60882))
    """and_expr: shift_expr ('&' shift_expr)*"""

    shift_expr = BinOper("arith_expr", Alt(Oper(ast.LShift, "<<", loc=(61013,61017)), Oper(ast.RShift, ">>", loc=(61037,61041)), loc=(61009,61012)), loc=(60987,60994))
    """shift_expr: arith_expr (('<<'|'>>') arith_expr)*"""

    arith_expr = BinOper("term", Alt(Oper(ast.Add, "+", loc=(61159,61163)), Oper(ast.Sub, "-", loc=(61179,61183)), loc=(61155,61158)), loc=(61139,61146))
    """arith_expr: term (('+'|'-') term)*"""

    term = BinOper("factor", Alt(Oper(ast.Mult, "*", loc=(61279,61283)), Oper(ast.MatMult, "@", loc=(61300,61304)),
                                 Oper(ast.Div, "/", loc=(61357,61361)), Oper(ast.Mod, "%", loc=(61377,61381)),
                                 Oper(ast.FloorDiv, "//", loc=(61430,61434)), loc=(61275,61278)), loc=(61257,61264))
    """term: factor (('*'|'/'|'%'|'//') factor)*"""

    @action(Seq(Alt(Oper(ast.UAdd, "+", loc=(61530,61534)), Oper(ast.USub, "-", loc=(61551,61555)), Oper(ast.Invert, "~", loc=(61572,61576)), loc=(61526,61529)),
                Rule("factor", loc=(61612,61616)), loc=(61522,61525)), loc=(61515,61521))
    def factor_1(self, op, factor):
        _all_stmts[(61633,61636)] = True
        return ast.UnaryOp(op=op, operand=factor,
                           loc=op.loc.join(factor.loc))

    factor = Alt(factor_1, Rule("power", loc=(61799,61803)), loc=(61785,61788))
    """factor: ('+'|'-'|'~') factor | power"""

    @action(Seq(Rule("atom", loc=(61878,61882)), Star(Rule("trailer", loc=(61897,61901)), loc=(61892,61896)), Opt(Seq(Loc("**", loc=(61923,61926)), Rule("factor", loc=(61934,61938)), loc=(61919,61922)), loc=(61915,61918)), loc=(61874,61877)), loc=(61867,61873))
    def power(self, atom, trailers, factor_opt):
        _all_stmts[(61957,61960)] = True
        """power: atom trailer* ['**' factor]"""
        for trailer in trailers:
            _all_stmts[(62059,62062)] = True
            if isinstance(trailer, ast.Attribute) or isinstance(trailer, ast.Subscript):
                _all_stmts[(62096,62098)] = True
                trailer.value = atom
            elif isinstance(trailer, ast.Call):
                _all_stmts[(62222,62226)] = True
                trailer.func = atom
            trailer.loc = atom.loc.join(trailer.loc)
            atom = trailer
        if factor_opt:
            _all_stmts[(62382,62384)] = True
            op_loc, factor = factor_opt
            return ast.BinOp(left=atom, op=ast.Pow(loc=op_loc), right=factor,
                             loc=atom.loc.join(factor.loc))
        return atom

    @action(Rule("testlist1", loc=(62608,62612)), loc=(62601,62607))
    def atom_1(self, expr):
        _all_stmts[(62631,62634)] = True
        return ast.Repr(value=expr, loc=None)

    @action(Tok("ident", loc=(62714,62717)), loc=(62707,62713))
    def atom_2(self, tok):
        _all_stmts[(62732,62735)] = True
        return ast.Name(id=tok.value, loc=tok.loc, ctx=None)

    @action(Alt(Tok("int", loc=(62833,62836)), Tok("float", loc=(62845,62848)), Tok("complex", loc=(62859,62862)), loc=(62829,62832)), loc=(62822,62828))
    def atom_3(self, tok):
        _all_stmts[(62880,62883)] = True
        return ast.Num(n=tok.value, loc=tok.loc)

    @action(Seq(Tok("strbegin", loc=(62969,62972)), Tok("strdata", loc=(62986,62989)), Tok("strend", loc=(63002,63005)), loc=(62965,62968)), loc=(62958,62964))
    def atom_4(self, begin_tok, data_tok, end_tok):
        _all_stmts[(63022,63025)] = True
        return ast.Str(s=data_tok.value,
                       begin_loc=begin_tok.loc, end_loc=end_tok.loc,
                       loc=begin_tok.loc.join(end_tok.loc))

    @action(Plus(atom_4, loc=(63253,63257)), loc=(63246,63252))
    def atom_5(self, strings):
        _all_stmts[(63271,63274)] = True
        return ast.Str(s="".join([x.s for x in strings]),
                       begin_loc=strings[0].begin_loc, end_loc=strings[-1].end_loc,
                       loc=strings[0].loc.join(strings[-1].loc))

    atom_6__26 = Rule("dictmaker", loc=(63523,63527))
    atom_6__27 = Rule("dictorsetmaker", loc=(63558,63562))

    atom__26 = Alt(BeginEnd("(", Opt(Alt(Rule("yield_expr", loc=(63623,63627)), Rule("testlist_comp", loc=(63643,63647)), loc=(63619,63622)), loc=(63615,63618)), ")",
                            empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(63601,63609)),
                   BeginEnd("[", Opt(Rule("listmaker", loc=(63798,63802)), loc=(63794,63797)), "]",
                            empty=lambda self: ast.List(elts=[], ctx=None, loc=None), loc=(63780,63788)),
                   BeginEnd("{", Opt(Rule("atom_6", loc=(63947,63951)), loc=(63943,63946)), "}",
                            empty=lambda self: ast.Dict(keys=[], values=[], colon_locs=[],
                                                        loc=None), loc=(63929,63937)),
                   BeginEnd("`", atom_1, "`", loc=(64147,64155)),
                   atom_2, atom_3, atom_5, loc=(63597,63600))
    """
    (2.6)
    atom: ('(' [yield_expr|testlist_gexp] ')' |
           '[' [listmaker] ']' |
           '{' [dictmaker] '}' |
           '`' testlist1 '`' |
           NAME | NUMBER | STRING+)
    (2.7)
    atom: ('(' [yield_expr|testlist_comp] ')' |
           '[' [listmaker] ']' |
           '{' [dictorsetmaker] '}' |
           '`' testlist1 '`' |
           NAME | NUMBER | STRING+)
    """

    @action(Loc("...", loc=(64634,64637)), loc=(64627,64633))
    def atom_7(self, loc):
        _all_stmts[(64650,64653)] = True
        return ast.Ellipsis(loc=loc)

    @action(Alt(Tok("None", loc=(64727,64730)), Tok("True", loc=(64740,64743)), Tok("False", loc=(64753,64756)), loc=(64723,64726)), loc=(64716,64722))
    def atom_8(self, tok):
        _all_stmts[(64772,64775)] = True
        if tok.kind == "None":
            _all_stmts[(64803,64805)] = True
            value = None
        elif tok.kind == "True":
            _all_stmts[(64859,64863)] = True
            value = True
        elif tok.kind == "False":
            _all_stmts[(64917,64921)] = True
            value = False
        return ast.NameConstant(value=value, loc=tok.loc)

    atom__30 = Alt(BeginEnd("(", Opt(Alt(Rule("yield_expr", loc=(65069,65073)), Rule("testlist_comp", loc=(65089,65093)), loc=(65065,65068)), loc=(65061,65064)), ")",
                            empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(65047,65055)),
                   BeginEnd("[", Opt(Rule("testlist_comp__list", loc=(65244,65248)), loc=(65240,65243)), "]",
                            empty=lambda self: ast.List(elts=[], ctx=None, loc=None), loc=(65226,65234)),
                   BeginEnd("{", Opt(Rule("dictorsetmaker", loc=(65403,65407)), loc=(65399,65402)), "}",
                            empty=lambda self: ast.Dict(keys=[], values=[], colon_locs=[],
                                                        loc=None), loc=(65385,65393)),
                   atom_2, atom_3, atom_5, atom_7, atom_8, loc=(65043,65046))
    """
    (3.0-)
    atom: ('(' [yield_expr|testlist_comp] ')' |
           '[' [testlist_comp] ']' |
           '{' [dictorsetmaker] '}' |
           NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False')
    """

    def list_gen_action(self, lhs, rhs):
        _all_stmts[(65878,65881)] = True
        if rhs is None: # (x)
            _all_stmts[(65923,65925)] = True
            return lhs
        elif isinstance(rhs, ast.Tuple) or isinstance(rhs, ast.List):
            _all_stmts[(65976,65980)] = True
            rhs.elts = [lhs] + rhs.elts
            return rhs
        elif isinstance(rhs, ast.ListComp) or isinstance(rhs, ast.GeneratorExp):
            _all_stmts[(66109,66113)] = True
            rhs.elt = lhs
            return rhs

    @action(Rule("list_for", loc=(66244,66248)), loc=(66237,66243))
    def listmaker_1(self, compose):
        _all_stmts[(66266,66269)] = True
        return ast.ListComp(generators=compose([]), loc=None)

    @action(List(Rule("test", loc=(66378,66382)), ",", trailing=True, leading=False, loc=(66373,66377)), loc=(66366,66372))
    def listmaker_2(self, elts):
        _all_stmts[(66432,66435)] = True
        return ast.List(elts=elts, ctx=None, loc=None)

    listmaker = action(
        Seq(Rule("test", loc=(66553,66557)),
            Alt(listmaker_1, listmaker_2, loc=(66579,66582)), loc=(66549,66552)), loc=(66533,66539)) \
        (list_gen_action)
    """listmaker: test ( list_for | (',' test)* [','] )"""

    testlist_comp_1__26 = Rule("test", loc=(66725,66729))
    testlist_comp_1__32 = Alt(Rule("test", loc=(66768,66772)), Rule("star_expr", loc=(66782,66786)), loc=(66764,66767))

    @action(Rule("comp_for", loc=(66814,66818)), loc=(66807,66813))
    def testlist_comp_2(self, compose):
        _all_stmts[(66836,66839)] = True
        return ast.GeneratorExp(generators=compose([]), loc=None)

    @action(List(Rule("testlist_comp_1", loc=(66956,66960)), ",", trailing=True, leading=False, loc=(66951,66955)), loc=(66944,66950))
    def testlist_comp_3(self, elts):
        _all_stmts[(67021,67024)] = True
        if elts == [] and not elts.trailing_comma:
            _all_stmts[(67062,67064)] = True
            return None
        else:
            _all_stmts[(67137,67141)] = True
            return ast.Tuple(elts=elts, ctx=None, loc=None)

    testlist_comp = action(
        Seq(Rule("testlist_comp_1", loc=(67244,67248)), Alt(testlist_comp_2, testlist_comp_3, loc=(67269,67272)), loc=(67240,67243)), loc=(67224,67230)) \
        (list_gen_action)
    """
    (2.6) testlist_gexp: test ( gen_for | (',' test)* [','] )
    (2.7, 3.0, 3.1) testlist_comp: test ( comp_for | (',' test)* [','] )
    (3.2-) testlist_comp: (test|star_expr) ( comp_for | (',' (test|star_expr))* [','] )
    """

    @action(Rule("comp_for", loc=(67589,67593)), loc=(67582,67588))
    def testlist_comp__list_1(self, compose):
        _all_stmts[(67611,67614)] = True
        return ast.ListComp(generators=compose([]), loc=None)

    @action(List(Rule("testlist_comp_1", loc=(67733,67737)), ",", trailing=True, leading=False, loc=(67728,67732)), loc=(67721,67727))
    def testlist_comp__list_2(self, elts):
        _all_stmts[(67798,67801)] = True
        return ast.List(elts=elts, ctx=None, loc=None)

    testlist_comp__list = action(
        Seq(Rule("testlist_comp_1", loc=(67939,67943)), Alt(testlist_comp__list_1, testlist_comp__list_2, loc=(67964,67967)), loc=(67935,67938)), loc=(67919,67925)) \
        (list_gen_action)
    """Same grammar as testlist_comp, but different semantic action."""

    @action(Seq(Loc(".", loc=(68133,68136)), Tok("ident", loc=(68143,68146)), loc=(68129,68132)), loc=(68122,68128))
    def trailer_1(self, dot_loc, ident_tok):
        _all_stmts[(68162,68165)] = True
        return ast.Attribute(attr=ident_tok.value, ctx=None,
                             loc=dot_loc.join(ident_tok.loc),
                             attr_loc=ident_tok.loc, dot_loc=dot_loc)

    trailer = Alt(BeginEnd("(", Opt(Rule("arglist", loc=(68433,68437)), loc=(68429,68432)), ")",
                           empty=_empty_arglist, loc=(68415,68423)),
                  BeginEnd("[", Rule("subscriptlist", loc=(68538,68542)), "]", loc=(68524,68532)),
                  trailer_1, loc=(68411,68414))
    """trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME"""

    @action(List(Rule("subscript", loc=(68686,68690)), ",", trailing=True, loc=(68681,68685)), loc=(68674,68680))
    def subscriptlist(self, subscripts):
        _all_stmts[(68730,68733)] = True
        """subscriptlist: subscript (',' subscript)* [',']"""
        if len(subscripts) == 1:
            _all_stmts[(68837,68839)] = True
            return ast.Subscript(slice=subscripts[0], ctx=None, loc=None)
        elif all([isinstance(x, ast.Index) for x in subscripts]):
            _all_stmts[(68944,68948)] = True
            elts  = [x.value for x in subscripts]
            loc   = subscripts[0].loc.join(subscripts[-1].loc)
            index = ast.Index(value=ast.Tuple(elts=elts, ctx=None,
                                              begin_loc=None, end_loc=None, loc=loc),
                              loc=loc)
            return ast.Subscript(slice=index, ctx=None, loc=None)
        else:
            _all_stmts[(69381,69385)] = True
            extslice = ast.ExtSlice(dims=subscripts,
                                    loc=subscripts[0].loc.join(subscripts[-1].loc))
            return ast.Subscript(slice=extslice, ctx=None, loc=None)

    @action(Seq(Loc(".", loc=(69610,69613)), Loc(".", loc=(69620,69623)), Loc(".", loc=(69630,69633)), loc=(69606,69609)), loc=(69599,69605))
    def subscript_1(self, dot_1_loc, dot_2_loc, dot_3_loc):
        _all_stmts[(69645,69648)] = True
        return ast.Ellipsis(loc=dot_1_loc.join(dot_3_loc))

    @action(Seq(Opt(Rule("test", loc=(69781,69785)), loc=(69777,69780)), Loc(":", loc=(69796,69799)), Opt(Rule("test", loc=(69810,69814)), loc=(69806,69809)), Opt(Rule("sliceop", loc=(69829,69833)), loc=(69825,69828)), loc=(69773,69776)), loc=(69766,69772))
    def subscript_2(self, lower_opt, colon_loc, upper_opt, step_opt):
        _all_stmts[(69852,69855)] = True
        loc = colon_loc
        if lower_opt:
            _all_stmts[(69950,69952)] = True
            loc = loc.join(lower_opt.loc)
        if upper_opt:
            _all_stmts[(70014,70016)] = True
            loc = loc.join(upper_opt.loc)
        step_colon_loc = step = None
        if step_opt:
            _all_stmts[(70115,70117)] = True
            step_colon_loc, step = step_opt
            loc = loc.join(step_colon_loc)
            if step:
                _all_stmts[(70227,70229)] = True
                loc = loc.join(step.loc)
        return ast.Slice(lower=lower_opt, upper=upper_opt, step=step,
                         loc=loc, bound_colon_loc=colon_loc, step_colon_loc=step_colon_loc)

    @action(Rule("test", loc=(70452,70456)), loc=(70445,70451))
    def subscript_3(self, expr):
        _all_stmts[(70470,70473)] = True
        return ast.Index(value=expr, loc=expr.loc)

    subscript__26 = Alt(subscript_1, subscript_2, subscript_3, loc=(70571,70574))
    """(2.6, 2.7) subscript: '.' '.' '.' | test | [test] ':' [test] [sliceop]"""

    subscript__30 = Alt(subscript_2, subscript_3, loc=(70716,70719))
    """(3.0-) subscript: test | [test] ':' [test] [sliceop]"""

    sliceop = Seq(Loc(":", loc=(70828,70831)), Opt(Rule("test", loc=(70842,70846)), loc=(70838,70841)), loc=(70824,70827))
    """sliceop: ':' [test]"""

    exprlist_1__26 = List(Rule("expr", loc=(70914,70918)), ",", trailing=True, loc=(70909,70913))
    exprlist_1__30 = List(Rule("star_expr", loc=(70974,70978)), ",", trailing=True, loc=(70969,70973))
    exprlist_1__32 = List(Alt(Rule("expr", loc=(71043,71047)), Rule("star_expr", loc=(71057,71061)), loc=(71039,71042)), ",", trailing=True, loc=(71034,71038))

    @action(Rule("exprlist_1", loc=(71110,71114)), loc=(71103,71109))
    def exprlist(self, exprs):
        _all_stmts[(71134,71137)] = True
        """
        (2.6, 2.7) exprlist: expr (',' expr)* [',']
        (3.0, 3.1) exprlist: star_expr (',' star_expr)* [',']
        (3.2-) exprlist: (expr|star_expr) (',' (expr|star_expr))* [',']
        """
        return self._wrap_tuple(exprs)

    @action(List(Rule("test", loc=(71428,71432)), ",", trailing=True, loc=(71423,71427)), loc=(71416,71422))
    def testlist(self, exprs):
        _all_stmts[(71467,71470)] = True
        """testlist: test (',' test)* [',']"""
        return self._wrap_tuple(exprs)

    @action(List(Seq(Rule("test", loc=(71602,71606)), Loc(":", loc=(71616,71619)), Rule("test", loc=(71626,71630)), loc=(71598,71601)), ",", trailing=True, loc=(71593,71597)), loc=(71586,71592))
    def dictmaker(self, elts):
        _all_stmts[(71666,71669)] = True
        """(2.6) dictmaker: test ':' test (',' test ':' test)* [',']"""
        return ast.Dict(keys=list(map(lambda x: x[0], elts)),
                        values=list(map(lambda x: x[2], elts)),
                        colon_locs=list(map(lambda x: x[1], elts)),
                        loc=None)

    dictorsetmaker_1 = Seq(Rule("test", loc=(72021,72025)), Loc(":", loc=(72035,72038)), Rule("test", loc=(72045,72049)), loc=(72017,72020))

    @action(Seq(dictorsetmaker_1,
                Alt(Rule("comp_for", loc=(72114,72118)),
                    List(dictorsetmaker_1, ",", leading=False, trailing=True, loc=(72152,72156)), loc=(72110,72113)), loc=(72072,72075)), loc=(72065,72071))
    def dictorsetmaker_2(self, first, elts):
        _all_stmts[(72217,72220)] = True
        if isinstance(elts, commalist):
            _all_stmts[(72266,72268)] = True
            elts.insert(0, first)
            return ast.Dict(keys=list(map(lambda x: x[0], elts)),
                            values=list(map(lambda x: x[2], elts)),
                            colon_locs=list(map(lambda x: x[1], elts)),
                            loc=None)
        else:
            _all_stmts[(72584,72588)] = True
            return ast.DictComp(key=first[0], value=first[2], generators=elts([]),
                                colon_loc=first[1],
                                begin_loc=None, end_loc=None, loc=None)

    @action(Seq(Rule("test", loc=(72814,72818)),
                Alt(Rule("comp_for", loc=(72848,72852)),
                    List(Rule("test", loc=(72891,72895)), ",", leading=False, trailing=True, loc=(72886,72890)), loc=(72844,72847)), loc=(72810,72813)), loc=(72803,72809))
    def dictorsetmaker_3(self, first, elts):
        _all_stmts[(72947,72950)] = True
        if isinstance(elts, commalist):
            _all_stmts[(72996,72998)] = True
            elts.insert(0, first)
            return ast.Set(elts=elts, loc=None)
        else:
            _all_stmts[(73118,73122)] = True
            return ast.SetComp(elt=first, generators=elts([]),
                               begin_loc=None, end_loc=None, loc=None)

    dictorsetmaker = Alt(dictorsetmaker_2, dictorsetmaker_3, loc=(73280,73283))
    """
    (2.7-)
    dictorsetmaker: ( (test ':' test (comp_for | (',' test ':' test)* [','])) |
                      (test (comp_for | (',' test)* [','])) )
    """

    @action(Seq(Loc("class", loc=(73506,73509)), Tok("ident", loc=(73520,73523)),
                Opt(Seq(Loc("(", loc=(73558,73561)), List(Rule("test", loc=(73573,73577)), ",", trailing=True, loc=(73568,73572)), Loc(")", loc=(73608,73611)), loc=(73554,73557)), loc=(73550,73553)),
                Loc(":", loc=(73636,73639)), Rule("suite", loc=(73646,73650)), loc=(73502,73505)), loc=(73495,73501))
    def classdef__26(self, class_loc, name_tok, bases_opt, colon_loc, body):
        _all_stmts[(73666,73669)] = True
        """(2.6, 2.7) classdef: 'class' NAME ['(' [testlist] ')'] ':' suite"""
        bases, lparen_loc, rparen_loc = [], None, None
        if bases_opt:
            _all_stmts[(73881,73883)] = True
            lparen_loc, bases, rparen_loc = bases_opt

        return ast.ClassDef(name=name_tok.value, bases=bases, keywords=[],
                            starargs=None, kwargs=None, body=body,
                            decorator_list=[], at_locs=[],
                            keyword_loc=class_loc, lparen_loc=lparen_loc,
                            star_loc=None, dstar_loc=None, rparen_loc=rparen_loc,
                            name_loc=name_tok.loc, colon_loc=colon_loc,
                            loc=class_loc.join(body[-1].loc))

    @action(Seq(Loc("class", loc=(74458,74461)), Tok("ident", loc=(74472,74475)),
                Opt(Seq(Loc("(", loc=(74510,74513)), Rule("arglist", loc=(74520,74524)), Loc(")", loc=(74537,74540)), loc=(74506,74509)), loc=(74502,74505)),
                Loc(":", loc=(74565,74568)), Rule("suite", loc=(74575,74579)), loc=(74454,74457)), loc=(74447,74453))
    def classdef__30(self, class_loc, name_tok, arglist_opt, colon_loc, body):
        _all_stmts[(74595,74598)] = True
        """(3.0) classdef: 'class' NAME ['(' [testlist] ')'] ':' suite"""
        arglist, lparen_loc, rparen_loc = [], None, None
        bases, keywords, starargs, kwargs = [], [], None, None
        star_loc, dstar_loc = None, None
        if arglist_opt:
            _all_stmts[(74913,74915)] = True
            lparen_loc, arglist, rparen_loc = arglist_opt
            bases, keywords, starargs, kwargs = \
                arglist.args, arglist.keywords, arglist.starargs, arglist.kwargs
            star_loc, dstar_loc = arglist.star_loc, arglist.dstar_loc

        return ast.ClassDef(name=name_tok.value, bases=bases, keywords=keywords,
                            starargs=starargs, kwargs=kwargs, body=body,
                            decorator_list=[], at_locs=[],
                            keyword_loc=class_loc, lparen_loc=lparen_loc,
                            star_loc=star_loc, dstar_loc=dstar_loc, rparen_loc=rparen_loc,
                            name_loc=name_tok.loc, colon_loc=colon_loc,
                            loc=class_loc.join(body[-1].loc))

    @action(Seq(Loc("*", loc=(75718,75721)), Rule("test", loc=(75728,75732)), Star(SeqN(1, Tok(",", loc=(75755,75758)), Rule("argument", loc=(75765,75769)), loc=(75747,75751)), loc=(75742,75746)),
                Opt(Seq(Tok(",", loc=(75809,75812)), Loc("**", loc=(75819,75822)), Rule("test", loc=(75830,75834)), loc=(75805,75808)), loc=(75801,75804)), loc=(75714,75717)), loc=(75707,75713))
    def arglist_1(self, star_loc, stararg, postargs, kwarg_opt):
        _all_stmts[(75851,75854)] = True
        dstar_loc = kwarg = None
        if kwarg_opt:
            _all_stmts[(75953,75955)] = True
            _, dstar_loc, kwarg = kwarg_opt

        for postarg in postargs:
            _all_stmts[(76020,76023)] = True
            if not isinstance(postarg, ast.keyword):
                _all_stmts[(76057,76059)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "only named arguments may follow *expression", {},
                    postarg.loc, [star_loc.join(stararg.loc)])
                self.diagnostic_engine.process(error)

        return postargs, \
               ast.Call(args=[], keywords=[], starargs=stararg, kwargs=kwarg,
                        star_loc=star_loc, dstar_loc=dstar_loc, loc=None)

    @action(Seq(Loc("**", loc=(76539,76542)), Rule("test", loc=(76550,76554)), loc=(76535,76538)), loc=(76528,76534))
    def arglist_2(self, dstar_loc, kwarg):
        _all_stmts[(76569,76572)] = True
        return [], \
               ast.Call(args=[], keywords=[], starargs=None, kwargs=kwarg,
                        star_loc=None, dstar_loc=dstar_loc, loc=None)

    @action(Seq(Rule("argument", loc=(76791,76795)),
                Alt(SeqN(1, Tok(",", loc=(76837,76840)), Alt(Rule("arglist_1", loc=(76851,76855)),
                                          Rule("arglist_2", loc=(76912,76916)),
                                          Rule("arglist_3", loc=(76973,76977)),
                                          Eps(loc=(77034,77037)), loc=(76847,76850)), loc=(76829,76833)),
                    Eps(loc=(77063,77066)), loc=(76825,76828)), loc=(76787,76790)), loc=(76780,76786))
    def arglist_3(self, arg, cont):
        _all_stmts[(77076,77079)] = True
        if cont is None:
            _all_stmts[(77116,77118)] = True
            return [arg], self._empty_arglist()
        else:
            _all_stmts[(77189,77193)] = True
            args, rest = cont
            return [arg] + args, rest

    @action(Alt(Rule("arglist_1", loc=(77280,77284)),
                Rule("arglist_2", loc=(77315,77319)),
                Rule("arglist_3", loc=(77350,77354)), loc=(77276,77279)), loc=(77269,77275))
    def arglist(self, args, call):
        _all_stmts[(77374,77377)] = True
        """arglist: (argument ',')* (argument [','] |
                                     '*' test (',' argument)* [',' '**' test] |
                                     '**' test)"""
        for arg in args:
            _all_stmts[(77598,77601)] = True
            if isinstance(arg, ast.keyword):
                _all_stmts[(77627,77629)] = True
                call.keywords.append(arg)
            elif len(call.keywords) > 0:
                _all_stmts[(77714,77718)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "non-keyword arg after keyword arg", {},
                    arg.loc, [call.keywords[-1].loc])
                self.diagnostic_engine.process(error)
            else:
                _all_stmts[(77980,77984)] = True
                call.args.append(arg)
        return call

    @action(Seq(Loc("=", loc=(78061,78064)), Rule("test", loc=(78071,78075)), loc=(78057,78060)), loc=(78050,78056))
    def argument_1(self, equals_loc, rhs):
        _all_stmts[(78090,78093)] = True
        def thunk(lhs):
            _all_stmts[(78137,78140)] = True
            if not isinstance(lhs, ast.Name):
                _all_stmts[(78165,78167)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "keyword must be an identifier", {}, lhs.loc)
                self.diagnostic_engine.process(error)
            return ast.keyword(arg=lhs.id, value=rhs,
                               loc=lhs.loc.join(rhs.loc),
                               arg_loc=lhs.loc, equals_loc=equals_loc)
        return thunk

    @action(Opt(Rule("comp_for", loc=(78596,78600)), loc=(78592,78595)), loc=(78585,78591))
    def argument_2(self, compose_opt):
        _all_stmts[(78619,78622)] = True
        def thunk(lhs):
            _all_stmts[(78662,78665)] = True
            if compose_opt:
                _all_stmts[(78690,78692)] = True
                generators = compose_opt([])
                return ast.GeneratorExp(elt=lhs, generators=generators,
                                        begin_loc=None, end_loc=None,
                                        loc=lhs.loc.join(generators[-1].loc))
            return lhs
        return thunk

    @action(Seq(Rule("test", loc=(79032,79036)), Alt(argument_1, argument_2, loc=(79046,79049)), loc=(79028,79031)), loc=(79021,79027))
    def argument(self, lhs, thunk):
        # This rule is reformulated to avoid exponential backtracking.
        _all_stmts[(79080,79083)] = True
        """
        (2.6) argument: test [gen_for] | test '=' test  # Really [keyword '='] test
        (2.7-) argument: test [comp_for] | test '=' test
        """
        return thunk(lhs)

    list_iter = Alt(Rule("list_for", loc=(79395,79399)), Rule("list_if", loc=(79413,79417)), loc=(79391,79394))
    """(2.6, 2.7) list_iter: list_for | list_if"""

    def list_comp_for_action(self, for_loc, target, in_loc, iter, next_opt):
        _all_stmts[(79486,79489)] = True
        def compose(comprehensions):
            _all_stmts[(79567,79570)] = True
            comp = ast.comprehension(
                target=target, iter=iter, ifs=[],
                loc=for_loc.join(iter.loc), for_loc=for_loc, in_loc=in_loc, if_locs=[])
            comprehensions += [comp]
            if next_opt:
                _all_stmts[(79821,79823)] = True
                return next_opt(comprehensions)
            else:
                _all_stmts[(79894,79898)] = True
                return comprehensions
        return compose

    def list_comp_if_action(self, if_loc, cond, next_opt):
        _all_stmts[(79966,79969)] = True
        def compose(comprehensions):
            _all_stmts[(80029,80032)] = True
            comprehensions[-1].ifs.append(cond)
            comprehensions[-1].if_locs.append(if_loc)
            comprehensions[-1].loc = comprehensions[-1].loc.join(cond.loc)
            if next_opt:
                _all_stmts[(80247,80249)] = True
                return next_opt(comprehensions)
            else:
                _all_stmts[(80320,80324)] = True
                return comprehensions
        return compose

    list_for = action(
        Seq(Loc("for", loc=(80423,80426)), Rule("exprlist", loc=(80435,80439)),
            Loc("in", loc=(80465,80468)), Rule("testlist_safe", loc=(80476,80480)), Opt(Rule("list_iter", loc=(80503,80507)), loc=(80499,80502)), loc=(80419,80422)), loc=(80403,80409)) \
        (list_comp_for_action)
    """(2.6, 2.7) list_for: 'for' exprlist 'in' testlist_safe [list_iter]"""

    list_if = action(
        Seq(Loc("if", loc=(80669,80672)), Rule("old_test", loc=(80680,80684)), Opt(Rule("list_iter", loc=(80702,80706)), loc=(80698,80701)), loc=(80665,80668)), loc=(80649,80655)) \
        (list_comp_if_action)
    """(2.6, 2.7) list_if: 'if' old_test [list_iter]"""

    comp_iter = Alt(Rule("comp_for", loc=(80832,80836)), Rule("comp_if", loc=(80850,80854)), loc=(80828,80831))
    """
    (2.6) gen_iter: gen_for | gen_if
    (2.7-) comp_iter: comp_for | comp_if
    """

    comp_for = action(
        Seq(Loc("for", loc=(80997,81000)), Rule("exprlist", loc=(81009,81013)),
            Loc("in", loc=(81039,81042)), Rule("or_test", loc=(81050,81054)), Opt(Rule("comp_iter", loc=(81071,81075)), loc=(81067,81070)), loc=(80993,80996)), loc=(80977,80983)) \
        (list_comp_for_action)
    """
    (2.6) gen_for: 'for' exprlist 'in' or_test [gen_iter]
    (2.7-) comp_for: 'for' exprlist 'in' or_test [comp_iter]
    """

    comp_if__26 = action(
        Seq(Loc("if", loc=(81299,81302)), Rule("old_test", loc=(81310,81314)), Opt(Rule("comp_iter", loc=(81332,81336)), loc=(81328,81331)), loc=(81295,81298)), loc=(81279,81285)) \
        (list_comp_if_action)
    """
    (2.6) gen_if: 'if' old_test [gen_iter]
    (2.7) comp_if: 'if' old_test [comp_iter]
    """

    comp_if__30 = action(
        Seq(Loc("if", loc=(81528,81531)), Rule("test_nocond", loc=(81539,81543)), Opt(Rule("comp_iter", loc=(81564,81568)), loc=(81560,81563)), loc=(81524,81527)), loc=(81508,81514)) \
        (list_comp_if_action)
    """
    (3.0-) comp_if: 'if' test_nocond [comp_iter]
    """

    testlist1 = action(List(Rule("test", loc=(81711,81715)), ",", trailing=False, loc=(81706,81710)), loc=(81699,81705))(_wrap_tuple)
    """testlist1: test (',' test)*"""

    @action(Seq(Loc("yield", loc=(81815,81818)), Opt(Rule("testlist", loc=(81833,81837)), loc=(81829,81832)), loc=(81811,81814)), loc=(81804,81810))
    def yield_expr__26(self, yield_loc, exprs):
        _all_stmts[(81857,81860)] = True
        """(2.6, 2.7, 3.0, 3.1, 3.2) yield_expr: 'yield' [testlist]"""
        if exprs is not None:
            _all_stmts[(81980,81982)] = True
            return ast.Yield(value=exprs,
                             yield_loc=yield_loc, loc=yield_loc.join(exprs.loc))
        else:
            _all_stmts[(82133,82137)] = True
            return ast.Yield(value=None,
                             yield_loc=yield_loc, loc=yield_loc)

    @action(Seq(Loc("yield", loc=(82262,82265)), Opt(Rule("yield_arg", loc=(82280,82284)), loc=(82276,82279)), loc=(82258,82261)), loc=(82251,82257))
    def yield_expr__33(self, yield_loc, arg):
        _all_stmts[(82305,82308)] = True
        """(3.3-) yield_expr: 'yield' [yield_arg]"""
        if isinstance(arg, ast.YieldFrom):
            _all_stmts[(82408,82410)] = True
            arg.yield_loc = yield_loc
            arg.loc = arg.loc.join(arg.yield_loc)
            return arg
        elif arg is not None:
            _all_stmts[(82562,82566)] = True
            return ast.Yield(value=arg,
                             yield_loc=yield_loc, loc=yield_loc.join(arg.loc))
        else:
            _all_stmts[(82711,82715)] = True
            return ast.Yield(value=None,
                             yield_loc=yield_loc, loc=yield_loc)

    @action(Seq(Loc("from", loc=(82840,82843)), Rule("test", loc=(82853,82857)), loc=(82836,82839)), loc=(82829,82835))
    def yield_arg_1(self, from_loc, value):
        _all_stmts[(82872,82875)] = True
        return ast.YieldFrom(value=value,
                             from_loc=from_loc, loc=from_loc.join(value.loc))

    yield_arg = Alt(yield_arg_1, Rule("testlist", loc=(83066,83070)), loc=(83049,83052))
    """(3.3-) yield_arg: 'from' test | testlist"""
