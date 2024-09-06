from app.database.connection import DatabaseConnection
import logging


# Configure logger
logger = logging.getLogger(__name__)

class Task:
    def __init__(self):
        self.database = DatabaseConnection()

    def database_connect(self):
        conn = self.database.connect()
        if conn is None:
            logger.critical("Failed to connect to the database.")
            return
        return conn

    def create_table(self):
        conn = self.database_connect()
        
        try:
            with conn.cursor() as cursor:
                # Create ENUM Type: The DO $$ BEGIN ... END $$; block ensures that the ENUM type is created only if it doesn’t already exist.
                # This prevents errors if the type is created more than once.
                cursor.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_status') THEN
                            CREATE TYPE task_status AS ENUM ('pending', 'ongoing', 'completed');
                        END IF;
                    END
                    $$;
                """)
                
                # Create table using ENUM type
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        description TEXT NOT NULL,
                        status task_status NOT NULL
                    )
                """)
                conn.commit()  # Commit the transaction
                print("Tasks table successfully created")
        except Exception as error:
            print(f"Error upon creating tasks table: {error}")
            conn.rollback()
        finally:
            self.database.close()
    
    def tasks(self):
        conn = self.database_connect()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tasks")
                result = cursor.fetchall()
                for item in result:
                    print(item)
                # print(f'Tasks: {result}')
        except Exception as e:
            logging.critical(f"An error occurred: {e}")
        finally:
            self.database.close()

    def create(self, description, status):
        # Check if description and status are provided
        if not description or not status:
            print("Error: Both description and status are required.")
            return

        # Validate status value
        valid_statuses = {"pending", "ongoing", "completed"}
        if status not in valid_statuses:
            print(f"Error: Invalid status. Must be one of {', '.join(valid_statuses)}.")
            return
        
        conn = self.database_connect()
        
        try:
            with conn.cursor() as cursor:
                # Execute the INSERT command using parameterized queries
                cursor.execute(
                    "INSERT INTO tasks (description, status) VALUES (%s, %s) RETURNING *",
                    (description, status)
                )
                 # Commit the transaction to save changes
                conn.commit()
                
                # Fetch the id of the newly inserted task
                result = cursor.fetchone()
                print(f"Task created successfully with ID: {result[0]} = {result}")
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            self.database.close()

    def find(self, search_keyword):
        conn = self.database_connect()
        # in PostgreSQL, if status is of type ENUM, you can't use LIKE directly on an ENUM type,
        # as it's intended for text values. For ENUM, you need to use an equality check (=) instead of LIKE.
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM tasks 
                    WHERE description LIKE %s
                    OR status = %s
                """
                # Format the search keyword with wildcards for LIKE
                like_pattern = f'%{search_keyword}%'
                cursor.execute(query, (like_pattern, search_keyword))
                result = cursor.fetchall()

                # cursor.execute("SELECT * FROM tasks WHERE description LIKE %s", ('%' + value + '%',))
                for item in result:
                    print(item)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.database.close()

    def find_by_id(self, id):
        if not id:
            print("Error: Id are required.")
            return
        
        if not self.is_exist(id):
            print("Task not found")
            return
        conn = self.database_connect()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
                result = cursor.fetchone()
                if result is not None:
                    print(f'Task with id {id}: {result}')
                else:
                    print("No matched task found")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.database.close()

    def update(self, id, description, status):
         # Check if description,status and id are provided
        if not description or not status or not id:
            print("Error: Id, description and status are required.")
            return

        # Validate status value
        valid_statuses = {"pending", "ongoing", "completed"}
        if status not in valid_statuses:
            print(f"Error: Invalid status. Must be one of {', '.join(valid_statuses)}.")
            return
        
        if not self.is_exist(id):
            print("Task not found")
            return
        
        conn = self.database_connect()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE tasks SET description = %s, status = %s WHERE id = %s RETURNING *", (description, status, id))
                result = cursor.fetchone()
                conn.commit()
                print(f"Task updated successfully with ID: {id} = {result}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.database.close()
    
    def delete(self, id):
         # Check if id provided
        if not id:
            print("Error: Id are required.")
            return

        if not self.is_exist(id):
            print("Task not found")
            return
        
        conn = self.database_connect()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM tasks WHERE id = %s RETURNING *", (id,))
                result = cursor.fetchone()
                conn.commit()
                print(f"Task deleted successfully with ID: {id} Contains =  {result}")
        except Exception as e:
            print(f"An error occurred HEHE: {e}")
        finally:
            self.database.close()
            
    def is_exist(self, id):
         # Check if id provided
        if not id:
            print("Error: Id are required.")
            return

        conn = self.database_connect()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
                return cursor.fetchone()

        except Exception as e:
            print(f"An error occurred IS EXISTS: {e}")
        finally:
            self.database.close()
