import flet as ft


class Header(ft.Container):
    def __init__(self,page:ft.Page,route):
        super().__init__()

        #Propierties
        self.page = page
        self.route = route
        self.menu_items = self._menu_items()

        #Styles
        self.padding = ft.Padding(
            left=25, 
            top=0, 
            right=25, 
            bottom=0)
        
        self.border = ft.border.all(
            width=3,
            color="#262b40")
        
        self.shadow = ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.BLACK54,
            offset=ft.Offset(4, 4),
            blur_style=ft.ShadowBlurStyle.NORMAL
        )

        self.height = 80

        self.bgcolor = "#131926"

        self.border_radius = 10


        # Content

        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self._build_logo(),
                self._build_menu()
            ]
        )

    def _build_logo(self):
        return ft.Row(
            controls=[
                ft.Text("XEN", size=38, weight='bold', style=ft.TextStyle(color='white'))
            ]
        )

    def _build_menu(self):
        return ft.Row([
            ft.PopupMenuButton(
                tooltip='',
                icon_color='white',
                icon=ft.Icons.MENU,
                icon_size=38,
                items=self.menu_items
            )
        ])

    def _menu_items(self):
        return [
            ft.PopupMenuItem(
                text="Home",
                disabled=self.route == "/",
                on_click=lambda _: self.page.go("/")
            ),
            ft.PopupMenuItem(
                text="Create a VM",
                disabled=self.route == "/create_vm",
                on_click=lambda _: self.page.go("/create_vm")
            ),
            ft.PopupMenuItem(
                text="About",
                disabled=self.route == "/about",
                on_click=lambda _: self.page.go("/about")
            )
        ]

