import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
import scipy.io.wavfile as wavfile
import wave
from scipy.fftpack import fft
samplerate, data = wavfile.read('muzyka.wav')
samplerate2, data2 = wavfile.read('szummuza21.wav')
assert samplerate == samplerate2

times = np.arange(len(data))/float(samplerate)

track = wave.open('muzyka.wav','r')
para = track.getparams()
print (para)

track2 = wave.open('szummuza21.wav','r')
para2 = track.getparams()
print (para2)

# w tym miejscu bez zakłóceń

dopasowanie=slice(0,len(data))
s_data2 = data2[dopasowanie]
# tutaj też ok
wavfile.write('dobrze.wav',samplerate,s_data2.astype('int16'))


plt.figure(figsize=(12, 6))
plt.subplot(211)
plt.title("Music before filtration")
plt.fill_between(times, data[:,0], data[:,1], color='k', label="music without noise")
plt.fill_between(times,s_data2[:,0],s_data2[:,1], label="music with noise")
plt.xlim(times[0], times[-1])
plt.grid()
plt.legend()
plt.xlabel('time')


d = ((data[:,0])/2+(data[:,1])/2)
u = ((s_data2[:,0])/2+(s_data2[:,1])/2)
# wavfile.write('rzeczywiscie.wav',samplerate,u.astype('int16'))

# filter
M = 1000
step = 0.1
y, e, w = adf.nlms(u, d, M, step)

dopasowanie2 = slice(0,len(y))
s_times = times[dopasowanie2]

plt.subplot(212)
plt.title("Music after filtration")
plt.fill_between(s_times,y,color='m',label="music after filtration")
plt.xlim(s_times[0], s_times[-1])
plt.grid()
plt.legend()
plt.xlabel('time')
plt.tight_layout(0,0.1,0)
plt.show()
dec = input('Do you want to see frequency spectum of signals? [Y/N]')

# if "yes" in dec or "Y" in dec or "absolutnie tak" in dec:
#     print ("no elo")
#     spectdata = fft(data)
#     x = len(spectdata)//2
#     N = 198109
#     T = 1.0 / 800.0
#     plt.figure(figsize=(12, 6))
#     plt.subplot(411)
#     freq = np.fft.fftfreq(data.size)
#     xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
#     plt.plot(xf, 2.0 / N * np.abs(spectdata[0:N // 2]))
#     #plt.plot(freq,abs(spectdata[:(x-1)]),'r')
#
#     plt.subplot(412)
#     spectdata2 = fft(data2)
#     x2 = len(spectdata2) // 2
#     plt.plot(abs(spectdata2[:(x2 - 1)]), 'g')
#
#     plt.subplot(413)
#     samplerate, noise = wavfile.read('szum.wav')
#     spectdata3 = fft(noise)
#     x3 = len(noise) // 2
#     plt.plot(abs(spectdata3[:(x3 - 1)]), 'm')
#
#     plt.subplot(414)
#     spectdata4 = fft(y)
#     x4 = len(spectdata4) // 2
#     plt.plot(abs(spectdata4[:(x4 - 1)]), 'k')
#     plt.show()
# może jednak dokonać decymacji żeby wykresy sprawniej działały
wavfile.write("bezszumu.wav", samplerate, y.astype('int16'))