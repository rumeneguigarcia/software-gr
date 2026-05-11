from abc import ABC, abstractmethod
from exceptions import DatosInvalidadosError, ReservaInvalidaError
import logging

class EntidadBase(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad # Atributo protegido

    @abstractmethod
    def obtener_detalles(self):
        pass

class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, email):
        super().__init__(id_cliente)
        self.__nombre = nombre  # Encapsulamiento (Privado)
        self.__email = email
        self._validar_datos()

    def _validar_datos(self):
        if not self.__nombre or "@" not in self.__email:
            raise DatosInvalidadosError(f"Datos de cliente inválidos: '{self.__nombre}'")

    def obtener_detalles(self):
        return f"Cliente: {self.__nombre} (ID: {self._id_entidad})"

class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        try:
            if self.duracion <= 0:
                raise ReservaInvalidaError("La duración debe ser mayor a cero.")
            
            costo = self.servicio.calcular_costo(cantidad=self.duracion)
            self.estado = "Confirmada"
            print(f"✅ Reserva {self.id_reserva} EXITOSA. Total: ${costo}")
            logging.info(f"Reserva {self.id_reserva} confirmada para {self.cliente.obtener_detalles()}")
            
        except ReservaInvalidaError as e:
            self.estado = "Fallida"
            logging.error(f"Error en Reserva {self.id_reserva}: {e}")
            raise  # Re-lanzar para el bloque superior
        finally:
            print(f"   [Sistema]: Finalizando procesamiento de Reserva {self.id_reserva}.")
