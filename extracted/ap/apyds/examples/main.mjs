import { Rule, Search, buffer_size } from "../atsds/index.mts";

function main() {
    const temp_data_size = 1000;
    const temp_text_size = 1000;
    const single_result_size = 10000;

    buffer_size(temp_text_size);
    const search = new Search(temp_data_size, single_result_size);

    // P -> Q, P |- Q
    search.add("(`P -> `Q) `P `Q");
    // p -> (q -> p)
    search.add("(`p -> (`q -> `p))");
    // (p -> (q -> r)) -> ((p -> q) -> (p -> r))
    search.add("((`p -> (`q -> `r)) -> ((`p -> `q) -> (`p -> `r)))");
    // (!p -> !q) -> (q -> p)
    search.add("(((! `p) -> (! `q)) -> (`q -> `p))");

    // premise
    search.add("(! (! X))");

    const target = new Rule("X");

    while (true) {
        let success = false;

        const callback = (candidate) => {
            if (candidate.key() === target.key()) {
                console.log("Found!");
                console.log(candidate.toString());
                success = true;
                return true;
            }
            return false;
        };

        search.execute(callback);
        if (success) {
            break;
        }
    }
}

for (let i = 0; i < 10; i++) {
    const begin = new Date();
    main();
    const end = new Date();
    console.log(`Execution time: ${(end - begin) / 1000} seconds`);
}
