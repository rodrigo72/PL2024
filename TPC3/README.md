# TPC3

- **Título**: Somador on/off
- **Autor**: Rodrigo Monteiro, a100706
- **Problema**:
    1. Pretende-se um programa que some todas as sequências de dígitos que encontre num texto;
    2. Sempre que encontrar a string “Off” em qualquer combinação de maiúsculas e minúsculas, esse comportamento é desligado;
    3. Sempre que encontrar a string “On” em qualquer combinação de maiúsculas e minúsculas, esse comportamento é novamente ligado;
    4. Sempre que encontrar o caráter “=”, o resultado da soma é colocado na saída.
- **Solução**:
    É utilizada uma expressão regular, que identifica inicialmente "on" ou "off" e captura o que estiver à frente (*as few times as possible (lazy)*) até encontrar novamente "on", "off" ou EOF, "\Z", através de um *positive lookahead*: `r'(?i)(on|off)(.*?)(?=on|off|\Z)'`. De acordo com o grupo que capturou, encontra os números e soma-os, e caso encontre um "=" imprime o resultado atual da soma.