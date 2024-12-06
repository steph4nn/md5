import struct
import math


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

        # Inicializa valores temporários
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
            B = (B + ((F << shifts[i]) | (F >> (32 - shifts[i]))) & 0xFFFFFFFF) & 0xFFFFFFFF

        # Adiciona os resultados dessa rodada aos valores iniciais
        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF

    # Retorna o hash final no formato hexadecimal
    return ''.join(f'{x:02x}' for x in struct.pack('<4I', A, B, C, D))


if __name__ == "__main__":
    test_input = "hello world!"
    result = md5(test_input)
    print(f"MD5('{test_input}') = {result}")
