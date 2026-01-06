import sys
from app.ast.expr import Expr, Binary, Grouping, Literal, Unary, Variable, Stmt, Expression, Print, Var, Block, If, While, Assign, Logical
from app.token.token_type import TokenType
from app.interpreter.environment import Environment


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

    def interpret(self, statements):
        try:
            for statement in statements:
                if statement is not None:
                    self.execute(statement)
        except RuntimeError as error:
            print(f"Runtime Error: {error}", file=sys.stderr)
            sys.exit(1)

    def execute(self, stmt: Stmt):
        return stmt.accept(self)

    def visit_block_stmt(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                if statement is not None:
                    self.execute(statement)
        finally:
            self.environment = previous

    def visit_if_stmt(self, stmt: If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None

    def visit_while_stmt(self, stmt: While):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_var_stmt(self, stmt: Var):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
            
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_expression_stmt(self, stmt: Expression):
        self.evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visit_variable_expr(self, expr: Variable):
        return self.environment.get(expr.name)

    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_logical_expr(self, expr: Logical):
        left = self.evaluate(expr.left)
        
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        elif expr.operator.type == TokenType.AND:
            if not self.is_truthy(left):
                return left
                
        return self.evaluate(expr.right)

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        elif expr.operator.type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif expr.operator.type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        elif expr.operator.type == TokenType.PLUS:
            # Handle both number addition and string concatenation
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, float) and isinstance(right, str):
                return self.stringify(left) + right
            elif isinstance(left, str) and isinstance(right, float):
                return left + self.stringify(right)
            else:
                raise RuntimeError("Operands must be two numbers or two strings.")
        elif expr.operator.type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        elif expr.operator.type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        # Unreachable
        return None

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

        # Unreachable
        return None

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(f"Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(f"Operands must be numbers.")

    def is_equal(self, a, b):
        # Handle nil (None) comparisons
        if a is None and b is None:
            return True
        if a is None:
            return False

        return a == b

    def is_truthy(self, obj):
        # False and nil are falsey, everything else is truthy
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def stringify(self, obj):
        if obj is None:
            return "nil"

        # Hack to remove trailing ".0" for integer-valued doubles
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(obj)