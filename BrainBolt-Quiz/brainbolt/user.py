"""
user.py
~~~~~~~
User domain class.  Demonstrates ENCAPSULATION (private fields + properties),
CONSTRUCTOR, and METHOD OVERLOADING via default arguments.
"""
from datetime import datetime, date


class User:
    """Holds registered user data.

    Private attributes (__name, __dob, __password) are accessed only via
    properties - that is encapsulation in Python.
    """

    def __init__(self, name: str, dob: str, phone: str, email: str, password: str):
        self.__name     = name.strip()
        self.__dob      = dob.strip()        # format: DD-MM-YYYY
        self.__phone    = phone.strip()
        self.__email    = email.strip()
        self.__password = password           # CASE-SENSITIVE (stored as-is)

    # ---------- read-only properties ----------
    @property
    def name(self):     return self.__name
    @property
    def dob(self):      return self.__dob
    @property
    def phone(self):    return self.__phone
    @property
    def email(self):    return self.__email
    @property
    def password(self): return self.__password

    @property
    def age(self) -> int:
        """Age computed live from DOB (DD-MM-YYYY)."""
        return User.calc_age(self.__dob)

    # ---------- helpers ----------
    @staticmethod
    def calc_age(dob_str: str) -> int:
        """Static helper - parses DD-MM-YYYY and returns whole-year age."""
        try:
            d = datetime.strptime(dob_str, "%d-%m-%Y").date()
        except ValueError:
            return 0
        today = date.today()
        return today.year - d.year - ((today.month, today.day) < (d.month, d.day))

    def whatsapp_number(self, default_country="+91") -> str:
        """METHOD OVERLOADING (via default arg) - returns +CC<phone>."""
        return self.__phone if self.__phone.startswith("+") else default_country + self.__phone

    def __repr__(self):
        return f"<User {self.__name}  age={self.age}  email={self.__email}>"
