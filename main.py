import ast
import unittest

class EliminateAdditionWithZero: 
    
    @classmethod
    def check(cls, node: ast.BinOp) -> bool:
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            # Check if either operand is a constant with value 0
            if isinstance(node.right, ast.Constant) and node.right.value == 0 or \
               isinstance(node.left, ast.Constant) and node.left.value == 0:
                return True
        return False
    
    @classmethod
    def apply(self, node: ast.BinOp) -> ast.AST:
        if isinstance(node.right, ast.Constant) and node.right.value == 0:
            return node.left
        else: 
            return node.right
        
class EliminateSubtractionByZero: 
    
    @classmethod
    def check(cls, node: ast.BinOp) -> bool:
        return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub) and isinstance(node.right, ast.Constant) and node.right.value == 0 
    
    @classmethod
    def apply(self, node: ast.BinOp) -> ast.AST:
        return node.left

class EliminateMultiplicationByOne:

    @classmethod
    def check(cls, node: ast.BinOp) -> bool:
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
            # Check if either operand is a contant with value 1
            if isinstance(node.right, ast.Constant) and node.right.value == 1 or \
               isinstance(node.left, ast.Constant) and node.left.value == 1:
                return True
        return False
    
    @classmethod
    def apply(self, node: ast.BinOp) -> ast.AST:
        if isinstance(node.right, ast.Constant) and node.right.value == 1:
            return node.left
        else: 
            return node.right

class Visitor(ast.NodeTransformer):
    
    def visit_BinOp(self, node: ast.AST) -> ast.AST:
        if EliminateAdditionWithZero.check(node):
            return EliminateAdditionWithZero.apply(node)
        elif EliminateSubtractionByZero.check(node):
            return EliminateSubtractionByZero.apply(node)
        elif EliminateMultiplicationByOne.check(node):
            return EliminateMultiplicationByOne.apply(node)
        else:
            # Visit the children nodes and return the transformed node
            return self.generic_visit(node)

class TestRewriteStrategies(unittest.TestCase):
    def test_eliminate_addition_with_zero(self):
        # Create an instance of Visitor
        visitor = Visitor()

        # Create an AST node representing 'x + 0'
        left = ast.Name(id='x', ctx=ast.Load()) 
        right = ast.Constant(0)
        addition_node = ast.BinOp(left, ast.Add(), right)

        # Apply the strategy and check the result
        simplified_ast = visitor.visit(addition_node)
        self.assertEqual(simplified_ast, left)

        # Create an AST node representing '0 + x'
        left = ast.Constant(0)
        right = ast.Name(id='x', ctx=ast.Load()) 
        addition_node = ast.BinOp(left, ast.Add(), right)

        # Apply the strategy and check the result
        simplified_ast = visitor.visit(addition_node)
        self.assertEqual(simplified_ast, right)

    def test_eliminate_subtraction_by_zero(self):
        # Create an instance of Visitor
        visitor = Visitor()

        # Create an AST node representing 'x - 0'
        left = ast.Name(id='x', ctx=ast.Load()) 
        right = ast.Constant(0)
        subtraction_node = ast.BinOp(left, ast.Sub(), right)

        # Apply the strategy and check the result
        simplified_ast = visitor.visit(subtraction_node)
        self.assertEqual(simplified_ast, left)

        # Create an AST node representing '0 - x'
        left = ast.Constant(0)
        right = ast.Name(id='x', ctx=ast.Load()) 
        subtraction_node = ast.BinOp(left, ast.Sub(), right)

        # Apply the strategy and check the result
        simplified_ast = visitor.visit(subtraction_node)
        self.assertEqual(simplified_ast, subtraction_node)

    def test_eliminate_multiplication_by_one(self):
        # Create an instance of Visitor
        visitor = Visitor()

        # Create an AST node representing 'x + 1'
        left = ast.Name(id='x', ctx=ast.Load()) 
        right = ast.Constant(1)
        multiplication_node = ast.BinOp(left, ast.Mult(), right)

        # Apply the strategy and check the result
        simplified_ast = visitor.visit(multiplication_node)
        self.assertEqual(simplified_ast, left)

        # Create an AST node representing '1 + x'
        left = ast.Constant(1)
        right = ast.Name(id='x', ctx=ast.Load()) 
        multiplication_node = ast.BinOp(left, ast.Mult(), right)

        # Apply the strategy and check the result
        simplified_ast = visitor.visit(multiplication_node)
        self.assertEqual(simplified_ast, right)

if __name__ == '__main__':
    unittest.main()