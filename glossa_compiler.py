
# -*- coding: utf-8 -*-
"""Minimal Glossa language compiler/interpreter.

The module lexes Glossa source code, parses it into a lightweight abstract
syntax tree, and immediately interprets the program. It supports a subset of
the language aimed at educational usage inside the bundled Tk IDE. Execution
is intentionally single-pass and keeps the data structures simple so new
students can follow the implementation.
"""
import re
from dataclasses import dataclass
from typing import List, Any, Optional, Tuple, Dict, Union

# -------------------- Lexer --------------------
Token = Tuple[str, Any, int]  # (type, value, line)
VarInfo = Tuple[str, Optional[List[int]]]  # (base type, dimensions or None)

KEYWORDS = {
    "ΠΡΟΓΡΑΜΜΑ": "PROGRAM",
    "ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ": "END_PROGRAM",
    "ΣΤΑΘΕΡΕΣ": "CONSTS",
    "ΜΕΤΑΒΛΗΤΕΣ": "VARS",
    "ΑΡΧΗ": "BEGIN",
    "ΑΝ": "IF",
    "ΤΟΤΕ": "THEN",
    "ΑΛΛΙΩΣ": "ELSE",
    "ΤΕΛΟΣ_ΑΝ": "END_IF",
    "ΟΣΟ": "WHILE",
    "ΕΠΑΝΑΛΑΒΕ": "DO",
    "ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ": "END_LOOP",
    "ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ": "REPEAT",
    "ΜΕΧΡΙΣ_ΟΤΟΥ": "UNTIL",
    "ΓΙΑ": "FOR",
    "ΑΠΟ": "FROM",
    "ΜΕΧΡΙ": "TO",
    "ΜΕ_ΒΗΜΑ": "STEP",
    "ΓΡΑΨΕ": "WRITE",
    "ΔΙΑΒΑΣΕ": "READ",
    "ΔΙΑΔΙΚΑΣΙΑ": "PROC",
    "ΤΕΛΟΣ_ΔΙΑΔΙΚΑΣΙΑΣ": "END_PROC",
    "ΣΥΝΑΡΤΗΣΗ": "FUNC",
    "ΤΕΛΟΣ_ΣΥΝΑΡΤΗΣΗΣ": "END_FUNC",
    "ΚΑΛΕΣΕ": "CALL",
    "ΕΠΙΣΤΡΕΨΕ": "RETURN",
    "ΕΠΙΛΕΞΕ": "SELECT",
    "ΠΕΡΙΠΤΩΣΗ": "CASE",
    "ΤΕΛΟΣ_ΕΠΙΛΟΓΩΝ": "END_SELECT",
    "ΠΙΝΑΚΕΣ": "ARRAYS",
    "ΑΛΗΘΗΣ": "TRUE",
    "ΨΕΥΔΗΣ": "FALSE",
    # Types
    "ΑΚΕΡΑΙΕΣ": "TYPE_INT",
    "ΑΚΕΡΑΙΑ": "TYPE_INT",
    "ΠΡΑΓΜΑΤΙΚΕΣ": "TYPE_REAL",
    "ΠΡΑΓΜΑΤΙΚΗ": "TYPE_REAL",
    "ΧΑΡΑΚΤΗΡΕΣ": "TYPE_CHAR",
    "ΧΑΡΑΚΤΗΡΑΣ": "TYPE_CHAR",
    "ΛΟΓΙΚΕΣ": "TYPE_BOOL",
    "ΛΟΓΙΚΗ": "TYPE_BOOL",
    # Operator words
    "DIV": "DIV",
    "MOD": "MOD",
    "ΚΑΙ": "AND",
    "Η": "OR",
    "ΟΧΙ": "NOT",
}

SYMBOLS = {
    "<-": "ASSIGN",
    "<=": "LE",
    ">=": "GE",
    "<>": "NE",
    "=": "EQ",
    "<": "LT",
    ">": "GT",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MUL",
    "/": "DIVIDE",
    "%": "MOD_SYM",
    "(": "LPAREN",
    ")": "RPAREN",
    "[": "LBRACKET",
    "]": "RBRACKET",
    ",": "COMMA",
    ":": "COLON",
}

IDENT_RE = re.compile(
    r"[A-Za-zΑ-Ωα-ωΆΈΉΊΌΎΏάέήίόύώϊΐϋΰ_][0-9A-Za-zΑ-Ωα-ωΆΈΉΊΌΎΏάέήίόύώϊΐϋΰ_]*"
)
NUM_RE = re.compile(r"\d+(\.\d+)?")
WS_RE = re.compile(r"[ \t]+")

class LexerError(Exception):
    """Raised when the lexer cannot match the current character sequence."""
    pass

def lex(source: str) -> List[Token]:
    """Return a token stream for *source* according to the Glossa language."""
    tokens: List[Token] = []
    i = 0
    line = 1
    n = len(source)
    while i < n:
        ch = source[i]
        # Newlines
        if ch == "\n":
            line += 1
            i += 1
            continue
        # Comments: '!' to end of line
        if ch == "!":
            while i < n and source[i] != "\n":
                i += 1
            continue
        # Whitespace
        m = WS_RE.match(source, i)
        if m:
            i = m.end()
            continue
        # Strings in double quotes or Greek quotes «...»
        if ch == '"' or ch == "«":
            quote = ch
            endq = '"' if quote == '"' else "»"
            i += 1
            s = ""
            while i < n and source[i] != endq:
                if source[i] == "\\":
                    if i+1 < n:
                        s += source[i+1]
                        i += 2
                        continue
                s += source[i]
                i += 1
            if i >= n or source[i] != endq:
                raise LexerError(f"Μη κλεισμένο αλφαριθμητικό στη γραμμή {line}")
            i += 1
            tokens.append(("STRING", s, line))
            continue
        # Multi-char symbols first
        matched = False
        for sym in ["<-","<=",">=","<>"]:
            if source.startswith(sym, i):
                tokens.append((SYMBOLS[sym], sym, line))
                i += len(sym)
                matched = True
                break
        if matched:
            continue
        # Single-char symbols
        if ch in SYMBOLS:
            tokens.append((SYMBOLS[ch], ch, line))
            i += 1
            continue
        # Numbers
        m = NUM_RE.match(source, i)
        if m:
            text = m.group(0)
            val = int(text) if "." not in text else float(text)
            tokens.append(("NUMBER", val, line))
            i = m.end()
            continue
        # Identifiers / keywords
        m = IDENT_RE.match(source, i)
        if m:
            ident = m.group(0)
            ttype = KEYWORDS.get(ident, "ID")
            val = True if ttype == "TRUE" else False if ttype == "FALSE" else ident
            tokens.append((ttype, val, line))
            i = m.end()
            continue
        raise LexerError(f"Μη αναγνωρίσιμο σύμβολο '{ch}' στη γραμμή {line}")
    tokens.append(("EOF", None, line))
    return tokens

# -------------------- Parser / AST --------------------

@dataclass
class ASTNode:
    """Base AST node capturing the source line number."""
    line: int

@dataclass
class Program(ASTNode):
    """Program header plus declarations and body statements."""
    name: str
    var_decls: Dict[str, VarInfo]  # name -> (type, dimensions)
    statements: List[ASTNode]
    procedures: Dict[str, "ProcedureDef"]
    functions: Dict[str, "FunctionDef"]

@dataclass
class Assign(ASTNode):
    """Assignment ``μεταβλητή <- έκφραση``."""
    name: str
    expr: ASTNode
    indices: Optional[List[ASTNode]] = None

@dataclass
class Write(ASTNode):
    """Output command emitting one or more expressions."""
    exprs: List[ASTNode]

@dataclass
class Read(ASTNode):
    """Input command reading values into variables."""
    targets: List[ASTNode]

@dataclass
class ProcCall(ASTNode):
    """ΚΑΛΕΣΕ statement invoking a procedure."""
    name: str
    args: List[ASTNode]

@dataclass
class Return(ASTNode):
    """ΕΠΙΣΤΡΕΨΕ statement returning from a function."""
    expr: Optional[ASTNode]

@dataclass
class If(ASTNode):
    """Conditional statement with optional else branch."""
    cond: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]]

@dataclass
class While(ASTNode):
    """ΟΣΟ loop guarded by a boolean expression."""
    cond: ASTNode
    body: List[ASTNode]

@dataclass
class Repeat(ASTNode):
    """ΑΡΧΗ_ΕΠΑΝΑΛΗΨΗΣ loop evaluated until condition becomes true."""
    body: List[ASTNode]
    cond: ASTNode

@dataclass
class Select(ASTNode):
    """ΕΠΙΛΕΞΕ multi-way branch with one or more ΠΕΡΙΠΤΩΣΗ blocks."""
    expr: ASTNode
    cases: List[Tuple[List[ASTNode], List[ASTNode]]]
    default: Optional[List[ASTNode]]

@dataclass
class For(ASTNode):
    """ΓΙΑ loop with start, end, optional step, and body."""
    var: str
    start: ASTNode
    end: ASTNode
    step: Optional[ASTNode]
    body: List[ASTNode]

@dataclass
class Parameter:
    """Subprogram parameter metadata."""
    name: str
    type: str

@dataclass
class ProcedureDef(ASTNode):
    """ΔΙΑΔΙΚΑΣΙΑ definition."""
    name: str
    params: List[Parameter]
    locals: Dict[str, VarInfo]
    statements: List[ASTNode]

@dataclass
class FunctionDef(ASTNode):
    """ΣΥΝΑΡΤΗΣΗ definition."""
    name: str
    params: List[Parameter]
    locals: Dict[str, VarInfo]
    statements: List[ASTNode]
    return_type: str

# Expressions
@dataclass
class BinOp(ASTNode):
    """Binary operator node (π.χ. +, -, AND)."""
    op: str
    left: ASTNode
    right: ASTNode

@dataclass
class UnOp(ASTNode):
    """Unary operator node (π.χ. NOT, unary minus)."""
    op: str
    expr: ASTNode

@dataclass
class Var(ASTNode):
    """Variable reference expression."""
    name: str

@dataclass
class ArrayRef(ASTNode):
    """Array element reference expression."""
    name: str
    indices: List[ASTNode]

@dataclass
class Number(ASTNode):
    """Numeric literal."""
    value: Union[int,float]

@dataclass
class String(ASTNode):
    """String literal."""
    value: str

@dataclass
class Bool(ASTNode):
    """Boolean literal."""
    value: bool

@dataclass
class FuncCall(ASTNode):
    """Function call returning a value."""
    name: str
    args: List[ASTNode]

class ParseError(Exception):
    """Raised when parsing fails due to invalid token ordering."""
    pass

class Parser:
    """Recursive-descent parser turning tokens into an AST."""

    def __init__(self, tokens: List[Token]):
        """Store the token list and initialise the cursor."""
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        """Return the token currently under the parser cursor."""
        return self.tokens[self.pos]

    def accept(self, *types: str) -> Optional[Token]:
        """Consume and return the current token if its type matches."""
        ttype, val, line = self.current()
        if ttype in types:
            self.pos += 1
            return (ttype, val, line)
        return None

    def expect(self, *types: str) -> Token:
        """Consume the current token or raise if it is not of the expected type."""
        tok = self.accept(*types)
        if not tok:
            ttype, val, line = self.current()
            raise ParseError(f"Συντακτικό λάθος στη γραμμή {line}: αναμενόταν {' ή '.join(types)}, βρέθηκε {ttype}")
        return tok

    def parse(self) -> Program:
        """Parse an entire Glossa program and return the AST."""
        t = self.expect("PROGRAM")
        _, _, line = t
        name_tok = self.expect("ID")
        name = name_tok[1]
        var_decls = self.parse_variable_sections()
        self.expect("BEGIN")
        stmts: List[ASTNode] = []
        procedures: Dict[str, ProcedureDef] = {}
        functions: Dict[str, FunctionDef] = {}
        while self.current()[0] != "END_PROGRAM":
            token = self.current()[0]
            if token == "PROC":
                proc = self.parse_procedure_def()
                if proc.name in procedures or proc.name in functions:
                    raise ParseError(f"Η υπορουτίνα '{proc.name}' έχει ήδη δηλωθεί")
                procedures[proc.name] = proc
                continue
            if token == "FUNC":
                func = self.parse_function_def()
                if func.name in procedures or func.name in functions:
                    raise ParseError(f"Η υπορουτίνα '{func.name}' έχει ήδη δηλωθεί")
                functions[func.name] = func
                continue
            stmts.append(self.parse_statement())
        self.expect("END_PROGRAM")
        while self.current()[0] != "EOF":
            token = self.current()[0]
            if token == "PROC":
                proc = self.parse_procedure_def()
                if proc.name in procedures or proc.name in functions:
                    raise ParseError(f"Η υπορουτίνα '{proc.name}' έχει ήδη δηλωθεί")
                procedures[proc.name] = proc
                continue
            if token == "FUNC":
                func = self.parse_function_def()
                if func.name in procedures or func.name in functions:
                    raise ParseError(f"Η υπορουτίνα '{func.name}' έχει ήδη δηλωθεί")
                functions[func.name] = func
                continue
            raise ParseError("Απροσδόκητο περιεχόμενο μετά το ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ")
        self.expect("EOF")
        return Program(line=line, name=name, var_decls=var_decls, statements=stmts, procedures=procedures, functions=functions)

    def parse_statements(self, until: Tuple[str, ...]) -> List[ASTNode]:
        """Collect statements until one of the tokens listed in *until* is met."""
        res: List[ASTNode] = []
        while self.current()[0] not in until:
            res.append(self.parse_statement())
        return res

    def parse_array_dimensions(self) -> List[int]:
        """Parse a bracketed list of integer dimensions."""
        self.expect("LBRACKET")
        dims: List[int] = []
        tok = self.expect("NUMBER")
        if not isinstance(tok[1], int):
            raise ParseError(f"Το μέγεθος πίνακα πρέπει να είναι ακέραιο (γραμμή {tok[2]})")
        if tok[1] <= 0:
            raise ParseError(f"Το μέγεθος πίνακα πρέπει να είναι θετικό (γραμμή {tok[2]})")
        dims.append(tok[1])
        while self.accept("COMMA"):
            tok = self.expect("NUMBER")
            if not isinstance(tok[1], int):
                raise ParseError(f"Το μέγεθος πίνακα πρέπει να είναι ακέραιο (γραμμή {tok[2]})")
            if tok[1] <= 0:
                raise ParseError(f"Το μέγεθος πίνακα πρέπει να είναι θετικό (γραμμή {tok[2]})")
            dims.append(tok[1])
        self.expect("RBRACKET")
        if len(dims) not in (1, 2):
            raise ParseError(f"Υποστηρίζονται μόνο μονοδιάστατοι ή διδιάστατοι πίνακες")
        return dims

    def parse_index_list(self) -> List[ASTNode]:
        """Parse one or more comma-separated index expressions."""
        indices = [self.parse_expr()]
        while self.accept("COMMA"):
            indices.append(self.parse_expr())
        return indices

    def parse_read_target(self) -> ASTNode:
        tok = self.expect("ID")
        name = tok[1]
        line = tok[2]
        if self.accept("LBRACKET"):
            indices = self.parse_index_list()
            self.expect("RBRACKET")
            return ArrayRef(line=line, name=name, indices=indices)
        return Var(line=line, name=name)

    def parse_variable_sections(self) -> Dict[str, VarInfo]:
        decls: Dict[str, VarInfo] = {}
        type_tokens = ("TYPE_INT","TYPE_REAL","TYPE_CHAR","TYPE_BOOL")
        while True:
            section = self.current()[0]
            if section == "VARS":
                self.pos += 1
                while self.current()[0] in type_tokens:
                    type_tok = self.expect(*type_tokens)
                    self.expect("COLON")
                    while True:
                        id_tok = self.expect("ID")
                        if id_tok[1] in decls:
                            raise ParseError(f"Η μεταβλητή '{id_tok[1]}' έχει ήδη δηλωθεί")
                        decls[id_tok[1]] = (type_tok[0], None)
                        if not self.accept("COMMA"):
                            break
                continue
            if section == "ARRAYS":
                self.pos += 1
                while self.current()[0] in type_tokens:
                    type_tok = self.expect(*type_tokens)
                    self.expect("COLON")
                    while True:
                        id_tok = self.expect("ID")
                        if id_tok[1] in decls:
                            raise ParseError(f"Η μεταβλητή '{id_tok[1]}' έχει ήδη δηλωθεί")
                        dims = self.parse_array_dimensions()
                        decls[id_tok[1]] = (type_tok[0], dims)
                        if not self.accept("COMMA"):
                            break
                continue
            break
        return decls

    def parse_parameter_list(self) -> List[Parameter]:
        params: List[Parameter] = []
        self.expect("LPAREN")
        if self.accept("RPAREN"):
            return params
        while True:
            name_tok = self.expect("ID")
            pname = name_tok[1]
            self.expect("COLON")
            type_tok = self.expect("TYPE_INT","TYPE_REAL","TYPE_CHAR","TYPE_BOOL")
            if any(p.name == pname for p in params):
                raise ParseError(f"Η παράμετρος '{pname}' έχει ήδη δηλωθεί")
            params.append(Parameter(name=pname, type=type_tok[0]))
            if self.accept("COMMA"):
                continue
            self.expect("RPAREN")
            break
        return params

    def parse_argument_list(self) -> List[ASTNode]:
        args: List[ASTNode] = []
        if self.accept("RPAREN"):
            return args
        args.append(self.parse_expr())
        while self.accept("COMMA"):
            args.append(self.parse_expr())
        self.expect("RPAREN")
        return args

    def parse_procedure_def(self) -> ProcedureDef:
        header = self.expect("PROC")
        _, _, line = header
        name_tok = self.expect("ID")
        params = self.parse_parameter_list()
        locals_decl = self.parse_variable_sections()
        self.expect("BEGIN")
        body = self.parse_statements(until=("END_PROC",))
        self.expect("END_PROC")
        return ProcedureDef(line=line, name=name_tok[1], params=params, locals=locals_decl, statements=body)

    def parse_function_def(self) -> FunctionDef:
        header = self.expect("FUNC")
        _, _, line = header
        name_tok = self.expect("ID")
        params = self.parse_parameter_list()
        self.expect("COLON")
        ret_type = self.expect("TYPE_INT","TYPE_REAL","TYPE_CHAR","TYPE_BOOL")[0]
        locals_decl = self.parse_variable_sections()
        self.expect("BEGIN")
        body = self.parse_statements(until=("END_FUNC",))
        self.expect("END_FUNC")
        return FunctionDef(line=line, name=name_tok[1], params=params, locals=locals_decl, statements=body, return_type=ret_type)

    def parse_statement(self) -> ASTNode:
        """Parse a single statement based on the next token."""
        ttype, val, line = self.current()
        if ttype == "WRITE":
            self.pos += 1
            exprs = [self.parse_expr()]
            while self.accept("COMMA"):
                exprs.append(self.parse_expr())
            return Write(line=line, exprs=exprs)
        if ttype == "READ":
            self.pos += 1
            targets = [self.parse_read_target()]
            while self.accept("COMMA"):
                targets.append(self.parse_read_target())
            return Read(line=line, targets=targets)
        if ttype == "CALL":
            self.pos += 1
            name_tok = self.expect("ID")
            self.expect("LPAREN")
            args = self.parse_argument_list()
            return ProcCall(line=line, name=name_tok[1], args=args)
        if ttype == "RETURN":
            self.pos += 1
            expr = self.parse_expr()
            return Return(line=line, expr=expr)
        if ttype == "IF":
            self.pos += 1
            cond = self.parse_expr()
            self.expect("THEN")
            then_body = self.parse_statements(until=("ELSE","END_IF"))
            else_body = None
            if self.accept("ELSE"):
                else_body = self.parse_statements(until=("END_IF",))
            self.expect("END_IF")
            return If(line=line, cond=cond, then_body=then_body, else_body=else_body)
        if ttype == "WHILE":
            self.pos += 1
            cond = self.parse_expr()
            self.expect("DO")
            body = self.parse_statements(until=("END_LOOP",))
            self.expect("END_LOOP")
            return While(line=line, cond=cond, body=body)
        if ttype == "REPEAT":
            self.pos += 1
            body = self.parse_statements(until=("UNTIL",))
            self.expect("UNTIL")
            cond = self.parse_expr()
            return Repeat(line=line, body=body, cond=cond)
        if ttype == "SELECT":
            self.pos += 1
            expr = self.parse_expr()
            cases: List[Tuple[List[ASTNode], List[ASTNode]]] = []
            default_body: Optional[List[ASTNode]] = None
            while True:
                next_type = self.current()[0]
                if next_type == "END_SELECT":
                    break
                self.expect("CASE")
                if self.accept("ELSE"):
                    self.accept("COLON")
                    default_body = self.parse_statements(until=("CASE","END_SELECT"))
                else:
                    values: List[ASTNode] = [self.parse_expr()]
                    while self.accept("COMMA"):
                        values.append(self.parse_expr())
                    self.expect("COLON")
                    body = self.parse_statements(until=("CASE","END_SELECT"))
                    cases.append((values, body))
                    continue
                # after default body, consume remaining cases? spec says default likely last
            self.expect("END_SELECT")
            return Select(line=line, expr=expr, cases=cases, default=default_body)
        if ttype == "FOR":
            self.pos += 1
            varname = self.expect("ID")[1]
            self.expect("FROM")
            start = self.parse_expr()
            self.expect("TO")
            end = self.parse_expr()
            step = None
            if self.accept("STEP"):
                step = self.parse_expr()
            body = self.parse_statements(until=("END_LOOP",))
            self.expect("END_LOOP")
            return For(line=line, var=varname, start=start, end=end, step=step, body=body)
        if ttype == "ID":
            self.pos += 1
            name = val
            indices = None
            if self.accept("LBRACKET"):
                indices = self.parse_index_list()
                self.expect("RBRACKET")
            self.expect("ASSIGN")
            expr = self.parse_expr()
            return Assign(line=line, name=name, expr=expr, indices=indices)
        raise ParseError(f"Άγνωστη εντολή στη γραμμή {line}: {ttype}")

    def parse_expr(self) -> ASTNode:
        """Parse an expression following Glossa precedence rules."""
        return self.parse_or()

    def parse_or(self) -> ASTNode:
        """Parse OR chains."""
        node = self.parse_and()
        while self.accept("OR"):
            rhs = self.parse_and()
            node = BinOp(op="OR", left=node, right=rhs, line=node.line)
        return node

    def parse_and(self) -> ASTNode:
        """Parse AND chains."""
        node = self.parse_not()
        while self.accept("AND"):
            rhs = self.parse_not()
            node = BinOp(op="AND", left=node, right=rhs, line=node.line)
        return node

    def parse_not(self) -> ASTNode:
        """Parse unary NOT expressions."""
        if self.accept("NOT"):
            expr = self.parse_not()
            return UnOp(op="NOT", expr=expr, line=expr.line)
        return self.parse_cmp()

    def parse_cmp(self) -> ASTNode:
        """Parse comparison operators."""
        node = self.parse_add()
        t = self.accept("EQ","NE","LT","LE","GT","GE")
        if t:
            op = t[0]
            rhs = self.parse_add()
            node = BinOp(op=op, left=node, right=rhs, line=node.line)
        return node

    def parse_add(self) -> ASTNode:
        """Parse addition/subtraction expressions."""
        node = self.parse_mul()
        while True:
            t = self.accept("PLUS","MINUS")
            if not t: break
            op = t[0]
            rhs = self.parse_mul()
            node = BinOp(op=op, left=node, right=rhs, line=node.line)
        return node

    def parse_mul(self) -> ASTNode:
        """Parse multiplication/division expressions."""
        node = self.parse_unary()
        while True:
            t = self.accept("MUL","DIVIDE","DIV","MOD","MOD_SYM")
            if not t: break
            op = t[0]
            rhs = self.parse_unary()
            node = BinOp(op=op, left=node, right=rhs, line=node.line)
        return node

    def parse_unary(self) -> ASTNode:
        """Parse unary plus/minus."""
        t = self.accept("MINUS","PLUS")
        if t:
            op = t[0]
            expr = self.parse_unary()
            return UnOp(op=op, expr=expr, line=expr.line)
        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        """Parse literals, identifiers, or parenthesised expressions."""
        ttype, val, line = self.current()
        if ttype == "NUMBER":
            self.pos += 1
            return Number(line=line, value=val)
        if ttype == "STRING":
            self.pos += 1
            return String(line=line, value=val)
        if ttype in ("TRUE","FALSE"):
            self.pos += 1
            return Bool(line=line, value=(ttype=="TRUE"))
        if ttype == "ID":
            self.pos += 1
            name = val
            if self.accept("LPAREN"):
                args = self.parse_argument_list()
                return FuncCall(line=line, name=name, args=args)
            if self.accept("LBRACKET"):
                indices = self.parse_index_list()
                self.expect("RBRACKET")
                return ArrayRef(line=line, name=name, indices=indices)
            return Var(line=line, name=name)
        if ttype == "LPAREN":
            self.pos += 1
            node = self.parse_expr()
            self.expect("RPAREN")
            return node
        raise ParseError(f"Συντακτικό λάθος στη γραμμή {line}: αναμενόταν έκφραση, βρέθηκε {ttype}")

# -------------------- Interpreter --------------------

class RuntimeErrorGlossa(Exception):
    """Raised while executing a program when runtime semantics are violated."""
    pass


class FunctionReturn(Exception):
    """Internal control flow exception for function returns."""

    def __init__(self, value: Any):
        self.value = value

class Env:
    """Hold variable metadata and values during interpretation."""

    def __init__(self, var_types: Dict[str, VarInfo], parent: Optional["Env"] = None,
                 procedures: Optional[Dict[str, ProcedureDef]] = None,
                 functions: Optional[Dict[str, FunctionDef]] = None):
        """Initialise storage with default values for declared variables."""
        self.parent = parent
        self.types = dict(var_types)
        self.values: Dict[str, Any] = {}
        self.procedures = procedures if procedures is not None else (parent.procedures if parent else {})
        self.functions = functions if functions is not None else (parent.functions if parent else {})
        for name, (base, dims) in self.types.items():
            if dims is None:
                self.values[name] = self._default_value(base)
            else:
                self.values[name] = self._make_array(dims, base)

    def _default_value(self, tp: str):
        if tp == "TYPE_INT":
            return 0
        if tp == "TYPE_REAL":
            return 0.0
        if tp == "TYPE_CHAR":
            return ""
        if tp == "TYPE_BOOL":
            return False
        raise RuntimeErrorGlossa(f"Άγνωστος τύπος {tp}")

    def _make_array(self, dims: List[int], tp: str):
        if len(dims) == 1:
            return [self._default_value(tp) for _ in range(dims[0])]
        if len(dims) == 2:
            rows, cols = dims
            return [
                [self._default_value(tp) for _ in range(cols)]
                for _ in range(rows)
            ]
        raise RuntimeErrorGlossa("Υποστηρίζονται μόνο 1D ή 2D πίνακες")

    def _coerce(self, tp: str, value: Any):
        if tp == "TYPE_INT":
            if isinstance(value, bool):
                value = int(value)
            if isinstance(value, float):
                value = int(value)
            if not isinstance(value, int):
                raise RuntimeErrorGlossa("Αναμενόταν ακέραιος")
            return value
        if tp == "TYPE_REAL":
            if isinstance(value, bool):
                value = float(value)
            if isinstance(value, int):
                value = float(value)
            if not isinstance(value, float):
                raise RuntimeErrorGlossa("Αναμενόταν πραγματικός")
            return value
        if tp == "TYPE_CHAR":
            if not isinstance(value, str):
                raise RuntimeErrorGlossa("Αναμενόταν αλφαριθμητικό")
            return value
        if tp == "TYPE_BOOL":
            if not isinstance(value, bool):
                raise RuntimeErrorGlossa("Αναμενόταν λογική τιμή")
            return value
        raise RuntimeErrorGlossa(f"Άγνωστος τύπος {tp}")

    def _find_owner(self, name: str) -> Optional["Env"]:
        if name in self.types:
            return self
        if self.parent:
            return self.parent._find_owner(name)
        return None

    def get_type(self, name: str) -> Tuple[str, Optional[List[int]]]:
        owner = self._find_owner(name)
        if owner is None:
            raise RuntimeErrorGlossa(f"Άγνωστη μεταβλητή '{name}'")
        return owner.types[name]

    def _resolve_indices(self, name: str, indices: List[int]) -> Tuple["Env", Any, List[int], str]:
        owner = self._find_owner(name)
        if owner is None:
            raise RuntimeErrorGlossa(f"Άγνωστη μεταβλητή '{name}'")
        base_type, dims = owner.types[name]
        if dims is None:
            raise RuntimeErrorGlossa(f"Η '{name}' δεν είναι πίνακας")
        if len(indices) != len(dims):
            raise RuntimeErrorGlossa(f"Ο πίνακας '{name}' αναμένει {len(dims)} δείκτες")
        zero_based: List[int] = []
        for idx_val, size in zip(indices, dims):
            if not isinstance(idx_val, int):
                raise RuntimeErrorGlossa("Οι δείκτες πίνακα πρέπει να είναι ακέραιοι")
            if idx_val < 1 or idx_val > size:
                raise RuntimeErrorGlossa(f"Η πρόσβαση στον πίνακα '{name}' είναι εκτός ορίων")
            zero_based.append(idx_val - 1)
        array_obj = owner.values[name]
        return owner, array_obj, zero_based, base_type

    def set(self, name: str, val: Any, indices: Optional[List[int]] = None):
        """Assign *val* to *name*, supporting optional array indices."""
        owner = self._find_owner(name)
        if owner is None:
            raise RuntimeErrorGlossa(f"Άγνωστη μεταβλητή '{name}'")
        base_type, dims = owner.types[name]
        if indices is None:
            if dims is not None:
                raise RuntimeErrorGlossa(f"Η '{name}' είναι πίνακας - απαιτούνται δείκτες")
            coerced = owner._coerce(base_type, val)
            owner.values[name] = coerced
            return
        owner_env, array_obj, zero_indices, base = self._resolve_indices(name, indices)
        coerced = owner_env._coerce(base, val)
        if len(zero_indices) == 1:
            array_obj[zero_indices[0]] = coerced
        else:
            array_obj[zero_indices[0]][zero_indices[1]] = coerced

    def get(self, name: str, indices: Optional[List[int]] = None):
        """Return the current value for *name* or a specific array element."""
        owner = self._find_owner(name)
        if owner is None:
            raise RuntimeErrorGlossa(f"Άγνωστη μεταβλητή '{name}'")
        base_type, dims = owner.types[name]
        if indices is None:
            if dims is not None:
                raise RuntimeErrorGlossa(f"Η '{name}' είναι πίνακας - δώσε δείκτες")
            return owner.values[name]
        _, array_obj, zero_indices, _ = self._resolve_indices(name, indices)
        if len(zero_indices) == 1:
            return array_obj[zero_indices[0]]
        return array_obj[zero_indices[0]][zero_indices[1]]

class IOHandler:
    """Abstract I/O surface used by the interpreter."""

    def __init__(self, input_queue: Optional[List[str]] = None):
        """Initialise a handler with optional scripted input."""
        self.outputs: List[str] = []
        self.input_queue = input_queue or []

    def write(self, text: str):
        """Record text output."""
        self.outputs.append(text)

    def read(self) -> str:
        """Pop the next scripted input or fail if none is available."""
        if not self.input_queue:
            raise RuntimeErrorGlossa("Απαιτείται είσοδος (ΔΙΑΒΑΣΕ) αλλά δεν δόθηκε input_queue")
        return self.input_queue.pop(0)

def eval_expr(node: ASTNode, env: Env, io: IOHandler, debugger=None) -> Any:
    """Evaluate an expression node within *env* and return the value."""
    if isinstance(node, Number):
        return node.value
    if isinstance(node, String):
        return node.value
    if isinstance(node, Bool):
        return node.value
    if isinstance(node, Var):
        return env.get(node.name)
    if isinstance(node, ArrayRef):
        indices = [_coerce_index(eval_expr(idx, env, io, debugger), node.line) for idx in node.indices]
        return env.get(node.name, indices)
    if isinstance(node, FuncCall):
        return call_function(node.name, node.args, env, io, debugger)
    if isinstance(node, UnOp):
        v = eval_expr(node.expr, env, io, debugger)
        if node.op == "MINUS":
            return -v
        if node.op == "PLUS":
            return +v
        if node.op == "NOT":
            return (not bool(v))
        raise RuntimeErrorGlossa("Άγνωστος μονοσήμαντος τελεστής")
    if isinstance(node, BinOp):
        l = eval_expr(node.left, env, io, debugger)
        r = eval_expr(node.right, env, io, debugger)
        op = node.op
        if op == "PLUS": return l + r
        if op == "MINUS": return l - r
        if op == "MUL": return l * r
        if op == "DIVIDE":
            if r == 0:
                raise RuntimeErrorGlossa("Διαίρεση με το μηδέν")
            return l / r
        if op == "DIV":
            if r == 0:
                raise RuntimeErrorGlossa("Διαίρεση με το μηδέν")
            return int(l) // int(r)
        if op in ("MOD","MOD_SYM"):
            if r == 0:
                raise RuntimeErrorGlossa("Υπόλοιπο με το μηδέν")
            return int(l) % int(r)
        if op == "EQ": return l == r
        if op == "NE": return l != r
        if op == "LT": return l < r
        if op == "LE": return l <= r
        if op == "GT": return l > r
        if op == "GE": return l >= r
        if op == "AND": return bool(l) and bool(r)
        if op == "OR": return bool(l) or bool(r)
        raise RuntimeErrorGlossa("Άγνωστος τελεστής")
    raise RuntimeErrorGlossa("Μη υποστηριζόμενη έκφραση")

def _coerce_index(value: Any, line: int) -> int:
    """Convert an index expression result to an integer with validation."""
    if isinstance(value, bool):
        value = int(value)
    if isinstance(value, float):
        if value.is_integer():
            value = int(value)
        else:
            raise RuntimeErrorGlossa(f"Ο δείκτης πίνακα πρέπει να είναι ακέραιος (γραμμή {line})")
    if not isinstance(value, int):
        raise RuntimeErrorGlossa(f"Ο δείκτης πίνακα πρέπει να είναι ακέραιος (γραμμή {line})")
    return value

def _convert_input(raw: str, base_type: str):
    """Convert text input to the requested base type."""
    if base_type == "TYPE_INT":
        return int(raw)
    if base_type == "TYPE_REAL":
        return float(raw)
    if base_type == "TYPE_CHAR":
        return str(raw)
    if base_type == "TYPE_BOOL":
        return True if raw.strip().upper() in ("ΑΛΗΘΗΣ","TRUE","1") else False
    return raw


def call_procedure(name: str, args: List[ASTNode], env: Env, io: IOHandler, debugger=None):
    proc = env.procedures.get(name)
    if proc is None:
        raise RuntimeErrorGlossa(f"Άγνωστη διαδικασία '{name}'")
    if len(args) != len(proc.params):
        raise RuntimeErrorGlossa(f"Η διαδικασία '{name}' αναμένει {len(proc.params)} ορίσματα")
    evaluated_args = [eval_expr(arg, env, io, debugger) for arg in args]
    local_types: Dict[str, VarInfo] = dict(proc.locals)
    for param in proc.params:
        local_types[param.name] = (param.type, None)
    child_env = Env(local_types, parent=env)
    for param, value in zip(proc.params, evaluated_args):
        child_env.set(param.name, value)
    try:
        exec_statements(proc.statements, child_env, io, debugger=debugger)
    except FunctionReturn:
        raise RuntimeErrorGlossa(f"Η διαδικασία '{name}' δεν μπορεί να επιστρέψει τιμή")


def call_function(name: str, args: List[ASTNode], env: Env, io: IOHandler, debugger=None):
    func = env.functions.get(name)
    if func is None:
        raise RuntimeErrorGlossa(f"Άγνωστη συνάρτηση '{name}'")
    if len(args) != len(func.params):
        raise RuntimeErrorGlossa(f"Η συνάρτηση '{name}' αναμένει {len(func.params)} ορίσματα")
    evaluated_args = [eval_expr(arg, env, io, debugger) for arg in args]
    local_types: Dict[str, VarInfo] = dict(func.locals)
    for param in func.params:
        local_types[param.name] = (param.type, None)
    child_env = Env(local_types, parent=env)
    for param, value in zip(func.params, evaluated_args):
        child_env.set(param.name, value)
    try:
        exec_statements(func.statements, child_env, io, debugger=debugger)
    except FunctionReturn as ret:
        return child_env._coerce(func.return_type, ret.value)
    raise RuntimeErrorGlossa(f"Η συνάρτηση '{name}' δεν επέστρεψε τιμή")

def exec_statements(stmts: List[ASTNode], env: Env, io: IOHandler, debugger=None):
    """Execute a list of statements sequentially.

    If *debugger* is supplied, its ``before_statement`` and ``after_statement``
    hooks (when available) wrap every statement execution.
    """
    for st in stmts:
        if debugger and hasattr(debugger, "before_statement"):
            debugger.before_statement(st, env)
        exec_statement(st, env, io, debugger=debugger)
        if debugger and hasattr(debugger, "after_statement"):
            debugger.after_statement(st, env)

def exec_statement(st: ASTNode, env: Env, io: IOHandler, debugger=None):
    """Execute a single statement node."""
    if isinstance(st, Assign):
        val = eval_expr(st.expr, env, io, debugger)
        indices = None
        if st.indices is not None:
            indices = [_coerce_index(eval_expr(idx, env, io, debugger), idx.line) for idx in st.indices]
        env.set(st.name, val, indices=indices)
    elif isinstance(st, Write):
        parts = [eval_expr(e, env, io, debugger) for e in st.exprs]
        def to_text(v):
            if isinstance(v, bool): return "ΑΛΗΘΗΣ" if v else "ΨΕΥΔΗΣ"
            return str(v)
        io.write(" ".join(to_text(p) for p in parts))
    elif isinstance(st, Read):
        for target in st.targets:
            raw = io.read()
            if isinstance(target, Var):
                base_type, _ = env.get_type(target.name)
                val = _convert_input(raw, base_type)
                env.set(target.name, val)
            elif isinstance(target, ArrayRef):
                base_type, _ = env.get_type(target.name)
                val = _convert_input(raw, base_type)
                indices = [_coerce_index(eval_expr(idx, env, io, debugger), idx.line) for idx in target.indices]
                env.set(target.name, val, indices=indices)
            else:
                raise RuntimeErrorGlossa("Μη υποστηριζόμενος στόχος ΔΙΑΒΑΣΕ")
    elif isinstance(st, If):
        cond = eval_expr(st.cond, env, io, debugger)
        if cond:
            exec_statements(st.then_body, env, io, debugger=debugger)
        elif st.else_body is not None:
            exec_statements(st.else_body, env, io, debugger=debugger)
    elif isinstance(st, While):
        while eval_expr(st.cond, env, io, debugger):
            exec_statements(st.body, env, io, debugger=debugger)
    elif isinstance(st, Repeat):
        while True:
            exec_statements(st.body, env, io, debugger=debugger)
            if eval_expr(st.cond, env, io, debugger):
                break
    elif isinstance(st, Select):
        target = eval_expr(st.expr, env, io, debugger)
        matched = False
        for values, body in st.cases:
            for val_expr in values:
                if eval_expr(val_expr, env, io, debugger) == target:
                    exec_statements(body, env, io, debugger=debugger)
                    matched = True
                    break
            if matched:
                break
        if not matched and st.default is not None:
            exec_statements(st.default, env, io, debugger=debugger)
    elif isinstance(st, ProcCall):
        call_procedure(st.name, st.args, env, io, debugger)
    elif isinstance(st, Return):
        value = eval_expr(st.expr, env, io, debugger) if st.expr is not None else None
        raise FunctionReturn(value)
    elif isinstance(st, For):
        start = eval_expr(st.start, env, io, debugger)
        end = eval_expr(st.end, env, io, debugger)
        step = eval_expr(st.step, env, io, debugger) if st.step is not None else 1
        env.set(st.var, start)
        if step >= 0:
            while env.get(st.var) <= end:
                exec_statements(st.body, env, io, debugger=debugger)
                env.set(st.var, env.get(st.var)+step)
        else:
            while env.get(st.var) >= end:
                exec_statements(st.body, env, io, debugger=debugger)
                env.set(st.var, env.get(st.var)+step)
    else:
        raise RuntimeErrorGlossa(f"Μη υποστηριζόμενη εντολή στη γραμμή {st.line}")

def compile_and_run(source: str, inputs: Optional[List[str]] = None) -> List[str]:
    """Convenience helper that lexes, parses, and executes *source*."""
    tokens = lex(source)
    parser = Parser(tokens)
    prog = parser.parse()
    env = Env(prog.var_decls, procedures=prog.procedures, functions=prog.functions)
    io = IOHandler(inputs)
    try:
        exec_statements(prog.statements, env, io)
    except FunctionReturn:
        raise RuntimeErrorGlossa("Η εντολή ΕΠΙΣΤΡΕΨΕ χρησιμοποιήθηκε εκτός συνάρτησης")
    return io.outputs

if __name__ == "__main__":
    src = """ΠΡΟΓΡΑΜΜΑ ΔΟΚΙΜΗ
ΜΕΤΑΒΛΗΤΕΣ
    ΑΚΕΡΑΙΕΣ: α, β, i
    ΛΟΓΙΚΕΣ: λ
ΑΡΧΗ
    α <- 5
    β <- 3
    ΓΡΑΨΕ "Άθροισμα:", α + β
    ΑΝ α > β ΤΟΤΕ
        ΓΡΑΨΕ "μεγαλύτερο"
    ΑΛΛΙΩΣ
        ΓΡΑΨΕ "όχι"
    ΤΕΛΟΣ_ΑΝ
    ΓΙΑ i ΑΠΟ 1 ΜΕΧΡΙ 3
        ΓΡΑΨΕ i
    ΤΕΛΟΣ_ΕΠΑΝΑΛΗΨΗΣ
ΤΕΛΟΣ_ΠΡΟΓΡΑΜΜΑΤΟΣ
"""
    out = compile_and_run(src)
    for line in out:
        print(line)
