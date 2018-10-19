import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class FileWatcher():
    def __init__(self, path_to_watch="."):
        self.path_to_watch = path_to_watch
        self.event_handler = LoggingEventHandler()
        self.observer = Observer()
        self.recursive=True
    
    def set_log(self, log_file_path):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=log_file_path
            )

    def schedule(self):
        self.observer.schedule(self.event_handler, self.path_to_watch, self.recursive)
    
    def start(self):
        self.observer.start()
    
    def stop(self):
        self.observer.stop()
    
    def join(self):
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    path_to_watch = sys.argv[1] if len(sys.argv) > 1 else '.'
    log_file_path = sys.argv[2] if len(sys.argv) > 2 else None
    watcher = FileWatcher(path_to_watch)
    watcher.set_log(log_file_path)
    watcher.schedule()
    watcher.join()
