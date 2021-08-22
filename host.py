import http.server
import subprocess
from socketserver import ThreadingMixIn

haproxy_host_port = 3001
host_ip = '192.168.43.26'


class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        if self.path == 'start_vm':
            vm_name = self.headers['start_vm']
            subprocess.call(["C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe",
                             "startvm", vm_name])

        elif self.path == "shutdown_vm":
            vm_name = self.headers['shutdown_vm']
            subprocess.call(
                ["C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe",
                 "controlvm", vm_name, "poweroff", "soft"])


class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    pass


server_address = (host_ip, haproxy_host_port)
ThreadedHTTPServer(server_address, Handler).serve_forever()
