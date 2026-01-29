import tkinter as tk 
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  


class IconConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Img 2 Ico")
        self.root.geometry("400x400")
        
        self.image = None
        self.image_path = None

        self.preview_label = tk.Label(root, text="No image selected")
        self.preview_label.pack(pady=10)

        tk.Button(self.root, text="Load Image", command=self.load_image).pack(pady=5)

        self.icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        self.size_vars = {}

        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=5)

        for size in self.icon_sizes:
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(size_frame, text=f"{size[0]}x{size[1]}", variable=var)
            chk.pack(side=tk.LEFT)
            self.size_vars[size] = var

        tk.Button(root, text="Convert to .ICO", command=self.convert).pack(pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if not path:
            return

        self.image_path = path
        self.image = Image.open(path)

    # Create preview
        preview = self.image.copy()
        preview.thumbnail((200, 200), Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(preview)

    # IMPORTANT: attach image to the label itself
        self.preview_label.config(image=tk_image, text="")
        self.preview_label.image = tk_image  # prevents garbage collection


    def convert(self):
        if not self.image:
            messagebox.showerror("Error","No Image Selected")
            return
        sizes = [(s,s) for s, v in self.size_vars.items() if v.get()]
        if not sizes:
            messagebox.showerror("Error", "Select at least one size.")
            return
        save_path = filedialog.asksaveasfile(
            defaultextension=".ico",
            filetypes=[("Icon file","*.ico")]
        )
        if not save_path:
            return
    
        try:
            self.image.save(save_path,format="ICO",sizes=sizes)
            messagebox.showinfo("Success","Icon created!")
        except Exception as e:
            messagebox.showerror("Error",str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = IconConverter(root)
    root.mainloop()


    
    

        
