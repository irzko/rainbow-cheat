import android_device_controller as adc
import time
import random
import string


# define funtion random name
def random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))




devices = adc.get_connected_devices()
controller = adc.DeviceController(devices[0])

# Dropdown
def run():
    devices[0].tap_screen(305,231)
    time.sleep(1)

    # Tap "Add anther wallet"
    devices[0].tap_screen(117,867)

    time.sleep(1)
    devices[0].tap_screen(86,275)

    time.sleep(1)
    devices[0].input_text(random_string(15))

    time.sleep(1)
    devices[0].tap_screen(267,340)

    time.sleep(1)
    devices[0].tap_screen(276,626)
    devices[0].tap_screen(269,920)
    devices[0].tap_screen(269,920)
    devices[0].tap_screen(125,628)

    time.sleep(6)
    devices[0].tap_screen(469,886)



    time.sleep(1)
    devices[0].tap_screen(272,730)

    time.sleep(1)
    devices[0].input_text("2GV-PCU")

    time.sleep(2)
    devices[0].tap_screen(271,721)


    # ----------------- 2 -----------------

    # [bỏ]
    # time.sleep(1)
    # devices[0].tap_screen(279,544)

    time.sleep(4)
    devices[0].tap_screen(262,867)

    time.sleep(1)
    devices[0].tap_screen(276,626)
    devices[0].tap_screen(269,920)
    devices[0].tap_screen(269,920)
    devices[0].tap_screen(125,628)

    time.sleep(20)
    devices[0].tap_screen(263,866)

    time.sleep(3)
    devices[0].swipe(265, 233, 265, 750, 500)

    time.sleep(1)
    devices[0].tap_screen(73, 883)


for i in range(2):
    run()
    print(i)
    time.sleep(1)
