# import argparse
import socket
import sounddevice as sd

DEFAULT_SERVER_IP = input("Enter the LAN IP of the target device: ")
DEFAULT_SERVER_PORT = int(input("Enter the port of the target device: "))
BUFFER_SIZE = 1024
SAMPLE_RATE = 48000

def audio_callback(indata, frames, time, status, sock):
    if status:
        print(status)
    sock.send(indata.tobytes())

def main():

    devices = sd.query_devices()
    print(f"\033[36mAvailable devices:\n {devices}\033[0m")

    # Fine the stereo device
    stereo_device = None
    for index, device in enumerate(devices):
        if "Stereo" in device['name']:
            stereo_device = index
            print()
            print(f"\033[34mDetected {index} as the stereo speaker: {device['name']}\033[0m")
            break

    if stereo_device is not None:
        user_input = input("\033[34mJust hit Enter to continue with this device, or enter a number to select a custom one(hit enter if you don't know what you're doing):\033[0m")
        if user_input.strip():
            selected_device = int(user_input)
        else:
            selected_device = stereo_device
    else:
        print("No stereo device detected. Please select a device manually.")
        selected_device = int(input("Enter the device number: "))

    # Establish connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to server...")
    sock.connect((DEFAULT_SERVER_IP, int(DEFAULT_SERVER_PORT)))
    print("Connected.")

    # Start audio stream
    print("Starting audio stream...")
    with sd.InputStream(callback=lambda indata, frames, time, status: audio_callback(indata, frames, time, status, sock),
                        channels=2,  # Stereo
                        samplerate=SAMPLE_RATE,
                        dtype='int16',
                        blocksize=BUFFER_SIZE,
                        device=selected_device):

        input('Press Enter to stop streaming...')

    # Close socket
    sock.close()
    print("Stopped streaming.")

if __name__ == "__main__":
    main()
