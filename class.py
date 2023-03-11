import tkinter

class HintEntry(tkinter.Entry):
    def __init__(self, master=None, hint_text=""):
        super().__init__(master)

        self.hint_text = hint_text
        self.insert("0", self.hint_text)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        if self.get() == self.hint_text:
            self.delete("0", "end")

    def _on_focus_out(self, event):
        if not self.get():
            self.insert("0", self.hint_text)