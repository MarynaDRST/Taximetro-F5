import sys
import time
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, 
    QPushButton, QWidget, QMessageBox, QScrollArea, QTextEdit, QLineEdit, QFormLayout,
    QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import QTimer, Qt
import logging

class ModernButton(QPushButton):
    def __init__(self, text, icon_path=None, color="#FFFFFF"):
        super().__init__()
        self.setText(text)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-size: 14px;
                min-width: 100px;
                min-height: 80px;
            }}
            QPushButton:hover {{
                background-color: {color.replace(')', ', 0.8)')};
            }}
        """)
        self.setLayout(QVBoxLayout())

class Taximetro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Taxímetro digital")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #F3F4F6;")

        # Главный контейнер
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Секция тарифов
        rates_frame = QFrame()
        rates_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        rates_layout = QVBoxLayout()
        
        # Заголовок секции тарифов
        rates_title = QLabel("Tarifa actual")
        rates_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        rates_title.setAlignment(Qt.AlignCenter)  # Выровнено по центру
        rates_layout.addWidget(rates_title)

        # Контейнер для полей ввода
        inputs_layout = QHBoxLayout()
        
        # Поле для тарифа в состоянии покоя
        standing_rate_layout = QVBoxLayout()
        standing_rate_label = QLabel("Tarifa en reposo (€/segundo)")
        standing_rate_label.setStyleSheet("color: #666;")
        self.input_tarifa_parado = QLineEdit("0,02")
        self.input_tarifa_parado.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background: white;
            }
        """)
        standing_rate_layout.addWidget(standing_rate_label)
        standing_rate_layout.addWidget(self.input_tarifa_parado)
        
        # Поле для тарифа в движении
        moving_rate_layout = QVBoxLayout()
        moving_rate_label = QLabel("Tarifa en movimiento (€/segundo)")
        moving_rate_label.setStyleSheet("color: #666;")
        self.input_tarifa_movimiento = QLineEdit("0,05")
        self.input_tarifa_movimiento.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background: white;
            }
        """)
        moving_rate_layout.addWidget(moving_rate_label)
        moving_rate_layout.addWidget(self.input_tarifa_movimiento)

        inputs_layout.addLayout(standing_rate_layout)
        inputs_layout.addLayout(moving_rate_layout)
        rates_layout.addLayout(inputs_layout)

        # Кнопка обновления тарифов
        self.btn_actualizar_tarifa = QPushButton("Actualizar Tarifa")
        self.btn_actualizar_tarifa.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        rates_layout.addWidget(self.btn_actualizar_tarifa)
        rates_frame.setLayout(rates_layout)
        main_layout.addWidget(rates_frame)

        # Информационная панель
        info_layout = QHBoxLayout()
        
        # Статус
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
        """)
        status_layout = QVBoxLayout()
        
        # Иконка такси
        taxi_icon = QLabel()
        taxi_icon.setPixmap(QPixmap("taxi.jpeg").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        taxi_icon.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(taxi_icon)
        
        self.label_estado = QLabel("Estado: Parado")
        self.label_estado.setAlignment(Qt.AlignCenter)
        self.label_estado.setStyleSheet("font-size: 18px; font-weight: bold;")
        status_layout.addWidget(self.label_estado)
        status_frame.setLayout(status_layout)
        info_layout.addWidget(status_frame)

        # Сумма
        total_frame = QFrame()
        total_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
        """)
        total_layout = QVBoxLayout()
        
        total_label = QLabel("Total")
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        total_layout.addWidget(total_label)
        
        self.label_total = QLabel("0.00 €")
        self.label_total.setAlignment(Qt.AlignCenter)
        self.label_total.setStyleSheet("font-size: 36px; font-weight: bold; color: #10B981;")
        total_layout.addWidget(self.label_total)
        
        total_frame.setLayout(total_layout)
        info_layout.addWidget(total_frame, stretch=2)
        main_layout.addLayout(info_layout)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        button_configs = [
            ("Iniciar", "play.png", "#10B981", self.iniciar_trayecto),
            ("Mover", "car.png", "#3B82F6", lambda: self.cambiar_estado("moviendo")),
            ("Parar", "pause.png", "#F59E0B", lambda: self.cambiar_estado("parado")),
            ("Finalizar", "stop.png", "#EF4444", self.finalizar_trayecto),
            ("Historial", "clock.png", "#6B7280", self.ver_historial)
        ]

        for text, icon, color, handler in button_configs:
            btn = ModernButton(text, icon, color)
            btn.clicked.connect(handler)
            buttons_layout.addWidget(btn)

        main_layout.addLayout(buttons_layout)

        # Инициализация остальных компонентов
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_costo)
        self.tarifa_parado = 0.02
        self.tarifa_movimiento = 0.05
        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = None
        self.history_file = "taxi_history.txt"
        self.start_datetime = None

        # Подключаем обработчик обновления тарифов
        self.btn_actualizar_tarifa.clicked.connect(self.actualizar_tarifas)

        # Отступы
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

    # Остальные методы остаются без изменений
    def iniciar_trayecto(self):
        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = time.time()
        self.start_datetime = datetime.now()
        self.timer.start(1000)
        self.label_estado.setText("Estado: Parado")
        self.label_total.setText("0.00 €")
        logging.info("Nuevo trayecto iniciado.")
        QMessageBox.information(self, "Inicio", "¡Trayecto iniciado!")

    def cambiar_estado(self, nuevo_estado):
        if self.tiempo_inicio is None:
            QMessageBox.warning(self, "Advertencia", "Primero inicie un trayecto.")
            return

        self.estado = nuevo_estado
        self.label_estado.setText(f"Estado: {'Moviendo' if nuevo_estado == 'moviendo' else 'Parado'}")

        if nuevo_estado == "moviendo":
            logging.info("El taxi ha comenzado a moverse.")
        elif nuevo_estado == "parado":
            logging.info("El taxi se ha detenido.")

    def finalizar_trayecto(self):
        if self.tiempo_inicio is None:
            QMessageBox.warning(self, "Advertencia", "Primero inicie un trayecto.")
            return

        self.timer.stop()
        end_datetime = datetime.now()
        self.guardar_historial(end_datetime)
        QMessageBox.information(self, "Fin", f"Trayecto finalizado. Total a pagar: {self.total:.2f} €")
        logging.info(f"Trayecto finalizado. Total: {self.total:.2f} €")
        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = None
        self.start_datetime = None
        self.label_estado.setText("Estado: Parado")
        self.label_total.setText("0.00 €")

    def actualizar_costo(self):
        tiempo_actual = time.time()
        if self.estado == "parado":
            self.total += self.tarifa_parado
        elif self.estado == "moviendo":
            self.total += self.tarifa_movimiento
        self.label_total.setText(f"{self.total:.2f} €")
        self.tiempo_inicio = tiempo_actual

    def actualizar_tarifas(self):
        try:
            self.tarifa_parado = float(self.input_tarifa_parado.text().replace(',', '.'))
            self.tarifa_movimiento = float(self.input_tarifa_movimiento.text().replace(',', '.'))
            QMessageBox.information(self, "Éxito", "Las tarifas han sido actualizadas.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese valores numéricos válidos.")
    
    def ver_historial(self):
        """Показывает окно с историей поездок"""
        
        try:
            # Создаем новое окно для истории
            self.history_window = QWidget()
            self.history_window.setWindowTitle("Historial de Trayectos")
            self.history_window.setGeometry(900, 400, 500, 400)

            # Создаем вертикальный layout
            layout = QVBoxLayout()

            # Создаем область прокрутки
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            
            # Создаем текстовое поле для отображения истории
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)

            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history_text = f.read()
                    if not history_text.strip():
                        text_edit.setText("No hay trayectos registrados.")
                    else:
                        text_edit.setText(history_text)
            except FileNotFoundError:
                text_edit.setText("No hay historial de trayectos disponible.")

            scroll.setWidget(text_edit)
            layout.addWidget(scroll)

            # Добавляем кнопку закрытия
            close_button = QPushButton("Cerrar")
            close_button.clicked.connect(self.history_window.close)
            layout.addWidget(close_button)

            self.history_window.setLayout(layout)
            self.history_window.show()

        except Exception as e:
            logging.error(f"Error al mostrar el historial: {e}")
            QMessageBox.warning(self, "Error", "No se pudo mostrar el historial de trayectos.")
        
    def guardar_historial(self, end_datetime):
        """Сохраняет информацию о поездке в файл истории"""
        try:
            duration = end_datetime - self.start_datetime
            with open(self.history_file, 'a', encoding='utf-8') as f:
                    f.write(f"""
=== Registro de Trayecto ===
Fecha: {self.start_datetime.strftime('%Y-%m-%d')}
Hora inicio: {self.start_datetime.strftime('%H:%M:%S')}
Hora fin: {end_datetime.strftime('%H:%M:%S')}
Duración: {str(duration).split('.')[0]}
Total: {self.total:.2f} €
========================
""")

            logging.info("Historial guardado correctamente")
        except Exception as e:
            logging.error(f"Error al guardar el historial: {e}")
            QMessageBox.warning(self, "Error", "No se pudo guardar el historial del trayecto.")


def main():
    app = QApplication(sys.argv)
    taximetro = Taximetro()
    taximetro.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()