import wave
import numpy as np
smp= 8000          # Sampling Rate
wind= 32           # windows size Integer

def read_wave_rtty(filename, FQm = 914.0, FQs = 1086.0):
  waveFile = wave.open(filename, 'r')
  mq=[];mi=[];sq=[];si=[]
  c = np.pi * 2.0 / smp
  for j in range(waveFile.getnframes()):
    buf = waveFile.readframes(1)
    mq.append((buf[0]-128)*np.sin(c * FQm*j))
    mi.append((buf[0]-128)*np.cos(c * FQm*j))
    sq.append((buf[0]-128)*np.sin(c * FQs*j))
    si.append((buf[0]-128)*np.cos(c * FQs*j))
    mk = sum(mq)**2 + sum(mi)**2
    sp = sum(sq)**2 + sum(si)**2
    yield (mk, sp, j)

    if j>wind:
          mq.pop(0);mi.pop(0);sq.pop(0);si.pop(0)
  waveFile.close()
