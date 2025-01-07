import pyodbc
import bcrypt

class AppDB:
    def __init__(self, cs):
        self._cs = cs
        self.connect_db()
    
    def connect_db(self):
        self._database = pyodbc.connect(self._cs)
        
        
    def validate_login(self, username, password):
        query = "SELECT pwt_pass FROM passwd_test WHERE pwt_username = ?;"
        
        
        result = self._database.cursor().execute(query, (username,)).fetchone()
        
        if result:
            db_pass = result[0].encode('utf-8')
            pass_hash = bcrypt.hashpw(password, db_pass)
            
            if pass_hash == db_pass:
                return True
                
        return False
        
        
    def get_next_question_id(self):
        query = "SELECT MAX(id) FROM quiz_questions;"
        
        result = self._database.cursor().execute(query)
        
        last_id = result.fetchone()
        
        return last_id[0] + 1
        
    def insert_question(self, text, answer):
        query = "INSERT INTO quiz_questions VALUES(?, ?, ?);"
        id = self.get_next_question_id()
        
        self._database.cursor().execute(query, (id, text, answer))
        self._database.commit()
        
    def get_question(self, q_id):
        query = """
                SELECT id, question, answer 
                    FROM quiz_questions 
                WHERE id = ?;
                """
                
        res = self._database.cursor().execute(query, (q_id,))
        
        x = res.fetchone()
        
        
        if x:
            quest = {'id':x[0], 'question':x[1], 'answer':x[2]}
        else:
            quest = None
        
        return quest
        
    