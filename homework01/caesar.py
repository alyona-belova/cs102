def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if ('a' <= i <= 'w') or ('A' <= i <= 'W'):
            ciphertext += chr(ord(i) + 3)
        elif ('x' <= i <= 'z') or ('X' <= i <= 'Z'):
            ciphertext += chr(ord(i) - 23)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if ('d' <= i <= 'z') or ('D' <= i <= 'Z'):
            plaintext += chr(ord(i) - 3)
        elif ('a' <= i <= 'c') or ('A' <= i <= 'C'):
            plaintext += chr(ord(i) + 23)
        else:
            plaintext += i
    return plaintext
