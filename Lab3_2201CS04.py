from scapy.all import *
import time
import statistics

def ping(dest_ip, count=4, ttl=64, packet_size=64, timeout=2):
    try:
        # Validate the destination IP
        socket.inet_aton(dest_ip)
    except socket.error:
        print(f"Invalid destination IP address: {dest_ip}")
        return
    
    # Initialize variables for tracking statistics
    rtts = []
    sent_packets = 0
    received_packets = 0

    for i in range(count):
        # Create an ICMP packet with the given TTL and packet size
        packet = IP(dst=dest_ip, ttl=ttl) / ICMP() / (b'X' * packet_size)
        sent_time = time.time()

        try:
            # Send the packet and wait for a response
            response = sr1(packet, timeout=timeout, verbose=0)
            sent_packets += 1

            if response:
                received_time = time.time()
                rtt = (received_time - sent_time) * 1000  # RTT in milliseconds
                rtts.append(rtt)
                print(f"Reply from {response.src}: bytes={packet_size} time={rtt:.2f}ms TTL={response.ttl}")
                received_packets += 1
            else:
                print(f"Request timed out.")
        
        except Exception as e:
            print(f"Error sending packet: {e}")
            continue
    
    # Calculate statistics
    if rtts:
        packet_loss = ((sent_packets - received_packets) / sent_packets) * 100
        avg_rtt = statistics.mean(rtts)
        max_rtt = max(rtts)
        min_rtt = min(rtts)
        print(f"\n--- {dest_ip} ping statistics ---")
        print(f"{sent_packets} packets transmitted, {received_packets} received, {packet_loss:.1f}% packet loss")
        print(f"rtt min/avg/max = {min_rtt:.2f}/{avg_rtt:.2f}/{max_rtt:.2f} ms")
    else:
        print(f"\nNo response received from {dest_ip}.")

if __name__ == "__main__":
    # Example usage:
    ping(dest_ip="8.8.8.8", count=5, ttl=64, packet_size=100, timeout=2)
