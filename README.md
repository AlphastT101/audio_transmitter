# Audo transmitter
Transmit Audio across devices such as phones, tablets, etc.
<hr>

## receiver.py
This script is the receiver, you can run it on the device you want the sound to be played. like, on phones, tablets. You need to install termux to run python in phone, you may need to install additional python packages too.
## transmitter.py
This script transmits the audio to the specified IP(LAN), you need to specify the device IP first, then choose a device to capture the audio from(will be asked as an input). Then the script will automitaclly connect to the specified IP then start streaming.
<hr>
You have to run receiver.py first. Then run transmitter.py after that. Otherwise it will cause an error.
<hr>
If your sound is not playing or you're getting a channel error, there's no problem with the script. try choosing stereo mix as a capture audio. Make sure to choose a speaker, not a mic or anything else.

If your device gets too hot, or it's lagging, try using a higher `BUFFER_SIZE` in the transmitter.py to solve it

I used my PC as the transmitter and phone as the receiver, my phone plays the audio without any kind of lags.

🌠 Thank you
<hr>


# How to use an Android phone as a speaker
**Setup your phone:**
* Install termux: https://play.google.com/store/apps/details?id=com.termux.
* Grant every permissions, including file management.
* Open termux. the the following commands in order:
```bash
pkg update && pkg upgrade
```
```bash
pkg install python clang libffi portaudio git
```

* Clone the gihub repo:
```bash
git clone https://github.com/AlphastT101/audio_transmitter.git
```
```bash
cd audio_transmitter
```

* Install required python libraries:
```bash
pip install -r requirements.txt
```

* Since we will play the sound on the phone, so we will run the receiver.py in phone.
```bash
python receiver.py
```

* Now the script will ask you to select an audio device as an output. For most of the device, it's `0: default`. So, enter `0`.
* Now the script will print your LAN IP and port. You need these info to connect the transmitter.

**Setup your PC:**
* Install python from microsoft store. I have used python 3.13.
* Run `pip install -r requirements.txt`
* Run `python transmitter.py`
* The script will ask you to select an audio device. It will automatically detect an audio device, just hit enter. Or if you want to use a custom one, choose a device by entering a number from the list.
* Now the script will automatically connect to your phone and will start streaming audio. Try playing an youtube video to test it.

Now working? please open an issue.