import sys
from collections import defaultdict

"""Constantes"""
config = {
    'separator': ',',
    'age_interval': 5,
    'id_idx': 0,
    'idade_idx': 5,
    'modalidade_idx': 8,
    'resultado_idx': 12
}

"""Classe para guardar a informação de cada atleta"""
class Info:
    def __init__(self, id, idade, modalidade, resultado):
        self.id = id
        self.idade = int(idade)
        self.modalidade = modalidade
        self.resultado = resultado.lower() in ['true', '1', 't']
        
    def __str__(self):
        return f"{self.id};{self.idade};{self.modalidade};{self.resultado}"

"""Recolha de dados"""
def read_data():
    info_dict = {}
    next(sys.stdin)
    for line in sys.stdin:
        data = line.strip().split(config['separator'])
        if data:
            info = Info(data[config['id_idx']], 
                        data[config['idade_idx']],
                        data[config['modalidade_idx']], 
                        data[config['resultado_idx']])
            info_dict[info.id] = info
    return info_dict

"""Processamento de dados"""
def process_data(info_dict):
    modalidades = set()
    total_aptos = 0
    escaloes = defaultdict(list)

    for info in info_dict.values():
        modalidades.add(info.modalidade)
        if info.resultado:
            total_aptos += 1
        escaloes[(info.idade // config['age_interval']) * config['age_interval']].append(info)

    return modalidades, total_aptos, escaloes

"""Aprensentação dos resultados"""
def print_results(data_size, modalidades, total_aptos, escaloes):
    modalidades = sorted(modalidades)
    print("\nLista ordenada alfabeticamente das modalidades desportivas:\n", modalidades, "\n")
    
    print("Percentagens de atletas aptos e inaptos para a pratica desportiva:\n"
      f"Aptos: {(total_aptos / data_size * 100):.2f}%\n"
      f"Inaptos: {((data_size - total_aptos) / data_size * 100):.2f}%\n")

    print("Distribuicao de atletas por escalao etario (escalao = intervalo de 5 anos):")

    for escalao, info_list in escaloes.items():
        info_list.sort(key=lambda x: x.idade)
        print(f"[{escalao}-{escalao + 4}]: {len(info_list) / data_size * 100:.2f}%")
        
        for info in info_list:
            print('\t', info)

def main():
    info_dict = read_data()
    modalidades, total_aptos, escaloes = process_data(info_dict)
    print_results(len(info_dict), modalidades, total_aptos, escaloes)


if __name__ == "__main__":
    main()
