import tkinter as tk
from tkinter import Toplevel
from functools import wraps

def manage_window_visibility(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # 从实例中获取主窗口
        main_window = self.root

        # 隐藏主窗口
        main_window.withdraw()

        # 调用原始函数
        result = func(self, *args, **kwargs)

        # 设置子窗口关闭时的回调
        if isinstance(result, Toplevel):
            result.protocol("WM_DELETE_WINDOW", lambda: on_child_close(main_window, result))

        return result
    return wrapper

def on_child_close(main_window, child_window):
    child_window.destroy()
    main_window.deiconify()  # 重新显示主窗口
    