import flet as ft
from views import home_view


def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                home_view(page)
            )
        # elif page.route == "/create_vm":
        #     page.views.append(
        #         create_vm_view(page)
        #     )
        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
    # Si solo queda una vista, no hagas nada (o puedes cerrar la app si quieres)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(main,assets_dir="src/assets")
