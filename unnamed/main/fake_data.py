from random import choice, randint, randrange, random
from datetime import datetime as dt, timedelta
import string
import datetime

def gen_str(max_size=10):
    allchar = string.ascii_letters + string.digits
    return "".join(choice(allchar) for _ in range(randint(1, max_size)))

def gen_date(start=dt(2000, 1, 1), end=dt.now()):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

def gen_customer():
    name = gen_str()
    surname = gen_str()
    email = gen_str()
    age = randint(1, 100)
    purch_sum = round(randint(1, 10000) * random(), 3)
    return name, surname, email, age, purch_sum

def gen_item():
    name = gen_str()
    price = round(randint(1, 1000) * random(), 3)
    amount = randint(0, 1000)
    weight = round(randint(1, 10) * random(), 3)
    return name, price, amount, weight

def gen_purchase(customers, items):
    customer = choice(customers)
    item = choice(items)
    purch_date = gen_date()
    discount = round(randint(0, 30) * 0.01, 3)
    return customer, item, purch_date, discount