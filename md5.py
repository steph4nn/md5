import struct
import math
import hashlib
import time

def md5(input):
    # --------- PRÉ-PROCESSAMENTO DO INPUT --------- #
    # Converte para bytes
    if isinstance(input, str):
        input = input.encode('utf-8')

    # Armazena o tamanho inicial do input em 64 bits
    original_length_bits = (len(input) * 8) & 0xFFFFFFFFFFFFFFFF

    # Adiciona um bit 1
    input += b'\x80'

    # Preenche o input com bytes 0x00 até chegar a 448 bits
    while (len(input) * 8) % 512 != 448:
        input += b'\x00'

    # Adiciona os 64 bits do tamanho original no final
    input += struct.pack('<Q', original_length_bits)

    # --------- -------------------------- --------- #

    # Valores iniciais das variáveis do MD5
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    # Constantes senoidais (K)
    K = [int(abs(math.sin(i + 1)) * (2**32)) & 0xFFFFFFFF for i in range(64)]

    # Shifts circulares para cada rodada
    shifts = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    # Processa em blocos de 64 bytes
    for bloco_index in range(0, len(input), 64):
        bloco = input[bloco_index:bloco_index + 64]

        # Converte 64 bytes em 16 inteiros de 32 bits
        X = struct.unpack('<16I', bloco)

        # Inicializa as variaveis temp
        AA, BB, CC, DD = A, B, C, D

        # 64 rodadas
        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | ~D)
                g = (7 * i) % 16

            # Cálculo principal da rodada
            F = (F + A + K[i] + X[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B

            # Cálculo de combinação de todos os valores
            B = (B + ((F << shifts[i]) | (F >> (32 - shifts[i]))) & 0xFFFFFFFF) & 0xFFFFFFFF

        # Adiciona os resultados dessa rodada aos valores iniciais
        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF

    # Retorna o hash final no formato hexadecimal
    return ''.join(f'{x:02x}' for x in struct.pack('<4I', A, B, C, D))


# Testes para atender aos objetivos
if __name__ == "__main__":
    # 1. Validação com hashlib
    def validar_md5(input):
        return hashlib.md5(input.encode('utf-8')).hexdigest()

    test_input = "hello world!"

    start = time.time()
    result_custom = md5(test_input)
    custom_time = time.time() - start
    print(f"Custom MD5 do '{test_input}': {result_custom}")
    print(f"Custom MD5: {custom_time:.5f} sec")

    start = time.time()
    result_lib = validar_md5(test_input)
    lib_time = time.time() - start
    print(f"\nHashlib MD5 do '{test_input}': {result_lib}")
    print(f"Hashlib MD5: {lib_time:.5f} sec")

    print(f"\nHashes são iguais: {result_custom == result_lib}")
    print(f"\nDiferença de tempo para '{test_input}': {abs(custom_time - lib_time):.5f} sec")

    # 2. Teste de imutabilidade
    input1 = "hello world!"
    input2 = "Hello world!"
    print(f"\nTeste de imutabilidade:")
    print(f"Hash de '{input1}': {md5(input1)}")
    print(f"Hash de '{input2}': {md5(input2)}")
    print(f"Hashes são iguais: {md5(input1) == md5(input2)}")

    # 3. Avaliação de desempenho
    large_input = "a" * 10**6 # 1 milhão de caracteres "a"
    print(f"\nTeste de desempenho:")

    # Tempo para a implementação customizada
    start = time.time()
    result_custom = md5(large_input)
    custom_time = time.time() - start
    print(f"Custom MD5 do Large Input: {result_custom}")
    print(f"Custom MD5: {custom_time:.5f} sec")

    # Tempo para a implementação hashlib
    start = time.time()
    result_lib = validar_md5(large_input)
    lib_time = time.time() - start
    print(f"\nHashlib MD5 do Large Input: {result_lib}")
    print(f"Hashlib MD5: {lib_time:.5f} sec")

    print(f"\nDiferença de tempo: {abs(custom_time - lib_time):.5f} sec")


