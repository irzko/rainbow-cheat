import cv2
import os
import re
import subprocess
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


class KeyEvent:
    KEYCODE_UNKNOWN = 0
    KEYCODE_SOFT_LEFT = 1
    KEYCODE_SOFT_RIGHT = 2
    KEYCODE_HOME = 3
    KEYCODE_BACK = 4
    KEYCODE_CALL = 5
    KEYCODE_ENDCALL = 6
    KEYCODE_0 = 7
    KEYCODE_1 = 8
    KEYCODE_2 = 9
    KEYCODE_3 = 10
    KEYCODE_4 = 11
    KEYCODE_5 = 12
    KEYCODE_6 = 13
    KEYCODE_7 = 14
    KEYCODE_8 = 15
    KEYCODE_9 = 16
    KEYCODE_STAR = 17
    KEYCODE_POUND = 18
    KEYCODE_DPAD_UP = 19
    KEYCODE_DPAD_DOWN = 20
    KEYCODE_DPAD_LEFT = 21
    KEYCODE_DPAD_RIGHT = 22
    KEYCODE_DPAD_CENTER = 23
    KEYCODE_VOLUME_UP = 24
    KEYCODE_VOLUME_DOWN = 25
    KEYCODE_POWER = 26
    KEYCODE_CAMERA = 27
    KEYCODE_CLEAR = 28
    KEYCODE_A = 29
    KEYCODE_B = 30
    KEYCODE_C = 31
    KEYCODE_D = 32
    KEYCODE_E = 33
    KEYCODE_F = 34
    KEYCODE_G = 35
    KEYCODE_H = 36
    KEYCODE_I = 37
    KEYCODE_J = 38
    KEYCODE_K = 39
    KEYCODE_L = 40
    KEYCODE_M = 41
    KEYCODE_N = 42
    KEYCODE_O = 43
    KEYCODE_P = 44
    KEYCODE_Q = 45
    KEYCODE_R = 46
    KEYCODE_S = 47
    KEYCODE_T = 48
    KEYCODE_U = 49
    KEYCODE_V = 50
    KEYCODE_W = 51
    KEYCODE_X = 52
    KEYCODE_Y = 53
    KEYCODE_Z = 54
    KEYCODE_COMMA = 55
    KEYCODE_PERIOD = 56
    KEYCODE_ALT_LEFT = 57
    KEYCODE_ALT_RIGHT = 58
    KEYCODE_SHIFT_LEFT = 59
    KEYCODE_SHIFT_RIGHT = 60
    KEYCODE_TAB = 61
    KEYCODE_SPACE = 62
    KEYCODE_SYM = 63
    KEYCODE_EXPLORER = 64
    KEYCODE_ENVELOPE = 65
    KEYCODE_ENTER = 66
    KEYCODE_DEL = 67
    KEYCODE_GRAVE = 68
    KEYCODE_MINUS = 69
    KEYCODE_EQUALS = 70
    KEYCODE_LEFT_BRACKET = 71
    KEYCODE_RIGHT_BRACKET = 72
    KEYCODE_BACKSLASH = 73
    KEYCODE_SEMICOLON = 74
    KEYCODE_APOSTROPHE = 75
    KEYCODE_SLASH = 76
    KEYCODE_AT = 77
    KEYCODE_NUM = 78
    KEYCODE_HEADSETHOOK = 79
    KEYCODE_FOCUS = 80
    KEYCODE_PLUS = 81
    KEYCODE_MENU = 82
    KEYCODE_NOTIFICATION = 83
    KEYCODE_APP_SWITCH = 187


def find_out_point(image, template):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
    (startX, startY) = maxLoc
    end_x = startX + template.shape[1]
    end_y = startY + template.shape[0]
    return Point((startX + end_x) / 2, (startY + end_y) / 2)


def run_command(cmd: str) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout


def get_connected_devices():
    try:
        result = subprocess.check_output(["adb", "devices"]).decode("utf-8")
        lines = result.strip().split('\n')
        # devices = [line.split('\t')[0] for line in lines[1:] if line.endswith('\tdevice')]
        devices: list[DeviceController] = []
        for line in lines[1:]:
            if line.endswith('\tdevice'):
                devices.append(DeviceController(line.split('\t')[0]))
        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []
    



class DeviceController:
    SWIPE_DEVICES = "adb -s {0} shell input swipe {1} {2} {3} {4} {5}"
    GET_SCREEN_RESOLUTION = 'adb -s {0} shell dumpsys display | Find \"mCurrentDisplayRect\"'
    TAP_DEVICES = "adb -s {0} shell input tap {1} {2}"
    SWIPE_DEVICES = "adb -s {0} shell input swipe {1} {2} {3} {4} {5}"
    KEY_DEVICES = "adb -s {0} shell input keyevent {1}"
    INPUT_TEXT_DEVICES = "adb -s {0} shell input text \"{1}\""
    LIST_INSTALLED_PACKAGES = "adb -s {0} shell pm list packages -f"
    OPEN_APP = "adb -s {0} shell monkey -p {1}"


    def __init__(self, device):
        self.device = device

    def long_press(self, x, y, duration=100):
        run_command(DeviceController.SWIPE_DEVICES.format(self.device, x, y, x, y, duration))

    def open_app(self, package_name):
        run_command(DeviceController.OPEN_APP.format(self.device, package_name))


    def list_installed_packages(self):
        try:
            result = run_command(DeviceController.LIST_INSTALLED_PACKAGES.format(self.device))
            packages = result.strip().split('\n')
            # Lọc ra tên gói ứng dụng
            package_names = []
            for package in packages:
                match = re.search(r'(.*)/(.*)\.apk=(.*)', package)
                if match:
                    package_names.append({'package_name': match.group(3), 'apk_name': match.group(2) + '.apk'})

            return package_names
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return []

    def tap_by_percent(self, x, y, count=1):
        resolution = DeviceController.getScreenResolution(self.device)
        num = int(x * (resolution.x * 1.0 / 100.0))
        num2 = int(y * (resolution.y * 1.0 / 100.0))
        text = DeviceController.TAP_DEVICES.format(self.device, num, num2)
        for i in range(count):
            text = text + " && " + DeviceController.TAP_DEVICES.format(self.device, x, y)
        run_command(text)

    def get_screen_size(self):
        cmd = DeviceController.GET_SCREEN_RESOLUTION.format(self.device)
        text = run_command(cmd)
        text = text[text.index("- "):]
        text = text[text.index(' '): text.index(')')]
        array = text.split(',')
        x = array[0].strip()
        y = array[1].strip()
        return Point(x, y)

    def tap_screen(self, x, y):
        try:
            run_command(DeviceController.TAP_DEVICES.format(self.device, x, y))
            print(f"Tapped at ({x}, {y}) on the screen.")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def swipe(self, x1, y1, x2, y2, duration=100):
        cmd_command = DeviceController.SWIPE_DEVICES.format(
            self.device,
            x1,
            y1,
            x2,
            y2,
            duration)
        run_command(cmd_command)

    def swipe_by_percent(self, x1, y1, x2, y2, duration=100):
        screen_resolution = self.getScreenResolution()
        num = int(x1 * (screen_resolution.x * 1.0 / 100.0))
        num2 = int(y1 * (screen_resolution.y * 1.0 / 100.0))
        num3 = int(x2 * (screen_resolution.x * 1.0 / 100.0))
        num4 = int(y2 * (screen_resolution.y * 1.0 / 100.0))
        cmd_command = DeviceController.SWIPE_DEVICES.format(self.device, num, num2, num3, num4, duration)
        run_command(cmd_command)

    def key(self, key):
        run_command(DeviceController.KEY_DEVICES.format(self.device, key))

    def input_text(self, text):
        cmd_command = DeviceController.INPUT_TEXT_DEVICES.format(self.device, text
                                                      .replace(" ", "%s")
                                                      .replace("&", "\\&")
                                                      .replace("<", "\\<")
                                                      .replace(">", "\\>")
                                                      .replace("?", "\\?")
                                                      .replace(":", "\\:")
                                                      .replace("{", "\\{")
                                                      .replace("}", "\\}")
                                                      .replace("[", "\\[")
                                                      .replace("]", "\\]")
                                                      .replace("|", "\\|"))
        run_command(cmd_command)

    def screenshot(self, is_delete_image_after_capture=True):
        device_name = self.device
        try:
            device_name = device_name.split(":")[1]
        finally:
            pass
        filename = "screenShot" + device_name + ".png"
        while True:
            if not os.path.isfile(filename):
                break
            try:
                os.remove(filename)
                break
            finally:
                break
        filename2 = os.getcwd().replace("\\\\", "\\")
        filename2 = "\"" + filename2 + "\""
        cmd_command = "adb -s {0} shell screencap -p \"{1}\"".format(self.device, "/sdcard/" + filename)
        cmd_command2 = "".join([
            "adb -s ",
            self.device,
            " pull /sdcard/",
            filename,
            " ",
            filename2])
        run_command(cmd_command)
        run_command(cmd_command2)
        try:
            image = cv2.imread(filename)
        finally:
            pass
        if is_delete_image_after_capture:
            try:
                os.remove(filename)
            finally:
                pass
            try:
                cmd_command3 = "".join([
                    "adb -s ",
                    self.device,
                    " shell \"rm /sdcard/",
                    filename, "\""])
                run_command(cmd_command3)
            finally:
                pass
        return image

    def find_image_and_click(self, templatePath):
        template = cv2.imread(templatePath)
        point = find_out_point(template)
        self.tap(point.x, point.y)

    def change_proxy(self, ip_proxy, port_proxy):
        run_command(
            "adb -s {0} shell settings put global http_proxy {1}:{2}".format(self.device, ip_proxy, port_proxy))

    def remove_proxy(self):
        run_command("adb -s {0} shell settings put global http_proxy :0".format(self.device))