import re, sys
from typing import Union, Callable, Final

"""
- Bold regex explained:
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
"""


class Element:
    def __init__(self, name: str, pattern: str, template: Union[str, Callable[[str], str]], flags=0, fix=None):
        self.name = name
        self.pattern = pattern
        self.template = template
        self.flags = flags
        self.fix = fix
        
    def replace_pattern(self, text: str) -> str:
        return self._fix(re.sub(self.pattern, self.template, text, flags=self.flags))
    
    def _fix(self, text: str) -> str:
        if self.fix is not None:
            return self.fix.replace_pattern(text)
        else:
            return text
        

class Converter:
    def __init__(self):
        self.elements: Final[Element] = [
            Element(
                'Image', 
                r'\!\[([^\]]*)\]\(([^\)]*)\)', 
                r'<img src="\2" alt="\1"/>'
            ),
            Element(
                'Link', 
                r'\[([^\]]*)\]\(([^\)]*)\)', 
                r'<a href="\2">\1</a>'
            ),
            Element(
                'Bold', 
                r'(\*\*|__)(?=(?:(?:[^`]*`[^`\r\n]*`)*[^`]*$))(?=[^*])(.*?)\1', 
                r'<b>\2</b>'
            ),
            Element(
                'Italic', 
                r'(\*|_)(?=(?:(?:[^`]*`[^`\r\n]*`)*[^`]*$))(.*?)\1', 
                r'<i>\2</i>'
            ),
            Element(
                'Header', 
                r'^(#{1,6})\s(.*?)\s*$', 
                (lambda match: f"<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>"), 
                flags=re.MULTILINE
            ),
            Element(
                'Horizontal rule',
                r'^\s*-{3,}\s*$',
                r'<hr>',
                flags=re.MULTILINE
            ),
            Element(
                'Quote', 
                r'^(?:\s{0,3})(?:\>\s*)(.*)', 
                r'<blockquote>\1</blockquote>', 
                flags=re.MULTILINE, 
                fix=Element('Fix quote', 
                            r'<\/blockquote>(\s?)<blockquote>', r'\1')
            ),
            Element(
                'Ordered list item', 
                r'^(\s{0,3})(\d+\.\s+)(.*)',
                r'<ol>\n\t<li>\3</li>\n</ol>',
                flags=re.MULTILINE,
                fix=Element('Fix ordered list item', 
                            r'\s?<\/ol>\s?<ol>', r'')
            ),
            Element(
                'Bullet points',
                r'^(\s{0,3})([-|+]\s+)(.*)',
                r'<ul>\n\t<li>\3</li>\n</ul>',
                flags=re.MULTILINE,
                fix=Element('Fix bullet points', 
                            r'\s?<\/ul>\s?<ul>', r'')
            ),
            Element(
                'Code',
                r"`(.*?)`",
                r"<code>\1</code>"
            )
        ]
        
    def run(self, text: str) -> str:
        for element in self.elements:
            text = element.replace_pattern(text)
        return text


def main():
    file = sys.stdin.read()
    file = Converter().run(file)
    print(file)
    

if __name__ == "__main__":
    main()
