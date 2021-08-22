import wave
import math
import numpy as np

smp= 8000           # Sampling Rate
wind= 40            # window

def read_wave_psk31(filename, FQ = 1000.0):
  waveFile = wave.open(filename, 'r')
  q=[];i=[]
  c = np.pi * 2.0 / smp
  for j in range(waveFile.getnframes()):
    buf = waveFile.readframes(1)
    q.append((buf[0]-128)*np.sin(c * FQ * j))
    i.append((buf[0]-128)*np.cos(c * FQ * j))
    yield (int(sum(q) > 0), int(sum(i) > 0))

    if j>wind:
      q.pop(0);i.pop(0)
  waveFile.close()