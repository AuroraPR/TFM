import sounddevice as sd
from scipy.io.wavfile import write
import sys

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

for x in range(20):
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(sys.argv[1]+'-'+str(x)+'.wav', fs, myrecording)  # Save as WAV file 