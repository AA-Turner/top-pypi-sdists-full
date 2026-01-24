# Generated from grammar/DynamoDbGrammar.g4 by ANTLR 4.13.2
# encoding: utf-8
# pylint: skip-file
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,30,239,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,1,0,1,0,1,
        0,1,1,1,1,1,1,5,1,59,8,1,10,1,12,1,62,9,1,1,2,1,2,1,2,1,3,1,3,1,
        3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,5,3,78,8,3,10,3,12,3,81,9,3,1,
        3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,
        3,99,8,3,1,3,1,3,1,3,1,3,1,3,1,3,5,3,107,8,3,10,3,12,3,110,9,3,1,
        4,1,4,1,5,1,5,1,5,1,6,1,6,1,6,1,6,4,6,121,8,6,11,6,12,6,122,1,7,
        1,7,1,7,1,7,5,7,129,8,7,10,7,12,7,132,9,7,1,8,1,8,1,8,1,8,1,9,1,
        9,1,9,1,9,5,9,142,8,9,10,9,12,9,145,9,9,1,10,1,10,1,10,1,11,1,11,
        1,11,1,11,5,11,154,8,11,10,11,12,11,157,9,11,1,12,1,12,1,12,1,13,
        1,13,1,13,1,13,5,13,166,8,13,10,13,12,13,169,9,13,1,14,1,14,1,15,
        1,15,3,15,175,8,15,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,
        3,16,186,8,16,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,3,17,196,8,
        17,1,18,1,18,1,18,1,18,1,18,5,18,203,8,18,10,18,12,18,206,9,18,1,
        18,1,18,1,19,1,19,5,19,212,8,19,10,19,12,19,215,9,19,1,20,1,20,1,
        21,1,21,1,21,1,21,1,21,3,21,224,8,21,1,22,1,22,1,23,1,23,1,23,1,
        24,1,24,1,24,1,25,4,25,235,8,25,11,25,12,25,236,1,25,0,1,6,26,0,
        2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,
        48,50,0,3,1,0,8,13,1,0,14,15,1,0,26,27,238,0,52,1,0,0,0,2,55,1,0,
        0,0,4,63,1,0,0,0,6,98,1,0,0,0,8,111,1,0,0,0,10,113,1,0,0,0,12,120,
        1,0,0,0,14,124,1,0,0,0,16,133,1,0,0,0,18,137,1,0,0,0,20,146,1,0,
        0,0,22,149,1,0,0,0,24,158,1,0,0,0,26,161,1,0,0,0,28,170,1,0,0,0,
        30,174,1,0,0,0,32,185,1,0,0,0,34,195,1,0,0,0,36,197,1,0,0,0,38,209,
        1,0,0,0,40,216,1,0,0,0,42,223,1,0,0,0,44,225,1,0,0,0,46,227,1,0,
        0,0,48,230,1,0,0,0,50,234,1,0,0,0,52,53,3,2,1,0,53,54,5,0,0,1,54,
        1,1,0,0,0,55,60,3,38,19,0,56,57,5,1,0,0,57,59,3,38,19,0,58,56,1,
        0,0,0,59,62,1,0,0,0,60,58,1,0,0,0,60,61,1,0,0,0,61,3,1,0,0,0,62,
        60,1,0,0,0,63,64,3,6,3,0,64,65,5,0,0,1,65,5,1,0,0,0,66,67,6,3,-1,
        0,67,68,3,34,17,0,68,69,3,8,4,0,69,70,3,34,17,0,70,99,1,0,0,0,71,
        72,3,34,17,0,72,73,5,16,0,0,73,74,5,2,0,0,74,79,3,34,17,0,75,76,
        5,1,0,0,76,78,3,34,17,0,77,75,1,0,0,0,78,81,1,0,0,0,79,77,1,0,0,
        0,79,80,1,0,0,0,80,82,1,0,0,0,81,79,1,0,0,0,82,83,5,3,0,0,83,99,
        1,0,0,0,84,85,3,34,17,0,85,86,5,17,0,0,86,87,3,34,17,0,87,88,5,19,
        0,0,88,89,3,34,17,0,89,99,1,0,0,0,90,99,3,36,18,0,91,92,5,2,0,0,
        92,93,3,6,3,0,93,94,5,3,0,0,94,95,6,3,-1,0,95,99,1,0,0,0,96,97,5,
        18,0,0,97,99,3,6,3,3,98,66,1,0,0,0,98,71,1,0,0,0,98,84,1,0,0,0,98,
        90,1,0,0,0,98,91,1,0,0,0,98,96,1,0,0,0,99,108,1,0,0,0,100,101,10,
        2,0,0,101,102,5,19,0,0,102,107,3,6,3,2,103,104,10,1,0,0,104,105,
        5,20,0,0,105,107,3,6,3,1,106,100,1,0,0,0,106,103,1,0,0,0,107,110,
        1,0,0,0,108,106,1,0,0,0,108,109,1,0,0,0,109,7,1,0,0,0,110,108,1,
        0,0,0,111,112,7,0,0,0,112,9,1,0,0,0,113,114,3,12,6,0,114,115,5,0,
        0,1,115,11,1,0,0,0,116,121,3,14,7,0,117,121,3,18,9,0,118,121,3,22,
        11,0,119,121,3,26,13,0,120,116,1,0,0,0,120,117,1,0,0,0,120,118,1,
        0,0,0,120,119,1,0,0,0,121,122,1,0,0,0,122,120,1,0,0,0,122,123,1,
        0,0,0,123,13,1,0,0,0,124,125,5,21,0,0,125,130,3,16,8,0,126,127,5,
        1,0,0,127,129,3,16,8,0,128,126,1,0,0,0,129,132,1,0,0,0,130,128,1,
        0,0,0,130,131,1,0,0,0,131,15,1,0,0,0,132,130,1,0,0,0,133,134,3,38,
        19,0,134,135,5,8,0,0,135,136,3,30,15,0,136,17,1,0,0,0,137,138,5,
        22,0,0,138,143,3,20,10,0,139,140,5,1,0,0,140,142,3,20,10,0,141,139,
        1,0,0,0,142,145,1,0,0,0,143,141,1,0,0,0,143,144,1,0,0,0,144,19,1,
        0,0,0,145,143,1,0,0,0,146,147,3,38,19,0,147,148,3,44,22,0,148,21,
        1,0,0,0,149,150,5,23,0,0,150,155,3,24,12,0,151,152,5,1,0,0,152,154,
        3,24,12,0,153,151,1,0,0,0,154,157,1,0,0,0,155,153,1,0,0,0,155,156,
        1,0,0,0,156,23,1,0,0,0,157,155,1,0,0,0,158,159,3,38,19,0,159,160,
        3,44,22,0,160,25,1,0,0,0,161,162,5,24,0,0,162,167,3,28,14,0,163,
        164,5,1,0,0,164,166,3,28,14,0,165,163,1,0,0,0,166,169,1,0,0,0,167,
        165,1,0,0,0,167,168,1,0,0,0,168,27,1,0,0,0,169,167,1,0,0,0,170,171,
        3,38,19,0,171,29,1,0,0,0,172,175,3,34,17,0,173,175,3,32,16,0,174,
        172,1,0,0,0,174,173,1,0,0,0,175,31,1,0,0,0,176,177,3,34,17,0,177,
        178,7,1,0,0,178,179,3,34,17,0,179,186,1,0,0,0,180,181,5,2,0,0,181,
        182,3,32,16,0,182,183,5,3,0,0,183,184,6,16,-1,0,184,186,1,0,0,0,
        185,176,1,0,0,0,185,180,1,0,0,0,186,33,1,0,0,0,187,196,3,38,19,0,
        188,196,3,44,22,0,189,196,3,36,18,0,190,191,5,2,0,0,191,192,3,34,
        17,0,192,193,5,3,0,0,193,194,6,17,-1,0,194,196,1,0,0,0,195,187,1,
        0,0,0,195,188,1,0,0,0,195,189,1,0,0,0,195,190,1,0,0,0,196,35,1,0,
        0,0,197,198,5,26,0,0,198,199,5,2,0,0,199,204,3,34,17,0,200,201,5,
        1,0,0,201,203,3,34,17,0,202,200,1,0,0,0,203,206,1,0,0,0,204,202,
        1,0,0,0,204,205,1,0,0,0,205,207,1,0,0,0,206,204,1,0,0,0,207,208,
        5,3,0,0,208,37,1,0,0,0,209,213,3,40,20,0,210,212,3,42,21,0,211,210,
        1,0,0,0,212,215,1,0,0,0,213,211,1,0,0,0,213,214,1,0,0,0,214,39,1,
        0,0,0,215,213,1,0,0,0,216,217,7,2,0,0,217,41,1,0,0,0,218,219,5,4,
        0,0,219,224,3,40,20,0,220,221,5,5,0,0,221,222,5,25,0,0,222,224,5,
        6,0,0,223,218,1,0,0,0,223,220,1,0,0,0,224,43,1,0,0,0,225,226,5,28,
        0,0,226,45,1,0,0,0,227,228,5,27,0,0,228,229,5,0,0,1,229,47,1,0,0,
        0,230,231,5,28,0,0,231,232,5,0,0,1,232,49,1,0,0,0,233,235,5,30,0,
        0,234,233,1,0,0,0,235,236,1,0,0,0,236,234,1,0,0,0,236,237,1,0,0,
        0,237,51,1,0,0,0,18,60,79,98,106,108,120,122,130,143,155,167,174,
        185,195,204,213,223,236
    ]

class DynamoDbGrammarParser ( Parser ):

    grammarFileName = "DynamoDbGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','", "'('", "')'", "'.'", "'['", "']'", 
                     "<INVALID>", "'='", "'<>'", "'<'", "'<='", "'>'", "'>='", 
                     "'+'", "'-'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "WS", "EQ", 
                      "NE", "LT", "LE", "GT", "GE", "PLUS", "MINUS", "IN", 
                      "BETWEEN", "NOT", "AND", "OR", "SET", "ADD", "DELETE", 
                      "REMOVE", "INDEX", "ID", "ATTRIBUTE_NAME_SUB", "LITERAL_SUB", 
                      "STRING_LITERAL", "UNKNOWN" ]

    RULE_projection_ = 0
    RULE_projection = 1
    RULE_condition_ = 2
    RULE_condition = 3
    RULE_comparator_symbol = 4
    RULE_update_ = 5
    RULE_update = 6
    RULE_set_section = 7
    RULE_set_action = 8
    RULE_add_section = 9
    RULE_add_action = 10
    RULE_delete_section = 11
    RULE_delete_action = 12
    RULE_remove_section = 13
    RULE_remove_action = 14
    RULE_set_value = 15
    RULE_arithmetic = 16
    RULE_operand = 17
    RULE_func = 18
    RULE_path = 19
    RULE_id_ = 20
    RULE_dereference = 21
    RULE_literal = 22
    RULE_expression_attr_names_sub = 23
    RULE_expression_attr_values_sub = 24
    RULE_unknown = 25

    ruleNames =  [ "projection_", "projection", "condition_", "condition", 
                   "comparator_symbol", "update_", "update", "set_section", 
                   "set_action", "add_section", "add_action", "delete_section", 
                   "delete_action", "remove_section", "remove_action", "set_value", 
                   "arithmetic", "operand", "func", "path", "id_", "dereference", 
                   "literal", "expression_attr_names_sub", "expression_attr_values_sub", 
                   "unknown" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    WS=7
    EQ=8
    NE=9
    LT=10
    LE=11
    GT=12
    GE=13
    PLUS=14
    MINUS=15
    IN=16
    BETWEEN=17
    NOT=18
    AND=19
    OR=20
    SET=21
    ADD=22
    DELETE=23
    REMOVE=24
    INDEX=25
    ID=26
    ATTRIBUTE_NAME_SUB=27
    LITERAL_SUB=28
    STRING_LITERAL=29
    UNKNOWN=30

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    def validateRedundantParentheses(self, redundantParens):
        if redundantParens:
            raise Exception('RedundantParenthesesException')



    class Projection_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def projection(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.ProjectionContext,0)


        def EOF(self):
            return self.getToken(DynamoDbGrammarParser.EOF, 0)

        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_projection_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProjection_" ):
                listener.enterProjection_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProjection_" ):
                listener.exitProjection_(self)




    def projection_(self):

        localctx = DynamoDbGrammarParser.Projection_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_projection_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.projection()
            self.state = 53
            self.match(DynamoDbGrammarParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProjectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def path(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.PathContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.PathContext,i)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_projection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProjection" ):
                listener.enterProjection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProjection" ):
                listener.exitProjection(self)




    def projection(self):

        localctx = DynamoDbGrammarParser.ProjectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_projection)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.path()
            self.state = 60
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 56
                self.match(DynamoDbGrammarParser.T__0)
                self.state = 57
                self.path()
                self.state = 62
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Condition_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.ConditionContext,0)


        def EOF(self):
            return self.getToken(DynamoDbGrammarParser.EOF, 0)

        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_condition_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition_" ):
                listener.enterCondition_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition_" ):
                listener.exitCondition_(self)




    def condition_(self):

        localctx = DynamoDbGrammarParser.Condition_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_condition_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.condition(0)
            self.state = 64
            self.match(DynamoDbGrammarParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.hasOuterParens = False


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_condition

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)
            self.hasOuterParens = ctx.hasOuterParens


    class OrContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.ConditionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.ConditionContext,i)

        def OR(self):
            return self.getToken(DynamoDbGrammarParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOr" ):
                listener.enterOr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOr" ):
                listener.exitOr(self)


    class NegationContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(DynamoDbGrammarParser.NOT, 0)
        def condition(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.ConditionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNegation" ):
                listener.enterNegation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNegation" ):
                listener.exitNegation(self)


    class InContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.OperandContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.OperandContext,i)

        def IN(self):
            return self.getToken(DynamoDbGrammarParser.IN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIn" ):
                listener.enterIn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIn" ):
                listener.exitIn(self)


    class AndContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.ConditionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.ConditionContext,i)

        def AND(self):
            return self.getToken(DynamoDbGrammarParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnd" ):
                listener.enterAnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnd" ):
                listener.exitAnd(self)


    class BetweenContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.OperandContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.OperandContext,i)

        def BETWEEN(self):
            return self.getToken(DynamoDbGrammarParser.BETWEEN, 0)
        def AND(self):
            return self.getToken(DynamoDbGrammarParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBetween" ):
                listener.enterBetween(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBetween" ):
                listener.exitBetween(self)


    class FunctionConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def func(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.FuncContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCondition" ):
                listener.enterFunctionCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCondition" ):
                listener.exitFunctionCondition(self)


    class ComparatorContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.OperandContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.OperandContext,i)

        def comparator_symbol(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.Comparator_symbolContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparator" ):
                listener.enterComparator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparator" ):
                listener.exitComparator(self)


    class ConditionGroupingContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ConditionContext
            super().__init__(parser)
            self.c = None # ConditionContext
            self.copyFrom(ctx)

        def condition(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.ConditionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConditionGrouping" ):
                listener.enterConditionGrouping(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConditionGrouping" ):
                listener.exitConditionGrouping(self)



    def condition(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = DynamoDbGrammarParser.ConditionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_condition, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = DynamoDbGrammarParser.ComparatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 67
                self.operand()
                self.state = 68
                self.comparator_symbol()
                self.state = 69
                self.operand()
                pass

            elif la_ == 2:
                localctx = DynamoDbGrammarParser.InContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 71
                self.operand()
                self.state = 72
                self.match(DynamoDbGrammarParser.IN)
                self.state = 73
                self.match(DynamoDbGrammarParser.T__1)
                self.state = 74
                self.operand()
                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==1:
                    self.state = 75
                    self.match(DynamoDbGrammarParser.T__0)
                    self.state = 76
                    self.operand()
                    self.state = 81
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 82
                self.match(DynamoDbGrammarParser.T__2)
                pass

            elif la_ == 3:
                localctx = DynamoDbGrammarParser.BetweenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 84
                self.operand()
                self.state = 85
                self.match(DynamoDbGrammarParser.BETWEEN)
                self.state = 86
                self.operand()
                self.state = 87
                self.match(DynamoDbGrammarParser.AND)
                self.state = 88
                self.operand()
                pass

            elif la_ == 4:
                localctx = DynamoDbGrammarParser.FunctionConditionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 90
                self.func()
                pass

            elif la_ == 5:
                localctx = DynamoDbGrammarParser.ConditionGroupingContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 91
                self.match(DynamoDbGrammarParser.T__1)
                self.state = 92
                localctx.c = self.condition(0)
                self.state = 93
                self.match(DynamoDbGrammarParser.T__2)

                self.validateRedundantParentheses(localctx.c.hasOuterParens)
                localctx.hasOuterParens=True
                        
                pass

            elif la_ == 6:
                localctx = DynamoDbGrammarParser.NegationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 96
                self.match(DynamoDbGrammarParser.NOT)
                self.state = 97
                self.condition(3)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 108
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 106
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        localctx = DynamoDbGrammarParser.AndContext(self, DynamoDbGrammarParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 100
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 101
                        self.match(DynamoDbGrammarParser.AND)
                        self.state = 102
                        self.condition(2)
                        pass

                    elif la_ == 2:
                        localctx = DynamoDbGrammarParser.OrContext(self, DynamoDbGrammarParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 103
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 104
                        self.match(DynamoDbGrammarParser.OR)
                        self.state = 105
                        self.condition(1)
                        pass

             
                self.state = 110
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Comparator_symbolContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(DynamoDbGrammarParser.EQ, 0)

        def NE(self):
            return self.getToken(DynamoDbGrammarParser.NE, 0)

        def LT(self):
            return self.getToken(DynamoDbGrammarParser.LT, 0)

        def LE(self):
            return self.getToken(DynamoDbGrammarParser.LE, 0)

        def GT(self):
            return self.getToken(DynamoDbGrammarParser.GT, 0)

        def GE(self):
            return self.getToken(DynamoDbGrammarParser.GE, 0)

        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_comparator_symbol

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparator_symbol" ):
                listener.enterComparator_symbol(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparator_symbol" ):
                listener.exitComparator_symbol(self)




    def comparator_symbol(self):

        localctx = DynamoDbGrammarParser.Comparator_symbolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_comparator_symbol)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 16128) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Update_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def update(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.UpdateContext,0)


        def EOF(self):
            return self.getToken(DynamoDbGrammarParser.EOF, 0)

        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_update_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUpdate_" ):
                listener.enterUpdate_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUpdate_" ):
                listener.exitUpdate_(self)




    def update_(self):

        localctx = DynamoDbGrammarParser.Update_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_update_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.update()
            self.state = 114
            self.match(DynamoDbGrammarParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UpdateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def set_section(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.Set_sectionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.Set_sectionContext,i)


        def add_section(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.Add_sectionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.Add_sectionContext,i)


        def delete_section(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.Delete_sectionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.Delete_sectionContext,i)


        def remove_section(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.Remove_sectionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.Remove_sectionContext,i)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_update

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUpdate" ):
                listener.enterUpdate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUpdate" ):
                listener.exitUpdate(self)




    def update(self):

        localctx = DynamoDbGrammarParser.UpdateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_update)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 120
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [21]:
                    self.state = 116
                    self.set_section()
                    pass
                elif token in [22]:
                    self.state = 117
                    self.add_section()
                    pass
                elif token in [23]:
                    self.state = 118
                    self.delete_section()
                    pass
                elif token in [24]:
                    self.state = 119
                    self.remove_section()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 122 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 31457280) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Set_sectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SET(self):
            return self.getToken(DynamoDbGrammarParser.SET, 0)

        def set_action(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.Set_actionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.Set_actionContext,i)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_set_section

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSet_section" ):
                listener.enterSet_section(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSet_section" ):
                listener.exitSet_section(self)




    def set_section(self):

        localctx = DynamoDbGrammarParser.Set_sectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_set_section)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.match(DynamoDbGrammarParser.SET)
            self.state = 125
            self.set_action()
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 126
                self.match(DynamoDbGrammarParser.T__0)
                self.state = 127
                self.set_action()
                self.state = 132
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Set_actionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def path(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.PathContext,0)


        def EQ(self):
            return self.getToken(DynamoDbGrammarParser.EQ, 0)

        def set_value(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.Set_valueContext,0)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_set_action

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSet_action" ):
                listener.enterSet_action(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSet_action" ):
                listener.exitSet_action(self)




    def set_action(self):

        localctx = DynamoDbGrammarParser.Set_actionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_set_action)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            self.path()
            self.state = 134
            self.match(DynamoDbGrammarParser.EQ)
            self.state = 135
            self.set_value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Add_sectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADD(self):
            return self.getToken(DynamoDbGrammarParser.ADD, 0)

        def add_action(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.Add_actionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.Add_actionContext,i)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_add_section

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdd_section" ):
                listener.enterAdd_section(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdd_section" ):
                listener.exitAdd_section(self)




    def add_section(self):

        localctx = DynamoDbGrammarParser.Add_sectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_add_section)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.match(DynamoDbGrammarParser.ADD)
            self.state = 138
            self.add_action()
            self.state = 143
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 139
                self.match(DynamoDbGrammarParser.T__0)
                self.state = 140
                self.add_action()
                self.state = 145
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Add_actionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def path(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.PathContext,0)


        def literal(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.LiteralContext,0)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_add_action

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdd_action" ):
                listener.enterAdd_action(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdd_action" ):
                listener.exitAdd_action(self)




    def add_action(self):

        localctx = DynamoDbGrammarParser.Add_actionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_add_action)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 146
            self.path()
            self.state = 147
            self.literal()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Delete_sectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DELETE(self):
            return self.getToken(DynamoDbGrammarParser.DELETE, 0)

        def delete_action(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.Delete_actionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.Delete_actionContext,i)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_delete_section

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDelete_section" ):
                listener.enterDelete_section(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDelete_section" ):
                listener.exitDelete_section(self)




    def delete_section(self):

        localctx = DynamoDbGrammarParser.Delete_sectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_delete_section)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 149
            self.match(DynamoDbGrammarParser.DELETE)
            self.state = 150
            self.delete_action()
            self.state = 155
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 151
                self.match(DynamoDbGrammarParser.T__0)
                self.state = 152
                self.delete_action()
                self.state = 157
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Delete_actionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def path(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.PathContext,0)


        def literal(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.LiteralContext,0)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_delete_action

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDelete_action" ):
                listener.enterDelete_action(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDelete_action" ):
                listener.exitDelete_action(self)




    def delete_action(self):

        localctx = DynamoDbGrammarParser.Delete_actionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_delete_action)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 158
            self.path()
            self.state = 159
            self.literal()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Remove_sectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REMOVE(self):
            return self.getToken(DynamoDbGrammarParser.REMOVE, 0)

        def remove_action(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.Remove_actionContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.Remove_actionContext,i)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_remove_section

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRemove_section" ):
                listener.enterRemove_section(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRemove_section" ):
                listener.exitRemove_section(self)




    def remove_section(self):

        localctx = DynamoDbGrammarParser.Remove_sectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_remove_section)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.match(DynamoDbGrammarParser.REMOVE)
            self.state = 162
            self.remove_action()
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 163
                self.match(DynamoDbGrammarParser.T__0)
                self.state = 164
                self.remove_action()
                self.state = 169
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Remove_actionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def path(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.PathContext,0)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_remove_action

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRemove_action" ):
                listener.enterRemove_action(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRemove_action" ):
                listener.exitRemove_action(self)




    def remove_action(self):

        localctx = DynamoDbGrammarParser.Remove_actionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_remove_action)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self.path()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Set_valueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_set_value

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ArithmeticValueContext(Set_valueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.Set_valueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def arithmetic(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.ArithmeticContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticValue" ):
                listener.enterArithmeticValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticValue" ):
                listener.exitArithmeticValue(self)


    class OperandValueContext(Set_valueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.Set_valueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operand(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.OperandContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperandValue" ):
                listener.enterOperandValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperandValue" ):
                listener.exitOperandValue(self)



    def set_value(self):

        localctx = DynamoDbGrammarParser.Set_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_set_value)
        try:
            self.state = 174
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                localctx = DynamoDbGrammarParser.OperandValueContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 172
                self.operand()
                pass

            elif la_ == 2:
                localctx = DynamoDbGrammarParser.ArithmeticValueContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 173
                self.arithmetic()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithmeticContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.hasOuterParens = False


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_arithmetic

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)
            self.hasOuterParens = ctx.hasOuterParens



    class PlusMinusContext(ArithmeticContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ArithmeticContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.OperandContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.OperandContext,i)

        def PLUS(self):
            return self.getToken(DynamoDbGrammarParser.PLUS, 0)
        def MINUS(self):
            return self.getToken(DynamoDbGrammarParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlusMinus" ):
                listener.enterPlusMinus(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlusMinus" ):
                listener.exitPlusMinus(self)


    class ArithmeticParensContext(ArithmeticContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.ArithmeticContext
            super().__init__(parser)
            self.a = None # ArithmeticContext
            self.copyFrom(ctx)

        def arithmetic(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.ArithmeticContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArithmeticParens" ):
                listener.enterArithmeticParens(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArithmeticParens" ):
                listener.exitArithmeticParens(self)



    def arithmetic(self):

        localctx = DynamoDbGrammarParser.ArithmeticContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_arithmetic)
        self._la = 0 # Token type
        try:
            self.state = 185
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                localctx = DynamoDbGrammarParser.PlusMinusContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 176
                self.operand()
                self.state = 177
                _la = self._input.LA(1)
                if not(_la==14 or _la==15):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 178
                self.operand()
                pass

            elif la_ == 2:
                localctx = DynamoDbGrammarParser.ArithmeticParensContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 180
                self.match(DynamoDbGrammarParser.T__1)
                self.state = 181
                localctx.a = self.arithmetic()
                self.state = 182
                self.match(DynamoDbGrammarParser.T__2)

                self.validateRedundantParentheses(localctx.a.hasOuterParens)
                localctx.hasOuterParens=True
                        
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.hasOuterParens = False


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_operand

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)
            self.hasOuterParens = ctx.hasOuterParens



    class PathOperandContext(OperandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.OperandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def path(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.PathContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathOperand" ):
                listener.enterPathOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathOperand" ):
                listener.exitPathOperand(self)


    class LiteralOperandContext(OperandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.OperandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.LiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralOperand" ):
                listener.enterLiteralOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralOperand" ):
                listener.exitLiteralOperand(self)


    class FunctionOperandContext(OperandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.OperandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def func(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.FuncContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionOperand" ):
                listener.enterFunctionOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionOperand" ):
                listener.exitFunctionOperand(self)


    class ParenOperandContext(OperandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.OperandContext
            super().__init__(parser)
            self.o = None # OperandContext
            self.copyFrom(ctx)

        def operand(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.OperandContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenOperand" ):
                listener.enterParenOperand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenOperand" ):
                listener.exitParenOperand(self)



    def operand(self):

        localctx = DynamoDbGrammarParser.OperandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_operand)
        try:
            self.state = 195
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                localctx = DynamoDbGrammarParser.PathOperandContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 187
                self.path()
                pass

            elif la_ == 2:
                localctx = DynamoDbGrammarParser.LiteralOperandContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 188
                self.literal()
                pass

            elif la_ == 3:
                localctx = DynamoDbGrammarParser.FunctionOperandContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 189
                self.func()
                pass

            elif la_ == 4:
                localctx = DynamoDbGrammarParser.ParenOperandContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 190
                self.match(DynamoDbGrammarParser.T__1)
                self.state = 191
                localctx.o = self.operand()
                self.state = 192
                self.match(DynamoDbGrammarParser.T__2)

                self.validateRedundantParentheses(localctx.o.hasOuterParens)
                localctx.hasOuterParens=True
                        
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_func

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class FunctionCallContext(FuncContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.FuncContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(DynamoDbGrammarParser.ID, 0)
        def operand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.OperandContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.OperandContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)



    def func(self):

        localctx = DynamoDbGrammarParser.FuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_func)
        self._la = 0 # Token type
        try:
            localctx = DynamoDbGrammarParser.FunctionCallContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 197
            self.match(DynamoDbGrammarParser.ID)
            self.state = 198
            self.match(DynamoDbGrammarParser.T__1)
            self.state = 199
            self.operand()
            self.state = 204
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 200
                self.match(DynamoDbGrammarParser.T__0)
                self.state = 201
                self.operand()
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 207
            self.match(DynamoDbGrammarParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def id_(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.Id_Context,0)


        def dereference(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DynamoDbGrammarParser.DereferenceContext)
            else:
                return self.getTypedRuleContext(DynamoDbGrammarParser.DereferenceContext,i)


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_path

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPath" ):
                listener.enterPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPath" ):
                listener.exitPath(self)




    def path(self):

        localctx = DynamoDbGrammarParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_path)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 209
            self.id_()
            self.state = 213
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 210
                    self.dereference() 
                self.state = 215
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Id_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(DynamoDbGrammarParser.ID, 0)

        def ATTRIBUTE_NAME_SUB(self):
            return self.getToken(DynamoDbGrammarParser.ATTRIBUTE_NAME_SUB, 0)

        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_id_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterId_" ):
                listener.enterId_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitId_" ):
                listener.exitId_(self)




    def id_(self):

        localctx = DynamoDbGrammarParser.Id_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_id_)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 216
            _la = self._input.LA(1)
            if not(_la==26 or _la==27):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DereferenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_dereference

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ListAccessContext(DereferenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.DereferenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INDEX(self):
            return self.getToken(DynamoDbGrammarParser.INDEX, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListAccess" ):
                listener.enterListAccess(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListAccess" ):
                listener.exitListAccess(self)


    class MapAccessContext(DereferenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.DereferenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def id_(self):
            return self.getTypedRuleContext(DynamoDbGrammarParser.Id_Context,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMapAccess" ):
                listener.enterMapAccess(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMapAccess" ):
                listener.exitMapAccess(self)



    def dereference(self):

        localctx = DynamoDbGrammarParser.DereferenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_dereference)
        try:
            self.state = 223
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                localctx = DynamoDbGrammarParser.MapAccessContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 218
                self.match(DynamoDbGrammarParser.T__3)
                self.state = 219
                self.id_()
                pass
            elif token in [5]:
                localctx = DynamoDbGrammarParser.ListAccessContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 220
                self.match(DynamoDbGrammarParser.T__4)
                self.state = 221
                self.match(DynamoDbGrammarParser.INDEX)
                self.state = 222
                self.match(DynamoDbGrammarParser.T__5)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_literal

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class LiteralSubContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DynamoDbGrammarParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LITERAL_SUB(self):
            return self.getToken(DynamoDbGrammarParser.LITERAL_SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralSub" ):
                listener.enterLiteralSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralSub" ):
                listener.exitLiteralSub(self)



    def literal(self):

        localctx = DynamoDbGrammarParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_literal)
        try:
            localctx = DynamoDbGrammarParser.LiteralSubContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 225
            self.match(DynamoDbGrammarParser.LITERAL_SUB)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression_attr_names_subContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ATTRIBUTE_NAME_SUB(self):
            return self.getToken(DynamoDbGrammarParser.ATTRIBUTE_NAME_SUB, 0)

        def EOF(self):
            return self.getToken(DynamoDbGrammarParser.EOF, 0)

        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_expression_attr_names_sub

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_attr_names_sub" ):
                listener.enterExpression_attr_names_sub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_attr_names_sub" ):
                listener.exitExpression_attr_names_sub(self)




    def expression_attr_names_sub(self):

        localctx = DynamoDbGrammarParser.Expression_attr_names_subContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_expression_attr_names_sub)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 227
            self.match(DynamoDbGrammarParser.ATTRIBUTE_NAME_SUB)
            self.state = 228
            self.match(DynamoDbGrammarParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression_attr_values_subContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LITERAL_SUB(self):
            return self.getToken(DynamoDbGrammarParser.LITERAL_SUB, 0)

        def EOF(self):
            return self.getToken(DynamoDbGrammarParser.EOF, 0)

        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_expression_attr_values_sub

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_attr_values_sub" ):
                listener.enterExpression_attr_values_sub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_attr_values_sub" ):
                listener.exitExpression_attr_values_sub(self)




    def expression_attr_values_sub(self):

        localctx = DynamoDbGrammarParser.Expression_attr_values_subContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_expression_attr_values_sub)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 230
            self.match(DynamoDbGrammarParser.LITERAL_SUB)
            self.state = 231
            self.match(DynamoDbGrammarParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnknownContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UNKNOWN(self, i:int=None):
            if i is None:
                return self.getTokens(DynamoDbGrammarParser.UNKNOWN)
            else:
                return self.getToken(DynamoDbGrammarParser.UNKNOWN, i)

        def getRuleIndex(self):
            return DynamoDbGrammarParser.RULE_unknown

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnknown" ):
                listener.enterUnknown(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnknown" ):
                listener.exitUnknown(self)




    def unknown(self):

        localctx = DynamoDbGrammarParser.UnknownContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_unknown)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 234 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 233
                self.match(DynamoDbGrammarParser.UNKNOWN)
                self.state = 236 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==30):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[3] = self.condition_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def condition_sempred(self, localctx:ConditionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         




