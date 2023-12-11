def center_window(window):
    """
    将窗口居中到屏幕。
    :param window: 窗口对象（Tk 或 Toplevel 实例）。
    """
    window.update_idletasks()
    window.geometry('')  # 清空固定大小，使窗口自适应
    width = window.winfo_width()
    height = window.winfo_height()
    #获取屏幕尺寸以计算布局参数，使窗口居中
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 计算居中位置
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    # 设置窗口的大小和位置
    window.geometry(f'{width}x{height}+{x}+{y}')