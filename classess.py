import datetime


class Operations:
    def __int__(self, date, state, operationamount, description, to):
        self.date = date
        self.state = state
        self.operationamount = operationamount
        self.description = description
        # self.from_ = from_
        self.to = to

    def correction_time(self):
        self.date = self.date.strftime("%d.%m.%Y")
