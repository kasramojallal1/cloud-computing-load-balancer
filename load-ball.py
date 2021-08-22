import http.client
import http.server
import threading
from socketserver import ThreadingMixIn

haproxy_host_port = 3001
vm_haproxy_port = 3000
host_ip = '192.168.43.26'
haproxy_ip = '192.168.143.12'

vm_states = ['on', 'off', 'off']

cpu1 = [0, 0, 0, 0]
cpu4 = [0, 0, 0, 0]
cpu5 = [0, 0, 0, 0]

memory1 = [0, 0, 0, 0]
memory4 = [0, 0, 0, 0]
memory5 = [0, 0, 0, 0]


def start_vm(vm_name):
    connection = http.client.HTTPConnection(host_ip, haproxy_host_port)
    connection.request(method='GET', url='start_vm', headers={'start_vm': vm_name})


def shutdown_vm(vm_name):
    connection = http.client.HTTPConnection(host_ip, haproxy_host_port)
    connection.request(method='GET', url='shutdown_vm', headers={'shutdown_vm': vm_name})


def get_state():
    global vm_states

    if vm_states[0] == 'on' and vm_states[1] == 'off' and vm_states[2] == 'off':
        return '100'
    elif vm_states[0] == 'on' and vm_states[1] == 'on' and vm_states[2] == 'off':
        return '110'
    elif vm_states[0] == 'on' and vm_states[1] == 'on' and vm_states[2] == 'on':
        return '111'


def haproxy_function():
    global cpu1, cpu4, cpu5
    if len(cpu1) > 15:
        temp1 = [cpu1[-4], cpu1[-3], cpu1[-2], cpu1[-1]]
        cpu1 = temp1

    if len(cpu4) > 15:
        temp4 = [cpu4[-4], cpu4[-3], cpu4[-2], cpu4[-1]]
        cpu4 = temp4

    if len(cpu5) > 15:
        temp5 = [cpu5[-4], cpu5[-3], cpu5[-2], cpu5[-1]]
        cpu5 = temp5

    print(vm_states)
    print('cpu1: ' + str(cpu1))
    print('cpu4: ' + str(cpu4))
    print('cpu5: ' + str(cpu5))

    state = get_state()
    if state == '100':
        cpu_sum = cpu1[-1] + cpu1[-2] + cpu1[-3] + cpu1[-4]
        cpu_avg = cpu_sum / 4
        print('cpu_avg: ' + str(cpu_avg))

        if cpu_avg > 80:
            vm_states[1] = 'on'
            start_vm('vm4')

    elif state == '110':
        cpu_sum = cpu1[-1] + cpu1[-2] + cpu1[-3] + cpu1[-4] + \
                  cpu4[-1] + cpu4[-2] + cpu4[-3] + cpu4[-4]

        if cpu4[-1] == 0:
            cpu_avg = cpu_sum / 4
        else:
            cpu_avg = cpu_sum / 8

        print('cpu_avg: ' + str(cpu_avg))

        if cpu_avg > 80 and cpu4[-1] != 0:
            vm_states[2] = 'on'
            start_vm('vm5')
        if cpu_avg < 40:
            vm_states[1] = 'off'
            shutdown_vm('vm4')

    elif state == '111':
        cpu_sum = cpu1[-1] + cpu1[-2] + cpu1[-3] + cpu1[-4] + \
                  cpu4[-1] + cpu4[-2] + cpu4[-3] + cpu4[-4] + \
                  cpu5[-1] + cpu5[-2] + cpu5[-3] + cpu5[-4]

        if cpu5[-1] == 0:
            cpu_avg = cpu_sum / 8
        else:
            cpu_avg = cpu_sum / 12
        print('cpu_avg: ' + str(cpu_avg))

        if cpu_avg < 50:
            vm_states[2] = 'off'
            shutdown_vm('vm5')

    threading.Timer(10.0, haproxy_function).start()


def handle_vm_info(data):
    vm_id = data[1]
    cpu_usage = data[3]
    memory_usage = data[5]

    if vm_id == '1':
        cpu1.append(int(cpu_usage))
        memory1.append(int(memory_usage))
    elif vm_id == '4':
        cpu4.append(int(cpu_usage))
        memory4.append(int(memory_usage))
    elif vm_id == '5':
        cpu5.append(int(cpu_usage))
        memory5.append(int(memory_usage))


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == 'vm_info':
            vm_info = self.headers['vm_info'].split()

            handle_vm_info(vm_info)


class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    pass


threading.Timer(0.0, haproxy_function).start()
server_address = (haproxy_ip, vm_haproxy_port)
server = ThreadedHTTPServer(server_address, Handler).serve_forever()
