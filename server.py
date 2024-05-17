#!python

import urllib.parse
import urllib.request
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import sites
import json


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass


PORT_NUMBER = 9137


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        args = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "url" in args:
            domain = args['url'][0]
            url = "https://" + domain
            start = time.time()
            try:
                urllib.request.urlopen(url, timeout=100).read()
            except Exception as e:
                if "CERTIFICATE" not in str(e) and "Forbidden" not in str(e):
                    return
            end = time.time()
            if end - start > 100.0:
                return
            text = "%.2f" % (end - start)
            loading_time = text.encode('ascii')
            print("Loaded " + url + " in " + str(loading_time))
            self.wfile.write(loading_time)
        elif self.path.endswith("sites"):
            dump = json.dumps(sites.sites)
            converted = dump.encode('ascii')
            self.wfile.write(converted)
        else:
            with open("index.html") as fin:
                s1 = fin.read()
                s2 = s1.encode('ascii')
                self.wfile.write(s2)
        # return


try:
    server = ThreadingServer(('', PORT_NUMBER), RequestHandler)
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
