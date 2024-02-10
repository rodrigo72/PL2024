# TPC1

- **Título**: Análise de um dataset
- **Autor**: Rodrigo Monteiro, a100706
- **Problema**:
    1. Proibido usar o módulo CSV;
    2. Ler o dataset, processá-lo e criar os seguintes resultados:
        1. Lista ordenada alfabeticamente das modalidades desportivas;
        2. Percentagens de atletas aptos e inaptos para a prática desportiva;
        3. Distribuição de atletas por escalão etário (escalão = intervalo de 5 anos): ... [30-34], [35-39], ...
- **Solução**:
    - É utilizada uma classe "Pessoa" com diversos atributos
    - O ficheiro CSV é lido, e é feito o parsing de cada linha
    - Os dados obtidos são iterados de modo a que seja adquirido um `set` de modalidades, um valor de `total_aptos` e de `total_inaptos`, e um dicionário cujas chaves são `int` (o valor mais baixo do intervalo do escalão) e cujos valores são listas de `Pessoa`.
    - Por fim, os resultados são guardados numa pasta "results", e também mostrados no terminal.
