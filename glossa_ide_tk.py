
# -*- coding: utf-8 -*-
"""Python-based IDE shell for the educational Glossa compiler.
Copyright (c) 2025 Prof. George Papagiannakis, University of Crete.
Vibe-coding example for educational purposes only.
Entirely  written with gpt-5-codex assistance.

The application embeds a text editor, syntax highlighter, and output console,
bridging directly to the in-repo ``glossa_compiler`` module for execution. It
is intentionally minimal so students can inspect both the tooling and compiler
code in one place.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font as tkfont
import re
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import glossa_compiler as glossa

KEYWORDS = list(glossa.KEYWORDS.keys())

class GUIIO(glossa.IOHandler):
    """tkinter-aware IO layer that redirects runtime output to the console."""

    def __init__(self, output_widget):
        """Store a reference to the console widget and reset buffers."""
        super().__init__(input_queue=None)
        self.output_widget = output_widget
        self.outputs = []  # keep a list too

    def write(self, text: str):
        """Append a line to both the stored transcript and the GUI widget."""
        self.outputs.append(text)
        self.output_widget.config(state='normal')
        self.output_widget.insert('end', text + "\n")
        self.output_widget.see('end')
        self.output_widget.config(state='disabled')

    def read(self) -> str:
        """Prompt the user when ΔΙΑΒΑΣΕ is encountered during execution."""
        resp = simpledialog.askstring("Είσοδος", "Δώσε τιμή (ΔΙΑΒΑΣΕ):")
        if resp is None:
            raise glossa.RuntimeErrorGlossa("Η είσοδος ακυρώθηκε από τον χρήστη")
        return resp


class DebugStop(Exception):
    """Signal used to terminate debugging without surfacing a runtime error."""


class TkDebuggerHook:
    """Adapter that bridges compiler debug callbacks to the Tk IDE."""

    def __init__(self, app: "GlossaIDE"):
        self.app = app

    def before_statement(self, stmt, env):
        self.app.debug_before_statement(stmt, env)

    def after_statement(self, stmt, env):
        self.app.debug_after_statement(stmt, env)


class GlossaIDE(tk.Tk):
    """Main Tk window coordinating editor, toolbar, and runtime."""

    def __init__(self):
        """Build the UI elements and preload a starter template."""
        super().__init__()
        self.title("ΕΠΙΤΕΛΟΥΣ ENA ΓΛΩΣΣΑ IDE (Python-based)")
        self.geometry("1600x2000")

        # Fonts
        self.code_font = tkfont.Font(family="Courier", size=12)

        # Layout: top toolbar, center editor, bottom output
        toolbar = tk.Frame(self)
        toolbar.pack(side='top', fill='x')

        tk.Button(toolbar, text="Άνοιγμα", command=self.open_file).pack(side='left')
        tk.Button(toolbar, text="Αποθήκευση", command=self.save_file).pack(side='left')
        tk.Button(toolbar, text="Αποθήκευση ως", command=self.save_as_file).pack(side='left')
        tk.Button(toolbar, text="Εκτέλεση", command=self.run_code).pack(side='left')
        tk.Button(toolbar, text="Βήμα", command=self.debug_step).pack(side='left')
        tk.Button(toolbar, text="Συνέχεια", command=self.debug_continue).pack(side='left')
        tk.Button(toolbar, text="Διακοπή", command=self.debug_stop).pack(side='left')

        # Paned editor/console
        self.paned = tk.PanedWindow(self, orient='vertical')
        self.paned.pack(fill='both', expand=True)

        # Editor
        editor_frame = tk.Frame(self.paned)
        self.line_numbers = tk.Text(editor_frame, width=5, state='disabled', background='#f5f5f5', foreground='#555555', relief='flat', font=self.code_font, padx=4, takefocus=0)
        self.line_numbers.pack(side='left', fill='y')
        self.editor = tk.Text(editor_frame, wrap='none', font=self.code_font, undo=True)
        yscroll = tk.Scrollbar(editor_frame)
        self.editor_scrollbar = yscroll
        self.editor.configure(yscrollcommand=self.on_editor_scroll)
        yscroll.configure(command=self.on_scrollbar)
        self.editor.pack(side='left', fill='both', expand=True)
        yscroll.pack(side='right', fill='y')
        self.paned.add(editor_frame)

        # Output console and watch panel
        output_frame = tk.Frame(self.paned)
        output_split = tk.PanedWindow(output_frame, orient='horizontal')
        output_split.pack(fill='both', expand=True)

        console_holder = tk.Frame(output_split)
        self.output = tk.Text(console_holder, wrap='word', height=10, state='disabled', font=("Helvetica", 12))
        yscroll2 = tk.Scrollbar(console_holder, command=self.output.yview)
        self.output.configure(yscrollcommand=yscroll2.set)
        self.output.pack(side='left', fill='both', expand=True)
        yscroll2.pack(side='right', fill='y')
        output_split.add(console_holder)

        watch_holder = tk.Frame(output_split)
        tk.Label(watch_holder, text="Μεταβλητές").pack(anchor='w')
        self.watch = tk.Text(watch_holder, width=25, height=10, state='disabled', font=("Courier New", 11))
        self.watch.pack(fill='both', expand=True)
        output_split.add(watch_holder)

        self.paned.add(output_frame)
        
        # Configure minimum sizes and let editor occupy most space
        self.paned.paneconfigure(editor_frame, minsize=400)
        self.paned.paneconfigure(output_frame, minsize=250)
        
        # Store reference to output_split for later positioning
        self.output_split = output_split

        # Syntax highlight tags
        self.keyword_font = self.code_font.copy()
        self.comment_font = self.code_font.copy()
        self.comment_font.configure(slant="italic")

        self.editor.tag_configure("kw", foreground="#0057b8", font=self.keyword_font)
        self.editor.tag_configure("str", foreground="#2ca02c")
        self.editor.tag_configure("com", foreground="#7f7f7f", font=self.comment_font)
        self.editor.tag_configure("debug_line", background="#fff3b0", foreground="#c00000")
        self.editor.tag_configure("error_line", background="#ffd6d6")

        self.editor.bind("<KeyRelease>", self.on_key_release)

        # Starter template
        template = """ΠΡΟΓΡΑΜΜΑ Παράδειγμα
ΜΕΤΑΒΛΗΤΕΣ
    ΑΚΕΡΑΙΕΣ: α, β, i
ΑΡΧΗ
    α <- 5
    β <- 3
    ΓΡΑΨΕ "Άθροισμα:", α + β
    ΓΙΑ i ΑΠΟ 1 ΜΕΧΡΙ 3
        ΓΡΑΨΕ i
    ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ
ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ
"""
        self.editor.insert("1.0", template)
        self.highlight_all()
        self.update_line_numbers()

        self.current_file = None
        self.debug_active = False
        self.debug_continue_mode = False
        self.debug_stop_requested = False
        self.debug_wait_var = tk.BooleanVar(value=False)
        self.debug_hook = None
        self.debug_env = None
        self.debug_prog = None
        self.update_watch(None)
        self.update_window_title()
        
        # Set initial paned position after window fully renders
        self.after(100, self._set_initial_paned_position)
        # Set horizontal split between output and variables (75% output, 25% vars)
        self.after(150, self._set_output_split_position)

    def _set_initial_paned_position(self):
        """Set sash position to show ~70 lines of code in the editor."""
        total_height = self.paned.winfo_height()
        if total_height > 1:
            # Calculate height for ~70 lines (18 pixels per line @ 12pt font)
            # But ensure output panel gets at least 250 pixels
            desired_editor = 70 * 18  # 1260 pixels for 70 lines
            min_output = 250
            
            if total_height >= (desired_editor + min_output):
                # We have enough space for 70 lines
                editor_height = desired_editor
            else:
                # Allocate what we can, leaving minimum for output
                editor_height = total_height - min_output
            
            self.paned.sash_place(0, 0, editor_height)
    
    def _set_output_split_position(self):
        """Set horizontal split to give Output 75% and Variables 25%."""
        total_width = self.output_split.winfo_width()
        if total_width > 1:
            # Give 75% to output console, 25% to variables
            output_width = int(total_width * 0.75)
            self.output_split.sash_place(0, output_width, 0)

    def update_window_title(self):
        """Update the window title to show the current file name."""
        base_title = "ΕΠΙΤΕΛΟΥΣ ENA ΓΛΩΣΣΑ IDE"
        if self.current_file:
            filename = os.path.basename(self.current_file)
            self.title(f"{base_title} - {filename}")
        else:
            self.title(base_title)

    def on_key_release(self, event):
        """Refresh syntax highlighting when edits occur."""
        self.highlight_line(self.editor.index("insert linestart"), self.editor.index("insert lineend"))
        self.update_line_numbers()

    def highlight_all(self):
        """Apply syntax highlighting tags across the entire buffer."""
        text = self.editor.get("1.0", "end-1c")
        self.editor.tag_remove("kw", "1.0", "end")
        self.editor.tag_remove("str", "1.0", "end")
        self.editor.tag_remove("com", "1.0", "end")
        # Strings: "..." or «...»
        for m in re.finditer(r'"[^"\\]*(?:\\.[^"\\]*)*"|«[^»]*»', text):
            self.editor.tag_add("str", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        # Comments: ! to end of line
        for m in re.finditer(r'!.*', text):
            self.editor.tag_add("com", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        # Keywords (whole words)
        for kw in sorted(KEYWORDS, key=len, reverse=True):
            for m in re.finditer(rf'\b{re.escape(kw)}\b', text):
                self.editor.tag_add("kw", f"1.0+{m.start()}c", f"1.0+{m.end()}c")

    def highlight_line(self, start, end):
        """Re-highlight a specific line range."""
        self.editor.tag_remove("kw", start, end)
        self.editor.tag_remove("str", start, end)
        self.editor.tag_remove("com", start, end)
        line_text = self.editor.get(start, end)
        base_index = self.editor.index(start)
        line_start_idx = self.index_to_offset("1.0", start)
        # Strings
        for m in re.finditer(r'"[^"\\]*(?:\\.[^"\\]*)*"|«[^»]*»', line_text):
            self.editor.tag_add("str", f"{start}+{m.start()}c", f"{start}+{m.end()}c")
        # Comments
        m = re.search(r'!.*', line_text)
        if m:
            self.editor.tag_add("com", f"{start}+{m.start()}c", f"{start}+{m.end()}c")
        # Keywords
        for kw in sorted(KEYWORDS, key=len, reverse=True):
            for m in re.finditer(rf'\b{re.escape(kw)}\b', line_text):
                self.editor.tag_add("kw", f"{start}+{m.start()}c", f"{start}+{m.end()}c")

    def index_to_offset(self, start, idx):
        """Placeholder helper kept for future enhancements."""
        return 0

    def on_editor_scroll(self, *args):
        self.editor_scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])

    def on_scrollbar(self, *args):
        self.editor.yview(*args)
        self.line_numbers.yview(*args)

    def update_line_numbers(self):
        total_lines = int(self.editor.index('end-1c').split('.')[0])
        content = "\n".join(str(i) for i in range(1, total_lines + 1))
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', content)
        self.line_numbers.config(state='disabled')
        first, _ = self.editor.yview()
        self.line_numbers.yview_moveto(first)

    def clear_error_highlight(self):
        self.editor.tag_remove("error_line", "1.0", "end")

    def highlight_error_line(self, line):
        try:
            index = f"{line}.0"
            self.editor.tag_add("error_line", index, f"{line}.0 lineend")
            self.editor.see(index)
        except tk.TclError:
            pass

    def highlight_error_from_message(self, message):
        if not message:
            return
        match = re.search(r"γραμμή\s+(\d+)", str(message))
        if match:
            self.highlight_error_line(int(match.group(1)))

    def prepare_output(self):
        """Clear the runtime console."""
        self.clear_error_highlight()
        self.output.config(state='normal')
        self.output.delete("1.0", "end")
        self.output.config(state='disabled')

    def update_watch(self, env):
        """Populate the watch panel with the current environment values."""
        self.watch.config(state='normal')
        self.watch.delete("1.0", "end")
        if not env:
            self.watch.insert("1.0", "(χωρίς δεδομένα)")
            self.watch.config(state='disabled')
            return
        lines = []
        current = env
        while current:
            prefix = "[L]" if current is env else "[G]"
            for name in sorted(current.types.keys()):
                value = current.values.get(name)
                if isinstance(value, bool):
                    display = "ΑΛΗΘΗΣ" if value else "ΨΕΥΔΗΣ"
                else:
                    display = str(value)
                lines.append(f"{prefix} {name} = {display}")
            current = getattr(current, "parent", None)
        if not lines:
            lines.append("(χωρίς μεταβλητές)")
        self.watch.insert("1.0", "\n".join(lines))
        self.watch.config(state='disabled')

    def clear_debug_highlight(self):
        """Remove any debugger line highlight."""
        self.editor.tag_remove("debug_line", "1.0", "end")

    def highlight_debug_line(self, line):
        """Highlight the line currently about to execute."""
        self.clear_debug_highlight()
        if line is None:
            return
        location = f"{line}.0"
        self.editor.tag_add("debug_line", location, f"{line}.0 lineend")
        self.editor.see(location)

    def debug_step(self):
        """Advance execution by one statement."""
        if not self.debug_active:
            self.start_debug_session(continue_mode=False)
        else:
            self.debug_continue_mode = False
            self.debug_wait_var.set(True)

    def debug_continue(self):
        """Resume execution without further pauses."""
        if not self.debug_active:
            self.start_debug_session(continue_mode=True)
        else:
            self.debug_continue_mode = True
            self.debug_wait_var.set(True)

    def debug_stop(self):
        """Request termination of the current debug session."""
        if not self.debug_active:
            return
        self.debug_stop_requested = True
        self.debug_wait_var.set(True)

    def start_debug_session(self, continue_mode: bool):
        """Compile and execute the buffer under debugger control."""
        if self.debug_active:
            return
        self.prepare_output()
        self.update_watch(None)
        self.clear_debug_highlight()
        src = self.editor.get("1.0", "end-1c")
        try:
            tokens = glossa.lex(src)
            parser = glossa.Parser(tokens)
            prog = parser.parse()
            env = glossa.Env(prog.var_decls, procedures=prog.procedures, functions=prog.functions)
        except glossa.LexerError as e:
            self.append_out(f"Σφάλμα αναλυτή (Lexer): {e}")
            self.highlight_error_from_message(e)
            return
        except glossa.ParseError as e:
            self.append_out(f"Σφάλμα σύνταξης: {e}")
            self.highlight_error_from_message(e)
            return
        io = GUIIO(self.output)
        self.debug_env = env
        self.debug_prog = prog
        self.debug_continue_mode = continue_mode
        self.debug_stop_requested = False
        self.debug_hook = TkDebuggerHook(self)
        self.debug_active = True
        self.update_watch(env)
        try:
            glossa.exec_statements(prog.statements, env, io, debugger=self.debug_hook)
            self.append_out("Η εκτέλεση ολοκληρώθηκε.")
        except DebugStop:
            self.append_out("Η εκτέλεση διακόπηκε από τον χρήστη.")
        except glossa.FunctionReturn:
            self.append_out("Η εντολή ΕΠΙΣΤΡΕΨΕ χρησιμοποιήθηκε εκτός συνάρτησης")
        except glossa.RuntimeErrorGlossa as e:
            self.append_out(f"Σφάλμα χρόνου εκτέλεσης: {e}")
            self.highlight_error_from_message(e)
        except Exception as e:
            self.append_out(f"Άγνωστο σφάλμα: {e}")
        finally:
            self.debug_finish()

    def debug_before_statement(self, stmt, env):
        """Handle the callback before each statement executes."""
        if self.debug_stop_requested:
            raise DebugStop()
        self.highlight_debug_line(getattr(stmt, "line", None))
        if env is not None:
            self.update_watch(env)
        if self.debug_continue_mode:
            return
        self.debug_wait_var.set(False)
        self.wait_variable(self.debug_wait_var)
        if self.debug_stop_requested:
            raise DebugStop()

    def debug_after_statement(self, stmt, env):
        """Update watch panel after each statement completes."""
        if env is not None:
            self.update_watch(env)

    def debug_finish(self):
        """Reset debugger state after a session completes."""
        self.debug_active = False
        self.debug_continue_mode = False
        self.debug_stop_requested = False
        self.debug_hook = None
        self.debug_prog = None
        self.debug_env = None
        self.debug_wait_var.set(True)
        self.clear_debug_highlight()

    def open_file(self):
        """Open a Glossa file and load it into the editor."""
        samples_dir = os.path.join(BASE_DIR, "samples")
        initial_dir = samples_dir if os.path.exists(samples_dir) else BASE_DIR
        path = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=[("Glossa files","*.gls *.txt *.psc"),("All files","*.*")])
        if not path: return
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        self.editor.delete("1.0","end")
        self.editor.insert("1.0", data)
        self.highlight_all()
        self.update_line_numbers()
        self.current_file = path
        self.update_window_title()

    def save_file(self):
        """Persist the current buffer to disk, prompting for a filename once."""
        if not self.current_file:
            path = filedialog.asksaveasfilename(defaultextension=".gls", filetypes=[("Glossa files","*.gls *.txt *.psc")])
            if not path: return
            self.current_file = path
        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0","end-1c"))
        self.update_window_title()
        messagebox.showinfo("Αποθήκευση", "Το αρχείο αποθηκεύτηκε.")

    def save_as_file(self):
        """Save the current buffer to a new file, always prompting for filename."""
        samples_dir = os.path.join(BASE_DIR, "samples")
        initial_dir = samples_dir if os.path.exists(samples_dir) else BASE_DIR
        path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            defaultextension=".gls",
            filetypes=[("Glossa files","*.gls *.txt *.psc")])
        if not path: return
        self.current_file = path
        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0","end-1c"))
        self.update_window_title()
        messagebox.showinfo("Αποθήκευση ως", "Το αρχείο αποθηκεύτηκε.")

    def run_code(self):
        """Compile and execute the buffer using the in-process compiler."""
        if self.debug_active:
            messagebox.showinfo("Αποσφαλμάτωση", "Σταματήστε πρώτα την αποσφαλμάτωση για κανονική εκτέλεση.")
            return
        src = self.editor.get("1.0","end-1c")
        self.prepare_output()
        self.clear_debug_highlight()
        self.update_watch(None)
        try:
            tokens = glossa.lex(src)
            parser = glossa.Parser(tokens)
            prog = parser.parse()
            env = glossa.Env(prog.var_decls, procedures=prog.procedures, functions=prog.functions)
            io = GUIIO(self.output)
            try:
                glossa.exec_statements(prog.statements, env, io)
            except glossa.FunctionReturn:
                self.append_out("Η εντολή ΕΠΙΣΤΡΕΨΕ χρησιμοποιήθηκε εκτός συνάρτησης")
        except glossa.LexerError as e:
            self.append_out(f"Σφάλμα αναλυτή (Lexer): {e}")
            self.highlight_error_from_message(e)
        except glossa.ParseError as e:
            self.append_out(f"Σφάλμα σύνταξης: {e}")
            self.highlight_error_from_message(e)
        except glossa.RuntimeErrorGlossa as e:
            self.append_out(f"Σφάλμα χρόνου εκτέλεσης: {e}")
            self.highlight_error_from_message(e)
        except Exception as e:
            self.append_out(f"Άγνωστο σφάλμα: {e}")

    def append_out(self, text):
        """Append text to the console widget, scrolling as needed."""
        self.output.config(state='normal')
        self.output.insert('end', str(text) + "\n")
        self.output.see('end')
        self.output.config(state='disabled')

if __name__ == "__main__":
    app = GlossaIDE()
    app.mainloop()
