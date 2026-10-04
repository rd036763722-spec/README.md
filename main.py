import random
import time

def run_simulation():
    secret_number = random.randint(1, 100)
    print(f"--- התחלת סימולציה: התוכנה בחרה מספר סודי בין 1 ל-100 ---")
    
    attempts = 0
    low = 1
    high = 100
    
    start_time = time.time()
    
    while True:
        attempts += 1
        guess = (low + high) // 2  # חיפוש בינארי
        print(f"ניסיון {attempts}: המחשב מנחש {guess}")
        
        if guess == secret_number:
            print(f"\nהצלחה! המספר הסודי הוא {secret_number}.")
            break
        elif guess < secret_number:
            print("   -> נמוך מדי, מעלה גבול תחתון.")
            low = guess + 1
        else:
            print("   -> גבוה מדי, מוריד גבול עליון.")
            high = guess - 1
            
        time.sleep(0.5) # השהייה קלה בשביל האפקט ביומן ההרצה
        
    duration = round(time.time() - start_time, 2)
    print(f"\n--- סיכום הרצה ---")
    print(f"מספר ניסיונות כולל: {attempts}")
    print(f"זמן ביצוע: {duration} שניות")

if __name__ == "__main__":
    run_simulation()
