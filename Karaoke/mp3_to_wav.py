from pydub import AudioSegment
 
sound = AudioSegment.from_mp3("a.mp3")
sound.export("a.wav", format="wav")