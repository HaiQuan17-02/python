import pyodbc

# Cấu hình kết nối cơ sở dữ liệu
server = 'LAPTOP-7O89H04L'
database = 'football'

def connect_db():
    """Kết nối đến cơ sở dữ liệu."""
    try:
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        return pyodbc.connect(connection_string)
    except pyodbc.Error as e:
        print("Error connecting to database:", e)
        return None

# Chức năng quản lý cầu thủ
def add_player(name, jersey_number, position, goals, matches_played, salary):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Players (PlayerName, JerseyNumber, Position, Goals, MatchesPlayed, Salary) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, jersey_number, position, goals, matches_played, salary))
            conn.commit()
            print("Đã thêm cầu thủ!")
        except pyodbc.Error as e:
            print("Error inserting data:", e)
        finally:
            cursor.close()
            conn.close()

def delete_player(player_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Players WHERE PlayerID = ?", (player_id,))
            conn.commit()
            print("Đã xóa cầu thủ!")
        except pyodbc.Error as e:
            print("Error deleting data:", e)
        finally:
            cursor.close()
            conn.close()


# Hiển thị danh sách cầu thủ, bao gồm lương
def show_players():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Players")
        players = cursor.fetchall()
        cursor.close()
        conn.close()

        if not players:
            print("Danh sách cầu thủ trống!")
        else:
            for player in players:
                print(f"ID: {player[0]}, Tên: {player[1]}, Số áo: {player[2]}, Vị trí: {player[3]}, "
                      f"Số bàn thắng: {player[4]}, Số trận: {player[5]}, Lương: {player[6]:,.2f}")
def search_player(player_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Players WHERE PlayerID = ?", (player_id,))
        player = cursor.fetchone()
        cursor.close()
        conn.close()

        if player:
            print(f"ID: {player[0]}, Tên: {player[1]}, Số áo: {player[2]}, Vị trí: {player[3]}, "
                  f"Số bàn thắng: {player[4]}, Số trận: {player[5]}")
        else:
            print("Không tìm thấy cầu thủ!")

# Cập nhật thông tin cầu thủ, bao gồm lương
def update_player(player_id, jersey_number=None, goals=None, salary=None):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            if jersey_number is not None:
                cursor.execute("UPDATE Players SET JerseyNumber = ? WHERE PlayerID = ?", (jersey_number, player_id))
            if goals is not None:
                cursor.execute("UPDATE Players SET Goals = ? WHERE PlayerID = ?", (goals, player_id))
            if salary is not None:
                cursor.execute("UPDATE Players SET Salary = ? WHERE PlayerID = ?", (salary, player_id))
            conn.commit()
            print("Thông tin cầu thủ đã được cập nhật!")
        except pyodbc.Error as e:
            print("Error updating data:", e)
        finally:
            cursor.close()
            conn.close()

# Chức năng quản lý trận đấu
def add_match(date, opponent, result):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO Matches (MatchDate, Opponent, Result) 
                              VALUES (?, ?, ?)''', (date, opponent, result))
            conn.commit()
            print("Đã thêm trận đấu!")
        except pyodbc.Error as e:
            print("Error inserting match data:", e)
        finally:
            cursor.close()
            conn.close()

def show_matches():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Matches")
        matches = cursor.fetchall()
        cursor.close()
        conn.close()
        if not matches:
            print("Danh sách trận đấu trống!")
        else:
            for match in matches:
                print(f"ID: {match[0]}, Ngày: {match[1]}, Đối thủ: {match[2]}, Kết quả: {match[3]}")

def update_match(match_id, result):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Matches SET Result = ? WHERE MatchID = ?", (result, match_id))
            conn.commit()
            print("Thông tin trận đấu đã được cập nhật!")
        except pyodbc.Error as e:
            print("Error updating match data:", e)
        finally:
            cursor.close()
            conn.close()

# Chức năng quản lý ban huấn luyện
def add_coach(phone_number, name, experience, position, salary):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Coaches (PhoneNumber, name, Experience, Position, Salary) 
                VALUES (?, ?, ?, ?, ?)
            ''', (phone_number, name, experience, position, salary))
            conn.commit()
            print("Đã thêm ban huấn luyện!")
        except pyodbc.Error as e:
            print("Error inserting coach data:", e)
        finally:
            cursor.close()
            conn.close()

# Hiển thị danh sách huấn luyện viên, bao gồm lương
def show_coaches():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Coaches")
        coaches = cursor.fetchall()
        cursor.close()
        conn.close()

        if not coaches:
            print("Danh sách ban huấn luyện trống!")
        else:
            for coach in coaches:
                print(f"ID: {coach[0]}, Tên: {coach[1]}, Kinh nghiệm: {coach[2]}, Chức vụ: {coach[3]}, Lương: {coach[4]:,.2f}")

# Cập nhật thông tin huấn luyện viên, bao gồm lương
def update_coach(coach_id, salary=None):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            if salary is not None:
                cursor.execute("UPDATE Coaches SET Salary = ? WHERE CoachID = ?", (salary, coach_id))
            conn.commit()
            print("Thông tin huấn luyện viên đã được cập nhật!")
        except pyodbc.Error as e:
            print("Error updating coach data:", e)
        finally:
            cursor.close()
            conn.close()

# Các menu phụ cho từng phần quản lý
def manage_players():
    while True:
        print("\n--- Quản lý cầu thủ ---")
        print("1. Thêm cầu thủ")
        print("2. Xóa cầu thủ")
        print("3. Hiển thị danh sách cầu thủ")
        print("4. Tìm cầu thủ")
        print("5. Cập nhật thông tin cầu thủ")
        print("0. Quay lại menu chính")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            name = input("Tên cầu thủ: ")
            jersey_number = int(input("Số áo: "))
            position = input("Vị trí: ")
            goals = int(input("Số bàn thắng: "))
            matches_played = int(input("Số trận đấu: "))
            salary = float(input("Lương: "))
            add_player(name, jersey_number, position, goals, matches_played, salary)

        elif choice == '2':
            player_id = int(input("Nhập ID cầu thủ cần xóa: "))
            delete_player(player_id)

        elif choice == '3':
            show_players()

        elif choice == '4':
            player_id = int(input("Nhập ID cầu thủ cần tìm: "))
            search_player(player_id)

        elif choice == '5':
            player_id = int(input("Nhập ID cầu thủ cần cập nhật: "))
            jersey_number = input("Nhập số áo mới (nhấn Enter để giữ nguyên): ")
            goals = input("Nhập số bàn thắng mới (nhấn Enter để giữ nguyên): ")
            salary = input("Nhập lương mới (nhấn Enter để giữ nguyên): ")

            jersey_number = int(jersey_number) if jersey_number else None
            goals = int(goals) if goals else None
            salary = float(salary) if salary else None
            
            update_player(player_id, jersey_number, goals, salary)

        elif choice == '0':
            break

        else:
            print("Lựa chọn không hợp lệ!")

def manage_matches():
    while True:
        print("\n--- Quản lý trận đấu ---")
        print("1. Thêm trận đấu")
        print("2. Hiển thị danh sách trận đấu")
        print("3. Cập nhật kết quả trận đấu")
        print("0. Quay lại menu chính")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            date = input("Nhập ngày trận đấu (YYYY-MM-DD): ")
            opponent = input("Nhập tên đối thủ: ")
            result = input("Nhập kết quả trận đấu: ")
            add_match(date, opponent, result)

        elif choice == '2':
            show_matches()

        elif choice == '3':
            match_id = int(input("Nhập ID trận đấu cần cập nhật: "))
            result = input("Nhập kết quả mới: ")
            update_match(match_id, result)

        elif choice == '0':
            break

        else:
            print("Lựa chọn không hợp lệ!")

def manage_coaches():
    while True:
        print("\n--- Quản lý ban huấn luyện ---")
        print("1. Thêm ban huấn luyện")
        print("2. Hiển thị danh sách ban huấn luyện")
        print("3. Cập nhật lương ban huấn luyện")
        print("0. Quay lại menu chính")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            phone_number = input("Nhập số điện thoại ban huấn luyện: ")
            name = input("Nhập tên ban huấn luyện: ")
            experience = int(input("Nhập kinh nghiệm: "))
            position = input("Nhập chức vụ: ")
            salary = float(input("Nhập lương: "))
            add_coach(phone_number, name, experience, position, salary)

        elif choice == '2':
            show_coaches()

        elif choice == '3':
            coach_id = int(input("Nhập ID ban huấn luyện cần cập nhật: "))
            salary = float(input("Nhập lương mới: "))
            update_coach(coach_id, salary)

        elif choice == '0':
            break

        else:
            print("Lựa chọn không hợp lệ!")

# Menu chính
if __name__ == "__main__":
    while True:
        print("\n--- Quản lý bóng đá ---")
        print("1. Quản lý cầu thủ")
        print("2. Quản lý trận đấu")
        print("3. Quản lý ban huấn luyện")
        print("0. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            manage_players()
        elif choice == '2':
            manage_matches()
        elif choice == '3':
            manage_coaches()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ!")
