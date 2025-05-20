import psutil,asyncio,socket,platform,time,subprocess,json,os,random

class HostController:
    def __init__(self,view):
        self._hostname = None
        self._ip_address = None
        self._os = None
        self._total_cpu = None
        self._total_memory = None
        self._total_storage = None
        self._uptime = None
        self.view = view
        self._running = False

    def get_hostname(self):
        self._hostname = socket.gethostname()
        return self._hostname
    
    def get_ip_address_active(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8',80))
            self._ip_address = s.getsockname()[0]
        finally:
            s.close()

        return self._ip_address  
    
    def get_pretty_os(self):
        self._os = platform.freedesktop_os_release()['PRETTY_NAME']
        return self._os
    
    def get_cpu_threads(self):
        self._total_cpu = psutil.cpu_count(logical=True)
        return self._total_cpu
    
    def get_total_memory(self):
        """
            Get total memory system installed (RAM) - MB
        """
        self._total_memory= (psutil.virtual_memory().total // (1024 ** 2))
        return self._total_memory

    def get_total_storage(self):
        """
            Get total storage from '/' partion (Disk) - GB
        """
        self._total_storage =(psutil.disk_usage('/').total // (1024 ** 3))
        return self._total_storage
    
    def get_uptime(self):
        boot_time = psutil.boot_time()
        now = time.time()
        uptime_seconds = int(now - boot_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self._uptime = f"{hours}:{minutes}:{seconds}"
        return self._uptime


    async def start(self):
        self._running = True
        while self._running:
            uptime = self.get_uptime()
            self.view.update_uptime(uptime)
            await asyncio.sleep(1)

    def stop(self):
        self._running = False
    

class CPUController:
    def __init__(self,view):
        self.view = view
        self._running = False

    async def start(self):
        self._running = True
        while self._running:
            usage = psutil.cpu_percent(interval=None)
            self.view.update_cpu_usage(usage)
            await asyncio.sleep(1)
    def stop(self):
        self._running = False


class RAMController:
    def __init__(self, view):
        self.view = view
        self._running = False

    def get_used_ram(self):
        """
        Return used RAM in GB
        """
        mem = psutil.virtual_memory()
        return mem.used / (1024 ** 3)

    def get_total_ram(self):
        """
        Return total RAM in GB
        """
        mem = psutil.virtual_memory()
        return mem.total / (1024 ** 3)

    def get_percent_ram(self):
        """
        Return RAM usage percent
        """
        mem = psutil.virtual_memory()
        return mem.percent

    async def start(self):
        self._running = True
        while self._running:
            percent = self.get_percent_ram()
            used_gb = self.get_used_ram()
            total_gb = self.get_total_ram()
            self.view.update_ram_usage(percent, used_gb, total_gb)
            await asyncio.sleep(1)

    def stop(self):
        self._running = False


class StorageController:

    def __init__(self):
        super().__init__()

        self._disk = psutil.disk_usage('/')
        self._used = None
        self._total = None
        self._percent = None

    def get_used_disk(self):
        """
            Return space used in GB
        """
        self._used = self._disk.used / (1024 ** 3)
        return self._used
    
    def get_total_disk(self):
        self._total = self._disk.total / (1024 ** 3)
        return self._total
    
    def get_percent_disk(self):
        self._percent = self._disk.percent
        return self._percent

    
class SystemController:

    @staticmethod
    def get_total_memory():
        mem = psutil.virtual_memory()
        total_memory = (mem.total//(1024**2))

        file = "src/data/machines.json"
        used = 0
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    vms = json.load(f)
                    for vm in vms:
                        used += int(vm["memory"])
                except Exception:
                    pass
        return int(total_memory-used)
    
    @staticmethod
    def get_total_vcpus():
        cpu = psutil.cpu_count(logical=True)
        file = "src/data/machines.json"
        used = 0
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    vms = json.load(f)
                    for vm in vms:
                        used += int(vm["vcpus"])
                except Exception:
                    pass
        return int(cpu-used)

    @staticmethod
    def get_total_storage():
        storage = psutil.disk_usage('/')
        total_storage = (storage.total // (1024**3))
        file = "src/data/machines.json"
        used = 0
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    vms = json.load(f)
                    for vm in vms:
                        used += int(vm["disk"])
                except Exception:
                    pass
        return int(total_storage - used)
    
    @staticmethod
    def get_iso_images():
        images_path = '/home/xen/operations_systems/'
        images = []
        try:
            images = subprocess.run(['ls', f'{images_path}'], text=True, stdout=subprocess.PIPE).stdout.splitlines()
        except subprocess.CalledProcessError as e:
            # print(f"Error: {e}")
            pass
        return images
    
    @staticmethod
    def get_random_mac():
        hex_list = ['a','b','c','d','e','f',1,2,3,4,5,6,7,8,9]
        output_list = [str(random.choice(hex_list)) + str(random.choice(hex_list)) for n in range(6)]
        return ":".join(output_list)

    @staticmethod
    def get_vnc_port():
        file = "src/data/machines.json"
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    vms = json.load(f)
                    port = int(len(vms))
                except Exception:
                    pass

        
        return port
    
    