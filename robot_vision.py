"""
KRSBI Robot Vision System
Program deteksi bola dan robot menggunakan OpenCV dan HSV color tracking
"""

import cv2
import numpy as np
import serial
import socket
import threading


class RobotVision:
    """Class untuk sistem vision robot KRSBI"""
    
    def __init__(self, serial_port='COM11', baudrate=115200, camera_index=0):
        """
        Inisialisasi sistem vision
        
        Args:
            serial_port: Port serial Arduino (default: COM11)
            baudrate: Baudrate komunikasi serial (default: 115200)
            camera_index: Index kamera (default: 0)
        """
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.camera_index = camera_index
        
        # Konfigurasi kamera
        self.frame_width = 960
        self.frame_height = 540
        
        # Setup serial connection (jika tersedia)
        try:
            self.serial_arduino = serial.Serial(serial_port, baudrate, timeout=1)
            self.serial_enabled = True
            print(f"Serial connected to {serial_port}")
        except:
            self.serial_arduino = None
            self.serial_enabled = False
            print("Serial connection failed. Running in demo mode.")
        
        # Setup socket untuk komunikasi
        self.socket_enabled = False
        self.setup_socket()
        
    def setup_socket(self):
        """Setup socket untuk komunikasi dengan base station"""
        try:
            self.s = socket.socket()
            self.host = socket.gethostname()
            self.port = 1234
            self.s.bind((self.host, self.port))
            self.s.listen(1)
            self.socket_enabled = True
            print(f"Socket listening on {self.host}:{self.port}")
        except:
            self.socket_enabled = False
            print("Socket setup failed.")
    
    @staticmethod
    def callback(value):
        """Callback untuk trackbar"""
        pass
    
    def send_serial_data(self, data):
        """Kirim data ke Arduino via serial"""
        if self.serial_enabled and self.serial_arduino:
            try:
                self.serial_arduino.write(data.encode())
            except:
                pass
    
    def calculate_position_grid(self, x, x_ranges):
        """
        Konversi posisi X ke grid position
        
        Args:
            x: Koordinat x
            x_ranges: List tuple (max_value, grid_code)
        
        Returns:
            Grid code
        """
        for max_val, code in x_ranges:
            if x < max_val:
                return code
        return x_ranges[-1][1]
    
    def main_loop(self):
        """Loop utama untuk deteksi objek"""
        # Setup kamera
        camera = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        
        # Buat windows dan trackbars untuk kalibrasi
        cv2.namedWindow("ROBOT", 0)
        cv2.createTrackbar("L_H", "ROBOT", 163, 255, self.callback)
        cv2.createTrackbar("U_H", "ROBOT", 189, 255, self.callback)
        cv2.createTrackbar("L_S", "ROBOT", 213, 255, self.callback)
        cv2.createTrackbar("U_S", "ROBOT", 255, 255, self.callback)
        cv2.createTrackbar("L_V", "ROBOT", 80, 255, self.callback)
        cv2.createTrackbar("U_V", "ROBOT", 255, 255, self.callback)
        
        cv2.namedWindow("BOLA", 0)
        cv2.createTrackbar("L_H", "BOLA", 0, 255, self.callback)
        cv2.createTrackbar("U_H", "BOLA", 35, 255, self.callback)
        cv2.createTrackbar("L_S", "BOLA", 199, 255, self.callback)
        cv2.createTrackbar("U_S", "BOLA", 255, 255, self.callback)
        cv2.createTrackbar("L_V", "BOLA", 220, 255, self.callback)
        cv2.createTrackbar("U_V", "BOLA", 255, 255, self.callback)
        
        # X position ranges (max_value, code)
        x_ranges = [
            (89, 201), (123, 202), (157, 203), (191, 204), (225, 205),
            (259, 206), (293, 207), (327, 208), (361, 209), (395, 210),
            (429, 211), (463, 212), (497, 213), (531, 214), (565, 215),
            (599, 216), (633, 217), (667, 218), (701, 219), (735, 220),
            (769, 221), (803, 222), (837, 223), (871, 224), (905, 225)
        ]
        
        # Y position ranges (max_value, code)
        y_ranges = [
            (33, 201), (66, 202), (99, 203), (132, 204), (165, 205),
            (198, 206), (231, 207), (264, 208), (297, 209), (330, 210),
            (363, 211), (396, 212), (429, 213), (462, 214), (495, 215),
            (528, 216)
        ]
        
        print("Program berjalan. Tekan 'q' untuk keluar.")
        
        while True:
            ret, image = camera.read()
            if not ret:
                print("Gagal membaca frame dari kamera")
                break
            
            # Konversi ke HSV
            frame_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Get trackbar values untuk BOLA (orange)
            l_h = cv2.getTrackbarPos("L_H", "BOLA")
            l_s = cv2.getTrackbarPos("L_S", "BOLA")
            l_v = cv2.getTrackbarPos("L_V", "BOLA")
            u_h = cv2.getTrackbarPos("U_H", "BOLA")
            u_s = cv2.getTrackbarPos("U_S", "BOLA")
            u_v = cv2.getTrackbarPos("U_V", "BOLA")
            
            # Get trackbar values untuk ROBOT (purple)
            l_h2 = cv2.getTrackbarPos("L_H", "ROBOT")
            l_s2 = cv2.getTrackbarPos("L_S", "ROBOT")
            l_v2 = cv2.getTrackbarPos("L_V", "ROBOT")
            u_h2 = cv2.getTrackbarPos("U_H", "ROBOT")
            u_s2 = cv2.getTrackbarPos("U_S", "ROBOT")
            u_v2 = cv2.getTrackbarPos("U_V", "ROBOT")
            
            # Threshold untuk deteksi warna
            thresh_ball = cv2.inRange(frame_hsv, (l_h, l_s, l_v), (u_h, u_s, u_v))
            thresh_robot = cv2.inRange(frame_hsv, (l_h2, l_s2, l_v2), (u_h2, u_s2, u_v2))
            
            # Morphological operations untuk noise reduction
            kernel = np.ones((5, 5), np.uint8)
            mask_ball = cv2.morphologyEx(thresh_ball, cv2.MORPH_OPEN, kernel)
            mask_ball = cv2.morphologyEx(mask_ball, cv2.MORPH_CLOSE, kernel)
            
            mask_robot = cv2.morphologyEx(thresh_robot, cv2.MORPH_OPEN, kernel)
            mask_robot = cv2.morphologyEx(mask_robot, cv2.MORPH_CLOSE, kernel)
            
            # Deteksi BOLA
            self.detect_ball(image, mask_ball, x_ranges, y_ranges)
            
            # Deteksi ROBOT TEMAN
            self.detect_robot(image, mask_robot, x_ranges)
            
            # Tampilkan hasil
            cv2.imshow("Original", image)
            cv2.imshow("TampilanBola", thresh_ball)
            cv2.imshow("TampilanRobot", thresh_robot)
            
            # Exit jika 'q' ditekan
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        camera.release()
        cv2.destroyAllWindows()
    
    def detect_ball(self, image, mask, x_ranges, y_ranges):
        """Deteksi posisi bola"""
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        if len(contours) > 0:
            # Ambil contour terbesar
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
                if radius > 10:  # Minimum radius threshold
                    # Draw circle dan info
                    cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(image, center, 3, (0, 0, 255), -1)
                    cv2.putText(image, "Bola", (center[0]+10, center[1]), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(image, f"({center[0]},{center[1]})", 
                              (center[0]+10, center[1]+15), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Kirim posisi X
                    x_code = self.calculate_position_grid(x, x_ranges)
                    self.send_serial_data(f"X{x_code}")
                    
                    # Kirim posisi Y
                    y_code = self.calculate_position_grid(y, y_ranges)
                    self.send_serial_data(f"Y{y_code}")
                    return
        
        # Jika tidak ada bola terdeteksi
        self.send_serial_data("X0")
        self.send_serial_data("Y0")
    
    def detect_robot(self, image, mask, x_ranges):
        """Deteksi posisi robot teman"""
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        if len(contours) > 0:
            # Ambil contour terbesar
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
                if radius > 10:  # Minimum radius threshold
                    # Draw circle dan info
                    cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(image, center, 3, (0, 0, 255), -1)
                    cv2.putText(image, "Robot", (center[0]+10, center[1]), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(image, f"({center[0]},{center[1]})", 
                              (center[0]+10, center[1]+15), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Kirim posisi robot
                    x_code = self.calculate_position_grid(x, x_ranges)
                    self.send_serial_data(f"W{x_code}")
                    return
        
        # Jika tidak ada robot terdeteksi
        self.send_serial_data("W0")
    
    def communication_loop(self):
        """Loop untuk komunikasi dengan base station"""
        if not self.socket_enabled:
            print("Socket tidak aktif, komunikasi dinonaktifkan")
            return
        
        print('Menunggu koneksi dari base station...')
        conn, addr = self.s.accept()
        print(f'Koneksi diterima dari {addr}')
        
        # Mapping command ke kode
        command_map = {
            "go3000,4100,0": (4, "Kick Off 1"),
            "go7400,3000,0": (5, "Kick Off 2"),
            "go9000,0,135": (6, "Corner A"),
            "go9000,6000,225": (9, "Corner B"),
            "j": (7, "Jalan"),
            "k": (8, "Stop")
        }
        
        while True:
            try:
                pesan = conn.recv(1024)
                if not pesan:
                    break
                
                data = pesan.decode('utf-8')
                print(f'Menerima pesan: {data}')
                
                if data in command_map:
                    code, action = command_map[data]
                    print(action)
                    for _ in range(100):
                        self.send_serial_data(f"Z{code}")
                        
            except Exception as e:
                print(f"Error dalam komunikasi: {e}")
                break
        
        conn.close()


def main():
    """Fungsi utama"""
    # Konfigurasi - sesuaikan dengan setup Anda
    SERIAL_PORT = 'COM11'  # Ganti sesuai port Arduino Anda
    BAUDRATE = 115200
    CAMERA_INDEX = 0
    
    # Buat instance RobotVision
    robot = RobotVision(
        serial_port=SERIAL_PORT,
        baudrate=BAUDRATE,
        camera_index=CAMERA_INDEX
    )
    
    # Buat dan jalankan thread
    t1 = threading.Thread(target=robot.main_loop)
    t2 = threading.Thread(target=robot.communication_loop)
    
    t1.start()
    t2.start()
    
    # Tunggu thread selesai
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
