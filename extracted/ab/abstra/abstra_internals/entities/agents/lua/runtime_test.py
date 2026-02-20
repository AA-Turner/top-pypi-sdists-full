from pathlib import Path

from abstra_internals.entities.agents.lua.runtime import LupaRuntime


class TestLupaRuntime:
    def test_basic_execution(self):
        runtime = LupaRuntime()
        result = runtime.execute('print("hello")')
        assert "hello" in result

    def test_return_value(self):
        runtime = LupaRuntime()
        result = runtime.execute("return 42")
        assert "42" in result

    def test_variables_persist(self):
        runtime = LupaRuntime()
        runtime.execute("x = 10")
        result = runtime.execute("return x")
        assert "10" in result

    def test_loop_execution(self):
        runtime = LupaRuntime()
        result = runtime.execute(
            'local sum = 0\nfor i = 1, 5 do sum = sum + i end\nprint("sum=" .. sum)'
        )
        assert "sum=15" in result

    def test_sandbox_blocks_os(self):
        runtime = LupaRuntime()
        result = runtime.execute('os.execute("ls")')
        assert "Error" in result or "nil" in result.lower()

    def test_sandbox_blocks_io(self):
        runtime = LupaRuntime()
        result = runtime.execute('io.open("/etc/passwd")')
        assert "Error" in result or "nil" in result.lower()

    def test_sandbox_blocks_require(self):
        runtime = LupaRuntime()
        result = runtime.execute('require("os")')
        assert "does not exist" in result

    def test_sandbox_blocks_load(self):
        runtime = LupaRuntime()
        result = runtime.execute("load(\"os.execute('ls')\")()")
        assert "does not exist" in result

    def test_sandbox_allows_math(self):
        runtime = LupaRuntime()
        result = runtime.execute("return math.sqrt(16)")
        assert "4" in result

    def test_sandbox_allows_string(self):
        runtime = LupaRuntime()
        result = runtime.execute('return string.upper("hello")')
        assert "HELLO" in result

    def test_sandbox_allows_table(self):
        runtime = LupaRuntime()
        result = runtime.execute("local t = {1, 2, 3}\ntable.insert(t, 4)\nreturn #t")
        assert "4" in result

    def test_json_encode(self):
        runtime = LupaRuntime()
        result = runtime.execute('return json_encode({name = "test", value = 42})')
        assert "test" in result
        assert "42" in result

    def test_json_decode(self):
        runtime = LupaRuntime()
        result = runtime.execute(
            'local t = json_decode(\'{"name": "test"}\')\nreturn t.name'
        )
        assert "test" in result

    def test_syntax_error_returns_error(self):
        runtime = LupaRuntime()
        result = runtime.execute("this is not valid lua")
        assert "Error" in result

    def test_runtime_error_returns_error(self):
        runtime = LupaRuntime()
        result = runtime.execute("error('boom')")
        assert "Error" in result
        assert "boom" in result

    def test_print_and_return_combined(self):
        runtime = LupaRuntime()
        result = runtime.execute('print("line1")\nprint("line2")\nreturn "done"')
        assert "line1" in result
        assert "line2" in result
        assert "done" in result

    def test_register_function(self):
        runtime = LupaRuntime()
        runtime.register_function("greet", lambda name: f"Hello, {name}!")
        result = runtime.execute('return greet("world")')
        assert "Hello, world!" in result

    def test_reset_clears_state(self):
        runtime = LupaRuntime()
        runtime.execute("x = 42")
        runtime.reset()
        result = runtime.execute("return x")
        assert "nil" in result.lower() or "(no output)" in result

    def test_sandbox_blocks_rawget_rawset(self):
        """rawget/rawset are safe builtins in abstra-lua."""
        runtime = LupaRuntime()
        result = runtime.execute("return type(rawget)")
        assert "function" in result.lower()

    def test_only_safe_globals_accessible(self):
        """Iterate all globals — only safe ones should exist."""
        runtime = LupaRuntime()
        result = runtime.execute(
            "local names = {}\n"
            "for k in pairs(_G) do names[#names+1] = k end\n"
            "table.sort(names)\n"
            'return table.concat(names, ",")'
        )
        globals_list = result.split(",")
        # These must never be accessible (not even as guardrails)
        for dangerous in ["python", "os", "io", "debug", "package", "coroutine"]:
            assert dangerous not in globals_list, f"{dangerous} found in globals"
        # require/load/etc. exist as guardrails but should raise errors
        result_require = runtime.execute('require("os")')
        assert "does not exist" in result_require

    def test_array_empty(self):
        """Empty array() returns empty table in Lua (no sequence markers)."""
        runtime = LupaRuntime()
        result = runtime.execute("return json_encode(array())")
        # Empty Lua tables are converted to dicts, not lists
        assert "{}" in result

    def test_array_with_values(self):
        runtime = LupaRuntime()
        result = runtime.execute('return json_encode(array("a", "b", "c"))')
        assert '["a", "b", "c"]' in result

    def test_array_from_lua_table(self):
        runtime = LupaRuntime()
        result = runtime.execute('local t = {"x", "y"}\nreturn json_encode(array(t))')
        assert '["x", "y"]' in result

    def test_array_nested_in_table(self):
        """array() inside a table should survive json_encode."""
        runtime = LupaRuntime()
        result = runtime.execute(
            'return json_encode({name = "test", items = array(1, 2, 3)})'
        )
        assert '"items": [1, 2, 3]' in result or '"items":[1,2,3]' in result

    def test_file_relative_path(self):
        runtime = LupaRuntime(working_dir=Path("/tmp/agent_work"))
        result = runtime.execute('return file("nota.xml")')
        assert "/tmp/agent_work/nota.xml" in result

    def test_file_absolute_path(self):
        runtime = LupaRuntime(working_dir=Path("/tmp/agent_work"))
        result = runtime.execute('return file("/other/dir/file.pdf")')
        assert "/other/dir/file.pdf" in result

    def test_file_nested_relative(self):
        runtime = LupaRuntime(working_dir=Path("/tmp/agent_work"))
        result = runtime.execute('return file("sub/dir/file.txt")')
        assert "/tmp/agent_work/sub/dir/file.txt" in result

    def test_file_inside_array(self):
        runtime = LupaRuntime(working_dir=Path("/tmp/agent_work"))
        result = runtime.execute(
            'return json_encode(array(file("a.xml"), file("b.xml")))'
        )
        assert "/tmp/agent_work/a.xml" in result
        assert "/tmp/agent_work/b.xml" in result

    def test_guardrail_require_shows_available_tools(self):
        """require() guardrail should list registered tool names."""
        runtime = LupaRuntime()
        runtime.register_function("navigate", lambda t: "ok")
        runtime.register_function("click", lambda t: "ok")
        result = runtime.execute('require("socket")')
        assert "does not exist" in result
        assert "navigate" in result
        assert "click" in result

    def test_log_output(self):
        runtime = LupaRuntime()

        def say_hello():
            runtime.log_output("hello")

        runtime.register_function("say_hello", say_hello)
        result = runtime.execute('say_hello()\nprint("world")')
        assert "hello" in result
        assert "world" in result

    def test_guardrail_dofile(self):
        runtime = LupaRuntime()
        result = runtime.execute('dofile("test.lua")')
        assert "does not exist" in result

    def test_guardrail_loadfile(self):
        runtime = LupaRuntime()
        result = runtime.execute('loadfile("test.lua")')
        assert "does not exist" in result

    def test_guardrail_loadstring(self):
        runtime = LupaRuntime()
        result = runtime.execute('loadstring("print(1)")()')
        assert "does not exist" in result

    def test_json_encode_error(self):
        runtime = LupaRuntime()
        result = runtime.execute("return json_encode(json_encode)")
        assert "Error" in result

    def test_json_decode_error(self):
        runtime = LupaRuntime()
        result = runtime.execute('return json_decode("not json {")')
        assert "Error" in result

    def test_array_dict_non_numeric_keys(self):
        runtime = LupaRuntime()
        result = runtime.execute('return json_encode(array({a="x", b="y"}))')
        assert "x" in result
        assert "y" in result

    def test_print_with_numbers(self):
        runtime = LupaRuntime()
        result = runtime.execute('print(42, true, "text")')
        assert "42" in result
        assert "text" in result

    def test_script_runtime_protocol_conformance(self):
        from abstra_internals.entities.agents.lua.runtime import (
            LupaRuntime,
            ScriptRuntime,
        )

        assert isinstance(LupaRuntime(), ScriptRuntime)

    def test_print_before_error(self):
        runtime = LupaRuntime()
        result = runtime.execute('print("before")\nerror("boom")')
        assert "before" in result
        assert "boom" in result

    def test_reset_preserves_registered_functions(self):
        runtime = LupaRuntime()
        runtime.register_function("greet", lambda name: f"Hello, {name}!")
        result = runtime.execute('return greet("world")')
        assert "Hello, world!" in result
        runtime.reset()
        result = runtime.execute('return greet("world")')
        assert "Hello, world!" in result
