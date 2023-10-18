class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.category}')
            category.deposit(amount, f'Transfer from {self.category}')
            return True
        else:
            return False

    def __str__(self):
        Title = self.category
        while len(Title) < 30:
            Title = f'*{Title}*'
        if len(Title) == 31:
            Title = Title[0:30]
        String = ''
        String += Title + '\n'
        # return str(self.ledger)

        # Make a formatted version of the ledger with the right number of characters.
        import copy
        sum = 0
        ledgCopy = copy.deepcopy(self.ledger)
        for i in ledgCopy:
            while len(i["description"]) < 23:
                i["description"] += ' '
            String += (f'{i["description"][0:23]}')

            sum += i["amount"]
            i["amount"] = f'{i["amount"]:.2f}'
            while len(str(i["amount"])) < 7:
                i["amount"] = ' ' + str(i["amount"])
            String += (f'{i["amount"][0:7]}\n')
        String += f'Total: {sum}'

        return String


def create_spend_chart(
        categories):  # create function to make spend chart, starting with making a dictionary of categories and total withdrawals
    if isinstance(categories, list):
        withsdict = dict()
        for n in categories:
            withs = 0
            for d in n.ledger:
                if int(d['amount']) < 0:
                    withs += d['amount']
            withsdict[n.category] = withs
        print(withsdict)

        sumWiths = 0  # find total withdrawals.
        for key in withsdict:
            sumWiths += withsdict[key]

        withsPercent = dict()  # find percentage spent in each category.
        for key in withsdict:
            withsPercent[key] = (withsdict[key] / sumWiths) * 100
        print(withsPercent)

        # Start making the bar graph.
        String = 'Percentage spent by category\n'
        for i in range(100, -1, -10):
            n = str(i)
            while len(n) < 3:
                n = ' ' + n
            Line = f'{n}|'
            for n in categories:
                if withsPercent[n.category] >= i:
                    Line += ' o '
                else:
                    Line += '   '
            String += f'{Line} \n'
        String += '    '
        for i in range(0, len(categories)):
            String += '---'
        String += '-\n'
        # Now for the vertical category names...
        catMaxLen = 0
        for i in categories:
            if len(i.category) > catMaxLen:
                catMaxLen = len(i.category)

        for n in range(0, catMaxLen):
            line = '    '
            for i in categories:
                try:
                    line += f' {i.category[n]} '
                except:
                    line += '   '
            String += f'{line} \n'
        String = String[:-1]
        return String
    else:
        print('Format that as a list please.')