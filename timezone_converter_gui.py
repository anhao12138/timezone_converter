import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from zoneinfo import ZoneInfo
import pytz


class TimezoneConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("时区转换工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 设置字体以确保中文显示正常
        self.font = ('SimHei', 10)

        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建标签页
        self.tab_control = ttk.Notebook(self.main_frame)

        # 当前时间标签页
        self.current_time_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.current_time_tab, text="当前时间")

        # 时间转换标签页
        self.convert_time_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.convert_time_tab, text="时间转换")

        # 时区列表标签页
        self.timezone_list_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.timezone_list_tab, text="时区列表")

        self.tab_control.pack(expand=1, fill="both")

        # 初始化各个标签页
        self.init_current_time_tab()
        self.init_convert_time_tab()
        self.init_timezone_list_tab()

        # 常用时区列表
        self.common_timezones = [
            'Asia/Shanghai',  # 北京时间
            'America/New_York',  # 纽约时间
            'Europe/London',  # 伦敦时间
            'Asia/Tokyo',  # 东京时间
            'Australia/Sydney',  # 悉尼时间
            'America/Los_Angeles',  # 洛杉矶时间
            'Europe/Moscow',  # 莫斯科时间
            'Europe/Paris',  # 巴黎时间
        ]

        # 更新当前时间
        self.update_current_time()

    def init_current_time_tab(self):
        # 创建框架
        frame = ttk.Frame(self.current_time_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # 时区选择
        ttk.Label(frame, text="选择时区:", font=self.font).grid(row=0, column=0, sticky=tk.W, pady=5)

        self.current_timezone_var = tk.StringVar(value='Asia/Shanghai')
        self.current_timezone_combo = ttk.Combobox(frame, textvariable=self.current_timezone_var, width=40)
        self.current_timezone_combo.grid(row=0, column=1, sticky=tk.W, pady=5)

        # 获取当前时间按钮
        ttk.Button(frame, text="获取当前时间", command=self.show_current_time).grid(row=0, column=2, padx=10, pady=5)

        # 当前时间显示区域
        self.current_time_label = ttk.Label(frame, text="", font=('SimHei', 16, 'bold'))
        self.current_time_label.grid(row=1, column=0, columnspan=3, pady=20)

        # 时间差计算区域
        ttk.Label(frame, text="比较时区:", font=self.font).grid(row=2, column=0, sticky=tk.W, pady=5)

        self.compare_timezone_var = tk.StringVar(value='UTC')
        self.compare_timezone_combo = ttk.Combobox(frame, textvariable=self.compare_timezone_var, width=40)
        self.compare_timezone_combo.grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Button(frame, text="计算时差", command=self.calculate_time_difference).grid(row=2, column=2, padx=10,
                                                                                        pady=5)

        self.time_difference_label = ttk.Label(frame, text="", font=self.font)
        self.time_difference_label.grid(row=3, column=0, columnspan=3, pady=5)

    def init_convert_time_tab(self):
        # 创建框架
        frame = ttk.Frame(self.convert_time_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # 输入时间
        ttk.Label(frame, text="输入时间 (YYYY-MM-DD HH:MM:SS):", font=self.font).grid(row=0, column=0, sticky=tk.W,
                                                                                      pady=5)

        self.input_time_var = tk.StringVar(value=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ttk.Entry(frame, textvariable=self.input_time_var, width=40).grid(row=0, column=1, sticky=tk.W, pady=5)

        # 源时区
        ttk.Label(frame, text="源时区:", font=self.font).grid(row=1, column=0, sticky=tk.W, pady=5)

        self.source_timezone_var = tk.StringVar(value='Asia/Shanghai')
        self.source_timezone_combo = ttk.Combobox(frame, textvariable=self.source_timezone_var, width=40)
        self.source_timezone_combo.grid(row=1, column=1, sticky=tk.W, pady=5)

        # 目标时区
        ttk.Label(frame, text="目标时区:", font=self.font).grid(row=2, column=0, sticky=tk.W, pady=5)

        self.target_timezone_var = tk.StringVar(value='UTC')
        self.target_timezone_combo = ttk.Combobox(frame, textvariable=self.target_timezone_var, width=40)
        self.target_timezone_combo.grid(row=2, column=1, sticky=tk.W, pady=5)

        # 转换按钮
        ttk.Button(frame, text="转换时间", command=self.convert_time).grid(row=3, column=0, columnspan=2, pady=10)

        # 转换结果
        self.convert_result_label = ttk.Label(frame, text="", font=self.font, wraplength=700)
        self.convert_result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def init_timezone_list_tab(self):
        # 创建框架
        frame = ttk.Frame(self.timezone_list_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # 刷新按钮
        ttk.Button(frame, text="刷新时区列表", command=self.refresh_timezone_list).grid(row=0, column=0, pady=5)

        # 创建一个带滚动条的文本框
        self.timezone_text = tk.Text(frame, wrap=tk.WORD, height=20, width=90, font=self.font)
        self.timezone_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.timezone_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.timezone_text.config(yscrollcommand=scrollbar.set)

        # 设置网格权重，使文本框能够扩展
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def update_current_time(self):
        """更新当前时间显示"""
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.current_time_label.config(text=f"本地当前时间: {current_time}")
        self.root.after(1000, self.update_current_time)

    def show_current_time(self):
        """显示所选时区的当前时间"""
        timezone = self.current_timezone_var.get()
        try:
            tz = ZoneInfo(timezone)
            current_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
            self.current_time_label.config(text=f"{timezone} 当前时间: {current_time}")
        except Exception as e:
            messagebox.showerror("错误", f"获取时间失败: {str(e)}")

    def calculate_time_difference(self):
        """计算两个时区之间的时差"""
        tz1 = self.current_timezone_var.get()
        tz2 = self.compare_timezone_var.get()

        try:
            zone1 = ZoneInfo(tz1)
            zone2 = ZoneInfo(tz2)

            # 获取两个时区的当前时间
            now1 = datetime.datetime.now(zone1)
            now2 = datetime.datetime.now(zone2)

            # 计算时差
            delta = now1 - now2
            hours_diff = delta.total_seconds() / 3600

            if hours_diff > 0:
                self.time_difference_label.config(text=f"{tz1} 比 {tz2} 快 {abs(hours_diff):.2f} 小时")
            elif hours_diff < 0:
                self.time_difference_label.config(text=f"{tz1} 比 {tz2} 慢 {abs(hours_diff):.2f} 小时")
            else:
                self.time_difference_label.config(text=f"{tz1} 和 {tz2} 时间相同")

        except Exception as e:
            messagebox.showerror("错误", f"计算时差失败: {str(e)}")

    def convert_time(self):
        """转换时间"""
        input_time = self.input_time_var.get()
        source_tz = self.source_timezone_var.get()
        target_tz = self.target_timezone_var.get()

        try:
            # 解析输入时间
            dt = datetime.datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')

            # 设置源时区
            source_zone = ZoneInfo(source_tz)
            dt = dt.replace(tzinfo=source_zone)

            # 转换为目标时区
            target_zone = ZoneInfo(target_tz)
            converted_dt = dt.astimezone(target_zone)

            # 显示结果
            result = f"{input_time} ({source_tz}) 转换为 {target_tz} 时区的时间是:\n{converted_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
            self.convert_result_label.config(text=result)

        except ValueError:
            messagebox.showerror("格式错误", "请使用 YYYY-MM-DD HH:MM:SS 格式输入时间")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")

    def refresh_timezone_list(self):
        """刷新时区列表"""
        self.timezone_text.delete(1.0, tk.END)
        self.timezone_text.insert(tk.END, "常用时区列表:\n\n")

        for tz in self.common_timezones:
            try:
                current_time = self.get_time_in_timezone(tz)
                self.timezone_text.insert(tk.END, f"- {tz}: {current_time}\n")
            except Exception as e:
                self.timezone_text.insert(tk.END, f"- {tz}: 获取时间失败 ({str(e)})\n")

    def get_time_in_timezone(self, timezone):
        """获取指定时区的当前时间"""
        tz = ZoneInfo(timezone)
        current_time = datetime.datetime.now(tz)
        return current_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')


if __name__ == "__main__":
    root = tk.Tk()
    app = TimezoneConverterApp(root)

    # Load timezone list to dropdowns (fixed line)
    all_timezones = sorted(pytz.all_timezones)  # Changed from ZoneInfo.available_timezones()
    app.current_timezone_combo['values'] = all_timezones
    app.compare_timezone_combo['values'] = all_timezones
    app.source_timezone_combo['values'] = all_timezones
    app.target_timezone_combo['values'] = all_timezones

    # 刷新时区列表
    app.refresh_timezone_list()

    root.mainloop()    