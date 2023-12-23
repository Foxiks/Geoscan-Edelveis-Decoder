import sys, socket, argparse, time, bitstring
from datetime import datetime

name=str(time.strftime("%m-%d_%H-%M"))
reg=0

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

def telemetry_decoder(data):
    data=data[32:]
    time_unix=datetime.utcfromtimestamp(int(bitstring.BitStream(hex=data[:8]).read('uintle'))).strftime('%Y-%m-%d %H:%M:%S')
    current=int(bitstring.BitStream(hex=data[8:12]).read('uintle'))*0.0000766
    current_pannels=int(bitstring.BitStream(hex=data[12:16]).read('uintle'))*0.00003076
    v_oneakb=int(bitstring.BitStream(hex=data[16:20]).read('uintle'))*0.00006928
    v_akball=int(bitstring.BitStream(hex=data[20:24]).read('uintle'))*0.00013856
    t_x_p=bitstring.BitStream(hex=data[24:26]).read('int')
    t_x_n=bitstring.BitStream(hex=data[26:28]).read('int')
    t_y_p=bitstring.BitStream(hex=data[28:30]).read('int')
    t_y_n=bitstring.BitStream(hex=data[30:32]).read('int')
    #t_z_p=bitstring.BitStream(hex=data[32:34]).read('int')
    t_z_n=bitstring.BitStream(hex=data[34:36]).read('int')
    t_bat1=bitstring.BitStream(hex=data[36:38]).read('int')
    t_bat2=bitstring.BitStream(hex=data[38:40]).read('int')
    cpu=bitstring.BitStream(hex=data[40:42]).read('int')*0.390625
    obc=int(bitstring.BitStream(hex=data[42:46]).read('intle'))-7476
    commu=int(bitstring.BitStream(hex=data[46:50]).read('intle'))-1505
    rssi=int(bitstring.BitStream(hex=data[50:52]).read('int'))-99
    with open('tlm.txt', 'w') as out_tlm_file:
        out_tlm_file.write(str(time_unix)+'\n')
        out_tlm_file.write(str(round(float(current), 2))+' A'+'\n')
        out_tlm_file.write(str(round(float(current_pannels), 2))+' A'+'\n')
        out_tlm_file.write(str(round(float(v_oneakb), 2))+' V'+'\n')
        out_tlm_file.write(str(round(float(v_akball), 2))+' V'+'\n')
        out_tlm_file.write(str(t_x_p)+' C'+'\n')
        out_tlm_file.write(str(t_x_n)+' C'+'\n')
        out_tlm_file.write(str(t_y_p)+' C'+'\n')
        out_tlm_file.write(str(t_y_n)+' C'+'\n')
        out_tlm_file.write(str('NONE')+'\n')
        out_tlm_file.write(str(t_z_n)+' C'+'\n')
        out_tlm_file.write(str(t_bat1)+' C'+'\n')
        out_tlm_file.write(str(t_bat2)+' C'+'\n')
        out_tlm_file.write(str(round(float(cpu), 2))+'%'+'\n')
        out_tlm_file.write(str(obc)+'\n')
        out_tlm_file.write(str(commu)+'\n')
        out_tlm_file.write(str(rssi)+'\n')

def main(s):
    global reg, name
    while True:
        frame = s.recv(2048).hex()
        frame = frame[74:]
        reply = [frame[i:i+2] for i in range(0, len(frame), 2)]
        frame = ' '.join(reply)
        img_sync = frame[:11]
        if(int(str(frame.find(' ff d8 ff db '))) >= int(0)):
            chb1=frame[21:23]
            chb2=frame[18:20]
            chb3=frame[15:17]
            reg=bitstring.BitStream(hex=str(str(chb1)+str(chb2)+str(chb3))).read('uint')
            name=str(time.strftime("%m-%d_%H-%M-%S"))
            x=int(str(frame[23:].find(' ff d8 ')))
            with open('out_image_'+str(name)+'.jpg', 'ab') as out_file:
                bitstring.BitArray(hex=str(str(frame[23+x:]).replace(' ', ''))).tofile(out_file)
            with open('data.ts', 'w') as o:
                o.write('out_image_'+str(name)+'.jpg')
        if(str(img_sync) == str('01 00 3e 05')):    
            chb1=frame[21:23]
            chb2=frame[18:20]
            chb3=frame[15:17]
            check_value=bitstring.BitStream(hex=str(str(chb1)+str(chb2)+str(chb3))).read('uint')
            if(int(check_value)==int(reg+56)):
                with open('out_image_'+str(name)+'.jpg', 'ab') as out_file:
                    bitstring.BitArray(hex=str(str(frame[23:]).replace(' ', ''))).tofile(out_file)
                reg+=56
            else:
                skipped=int(check_value-reg)/56
                lenz=112*int(skipped)
                if(lenz == 224):
                    lenz = 112
                with open('out_image_'+str(name)+'.jpg', 'ab') as out_file:
                    bitstring.BitArray(hex=str(str('0'*lenz))).tofile(out_file)
                    bitstring.BitArray(hex=str(str(frame[23:]).replace(' ', ''))).tofile(out_file)
                reg+=int(56*int(skipped))
        if(int(str(frame[23:].find(' ff d9 '))) >= int(0)):
            with open('out_image_'+str(name)+'.jpg', 'ab') as out_file:
                bitstring.BitArray(hex=str(str(frame[23:]).replace(' ', ''))).tofile(out_file)
        if(str(frame[:18]) == str('84 8a 82 86 9e 9c ')):
            telemetry_decoder(data=str(str(frame).replace(' ', '')))

if(__name__=='__main__'):
    ip=parser.parse_args().ip
    port=parser.parse_args().port
    s=start_socket(ip=ip, port=int(port))
    agw_connect(s=s)
    main(s=s)