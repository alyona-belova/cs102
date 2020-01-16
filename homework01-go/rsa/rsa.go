package rsa

import (
	"errors"
	"math"
	"math/big"
	"math/rand"
)

type Key struct {
	key, n int
}

type KeyPair struct {
	Private, Public Key
}

func isPrime(n int) bool {
	if n == 2 || n == 1 {
		return true
	}

	if n < 2 {
		return false
	}

	for i := 2; i <= int(math.Floor(math.Sqrt(float64(n)))); i++ {
		if n%i == 0 {
			return false
		}
	}
	return true
}

func gcd(a int, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func multiplicativeInverse(e int, phi int) int {
	var x int

	var history []int

	for e%phi > 0 {
		history = append(history, int(e/phi))
		e, phi = phi, e%phi
	}

	x = 0
	y := 1

	for i := len(history) - 1; i >= 0; i-- {
		prevX := x
		x = y
		y = prevX - y*(history[i])
	}

	return x
}

//GenerateKeypair generates keypair
func GenerateKeypair(p int, q int) (KeyPair, error) {
	var n int
	var phi int
	if !isPrime(p) || !isPrime(q) {
		return KeyPair{}, errors.New("both numbers must be prime")
	} else if p == q {
		return KeyPair{}, errors.New("p and q can't be equal")
	}

	n = p * q

	phi = (p - 1) * (q - 1)

	e := rand.Intn(phi-1) + 1
	g := gcd(e, phi)

	for g != 1 {
		e = rand.Intn(phi-1) + 1
		g = gcd(e, phi)
	}

	d := multiplicativeInverse(e, phi)

	return KeyPair{Key{e, n}, Key{d, n}}, nil
}

//Encrypt encrypts plaintext using a RSA cipher
func Encrypt(pk Key, plaintext string) []int {
	cipher := []int{}
	n := new(big.Int)
	for _, ch := range plaintext {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		cipher = append(cipher, int(n.Int64()))
	}
	return cipher
}

//Decrypt decrypts a ciphertext using a RSA cipher.
func Decrypt(pk Key, cipher []int) string {
	plaintext := ""
	n := new(big.Int)
	for _, ch := range cipher {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		plaintext += string(rune(int(n.Int64())))
	}
	return plaintext
}
