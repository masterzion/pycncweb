
import tornado.ioloop
import tornado.web

import configparser, json, html

WEB_PORT=8080

configFilePath = '/etc/pycnc.conf'
configvars = 'js/config.json'



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
        self.write( 'ok' )

'''
configParser = configparser.RawConfigParser()
configParser.read(configFilePath)
machine.coordinates()

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
'''


class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
      self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


application = tornado.web.Application([
    (r"/config", config),
#    (r"/", LoginHandler),
    (r"/(.*)",  NoCacheStaticFileHandler, {"path": "./", "default_filename": "index.html"}),
], cookie_secret="MY_BIG_SECRET")

if __name__ == '__main__':
    application.listen(WEB_PORT)
    tornado.ioloop.IOLoop.instance().start()
