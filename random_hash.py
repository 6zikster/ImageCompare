import random   
hash = ''.join(random.choice('01') for _ in range(1024))
with open('NewHash.txt', 'w') as file:
    # Write the string to the file
    file.write(hash)
