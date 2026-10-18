import sys
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import CardConnectionException, NoCardException

def run_nfc_test():
    # 1. جلب قائمة القارئات المتصلة
    all_readers = readers()
    
    if not all_readers:
        print("❌ Error: No card readers found! Check USB connection.")
        return

    reader = all_readers[0]
    print(f"🔍 Using Reader: {reader}")
    print("⏳ Waiting for card... (Place your NTAG215 on the reader)")

    try:
        # 2. محاولة الاتصال بالكارطة
        connection = reader.createConnection()
        connection.connect()
        
        # جلب الـ ATR (Answer To Reset)
        atr = toHexString(connection.getATR())
        print(f"✅ Card Detected!")
        print(f"🆔 ATR: {atr}")

        # 3. أمر APDU لقراءة الـ UID (رقم الكارطة الفريد)
        # هذا الأمر يشتغل مع أغلب قارئات NFC لبطاقات MIFARE/NTAG
        GET_UID_COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        
        data, sw1, sw2 = connection.transmit(GET_UID_COMMAND)
        
        # التأكد من نجاح العملية (Status Word 0x90 0x00)
        if sw1 == 0x90 and sw2 == 0x00:
            uid = toHexString(data)
            print(f"✨ Success! Card UID: {uid}")
            print("-" * 30)
            print(f"This card is ready for your PFE project!")
        else:
            print(f"⚠️ Card found but couldn't read UID. Status: {hex(sw1)}, {hex(sw2)}")

    except NoCardException:
        print("❌ Error: No card on reader. Please place the card and try again.")
    except CardConnectionException as e:
        print(f"❌ Connection Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    run_nfc_test()