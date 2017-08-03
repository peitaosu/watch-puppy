import win32api
import win32con
import logging
import sys

if __name__ == "__main__":
    hive_switcher = {
        'HKCU': win32con.HKEY_CURRENT_USER,
        'HKLM': win32con.HKEY_LOCAL_MACHINE,
        'HKCR': win32con.HKEY_CLASSES_ROOT
    }

    hive_to_watch = hive_switcher[sys.argv[1]] if len(
        sys.argv) > 1 else win32con.HKEY_CURRENT_USER
    key_to_watch = sys.argv[2] if len(sys.argv) > 2 else 'Software'
    log_file_path = sys.argv[3] if len(sys.argv) > 3 else None
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_file_path
                        )
    log = logging.getLogger()

    values = {(hive_to_watch, key_to_watch, 'DateTime'): (win32con.REG_DWORD, 1),
              (hive_to_watch, key_to_watch, 'Templates'): (win32con.REG_DWORD, 0),
              (hive_to_watch, key_to_watch, 'UnitConv'): (win32con.REG_DWORD, 0)}

    while True:
        for (hive, key, value_name), (value_type, value) in values.iteritems():
            handle_with_set_rights = win32api.RegOpenKeyEx(
                hive, key, 0, win32con.KEY_SET_VALUE)
            log.info(r'Setting %s\%s\%s = %s' % (hive, key, value_name, value))
            win32api.RegSetValueEx(
                handle_with_set_rights, value_name, 0, value_type, value)
            win32api.RegCloseKey(handle_with_set_rights)

        # Open and close the handle here as otherwise the set operation above
        # will trigger a further round
        handle_to_be_watched = win32api.RegOpenKeyEx(
            hive_to_watch, key_to_watch, 0, win32con.KEY_NOTIFY)
        win32api.RegNotifyChangeKeyValue(
            handle_to_be_watched, False, win32api.REG_NOTIFY_CHANGE_LAST_SET, None, False)
        win32api.RegCloseKey(handle_to_be_watched)
