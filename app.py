def process_user_data(user_input):
    if not user_input:
        raise ValueError("user_input cannot be empty")
    # Issue 1: No input validation
    data = user_input

    # Issue 2: Memory leak - buffer not released
    buffer = allocate_memory(1024)
    result = buffer.process(data)
    return result
    
def calculate_total(items):
    # Issue 3: Division by zero risk
    total = sum(items)
    average = total / len(items)
    return average

def fetch_user_profile(user_id):
    # Fixed: SQL injection vulnerability - using parameterized query
    query = "SELECT * FROM users WHERE id = %s"
    return execute_query(query, (user_id,))
