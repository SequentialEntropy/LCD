import platform
import subprocess
import getpass
import time

system = platform.system()

# pwd = subprocess.Popen(['echo', getpass.getpass('Password:')], stdout=subprocess.PIPE)

# def get_temp():
#     command = "sudo powermetrics --samplers smc -i1 -n1"
#     cmd1 = subprocess.Popen(['echo', getpass.getpass('Password:')], stdout=subprocess.PIPE)
#     cmd2 = subprocess.Popen(['sudo', '-S'] + command.split(), stdin=cmd1.stdout, stdout=subprocess.PIPE)

#     output = cmd2.stdout.read().decode()

#     lines = output.split("\n")

#     for line in lines:
#         if "CPU die temperature" in line:
#             return int(float(line.split()[3]))

#     return subprocess.call(" ".split("sudo powermetrics --samplers smc -i1 -n1 | grep -i \"CPU die temperature\""))
#     return os.popen("sudo powermetrics --samplers smc -i1 -n1 | grep -i \"CPU die temperature\"")

class get_temp:

    if system == "Darwin":
        command = "sudo -S powermetrics --samplers smc -i1 -n1"
        stdin = subprocess.Popen(['echo', getpass.getpass('Password:')], stdout=subprocess.PIPE).stdout
        filter = ["CPU die temperature: ", " C"]
    elif system == "Linux":
        command = "vcgencmd measure_temp"
        stdin = None
        filter = ["temp=", "'C"]

    def __call__(self):

        output = subprocess.Popen(self.command.split(), stdin=self.stdin, stdout=subprocess.PIPE).stdout.read().decode()

        return self.decode_output(output)

    def decode_output(self, output):
        for line in output.split("\n"):
            if self.filter[0] in line:
                for phrase in self.filter:
                    line = line.replace(phrase, "")
                return float(line)

temp = get_temp()

# while True:
#     print(temp())
#     time.sleep(1)