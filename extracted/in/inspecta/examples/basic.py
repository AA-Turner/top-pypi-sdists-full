
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()


# =========================================
#       EXAMPLE
# --------------------------------------

import inspecta

data = {
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

print('\n.inspect(data)\n')

print(inspecta.inspect(data))

print('\n.print(data)\n')

inspecta.print(data)
