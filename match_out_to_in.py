from os.path import join
from os import listdir
from scapy.all import *
import shutil

mypath = "/media/sf_ubuntu_sf/out_1to5Split"
write_path = "/media/sf_ubuntu_sf/Combined"
onlyfiles = [f for f in listdir(mypath) if f.endswith(".pcap")]

for pcap in onlyfiles:
    out_nat_path = join(mypath, pcap)
    out_nat_packets = sniff(offline=out_nat_path, count=1)
    out_nat = out_nat_packets[0]

    print('matching %s' % out_nat_path)
    moved = False
    for root, dirs, files in os.walk(write_path):
        for in_pcap in files:
            test_pcap_path = join(root, in_pcap)
            #nat_packets = rdpcap(test_pcap_path)
            #nat = nat_packets[0]
            nat = sniff(offline=test_pcap_path, count=1)[0]
            if 'IP' in nat and 'IP' in out_nat:
                if nat['IP'].proto == out_nat['IP'].proto and ((nat['IP'].src == out_nat['IP'].src or nat['IP'].src == out_nat['IP'].dst) or (nat['IP'].dst == out_nat['IP'].src or nat['IP'].dst == out_nat['IP'].dst)):
                    proto = nat.summary().split('/')[2].split()[0]
                    if (nat[proto].dport == out_nat[proto].dport and nat[proto].sport == out_nat[proto].sport) or (nat[proto].dport == out_nat[proto].sport and nat[proto].sport == out_nat[proto].dport):
                        shutil.move(out_nat_path, join(root, pcap))
                        print('mached %s to %s' % (pcap, root))
                        moved = True
                        break


            # if not same ip and proto
            else:
                continue


        if moved:
            break
