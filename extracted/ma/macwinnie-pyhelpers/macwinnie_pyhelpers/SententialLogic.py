#!/usr/bin/env python3
import re


class Truth:
    """
    Basic truth check class.
    """

    def __init__(self, interpretingExample=None):
        """
        Given an example object, which should be able to support interpretion
        of propopsitions, its type will be stored as interpreter. Defaults to
        `None`, could be an `Version` object out of `macwinnie_pyhelpers.Version`
        """
        if type(interpretingExample) == type(None):
            self.interpreter = None
        else:
            self.interpreter = type(interpretingExample)

    def verify(self, proposition):
        """
        * boolean propositions will be returned as they are
        * numbers (float, integers) will return true if > 0, 0 and negatives will return false
        * `nein`, `no`, `n`, `falsch`, `false`, `f` will return `False`
        * `ja`, `j`, `yes`, `y`, `wahr`, `w`, `true`, `t` will return `True`
        """
        trueMatch = r"^((t(rue)?)|(y(es)?)|(w(ahr)?)|(j(a)?))$"
        falseMatch = r"^((f((alse)|(alsch))?)|(n((o)|(ein))?))$"
        if type(proposition) is bool:
            return proposition
        elif isinstance(proposition, (int, float)):
            return proposition > 0
        elif type(proposition) is str:
            if re.match(trueMatch, proposition.strip(), re.IGNORECASE):
                return True
            elif re.match(falseMatch, proposition.strip(), re.IGNORECASE):
                return False
            elif self.interpreter != None:
                try:
                    return self.interpret(proposition)
                except:
                    pass
        raise Exception(
            'No interpretion found for given proposition "{}"!'.format(proposition)
        )

    def interpret(self, proposition):
        """
        Method for deep-diving proposition interpretation.
        Will check for `P1 o P2` with `P1`, `P2` propositions and `o` an operator
        out of:
        * `<=` for “less or equal”
        * `<` for “less”
        * `>=` for “greater or equal”
        * `>` for “greater”
        * `!=` for “not equal”
        * `==` for “equal”
        """
        rx = r"((((<|>)=?)|(!|=)=))"
        cRx = re.compile(rx)
        splitting = []
        foundOperators = cRx.finditer(proposition)
        for idx, match in enumerate(foundOperators):
            s = match.start()
            e = match.end()
            splitting.append([s, e])

        if splitting == []:
            raise Exception(f'No valid truth proposition given by "{proposition}"!')

        # f = open("./test.log", "a")
        # import json
        # f.write(json.dumps(splitting) + "\n\n-----\n\n")
        # f.close()

        checks = []
        s3 = 0
        for i, s in enumerate(splitting):
            s1 = s3
            s2 = s[0]
            s3 = s[1]
            if i != len(splitting) - 1:
                s4 = splitting[i + 1][0]
            else:
                s4 = len(proposition)
            checks.append(
                [
                    proposition[s1:s2].strip(),
                    proposition[s2:s3].strip(),
                    proposition[s3:s4].strip(),
                ]
            )
        verum = True
        for c in checks:
            o0 = self.interpreter(c[0])
            o1 = self.interpreter(c[2])
            if c[1] == "<=":
                verum = verum and o0 <= o1
            elif c[1] == "<":
                verum = verum and o0 < o1
            elif c[1] == ">=":
                verum = verum and o0 >= o1
            elif c[1] == ">":
                verum = verum and o0 > o1
            elif c[1] == "!=":
                verum = verum and o0 != o1
            elif c[1] == "==":
                verum = verum and o0 == o1
        return verum


class Sentence:
    """
    String to be checked for truth.

    Binding can be done using regular brackets `(` and `)` – and
    the operators binding order.

    Operators supported are (top is more binding than bottom):
    * `¬` as `not`
    * `∧` as `and`
    * `∨` as `or` (not the letter `v`!)
    """

    def __init__(
        self,
        sentence,
        interpretingExample=None,
        verifier=None,
        pretested=False,
        openingBracketRX=r"\(",
        closingBracketRX=r"\)",
    ):
        """
        Given a `sentence`, this classes objects will be used to verify a logical
        sentence.

        With an `interpreter` defined and `verifier` not set – may be the string
        `Version` to use the same named class from this package or `int` or
        something like that – the `verifier` from this package `Truth` will be
        instanciated.

        `verifier` has to be an instance of a class implementing a method `verify`
        which returns boolean values for string input.

        `pretested` is to be used internally - when all propositions have
        already been replaced by truthy literals.
        """
        self.verifier = None
        self.atomized = None
        self.tsentence = None

        self.sentence = sentence
        self.setBrackets(openingBracketRX, closingBracketRX)

        if not pretested:
            if verifier == None:
                if type(interpretingExample) == type(None):
                    self.verifier = Truth()
                else:
                    self.verifier = Truth(interpretingExample)
            else:
                self.verifier = verifier
            self.verifyAllPropositions()
        else:
            self.tsentence = sentence
        self.atomizeBraces()

    def __bool__(self):
        return self.truth()

    def __str__(self, literals=True):
        return self.getLiteral(self.truth())

    def getLiteral(self, booleanValue):
        """Somehow static function to get a literal for boolean values"""
        if booleanValue:
            return "⊤"
        else:
            return "⊥"

    def verifyAllPropositions(self):
        """Turn all propositions into `⊤` for truthy and `⊥` for false values"""
        deviders = r"([^(¬∧∨\(\)]+)"
        verified = []
        self.tsentence = self.sentence
        for p in re.findall(deviders, self.tsentence):
            x = p.strip()
            if x not in verified and len(x) > 0:
                self.tsentence = self.tsentence.replace(
                    p, self.getLiteral(self.verifier.verify(x.strip()))
                )
        self.tsentence = re.sub(r"\s", "", self.tsentence)

    def truth(self):
        """Final method that returns the truth value of a sentence"""
        while not self.isAtomic():
            # do everything to do with ¬, as it has the stronges binding
            rx = r"¬(.)"
            x = re.search(rx, self.atomized)
            if x != None:
                literal = x.group(1)
                z = not Sentence(
                    literal, verifier=self.verifier, pretested=True
                ).truth()
                self.atomized = self.atomized.replace(x.group(0), self.getLiteral(z))
            else:
                # do everything to do with ∧, as it's the next after ¬
                rx = r"(.)∧(.)"
                x = re.search(rx, self.atomized)
                if x != None:
                    literalA = x.group(1)
                    literalB = x.group(2)
                    boolA = Sentence(
                        literalA, verifier=self.verifier, pretested=True
                    ).truth()
                    boolB = Sentence(
                        literalB, verifier=self.verifier, pretested=True
                    ).truth()
                    self.atomized = self.atomized.replace(
                        x.group(0), self.getLiteral(boolA and boolB)
                    )
                else:
                    # do everything to do with ∨, as it's the next after ∧
                    rx = r"(.)∨(.)"
                    x = re.search(rx, self.atomized)
                    if x != None:
                        literalA = x.group(1)
                        literalB = x.group(2)
                        boolA = Sentence(
                            literalA, verifier=self.verifier, pretested=True
                        ).truth()
                        boolB = Sentence(
                            literalB, verifier=self.verifier, pretested=True
                        ).truth()
                        self.atomized = self.atomized.replace(
                            x.group(0), self.getLiteral(boolA or boolB)
                        )
        if self.atomized == "⊤":
            return True
        elif self.atomized == "⊥":
            return False

    def isAtomic(self):
        """
        Check if the given sentence is a single, atomic literal so it can be translated to boolean
        """
        if len(self.atomized) == 1:
            return True
        else:
            return False

    def setBrackets(self, opening=r"\(", closing=r"\)"):
        self.openingCharRX = opening
        self.closingCharRX = closing

    def getBraceIdx(self):
        """Analyze sentence for brackets and return their type and index"""
        oRx = re.compile(self.openingCharRX)
        cRx = re.compile(self.closingCharRX)

        braces = {}
        for m in oRx.finditer(self.atomized):
            c = m.group()
            if len(c) != 1:
                raise Exception("Opening only has to match single characters!")
            braces[m.start()] = "o"

        for m in cRx.finditer(self.atomized):
            c = m.group()
            if len(c) != 1:
                raise Exception("Closing only has to match single characters!")
            braces[m.start()] = "c"

        brackets = {k: braces[k] for k in sorted(braces.keys())}

        idx = list(brackets.keys())
        if len(idx) > 0:
            if brackets[idx[-1]] != "c":
                raise Exception("Last bracket has to be a closing one!")

            if brackets[idx[0]] != "o":
                raise Exception("First bracket has to be an opening one!")

        return brackets, idx

    def atomizeBraces(self):
        """Find matching outer brackets as long as existent and get literals `⊤` or `⊥` for the inner sentence"""
        if self.atomized == None:
            self.atomized = self.tsentence
        br, idx = self.getBraceIdx()
        while len(idx) > 0:
            i = 0
            z = 1
            x1 = idx[i]
            while z > 0:
                i = i + 1
                if br[idx[i]] == "o":
                    z = z + 1
                else:
                    z = z - 1
            x2 = idx[i] + 1
            toBeReplaced = self.atomized[x1:x2]
            subSentence = toBeReplaced[1:-1]
            self.atomized = self.atomized.replace(
                toBeReplaced,
                self.getLiteral(
                    Sentence(
                        subSentence, verifier=self.verifier, pretested=True
                    ).truth()
                ),
            )
            br, idx = self.getBraceIdx()
