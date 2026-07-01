"""
================================================================
                B R A I N B O L T   -   S P A R K   Y O U R   M I N D
                       OOP-Based Quiz Mini-Project
================================================================
Pipeline (10 steps - exactly as requested)
--------------------------------------------------------------
 1  Splash logo + opening music (Pygame)
 2  Register  (name, DOB -> live age, phone, email, password*)
 3  Login     (recursive until correct, case-sensitive password)
 4  WhatsApp OTP via pywhatkit (with terminal-fallback)
 5  Home page - choose: Python / Data Science / Java / Full Stack
 6  Instructions screen + "ALL THE BEST!"
 7  3-2-1 Pygame countdown
 8  15 MCQs (shuffled questions + shuffled options)
 9  Result with emoji + answer review (only for chosen topic)
10  Auto-generate the right certificate (Gold / Silver / Bronze /
    Appreciation) - emailed via Gmail SMTP + summary on WhatsApp.

OOP Concepts demonstrated
--------------------------------------------------------------
 * Class & Object   -> User, Database, Mailer, OTPService, QuizRunner ...
 * Encapsulation    -> User.__name / __password, Database.__conn
 * Abstraction      -> BaseQuiz (ABC) + AuthService facade
 * Inheritance      -> PythonQuiz / DataScienceQuiz / JavaQuiz /
                       FullStackQuiz   extend BaseQuiz
 * Polymorphism     -> Same .topic_key() / .pretty_name() /
                       .motivational_quote() behave differently per class
 * Constructor/Destructor -> Database.__init__ + __del__
================================================================
"""
import os
import sys
import time

from brainbolt.config       import TOPICS, CERT_TIERS, ASSETS_DIR
from brainbolt.database     import Database
from brainbolt.otp_service  import OTPService
from brainbolt.auth         import AuthService
from brainbolt.splash       import show_splash
from brainbolt.countdown    import countdown
from brainbolt.quizzes      import make_quiz
from brainbolt.quiz_runner  import QuizRunner
from brainbolt.certificate  import pick_certificate
from brainbolt.mailer       import Mailer


# ------------------------------------------------------------------
def banner(line, char="="):
    print("\n" + char * 64)
    print(line.center(64))
    print(char * 64)


# ------------------------------------------------------------------
def home_page():
    banner("CHECK YOUR TODAY'S KNOWLEDGE !")
    print("\n  Pick a topic to challenge yourself:\n")
    for k, (_, label) in TOPICS.items():
        print(f"     {k}.  {label}")

    while True:
        choice = input("\n  Your choice (1 / 2 / 3 / 4) : ").strip()
        if choice in TOPICS:
            return TOPICS[choice]            # (key, label)
        print("  Please pick 1, 2, 3 or 4.")


# ------------------------------------------------------------------
def instructions(topic_label):
    banner(f"INSTRUCTIONS - {topic_label.upper()} QUIZ")
    print(f"""
   You have selected  ->  {topic_label}

   * There are 15 MCQ questions.
   * Each correct answer earns 1 point  (max = 15).
   * Certificate tiers:
        >  13  points  ->  GOLD certificate
        11 - 13 points ->  SILVER certificate
         9 - 10 points ->  BRONZE certificate
        <   9  points  ->  APPRECIATION certificate
   * Type A, B, C or D and press Enter for each question.

                    *** ALL THE BEST !! ***
    """)
    input("   Press Enter when you're ready ... ")


# ------------------------------------------------------------------
def show_result_and_review(runner: QuizRunner):
    runner.review_answers()


# ------------------------------------------------------------------
def deliver_certificate(user_row, topic_label, score, total, otp_svc):
    banner("DO YOU WANT TO PRINT YOUR CERTIFICATE ?")
    ch = input("   Type 'yes' to email + WhatsApp it, anything else to skip : ").strip().lower()
    if ch not in {"y", "yes"}:
        print("   Okay - skipping certificate delivery.")
        return

    CertClass = pick_certificate(score, total)
    cert      = CertClass(user_row["name"], topic_label, score, total)
    pdf_path  = cert.generate()
    print(f"\n   {cert.tier} certificate generated at:")
    print(f"      {pdf_path}")

    # email
    mailer = Mailer()
    mailer.send_certificate(
        to_email     = user_row["email"],
        user_name    = user_row["name"],
        topic_label  = topic_label,
        score        = score,
        total        = total,
        tier         = cert.tier,
        pdf_path     = pdf_path,
    )

    # WhatsApp summary too
    wa = user_row["phone"]
    if not wa.startswith("+"):
        wa = "+91" + wa
    otp_svc.send_certificate_message(
        wa_number = wa,
        user_name = user_row["name"],
        topic     = topic_label,
        score     = score,
        total     = total,
        cert_tier = cert.tier,
    )


# ------------------------------------------------------------------
def main():
    # ---- STEP 1 : SPLASH ----
    show_splash(seconds=6)

    banner("Welcome to BrainBolt  -  Spark Your Mind", char="*")
    print("\n   A Python OOP mini-project for PyCharm")
    print("   Powered by Pygame + Pillow + ReportLab + pywhatkit\n")

    # ---- bootstrap ----
    db      = Database()
    otp_svc = OTPService()
    auth    = AuthService(db, otp_svc)

    # ---- STEP 2 : REGISTER ----
    auth.register()

    # ---- STEP 3 : LOGIN ----
    user_row = auth.login()

    # ---- STEP 4 : WHATSAPP OTP ----
    auth.verify_otp(user_row)

    # ---- STEP 5 : HOME PAGE ----
    topic_key, topic_label = home_page()

    # ---- STEP 6 : INSTRUCTIONS ----
    instructions(topic_label)

    # ---- STEP 7 : COUNTDOWN ----
    print("\n   Starting in 3 ... 2 ... 1 ...")
    countdown()

    # ---- STEP 8 : QUIZ ----
    quiz   = make_quiz(topic_key)
    runner = QuizRunner(quiz)
    runner.run()

    # save the attempt in DB (record EVERYTHING, not only top scorers)
    cert_class = pick_certificate(quiz.score, quiz.total())
    db.save_attempt(
        user_name   = user_row["name"],
        topic       = topic_label,
        score       = quiz.score,
        total       = quiz.total(),
        certificate = cert_class.tier,
    )

    # ---- STEP 9 : VALIDATION + ANSWER REVIEW ----
    banner("DO YOU WANT TO VALIDATE YOUR ANSWERS ?")
    ch = input("   Type 'yes' to see all 15 correct answers + explanations : ").strip().lower()
    if ch in {"y", "yes"}:
        show_result_and_review(runner)

    input("\n   Press Enter to continue to certificate delivery ... ")

    # ---- STEP 10 : CERTIFICATE ----
    deliver_certificate(user_row, topic_label,
                        quiz.score, quiz.total(), otp_svc)

    # ---- FAREWELL ----
    banner("THANKS FOR TAKING THIS TEST !", char="*")
    print("\n   Choose to be more knowledgeable than yesterday.  See you soon!\n")


# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n   Exited by user. Bye!\n")
        sys.exit(0)
