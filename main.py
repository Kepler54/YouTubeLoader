from os import mkdir
from typing import Any
from loader_app import App
from loader_console import ConsoleLoader

csl = ConsoleLoader()


def create_path() -> None:
    """The function creates a working folder "Download" in case of its absence"""
    try:
        mkdir('Download')
    except FileExistsError:
        pass


def read_interface_view() -> str | int:
    """
    The function returns the contents of a text file
    :return: str | int
    """
    try:
        with open('interface_view.spec', encoding='UTF-8') as ivr:
            return ivr.read()
    except FileNotFoundError:
        with open('interface_view.spec', 'w', encoding='UTF-8') as ivw:
            return ivw.write('app')


def start_app() -> None:
    app = App()
    app.resizable(False, False)
    app.get_start_image()
    app.mainloop()


def verify_interface_view() -> Any | None:
    """
    Function for selecting the interface view
    :return: Any | None
    """
    create_path()
    if read_interface_view() == 'console':
        return csl.download_video()
    if read_interface_view() == 'app':
        return start_app()
    else:
        return csl.download_video()


def main() -> None:
    """Entry point"""
    verify_interface_view()


if __name__ == '__main__':
    main()
