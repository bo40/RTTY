import numpy as np

START_BIT = 0
STOP_BIT = 1

WAIT_START = 0
READ_BYTE = 1
EXPECT_STOP = 2

def filter_window_vals(window_vals):
  prev_bit = 0
  start_time = 0

  for (mk, sp, time) in window_vals:
    if mk > sp:
      bit = 1
    else:
      bit = 0
    if (bit != prev_bit):
      yield (prev_bit, time - start_time)
      start_time = time
      prev_bit = bit
  yield (prev_bit, time - start_time + 1)

def extract_bits(bits_with_length, baud = 45.45, smp = 8000):
  duration = smp / baud

  duration30per = duration * 0.3

  total_length = 0

  for (bit, length) in bits_with_length:
    total_length += length
    while total_length > duration30per:
      if total_length > duration:
        total_length -= duration
        yield (bit, 1)
      else:
        yield (bit, total_length / duration)
        total_length = 0

def translate_bitcodes(bits):
  # ５ビットをまとめてbitcodeにする
  prev_bit = 0

  state = WAIT_START
  buffer = []

  for bit, _ in bits:
    if state == WAIT_START:
      if bit == START_BIT:
        state = READ_BYTE
        buffer.append(bit)
    elif state == READ_BYTE:
      buffer.append(bit)
      if len(buffer) >= 6:
        state = EXPECT_STOP
    elif state == EXPECT_STOP:
      if bit == STOP_BIT:
        bit4 = buffer.pop()
        bit3 = buffer.pop()
        bit2 = buffer.pop()
        bit1 = buffer.pop()
        bit0 = buffer.pop()
        yield (f"{bit0}{bit1}{bit2}{bit3}{bit4}")
        buffer.clear()
        state = WAIT_START
      else:
        buffer.append(bit)

def window_vals_to_bitcodes(window_vals):

  bits_with_length = filter_window_vals(window_vals)

  bits = extract_bits(bits_with_length)

  bitcodes = translate_bitcodes(bits)

  return bitcodes