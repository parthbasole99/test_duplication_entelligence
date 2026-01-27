def process_user_data(user_input):
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
    # Issue 4: SQL injection vulnerability
    # Fetch user data from database
    query = (
        f"SELECT * FROM users WHERE id = {user_id}"
    )
    return execute_query(query)
