import psycopg2
import pandas as pd

# Connect to the Language database
class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="",
            host="localhost",
            port="5433"
        )
        # 2. Create a cursor object to execute SQL commands
        self.cursor = self.conn.cursor()
        print("Database Connected")

    def entry(self, englishText, targetText, language, level, grammarPoint):
        self.cursor.execute(f"INSERT INTO Cards (english_text, target_text, language, level, grammar_point) "
        f"VALUES('{englishText}', '{targetText}', '{language}', '{level}', '{grammarPoint}');")
        self.conn.commit()
        print("Card inserted successfully!")
    
    def updateEntry(self, id):
        print("Entry Updated")
    
    def deletEntry(self, id):
        print("Entry Deleted")
    
    def loadCards(self, language):
        try:
            self.cursor.execute(f"SELECT * FROM Cards WHERE language = '{language}'")
            results = self.cursor.fetchall()

            cards = []

            for row in results:
                card = {
                "id": row[0],
                "english_text": row[1],
                "target_text": row[2],
                "language": row[3],
                "level": row[4],
                "grammar_point": row[5]
                }
                cards.append(card)
            return cards
        except Exception as error:
            self.conn.rollback()
            print("Database error:", error)
            raise
        
    def saveDecision(self, user_id, card_id, decision):
        try:
            self.cursor.execute(
                """
                INSERT INTO user_cards (user_id, card_id, decision)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, card_id)
                DO UPDATE SET
                    decision = EXCLUDED.decision
                """,
                (user_id, card_id, decision)
            )
            self.conn.commit()
            print("Decison Saved")
        except Exception as error:

            # Undo the failed transaction.
            self.conn.rollback()

            # Print the actual database error.
            print("Database error:", error)

            raise

    def getLessonCards(self, user_id, language):
        try: 
            self.cursor.execute(
                """
                SELECT english_text, target_text, grammar_point FROM User_cards U
                JOIN Cards C ON c.id = U.card_id
                WHERE u.user_id = %s AND 
                u.decision = 'like' AND 
                LOWER(c.language) = %s;

                """, (user_id, language,))

            results = self.cursor.fetchall()
            cards = []
            for row in results:
                card = {
                    "english_text": row[0],
                    "target_text": row[1],
                    "grammar_point": row[2]
                }
                cards.append(card)
            print("obtained cards for lesson")
        
            return cards

        
        except Exception as error:
            self.conn.rollback()
            print("Database error:", error)
            raise