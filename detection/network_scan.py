"""
Simple pcap analyzer to detect periodic small POST requests.
Requires scapy or pyshark. Placeholder with scapy.
"""
from scapy.all import rdpcap, TCP, IP, Raw

def find_exfil_beacons(pcap_file, interval=30, min_size=20):
    beacons = []
    packets = rdpcap(pcap_file)
    post_times = []
    for pkt in packets:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            load = pkt[Raw].load.decode(errors='ignore')
            if "POST" in load and len(load) > min_size:
                post_times.append(pkt.time)
    # Simple time delta analysis
    for i in range(1, len(post_times)):
        delta = post_times[i] - post_times[i-1]
        if abs(delta - interval) < 5:   # within 5s of expected interval
            beacons.append(f"Beacon detected at {post_times[i]} (delta {delta:.2f}s)")
    return beacons