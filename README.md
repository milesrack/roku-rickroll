# roku-rickroll :musical_note:
<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>

Plays [Never Gonna Give You Up](https://www.youtube.com/watch?v=dQw4w9WgXcQ) to Roku TVs on your local network.

![rickroll](media/rickroll.gif)

## :pushpin: Installation
```
git clone https://github.com/milesrack/roku-rickroll.git
cd roku-rickroll
pip3 install -r requirements.txt
python3 roku-rickroll.py
```
## :pushpin: Usage
```
usage: roku-rickroll.py [-h] [-d] [-t TARGET] [-a] [-r [REPLAY]]

optional arguments:
  -h, --help            show this help message and exit
  -d, --discover        Discover Roku devices on the local network
  -t TARGET, --target TARGET
                        Target to Rickroll
  -a, --target-all      Target all Roku devices on the local network
  -r [REPLAY], --replay [REPLAY]
                        Number of times to replay the video (default 0)
```
This not work 100% of the time (errors, YouTube promotions/messages, latency) but re-running the script or slightly increasing values for `time.wait()` usually fixes these issues.
## :pushpin: TODO
|Status|Task|
|----------|--------|
|:heavy_check_mark:|Initial commit|
||Discover Roku devices via SSDP rather than scanning port 8060 on 255 hosts|
||Possibly cast locally stored videos to the Roku (no ads, less latency)|

**NOTE:** Do not use this on people's TVs without their permission. I am not responsible for what you do.
