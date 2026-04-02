import { Item, buffer_size } from "../atsds/index.mts";

let v = null;

beforeEach(() => {
    v = new Item("item");
});

test("toString", () => {
    expect(v.toString()).toBe("item");

    const old_buffer_size = buffer_size(4);
    expect(() => v.toString()).toThrow();
    buffer_size(old_buffer_size);
});

test("copy", () => {
    expect(v.copy().toString()).toBe("item");
});

test("key", () => {
    expect(v.copy().key()).toBe(v.key());
});

test("create_from_same", () => {
    const v2 = new Item(v);
    expect(v2.toString()).toBe("item");

    expect(() => new Item(v, 100)).toThrow();
});

test("create_from_base", () => {
    const v2 = new Item(v.value);
    expect(v2.toString()).toBe("item");
});

test("create_from_text", () => {
    const v2 = new Item("item");
    expect(v2.toString()).toBe("item");
});

test("create_from_bytes", () => {
    const v2 = new Item(v.data());
    expect(v2.toString()).toBe("item");

    expect(() => new Item(v.data(), 100)).toThrow();
});

test("create_fail", () => {
    expect(() => new Item(100)).toThrow();
});

test("name", () => {
    expect(v.name().toString()).toBe("item");
});
