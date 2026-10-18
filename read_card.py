from smartcard.System import readers
from smartcard.util import toHexString
import time

def read_card_data():
    print("--- 🔍 محاولة استخراج بيانات الكارت ---")
    try:
        r = readers()
        if not r:
            print("❌ لم يتم العثور على قارئ.")
            return

        reader = r[0]
        print(f"📡 القارئ: {reader}")
        
        connection = reader.createConnection()
        connection.connect()

        # 1. الحصول على الـ ATR (هوية الكارت)
        atr = toHexString(connection.getATR())
        print(f"✅ تم الاتصال!")
        print(f"🆔 ATR (نوع الكارت): {atr}")

        # 2. محاولة قراءة الاسم أو البيانات (بواسطة أمر APDU عام)
        # ملاحظة: كل كارت عندها أوامر خاصة (APDU)
        # هاد الأمر كيحاول يقرأ الـ Serial Number (UID) إيلا كانت الكارت كدعمو
        try:
            # أمر Get Data (للكارطات بحال Mifare أو JavaCards)
            COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] 
            data, sw1, sw2 = connection.transmit(COMMAND)
            
            if sw1 == 0x90:
                print(f"📊 بيانات UID المستخرجة: {toHexString(data)}")
            else:
                print(f"⚠️ الكارت متصلة ولكنها محمية أو تحتاج أوامر خاصة (SW: {hex(sw1)} {hex(sw2)})")
        except:
            print("⚠️ لا يمكن قراءة البيانات الداخلية بدون 'مفتاح الوصول' (Key).")

    except Exception as e:
        if "0x80100066" in str(e):
            print("❌ خطأ: الكارت لا تستجيب (تأكد من وضعية الكارت أو جرب CIN).")
        else:
            print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    read_card_data()