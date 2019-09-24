from app import db


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
