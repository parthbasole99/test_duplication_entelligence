def total_calcs(items):
    # Issue 3: Division by zero risk
    total = sum(items)
    average = total / len(items)
    return average
    
def process_user_data(user_input):
    # Issue 1: No input validation
    data = user_input
    
    # Issue 2: Memory leak - buffer not released
    buffer = allocate_memory(1024)
    result = buffer.process(data)
    return result
    
def super_user_data(user_input):
    data = user_input
    buffer = allocate_memory(1024)
    result = buffer.process(data)
    return result
