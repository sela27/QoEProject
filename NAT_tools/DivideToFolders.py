from scapy.all import *
from os import listdir, makedirs
from os.path import isfile, join, exists
import shutil

mypath = "/media/sf_ubuntu_sf/1to5Split"
onlyfiles = [f for f in listdir(mypath) if f.endswith(".pcap")]


for pcap in onlyfiles:
    ips = set((p[IP].src, p[IP].dst) for p in PcapReader(pcap) if IP in p)
    if len(list(ips)) != 0:
        ip = list(ips)[0][0]
        if not ip.startswith("10.42.0"):
            ip = list(ips)[0][1]
    else:
        continue
    base_path = "/media/sf_ubuntu_sf/1to5Split"
    path = join(base_path,ip)
    if not exists(path):
        makedirs(path)
        print("created folder %s" % path)
    fullpath = join(base_path,pcap)
    newpath = join(path,pcap)
    shutil.move(fullpath,newpath)
    print("move file %s to %s" % (pcap, newpath))
