from pathlib import Path
import shutil
import subprocess
import sys


# CUTS is a sequence timestamp tuples signifying start and end points to cut from an mp4
# e.g. [("1:00", "1:05"), ("2:21", "2:44")] will remove 1:00-1:05 and 2:21-2:44
# to cut to the end of a file, use `None` as the final end timestamp
# e.g. [("3:00", None)] will cut from 3:00 to the end

CUTS = [
    # TODO add your start and end times here
]


if len(sys.argv) < 2 or not CUTS:
    print(
        """Usage: python3 mp4slice.py [filename]

You must edit mp4slice.py to include start and end offsets you wish to
cut from the filename."""
    )
    sys.exit()


def _to_seconds(time):
    return sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":"))))


def _to_ts(filename):
    subprocess.run(
        f"ffmpeg -y -i {filename}.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts {filename}.ts",
        shell=True,
    )


shutil.copyfile(sys.argv[-1], "_sliceinput.mp4")

last_duration = 0
for start, end in CUTS:
    start = _to_seconds(start) - last_duration
    if end is not None:
        end = _to_seconds(end) - last_duration
        last_duration += end - start

    if start:
        subprocess.run(
            f"ffmpeg -y -i _sliceinput.mp4 -t {start} -c copy _begin.mp4", shell=True
        )
        if end is None:
            Path("_sliceinput.mp4").unlink()
            Path("_begin.mp4").rename("_sliceinput.mp4")
            break
        _to_ts("_begin")
    subprocess.run(f"ffmpeg -y -i _sliceinput.mp4 -ss {end} _end.mp4", shell=True)
    if not start:
        Path("_sliceinput.mp4").unlink()
        Path("_end.mp4").rename("_sliceinput.mp4")
        continue
    _to_ts("_end")
    subprocess.run(
        'ffmpeg -y -i "concat:_begin.ts|_end.ts" -c copy _sliceinput.mp4', shell=True
    )


for path in [Path(i) for i in ("_begin.ts", "_begin.mp4", "_end.ts", "_end.mp4")]:
    if path.exists():
        path.unlink()


Path("_sliceinput.mp4").rename("final.mp4")
