# console-recording-scripts
Helper scripts for recording console actions using Debian Linux.

## Usage

### `xdo.py`

1. Ensure you have `xdotool` installed:

```
sudo apt-get update
sudo apt-get install xdotool
```

2. Create a "script" text file of the commands to type within the console. You can also use the following special commands:

* `@P[num]@` tells the script to delay for a number of seconds
* `@U@`, `@D@`, `@L@`, `@R@` for up, down, left, and right on the keypad

An example script:

```
brownie console --network mainnet
@P2@comptroller = @D@.f@D@@D@@D@('0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b', as_proxy_for='0x97BD4Cc841FC999194174cd1803C543247a014fe')
@P8@cDai = @D@.f@D@@D@@D@('0x5d3a536e4d6dbd6114cc1ead35777bab948e3643')
@P5@cDai.s@D@@D@('cDai')
@P1@cEth = @D@('cEth')
```

3. If necessary, you can adjust the default delay between keypresses within `xdo.py`

4. For recording your desktop, I recommend [Kazam](https://launchpad.net/kazam):

```bash
sudo add-apt-repository ppa:kazam-team/stable-series
sudo apt-get update
sudo apt-get install kazam
```

5. Begin a screen capture with Kazam. In one console, run `python xdo.py [script filename]`. You will have 5 seconds to switch to another console where the script will be executed.

6. When you are finished, be sure to save the output in mp4 format.

### `mp4slice.py`

1. Ensure you have `ffmpeg` installed:

```
sudo apt-get update
sudo apt-get install ffmpeg
```

2. Edit `mp4slice.py` and set the specific start and end points that you wish to cut from the video.

3. Run as `python mp4slice.py [filename]`. The output will be given as `final.mp4`.

4. For conversion from `mp4` to gif, use [FFMPEG-gif-script-for-bash](https://github.com/thevangelist/FFMPEG-gif-script-for-bash)
