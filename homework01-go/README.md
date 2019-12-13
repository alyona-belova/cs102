$ go test -v ./caesar  
=== RUN   TestEncryptCaesar  
--- PASS: TestEncryptCaesar (0.00s)  
=== RUN   TestDecryptCaesar  
--- PASS: TestDecryptCaesar (0.00s)  
PASS  
ok  	_/home/alena/cs102/homework01-go/caesar	0.002s  

----------------------------------------------------------------------
$ go test -v ./rsa  
=== RUN   TestIsPrime  
--- PASS: TestIsPrime (0.00s)  
=== RUN   TestGCD  
--- PASS: TestGCD (0.00s)  
=== RUN   TestMultiplicativeInverse  
--- PASS: TestMultiplicativeInverse (0.00s)  
=== RUN   TestEncrypt  
--- PASS: TestEncrypt (0.00s)  
=== RUN   TestDecrypt  
--- PASS: TestDecrypt (0.00s)  
PASS  
ok  	_/home/alena/cs102/homework01-go/rsa	0.002s  

----------------------------------------------------------------------
$ go test -v ./vigenere  
=== RUN   TestEncryptVigenere  
--- PASS: TestEncryptVigenere (0.00s)  
=== RUN   TestDecryptVigenere  
--- PASS: TestDecryptVigenere (0.00s)  
PASS  
ok  	_/home/alena/cs102/homework01-go/vigenere	0.003s  

----------------------------------------------------------------------
$ go run main.go -p=11 -q=17 -text=very_secret  
Encrypted message: [84 50 113 110 184 174 50 143 113 50 24]  
Decrypted message: very_secret  
