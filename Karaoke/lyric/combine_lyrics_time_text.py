f1 = open('text.txt','r')
linenum = len(f1.readlines())
f1.close()
f1 = open('text.txt','r')
f2 = open('time.txt','r')
for i in range(linenum):
  try:
    lrc = f1.readline()
    time = f2.readline()
    line = time.strip()+' '+lrc
    with open('final_lyrics.txt','a+') as f:
      f.write(line)
  except:
    break
f1.close()
f2.close()
f.close()