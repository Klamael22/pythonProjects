import platform
import subprocess
import socket
import re

# Set global regex flags
re_flags = re.IGNORECASE | re.MULTILINE

# Detect OS - Windows or Linux
def getOS():
    return platform.system()

# Windows checks
## Windows system checking function, takes a regex pattern, a command, an exception to matches, and a test id(like CPU, or NIC etc.)
def win_system_checker(pattern, command, exceptions, identifier):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, check=True, text=True)
        matchCount = 0
        lines = result.stdout.split('\n')

        for line in lines:
            match = pattern.fullmatch(line)
            if match:
                field = line.split('=')[0].strip()
                value = line.split('=')[1].strip()
                if not(exceptions in value for exception in exceptions):
                    matchCount += 1
                    print(f"\033[91m{identifier} indicator found: '{match.group(1)}' in the field '{field}' with value '{value}'")
        if matchCount == 0:
            print(f"\033[0m{identifier} indicators not found.")
    except subprocess.CalledProcessError as e:
        print(f"\033[0mError: {e}")

## Windows network layer checking
def check_dns_win():
    patterns = re.compile(r'vm|guest|virtual|vbox|vmware|hyperv|qemu|localdomain|local|lan|virtualbox')
    host_name = socket.gethostname()
    fqdn = socket.getfqdn()

    match_host = patterns.search(host_name)
    match_fqdn = patterns.search(fqdn)
    if match_host or match_fqdn:
        print("\033[91mPossible DNS indicators:")
        if match_host:
            print(f"\033[91mHostname: {host_name}")
        if match_fqdn:
            print(f"\033[91mFQDN: {fqdn}")
    else:
        print("\033[0mDNS indicators not found.")

## Windows registry checking - this function queries registry paths for patterns that can indicate the host may be a VM
def check_registry():
    patterns = ['vmware', 'oracle', 'VirtualBox', 'vbox', 'qemu', 'virtio']
    software_path = r'HKEY_LOCAL_MACHINE\SOFTWARE'
    hardware_path = r'HKEY_LOCAL_MACHINE\HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 0\Target Id 0\Logical Unit Id 0'
    hypervisor_present_path = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control'
    system_paths = [
        r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services',
        r'HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services',
    ]

    matches = 0
    for pattern in patterns:
        try:
            # software path check
            print(f"\033[0mChecking {software_path} for {pattern}.")
            software_result = subprocess.run(['reg', 'query', software_path], stdout=subprocess.PIPE, check=True, text=True)
            if pattern.lower() in software_result.stdout.lower():
                matches += 1
                print(f"\033[91mPattern '{pattern}' found in registry key: '{software_path}'.")
            
            # hardware path check
            print(f"\033[0mChecking {hardware_path} for {pattern}.")
            hardware_result = subprocess.run(['reg', 'query', hardware_path], stdout=subprocess.PIPE, check=True, text=True)
            if pattern.lower() in hardware_result.stdout.lower():
                matches += 1
                print(f"\033[91mPattern '{pattern}' found in registry key: '{hardware_path}'.")
            
            # hypervisorpresent path check
            print(f"\033[0mChecking {hypervisor_present_path} for 'HypervisorPresent=1.")
            hypervisor_present_result = subprocess.run(['reg', 'query', hypervisor_present_path], stdout=subprocess.PIPE, check=True, text=True)
            if "HypervisorPresent" in hypervisor_present_result.stdout and "0x1" in hypervisor_present_result.stdout:
                matches += 1
                print("\033[91mHypervisorPresent value is set to 1.")
            
            # system paths check
            for path in system_paths:
                print(f"\033[0mChecking {path} for {pattern}.")
                system_result = subprocess.run(['reg', 'query', path, '/s'], stdout=subprocess.PIPE, check=True, text=True)
                if pattern.lower() in system_result.stdout.lower():
                    matches += 1
                    print(f"\033[91mPattern '{pattern}' found in registry key: '{path}'.")
        except subprocess.CalledProcessError as e:
            print(f"\033[0mError: {e}")
        
        if matches == 0:
            print("\033[0mRegistry indicators not found.")

# CPU and NIC checks - For now only Windows is supported
## CPU checking
def check_cpu_win():
    pattern = re.compile(r'virtio|virtual|vm|qemu|amd-v|vt-x|kvm|microsoft')
    exceptions = [r'false']
    win_system_checker(pattern, ['wmic', 'cpu', 'get', '/format:list'], exceptions, "CPU")

## NIC checking
def check_nic_win():
    pattern = re.compile(r'(virtio|virtual|00:(50:56|0C:29|03:FF)|08:00:27|52:54:00)')
    exceptions = [r'Microsoft Wi-Fi Direct Virtual Adapter|VirtualBox Host-Only Ethernet Adapter']
    win_system_checker(pattern, ['wmic', 'nic', 'get', '/format:list'], exceptions, "NIC")

def main():
    os_type = getOS()
    if os_type == "Windows":
       check_cpu_win()
       check_nic_win()
       check_dns_win()
       check_registry()
    else:
        print("Non-Windows OS support coming soon!")

if __name__ == "__main__":
    main()