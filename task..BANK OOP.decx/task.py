import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hash_password(password) == hashed
 models.py – klasslar

import uuid
import json
from datetime import datetime
from utils import hash_password, check_password

class Transaction:
    def __init__(self, type_, amount, from_account, to_account):
        self.transaction_id = str(uuid.uuid4())
        self.type = type_
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return self.__dict__

class BankAccount:
    def __init__(self, account_number, user_id, currency='USD'):
        self.account_number = account_number
        self.user_id = user_id
        self.balance = 0.0
        self.currency = currency
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(Transaction("deposit", amount, self.account_number, self.account_number).to_dict())

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(Transaction("withdraw", amount, self.account_number, self.account_number).to_dict())
            return True
        return False

    def transfer(self, to_account, amount):
        if amount <= self.balance:
            self.balance -= amount
            to_account.balance += amount
            self.transactions.append(Transaction("transfer", amount, self.account_number, to_account.account_number).to_dict())
            to_account.transactions.append(Transaction("transfer", amount, self.account_number, to_account.account_number).to_dict())
            return True
        return False

    def get_statement(self):
        return self.transactions

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "user_id": self.user_id,
            "balance": self.balance,
            "currency": self.currency,
            "transactions": self.transactions
        }

class User:
    def __init__(self, user_id, full_name, phone, password):
        self.user_id = user_id
        self.full_name = full_name
        self.phone = phone
        self.password = hash_password(password)
        self.accounts = []

    def authenticate(self, password):
        return check_password(password, self.password)

    def add_account(self, account):
        self.accounts.append(account.account_number)

    def get_accounts(self):
        return self.accounts

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "phone": self.phone,
            "password": self.password,
            "accounts": self.accounts
        }

class BankSystem:
    def __init__(self):
        self.users = {}
        self.accounts = {}
        self.failed_logins = {}
        self.load_from_file()

    def register_user(self, name, phone, password):
        if phone in self.users:
            return None
        user_id = len(self.users) + 1
        user = User(user_id, name, phone, password)
        self.users[phone] = user
        self.save_to_file()
        return user

    def login(self, phone, password):
        user = self.users.get(phone)
        if not user:
            return None
        if self.failed_logins.get(phone, 0) >= 3:
            print("❌ Hisob bloklangan.")
            return None
        if user.authenticate(password):
            self.failed_logins[phone] = 0
            return user
        else:
            self.failed_logins[phone] = self.failed_logins.get(phone, 0) + 1
            return None

    def create_account(self, user, currency='USD'):
        acc_number = str(100000 + len(self.accounts) + 1)
        account = BankAccount(acc_number, user.user_id, currency)
        self.accounts[acc_number] = account
        user.add_account(account)
        self.save_to_file()
        return account

    def find_user_by_phone(self, phone):
        return self.users.get(phone)

    def save_to_file(self):
        data = {
            "users": {phone: user.to_dict() for phone, user in self.users.items()},
            "accounts": {acc_num: acc.to_dict() for acc_num, acc in self.accounts.items()}
        }
        with open("storage.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        try:
            with open("storage.json", "r") as f:
                data = json.load(f)
                for phone, u in data.get("users", {}).items():
                    user = User(u['user_id'], u['full_name'], phone, "temp")
                    user.password = u['password']
                    user.accounts = u['accounts']
                    self.users[phone] = user
                for acc_num, a in data.get("accounts", {}).items():
                    acc = BankAccount(a['account_number'], a['user_id'], a['currency'])
                    acc.balance = a['balance']
                    acc.transactions = a['transactions']
                    self.accounts[acc_num] = acc
        except FileNotFoundError:
            pass
 main.py – dastur ishga tushirish

from models import BankSystem

bank = BankSystem()

while True:
    print("\n1. Ro'yxatdan o'tish\n2. Kirish\n3. Chiqish")
    tanlov = input("Tanlang: ")

    if tanlov == '1':
        name = input("Ism: ")
        phone = input("Telefon: ")
        password = input("Parol: ")
        user = bank.register_user(name, phone, password)
        if user:
            print(" Muvaffaqiyatli ro'yxatdan o'tdingiz.")
        else:
            print("⚠ Bu telefon raqam allaqachon ro'yxatdan o'tgan.")

    elif tanlov == '2':
        phone = input("Telefon: ")
        password = input("Parol: ")
        user = bank.login(phone, password)
        if user:
            print(f" Xush kelibsiz, {user.full_name}!")

            while True:
                print("\n1. Hisob yaratish\n2. Balans ko'rish\n3. Pul qo'shish\n4. Pul yechish\n5. Pul o'tkazish\n6. Tranzaktsiyalar\n7. Chiqish")
                action = input("Tanlang: ")

                if action == '1':
                    currency = input("Valyuta (USD/EUR/UZS): ")
                    acc = bank.create_account(user, currency)
                    print(f" Yangi hisob: {acc.account_number}")

                elif action == '2':
                    for acc_num in user.get_accounts():
                        acc = bank.accounts[acc_num]
                        print(f"{acc.account_number} | {acc.balance} {acc.currency}")

                elif action == '3':
                    acc_num = input("Hisob raqami: ")
                    amount = float(input("Miqdor: "))
                    acc = bank.accounts.get(acc_num)
                    if acc and acc.user_id == user.user_id:
                        acc.deposit(amount)
                        print(" Pul qo‘shildi.")
                        bank.save_to_file()
                    else:
                        print("⚠ Hisob topilmadi.")

                elif action == '4':
                    acc_num = input("Hisob raqami: ")
                    amount = float(input("Miqdor: "))
                    acc = bank.accounts.get(acc_num)
                    if acc and acc.user_id == user.user_id:
                        if acc.withdraw(amount):
                            print(" Pul yechildi.")
                            bank.save_to_file()
                        else:
                            print("⚠ Yetarli mablag' yo'q.")
                    else:
                        print("⚠ Hisob topilmadi.")

                elif action == '5':
                    from_acc = input("Sizning hisob raqamingiz: ")
                    to_acc = input("Qabul qiluvchi hisob raqami: ")
                    amount = float(input("Miqdor: "))
                    acc1 = bank.accounts.get(from_acc)
                    acc2 = bank.accounts.get(to_acc)
                    if acc1 and acc2 and acc1.user_id == user.user_id:
                        if acc1.transfer(acc2, amount):
                            print(" Pul o'tkazildi.")
                            bank.save_to_file()
                        else:
                            print(" Yetarli mablag' yo'q.")
                    else:
                        print(" Hisob(lar) topilmadi.")

                elif action == '6':
                    for acc_num in user.get_accounts():
                        acc = bank.accounts[acc_num]
                        print(f"\nHisob: {acc.account_number}")
                        for t in acc.get_statement():
                            print(f"{t['timestamp']} | {t['type']} | {t['amount']}")

                elif action == '7':
                    break
        else:
            print(" Login yoki parol noto‘g‘ri.")

    elif tanlov == '3':
        break
