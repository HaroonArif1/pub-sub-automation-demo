import subprocess
import sys
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    publisher_proc = subprocess.Popen(
        [sys.executable, os.path.join(BASE_DIR, "publisher.py")]
    )

    # Give the publisher server a moment to bind its socket before the subscriber connects.
    time.sleep(0.5)

    subscriber_proc = subprocess.Popen(
        [sys.executable, os.path.join(BASE_DIR, "subscriber.py")]
    )

    try:
        publisher_proc.wait()
        subscriber_proc.wait()
    except KeyboardInterrupt:
        publisher_proc.terminate()
        subscriber_proc.terminate()


if __name__ == "__main__":
    main()
