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
        with open('interface_view.spec') as ivr:
            return ivr.read()
    except FileNotFoundError:
        with open('interface_view.spec', 'w') as ivw:
            return ivw.write('console')


def verify_interface_view() -> Any | None:
    """
    Function for selecting the interface view
    :return: Any | None
    """
    create_path()
    if read_interface_view() == 'console':
        return csl.download_video()
    if read_interface_view() == 'app':
        app = App()
        return app.mainloop()
    else:
        return csl.download_video()


def main() -> None:
    """Entry point"""
    verify_interface_view()


if __name__ == '__main__':
    main()
