import os

COUNTER_FILE = "download_counter.txt"

def increment_download_count():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")
    else:
        with open(COUNTER_FILE, "r+") as f:
            try:
                count = int(f.read().strip() or 0) + 1
            except:
                count = 1
            f.seek(0)
            f.write(str(count))
            f.truncate()

def get_download_count():
    if not os.path.exists(COUNTER_FILE):
        return 0
    try:
        with open(COUNTER_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except:
        return 0
