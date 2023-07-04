from multiprocessing import Process, Queue
from bluepy.btle import Scanner, DefaultDelegate

from config import devices

class ScanDelegate(DefaultDelegate):
    def __init__(self, data_queue):
        DefaultDelegate.__init__(self)
        self.data_queue = data_queue

    def handleDiscovery(self, dev, is_new_device, is_new_data):
        self.data_queue.put((dev))

def _target(data_queue):
    scanner = Scanner().withDelegate(ScanDelegate(data_queue))
    while True:
        scanner.scan(3600)

def start_process():
    data_queue = Queue()
    process = Process(target=_target, args=(data_queue,))
    process.start()
    return process, data_queue