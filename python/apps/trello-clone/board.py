import itertools
from flet import (
    UserControl,
    Column,
    Row,
    FloatingActionButton,
    Text,
    GridView,
    Container,
    TextField,
    AlertDialog,
    Container,
    icons,
    border_radius,
    border,
    colors,
    padding,
    alignment,
    margin
)
from board_list import BoardList


class Board(UserControl):
    id_counter = itertools.count()

    def __init__(self, app, identifier: str):
        super().__init__()
        self.board_id = next(BoardList.id_counter)
        self.app = app
        self.visible = False
        self.identifier = identifier
        self.nav_rail_index = None
        self.add_list_button = FloatingActionButton(
            icon=icons.ADD, text="add a list", height=30, on_click=self.addListDlg)

        self.board_lists = [
            Container(
                bgcolor=colors.BLACK26,
                border_radius=border_radius.all(30),
                height=100,
                alignment=alignment.center_right,
                width=3,
                opacity=0.0
            ),

            self.add_list_button
        ]
        for l in self.app.store.get_lists_by_board(self.board_id):
            self.add_list(l)

        self.list_wrap = Row(
            self.board_lists,
            vertical_alignment="start",
            visible=True,
            scroll="auto",
            width=(self.app.page.width - 315),
            height=(self.app.page.height - 95)
        )

    def build(self):
        self.view = Container(
            content=Column(
                controls=[
                    self.list_wrap
                ],

                scroll="auto",
                expand=True
            ),
            data=self,
            margin=margin.all(0),
            padding=padding.only(top=10, right=0),
            height=self.app.page.height,
        )
        return self.view

    def resize(self, width, height):
        self.list_wrap.width = width
        self.view.height = height
        self.list_wrap.update()
        self.view.update()

    def addListDlg(self, e):

        option_dict = {
            colors.LIGHT_GREEN: self.color_option_creator(colors.LIGHT_GREEN),
            colors.RED_200: self.color_option_creator(colors.RED_200),
            colors.PINK_300: self.color_option_creator(colors.PINK_300),
            colors.AMBER_500: self.color_option_creator(colors.AMBER_500),
            colors.ORANGE_300: self.color_option_creator(colors.ORANGE_300),
            colors.DEEP_ORANGE_300: self.color_option_creator(colors.DEEP_ORANGE_300),
            colors.PURPLE_100: self.color_option_creator(colors.PURPLE_100),
            colors.TEAL_500: self.color_option_creator(colors.TEAL_500),
            colors.YELLOW_400: self.color_option_creator(colors.YELLOW_400),
            colors.LIGHT_BLUE: self.color_option_creator(colors.LIGHT_BLUE),
            colors.PURPLE_400: self.color_option_creator(colors.PURPLE_400),
            colors.BROWN_300: self.color_option_creator(colors.BROWN_300),
            colors.CYAN_500: self.color_option_creator(colors.CYAN_500),
            colors.BLUE_GREY_500: self.color_option_creator(colors.BLUE_GREY_500),
            colors.GREEN_500: self.color_option_creator(colors.GREEN_500),
        }

        def set_color(e):
            color_options.data = e.control.data
            for k, v in option_dict.items():
                if k == e.control.data:
                    v.border = border.all(3, colors.BLACK26)
                else:
                    v.border = None
            dialog.content.update()

        color_options = GridView(
            runs_count=3, max_extent=40, data="", height=150)

        for _, v in option_dict.items():
            v.on_click = set_color
            color_options.controls.append(v)

        def close_dlg(e):
            new_list = BoardList(self, e.control.value,
                                 color=color_options.data)
            self.add_list(new_list)
            self.app.store.add_list(self.board_id, new_list)
            dialog.open = False
            self.app.page.update()
            self.update()

        dialog = AlertDialog(
            title=Text("Name your new list"),
            content=Column([
                Container(content=TextField(label="New List Name", on_submit=close_dlg),
                          padding=padding.symmetric(horizontal=5)),
                color_options
            ], tight=True, alignment="center"),

            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.app.page.dialog = dialog
        dialog.open = True
        self.app.page.update()

    def remove_list(self, list: BoardList, e):
        # add confirmation ?
        i = self.board_lists.index(list)
        # delete both list and divider
        del self.board_lists[i:i+2]
        self.app.store.remove_list(self.board_id, list.board_list_id)
        self.update()

    def add_list(self, list: BoardList):
        divider = Container(
            bgcolor=colors.BLACK26,
            border_radius=border_radius.all(30),
            height=100,
            alignment=alignment.center_right,
            width=3,
            opacity=0.0
        )
        # insert both list and divider
        self.board_lists[-1:-1] = [list, divider]

    def move_board(self, list: BoardList, displacement: int):
        i = self.boardList.index(list)
        listToMove = self.boardList.pop(i)
        self.boardList.insert(i + displacement, list)

    def color_option_creator(self, color: str):
        return Container(
            bgcolor=color,
            border_radius=border_radius.all(50),
            height=10,
            width=10,
            padding=padding.all(5),
            alignment=alignment.center,
            data=color
        )