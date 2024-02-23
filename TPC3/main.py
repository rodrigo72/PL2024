import sys, re
            

def main():
    
    total = 0
    on = False
    file = sys.stdin.read()
    matches = re.findall(r'(?i)(on|off)(.*?)(?=on|off|\Z)', file, re.DOTALL)

    for match in matches:        
        on = True if match[0].lower() == 'on' else False
        
        if on:
            numbers = re.findall(r'\d+', match[1], re.DOTALL)
            total += sum(map(int, numbers))
            
        if re.findall(r'\=', match[1], re.DOTALL):
            print(f'Soma = {total}')
                        

if __name__ == "__main__":
    main()
