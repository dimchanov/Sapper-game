Взаимодействие с пользователем происходит посредством командной строки, состояние поля после каждого шага отображается в консоли, пользователь делает ход с помощью команд троек X,Y,Action, где X и Y — координаты клетки на поле, а Action – действие, которое необходимо совершить: Flag — установить флажок на соответвующую клетку, пометив её как предположительно содержащую бомбу; Open – раскрыть содержимое клетки. 

Сохранение состояния поля выполняется автоматически в файл auto_save.txt, пользователь может выполнить сохранение в собственный файл с помощью команды пары Save Filename.txt . Загрузка сохранения выполняется в начале игры с помощью команды пары Load Filename.txt