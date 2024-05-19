class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def __str__(self):
        name = self.name
        required_string = name.center(30,"*")
        for activity in self.ledger:
            try:
                left = activity['description'][0:23]
            except TypeError:
                left = ''
            right = str("{:.2f}".format(activity['amount']))
            required_string += f"\n{left:<23}{right:>7}"
        required_string += "\nTotal: "+ str(self.get_balance())
        return required_string

    def deposit(self, amount, description=''):
        self.ledger.append({
            "amount": amount,
            "description": description
        })

    def get_balance(self):
        total = 0
        for activity in self.ledger:
            total += activity["amount"]
        return total

    def check_funds(self, amount):
        if self.get_balance() >= amount:
            return True
        return False

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": -1 * amount,
                "description": description
            })
            return True
        return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        return False

def create_spend_chart(categories):
    expense_dict = {}
    for category in categories:
        spend = 0
        for activity in category.ledger:
            if activity['amount'] < 0 :
                spend += abs(activity['amount'])

        expense_dict[category.name] = round(spend,2)
    total = sum(expense_dict.values())

    percent_dict = {}
    for key in expense_dict.keys():
        percent_dict[key] = int(round(expense_dict[key] / total, 2) * 100)

    output = 'Percentage spent by category\n'
    for num in range(100,-10,-10):
        output += f'{num}'.rjust(3) + '| '
        for value in percent_dict.values():
            if value >= num:
                output += 'o  '
            else:
                output+= '   '
        output += '\n'

    output += ' ' * 4 + '-' * (len(percent_dict.values()) * 3 + 1)
    output += '\n     '

    dict_key_list = list(percent_dict.keys())
    max_len_category = max([len(i) for i in dict_key_list])
    for i in range(max_len_category):
        for name in dict_key_list:
            if len(name) > i:
                output += name[i] + '  '
            else:
                output += '   '
        if i < max_len_category-1:
            output += '\n     '

    return output
