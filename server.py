import configparser, json, html

import tornado.ioloop
import tornado.web
import cnc.config
import _thread
import cnc.logging_config as logging_config
from cnc.gcode import GCode, GCodeException
from cnc.gmachine import GMachine, GMachineException

logging_config.debug_enable()

WEB_PORT=8080

configFilePath = '/etc/pycnc.conf'
configvars = 'js/config.json'

gcodetext=[]
gcodeindex=0

machine = GMachine()
cancelprint = False;
isprinting = False;

def do_line(line):
    try:
        g = GCode.parse_line(line)
        res = machine.do_command(g)
    except (GCodeException, GMachineException) as e:
        return 'ERROR ' + str(e)
    if res is not None:
        return 'OK ' + res
    else:
        return 'OK'
    return True

def PrintFile():
    global isprinting
    global cancelprint
    global gcodeindex
    global gcodetext

    isprinting = True
    cancelprint = False
    print("printing "+ str(len(gcodetext)) + " lines" )
    logging_config.debug_disable()
    for line in gcodetext:
        print('line'+str(gcodeindex))
        if cancelprint:
            isprinting = False
            break;
        gcodeindex+=1
        do_line(line)
    logging_config.debug_enable()

class gcodefile(tornado.web.RequestHandler):
    def post(self):
        global gcodeindex
        global gcodetext
        gcodeindex=0
        str=self.request.body.decode('utf-8')
        gcodetext=str.split('\n')
#        print(gcodetext)
        self.write( 'ok' )

class config(tornado.web.RequestHandler):
    def get(self):

#        for item in configParser.sections():
#            print(configParser[item])
#            json_data[item] = configParser[item]
        json_data = []
        with open(configvars) as json_file:
            json_data = json.load(json_file)

        self.set_header('Content-type','application/json')
        configParser = configparser.RawConfigParser()
        configParser.read(configFilePath)
        for value in json_data:
            for item in json_data[value]:
    #            print(value+' '+ item + ' :'+json_data[value][item])
                if json_data[value][item] == 'int':
                    json_data[value][item] = configParser.getint(value, item)
                else:
                    json_data[value][item] = configParser.getboolean(value, item)
#        print(json_data)
        self.write( json_data  )

    def post(self):
        config = configparser.ConfigParser()
        json_data = json.loads(self.request.body)
        for value in json_data:
            config[value] = json_data[value]
        with open(configFilePath, 'w') as configfile:
            config.write(configfile)
        machine.reloadconfig()
        self.write( 'ok' )

class gcodeaction(tornado.web.RequestHandler):
    def post(self):
        global isprinting
        global cancelprint
        global gcodeindex
        global gcodetext

        action = str(self.request.body, 'utf8')
        res=""
        print(action)
        if action == "pause":
            if isprinting:
                cancelprint = True
                res="OK"
            else:
                res="ERROR: not printing"
        elif action == "stop":
            cancelprint = True
            gcodeindex = 0
            res="OK"
        elif action == "play":
            if isprinting:
                res="ERROR: is already printing"
            else:
                self.thread = _thread.start_new_thread(PrintFile, () )
                self.write( "ok" )
        elif action == "reset":
            if isprinting:
                res='ERROR: Printing'
            else:
                machine.reloadconfig()
                res="ok"
        self.write( res )

class positions(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-type','application/json')
        coord=machine.coordinates()
        obj={
            "X" : coord[0],
            "Y" : coord[1],
            "Z" : coord[2],
            "E" : coord[3],
            "gcodeindex" : (gcodeindex+0)
        }
#        print (obj);
        self.write( json.dumps( obj ) )

    def post(self):
        if not isprinting:
            config = configparser.ConfigParser()
            json_data = json.loads(self.request.body)
            line="G1"
            print(json_data)
            if 'add' in json_data:
                coord=machine.coordinates()
                for key, val in enumerate(['X', 'Y', 'Z', 'E']):
                    if val in json_data['add']:
                        line+=" "+val+str(coord[key]+json_data['add'][val])
            else:
                for key, val in enumerate(json_data['pos']):
                    line+=" "+val+str(json_data['pos'][val])
            do_line(line)
            self.write( 'ok' )
        else:
            self.write( 'ERROR: Printing' )

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
      self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


application = tornado.web.Application([
    (r"/config", config),
    (r"/gcodefile", gcodefile),
    (r"/positions", positions),
    (r"/gcodeaction", gcodeaction),
#    (r"/", LoginHandler),
    (r"/(.*)",  NoCacheStaticFileHandler, {"path": "./", "default_filename": "index.html"}),
], cookie_secret="MY_BIG_SECRET")

if __name__ == '__main__':
    application.listen(WEB_PORT)
    tornado.ioloop.IOLoop.instance().start()
