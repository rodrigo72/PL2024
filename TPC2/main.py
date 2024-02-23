import re, sys
from typing import Union, Callable


class Element:
    def __init__(self, name: str, pattern: str, template: Union[str, Callable[[str], str]], priority: int = 100, flags=0, fix=None):
        self.name = name
        self.pattern = pattern
        self.template = template
        self.priority = priority
        self.flags = flags
        self.fix = fix
        
    def replace_pattern(self, text: str) -> str:
        return self._fix(re.sub(self.pattern, self.template, text, flags=self.flags))
    
    def _fix(self, text: str) -> str:
        return self.fix.replace_pattern(text) if self.fix is not None else text
        

class Converter:
    def __init__(self):
        self.elements = [
            Element
                (
                    'Image',
                    r'\!\[([^\]]*)\]\(([^\)]*)\)', 
                    r'<img src="\2" alt="\1"/>', 
                    priority=1
                ),
            Element
                (
                    'Link',
                    r'\[([^\]]*)\]\(([^\)]*)\)', 
                    r'<a href="\2">\1</a>', 
                    priority=2
                ),
            Element
                (
                    'Bold',
                    r'(\*\*|__)(?=(?:(?:[^`]*`[^`\r\n]*`)*[^`]*$))(?=[^*])(.*?)\1', 
                    r'<b>\2</b>', 
                    priority=3
                ),
            Element
                (
                    'Italic',
                    r'(\*|_)(?=(?:(?:[^`]*`[^`\r\n]*`)*[^`]*$))(.*?)\1', 
                    r'<i>\2</i>', 
                    priority=4
                ),
            Element
                (
                    'Header',
                    r'^(#{1,6})\s(.*?)\s*$', 
                    (lambda match: f"<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>"), 
                    priority=5,
                    flags=re.MULTILINE
                ),
            Element
                (
                    'Horizontal rule',
                    r'^\s*-{3,}\s*$',
                    r'<hr>', 
                    priority=6,
                    flags=re.MULTILINE
                ),
            Element
                (
                    'Quote',
                    r'^(?:\s{0,3})(?:\>\s*)(.*)', 
                    r'<blockquote>\1</blockquote>',
                    priority=7,
                    flags=re.MULTILINE, 
                    fix=Element('Fix quote', r'<\/blockquote>(\s?)<blockquote>', r'\1')
                ),
            Element
                (
                    'Ordered list item',
                    r'^(\s{0,3})(\d+\.\s+)(.*)',
                    r'<ol>\n\t<li>\3</li>\n</ol>',
                    priority=8,
                    flags=re.MULTILINE,
                    fix=Element('Fix ordered list item', r'\s?<\/ol>\s?<ol>', r'')
                ),
            Element
                (
                    'Bullet points',
                    r'^(\s{0,3})([-|+]\s+)(.*)',
                    r'<ul>\n\t<li>\3</li>\n</ul>',
                    priority=9,
                    flags=re.MULTILINE,
                    fix=Element('Fix bullet points', r'\s?<\/ul>\s?<ul>', r'')
                ),
            Element
                (
                    'Code',
                    r"`(.*?)`",
                    r"<code>\1</code>",
                    priority=10
                )
        ]
        
    def run(self, text: str) -> str:
        for element in sorted(self.elements, key=lambda x: x.priority):
            text = element.replace_pattern(text)
        return text


def main():
    file = sys.stdin.read()
    file = Converter().run(file)
    print(file)
    

if __name__ == "__main__":
    main()
