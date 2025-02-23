# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip

class TextProcessorApp:
    def __init__(self, master):
        self.master = master
        master.title("智能文本格式化工具 v2.0")
        self.setup_ui()
        
    def setup_ui(self):
        """初始化用户界面"""
        # 窗口设置
        self.master.geometry("800x600+200+100")
        self.master.resizable(True, True)
        
        # 主框架
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 配置选项区域
        self.options_frame = ttk.LabelFrame(main_frame, text="处理选项", padding=10)
        self.options_frame.pack(fill=tk.X, pady=5)
        
        # 格式保留复选框
        self.keep_format = tk.BooleanVar(value=False)
        self.format_check = ttk.Checkbutton(
            self.options_frame,
            text="保留原始格式（换行符等）",
            variable=self.keep_format
        )
        self.format_check.pack(anchor=tk.W)

        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        self.input_label = ttk.Label(input_frame, text="输入文本:")
        self.input_label.pack(anchor=tk.W)
        
        self.input_area = scrolledtext.ScrolledText(
            input_frame, 
            wrap=tk.WORD,
            height=10,
            font=('微软雅黑', 10)
        )
        self.input_area.pack(fill=tk.BOTH, expand=True, pady=5)

        # 处理按钮
        self.process_btn = ttk.Button(
            main_frame,
            text="开始处理",
            command=self.process_text
        )
        self.process_btn.pack(pady=10, ipadx=20)

        # 输出区域
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_label = ttk.Label(output_frame, text="处理结果:")
        self.output_label.pack(anchor=tk.W)
        
        self.output_area = scrolledtext.ScrolledText(
            output_frame, 
            wrap=tk.WORD,
            height=10,
            font=('微软雅黑', 10),
            state='disabled'
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=5)

        # 状态栏
        self.status_bar = ttk.Label(
            main_frame, 
            text="就绪",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def is_chinese(self, char):
        """判断字符是否为中文"""
        return '\u4e00' <= char <= '\u9fff'

    def process_text(self):
        """核心处理逻辑"""
        try:
            # 获取输入文本
            input_text = self.input_area.get("1.0", tk.END).strip()
            if not input_text:
                messagebox.showwarning("警告", "请输入需要处理的文本！")
                return

            result = []
            prev_is_chinese = False
            prev_char = None
            
            # 显示处理进度
            self.update_status("正在处理...", "blue")
            total_chars = len(input_text)
            self.master.update()

            for i, char in enumerate(input_text):
                # 处理换行符
                if char == '\n':
                    if self.keep_format.get():
                        result.append('\n')
                        prev_is_chinese = False
                        prev_char = None
                        continue
                    else:
                        char = ' '  # 替换为空格

                # 处理常规字符
                current_is_chinese = self.is_chinese(char)
                
                # 添加空格规则
                if current_is_chinese:
                    if prev_is_chinese and prev_char not in (' ', '\n'):
                        result.append(' ')
                    result.append(char)
                    prev_is_chinese = True
                else:
                    if prev_is_chinese and char != ' ':
                        result.append(' ')
                    result.append(char)
                    prev_is_chinese = False
                
                prev_char = char

                # 每处理500字符更新进度
                if i % 500 == 0 or i == total_chars-1:
                    progress = (i+1)/total_chars
                    self.update_status(f"处理进度：{progress:.0%}", "blue")

            processed_text = ''.join(result).strip()
            
            # 显示结果
            self.display_result(processed_text)
            
            # 自动复制到剪贴板
            try:
                pyperclip.copy(processed_text)
                self.update_status("处理完成，结果已自动复制到剪贴板！", "green")
            except Exception as e:
                self.update_status(f"剪贴板访问失败：{str(e)}", "red")
                messagebox.showerror("错误", f"无法复制到剪贴板，请手动复制结果\n错误信息：{str(e)}")

        except Exception as e:
            self.update_status(f"处理出错：{str(e)}", "red")
            messagebox.showerror("系统错误", f"发生未预期的错误：\n{str(e)}")

    def display_result(self, text):
        """显示处理结果"""
        self.output_area.config(state='normal')
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, text)
        self.output_area.config(state='disabled')

    def update_status(self, message, color="black"):
        """更新状态栏"""
        self.status_bar.config(text=message, foreground=color)
        self.master.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextProcessorApp(root)
    
    # 设置字体兼容性
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root.mainloop()