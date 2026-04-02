#include <chrono>
#include <cstring>
#include <functional>
#include <iostream>

#include <ds/ds.hh>
#include <ds/search.hh>
#include <ds/utility.hh>

void run() {
    int temp_data_size = 1000;
    int temp_text_size = 1000;
    int single_result_size = 10000;

    auto search = ds::search_t(temp_data_size, single_result_size);

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

    auto target = ds::text_to_rule("X", temp_data_size);

    while (true) {
        bool success = false;

        auto callback = [&target, &success, &temp_text_size](ds::rule_t* candidate) {
            if (candidate->data_size() != target->data_size()) {
                return false;
            }
            auto data_size = candidate->data_size();
            auto equal = memcmp(candidate->head(), target->head(), data_size) == 0;
            if (equal) {
                printf("Found!\n");
                printf("%s", ds::rule_to_text(candidate, temp_text_size).get());
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

void timer(std::function<void()> func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    std::cout << "Execution time: " << duration.count() << " seconds" << std::endl;
}

int main() {
    for (auto i = 0; i < 10; ++i) {
        timer(run);
    }
}
