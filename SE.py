import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

def motor_inferencia(sintomas_paciente):
    # Convertir síntomas a minúsculas
    sintomas_paciente = set(sintoma.lower() for sintoma in sintomas_paciente)

    # Definir la Base de Conocimiento para síntomas médicos y enfermedades
    reglas_medicas = [
        (3, {'fiebre', 'dolor de cabeza'}, 'Gripe'),
        (6, {'tos', 'dificultad para respirar'}, 'Bronquitis'),
        (7, {'fiebre', 'dolor de garganta'}, 'Amigdalitis'),
        (2, {'dolor de cabeza', 'cansancio'}, 'Migraña'),
        (5, {'escalofríos', 'fatiga', 'fiebre'}, 'Influenza'),
        (9, {'dolor abdominal', 'náuseas'}, 'Gastritis'),
        (8, {'dolor en el pecho', 'falta de aire'}, 'Ataque al Corazón'),
        (1, {'dolor en las articulaciones', 'fatiga'}, 'Artritis')
    ]

    # Inicializar enfermedades inferidas
    enfermedades_inferidas = []

    # Procesar reglas de acuerdo a la prioridad
    for prioridad, sintomas, enfermedad in sorted(reglas_medicas, key=lambda x: x[0]):
        if sintomas.issubset(sintomas_paciente):
            return f"Posible enfermedad: {enfermedad}"

    # Si ninguna regla se activa, devolver None
    return "No se pudo determinar la enfermedad"

# Interfaz gráfica
class SistemaExpertoGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Experto Médico")

        self.label = QLabel("¿El paciente tiene el siguiente síntoma?")
        self.result_label = QLabel("")
        self.button_yes = QPushButton("Sí")
        self.button_no = QPushButton("No")

        self.button_yes.clicked.connect(self.respuesta_si)
        self.button_no.clicked.connect(self.respuesta_no)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.button_yes)
        layout.addWidget(self.button_no)

        self.setLayout(layout)
        self.preguntas = iter([
            'fiebre', 'dolor de cabeza', 'tos', 'dificultad para respirar',
            'dolor de garganta', 'dolor de cabeza', 'cansancio',
            'escalofríos', 'fatiga', 'fiebre', 'dolor abdominal', 'náuseas',
            'dolor en el pecho', 'falta de aire', 'dolor en las articulaciones', 'fatiga'
        ])
        self.sintomas_paciente = set()

    def mostrar_pregunta(self, pregunta):
        self.label.setText(f"¿El paciente tiene {pregunta}?")

    def respuesta_si(self):
        try:
            sintoma = next(self.preguntas)
            self.mostrar_pregunta(sintoma)
            self.sintomas_paciente.add(sintoma)
        except StopIteration:
            resultado = motor_inferencia(self.sintomas_paciente)
            self.result_label.setText(resultado)

    def respuesta_no(self):
        try:
            _ = next(self.preguntas)  # Descartar la pregunta actual
            sintoma = next(self.preguntas)
            self.mostrar_pregunta(sintoma)
        except StopIteration:
            resultado = motor_inferencia(self.sintomas_paciente)
            self.result_label.setText(resultado)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SistemaExpertoGUI()
    ventana.mostrar_pregunta(next(ventana.preguntas))  # Mostrar la primera pregunta
    ventana.show()
    sys.exit(app.exec_())