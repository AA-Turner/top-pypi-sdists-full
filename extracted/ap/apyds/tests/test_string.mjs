import { String_, buffer_size } from "../atsds/index.mts";

let v = null;

beforeEach(() => {
    v = new String_("string");
});

test("toString", () => {
    expect(v.toString()).toBe("string");

    const old_buffer_size = buffer_size(4);
    expect(() => v.toString()).toThrow();
    buffer_size(old_buffer_size);
});

test("copy", () => {
    expect(v.copy().toString()).toBe("string");
});

test("key", () => {
    expect(v.copy().key()).toBe(v.key());
});

test("create_from_same", () => {
    const v2 = new String_(v);
    expect(v2.toString()).toBe("string");

    expect(() => new String_(v, 100)).toThrow();
});

test("create_from_base", () => {
    const v2 = new String_(v.value);
    expect(v2.toString()).toBe("string");
});

test("create_from_text", () => {
    const v2 = new String_("string");
    expect(v2.toString()).toBe("string");
});

test("create_from_bytes", () => {
    const v2 = new String_(v.data());
    expect(v2.toString()).toBe("string");

    expect(() => new String_(v.data(), 100)).toThrow();
});

test("create_fail", () => {
    expect(() => new String_(100)).toThrow();
});
