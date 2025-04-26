import tkinter as tk
from tkinter import messagebox
from typing import Optional


class MessageBox:
    @staticmethod
    def showinfo(title: Optional[str] = None, message: Optional[str] = None, **options):
        """
        显示信息消息框
        :param title: 消息框标题
        :param message: 消息内容
        :param options: 其他可选参数
        :return: 消息框的返回值
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.showinfo(title, message, **options)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def showwarning(title: Optional[str] = None, message: Optional[str] = None, **options):
        """
        显示警告消息框
        :param title: 消息框标题
        :param message: 消息内容
        :param options: 其他可选参数
        :return: 消息框的返回值
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.showwarning(title, message, **options)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def showerror(title: Optional[str] = None, message: Optional[str] = None, **options):
        """
        显示错误消息框
        :param title: 消息框标题
        :param message: 消息内容
        :param options: 其他可选参数
        :return: 消息框的返回值
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.showerror(title, message, **options)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askquestion(title: Optional[str] = None, message: Optional[str] = None, **options):
        """
        显示询问消息框
        :param title: 消息框标题
        :param message: 消息内容
        :param options: 其他可选参数
        :return: 消息框的返回值
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askquestion(title, message, **options)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askokcancel(title: Optional[str] = None, message: Optional[str] = None, **options):
        """
        显示确认取消消息框
        :param title: 消息框标题
        :param message: 消息内容
        :param options: 其他可选参数
        :return: 消息框的返回值，True 表示确认，False 表示取消
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askokcancel(title, message, **options)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askyesno(title: Optional[str] = None, message: Optional[str] = None, **options):
        """
        显示是/否消息框
        :param title: 消息框标题
        :param message: 消息内容
        :param options: 其他可选参数
        :return: 消息框的返回值，True 表示是，False 表示否
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askyesno(title, message, **options)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askyesnocancel(title: Optional[str] = None, message: Optional[str] = None, **options):
        """
        显示是/否/取消消息框
        :param title: 消息框标题
        :param message: 消息内容
        :param options: 其他可选参数
        :return: 消息框的返回值，True 表示是，False 表示否，None 表示取消
        """
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askyesnocancel(title, message, **options)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askretrycancel(title: Optional[str] = None, message: Optional[str] = None, **options):
        """
        显示重试取消消息框
        :param title: 消息框标题
        :param message: 消息内容
        :param options: 其他可选参数
        :return: 消息框的返回值，True 表示重试，False 表示取消
        """
        root = tk.Tk()
        root.withdraw()
        res = messagebox.askretrycancel(title, message, **options)
        root.destroy()  # 销毁主窗口
        return res