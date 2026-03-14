import tkinter as tk
from tkinter import ttk
import math
import time
import json
import os
import sys
from pynput import keyboard
import ctypes

# sets relative path to app icon
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MortarCalc:
    def __init__(self):
        self.config_file = "pubg_mortar_calculator.json"
        self.root = tk.Tk()
        self.root.title("PUBG Mortar Calculator")

        # --- THE DARK TITLE BAR FIX (Windows 10/11) ---
        self.root.update() # Required to get the window handle
        try:
            # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            dark_mode = ctypes.c_int(1)
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode))
        except:
            pass # Fails gracefully on non-Windows systems
        # ----------------------------------------------
        
        # Ensure the root window itself is black
        self.root.attributes("-topmost", True)
        self.root.config(padx=15, pady=15, bg="#1a1a1a")

        self.icon_path = resource_path("app.ico")
        self.set_all_icons(self.root)

        # --- THE MISSING STYLE TWEAKS ---
        style = ttk.Style()
        # 'alt' or 'clam' allows better color customization on Windows
        style.theme_use('alt')
        style.configure("TLabel", background="#1a1a1a", foreground="#FFFFFF", font=("Consolas", 10, "bold"))
        style.configure("TButton", font=("Consolas", 9, "bold"), background="#333333", foreground="#FFFFFF")
        style.map("TButton",
                  background=[('active', '#121212'), ('pressed', '#000000')], # Gets DARKER on hover
                  foreground=[('active', '#FFFFFF')])
        style.configure("Horizontal.TScale", background="#1a1a1a")
        style.configure("TSeparator", background="#FFFFFF")

        # Define variables BEFORE loading
        self.pixel_to_meter_ratio = 1.0 
        self.ui_scale = 1.0 
        self.overlay_opacity = 0.3
        self.mode = "calibrate"
        self.is_overlay_active = False
        self.last_distance = "Ready"
        self.last_press_time = 0
        self.selection_obj = None
        self.overlay_x = 50 # Default start X
        self.overlay_y = 50 # Default start Y

        self.load_settings()
        self.setup_result_window()
        self.setup_overlay_window()

        # Changed Arial to Consolas here
        ttk.Label(self.root, text="--- UI SCALING ---", font=("Consolas", 10, "bold")).pack(pady=5)
        
        self.scale_label = ttk.Label(self.root, text=f"Scale: {self.ui_scale:.1f}x")
        self.scale_label.pack()

        self.scale_slider = ttk.Scale(
            self.root, from_=0.5, to=3.0, orient="horizontal", command=self.update_ui_scale
        )
        self.scale_slider.set(self.ui_scale) 
        self.scale_slider.pack(fill="x", pady=5)

        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=10)

        # Buttons
        ttk.Button(self.root, text="Toggle Overlay Visibility", command=self.toggle_label_visibility).pack(fill="x", pady=2)
        ttk.Button(self.root, text="Reset Overlay Position", command=self.reset_overlay_pos).pack(fill="x", pady=2)
        ttk.Button(self.root, text="Reset Overlay Scaling", command=self.reset_ui_scale).pack(fill="x", pady=2)
        ttk.Button(self.root, text="Reset Calibration", command=self.reset_calibration).pack(fill="x", pady=2)
        
        # Added a little spacer for visual clarity
        ttk.Label(self.root, text="").pack()
        
        ttk.Button(self.root, text="Exit & Save", command=self.safe_exit).pack(fill="x", pady=10)

        # Centering Logic
        self.root.update_idletasks()
        width = 350
        height = 350 # Bumped height slightly to fit the new layout/fonts
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+s': lambda: self.root.after_idle(self.toggle_calibrate),
            '<alt>+s': lambda: self.root.after_idle(self.toggle_measure)
        })
        self.listener.start()

    def set_all_icons(self, window):
        try:
            window.iconbitmap(self.icon_path)
        except:
            pass

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.ui_scale = data.get("ui_scale", 1.0)
                    self.pixel_to_meter_ratio = data.get("ratio", 1.0)
                    # load default position to 50, 50 if not found
                    self.overlay_x = data.get("overlay_x", 50)
                    self.overlay_y = data.get("overlay_y", 50)
            except:
                self.set_default_state()
        else:
            self.set_default_state()

    def set_default_state(self):
        self.ui_scale = 1.0
        self.pixel_to_meter_ratio = 1.0
        self.overlay_x = 50
        self.overlay_y = 50

    def reset_overlay_pos(self):
        """Snaps the result window back to 50, 50."""
        w = self.res_win.winfo_width()
        h = self.res_win.winfo_height()
        self.res_win.geometry(f"{w}x{h}+50+50")
        self.save_settings()

    def reset_ui_scale(self):
        """Snaps UI scale back to 1.0 and refreshes all windows."""
        self.ui_scale = 1.0
        self.scale_slider.set(1.0) # This will automatically trigger self.update_ui_scale
        self.save_settings()

    def save_settings(self):
        # Capture current window position before saving
        current_x = self.res_win.winfo_x()
        current_y = self.res_win.winfo_y()
        
        data = {
            "ui_scale": self.ui_scale,
            "ratio": self.pixel_to_meter_ratio,
            "overlay_x": current_x,
            "overlay_y": current_y
        }
        with open(self.config_file, "w") as f:
            json.dump(data, f)

    def safe_exit(self):
        self.save_settings()
        self.root.destroy()

    def update_ui_scale(self, value):
        self.ui_scale = float(value)
        self.scale_label.config(text=f"Scale: {self.ui_scale:.1f}x")
        
        new_w = int(200 * self.ui_scale)
        new_h = int(70 * self.ui_scale)
        self.res_win.geometry(f"{new_w}x{new_h}")
        
        new_font_size = int(10 * self.ui_scale)
        self.label.config(font=("Consolas", new_font_size, "bold"))

    def setup_result_window(self):
        self.res_win = tk.Toplevel(self.root)
        self.res_win.overrideredirect(True)
        self.res_win.attributes("-topmost", True)
        self.res_win.config(bg="#1a1a1a")
        self.set_all_icons(self.res_win)
        
        # Apply the loaded position and current scale
        w = int(200 * self.ui_scale)
        h = int(70 * self.ui_scale)
        self.res_win.geometry(f"{w}x{h}+{self.overlay_x}+{self.overlay_y}")
        
        self.label = tk.Label(
            self.res_win, text="Ctrl+Alt+S to Calibrate", 
            bg="#1a1a1a", fg="#00FF00", font=("Consolas", 10, "bold")
        )
        self.label.pack(expand=True, fill="both")
        self.label.bind("<Button-1>", self.start_window_drag)
        self.label.bind("<B1-Motion>", self.do_window_drag)

    def setup_overlay_window(self):
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-alpha", self.overlay_opacity)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-topmost", True)
        self.overlay.config(cursor="cross")
        self.set_all_icons(self.overlay)
        self.overlay.withdraw()
        self.overlay.bind("<Escape>", lambda e: self.close_overlay())

        self.canvas = tk.Canvas(self.overlay, bg="grey", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def toggle_label_visibility(self):
        if self.res_win.winfo_viewable(): self.res_win.withdraw()
        else: self.res_win.deiconify()

    def reset_calibration(self):
        self.pixel_to_meter_ratio = 1.0
        self.label.config(text="CALIBRATION RESET\nUse Ctrl+Alt+S")

    def debounce(self):
        curr = time.time()
        if curr - self.last_press_time > 0.3:
            self.last_press_time = curr
            return True
        return False

    def toggle_calibrate(self):
        if self.debounce():
            if self.is_overlay_active and self.mode == "calibrate": self.close_overlay()
            else: self.open_overlay("calibrate")

    def toggle_measure(self):
        if self.debounce():
            if self.is_overlay_active and self.mode == "measure": self.close_overlay()
            else: self.open_overlay("measure")

    def open_overlay(self, mode):
        self.mode = mode
        self.is_overlay_active = True
        self.canvas.delete("all")
        self.overlay.deiconify()
        self.label.config(text=f"MODE: {mode.upper()}\nClick & Drag")

    def close_overlay(self):
        self.is_overlay_active = False
        self.overlay.withdraw()
        self.label.config(text=f"DIST: {self.last_distance}\nAlt+S to Measure")
        self.save_settings()

    def start_window_drag(self, event):
        self.x_off, self.y_off = event.x, event.y

    def do_window_drag(self, event):
        x = self.res_win.winfo_x() + (event.x - self.x_off)
        y = self.res_win.winfo_y() + (event.y - self.y_off)
        self.res_win.geometry(f"+{x}+{y}")

    def on_click(self, event):
        self.canvas.delete("all")
        self.start_x, self.start_y = event.x, event.y
        line_w = max(1, int(2 * self.ui_scale))
        
        if self.mode == "calibrate":
            self.selection_obj = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y, outline="lime", width=line_w
            )
        else:
            self.selection_obj = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y, fill="cyan", width=line_w
            )

    def on_drag(self, event):
        if self.selection_obj:
            self.canvas.coords(self.selection_obj, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        dx, dy = event.x - self.start_x, event.y - self.start_y
        if self.mode == "calibrate":
            dist_px = abs(dx)
            if dist_px > 5:
                self.pixel_to_meter_ratio = 100.0 / dist_px
                self.mode = "measure"
                self.label.config(text="CALIBRATED!\nDrag Line to Target")
                self.save_settings()
                self.canvas.delete("all")
        else:
            dist_px = math.hypot(dx, dy)
            if dist_px > 2:
                dist_m = dist_px * self.pixel_to_meter_ratio
                self.last_distance = f"{int(dist_m)}m"
                self.label.config(text=f"DISTANCE: {self.last_distance}\nEsc to Close")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.safe_exit)
        self.root.mainloop()

if __name__ == "__main__":
    app = MortarCalc()
    app.run()