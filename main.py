import tkinter as tk
from script_center import ScriptCenter
from recon_center import ReconCenter


def open_script_center():
    global script_center_app
    root.withdraw()  # Hide the main root window
    script_center_app = ScriptCenter()
    script_center_app.protocol("WM_DELETE_WINDOW", close_script_center)


def close_script_center():
    root.deiconify()  # Restore the main root window
    # Restore the close button behavior
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    script_center_app.destroy()


def open_recon_center():
    global close_recon_center
    root.withdraw()  # Hide the main root window
    close_recon_center = ReconCenter()
    close_recon_center.protocol("WM_DELETE_WINDOW", close_script_center)


def close_recon_center():
    root.deiconify()  # Restore the main root window
    # Restore the close button behavior
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    close_recon_center.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("400x400")
    button_font = ("Arial", 18, "bold")

    script_center_button = tk.Button(
        root, text="Script Center", command=open_script_center, font=button_font, height=3)
    script_center_button.pack(pady=20)

    recon_button = tk.Button(
        root, text="Recon Center", command=open_recon_center, font=button_font, height=3)
    recon_button.pack(pady=20)

    analyze_button = tk.Button(
        root, text="Analyze Center", command=None, font=button_font, height=3)
    analyze_button.pack(pady=20)

    root.mainloop()
