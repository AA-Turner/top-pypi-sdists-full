import { Search, Rule } from "../atsds/index.mts";

let search = null;

beforeEach(() => {
    search = new Search(100, 1000);
});

test("reset_parameters", () => {
    search.set_limit_size(50);
    search.set_buffer_size(500);
    search.reset();
});

test("add_rule_and_fact", () => {
    expect(search.add("test rule")).toBe(true);
    expect(search.add("fact")).toBe(true);
});

test("add_fail", () => {
    search.set_limit_size(10);
    expect(search.add("a-long-facts-that-exceeds-limit")).toBe(false);
});

test("execute_single", () => {
    search.add("p q");
    search.add("p");
    const target = new Rule("q");
    let success = false;
    const count = search.execute((rule) => {
        if (rule.key() === target.key()) {
            success = true;
        }
        return success;
    });
    expect(count).toBe(1);
    expect(success).toBe(true);
});

test("execute_long", () => {
    search.add("p q r");
    search.add("p");
    search.add("q");
    const target1 = new Rule("q r");
    const target2 = new Rule("r");
    let success1 = false;
    let success2 = false;
    count1 = search.execute((rule) => {
        if (rule.key() === target1.key()) {
            success1 = true;
        }
        return false;
    });
    count2 = search.execute((rule) => {
        if (rule.key() === target2.key()) {
            success2 = true;
        }
        return false;
    });
    expect(count1).toBe(1);
    expect(success1).toBe(true);
    expect(count2).toBe(1);
    expect(success2).toBe(true);
});

test("execute_duplicated_facts", () => {
    search.add("p r");
    search.add("p r");
    search.add("p");
    search.add("q");
    const count = search.execute((rule) => false);
    expect(count).toBe(1);
});

test("execute_duplicated_rules", () => {
    search.add("p r s");
    search.add("p r s");
    search.add("p");
    search.add("q");
    const count = search.execute((rule) => false);
    expect(count).toBe(1);
});

test("execute_exceed", () => {
    search.set_limit_size(100);
    expect(search.add("(2 `x) (`x `x`)")).toBe(true);
    expect(search.add("(2 a-very-long-fact-that-exceeds-half-of-the-limit-size)")).toBe(true);
    const count = search.execute((rule) => false);
    expect(count).toBe(0);
});
