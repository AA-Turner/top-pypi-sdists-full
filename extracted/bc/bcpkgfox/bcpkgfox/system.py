from selenium.webdriver.remote.webelement import WebElement
from .get_driver import RD, RESET, ORANGE
from typing import Optional
import tkinter as tk
import time
import os

class System:
    def __init__(self):
        self.button = None
        self.user_input = None

    def message_of_choices(
        self,
        message: str,
        choice_1: str,
        choice_2: str,
        title: Optional[str] = None
    ) -> int:
        def on_button(root, window, choice):
            self.button = choice
            window.destroy()
            root.destroy()

        root = tk.Tk()
        root.withdraw()

        window = tk.Toplevel(root)
        window.title(title if title else "Atenção!")
        window.configure(bg="white")

        # Centralizar e configurar tamanho
        largura, altura = 400, 200
        pos_x = (root.winfo_screenwidth() - largura) // 2
        pos_y = (root.winfo_screenheight() - altura) // 2
        window.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        window.resizable(False, False)
        window.attributes("-topmost", True)

        # Mensagem
        label = tk.Label(
            window,
            text=message,
            bg="white",
            fg="black",
            font=("Helvetica", 12),
            wraplength=380,
            justify="center"
        )
        label.pack(expand=True, padx=20, pady=20)

        # Botões
        button_frame = tk.Frame(window, bg="white")
        button_frame.pack(pady=10)

        btn1 = tk.Button(
            button_frame,
            text=choice_1,
            command=lambda: on_button(root, window, 1),
            width=10,
            font=("Helvetica", 10)
        )
        btn1.pack(side="left", padx=10)

        btn2 = tk.Button(
            button_frame,
            text=choice_2,
            command=lambda: on_button(root, window, 2),
            width=10,
            font=("Helvetica", 10)
        )
        btn2.pack(side="left", padx=10)

        window.grab_set()
        window.focus_set()
        window.wait_window()

        return self.button

    def message_of_input(
        self,
        question: str,
        title: Optional[str] = None
    ) -> str:
        def on_submit(root, window):
            self.user_input = entry.get()
            window.destroy()
            root.destroy()

        root = tk.Tk()
        root.withdraw()

        window = tk.Toplevel(root)
        window.title(title if title else "Atenção!")
        window.configure(bg="white")

        # Centralizar e configurar tamanho
        largura, altura = 400, 200
        pos_x = (root.winfo_screenwidth() - largura) // 2
        pos_y = (root.winfo_screenheight() - altura) // 2
        window.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        window.resizable(False, False)
        window.attributes("-topmost", True)

        # Mensagem
        label = tk.Label(
            window,
            text=question,
            bg="white",
            fg="black",
            font=("Helvetica", 12),
            wraplength=380,
            justify="center"
        )
        label.pack(expand=True, padx=20, pady=10)

        # Campo de entrada
        entry = tk.Entry(
            window,
            width=30,
            font=("Helvetica", 12),
            justify="center"
        )
        entry.pack(pady=10)
        entry.focus()

        # Botão de confirmação
        btn_submit = tk.Button(
            window,
            text="Próximo",
            command=lambda: on_submit(root, window),
            width=10,
            font=("Helvetica", 10)
        )
        btn_submit.pack(pady=10)

        window.grab_set()
        window.focus_set()
        window.wait_window()

        return self.user_input

    @staticmethod
    def extract_pdf(pdf_path: str = None) -> str:
        """
        Extracts and returns the text content from a PDF file.

        Args:
            pdf_path (str): The path to the PDF file to extract text from.

        Returns:
            str: The extracted text from the PDF.

        Raises:
            ValueError: If the file does not exist, is not a valid file, or if an error occurs during extraction.

        Note:
            Use `resource_path` to localize the `pdf_path` to avoid issues with pyinstaller.
        """
        import fitz
        if not pdf_path:
            raise ValueError("PDF path cannot be None.")

        if not os.path.exists(pdf_path) or not os.path.isfile(pdf_path):
            raise ValueError("File not found or is not a valid file.")

        try:
            # Use a context manager to ensure the file is properly closed
            with fitz.open(pdf_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                return text
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}") from e

    @staticmethod
    def resource_path(relative_path):
        """Get the absolute path to a resource, works for dev and for PyInstaller."""
        import sys
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def wait_for_window(self,
        object: Optional[str|list],
        timeout: Optional[int] = 10
    ) -> str | WebElement:
        """
        it function will disregrated difference between upper and lower case.
        and you can pass multiples titles to analise.

        Args:
            object (str | list): pass the window titles(s)
        """

        from .get_driver import RD, RESET
        import pygetwindow as gw

        timeout = float("inf") if timeout == 0 else timeout
        attempt = 0
        if isinstance(object, str) == True: object = [object]
        while attempt < timeout:
            for title_ in object:
                for native_title in gw.getAllTitles():
                    if title_.lower() in native_title.lower(): return gw.getWindowsWithTitle(str(native_title))
                time.sleep(1)
                attempt += 1
        raise ModuleNotFoundError("Janela não encontrada")

    def accents_remover(self, text):
        import unicodedata

        return ''.join(
            letra for letra in unicodedata.normalize('NFD', text)
            if unicodedata.category(letra) != 'Mn'
        )


