import cmd, re

class ECalc:
    def calc_expr(self, expression):
        try:
            res = eval(expression)
            return res
        except Exception as e:
            return f"Ошибка: {e}"

class CalculatorConsole(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.calculator = ECalc()
        self.prompt = "Ввод > "

    def default(self, line):
        result = self.calculator.calc_expr(line)
        print(result)

    # Выход из программы
    def do_exit(self, line):
        return True

def main():
    console = CalculatorConsole()
    console.cmdloop("Добро пожаловать в консольный калькулятор!")

if __name__ == "__main__":
    main()
