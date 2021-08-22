import enum
import numpy as np

smp = 8000 # Sampling rate
symbol_rate = 31.25 # Symbol rate
symbol_interval = int(smp / symbol_rate) # Symbol interval

class PhaseShift(enum.Enum):
  ZERO = '0'
  PLUS = '+90'
  MINUS = '-90'
  INV = '+180'

  def __str__(self):
    return self.value

def calc_shift(prev_q, prev_i, next_q, next_i):
  if prev_q == 0 and prev_i == 0:
    if next_q == 0 and next_i == 0: return PhaseShift.ZERO
    elif next_q == 0 and next_i == 1: return PhaseShift.PLUS
    elif next_q == 1 and next_i == 0: return PhaseShift.MINUS
    elif next_q == 1 and next_i == 1: return PhaseShift.INV
  elif prev_q == 0 and prev_i == 1:
    if next_q == 0 and next_i == 0: return PhaseShift.MINUS
    elif next_q == 0 and next_i == 1: return PhaseShift.ZERO
    elif next_q == 1 and next_i == 0: return PhaseShift.INV
    elif next_q == 1 and next_i == 1: return PhaseShift.PLUS
  elif prev_q == 1 and prev_i == 0:
    if next_q == 0 and next_i == 0: return PhaseShift.PLUS
    elif next_q == 0 and next_i == 1: return PhaseShift.INV
    elif next_q == 1 and next_i == 0: return PhaseShift.ZERO
    elif next_q == 1 and next_i == 1: return PhaseShift.MINUS
  elif prev_q == 1 and prev_i == 1:
    if next_q == 0 and next_i == 0: return PhaseShift.INV
    elif next_q == 0 and next_i == 1: return PhaseShift.MINUS
    elif next_q == 1 and next_i == 0: return PhaseShift.PLUS
    elif next_q == 1 and next_i == 1: return PhaseShift.ZERO
  return -1

CONVOLUTION_TABLE = {
  '00000': PhaseShift.INV, '00001': PhaseShift.PLUS, '00010': PhaseShift.MINUS, '00011': PhaseShift.ZERO, '00100': PhaseShift.MINUS, '00101': PhaseShift.ZERO, '00110': PhaseShift.INV, '00111': PhaseShift.PLUS,
  '01000': PhaseShift.ZERO, '01001': PhaseShift.MINUS, '01010': PhaseShift.PLUS, '01011': PhaseShift.INV, '01100': PhaseShift.PLUS, '01101': PhaseShift.INV, '01110': PhaseShift.ZERO, '01111': PhaseShift.MINUS,
  '10000': PhaseShift.PLUS, '10001': PhaseShift.INV, '10010': PhaseShift.ZERO, '10011': PhaseShift.MINUS, '10100': PhaseShift.ZERO, '10101': PhaseShift.MINUS, '10110': PhaseShift.PLUS, '10111': PhaseShift.INV,
  '11000': PhaseShift.MINUS, '11001': PhaseShift.ZERO, '11010': PhaseShift.INV, '11011': PhaseShift.PLUS, '11100': PhaseShift.INV, '11101': PhaseShift.PLUS, '11110': PhaseShift.MINUS, '11111': PhaseShift.ZERO
}

def find_symbol_interval_offset(vals):
  current_q = 0
  current_i = 0
  successive_length = 0
  offset = 0

  for index, (q, i) in enumerate(vals):
    if q == current_q and i == current_i:
      successive_length += 1
    else:
      current_q = q
      current_i = i
      successive_length = 1
      offset = index
    if successive_length > (symbol_interval * 0.95):
      return offset % symbol_interval
  return -1

def estimate_quadriphase_points(vals, ofs):
  total_length = 0
  buf_q = []; buf_i = []
  for index, (q, i) in enumerate(vals):
    if index < ofs:
      continue
    if (index - ofs) % symbol_interval == 0:
      estimate_q = sum(buf_q) / symbol_interval
      estimate_i = sum(buf_i) / symbol_interval
      yield(int(estimate_q >= 0.5), int(estimate_i >= 0.5))
      buf_q.clear()
      buf_i.clear()
      # # for DEBUG
      # if 0.3 < estimate_q and estimate_q < 0.7:
      #   if 0.3 < estimate_i and estimate_i < 0.7:
      #     print(f"{estimate_q}, {estimate_i},{index}")
    total_length = index
    buf_q.append(q)
    buf_i.append(i)

def quadriphase_to_phase_shifts(points):
  prev_q = 0
  prev_i = 0
  for index, (q, i) in enumerate(points):
    if index == 0:
      prev_q = q
      prev_i = i
    else:
      yield(calc_shift(prev_q, prev_i, q, i))
      prev_q = q
      prev_i = i

def convolution_encode(state, bit):
  next_state = state[1:] + str(bit)
  return (next_state, CONVOLUTION_TABLE[next_state])


def naive_decode(phase_shifts):
  state = '00000'
  errors_buf = []
  varicode_bit = 0

  for phase_shift in phase_shifts:

    (next_state0, phase_shift0) = convolution_encode(state, 0)
    (next_state1, phase_shift1) = convolution_encode(state, 1)
    if phase_shift0 == phase_shift:
      state = next_state0
      varicode_bit = 0
    elif phase_shift1 == phase_shift:
      state = next_state1
      varicode_bit = 1
    else:
      errors_buf.append(phase_shift)
      if len(errors_buf) > 5:
        state = '00000'
        errors_buf = []
      continue

    yield varicode_bit


def viterbi_decode(phase_shifts):
  state = '00000'
  return 0

def bits_to_bitcode(bits):
  buf = ''
  prev_bit = 0

  for current_bit in bits:
    if prev_bit == 0 and current_bit == 0:
      if buf != '':
        yield buf.rstrip('0')
        buf = ''
    else:
      buf = buf + str(current_bit)
    prev_bit = current_bit

  if buf != '':
    yield buf.rstrip('0')


def qpsk_vals_to_bitcodes(vals):
  ofs = find_symbol_interval_offset(vals)

  # print(f"symbol interval offset = {ofs}")
  if ofs < 0:
    print("Can't find symbol interval offset!")
    return 0

  quadriphase_points = estimate_quadriphase_points(vals, ofs)

  phase_shifts = quadriphase_to_phase_shifts(quadriphase_points)

  bits = naive_decode(phase_shifts)

  bitcodes = bits_to_bitcode(bits)

  return bitcodes