"""
NonLogs Backend - Database Management Script
Initialize and seed the database
"""

from app import app, db, Cryptocurrency
from datetime import datetime
import sys


def init_db():
    """Initialize the database"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")


def seed_db():
    """Seed the database with sample data"""
    with app.app_context():
        print("\nSeeding database with cryptocurrency data...")
        
        # Sample cryptocurrencies
        cryptocurrencies = [
            {
                'symbol': 'BTC',
                'name': 'Bitcoin',
                'price': 45320.50,
                'change_24h': 5.2,
                'market_cap': 890000000000
            },
            {
                'symbol': 'ETH',
                'name': 'Ethereum',
                'price': 2580.75,
                'change_24h': 3.8,
                'market_cap': 310000000000
            },
            {
                'symbol': 'XRP',
                'name': 'Ripple',
                'price': 0.58,
                'change_24h': 2.1,
                'market_cap': 31000000000
            },
            {
                'symbol': 'ADA',
                'name': 'Cardano',
                'price': 0.42,
                'change_24h': 1.5,
                'market_cap': 15000000000
            },
            {
                'symbol': 'SOL',
                'name': 'Solana',
                'price': 24.50,
                'change_24h': 4.2,
                'market_cap': 8000000000
            },
            {
                'symbol': 'BNB',
                'name': 'Binance Coin',
                'price': 312.45,
                'change_24h': 2.8,
                'market_cap': 48000000000
            },
            {
                'symbol': 'USDC',
                'name': 'USD Coin',
                'price': 1.00,
                'change_24h': 0.0,
                'market_cap': 25000000000
            },
            {
                'symbol': 'DOGE',
                'name': 'Dogecoin',
                'price': 0.12,
                'change_24h': 3.5,
                'market_cap': 18000000000
            }
        ]
        
        # Check if cryptocurrencies already exist
        if Cryptocurrency.query.count() > 0:
            print("✅ Cryptocurrencies already seeded!")
            return
        
        # Add cryptocurrencies
        for crypto_data in cryptocurrencies:
            crypto = Cryptocurrency(
                symbol=crypto_data['symbol'],
                name=crypto_data['name'],
                price=crypto_data['price'],
                change_24h=crypto_data['change_24h'],
                market_cap=crypto_data['market_cap']
            )
            db.session.add(crypto)
        
        try:
            db.session.commit()
            print(f"✅ Successfully seeded {len(cryptocurrencies)} cryptocurrencies!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding database: {str(e)}")
            sys.exit(1)


def reset_db():
    """Reset the database (drop all tables and recreate)"""
    with app.app_context():
        print("⚠️  Warning: This will delete all data!")
        response = input("Are you sure you want to reset the database? (yes/no): ")
        
        if response.lower() != 'yes':
            print("❌ Database reset cancelled")
            return
        
        print("Dropping all tables...")
        db.drop_all()
        print("✅ All tables dropped!")
        
        init_db()
        seed_db()
        print("✅ Database reset complete!")


def show_stats():
    """Show database statistics"""
    with app.app_context():
        from app import User, Trade, Portfolio
        
        print("\n📊 Database Statistics:")
        print(f"  Users: {User.query.count()}")
        print(f"  Trades: {Trade.query.count()}")
        print(f"  Portfolio Items: {Portfolio.query.count()}")
        print(f"  Cryptocurrencies: {Cryptocurrency.query.count()}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python manage.py [command]")
        print("\nCommands:")
        print("  init        - Initialize database tables")
        print("  seed        - Seed database with sample data")
        print("  reset       - Reset database (drop all tables)")
        print("  stats       - Show database statistics")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        init_db()
    elif command == 'seed':
        seed_db()
    elif command == 'reset':
        reset_db()
    elif command == 'stats':
        show_stats()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
