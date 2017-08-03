# watch-puppy

[![GitHub license](https://img.shields.io/badge/license-WTFPL-blue.svg)](https://raw.githubusercontent.com/peitaosu/watch-puppy/master/LICENSE)

## What is watch-puppy ?

watch-puppy is a watchdog tool which can be used to observe file system changes (Linux, Windows and OSX), and registry changes (Windows).

## How To Use ?

1. Observe File System:

```
> python watch-fs.py [<path_to_watch>[, <log_file_path>]]

- path_to_watch: optional, path which you want to observe, default is ./
- log_file_path: optional, path to save logs, if not set, log will print to console
```

2. Observe Registry:

```
> python watch-reg.py [<hive_to_watch>[, <key_to_watch>[, <log_file_path>]]]

- hive_to_watch: optional, registry hive which you want to observe, default is HKCU
- key_to_watch: optional, registry key which you want to observe, default is SOFTWARE
- log_file_path: optional, path to save logs, if not set, log will print to console
```