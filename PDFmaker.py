import os
from datetime import datetime
from PIL import Image
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from tkinter import Tk
from tkinter import filedialog

# Set window size for a larger interface
Window.size = (600, 500)

class PDFConverterApp(MDApp):
    def build(self):
        # Main screen
        screen = MDScreen()

        # Create a layout for buttons and image selection feedback
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        # Label to show the number of selected images
        self.image_feedback_label = MDLabel(text="Hech qanday rasm tanlanmadi", halign="center", theme_text_color="Hint")
        layout.add_widget(self.image_feedback_label)

        # Create buttons
        self.choose_image_btn = MDRaisedButton(
            text="Rasm tanlash", 
            pos_hint={"center_x": 0.5}, 
            md_bg_color=[0.2, 0.6, 0.86, 1],
            size_hint=(0.8, None),
            height=50
        )
        self.choose_image_btn.bind(on_release=self.choose_images)

        self.convert_pdf_btn = MDRaisedButton(
            text="PDF ga aylantirish", 
            pos_hint={"center_x": 0.5}, 
            md_bg_color=[0.13, 0.55, 0.13, 1],
            size_hint=(0.8, None),
            height=50
        )
        self.convert_pdf_btn.bind(on_release=self.convert_to_pdf)

        # Add buttons to the layout
        layout.add_widget(self.choose_image_btn)
        layout.add_widget(self.convert_pdf_btn)

        # Center the layout vertically within the screen
        layout.bind(size=layout.setter('size'))

        # Add layout to the screen
        screen.add_widget(layout)

        self.image_paths = []

        return screen

    def choose_images(self, instance):
        # Create a tkinter root window and hide it
        root = Tk()
        root.withdraw()  # Hide the root window
        # Open file dialog for multiple image selection
        file_paths = filedialog.askopenfilenames(
            title="Rasm tanlang",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")],
            initialdir=os.getcwd()  # Open in the current directory
        )
        # Update the image paths and feedback label
        if file_paths:
            for path in file_paths:
                if path not in self.image_paths:  # Avoid duplicates
                    self.image_paths.append(path)
            self.image_feedback_label.text = f"{len(self.image_paths)} ta rasm tanlandi"
        else:
            self.image_feedback_label.text = "Hech qanday rasm tanlanmadi"

    def convert_to_pdf(self, instance):
        # Disable the button to prevent multiple taps
        self.convert_pdf_btn.disabled = False
        
        if not self.image_paths:
            self.show_message("Iltimos, rasm tanlang!")
            self.convert_pdf_btn.disabled = False  # Re-enable the button
            return
        
        try:
            # Create the output folder with the current date
            date_str = datetime.now().strftime('%Y-%m-%d')
            output_folder = os.path.join(os.path.expanduser("~"), "Documents", date_str)
            os.makedirs(output_folder, exist_ok=True)

            # Find the next available output filename
            base_pdf_name = "PDF"
            pdf_extension = ".pdf"
            counter = 1
            pdf_path = os.path.join(output_folder, f"{base_pdf_name}{counter:03}{pdf_extension}")  # Format with leading zeros

            # Check for existing files and increment the counter
            while os.path.exists(pdf_path):
                counter += 1
                pdf_path = os.path.join(output_folder, f"{base_pdf_name}{counter:03}{pdf_extension}")  # Maintain formatting

            # Convert images to PDF
            images = [Image.open(img).convert('RGB') for img in self.image_paths]
            images[0].save(pdf_path, save_all=True, append_images=images[1:])

            # Show success message
            self.show_message(f"Muvaffaqiyatli: {pdf_path}")
        except Exception as e:
            self.show_message(f"Xatolik yuz berdi: {str(e)}")
        finally:
            # Re-enable the button after processing
            self.convert_pdf_btn.disabled = False


    def show_message(self, message):
        # Show a message dialog
        dialog = MDDialog(title="Natija", text=message, size_hint=(0.8, 0.4))
        dialog.buttons = [MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        dialog.open()

# Run the app
if __name__ == "__main__":
    PDFConverterApp().run()
