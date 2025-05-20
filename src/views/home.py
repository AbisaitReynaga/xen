import flet as ft

from components import Header,CPUChartUsage,HostInformation,StorageChartUsage,RAMChartUsage
from components import VirtualMachinList
from controllers import VirtualMachinController


def home_view(page:ft.Page):
    controller = VirtualMachinController()
    virtual_machines = controller.get_all_vms()

    return ft.View(
        route="/",
        controls=[
            ft.Column(
                controls=[
                    Header(page,"/"),
                    ft.Row(
                        controls=[
                            HostInformation(),
                            CPUChartUsage(),
                            RAMChartUsage(),
                            StorageChartUsage()
                        ]
                    ),
                    
                    ft.Row(
                        expand=True,
                        controls=[VirtualMachinList(virtual_machines)]
                    )


                ]
            )

        ]

    ) 