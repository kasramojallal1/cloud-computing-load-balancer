import threading
import http.client
import psutil

vm_haproxy_port = 3000
haproxy_ip = '192.168.143.12'
vm_id = '5'


def send_usage_data():
    cpu_idle = psutil.cpu_times_percent(interval=1)[3]
    cpu_busy = int(100 - cpu_idle)
    memory_busy = int(psutil.virtual_memory()[2])

    vm_info = 'vm_id ' + vm_id + ' cpu ' + str(cpu_busy) + ' memory ' + str(memory_busy)
    print(vm_info)

    try:
        connection = http.client.HTTPConnection(haproxy_ip, vm_haproxy_port)
        connection.request(method='GET', url='vm_info', headers={'vm_info': vm_info})
    except:
        pass

    threading.Timer(30.0, send_usage_data).start()


threading.Timer(0.0, send_usage_data).start()
