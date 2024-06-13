import tkinter as tk;
import os;
from tkinter import ttk;
from tkinter import filedialog as fd;
from tkinter import messagebox as msgbx;
import json;
import sys;
with open("config.json") as f:
    path = json.load(f);
    print(path);



class App:
    def __init__(self) -> None:
        self.loader = None
        self.version = None
    def config_loader(self):

        def set_loader():
            self.loader = chooser.get()
            root.destroy()
        def enable_btn(*args):
            if chooser.get() != "":
                valid_btn.config(state="enabled")
            else:
                valid_btn.config(state="disabled")
        root = tk.Tk()
        root.geometry("300x200")
        loaders_label = ttk.Label(root, text="Choose a loader")
        loaders_label.pack()
        loaders = os.listdir(path["modsdir"])
        chooser = ttk.Combobox(root, values = loaders)
        chooser.pack()
        valid_btn = ttk.Button(root, text="validate", command=set_loader, state="disabled")
        valid_btn.pack()
        chooser.bind("<<ComboboxSelected>>", enable_btn)
        root.wm_protocol("WM_DELETE_WINDOW", sys.exit)
        root.mainloop()
    def config_version(self):
        
        def set_version():
            self.version = version.get()
            root.destroy()
        def enable_btn(*args):
            if version.get() != "":
                valid_btn.config(state="enabled")
            else:
                valid_btn.config(state="disabled")
        root = tk.Tk()
        root.geometry("300x200")
        version_label = ttk.Label(root, text="Choose a version")
        version_label.pack()
        versions = os.listdir(os.path.join(path["modsdir"], self.loader))
        version = ttk.Combobox(root, values = versions)
        version.pack()
        version.bind("<<ComboboxSelected>>", enable_btn)
        valid_btn = ttk.Button(root, text="validate", command=set_version, state="disabled")
        valid_btn.pack()
        root.wm_protocol("WM_DELETE_WINDOW", sys.exit)
        root.mainloop()



    def run(self):
        self.config_loader()
        self.config_version()
        print(self.loader, self.version)
app = App()
app.run()