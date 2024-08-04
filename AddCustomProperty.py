import sys
import os
from tkinter import Tk, Button, Label, messagebox
from tkinter.font import Font
from PyPDF2 import PdfReader, PdfWriter

# Function to check if the file is a PDF file
def is_pdf(file_path):
    return file_path.lower().endswith('.pdf')

# Function to check if the PDF file has a specific metadata
def get_metadata(input_pdf):
    reader = PdfReader(input_pdf)
    comments = reader.metadata.get('/Comments', '')
    return comments == 'filesettomesuvag'

# Function to set the metadata of a PDF file
def set_metadata(input_pdf):
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        
        metadata = {key: value for key, value in reader.metadata.items()}
        metadata['/Comments'] = 'filesettomesuvag'
        writer.add_metadata(metadata)
        
        with open(input_pdf, 'wb') as output_file:
            writer.write(output_file)
    except IOError:
        show_warning("The file is already open and cannot be written. Please close the PDF file and try again.")

# Function to unset the metadata of a PDF file
def unset_metadata(input_pdf):
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        
        metadata = {key: value for key, value in reader.metadata.items()}
        if '/Comments' in metadata:
            del metadata['/Comments']
        writer.add_metadata(metadata)
        
        with open(input_pdf, 'wb') as output_file:
            writer.write(output_file)
    except IOError:
        show_warning("The file is already open and cannot be written. Please close the PDF file and try again.")


# Function to show a warning message
def show_warning(message):
    root.withdraw()  # Hide the root window
    messagebox.showwarning("Warning", message)
    root.destroy()

# Function to toggle the metadata of a PDF file
def toggle_metadata():
    if get_metadata(file_path):
        unset_metadata(file_path)
        btn_toggle.config(text="Set Confidential")
        btn_toggle.config(bg='lightgreen')
    else:
        set_metadata(file_path)
        btn_toggle.config(text="Unset Confidential")
        btn_toggle.config(bg='lightcoral')

# Check if the script received a file path argument
if len(sys.argv) != 2:
    print("Usage: script.py <path_to_pdf>")
    sys.exit(1)

file_path = sys.argv[1]

if not os.path.isfile(file_path) or not is_pdf(file_path):
    print(f"Error: {file_path} is not a valid PDF file.")
    sys.exit(1)

# Create the GUI window
root = Tk()
root.title("PDF Metadata Toggle")
root.resizable(False, False)
root.geometry("350x150")

label_font = Font(size=12)
button_font = Font(size=16)

# Create and place the status label
status_label = Label(root, 
                     font=label_font, 
                     bg='darkgrey', 
                     text=f"File: {os.path.basename(file_path)}",
                     wraplength=340)  # wrap text to fit within the window size
status_label.pack()

# Create and place the toggle button
btn_text = "Unset Confidential" if get_metadata(file_path) else "Set Confidential"
btn_color = 'lightcoral' if get_metadata(file_path) else 'lightgreen'
btn_toggle = Button(root, text=btn_text,font=button_font, bg=btn_color, command=toggle_metadata)
btn_toggle.pack(anchor='center', pady=20)


# Run the Tkinter main loop
root.mainloop()
