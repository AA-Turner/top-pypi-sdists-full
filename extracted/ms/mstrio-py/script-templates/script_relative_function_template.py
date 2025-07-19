# values is a vector input
# Metric expression example: ScriptFunctionRelative<_InputNames="values",  _ScriptName="get_running_sums", BreakBy={Year}, 
#                            SortBy={Date}>(Revenue)

def get_running_sums(values):
    # Initialize an empty list to store the running sums
    running_sums = []
    # Initialize a variable to keep track of the cumulative sum
    cumulative_sum = 0
    # Iterate through the list of values
    for value in values:
        # Update the cumulative sum with the current value
        cumulative_sum += value
        # Append the cumulative sum to the running sums list
        running_sums.append(cumulative_sum)
    return running_sums

# must-have method which returns the values served as the metric evaluation results. 
def get_results():
    return get_running_sums($values)

print(get_results())
