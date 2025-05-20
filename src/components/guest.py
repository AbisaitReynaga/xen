import flet as ft
import asyncio

from components import CustomContainer
from models import VirtualMachineModel
from controllers import VirtualMachinController

class VirtualMachinList(CustomContainer):
    def __init__(self,vms:VirtualMachineModel):
        super().__init__()
        
        self.expand = True
        self.vms = vms


        self.rows = []
        for vm in self.vms:
            if vm.status:  # Suponiendo que VM tiene un atributo 'status'
                self.rows.append(VirtualMachine(vm))
            else:
                self.rows.append(VirtualMachineOffline(vm))

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Virtual Machines",
                    size=28,
                    weight='bold',
                    color='white',
                ),
                ft.Row(
                    controls=[
                        ft.DataTable(
                            expand=True,
                            columns=[
                                ft.DataColumn(label=ft.Text("Name", size=20)),
                                ft.DataColumn(label=ft.Text("VCPUS (Cores)", size=20)),
                                ft.DataColumn(label=ft.Text("Memory (Mb)", size=20)),
                                ft.DataColumn(label=ft.Text("Storage (GB)", size=20)),
                                ft.DataColumn(label=ft.Text("Uptime", size=20)),
                                ft.DataColumn(label=ft.Text("MAC", size=20)),
                                ft.DataColumn(label=ft.Text("VNC Port", size=20)),
                                ft.DataColumn(label=ft.Text("Actions", size=20)),
                            ],
                            rows=self.rows
                        )
                    ]
                )
            ]
        )

class VirtualMachineOffline(ft.DataRow):
    def __init__(self, vm):
        super().__init__(
            cells=[
                ft.DataCell(ft.Text(vm.name.upper(), size=18)),
                ft.DataCell(ft.Text(str(vm.vcpus), size=18)),
                ft.DataCell(ft.Text(str(vm.memory), size=18)),
                ft.DataCell(ft.Text(str(vm.disk), size=18)),
                ft.DataCell(ft.Text("00:00:00", size=18)), 
                ft.DataCell(ft.Text(vm.mac_adress.upper(), size=18)),
                ft.DataCell(ft.Text(str(vm.vnc_port+5900), size=18)),
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.PLAY_ARROW,
                        icon_color=ft.Colors.GREEN_300,
                        icon_size=30,
                        tooltip="TURN ON",
                        on_click=lambda e: self.turn_on(
                            vm.name
                        )
                    )
                ),
            ]
        )
    def turn_on(self, vm_name):
        VirtualMachinController().turn_on_vm(vm_name)
        self.page.go("/refresh")
        self.page.go("/")


class VirtualMachine(ft.DataRow):
    def __init__(self, vm):
        self._running = False

        self.vm = vm
        self.vm_controller = VirtualMachinController()
        self.uptime_text = ft.Text(self.vm_controller.get_uptime_vm(vm.name), size=18, color="white")
        super().__init__(
            cells=[
                ft.DataCell(ft.Text(vm.name.upper(), size=18)),
                ft.DataCell(ft.Text(str(vm.vcpus), size=18)),
                ft.DataCell(ft.Text(str(vm.memory), size=18)),
                ft.DataCell(ft.Text(str(vm.disk), size=18)),
                ft.DataCell(self.uptime_text),  # O calcula el uptime real
                ft.DataCell(ft.Text(vm.mac_adress.upper(), size=18)),
                ft.DataCell(ft.Text(str(vm.vnc_port+5900), size=18)),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.STOP,
                                icon_color=ft.Colors.RED_300,
                                icon_size=30,
                                tooltip="TURN OFF",
                                on_click=lambda e: self.turn_off(vm.name)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.RESTORE,
                                icon_color=ft.Colors.AMBER_300,
                                icon_size=30,
                                tooltip="RESET",
                                on_click=None
                            ),
                        ]
                    )
                ),
            ]
        )

    def turn_off(self, vm_name):
        VirtualMachinController().turn_off_vm(vm_name)
        self.page.go("/refresh")
        self.page.go("/")

    
    def did_mount(self):
            self._running = True
            self.page.run_task(self.update_time)

    def will_unmount(self):
        self._running = False

    async def update_time(self):
        while self._running and self.page is not None:
            self.uptime_text.value = self.vm_controller.get_uptime_vm(self.vm.name)
            try:
                self.page.update()
            except Exception:
                pass
            await asyncio.sleep(1)