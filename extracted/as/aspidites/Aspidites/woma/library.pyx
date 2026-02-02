#cython: language_level=3, annotation_typing=False, c_string_encoding=utf-8, binding=True
# THIS FILE IS GENERATED - DO NOT EDIT #
from typing import Any
from collections.abc import Generator
import cython  # type: ignore
from cython import declare as decl,address as addr,sizeof,typeof,struct,cfunc,ccall,nogil,no_gc,inline,union,typedef,cast,char,short,int as cint,bint,short,double,long,longdouble,longdoublecomplex,longlong,complex,float as cfloat
from Aspidites._vendor.pyrsistent import pset as __pset,pmap as __pmap,pvector as __pvector,s,v,m
from Aspidites.woma import *
from Aspidites._vendor import take,drop,takelast,droplast,consume,nth,first_true,iterate,padnone,ncycles,repeatfunc,grouper,group_by,roundrobin,partition,splitat,splitby,powerset,pairwise,iter_suppress,flatten,accumulate,reduce,filterfalse,zip_longest,chain,combinations,cycle,dropwhile,islice,repeat,starmap,takewhile,tee,call,apply,flip,curry,curried,zipwith,foldl,foldr,unfold,Capture,Strict,OneOf,AllOf,NoneOf,Not,Each,EachItem,Some,Between,Length,Contains,Regex,Check,InstanceOf,SubclassOf,Arguments,Returns,Transformed,At,Object,match as __match,_
from Aspidites.monads import Maybe as __maybe,Surely as __surely
from Aspidites.math import Undefined as __undefined,SafeDiv as __safeDiv,SafeExp as __safeExp,SafeMod as __safeMod,SafeFloorDiv as __safeFloorDiv,SafeUnaryAdd as __safeUnaryAdd,SafeUnarySub as __safeUnarySub,SafeFactorial as __safeFactorial
from Aspidites._vendor.contracts import contract as __contract,new_contract as __new_contract,check
from Aspidites._vendor.RestrictedPython.Guards import safe_builtins as __safe_builtins
from Aspidites._vendor.RestrictedPython.compile import compile_restricted as compile
from Aspidites.type_guard import safer_type as type
__safe_builtins['new_contract']=__new_contract
__safe_builtins['check']=check
__safe_builtins['type']=type
__safe_builtins['compile']=compile
__safe_builtins['print']=print
__safe_builtins['take']=take
__safe_builtins['drop']=drop
__safe_builtins['takelast']=takelast
__safe_builtins['droplast']=droplast
__safe_builtins['consume']=consume
__safe_builtins['nth']=nth
__safe_builtins['first_true']=first_true
__safe_builtins['iterate']=iterate
__safe_builtins['padnone']=padnone
__safe_builtins['ncycles']=ncycles
__safe_builtins['repeatfunc']=repeatfunc
__safe_builtins['grouper']=grouper
__safe_builtins['group_by']=group_by
__safe_builtins['roundrobin']=roundrobin
__safe_builtins['partition']=partition
__safe_builtins['splitat']=splitat
__safe_builtins['splitby']=splitby
__safe_builtins['powerset']=powerset
__safe_builtins['pairwise']=pairwise
__safe_builtins['iter_suppress']=iter_suppress
__safe_builtins['flatten']=flatten
__safe_builtins['accumulate']=accumulate
__safe_builtins['reduce']=reduce
__safe_builtins['filterfalse']=filterfalse
__safe_builtins['zip_longest']=zip_longest
__safe_builtins['chain']=chain
__safe_builtins['combinations']=combinations
__safe_builtins['cycle']=cycle
__safe_builtins['dropwhile']=dropwhile
__safe_builtins['islice']=islice
__safe_builtins['repeat']=repeat
__safe_builtins['starmap']=starmap
__safe_builtins['takewhile']=takewhile
__safe_builtins['tee']=tee
__safe_builtins['call']=call
__safe_builtins['apply']=apply
__safe_builtins['flip']=flip
__safe_builtins['curry']=curry
__safe_builtins['curried']=curried
__safe_builtins['zipwith']=zipwith
__safe_builtins['foldl']=foldl
__safe_builtins['foldr']=foldr
__safe_builtins['unfold']=unfold
__safe_builtins['Capture']=Capture
__safe_builtins['Strict']=Strict
__safe_builtins['OneOf']=OneOf
__safe_builtins['AllOf']=AllOf
__safe_builtins['NoneOf']=NoneOf
__safe_builtins['Not']=Not
__safe_builtins['Each']=Each
__safe_builtins['EachItem']=EachItem
__safe_builtins['Some']=Some
__safe_builtins['Between']=Between
__safe_builtins['Length']=Length
__safe_builtins['Contains']=Contains
__safe_builtins['Regex']=Regex
__safe_builtins['Check']=Check
__safe_builtins['InstanceOf']=InstanceOf
__safe_builtins['SubclassOf']=SubclassOf
__safe_builtins['Arguments']=Arguments
__safe_builtins['Returns']=Returns
__safe_builtins['Transformed']=Transformed
__safe_builtins['At']=At
__safe_builtins['Object']=Object
__safe_builtins['_']=_
globals().update(dict(__builtins__=__pmap(__safe_builtins)))  # add all imports to globals
procedure: None
coroutine: Generator
number: Any
new_contract = __new_contract


@__contract()
def add(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return x+y


@__contract()
def sub(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return x-y


@__contract()
def div(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return __maybe(__safeDiv, x, y)()


@__contract()
def exp(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return __maybe(__safeExp, x, y, )()


@__contract()
def mod(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return __maybe(__safeMod, x, y, )()


@__contract()
def mul(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return x*y


@__contract()
def neg(x : 'number' = 0) -> 'number':
    return -x


@__contract()
def inv(x : 'bool' = __undefined()) -> '*':
    x : 'int' = -x+1
    return __maybe(bool, x)()


@__contract()
def iterate(f : 'Callable' = __undefined(), x : '*' = __undefined()) -> 'coroutine':
    for i in __maybe(iter, int, 1)():
        x = __maybe(f, x)()
        yield __maybe(f, x)()


@__contract()
def partition(predictor : 'Callable' = __undefined(), iterable : 'Iterable' = __undefined()) -> 'list':
    t : 'tuple' = __maybe(tee, iterable)()
    t1 : 'Iterable' = t[0]
    t2 : 'Iterable' = t[1]
    p1 : 'Iterable' = __maybe(filterfalse, predictor, t1)()
    p2 : 'Iterable' = __maybe(filter, predictor, t2)()
    return __pvector([p1, p2])


