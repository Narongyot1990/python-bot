import cv2

# ใส่ URL ของ IP Camera หรือ index ของกล้อง (สำหรับกล้อง USB)
# ตัวอย่าง URL: 'rtsp://username:password@camera_ip_address:port/unicast/c<channel number>/s<stream type>'
camera_url = 'rtsp://admin:kowa1234@@192.168.1.100:554/unicast/c4/s0'
# ถ้าเป็นกล้อง USB ใช้ index
# camera_url = 0

# เปิดการเชื่อมต่อกับกล้อง
cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("ไม่สามารถเปิดการเชื่อมต่อกับกล้องได้")
    exit()

while True:
    # อ่านเฟรมจากกล้อง
    ret, frame = cap.read()

    if not ret:
        print("ไม่สามารถอ่านเฟรมจากกล้องได้")
        break

    # แสดงผลเฟรม
    cv2.imshow('Camera Feed', frame)

    # กด 'q' เพื่อออกจากการแสดงผล
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดการเชื่อมต่อกับกล้องและหน้าต่างแสดงผล
cap.release()
cv2.destroyAllWindows()