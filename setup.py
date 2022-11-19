import subprocess
import sys
import os
import pandas as pd


# Installing all necessary packages for the project
def install_lib(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def pack_checker(pack):
    try:
        import pack
    except: install_lib(pack)


packs = ["yandex-music", "mutagen", "pandas"]

for pack in packs:
    pack_checker(pack)


# Creating all the necessary directions
if not os.path.exists("Music_DB"):
    os.mkdir("Music_DB")
if not os.path.exists("Process"):
    os.mkdir("Process")


# Creating music library metadata file
if not os.path.exists("Library_MetaData.csv"):
    music_metadata = pd.DataFrame(columns=['ID', 'Name', 'Artrist', 'Album'])
    music_metadata.to_csv("Library_MetaData.csv", index=False, encoding='UTF-8')
