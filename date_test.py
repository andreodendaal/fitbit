import datetime
from datetime import timedelta

start_date_init = '2015-01-01'
end_date = datetime.date.today()

my_date = datetime.date(year=2015, day=1, month=1)

while my_date < end_date:
    print(my_date)
    my_date = my_date + timedelta(days=1)