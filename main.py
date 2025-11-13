import itertools
import threading
import time
import sys
from Utils.getEmail import email_parser

stop_flag = False

def key_listener():
    global stop_flag

    if not sys.stdin.isatty():
        print("[Fallback] Press 'q' + Enter to stop.")
        while not stop_flag:
            ch = input()
            if ch.strip().lower() == 'q':
                stop_flag = True
                break
        return

    import termios
    import tty
    import select

    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    try:
        while not stop_flag:
            if select.select([sys.stdin], [], [], 0)[0]:
                ch = sys.stdin.read(1)
                if ch.lower() == 'q':
                    stop_flag = True
                    break
            time.sleep(0.05)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    t_key = threading.Thread(target=key_listener, daemon=True)
    t_key.start()

    email_parser(lambda: stop_flag)
