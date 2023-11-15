 # display the image with pillow
import time
import tkinter as tk
from PIL import ImageTk, Image
import os
import threading
from queue import Queue


# Global reference to the window
g_windowForImage = None
g_labelForImage = None


def create_window():

    global g_windowForImage
    global g_labelForImage

    # create image display window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    g_windowForImage = tk.Toplevel(root)
    g_windowForImage.geometry("+1000+250")  # Position at (500, 500)

def display_image(image_path):

    global g_windowForImage
    global g_labelForImage

    # Open an image file
    try:
        img = Image.open(image_path)
    except Exception as e:
        print("Error opening image file")
        print(e)
        return
    
    # Convert the image to a PhotoImage
    img = ImageTk.PhotoImage(img)
    # Create a label and add the image to it
    g_labelForImage = tk.Label(g_windowForImage, image=img)
    g_labelForImage.image = img  # Keep a reference to the image to prevent it from being garbage collected
    g_labelForImage.pack() # Show the label

def close_window():

    global g_windowForImage
    global g_labelForImage

    if g_windowForImage is not None:
        g_windowForImage.destroy()
        g_windowForImage = None



newFileName = "./history/image1.png"
'''
image = Image.open(newFileName)
image.show()

''' 
#Experimenting with control of the image display window

create_window()

# create image display window in a new thread
qImageDisplayControl = Queue()
#displayThread = threading.Thread(target=displayWindow.display_image, args=(qImageDisplayControl,newFileName),daemon=True)
#displayThread.start()

display_image(newFileName)
runLoop = True
while runLoop:
    g_windowForImage.update_idletasks()
    g_windowForImage.update()
    time.sleep(10)
    runLoop = False


# When it's time to display the image:

print("Image displayed")
# delay 10 seconds 
time.sleep(10)
print("Image closed")
# When it's time to close the window:
close_window()