import csv
import sys
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
from pathlib import Path

# Set theme and appearance
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Tracker")
        
        # Window dimensions
        window_width = 700
        window_height = 500
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate center position
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        self.study_material = ""
        self.start_time = None
        self.timer_label = None
        self.timer_running = False
        
        self.build_start_screen()
    
    def build_start_screen(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container for centering - using place for true centering
        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(frame, text="What are you going to study?", font=("Roboto", 42, "bold")).pack(pady=(20, 20))
        
        self.entry_material = ctk.CTkTextbox(frame, width=500, height=100, font=("Roboto", 18), corner_radius=20)
        self.entry_material.pack(pady=20)
        self.entry_material.insert("1.0", "e.g. Quadratic formula homework, French review, etc.")
        self.entry_material.bind("<FocusIn>", self._clear_placeholder)
        self.entry_material.focus()
        
        ctk.CTkButton(frame, text="Start Studying", command=self.start_study, width=300, height=70, font=("Roboto", 22, "bold"), corner_radius=20).pack(pady=(20, 20))
    
    def _clear_placeholder(self, event):
        current_text = self.entry_material.get("1.0", "end-1c")
        if current_text == "e.g. Quadratic formula homework, French review, etc.":
            self.entry_material.delete("1.0", "end")
    
    def start_study(self):
        self.study_material = self.entry_material.get("1.0", "end-1c").strip()
        if not self.study_material or self.study_material == "e.g. Quadratic formula homework, French review, etc.":
            messagebox.showerror("Error", "Please enter your study material.")
            return
        
        self.start_time = datetime.now()
        self.timer_running = True
        self.build_session_screen()
        self.update_timer()
    
    def build_session_screen(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Currently Studying:", font=("Roboto", 20)).pack(pady=(40, 10))
        ctk.CTkLabel(frame, text=f"{self.study_material}", font=("Roboto", 32, "bold"), text_color="#3B8ED0").pack(pady=10)
        
        self.timer_label = ctk.CTkLabel(frame, text="00:00:00", font=("Roboto", 90, "bold"))
        self.timer_label.pack(pady=60)
        
        ctk.CTkButton(frame, text="End Session", command=self.end_study, fg_color="#C0392B", hover_color="#E74C3C", width=300, height=70, font=("Roboto", 22, "bold")).pack(pady=30)
    
    def update_timer(self):
        if not self.timer_running:
            return
        
        elapsed = datetime.now() - self.start_time
        total_seconds = int(elapsed.total_seconds())
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        self.timer_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
        
        # call this function again after 1000 ms
        self.root.after(1000, self.update_timer)
    
    def end_study(self):
        self.timer_running = False
        end_time = datetime.now()
        duration_minutes = (end_time - self.start_time).total_seconds() / 60.0
        
        # Popup dialog to ask for efficiency and done
        self.ask_feedback_and_save(end_time, duration_minutes)
    
    def ask_feedback_and_save(self, end_time, duration_minutes):
        feedback_win = ctk.CTkToplevel(self.root)
        feedback_win.title("Session Feedback")
        feedback_win.geometry("700x300")
        feedback_win.grab_set() # Modal
        
        # Main container
        main_frame = ctk.CTkFrame(feedback_win, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Horizontal container for inputs
        input_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_container.pack(expand=True, fill="x", pady=10)
        
        # 1. Subject Column
        subject_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        subject_frame.pack(side="left", expand=True, fill="both", padx=5)
        
        ctk.CTkLabel(subject_frame, text="Subject:", font=("Roboto", 14)).pack(pady=(0, 5))
        self.subject_entry = ctk.CTkEntry(subject_frame, placeholder_text="e.g. Math")
        self.subject_entry.pack(fill="x")
        
        # 2. Efficiency Column
        eff_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        eff_frame.pack(side="left", expand=True, fill="both", padx=5)
        
        ctk.CTkLabel(eff_frame, text="Efficiency (1-5):", font=("Roboto", 14)).pack(pady=(0, 5))
        efficiency_var = ctk.StringVar(value="3")
        ctk.CTkOptionMenu(eff_frame, variable=efficiency_var, values=["1", "2", "3", "4", "5"]).pack()
        
        # 3. Done Column
        done_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        done_frame.pack(side="left", expand=True, fill="both", padx=5)
        
        ctk.CTkLabel(done_frame, text="Done?", font=("Roboto", 14)).pack(pady=(0, 5))
        done_var = ctk.StringVar(value="Y")
        ctk.CTkOptionMenu(done_frame, variable=done_var, values=["Y", "N"]).pack()
        
        def submit():
            subject = self.subject_entry.get().strip()
            efficiency = efficiency_var.get()
            done = done_var.get()
            
            if not subject:
                messagebox.showerror("Error", "Please enter a subject.")
                return

            self.write_log(end_time, duration_minutes, subject, efficiency, done)
            feedback_win.destroy()
            messagebox.showinfo("Saved", "Study session saved.")
            self.build_start_screen()
        
        ctk.CTkButton(main_frame, text="Submit Log", command=submit, width=200, height=50, font=("Roboto", 16, "bold")).pack(pady=20)
    
    def write_log(self, end_time, duration_minutes, subject, efficiency, done):
        # Determine the directory where the app is running
        if getattr(sys, 'frozen', False):
            # If run as an exe
            app_path = Path(sys.executable).parent
        else:
            # If run as a script
            app_path = Path(__file__).parent
            
        log_path = app_path / "StudyLog.csv"
        
        file_exists = log_path.exists()
        
        try:
            with log_path.open("a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow([
                        "date", "study_material", "start_time", "end_time",
                        "duration_minutes", "subject", "efficiency", "done"
                    ])
                writer.writerow([
                    date.today().isoformat(),
                    self.study_material,
                    self.start_time.strftime("%H:%M:%S"),
                    end_time.strftime("%H:%M:%S"),
                    round(duration_minutes, 2),
                    subject,
                    efficiency,
                    done
                ])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write to log file at {log_path}:\n{e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = StudyTrackerApp(root)
    root.mainloop()
