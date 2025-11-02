# Glossa IDE – macOS User Guide

# Glossa IDE Toolkit

---

## 📚 Prof. George Papagiannakis

**University of Crete, Greece**  
**Foundation for Research and Technology - Hellas (FORTH-ICS)**

*Copyright © 2025 George Papagiannakis. All rights reserved.*

---

## Getting Started
1. **Download / copy** the signed and notarized `glossa-ide.app` bundle created with `Bundles/build_mac.sh` and `Bundles/notarize_mac.sh`.
2. Double-click the app—no extra Gatekeeper confirmations should appear when the ticket is stapled. (If you are testing an unsigned build, see the build scripts to sign/notarize before distributing.)
3. The IDE ships with the Python runtime and required libraries, so no additional installation is needed. Just ensure your macOS version matches the architecture (Intel vs Apple Silicon) used during the build.

## IDE Overview
- **Toolbar**
  - `Άνοιγμα`: Load existing `.gls`, `.psc`, or `.txt` Glossa programs.
  - `Αποθήκευση`: Save the current editor buffer (prompts for a filename on first save).
  - `Εκτέλεση`: Run the program immediately; output appears in the console, and errors highlight the corresponding lines.
  - `Βήμα`: Start or advance a debugger session one statement at a time.
  - `Συνέχεια`: Resume execution without further pauses until completion or a manual stop.
  - `Διακοπή`: Halt the debugger and reset state.
- **Editor Pane**
  - Syntax highlighting for keywords, strings, comments.
  - Line numbers gutter for easy navigation.
  - Current statement highlight during debugging.
- **Console Output**
  - Displays program output and error messages; scrolls automatically.
  - Input prompts (for `ΔΙΑΒΑΣΕ`) appear as modal dialogs.
- **Watch Panel**
  - Lists the current values of variables. Local scope entries are tagged `[L]`, outer scopes `[G]`.

## Language Features Supported
- **Control Structures**
  - `ΑΝ ... ΑΛΛΙΩΣ ... ΤΕΛΟΣ_ΑΝ`
  - `ΟΣΟ ... ΕΠΑΝΑΛΑΒΕ ... ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ`
  - `ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ ... ΜΕΧΡΙΣ_ΟΤΟΥ`
  - `ΓΙΑ ... ΑΠΟ ... ΜΕΧΡΙ ... ΜΕ_ΒΗΜΑ`
  - `ΕΠΙΛΕΞΕ ... ΠΕΡΙΠΤΩΣΗ ... ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ`
- **Data Structures**
  - Scalar types: ΑΚΕΡΑΙΑ, ΠΡΑΓΜΑΤΙΚΗ, ΧΑΡΑΚΤΗΡΑ, ΛΟΓΙΚΗ.
  - 1D & 2D arrays via `ΠΙΝΑΚΕΣ` declarations with bounds checking.
- **I/O**
  - `ΓΡΑΨΕ` for formatted output (automatically adds spaces between expressions).
  - `ΔΙΑΒΑΣΕ` supports both scalar variables and array elements.
- **Subprograms**
  - `ΔΙΑΔΙΚΑΣΙΑ ... ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ` with typed parameters.
  - `ΣΥΝΑΡΤΗΣΗ ... ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ` returning typed results via `ΕΠΙΣΤΡΕΨΕ`.
  - Nested lexical scopes with separate local variables and inherited globals.
- **Expressions**
  - Arithmetic, relational, logical operators (`DIV`, `MOD`, `ΚΑΙ`, `Η`, `ΟΧΙ`).
  - Function calls inside expressions.
  - Parentheses for precedence control.

## Debugging Workflow
1. **Start**: Click `Βήμα`. The program compiles and pauses before the first statement.
2. **Step**: Repeat `Βήμα` to walk forward; the current line is highlighted.
3. **Continue**: Click `Συνέχεια` to run freely. Press `Βήμα` again to re-enter stepping mode.
4. **Stop**: Use `Διακοπή` to cancel the session. The console logs the interruption.
5. **Watch Panel**: Tracks variable updates after each statement. Array values show as Python-style lists.
6. **Error Highlighting**: Runtime exceptions or syntax errors color the relevant line; messages appear in the console.

## Sample Programs
The app bundles the `samples/` directory:
- Control flow examples (`countdown.gls`, `repeat_until.gls`, `select_case.gls`).
- Data processing (`matrix_processing.gls`, `arrays_*.gls`).
- Algorithms (`factorial.gls`, `fibonacci.gls`, `linear_search.gls`).
- Interactive demos (`stack_demo.gls`, `queue_demo.gls`).
- Subprogram showcase (`procedures_demo.gls`).
Open any sample via the toolbar to experiment.

## Known Limitations
- Array parameters are passed by value; large arrays should be manipulated globally for now.
- No breakpoint UI—debugger stepping begins at the top of the program.
- Generated `.app` is unsigned; macOS will show first-run warnings until you approve it in *System Settings → Privacy & Security*.

## Version History (macOS Bundles)
- **v0.2.0**
  - First macOS bundle with debugger, arrays, repeat–until, select/case, and subprogram support.
  - Bundled samples and watch panel enhancements.
- **v0.1.0**
  - Prototype release with core controls (open/save/run) and basic language subset.

For build steps or troubleshooting, refer to `Bundles/README.md`. Enjoy exploring ΓΛΩΣΣΑ on macOS!
