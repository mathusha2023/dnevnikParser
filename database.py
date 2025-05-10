import json
import config
import parser.all_marks_parser


class Database:
    def __init__(self, fp):
        self.fp = fp

    def get_data(self):
        with open(self.fp) as file:
            data = json.load(file)
        return data

    def write_data(self, data):
        with open(self.fp, "w") as file:
            json.dump(data, file)

    def add_user_if_not_exists(self, user_id, user_name):
        data = self.get_data()
        if data.get(str(user_id), None) is None:
            data[user_id] = {"name": user_name}
            self.write_data(data)

    def is_logged_in(self, user_id):
        data = self.get_data()
        user = data[str(user_id)]
        cookies = user.get("cookies", None)
        return cookies is not None

    def write_cookies(self, user_id, cookies):
        data = self.get_data()
        user = data[str(user_id)]
        user["cookies"] = cookies
        self.write_data(data)

    def logout(self, user_id):
        data = self.get_data()
        user = data[str(user_id)]
        if user.get("cookies", None):
            del user["cookies"]
            self.write_data(data)

    def get_all_marks(self, user_id):
        data = self.get_data()
        user = data[str(user_id)]
        cookies = user["cookies"]
        marks = parser.all_marks_parser.parse_all_marks(cookies)
        return marks



database = Database(config.DATABASE_FILE)
