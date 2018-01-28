
import pyaudio
from multiprocessing import Process, Value
import matplotlib.pyplot as plt
from scipy import misc
from time import sleep
from scipy.ndimage import interpolation, rotate
import numpy as np


def beepInBackground(rate):
    while True:
        duration = 0.25
        play_sound(800)
        sleep(2*rate.value)




lung1 = misc.imread("lungs.jpg",flatten=True)
lung2 = misc.imread("lungs2.jpg",flatten=True)

fig = plt.figure()
ax = fig.add_subplot(111)

fixed = ax.imshow(lung1, cmap="Greens_r")
floating = ax.imshow(lung2, cmap="Purples_r", alpha=0.5)

def tone(freq):
    sampling_rate = 44100   # integer sampling rate in Hz
    duration = 0.25         # in seconds
    # sample values must be in range [-1.0, 1.0]
    sample = (np.sin(2*np.pi*np.arange(sampling_rate*duration)*freq/sampling_rate)).astype(np.float32)
    return sample

def play_sound(freq):
    p = pyaudio.PyAudio()

    volume = 1.0            # range [0.0, 1.0]
    sampling_rate = 44100   # integer sampling rate in Hz
    duration = 0.8          # in seconds
    stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sampling_rate,
                output=True)

    stream.write(volume*tone(freq))

    stream.stop_stream()
    stream.close()

    p.terminate()

def cost_function(im1,im2):
    return np.mean((im1-im2)**2)+400.0

# separate out the user interface and shift functions
def eventHandler(event):
    """
    This function handles deciphering what the user wants us to do,
    the event knows which key has been pressed.
    """
    UD = 0
    LR = 0
    CW = 0
    whichKey = event.key
    if whichKey == "up":
        UD -= 1
    elif whichKey == "down":
        UD += 1
    elif whichKey == "left":
        LR -= 1
    elif whichKey == "right":
        LR += 1
    elif whichKey == "alt+left":
        CW += 1
    elif whichKey == "alt+right":
        CW -= 1

    shiftImages([UD,LR,CW])
    
global rate
rate = Value('d', 1.0)

def shiftImages(shifts):
    """
    This function interpolates the image into its shifted position.
    """

    UD, LR, CW = shifts

    global lung2

    lung2 = interpolation.shift(lung2, (UD,LR), mode='nearest', order=1)
    lung2 = rotate(lung2, CW, reshape=False)

    floating.set_data(lung2)
    cost = cost_function(lung1,lung2)
    ax.set_title(cost)
    maxCost = np.mean(lung1**2) #+400.90
    global rate
    rate.value = cost/maxCost
    # open("rateFile", 'w').write(str(cost/maxCost))
    fig.canvas.draw()


def main():
    global rate
    process = Process(target=beepInBackground, args=(rate,))
    process.start()

    # Connect the event handler to the plot
    fig.canvas.mpl_connect('key_press_event', eventHandler)
    plt.show()

    process.terminate()

if __name__ == "__main__":
    main()