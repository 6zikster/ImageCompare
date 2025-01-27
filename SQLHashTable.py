import json
import sqlite3
import Levenshtein
import count_dif_symbols

class HashTable:
    def __init__(self, db_name="hash_table.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        """Create the table if it does not exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS HashTable (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Hash TEXT NOT NULL,
                    NearestNeighbors TEXT DEFAULT NULL
                )
                """
            )

    def add_element(self, name, hash_value):
        """Add a new element to the table."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO HashTable (Name, Hash) VALUES (?, ?)", (name, hash_value))
            conn.commit()
            new_id = cursor.lastrowid
            self.update_neighbors()
            return new_id
        
    def edit_element(self, element_id, new_name=None, new_hash=None):
        """Edit an element's name and/or hash."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Check if the element exists
            cursor.execute("SELECT ID, Hash FROM HashTable WHERE ID = ?", (element_id,))
            result = cursor.fetchone()
            if result is None:
                print(f"No element found with ID {element_id}.")
                return False

            old_hash = result[1]
            updates = []
            params = []

            # Update Name if provided
            if new_name is not None:
                updates.append("Name = ?")
                params.append(new_name)

            # Update Hash if provided
            if new_hash is not None:
                updates.append("Hash = ?")
                params.append(new_hash)

            # If no changes are specified, return early
            if not updates:
                print("No updates specified.")
                return False

            params.append(element_id)
            update_query = f"UPDATE HashTable SET {', '.join(updates)} WHERE ID = ?"
            cursor.execute(update_query, params)
            conn.commit()
            print(f"Element with ID {element_id} updated successfully.")

            # If the Hash was updated, recalculate neighbors
            if new_hash is not None and new_hash != old_hash:
                self.update_neighbors()
            return True



    def get_all_elements(self):
        """Retrieve all elements from the table."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, Name, Hash, NearestNeighbors FROM HashTable")
            return cursor.fetchall()

    def get_element(self, element_id):
        """Retrieve a specific element by its ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, Name, Hash, NearestNeighbors FROM HashTable WHERE ID = ?", (element_id,))
            return cursor.fetchone()
    def delete_element(self, element_id):
        """Delete an element by its ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Check if the element exists
            cursor.execute("SELECT ID FROM HashTable WHERE ID = ?", (element_id,))
            if cursor.fetchone() is None:
                print(f"No element found with ID {element_id}.")
                return False

            # Delete the element
            cursor.execute("DELETE FROM HashTable WHERE ID = ?", (element_id,))
            conn.commit()
            print(f"Element with ID {element_id} deleted successfully.")

            # Update neighbors for all remaining elements
            self.update_neighbors()
            return True



    def update_neighbors(self):
        """Update the nearest neighbors for the given element."""
        elements = self.get_all_elements()  # Fetch all elements from the database

        # Iterate over each element to calculate nearest neighbors
        for upd in elements:
            differences = []

            # Calculate the difference for all other elements
            for element in elements:
                if upd[0] != element[0]:  # Exclude self
                    diff = count_dif_symbols.Count.count_different_symbols(upd[2], element[2])
                    differences.append((element[0], diff))

            # Sort by difference
            differences.sort(key=lambda x: x[1])

            # Take the two closest neighbors
            nearest_neighbors = [differences[0][0], differences[1][0]] if len(differences) > 1 else []

            # Convert to a string for storage (e.g., comma-separated values)
            nearest_neighbors_str = ",".join(map(str, nearest_neighbors))

            # Update the database
            self.execute_query(
                "UPDATE HashTable SET NearestNeighbors = ? WHERE ID = ?",
                (nearest_neighbors_str, upd[0])
            )
    def execute_query(self, query, params=None):
        """Execute a query against the database."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

