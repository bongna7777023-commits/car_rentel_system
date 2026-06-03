from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


class AdminAccount(db.Model):
    __tablename__ = 'admin_accounts'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    car_id = db.Column(db.Integer, nullable=False)
    car_name = db.Column(db.String(100), nullable=False)
    car_image = db.Column(db.Text)
    pickup_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    base_cost = db.Column(db.Numeric(10, 2), nullable=False)
    discount_amount = db.Column(db.Numeric(10, 2), default=0)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    discounts_applied = db.Column(db.Text)
    promotion_id = db.Column(db.Integer, default=None)
    status = db.Column(db.String(20), default='confirmed')
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)


class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.Text)
    seats = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(20), nullable=False)
    fuel_type = db.Column(db.String(30), default='Gasoline')
    engine = db.Column(db.String(50))
    horsepower = db.Column(db.Integer)
    mileage = db.Column(db.Integer, default=0)
    license_plate = db.Column(db.String(20), unique=True)
    vin = db.Column(db.String(50), unique=True)
    location = db.Column(db.String(100), default='Main Branch')
    features = db.Column(db.Text)
    color = db.Column(db.String(50))
    doors = db.Column(db.Integer, default=4)
    luggage_capacity = db.Column(db.Integer, default=2)
    air_conditioning = db.Column(db.Boolean, default=True)
    gps = db.Column(db.Boolean, default=False)
    bluetooth = db.Column(db.Boolean, default=True)
    backup_camera = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Promotion(db.Model):
    __tablename__ = 'promotions'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    discount_type = db.Column(db.String(20), nullable=False, default='percentage')
    discount_value = db.Column(db.Numeric(10, 2), nullable=False)
    active_from = db.Column(db.Date)
    active_to = db.Column(db.Date)
    max_uses = db.Column(db.Integer, default=None)
    uses_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text)
    promotion_id = db.Column(db.Integer)
    is_read = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


__all__ = [
    'User', 'AdminAccount', 'Booking', 'Car', 'Promotion', 'Notification',
]
