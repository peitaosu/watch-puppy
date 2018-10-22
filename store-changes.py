import os, sys, shutil

def read_logs(fs_watch_log):
    with open(fs_watch_log) as in_file:
        return in_file.read().split("\n")

def parse_logs(logs):
    fs_logs = []
    for log in logs:
        if log == "":
            continue
        log = log[22:]
        fs_logs.append(log)
    return fs_logs

def store_changes(fs_logs, store_path):
    for fs_log in fs_logs:
        fs_op = fs_log.split(": ")[0]
        fs_path = fs_log.split(": ")[1]
        if not os.path.isfile(fs_path) and not os.path.isdir(fs_path):
            continue
        store_fs_path = os.path.join(store_path, fs_path[3:])
        if fs_op == "Modified file" or fs_op == "Created file":
            if not os.path.isdir(os.path.dirname(store_fs_path)):
                os.makedirs(os.path.dirname(store_fs_path))
            shutil.copyfile(fs_path, store_fs_path)
        elif fs_op == "Modified directory":
            if not os.path.isdir(store_fs_path):
                os.makedirs(store_fs_path)
        elif fs_op == "Deleted file":
            pass

if __name__ == "__main__":
    fs_watch_log = sys.argv[1]
    store_path = sys.argv[2]
    logs = read_logs(fs_watch_log)
    fs_logs = parse_logs(logs)
    store_changes(fs_logs, store_path)