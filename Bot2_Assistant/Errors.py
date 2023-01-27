class Error:
    def __init__(self, name: str, des: str):
        self.description = des
        self.name = name

    def get_description(self) -> str:
        return self.description

    def get_name(self) -> str:
        return self.name

    def error_des(self) -> str:
        return f"Error {self.name} -> {self.description}"
