from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import time
import os
import cv2
import threading

#Initial directory
dirname = os.getcwd()

root = Tk()
root.title('Image Capture')
root.geometry('527x297')
#root.iconbitmap()

file_path_frame = LabelFrame(root, text = 'File Path')
file_path_frame.grid(row = 0 , column = 0 , columnspan = 3 , padx = 5 , pady = 5 , sticky = 'WE')

path_label = Label(file_path_frame , text = 'Please Set Your Path To Save Your Pictures : ')
path_label.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = 'W')

path_entry = Entry(file_path_frame , width = 60)
path_entry.grid(row = 1 , column = 0 , padx = 5 , pady = 5)
path_entry.insert(0 , os.getcwd())


browse_button = Button(file_path_frame , text = 'Browse'  ,   width = 12 , command = lambda : browse())
browse_button.grid(row = 1 , column = 2 , padx = 5 , pady = 5 , sticky = 'E')

############### another frame ########################

setting_frame =  LabelFrame(root, text = 'Setting')
setting_frame.grid(row = 1 , column = 0 , columnspan = 3 , padx = 5 , pady = 5 , sticky = 'WE')

image_names_label = Label(setting_frame , text = 'Enter Your Image Name : ')
image_names_label.grid(row = 0 , column  = 0 , padx = 5 , pady = 5)

image_name_entry = Entry(setting_frame , width = 40)
image_name_entry.grid(row = 0 , column = 1 , padx = 5 , pady = 5)
image_name_entry.insert(0 , 'image_name')

delay_label = Label(setting_frame , text = 'Delay(sec) : ')
delay_label.grid(row = 1 , column = 0  , padx = 5 , pady = 5 , sticky = 'W')

delay_entry = Entry(setting_frame , width = 8)
delay_entry.grid(row = 1 , column = 1 , padx = 5 , pady = 5 , sticky = 'W')
delay_entry.insert(0, 2)

duration_label = Label(setting_frame , text = 'Duration(sec) : ')
duration_label.grid(row = 2 , column = 0  , padx = 5 , pady = 5 , sticky = 'W')

duration_entry = Entry(setting_frame , width = 8)
duration_entry.grid(row = 2 , column = 1 , padx = 5 , pady = 5 , sticky = 'W')
duration_entry.insert(0 , 5)

capture_buttton = Button(setting_frame , text = 'Capture' , width = 12 , command = lambda : threading.Thread(target = image_capture).start())
capture_buttton.grid(row = 3 , column = 2 , padx = 5 , pady = 5 , sticky = 'E')

exit_button = Button(root , text = 'Exit' , width = 12 , command = lambda : root.destroy())
exit_button.grid(row = 2 , column = 1 , padx = 5 , pady = 5)

# save_path = 'C:/example/'

# name_of_file = raw_input("What is the name of the file: ")

# completeName = os.path.join(save_path, name_of_file+".txt")  

def browse():
    global dirname
    dirname = filedialog.askdirectory(initialdir = os.getcwd() , title = 'Select a Directory')
    path_entry.delete(0, 'end')
    path_entry.insert(0 , string = dirname)
    
    save_path = dirname

def image_capture():
    cap = cv2.VideoCapture(0)
    
    img_counter = 0
    sec = 0
    
    while True:
        global dirname
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        time.sleep(0.1)
        sec += 0.1

        if (sec >= 0) and (sec <= float(delay_entry.get())):
            _ , frame = cap.read()
            cv2.putText(frame, 'Press ESC to stop processing...',  (0, 470), font, 0.5, (0, 0, 0), 1, cv2.LINE_4)
            cv2.putText(frame, 'Recording In '+  str(round(float(delay_entry.get()) - sec , 2)) + ' s',  (0, 25), font, 0.5, (0, 0, 0), 1, cv2.LINE_4)
            cv2.imshow('Image Capture' , frame)


        elif (sec >= float(delay_entry.get())) and (sec <= (float(duration_entry.get()) + float(delay_entry.get()))):
            _ , frame = cap.read()

            img_name = "{}({}).png".format(str(image_name_entry.get()) , img_counter)
            completeName = os.path.join(dirname, img_name)
            cv2.imwrite(completeName, frame)
            
            cv2.putText(frame, 'Press ESC to stop processing...',  (0, 470), font, 0.5, (0, 0, 0), 1, cv2.LINE_4)
            cv2.putText(frame, str(img_counter) + ' images have been captured...',  (0, 25), font, 0.5, (0, 0, 0), 1, cv2.LINE_4)
            cv2.imshow('Image Capture' , frame)
        
            

            img_counter += 1
            # print("{} written!".format(img_name))
        
        elif (sec >= (float(duration_entry.get()) + float(delay_entry.get()))) :
            messagebox.showinfo('Number of Images' , '{} Images Have Been Captured!'.format(str(img_counter)))
            break
        k = cv2.waitKey(1)
        
        if k%256 == 27:             # ESC pressed
            #print("Escape hit, closing...")
            response = messagebox.askyesno(title = 'Exit' , message = 'Process Has Been Paused.\nWould You Like To Exit?')
            if response == 1:
                messagebox.showinfo('Number of Images' , '{} Images Have Been Captured!'.format(str(img_counter)))
                break
            else:
                continue   
    
    cap.release()
    cv2.destroyAllWindows()


root.mainloop()
