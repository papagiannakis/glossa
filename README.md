# Glossa IDE Toolkit

---

## 📚 Prof. George Papagiannakis

**University of Crete, Greece**  
**Foundation for Research and Technology - Hellas (FORTH-ICS)**

*Copyright © 2025 George Papagiannakis. All rights reserved.*

---

## Overview
This repository contains a lightweight implementation of the Greek educational programming language ΓΛΩΣΣΑ together with a Tkinter-based IDE. It is intended as a ready-to-use teaching toolkit for the “Ανάπτυξη Εφαρμογών σε Προγραμματιστικό Περιβάλλον” curriculum.

### Key features
- **ΓΛΩΣΣΑ interpreter** (`glossa_compiler.py`): lexer, parser, and interpreter that support the full high-school subset—assignments, αριθμητικές/λογικές εκφράσεις, συνθήκες, `ΟΣΟ`, `ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ`, `ΓΙΑ ... ΜΕ_ΒΗΜΑ`, `ΕΠΙΛΕΞΕ`, πολυδιάστατους πίνακες, διαδικασίες, συναρτήσεις, αναδρομή, και χειρισμό σφαλμάτων (π.χ. διαίρεση με το μηδέν).
- **Desktop IDE** (`glossa_ide_tk.py`): Tkinter-based editor with syntax highlighting, drag–resize panes, Ελληνικό UI, γραμμή εργαλείων, debugging (βήμα–βήμα, συνέχεια, διακοπή), watches [τοπικές/καθολικές], φωτισμό τρέχουσας γραμμής και εμφάνιση σφαλμάτων.
- **Extensive sample suite** (`samples/`): 50+ έτοιμα παραδείγματα με σχόλια “Περιγραφή / Βήμα-βήμα” που καλύπτουν από βασικούς αλγορίθμους έως προχωρημένες τεχνικές (δυναμικός προγραμματισμός, BFS, αναδρομή με απομνημόνευση, αξιολόγηση ποιότητας λογισμικού).
- **Tk-first workflow**: καμία εξάρτηση από τρίτες βιβλιοθήκες· αρκεί η standard βιβλιοθήκη της Python.

## Requirements
- Python 3.9+ with Tkinter support (e.g. the Elements 3.10 environment or the system CPython build).
- No third-party packages are needed; standard-library Tkinter and dataclasses are sufficient.

If you use a Python build without Tk support, install the appropriate system package (e.g. `sudo apt install python3-tk` on Debian/Ubuntu or `brew install python-tk@3.10` on macOS).

## Installation
1. Clone or download this repository.
2. (Optional) Create a virtual environment aligned with the Elements310 distribution or another Python 3.9+ install.
3. Ensure Tkinter is available by running `python - <<'PY'\nimport tkinter\nprint('Tk OK')\nPY`.

## Running the IDE
Launch the IDE with:
```bash
python run_ide.py
```
This opens the Tk window with a starter ΓΛΩΣΣΑ program. Use the toolbar buttons to open/save files, execute programs, or drive the debugger (`Βήμα`, `Συνέχεια`, `Διακοπή`).

## IDE quickstart

### English guide
- **Layout**: Editor (left), output console and watch panel (right). The watch panel labels local variables with `[L]` and outer-scope ones with `[G]`.
- **Open (`Άνοιγμα`)**: load an existing `.gls` file; the editor highlights ΓΛΩΣΣΑ keywords automatically.
- **Save (`Αποθήκευση`)**: write the current tab back to disk; unsaved changes trigger a prompt when closing.
- **Run (`Εκτέλεση`)**: compile and execute the whole program, printing `ΓΡΑΨΕ` output in the console.
- **Step (`Βήμα`)**: start the debugger (first click) and advance one statement per click. The current line is highlighted in yellow.
- **Continue (`Συνέχεια`)**: resume execution until the next breakpoint (first error) or program completion.
- **Stop (`Διακοπή`)**: terminate the running/paused program and clear the debugger state.
- **Error handling**: syntax errors appear in the console and the offending line is highlighted; runtime errors (e.g. division by zero) show descriptive Greek messages.
- **Input**: when a program uses `ΔΙΑΒΑΣΕ`, the console prompts interactively; provide one value per line.

### Οδηγός στα Ελληνικά
- **Διάταξη**: επεξεργαστής αριστερά, κονσόλα και πίνακας παρακολούθησης δεξιά. Οι τοπικές μεταβλητές σημειώνονται με `[L]`, οι καθολικές με `[G]`.
- **Άνοιγμα**: φόρτωση υπάρχοντος αρχείου `.gls` με πλήρη επισήμανση σύνταξης.
- **Αποθήκευση**: καταγραφή των αλλαγών στο δίσκο· αν κλείσετε με εκκρεμείς αλλαγές, θα ζητηθεί επιβεβαίωση.
- **Εκτέλεση**: μεταφράζει και τρέχει ολόκληρο το πρόγραμμα, εμφανίζοντας τις εντολές `ΓΡΑΨΕ` στην κονσόλα.
- **Βήμα**: εκκινεί τον αποσφαλματωτή (στην πρώτη χρήση) και προχωράει μία εντολή κάθε φορά με οπτική επισήμανση.
- **Συνέχεια**: συνεχίζει την εκτέλεση μέχρι να ολοκληρωθεί ή να προκύψει σημείο διακοπής/σφάλμα.
- **Διακοπή**: τερματίζει την τρέχουσα εκτέλεση και καθαρίζει την κατάσταση του αποσφαλματωτή.
- **Σφάλματα**: συντακτικά λάθη και μηνύματα χρόνου εκτέλεσης εμφανίζονται στην κονσόλα, ενώ η σχετική γραμμή φωτίζεται για εύκολο εντοπισμό.
- **Είσοδος**: όταν χρησιμοποιείται `ΔΙΑΒΑΣΕ`, πληκτρολογείτε την τιμή στην κονσόλα και πατάτε Enter.

## Samples
Load any sample via *Άνοιγμα* in the IDE or run it programmatically with `glossa_compiler.compile_and_run(source, inputs=...)`.

### ΓΛΩΣΣΑ language coverage
- **Program structure** – `countdown.gls`, `ch06_program_structure.gls`
- **Input/Output (`ΔΙΑΒΑΣΕ` / `ΓΡΑΨΕ`)** – `countdown.gls`, `factorial.gls`, `ch08_factor_search.gls`
- **Assignments & expressions** – `ch02_stepwise_invoice.gls`, `ch07_expression_order.gls`
- **Arithmetic operators (`+`, `-`, `*`, `/`, `DIV`, `MOD`)** – `factorial.gls`, `ch02_gcd_bruteforce.gls`, `ch05_growth_ratio.gls`
- **Relational & logical operators** – `grades.gls`, `ch07_truth_table_and.gls`, `ch07_type_conversion_demo.gls`
- **Control flow (`ΑΝ` / `ΑΛΛΙΩΣ`)** – `factorial.gls`, `ch08_case_tiering.gls`
- **Multi-way selection (`ΕΠΙΛΕΞΕ`)** – `select_case.gls`, `ch08_case_tiering.gls`, `ch11_object_messages.gls`
- **Loops (`ΟΣΟ`, `ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ ... ΜΕΧΡΙΣ_ΟΤΟΥ`, `ΓΙΑ ... ΜΕ_ΒΗΜΑ`)** – `countdown.gls`, `repeat_until.gls`, `ch02_running_total.gls`, `ch02_binary_search_walkthrough.gls`
- **Stepped / decrement loops** – `ch04_dp_climb_stairs.gls`, `ch08_nested_loop_pattern.gls`
- **Procedures (`ΔΙΑΔΙΚΑΣΙΑ`)** – `procedures_demo.gls`, `ch10_grade_module.gls`, `ch11_object_accounts.gls`
- **Functions (`ΣΥΝΑΡΤΗΣΗ`)** – `procedures_demo.gls`, `ch10_geometry_library.gls`, `ch10_sequence_generators.gls`
- **Return & recursion (`ΕΠΙΣΤΡΕΨΕ`)** – `ch02_algorithm_equivalence.gls`, `ch04_recursive_minimum.gls`, `ch10_fast_power.gls`
- **Arrays (1D / 2D)** – `arrays_1d.gls`, `arrays_2d.gls`, `ch09_matrix_rotation.gls`, `ch09_transpose_matrix.gls`
- **Parallel arrays / record emulation** – `ch03_parallel_records.gls`, `ch11_object_accounts.gls`
- **Queue and stack operations** – `queue_demo.gls`, `ch03_queue_array.gls`, `ch03_stack_array.gls`, `ch03_stack_linked.gls`, `ch03_priority_queue.gls`
- **Dynamic programming / memoisation** – `ch04_dp_knapsack.gls`, `ch04_dp_climb_stairs.gls`, `ch10_grid_paths.gls`
- **Greedy algorithms** – `ch04_greedy_intervals.gls`, `ch04_greedy_coin_change.gls`
- **Search & sort** – `linear_search.gls`, `ch05_best_worst_linear.gls`, `ch04_merge_sort.gls`
- **Mathematical utilities / graph traversal** – `ch02_euclid_trace.gls`, `ch03_bfs_network.gls`
- **Runtime guards & error handling** – `ch13_runtime_guard.gls`, `ch08_factor_search.gls`
- **Tracing & debugging aids** – `ch13_trace_logger.gls`, `ch05_invariant_checker.gls`
- **Quality / documentation analytics** – `ch14_quality_dashboard.gls`, `ch14_mod11_checksum.gls`

### Core mini-examples
- `arrays_1d.gls` – populates a 1D array, then sums the contents.
- `arrays_2d.gls` – fills a 2×3 array and computes the aggregate total.
- `countdown.gls` – performs an interactive countdown using `ΟΣΟ`.
- `factorial.gls` – multiplies `2..ν` to obtain `n!` with input validation.
- `fibonacci.gls` – prints the first _k_ Fibonacci numbers iteratively.
- `grades.gls` – classifies a grade into *Αποτυχία / Καλώς / Λίαν καλώς / Άριστα*.
- `linear_search.gls` – scans user-provided values and reports the first match.
- `matrix_processing.gls` – reads a matrix, prints the diagonal, sum, and maximum.
- `procedures_demo.gls` – demonstrates procedure and function calls.
- `queue_demo.gls` – circular queue with push/pop and overflow detection.
- `repeat_until.gls` – minimal `ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ ... ΜΕΧΡΙΣ_ΟΤΟΥ` showcase.
- `select_case.gls` – `ΕΠΙΛΕΞΕ` dispatch across 1, 2–3, or default.
- `stack_demo.gls` – stack push/pop menu with underflow/overflow handling.

### Chapter-aligned advanced set
- **Κεφάλαιο 1** (Ανάλυση προβλήματος)  
  `ch01_capacity_balance.gls` – compares διαθέσιμη ικανότητα vs. ζήτηση ανά τρίμηνο.  
  `ch01_project_feasibility.gls` – evaluates συνολικό κόστος, διάρκεια, κίνδυνο έργου.  
  `ch01_risk_matrix.gls` – builds a risk matrix and suggests mitigation priorities.
- **Κεφάλαιο 2** (Βασικές έννοιες αλγορίθμων)  
  `ch02_algorithm_equivalence.gls` – compares iterative vs. recursive factorial.  
  `ch02_binary_search_walkthrough.gls` – traces search bounds step-by-step.  
  `ch02_euclid_trace.gls` – logs the Euclidean algorithm rounds for ΜΚΔ.  
  `ch02_gcd_bruteforce.gls` – brute-force ΜΚΔ μειώνοντας τον μικρότερο αριθμό με MOD.  
  `ch02_stepwise_invoice.gls` – sequential invoice calculation highlighting algorithmic steps.  
  `ch02_max_of_three.gls` – nested decisions to locate the largest of three values.  
  `ch02_running_total.gls` – running average via counted `ΓΙΑ` loop.  
  `ch02_swap_demo.gls` – demonstrates the swap pattern with a temporary variable.
- **Κεφάλαιο 3** (Δομές δεδομένων & αλγόριθμοι)  
  `ch03_bfs_network.gls` – breadth-first traversal over an adjacency matrix.  
  `ch03_queue_scheduling.gls` – FCFS scheduling with waiting-time analytics.  
  `ch03_stack_simulation.gls` – scripted stack operations with status reporting.  
  `ch03_queue_array.gls` – circular queue implementation with wrap-around indices.  
  `ch03_stack_array.gls` – fixed-size array stack with push/pop operations.  
  `ch03_stack_linked.gls` – stack emulated via linked structure pointers.  
  `ch03_priority_queue.gls` – priority-based dequeue using simple array scans.  
  `ch03_frequency_table.gls` – builds category frequency counts from survey votes.  
  `ch03_parallel_records.gls` – manages parallel arrays of names and grades.  
  `ch03_matrix_column_sums.gls` – sums each column of a 3×3 data grid.  
  `ch03_inventory_levels.gls` – adjusts stock levels after deliveries and orders.
- **Κεφάλαιο 4** (Τεχνικές σχεδίασης αλγορίθμων)  
  `ch04_dp_knapsack.gls` – 0/1 knapsack solved via dynamic programming.  
  `ch04_greedy_intervals.gls` – greedy activity selection sorted by finish time.  
  `ch04_merge_sort.gls` – classic divide-and-conquer merge sort.  
  `ch04_recursive_minimum.gls` – divide-and-conquer search for the minimum value.  
  `ch04_recursive_sum.gls` – recursive aggregation of array segments.  
  `ch04_dp_climb_stairs.gls` – staircase counting with memoised subproblems.  
  `ch04_greedy_coin_change.gls` – greedy change-making with euro-style coins.
- **Κεφάλαιο 5** (Ανάλυση αλγορίθμων)  
  `ch05_complexity_estimator.gls` – counts operations for an O(n²) loop nest.  
  `ch05_invariant_checker.gls` – tracks the insertion sort invariant per pass.  
  `ch05_search_comparison.gls` – contrasts linear vs. binary search effort.  
  `ch05_halving_counter.gls` – measures the logarithmic behaviour of repeated halving.  
  `ch05_nested_loop_table.gls` – tallies triangular numbers from nested loops.  
  `ch05_best_worst_linear.gls` – compares best/worst-case linear search passes.  
  `ch05_growth_ratio.gls` – contrasts n² and n³ growth rates for sample sizes.
- **Κεφάλαιο 6** (Εισαγωγή στον προγραμματισμό)  
  `ch06_language_selector.gls` – weighted scoring of programming language choices.  
  `ch06_parallel_readiness.gls` – flags tasks that fit parallel execution limits.  
  `ch06_translation_pipeline.gls` – models compiler stages and cumulative timings.  
  `ch06_language_generations.gls` – timeline of programming-language generations.  
  `ch06_translation_modes.gls` – associates compilation stages with tooling roles.  
  `ch06_program_structure.gls` – outlines input/process/output blocks.  
  `ch06_development_models.gls` – compares software development models and durations.
- **Κεφάλαιο 7** (Βασικές έννοιες προγραμματισμού)  
  `ch07_expression_stages.gls` – evaluates a composite expression step by step.  
  `ch07_type_audit.gls` – combines integers, reals, booleans per record.  
  `ch07_validation_suite.gls` – reusable function to validate measurement ranges.  
  `ch07_truth_table_and.gls` – prints the truth table of the logical AND operator.  
  `ch07_type_conversion_demo.gls` – illustrates implicit type conversions.  
  `ch07_expression_order.gls` – demonstrates operator precedence through staged results.  
  `ch07_constant_usage.gls` – pricing example using constant-like parameters.
- **Κεφάλαιο 8** (Επιλογή και επανάληψη)  
  `ch08_adaptive_iteration.gls` – adaptive step search towards a numeric target.  
  `ch08_decision_matrix.gls` – cross-references performance and attendance.  
  `ch08_repeat_convergence.gls` – Newton method for square roots with repeat-until.  
  `ch08_nested_loop_pattern.gls` – triangular star pattern from nested loops.  
  `ch08_factor_search.gls` – `ΟΣΟ` loop to locate the first divisor.  
  `ch08_repeat_threshold.gls` – repeat-until loop reducing a value to a limit.  
  `ch08_case_tiering.gls` – `ΕΠΙΛΕΞΕ` classification into satisfaction tiers.
- **Κεφάλαιο 9** (Πίνακες)  
  `ch09_matrix_rotation.gls` – rotates a 4×4 matrix by 90°.  
  `ch09_merge_datasets.gls` – merges two sorted sequences.  
  `ch09_sliding_window.gls` – moving-average filter over time series data.  
  `ch09_median_parity.gls` – διάμεσος ταξινομημένου πίνακα με έλεγχο MOD.  
  `ch09_transpose_matrix.gls` – constructs the transpose of a 3×3 matrix.  
  `ch09_row_averages.gls` – reports row means in a 4×3 dataset.  
  `ch09_histogram_bins.gls` – bins continuous measurements into histogram buckets.  
  `ch09_diagonal_sums.gls` – sums main and secondary diagonals of a 4×4 matrix.
- **Κεφάλαιο 10** (Υποπρογράμματα)  
  `ch10_fast_power.gls` – fast exponentiation using recursion.  
  `ch10_grid_paths.gls` – memoised count of lattice paths.  
  `ch10_statistical_modules.gls` – modular mean and variance computation.  
  `ch10_geometry_library.gls` – area/perimeter helpers for rectangles and circles.  
  `ch10_sequence_generators.gls` – functions returning triangular and square numbers.  
  `ch10_grade_module.gls` – procedure-based student report with verbal feedback.  
  `ch10_finance_tools.gls` – simple-interest and compound-value utilities.
- **Κεφάλαιο 11** (Σύγχρονα προγραμματιστικά περιβάλλοντα)  
  `ch11_event_dispatcher.gls` – event-type dispatch for GUI interactions.  
  `ch11_message_bus.gls` – routes messages to domain services by code range.  
  `ch11_ui_flow_controller.gls` – orchestrates UI states through a controller.  
  `ch11_object_accounts.gls` – ομοίωμα τάξης λογαριασμού με «μεθόδους» κατάθεσης/ανάληψης.  
  `ch11_object_messages.gls` – κοινή διαδικασία χειρισμού μηνυμάτων αντικειμένων διεπαφής.
- **Κεφάλαιο 12** (Σχεδίαση διεπαφής χρήστη)  
  `ch12_accessibility_audit.gls` – calculates WCAG contrast ratios.  
  `ch12_dialog_layout.gls` – detects misaligned cells in a dialog grid.  
  `ch12_menu_layout.gls` – checks if menu entries fit on one row.
- **Κεφάλαιο 13** (Εκσφαλμάτωση προγράμματος)  
  `ch13_error_classification.gls` – groups error codes into syntax/logic/runtime.  
  `ch13_runtime_guard.gls` – guards divisions against zero denominators.  
  `ch13_trace_logger.gls` – logs multiplication trace for debugging analysis.  
  `ch13_leap_year_rules.gls` – εφαρμογή των κανόνων mod 4/100/400 για δίσεκτα έτη.
- **Κεφάλαιο 14** (Αξιολόγηση – Τεκμηρίωση)  
  `ch14_documentation_tracker.gls` – reports documentation deliverable status.  
  `ch14_lifecycle_projection.gls` – accumulates phase durations in a lifecycle.  
  `ch14_quality_dashboard.gls` – weighted quality scoring across subsystems.  
  `ch14_mod11_checksum.gls` – υπολογισμός ψηφίου ελέγχου με MOD 11.

## Debugging Workflow
1. Click **Βήμα** to begin a debug session (first click compiles and stops on the first statement).
2. Use **Βήμα** to advance statement-by-statement or **Συνέχεια** to run freely until completion/stop.
3. The watch panel shows local `[L]` and outer-scope `[G]` variables; the current source line is highlighted.
4. Errors highlight the relevant line automatically with explanatory output in the console.

## Version History
- **v0.4.0** (current)
  - Added 36 new chapter-aligned samples (4 per chapter from 2–10) with inline walkthroughs.
  - Documented the IDE in English and Greek, covering toolbar controls and debugging workflow.
  - Refined geometry/finance examples for compatibility with the interpreter’s feature set.
- **v0.3.0**
  - Curated 40+ chapter-aligned sample programs with in-source documentation.
  - Expanded README and in-code comments for easier onboarding and teaching use.
  - Tidied repository assets for public publication (no generated artefacts).
- **v0.2.0**
  - Added repeat–until loops, switch/case branching, 1D/2D arrays, and full procedure/function support.
  - Enhanced IDE with debugger controls, watch panel, error highlighting, and line numbers.
  - Supplied the first wave of comprehensive sample programs.
- **v0.1.0**
  - Initial release with core ΓΛΩΣΣΑ interpreter, Tkinter IDE, and basic control-flow examples.

## Contributing / Extending
Pull requests are welcome. High-priority ideas:
- Breakpoints and call-stack inspection in the debugger.
- Pass-by-reference parameters for arrays.
- Exporting execution traces or unit tests for sample programs.
