 # display the image with pillow
import time
import tkinter as tk
from PIL import ImageTk, Image
import os
import threading
from queue import Queue
import random

# Instructions text
instructions = ('\r\n\nWelcome to the experiment. \n\r When you are ready, press the red button' 
+ ' and hold it down while you speak your instructions. Then release the button and wait.'
+ ' An image will appear shortly.')

# Global reference to the window
g_windowForImage = None
g_windowForInstructions = None

def create_instructions_window():

    global g_windowForInstructions

    g_windowForInstructions = tk.Toplevel(root, bg='#52837D')
    g_windowForInstructions.title("Instructions")
    g_windowForInstructions.geometry("500x500+50+0")  # Position at (150, 250)
    label = tk.Label(g_windowForInstructions, text=instructions, 
                     font=("Helvetica", 32),
                     justify=tk.CENTER,
                     width=80,
                     wraplength=400,
                     bg='#52837D',
                     fg='#FFFFFF',
                     )
    label.pack()

def create_image_window():

    global g_windowForImage

    g_windowForImage = tk.Toplevel(root)
    g_windowForImage.title("Images")
    screen_width = g_windowForImage.winfo_screenwidth()
    screen_height = g_windowForImage.winfo_screenheight()
    g_windowForImage.geometry("+%d+%d" % (screen_width-1000, screen_height*.1))
    label = tk.Label(g_windowForImage)

    return label

def display_image(image_path, label=None):

    global g_windowForImage

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
    label.configure(image=photoImage)
    label.image = photoImage  # Keep a reference to the image to prevent it from being garbage collected
    label.pack() # Show the label

    return label

def close_image_window():

    global g_windowForImage

    if g_windowForImage is not None:
        g_windowForImage.destroy()
        g_windowForImage = None


# ------------------ Main Program --------------------

# create root window and hide it
root = tk.Tk()
root.withdraw()  # Hide the root window

create_instructions_window()

# list all png files in the history folder
historyFolder = "./history"
historyFiles = os.listdir(historyFolder)

#remove any non-png files from historyFiles
imagesToDisplay = []
for file in historyFiles:
    if file.endswith(".png"):
        #remove from the list
        imagesToDisplay.append(file)
        

#Experimenting with control of the image display window

label = create_image_window()

#display_image(newFileName, label)
runLoop = True
while runLoop:
    #display the image
    random.shuffle(imagesToDisplay)
    imagePath = './history/' + imagesToDisplay[0]
    print("Image displayed" + imagePath)
    display_image(imagePath, label)
    g_windowForImage.update_idletasks()
    g_windowForImage.update()
    time.sleep(3)


# When it's time to display the image:

print("Image displayed")
# delay 10 seconds 
time.sleep(10)
print("Image closed")
# When it's time to close the window:
close_image_window()