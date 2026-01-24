import { List, Item, Variable, Term, buffer_size } from "../atsds/index.mts";

let v = null;

beforeEach(() => {
    v = new Term("(a b c)");
});

test("toString", () => {
    expect(v.toString()).toBe("(a b c)");

    const old_buffer_size = buffer_size(4);
    expect(() => v.toString()).toThrow();
    buffer_size(old_buffer_size);
});

test("copy", () => {
    expect(v.copy().toString()).toBe("(a b c)");
});

test("key", () => {
    expect(v.copy().key()).toBe(v.key());
});

test("create_from_same", () => {
    const v2 = new Term(v);
    expect(v2.toString()).toBe("(a b c)");

    expect(() => new Term(v, 100)).toThrow();
});

test("create_from_base", () => {
    const v2 = new Term(v.value);
    expect(v2.toString()).toBe("(a b c)");
});

test("create_from_text", () => {
    const v2 = new Term("(a b c)");
    expect(v2.toString()).toBe("(a b c)");
});

test("create_from_bytes", () => {
    const v2 = new Term(v.data());
    expect(v2.toString()).toBe("(a b c)");

    expect(() => new Term(v.data(), 100)).toThrow();
});

test("create_fail", () => {
    expect(() => new Term(100)).toThrow();
});

test("term", () => {
    expect(new Term("()").term()).toBeInstanceOf(List);
    expect(new Term("a").term()).toBeInstanceOf(Item);
    expect(new Term("`a").term()).toBeInstanceOf(Variable);
});

test("ground_simple", () => {
    const a = new Term("`a");
    const b = new Term("((`a b))");
    expect(a.ground(b).toString()).toBe("b");

    expect(a.ground(new Term("((`a b c d e))"))).toBeNull();
});

test("ground_scope", () => {
    const a = new Term("`a");
    const b = new Term("((x y `a `b) (y x `b `c))");
    expect(a.ground(b, "x").toString()).toBe("`c");
});

test("rename_simple", () => {
    const a = new Term("`x");
    const b = new Term("((pre_) (_suf))");
    expect(a.rename(b).toString()).toBe("`pre_x_suf");
});

test("rename_empty_prefix", () => {
    const a = new Term("`x");
    const b = new Term("(() (_suf))");
    expect(a.rename(b).toString()).toBe("`x_suf");
});

test("rename_empty_suffix", () => {
    const a = new Term("`x");
    const b = new Term("((pre_) ())");
    expect(a.rename(b).toString()).toBe("`pre_x");
});

test("rename_list", () => {
    const a = new Term("(`x `y)");
    const b = new Term("((p_) (_s))");
    expect(a.rename(b).toString()).toBe("(`p_x_s `p_y_s)");
});

test("rename_invalid", () => {
    const a = new Term("`x");
    const b = new Term("item");
    expect(a.rename(b)).toBeNull();
});

test("match_simple", () => {
    const a = new Term("`a");
    const b = new Term("b");
    const result = a.match(b);
    expect(result).not.toBeNull();
    expect(result.toString()).toBe("((1 2 `a b))");
});

test("match_complex", () => {
    const a = new Term("(f b a)");
    const b = new Term("(f `x a)");
    const result = a.match(b);
    expect(result).not.toBeNull();
    expect(result.toString()).toBe("((2 1 `x b))");
});

test("match_fail", () => {
    const a = new Term("(f `x)");
    const b = new Term("(g `y)");
    const result = a.match(b);
    expect(result).toBeNull();
});
