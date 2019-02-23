def record(self):
	import numpy as np
	import tkinter as Tk
	import matplotlib
	matplotlib.use('TkAgg')
	import matplotlib.pyplot as plt
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
	from matplotlib.figure import Figure
	import pyaudio
	import struct
	import wave
	import math
	import pygame

	# root = Tk.Tk()  

    
	wf2 = wave.open('accompany.wav','rb')

	#def plot():
	WIDTH     = 2         # bytes per sample
	CHANNELS  = 1         
	RATE      = 44100     # Sampling rate (samples/second)
	BLOCKSIZE = 4000      # length of block (samples)
	DURATION  = 10        # Duration (seconds)
	#signal_len = 1544196
	NumBlocks = int( DURATION *RATE / BLOCKSIZE )
	MAXVALUE = 2**15 -1
    
	wfo = wave.open('record.wav','w')
	wfo.setnchannels(CHANNELS)
	wfo.setsampwidth(WIDTH)
	wfo.setframerate(RATE)
	

	p = pyaudio.PyAudio()
	PA_FORMAT = p.get_format_from_width(WIDTH)

	stream = p.open(
	    format = PA_FORMAT,
	    channels = 1,
	    rate = RATE,
	    input = True,
	    output = False)



	for i in range(0, NumBlocks):
	    input_string = stream.read(BLOCKSIZE)
	    #input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)
	    # origin_string = wf2.readframes(BLOCKSIZE)
	    # stream.write(origin_string)
	    #origin_tuple = struct.unpack('h'*BLOCKSIZE, input_string)
	    #X1 = np.fft.fft(input_tuple)
	    #line1.set_ydata(20*np.log10(abs(X1)))
	    #output_block = clip16(input_tuple)
	    #output_block = np.clip(input_tuple, -MAXVALUE, MAXVALUE)
	    #output_block = output_block.astype(int)
	    #output_data = struct.pack('h'*BLOCKSIZE,*output_block)
	    wfo.writeframes(input_string)
	    #X2 = np.fft.fft(origin_tuple)
	    #line2.set_ydata(20*np.log10(abs(X2)))
	    #plt.pause(0.001)
	    #stream.write(origin_string)
	    #canvas.draw()

		#plt.close()
	stream.stop_stream()
	p.terminate()
	print('*Finished')

    #def lyrics():

	# fig=plt.figure(figsize=(4,4))
	# canvas=FigureCanvasTkAgg(fig,master=root)
	# canvas.get_tk_widget().grid(row=0,column=1)
	# canvas.draw()
	# plotbutton=Tk.Button(master=root, text="plot", command= plot)
	# plotbutton.grid(row=0,column=0)
	# #changebutton = Tk.Button(master = root, text = "change", command = tone_change)
	# #changebutton.grid(row = 1, column = 0)
	# root.mainloop()

if __name__ == "__main__":
    record_Grade()
