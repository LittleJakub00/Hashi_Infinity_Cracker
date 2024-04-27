import hashlib
import itertools
import string
import time
import threading
import sys

# Hashi_Infinity_Cracker Version 1.04 (MD5)
#                        - Code: JJ


def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes} minutes {seconds:.2f} seconds"

def check_passwords(hash_to_crack, characters, max_length, total_combinations, result, start, end, start_time):
    combination_count = 0  # Initialize combination count
    for length in range(1, max_length + 1):
        for password in itertools.product(characters, repeat=length):
            combination_count += 1
            password = ''.join(password)
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            if hashed_password == hash_to_crack:
                end_time = time.time()
                time_elapsed = end_time - start_time
                result.append((password, time_elapsed))
                return
            
            if combination_count % 1000 == 0:
                progress = f"Progress: {combination_count}/{total_combinations}"
                sys.stdout.write('\r' + progress)
                sys.stdout.flush()


def crack_md5():
    max_length = int(input("Enter the maximum length of the password: "))

    # Define the characters to be used in generating passwords
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generating all possible combinations of passwords
    total_combinations = sum(len(characters) ** i for i in range(1, max_length + 1))
    print(f"Total combinations to check: {total_combinations}")

    hash_to_crack = input("Enter the MD5 hash to crack: ")
    start_time = time.time()  # Start time

    result = []
    threads = []
    thread_count = 1  # Adjust based on your system capabilities
    chunk_size = total_combinations // thread_count
    for i in range(thread_count):
        start = i * chunk_size + 1
        end = start + chunk_size - 1 if i < thread_count - 1 else total_combinations
        thread = threading.Thread(target=check_passwords,
                                  args=(hash_to_crack, characters, max_length, total_combinations, result, start,
                                        end, start_time))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    if result:
        password, time_elapsed = result[0]
        print("\nPassword cracked:", password)
        print("Time elapsed:", format_time(time_elapsed))
        return password
    else:
        print("Failed to crack the password.")
        return None

if __name__ == "__main__":
    # Example usage
    cracked_password = crack_md5()
