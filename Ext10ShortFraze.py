# Задание №10. Необходимо написать тест, который просит ввести в консоли любую фразу короче 15 символов. А затем с помощью assert проверяет, что фраза действительно короче 15 символов.
class Test_ShortPhrase:
    def test_short_fraze(self):
        self.phrase = input("Введите любую фразу короче 15 символов: ")
        length_of_phrase = len(self.phrase)
        assert len(
            self.phrase) < 15, f"Вы ввели слишком длинную фразу, размер которой превышает целевое значение на {length_of_phrase - 15} шт."
        print(f"Вы успешно ввели фразу: '{self.phrase}' длиной {length_of_phrase} символов")