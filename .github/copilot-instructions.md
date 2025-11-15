# Glossa IDE Toolkit – AI Coding Agent Instructions

## Project Overview
Educational Greek programming language (ΓΛΩΣΣΑ) compiler and Tkinter-based IDE for high-school computer science curriculum. Zero external dependencies – pure Python 3.9+ with stdlib only.

**Core architecture**: Single-pass interpreter with lexer → parser → immediate AST execution. No intermediate bytecode or optimization passes – intentionally simple for educational transparency.

## Key Components

### `glossa_compiler.py` (1138 lines)
**Single-file compiler implementing the complete language pipeline:**
- **Lexer** (`lex()`): Regex-based tokenizer handling Greek keywords, UTF-8 strings (`"..."` or `«...»`), comments (`!` to EOL), and multi-char operators (`<-`, `<=`, `>=`, `<>`)
- **Parser** (`Parser` class): Recursive-descent parser producing dataclass AST nodes (`Program`, `Assign`, `If`, `While`, `For`, `Select`, `ProcedureDef`, `FunctionDef`, etc.)
- **Interpreter** (`exec_statement()`, `eval_expr()`): Direct AST walker with no optimization. Environment (`Env` class) manages variable scoping with parent-chain lookup for nested procedure/function contexts
- **Type system**: Variables declared with Greek types (`ΑΚΕΡΑΙΕΣ`, `ΠΡΑΓΜΑΤΙΚΕΣ`, `ΧΑΡΑΚΤΗΡΕΣ`, `ΛΟΓΙΚΕΣ`) and coerced at assignment/expression evaluation
- **Arrays**: 1D/2D only, 1-indexed (`Δεδομένα[1]` to `Δεδομένα[n]`), bounds-checked at runtime via `_resolve_indices()`
- **Built-in functions** (`call_builtin_function()`): Eight mathematical functions implemented using Python's `math` module:
  - `Α_Μ(x)`: Integer part (truncates towards zero)
  - `Α_Τ(x)`: Absolute value (preserves type: int→int, float→float)
  - `Ε(x)`: Exponential (e^x)
  - `ΕΦ(x)`, `ΗΜ(x)`, `ΣΥΝ(x)`: Tangent, sine, cosine (input in **degrees**, not radians)
  - `ΛΟΓ(x)`: Natural logarithm (rejects x ≤ 0)
  - `Τ_Ρ(x)`: Square root (rejects x < 0)
- **I/O abstraction**: `IOHandler` base class with `write()`/`read()` methods – overridden by `GUIIO` in IDE for console redirection

**Critical implementation details:**
- Variables default-initialized: `TYPE_INT→0`, `TYPE_REAL→0.0`, `TYPE_CHAR→""`, `TYPE_BOOL→False`
- Loop semantics: `ΓΙΑ i ΑΠΟ start ΜΕΧΡΙ end ΜΕ_ΒΗΜΑ step` allows negative steps for countdown
- Function returns: Internal `FunctionReturn` exception propagates values up the call stack
- Debugger hooks: `before_statement(stmt, env)` / `after_statement(stmt, env)` callbacks injected during `exec_statements()`

### `glossa_ide_tk.py` (458 lines)
**Tkinter desktop IDE with integrated debugger:**
- **Editor**: `tk.Text` widget with line numbers (`line_numbers` sidebar), syntax highlighting via tags (`"kw"`, `"str"`, `"com"`), and error line highlighting (`"error_line"`, `"debug_line"`)
- **Console**: Disabled `tk.Text` for output; `GUIIO` overrides `IOHandler.write()` to append lines, `IOHandler.read()` uses `simpledialog.askstring()` for `ΔΙΑΒΑΣΕ` prompts
- **Watch panel**: Shows variables as `name = value` with scope markers `[L]` (local) or `[G]` (global/outer)
- **Debugger state machine**:
  - `debug_step()`: First click initializes debugger, subsequent clicks advance one statement (blocking via `wait_variable(self.debug_wait_var)`)
  - `debug_continue()`: Runs until program end or error without pausing
  - `debug_stop()`: Raises `DebugStop` exception to abort execution
  - `TkDebuggerHook`: Adapter bridging compiler callbacks to IDE methods (`debug_before_statement()`, `debug_after_statement()`)
- **Syntax highlighting**: Applied on `<KeyRelease>` events via regex matching Greek keywords (`ΠΡΟΓΡΑΜΜΑ`, `ΑΝ`, `ΟΣΟ`, etc.) and string/comment patterns

**UI layout:**
```
Toolbar (Άνοιγμα, Αποθήκευση, Εκτέλεση, Βήμα, Συνέχεια, Διακοπή)
├─ PanedWindow (vertical)
│  ├─ Editor frame (line_numbers + editor + scrollbar)
│  └─ Output frame
│     └─ PanedWindow (horizontal)
│        ├─ Console (output text widget)
│        └─ Watch panel (variable display)
```

### `run_ide.py` (10 lines)
Launcher entry point – instantiates `GlossaIDE()` and calls `mainloop()`. Used by PyInstaller for bundling.

### `samples/` (50+ `.gls` files)
Chapter-aligned example programs demonstrating language features. Each file follows the template:
```
! Περιγραφή: [Brief description in Greek]
! Βήμα 1: [Step-by-step explanation]
! Βήμα 2: ...
ΠΡΟΓΡΑΜΜΑ ΌνομαΠρογράμματος
ΜΕΤΑΒΛΗΤΕΣ
    ...
ΑΡΧΗ
    ...
ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ
```

**Key samples for feature reference:**
- `builtin_functions.gls`: Comprehensive test of all 8 built-in mathematical functions
- `factorial.gls`: Input validation, `ΓΙΑ` loop
- `procedures_demo.gls`: `ΔΙΑΔΙΚΑΣΙΑ` and `ΣΥΝΑΡΤΗΣΗ` definitions
- `ch04_recursive_minimum.gls`: Divide-and-conquer recursion with global array access
- `ch03_queue_array.gls`: Circular queue with modular arithmetic
- `ch08_case_tiering.gls`: `ΕΠΙΛΕΞΕ` multi-way branching

## Development Workflows

### Running the IDE
```bash
python run_ide.py
```
Opens Tkinter window with starter template pre-loaded. No environment activation needed (pure stdlib).

### Testing compiler standalone
```python
from glossa_compiler import compile_and_run

source = """ΠΡΟΓΡΑΜΜΑ Τεστ
ΜΕΤΑΒΛΗΤΕΣ
    ΑΚΕΡΑΙΕΣ: α
ΑΡΧΗ
    α <- 42
    ΓΡΑΨΕ α
ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ"""

outputs = compile_and_run(source, inputs=[])  # Returns list of ΓΡΑΨΕ outputs
```

### Building executables (PyInstaller)
**macOS**: `bash Bundles/build_mac.sh` (produces `Bundles/dist/macOS/glossa-ide.app`)
**Windows x64**: `powershell Bundles\build_windows_x64.ps1`
**Windows ARM64**: `powershell Bundles\build_windows_arm64.ps1`

**Critical flags**: `--add-data "samples:samples"` bundles sample programs into executable

### Adding language features
1. **Lexer**: Add keyword to `KEYWORDS` dict or symbol to `SYMBOLS` dict in `glossa_compiler.py`
2. **AST**: Define new `@dataclass` node inheriting from `ASTNode` (see existing patterns like `While`, `For`)
3. **Parser**: Add production rule in `Parser` class (e.g., new method or extend `parse_statement()`)
4. **Interpreter**: Handle new node type in `exec_statement()` or `eval_expr()`
5. **IDE**: If new keyword, add to `KEYWORDS` list in `glossa_ide_tk.py` for syntax highlighting

### Adding built-in functions
Built-in functions are checked before user-defined functions in `call_function()`:
1. Add function name to `builtin_funcs` list in `call_builtin_function()`
2. Implement logic with appropriate error handling (domain validation for math functions)
3. Use `math.radians()` for trigonometric functions (ΓΛΩΣΣΑ spec requires degrees, not radians)
4. Return `None` from `call_builtin_function()` to fall through to user-defined function lookup

### Debugging strategy
- **Syntax errors**: Raised by `Parser` with Greek messages (`"Συντακτικό λάθος στη γραμμή {line}..."`)
- **Runtime errors**: `RuntimeErrorGlossa` exceptions with descriptive Greek text (e.g., `"Διαίρεση με το μηδέν"`, `"Άγνωστη μεταβλητή"`)
- **Division by zero**: Handled in `eval_expr()` for `/`, `DIV`, `MOD` operators
- **Array bounds**: Checked in `Env._resolve_indices()` with 1-indexed validation

## Project-Specific Conventions

### Greek-first naming
- **Keywords**: Always Greek (`ΠΡΟΓΡΑΜΜΑ`, `ΜΕΤΑΒΛΗΤΕΣ`, `ΑΝ`, `ΤΟΤΕ`, etc.) – never English equivalents
- **Error messages**: Written in Greek for target student audience
- **UI labels**: Toolbar buttons and menu items use Greek text (`Άνοιγμα`, `Εκτέλεση`, etc.)
- **Code comments**: Mix of Greek (for domain concepts) and English (for technical implementation notes)

### Type coercion rules
- `bool → int/float` allowed (e.g., `ΑΛΗΘΗΣ` becomes `1` or `1.0`)
- `int → float` automatic in mixed expressions
- No implicit string conversions – must be explicit in user code

### Parser design patterns
- **Token lookahead**: Use `self.current()` to inspect, `self.accept(*types)` to conditionally consume, `self.expect(*types)` to enforce
- **Error recovery**: None – first error halts parsing with descriptive Greek message
- **Subprogram placement**: Procedures/functions parsed after main program body OR after `ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ` (both locations supported)

### IDE event handling
- **Syntax highlighting**: Triggered on `<KeyRelease>` – only re-highlights current line for performance
- **File state tracking**: `self.current_file` stores path; `None` indicates unsaved buffer
- **Debugger blocking**: Uses `wait_variable(self.debug_wait_var)` to pause execution until next `Βήμα` click

## Integration Points

### Compiler ↔ IDE coupling
- IDE imports `glossa_compiler` module directly (no subprocess isolation)
- IDE provides `GUIIO(output_widget)` to redirect `ΓΡΑΨΕ` output to console
- Debugger: IDE creates `TkDebuggerHook` instance and passes to `exec_statements(debugger=...)`

### PyInstaller bundling
- `--windowed` flag suppresses console window on Windows/macOS
- `--onefile` produces single executable with samples embedded
- Notarization: Optional `Bundles/notarize_mac.sh` for macOS Gatekeeper (requires Apple Developer ID)

## External Dependencies
**None** – project uses only Python stdlib. `requirements.txt` is empty except for reminder to ensure Tkinter support.

**Python builds**: Some distributions (e.g., Debian/Ubuntu apt, Homebrew) ship Python without Tk. Install `python3-tk` (Debian) or `python-tk@3.10` (Homebrew) if needed.

## Documentation Standards
- **Sample programs**: Must include `! Περιγραφή:` and numbered `! Βήμα N:` comments explaining algorithm steps
- **Code docstrings**: English for implementation details (e.g., `"""Recursive-descent parser turning tokens into an AST."""`)
- **README**: Bilingual (English + Greek) – English for technical setup, Greek for curriculum alignment and usage guide

## Testing Approach
**No formal test suite** – validation via 50+ sample programs covering language features. To verify changes:
1. Load sample in IDE (`Άνοιγμα` → select `.gls` file)
2. Click `Εκτέλεση` – confirm output matches expected behavior
3. Use `Βήμα` debugger to step through and verify variable states

**Common edge cases to verify:**
- Empty arrays, single-element arrays, max-size arrays (declared bounds)
- Negative loop steps (`ΓΙΑ i ΑΠΟ 10 ΜΕΧΡΙ 1 ΜΕ_ΒΗΜΑ -1`)
- Recursive functions without base case (should stack overflow gracefully)
- Division/modulo by zero (must raise `RuntimeErrorGlossa`)

## File Naming Patterns
- Core modules: `glossa_*.py` (e.g., `glossa_compiler.py`, `glossa_ide_tk.py`)
- Samples: `chXX_*.gls` for chapter-specific, `*.gls` for basics (e.g., `factorial.gls`, `arrays_2d.gls`)
- Build outputs: `Bundles/dist/{macOS,windows-x64,windows-arm64}/`
