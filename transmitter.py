import socket
import sounddevice as sd

BUFFER_SIZE = 1024
SAMPLE_RATE = 48000

def audio_callback(indata, frames, time, status, sock):
    try:
        if status:
            print(status)
        sock.send(indata.tobytes())
    except Exception as e:
        print(f"Error: {e}")
        exit(0)

def main():
    print()
    devices = sd.query_devices()
    print(f"\033[36mAvailable devices:\n {devices}\033[0m")

    # Find the stereo device
    stereo_device = None
    for index, device in enumerate(devices):
        if "Stereo" in device['name']:
            stereo_device = index
            print()
            print(f"\033[34mDetected {index} as the stereo speaker: {device['name']}\033[0m")
            break

    if stereo_device is not None:
        user_input = input("\033[34mJust hit Enter to continue with this device, or enter a number to select a custom one (hit Enter if you don't know what you're doing):\033[0m")
        if user_input.strip():
            selected_device = int(user_input)
        else:
            selected_device = stereo_device
    else:
        print("No stereo device detected. Please select a device manually.")
        selected_device = int(input("Enter the device number: "))


    print("Listening for server broadcasts...")
    addr = input("Enter the LAN IP address of the receiver device: ")

    # Connect to the detected receiver
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to server...")
    try:
        print(str(addr[0]))
        sock.connect((str(addr[0]), 9678))
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
    except Exception as e:
        print(f"Error during connection or streaming: {e}")
    finally:
        sock.close()
        print("Stopped streaming.")

if __name__ == "__main__":
    main()