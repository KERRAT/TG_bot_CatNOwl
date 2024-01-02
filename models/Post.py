class Post:
    def __init__(self, selected_date, selected_time=None, title=None, text=None, footer=None):
        self.selected_date = selected_date
        self.selected_time = selected_time
        self.title = title
        self.text = text
        self.footer = footer
