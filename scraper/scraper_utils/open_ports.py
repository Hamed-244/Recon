import socket

def port_scanner (domain) :
    try :
        ports = []
        ipAddres = socket.gethostbyname(domain)
        common_ports = [21, 22, 23, 25, 53, 80, 110, 119, 123, 143, 161, 194, 443, 445, 993, 995]

        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ipAddres, port))
            sock.close()
            if result == 0:
                ports.append(port)

        return ports
    except Exception as error:
        print('error in port scanner :' ,error)
        return []