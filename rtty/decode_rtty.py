import sys
from read_wave import read_wave_rtty
from window_decoder import window_vals_to_bitcodes
from ita2 import parse_ita2

if __name__ == '__main__':
  print("Start decoding rtty!")

  window_vals = read_wave_rtty(sys.argv[1])

  bitcodes = window_vals_to_bitcodes(window_vals)

  ita2_string = parse_ita2(bitcodes)

  for c, _ in ita2_string:
    print(c, end='')

  print("\nFinish decoding rtty!")