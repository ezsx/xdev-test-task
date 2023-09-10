from faker import Faker
from sqlalchemy import create_engine, text
import random
import uuid

# Create a Faker instance
fake = Faker()

# Create a SQLAlchemy engine
engine = create_engine('postgresql://user:mysecretpassword@localhost:5432/mydatabase')

# Number of records to generate
num_records = 100

# Start a new SQLAlchemy session
with engine.connect() as connection:
    for _ in range(num_records):
        # Generate fake data for the users table
        user_id = connection.execute(text("INSERT INTO users (name, email, created_at, updated_at) VALUES (:name, :email, :created_at, :updated_at) RETURNING id"),
                                     name=fake.name(),
                                     email=fake.email(),
                                     created_at=fake.date_time_this_year(),
                                     updated_at=fake.date_time_this_year()).scalar()

        # Generate fake data for the pillows table
        connection.execute(text("INSERT INTO pillows (user_id, device_uuid, num_pillows, created_at, updated_at, deleted_at) VALUES (:user_id, :device_uuid, :num_pillows, :created_at, :updated_at, :deleted_at)"),
                           user_id=user_id,
                           device_uuid=str(uuid.uuid4()),
                           num_pillows=random.randint(1, 10),
                           created_at=fake.date_time_this_year(),
                           updated_at=fake.date_time_this_year(),
                           deleted_at=fake.date_time_this_year() if random.choice([True, False]) else None)

        # Generate fake data for the pillows_history table
        connection.execute(text("INSERT INTO pillows_history (user_id, device_uuid, amount, created_at) VALUES (:user_id, :device_uuid, :amount, :created_at)"),
                           user_id=user_id,
                           device_uuid=str(uuid.uuid4()),
                           amount=random.randint(1, 10),
                           created_at=fake.date_time_this_year())
