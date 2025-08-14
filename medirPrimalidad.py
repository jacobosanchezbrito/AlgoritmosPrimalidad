import random
import math
import time

# ----------------------------
# 1. Miller-Rabin
# ----------------------------
def miller_rabin(n, k=5):
    if n < 2:
        return False
    # Casos pequeños
    for p in [2, 3]:
        if n % p == 0:
            return n == p
    # Factoriza n-1 como 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# ----------------------------
# 2. Fermat
# ----------------------------
def fermat(n, k=5):
    if n <= 1:
        return False
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n-1, n) != 1:
            return False
    return True

# ----------------------------
# 3. Solovay-Strassen
# ----------------------------
def jacobi_symbol(a, n):
    if a == 0:
        return 0
    result = 1
    if a < 0:
        a = -a
        if n % 4 == 3:
            result = -result
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0

def solovay_strassen(n, k=5):
    if n < 2:
        return False
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = jacobi_symbol(a, n)
        if x == 0 or pow(a, (n - 1) // 2, n) != (x % n):
            return False
    return True

# ----------------------------
# 4. Baillie-PSW
# ----------------------------
def is_square(n):
    r = int(math.isqrt(n))
    return r * r == n

def lucas_test(n):
    if is_square(n):
        return False
    # Lucas parameters
    D = 5
    while True:
        if math.gcd(D, n) > 1:
            return n == math.gcd(D, n)
        if pow(D, (n - 1) // 2, n) == n - 1:
            break
        D = -D + 2 if D > 0 else -D + 2
    P = 1
    Q = (1 - D) // 4
    k = n + 1
    U, V = 0, 2
    for bit in bin(k)[2:]:
        U, V = (U * V) % n, (V * V - 2) % n
        if bit == "1":
            U, V = (P * U + V) % n, (D * U + P * V) % n
    return U == 0

def baillie_psw(n):
    if n < 2:
        return False
    if not miller_rabin(n, 1):
        return False
    return lucas_test(n)

# ----------------------------
# 5. AKS (versión simplificada, no optimizada)
# ----------------------------
def is_perfect_power(n):
    for b in range(2, int(math.log2(n)) + 2):
        a = round(n ** (1 / b))
        if a ** b == n:
            return True
    return False

def aks(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or is_perfect_power(n):
        return False
    r = 2
    while r < n:
        if math.gcd(n, r) > 1:
            return n == r
        if pow(n, r, r) != n % r:
            break
        r += 1
    max_a = int(math.sqrt(r) * math.log2(n))
    for a in range(1, max_a + 1):
        if pow(a, n, n) != a % n:
            return False
    return True

# ----------------------------
# 6. Wilson
# ----------------------------
def wilson(n):
    if n < 2:
        return False
    return math.factorial(n - 1) % n == n - 1

# ----------------------------
# 7. Lucas-Lehmer (para números de Mersenne)
# ----------------------------
def lucas_lehmer(p):
    if p == 2:
        return True
    M = 2**p - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % M
    return s == 0

# ----------------------------
# 8. Lehmann
# ----------------------------
def lehmann(n, k=5):
    if n < 2:
        return False
    for _ in range(k):
        a = random.randint(1, n - 1)
        r = pow(a, (n - 1) // 2, n)
        if r != 1 and r != n - 1:
            return False
    return True


# DeterminarNumeroPrimo1
def determinar_numero_primo1(numero):
    resultado = 0
    for i in range(2, numero):
        if numero % i == 0:
            resultado = 1
    return resultado == 0


# DeterminarNumeroPrimo2
def determinar_numero_primo2(numero):
    centi = True
    i = 2
    while i <= numero // 2 and centi:
        if numero % i == 0:
            centi = False
        i += 1
    return centi


# DeterminarNumeroPrimo3
def determinar_numero_primo3(numero):
    for i in range(2, numero // 2 + 1):
        if numero % i == 0:
            break
    if numero // 2 < i:
        return True
    else:
        return False


# DeterminarNumeroPrimo4
import math
def determinar_numero_primo4(numero):
    for i in range(2, int(math.sqrt(numero)) + 1):
        if numero % i == 0:
            return False
    return True


# DeterminarNumeroPrimo5
def determinar_numero_primo5(numero):
    if numero < 2:
        return False
    i = 2
    while i * i <= numero:
        if numero % i == 0:
            return False
        i += 1
    return True



# ----------------------------
# Función para medir tiempos
# ----------------------------
def medir_tiempo(algoritmo, numero, repeticiones=1):
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter_ns()
        algoritmo(numero)
        fin = time.perf_counter_ns()
        tiempos.append(fin - inicio)
    promedio = sum(tiempos) / len(tiempos)
    return promedio

if __name__ == "__main__":
    #numero_prueba = 999_999_999
    #numero_prueba = 987_654_321
    #numero_prueba = 900_500_345
    numero_prueba = 979_797_980
    #numero_prueba = 198_765_432
    algoritmos = [
        #("Miller-Rabin", miller_rabin),
        #("Fermat", fermat),
        #("Solovay-Strassen", solovay_strassen),
        ("Baillie-PSW", baillie_psw),
        #("AKS", aks),
        #("Wilson", wilson),
        #("Lucas-Lehmer", lambda n: lucas_lehmer(23)), 
        #("Lehmann", lehmann),
        #("DP1", determinar_numero_primo1),
        #("DP2", determinar_numero_primo2),
        #("DP3", determinar_numero_primo3),
        #("DP4", determinar_numero_primo4),
        #("DP5", determinar_numero_primo5)
    ]
    
    for nombre, func in algoritmos:
        promedio = medir_tiempo(func, numero_prueba)
        print(f"{nombre}: {promedio:.2f} ns en promedio")

