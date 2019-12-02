from app import db
from sqlalchemy.dialects.postgresql import JSON, BYTEA, TIME, BOOLEAN


class Stocks(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Numeric(100, 2), nullable=False)
    index = db.Column(db.String(25), nullable=False)
    sector = db.Column(db.String(250), nullable=False)

    def __init__(self, name, quantity, cost, index, sector):
        self.name = name
        self.quantity = quantity
        self.cost = cost
        self.index = index
        self.sector = sector

    def __repr__(self):
        return "<id {}, name {}>".format(self.id, self.name)

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def insert(cls, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()


class CurStockData(db.Model):
    __tablename__ = "cur_stock_data"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Numeric(100, 2), nullable=False)
    chg = db.Column(db.Numeric(100, 2), nullable=False)
    dividend = db.Column(db.Numeric(100, 2))
    eps = db.Column(db.Numeric(100, 2))
    pe = db.Column(db.Numeric(100, 2))
    d_open = db.Column(db.Numeric(100, 2), nullable=False)
    d_close = db.Column(db.Numeric(100, 2), nullable=False)

    def __init__(self, name, cost, chg, dividend, eps, pe, d_open, d_close):
        self.name = name
        self.cost = cost
        self.chg = chg
        self.dividend = dividend
        self.eps = eps
        self.pe = pe
        self.d_open = d_open
        self.d_close = d_close

    def __repr__(self):
        return "<id {}, name {}>".format(self.id, self.name)

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def insert(cls, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()


class Leadership(db.Model):
    __tablename__ = "leadership"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    icon = db.Column(db.LargeBinary)
    description = db.Column(db.String(500))
    position = db.Column(db.String(50))
    major = db.Column(db.String(50))
    year = db.Column(db.Integer)
    active = db.Column(BOOLEAN())

    def __init__(self, name, icon, description, position, major, year):
        self.name = name
        self.icon = icon
        self.description = description
        self.active = True
        self.position = position
        self.major = major
        self.year = year

    # def __repr__(self):
    #     return "<id {}, name {}>".format(self.id, self.name)

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def insert(cls, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()
