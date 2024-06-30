# Permutation 10
P10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]

# Permutation 8
P8 = [5, 2, 6, 3, 7, 4, 9, 8]

# Initial permutation IP
IP = [1, 5, 2, 0, 3, 7, 4, 6]

# Inverse initial permutation IP^-1
IP_INV = [3, 0, 2, 4, 6, 1, 7, 5]

# Expansion permutation E/P
EP = [3, 0, 1, 2, 1, 2, 3, 0]

# Permutation 4
P4 = [1, 3, 2, 0]

# S-Box Definitions
S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

# Left shift for key generation
LS = [1, 2, 2, 2]

# Permute according to table
def permute(input_str, permutation):
    return ''.join(input_str[i] for i in permutation)

# Left circular shift
def left_circular_shift(key, n):
    return key[n:] + key[:n]

# Generate subkeys
def generate_subkeys(key):
    key = permute(key, P10)
    subkeys = []
    for i in range(4):
        key = left_circular_shift(key[:5], LS[i]) + left_circular_shift(key[5:], LS[i])
        subkeys.append(permute(key, P8))
    return subkeys

# XOR operation on two strings
def xor(a, b):
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))

# S-Box lookup
def sbox_lookup(input_str, sbox):
    row = int(input_str[0] + input_str[3], 2)
    col = int(input_str[1:3], 2)
    return format(sbox[row][col], '02b')

# S-DES encryption function
def sdes_encrypt(plaintext, key):
    subkeys = generate_subkeys(key)
    # Initial Permutation
    permuted_text = permute(plaintext, IP)
    left_half = permuted_text[:4]
    right_half = permuted_text[4:]

    # Round 1
    expanded_right = permute(right_half, EP)
    xor_result = xor(expanded_right, subkeys[0])
    s0_input = xor_result[:4]
    s1_input = xor_result[4:]
    s0_output = sbox_lookup(s0_input, S0)
    s1_output = sbox_lookup(s1_input, S1)
    permuted_xor = permute(s0_output + s1_output, P4)
    xor_with_left = xor(permuted_xor, left_half)
    left_half = right_half
    right_half = xor_with_left

    # Round 2
    expanded_right = permute(right_half, EP)
    xor_result = xor(expanded_right, subkeys[1])
    s0_input = xor_result[:4]
    s1_input = xor_result[4:]
    s0_output = sbox_lookup(s0_input, S0)
    s1_output = sbox_lookup(s1_input, S1)
    permuted_xor = permute(s0_output + s1_output, P4)
    xor_with_left = xor(permuted_xor, left_half)
    encrypted_text = xor_with_left + right_half

    # Inverse Initial Permutation
    return permute(encrypted_text, IP_INV)

# S-DES decryption function
def sdes_decrypt(ciphertext, key):
    subkeys = generate_subkeys(key)
    # Initial Permutation
    permuted_text = permute(ciphertext, IP)
    left_half = permuted_text[:4]
    right_half = permuted_text[4:]

    # Round 1
    expanded_right = permute(right_half, EP)
    xor_result = xor(expanded_right, subkeys[1]) # Subkeys used in reverse order
    s0_input = xor_result[:4]
    s1_input = xor_result[4:]
    s0_output = sbox_lookup(s0_input, S0)
    s1_output = sbox_lookup(s1_input, S1)
    permuted_xor = permute(s0_output + s1_output, P4)
    xor_with_left = xor(permuted_xor, left_half)
    left_half = right_half
    right_half = xor_with_left

    # Round 2
    expanded_right = permute(right_half, EP)
    xor_result = xor(expanded_right, subkeys[0]) # Subkeys used in reverse order
    s0_input = xor_result[:4]
    s1_input = xor_result[4:]
    s0_output = sbox_lookup(s0_input, S0)
    s1_output = sbox_lookup(s1_input, S1)
    permuted_xor = permute(s0_output + s1_output, P4)
    xor_with_left = xor(permuted_xor, left_half)
    decrypted_text = xor_with_left + right_half

    # Inverse Initial Permutation
    return permute(decrypted_text, IP_INV)

plaintext = list(input("Enter a 8-bit Plaintext: "))
# Ensure the input is a valid 8-bit binary string
while len(plaintext) != 8 or not all(char in '01' for char in plaintext):
  plaintext = list(input("Invalid key. Enter a 8-bit binary string: "))

key = list(input("Enter a 10-bit key: "))
# Ensure the input is a valid 10-bit binary string
while len(key) != 10 or not all(char in '01' for char in key):
  key = list(input("Invalid key. Enter a 10-bit binary string: "))

encrypted_text = sdes_encrypt(plaintext, key)
print("Encrypted text:", encrypted_text)
decrypted_text = sdes_decrypt(encrypted_text, key)
print("Decrypted text:", decrypted_text)