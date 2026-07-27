import customtkinter as ctk
from tkinter import filedialog
import os
import pyperclip
import hashing

VERSION = "1.0"
class HashVerifier(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initializing and setting up the window
        self.title("Hash Verifier")
        self.geometry("900x600")
        self.minsize(800,500)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.selectedFile = None
        self.hashes = None
        self.aboutWindow=None

        self.topbar = ctk.CTkFrame(
            self,
            height=60,
            corner_radius=0
        )
        self.mainframe = ctk.CTkFrame(
            self
        )
        self.statusbar = ctk.CTkFrame(
            self,
            height=30,
            corner_radius=0
        )

        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew"
        )
        self.mainframe.grid(
            row=1,
            column=0,
            sticky="news"
        )
        self.statusbar.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        self.topbar.grid_columnconfigure(0, weight=1)

        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=2)

        self.statusbar.grid_columnconfigure(0, weight=1)
        self.statusbar.grid_columnconfigure(1, weight=0)

        self.titleLabel = ctk.CTkLabel(
            self.topbar,
            text="Hash Verifier",
            font=("Segoe UI", 24, "bold")
        )
        self.titleLabel.grid(
            row=0,
            column=0,
            padx=20,
            pady=15,
            sticky="w"
        )
        self.aboutButton = ctk.CTkButton(
            self.topbar,
            text="About",
            width=100,
            command=self.showAbout
        )
        self.aboutButton.grid(
            row=0,
            column=1,
            padx=20,
            pady=10
        )

        self.controlPanel = ctk.CTkFrame(
            self.mainframe,
            corner_radius=10
        )
        self.controlPanel.grid(
            row=0,
            column=0,
            padx=(15,8),
            pady=15,
            sticky="nsew"
        )
        self.controlPanel.grid_columnconfigure(0, weight=1)

        # widgets for control panel
        self.browseButton = ctk.CTkButton(
            self.controlPanel,
            text="Browse File",
            command=self.hashfile
        )
        self.browseButton.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )

        self.selectedFileTitle = ctk.CTkLabel(
            self.controlPanel,
            text="Selected File:",
            font=("Segoe UI", 14, "bold")
        )
        self.selectedFileTitle.grid(
            row=2,
            column=0,
            padx=20,
            pady=(15,5),
            sticky="w"
        )

        self.fileLabel = ctk.CTkLabel(
            self.controlPanel,
            text="No file selected",
            wraplength=220,
            justify="left"
        )
        self.fileLabel.grid(
            row=3,
            column=0,
            padx=20,
            pady=(0,15),
            sticky="w"
        )

        self.verifyLabel = ctk.CTkLabel(
            self.controlPanel,
            text="Verify Hash:"
        )
        self.verifyLabel.grid(
            row=4,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        self.hashentry = ctk.CTkEntry(
            self.controlPanel,
            placeholder_text="Hash..."
        )
        self.hashentry.grid(
            row=5,
            column=0,
            padx=20,
            pady=(5,15),
            sticky="ew"
        )

        self.verifyButton = ctk.CTkButton(
            self.controlPanel,
            text="Verify",
            command=self.verifyHash
        )
        self.verifyButton.grid(
            row=6,
            column=0,
            padx=20,
            pady=(5,15),
            sticky="ew"
        )
        self.verifyButton.configure(state="disabled")

        self.verifyResult = ctk.CTkLabel(
            self.controlPanel,
            text="",
            font=("Segoe UI", 14, "bold")
        )
        self.verifyResult.grid(
            row=7,
            column=0,
            padx=20,
            pady=(0,20),
            sticky="w"
        )

        # setting up resultspanel
        self.resultsPanel = ctk.CTkFrame(
            self.mainframe,
            corner_radius=10
        )
        self.resultsPanel.grid(
            row=0,
            column=1,
            padx=(8,15),
            pady=8,
            sticky="nsew"
        )

        self.resultsPanel.grid_columnconfigure(0, weight=1)
        self.resultsPanel.grid_columnconfigure(1, weight=0)

        self.fileNameLabel = ctk.CTkLabel(
            self.resultsPanel,
            text="File: None",
            font=("Segoe UI", 16, "bold")
        )
        self.fileNameLabel.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(20,5),
            sticky="w"
        )

        self.fileSizeLabel = ctk.CTkLabel(
            self.resultsPanel,
            text="Size: --"
        )
        self.fileSizeLabel.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=20,
            pady=(0,20),
            sticky="w"
        )

        self.md5Label = ctk.CTkLabel(
            self.resultsPanel,
            text="MD5"
        )
        self.md5Label.grid(
            row=2,
            column=0,
            padx=20,
            sticky="w"
        )

        self.md5Entry = ctk.CTkEntry(
            self.resultsPanel,
            state="disabled"
        )
        self.md5Entry.grid(
            row=3,
            column=0,
            padx=(20,10),
            pady=(5,15),
            sticky="ew"
        )

        self.md5Copy = ctk.CTkButton(
            self.resultsPanel,
            text="Copy",
            width=70,
            command=lambda: self.copyHash(self.md5Entry.get())
        )
        self.md5Copy.grid(
            row=3,
            column=1,
            padx=(0,20),
            pady=(5,15)
        )
        self.md5Copy.configure(state="disabled")

        self.sha1Label = ctk.CTkLabel(
            self.resultsPanel,
            text="SHA-1"
        )
        self.sha1Label.grid(
            row=4,
            column=0,
            padx=20,
            sticky="w"
        )

        self.sha1Entry = ctk.CTkEntry(
            self.resultsPanel,
            state="disabled"
        )
        self.sha1Entry.grid(
            row=5,
            column=0,
            padx=(20,10),
            pady=(5,15),
            sticky="ew"
        )

        self.sha1Copy = ctk.CTkButton(
            self.resultsPanel,
            text="Copy",
            width=70,
            command=lambda: self.copyHash(self.sha1Entry.get())
        )
        self.sha1Copy.grid(
            row=5,
            column=1,
            padx=(0,20),
            pady=(5,15)
        )
        self.sha1Copy.configure(state="disabled")

        self.sha256Label = ctk.CTkLabel(
            self.resultsPanel,
            text="SHA-256"
        )
        self.sha256Label.grid(
            row=6,
            column=0,
            padx=20,
            sticky="w"
        )

        self.sha256Entry = ctk.CTkEntry(
            self.resultsPanel,
            state="disabled"
        )
        self.sha256Entry.grid(
            row=7,
            column=0,
            padx=(20,10),
            pady=(5,15),
            sticky="ew"
        )

        self.sha256Copy = ctk.CTkButton(
            self.resultsPanel,
            text="Copy",
            width=70,
            command=lambda: self.copyHash(self.sha256Entry.get())
        )
        self.sha256Copy.grid(
            row=7,
            column=1,
            padx=(0,20),
            pady=(5,15)
        )  
        self.sha256Copy.configure(state="disabled") 

        # Widgets in statusbar
        self.statusLabel = ctk.CTkLabel(
            self.statusbar,
            text="Status: Ready",
            anchor="w"
        )
        self.statusLabel.grid(
            row=0,
            column=0,
            padx=15,
            pady=5,
            sticky="w"
        )

        self.versionNumber = ctk.CTkLabel(
            self.statusbar,
            text=f"v{VERSION}",
            anchor="w"
        )
        self.versionNumber.grid(
            row=0,
            column=1,
            padx=30,
            pady=5,
            sticky="e"
        )

    def verifyHash(self):
        if self.hashes is None:
            self.verifyResult.configure(
                text="Please select a file first."
            )
            self.statusLabel.configure(
                text="Status: No file selected"
            )
            return

        userHash = self.hashentry.get().strip().lower()

        if userHash == "":
            self.verifyResult.configure(
                text="Please enter a hash"
            )
            return
        if userHash == self.hashes["MD5"].lower():
            self.verifyResult.configure(text="MD5 Match")
        elif userHash == self.hashes["SHA1"].lower():
            self.verifyResult.configure(text="SHA-1 Match")
        elif userHash == self.hashes["SHA256"].lower():
            self.verifyResult.configure(text="SHA-256 Match")
        else:
            self.verifyResult.configure(text="Hash doesn't match")
        self.statusLabel.configure(
            text="Status: Verification Complete"
        )
    
    def copyHash(self, text):
        pyperclip.copy(text)
        self.statusLabel.configure(
            text="Status: Hash copied to clipboard"
        )

    def formatSize(self, size):
        units = ["bytes", "KB", "MB", "GB", "TB"]

        index = 0

        while size>=1024 and index<len(units) - 1:
            size/=1024
            index+=1

        if index == 0:
            return f"{int(size)} {units[index]}"

        return f"{size:.2f} {units[index]}"

    def showAbout(self):
        if self.aboutWindow is not None and self.aboutWindow.winfo_exists():
            self.aboutWindow.focus()
            return

        self.aboutWindow = ctk.CTkToplevel(self)
        about = self.aboutWindow
        about.protocol(
            "WM_DELETE_WINDOW",
            self.closeAbout
        )
        about.title("About")
        about.geometry("420x390")
        about.resizable(False,False)

        self.update_idletasks()

        x=self.winfo_x()+(self.winfo_width()//2)-210
        y=self.winfo_y()+(self.winfo_height()//2)-170

        about.geometry(f"420x390+{x}+{y}")
        about.grab_set()

        title = ctk.CTkLabel(
            about,
            text="Hash Verifier",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(pady=(20, 5))

        versionLabel = ctk.CTkLabel(
            about,
            text=f"Version {VERSION}",
            font=("Segoe UI", 14)
        )
        versionLabel.pack()

        description = ctk.CTkLabel(
            about,
            text=(
                "A simple desktop utility for generating\n"
                "and verifying file hashes."
            ),
            justify="center"
        )
        description.pack(pady=15)

        featuresTitle = ctk.CTkLabel(
            about,
            text="Features",
            font=("Segoe UI", 14, "bold")
        )
        featuresTitle.pack(pady=(5,5))

        featuresList = ctk.CTkLabel(
            about,
            text=(
                "• Generate MD5\n"
                "• Generate SHA-1\n"
                "• Generate SHA-256\n"
                "• Verify Hashes\n"
                "• Copy hashes to clipboard"
            ),
            justify="left",
            font=("Segoe UI", 13)
        )
        featuresList.pack()

        authorLabel = ctk.CTkLabel(
            about,
            text="Developed by Prajwal",
            font=("Segoe UI", 12)
        )
        authorLabel.pack(pady=(15,5))

        closeButton = ctk.CTkButton(
            about,
            text="Close",
            command=self.closeAbout,
            width=100
        )
        closeButton.pack(pady=(0,20))

    def closeAbout(self):
        self.aboutWindow.destroy()
        self.aboutWindow = None

    def hashfile(self):
        path = filedialog.askopenfilename(
            title="Select a File"
        )
        if not path:
            return
        self.selectedFile = path
        try:
            self.hashes = hashing.hashFile(self.selectedFile)
            filename = os.path.basename(self.selectedFile)
            size = os.path.getsize(self.selectedFile)
            self.fileNameLabel.configure(
                text=f"File: {filename}"
            )
            self.fileSizeLabel.configure(
                text=f"Size: {self.formatSize(size)}"
            )

            self.md5Entry.configure(state="normal")
            self.md5Entry.delete(0, "end")
            self.md5Entry.insert(0, self.hashes["MD5"])
            self.md5Entry.configure(state="disabled")

            self.sha1Entry.configure(state="normal")
            self.sha1Entry.delete(0, "end")
            self.sha1Entry.insert(0, self.hashes["SHA1"])
            self.sha1Entry.configure(state="disabled")

            self.sha256Entry.configure(state="normal")
            self.sha256Entry.delete(0, "end")
            self.sha256Entry.insert(0, self.hashes["SHA256"])
            self.sha256Entry.configure(state="disabled")

            self.verifyResult.configure(text="")
            self.hashentry.delete(0, "end")
             
        except Exception as e:
            self.statusLabel.configure(text=f"Status: {e}")
            return
        filename=os.path.basename(path)
        self.fileLabel.configure(text=filename)
        self.statusLabel.configure(
            text=f"Status: Hashes generated"
        )
        self.verifyButton.configure(state="normal")
        self.md5Copy.configure(state="normal")
        self.sha1Copy.configure(state="normal")
        self.sha256Copy.configure(state="normal")
        


if __name__ == "__main__":
    app = HashVerifier()
    app.mainloop()