import ipaddress

def ip_range_to_subnet(ip_range):
    # Phân tách chuỗi đầu vào thành địa chỉ IP bắt đầu và kết thúc
    start_ip, end_ip = ip_range.split('-')
    start = ipaddress.IPv4Address(start_ip.strip())
    end = ipaddress.IPv4Address(end_ip.strip())
    num_ips = int(end) - int(start) + 1
    
    # Tìm prefix length
    prefix_length = 32
    while num_ips != 0:
        num_ips >>= 1
        prefix_length -= 1
    
    # Tạo subnet
    network = ipaddress.IPv4Network(f"{start_ip}/{prefix_length}", strict=False)
    
    # Điều chỉnh subnet để đảm bảo nó bao gồm cả dải IP
    while not (int(network.network_address) <= int(start) and int(network.broadcast_address) >= int(end)):
        prefix_length -= 1
        network = ipaddress.IPv4Network(f"{start_ip}/{prefix_length}", strict=False)
    
    return str(network)

# Nhập dải IP dưới dạng chuỗi
ip_range_input = "192.168.1.64-192.168.1.127"
subnet = ip_range_to_subnet(ip_range_input)
print(f"Subnet tương ứng: {subnet}")
