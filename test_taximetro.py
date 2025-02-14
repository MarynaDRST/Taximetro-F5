import unittest
import time
from datetime import datetime
from taximetro import Taximetro
from PyQt5.QtWidgets import QApplication
import os


class TestTaximetro(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Inicializa la aplicación Qt antes de todas las pruebas."""
        cls.app = QApplication([])

    def setUp(self):
        """Inicializa el taxímetro antes de cada prueba."""
        self.taximetro = Taximetro()
        self.taximetro.en_prueba = True  # Включаем режим тестирования

    def test_iniciar_trayecto(self):
        """Prueba que el trayecto se inicie correctamente."""
        self.taximetro.iniciar_trayecto()
        self.assertIsNotNone(self.taximetro.tiempo_inicio)
        self.assertEqual(self.taximetro.estado, "parado")
        self.assertEqual(self.taximetro.total, 0)  
        self.assertEqual(self.taximetro.label_total.text(), "0.00 €")
        self.assertEqual(self.taximetro.label_estado.text(), "Estado: Parado")

    def test_cambiar_estado(self):
        """Prueba que el estado del taxímetro cambie correctamente."""
        self.taximetro.iniciar_trayecto()
        self.taximetro.cambiar_estado("moviendo")
        self.assertEqual(self.taximetro.estado, "moviendo")
        self.assertEqual(self.taximetro.label_estado.text(), "Estado: Moviendo")

        self.taximetro.cambiar_estado("parado")
        self.assertEqual(self.taximetro.estado, "parado")
        self.assertEqual(self.taximetro.label_estado.text(), "Estado: Parado")

    def test_actualizar_costo(self):
        """Prueba que el costo se actualice correctamente."""
        self.taximetro.en_prueba = False  # Отключаем режим тестирования для этого теста
        self.taximetro.iniciar_trayecto()
        self.taximetro.cambiar_estado("moviendo")
        time.sleep(1) 
        self.taximetro.actualizar_costo()
        self.assertGreater(self.taximetro.total, 0)

    def test_finalizar_trayecto(self):
        """Prueba que el trayecto se finalice correctamente."""
        self.taximetro.iniciar_trayecto()
        self.taximetro.cambiar_estado("moviendo")
        time.sleep(1) 
        self.taximetro.finalizar_trayecto()
        self.assertIsNone(self.taximetro.tiempo_inicio)
        self.assertEqual(self.taximetro.estado, "parado")
        self.assertEqual(self.taximetro.total, 0)
        self.assertEqual(self.taximetro.label_total.text(), "0.00 €")
        self.assertEqual(self.taximetro.label_estado.text(), "Estado: Parado")

    def test_actualizar_tarifas(self):
        """Prueba que las tarifas se actualicen correctamente."""
        self.taximetro.input_tarifa_parado.setText("0.03")
        self.taximetro.input_tarifa_movimiento.setText("0.06")
        self.taximetro.actualizar_tarifas()
        self.assertEqual(self.taximetro.tarifa_parado, 0.03)
        self.assertEqual(self.taximetro.tarifa_movimiento, 0.06)

    def test_guardar_historial(self):
        """Prueba que el historial se guarde correctamente."""
        self.taximetro.iniciar_trayecto()
        self.taximetro.cambiar_estado("moviendo")
        time.sleep(1)
        end_datetime = datetime.now()
        self.taximetro.guardar_historial(end_datetime)

        # Verificamos que el archivo de historial existe y contiene la información correcta
        self.assertTrue(os.path.exists(self.taximetro.history_file))
        with open(self.taximetro.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("=== Registro de Trayecto ===", content)
            self.assertIn("Total:", content)

    def test_ver_historial(self):
        """Prueba que la ventana de historial se muestre correctamente."""
        self.taximetro.ver_historial()
        self.assertTrue(self.taximetro.history_window.isVisible())

    def tearDown(self):
        """Limpia después de cada prueba."""
        if os.path.exists(self.taximetro.history_file):
            os.remove(self.taximetro.history_file)

if __name__ == "__main__":
    unittest.main()