
from baseconvert import base
import socket
from flask import Flask, send_file
import logging

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

if __name__ != "__main__":
    import __main__

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 80))
    localip = s.getsockname()[0]
    s.close()

    tankid = getid(localip, 0)

    # Flask stuff
    app = Flask(__name__, static_url_path='')
    
    @app.route('/')
    @app.route('/<file>')
    def handle(file=None):
        try:
            if file == None: file = "index.html"
            with open("./www/"+file, "r") as f:
                return f.read()
        except FileNotFoundError:
            return '<p>Error 404</p><a href=\"/\">Go back to Home?</a>', 404

    def begin():
        __main__.loop()
        __main__.gunLoop()

        print()
        print("====================================================================\n")
        print(" TANK:"+str(tankid), "is now fired up!  Go to", "http://localhost:5000", 'to battle!', '\n')
        print("====================================================================\n")
        
        app.run()


else:
    print("\nNotice! Please run this by importing the module, inside tank code")
