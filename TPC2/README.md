# TPC2

- **Título**: Conversor simples de Markdown para HTML com Regex
- **Autor**: Rodrigo Monteiro, a100706
- **Problema**:

Criar em Python um pequeno conversor de MarkDown para HTML para os elementos descritos na "Basic Syntax" da [Cheat Sheet](https://www.markdownguide.org/cheat-sheet/):

 **Element**     | **Markdown Syntax**                                                                             
:---------------:|:------------------------------------:
 Heading         | # H1                                                    
 Bold            | **bold text**      
 Italic          | *italicized text*  
 Blockquote      | &gt; blockquote       
 Ordered List    | 1. First item         
 Unordered List  | - First item
 Code            | \`code\`                    
 Horizontal Rule | ---      
 Link            | [title](https://www.example.com)                                                   
 Image           | ![kermitsip](kermitsip.png)

- **Solução**

São utilizadas duas classes: `Element` e `Converter`.
A classe `Element` é utilizada para converter um certo elemento de markdown em HTML. Assim, recebe os seguintes atributos:
- *name*: nome dado ao element (para efeitos de identificação)
- *pattern*: padrão de regex para identificar os elementos num texto 
- *template*: modelo de substituição que utliza os grupos definidos pelo padrão
- *flags*: flags para a substiuição (foi utilizada a `re.MULTILINE` em alguns casos)
- *fix*: `Element` ou `None` - alguns elementos precisam de um ajuste (portanto, uma segunda substituição), como é o caso das listas ordenadas, bullet points, e quotes.

Também possui as funções `replace_pattern`, e `_fix`, que fazem a substituição utilizando os atributos descritos acima. 

A classe `Converter` inicia um array (cuja ordem importa) de `Element`, e possui uma função `run` que passa o input ordenadamente por todos os elementos do array, chamando `replace_pattern` em cada um.


Explicação do regex utilizado para a substituição do *bold text*:
```
        (\*\*)                          # matches exactly 2 *
        (?=                             # positive lookahead (example: q(?=u) matches a q that is followed by a 'u')
            (?:                         # non-capturing group (ignored in the final result)
                (?:[^`]*`[^`\r\n]*`)    # non-capturing group; 1. Match a character that is not "`", [0, inf[ times
                                        #                      2. Match a "`" character
                                        #                      3. Match any character that is not "`", "\n" or "\r", [0, inf] times
                                        #                      4. Match a "`" character
            *[^`]*$)                    # match the previous group 0 or more times (as many as possible -- * is greedy) -- a code area. 
                                        # match a character that is not "`" 0 or more times until the end of the line -- no "`" left
        )                               #
        (?=[^*])                        # positive lookahead; keep "*" out of the second group
        (.*?)                           # matches any character between zero and unlimited times, as few times as possible, expanding as needed (lazy)
                                        # this way does not match more "**" in between other "**"
        \1                              # matches the same text captured in the first group
```