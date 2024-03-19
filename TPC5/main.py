import ply.lex as lex
import sys

"""
> In advanced parsing applications, it may be useful to have different lexing states. 
> For instance, you may want the occurrence of a certain token or syntactic construct 
> to trigger a different kind of lexing. PLY supports a feature that allows the 
> underlying lexer to be put into a series of different states. Each state can 
> have its own tokens, lexing rules, and so forth.

https://ply.readthedocs.io/en/latest/ply.html
"""


class VendingMachine():
    
    states = [
        ('LISTING', 'inclusive'), # inclusive: adds additional tokens and rules to the default set of rules
        ('INPUT', 'inclusive'),
        ('SELECT', 'inclusive'),
        ('LEAVE', 'inclusive')
    ]

    keyword_states = {
        "LISTAR": "LISTING",
        "SELECIONAR": "SELECT",
        "MOEDA": "INPUT",
        "SAIR": "LEAVE"
    }

    tokens = [
        'NUMBER',
        'KEYWORD',
        'OPTION',
        'UNKNOWN_KEYWORD',
        'COIN'
    ] + list(keyword_states.keys())
    
    
    def __init__(self, products):
        self.balance = 0;
        self.products = products;
        self.lexer = None
        self.leave = False
        self.name = 'maq'
        
    
    def coin_value(self, num):
        cur = float(num[:-1])

        if num[-1] == 'e':
            cur *= 100

        return cur  # could throw exception for values like "300c"
    
    
    def format_currency(self, val):
        return f"{'%0.0f'%(val,) + 'c' if val < 100 else '%0.2f'%(val / 100,) + 'e'}"
        
    
    def return_change(self):
        denominations = {
            '2e': 200,
            '1e': 100,
            '50c': 50,
            '20c': 20,
            '10c': 10,
            '5c': 5,
            '2c': 2,
            '1c': 1
        }

        change = {}
        change_str = ""
        
        for coin, value in denominations.items():
            count = self.balance // value
            if count > 0:
                change[coin] = count
                self.balance %= value

        for coin, count in change.items():
            change_str += f"{count}x {coin}\t"

        if change_str != "":
            print(f"Pode retirar o troco: {change_str}")
        
        
    def get_product(self, cod, inv):
        for product in self.products:
            if product["cod"] == cod:
                return product
        return inv 
    
    
    def change_product_quantity(self, cod, diff):
        for product in self.products:
            if product["cod"] == cod:
                product["quant"] += diff
                return
        return 
        
    
    def process_request(self, option):
        product = self.get_product(option, "Inválido")
        
        if product == "Inválido":  # cod não encontrado
            print("Produto indisponível.")
            print(f"{self.name}: Saldo = {self.format_currency(self.balance)}")
            
        elif product["quant"] <= 0:  # quantidade insuficiente
            print("Quantidade insuficiente.")
            print(f"{self.name}: Saldo = {self.format_currency(self.balance)}")
            
        else:
            product_price = product["preco"] * 100
            if self.balance - product_price < 0:
                print(f'{self.name}: Saldo insuficiente.')
                print(f"{self.name}: Saldo = {self.format_currency(self.balance)}; Pedido = {self.format_currency(product_price)}")
            else:
                self.balance -= product_price;
                self.change_product_quantity(option, -1)
                print(f'{self.name}: Pode retirar o produto dispensado "{product["nome"]}"')
                print(f"{self.name}: Saldo = {self.format_currency(self.balance)}")
                
    
    def t_INPUT_NUMBER(self, t):
        r'\d+(c|e)'
        t.type = 'COIN'
        self.balance += self.coin_value(t.value)
        return t

    
    def t_SELECT_STRING(self, t):
        r'\w+'
        t.type = 'OPTION'
        self.process_request(t.value)
        return t
    
    
    def t_KEYWORD(self, t):
        r'\w+'

        t.type = t.value.upper() if t.value.upper() in self.keyword_states.keys() else "UNKNOWN_KEYWORD"  

        if t.type == "UNKNOWN_KEYWORD":
            match t.lexer.lexstate:
                case "INPUT":
                    print('Formato da moeda errado.')
                case _:
                    print("Keyword não foi reconhecida.")

            t.lexer.begin('INITIAL')

        else:
            t.lexer.begin(self.keyword_states.get(t.type, "UNKNOWN_TYPE"))

        return t
    
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        

    def t_LISTING_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

        print(f"{self.name}:")
        for p in self.products:
            print(f'Cod: {p["cod"]},  Nome: {p["nome"]},  Quantidade: {p["quant"]},  Preço:{self.format_currency(p["preco"] * 100)}')

        t.lexer.begin('INITIAL')
        
    
    def t_INPUT_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        print(f"Saldo: {self.format_currency(self.balance)}")
        t.lexer.begin('INITIAL')


    def t_SELECT_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.begin('INITIAL')


    def t_LEAVE_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.return_change()
        self.leave = True
        t.lexer.begin('INITIAL')


    t_ignore  = ' \t,'    
    
        
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
        
        
    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)
        
        
    def run(self):
        if self.lexer is None:
            self.build()
        
        for line in sys.stdin:
            self.lexer.input(line)
            
            for _ in self.lexer:
                pass
            
            if self.leave:
                return    
        
        
if __name__ == "__main__":
    stock = [
        {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
        {"cod": "A24", "nome": "sumo 0.5L", "quant": 1, "preco": 1.80}
    ]
    
    vending_machine = VendingMachine(stock)
    vending_machine.run()
