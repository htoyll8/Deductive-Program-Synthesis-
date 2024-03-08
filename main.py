import ast
import unittest

class EliminateAdditionWithZero: 
    
    @classmethod
    def check(cls, node: ast.BinOp) -> bool:
        return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add) and isinstance(node.right, ast.Constant) and node.right.value == 0
    
    @classmethod
    def apply(self, ast: ast.BinOp) -> ast.AST:
        return ast.left

class EliminateMultiplicationByOne:

    @classmethod
    def check(cls, node: ast.BinOp) -> bool:
        return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) and isinstance(node.right, ast.Constant) and node.right.value == 1
    
    @classmethod
    def apply(self, ast: ast.BinOp) -> ast.AST:
        return ast.left

class Visitor(ast.NodeTransformer):
    
    def visit_BinOp(self, node: ast.AST) -> ast.AST:
        if EliminateAdditionWithZero.check(node):
            return EliminateAdditionWithZero.apply(node)
        elif EliminateMultiplicationByOne.check(node):
            return EliminateMultiplicationByOne.apply(node)
        # Visit the children nodes and return the transformed node
        else:
            return self.generic_visit(node)

class TestRewriteStrategies(unittest.TestCase):
    def test_eliminate_addition_with_zero(self):
        # Create an AST node representing 'x + 0'
        left = ast.Name(id='x', ctx=ast.Load()) 
        right = ast.Constant(0)
        addition_node = ast.BinOp(left, ast.Add(), right)

        # Create an instance of Visitor
        visitor = Visitor()

        # Apply the strategy and check the result
        simplified_ast = visitor.visit(addition_node)
        print("Transformed node: ", ast.unparse(simplified_ast))
        self.assertEqual(simplified_ast, left)

    def test_eliminate_multiplication_by_one(self):
        # Create an AST node representing 'x + 0'
        left = ast.Name(id='x', ctx=ast.Load()) 
        right = ast.Constant(1)
        multiplication_node = ast.BinOp(left, ast.Mult(), right)

        # Create an instance of Visitor
        visitor = Visitor()

        # Apply the strategy and check the result
        simplified_ast = visitor.visit(multiplication_node)
        print("Transformed node: ", ast.unparse(simplified_ast))
        self.assertEqual(simplified_ast, left)

if __name__ == '__main__':
    unittest.main()