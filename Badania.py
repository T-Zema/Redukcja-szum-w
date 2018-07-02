
import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
import scipy.io.wavfile as wavfile
import wave
from scipy.fftpack import fft
# Prawdopodobnie ze względu na tak wysoki poziom szumu, zredukowana muzyka ma trochę inne brzmienie

samplerate, data = wavfile.read('muzyka.wav')
samplerate2, data2 = wavfile.read('szummuza21.wav')
samplerate3, data3 = wavfile.read('bezszumu.wav')
samplerate4, noise = wavfile.read('szum.wav')
assert samplerate == samplerate2
times = np.arange(len(data))/float(samplerate)

track = wave.open('muzyka.wav','r')
para = track.getparams()
print ("Parametry dla muzki")
print (para)

track2 = wave.open('szummuza21.wav','r')
para2 = track2.getparams()
print ("Parametry dla muzki z szumem")
print (para2)

track3 = wave.open('bezszumu.wav','r')
para3 = track3.getparams()
print ("Parametry dla muzyki po filtracji")
print (para3)

track4 = wave.open('szum.wav','r')
para4 = track4.getparams()
print ("Parametry dla szumu")
print (para4)


dopasowanie = slice(0,len(data))
s_data2 = data2[dopasowanie]


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

if "yes" in dec or "Y" in dec or "absolutnie tak" in dec:
    plt.figure(figsize=(12, 6))

    plt.subplot(411)
    plt.title("Frequency spectrums of music samples")

    spectdata = fft((data2[:, 0] / 2) + (data2[:, 1] / 2))
    x = len(spectdata)
    freqz = np.fft.fftfreq(len(spectdata), 1 / samplerate)
    plt.plot(freqz, np.abs(spectdata), label="Music")
    plt.xlim(0, 5000)
    plt.legend()

    plt.subplot(412)
    spectdata2 = fft((data2[:, 0] / 2) + (data2[:, 1] / 2))
    x2 = len(spectdata2)
    freqz = np.fft.fftfreq(len(data2), 1 / samplerate2)
    plt.plot(freqz, abs(spectdata2), 'g', label="Noise plus Music")
    plt.xlim(0, 5000)
    plt.legend()

    print("Tutaj to trochę potrwa, proszę czekać...")
    print("na tą chwilę nie mam pojęcia dlaczego fft dla samego szumu tak długo się robi")

    plt.subplot(413)
    mniej = slice(0, len(data))
    s_noise = noise[mniej]
    print(len(s_noise))
    print(len(noise))
    spectdata3 = fft(((s_noise[:,0]/2) + (s_noise[:,1]/2)))
    freqz = np.fft.fftfreq((len(s_noise)), 1 / samplerate4)
    plt.plot(freqz, abs(spectdata3), 'm', label="Noise applied to music")
    plt.xlim(0, 5000)
    plt.legend()

    plt.subplot(414)
    spectdata4 = fft(data3)
    x4 = len(spectdata4)
    freqz = np.fft.fftfreq((len(data3)), 1 / samplerate3)
    plt.plot(freqz, abs(spectdata4[:(x4)]), 'k', label="music after filtration")
    plt.xlim(0, 5000)
    plt.legend()
    plt.tight_layout(0, 0.1, 0)
    plt.show()

#może jednak dokonać decymacji żeby wykresy sprawniej działały
wavfile.write("bezszumu.wav", samplerate, y.astype('int16'))