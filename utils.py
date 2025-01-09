def get_wasapi_devices(pyaudio):
    """
    Get available WASAPI devices.
    :param pyaudio: PyAudio object
    :return: a dictionary containing the device ID mapped with the device
             information
    """
    device_id = -1
    wasapi_devices = dict()
    while True:
        device_id += 1
        try:
            device_info = pyaudio.get_device_info_by_index(device_id)
            api_info = pyaudio.get_host_api_info_by_index(device_info["hostApi"])
            is_wasapi = api_info["name"].find("WASAPI") != -1
            if is_wasapi:
                wasapi_devices[device_id] = device_info
        except IOError:
            # device_id not found
            break

    return wasapi_devices


def get_output_devices(pyaudio):
    """
    Get available output devices.
    :param pyaudio: PyAudio object
    :return: a dictionary containing the device ID mapped with the device
             information
    """
    device_id = -1
    output_devices = dict()
    while True:
        device_id += 1
        try:
            device_info = pyaudio.get_device_info_by_index(device_id)
            is_output = device_info["maxOutputChannels"] > 0
            if is_output:
                output_devices[device_id] = device_info
        except IOError:
            # device_id not found
            break

    return output_devices


def print_device_dict(device_dict):
    """
    Print the given device dictionary in a user friendly way.
    :param device_dict: a dictionary containing the device ID mapped with the
                        device information
    """
    for device_id in device_dict:
        print(str(device_id) + ':', device_dict[device_id]['name'])


def handle_device_selection(selected_device_id_str, valid_devices):
    """
    Checks whether a device selection is valid based on a dictionary of valid
    devices or prompts the user for a new selection otherwise.
    :param selected_device_id_str: the selected device ID (string or None)
    :param valid_devices: valid devices in a dictionary containing the device
                          ID mapped with the device information
    :return: the final device ID selection, which is guaranteed to be valid
             (integer)
    """
    if selected_device_id_str is None:
        # no ID specified
        valid_device_selected = False
    else:
        # device ID is specified, check if valid
        selected_device_id = int(selected_device_id_str)
        if selected_device_id in valid_devices:
            valid_device_selected = True
        else:
            valid_device_selected = False
            print('Invalid device ID given (' + str(selected_device_id) + ').')

    if not valid_device_selected:
        # device ID invalid or not specified, prompt for selection
        print('\033[36mAvailable devices:')
        print_device_dict(valid_devices)
        print()
        selected_device_id = int(input('Choose a device as a speaker from the list above: \033[0m'))
        while selected_device_id not in valid_devices:
            selected_device_id = int(input('Invalid device ID, please try again: '))

    return selected_device_id

def get_lan_ip(socket):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan_ip = s.getsockname()[0]
        s.close()
        return lan_ip
    except Exception as e:
        return f"Error: {e}"


def broadcast_presence(ip, port, socket, time):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    broadcast_message = ip
    broadcast_address = ('<broadcast>', port)
    
    # Create a separate socket to listen for responses on the LAN IP
    response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    response_socket.bind(('', port))  # Bind to the LAN IP specifically

    print("Waiting for transmitter to connect...")
    try:
        while True:
            # Broadcast the message
            server_socket.sendto(broadcast_message.encode(), broadcast_address)
            time.sleep(9999999)
            print("bb")

            try:
                data, addr = response_socket.recvfrom(1024)
                print(addr, data)
                if addr[0] != ip:  # Ignore messages from the server's own IP
                    print(f"Detected Transmitter: {addr[0]}")
                    return addr[0]
            except socket.timeout:
                pass
    finally:
        server_socket.close()
        response_socket.close()