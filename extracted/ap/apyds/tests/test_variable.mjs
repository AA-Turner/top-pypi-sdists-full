import { Variable, buffer_size } from "../atsds/index.mts";

let v = null;

beforeEach(() => {
    v = new Variable("`variable");
});

test("toString", () => {
    expect(v.toString()).toBe("`variable");

    const old_buffer_size = buffer_size(4);
    expect(() => v.toString()).toThrow();
    buffer_size(old_buffer_size);
});

test("copy", () => {
    expect(v.copy().toString()).toBe("`variable");
});

test("key", () => {
    expect(v.copy().key()).toBe(v.key());
});

test("create_from_same", () => {
    const v2 = new Variable(v);
    expect(v2.toString()).toBe("`variable");

    expect(() => new Variable(v, 100)).toThrow();
});

test("create_from_base", () => {
    const v2 = new Variable(v.value);
    expect(v2.toString()).toBe("`variable");
});

test("create_from_text", () => {
    const v2 = new Variable("`variable");
    expect(v2.toString()).toBe("`variable");
});

test("create_from_bytes", () => {
    const v2 = new Variable(v.data());
    expect(v2.toString()).toBe("`variable");

    expect(() => new Variable(v.data(), 100)).toThrow();
});

test("create_fail", () => {
    expect(() => new Variable(100)).toThrow();
});

test("name", () => {
    expect(v.name().toString()).toBe("variable");
});
