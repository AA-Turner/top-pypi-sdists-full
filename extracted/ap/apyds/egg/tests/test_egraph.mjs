/**
 * Tests for the EGraph implementation in atsds-egg
 */
import { Term } from "atsds";
import { EGraph, ENode, UnionFind } from "../dist/index.mjs";

test("unionfind_basic", () => {
    const uf = new UnionFind();
    const a = 0;
    const b = 1;

    expect(uf.find(a)).toBe(a);
    expect(uf.find(b)).toBe(b);

    uf.union(a, b);
    expect(uf.find(a)).toBe(uf.find(b));
});

test("unionfind_path_compression", () => {
    const uf = new UnionFind();
    const a = 0;
    const b = 1;
    const c = 2;

    uf.union(a, b);
    uf.union(b, c);

    expect(uf.find(a)).toBe(uf.find(c));
});

test("enode_creation", () => {
    const a = 0;
    const b = 1;
    const node = new ENode("+", [a, b]);

    expect(node.op).toBe("+");
    expect(node.children).toEqual([a, b]);
});

test("enode_canonicalize", () => {
    const uf = new UnionFind();
    const a = 0;
    const b = 1;
    const c = 2;
    const d = 3;

    uf.union(a, c);
    uf.union(d, b);

    const node = new ENode("+", [a, b]);
    const canon = node.canonicalize(uf.find.bind(uf));

    expect(canon.children[0]).toBe(uf.find(a));
    expect(canon.children[1]).toBe(uf.find(b));
});

test("enode_key", () => {
    const a = 0;
    const b = 1;
    const node1 = new ENode("+", [a, b]);
    const node2 = new ENode("+", [a, b]);

    expect(node1.key()).toBe(node2.key());
});

test("egraph_add_item", () => {
    const eg = new EGraph();
    const x = eg.add(new Term("x"));

    expect(typeof x).toBe("number");
    expect(eg.find(x)).toBe(x);
});

test("egraph_add_variable", () => {
    const eg = new EGraph();
    const x = eg.add(new Term("`x"));

    expect(typeof x).toBe("number");
    expect(eg.find(x)).toBe(x);
});

test("egraph_add_list", () => {
    const eg = new EGraph();
    const lst = eg.add(new Term("(a b c)"));

    expect(typeof lst).toBe("number");
    expect(eg.find(lst)).toBe(lst);
});

test("egraph_add_same_term_twice", () => {
    const eg = new EGraph();
    const x1 = eg.add(new Term("x"));
    const x2 = eg.add(new Term("x"));

    expect(x1).toBe(x2);
});

test("egraph_add_compound_term", () => {
    const eg = new EGraph();
    const a = eg.add(new Term("a"));
    const x = eg.add(new Term("x"));
    const ax = eg.add(new Term("(+ a x)"));

    expect(eg.find(a)).toBe(a);
    expect(eg.find(x)).toBe(x);
    expect(eg.find(ax)).toBe(ax);
});

test("egraph_merge_simple", () => {
    const eg = new EGraph();
    const a = eg.add(new Term("a"));
    const b = eg.add(new Term("b"));

    expect(eg.find(a)).not.toBe(eg.find(b));

    eg.merge(a, b);

    expect(eg.find(a)).toBe(eg.find(b));
});

test("egraph_merge_idempotent", () => {
    const eg = new EGraph();
    const a = eg.add(new Term("a"));
    const b = eg.add(new Term("b"));

    const r1 = eg.merge(a, b);
    const r2 = eg.merge(a, b);

    expect(r1).toBe(r2);
});

test("egraph_congruence", () => {
    const eg = new EGraph();

    const ax = eg.add(new Term("(+ a x)"));
    const bx = eg.add(new Term("(+ b x)"));

    expect(eg.find(ax)).not.toBe(eg.find(bx));

    const a = eg.add(new Term("a"));
    const b = eg.add(new Term("b"));

    eg.merge(a, b);
    eg.rebuild();

    expect(eg.find(ax)).toBe(eg.find(bx));
});

test("egraph_congruence_nested", () => {
    const eg = new EGraph();

    const acc = eg.add(new Term("(g (f a x) c x)"));
    const bcc = eg.add(new Term("(g (f b x) d x)"));

    const a = eg.add(new Term("a"));
    const b = eg.add(new Term("b"));
    const c = eg.add(new Term("c"));
    const d = eg.add(new Term("d"));

    eg.merge(a, b);
    eg.merge(c, d);
    eg.rebuild();

    expect(eg.find(acc)).toBe(eg.find(bcc));
});

test("egraph_multiple_merges", () => {
    const eg = new EGraph();

    const a = eg.add(new Term("a"));
    const b = eg.add(new Term("b"));
    const c = eg.add(new Term("c"));

    eg.merge(a, b);
    eg.merge(b, c);

    expect(eg.find(a)).toBe(eg.find(c));
});

test("egraph_immediate_congruence", () => {
    const eg = new EGraph();
    const a = eg.add(new Term("a"));

    expect(eg.find(a)).toBe(a);
});

test("egraph_mixed_terms", () => {
    const eg = new EGraph();

    const item = eg.add(new Term("item"));
    const varTerm = eg.add(new Term("`var"));
    const lst = eg.add(new Term("(item `var)"));

    expect(typeof item).toBe("number");
    expect(typeof varTerm).toBe("number");
    expect(typeof lst).toBe("number");
});

test("egraph_empty_list", () => {
    const eg = new EGraph();

    const empty = eg.add(new Term("()"));

    expect(typeof empty).toBe("number");
    expect(eg.find(empty)).toBe(empty);
});

test("egraph_nested_lists", () => {
    const eg = new EGraph();

    const inner = eg.add(new Term("(a b)"));
    const outer = eg.add(new Term("((a b) c)"));

    expect(typeof inner).toBe("number");
    expect(typeof outer).toBe("number");
});

test("egraph_hashcons", () => {
    const eg = new EGraph();

    const ab1 = eg.add(new Term("(f a b)"));
    const ab2 = eg.add(new Term("(f a b)"));

    expect(ab1).toBe(ab2);
    expect(eg.classes.size).toBe(4);
});
