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
gindex=0

machine = GMachine()
cancelprint = False;

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

class gcodeindex(tornado.web.RequestHandler):
    def get(self):
        self.write( str( gindex ) )


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



class reset(tornado.web.RequestHandler):
    def get(self):
        machine.reset()
        self.write( 'ok' )

class coordinates(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-type','application/json')
        coord=machine.coordinates()
        obj={
            "x" : coord[0],
            "y" : coord[1],
            "z" : coord[2],
            "e" : coord[3]
        }
#        print (obj);
        self.write( json.dumps( obj ) )

    def post(self):
        config = configparser.ConfigParser()
        json_data = json.loads(self.request.body)
        do_line("x"+str(json_data.x)+" y"+str(json_data.y)+" z"+str(json_data.z))
        self.write( 'ok' )


class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
      self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


application = tornado.web.Application([
    (r"/config", config),
    (r"/gcodefile", gcodefile),
    (r"/gcodeindex", gcodeindex),
    (r"/coordinates", coordinates),
#    (r"/", LoginHandler),
    (r"/(.*)",  NoCacheStaticFileHandler, {"path": "./", "default_filename": "index.html"}),
], cookie_secret="MY_BIG_SECRET")

if __name__ == '__main__':
    application.listen(WEB_PORT)
    tornado.ioloop.IOLoop.instance().start()
