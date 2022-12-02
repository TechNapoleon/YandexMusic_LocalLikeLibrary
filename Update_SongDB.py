from yandex_music import Client
import os, mutagen, shutil, csv, json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.easyid3 import EasyID3
import pandas as pd
import numpy as np
import platform
import config


def metadata_updater(root_dir, os_sign, line):
    with open(root_dir + os_sign + "Library_MetaData.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(line)


target_os = platform.system()
Token_Client = config.api_token
client = Client(Token_Client).init()

if platform.system() == "Windows":
    os_sign = '\\'
else:
    os_sign = '/'

root_dir = config.project_dir
process_dir = root_dir + os_sign + "Process" + os_sign
fin_dir = root_dir + os_sign + "Music_DB" + os_sign

track_json = str(client.users_likes_tracks()).replace('None', '\"\"').replace("\'", "\"")
track_json = json.loads(track_json)

ids_ym = []
for track in track_json["tracks"]:
    ids_ym.append(int(track["id"]))

os.chdir(root_dir)
df_lib = pd.read_csv(root_dir + os_sign + "Library_MetaData.csv")
ids_loc = df_lib['ID'].tolist()

ids_for_download = []
for element in ids_ym:
    if element not in ids_loc:
        ids_for_download.append(element)

tracks_for_download = client.tracks(ids_for_download)
tracks_failed_download = []

cnt = -1  # Counter for tracks downloader
cnt_double = 0  # Num of attempts to download the tracks
cnt_success = 0

os.chdir(process_dir)
print("--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|")
print("                                       STARTING TO PROCESS THE UPDATE...")
print("--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|")
print("Starting to process the update...")
while True:
    if cnt_double <= 1:
        cnt += 1
    else:
        cnt += 2
        cnt_double = 0
    if cnt > len(ids_for_download) - 1:
        break
    track = tracks_for_download[cnt]
    try:
        name = track.title.replace("\\","").replace("/","")
        artist = track.artists[0].name
        print(cnt, " Processing {} by artist {}. ".format(name, artist))
        track.download(name + '.mp3')

        try:
            meta = EasyID3(name + '.mp3')
        except mutagen.id3.ID3NoHeaderError:
            meta = mutagen.File(name + '.mp3', easy=True)
            meta.add_tags()
        try:
            album = track.albums[0].title
        except:
            album = np.nan

        meta['artist'] = artist
        meta['album'] = album
        tack_id = track.id

        meta.save()

        audio = MP3(name + '.mp3', ID3=ID3)

        try:
            audio.add_tags()
        except error:
            pass

        try:
            track.downloadOgImage(filename='cover.jpeg', size='1000x1000')
            audio.tags.add(APIC(mime='cover.jpeg', type=3, desc=u'Cover', data=open('cover.jpeg', 'rb').read()))
            audio.tags.add(
                APIC(mime='cover.jpeg', type=3, desc=u'Front cover', data=open('cover.jpeg', 'rb').read()))
            audio.save()
        except:
            pass

        shutil.copy(process_dir + os_sign + name + '.mp3', fin_dir)

        for f in os.listdir():
            os.remove(f)

        cnt_double = 0

        metadata_updater(root_dir, os_sign, [tack_id, name, artist, album])
        cnt_success += 1
    except:
        tracks_failed_download.append([track.title, track.artists[0].name])
        print("An error has been occurred while trying to download this track")
        cnt -= 1
        cnt_double += 1

print("--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|")
print("                                         DONE UPDATING PROCESS")
print("--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|")


if len(tracks_failed_download) != 0:
    tmp_list = []
    for l in tracks_failed_download:
        if l not in tmp_list:
            tmp_list.append(l)
    tracks_failed_download = tmp_list
    print("There were {} tracks that failed to download. \nIf you see those tracks been failed every time, they maybe faulty. Here are the tracks-".format(len(tracks_failed_download)))
    for track in tracks_failed_download:
        print("Track {} by artist {} failed to download".format(track[0], track[1]))


print("There were {} tacks added to your library. Have a great time listening to your favorite music :)".format(cnt_success))
