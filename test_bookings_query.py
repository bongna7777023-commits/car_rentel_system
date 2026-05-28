#!/usr/bin/env python
"""Test the bookings query directly"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.models.db_config import get_db_connection, close_db_connection

# Test with user_id 15 (our test user)
user_id = 15

conn = get_db_connection()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    print(f"\n🔍 Testing bookings query for user_id={user_id}:")
    print("="*80)
    
    # Run the exact query from the bookings route
    query = """
        SELECT
            b.id,
            b.booking_reference,
            b.status,
            b.total_cost,
            b.discount_amount,
            b.start_date,
            b.end_date,
            b.pickup_location,
            b.dropoff_location,
            b.created_at,
            c.name AS car_name,
            c.image AS car_image,
            c.id AS car_id,
            u.username,
            u.email,
            u.first_name,
            u.last_name,
            u.phone,
            p.code AS promo_code
        FROM bookings b
        LEFT JOIN cars c ON c.id = b.car_id
        LEFT JOIN users u ON u.id = b.user_id
        LEFT JOIN promotions p ON p.id = b.promotion_id
        WHERE b.user_id = %s
        ORDER BY b.created_at DESC
    """
    
    cursor.execute(query, (user_id,))
    bookings = cursor.fetchall()
    
    print(f"\n✅ Query returned {len(bookings)} bookings")
    if bookings:
        for b in bookings:
            print(f"\n  Booking #{b['id']}:")
            print(f"    Reference: {b['booking_reference']}")
            print(f"    Status: {b['status']}")
            print(f"    Car: {b['car_name']} (ID: {b['car_id']})")
            print(f"    User: {b['first_name']} {b['last_name']} ({b['email']})")
            print(f"    Dates: {b['start_date']} to {b['end_date']}")
            print(f"    Total Cost: ${b['total_cost']}")
    else:
        print("\n❌ No bookings found!")
    
    cursor.close()
    close_db_connection(conn)
