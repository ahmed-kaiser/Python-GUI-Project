import tkinter as tk
import math

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('336x435')
        self.root.resizable(0,0)
        self.root.iconbitmap('cal.ico')
        self.root.title('Calculator')
        
        self.expression = "" # holds the real expression 
        self.total = "0" # holds the total value after executing the expression

        self.display_frame = self.create_display_frame()
        self.expression_label, self.total_label = self.create_display_levels()
        self.button_frame = self.create_button_frame()
        self.create_digits()

        self.eval_exp = "" # holds the expression, which will going to be executed
        self.temp = "" # holds the entered value, temporarily
        
        self.digits = ['0','1','2','3','4','5','6','7','8','9','.', 'π', 'e']
        self.op_dict = {
            '×':'*', '÷':'/', '+':'+', '−':'-', '=':'=', '^':'**'
        }
        self.special_op_dict = {
            'x!':'!', '√x':'√', '1/x':'1/', 'x^2':'^2', '2^x':'2^', 'log2()':'log2', 'log10()':'log10'
        }
        self.brackets = {'(':0, ')':0}
        
    def create_display_frame(self):
        display_frame = tk.Frame(self.root, height=120)
        display_frame.pack(fill="both", expand=True, padx=3)
        display_frame.pack_propagate(0)
        return display_frame


    def create_button_frame(self):
        button_frame = tk.Frame(self.root, height=350, bg="lightgray")
        button_frame.pack(fill="both", expand=True, padx=3)
        return button_frame


    def create_display_levels(self):
        exp_label = tk.Label(self.display_frame, text=self.expression, font="Times 14", anchor="w", \
                             padx=10, background='#a7c8d4')
        exp_label.pack(fill="both", expand=True)

        t_label = tk.Label(self.display_frame, text=self.total, font="Times 20 bold", anchor="e", \
                          padx=10, background='#a7c8d4', fg='#24364f')
        t_label.pack(fill="both", expand=True)
        
        return exp_label, t_label


    def calculate(self, value):
        if value == 'C':
            # when pressed clear(C) button
            self.expression = ""
            self.total = "0"
            self.temp = ""
            self.eval_exp = ""

        elif value == 'DEL':
            # when pressed delete(DEL) button
            if self.temp:
                self.temp = self.temp[:len(self.temp)-1]

            else:
                self.expression = ""
                self.total = "0"
                self.temp = ""
                self.eval_exp = ""

        elif value in self.digits:
            # when the entered value is a digit or '.'
            if value == '.' and value in self.temp:
                pass # temp variable already consist a dot(.)
            else:
                if value == 'π':
                    self.temp = ""
                    value = '3.1416'
                if value == 'e':
                    self.temp = ""
                    value = '2.7182818'

                self.temp += value

        elif value in self.brackets.keys():
            # when entered value is brackets
            if value == '(':
                self.brackets['('] += 1
                self.expression += '('
                self.eval_exp += '('

            if value == ')':
                if self.expression[len(self.expression)-1] == ')' and self.brackets['('] - self.brackets[')'] == 1: 
                    self.brackets[')'] += 1
                    self.expression += ')'
                    self.eval_exp += ')'
                    self.temp = ""

                if self.brackets['('] > self.brackets[')'] and self.expression[len(self.expression)-1] in self.op_dict \
                   and self.temp:
                    self.brackets[')'] += 1
                    self.expression += self.temp + ')'
                    self.eval_exp += self.temp + ')'
                    self.temp = ""
            try:
                if self.brackets['('] == self.brackets[')']:
                    # execute the expression when the brackets are balanced
                    self.brackets['('], self.brackets[')'] = 0, 0
                    self.total = eval(self.eval_exp)
                    self.temp = ""
            except:
                self.temp = ""
                self.total = "Syntext error"

        elif value in self.op_dict.keys():
            # when the entered value is a basic operator
            if self.expression and self.expression[len(self.expression)-1] == '=':
                # when previous expression is executed and, wants to add new exp. with the total
                self.expression = str(self.total) + value
                self.eval_exp = str(self.total) + self.op_dict[value]

            elif self.expression and self.expression[len(self.expression)-1] == '(':
                # when last index value of the expression is '('
                self.expression += (self.temp + value)
                self.eval_exp += (self.temp + self.op_dict[value])
                self.temp = ""

            elif self.expression and self.expression[len(self.expression)-1] == ')':
                # when last index value of the expression is ')'
                self.expression += value
                self.eval_exp += self.op_dict[value]

            else:
                if self.expression and self.expression[len(self.expression)-1] not in self.op_dict.keys():
                    # when last index value of the expression is not an operator
                    self.expression += value
                    self.eval_exp += self.op_dict[value]
                else:
                    # when last index value of the expression is an operator
                    self.expression += (self.temp + value)
                    self.eval_exp += (self.temp + self.op_dict[value])
                    self.temp = ""

                try:
                    if self.brackets['('] == 0 and self.expression[len(self.expression)-1] != '^':
                        self.total = eval(self.eval_exp[:len(self.eval_exp)-1])
                        self.temp = ""
                except:
                    self.total = ""
                    self.temp = "Syntext error"

        elif value in self.special_op_dict.keys():
            hold_exp = ""
            if value == 'x!':
                if (self.expression and self.expression[len(self.expression)-1] == '=') or \
                    self.expression[len(self.expression)-1] not in self.op_dict:
                    # when the expression is in complete manner
                    sub_total = math.factorial(int(self.total))
                    hold_exp = str(self.total) + self.special_op_dict[value]
                    self.expression = hold_exp
                    self.eval_exp = str(sub_total)

                if self.temp:
                    # when the expression is not in complete manner
                    sub_total = math.factorial(int(self.temp))
                    hold_exp = self.temp + self.special_op_dict[value]
                    self.temp = ""
                    self.expression += hold_exp
                    self.eval_exp += str(sub_total)

            elif value == '√x':
                if (self.expression and self.expression[len(self.expression)-1] == '=') or \
                    self.expression[len(self.expression)-1] not in self.op_dict:
                    # when the expression is in complete manner
                    sub_total = math.sqrt(int(self.total))
                    hold_exp = self.special_op_dict[value] + str(self.total)
                    self.expression = hold_exp
                    self.eval_exp = str(sub_total)

                if self.temp:
                    # when the expression is not in complete manner
                    sub_total = math.sqrt(int(self.temp))
                    hold_exp = self.special_op_dict[value] + self.temp
                    self.temp = ""
                    self.expression += hold_exp
                    self.eval_exp += str(sub_total)

            elif value == 'x^2':
                if (self.expression and self.expression[len(self.expression)-1] == '=') or \
                    self.expression[len(self.expression)-1] not in self.op_dict:
                    # when the expression is in complete manner
                    sub_total = pow(int(self.total), 2)
                    hold_exp = str(self.total) + self.special_op_dict[value]
                    self.expression = hold_exp
                    self.eval_exp = str(sub_total)

                if self.temp:
                    # when the expression is not in complete manner
                    sub_total = pow(int(self.temp), 2)
                    hold_exp = self.temp + self.special_op_dict[value]
                    self.temp = ""
                    self.expression += hold_exp
                    self.eval_exp += str(sub_total)

            elif value == '2^x':
                if (self.expression and self.expression[len(self.expression)-1] == '=') or \
                    self.expression[len(self.expression)-1] not in self.op_dict:
                    # when the expression is in complete manner
                    sub_total = pow(2, int(self.total))
                    hold_exp = self.special_op_dict[value] + str(self.total)
                    self.expression = hold_exp
                    self.eval_exp = str(sub_total)

                if self.temp:
                    # when the expression is not in complete manner
                    sub_total = pow(2, int(self.temp))
                    hold_exp = self.special_op_dict[value] + self.temp
                    self.temp = ""
                    self.expression += hold_exp
                    self.eval_exp += str(sub_total)

            elif value == '1/x':
                try:
                    if (self.expression and self.expression[len(self.expression)-1] == '=') or \
                    self.expression[len(self.expression)-1] not in self.op_dict:
                    # when the expression is in complete manner
                        sub_total = 1/int(self.total)
                        hold_exp = self.special_op_dict[value] + str(self.total)
                        self.expression = hold_exp
                        self.eval_exp = str(sub_total)

                    if self.temp:
                        # when the expression is not in complete manner
                        sub_total = 1/int(self.temp)
                        hold_exp = self.special_op_dict[value] + self.temp
                        self.temp = ""
                        self.expression += hold_exp
                        self.eval_exp += str(sub_total)

                except:
                    sub_total = 0
                    self.temp_exp = ""

            elif value == 'log2()':
                if (self.expression and self.expression[len(self.expression)-1] == '=') or \
                    self.expression[len(self.expression)-1] not in self.op_dict:
                    # when the expression is in complete manner
                    sub_total = math.log2(int(self.total))
                    hold_exp = self.special_op_dict[value] + '(' + str(self.total) + ')'
                    self.expression = hold_exp
                    self.eval_exp = str(sub_total)

                if self.temp:
                    # when the expression is not in complete manner
                    sub_total = math.log2(int(self.temp))
                    hold_exp = self.special_op_dict[value] + '(' + self.temp + ')'
                    self.temp = ""
                    self.expression += hold_exp
                    self.eval_exp += str(sub_total)

            elif value == 'log10()':
                if (self.expression and self.expression[len(self.expression)-1] == '=') or \
                    self.expression[len(self.expression)-1] not in self.op_dict:
                    # when the expression is in complete manner
                    sub_total = math.log10(int(self.total))
                    hold_exp = self.special_op_dict[value] + '(' + str(self.total) + ')'
                    self.expression = hold_exp
                    self.eval_exp = str(sub_total)

                if self.temp:
                    # when the expression is not in complete manner
                    sub_total = math.log10(int(self.temp))
                    hold_exp = self.special_op_dict[value] + '(' + self.temp + ')'
                    self.temp = ""
                    self.expression += hold_exp
                    self.eval_exp += str(sub_total)

            try:
                self.total = eval(self.eval_exp)
            except:
                self.temp = ""
                self.total = "Syntext error"

        self.update_expression_label() # call update_expression_label to update the expression
        self.update_total_label() # call update_total_label to update the total
        

    def create_digits(self):
        buttons = {
            '1/x':(0,1), 'x^2':(0,2), '2^x':(0,3), 'C':(0,4), 'DEL':(0,5),
            '(':(1,1), ')':(1,2), '^':(1,3), 'x!':(1,4), '√x':(1,5),
            '7':(2, 1), '8':(2,2), '9':(2,3), '×':(2, 4), 'e':(2,5),
            '4':(3, 1), '5':(3,2), '6':(3,3), '+':(3, 4), 'log2()':(3,5),
            '1':(4, 1), '2':(4,2), '3':(4,3), '−':(4, 4), 'log10()':(4,5),
            '0':(5, 1), '.':(5, 2), 'π':(5, 3), '÷':(5, 4), '=':(5, 5)
        }
        
        for key, cordinate in buttons.items():
            button = tk.Button(self.button_frame, text=str(key), padx=10, pady=6, font='Arial 10 bold', border=0, \
                               fg="#93f1fa", bg='#2e3847', width=5, height=2, activebackground="#b8c8cf", \
                               relief="solid", command=lambda n=key:self.calculate(n))

            button.grid(row=cordinate[0], column=cordinate[1], padx=1, pady=1)


    def update_expression_label(self):
        self.expression_label.config(text=self.expression)


    def update_total_label(self):
        if self.total:
            text = self.total
        if self.temp:
            text = self.temp

        n = len(str(self.total))
        # set total label font size based on number of digits
        if n < 23:
            self.total_label.config(text=text)
        elif n > 22 and n < 29:
            self.total_label.config(text=text, font="Times 16 bold")
        elif n > 28 and n < 31:
            self.total_label.config(text=text, font="Times 14 bold")
        else:
         self.total_label.config(text="Out of display range")

    def run_mainloop(self):
        return tk.mainloop()

        


if __name__ == '__main__':
    calc = Calculator()
    calc.run_mainloop()
    hello = 0
