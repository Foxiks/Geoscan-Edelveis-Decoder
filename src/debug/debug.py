import sys, socket, argparse, time, bitstring

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port")
parser.add_argument("-ip", "--ip", help="ip")

def agw_connect(s):
    s.send(b'\x00\x00\x00\x00k\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    return

def start_socket(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        time.sleep(5)
        sys.exit()
    host = str(ip)
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        time.sleep(5)
        sys.exit()
    s.connect((remote_ip , port))
    print('Connected to ' + str(remote_ip) + ":" + str(port))
    print("")
    return s

def main(s):
    while True:
        frame = s.recv(1024).hex()
        frame = frame[74:]
        reply = [frame[i:i+2] for i in range(0, len(frame), 2)]
        frame = ' '.join(reply)
        with open('debug'+str(name)+'.bin', 'ab') as out_file:
            bitstring.BitArray(hex=str(frame).replace(' ', '')).tofile(out_file)
        with open('debug'+str(name)+'.txt', 'a') as out_file1:
            out_file1.write(str(frame)+'\n')

if(__name__=='__main__'):
    ip=parser.parse_args().ip
    port=parser.parse_args().port
    reg=0
    name=str(time.strftime("%m-%d_%H-%M"))
    s=start_socket(ip=ip, port=int(port))
    agw_connect(s=s)
    main(s=s)
