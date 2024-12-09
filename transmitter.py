import argparse
import socket
import sounddevice as sd

DEFAULT_SERVER_IP = input("Enter the LAN IP of the target device: ")
DEFAULT_SERVER_PORT = 9999
BUFFER_SIZE = 1024
SAMPLE_RATE = 48000

def audio_callback(indata, frames, time, status, sock):
    if status:
        print(status)
    sock.send(indata.tobytes())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', help="The server's IP address (default: "
                                    + str(DEFAULT_SERVER_IP) + ")",
                        default=DEFAULT_SERVER_IP)
    parser.add_argument('-p', '--port', help="The server's port to connect "
                                             "to (default: " + str(DEFAULT_SERVER_PORT) + ")",
                        default=DEFAULT_SERVER_PORT)
    parser.add_argument('-d', '--device', help="The audio device index or name for loopback capture.",
                        default=None)
    args = parser.parse_args()

    # List devices if no device is provided
    if args.device is None:
        print("Available devices:")
        print(sd.query_devices())
        device = int(input("Choose one(must be an int): "))

    # Establish connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to server...")
    sock.connect((args.ip, int(args.port)))
    print("Connected.")

    # Start audio stream
    print("Starting audio stream...")
    with sd.InputStream(callback=lambda indata, frames, time, status: audio_callback(indata, frames, time, status, sock),
                        channels=2,  # Stereo
                        samplerate=SAMPLE_RATE,
                        dtype='int16',
                        blocksize=BUFFER_SIZE,
                        device=device):  # Replace with your chosen device index

        input('Press Enter to stop streaming...')

    # Close socket
    sock.close()
    print("Stopped streaming.")

if __name__ == "__main__":
    main()
