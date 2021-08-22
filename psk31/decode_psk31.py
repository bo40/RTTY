import sys
from read_wave import read_wave_psk31
from qpsk_decoder import qpsk_vals_to_bitcodes
from varicode import parse_varicode

if __name__ == '__main__':
  print("Start decoding rtty!\n")

  qpsk_vals = read_wave_psk31(sys.argv[1])

  bitcodes = qpsk_vals_to_bitcodes(qpsk_vals)

  varicode_string = parse_varicode(bitcodes)

  for c, _ in varicode_string:
    print(c, end='')

  print("\n\nFinish decoding rtty!")