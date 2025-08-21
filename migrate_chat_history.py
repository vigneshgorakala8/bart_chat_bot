#!/usr/bin/env python3
"""
Migration script to update chat_history table to Rails-style schema
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import ChatHistory
from sqlalchemy import text

def migrate_chat_history():
    """Migrate chat_history table to new schema"""
    app = create_app()
    
    with app.app_context():
        print("=== Chat History Migration ===")
        
        # Check if we need to migrate
        try:
            # Try to access the old columns
            old_records = db.session.execute(text("SELECT message, response, timestamp FROM chat_history LIMIT 1")).fetchall()
            if old_records:
                print("Found old schema. Starting migration...")
                
                # Create new table with Rails-style schema
                print("Creating new chat_histories table...")
                db.session.execute(text("""
                    CREATE TABLE IF NOT EXISTS chat_histories_new (
                        id SERIAL PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        chat_id INTEGER NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                    )
                """))
                
                # Copy data from old table to new table
                print("Migrating data...")
                db.session.execute(text("""
                    INSERT INTO chat_histories_new (question, answer, chat_id, created_at, updated_at)
                    SELECT message, response, chat_id, timestamp, timestamp
                    FROM chat_history
                """))
                
                # Drop old table and rename new table
                print("Updating table structure...")
                db.session.execute(text("DROP TABLE chat_history"))
                # Check if chat_histories already exists and drop it
                try:
                    db.session.execute(text("DROP TABLE chat_histories"))
                except:
                    pass  # Table doesn't exist, which is fine
                db.session.execute(text("ALTER TABLE chat_histories_new RENAME TO chat_histories"))
                
                # Create index on chat_id
                db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_chat_histories_chat_id ON chat_histories(chat_id)"))
                
                db.session.commit()
                print("✅ Migration completed successfully!")
                
            else:
                print("No old data found. Table might already be migrated or empty.")
                
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()
            return False
        
        # Verify migration
        try:
            new_records = db.session.execute(text("SELECT question, answer, chat_id, created_at FROM chat_histories LIMIT 1")).fetchall()
            if new_records:
                print("✅ Migration verification successful!")
                print(f"Sample record: question='{new_records[0][0][:50]}...', answer='{new_records[0][1][:50]}...'")
            else:
                print("⚠️  No records found in new table")
                
        except Exception as e:
            print(f"❌ Migration verification failed: {e}")
            return False
        
        return True

def rollback_migration():
    """Rollback migration if needed"""
    app = create_app()
    
    with app.app_context():
        print("=== Rollback Migration ===")
        
        try:
            # Check if new table exists
            new_records = db.session.execute(text("SELECT question, answer, chat_id, created_at FROM chat_histories LIMIT 1")).fetchall()
            if new_records:
                print("Found new schema. Rolling back...")
                
                # Create old table structure
                db.session.execute(text("""
                    CREATE TABLE IF NOT EXISTS chat_history_old (
                        id SERIAL PRIMARY KEY,
                        message TEXT NOT NULL,
                        response TEXT NOT NULL,
                        chat_id INTEGER NOT NULL,
                        timestamp TIMESTAMP DEFAULT NOW()
                    )
                """))
                
                # Copy data back
                db.session.execute(text("""
                    INSERT INTO chat_history_old (message, response, chat_id, timestamp)
                    SELECT question, answer, chat_id, created_at
                    FROM chat_histories
                """))
                
                # Drop new table and rename old table
                db.session.execute(text("DROP TABLE chat_histories"))
                db.session.execute(text("ALTER TABLE chat_history_old RENAME TO chat_history"))
                
                db.session.commit()
                print("✅ Rollback completed successfully!")
                
            else:
                print("No new data found.")
                
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            db.session.rollback()
            return False
        
        return True

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        success = rollback_migration()
    else:
        success = migrate_chat_history()
    
    if success:
        print("\n🎉 Operation completed successfully!")
    else:
        print("\n❌ Operation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
