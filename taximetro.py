import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, 
    QPushButton, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt
import logging

# Настройка логирования
logging.basicConfig(
    filename="taxi_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class Taximetro(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка интерфейса
        self.setWindowTitle("Taxímetro digital *** Factoria F5")
        self.setGeometry(300, 300, 600, 400)

        self.setStyleSheet("background-color: #FFFFFF;")

        # Создаем главный горизонтальный контейнер
        main_layout = QHBoxLayout()

        # Создаем вертикальный контейнер для логотипа
        logo_layout = QVBoxLayout()
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(image_label, 0, Qt.AlignVCenter)
        # Загружаем и устанавливаем логотип
        try:
            pixmap = QPixmap("taxi.jpeg")
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    400, 300,  # Размер логотипа
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
                
            else:
                print("Не удалось загрузить изображение.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")

        logo_layout.addWidget(image_label)

        # Создаем вертикальный контейнер для кнопок
        buttons_layout = QVBoxLayout()

        # Метка состояния
        self.label_estado = QLabel("Estado: Parado")
        self.label_estado.setStyleSheet("font-size: 16px;")
        buttons_layout.addWidget(self.label_estado)

        # Метка стоимости
        self.label_total = QLabel("Total: 0.00 €")
        self.label_total.setStyleSheet("font-size: 18px;")
        buttons_layout.addWidget(self.label_total)

        # Кнопки
        buttons = [
            ("Iniciar Trayecto", self.iniciar_trayecto),
            ("Mover", lambda: self.cambiar_estado("moviendo")),
            ("Parar", lambda: self.cambiar_estado("parado")),
            ("Finalizar Trayecto", self.finalizar_trayecto)
        ]

        for text, handler in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            buttons_layout.addWidget(btn)

        # Добавляем вертикальные layouts в главный горизонтальный layout
        main_layout.addLayout(logo_layout)
        main_layout.addLayout(buttons_layout)

        # Настройка центрального виджета
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Инициализация переменных для таймера и состояния
        self.tarifa_parado = 0.02
        self.tarifa_movimiento = 0.05
        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = None

        # Таймер для расчета стоимости
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_costo)

    def iniciar_trayecto(self):
        #Начало нового маршрута.

        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = time.time()
        self.timer.start(1000)  # Запускаем таймер с интервалом в 1 сек
        self.label_estado.setText("Estado: Parado")
        self.label_total.setText("Total: 0.00 €")
        logging.info("🚖 Nuevo trayecto iniciado.")
        QMessageBox.information(self, "Inicio", "¡Trayecto iniciado!")


    def cambiar_estado(self, nuevo_estado):
        """
        Изменение состояния (движется или стоит).
        """
        if self.tiempo_inicio is None:
            QMessageBox.warning(self, "Advertencia", "Primero inicie un trayecto.")
            return

        self.estado = nuevo_estado
        self.label_estado.setText(f"Estado: {'Moviendo' if nuevo_estado == 'moviendo' else 'Parado'}")

        # Логирование
        if nuevo_estado == "moviendo":
            logging.info("El taxi ha comenzado a moverse.")
        elif nuevo_estado == "parado":
            logging.info("El taxi se ha detenido.")

    def finalizar_trayecto(self):
        """
        Завершение маршрута.
        """
        if self.tiempo_inicio is None:
            QMessageBox.warning(self, "Advertencia", "Primero inicie un trayecto.")
            return

        self.timer.stop()
        QMessageBox.information(self, "Fin", f"Trayecto finalizado. Total a pagar: {self.total:.2f} €")
        logging.info(f"Trayecto finalizado. Total: {self.total:.2f} €")
        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = None
        self.label_estado.setText("Estado: Parado")
        self.label_total.setText("Total: 0.00 €")

    def actualizar_costo(self):
        """
        Обновление стоимости в реальном времени.
        """
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio

        if self.estado == "parado":
            self.total += self.tarifa_parado
        elif self.estado == "moviendo":
            self.total += self.tarifa_movimiento

        self.label_total.setText(f"Total: {self.total:.2f} €")
        self.tiempo_inicio = tiempo_actual

def main():
    app = QApplication(sys.argv)
    taximetro = Taximetro()
    taximetro.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()