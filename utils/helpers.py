import random
import string

def generate_random_email():
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    domain = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{username}@{domain}.com"
