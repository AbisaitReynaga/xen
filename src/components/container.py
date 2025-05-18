import flet as ft


class CustomContainer(ft.Container):
    def __init__(self):
        super().__init__(height=300, width=400, bgcolor="#131926")
        self.border_radius = 10
        self.padding = ft.Padding(10, 0, 0, 0)
        self.shadow = ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.BLACK54, #Cambiar
            offset=ft.Offset(4, 4),
            blur_style=ft.ShadowBlurStyle.NORMAL
        )
        self.border = ft.border.all(2, "#262b40")

