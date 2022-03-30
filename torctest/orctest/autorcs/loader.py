#-*-coding:GBK -*-
import os
from xml.dom.minidom import parse
 
def now_track(torcspath):
    dtree = parse(torcspath + "/config/raceman/cybercruise.xml")
    para = dtree.getElementsByTagName("params")
    sections = para[0].getElementsByTagName("section")

    select = None
    for s in sections:
        if s.getAttribute("name") == 'Tracks':
            select = s
            break

    select = select.getElementsByTagName("section")
    select = select[0].getElementsByTagName("attstr")

    track = select[0].getAttribute("val")
    return track

def loaddir(filepath):

    filepath += '/tracks'
    roadlist = os.listdir(filepath)

    with open('./track.txt','w+') as f:
        for i, road in enumerate(roadlist):
            roadpath = os.path.join(filepath, road)
            tracklist = os.listdir(roadpath)
            for j, track in enumerate(tracklist):
                f.writelines([track, ',', str(i), ',', str(j), '\n'])

def get_track_num(name):

    print(name)
    tracklist = []
    with open('./track.txt','r') as f:
        for line in f:
            tracklist.append(line[:-1].split(','))

    for track in tracklist:
        print(track)
        if name == track[0]:
            return int(track[1]), int(track[2])
    raise KeyError('track name not found')

#track_num('dirt-1')
#loaddir(r"D:\#作业、pre\大二下 控制导论\CyberTORCS_2022Spring_V2.0_Publish\CyberTORCS_2022Spring_V2.0_Publish\tracks")
#loadtorcs(r"D:\#作业、pre\大二下 控制导论\CyberTORCS_2022Spring_V2.0_Publish\CyberTORCS_2022Spring_V2.0_Publish")

 