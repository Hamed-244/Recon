import socket
import whois
import re

def get_url_info(domain ):
    try :
        whois_server =  "whois.iana.org"
        sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

        sock.connect((whois_server,43))

        sock.send((domain+"\r\n").encode())

        msg = sock.recv(10000).decode()
        pattern = r'^[A-z.1-]*:'
        data = {}
        
        for line in msg.split("\n"):
            if re.findall(pattern , line):
                key , value = line.split(':',1)
                if data.get(key) :
                    last_value = [data.get(key)] if type(data.get(key)) == str  else data.get(key)
                    last_value.extend([value.strip()])
                    data[key] = last_value
                else :
                    data[key] = value.strip()

        return data
    except Exception as error:
        print('error in url info :' ,error)
        return None