import tkinter as tk
from tkinter import ttk, messagebox, font
import subprocess
import sys
import os
from datetime import datetime

class ModernLinuxGuide:
    def __init__(self):
        # Modern Color Palette
        self.colors = {
            'primary': '#2C3E50',       # Dark Blue-Gray
            'secondary': '#3498DB',      # Bright Blue
            'accent': '#E74C3C',        # Red
            'success': '#27AE60',       # Green
            'warning': '#F39C12',       # Orange
            'background': '#ECF0F1',    # Light Gray
            'surface': '#FFFFFF',       # White
            'text_primary': '#2C3E50',  # Dark
            'text_secondary': '#7F8C8D', # Gray
            'hover': '#34495E',         # Darker Blue-Gray
            'gradient_start': '#667eea', # Blue gradient start
            'gradient_end': '#764ba2'    # Purple gradient end
        }
        
        # Check dependencies first
        self.check_dependencies()
        
        # Load commands
        self.all_commands = self.load_commands("commands_clean.txt")
        
        # Initialize GUI
        self.create_modern_gui()
        
    def check_dependencies(self):
        """Enhanced dependency checking with modern styling"""
        self.arabic_reshaper = self.check_and_import("arabic_reshaper")
        self.bidi = self.check_and_import("bidi.algorithm")
        self.get_display = getattr(self.bidi, "get_display", lambda x: x) if self.bidi else lambda x: x
        
        # Check pip dependencies
        required_pip = ["arabic_reshaper", "bidi"]
        missing_pip = [pkg for pkg in required_pip if self.check_and_import(pkg) is None]
        
        if missing_pip:
            self.show_modern_warning("Missing Python Packages", 
                                   f"Required packages: {', '.join(missing_pip)}\n"
                                   "Run: pip install " + " ".join(missing_pip))
    
    def check_and_import(self, package_name):
        """Import package with error handling"""
        try:
            return __import__(package_name)
        except ImportError:
            return None
    
    def show_modern_warning(self, title, message):
        """Show warning with modern styling"""
        warning_window = tk.Toplevel()
        warning_window.title(title)
        warning_window.geometry("400x200")
        warning_window.configure(bg=self.colors['background'])
        warning_window.resizable(False, False)
        
        # Center the window
        warning_window.transient()
        warning_window.grab_set()
        
        # Warning icon and message
        frame = tk.Frame(warning_window, bg=self.colors['background'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="⚠️", font=('Arial', 24), 
                bg=self.colors['background'], fg=self.colors['warning']).pack(pady=10)
        
        tk.Label(frame, text=title, font=('Arial', 12, 'bold'),
                bg=self.colors['background'], fg=self.colors['text_primary']).pack()
        
        tk.Label(frame, text=message, font=('Arial', 10),
                bg=self.colors['background'], fg=self.colors['text_secondary'],
                wraplength=350, justify='center').pack(pady=10)
        
        # OK Button
        ok_btn = tk.Button(frame, text="OK", command=warning_window.destroy,
                          bg=self.colors['secondary'], fg='white',
                          font=('Arial', 10, 'bold'), padx=20, pady=5,
                          relief='flat', cursor='hand2')
        ok_btn.pack(pady=10)
        
    def fix_arabic(self, text):
        """Fix Arabic text direction and shaping"""
        if self.arabic_reshaper:
            try:
                reshaped = self.arabic_reshaper.reshape(text)
                return self.get_display(reshaped)
            except:
                pass
        return text
    
    def load_commands(self, file_path):
        """Load commands from file with error handling"""
        if not os.path.exists(file_path):
            # Create sample commands if file doesn't exist
            sample_commands = [
                ("ls -la", "عرض جميع الملفات والمجلدات مع التفاصيل"),
                ("cd /path", "تغيير المجلد الحالي"),
                ("pwd", "عرض المسار الحالي"),
                ("mkdir folder", "إنشاء مجلد جديد"),
                ("rmdir folder", "حذف مجلد فارغ"),
                ("cp file dest", "نسخ ملف إلى مكان آخر"),
                ("mv file dest", "نقل أو إعادة تسمية ملف"),
                ("rm file", "حذف ملف"),
                ("cat file", "عرض محتوى الملف"),
                ("grep pattern file", "البحث عن نمط في ملف"),
                ("find /path -name file", "البحث عن ملف"),
                ("chmod 755 file", "تغيير صلاحيات الملف"),
                ("chown user:group file", "تغيير مالك الملف"),
                ("ps aux", "عرض العمليات الجارية"),
                ("top", "عرض العمليات في الوقت الفعلي"),
                ("kill PID", "إنهاء عملية معينة"),
                ("df -h", "عرض مساحة القرص الصلب"),
                ("du -sh", "عرض حجم المجلد"),
                ("free -h", "عرض استخدام الذاكرة"),
                ("uname -a", "عرض معلومات النظام")
            ]
            return sample_commands
        
        commands = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        cmd, desc = map(str.strip, line.strip().split(':', 1))
                        commands.append((cmd, desc))
        except Exception as e:
            self.show_modern_warning("Error Loading File", f"Could not load {file_path}: {str(e)}")
            return []
        
        return commands
    
    def create_modern_gui(self):
        """Create modern GUI with advanced styling"""
        self.root = tk.Tk()
        self.root.title("🐧 Linux Command Reference - Professional Edition")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.colors['background'])
        self.root.minsize(800, 600)
        
        # Configure modern fonts
        self.title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        self.normal_font = font.Font(family="Segoe UI", size=10)
        self.button_font = font.Font(family="Segoe UI", size=9, weight="bold")
        
        # Configure modern style for ttk widgets
        self.setup_modern_style()
        
        # Create main layout
        self.create_header()
        self.create_search_section()
        self.create_main_content()
        self.create_footer()
        
        # Initialize with all commands
        self.update_tree(self.all_commands)
        
        # Bind events
        self.bind_events()
        
    def setup_modern_style(self):
        """Setup modern styling for ttk widgets"""
        style = ttk.Style()
        
        # Configure Treeview style
        style.configure("Modern.Treeview",
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['surface'],
                       borderwidth=0,
                       rowheight=30)
        
        style.configure("Modern.Treeview.Heading",
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat',
                       borderwidth=0)
        
        # Configure frame styles
        style.configure("Card.TFrame",
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=1)
        
    def create_header(self):
        """Create modern header with better visibility"""
        header = tk.Frame(self.root, height=100, bg=self.colors['primary'])
        header.pack(fill='x')
        header.pack_propagate(False)

        # Title with icon
        title_frame = tk.Frame(header, bg=self.colors['primary'])
        title_frame.pack(expand=True)

        title_label = tk.Label(title_frame, 
                          text="🐧 Linux Command Reference",
                          font=("Segoe UI", 20, "bold"),  # حجم أكبر وخط أعرض
                          bg=self.colors['primary'],
                          fg='white')
        title_label.pack(pady=(20, 5))

        subtitle_label = tk.Label(title_frame,
                             text="Professional Command Line Guide",
                             font=('Segoe UI', 12),
                             bg=self.colors['primary'],
                             fg=self.colors['text_secondary'])
        subtitle_label.pack()

    
    def create_search_section(self):
        """Create modern search section with full-width input"""
        search_frame = tk.Frame(self.root, bg=self.colors['background'])
        search_frame.pack(fill='x', padx=20, pady=(10, 0))

        # Title label
        search_label = tk.Label(search_frame, 
                            text="🔍 Search Commands:",
                            font=self.button_font,
                            bg=self.colors['background'],
                            fg=self.colors['text_primary'])
        search_label.pack(anchor='w', pady=(0, 5))

        # Container for entry + button
        search_container = tk.Frame(search_frame, bg=self.colors['background'])
        search_container.pack(fill='x')

        self.search_var = tk.StringVar()

        # Search Entry – fully expanded
        self.search_entry = tk.Entry(search_container,
                                 textvariable=self.search_var,
                                 font=('Segoe UI', 13),
                                 relief='flat',
                                 bg='white',
                                 fg=self.colors['text_primary'],
                                 insertbackground=self.colors['secondary'],
                                 bd=2)
        self.search_entry.pack(side='left', fill='x', expand=True, ipady=10)

        # Clear button next to it
        clear_btn = tk.Button(search_container,
                          text="✖ Clear",
                          command=self.clear_search,
                          bg=self.colors['accent'],
                          fg='white',
                          font=self.button_font,
                          relief='flat',
                          padx=15,
                          pady=8,
                          cursor='hand2')
        clear_btn.pack(side='left', padx=(10, 0))

        # Bind search events
        self.search_var.trace_add("write", self.search_commands)


        
    def create_main_content(self):
        """Create main content area with modern treeview"""
        content_frame = tk.Frame(self.root, bg=self.colors['background'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Commands container
        commands_container = tk.Frame(content_frame, bg=self.colors['surface'], relief='flat', bd=1)
        commands_container.pack(fill='both', expand=True)
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(commands_container, bg=self.colors['surface'])
        tree_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Create Treeview
        columns = ('command', 'description')
        self.tree = ttk.Treeview(tree_frame, 
                                columns=columns,
                                show='headings',
                                style="Modern.Treeview",
                                height=15)
        
        # Configure columns
        self.tree.heading('command', text='💻 Command', anchor='w')
        self.tree.heading('description', text='📝 Description (Arabic)', anchor='w')
        self.tree.column('command', width=250, minwidth=200)
        self.tree.column('description', width=600, minwidth=400)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
    def create_footer(self):
        """Create modern footer with status and actions"""
        footer = tk.Frame(self.root, bg=self.colors['surface'], height=60)
        footer.pack(fill='x')
        footer.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(footer,
                                    text="Ready - Click on a command to copy it",
                                    font=self.normal_font,
                                    bg=self.colors['surface'],
                                    fg=self.colors['text_secondary'],
                                    anchor='w')
        self.status_label.pack(side='left', padx=20, pady=15)
        
        # Action buttons
        button_frame = tk.Frame(footer, bg=self.colors['surface'])
        button_frame.pack(side='right', padx=20, pady=10)
        
        # Copy button
        self.copy_btn = tk.Button(button_frame,
                                 text="📋 Copy Selected",
                                 command=self.copy_command,
                                 bg=self.colors['success'],
                                 fg='white',
                                 font=self.button_font,
                                 relief='flat',
                                 padx=15,
                                 pady=8,
                                 cursor='hand2')
        self.copy_btn.pack(side='right', padx=(10, 0))
        
        # Refresh button
        refresh_btn = tk.Button(button_frame,
                               text="🔄 Refresh",
                               command=self.refresh_commands,
                               bg=self.colors['secondary'],
                               fg='white',
                               font=self.button_font,
                               relief='flat',
                               padx=15,
                               pady=8,
                               cursor='hand2')
        refresh_btn.pack(side='right')
        
    def bind_events(self):
        """Bind events for modern interactions"""
        # Treeview selection
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        # تغيير هنا: استبدال النقر المزدوج بنقرة واحدة
        self.tree.bind('<ButtonRelease-1>', lambda e: self.copy_command())
        
        # Hover effects for buttons
        self.add_hover_effect(self.copy_btn, self.colors['success'], '#219A52')
        
    def add_hover_effect(self, widget, normal_color, hover_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            widget.configure(bg=hover_color)
        
        def on_leave(e):
            widget.configure(bg=normal_color)
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
        
    def search_commands(self, *args):
        """Search commands with highlighting"""
        query = self.search_var.get().lower().strip()
        if not query:
            self.update_tree(self.all_commands)
            return
        
        # Filter commands
        filtered = []
        for cmd, desc in self.all_commands:
            if query in cmd.lower() or query in desc.lower():
                filtered.append((cmd, desc))
        
        self.update_tree(filtered)
        self.update_status(f"Found {len(filtered)} commands matching '{query}'", 'info')
        
    def clear_search(self):
        """Clear search and show all commands"""
        self.search_var.set("")
        self.search_entry.focus()
        
    def update_tree(self, commands):
        """Update treeview with commands"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        for cmd, desc in commands:
            fixed_desc = self.fix_arabic(desc)
            self.tree.insert('', 'end', values=(cmd, fixed_desc))
        
        # Update status
        if not commands:
            self.update_status("No commands found", 'warning')
        else:
            self.update_status(f"Showing {len(commands)} commands", 'success')
    
    def on_select(self, event=None):
        """Handle treeview selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            command = item['values'][0] if item['values'] else ""
            self.update_status(f"Selected: {command}", 'info')
    
    def copy_command(self):
        """Copy selected command to clipboard"""
        selection = self.tree.selection()
        if not selection:
            self.update_status("⚠️ No command selected", 'warning')
            return
        
        item = self.tree.item(selection[0])
        if not item['values']:
            return
            
        command = item['values'][0]
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(command)
        
        # Update status with success message
        self.update_status(f"✅ Copied: {command}", 'success')
        
    def refresh_commands(self):
        """Refresh command list"""
        self.all_commands = self.load_commands("commands_clean.txt")
        self.update_tree(self.all_commands)
        self.search_var.set("")
        self.update_status("✅ Commands refreshed", 'success')
        
    def update_status(self, message, status_type='info'):
        """Update status label with colored message"""
        colors = {
        'success': self.colors['success'],
        'warning': self.colors['warning'],
        'error': self.colors['accent'],
        'info': self.colors['text_secondary']
        }
    
        color = colors.get(status_type, self.colors['text_secondary'])
        self.status_label.config(text=message, fg=color)
        self.status_label.update_idletasks()  # << مهم جداً لإجبار التحديث الفوري

        # Auto-clear status after 5 seconds for non-info messages
        if status_type != 'info':
            self.root.after(5000, lambda: self.status_label.config(
                text="Ready - Click on a command to copy it",
                fg=self.colors['text_secondary']
            ))

    
    def run(self):
        """Run the application"""
        try:
            # Center the window
            self.root.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
            y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
            self.root.geometry(f"+{x}+{y}")
            
            # Start the main loop
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("\nApplication terminated by user")
            sys.exit(0)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            sys.exit(1)

# --- Main Execution ---
if __name__ == "__main__":
    try:
        app = ModernLinuxGuide()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)
