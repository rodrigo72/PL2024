import sys, re
            

def main():
    
    total = 0
    on = True
    file = sys.stdin.read()
    matches = re.findall(r'(?i)(^|on|off|\=)(.*?)(?=on|off|\=|\Z)', file, re.DOTALL)

    for match in matches:        
        if match[0].lower() == 'off':
            on = False
        elif match[0] == '=':
            print(f'Soma = {total}')
        elif match[0].lower() == 'on':
            on = True

        if on:
            numbers = re.findall(r'(?:\D|^)(\d+)(?=\D|\Z)', match[1], re.DOTALL)
            total += sum(map(int, numbers))
                        

if __name__ == "__main__":
    main()
