import usb.core
import time


def get_usb_devices():
    devices = usb.core.find(find_all=True)
    usb_set = set()

    for dev in devices:
        usb_set.add((dev.idVendor, dev.idProduct))
    return usb_set

old_devices = get_usb_devices()

while True:
    time.sleep(3)

    new_devices = get_usb_devices()

    added = new_devices - old_devices
    removed = old_devices - new_devices

    for dev in added:
        print(f"USB added: Vendor={hex(dev[0])}, Product={hex(dev[1])}")

    for dev in removed:
        print(f"USB removed: Vendor={hex(dev[0])}, Product={hex(dev[1])}")

    old_devices = new_devices
