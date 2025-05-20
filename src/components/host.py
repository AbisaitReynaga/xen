import flet as ft

from components import CustomContainer
from controllers import CPUController, HostController,RAMController,StorageController
from controllers import SystemController


class HostInformation(CustomContainer):
    def __init__(self):
        super().__init__()
        self.host_controller = HostController(self)

        # Controls and build internal components
        self.uptime_label = ft.Text(
            f"{self.host_controller.get_uptime()} MB",
            color="white"
        )

        self.title = ft.Text(
            "Host information",
            color="white",
            size=38
        )
        
        self.expand =True


        self.content = ft.Column(
            controls=[
                self.title,
                self._build_machine(),
                self._build_ip_address(),
                self._build_os(),
                self._build_cpu(),
                self._build_memory(),
                self._build_storage(),
                self._build_uptime()
            ]
        )

    def _build_machine(self):
        return ft.Row(
            controls=[
                ft.Text(
                    "Machine:",
                    width=100,
                    color="white"),
                ft.Text(
                    f"{self.host_controller.get_hostname()}",
                    color="white")])

    def _build_ip_address(self):
        return ft.Row(
            controls=[
                ft.Text(
                    "IP Address:",
                    width=100,
                    color="white"),
                ft.Text(
                    f"{self.host_controller.get_ip_address_active()}",
                    color="white")])

    def _build_os(self):
        return ft.Row(
            controls=[
                ft.Text("OS:",
                        width=100,
                        color="white"),
                ft.Text(f"{self.host_controller.get_pretty_os()}",
                        color="white")
            ]
        )

    def _build_cpu(self):
        return ft.Row(
            controls=[
                ft.Text(
                    "CPU:",
                    width=100,
                    color="white"),
                ft.Text(
                    f"{self.host_controller.get_cpu_threads()} Cores",
                    color="white")
            ]
        )

    def _build_memory(self):
        return ft.Row(
            controls=[
                ft.Text(
                    "Memory:",
                    width=100,
                    color="white"),
                ft.Text(
                    f"{self.host_controller.get_total_memory()} MB",
                    color="white")
            ]
        )

    def _build_storage(self):
        return ft.Row(
            controls=[
                ft.Text(
                    "Storage:",
                    width=100,
                    color="white"),
                ft.Text(
                    f"{self.host_controller.get_total_storage()} GB",
                    color="white")
            ]
        )

    def _build_uptime(self):
        return ft.Row(
            controls=[
                ft.Text("Uptime:", width=100, color="white"),
                self.uptime_label
            ]
        )

    # Functions

    def update_uptime(self, uptime):
        self.uptime_label.value = uptime
        self.uptime_label.update()

    def did_mount(self):
        self.page.run_task(self.host_controller.start)

    def will_unmount(self):
        self.host_controller.stop()

class CPUChartUsage(CustomContainer):
    def __init__(self):
        super().__init__()

        # Controllers
        self.controller = CPUController(self)

        # Propierties
        self.title = ft.Text(
            "CPU Usage",
            size=24,
            color="white",
            weight=ft.FontWeight.BOLD)  # Title

        self.percent_label = ft.Text(
            "0%",
            size=20,
            color="white",
            weight=ft.FontWeight.BOLD)  # Percent label

        self.bar_background = ft.Container(  # Backgroud bar
            width=300,
            height=20,
            bgcolor="#2e2e3e",
            border_radius=10
        )

        self.bar_fill = ft.Container(  # Fill bar
            width=0,
            height=20,
            bgcolor="#3be38b",
            border_radius=10
        )

        # Style
        self.padding = ft.Padding(0, 30, 0, 80)


        # Contenido alineado
        self.content = ft.Column(
            controls=[
                self.title,
                ft.Container(
                    content=self._build_bar(),
                    alignment=ft.alignment.center),
                self.percent_label],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)

    def update_cpu_usage(self, usage):
        self.bar_fill.width = 2 * usage
        self.percent_label.value = f"{usage:.0f}%"
        self.bar_fill.update()
        self.percent_label.update()

    def did_mount(self):
        self.page.run_task(self.controller.start)

    def will_unmount(self):
        self.controller.stop()

    def _build_bar(self):
        return ft.Stack(
            controls=[
                self.bar_background,
                self.bar_fill
            ],
            width=300,
            height=20
        )

class RAMChartUsage(CustomContainer):
    def __init__(self):
        super().__init__()
        
        self.controller = RAMController(self)

        self.padding = ft.Padding(0, 30, 0, 30)
        
        # Título
        self.title = ft.Text("RAM Usage", size=24, color="white", weight=ft.FontWeight.BOLD)

        # Etiqueta de porcentaje
        self.percent_label = ft.Text("0%", size=20, color="white", weight=ft.FontWeight.BOLD)

        # Etiqueta GB usados / totales
        self.gb_label = ft.Text("0.0 GB / 0.0 GB", size=16, color="white")

        # Barra de fondo
        self.bar_background = ft.Container(
            width=300,
            height=20,
            bgcolor="#2e2e3e",
            border_radius=10
        )

        # Barra de llenado
        self.bar_fill = ft.Container(
            width=0,
            height=20,
            bgcolor="#3be38b",
            border_radius=10
        )

        # Stack con ambas barras
        self.bar = ft.Stack(
            controls=[
                self.bar_background,
                self.bar_fill
            ]
        )

        # Contenedor con todo centrado
        self.content = ft.Column(
            controls=[
                self.title,
                ft.Container(content=self.bar, alignment=ft.alignment.center),
                self.percent_label,
                self.gb_label
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )

    def update_ram_usage(self, percent, used_gb, total_gb):
        self.bar_fill.width = 3 * percent  # Ajusta el factor según el ancho máximo (300px)
        self.percent_label.value = f"{percent:.0f}%"
        self.gb_label.value = f"{used_gb:.1f} GB / {total_gb:.1f} GB"
        self.bar_fill.update()
        self.percent_label.update()
        self.gb_label.update()

    def did_mount(self):
        self.page.run_task(self.controller.start)

    def will_unmount(self):
        self.controller.stop()

class StorageChartUsage(CustomContainer):
    def __init__(self):
        super().__init__()
        self.padding = ft.Padding(0,30,0,30)
       
        self.storage_controller = StorageController()
       

        # Título
        self.title = ft.Text("Storage", size=24, color="white", weight=ft.FontWeight.BOLD)

        # Etiquetas
        self.percent_label = ft.Text(f"{self.storage_controller.get_used_disk():.1f}%", size=20, color="white", weight=ft.FontWeight.BOLD)
        self.gb_label = ft.Text(f"{self.storage_controller.get_used_disk():.1f} GB / {self.storage_controller.get_total_disk():.1f} GB", size=16, color="white")

        # Barra de fondo
        self.bar_background = ft.Container(
            width=300,
            height=20,
            bgcolor="#2e2e3e",
            border_radius=10
        )

        # Barra de llenado
        self.bar_fill = ft.Container(
            width=3 * self.storage_controller.get_percent_disk(),  # Escala a 300px
            height=20,
            bgcolor="#3be38b",  # color verdoso para almacenamiento
            border_radius=10
        )

        # Stack para barra
        self.bar = ft.Stack(
            controls=[
                self.bar_background,
                self.bar_fill
            ]
        )

        # Layout general
        self.content = ft.Column(
            controls=[
                self.title,
                ft.Container(content=self.bar, alignment=ft.alignment.center),
                self.percent_label,
                self.gb_label
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        )

class CPUChartAvaiable(CustomContainer):
    def __init__(self):
        super().__init__()
        self._controller = SystemController()
        self.cores_text = ft.Text(f"{self._controller.get_total_vcpus()} Cores", size=28, color="#3be38b")

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        
            controls=[
                self.cores_text,
                ft.Container(height=30),
                ft.Text("CPU Available", size=22, weight='bold', color='white'),
                
            ]
        )

class RAMChartAvailable(CustomContainer):
    def __init__(self):
        super().__init__()
        self._controller = SystemController()
        self.memory_text = ft.Text(f"{self._controller.get_total_memory()} MB", size=28, color="#3be38b")

        self.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[
                    self.memory_text,
                    ft.Container(height=30),
                    ft.Text("RAM Available", size=22, weight='bold', color='white'),
                    
                ]
            )

class StorageChartAvailable(CustomContainer):
    def __init__(self):
        super().__init__()
        self._controller = SystemController()
        self.storage_text = ft.Text(f"{self._controller.get_total_storage()} GB", size=28, color="#3be38b")

        self.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[
                    self.storage_text,
                    ft.Container(height=30),
                    ft.Text("Storage Available", size=22, weight='bold', color='white'),
                    
                ]
            )
    