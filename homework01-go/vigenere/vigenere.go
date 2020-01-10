package vigenere

//EncryptVigenere encrypts plaintext using a Vigenere cipher
func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string
	var minusOrd, shift, letterOrd int

	keywordInd := 0

	for ind := 0; ind < len(plaintext); ind++ {
		if keyword[keywordInd] >= 'A' && keyword[keywordInd] <= 'Z' {
			minusOrd = 'A'
		} else {
			minusOrd = 'a'
		}

		shift = int(keyword[keywordInd]) - minusOrd
		letter := plaintext[ind]

		if letter >= 'A' && letter <= 'Z' {
			letterOrd = 'A'
		} else if letter >= 'a' && letter <= 'z' {
			letterOrd = 'a'
		} else {
			ciphertext += string(letter)
			continue
		}

		letterOrd += (int(letter) - letterOrd + shift) % 26
		ciphertext += string(letterOrd)
		keywordInd = (keywordInd + 1) % len(keyword)
	}

	return ciphertext
}

//DecryptVigenere decrypts a ciphertext using a Vigenere cipher
func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string
	var minusOrd, shift, letterOrd int

	keywordInd := 0

	for i := 0; i < len(ciphertext); i++ {
		if keyword[keywordInd] >= 'A' && keyword[keywordInd] <= 'Z' {
			minusOrd = 'A'
		} else {
			minusOrd = 'a'
		}

		shift = int(keyword[keywordInd]) - minusOrd
		letter := ciphertext[i]

		if letter >= 'A' && letter <= 'Z' {
			letterOrd = 'Z'
		} else if letter >= 'a' && letter <= 'z' {
			letterOrd = 'z'
		} else {
			plaintext += string(letter)
			continue
		}

		letterOrd -= (letterOrd - int(letter) + shift) % 26
		plaintext += string(letterOrd)

		keywordInd = (keywordInd + 1) % len(keyword)

	}

	return plaintext
}
