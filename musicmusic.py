from scipy.io.wavfile import read
import RPi.GPIO as GPIO
import random, os, fnmatch, pygame, sys, time

def clear():
    os.system('clear')
    
def main():
	
    #colours for terminal text
    COLOUR = '\033[0;{}m'.format(random.randint(31,37))
    CLEAR = '\033[0m'
    playing = False
    #printing playable songs inside the folder
    filelist = os.listdir(".")
    pattern = "*.wav"
    print("\033[0;35m" + "Songs currently in folder:" + CLEAR)
    for item in filelist:
        if fnmatch.fnmatch(item, pattern):
            print(item)
    #read amplitude and frequency of music file with defined frame skips
    file_name = raw_input("Enter song name: ")
    frame_rate, amplitude = read(file_name)
    frame_skip = frame_rate/1000.0
    try: 
        amplitude = amplitude[:,0] + amplitude[:,1]
    except:
        pass
    song_total = float(len(amplitude)/frame_rate) # song time in seconds
    clear()
    amplitude = amplitude[::int(frame_skip)]
    print("loading song...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(14, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    
    

    max_amplitude = max(amplitude)
    for i in range(len(amplitude)- 2):
            amplitude[i] = float(abs(amplitude[i]))/max_amplitude*50
            
    pygame.mixer.init(frame_rate)
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    clear()
    print(COLOUR + "playing " + file_name + CLEAR)
    print("song length: " + str(int(song_total)) + " seconds")
    time.sleep(0.275)
    now = time.time()

    for i in range(len(amplitude)):
        #*(0.1125/10) for 22k sample
        #0.1125 for 48k sample
            #enabling LEDs depending on the amplitude
        if amplitude[i] > 3:
            GPIO.output(14,GPIO.HIGH)
        else:
            GPIO.output(14,GPIO.LOW)
        if amplitude[i] > 8:
            GPIO.output(15,GPIO.HIGH)
        else:
            GPIO.output(15,GPIO.LOW)
        if amplitude[i] > 15:
            GPIO.output(18,GPIO.HIGH)
        else:
            GPIO.output(18,GPIO.LOW)
        if amplitude[i] > 22:
            GPIO.output(23,GPIO.HIGH)
        else:
            GPIO.output(23,GPIO.LOW)
        if amplitude[i] > 30:
            GPIO.output(24,GPIO.HIGH)
        else:
            GPIO.output(24,GPIO.LOW)
        if amplitude[i] > 34:
            GPIO.output(25,GPIO.HIGH)
        else:
            GPIO.output(25,GPIO.LOW)
        if amplitude[i] > 39:
            GPIO.output(8,GPIO.HIGH)
        else:
            GPIO.output(8,GPIO.LOW)
        if amplitude[i] > 43:
            GPIO.output(7,GPIO.HIGH)
        else:
            GPIO.output(7,GPIO.LOW)
            
        while time.time()< now + (1.0000000000/frame_rate*frame_skip*0.99):
	    time.sleep(.00000000001)
	now = time.time()
	
            


if __name__== '__main__':
    main()
