class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Длина шага
    M_IN_KM: float = 1000  # Константа для перевода расстояния
    workout_type: str = ''  # Константа для типа тренировки

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance: float = 0
        self.mean_speed: float = 0
        self.spent_calories: float = 0

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = (self.action
                         * self.LEN_STEP / self.M_IN_KM)  # Расчет расстояния
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = (self.get_distance()
                           / self.duration)  # Расчет средней скорости
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.workout_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )
        return info


class Running(Training):
    """Тренировка: бег."""
    coeff_cal_1: float = 18
    coeff_cal_2: float = 20
    workout_type: str = 'Running'  # Константа для типа тренировки

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.coeff_cal_1
                               * self.get_mean_speed()
                               - self.coeff_cal_2)
                               * self.weight
                               / self.M_IN_KM
                               * self.duration
                               * 60.0)
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_cal_1: float = 0.035
    coeff_cal_2: float = 0.029
    workout_type: str = 'SportsWalking'  # Константа для типа тренировки

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.coeff_cal_1
                                * self.weight
                                + (self.get_mean_speed() ** 2
                                   // self.height)
                                * self.coeff_cal_2
                                * self.weight)
                               * self.duration * 60)
        return self.spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_cal_1: float = 1.1
    coeff_cal_2: float = 2
    workout_type: str = 'Swimming'  # Константа для типа тренировки

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.mean_speed = (self.length_pool
                           * self.count_pool
                           / self.M_IN_KM
                           / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.get_mean_speed()
                                + self.coeff_cal_1)
                               * self.coeff_cal_2
                               * self.weight)
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    tr_sl = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    tren = tr_sl[workout_type](*data)
    return tren


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
