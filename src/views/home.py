import flet as ft

from components import Header,CPUChartUsage,HostInformation,StorageChartUsage,RAMChartUsage

def home_view(page:ft.Page):

    return ft.View(
        route="/",
        controls=[
            ft.Column(
                expand=True,
                controls=[
                    Header(page,"/"),
                    ft.Row(
                        controls=[
                            HostInformation(),
                            CPUChartUsage(),
                            RAMChartUsage(),
                            StorageChartUsage()
                        ]
                    )

                ]
            )

        ]

    ) 