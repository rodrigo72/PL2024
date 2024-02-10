import os
from collections import defaultdict


class Pessoa:
    def __init__(self, _id, index, dataEMD, primeiro_nome, último_nome, idade, 
                 género, morada, modalidade, clube, email, federado, resultado):
        self._id = _id
        self.index = index
        self.dataEMD = dataEMD
        self.primeiro_nome = primeiro_nome
        self.último_nome = último_nome
        self.idade = int(idade)
        self.género = género
        self.morada = morada
        self.modalidade = modalidade
        self.clube = clube
        self.email = email
        self.federado = federado.lower() in ['true', '1', 't']
        self.resultado = resultado.lower() in ['true', '1', 't']
        
    def __str__(self):
        return (f"{self._id} {self.index} {self.dataEMD} "
                f"{self.primeiro_nome} {self.último_nome} {self.idade} "
                f"{self.género} {self.morada} {self.modalidade} {self.clube} "
                f"{self.email} {self.federado} {self.resultado}")


def main():
    pessoas_dict = {}
    
    with open(r'TPC1\emd.csv', 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            data = line.strip().split(',')
            if data:
                pessoa = Pessoa(*data)
                pessoas_dict[pessoa._id] = pessoa
                
    modalidades = set()
    total_aptos = total_inaptos = 0
    escaloes = defaultdict(list)
                
    for pessoa in pessoas_dict.values():
        modalidades.add(pessoa.modalidade)
        if pessoa.resultado:
            total_aptos += 1
        else:
            total_inaptos += 1
        escaloes[(pessoa.idade // 5) * 5].append(pessoa)
        
    os.makedirs(r'TPC1\results', exist_ok=True)
            
    modalidades = sorted(modalidades)
    print()
    print("Lista ordenada alfabeticamente das modalidades desportivas")
    print(modalidades)
    print()
    
    with open(r'TPC1\results\modalidades.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(modalidades))
    
    total_aptos_percetagem = total_aptos / (total_aptos + total_inaptos) * 100
    total_inaptos_percetagem = total_inaptos / (total_aptos + total_inaptos) * 100
    
    print("Percentagens de atletas aptos e inaptos para a prática desportiva")
    print(f"Aptos: {total_aptos_percetagem:.2f}%")
    print(f"Inaptos: {total_inaptos_percetagem:.2f}%")
    print()
    
    with open(r'TPC1\results\percentagens.txt', 'w', encoding='utf-8') as file:
        file.write(f"Aptos: {total_aptos_percetagem:.2f}%\n")
        file.write(f"Inaptos: {total_inaptos_percetagem:.2f}%\n")
    
    print("Distribuição de atletas por escalão etário (escalão = intervalo de 5 anos):")
    
    with open(r'TPC1\results\escaloes.txt', 'w', encoding='utf-8') as file:
        for escalao, pessoas in escaloes.items():
            print(f"[{escalao}-{escalao + 4}]: {len(pessoas)}")
            file.write(f"[{escalao}-{escalao + 4}]\n")
            for pessoa in pessoas:
                file.write(f"\t{pessoa}\n")
        
if __name__ == "__main__":
    main()
