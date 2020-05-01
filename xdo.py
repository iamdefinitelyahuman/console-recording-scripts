#!/usr/bin/python3

from pykeyboard.x11_keysyms import KEYSYMS
from subprocess import run
import time
import sys

# delays are given as 2-item tuples of (seconds before, seconds after)

DEFAULT_DELAY = (0, 0.05)
DELAYS = {
    "\n": (0.33, 1.75),
    "@D@": (0.25, 0.25),
    ".": (1, 0.5),
    "(": (1, 0.5),
    ",": (0.5, 0.5),
    " ": (0, 0.25),
}


if len(sys.argv) < 2:
    print(
        """Usage: python3 xdo.py [filename]

You will have 5 seconds to move to your target application before the text
in the file starts typing.

You can edit xdo.py to adjust delays before and after each keypress."""
    )
    sys.exit()


REPLACEMENT_VALUES = KEYSYMS.copy()
REPLACEMENT_VALUES.update(
    {
        "\n": "KP_Enter",
        "@U@": "KP_Up",
        "@D@": "KP_Down",
        "@L@": "KP_Left",
        "@R@": "KP_Right",
    }
)


def get_next(text):
    if text[0] == "@":
        idx = text.index("@", 1) + 1
    else:
        idx = 1

    n = text[:idx]
    text = text[idx:]

    pre, post = DELAYS.get(n, DEFAULT_DELAY)
    return REPLACEMENT_VALUES.get(n, n), pre, post, text


with open(sys.argv[-1]) as fp:
    cmdlist = fp.read()


for i in range(5, 0, -1):
    print(i, "...")
    time.sleep(1)

delay_active = True


while cmdlist:
    key, pre_delay, post_delay, cmdlist = get_next(cmdlist)
    if key.startswith("@P"):
        time.sleep(int(key[2:-1]))
        continue
    if key.startswith("quote"):
        delay_active = not delay_active
    if not delay_active:
        pre_delay, post_delay = 0, 0
    time.sleep(pre_delay)
    run(["xdotool", "key", key])
    time.sleep(post_delay)
