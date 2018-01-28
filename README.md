# SoundCost
An image registration code in which the cost function in sonic!


## Origin story
This code came about as part of the Manchester-led part of a Bioinformatics MSc in which the students are taught about medical imaging. In particular, we do a lot of python programming to develop an image registration tool and do some tumour response measurements (with fake data).

Together with Mat Lowe, I teach the python part, and also prepare the practicals (which are in another repository). This year we also came up with some extension tasks for when the particularly good programmers got to the end of everything else. This was almost one of those tasks.

## What does it do
The code loads two images and displays them in a green/purple fusion window. The keyboard arrow keys are mapped such that they will move one of the images around. A mean squared error cost function is used to tell you when the images are overlapping well.

But that's not all...

The code launches a process in the background which beeps. The beep rate is dependant on the cost function so that as the cost function gets smaller (i.e. the images are closer together), the beeps get faster. 

This is a completely pointless addition to the 'image registration' code, but does show how to launch a simple process in the background to do stuff while your main process is doing something else.


## Dependencies
- matplotlib
- numpy
- scipy
- pyaudio
- multiprocessing
- time
