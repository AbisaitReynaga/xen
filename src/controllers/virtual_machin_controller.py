import json,os,subprocess
from models import VirtualMachineModel

class VirtualMachinController:
    def __init__(self):
        pass

    def save_vm_cfg(self,vm:VirtualMachineModel):
        file = "src/data/machines.json"
        vms_cfg = []
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    vms_cfg = json.load(f)
                except json.JSONDecodeError:
                    vms_cfg = []
        vms_cfg.append(vm.to_dict())
        with open(file, "w") as f:
            json.dump(vms_cfg, f, indent=4)

    def vm_exists(self,vm_name:str):
        file = "src/data/machines.json"
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    vms_cfg = json.load(f)
                    for vm in vms_cfg:
                        if vm["name"] == vm_name:
                            return True
                except json.JSONDecodeError:
                    return False
        return False

    def get_all_vms(self):
        file = "src/data/machines.json"
        vms = []
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    vms_data = json.load(f)
                    for vm_data in vms_data:
                        vms.append(VirtualMachineModel(**vm_data))
                except Exception:
                    pass
        return vms
    @staticmethod
    def create_vm_cfg(vm:VirtualMachineModel):
        subprocess.run(['mkdir', f'/home/xen/domains/{vm.name}'])
        subprocess.run(['qemu-img', 'create', '-f', 'raw', f'/home/xen/domains/{vm.name}/disk.img', f'{vm.disk}G'])
        
        cfg = f"""
name = '{vm.name}'
type = 'hvm'
firmware = '{vm.firmware.lower()}'
memory = {vm.memory}
vcpus = {vm.vcpus}
vif = [ 'mac={vm.mac_adress}, bridge=xenbr0']
disk = ['file:/home/xen/domains/{vm.name}/disk.img,hda,w','file:/home/xen/operations_systems/{vm.iso_image},hdc:cdrom,r']
acpi = 1
device_model_version = 'qemu-xen'
bood = 'd'
sdl = 0
vnc = 1
vncdisplay = {vm.vnc_port}
vnclisten = ''
vncpassword = ''
"""
        subprocess.run(['touch', f'/etc/xen/config_machines/{vm.name}.cfg'])
        with open(f'/etc/xen/config_machines/{vm.name}.cfg', 'w') as f:
            f.write(cfg)

    @staticmethod
    def update_vm_status(vm_name: str, status: bool):
        file = "src/data/machines.json"
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    vms_cfg = json.load(f)
                except json.JSONDecodeError:
                    vms_cfg = []
            for vm in vms_cfg:
                if vm["name"] == vm_name:
                    vm["status"] = status
            with open(file, "w") as f:
                json.dump(vms_cfg, f, indent=4)


    @staticmethod
    def turn_on_vm(name):
        
        try:
            result = subprocess.run(['xl', 'create', f'/etc/xen/config_machines/{name}.cfg'],
                    text=True, 
                    capture_output=True,
                    check=True)
            VirtualMachinController().update_vm_status(name, True)
            return True
        except subprocess.CalledProcessError as e:
            return False
        

    @staticmethod
    def turn_off_vm(name):
        
        try:
            result = subprocess.run(['xl', 'destroy', f'{name}'],
                    text=True, 
                    capture_output=True,
                    check=True)
            VirtualMachinController().update_vm_status(name, False)
            return True
        except subprocess.CalledProcessError as e:
            return False
    @staticmethod
    def get_uptime_vm(name):
        try:
            result = subprocess.run(['xl', 'uptime', name],
                    text=True, 
                    capture_output=True,
                    check=True).stdout.split()[1:]
            return str(result[4])
        except subprocess.CalledProcessError as e:
            return False
