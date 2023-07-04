from multiprocessing import Process
from threading import Timer

from bluepy.btle import ScanEntry

AD_TP_DATA = 0x3A

class Device:
    def __init__(self, addr, timeout=120):
        self.addr = addr
        self.active = True
        self._timeout = timeout
        self._expired_callback = expired_callback

        self._timer = None
        self.renew()

    def _expiry(self):
        print(f"Device with address {self.addr} has expired!")
        self.active = False

    def renew(self):
        self.active = True
        if self._timer is not None:
            self._timer.cancel()
        self._timer = Timer(self._timeout, self._expiry)
        self._timer.start()

    def __repr__(self):
        return f"[addr={self.addr}, active={self.active}]"

found_devices = {}
def start(data_queue):
    while True:
        dev = data_queue.get()
        if dev.addr not in found_devices:
            print(f" --- Found new device {dev.addr}, rssi {dev.rssi}")
            
            found_devices[dev.addr] = Device(dev.addr)
        else:
            found_devices[dev.addr].renew()
