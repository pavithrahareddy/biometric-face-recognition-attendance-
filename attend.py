import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import pymysql
import tkinter.ttk as ttk
import tkinter.font as font

window1 = tk.Tk()
window1.title("FACULTY FACE RECOGNITION ATTENDANCE SYSTEM")
window1.geometry('600x300')
window1.configure(background='blue')
message1 = tk.Label(window1, text="Faculty Attendance Portal"  ,fg="black", bg="white"  ,font=('Comic Sans MS', 20, 'bold underline'))
message1.place(x=160, y=50)


def DispWin():
    
    window = tk.Tk()
    window.title("Face_Recogniser")

    dialog_title = 'QUIT'
    dialog_text = 'Are you sure?'
 
    window.geometry('1280x720')
    window.configure(background='black')


    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)


    message = tk.Label(window, text="Faculty Attendance System"  ,fg="white", bg="black"  ,font=('arial', 26, 'bold underline'))

    message.place(x=300, y=50)

    lbl = tk.Label(window, text="Enter ID No.",width=20  ,height=2, bg="grey"  ,font=('arial', 15, ' bold ') )
    lbl.place(x=200, y=200)

    txt = tk.Entry(window,width=20  ,bg="white" ,font=('arial', 15, ' bold '))
    txt.place(x=600, y=215)

    lbl2 = tk.Label(window, text="Enter Name",width=20  ,bg="grey"    ,height=2 ,font=('arial', 15, ' bold ')) 
    lbl2.place(x=200, y=300)

    txt2 = tk.Entry(window,width=20  ,bg="white"  ,font=('arial', 15, ' bold ')  )
    txt2.place(x=600, y=315)

    lbl3 = tk.Label(window, text="Notification : ",width=20  ,bg="grey"  ,height=2 ,font=('arial', 15, ' bold ')) 
    lbl3.place(x=200, y=400)

    message = tk.Label(window, text="" ,bg="grey"  ,width=30  ,height=2, activebackground = "yellow" ,font=('arial', 15, ' bold ')) 
    message.place(x=600, y=400)

    

    

    
    
 
    def clear():
        txt.delete(0, 'end')    
        res = ""
        message.configure(text= res)

    def clear2():
        txt2.delete(0, 'end')    
        res = ""
        message.configure(text= res)    
    
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
 
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
 
        return False
 
    def TakeImages():        
        Id=(txt.get())
        name=(txt2.get())
        if(is_number(Id) and name != ""):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    sampleNum=sampleNum+1
                    cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('frame',img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum>60:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name]
            with open('StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)

    def TrainImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("trainner.yml")
        res = "Image Trained"
        message.configure(text= res)

    
    


    def getImagesAndLabels(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        faces=[]
        Ids=[]
        for imagePath in imagePaths:
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,'uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)        
        return faces,Ids

    
        
    clearButton = tk.Button(window, text="Clear", command=clear  ,width=5  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton.place(x=850, y=210)
    clearButton2 = tk.Button(window, text="Clear", command=clear2  ,width=5  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton2.place(x=850, y=310)    
    takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 17, ' bold '))
    takeImg.place(x=200, y=500)
    trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 17, ' bold '))
    trainImg.place(x=500, y=500)
    quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,width=12  ,height=2, activebackground = "Red" ,font=('times', 17, ' bold '))
    quitWindow.place(x=800, y=500)
    window.mainloop()

def TrackImages():
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)    
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 60):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]

                
                else:
                    Id='Unknown'                
                    tt=str(Id)  
                        
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
            cv2.imshow('Press q to mark attendance',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance\Attendance_"+date+".csv"
        attendance.to_csv(fileName,index=False)
        db = pymysql.connect("localhost", "root", "", "attendance")
        cursor = db.cursor()
        csv_data = csv.reader(open(fileName))
        next(csv_data)
        for row in csv_data:
            cursor.execute('INSERT INTO info(ID,NAME,DATE,TIME) VALUES(%s, %s, %s, %s)', row)
        db.commit()
        cursor.close()
        cam.release()
        cv2.destroyAllWindows()
        res=attendance
        message2.configure(text= res)

Attend = tk.Button(window1, text="Attendance", command=TrackImages  ,width=10  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
Attend.place(x=110, y=140)
Register = tk.Button(window1, text="Register", command=DispWin  ,width=10  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
Register.place(x=360, y=140)
message2 = tk.Label(window1, text="" ,bg="grey",activeforeground = "black",width=30  ,height=2  ,font=('arial', 15, ' bold ')) 
message2.place(x=180, y=210)

window1.mainloop()




