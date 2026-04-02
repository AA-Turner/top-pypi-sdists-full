import apyds
from apyds_egg import EGraph, ENode, UnionFind, EClassId


def test_unionfind_basic():
    uf = UnionFind()
    a = EClassId(0)
    b = EClassId(1)

    assert uf.find(a) == a
    assert uf.find(b) == b

    uf.union(a, b)
    assert uf.find(a) == uf.find(b)


def test_unionfind_path_compression():
    uf = UnionFind()
    a = EClassId(0)
    b = EClassId(1)
    c = EClassId(2)

    uf.union(a, b)
    uf.union(b, c)

    assert uf.find(a) == uf.find(c)


def test_enode_creation():
    a = EClassId(0)
    b = EClassId(1)
    node = ENode("+", (a, b))

    assert node.op == "+"
    assert node.children == (a, b)


def test_enode_canonicalize():
    uf = UnionFind()
    a = EClassId(0)
    b = EClassId(1)
    c = EClassId(2)
    d = EClassId(3)

    uf.union(a, c)
    uf.union(d, b)

    node = ENode("+", (a, b))
    canon = node.canonicalize(uf.find)

    assert canon.children[0] == uf.find(a)
    assert canon.children[1] == uf.find(b)


def test_enode_frozen():
    a = EClassId(0)
    b = EClassId(1)
    node1 = ENode("+", (a, b))
    node2 = ENode("+", (a, b))

    assert node1 == node2
    assert hash(node1) == hash(node2)


def test_egraph_add_item():
    eg = EGraph()
    x = eg.add(apyds.Term("x"))

    assert isinstance(x, int)
    assert eg.find(x) == x


def test_egraph_add_variable():
    eg = EGraph()
    x = eg.add(apyds.Term("`x"))

    assert isinstance(x, int)
    assert eg.find(x) == x


def test_egraph_add_list():
    eg = EGraph()
    lst = eg.add(apyds.Term("(a b c)"))

    assert isinstance(lst, int)
    assert eg.find(lst) == lst


def test_egraph_add_same_term_twice():
    eg = EGraph()
    x1 = eg.add(apyds.Term("x"))
    x2 = eg.add(apyds.Term("x"))

    assert x1 == x2


def test_egraph_add_compound_term():
    eg = EGraph()
    a = eg.add(apyds.Term("a"))
    x = eg.add(apyds.Term("x"))
    ax = eg.add(apyds.Term("(+ a x)"))

    assert eg.find(a) == a
    assert eg.find(x) == x
    assert eg.find(ax) == ax


def test_egraph_merge_simple():
    eg = EGraph()
    a = eg.add(apyds.Term("a"))
    b = eg.add(apyds.Term("b"))

    assert eg.find(a) != eg.find(b)

    eg.merge(a, b)

    assert eg.find(a) == eg.find(b)


def test_egraph_merge_idempotent():
    eg = EGraph()
    a = eg.add(apyds.Term("a"))
    b = eg.add(apyds.Term("b"))

    r1 = eg.merge(a, b)
    r2 = eg.merge(a, b)

    assert r1 == r2


def test_egraph_congruence():
    eg = EGraph()

    ax = eg.add(apyds.Term("(+ a x)"))
    bx = eg.add(apyds.Term("(+ b x)"))

    assert eg.find(ax) != eg.find(bx)

    a = eg.add(apyds.Term("a"))
    b = eg.add(apyds.Term("b"))

    eg.merge(a, b)
    eg.rebuild()

    assert eg.find(ax) == eg.find(bx)


def test_egraph_congruence_nested():
    eg = EGraph()

    acc = eg.add(apyds.Term("(g (f a x) c x)"))
    bcc = eg.add(apyds.Term("(g (f b x) d x)"))

    a = eg.add(apyds.Term("a"))
    b = eg.add(apyds.Term("b"))
    c = eg.add(apyds.Term("c"))
    d = eg.add(apyds.Term("d"))

    eg.merge(a, b)
    eg.merge(c, d)
    eg.rebuild()

    assert eg.find(acc) == eg.find(bcc)


def test_egraph_multiple_merges():
    eg = EGraph()

    a = eg.add(apyds.Term("a"))
    b = eg.add(apyds.Term("b"))
    c = eg.add(apyds.Term("c"))

    eg.merge(a, b)
    eg.merge(b, c)

    assert eg.find(a) == eg.find(c)


def test_egraph_immediate_congruence():
    eg = EGraph()
    a = eg.add(apyds.Term("a"))

    assert eg.find(a) == a


def test_egraph_mixed_terms():
    eg = EGraph()

    item = eg.add(apyds.Term("item"))
    var = eg.add(apyds.Term("`var"))
    lst = eg.add(apyds.Term("(item `var)"))

    assert isinstance(item, int)
    assert isinstance(var, int)
    assert isinstance(lst, int)


def test_egraph_empty_list():
    eg = EGraph()

    empty = eg.add(apyds.Term("()"))

    assert isinstance(empty, int)
    assert eg.find(empty) == empty


def test_egraph_nested_lists():
    eg = EGraph()

    inner = eg.add(apyds.Term("(a b)"))
    outer = eg.add(apyds.Term("((a b) c)"))

    assert isinstance(inner, int)
    assert isinstance(outer, int)


def test_egraph_hashcons():
    eg = EGraph()

    ab1 = eg.add(apyds.Term("(f a b)"))
    ab2 = eg.add(apyds.Term("(f a b)"))

    assert ab1 == ab2
    assert len(eg.classes) == 4
