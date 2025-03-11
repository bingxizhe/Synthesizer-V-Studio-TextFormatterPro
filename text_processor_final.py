import re
import tkinter as tk
import pyperclip
from tkinter import ttk, scrolledtext, messagebox

class TextProcessorApp:
    def __init__(self, master):
        self.master = master
        master.title("智能文本处理器 v4.0")
        master.geometry("1000x800")
        
        self.create_widgets()
        self.setup_style()
        self.setup_bindings()
        
    def setup_style(self):
        style = ttk.Style()
        style.configure("TButton", padding=8, font=('微软雅黑', 11))
        style.configure("TLabel", font=('微软雅黑', 11))
        style.map("TButton",
                foreground=[('pressed', 'white'), ('active', 'white')],
                background=[('pressed', '#45B39D'), ('active', '#45B39D')])
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 输入区
        input_frame = ttk.LabelFrame(main_frame, text="输入文本")
        input_frame.pack(fill=tk.X, pady=10)
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            height=12,
            font=('宋体', 12),
            undo=True
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # 控制面板
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            control_frame,
            text="处理剪贴板",
            command=self.process_clipboard
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="处理文本",
            command=self.process_text
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="清空内容",
            command=self.clear_all
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="复制结果",
            command=self.copy_result
        ).pack(side=tk.RIGHT, padx=5)
        
        # 输出区
        output_frame = ttk.LabelFrame(main_frame, text="处理结果")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            height=18,
            font=('宋体', 12),
            state="disabled"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_bindings(self):
        self.master.bind("<Control-v>", lambda e: self.paste_to_input())
        self.master.bind("<Control-c>", lambda e: self.copy_result())
        
    def enhanced_spacing(self, text):
        """智能文本处理引擎"""
        # 保护英文内容（支持don't、passer-by等格式）
        protected = []
        def protect_english(match):
            protected.append(match.group(0))
            return f"\uE000{len(protected)-1}\uE001"
        
        # 改进的正则表达式（支持'’‘’三种引号和连字符）
        english_pattern = r"\b[a-zA-Z]+(?:['’‘’-][a-zA-Z]+)*\b"
        text = re.sub(english_pattern, protect_english, text)
        
        # 处理CJK字符
        cjk_ranges = [
            (0x2E80, 0x2E99), (0x2E9B, 0x2EF3), (0x2F00, 0x2FD5),
            (0x3000, 0x303F), (0x4E00, 0x9FFF), (0x3400, 0x4DBF),
            (0xF900, 0xFAFF), (0xFE30, 0xFE4F)
        ]
        cjk_pattern = "".join(fr"{chr(s)}-{chr(e)}" for s, e in cjk_ranges)
        processed = re.sub(fr"([{cjk_pattern}])", r" \1 ", text)
        
        # 恢复被保护的英文
        def restore_english(match):
            index = int(match.group(1))
            return protected[index]
            
        processed = re.sub(r"\uE000(\d+)\uE001", restore_english, processed)
        
        # 清理多余空格
        processed = re.sub(r"\s+", " ", processed)
        processed = re.sub(r" ([.,!?%:;’‘“”])", r"\1", processed)
        return processed.strip()
    
    def process_text(self):
        """处理输入框文本"""
        try:
            input_str = self.input_text.get("1.0", tk.END).strip()
            if not input_str:
                messagebox.showwarning("提示", "输入文本不能为空")
                return
            
            processed = self.enhanced_spacing(input_str)
            
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, processed)
            self.output_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("处理错误", f"发生意外错误：{str(e)}")
    
    def process_clipboard(self):
        """自动处理剪贴板内容"""
        try:
            clipboard_content = pyperclip.paste().strip()
            if not clipboard_content:
                messagebox.showwarning("提示", "剪贴板中没有文本内容")
                return
            
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, clipboard_content)
            self.process_text()
            
            output_str = self.output_text.get("1.0", tk.END).strip()
            if output_str:
                pyperclip.copy(output_str)
                
        except Exception as e:
            messagebox.showerror("错误", f"剪贴板操作失败：{str(e)}")
    
    def copy_result(self):
        """智能复制功能"""
        try:
            # 检查是否有选中文本
            selected = self.output_text.tag_ranges(tk.SEL)
            if selected:
                # 复制选中部分
                start, end = selected
                text = self.output_text.get(start, end)
            else:
                # 复制全部内容
                text = self.output_text.get("1.0", tk.END).strip()
                
            if text:
                pyperclip.copy(text)
        except Exception as e:
            messagebox.showerror("错误", f"复制失败：{str(e)}")
    
    def paste_to_input(self):
        """粘贴到输入框"""
        try:
            clipboard_content = pyperclip.paste()
            self.input_text.insert(tk.INSERT, clipboard_content)
        except Exception as e:
            messagebox.showerror("错误", f"粘贴失败：{str(e)}")
    
    def clear_all(self):
        """清空所有内容"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextProcessorApp(root)
    root.mainloop()