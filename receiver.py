import utils
import socket
import pyaudio

# default configuration parameters
DEFAULT_SERVER_PORT = 9999
STREAM_FORMAT = pyaudio.paInt16
BUFFER_SIZE = 65536


def run_socket_connection(port, audio_stream):
    while True:
        try:
            # Create and bind the server socket
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.bind(('', int(port)))
            serversocket.listen(5)
            
            print()
            ip = utils.get_lan_ip(socket)
            print(f"Your LAN IP: {ip}")
            print(f"Your PORT: {port}")
            print('Waiting for client connection...')
            transmitter, addr = serversocket.accept()
            print('Client connected.')

            while True:
                data = transmitter.recv(BUFFER_SIZE)
                if not data:  # Check if the client has disconnected
                    print("Client disconnected.")
                    break
                
                audio_stream.write(data)

        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f"Connection error: {str(e)}")
            break  # Exit the outer loop to terminate the server
        
        finally:
            serversocket.close()
            print("Server socket closed.")
            break

    print("Server terminated.")



def main():

    audio = pyaudio.PyAudio()
    output_devices = utils.get_output_devices(audio)
    if len(output_devices) == 0:
        print('No output device found')
        sys.exit()

    selected_device_id = utils.handle_device_selection(None, output_devices)
    selected_device_info = output_devices[selected_device_id]
    # print('You have selected:', selected_device_info) uncomment this line if u want more info  about the device

    channels = max(selected_device_info["maxInputChannels"],
                   selected_device_info["maxOutputChannels"])

    try:
        stream = audio.open(format=STREAM_FORMAT,
                            channels=channels,
                            rate=int(selected_device_info["defaultSampleRate"]),
                            output=True,
                            frames_per_buffer=BUFFER_SIZE,
                            output_device_index=selected_device_id)

        run_socket_connection(DEFAULT_SERVER_PORT, stream)

    finally:
        print('Shutting down')
        stream.close()
        audio.terminate()


main()
