"""
otp_service.py
~~~~~~~~~~~~~~
Sends an OTP message to a user's WhatsApp using pywhatkit.
If WhatsApp Web isn't available, falls back to printing the OTP locally so
the pipeline never stalls.
"""
import time


class OTPService:
    """Thin wrapper around pywhatkit.sendwhatmsg_instantly."""

    def send_otp(self, wa_number: str, user_name: str, otp: int) -> bool:
        msg = (
            f"BrainBolt - Spark Your Mind\n"
            f"Hello {user_name}, your login OTP is : {otp}\n"
            f"Please enter it in the terminal to continue."
        )
        print(f"\n   Sending OTP to WhatsApp {wa_number} ...")

        try:
            import pywhatkit as pk
            pk.sendwhatmsg_instantly(wa_number, msg, wait_time=15, tab_close=True)
            time.sleep(6)
            try:
                import pyautogui as pg
                pg.click()
            except Exception:
                pass
            print("   OTP sent via WhatsApp.")
            return True
        except Exception as e:
            # Graceful fallback so the program never hangs
            print(f"   (WhatsApp send failed: {e})")
            print(f"   FALLBACK >>>  YOUR OTP IS :  {otp}  <<<")
            return False

    # ----- Used to send the certificate as a WhatsApp message too -----
    def send_certificate_message(self, wa_number: str, user_name: str,
                                 topic: str, score: int, total: int,
                                 cert_tier: str) -> bool:
        msg = (
            f"BrainBolt - Certificate Issued\n"
            f"Name   : {user_name}\n"
            f"Topic  : {topic}\n"
            f"Score  : {score} / {total}\n"
            f"Tier   : {cert_tier} certificate\n"
            f"Thanks for taking the quiz!"
        )
        try:
            import pywhatkit as pk
            pk.sendwhatmsg_instantly(wa_number, msg, wait_time=15, tab_close=True)
            time.sleep(6)
            try:
                import pyautogui as pg
                pg.click()
            except Exception:
                pass
            print("   Certificate summary sent on WhatsApp.")
            return True
        except Exception as e:
            print(f"   (WhatsApp certificate send failed: {e})")
            return False
