class VirtualMachineModel:
    def __init__(self, name: str,vcpus:int,memory:int,disk:int,firmware:str,
                 iso_image: str,mac_adress:str,vnc_port:int,status:bool,delete:bool=False):
        
        self.name = name
        self.vcpus = vcpus
        self.memory = memory
        self.disk = disk
        self.firmware = firmware
        self.iso_image = iso_image
        self.mac_adress = mac_adress
        self.vnc_port = vnc_port
        self.status = status
        self.delete = delete

    def to_dict(self):
        return {
            "name": self.name,
            "vcpus": self.vcpus,
            "memory": self.memory,
            "disk": self.disk,
            "firmware": self.firmware,
            "iso_image": self.iso_image,
            "mac_adress": self.mac_adress,
            "vnc_port": self.vnc_port,
            "status": self.status,
            "delete": self.delete
        }