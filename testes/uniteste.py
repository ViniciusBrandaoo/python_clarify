import unittest

from teste_unitario import somar, subtrair, multiplicar, dividir 

class TestOperacoes(unittest.TestCase):
    
    def test_somar(self):
        self.assertEqual(somar(2,3), 5)
        self.assertEqual(somar(-1, 1), 0)
        self.assertEqual(somar(-2, -3), -5)
        
    def test_subtrair(self):
        self.assertEqual(subtrair(5,-3), 2)
        self.assertEqual(subtrair(-1, 1), 2)
        self.assertEqual(subtrair(0, 0), -0)
        
if __name__ == '__main__':
    unittest.main()