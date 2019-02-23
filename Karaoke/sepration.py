import pyaudio
import struct
import wave,math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

wf = wave.open( 'Rolling in the Deep.wav', 'rb')
# Read wave file properties
RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)
 
left = []
right = []
datawav = wf.readframes(LEN)
datause = np.fromstring(datawav, dtype = np.short)
datause.shape = -1,2
datause = datause.T
left = datause[0]
right = datause[1]

global c,d
N = 10*RATE #采样点数
start = 0 #开始采样位置
df = RATE/(N-1) #分辨率
freq = [df*n for n in range(0,N)]
fft1 = left[start:start+N]
c = np.fft.fft(fft1)
d = int(len(c)/2) #对称性，显示一半频谱
plt.figure(1)
plt.xlim(0,5000)
line, = plt.plot(freq[:d-1],abs(c[:d-1]),'r')
plt.show()



#plt.figure(1)
#left_fft = np.fft.fft(left)
#line, = plt.plot(abs(fftshift(left_fft)))
#line.set_Xdata(LEN)
#line.set_ydata(abs(left_fft))
#plt.show()
#plt.subplot(211)
#line, = plt.plot(left, color = 'red')
#plt.subplot(212)
#line, = plt.plot(right, color = 'blue')

new_left = left - right
new_right = left - right
new = new_left + new_right

fft2 = new[start:start+N]
c = np.fft.fft(fft2)
d = int(len(c)/2) #对称性，显示一半频谱
plt.figure(2)
plt.xlim(0,5000)
line, = plt.plot(freq[:d-1],abs(c[:d-1]),'r')
plt.show()



#[b,a] = signal.butter(8,[0.1,0.6],'pass')
#music = signal.lfilter(b,a,new)
#print(left)
#print(right)

wfn = wave.open('new.wav','w')
wfn.setnchannels(1)
wfn.setsampwidth(2)
wfn.setframerate(RATE)
wfn.writeframes(new)
#wfr.close()


wfm = wave.open('new.wav','rb')

output_wf = wave.open('accompany9.wav', 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(2)
output_wf.setnchannels(1)

#b,a = signal.ellip(30,0.1,50,0.03)
b1,a1 = signal.ellip(8, 0.2, 50, 500/RATE)
b2,a2 = signal.ellip(8, 0.2, 50, 2000/RATE, 'high')
#zi = signal.lfilter_zi(b,a)

BLOCKLEN = 1544196
num_blocks = LEN/BLOCKLEN
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Get first set of frame from wave file
binary_data = wfm.readframes(BLOCKLEN)

ORDER = 8   # filter is fourth order
states = np.zeros(ORDER)

#for n in range(num_blocks):
#    binary_data = wfm.readframes(BLOCKLEN)
#    input_block = struct.unpack('h' * BLOCKLEN, binary_data) 
#    output_block = signal.lfilter(b, a, input_block)
#    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)
    

while len(binary_data) >= BLOCKLEN:

    # convert binary data to numbers
    input_block = struct.unpack('h' * BLOCKLEN, binary_data) 

    # filter
    output_block, states = signal.lfilter(b1, a1, input_block, zi = states)

    output_block, states = signal.lfilter(b2, a2, output_block, zi = states)
    
    output_block = 50*output_block

    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)     

    # convert to integer
    output_block = output_block.astype(int)     

    # Convert output value to binary data
    output_data = struct.pack('h' * BLOCKLEN, *output_block)                   

    # Write binary data to output wave file
    output_wf.writeframes(output_data)

    # Get next frame from wave file
    binary_data = wfm.readframes(BLOCKLEN)

print('* Finished')

wfa = wave.open('accompany9.wav', 'rb')
len1 = wfa.getnframes()      # wave file
datawav1= wfa.readframes(len1)
datause1 = np.fromstring(datawav1, dtype = np.short)
datause1 = datause1.T

print(len1)

N = 10*RATE #采样点数
start = 10*RATE #开始采样位置
fft3 = datause1[start:start+N]
c = np.fft.fft(fft3)
d = int(len(c)/2) #对称性，显示一半频谱
plt.figure(3)
plt.xlim(0,5000)
line, = plt.plot(freq[:d-1],abs(c[:d-1]),'r')
plt.show()


# Close wavefiles

wfm.close()
output_wf.close()
















#plt.subplot(223)
#left_fft = np.fft.fft(left)
#line, = plt.plot(left_fft, color = 'red')
#plt.subplot(224)
#right_fft = np.fft.fft(right)
#line, = plt.plot(right_fft, color = 'blue')
#plt.show()

#wfl = wave.open('1_left.wav','w')
#wfl.setnchannels(1)
#wfl.setsampwidth(2)
#wfl.setframerate(RATE)
#wfl.writeframes(np.array(left))
#wfl.close()

#wfr = wave.open('1_right.wav','w')
#wfr.setnchannels(1)
#wfr.setsampwidth(2)
#wfr.setframerate(RATE)
#wfr.writeframes(np.array(right))
#wfr.close()


