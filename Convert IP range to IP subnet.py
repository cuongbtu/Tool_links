import ipaddress

def ip_range_to_subnet(ip_range):
    start_ip, end_ip = ip_range.split('-')
    start = ipaddress.IPv4Address(start_ip.strip())
    end = ipaddress.IPv4Address(end_ip.strip())
    num_ips = int(end) - int(start) + 1
    
    prefix_length = 32
    while num_ips != 0:
        num_ips >>= 1
        prefix_length -= 1
    
    network = ipaddress.IPv4Network(f"{start_ip}/{prefix_length}", strict=False)
    
    while not (int(network.network_address) <= int(start) and int(network.broadcast_address) >= int(end)):
        prefix_length -= 1
        network = ipaddress.IPv4Network(f"{start_ip}/{prefix_length}", strict=False)
    
    return str(network)

def process_ip_ranges(file_path):
    with open(file_path, 'r') as file:
        ip_ranges = file.readlines()
    
    subnets = [ip_range_to_subnet(ip_range.strip()) for ip_range in ip_ranges]
    
    return subnets

# Thay đổi 'ip_ranges.txt' bằng đường dẫn đến file của bạn
file_path = 'ip_ranges.txt'
subnets = process_ip_ranges(file_path)

# In ra hoặc lưu kết quả
for subnet in subnets:
    print(subnet)

# Nếu bạn muốn lưu kết quả vào một file
with open('subnets_output.txt', 'w') as output_file:
    for subnet in subnets:
        output_file.write(subnet + '\n')
