import win32api
import win32con
import logging
import sys


class RegWatcher():

    def __init__(self):
        pass

    def set_reg_root(self, reg_root):
        reg_roots = {
            "HKCU": win32con.HKEY_CURRENT_USER,
            "HKLM": win32con.HKEY_LOCAL_MACHINE,
            "HKCR": win32con.HKEY_CLASSES_ROOT
        }
        self.reg_root = reg_roots[reg_root]

    def set_reg_key(self, reg_key):
        self.reg_key = reg_key

    def set_log(self, log_file_path):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_file_path
        )
        self.log = logging.getLogger()

    def start(self):
        values = {(self.reg_root, self.reg_key, "DateTime"): (win32con.REG_DWORD, 1),
                  (self.reg_root, self.reg_key, "Templates"): (win32con.REG_DWORD, 0),
                  (self.reg_root, self.reg_key, "UnitConv"): (win32con.REG_DWORD, 0)}

        while True:
            for (hive, key, value_name), (value_type, value) in values.iteritems():
                handle_with_set_rights = win32api.RegOpenKeyEx(
                    hive, key, 0, win32con.KEY_SET_VALUE)
                self.log.info(r"Setting %s\%s\%s = %s" %
                              (hive, key, value_name, value))
                win32api.RegSetValueEx(
                    handle_with_set_rights, value_name, 0, value_type, value)
                win32api.RegCloseKey(handle_with_set_rights)

            # Open and close the handle here as otherwise the set operation above
            # will trigger a further round
            handle_to_be_watched = win32api.RegOpenKeyEx(
                self.reg_root, self.reg_key, 0, win32con.KEY_NOTIFY)
            win32api.RegNotifyChangeKeyValue(
                handle_to_be_watched, False, win32api.REG_NOTIFY_CHANGE_LAST_SET, None, False)
            win32api.RegCloseKey(handle_to_be_watched)


if __name__ == "__main__":
    watcher = RegWatcher()
    watcher.set_reg_root(sys.argv[1]) if len(sys.argv) > 1 else watcher.set_reg_root("HKCU")
    watcher.set_reg_key(sys.argv[2]) if len(sys.argv) > 2 else watcher.set_reg_key("Software")
    watcher.set_log(sys.argv[3]) if len(sys.argv) > 3 else watcher.set_log(None)
    watcher.start()
