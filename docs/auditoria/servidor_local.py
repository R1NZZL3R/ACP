import http.server, os, sys
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','frontend')
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p=path.split('?')[0].split('#')[0]
        if p=='/': p='/index.html'
        elif '.' not in os.path.basename(p): p=p+'.html'
        return ROOT+p
    def log_message(self,*a): pass
http.server.ThreadingHTTPServer(('127.0.0.1',8765),H).serve_forever()
