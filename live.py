try:
    import pyaudio
    import numpy as np
    import pylab
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    import time
    import sys
    import seaborn as sns
    import padasip as pa
    from scipy import signal
    from scipy.io import wavfile
    import wave
    from scipy.fftpack import fft
except:
    print ("You dont have nescessary libraries")


# zabawa z filtrowaniem

i=0
f,ax = plt.subplots(4)

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,16800)
ax[0].set_ylim(-50000,50000)
ax[0].set_title("Sygnał z mikrofonu")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,20000)
ax[1].set_ylim(0,20000000)
ax[1].set_title("Fast Fourier Transform")
# Plot 2
li3, = ax[2].plot(x, y)
ax[2].set_xlim(0,30000)
ax[2].set_ylim(0,10000000000000)
ax[2].set_title("filtracja")

# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()

FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
RATE = 44100
CHUNK = 16384 # 8192 1024bytes of data read from a buffer
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True)#,
                    #frames_per_buffer=CHUNK)

global keep_going
keep_going = True

#def const():

    # get sound samples and reshape it to length of CHUNK and convert to float
    # samplerate, data = wavfile.read('bezszumu.wav')

#const()

def plot_data(in_data):


    process_data.audio_data = np.fromstring(in_data, np.int16)

    fft1 = fft(process_data.audio_data)
    freqz = np.fft.fftfreq(len(fft1), 1 / RATE)


    li.set_xdata(np.arange(len(process_data.audio_data)))
    li.set_ydata(process_data.audio_data)
    li2.set_xdata(np.arange(len(freqz))*10.)
    li2.set_ydata(np.abs(fft1))




    # Show the updated plot, but without blocking
    plt.pause(0.01)
    if keep_going:
        return True
    else:
        return False

def process_data():
    # s =[]
    process_data.audio_data = np.fromstring(stream.read(CHUNK), np.int16)
    # print ("Length of one chunk",len(process_data.audio_data))
    # print("Time of one chunk",len(process_data.audio_data) / RATE)
    # for i in range(0,5):
    #    s.extend(process_data.audio_data)
    # print (len(s))
    # print("Time of 5 chunks", len(s) / RATE)

def czunkow5():
    czunkow5.s = []
    for i in range(0,5):
        czunkow5.s.extend(process_data.audio_data)

# Open the connection and start streaming the data
stream.start_stream()
print ("\n+---------------------------------+")
print ("| Press Ctrl+C to Break Recording |")
print ("+---------------------------------+\n")

# Loop so program doesn't end while the stream callback's
# itself for new data
while keep_going:
    try:
        #process_data()
        plot_data(stream.read(CHUNK))

    except KeyboardInterrupt:
        keep_going=False
    except:
        pass

# Close up shop (currently not used because KeyboardInterrupt
# is the only way to close)
stream.stop_stream()
stream.close()

audio.terminate()