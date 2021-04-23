Skrypt generuje kod LaTeXa do wykresów, lecz nie może być więcej niż 12 problemów.
Nie obsługuje także dużych odchyleń wyników, przez co może się zdarzyć sytuacja, że LaTeX nas opluje, że za duża/mała wartość, albo brzydko ustawi ymin i ymax.
W takich wypadkach najprościej ręcznie zmienić ymin oraz ymax, a jak nadal nie pomoże to wywalić te odstające wartości z kodu LaTeXa.

Skrypt jest w pythonie 3.9 (chyba wystarczy >=3.6, ale nie jestem pewien, 3.8 na pewno starczy) - potrzebna biblioteka: pandas.

CSV musi posiadać kolumny:
-problem
-method
-gens
-...
    tutaj kolumny takie jak FFE, time itp. tych wartości, którch chce się pokazać na wykresch - wystarczy jedna
-...

Z jednego CSV generowana jest jedna figura LaTeXowa dla podanej kolumny miary,
jeden problem -> jedna subfigura,
jedna metoda -> jeden rodzaj linii na wykresie (unikalne połączenie koloru i markera) == jeden plot w subfigurze

dlatego pilnuj, żeby nie duplikować danych pochodzących z tego samego badania

Uruchomienie skryptu:

python <nazwa skryptu> <nazwa csv> <nazwa kolumny, np FFE> <nazwa figury w raporcie/caption> <label do referencji w LaTeXu, np. fig:myPlot>

<label> jest opcjonalnym argumentem, nie trzeba go wpisywać

kod wyjściowy LaTeXa zostanie zapisany w pliku a.txt, więc trzeba przypilnować, żeby przypadkiem nie zostało coś ważnego nadpisane.

