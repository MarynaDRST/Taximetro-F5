import sys
import time
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, 
    QPushButton, QWidget, QMessageBox, QScrollArea, QTextEdit
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
        self.setGeometry(400, 400, 500, 400)

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
                    150, 150,  # Размер логотипа
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
            ("Finalizar Trayecto", self.finalizar_trayecto),
            ("Ver Historial", self.ver_historial)  # Новая кнопка
        ]

        for text, handler in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            buttons_layout.addWidget(btn)
        
              
        # Добавляем вертикальные layouts в главный горизонтальный layout
        main_layout.addLayout(logo_layout)
        main_layout.addLayout(buttons_layout)

        # Устанавливаем пропорции между логотипом и кнопками
        main_layout.setStretch(0, 1)  # Логотип занимает 2 части
        main_layout.setStretch(1, 4)  # Кнопки занимают 1 часть

        # Настройка центрального виджета
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # После создания main_layout добавьте:
        main_layout.setSpacing(10)  # Расстояние между логотипом и кнопками
        buttons_layout.setSpacing(10)  # Расстояние между кнопками

            # Добавим отступы по краям
        central_widget.setContentsMargins(20, 20, 20, 20)


        # Инициализация переменных для таймера и состояния
        self.tarifa_parado = 0.02
        self.tarifa_movimiento = 0.05
        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = None

        # Добавляем атрибут для файла истории
        self.history_file = "taxi_history.txt"
        self.start_datetime = None

        # Таймер для расчета стоимости
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_costo)

    def iniciar_trayecto(self):
        #Начало нового маршрута.

        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = time.time()
        self.start_datetime = datetime.now()  # Сохраняем дату и время начала
        self.timer.start(1000)  # Запускаем таймер с интервалом в 1 сек
        self.label_estado.setText("Estado: Parado")
        self.label_total.setText("Total: 0.00 €")
        logging.info("Nuevo trayecto iniciado.")
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
        end_datetime = datetime.now()

        # Сохраняем историю поездки
        self.guardar_historial(end_datetime)

        QMessageBox.information(self, "Fin", f"Trayecto finalizado. Total a pagar: {self.total:.2f} €")
        logging.info(f"Trayecto finalizado. Total: {self.total:.2f} €")
        self.total = 0
        self.estado = "parado"
        self.tiempo_inicio = None
        self.start_datetime = None
        self.label_estado.setText("Estado: Parado")
        self.label_total.setText("Total: 0.00 €")
    
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