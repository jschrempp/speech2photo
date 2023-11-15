 # display the image with pillow
import time
import tkinter as tk
from PIL import ImageTk, Image
import os
import threading
from queue import Queue
import random


# Global reference to the window
g_windowForImage = None
#label = None

def create_window():

    global g_windowForImage
    # create image display window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    g_windowForImage = tk.Toplevel(root)
    g_windowForImage.geometry("+750+250")  # Position at (500, 500)
    label = tk.Label(g_windowForImage)

    return label

def display_image(image_path, label=None):

    global g_windowForImage
    #global label


    # Open an image file
    try:
        img = Image.open(image_path)
    except Exception as e:
        print("Error opening image file")
        print(e)
        return

    #resize the image to fit the window
    img = img.resize((800, 850), Image.NEAREST)

    # Convert the image to a PhotoImage
    photoImage = ImageTk.PhotoImage(img)
    # Create a label and add the image to it
    #if label is None:
        #label = tk.Label(g_windowForImage)
    label.configure(image=photoImage)
    label.image = photoImage  # Keep a reference to the image to prevent it from being garbage collected
    label.pack() # Show the label

    return label

def close_window():

    global g_windowForImage

    if g_windowForImage is not None:
        g_windowForImage.destroy()
        g_windowForImage = None


# list all png files in the history folder
historyFolder = "./history"
historyFiles = os.listdir(historyFolder)

#remove any non-png files from historyFiles
imagesToDisplay = []
for file in historyFiles:
    if file.endswith(".png"):
        #remove from the list
        imagesToDisplay.append(file)
        
'''
newFileName = "./history/image1.png"
secondFileName = "./history/image2.png"

image = Image.open(newFileName)
image.show()

''' 
#Experimenting with control of the image display window

label = create_window()

#display_image(newFileName, label)
runLoop = True
while runLoop:
    #display the image
    random.shuffle(imagesToDisplay)
    display_image('./history/' + imagesToDisplay[0], label)
    g_windowForImage.update_idletasks()
    g_windowForImage.update()
    time.sleep(3)


# When it's time to display the image:

print("Image displayed")
# delay 10 seconds 
time.sleep(10)
print("Image closed")
# When it's time to close the window:
close_window()