def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i, a in enumerate(plaintext):
        if 'A' <= a <= 'Z':
            number = ord(a) + ord(keyword[i % len(keyword)]) - ord('A')
            if number > ord('Z'):
                number -= 26
            ciphertext += chr(number)
        elif 'a' <= a <= 'z':
            number = ord(a) + ord(keyword[i % len(keyword)]) - ord('a')
            if number > ord('z'):
                number -= 26
            ciphertext += chr(number)
        else:
            chiphertext += a
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i, a in enumerate(ciphertext):
        if 'A' <= a <= 'Z':
            number = ord(a) - ord(keyword[i % len(keyword)]) + ord('A')
            if number < ord('A'):
                number += 26
            plaintext += chr(number)
        elif 'a' <= a <= 'z':
            number = ord(a) - ord(keyword[i % len(keyword)]) + ord('a')
            if number < ord('a'):
                number += 26
            plaintext += chr(number)
        else:
            plaintext += a
    return plaintext
