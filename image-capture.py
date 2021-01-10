import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time
import threading
import cv2
import os

class MainWindow(tk.Frame):
    def __init__(self , master):
        tk.Frame.__init__(self , master)
        self.master = master
        self.dirname = os.getcwd()
        self.initializer_user_interface()
    
    def initializer_user_interface(self):
        self.master.title('Image Capture App')
        self.master.geometry('527x297')
        #self.master.grid_rowconfigure(0, weight=1)
        #self.master.grid_columnconfigure(0, weight=1)
        self.file_path_frame = tk.LabelFrame(self.master , text = 'File Path')
        self.file_path_frame.grid(row = 0 , column = 0 , columnspan = 3 , padx = 5 , pady = 5 , sticky = 'WE')
        
        self.path_label = tk.Label(self.file_path_frame , text = 'Please Set Your Path To Save Your Pictures : ')
        self.path_label.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = 'W')

        self.path_entry = tk.Entry(self.file_path_frame , width = 60)
        self.path_entry.grid(row = 1 , column = 0 , padx = 5 , pady = 5)
        self.path_entry.insert(0 , os.getcwd())

        self.browse_button = tk.Button(self.file_path_frame , text = 'Browse'  ,   width = 12 , command = lambda : self.browse())
        self.browse_button.grid(row = 1 , column = 2 , padx = 5 , pady = 5 , sticky = 'E')

        # Another frame
        self.setting_frame =  tk.LabelFrame(self.master , text = 'Setting')
        self.setting_frame.grid(row = 1 , column = 0 , columnspan = 3 , padx = 5 , pady = 5 , sticky = 'WE')

        self.image_names_label = tk.Label(self.setting_frame , text = 'Enter Your Image Name : ')
        self.image_names_label.grid(row = 0 , column  = 0 , padx = 5 , pady = 5)

        self.image_name_entry = tk.Entry(self.setting_frame , width = 40)
        self.image_name_entry.grid(row = 0 , column = 1 , padx = 5 , pady = 5)
        self.image_name_entry.insert(0 , 'image_name')

        self.delay_label = tk.Label(self.setting_frame , text = 'Delay(sec) : ')
        self.delay_label.grid(row = 1 , column = 0  , padx = 5 , pady = 5 , sticky = 'W')

        self.delay_entry = tk.Entry(self.setting_frame , width = 8)
        self.delay_entry.grid(row = 1 , column = 1 , padx = 5 , pady = 5 , sticky = 'W')
        self.delay_entry.insert(0, 2)

        self.duration_label = tk.Label(self.setting_frame , text = 'Duration(sec) : ')
        self.duration_label.grid(row = 2 , column = 0  , padx = 5 , pady = 5 , sticky = 'W')

        self.duration_entry = tk.Entry(self.setting_frame , width = 8)
        self.duration_entry.grid(row = 2 , column = 1 , padx = 5 , pady = 5 , sticky = 'W')
        self.duration_entry.insert(0 , 5)
        
        self.capture_buttton = tk.Button(self.setting_frame , text = 'Capture' , width = 12 , command = lambda : threading.Thread(target = self.image_capture).start())
        self.capture_buttton.grid(row = 3 , column = 2 , padx = 5 , pady = 5 , sticky = 'E')

        self.exit_button = tk.Button(self.master , text = 'Exit' , width = 12 , command = lambda : self.master.destroy())
        self.exit_button.grid(row = 2 , column = 1 , padx = 5 , pady = 5)

    def browse(self):
        global dirname
        self.dirname = tk.filedialog.askdirectory(initialdir = os.getcwd() , title = 'Select a Directory')
        self.path_entry.delete(0, 'end')
        self.path_entry.insert(0 , string = self.dirname)
        self.save_path = self.dirname

    def image_capture(self):
        cap = cv2.VideoCapture(0)
        self.img_counter = 0
        self.sec = 0
        
        while True:
            #global self.dirname
            self.font = cv2.FONT_HERSHEY_SIMPLEX            
            time.sleep(0.1)
            self.sec += 0.1

            if (self.sec >= 0) and (self.sec <= float(self.delay_entry.get())):
                _ , self.frame = cap.read()
                cv2.putText(self.frame, 'Press ESC to stop processing...',  (0, 470), self.font, 0.5, (0, 0, 0), 1, cv2.LINE_4)
                cv2.putText(self.frame, 'Recording In '+  str(round(float(self.delay_entry.get()) - self.sec , 2)) + ' s',  (0, 25), self.font, 0.5, (0, 0, 0), 1, cv2.LINE_4)
                cv2.imshow('Image Capture' , self.frame)

            elif (self.sec >= float(self.delay_entry.get())) and (self.sec <= (float(self.duration_entry.get()) + float(self.delay_entry.get()))):
                _ , self.frame = cap.read()

                self.img_name = "{}({}).png".format(str(self.image_name_entry.get()) , self.img_counter)
                self.completeName = os.path.join(self.dirname, self.img_name)
                cv2.imwrite(self.completeName, self.frame)
                
                cv2.putText(self.frame, 'Press ESC to stop processing...',  (0, 470), self.font, 0.5, (0, 0, 0), 1, cv2.LINE_4)
                cv2.putText(self.frame, str(self.img_counter) + ' images have been captured...',  (0, 25), self.font, 0.5, (0, 0, 0), 1, cv2.LINE_4)
                cv2.imshow('Image Capture' , self.frame)
            
                self.img_counter += 1
                # print("{} written!".format(img_name))
            
            elif (self.sec >= (float(self.duration_entry.get()) + float(self.delay_entry.get()))) :
                messagebox.showinfo('Number of Images' , '{} Images Have Been Captured!'.format(str(self.img_counter)))
                break
            k = cv2.waitKey(1)
            
            if k%256 == 27:             # ESC pressed
                #print("Escape hit, closing...")
                self.response = messagebox.askyesno(title = 'Exit' , message = 'Process Has Been Paused.\nWould You Like To Exit?')
                if self.response == 1:
                    messagebox.showinfo('Number of Images' , '{} Images Have Been Captured!'.format(str(self.img_counter)))
                    break
                else:
                    continue   
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
   root = tk.Tk()
   run = MainWindow(root)
   root.mainloop()
