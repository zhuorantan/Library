# Library
### A library management system built with Flask, SQLAlchemy and Bootstrap

# Run
```shell
python main.py
```

To populate example data, uncomment the following line in `main.py`
```python
populate_data()
```

# Gmail
To enable the email notification via Gmail API, follow this [instruction](https://developers.google.com/gmail/api/quickstart/python) and uncomment the following two lines in `main.py`
```python
...
from gmail import send_email

...
send_email(reservation.reader.email, '您预约的书《%s》可借了' % book.cip.book_name, message)
...
```

# [License](LICENSE)
