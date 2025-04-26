from dataclasses import dataclass
from test_results_parser import build_message, shorten_file_paths


@dataclass
class TestRunsPayload:
    failed = 0
    passed = 0
    skipped = 0
    failures = []

@dataclass
class Run:
    name = ""
    testsuite = ""
    failure_message = ""
    duration = 0.0 


def test_shorten_file_paths():
    with open('./tests/windows.junit.xml') as f:
        failure_message = f.read()

    res = shorten_file_paths(failure_message)

    assert res == """Error: expect(received).toBe(expected) // Object.is equality

Expected: 4
Received: 5
at Object.&lt;anonymous&gt;
(.../demo/calculator/calculator.test.ts:5:26)
at Promise.then.completed
(.../jest-circus/build/utils.js:298:28)
at new Promise (&lt;anonymous&gt;)
at callAsyncCircusFn
(.../jest-circus/build/utils.js:231:10)
at _callCircusTest
(.../jest-circus/build/run.js:316:40)
at processTicksAndRejections (node:internal/process/task_queues:95:5)
at _runTest
(.../jest-circus/build/run.js:252:3)
at _runTestsForDescribeBlock
(.../jest-circus/build/run.js:126:9)
at run
(.../jest-circus/build/run.js:71:3)
at runAndTransformResultsToJestFormat
(.../build/legacy-code-todo-rewrite/jestAdapterInit.js:122:21)
at jestAdapter
(.../build/legacy-code-todo-rewrite/jestAdapter.js:79:19)
at runTestInternal
(.../jest-runner/build/runTest.js:367:16)
at runTest
(.../jest-runner/build/runTest.js:444:34)"""

def test_shorten_file_paths_short_path():
    failure_message = "short/file/path.txt"
    res = shorten_file_paths(failure_message)
    assert res == failure_message

def test_shorten_file_paths_long_path():
    failure_message = "very/long/file/path/should/be/shortened.txt"
    res = shorten_file_paths(failure_message)
    assert res == ".../should/be/shortened.txt"

def test_shorten_file_paths_long_path_leading_slash():
    failure_message = "/very/long/file/path/should/be/shortened.txt"
    res = shorten_file_paths(failure_message)
    assert res == ".../should/be/shortened.txt"

def test_build_message_no_failures():
    payload = TestRunsPayload()
    res = build_message(payload)

    assert res == """:white_check_mark: All tests successful. No failed tests were found.

:mega: Thoughts on this report? [Let Codecov know!](https://github.com/codecov/feedback/issues/304) | Powered by [Codecov](https://about.codecov.io/)"""


def test_build_message():
    run1 = Run()
    run2 = Run()
    run3 = Run()
    run4 = Run()

    run1.testsuite = "hello"
    run1.name = "test_name_run1"
    run1.failure_message = "Shared \n\n\n\n <pre> ````````\n \r\n\r\n | test | test | test </pre>failure message"
    run1.duration = 0.098
    run1.build_url = None

    run2.testsuite = "hello"
    run2.name = "test_name_run2"
    run2.failure_message = None
    run2.duration = 0.07
    run2.build_url = "https://example.com/build"

    run3.testsuite = "hello"
    run3.name = "don't show; too slow"
    run3.failure_message = None
    run3.duration = 0.101
    run3.build_url = "https://example.com/build_no_show"

    run4.testsuite = "hello"
    run4.name = "test_name_run4"
    run4.failure_message = "This is the fastest run"
    run4.duration = 0.001
    run4.build_url = "https://example.com/build_fast"

    payload = TestRunsPayload()
    payload.passed = 1
    payload.failed = 4
    payload.skipped = 3
    payload.failures = [run1, run2, run3, run4]

    res = build_message(payload)

    assert res == """### :x: 4 Tests Failed:
| Tests completed | Failed | Passed | Skipped |
|---|---|---|---|
| 8 | 4 | 1 | 3 |
<details><summary>View the top 3 failed tests by shortest run time</summary>

> 
> ```
> test_name_run4
> ```
> 
> <details><summary>Stack Traces | 0.001s run time</summary>
> 
> > ```
> > This is the fastest run
> > ```
> > [View](https://example.com/build_fast) the CI Build
> 
> </details>


> 
> ```
> test_name_run2
> ```
> 
> <details><summary>Stack Traces | 0.070s run time</summary>
> 
> > ```
> > No failure message available
> > ```
> > [View](https://example.com/build) the CI Build
> 
> </details>


> 
> ```
> test_name_run1
> ```
> 
> <details><summary>Stack Traces | 0.098s run time</summary>
> 
> > `````````
> > Shared 
> > 
> > 
> > 
> >  <pre> ````````
> >  
> > 
> >  | test | test | test </pre>failure message
> > `````````
> 
> </details>


</details>

:mega: Thoughts on this report? [Let Codecov know!](https://github.com/codecov/feedback/issues/304) | Powered by [Codecov](https://about.codecov.io/)"""
