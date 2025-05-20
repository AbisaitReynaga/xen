import flet as ft
from controllers import VirtualMachinController,SystemController
from models import VirtualMachineModel
from components import CustomContainer




class CustomSlider(ft.Container):
    def __init__(self, type_slider:str,unit:str,min: int, max: int, divisions: int, page: ft.Page):
        self.type_slider = type_slider
        self.unit = unit
        self.min = min
        self.max = max
        self.divisions = divisions
        self.page = page

        # Controls
    
        self.lbl_txt = ft.Text(f"{self.type_slider}: ")
        self.slider = ft.Slider(
            min=self.min,
            max=self.max,
            divisions=self.divisions,
            label="{value} "+self.unit,
            on_change=self.slider_changed,
            width=400
        )
        self.left_text = ft.Text(f"{self.min} {self.unit}")
        self.right_text = ft.Text(f"{self.max} {self.unit}")

        self.value_text = ft.TextField(
            label=f"{self.unit}",
            on_change=self.textfield_changed,
            width=100,
            bgcolor="#262b40",
            color='white',
            border_color="white",
            border_radius=8

        )

        # Building the container
        super().__init__(
            width=500,
            height=100,
            content=ft.Column(
                controls=[

                    ft.Row(
                        controls=[
                            self.lbl_txt,
                            self.slider,
                            self.value_text
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.left_text,
                            self.right_text
                        ]
                    )
                ]
            )
        )
    
        # Function when the slider changes
    def slider_changed(self, e):
        self.value_text.value = str(int(e.control.value))
        try:
            self.page.update()
        except ValueError:
            self.page.update()

    # Function when the text field changes
    def textfield_changed(self, e):
        try:
            val = int(e.control.value)
            if self.min <= val <= self.max:
                self.slider.value = val
                self.page.update()
        except ValueError:
            self.page.update()

class HardwareCard(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        self.title = ft.Text(
            "Hardware",
            size=24,
            weight='bold',
            color="white"
        )

        self.vcpus = SystemController.get_total_vcpus()
        self.memory = SystemController.get_total_memory()


        # Controls
        self.vcpus_slider = CustomSlider("VCPUs", "Cores", 0, self.vcpus, self.vcpus, page)
        self.memory_slider = CustomSlider("Memory", "MB", 0, self.memory, self.memory//1024, page)




        super().__init__(
            content=ft.Column(
                controls=[
                    self.title,
                    ft.Row(
                        spacing=150,
                        controls=[
                            self.memory_slider,
                            self.vcpus_slider
                    ])
                ]
            )
        )

class StorageCard(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page
        self.title = ft.Text(
            "Storage",
            size=24,
            weight='bold',
            color="white"
        )

        self.storage = SystemController.get_total_storage()
        self.min_storage = 0  # GB mínimo recomendado
        self.max_storage = self.storage

        self.divisions = max((self.max_storage - self.min_storage) // 10, 1)  # Al menos 1 división



        # Controls
        self.storage_slider =CustomSlider("Storage", "GB", 0, self.max_storage, self.divisions, page)


        super().__init__(
            # width=400,
            # height=180,
            content=ft.Column(
                controls=[
                    self.title,
                    ft.Row(
                        spacing=150,
                        controls=[
                            self.storage_slider
                        ]
                    )
                ]
            )
        )

class FirmwareCard(ft.Container):
    def __init__(self, page: ft.Page):

        self.page = page

        # Controls
        self.title = ft.Text(
            "Firmware",
            size=24,
            weight='bold',
            color="white"
        )

        self.firmware = ft.Dropdown(
                                    editable=True,
                                    options=[
                                        ft.dropdown.Option("BIOS"),
                                        ft.dropdown.Option("UEFI")
                                    ],
                                    width=300,
                                    bgcolor="#262b40",
                                    border_color="white",
                                    color="white"
        )
       


        super().__init__(
            width=400,
            height=180,
            content=ft.Column(
                controls=[
                    self.title,
                    ft.Row(
                        spacing=150,
                        controls=[
                        self.firmware,
                        
                    ])
                ]
            )
        )


class VirtualMachinForm(ft.Container):
    def __init__(self,page:ft.Page):
        
        self.page = page

        #Controllers

        self.contoller = VirtualMachinController()
        self.system_controller = SystemController()

        # Controls

        self.title = ft.Text(
            "Create a new VM",
            size=28,
            weight='bold',
            color="white"
        )

        self.vm_name = ft.TextField(
            label="VM Name",
            hint_text="Enter the name of the VM",
            width=600,
            bgcolor="#262b40",
            border_radius=8,
            border_color="white",
            color="white",
        )

        self.iso_image = ft.Dropdown(
            editable=True,
            label="Select an ISO image",
            options=self.get_options_images(),
            width=500,
            border_color='white',
            bgcolor="#262b40",
            color="white",
            border_radius=8,

        )

        self.btn_create = ft.ElevatedButton(
            text="Create VM",
            bgcolor="#3be38b",
            color="black",
            width=200,
            height=35,
            on_click=self.create_vm,
        )

        self.hardware_card = HardwareCard(page)
        self.storage_card = StorageCard(page)
        self.firmware_card = FirmwareCard(page)


        super().__init__(
                content=ft.Column(
                    controls=[
                        self.title,
                        ft.Row(
                            spacing=100,
                            controls=[
                            self.vm_name,
                            self.iso_image
                        ]),
                        
                        self.hardware_card,

                        ft.Row(
                            spacing=300,
                            # alignment=ft.MainAxisAlignment.START,  # o CENTER
                            # vertical_alignment=ft.CrossAxisAlignment.START,  # importante
                            controls=[
                                self.storage_card,
                                self.firmware_card
                            ]
                        ),
                        self.btn_create
                    
                    ]
            ),
            bgcolor="#131926",
            border_radius=10,
            padding=ft.Padding(15, 0, 0, 0),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.BLACK54,
                offset=ft.Offset(4, 4),
                blur_style=ft.ShadowBlurStyle.NORMAL
            ),
            border=ft.border.all(2, "#262b40")
        )
    
    def get_options_images(self):
        images = self.system_controller.get_iso_images()
        options = []
        for image in images:
            options.append(ft.dropdown.Option(image))
        return options
    
    def create_vm(self,e):

        if self.is_empty_fields():
            self.page.open(
                ft.AlertDialog(
                title=ft.Text("Empty field"),
                content=ft.Text("There is a missing field, please retry again"),
                alignment=ft.alignment.center,
                bgcolor="#131926",
                
                title_padding=ft.padding.all(25),
                )
            )
        else:

            if self.contoller.vm_exists(self.vm_name.value):
                self.page.open(
                    ft.AlertDialog(
                    title=ft.Text("VM already exists"),
                    content=ft.Text("The VM name already exists, please retry again"),
                    alignment=ft.alignment.center,
                    bgcolor="#131926",
                    
                    title_padding=ft.padding.all(25),
                    )
                )
            else:
                #Create the VM model
                vm = VirtualMachineModel(
                    name=self.vm_name.value,
                    vcpus=int(self.hardware_card.vcpus_slider.slider.value),
                    memory=int(self.hardware_card.memory_slider.slider.value),
                    disk=int(self.storage_card.storage_slider.slider.value),
                    firmware=self.firmware_card.firmware.value,
                    iso_image=self.iso_image.value,
                    mac_adress=SystemController.get_random_mac(),
                    vnc_port=SystemController.get_vnc_port(),
                    status=False,
                    delete=False
                )

                self.contoller.create_vm_cfg(vm)
                self.contoller.save_vm_cfg(vm)
                self.page.open(
                    ft.AlertDialog(
                    title=ft.Text("VM created"),
                    content=ft.Text("The VM has been created successfully"),
                    alignment=ft.alignment.center,
                    bgcolor="#131926",
                    
                    title_padding=ft.padding.all(25),
                    )
                )
                self.page.go("/")   

    def is_empty_fields(self):
        if self.vm_name.value == "":
            return True
        if self.iso_image.value == None:
            return True
        if self.hardware_card.vcpus_slider.slider.value == 0:
            return True
        if self.hardware_card.memory_slider.slider.value == 0:
            return True
        if self.storage_card.storage_slider.slider.value == 0:
            return True
        if self.firmware_card.firmware.value == None:
            return True
        return False
    