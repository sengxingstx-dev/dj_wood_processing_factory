import random
import string


def generate_unique_identifier():
    # Generate a random alphanumeric string of length 6
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
