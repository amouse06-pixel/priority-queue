class PriorityQueue:  # объявляем класс

    def __init__(self):  # создаем кучи
        self.heap = []  # создаем пустой список для кучи, элементы вида (priority, value) хранятся как кортежи

    def enqueue(self, value, priority):  # добавляем элемент
        self.heap.append((priority, value))  # кладем новый элемент в конец списка
        self._sift_up(len(self.heap) - 1)  # поднмаем элемент наверх, пока он не встанет на правильное место

    def dequeue(self):  # достаем главный элемент
        if self.is_empty():
            raise IndexError(
                "удаление из пустой кучи")  # поднимаем ошибку, если пытаться удалить элемент из пустой кучи
        top = self.heap[0]  # это корень с минимаьным приоритетом
        last = self.heap.pop()  # убираем последний элемент списка
        if self.heap:  # проверяем, остались ли еще элементы
            self.heap[0] = last  # ставим бывший последний элемент на место корня
            self._sift_down(0)  # опускает его вниз, пока порядок не станет верным
        return top[1]  # возвращает значение, а не весь кортеж

    def peek(self):  # проверяем пустоту и возвращаем значение корня без удаления
        if self.is_empty():
            raise IndexError("пустая очередь")  # если пустая
        return self.heap[0][1]  # если не пустая, то возвращаем количество элементов

    def is_empty(self):  # проверяем пустоту
        return len(self.heap) == 0  # True, если пустая

    def size(self):  # возвращаем количество элементов
        return len(self.heap)

    def _sift_up(self, i):  # подъем элемента вверх после вставки
        while i > 0:  # считаем, чтобы перестать, когда дойдем до корня
            parent = (i - 1) // 2  # находим родителя
            if self.heap[i][0] < self.heap[parent][
                0]:  # сравниваем приоритеты элемента и родителя, елси элемент меньше родителя, то порядок нарушен
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[
                    i]  # если порядок нарушен, то меняем их местами
                i = parent  # переходим на уровень выше и проверяем все то же самое снова
            else:
                break  # если порядок правильный, то выходим из цикла и переходим на следующий элемент

    def _sift_down(self, i):  # проделываем спуск вниз после удаления
        n = len(self.heap)  # узнаем размер кучи
        while True:  # повторяем, пока элемент не займет место
            left = 2 * i + 1  # индекс детей
            right = 2 * i + 2  # индекс детей
            smallest = i  # предполагаем, что текущий элемент минимальный из троих(он сам и два ребенка)
            if left < n and self.heap[left][0] < self.heap[smallest][
                0]:  # проверяем, что ребенок существует(<n) и что его приоритет меньше текущего минимума
                smallest = left  # если да, то запоминаем индекс
            if right < n and self.heap[right][0] < self.heap[smallest][0]:  # то же самое
                smallest = right
            if smallest == i:  # если оба ребенка меньше, значит, куча корректна
                break
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[
                i]  # иначе меняем элемент с меньшим ребенком местами и продолжаем с i = smallest
            i = smallest


# Тесты, каждый из них создает новую пустую очередь q = PriorityQueue(), чтобы тесты не влияли друг на друга
def test_empty():  # пустота новой очереди
    q = PriorityQueue()  # создаем новую пустую очередь
    assert q.is_empty()  # проверяем, что is_empty() вернул True
    assert q.size() == 0  # проверяем, что размер равен 0


def test_enqueue_and_size():  # проверка, что добавление меняет состояние
    q = PriorityQueue()  # создаем новую пустую очередь
    q.enqueue("a", 3)  # добавлем элемент а с приоритетом 3
    q.enqueue("b", 1)  # добавляем элемент b с приоритетом 1
    assert not q.is_empty()  # проверяем, что очередь не пустая
    assert q.size() == 2  # проверяем, что размер равен именно 2


def test_peek():  # проверка просмотра без удаления
    q = PriorityQueue()  # создаем новую пустую очередь
    q.enqueue("low", 10)  # добавляем элемент low с приоритетом 10
    q.enqueue("high", 1)  # добавляем элемент high с приоритетом 1
    q.enqueue("mid", 5)  # добавляем элемент mid с приоритетом 5
    assert q.peek() == "high"  # проверяем, что элемент с первым приоритетом поднялся наверх, несмотря на то, что был добавлен вторым
    assert q.size() == 3  # проверяем, что peek не удаляет элемент, то есть размер остался 3


def test_dequeue_order(): # тест корректности
    q = PriorityQueue() # создаем новую пустую очередь
    q.enqueue("c", 3) # добавляем элементы в рандомном, не отсортированном порядке
    q.enqueue("a", 1)
    q.enqueue("e", 5)
    q.enqueue("b", 2)
    q.enqueue("d", 4)
    result = [q.dequeue() for _ in range(5)] # 5 раз достаем главный элемент и собираем их в список
    assert result == ["a", "b", "c", "d", "e"] # проверем, что порядок выхода соответствует возрастанию приоритета
    assert q.is_empty() # проверяем, что после 5 удалений очередь пуста


def test_same_priorities(): # элементы с одинаковыми приоритетами
    q = PriorityQueue() # создаем новую пустую очередь
    q.enqueue("x", 2) # добавляем три разных элемента с одинаковыми приоритетами
    q.enqueue("y", 2)
    q.enqueue("z", 2)
    assert sorted([q.dequeue() for _ in range(3)]) == ["x", "y", "z"] # проверяем, что при запросе элементов полученной очереди выходят все три элемента


def test_negative_and_zero_priorities():# проверяем, что значения приоритетов могут быть нулем или отрицательными числами
    q = PriorityQueue() # создаем новую пустую очередь
    q.enqueue("zero", 0) # добавляем элементы, среди которых - с нулевым и отрицательным приоритетом
    q.enqueue("neg", -5)
    q.enqueue("pos", 7)
    assert q.dequeue() == "neg" # должен выйти 1
    assert q.dequeue() == "zero" # должен выйти 2
    assert q.dequeue() == "pos" # должен выйти 3



def test_empty_errors(): # ошибки с пустой очередью
    q = PriorityQueue() # создаем новую пустую очередь
    for action in (q.dequeue, q.peek): # пытаемся достать элемент из пустой очереди
        try:
            action() # поочередно вызываем методы у пустой очереди, ожидается получить IndexError
            assert False, "ожидалась IndexError" # если не получили ошибку на этапе предыдущей строки, то выводится сообщение об ошибке
        except IndexError: # если поднимается ошибка IndexError, то все хорошо
            pass


if __name__ == "__main__":
    test_empty()
    test_enqueue_and_size()
    test_peek()
    test_dequeue_order()
    test_same_priorities()
    test_negative_and_zero_priorities()
    test_empty_errors()
    print("Все тесты пройдены")
