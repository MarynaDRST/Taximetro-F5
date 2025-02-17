### 🚖 **TAXÍMETRO Digital**  

Esta aplicación está desarrollada con **PyQt5** y está diseñada para simular el funcionamiento de un **taxímetro**. Permite calcular el costo del viaje según el tiempo de espera y el tiempo en movimiento, además de guardar el historial de trayectos.

---

## 📋 **Funcionalidades:**  
- **Configuración de tarifas:** Posibilidad de modificar las tarifas por tiempo detenido y tiempo en movimiento.  
- **Estado actual:** Muestra el estado actual: **"Parado"** o **"Moviendo"**.  
- **Cálculo del costo:** Cálculo automático del costo del trayecto en tiempo real.  
- **Historial de trayectos:** Guarda y muestra el historial de todos los trayectos.  
- **Interfaz moderna:** Basada en PyQt5 con un diseño funcional.  

---

## ✅ **Checklist de funcionalidades implementadas:**  

### 🟢 **Nivel Básico**  
- [x] **Iniciar un trayecto.**  
- [x] **Calcular tarifa mientras el taxi está parado** (2 céntimos por segundo).  
- [x] **Calcular tarifa mientras el taxi está en movimiento** (5 céntimos por segundo).  
- [x] **Finalizar un trayecto y mostrar el total en euros.**  
- [x] **Permitir iniciar un nuevo trayecto sin cerrar el programa.**  

### 🟡 **Nivel Medio**  
- [x] **Implementar un sistema de logs** para la trazabilidad del código.  
- [x] **Agregar tests unitarios** para asegurar el correcto funcionamiento del programa.  
- [x] **Crear un registro histórico de trayectos** pasados en un archivo de texto plano.  
- [x] **Permitir la configuración de precios** para adaptarse a la demanda actual.  

### 🟠 **Nivel Avanzado**  
- [x] **Refactorizar el código utilizando un enfoque orientado a objetos (OOP).**  
- [ ] **Implementar un sistema de autenticación con contraseñas** para proteger el acceso al programa.  
- [x] **Desarrollar una interfaz gráfica de usuario (GUI)** para hacer el programa más amigable.  

### 🔴 **Nivel Experto**  
- [ ] **Integrar una base de datos** para almacenar los registros de trayectos pasados.  
- [ ] **Dockerizar la aplicación** para facilitar su despliegue y portabilidad.  
- [ ] **Desarrollar una versión web** de la aplicación accesible a través de internet.  

---

## 🖥️ **Requisitos:**  
Antes de ejecutar la aplicación, asegúrate de tener instaladas las siguientes dependencias:  
- Python 3.11.9  
- PyQt5  

---

## 🚀 **Instalación y ejecución:**  
1. **Clona el repositorio:**  
```sh
git clone https://github.com/MarynaDRST/Taximetro-F5.git
cd taximetro
```
2. **Ejecuta la aplicación:**  
```sh
python taximetro.py
```

---

## 📚 **Estructura del proyecto:**  
```plaintext
taximetro/
│
├── taximetro.py               
├── widgets.py  
├── test_taximetro.py          
├── taxi_history.txt         
└── README.md  
```

---

## 🧩 **Componentes principales:**  
- **TAXIMETRO:** Clase principal que hereda de `QMainWindow`.  
- **Tarifas:** Entrada de tarifas para estados de "Parado" y "Moviendo".  
- **Botones de control:**  
  - **Iniciar:** Inicia un trayecto.  
  - **Mover:** Cambia el estado a "Moviendo".  
  - **Parar:** Cambia el estado a "Parado".  
  - **Finalizar:** Finaliza el trayecto y guarda el historial.  
  - **Historial:** Muestra el historial de trayectos.  
- **Historial:** Guarda la información de los trayectos en `taxi_history.txt`.

---

## ⚙️ **Métodos principales:**  
- `iniciar_trayecto()` – Inicia un trayecto y arranca el temporizador.  
- `cambiar_estado(nuevo_estado)` – Cambia el estado a "moviendo" o "parado".  
- `finalizar_trayecto()` – Detiene el temporizador y guarda el historial.  
- `actualizar_costo()` – Actualiza el costo según el estado actual.  
- `actualizar_tarifas()` – Actualiza las tarifas según los datos ingresados.  
- `ver_historial()` – Abre una ventana con el historial de trayectos.  
- `guardar_historial(end_datetime)` – Guarda la información del trayecto en un archivo.  

---

## 🔧 **Configuración de tarifas:**  
- **Tarifa auto parado (€/segundo)** – Costo cuando el vehículo está detenido.  
- **Tarifa auto en movimiento (€/segundo)** – Costo cuando el vehículo está en movimiento.  
- Los valores se pueden cambiar en la interfaz o directamente en el código:  
```python
self.tarifa_parado = 0.02
self.tarifa_movimiento = 0.05
```

---

## 🎨 **Características de la interfaz:**  
- Diseño moderno usando **QFrame** para tarjetas informativas.  
- **QVBoxLayout** y **QHBoxLayout** para una distribución flexible.  
- Uso de **QPixmap** para íconos.  

---

## 📜 **Historial de trayectos:**  
El historial se guarda en el archivo `taxi_history.txt` y contiene:  
- Fecha del trayecto.  
- Hora de inicio y fin.  
- Duración del trayecto.  
- Costo total.  

---

## 🚧 **Mejoras potenciales:**  
  
- Implementar soporte para múltiples zonas tarifarias.  
- Localización y soporte multilingüe.  
- Implementar un sistema de autenticación con contraseña.
- Integrar una base de datos.
- Dockerizar la aplicación.
- Desarrollar una versión web.  



