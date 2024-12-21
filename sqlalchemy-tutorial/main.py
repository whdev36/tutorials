from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, CHAR, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    ssn = Column(Integer, Sequence('person_ssn'), primary_key=True)
    first_name = Column('first_name', String(30))
    last_name = Column('last_name', String(30))
    gender = Column('gender', CHAR)
    age = Column('age', Integer)

    def __init__(self, ssn, first_name, last_name, gender, age):
        self.ssn = ssn
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f'({self.ssn}) {self.first_name} {self.last_name} ({self.gender}, {self.age})'

class Thing(Base):
    __tablename__ = 'things'
    tid = Column(Integer, Sequence('tid'), primary_key=True)
    description = Column('description', String(300))
    owner = Column(Integer, ForeignKey('people.ssn'))

    def __init__(self, tid, description, owner):
        self.tid = tid
        self.description = description
        self.owner = owner

    def __repr__(self):
        return f'({self.tid}) {self.description} owned by {self.owner}'

engine = create_engine('mysql+pymysql://root:password@localhost:3306/person', echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

p1 = Person(12345, 'Alice', 'Johnson', 'f', 28)
p2 = Person(12346, 'Bob', 'Williams', 'm', 42)
p3 = Person(12347, 'Charlie', 'Brown', 'm', 31)
p4 = Person(12348, 'Diana', 'Garcia', 'f', 25)
p5 = Person(12349, 'Ethan', 'Martinez', 'm', 36)
p6 = Person(12350, 'Fiona', 'Hernandez', 'f', 29)
p7 = Person(12351, 'George', 'Lopez', 'm', 45)
p8 = Person(12352, 'Hannah', 'Clark', 'f', 33)
p9 = Person(12353, 'Ian', 'Rodriguez', 'm', 22)
p10 = Person(12354, 'Julia', 'Lewis', 'f', 39)

people = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
for p in people:
    session.add(p)
session.commit()

results = session.query(Person).all()
for r in results:
    print(r)

results = session.query(Person).filter(Person.first_name == 'Bob')
for r in results:
    print(r)

results = session.query(Person).filter(Person.age > 25)
for r in results:
    print(r)

results = session.query(Person).filter(Person.last_name.like('%A%'))
for r in results:
    print(f'{r.first_name} {r.last_name}')

results = session.query(Person).filter(Person.first_name.in_(['Alice', 'Bob']))
for r in results:
    print(f'{r.ssn} - ({r.first_name} {r.last_name})')

t1 = Thing(1, 'Car', p1.ssn)
t2 = Thing(2, 'Book', p2.ssn)
t3 = Thing(3, 'Bike', p3.ssn)
t4 = Thing(4, 'Laptop', p4.ssn)
t5 = Thing(5, 'Phone', p5.ssn)
t6 = Thing(6, 'Tablet', p6.ssn)
t7 = Thing(7, 'Watch', p7.ssn)
t8 = Thing(8, 'Camera', p8.ssn)
t9 = Thing(9, 'Headphones', p9.ssn)
t10 = Thing(10, 'Speaker', p10.ssn)

things = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
for thing in things:
    session.add(thing)
session.commit()

results = session.query(Thing, Person).filter(Thing.owner == Person.ssn)
for r in results:
    print(r)