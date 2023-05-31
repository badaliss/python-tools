# !/usr/bin/env python
import argparse
import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    # scapy.ls(scapy.ARP()) - to see the fields for ip and mac
    arp_request_broadcast = broadcast/arp_request
    answered_lst = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for i in answered_lst:
        client_dict = {'ip': i[1].psrc, 'mac': i[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='target', help='Target network for scanning')
    options = parser.parse_args()
    if not options.target:
        parser.error('[-] Pls enter option -t with target IP / IP range')
    return options


def print_result(result_list):
    print('IP\t\t\tMAC address\n------------------------------------------------')
    for i in result_list:
        print(i['ip'] + '\t\t' + i['mac'])


option = get_arguments()
scan_result = scan(option.target)
print_result(scan_result)
