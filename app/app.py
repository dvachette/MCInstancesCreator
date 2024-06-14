import tkinter as tk;
import os;
from tkinter import ttk;
from tkinter import filedialog as fd;
from tkinter import messagebox as msgbx;
import json;
import sys;
import zipfile;
import shutil;
import toml;

with open("config.json") as f:
    path = json.load(f);
    print(path);

with open(path["loaderspath"]) as f:
    loaders = json.load(f);
    print(loaders);

"""Add mods to the mods folder,
and create a table of dependencies for each mods
by reading it META-INF/mods.toml file"""

def select_mod():
    emptying_dir(path["tempdir"])   
    root = tk.Tk()
    mod_path = ""
    while mod_path == "":
        mod_path = fd.askopenfilename(
            master=root,
            title="Select mods to add",
            filetypes=[("jar files", "*.jar")]
        )
        if mod_path != "":
            with zipfile.ZipFile(mod_path, "r") as zip_ref:
                zip_ref.extractall(path["tempdir"])
        else:
            if msgbx.askretrycancel("Error", "No mods selected") == False:
                sys.exit()
    root.destroy()
    return mod_path
def place_mod(path_mod):
    if not os.listdir(path["tempdir"]):
        msgbx.showerror("Error", "No mod into the temp folder")
        sys.exit()
    else:
        meta_inf = lire_fichier_toml(os.path.join(path["tempdir"], "META-INF","mods.toml"))
        loader = loaders[meta_inf['modLoader']]
        mod_id = meta_inf["mods"][0]["modId"]
        print(loader)
        print(mod_id)
        dependencies = list()
        for mod in meta_inf["dependencies"][mod_id]:
            if mod['modId'] not in [loader, "minecraft"]:
                dependencies.append(mod['modId'])
            if mod['modId'] == "minecraft":
                versions = mod["versionRange"][1:-1].split(",")
        dict_to_dump = {"modId": mod_id, "loader": loader, "dependencies": dependencies, "versions": versions}
        with open(path["dependenciespath"], 'r') as f:
            dependencies_list = json.load(f)
            dependencies_list.append(dict_to_dump)
        with open(path["dependenciespath"], 'w') as f:
            json.dump(dependencies_list, f, indent=4)
        for version in versions:
            if not os.path.exists(os.path.join(path["modsdir"], loader, version)):
                os.makedirs(os.path.join(path["modsdir"], loader, version))
            shutil.copy(path_mod, os.path.join(path["modsdir"], loader, version, mod_id + ".jar"))



def lire_fichier_toml(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        contenu = toml.load(fichier)
    return contenu


def run():
    path_mod = select_mod()
    place_mod(path_mod)

def emptying_dir(chemin_repertoire):
    for nom in os.listdir(chemin_repertoire):
        chemin_complet = os.path.join(chemin_repertoire, nom)
        if os.path.isfile(chemin_complet) or os.path.islink(chemin_complet):
            os.remove(chemin_complet)
        elif os.path.isdir(chemin_complet):
            shutil.rmtree(chemin_complet)




run()