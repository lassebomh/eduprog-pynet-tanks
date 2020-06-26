#
#  Creating id's for tanks on the LAN.
#
#  Limits:
#
#    Your IP can range from 192.168.0.0 to 192.168.255.255
#
#    Your Tank ID can range from 0 to 24 (including 0 and 24)
#
#  Examples:
#
#    1.  IP 192.168.255.255, TANK 24      =  Z473
#
#    2.  IP 192.168.1.1, TANK 0           =  0075
#
#    3.  IP 192.168.2.235, TANK 10        =  E297
#
#  Usage example at the bottom...
#

from baseconvert import base

def basep(*args, pad=0, **kwargs):       #  Converts base AND pads the result with
    out = base(*args, **kwargs)          #  zeroes (on the left side of the number).
    return "0"*(pad-len(out))+out

def getid(ip, tank):
    ip1, ip2 = map(int, ip.split('.')[2:])

    return basep(
              basep(tank, 10, 16, string=True, pad=2) +
              basep(ip1, 10, 16, string=True, pad=2) +
              basep(ip2, 10, 16, string=True, pad=2)
                 , 16, 36, string=True, pad=4)

def fromid(id):
    out = basep(id, 36, 16, string=True, pad=6)
    result = tuple(map(lambda x: "".join(map(lambda y: str(y), base(x, 16, 10, string=True))), (out[2:4], out[4:6], out[0:2])))
    return ('192.168.'+result[0]+"."+result[1], int(result[2]))

if __name__ == "__main__":

    from random import randint

    # Usage example
    print("getid:\t", getid(ip="192.168.1.235", tank=8))

    print("fromid:\t", fromid("Z4EX"))
