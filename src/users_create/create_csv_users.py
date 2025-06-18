# Создание csv файла с 1000000 анкет

import csv
import random
from faker import Faker


fake = Faker('ru_RU')
Faker.seed(0)
random.seed(0)

def generate_user_row():
    return [
        fake.first_name(),
        fake.last_name(),
        fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        random.choice(["male", "female"]),
        ', '.join(fake.words(nb=random.randint(1, 5))),
        fake.city(),
        fake.password(length=10)
    ]

with open("users_1m.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['first_name', 'last_name', 'birth_date', 'gender', 'interests', 'city', 'hashed_password'])
    for _ in range(1_000_000):
        writer.writerow(generate_user_row())
