# Copyrights (C) 2021 ny-a.
# This program is written by ny-a (https://github.com/ny-a), and modified some.

TABLE = {
    '1010101011': 'NUL',
    '1011011011': 'SOH',
    '1011101101': 'STX',
    '1101110111': 'ETX',
    '1011101011': 'EOT',
    '1101011111': 'ENQ',
    '1011101111': 'ACK',
    '1011111101': 'BEL',
    '1011111111': 'BS',
    '11101111': 'HT',
    '11101': 'LF',
    '1101101111': 'VT',
    '1011011101': 'FF',
    '11111': 'CR',
    '1101110101': 'SO',
    '1110101011': 'SI',
    '1011110111': 'DLE',
    '1011110101': 'DC1',
    '1110101101': 'DC2',
    '1110101111': 'DC3',
    '1101011011': 'DC4',
    '1101101011': 'NAK',
    '1101101101': 'SYN',
    '1101010111': 'ETB',
    '1101111011': 'CAN',
    '1101111101': 'EM',
    '1110110111': 'SUB',
    '1101010101': 'ESC',
    '1101011101': 'FS',
    '1110111011': 'GS',
    '1011111011': 'RS',
    '1101111111': 'US',
    '1': ' ',
    '111111111': '!',
    '101011111': '"',
    '111110101': '#',
    '111011011': '$',
    '1011010101': '%',
    '1010111011': '&',
    '101111111': "'",
    '11111011': '(',
    '11110111': ')',
    '101101111': '*',
    '111011111': '+',
    '1110101': ',',
    '110101': '-',
    '1010111': '.',
    '110101111': '/',
    '10110111': '0',
    '10111101': '1',
    '11101101': '2',
    '11111111': '3',
    '101110111': '4',
    '101011011': '5',
    '101101011': '6',
    '110101101': '7',
    '110101011': '8',
    '110110111': '9',
    '11110101': ':',
    '110111101': ';',
    '111101101': '<',
    '1010101': '=',
    '111010111': '>',
    '1010101111': '?',
    '1010111101': '@',
    '1111101': 'A',
    '11101011': 'B',
    '10101101': 'C',
    '10110101': 'D',
    '1110111': 'E',
    '11011011': 'F',
    '11111101': 'G',
    '101010101': 'H',
    '1111111': 'I',
    '111111101': 'J',
    '101111101': 'K',
    '11010111': 'L',
    '10111011': 'M',
    '11011101': 'N',
    '10101011': 'O',
    '11010101': 'P',
    '111011101': 'Q',
    '10101111': 'R',
    '1101111': 'S',
    '1101101': 'T',
    '101010111': 'U',
    '110110101': 'V',
    '101011101': 'W',
    '101110101': 'X',
    '101111011': 'Y',
    '1010101101': 'Z',
    '111110111': '[',
    '111101111': '\\',
    '111111011': ']',
    '1010111111': '^',
    '101101101': '_',
    '1011011111': '`',
    '1011': 'a',
    '1011111': 'b',
    '101111': 'c',
    '101101': 'd',
    '11': 'e',
    '111101': 'f',
    '1011011': 'g',
    '101011': 'h',
    '1101': 'i',
    '111101011': 'j',
    '10111111': 'k',
    '11011': 'l',
    '111011': 'm',
    '1111': 'n',
    '111': 'o',
    '111111': 'p',
    '110111111': 'q',
    '10101': 'r',
    '10111': 's',
    '101': 't',
    '110111': 'u',
    '1111011': 'v',
    '1101011': 'w',
    '11011111': 'x',
    '1011101': 'y',
    '111010101': 'z',
    '1010110111': '{',
    '110111011': '|',
    '1010110101': '}',
    '1011010111': '~',
    '1110110101': 'DEL',
}


def parse_varicode(bit_chunks):
    for chunk in bit_chunks:
        char = TABLE[chunk]
        yield (char, chunk)