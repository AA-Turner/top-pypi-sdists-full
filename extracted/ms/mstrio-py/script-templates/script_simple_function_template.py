# x is a scalar input
# y is a scalar input
# Metric expression example: ScriptFunctionSimple<_InputNames="x, y", _ScriptName=”minus_two_numbers”>(Revenue, Cost)

def minus_two_numbers(x, y):
    return x - y

# must-have method which returns the values served as the metric evaluation results. 
def get_results():
    return minus_two_numbers($x, $y)


print(get_results())
