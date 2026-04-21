import ctypes, sys, os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Ensure the working directory is preserved for the new process
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    
    # Relaunch with "runas" (Admin prompt)
    ret = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    
    if int(ret) <= 32:
        print("Failed to elevate privileges or user denied prompt.")
    
    sys.exit()

import customtkinter as tk
from tkinter import filedialog
import subprocess
import glob

# OS things

TOOL_MAP =  {
    ".hve": {
        "path":"",
        "exe": "AmcacheParser.exe",
        "args":["-f"]},

    ".pf" : {
        "path":"",
        "exe":"PECmd.exe",
        "args":["-f"]},

    ".evtx":{
        "path":["EvtxECmd"],
        "exe":"EvtxECmd.exe",
        "args": ["-f"]},
    
    ".lnk":{
        "path":"",
        "exe":"LECmd.exe",
        "args":["-f"]},
    
    ".customDestinations-ms":{
        "path":"",
        "exe":"JLECmd",
        "args":["-f"]},

    ".automaticDestinations-ms":{
        "path":"",
        "exe":"JLECmd",
        "args":["-f"]},

    ".bcf":{
        "path":"",
        "exe":"RecentFileCacheParser.exe",
        "args":["-f"]
    }
}

def get_tool(path):
        name = os.path.basename(path).lower()
        ext = os.path.splitext(name)[1]

        if name == "$mft" or name.lower() == "mft":
            return {
                "path":["MFTECmd"],
                "exe":"MFTECmd.exe",
                "args":["-f"]
            }
        
        if name.lower() == "srudb.dat":
            return {
                "path":"",
                "exe":"SrumECmd.exe",
                "args":["-f"]
            }
        
        return TOOL_MAP.get(ext)


def run_tool(path):
        tool = get_tool(path)
        if not tool:
            return None, "Unsupported File Type! Select from:\n MFT \n .HVE \n .EVTX \n .PF \n .bcf \n"
        
        base_dir = os.path.dirname(__file__)

        if tool["path"] == "":
            exe_path = os.path.join(base_dir, tool["exe"])
        else:
            exe_path = os.path.join(base_dir, *tool["path"], tool["exe"])   
        output = os.path.dirname(path)
        cmd = [exe_path] + tool["args"] + [path, "--csv", output]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                )
            return output, result.stdout
        except subprocess.CalledProcessError as Error:
            return None, Error.stderr
    
# GUI implementation


tk.set_appearance_mode("dark")
tk.set_default_color_theme("blue")

class GUI(tk.CTk):
    def __init__(self):
        ## GUI
        super().__init__()
        self.iconbitmap(os.path.join(os.path.dirname(__file__), "favicon.ico"))
        self.title("EZ-ZTools V1.1")
        self.geometry("860x540")
        self.geometry("1700x600")
        self.minsize(800, 500)
        self.generated_csvs = []
        self.generated_csv = None
        
        

       
        sidebar = tk.CTkFrame(self, width=100)
        sidebar.pack(side="left", fill="y", padx=5, pady=5)
        

        # Actions
        global frame_middle
        frame_middle = tk.CTkFrame(self)
        frame_middle.pack(pady=10,padx=10,fill="x")
        self.file_label = tk.CTkLabel(frame_middle, text="Select File")
        
        selectBTN = tk.CTkButton(frame_middle,text="Select File",command=self.browse_file)
        selectBTN.pack(side="right",padx=10)
        processBTN = tk.CTkButton(frame_middle,text="Process File", command=self.process_file)
        processBTN.pack(side="left",padx=5)

        clearBTN = tk.CTkButton(frame_middle, text="Clear Output", command=self.clear_output)
        clearBTN.pack(side="right",padx=10)

        ezvBTN = tk.CTkButton(frame_middle, text="Open EZViewer", command=self.launch_ezviewer )
        ezvBTN.pack(side="left", padx=10)

        tleBTN = tk.CTkButton(frame_middle, text="Open Timeline Explorer (CSV)", command=self.launch_tle)
        tleBTN.pack(side="left", padx=10)

        # SIDE BAR FOR OUTPUTS
        

        self.sidebar = sidebar
        self.sb_btn = tk.CTkButton(frame_middle,text="Open ShellBag Explorer",command=self.launch_SBexplorer)
       
        # Outputs

        frame_bottom = tk.CTkFrame(self)
        frame_bottom.pack(pady=10,padx=10,fill="both", expand=True)

        self.output_box = tk.CTkTextbox(frame_bottom, wrap="word", font=("Courier", 16))
        self.output_box.pack(fill="both", expand=True, padx=5, pady=5)
    
    
        self.recentCSVs = []
    ## FILE FUNCTIONS

        
    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Supported files", "*.hve *.pf *.evtx *.lnk *.mft *.dat"),
        ("All files", "*.*")])
        if file:
            self.file_label.configure(text=file)
            self.output_box.insert("end", f"Selected: {file}\n")
            self.file_ext = os.path.splitext(file)[1].lower()  # store extension
            if self.checkDAT():
                self.sb_btn.pack(side="left", padx=10)
            else:
                self.sb_btn.pack_forget()
            
        
    
    def process_file(self):
        file_path = self.file_label.cget("text")
        if file_path == "Select File":
            self.output_box.insert("end","Error! Select a File!\n")
            self.after(1000,self.clear_output)  
        else:
            self.output_box.insert("end",f"Parsing: {file_path}\n")
            self.update()
            output_dir, output = run_tool(file_path)

            if not output_dir:
                self.output_box.insert("end",f"Error: {output}\n")
                return
            self.output_box.insert("end",output + "\n")


            csv_files = glob.glob(os.path.join(output_dir, "*.csv"))
            if csv_files:
                self.generated_csvs =  csv_files
                self.generated_csv = max(csv_files,key=os.path.getctime)
                self.output_box.insert("end",f"Detected {len(csv_files)} CSV file(s)\n")
                self.recentCSVs.insert(0, csv_files)

    
    ## Operational Functions
    def launch_ezviewer(self):
        ezviewer_path = os.path.join(os.path.dirname(__file__),"EZViewer","EZViewer.exe")
        if not os.path.exists(ezviewer_path):
            print("EZViewer.exe not found!")
        
            return
        file_path = self.file_label.cget("text")
        subprocess.Popen([ezviewer_path, file_path])
        
    def launch_tle(self):
        tle_path = os.path.join(os.path.dirname(__file__),"TimelineExplorer","TimelineExplorer.exe")
        if not os.path.exists(tle_path):
            print("TimelineExplorer.exe not found!")
            self.output_box.insert("end","TimelineExplorer.exe not Found! FATAL!")
            return    
        
        if not hasattr(self,"generated_csvs") or not self.generated_csvs:
            self.output_box.insert("end","No CSV Files available. Please Process a File First.\n")
            return
        subprocess.Popen([tle_path]  + self.generated_csvs)

    def view_csv_button(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if file:
            self.launch_ezviewer(file)

    def checkDAT(self):
        return hasattr(self, "file_ext") and self.file_ext == ".dat"
    def launch_SBexplorer(self):
        sbe_path = os.path.join(os.path.dirname(__file__),"ShellBagsExplorer","ShellBagsExplorer.exe")
        if not os.path.exists(sbe_path):
            self.output_box.insert("end","ShellBagsExplorer.exe not Found! FATAL!")
        file_path = self.file_label.cget("text")
        subprocess.Popen([sbe_path, file_path])

    
    

    ## EXTRANEOUS FUNCTIONS
    def clear_output(self):
        self.output_box.delete("1.0","end")

# Run App
app = GUI()
app.mainloop()


# 3/23:
# I added the general UI and Amcache Processing.
# First official creation of this project.
# Upcoming changes involve opening processed Files in CSV / Plaintext Format