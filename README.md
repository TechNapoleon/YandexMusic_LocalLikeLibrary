# YandexMusic downloader – Your Local Music Library

Preface - 
This Python project built for creating and managing a local music library based on your favorite music on YandexMusic platform. This project was created in order to listen to my favorite music via my favorite music player and to be able to control the music with hotkeys while using the pc. Btw, I  recommend you to use Tauon Music Box as the music player. You can find it on github – https://github.com/Taiko2k/TauonMusicBox . 
This library mostly based on project of developer by nick name MarshelX which author of project yandex-music-api. This is the link for his project – https://github.com/MarshalX/yandex-music-api .


Overview of the program - 
The program connects to YandexMusic profile via api-token that you provide in configuration file.
After the connection its checks in local csv file to see which tracks are already exists in the local library and differs it to list of track that are “liked” in the YandexMusic profile.
After the differ, the program download the tracks that does not exist in your local library. 
The tracks downloaded and processed to have a metadata of the track, with the name of the track, artist, album and cover of the track as you see it the YandexMusic platform. The script built in the way that after every track being download, the csv is updated as well. In other words, if the script stops in the middle of the process, the progression is saved and it will process rest of the tracks after you restart it.

Instruction -

First of all please run a setup.py script that creates directories that are needed later on to process the tracks, creates new csv file that used later to record downloaded tracks, and checks for necessary python packages.
As the second stage, please edit config.py file. To check your api-token you can use a telegram bot music-yandex-bot.ru which is a full telegram base YandexMusic client in which you can check your api-token or just google it :).
Third stage, just run the Update_SongDB.py script and enjoy the music :) .
 
Notes:
1. I mostly tasted the script in Linux environment so if you have so kind of problem, please let me know and I will try to work it around.
2. There some tracks that are defective and you may see them failing to download every time you update your local library. This tracks are printed to terminal in the end of the script if you run it manually. Please consider to delete in from you favorite list in the platform.
