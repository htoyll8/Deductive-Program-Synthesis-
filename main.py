from ast import AST, parse, BinOp, Add, Mult, Constant, Name, Load, dump
from typing import Optional, List

import unittest

class RewriteStrategy: 
    def matches(self, ast: AST) -> bool:
        # Check if this rule's pattern matches the AST node
        pass

    def apply(self, ast: AST) -> AST:
        # Applies the transformation logic
        raise NotImplementedError

# Concrete strategies for different rewrite rules
class EliminateAdditionWithZero(RewriteStrategy):
    def matches(self, ast: AST) -> bool:
        print(isinstance(ast, BinOp))
        print(isinstance(ast.op, Add))
        print(isinstance(ast.right, Constant))
        print(ast.right.value == 0)
        return isinstance(ast, BinOp) and isinstance(ast.op, Add) and isinstance(ast.right, Constant) and ast.right.value == 0

    def apply(self, ast: BinOp) -> AST:
        return ast.left
    
class EliminateMultiplicationByOne(RewriteStrategy):
    def matches(self, ast: AST) -> bool:
        print(isinstance(ast, BinOp))
        print(isinstance(ast.op, Mult))
        print(isinstance(ast.right, Constant))
        print(ast.right.value == 1)
        return isinstance(ast, BinOp) and isinstance(ast.op, Mult) and isinstance(ast.right, Constant) and ast.right.value == 1

    def apply(self, ast: BinOp) -> AST:
        return ast.left
    
class Context: 
    def __init__(self):
        self.strategy: Optional[RewriteStrategy] = None
    
    def set_strategy(self, strategy: RewriteStrategy) -> None:
        self.strategy = strategy

    def apply_rewrite(self, ast: AST) -> AST:
        if self.strategy is not None:
            return self.strategy.apply(ast)
        return ast

class RewriteRuleDispatcher:
    def __init__(self): 
        self.rules: List[RewriteStrategy] = [
            EliminateAdditionWithZero(), 
            EliminateMultiplicationByOne(),
            # More strategies...
        ]

    def dispatch(self, ast: AST, context: Context) -> AST:
        # Determine which pattern matches the AST
        for rule in self.rules:
            if rule.matches(ast):
                context.set_strategy(rule)
                break
        
        return context.apply_rewrite(ast)

class TestRewriteStrategies(unittest.TestCase):
    def test_eliminate_addition_with_zero(self):
        # Create an AST node representing 'x + 0'
        left = Name(id='x', ctx=Load()) 
        right = Constant(0)
        addition_node = BinOp(left, Add(), right)

        # Create an instance of the strategy
        strategy = EliminateAdditionWithZero()

        # Check if the strategy matches the AST node
        self.assertTrue(strategy.matches(addition_node))

        # Apply the strategy and check the result
        simplified_ast = strategy.apply(addition_node)
        self.assertEqual(simplified_ast, left)

    def test_eliminate_multiplication_by_one(self):
        # Create an AST node representing 'x + 0'
        left = Name(id='x', ctx=Load()) 
        right = Constant(1)
        multiplication_node = BinOp(left, Mult(), right)

        # Create an instance of the strategy
        strategy = EliminateMultiplicationByOne()

        # Check if the strategy matches the AST node
        self.assertTrue(strategy.matches(multiplication_node))

        # Apply the strategy and check the result
        simplified_ast = strategy.apply(multiplication_node)
        self.assertEqual(simplified_ast, left)

if __name__ == '__main__':
    unittest.main()

