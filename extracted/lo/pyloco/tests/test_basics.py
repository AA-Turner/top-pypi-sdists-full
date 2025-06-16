"""pyloco unittest module
"""

import os
import unittest

import pyloco

here, myname = os.path.split(__file__)

text = "Hello World!"


class MyTaskHub(pyloco.TaskHub):

    def __init__(self):
        pass
 
    def map_data(self, paths, reduced):
 
        for path in paths:
            self.departure_data[path]["data"] = reduced["datasum"]

    def reduce_data(self, forwards):

        datasum = 0

        for pathid, data in forwards.items():
            datasum += data.get("data", 0)
        
        return {"datasum": datasum}
  

class PlusoneTask(pyloco.GroupTask):
    """adding one

T.B.D.
"""

    _name_ = "plusone"
    _version_ = "0.1.0"

    def __init__(self, parent):

        self.add_data_argument("data", required=True, type=int, help="a number to add")
        self.register_forward("sum", type=int, help="summation result")

    def reduce_data(self, forwards):

        totalsum = 0

        for pathid, data in forwards.items():
            totalsum += data.get("data", 0)

        return {"totalsum": totalsum}

    def forward_data(self, reduced):

        return {"sum": reduced["totalsum"]}

    def perform(self, targs):

        taskdef = ["input", {"argv": ["--forward", "data=int(_{data[0]:arg}_) + 1"]}]
        path1 = pyloco.TaskPath()

        path1.append_task(taskdef[0], **taskdef[1])

        clones = self.copy_taskpath(path1, 4) # share entry and exit

        hub = MyTaskHub()

        for path in clones:
            self.connect_taskpath(self, path, hub)
            self.load_data(path, data=targs.data)

        path2 = pyloco.TaskPath()

        path2.append_task(taskdef[0], **taskdef[1])
        #path2.append_task("print")

        self.connect_taskpath(hub, path2, self)



# Command-line interface
class TaskCLITests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

#    def test_usage(self):
#
#        ret, out = pyloco.perform(pyloco.OptionTask)
#
#        self.assertEqual(ret, 0)
#        self.assertIsNone(out)

    def test_input(self):

        ret, out = pyloco.perform("input", "1 --forward 'x=_{data[0]:arg}_'")

        self.assertEqual(ret, 0)
        self.assertTrue(isinstance(out, dict))
        self.assertIn("x", out)
        self.assertEqual(out["x"], "1")

    def test_print(self):

        ret, out = pyloco.perform("print", "1 -n --debug")

        self.assertEqual(ret, 0)
        self.assertTrue(isinstance(out, dict))
        self.assertIn("stdout", out)
        self.assertEqual(out["stdout"], '1')

    def test_pipe(self):

        ret, out = pyloco.perform(
            "", "--debug --reduce \"stdout=(lambda x, y: x+y, stdout)\" ",
            ("input '%s' --forward \"data=_{data[0]:arg}_\""
             " --assert-output \"data == '%s'\" -- print -n") %
            (text, text)
        )

        self.assertEqual(ret, 0)
        self.assertTrue(isinstance(out, dict))
        self.assertIn("stdout", out)
        self.assertEqual(out["stdout"], text)

    def test_assert_input(self):

        ret, out = pyloco.perform(
            "", "--reduce \"stdout=(lambda x, y: x+y, stdout)\" "
            "--debug --log assertinput", (
                "input '%s' --forward \"data=_{data[0]:arg}_\" "
                "--assert-input \"data == ['%s']\" -- print -n "
            ) % (text, text)
        )
        self.assertEqual(ret, 0)
        self.assertTrue(isinstance(out, dict))
        self.assertIn("stdout", out)
        self.assertEqual(out["stdout"], text)

    def test_plx(self):

        textout = 'Printed text is %s' % text
        textresult = 'Printed text is %s' % text
        plx = os.path.join(here, "example.plx")
        ret, out = pyloco.perform(
            plx, [
                "--debug", "--log", "testplx",
                "%s" % text, "--assert-output",
                "'textout.rstrip()==\"%s\"'" % textout
            ]
        )
        self.assertEqual(ret, 0)
        self.assertTrue(isinstance(out, dict))
        self.assertIn("textout", out)
        self.assertEqual(out["textout"].rstrip(), textresult)

    def ttest_pack(self):

        echo = os.path.join(here, "echo.py")
        plz = os.path.join(here, "..", "echotask.plz")
        ret, out = pyloco.perform(
            "pack", "--debug --log testplz",
            "'{echo}' '{text}'".format(echo=echo, text=text)
        )
        self.assertEqual(ret, 0)
        self.assertTrue(isinstance(out, dict))

        ret, out = pyloco.perform(
            plz, argv="'%s' --assert-output 'text==\"%s\"' " % (text, text)
        )

        self.assertEqual(ret, 0)
        self.assertTrue(isinstance(out, dict))

        os.remove(plz)

    def test_group(self):

        task = PlusoneTask(pyloco.PylocoManager())
        out, fwd = task.run(["1", "--multiproc", "2", "--log", "plusone.log"])
        #out, fwd = task.run(["1", "--log", "plusone.log"])

        self.assertIn("sum", fwd)
        self.assertEqual(fwd["sum"], 9)

    def test_groupcmd(self):

        ret, fwd = pyloco.perform(
                "", argv="--multiproc 3 --reduce 'x=(lambda x,y: x+y, stdout)' --clone '1,2,3' --debug", subargv="print" 
                #"", argv="--reduce 'x=(lambda x,y: x+y, stdout)' --clone '1,2,3' --debug", subargv="print" 
        )

        self.assertIn("x", fwd)
        out = fwd['x'].split("\n")
        self.assertIn("1", out)
        self.assertIn("2", out)
        self.assertIn("3", out)


    def test_global(self):

        t1 = pyloco.Task(pyloco.PylocoManager())
        t1.tglobal.test = 1

        t2 = pyloco.Task(pyloco.PylocoManager())
        self.assertEqual(t1.tglobal.test, t2.tglobal.test)

#    def test_multiproc(self):
#
#        ret, out = pyloco.perform(
#            "", "--multiproc 3 --arrange rank --debug --log testmultiproc",
#            "print 1 --assert-output 'stdout==\"1\\n\"' -- print 2"
#        )
#
#        self.assertEqual(ret, 0)
#        self.assertTrue(isinstance(out, dict))


#    def test_install(self):
#
#        echo = os.path.join(here, "echo.py")
#        ret, out = pyloco.perform(
#            "install", "--debug --log testinstall",
#            "'{echo}'".format(echo=echo)
#        )
#        self.assertEqual(ret, 0)
#        self.assertTrue(isinstance(out, dict))
#
#        ret, out = pyloco.perform("echo", argv="'%s' --assert-output
#                                  'text==\"%s\"' "%(text, text))
#
#        self.assertEqual(ret, 0)
#        self.assertTrue(isinstance(out, dict))
#
#        ret, out = pyloco.perform("uninstall",
#                                  "--debug --log testuninstall", "echo")
#        self.assertEqual(ret, 0)
#        self.assertTrue(isinstance(out, dict))


# PlX interfaace
test_classes = (TaskCLITests,)
