
# =========================================
#       IMPORTS
# --------------------------------------


from __future__ import print_function

import rootpath

rootpath.append()

from inspecta.tests import helper

import inspecta

from os import environ as env

env['COLORS'] = 'true' # lower prio
env['VERBOSE'] = 'true' # lower prio

env['INSPECTOR_COLORS'] = 'false' # higher prio
env['INSPECTOR_VERBOSE'] = 'false' # higher prio


# =========================================
#       HELPERS
# --------------------------------------

def trim(string):
    return string.replace(' ', '').replace('\n', '')


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    def test__import(self):
        self.assertModule(inspecta)

    def test_inspect(self):
        self.assertTrue(callable(inspecta.inspect))

        with self.assertRaises(Exception):
            self.assertEqual(inspecta.inspect(), '')

        with self.assertNotRaises(Exception):
            result = inspecta.inspect(None)
            result = trim(result)

        self.assertEqual(result, 'None')

        with self.assertNotRaises(Exception):
            result = inspecta.inspect({})
            result = trim(result)

        self.assertEqual(result, '{}')

        with self.assertNotRaises(Exception):
            result = inspecta.inspect({'foo': 'bar'})
            result = trim(result)

        self.assertEqual(result, "{'foo':'bar'}")

        with self.assertNotRaises(Exception):
            result = inspecta.inspect({
                'foo': {
                    'bar': {
                        'baz': [
                            {
                                'a': 1,
                                'b': 'two',
                                'c': ('three', 4, 'five')
                            }
                        ]
                    }
                },
                'bar': [1, 2, 3],
                'baz': True
            })
            result = trim(result)

        self.assertEqual(result, "{'bar':[1,2,3],'baz':True,'foo':{'bar':{'baz':[{'a':1,'b':'two','c':('three',4,'five')}]}}}")

        with self.assertNotRaises(Exception):
            result = inspecta.inspect([])
            result = trim(result)

        self.assertEqual(result, '[]')

        with self.assertNotRaises(Exception):
            result = inspecta.inspect([1, 2, 3])
            result = trim(result)

        self.assertEqual(result, '[1,2,3]')

        with self.assertNotRaises(Exception):
            result = inspecta.inspect([
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                },
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                }
            ])
            result = trim(result)

        self.assertEqual(result, "[{'bar':[1,2,3],'baz':True,'foo':{'bar':{'baz':[{'a':1,'b':'two','c':('three',4,'five')}]}}},{'bar':[1,2,3],'baz':True,'foo':{'bar':{'baz':[{'a':1,'b':'two','c':('three',4,'five')}]}}}]")

        with self.assertNotRaises(Exception):
            result = inspecta.inspect(())
            result = trim(result)

        self.assertEqual(result, '()')

        with self.assertNotRaises(Exception):
            result = inspecta.inspect((1, 2, 3))
            result = trim(result)

        self.assertEqual(result, '(1,2,3)')

        with self.assertNotRaises(Exception):
            result = inspecta.inspect((
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                },
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                }
            ))
            result = trim(result)

        self.assertEqual(result, "({'bar':[1,2,3],'baz':True,'foo':{'bar':{'baz':[{'a':1,'b':'two','c':('three',4,'five')}]}}},{'bar':[1,2,3],'baz':True,'foo':{'bar':{'baz':[{'a':1,'b':'two','c':('three',4,'five')}]}}})")

        with self.assertNotRaises(Exception):
            result = inspecta.inspect((
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                },
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                }
            ), colors = True)
            result = trim(result)

        self.assertNotEqual(result, "({'bar':[1,2,3],'baz':True,'foo':{'bar':{'baz':[{'a':1,'b':'two','c':('three',4,'five')}]}}},{'bar':[1,2,3],'baz':True,'foo':{'bar':{'baz':[{'a':1,'b':'two','c':('three',4,'five')}]}}})")
        self.assertTrue(u"\x1b[" in result)

    def test_print(self):
        self.assertTrue(callable(inspecta.print))

        with self.assertRaises(Exception):
            inspecta.print()

        with self.assertNotRaises(Exception):
            inspecta.print(None)

        with self.assertNotRaises(Exception):
            inspecta.print({})

        with self.assertNotRaises(Exception):
            inspecta.print({'foo': 'bar'})

        with self.assertNotRaises(Exception):
            inspecta.print({
                'foo': {
                    'bar': {
                        'baz': [
                            {
                                'a': 1,
                                'b': 'two',
                                'c': ('three', 4, 'five')
                            }
                        ]
                    }
                },
                'bar': [1, 2, 3],
                'baz': True
            })

        with self.assertNotRaises(Exception):
            inspecta.print([])

        with self.assertNotRaises(Exception):
            inspecta.print([1, 2, 3])

        with self.assertNotRaises(Exception):
            inspecta.print([
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                },
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                }
            ])

        with self.assertNotRaises(Exception):
            inspecta.print(())

        with self.assertNotRaises(Exception):
            inspecta.print((1, 2, 3))

        with self.assertNotRaises(Exception):
            inspecta.print((
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                },
                {
                    'foo': {
                        'bar': {
                            'baz': [
                                {
                                    'a': 1,
                                    'b': 'two',
                                    'c': ('three', 4, 'five')
                                }
                            ]
                        }
                    },
                    'bar': [1, 2, 3],
                    'baz': True
                }
            ))


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':
    helper.run(TestCase)
