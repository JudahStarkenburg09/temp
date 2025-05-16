import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from datetime import datetime
import os

class Windows11LockScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows 11 Lock Screen")
        self.root.attributes('-fullscreen', True)
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Create a canvas that covers the entire screen
        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height, 
                            highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Load both background images
        self.load_background_images()
        
        # Display the normal background image
        self.bg_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Create the clock and date display
        self.time_id = self.canvas.create_text(
            self.screen_width // 2, 
            self.screen_height // 2 - 300,
            text="", 
            font=("Segoe UI", 110), 
            fill="white"
        )
        
        self.date_id = self.canvas.create_text(
            self.screen_width // 2, 
            self.screen_height // 2 - 200,
            text="", 
            font=("Segoe UI", 24), 
            fill="white"
        )
        

        
        # Update the clock
        self.update_clock()
        
        # Bind click and space key events
        self.canvas.bind("<Button-1>", self.start_transition)
        self.root.bind("<space>", self.start_transition)
        
        # Flag to track if animation is in progress
        self.animating = False
        
        # Create login screen elements (initially hidden)
        self.setup_login_screen()
        
        # Prepare blended images for fade effect
        self.prepare_fade_images()
        
    def load_background_images(self):
        """Load both normal and blurred background images"""
        # Load normal background
        if os.path.exists("bg.png"):
            try:
                self.bg_image = Image.open("bg.png")
                print("Successfully loaded bg.png")
            except Exception as e:
                print(f"Error loading bg.png: {e}")
                self.bg_image = Image.new('RGB', (1920, 1080), color=(0, 120, 212))
        else:
            print("bg.png not found, using placeholder")
            self.bg_image = Image.new('RGB', (1920, 1080), color=(0, 120, 212))
        
        # Resize to fit screen
        self.bg_image = self.bg_image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Load blurred background
        if os.path.exists("bgblur.png"):
            try:
                self.blur_image = Image.open("bgblur.png")
                print("Successfully loaded bgblur.png")
            except Exception as e:
                print(f"Error loading bgblur.png: {e}")
                # If blurred image can't be loaded, use the normal one
                self.blur_image = self.bg_image
        else:
            print("bgblur.png not found, using normal background")
            self.blur_image = self.bg_image
        
        # Resize to fit screen
        self.blur_image = self.blur_image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        self.blur_photo = ImageTk.PhotoImage(self.blur_image)
    
    def prepare_fade_images(self):
        """Prepare a series of blended images for the fade effect"""
        # Number of steps in the fade
        self.fade_steps = 10
        self.fade_images = []
        
        # Convert both images to 'RGB' mode to avoid the ValueError
        self.bg_image = self.bg_image.convert('RGB')
        self.blur_image = self.blur_image.convert('RGB')
        
        # Create blended images at different opacity levels
        for i in range(self.fade_steps + 1):
            # Calculate alpha (0.0 to 1.0)
            alpha = i / self.fade_steps
            
            # Blend the images
            blended = Image.blend(self.bg_image, self.blur_image, alpha)
            
            # Convert to PhotoImage and store
            self.fade_images.append(ImageTk.PhotoImage(blended))

        
    def update_clock(self):
        """Update the clock and date display"""
        now = datetime.now()
        
        # Format time as #:## (hour:minute) - Windows compatible
        hour = now.strftime("%I").lstrip("0")
        minute = now.strftime("%M")
        time_str = f"{hour}:{minute}"
        
        # Format date as "Thursday, April 24"
        date_str = now.strftime("%A, %B %d")
        
        # Update the text on canvas
        self.canvas.itemconfig(self.time_id, text=time_str)
        self.canvas.itemconfig(self.date_id, text=date_str)
        
        # Schedule the next update
        self.root.after(1000, self.update_clock)
    
    def setup_login_screen(self):
        """Create the login screen elements directly on the canvas (initially hidden)"""
        # We'll create login elements directly on the canvas instead of using a frame
        # This way the blurred background will be visible


        
        
        # User profile circle (initially hidden)
        self.user_img = Image.open("user2.png")
        # Resize to match the circle dimensions (120x120 pixels)
        dim = 200
        self.user_img = self.user_img.resize((dim, dim), Image.LANCZOS)
        self.user_photo = ImageTk.PhotoImage(self.user_img)
        
        # Create image at the same position as the previous circle
        self.profile_circle = self.canvas.create_image(
            self.screen_width // 2 - 60,  # Left edge of the previous circle
            self.screen_height // 2 - 120,  # Top edge of the previous circle
            image=self.user_photo,
            anchor="nw",  # Northwest anchor to match the oval positioning
            state="hidden"
        )
        
        # Username text
        self.username_text = self.canvas.create_text(
            self.screen_width // 2,
            self.screen_height // 2 + 20,
            text="User",
            font=("Segoe UI", 24),
            fill="white",
            state="hidden"
        )
        
        # Create a frame just for the password entry and button
        # This is necessary because we can't create Entry widgets directly on canvas
        self.password_container = tk.Frame(self.root)
        self.password_container.configure(bg="")  # Transparent background
        
        # Password entry
        self.password_entry = tk.Entry(
            self.password_container, 
            font=("Segoe UI", 14), 
            show="•", 
            width=20,
            bd=0,
            highlightthickness=1,
            highlightbackground="#FFFFFF"
        )
        self.password_entry.pack(pady=5, ipady=8)
        self.password_entry.bind("<Return>", self.login)
        
        # Sign-in button
        self.signin_button = tk.Button(
            self.password_container, 
            text="Sign in", 
            font=("Segoe UI", 12), 
            bg="#FFFFFF", 
            fg="#0078D7",
            bd=0,
            padx=20,
            pady=5,
            command=self.login
        )
        self.signin_button.pack(pady=10)
        
        # Position the password container but hide it initially
        self.password_window = self.canvas.create_window(
            self.screen_width // 2,
            self.screen_height // 2 + 100,
            window=self.password_container,
            anchor="center",
            state="hidden"
        )



        
    
    def start_transition(self, event=None):
        """Start the transition from lock screen to login screen"""
        if self.animating:
            return
            
        self.animating = True
        
        # Stop updating the clock
        self.root.after_cancel(self.update_clock)
        
        # Slide the text up off screen
        self.slide_text_up()
    
    def slide_text_up(self):
        """Animate the text sliding up off the screen"""
        # Number of animation steps
        steps = 25
        
        # Calculate movement per step
        move_per_step = self.screen_height / steps
        
        def animate_step(step=0):
            # Move text up
            self.canvas.move(self.time_id, 0, -move_per_step)
            self.canvas.move(self.date_id, 0, -move_per_step)
            
            # Continue animation if not complete
            if step < steps - 1:
                self.root.after(5, lambda: animate_step(step + 1))
            else:
                # Animation complete, fade to blurred background
                self.fade_to_blurred()
        
        # Start animation
        animate_step()
    
    def fade_to_blurred(self):
        """Fade from normal background to blurred background"""
        def fade_step(step=0):
            if step <= self.fade_steps:
                # Update the background image to the current fade step
                self.canvas.itemconfig(self.bg_id, image=self.fade_images[step])
                
                # Schedule the next fade step
                self.root.after(1, lambda: fade_step(step + 1))
            else:
                # Fade complete, show login elements
                self.show_login_elements()
        
        # Start the fade animation
        fade_step()
    
    def show_login_elements(self):
        """Show the login elements after fade completes"""
        # Show the login elements
        self.canvas.itemconfig(self.profile_circle, state="normal")
        self.canvas.itemconfig(self.username_text, state="normal")
        self.canvas.itemconfig(self.password_window, state="normal")
        
        # Use different variable names for the second image
        self.other_user_img = Image.open("user.png")
        dim = 50
        self.other_user_img = self.other_user_img.resize((dim, dim), Image.LANCZOS)
        self.other_user_photo = ImageTk.PhotoImage(self.other_user_img)
        
        # Calculate positions
        user_x = self.screen_width // 12 - 130
        user_y = self.screen_height - 80
        
        # Create the user image on canvas
        self.user_img_id = self.canvas.create_image(
            user_x+2, user_y, 
            image=self.other_user_photo,  # Use the new photo object
            anchor="nw"
        )
        
        # Create "other user" text
        self.other_user_text = self.canvas.create_text(
            user_x + 62,
            user_y + 22,
            text="Other user",
            font=("Segoe UI", 12),
            fill="white",
            anchor="w"
        )
        
        # Focus on password entry
        self.password_entry.focus()
        
        # Animation is complete
        self.animating = False
    
    def login(self, event=None):
        """Handle login attempt"""
        password = self.password_entry.get()
        
        # Print the password to the console
        print("Entered password:", password)
        
        # This is a simulation, so we'll just show a message
        if password:
            # Clear the canvas
            self.canvas.delete("all")
            
            # Show desktop simulation
            self.canvas.create_rectangle(0, 0, self.screen_width, self.screen_height, 
                                        fill="#0C0C0C", outline="")
            
            welcome_text = self.canvas.create_text(
                self.screen_width // 2,
                self.screen_height // 2 - 50,
                text="Welcome to Windows 11 Simulation",
                font=("Segoe UI", 24),
                fill="white"
            )
            
            note_text = self.canvas.create_text(
                self.screen_width // 2,
                self.screen_height // 2,
                text="This is a Python simulation for educational purposes only.",
                font=("Segoe UI", 14),
                fill="white"
            )
            
            # Add exit button
            exit_button = tk.Button(
                self.root,
                text="Exit Simulation",
                font=("Segoe UI", 12),
                bg="#0078D7",
                fg="white",
                bd=0,
                padx=20,
                pady=10,
                command=self.root.destroy
            )
            exit_button_window = self.canvas.create_window(
                self.screen_width // 2,
                self.screen_height // 2 + 100,
                window=exit_button
            )
        else:
            # Shake the password entry to indicate error
            original_x = self.password_entry.winfo_x()
            for i in range(10):
                offset = 10 if i % 2 == 0 else -10
                self.password_entry.place(x=original_x + offset)
                self.password_entry.update()
                time.sleep(0.05)
            self.password_entry.place(x=original_x)


if __name__ == "__main__":
    root = tk.Tk()
    app = Windows11LockScreen(root)
    root.mainloop()