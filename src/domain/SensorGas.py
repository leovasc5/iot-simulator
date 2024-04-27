import random
from datetime import datetime
from .ModeloSensor import ModeloSensor

class SensorGas(ModeloSensor):
    def __init__(self, id, nome, nome_bruto, fabricante, funcionalidade, tipo, unidade_medida, min_val, max_val, regular_min_val, regular_max_val, is_anomalia):
        super().__init__(id, nome, nome_bruto, fabricante, funcionalidade, tipo, unidade_medida, min_val, max_val, regular_min_val, regular_max_val, is_anomalia)

    def sortear_anomalia(self):
        return random.random() < 0.001

    def simular_dado(self, ultima_ocorrencia=None):
        if self.is_anomalia and self.sortear_anomalia():
            return self.set_range_limite(random.uniform(0, 0.5))

        if ultima_ocorrencia:
            if 10 <= int(datetime.now().strftime('%H')) <= 13 or 17 <= int(datetime.now().strftime('%H')) <= 20:
                return self.set_range_limite(random.uniform(float(self.regular_min), float(self.regular_max)) + 0.5)
            else:
                return self.set_range_limite(ultima_ocorrencia + random.uniform(-0.1, 0.1))
        else:
            if 10 <= int(datetime.now().strftime('%H')) <= 13 or 17 <= int(datetime.now().strftime('%H')) <= 20:
                return self.set_range_limite(random.uniform(float(self.regular_min), float(self.regular_max)) + random.uniform(0.5, 1.5))
            else:
                return self.set_range_limite(random.uniform(float(self.regular_min), float(self.regular_max)))
