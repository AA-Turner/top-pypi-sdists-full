import time
import apyds


def main():
    temp_data_size = 1000
    temp_text_size = 1000
    single_result_size = 10000

    apyds.buffer_size(temp_text_size)
    search = apyds.Search(temp_data_size, single_result_size)

    # P -> Q, P |- Q
    search.add("(`P -> `Q) `P `Q")
    # p -> (q -> p)
    search.add("(`p -> (`q -> `p))")
    # (p -> (q -> r)) -> ((p -> q) -> (p -> r))
    search.add("((`p -> (`q -> `r)) -> ((`p -> `q) -> (`p -> `r)))")
    # (!p -> !q) -> (q -> p)
    search.add("(((! `p) -> (! `q)) -> (`q -> `p))")

    # premise
    search.add("(! (! X))")

    target = apyds.Rule("X")

    while True:
        success = False

        def callback(candidate: apyds.Rule) -> bool:
            if candidate == target:
                print("Found!")
                print(candidate)
                nonlocal success
                success = True
                return True
            return False

        search.execute(callback)
        if success:
            break


for i in range(10):
    begin = time.time()
    main()
    end = time.time()
    print(f"Execution time: {end - begin:.8f} seconds")
