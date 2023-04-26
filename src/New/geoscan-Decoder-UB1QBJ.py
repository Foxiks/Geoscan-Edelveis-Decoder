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
        img_sync = frame[:8]
        if(int(str(frame.find('ffd8'))) >= int(0)):
            reg=4
            name=str(time.strftime("%m-%d_%H-%M"))
            with open('out_iamge_'+str(name)+'.jpg', 'ab') as out_file:
                bitstring.BitArray(hex=str(frame[16:])).tofile(out_file)
            with open('data.ts', 'w') as o:
                o.write('out_iamge_'+str(name)+'.jpg')
        if(str(img_sync) == str('01003e05')):    
            chb1=frame[12:14]
            chb2=frame[10:12]
            check_value=bitstring.BitStream(hex=str(str(chb1)+str(chb2))).read('uint')
            if(int(check_value)==int(reg+56)):
                with open('out_iamge_'+str(name)+'.jpg', 'ab') as out_file:
                    bitstring.BitArray(hex=str(frame[16:])).tofile(out_file)
                reg+=56
            else:
                skipped=int(check_value-reg)/56
                with open('out_iamge_'+str(name)+'.jpg', 'ab') as out_file:
                    bitstring.BitArray(hex=str(str('0'*112)*int(skipped))).tofile(out_file)
                reg+=int(56*int(skipped))
        if(int(str(frame.find('ffd9'))) >= int(0)):
            with open('out_iamge_'+str(name)+'.jpg', 'ab') as out_file:
                bitstring.BitArray(hex=str(frame[16:])).tofile(out_file)

if(__name__=='__main__'):
    ip=parser.parse_args().ip
    port=parser.parse_args().port
    reg=0
    name=str(time.strftime("%m-%d_%H-%M"))
    s=start_socket(ip=ip, port=int(port))
    agw_connect(s=s)
    main(s=s)