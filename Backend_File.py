
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QPalette, QBrush, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QMessageBox

class MAINCODEPMT(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("Images/new.png"))
        self.setWindowTitle("PMT CONTROL 1.0.5 ")
        self.setFixedSize(1234, 794)
        self.voltage = 0.0

        self.is_running = False
        self.rx_running = False
        self.is_running = False  # Tracks Start/Stop
        self.is_connected = False  # Tracks Connect/Disconnect
        self.device_connected = False
        self.set_background("Images/GUI.png")
        self.ser = self.connect_first_available_port()
        if self.ser and self.ser.is_open:
            pass



    def connect_first_available_port(self, baudrate=9600, timeout=1):
        try:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                try:
                    ser = serial.Serial(port.device, baudrate=baudrate, timeout=timeout)
                    if ser.is_open:
                        print(f"Connected to {port.device}")
                        return ser
                except serial.SerialException:
                    continue
            self.show_popup()
            return None
        except:
            pass


    def show_popup(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("USB device not detected")
        msg.setText("• Connect PMT device\n"
        "• Check USB cable\n")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    QApplication.quit()


    def start_rx_thread(self):
        try:
            if self.rx_running:
                return
            self.rx_running = True
            def rx_loop():
                while self.rx_running:
                    try:
                        if self.ser and self.ser.is_open and self.ser.in_waiting:
                            data = self.ser.readline().decode(errors="ignore").strip()
                            if data:
                                QtCore.QMetaObject.invokeMethod(self, "handle_rx_data", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, data))
                    except Exception as e:
                        print("RX error:", e)

            self.rx_thread = QtCore.QThread()
            self.rx_thread.run = rx_loop
            self.rx_thread.start()
        except:
            pass

    def connect_device(self):
        try:

            if not self.ser or not self.ser.is_open:
                return
            # 🔹 TX FIRST
            self.send_cmd("CONNECT")
            # 🔹 THEN start RX
            self.start_rx_thread()
        except:
            pass



    @QtCore.pyqtSlot(str)
    def handle_rx_data(self, data):
        print("RX:", data)
        # 🔹 Handshake
        if data == "CONNECTED":
            self.device_connected = True
            print("MCU connected successfully")

        # 🔹 Continuous data only AFTER connect
        elif self.device_connected and "," in data:
            try:
                tia, hv = data.split(",")

                if self.voltage == 0.0:
                    pass
                else:
                    self.label_pmt.setText(f"{float(tia):.1f} V")
                    self.label_HV_l.setText(f"{float(hv):.1f} V")
            except ValueError:
                pass


    def send_cmd(self, cmd: str):
        try:

            if self.ser and self.ser.is_open:
                self.ser.write((cmd + "\n").encode())
                print("TX:", cmd)
        except:
            pass


###### Control Time Constant
    def send_S1(self):
        self.send_cmd("1S")
        self.btn_a.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_b.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_c.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_d.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_e.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_f.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")

    def send_S2(self):
        self.send_cmd("2S")
        self.btn_a.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_b.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_c.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_d.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_e.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_f.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")

    def send_S3(self):
        self.send_cmd("3S")
        self.btn_a.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_b.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_c.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_d.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_e.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_f.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")

    def send_S4(self):
        self.send_cmd("4S")
        self.btn_a.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_b.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_c.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_d.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_e.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_f.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")

    def send_S5(self):
        self.send_cmd("5S")
        self.btn_a.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_b.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_c.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_d.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_e.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_f.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")


    def send_S6(self):
        self.send_cmd("6S")
        self.btn_a.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_b.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_c.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_d.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_e.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_f.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")


###### Control Gain
    def send_b_x1(self):
        self.send_cmd("1X")
        self.btn_aa.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_bb.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_cc.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_dd.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")

    def send_b_x10(self):
        self.send_cmd("10X")
        self.btn_aa.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_bb.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_cc.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_dd.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")

    def send_b_x100(self):
        self.send_cmd("100X")
        self.btn_aa.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_bb.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_cc.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_dd.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")

    def send_b_x1000(self):
        self.send_cmd("1000X")
        self.btn_aa.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_bb.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_cc.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_dd.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")




    def set_background(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(
            QPalette.Window,
            QBrush(pixmap.scaled(self.size(),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)))
        self.setPalette(palette)



####################################################################
        # Button 0.01 sec
        self.btn_a = QPushButton("1μs", self)
        self.btn_a.setGeometry(72, 150, 102, 40)
        self.btn_a.setFlat(True)
        self.btn_a.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        # CONNECT BUTTON
        self.btn_a.clicked.connect(self.send_S1)

        # Button 0.1 sec
        self.btn_b = QPushButton("10μs", self)
        self.btn_b.setGeometry(188, 150,102, 40)
        self.btn_b.setFlat(True)
        self.btn_b.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_b.clicked.connect(self.send_S2)

        # Button 1 sec
        self.btn_c = QPushButton("100μs", self)
        self.btn_c.setGeometry(301, 150, 102, 40)
        self.btn_c.setFlat(True)
        self.btn_c.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_c.clicked.connect(self.send_S3)

        # Button 10 sec
        self.btn_d = QPushButton("1ms", self)
        self.btn_d.setGeometry(72, 202, 102, 40)
        self.btn_d.setFlat(True)
        self.btn_d.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_d.clicked.connect(self.send_S4)

        # Button 100 sec
        self.btn_e = QPushButton("10ms", self)
        self.btn_e.setGeometry(188, 202, 102, 40)
        self.btn_e.setFlat(True)
        self.btn_e.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_e.clicked.connect(self.send_S5)

        # Button 1000 sec
        self.btn_f = QPushButton("100ms", self)
        self.btn_f.setGeometry(301 , 202, 102, 40)
        self.btn_f.setFlat(True)
        self.btn_f.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_f.clicked.connect(self.send_S6)


#################################################
        # Button 1x
        self.btn_aa = QPushButton("1X", self)
        self.btn_aa.setGeometry(72, 303, 102, 40)
        self.btn_aa.setFlat(True)
        self.btn_aa.setStyleSheet("""QPushButton {color: red;font-size: 22px;font-weight: bold;}""")
        self.btn_aa.clicked.connect(self.send_b_x1)

        # Button 10x
        self.btn_bb = QPushButton("10X", self)
        self.btn_bb.setGeometry(188, 303, 102, 40)
        self.btn_bb.setFlat(True)
        self.btn_bb.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_bb.clicked.connect(self.send_b_x10)

        # Button 100x
        self.btn_cc = QPushButton("100X", self)
        self.btn_cc.setGeometry(300, 303, 102, 40)
        self.btn_cc.setFlat(True)
        self.btn_cc.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_cc.clicked.connect(self.send_b_x100)

        # Button 1000x
        self.btn_dd = QPushButton("1000X", self)
        self.btn_dd.setGeometry(412, 303, 102, 40)
        self.btn_dd.setFlat(True)
        self.btn_dd.setStyleSheet("""QPushButton {color: black;font-size: 22px;font-weight: bold;}""")
        self.btn_dd.clicked.connect(self.send_b_x1000)


        # Simple Label OffSet
        self.label1 = QLabel("1.650 V", self)
        self.label1.setGeometry(260, 400, 440, 50)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("""QLabel {color: #b4f5fc; font-size: 30px; font-weight: bold;}""")


        # Simple Label OffSet
        self.label_pmt = QLabel("0.0 V", self)
        self.label_pmt.setGeometry(690, 344, 440, 50)
        self.label_pmt.setAlignment(Qt.AlignCenter)
        self.label_pmt.setStyleSheet("""QLabel {color: #b4f5fc; font-size: 40px; font-weight: bold;}""")


        # Simple Label OffSet
        self.label_HV_l = QLabel("0.0 V", self)
        self.label_HV_l.setGeometry(690, 176, 440, 50)
        self.label_HV_l.setAlignment(Qt.AlignCenter)
        self.label_HV_l.setStyleSheet("""QLabel {color: #b4f5fc; font-size: 40px; font-weight: bold;}""")


        # Slider Offset
        self.slider1 = QSlider(Qt.Horizontal, self)
        self.slider1.setRange(0, 3300)
        self.slider1.setGeometry(135, 446, 160, 40)
        self.slider1.setValue(1650)
        self.slider1.setTickInterval(150)
        self.slider1.setTickPosition(QSlider.TicksBelow)
        # Update voltage display
        self.slider1.valueChanged.connect(self.update_voltage)


        # 🎨 Dark theme slider style
        self.slider1.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #2e2e2e;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #2196F3;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #2e2e2e;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #212121;
                border: 2px solid #2196F3;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #bbdefb;
            }
            QSlider::handle:horizontal:pressed {
                background: #90caf9;
            }""")


        # Button - Offset
        self.btn_c1 = QPushButton(" ", self)
        self.btn_c1.setGeometry(68, 440, 55, 45)
        self.btn_c1.clicked.connect(self.decrease_offset)
        self.btn_c1.setFlat(True)
        self.btn_c1.setStyleSheet("""QPushButton {color: black;font-size: 25px;font-weight: bold;}""")


        # Button + Offset
        self.btn_d1 = QPushButton(" ", self)
        self.btn_d1.setGeometry(305, 440, 55, 45)
        self.btn_d1.clicked.connect(self.increase_offset)
        self.btn_d1.setFlat(True)
        self.btn_d1.setStyleSheet(""" QPushButton {color: black; font-size: 25px; font-weight: bold;}""")


        # Simple Label High Voltage
        self.label2 = QLabel("0.000 V", self)
        self.label2.setGeometry(380, 527, 190, 30)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet(""" QLabel { color: #b4f5fc; font-size: 30px;font-weight: bold;}""")


        # Slider for High Voltage
        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setRange(0, 5000)
        self.slider2.setGeometry(135, 560, 160, 40)
        self.slider2.setTickInterval(0)


        self.slider2.setTickPosition(QSlider.TicksBelow)
        # Update voltage display
        self.slider2.valueChanged.connect(self.update_voltage_hv)
        # 🎨 Dark theme slider style
        self.slider2.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #2e2e2e;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #2196F3;
                border-radius: 4px;
            }
            QSlider::add-page:horizontal {
                background: #2e2e2e;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #212121;
                border: 2px solid #2196F3;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #bbdefb;
            }
            QSlider::handle:horizontal:pressed {
                background: #90caf9;
            }
        """)


        # Button - High Voltage
        self.btn_h1 = QPushButton(" ", self)
        self.btn_h1.setGeometry(68, 554, 55, 45)  # x, y, width, height
        self.btn_h1.clicked.connect(self.decrease_high_v)
        self.btn_h1.setFlat(True)
        self.btn_h1.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #2196F3;
            }
            QPushButton:pressed {
                color: #90caf9;
            }
        """)


        # Button + High Voltage
        self.btn_h2 = QPushButton(" ", self)
        self.btn_h2.setGeometry(305, 555, 55, 45)  # x, y, width, height
        self.btn_h2.clicked.connect(self.increase_high_v)
        self.btn_h2.setFlat(True)
        self.btn_h2.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #2196F3;
            }
            QPushButton:pressed {
                color: #90caf9;
            }
        """)

        self.condis_icon_size = QSize(400, 360)
        self.start_btn1 = QPushButton(self)
        self.start_btn1.setIcon(QIcon("Images/startb.png"))
        self.start_btn1.setIconSize(self.condis_icon_size)
        self.start_btn1.setGeometry(300, 615, 220, 200)
        self.start_btn1.setStyleSheet("border: none;")
        self.start_btn1.clicked.connect(self.toggle_start_stop)

        self.startstop_icon_size = QSize(420, 380)
        self.start_btn11 = QPushButton(self)
        self.start_btn11.setIcon(QIcon("Images/Connectb.png"))
        self.start_btn11.setIconSize(self.startstop_icon_size)
        self.start_btn11.setGeometry(50, 615, 220, 200)
        self.start_btn11.setStyleSheet("border: none;")
        self.start_btn11.clicked.connect(self.toggle_connect_disconnect)
        self.is_running = False


    def toggle_connect_disconnect(self):
        try:
            if not self.ser or not self.ser.is_open:
                return

            if not self.is_connected:
                # Connect
                self.is_connected = True
                self.start_btn11.setIcon(QIcon("Images/DisconnectB.png"))
                self.startstop_icon_size = QSize(400, 360)
                self.start_btn11.repaint()
                self.send_cmd("CONNECT")
            else:
                # Disconnect
                self.is_connected = False
                #self.start_btn11.setIcon(QIcon("Images/Connectb.png"))
                #self.startstop_icon_size = QSize(400, 360)
                #self.start_btn11.repaint()
                self.send_cmd("DISCONNECT")
                QtWidgets.QApplication.quit()  # optional if you want to quit app
        except:
            pass




    def toggle_start_stop(self):
        try:
            if not self.ser or not self.ser.is_open or not self.is_connected:
                # Optional: show message "Connect device first"
                return
            if not self.is_running:
                # Start
                self.is_running = True
                self.start_btn1.setIcon(QIcon("Images/Stopb.png"))
                self.start_btn1.setIconSize(self.condis_icon_size)
                self.start_btn1.repaint()
                self.send_cmd("ON")
                self.start_rx_thread()
            else:
                # Stop
                self.is_running = False
                self.start_btn1.setIcon(QIcon("Images/startB.png"))
                self.start_btn1.setIconSize(self.condis_icon_size)
                self.start_btn1.repaint()
                self.send_cmd("OFF")
                self.stop_rx_thread()
        except:
            pass



        

    def stop_rx_thread(self):
        try:
            self.rx_running = False
            if hasattr(self, "rx_thread"):
                self.rx_thread.quit()
                self.rx_thread.wait()
        except:
            pass

    def closeEvent(self, event):
        self.rx_running = False
        if self.ser and self.ser.is_open:
            self.send_cmd("DISCONNECT")
            self.ser.close()
        event.accept()

    def update_voltage(self, value):
        try:
            voltage = value / 1000.0
            self.label1.setText(f"{voltage:.3f} V")
            self.send_cmd(f"SETV{value}")
        except:
            pass

    def update_voltage_hv(self, value):
        try:
            self.voltage = value / 1000.0
            self.label2.setText(f"{self.voltage:.3f} V")
            self.send_cmd(f"HV{value}")
        except:
            pass


    # offset Slider Increase
    def increase_offset(self):
        try:
            """+ Button → increase voltage"""
            step = 150
            new_value = self.slider1.value() + step
            if new_value <= 3300:
                self.slider1.setValue(new_value)
        except:
            pass


    # offset Slider Decrease
    def decrease_offset(self):
        try:
            """- Button → decrease voltage"""
            step = 150
            new_value = self.slider1.value() - step
            if new_value >= 0:
                self.slider1.setValue(new_value)
        except:
            pass


    # high Voltage Slider Increase
    def increase_high_v(self):
        try:
            """+ Button → increase voltage """
            step = 500
            new_value = self.slider2.value() + step
            if new_value <= 5000:
                self.slider2.setValue(new_value)
        except:
            pass


    # high Voltage Slider Decrease
    def decrease_high_v(self):
        try:

            """ Button → decrease voltage """
            step = 500
            new_value = self.slider2.value() - step
            if new_value >= 0:
                self.slider2.setValue(new_value)
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    page = MAINCODEPMT()
    page.show()
    sys.exit(app.exec_())

