# audio_transmitter
Transmit Audio across devices
# Audo transmitter
Transmit Audio across devices such as phones, tablets, etc.
<hr>

# receiver.py
This script is the receiver, you can run it on the device you want the sound to be played. like, on phones, tablets. You need to install termux to run python in phone, you may need to install additional python packages too.
# transmitter.py
This script transmits the audio to the specified IP(LAN), you need to specify the device IP first, then choose a device to capture the audio from(will be asked as an input). Then the script will automitaclly connect to the specified IP then start streaming.
<hr>
You have to run receiver.py first. Then run transmitter.py after that. Otherwise it will cause an error.
<hr>
If your sound is not playing or you're getting a channel error, there's no problem with the script. try choosing stereo mix as a capture audio. Make sure to choose a speaker, not a mic or anything else.

If your device gets too hot, or it's lagging, try using a higher `BUFFER_SIZE` in the transmitter.py to solve it

I used my PC as the transmitter and phone as the receiver, my phone plays the audio without any kind of lags.

🌠 Thank you