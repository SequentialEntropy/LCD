import platform
import subprocess
import getpass
import time
import shutil
import psutil

system = platform.system()

class get_temp:

    if system == "Darwin":
        command = "sudo -S powermetrics --samplers smc -i1 -n1"
        stdin = subprocess.Popen(['echo', getpass.getpass('Password:')], stdout=subprocess.PIPE).stdout
        filter = ["CPU die temperature: ", " C"]
    elif system == "Linux":
        command = "vcgencmd measure_temp"
        stdin = None
        filter = ["temp=", "'C"]

    def __call__(self, places=0):

        output = subprocess.Popen(self.command.split(), stdin=self.stdin, stdout=subprocess.PIPE).stdout.read().decode()

        return decimals(self.decode_output(output), places)

    def decode_output(self, output):
        for line in output.split("\n"):
            if self.filter[0] in line:
                for phrase in self.filter:
                    line = line.replace(phrase, "")
                return float(line)

temp_cpu = get_temp()

def total_space(places=0):
    return decimals(shutil.disk_usage("/")[0] / (2**30), places)

def used_space(places=0):
    return decimals(shutil.disk_usage("/")[1] / (2**30), places)

def percent_space(places=0):
    return decimals(used_space(None) / total_space(None) * 100, places)

def total_ram(places=0):
    return decimals(dict(psutil.virtual_memory()._asdict())["total"] / (2**30), places)

def used_ram(places=0):
    return decimals(dict(psutil.virtual_memory()._asdict())["used"] / (2**30), places)

def percent_ram(places=0):
    return decimals(used_ram(None) / total_ram(None) * 100, places)

def percent_cpu(places=0):
    return decimals(psutil.cpu_percent(), places)

def decimals(number, places=0):
    if places == None:
        return number
    elif places == 0:
        return int(number)
    return int(number * 10**places) / 10**places