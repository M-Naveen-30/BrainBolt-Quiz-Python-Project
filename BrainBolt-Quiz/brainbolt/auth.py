"""
auth.py
~~~~~~~
Registration + recursive login + WhatsApp-OTP verification.
Demonstrates ABSTRACTION - hides DB & OTP details behind clean methods.
"""
import re
import random
import time

from .user import User
from .database import Database
from .otp_service import OTPService


class AuthService:
    """High-level facade for registration and login."""

    def __init__(self, db: Database, otp: OTPService):
        self._db  = db
        self._otp = otp

    # ===========================================================
    #   REGISTRATION
    # ===========================================================
    def register(self) -> User:
        print("\n" + "=" * 60)
        print(" " * 18 + "  STEP 1 :  REGISTER")
        print("=" * 60)

        while True:
            name = input(" Full Name              : ").strip()
            if not name:
                print("   Name cannot be empty.")
                continue
            if self._db.user_exists(name):
                print(f"   '{name}' is already registered. Please use another name.")
                continue
            break

        # DOB + live age
        while True:
            dob = input(" Date of Birth (DD-MM-YYYY) : ").strip()
            age = User.calc_age(dob)
            if age <= 0 or age > 120:
                print("   Invalid date.  Please use DD-MM-YYYY (e.g. 14-08-2003).")
                continue
            print(f"   --> You are {age} years old.")
            break

        # Phone (10 digit, can have +cc)
        while True:
            phone = input(" Phone Number (10 digit) : ").strip()
            if re.fullmatch(r"\+?\d{10,13}", phone):
                break
            print("   Invalid phone. Digits only (optional + and country code).")

        # Email
        while True:
            email = input(" Email Address          : ").strip()
            if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                break
            print("   Invalid email.  Please re-enter.")

        # Password (case sensitive)
        while True:
            password = input(" Create Password (case-sensitive) : ")
            if len(password) >= 4:
                break
            print("   Password must be at least 4 characters.")

        # save
        user = User(name, dob, phone, email, password)
        self._db.add_user(name, dob, user.age, phone, email, password)
        print("\n   Registration successful!  Welcome,", name, "\n")
        return user

    # ===========================================================
    #   LOGIN  (recursive)
    # ===========================================================
    def login(self) -> dict:
        print("\n" + "=" * 60)
        print(" " * 19 + " STEP 2 :  LOGIN")
        print("=" * 60)
        return self._do_login()

    def _do_login(self):
        name = input(" User Name              : ").strip()
        if not self._db.user_exists(name):
            print("   No such user.  Try again.")
            return self._do_login()

        password = input(" Password (case-sensitive) : ")
        if not self._db.verify_password(name, password):
            print("   Wrong password.  Try again.")
            return self._do_login()

        print("\n   LOGIN SUCCESSFUL.  Welcome back,", name, "\n")
        return self._db.get_user(name)

    # ===========================================================
    #   OTP  (WhatsApp)
    # ===========================================================
    def verify_otp(self, user_row: dict):
        print("\n" + "=" * 60)
        print(" " * 19 + " STEP 3 :  OTP CHECK")
        print("=" * 60)

        otp = random.randint(1000, 9999)
        target = user_row["phone"]
        if not target.startswith("+"):
            target = "+91" + target

        self._otp.send_otp(target, user_row["name"], otp)
        time.sleep(1)
        self._recursive_otp_check(otp)

    def _recursive_otp_check(self, otp: int):
        entered = input(" Enter the OTP you received : ").strip()
        if entered == str(otp):
            print("\n   OTP VERIFIED.  Identity confirmed!\n")
        else:
            print("   Invalid OTP. Try again.")
            self._recursive_otp_check(otp)
