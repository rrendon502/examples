import importlib.util
import os
import sys
from os.path import isfile, join
from pathlib import Path

import flet as ft


class GridItem:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.examples = []
        self.description = None


class ExampleItem:
    def __init__(self):
        self.name = None
        self.file_name = None
        self.order = None
        self.example = None
        self.source_code = None


class ControlGroup:
    def __init__(self, name, label, icon, selected_icon, index):
        self.name = name
        self.label = label
        self.icon = icon
        self.selected_icon = selected_icon
        self.grid_items = []
        self.index = index

    def sort_grid_items(self):
        controls_list = []
        sorted_grid_items = []
        for grid_item in self.grid_items:
            controls_list.append(grid_item.name)
        controls_list.sort()
        for item in controls_list:
            sorted_grid_items.append(self.find_grid_item(item))

        self.grid_items = sorted_grid_items

    def find_grid_item(self, name):
        for grid_item in self.grid_items:
            if grid_item.name == name:
                return grid_item


class GalleryData:
    def __init__(self):

        self.destinations_list = [
            ControlGroup(
                name="layout",
                label="Layout",
                icon=ft.icons.GRID_VIEW,
                selected_icon=ft.icons.GRID_VIEW_SHARP,
                index=0,
            ),
            ControlGroup(
                name="navigation",
                label="Navigation",
                icon=ft.icons.MENU_SHARP,
                selected_icon=ft.icons.MENU_SHARP,
                index=1,
            ),
            ControlGroup(
                name="displays",
                label="Displays",
                icon=ft.icons.INFO_OUTLINED,
                selected_icon=ft.icons.INFO_SHARP,
                index=2,
            ),
            ControlGroup(
                name="buttons",
                label="Buttons",
                icon=ft.icons.SMART_BUTTON_SHARP,
                selected_icon=ft.icons.SMART_BUTTON_SHARP,
                index=3,
            ),
            ControlGroup(
                name="input",
                label="Input",
                icon=ft.icons.INPUT_SHARP,
                selected_icon=ft.icons.INPUT_OUTLINED,
                index=4,
            ),
            ControlGroup(
                name="dialogs",
                label="Dialogs",
                icon=ft.icons.MESSAGE_OUTLINED,
                selected_icon=ft.icons.MESSAGE_SHARP,
                index=5,
            ),
            ControlGroup(
                name="charts",
                label="Charts",
                icon=ft.icons.INSERT_CHART_OUTLINED,
                selected_icon=ft.icons.INSERT_CHART_SHARP,
                index=6,
            ),
            ControlGroup(
                name="animations",
                label="Animations",
                icon=ft.icons.ANIMATION_SHARP,
                selected_icon=ft.icons.ANIMATION_SHARP,
                index=7,
            ),
            ControlGroup(
                name="utility",
                label="Utility",
                icon=ft.icons.PAN_TOOL_OUTLINED,
                selected_icon=ft.icons.PAN_TOOL_SHARP,
                index=8,
            ),
            ControlGroup(
                name="colors",
                label="Colors",
                icon=ft.icons.FORMAT_PAINT_OUTLINED,
                selected_icon=ft.icons.FORMAT_PAINT_SHARP,
                index=9,
            ),
            ControlGroup(
                name="contrib",
                label="Contrib",
                icon=ft.icons.MY_LIBRARY_ADD_OUTLINED,
                selected_icon=ft.icons.LIBRARY_ADD_SHARP,
                index=10,
            ),
        ]
        self.import_modules()
        self.selected_control_group = self.destinations_list[0]

    def get_control_group(self, control_group_name):
        for control_group in self.destinations_list:
            if control_group.name == control_group_name:
                return control_group

    def get_control(self, control_group_name, control_name):
        control_group = self.get_control_group(control_group_name)
        for grid_item in control_group.grid_items:
            if grid_item.id == control_name:
                return grid_item

    def list_control_dirs(self, dir):
        file_path = os.path.join(str(Path(__file__).parent), dir)
        control_dirs = [
            f
            for f in os.listdir(file_path)
            if not isfile(f)
            and f not in ["index.py", "images", "__pycache__", ".venv", ".git"]
        ]
        return control_dirs

    def list_example_files(self, control_group_dir, control_dir):
        file_path = os.path.join(
            str(Path(__file__).parent), control_group_dir, control_dir
        )
        example_files = [f for f in os.listdir(file_path) if not f.startswith("_")]
        return example_files

    def import_modules(self):
        for control_group_dir in self.destinations_list:
            for control_dir in self.list_control_dirs(control_group_dir.name):
                grid_item = GridItem(control_dir)

                for file in self.list_example_files(
                    control_group_dir.name, control_dir
                ):
                    file_name = os.path.join(control_group_dir.name, control_dir, file)
                    module_name = file_name.replace("/", ".").replace(".py", "")

                    if module_name in sys.modules:
                        print(f"{module_name!r} already in sys.modules")
                    else:
                        file_path = os.path.join(str(Path(__file__).parent), file_name)

                        spec = importlib.util.spec_from_file_location(
                            module_name, file_path
                        )
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)
                        print(f"{module_name!r} has been imported")
                        if file == "index.py":
                            grid_item.name = module.name
                            grid_item.description = module.description
                        else:
                            example_item = ExampleItem()
                            example_item.example = module.example

                            example_item.file_name = (
                                module_name.replace(".", "/") + ".py"
                            )
                            example_item.name = module.name
                            example_item.order = file[
                                :2
                            ]  # first 2 characters of example file name (e.g. '01')
                            grid_item.examples.append(example_item)
                grid_item.examples.sort(key=lambda x: x.order)
                control_group_dir.grid_items.append(grid_item)
            control_group_dir.sort_grid_items()
