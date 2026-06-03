"""
Seed data for all tables in the car rental system.
Run: python scripts/seed_data.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta, date
from werkzeug.security import generate_password_hash
from app.models.db_config import get_db_connection, close_db_connection


def seed_users(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS cnt FROM users")
    if cursor.fetchone()['cnt'] > 3:
        cursor.close()
        return False

    users = [
        ('Alice Johnson', 'alice@example.com', 'AlicePass1', '1234567890'),
        ('Bob Smith', 'bob@example.com', 'BobPass123', '0987654321'),
        ('Charlie Brown', 'charlie@example.com', 'CharliePass1', '1122334455'),
    ]
    inserted = 0
    for name, email, pw, phone in users:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            continue
        pwhash = generate_password_hash(pw)
        cursor.execute(
            "INSERT INTO users (name, email, password, phone) VALUES (%s, %s, %s, %s)",
            (name, email, pwhash, phone)
        )
        inserted += 1
    conn.commit()
    cursor.close()
    return inserted


def seed_cars(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS cnt FROM cars")
    if cursor.fetchone()['cnt'] > 0:
        cursor.close()
        return False

    cars = [
        ('Tesla Model S', 'Tesla', 'Model S', 2024, 'luxury', 299.99,
         'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800', 5, 'automatic',
         'Electric', 'Electric Motor', 1020, 0, 'LIC-TSLA-001', '5YJSA1E26LF123456',
         'Main Branch', '["Autopilot","Premium Sound","Panoramic Roof","Heated Seats"]',
         'Pearl White', 4, 2, True, True, True, False),
        ('BMW 7 Series', 'BMW', '7 Series', 2024, 'luxury', 249.99,
         'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800', 5, 'automatic',
         'Gasoline', '4.4L V8', 523, 0, 'LIC-BMW-002', 'WBA7E2C54LJ789012',
         'Main Branch', '["Massage Seats","Executive Lounge","Premium Audio","Night Vision"]',
         'Black Sapphire', 4, 3, True, True, True, False),
        ('Mercedes-Benz S-Class', 'Mercedes-Benz', 'S-Class', 2024, 'luxury', 279.99,
         'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800', 5, 'automatic',
         'Gasoline', '3.0L V6', 429, 0, 'LIC-MB-003', 'WDX7L8D94KN345678',
         'Main Branch', '["MBUX System","Burmester Audio","Air Balance","Magic Body Control"]',
         'Selenite Grey', 4, 3, True, True, True, False),
        ('Toyota Camry', 'Toyota', 'Camry', 2024, 'sedan', 89.99,
         'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800', 5, 'automatic',
         'Gasoline', '2.5L I4', 203, 0, 'LIC-TOY-004', '4T1B11HK5LU901234',
         'Main Branch', '["Apple CarPlay","Lane Assist","Adaptive Cruise","Backup Camera"]',
         'Silver', 4, 2, True, True, True, True),
        ('Honda Accord', 'Honda', 'Accord', 2024, 'sedan', 85.99,
         'https://images.unsplash.com/photo-1590362891991-f776e747a588?w=800', 5, 'automatic',
         'Gasoline', '1.5L I4 Turbo', 192, 0, 'LIC-HON-005', '1HGCV1F45LA567890',
         'Main Branch', '["Honda Sensing","Wireless Charging","Sunroof","Premium Audio"]',
         'Modern Steel', 4, 2, True, True, True, False),
        ('Porsche 911', 'Porsche', '911', 2024, 'sports', 399.99,
         'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800', 2, 'automatic',
         'Gasoline', '3.0L Twin-Turbo H6', 443, 0, 'LIC-POR-006', 'WP0AA2A97LS123456',
         'Main Branch', '["Sport Chrono","PASM","Sport Exhaust","Carbon Brakes"]',
         'Guards Red', 2, 1, True, True, True, False),
        ('Ford Mustang GT', 'Ford', 'Mustang GT', 2024, 'sports', 179.99,
         'https://images.unsplash.com/photo-1584345604476-8ec5f49fdb28?w=800', 4, 'manual',
         'Gasoline', '5.0L V8', 450, 0, 'LIC-FRD-007', '1FA6P8CF2LZ789012',
         'Main Branch', '["5.0L V8","Performance Pack","Recaro Seats","Active Exhaust"]',
         'Race Red', 2, 1, True, True, True, False),
        ('Toyota RAV4', 'Toyota', 'RAV4', 2024, 'suv', 95.99,
         'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800', 5, 'automatic',
         'Gasoline', '2.5L I4', 203, 0, 'LIC-TOY-008', '2T3H1RFV6LW345678',
         'Main Branch', '["AWD","Safety Sense","Power Liftgate","Blind Spot Monitor"]',
         'Blueprint', 4, 3, True, True, True, True),
        ('Honda CR-V', 'Honda', 'CR-V', 2024, 'suv', 92.99,
         'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800', 5, 'automatic',
         'Gasoline', '1.5L I4 Turbo', 190, 0, 'LIC-HON-009', '7FARW1H51LE901234',
         'Main Branch', '["Honda Sensing","Turbo Engine","Hands-Free Liftgate","Panoramic Sunroof"]',
         'Sonic Gray Pearl', 4, 3, True, True, True, False),
        ('Lamborghini Huracán', 'Lamborghini', 'Huracán EVO', 2024, 'exotic', 899.99,
         'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800', 2, 'automatic',
         'Gasoline', '5.2L V10', 631, 0, 'LIC-LAM-010', 'ZHWUE4UJ8LLA567890',
         'VIP Garage', '["V10 Engine","Carbon Fiber","Track Mode","Launch Control"]',
         'Arancio Borealis', 2, 1, True, True, False, False),
        ('Ferrari F8 Tributo', 'Ferrari', 'F8 Tributo', 2024, 'exotic', 999.99,
         'https://images.unsplash.com/photo-1592198084033-aade902d1aae?w=800', 2, 'automatic',
         'Gasoline', '3.9L Twin-Turbo V8', 710, 0, 'LIC-FER-011', 'ZFF80JNA4LZ123456',
         'VIP Garage', '["Twin-Turbo V8","Side Slip Control","F1-Trac","Carbon Fiber"]',
         'Rosso Corsa', 2, 1, True, True, False, False),
    ]

    cursor.executemany("""
        INSERT INTO cars (name, brand, model, year, category, price, image, seats,
                          transmission, fuel_type, engine, horsepower, mileage,
                          license_plate, vin, location, features, color, doors,
                          luggage_capacity, air_conditioning, gps, bluetooth, backup_camera)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, cars)
    conn.commit()
    cursor.close()
    return len(cars)


def seed_admin_accounts(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS cnt FROM admin_accounts")
    if cursor.fetchone()['cnt'] > 1:
        cursor.close()
        return False

    admins = [
        ('Vanna Admin', 'vanna@luxedrive.com', 'AdminVanna1', '0977777777'),
    ]
    inserted = 0
    for name, email, pw, phone in admins:
        cursor.execute("SELECT id FROM admin_accounts WHERE email = %s", (email,))
        if cursor.fetchone():
            continue
        pwhash = generate_password_hash(pw)
        cursor.execute(
            "INSERT INTO admin_accounts (fullname, email, phone, password) VALUES (%s, %s, %s, %s)",
            (name, email, phone, pwhash)
        )
        inserted += 1
    conn.commit()
    cursor.close()
    return inserted


def seed_promotions(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS cnt FROM promotions")
    if cursor.fetchone()['cnt'] > 0:
        cursor.close()
        return False

    today = date.today()
    promotions = [
        ('SUMMER20', 'Summer special - 20% off all bookings', 'percentage', 20.00,
         today, today + timedelta(days=90), 100, 0, True),
        ('WELCOME10', 'Welcome discount for new customers', 'percentage', 10.00,
         today, today + timedelta(days=365), 500, 0, True),
        ('FLAT50', '$50 off any booking over $200', 'fixed', 50.00,
         today, today + timedelta(days=60), 50, 0, True),
        ('VIP25', 'VIP members - 25% off luxury cars', 'percentage', 25.00,
         today, today + timedelta(days=45), 20, 0, True),
    ]
    cursor.executemany("""
        INSERT INTO promotions (code, description, discount_type, discount_value,
                                active_from, active_to, max_uses, uses_count, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, promotions)
    conn.commit()
    cursor.close()
    return len(promotions)


def seed_bookings(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS cnt FROM bookings")
    if cursor.fetchone()['cnt'] > 0:
        cursor.close()
        return False

    cursor.execute("SELECT id, name, email FROM users ORDER BY id LIMIT 3")
    users = cursor.fetchall()
    cursor.execute("SELECT id, name, image, price FROM cars ORDER BY id LIMIT 5")
    cars = cursor.fetchall()

    if len(users) < 1 or len(cars) < 1:
        cursor.close()
        return False

    today = date.today()
    bookings_data = []

    # Booking 1: Alice -> Tesla (3 days)
    if len(users) > 0 and len(cars) > 0:
        u = users[0]
        c = cars[0]
        pickup = today + timedelta(days=2)
        ret = pickup + timedelta(days=3)
        days = (ret - pickup).days
        base = float(c['price']) * days
        bookings_data.append((
            u['email'], u['name'], '1234567890',
            c['id'], c['name'], c['image'],
            pickup, ret, days, base, 0, base, None, 'confirmed'
        ))

    # Booking 2: Bob -> BMW (5 days)
    if len(users) > 1 and len(cars) > 1:
        u = users[1]
        c = cars[1]
        pickup = today + timedelta(days=5)
        ret = pickup + timedelta(days=5)
        days = (ret - pickup).days
        base = float(c['price']) * days
        bookings_data.append((
            u['email'], u['name'], '0987654321',
            c['id'], c['name'], c['image'],
            pickup, ret, days, base, 0, base, None, 'confirmed'
        ))

    # Booking 3: Alice -> Camry (2 days, completed)
    if len(users) > 0 and len(cars) > 2:
        u = users[0]
        c = cars[3]
        pickup = today - timedelta(days=10)
        ret = pickup + timedelta(days=2)
        days = (ret - pickup).days
        base = float(c['price']) * days
        bookings_data.append((
            u['email'], u['name'], '1234567890',
            c['id'], c['name'], c['image'],
            pickup, ret, days, base, 0, base, None, 'completed'
        ))

    # Booking 4: Charlie -> Mustang (7 days)
    if len(users) > 2 and len(cars) > 6:
        u = users[2]
        c = cars[6]
        pickup = today + timedelta(days=14)
        ret = pickup + timedelta(days=7)
        days = (ret - pickup).days
        base = float(c['price']) * days
        bookings_data.append((
            u['email'], u['name'], '1122334455',
            c['id'], c['name'], c['image'],
            pickup, ret, days, base, 0, base, None, 'confirmed'
        ))

    if not bookings_data:
        cursor.close()
        return False

    cursor.executemany("""
        INSERT INTO bookings (user_email, user_name, phone, car_id, car_name,
                              car_image, pickup_date, return_date, days, base_cost,
                              discount_amount, total_cost, promotion_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, bookings_data)
    conn.commit()
    cursor.close()
    return len(bookings_data)


def seed_notifications(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS cnt FROM notifications")
    if cursor.fetchone()['cnt'] > 0:
        cursor.close()
        return False

    cursor.execute("SELECT id, name FROM users ORDER BY id LIMIT 2")
    users = cursor.fetchall()
    cursor.execute("SELECT id, code FROM promotions ORDER BY id LIMIT 3")
    promos = cursor.fetchall()

    if len(users) < 1:
        cursor.close()
        return False

    notifications = []

    for u in users:
        notifications.append((
            u['id'], f'Welcome {u["name"]}!',
            'Thank you for joining LuxeDrive. Enjoy premium car rental services!',
            None, 0
        ))

    if len(promos) > 0:
        p = promos[0]
        if len(users) > 0:
            notifications.append((
                users[0]['id'], f'Promo: {p["code"]}',
                f'Use code {p["code"]} for your next booking and save big!',
                p['id'], 0
            ))

    cursor.executemany("""
        INSERT INTO notifications (user_id, title, message, promotion_id, is_read)
        VALUES (%s, %s, %s, %s, %s)
    """, notifications)
    conn.commit()
    cursor.close()
    return len(notifications)


def main():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database.")
        sys.exit(1)

    results = {}
    results['users'] = seed_users(conn)
    results['admin_accounts'] = seed_admin_accounts(conn)
    results['cars'] = seed_cars(conn)
    results['promotions'] = seed_promotions(conn)
    results['bookings'] = seed_bookings(conn)
    results['notifications'] = seed_notifications(conn)

    close_db_connection(conn)

    print("Seed data results:")
    for table, count in results.items():
        if count is False:
            print(f"  {table}: already has data, skipped")
        elif count == 0:
            print(f"  {table}: 0 rows inserted")
        else:
            print(f"  {table}: {count} rows inserted")


if __name__ == '__main__':
    main()
