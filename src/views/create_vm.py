import flet as ft

from components import Header,VirtualMachinForm,CPUChartAvaiable,RAMChartAvailable,StorageChartAvailable
from components import HostInformation
def create_vm_view(page:ft.Page):
    return ft.View(
        route="/create_vm",
        scroll=ft.ScrollMode.ALWAYS,
        controls=[
            ft.Column(
                
                controls=[
                    Header(page,"/create_vm"),
                    ft.Row([HostInformation(),CPUChartAvaiable(),RAMChartAvailable(),StorageChartAvailable()]),
                    VirtualMachinForm(page)
                ]
            )
        ]

    )