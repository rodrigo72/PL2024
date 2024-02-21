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