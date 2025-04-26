import inspect
from collections import defaultdict

dispatch_template = """
class MISSING:
    pass

def __DISPATCH__(self, {args}):
    {inits}
    {body}

    method = self.map[({lookup})]
    return method({posargs})
"""


# @dataclass
# class Group:
#     active: bool = False
#     initializer: str = None
#     lookup_arg: str = None
#     pos_arg: str = None


class ArgumentAnalyzer:
    def __init__(self):
        self.name_to_positions = defaultdict(set)
        self.position_to_names = defaultdict(set)
        self.counts = defaultdict(lambda: [0, 0])
        self.total = 0
        self.is_method = None

    def add(self, fn):
        sig = inspect.signature(fn)
        is_method = False
        for i, (name, param) in enumerate(sig.parameters.items()):
            if name == "self":
                assert i == 0
                is_method = True
                continue
            if param.kind is inspect._POSITIONAL_ONLY:
                cnt = self.counts[i]
                self.position_to_names[i].add(None)
            elif param.kind is inspect._POSITIONAL_OR_KEYWORD:
                cnt = self.counts[i]
                self.position_to_names[i].add(param.name)
                self.name_to_positions[param.name].add(i)
            elif param.kind is inspect._KEYWORD_ONLY:
                cnt = self.counts[param.name]
                self.name_to_positions[param.name].add(param.name)
            elif param.kind is inspect._VAR_POSITIONAL:
                raise TypeError("ovld does not support *args")
            elif param.kind is inspect._VAR_KEYWORD:
                raise TypeError("ovld does not support **kwargs")

            cnt[0] += 1 if param.default is inspect._empty else 0
            cnt[1] += 1

        self.total += 1

        if self.is_method is None:
            self.is_method = is_method
        elif self.is_method != is_method:
            raise TypeError(
                "Some, but not all registered methods define `self`. It should be all or none."
            )

    def compile(self):
        if any(
            len(pos) != 1
            for _name, pos in self.name_to_positions.items()
            if (name := _name) is not None
        ):
            raise TypeError(
                f"Argument {name} is found both in a positional and keyword setting."
            )
        npositional = 0
        positional = []
        for pos, names in sorted(self.position_to_names.items()):
            required, total = self.counts[pos]
            name = f"_ovld_arg{pos}"
            if len(names) == 1 and total == self.total:
                name = list(names)[0]
            else:
                npositional = pos + 1
            positional.append((name, required == self.total))

        keywords = []
        for key, (name,) in self.name_to_positions.items():
            if isinstance(name, int):
                pass  # ignore positional arguments
            else:
                assert key == name
                required, total = self.counts[key]
                keywords.append((name, required == self.total))

        return positional[:npositional], positional[npositional:], keywords

    def generate_dispatch(self):
        po, pn, kw = self.compile()

        inits = set()

        argsstar = ""
        kwargsstar = ""
        targsstar = ""

        args = []
        body = [""]
        posargs = []
        lookup = []

        def _positional(k, necessary):
            nonlocal argsstar, targsstar
            if necessary:
                args.append(k)
                posargs.append(k)
                lookup.append(f"type({k})")
            else:
                args.append(f"{k}=MISSING")
                argsstar = "*ARGS"
                targsstar = "*TARGS"
                inits.add("ARGS = []")
                inits.add("TARGS = []")
                body.append(f"if {k} is not MISSING:")
                body.append(f"    ARGS.append({k})")
                body.append(f"    TARGS.append(type({k}))")

        for k, necessary in po:
            _positional(k, necessary)

        args.append("/")

        for k, necessary in pn:
            _positional(k, necessary)

        if kw:
            args.append("*")

        for k, necessary in kw:
            if necessary:
                posargs.append(f"{k}={k}")
                lookup.append(f"({k!r}, type({k}))")
            else:
                args.append(f"{k}=MISSING")
                kwargsstar = "**KWARGS"
                targsstar = "*TARGS"
                inits.add("KWARGS = []")
                inits.add("TARGS = []")
                body.append(f"if {k} is not MISSING:")
                body.append(f"    KWARGS[{k!r}] = {k}")
                body.append(f"    TARGS.append(({k!r}, type({k})))")

        posargs.append(argsstar)
        posargs.append(kwargsstar)
        lookup.append(targsstar)

        code = dispatch_template.format(
            inits="\n    ".join(inits),
            args=", ".join(x for x in args if x),
            posargs=", ".join(x for x in posargs if x),
            body="\n    ".join(x for x in body if x),
            lookup=", ".join(x for x in lookup if x) + ",",
        )
        # code = re.sub(string=code, pattern=r"[ \n]*\n", repl="\n")
        return code


anal = ArgumentAnalyzer()


def foo(fn):
    anal.add(fn)


@foo
def f(x):
    pass


@foo
def f(x):
    pass


foo(lambda x, y: ...)


# @foo
# def f(x, y, *, zou):
#     pass

# @foo
# def f(x, y=3, *, fax, coop):
#     pass


def main():
    print(anal.generate_dispatch())
    # po, pn, kw = anal.compile()

    # argsinit = ""
    # kwargsinit = ""
    # targsinit = ""

    # argsstar = ""
    # kwargsstar = ""
    # targsstar = ""

    # args = []
    # body = [""]
    # posargs = []
    # lookup = []

    # def _positional(k, necessary):
    #     nonlocal argsinit, targsinit, argsstar, targsstar
    #     if necessary:
    #         args.append(k)
    #         posargs.append(k)
    #         lookup.append(f"type({k})")
    #     else:
    #         args.append(f"{k}=MISSING")
    #         argsstar = "*ARGS"
    #         targsstar = "*TARGS"
    #         argsinit = "ARGS = []"
    #         targsinit = "TARGS = []"
    #         body.append(f"if {k} is not MISSING:")
    #         body.append(f"    ARGS.append({k})")
    #         body.append(f"    TARGS.append(type({k}))")

    # for k, necessary in po:
    #     _positional(k, necessary)

    # args.append("/")

    # for k, necessary in pn:
    #     _positional(k, necessary)

    # if kw:
    #     args.append("*")

    # for k, necessary in kw:
    #     if necessary:
    #         posargs.append(f"{k}={k}")
    #         lookup.append(f"({k!r}, type({k}))")
    #     else:
    #         args.append(f"{k}=MISSING")
    #         kwargsstar = "**KWARGS"
    #         targsstar = "*TARGS"
    #         kwargsinit = "KWARGS = []"
    #         targsinit = "TARGS = []"
    #         body.append(f"if {k} is not MISSING:")
    #         body.append(f"    KWARGS[{k!r}] = {k}")
    #         body.append(f"    TARGS.append(({k!r}, type({k})))")

    # posargs.append(argsstar)
    # posargs.append(kwargsstar)
    # lookup.append(targsstar)

    # code = template.format(
    #     argsinit=argsinit,
    #     kwargsinit=kwargsinit,
    #     targsinit=targsinit,
    #     args=", ".join(x for x in args if x),
    #     posargs=", ".join(x for x in posargs if x),
    #     body="\n    ".join(x for x in body if x),
    #     lookup=", ".join(x for x in lookup if x) + ",",
    # )
    # code = re.sub(string=code, pattern=r"[ \n]*\n", repl="\n")
    # print(code)


# def main():
#     MISSING = object()

#     def boo(quack):
#         return quack * quack

#     def f1(z, *, quack=MISSING, bob=MISSING, crack=MISSING):
#         if crack is MISSING and bob is MISSING and quack is MISSING:
#             return boo(z)
#         else:
#             KWARGS = {}
#             if quack is not MISSING:
#                 KWARGS['quack'] = quack
#             if bob is not MISSING:
#                 KWARGS['bob'] = bob
#             if crack is not MISSING:
#                 KWARGS['crack'] = crack
#             return boo(z, **KWARGS)

#     def f2(z, **KWARGS):
#         return boo(z, **KWARGS)

#     print(timeit(stmt=lambda: f1(7), number=1000000))
#     print(timeit(stmt=lambda: f2(7), number=1000000))


if __name__ == "__main__":
    main()
