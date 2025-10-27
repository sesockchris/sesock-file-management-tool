import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
import tkinter.scrolledtext as tkscrolled
from tkinter.filedialog import askopenfilename
from tkinter.font import Font 
import os, shutil, re, string, random, time, hashlib
from time import sleep
from datetime import date
import platform

master = tk.Tk()
master.title("Sesock File Manager")
left_edge = master.winfo_screenwidth()/3
top_edge = master.winfo_screenheight()/3
master.geometry('%dx%d+250+250' %(700, 560))
master.resizable(False, False)

regex = '\([^()]*\)'

master.tk.call('source', 'forest-dark.tcl')
s = ttk.Style(master).theme_use('forest-dark')

BUTTON_WIDTH = 17
console_font = Font(family="Consolas", size=11)

master.bind('<Control-c>', lambda event: console.delete(1.0, "end"))
master.bind('<Control-o>', lambda event: changeDirectory())
master.bind('<F1>', lambda event: aboutDialog())

try:
    photo = PhotoImage(file="assets\\IconSmall.png")
    master.iconphoto(False, photo)
except:
    pass

full_directory = os.getcwd()
text = tk.StringVar()
text.set(full_directory[-48:])

TAB_CONTROL = ttk.Notebook(master)
tabBasicOperations = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabBasicOperations, text="Basic Tools")
tabAdvancedOperations = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabAdvancedOperations, text="Advanced Tools")
tabSettings = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(tabSettings, text="Settings")
TAB_CONTROL.pack(expand=1, fill="both")

currentDirectory1 = ttk.Label(tabBasicOperations, text="Current Directory: ").place(x=120, y=20)
directoryText1 = ttk.Label(tabBasicOperations, textvariable=text, foreground="#217346").place(x=225, y=20)
currentDirectory2 = ttk.Label(tabAdvancedOperations, text="Current Directory: ").place(x=20, y=20)
directoryText2 = ttk.Label(tabAdvancedOperations, textvariable=text, foreground="#217346").place(x=130, y=20)

#Interface buttons
#Column 1
renameButton = ttk.Button(tabBasicOperations, text="Rename Files", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:renameFiles()).place(x=20, y=60)
organizeButton = ttk.Button(tabBasicOperations, text="Organize Files", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:organizeFiles()).place(x=20, y=95)
moveupButton = ttk.Button(tabBasicOperations, text="Move Files Up", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:moveupFiles()).place(x=20, y=130)
backupButton = ttk.Button(tabBasicOperations, text='Hash Files', width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:hashFiles()).place(x=20, y=165)
#Column 2
directoryButton = ttk.Button(tabBasicOperations, text="Change Directory...", width=BUTTON_WIDTH, command=lambda:changeDirectory()).place(x=180, y=60)
listfilesButton = ttk.Button(tabBasicOperations,text='List Files', width=BUTTON_WIDTH, command=lambda:listFiles()).place(x=180, y=95)
clearConsoleButton = ttk.Button(tabBasicOperations, text="Clear Console", width=BUTTON_WIDTH, command=lambda:clearConsole()).place(x=180, y=130)
resetDirectoryButton = ttk.Button(tabBasicOperations, text="Reset Directory", width=BUTTON_WIDTH, command=lambda:resetDirectory()).place(x=180, y=165)

check_frame = ttk.LabelFrame(master, text="Options").place(x=320, y=60)
check_1 = ttk.Checkbutton(check_frame, text="Unchecked")

# Create a Frame for the Radiobuttons
radio_frame = ttk.LabelFrame(tabBasicOperations, text="Name Schema", padding=(5, 5))
radio_frame.place(x=350, y=53)
d = tk.IntVar(value=3)
# Radiobuttons
radio_1 = ttk.Radiobutton(radio_frame, text="Numbers", variable=d, value=1)
radio_1.grid(row=0, column=0, padx=5, pady=6, sticky="nsew")
radio_2 = ttk.Radiobutton(radio_frame, text="Hashes", variable=d, value=2)
radio_2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
radio_3 = ttk.Radiobutton(radio_frame, text="Mixed", variable=d, value=3)
radio_3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

#Console
#console = tkscrolled.ScrolledText(height=13, width=57, foreground='white', background='black', undo=True)
console = tkscrolled.ScrolledText(height=15, width=82, font=console_font, foreground='white', background='black', undo=True)
console.place(x=10, y=250)
console.insert(1.0, "> Sesock File Management Tool [Version 0.0.6.1]\n")
console.insert(2.0, "> (c) Chris Sesock " + str(date.today().year))

#Footer
length_label1 = ttk.Label(text="Files : ", foreground='#d0d5db').place(x=10, y=530)
length_text = tk.StringVar()
length_text.set("0")
length_label = ttk.Label(textvariable=length_text, foreground='#d0d5db').place(x=50, y=530)

os_name = platform.system()
system_label = ttk.Label(text=str(os_name), foreground="#d0d5db").place(x=620, y=530)

#Advanced Tab
regexLabel = ttk.Label(tabAdvancedOperations, text="Regex").place(x=20, y=75)
replacementLabel = ttk.Label(tabAdvancedOperations, text="Replacement").place(x=235, y=75)
modifyButton = ttk.Button(tabAdvancedOperations, text="Modify with Regex", width=BUTTON_WIDTH, style="Accent.TButton", command=lambda:modifyWithRegex()).place(x=20, y=135)

modifyEntry = ttk.Entry(tabAdvancedOperations, width=28)
modifyEntry.place(x=20, y=100)
modifyEntry.insert(0, regex)

parameterEntry = ttk.Entry(tabAdvancedOperations, width=29)
parameterEntry.place(x=235, y=100)

#Settings Buttons
defaultDirectoryLabel = ttk.Label(tabSettings, text="Default Directory:").place(x=30, y=55)
defaultDirectory = ttk.Entry(tabSettings, width=70)
defaultDirectory.place(x=160, y=50)
defaultDirectory.insert(0, full_directory)

defaultBackupLabel = ttk.Label(tabSettings, text="Default Backup:").place(x=30, y=95)
defaultBackup = ttk.Entry(tabSettings, width=70)
defaultBackup.place(x=160, y=90)
defaultBackup.insert(0, full_directory+'\\backup')

defaultHashLengthLabel = ttk.Label(tabSettings, text="Default Hash Length:").place(x=30, y=135)
defaultHashLength = ttk.Entry(tabSettings, width=5)
defaultHashLength.place(x=160, y=130)
defaultHashLength.insert(0, '5')

#Batch renaming of files
def renameFiles(event=None):
    console.delete(1.0, 'end')
    console.insert(1.0, '> Renaming Files...\n')

    directory = full_directory
    to_be_named = os.listdir(path = directory)

    total = getFileCount()
    counter = 2.0
    if d.get() == 3: #mix of hashes and numbers
        for i in range(0, len(to_be_named)):
            extension = os.path.splitext(to_be_named[i])[1]
            filename = str(i+1)+'-'+''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(int(defaultHashLength.get())))+extension
            os.rename(os.path.join(full_directory, to_be_named[i]), os.path.join(full_directory, filename))
            console.insert(counter, "> Renaming file "+str(i)+" of "+str(total)+"\n")
            counter+=1     
        console.insert(counter, "> Files successfully renamed")
    elif d.get() == 2: # just hashes
        for i in range(0, len(to_be_named)):
            extension = os.path.splitext(to_be_named[i])[1]
            filename = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(int(defaultHashLength.get())))+extension
            os.rename(os.path.join(full_directory, to_be_named[i]), os.path.join(full_directory, filename))
            console.insert(counter, "Renaming file "+str(i)+" of "+str(total)+"\n")
            counter+=1     
        console.insert(counter, "Files successfully renamed")
    else:
        for i in range(0, len(to_be_named)):
            extension = os.path.splitext(to_be_named[i])[1]
            filename = str(i+1)+extension
            #os.rename(os.path.join(full_directory, to_be_named[i]), os.path.join(full_directory, re.sub('\([^()]*\)', "", to_be_named[i])))
            #re.sub('\([^()]*\)', "", to_be_named[i])
            console.insert(counter, "Renaming file "+str(i)+" of "+str(total)+"\n")
            counter+=1     
        console.insert(counter, "Files successfully renamed")

def modifyWithRegex():
    to_be_named = os.listdir(full_directory)
    #regex = 
    try:
        for i in range(0, len(to_be_named)):
            extension = os.path.splitext(to_be_named[i])[1]
            filename = str(i+1)+extension
            os.rename(os.path.join(full_directory, to_be_named[i]), os.path.join(full_directory, re.sub(modifyEntry.get(), "", to_be_named[i])))
    except:
        print("There was an unknown error...")

def organizeFiles(event=None):
    console.delete(1.0, "end")
    console.insert(1.0, "> Organizing Files...")
    #shutil.move(path+'/'+file_, path+'/'+ext+'/'+file_)

#Moves all files in current directory up one level
def moveupFiles(event=None):
    filename = filedialog.askdirectory()
    for root, dirs, files in os.walk(filename, topdown=False):
        for file in files:
            try:
                shutil.move(os.path.join(root, file), filename)
            except OSError:
                pass

def hashFiles():
    console.delete(1.0, 'end')
    console.insert(1.0, "> Generating MD5 hashes for all files in current directory...")
    directory = full_directory
    to_be_named = os.listdir(path = directory)
    filenames = glob.glob(full_directory)
    to_be_named = os.listdir(path = full_directory)
    hashes = []

#Creates backup of files in current directory
def backupFiles(event=None):
    console.delete(1.0, 'end')
    console.insert(1.0, "> Opening Backup File dialog...\n")

    filename = tk.filedialog.askopenfilename(title="Choose File to Backup")
    shutil.copy(filename, os.getcwd())

    console.insert(2.0, "> Files successfully backed up")

#Compresses files in current directory
def compressFiles(event=None):
    filename = tk.filedialog.askopenfilename(title="Choose File to Compress")
    shutil.make_archive('compressed', 'zip', filename)

#Prints all files in current directory to console
def listFiles(event=None):
    line_number = 1
    files = os.listdir(full_directory)
    console.delete(1.0, 'end')
    counter = 2.0
    console.insert(1.0, "> Total File Count: " + str(len(files)) +"\n")
    for file in files:
        filename = os.path.splitext(file)[0]
        extension = os.path.splitext(file)[1]
        console.insert(counter, str(line_number)+")\t"+filename+'\n')
        counter+=1.0
        line_number+=1

#Changes current directory used by the tool
def changeDirectory(event=None):
    console.delete(1.0, 'end')
    console.insert(1.0, "> Changing directory...\n")
    
    global full_directory
    filename = filedialog.askdirectory()
    if not filename:
        console.insert(2.0, "> Operation cancelled\n")
        return 
    full_directory = filename 
    text.set(filename[-65:])
    length_text.set(str(getFileCount()))
    console.insert(2.0, "> Directory successfully changed\n")

#Returns int of file count
def getFileCount():
    return len(os.listdir(full_directory))

#Outputs int of file count to console
def outputFileCount(event=None):
    list = os.listdir(full_directory)
    number = len(list)
    console.delete(1.0, 'end')
    console.insert(1.0, str(len(os.listdir(full_directory))))
    
def clearConsole(event=None):
    console.delete(1.0, "end")

def resetDirectory(event=None):
    console.delete(1.0, "end")
    global full_directory
    full_directory = os.getcwd()
    text.set(full_directory[-48:])
    console.insert(2.0, "> Directory Reset")

def load(n):
    console.delete(1.0, 'end')
    for i in range(n):
        sleep(0.1)
        console.insert(1.0, f"{i/n*100:.1f} %", end="\r")  

def aboutDialog():
    dialog = """ Author: Chris Sesock \n Version: 0.0.5 \n Commit: 077788d6166f5d69c9b660454aa264dd62956fb6 \n Date: 2021--06:12:00:00 \n Python: 3.8.5 \n OS: Windows_NT x64 10.0.10363
             """
    messagebox.showinfo("About", dialog)

if __name__ == '__main__':
    master.mainloop()
