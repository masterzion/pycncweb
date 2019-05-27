import configparser, json, html

import tornado.ioloop
import tornado.web
import cnc.config
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

class gcodefile(tornado.web.RequestHandler):
    def post(self):
        str=self.request.body.decode('utf-8')
        gcodetext=str.split('\n')
        print(gcodetext)
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




class resetpos(tornado.web.RequestHandler):
    def post(self):
        machine.reloadconfig()
        self.write( "ok" )

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
    (r"/reset", resetpos),
#    (r"/", LoginHandler),
    (r"/(.*)",  NoCacheStaticFileHandler, {"path": "./", "default_filename": "index.html"}),
], cookie_secret="MY_BIG_SECRET")

if __name__ == '__main__':
    application.listen(WEB_PORT)
    tornado.ioloop.IOLoop.instance().start()
