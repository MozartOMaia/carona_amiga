from typing import Dict


def bitsToInteger(bits: Dict):
    bits = bits.values()

    current_value = 1
    value = 0

    for bit in reversed(bits):
        if bit == 1:
            value += current_value

        current_value *= 2

    return value
