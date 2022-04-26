# encrypted-file-sharing

1. jesli komputer nie ma wygenerowanych kluczy, trzeba je wygenerowac alg. RSA

prywatny musi zostac zabezpieczony haslem
publicznym trzeba sie wymienic z drugim userem (w bezpieczny sposob)

2. do komunikacji trzeba podac ip drugiego usera

3. po udanym polaczeniu, jeden uzytkownik generuje session key, szyfruje go kluczem publicznym drugiego usera i wysyla go do niego

4. drugi user odszyfrowuje klucz sesyjny swoim kluczem prywatnym klucz sesyjny bedzie sluzyl do szyfrowania danych?

GUI:
1. ma pozwalac na pisanie wiadomosci i wysylanie plikow (.txt .png .pdf .avi) z dowolnym rozmiarem (od malych nawet do 500MB)
2. wybor sposobu kodowanie (ECB, CBC)
3. pasek postepu wysylanie wiadomosci/pliku
4. wiadomosc potwierdzajaca od odbiorcy


Szyfrowanie:
1. nalezy uzyc algorytmu AES

2. ECB, CBC

3. generator liczb pseudolosowych do wygenerowania klucza sesyjnego

4. klucz publiczny i prywatny musza byc trzymane osobno

5. klucze prywatne i publiczne maja byc zaszyfrowane przy uzyciu CBC

6. klucz do rozszyfrowania kluczy prywatnego i publicznego to hash (SHA) hasla 

