import { Chain, Rule } from "../atsds/index.mts";

let chain = null;

beforeEach(() => {
    chain = new Chain(100, 1000);
});

test("reset_parameters", () => {
    chain.set_limit_size(50);
    chain.set_buffer_size(500);
    chain.reset();
});

test("add_rule_and_fact", () => {
    expect(chain.add("test rule")).toBe(true);
    expect(chain.add("fact")).toBe(true);
});

test("add_fail", () => {
    chain.set_limit_size(10);
    expect(chain.add("a-long-facts-that-exceeds-limit")).toBe(false);
});

test("execute_single_premise", () => {
    chain.add("p q");
    chain.add("p");
    const target = new Rule("q");
    let success = false;
    const count = chain.execute((rule) => {
        if (rule.key() === target.key()) {
            success = true;
            return true;
        }
        return false;
    });
    expect(count).toBe(1);
    expect(success).toBe(true);
});

test("execute_multiple_premises_chain", () => {
    chain.add("p q r");
    chain.add("p");
    chain.add("q");
    const target = new Rule("r");
    let success = false;
    const count = chain.execute((rule) => {
        if (rule.key() === target.key()) {
            success = true;
        }
        return false;
    });
    expect(count).toBe(2);
    expect(success).toBe(true);
});

test("execute_multiple_premises_partial", () => {
    chain.add("p q r");
    chain.add("p");
    const count = chain.execute((rule) => false);
    expect(count).toBe(1);
});

test("execute_three_premises", () => {
    chain.add("p q r s");
    chain.add("p");
    chain.add("q");
    chain.add("r");
    const target = new Rule("s");
    let success = false;
    const count = chain.execute((rule) => {
        if (rule.key() === target.key()) {
            success = true;
        }
        return false;
    });
    expect(count).toBe(3);
    expect(success).toBe(true);
});

test("execute_duplicated_fact", () => {
    chain.add("p r");
    chain.add("q r");
    chain.add("p");
    chain.add("q");
    const count = chain.execute((rule) => false);
    expect(count).toBe(1);
});

test("execute_exceed", () => {
    chain.set_limit_size(100);
    expect(chain.add("(2 `x) (`x `x`)")).toBe(true);
    expect(chain.add("(2 a-very-long-fact-that-exceeds-half-of-the-limit-size)")).toBe(true);
    const count = chain.execute((rule) => false);
    expect(count).toBe(0);
});

test("dont_generate_duplicated_fact", () => {
    expect(chain.add("aaaaa bbbbb")).toBe(true);
    expect(chain.add("aaaaa")).toBe(true);
    expect(chain.execute((rule) => false)).toBe(1);
    expect(chain.execute((rule) => false)).toBe(0);
});

test("execute_exceed_by_too_many_premises", () => {
    const newChain = new Chain(100, 1000);
    expect(newChain.add("aaaaa bbbbb ccccc ddddd eeeee fffff")).toBe(true);
    expect(newChain.add("aaaaa")).toBe(true);
    expect(newChain.add("bbbbb")).toBe(true);
    expect(newChain.add("ccccc")).toBe(true);
    expect(newChain.add("ddddd")).toBe(true);
    expect(newChain.add("eeeee")).toBe(true);
    expect(newChain.execute((rule) => false)).toBe(5);

    newChain.reset();
    newChain.set_limit_size(100);
    newChain.set_buffer_size(1000);
    expect(newChain.add("aaaaa bbbbb ccccc ddddd eeeee fffff")).toBe(true);
    expect(newChain.add("aaaaa")).toBe(true);
    expect(newChain.add("bbbbb")).toBe(true);
    expect(newChain.add("ccccc")).toBe(true);
    expect(newChain.add("ddddd")).toBe(true);
    expect(newChain.add("eeeee")).toBe(true);
    expect(newChain.execute((rule) => false)).toBe(5);

    newChain.reset();
    newChain.set_limit_size(100);
    newChain.set_buffer_size(100);
    expect(newChain.add("aaaaa bbbbb ccccc ddddd eeeee fffff")).toBe(true);
    expect(newChain.add("aaaaa")).toBe(true);
    expect(newChain.add("bbbbb")).toBe(true);
    expect(newChain.add("ccccc")).toBe(true);
    expect(newChain.add("ddddd")).toBe(true);
    expect(newChain.add("eeeee")).toBe(true);
    expect(newChain.execute((rule) => false)).toBe(1);
});

test("iterator", () => {
    chain.add("a");
    chain.add("b");
    chain.add("a b c");
    const expected = ["b\n----\nc\n", "----\nc\n"];
    let count = 0;
    for (const rule of chain) {
        expect(count).toBeLessThan(expected.length);
        expect(rule.toString()).toBe(expected[count]);
        count++;
    }
    expect(count).toBe(expected.length);
});
