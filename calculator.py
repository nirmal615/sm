"""
Scientific Calculator with Modern UI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A beginner-friendly scientific calculator with CLI and interactive modes.

Features:
  - Basic operations: add, sub, mul, div, pow, mod
  - Scientific functions: sin, cos, tan, log, sqrt, etc.
  - Modern grid-based UI layout
  - Color-coded buttons
  - Real-time calculation display
"""
import argparse
import sys
import time
import math

# ANSI Color codes for terminal styling
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    BG_LIGHT = '\033[47m'
    BG_DARK = '\033[40m'
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[46m'
    BG_MAGENTA = '\033[45m'

# Separator patterns
SEPARATOR = f"{Colors.CYAN}{'='*60}{Colors.ENDC}"
DIVIDER = f"{Colors.MAGENTA}{'─'*60}{Colors.ENDC}"


def cascade_print(text, delay=0.02):
    """Print text with cascading animation effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def spinner(duration=0.6, interval=0.08):
    """Simple spinner animation for the terminal."""
    chars = ['|', '/', '-', '\\']
    end = time.time() + duration
    while time.time() < end:
        for c in chars:
            if time.time() >= end:
                break
            print(f"{Colors.YELLOW}{c}{Colors.ENDC}", end='\r', flush=True)
            time.sleep(interval)
    print(' ', end='\r', flush=True)


def pop_effect(text, times=2, delay=0.08):
    """Brief pop/bounce effect for showing important text."""
    for _ in range(times):
        print(f"{Colors.BOLD}{Colors.GREEN}{text}{Colors.ENDC}", end='\r', flush=True)
        time.sleep(delay)
        print(f"{Colors.YELLOW}{text}{Colors.ENDC}", end='\r', flush=True)
        time.sleep(delay)
    print(text)


def cascade_result(a, op_symbol, b, result):
    """Display result with cascading animation in a box"""
    print(f'{Colors.GREEN}{Colors.BOLD}')
    print('   ╔══════════════════════════════════╗')
    cascade_print(f'   ║  {a} {op_symbol} {b}', delay=0.01)
    time.sleep(0.1)
    print(f'   ║          ⬇️')
    time.sleep(0.15)
    cascade_print(f'   ║  ➜ Result: {result}', delay=0.02)
    print('   ║')
    print('   ╚══════════════════════════════════╝')
    print(f'{Colors.ENDC}\n')


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return a / b


def powr(a, b):
    return a ** b


def mod(a, b):
    if b == 0:
        raise ZeroDivisionError("Mod by zero")
    return a % b


OPS = {
    'add': add,
    'sub': sub,
    'mul': mul,
    'div': div,
    'pow': powr,
    'mod': mod,
}


def parse_args(argv):
    p = argparse.ArgumentParser(description='Simple CLI calculator')
    p.add_argument('operation', nargs='?', choices=OPS.keys(), help='operation')
    p.add_argument('a', nargs='?', type=float, help='first operand')
    p.add_argument('b', nargs='?', type=float, help='second operand')
    p.add_argument('-i', '--interactive', action='store_true', help='run interactive prompt')
    return p.parse_args(argv)


def interactive_prompt():
    # Display scientific calculator UI
    print(f'\n{Colors.BG_CYAN}{Colors.BOLD}{Colors.BLUE}')
    cascade_print('╔════════════════════════════════════════════════════════╗', delay=0.01)
    cascade_print('║                                                        ║', delay=0.01)
    cascade_print('║         🧮  SCIENTIFIC CALCULATOR  🧮                  ║', delay=0.02)
    cascade_print('║                                                        ║', delay=0.01)
    cascade_print('╚════════════════════════════════════════════════════════╝', delay=0.01)
    print(f'{Colors.ENDC}\n')
    
    display = "0"
    history = []
    
    def show_ui():
        nonlocal display
        # Display screen
        print(f'{Colors.MAGENTA}')
        print('┌─────────────────────────────────────────────────────┐')
        print(f'│  {Colors.YELLOW}{Colors.BOLD}{display:>52}{Colors.MAGENTA}│')
        print('└─────────────────────────────────────────────────────┘')
        print(f'{Colors.ENDC}')
        
        # Animated button grid entrance
        rows = [
            (f'{Colors.CYAN}{Colors.BOLD}Function Buttons:{Colors.ENDC}', f'  {Colors.WHITE}{Colors.BOLD}[AC]{Colors.ENDC}  {Colors.WHITE}[DEL]{Colors.ENDC}  {Colors.WHITE}[√]{Colors.ENDC}  {Colors.WHITE}[x²]{Colors.ENDC}  {Colors.WHITE}[x³]{Colors.ENDC}  {Colors.WHITE}[%]{Colors.ENDC}'),
            (f'{Colors.CYAN}{Colors.BOLD}Trigonometric:{Colors.ENDC}', f'  {Colors.YELLOW}[sin]{Colors.ENDC}  {Colors.YELLOW}[cos]{Colors.ENDC}  {Colors.YELLOW}[tan]{Colors.ENDC}  {Colors.YELLOW}[log]{Colors.ENDC}  {Colors.YELLOW}[ln]{Colors.ENDC}  {Colors.YELLOW}[π]{Colors.ENDC}'),
            (f'{Colors.CYAN}{Colors.BOLD}Numbers & Operations:{Colors.ENDC}', f'  {Colors.GREEN}[7]{Colors.ENDC}  {Colors.GREEN}[8]{Colors.ENDC}  {Colors.GREEN}[9]{Colors.ENDC}  {Colors.WHITE}[÷]{Colors.ENDC}  {Colors.WHITE}[×]{Colors.ENDC}'),
            ('', f'  {Colors.GREEN}[4]{Colors.ENDC}  {Colors.GREEN}[5]{Colors.ENDC}  {Colors.GREEN}[6]{Colors.ENDC}  {Colors.WHITE}[-]{Colors.ENDC}  {Colors.WHITE}[+]{Colors.ENDC}'),
            ('', f'  {Colors.GREEN}[1]{Colors.ENDC}  {Colors.GREEN}[2]{Colors.ENDC}  {Colors.GREEN}[3]{Colors.ENDC}  {Colors.WHITE}[.]{Colors.ENDC}  {Colors.BLUE}{Colors.BOLD}[=]{Colors.ENDC}'),
            ('', f'  {Colors.GREEN}[0]{Colors.ENDC}                    {Colors.WHITE}[()]{Colors.ENDC}'),
        ]
        for title, line in rows:
            if title:
                cascade_print(title, delay=0.005)
            cascade_print(line, delay=0.004)
            time.sleep(0.06)

        print(f'\n{Colors.MAGENTA}{"─"*55}{Colors.ENDC}')
        print(f'{Colors.CYAN}Commands: help | clear | exit{Colors.ENDC}\n')
    
    show_ui()
    
    while True:
        try:
            cmd = input(f'{Colors.YELLOW}{Colors.BOLD}➜ Enter button or operation:{Colors.ENDC} ').strip()
        except (EOFError, KeyboardInterrupt):
            print(f'\n{Colors.GREEN}{Colors.BOLD}✨ Thanks for using Calculator! Goodbye! ✨{Colors.ENDC}\n')
            return
        
        if not cmd:
            continue
        
        if cmd.lower() in ('exit', 'quit'):
            print(f'{Colors.GREEN}{Colors.BOLD}✨ Thanks for using Calculator! Goodbye! ✨{Colors.ENDC}\n')
            return
        
        if cmd.lower() == 'clear' or cmd.lower() == 'ac':
            display = "0"
            print(f'\n{Colors.CYAN}Screen cleared!{Colors.ENDC}\n')
            show_ui()
            continue
        
        if cmd.lower() == 'help':
            print(f'\n{Colors.CYAN}{Colors.BOLD}')
            print('╔═══════════════════════════════════════════════╗')
            print('║           📚 AVAILABLE OPERATIONS             ║')
            print('╠═══════════════════════════════════════════════╣')
            print('║  Numbers: 0-9                                 ║')
            print('║  Basic: + - × ÷ =                             ║')
            print('║  Power: x² x³ x^y √                           ║')
            print('║  Trig: sin cos tan (in degrees)               ║')
            print('║  Log: log (base 10) ln (natural log)          ║')
            print('║  Other: π % ( ) AC DEL                        ║')
            print('╚═══════════════════════════════════════════════╝')
            print(f'{Colors.ENDC}\n')
            continue
        
        # Parse input
        cmd_lower = cmd.lower()
        
        try:
            # Number input
            if cmd.isdigit() or (cmd == '.' and '.' not in display):
                if display == "0":
                    display = cmd
                else:
                    display += cmd
            
            # Operations
            elif cmd in ['+', '-', '*', 'x', '×', '/', '÷']:
                if display != "0":
                    display += f" {cmd} "
            
            # Scientific functions
            elif cmd_lower == 'sin':
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    result = math.sin(math.radians(val))
                    display = str(round(result, 8))
                except:
                    display = "Error"
            elif cmd_lower == 'cos':
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    result = math.cos(math.radians(val))
                    display = str(round(result, 8))
                except:
                    display = "Error"
            elif cmd_lower == 'tan':
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    result = math.tan(math.radians(val))
                    display = str(round(result, 8))
                except:
                    display = "Error"
            elif cmd_lower == 'log':
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    result = math.log10(val)
                    display = str(round(result, 8))
                except:
                    display = "Error"
            elif cmd_lower == 'ln':
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    result = math.log(val)
                    display = str(round(result, 8))
                except:
                    display = "Error"
            elif cmd_lower == 'sqrt' or cmd == '√':
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    result = math.sqrt(val)
                    display = str(round(result, 8))
                except:
                    display = "Error"
            elif cmd == 'π':
                display = str(math.pi)
            elif cmd_lower == 'del':
                display = display[:-1] if len(display) > 1 else "0"
            elif cmd == '%':
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    display = str(val / 100)
                except:
                    display = "Error"
            elif cmd == '=':
                try:
                    # show spinner while calculating
                    spinner(duration=0.5, interval=0.06)
                    result = eval(display.replace('×', '*').replace('÷', '/'))
                    if isinstance(result, float) and result.is_integer():
                        display = str(int(result))
                    else:
                        display = str(round(result, 8))
                    history.append(f'{display}')
                    # pop effect for the result
                    pop_effect(f' ➜ {display}', times=2, delay=0.06)
                except Exception:
                    display = "Error"
            elif cmd == '(':
                if display == "0":
                    display = "("
                else:
                    display += "("
            elif cmd == ')':
                display += ")"
            elif cmd_lower in ['x²', 'x^2']:
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    result = val ** 2
                    display = str(round(result, 8))
                except:
                    display = "Error"
            elif cmd_lower in ['x³', 'x^3']:
                try:
                    val = float(eval(display.replace('×', '*').replace('÷', '/')))
                    result = val ** 3
                    display = str(round(result, 8))
                except:
                    display = "Error"
            
            print()
            show_ui()
        
        except Exception as e:
            print(f'{Colors.RED}❌ Invalid input: {e}{Colors.ENDC}\n')
            show_ui()


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)
    
    if args.interactive:
        interactive_prompt()
        return
    
    if not args.operation or args.a is None or args.b is None:
        # Display very attractive help screen with cascading effect
        print(f'\n{Colors.BG_CYAN}{Colors.BLUE}{Colors.BOLD}')
        cascade_print('╔════════════════════════════════════════════════════════╗', delay=0.01)
        cascade_print('║                                                        ║', delay=0.01)
        cascade_print('║           📱 STYLISH CALCULATOR v2.0 📱                ║', delay=0.02)
        cascade_print('║                                                        ║', delay=0.01)
        cascade_print('║          Your Gateway to Colorful Math 🌈             ║', delay=0.015)
        cascade_print('║                                                        ║', delay=0.01)
        cascade_print('╚════════════════════════════════════════════════════════╝', delay=0.01)
        print(f'{Colors.ENDC}\n')
        print(f'{Colors.CYAN}{Colors.BOLD}Usage:{Colors.ENDC}')
        print(f'  {Colors.MAGENTA}<operation> <num1> <num2>{Colors.ENDC}')
        print(f'\n{Colors.CYAN}{Colors.BOLD}🎨 Operations:{Colors.ENDC}')
        print(f'┌─ {Colors.YELLOW}add{Colors.ENDC}  →  Addition       {Colors.CYAN}Example: add 5 3{Colors.ENDC}')
        print(f'├─ {Colors.YELLOW}sub{Colors.ENDC}  →  Subtraction    {Colors.CYAN}Example: sub 10 4{Colors.ENDC}')
        print(f'├─ {Colors.YELLOW}mul{Colors.ENDC}  →  Multiplication {Colors.CYAN}Example: mul 6 7{Colors.ENDC}')
        print(f'├─ {Colors.YELLOW}div{Colors.ENDC}  →  Division       {Colors.CYAN}Example: div 20 4{Colors.ENDC}')
        print(f'├─ {Colors.YELLOW}pow{Colors.ENDC}  →  Power          {Colors.CYAN}Example: pow 2 8{Colors.ENDC}')
        print(f'└─ {Colors.YELLOW}mod{Colors.ENDC}  →  Modulo         {Colors.CYAN}Example: mod 10 3{Colors.ENDC}')
        print(f'\n{Colors.MAGENTA}{Colors.BOLD}✨ Interactive Mode:{Colors.ENDC}')
        print(f'  {Colors.YELLOW}--interactive{Colors.ENDC}  {Colors.CYAN}(or -i for short){Colors.ENDC}')
        print(f'\n{Colors.MAGENTA}{"━"*60}{Colors.ENDC}\n')
        return
    
    func = OPS[args.operation]
    
    try:
        result = func(args.a, args.b)
    except ZeroDivisionError:
        print(f'{Colors.RED}{Colors.BOLD}❌ Error: Cannot divide by zero{Colors.ENDC}')
        return
    except Exception as e:
        print(f'{Colors.RED}{Colors.BOLD}❌ Error: {e}{Colors.ENDC}')
        return
    
    # Format result nicely
    op_symbol = {
        'add': '+', 'sub': '-', 'mul': '×', 'div': '÷', 'pow': '^', 'mod': 'mod'
    }.get(args.operation, args.operation)
    
    # Print integer results without decimal when possible
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    
    print(f'{Colors.GREEN}{Colors.BOLD}✅ {args.a} {op_symbol} {args.b} = {Colors.YELLOW}{result}{Colors.ENDC}')


if __name__ == '__main__':
    main()
